#!/usr/bin/env python3
"""SolarScan Verify — live demo server (local only, no keys in repo).

Run locally for the Session 6 demo:
    export GEMINI_API_KEY="$(cat ~/.gemini_api_key)"
    export OPENROUTER_API_KEY="$(cat ~/.openrouter_api_key)"
    python3 scripts/demo_server.py            # serves on http://127.0.0.1:8765

Endpoints:
    GET  /                       -> demo UI (presentation/demo.html)
    POST /api/analyze_image      -> multipart: file=<roof image>
    POST /api/analyze_address    -> JSON: {"address": "511 W 182nd St"}

Design: 4 models in parallel (same prompt, temp 0) -> decision rule
(agree & conf >= .6 accept; else escalate) -> optional NYC permit
cross-check by address -> human-readable verdict + recommendation.

SECURITY: reads keys from env only. Never commit keys.
"""
import base64
import io
import json
import math
import os
import re
import sys
import threading
import time
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PORT = int(os.environ.get("DEMO_PORT", "8765"))

MODELS = [
    {"id": "gemini-3.5-flash-lite", "provider": "gemini", "label": "Gemini 3.5 Flash-Lite", "color": "purple"},
    {"id": "openrouter:openai/gpt-5.5", "provider": "openrouter", "label": "GPT-5.5", "color": "blue"},
    {"id": "openrouter:moonshotai/kimi-k3", "provider": "openrouter", "label": "Kimi K3 (open)", "color": "green"},
    {"id": "openrouter:google/gemma-4-26b-a4b-it", "provider": "openrouter", "label": "Gemma 4-26B (open)", "color": "amber"},
]

SYSTEM_PROMPT = (
    "You are a rooftop solar verification agent for a utility company. "
    "Classify whether the roof in the image has solar panels. "
    "Reply with JSON ONLY: "
    '{"label": "solar" | "no_solar" | "uncertain", "confidence": 0.0, '
    '"reason": "one short sentence"}. '
    "If the image is not a rooftop or is unusable, reply "
    '{"label": "uncertain", "confidence": 0.1, "reason": "image not usable"}.'
)

UA = {"User-Agent": "solarscan-verify-demo"}


def env_key(name):
    v = os.environ.get(name)
    if v:
        return v.strip()
    f = Path.home() / f".{name.lower()}"
    return f.read_text().strip() if f.exists() else ""


def ask_model(model, image_bytes):
    """Call one model; returns {label, confidence, reason}."""
    b64 = base64.b64encode(image_bytes).decode()
    if model["provider"] == "gemini":
        key = env_key("GEMINI_API_KEY")
        url = (f"https://generativelanguage.googleapis.com/v1beta/models/"
               f"{model['id']}:generateContent?key={key}")
        payload = {
            "contents": [{"parts": [
                {"text": SYSTEM_PROMPT},
                {"inline_data": {"mime_type": "image/jpeg", "data": b64}},
            ]}],
            "generationConfig": {"temperature": 0},
        }
        req = urllib.request.Request(url, data=json.dumps(payload).encode(),
                                     headers={"Content-Type": "application/json"})
    else:
        key = env_key("OPENROUTER_API_KEY")
        slug = model["id"].split(":", 1)[1]
        url = "https://openrouter.ai/api/v1/chat/completions"
        payload = {
            "model": slug,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": [
                    {"type": "text", "text": "Classify this rooftop image."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}},
                ]},
            ],
            "temperature": 0,
        }
        req = urllib.request.Request(url, data=json.dumps(payload).encode(),
                                     headers={"Content-Type": "application/json",
                                              "Authorization": f"Bearer {key}"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                data = json.loads(r.read())
            text = data["candidates"][0]["content"]["parts"][0]["text"] \
                if model["provider"] == "gemini" else data["choices"][0]["message"]["content"]
            m = re.search(r"\{.*\}", text, re.S)
            if m:
                out = json.loads(m.group(0))
                return {"label": out.get("label", "uncertain"),
                        "confidence": float(out.get("confidence", 0)),
                        "reason": str(out.get("reason", ""))[:140]}
            return {"label": "uncertain", "confidence": 0.1, "reason": "unparseable output"}
        except Exception as e:
            if attempt == 2:
                return {"label": "uncertain", "confidence": 0.1,
                        "reason": f"API error: {type(e).__name__}"}
            time.sleep(2 * (attempt + 1))


def geocode(address):
    """NYC Geosearch -> {lat, lon, bbl, label} or None."""
    url = ("https://geosearch.planninglabs.nyc/v2/search?" +
           urllib.parse.urlencode({"text": address, "size": "1"}))
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=25) as r:
            g = json.loads(r.read())
        f = (g.get("features") or [None])[0]
        if not f:
            return None
        props = f["properties"]
        lon, lat = f["geometry"]["coordinates"]
        return {"lat": lat, "lon": lon,
                "bbl": props.get("addendum", {}).get("pad", {}).get("bbl"),
                "label": props.get("label", address)}
    except Exception:
        return None


def fetch_ortho_tile(lat, lon, z=19):
    """Download a NYC Orthos 2024 tile for a lat/lon."""
    n = 2 ** z
    x = int((lon + 180.0) / 360.0 * n)
    lat_rad = math.radians(lat)
    y = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
    url = ("https://tiles.arcgis.com/tiles/yG5s3afENB5iO9fj/arcgis/rest/"
           f"services/NYC_Orthos_2024/MapServer/tile/{z}/{y}/{x}")
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=30) as r:
            data = r.read()
        return data if data[:3] == b"\xff\xd8\xff" else None
    except Exception:
        return None


