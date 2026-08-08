# Questions for Con Edison — SolarScan Verify

Team: Yongpeng, Praewa, Kenji, Tanapat, Victor
Brief: Solar Scanner Optimization
Purpose: Brief clinic, Session 5. Prepared before the session.

---

## Q1 · Current decision and evidence available

> When the current scanner flags a rooftop as ambiguous, what does the human
> reviewer actually do today — what evidence do they pull, and how long does
> the review take per rooftop? What is the current error rate on complex
> rooftops, and do you have labeled ground-truth examples of the scanner's
> mistakes that we could use (publicly or under an approved arrangement) to
> benchmark a verification layer?

**Why we ask:** Our proposal only helps if the ambiguous cases are worth the
effort. This question tells us the size of the problem (how many roofs, how
much human time), what the review process looks like today, and whether any
labeled data exists to measure against. It also tells us where our
verification layer would sit in the existing workflow — before, after, or
instead of part of the human review.

## Q2 · Costly errors

> Which error has historically been more costly — a false "solar" (sending a
> team to verify a roof that has no panels) or a false "no solar" (missing
> real generation potential)? Is there a public or anonymized dataset of past
> scan results and outcomes we could use to benchmark our prototype?

**Why we ask:** A verification system cannot optimize for everything at once;
it has to know which mistake hurts more. The answer decides the design: if
false "solar" is the expensive error, the system should bias toward
"uncertain" and escalate; if false "no solar" is worse, it should bias toward
flagging anything remotely panel-like. The dataset question tells us whether
our §6 benchmark (100 images, 90% clear-case accuracy, escalation recall
1.0) can use real scan history or must be built from public/synthetic
imagery.

## Q3 · Data limits and integration

> For the contextual signals we want to combine — building footprints, permit
> records, historical rooftop imagery, roof geometry — which are available to
> us as public or shareable data, and which are restricted? Are there
> constraints on how verification results should be returned to your system
> (format, API, or review tooling)?

**Why we ask:** The PRD's multimodal design depends on which context signals
actually exist and can be used. If permit records are restricted, the
verification layer must work from imagery plus public footprints; if
historical imagery exists, the change-detection feature is viable. The
integration question tells us whether the prototype should produce a
standalone report or match a specific interface Con Edison already uses.