def check_permit(address):
    """LL24 solar permit lookup by address (public data).

    LL24 stores addresses like '511 West 182nd St'; geosearch labels are
    like '511 WEST 182 STREET'. Normalize both sides before matching so
    '182nd' is preserved and street-suffix spellings align.
    """
    def norm(a):
        s = a.upper()
        s = re.sub(r"\bSTREET\b", "ST", s)
        s = re.sub(r"\bAVE\b|\bAVENUE\b", "AVE", s)
        s = re.sub(r"\bW\b|\bWEST\b", "W", s)
        s = re.sub(r"\bE\b|\bEAST\b", "E", s)
        s = re.sub(r"\bN\b|\bNORTH\b", "N", s)
        s = re.sub(r"\bS\b|\bSOUTH\b", "S", s)
        s = re.sub(r"\s+", " ", s).strip()
        return s

    naddr = norm(address)
    # street number is the anchor: filter server-side to candidates
    mnum = re.search(r"(\d+)\s+([A-Z0-9 ]+)", naddr)
    if mnum:
        num = mnum.group(1)
        where = (f"status = 'Completed' and "
                 f"address like '{num}%'")
    else:
        where = "status = 'Completed'"
    params = {"$where": where, "$limit": "200",
              "$select": "address,status,installation_date"}
    url = ("https://data.cityofnewyork.us/resource/cfz5-6fvh.json?"
           + urllib.parse.urlencode(params))
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=25) as r:
            rows = json.loads(r.read())
        # match by normalized address token set
        key_tokens = set(re.findall(r"[a-z0-9]+", naddr))
        best = []
        for row in rows:
            row_tokens = set(re.findall(r"[a-z0-9]+", norm(row.get("address", ""))))
            # require the street number + at least 2 more tokens in common
            if key_tokens and row_tokens and len(key_tokens & row_tokens) >= max(2, len(key_tokens) - 1):
                best.append(row)
        return best[:3]
    except Exception:
        return []


def decide(results):
    """Decision rule (PRD §5): agree & conf>=.6 accept; else escalate."""
    labels = [r["label"] for r in results if r.get("label")]
    if not labels:
        return {"action": "ESCALATE", "reason": "no usable model output"}
    top = max(set(labels), key=labels.count)
    agree = labels.count(top)
    avg_conf = sum(r["confidence"] for r in results) / len(results)
    if agree >= 3 and avg_conf >= 0.6:
        return {"action": "ACCEPT", "verdict": top,
                "reason": f"{agree}/4 models agree at avg conf {avg_conf:.2f}"}
    return {"action": "ESCALATE", "verdict": None,
            "reason": f"models split ({agree}/4 agree) or low confidence ({avg_conf:.2f})"}


def recommend(decision, permit_rows, verdict=None):
    """Human-readable recommendation for the demo UI."""
    lines = []
    if permit_rows:
        d = permit_rows[0].get("installation_date", "")[:10]
        lines.append(f"📋 Public record: solar permit **Completed {d}** found for this address.")
    if decision["action"] == "ACCEPT":
        if verdict == "solar":
            lines.append(f"✅ **Accept: this roof has solar panels.** ({decision['reason']})")
            if permit_rows:
                lines.append("The permit record agrees — high confidence.")
            else:
                lines.append("No permit on file — consider a quick record check.")
        else:
            lines.append(f"✅ **Accept: no solar panels on this roof.** ({decision['reason']})")
            if permit_rows:
                lines.append("⚠️ BUT a permit exists — conflict! Send this to a human reviewer.")
            else:
                lines.append("No permit on file — consistent.")
    else:
        lines.append(f"⚠️ **Escalate to a human reviewer.** ({decision['reason']})")
        if permit_rows:
            lines.append("A permit record exists — the reviewer should weigh both signals.")
        else:
            lines.append("No permit on file — the reviewer judges from imagery alone.")
    return " ".join(lines)


def analyze(image_bytes, address=None):
    """Run the full pipeline: 4 models -> decision -> permit cross-check."""
    results = []
    threads = []
    lock = threading.Lock()
    for model in MODELS:
        def run(m=model):
            r = ask_model(m, image_bytes) or {}
            r["model"] = m["label"]
            r["color"] = m["color"]
            with lock:
                results.append(r)
        t = threading.Thread(target=run)
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    decision = decide(results)
    permit_rows = check_permit(address) if address else []
    if address and permit_rows and decision["action"] == "ACCEPT" and decision["verdict"] == "no_solar":
        decision = {"action": "ESCALATE", "verdict": None,
                    "reason": "permit conflict: Completed permit vs model 'no_solar'"}
    rec = recommend(decision, permit_rows, decision.get("verdict"))
    return {"results": results, "decision": decision, "permit": permit_rows,
            "recommendation": rec, "address": address}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _send(self, code, body, ctype="application/json"):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            f = REPO / "presentation/demo.html"
            if f.exists():
                self._send(200, f.read_bytes(), "text/html; charset=utf-8")
            else:
                self._send(404, b"demo.html not found", "text/plain")
        else:
            self._send(404, b"not found", "text/plain")

    def do_POST(self):
        if self.path == "/api/analyze_image":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            # multipart parse (single file)
            boundary = None
            ct = self.headers.get("Content-Type", "")
            m = re.search(r"boundary=([^;]+)", ct)
            if m:
                boundary = m.group(1).encode()
            image_bytes = None
            if boundary and body.startswith(b"--" + boundary):
                parts = body.split(b"--" + boundary)
                for part in parts:
                    if b"filename=" in part and b"\r\n\r\n" in part:
                        image_bytes = part.split(b"\r\n\r\n", 1)[1].rsplit(b"\r\n", 1)[0]
                        break
            if not image_bytes or len(image_bytes) < 100:
                self._send(400, json.dumps({"error": "no usable image"}).encode())
                return
            out = analyze(image_bytes)
            self._send(200, json.dumps(out).encode())
        elif self.path == "/api/analyze_address":
            length = int(self.headers.get("Content-Length", 0))
            try:
                data = json.loads(self.rfile.read(length))
                address = str(data.get("address", "")).strip()
            except Exception:
                self._send(400, json.dumps({"error": "bad json"}).encode())
                return
            if not address:
                self._send(400, json.dumps({"error": "address required"}).encode())
                return
            geo = geocode(address)
            if not geo:
                self._send(404, json.dumps({"error": "address not found",
                                            "hint": "try a NYC address like 511 W 182nd St"}).encode())
                return
            tile = fetch_ortho_tile(geo["lat"], geo["lon"])
            if not tile:
                self._send(502, json.dumps({"error": "imagery fetch failed"}).encode())
                return
            out = analyze(tile, address=geo["label"])
            out["geo"] = geo
            self._send(200, json.dumps(out).encode())
        else:
            self._send(404, json.dumps({"error": "not found"}).encode())


if __name__ == "__main__":
    gkey = "yes" if env_key("GEMINI_API_KEY") else "MISSING"
    okey = "yes" if env_key("OPENROUTER_API_KEY") else "MISSING"
    print(f"SolarScan Verify demo server on http://127.0.0.1:{PORT}")
    print(f"  GEMINI_API_KEY: {gkey}  OPENROUTER_API_KEY: {okey}")
    if gkey == "MISSING" or okey == "MISSING":
        print("  (missing keys — set env vars from ~/.gemini_api_key / ~/.openrouter_api_key)")
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
