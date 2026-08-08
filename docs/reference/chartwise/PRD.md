# ChartWise: The Average Trap — Project 2 PRD (reference)

> Reference document from Yongpeng's Project 2 (Design a Sim). Kept here as a
> model of PRD structure and AI-evidence documentation for SolarScan Verify.
> Source: `li_ChartWise_PRD.pdf` (5 pages), AI outputs and OpenRouter logs
> preserved in `AI_Outputs/` and `AI_Logs/`.

Business Visualization Decision Simulator ChartWise Yongpeng Li
 
What it teaches 
After this run, a player can recognize when averaging a dataset hides the business insight that the audience actually needs, and defend a visualization that preserves meaningful variation.
I would know it worked if, during the debrief, a player says that the cleanest-looking chart was not necessarily the most informative one because averaging removed the difference between low-end and premium ticket prices.
Overview 
ChartWise: The Average Trap is a 15-minute business data visualization sim designed to help business students and early-career professionals practice visualization judgment rather than chart-building mechanics. In this run, players act as junior business analysts preparing an executive presentation about World Cup ticket pricing and compare two plausible ways to summarize the same data: one chart uses a single average price per city, while the other preserves each city's minimum-to-maximum price range. The team must send one recommendation to management and defend what information the visualization preserves or removes.
Goals 
- Make the information lost through averaging visible. 
- Create genuine disagreement between simplicity and completeness. 
- Make players connect the visualization choice to the manager's actual question. 
- End with one visualization recommendation the team is willing to defend. 
Non-Goals 
- Teaching Excel, Python, R, Tableau, or chart-building mechanics. 
- Teaching every major chart type or advanced statistics. 
- Running a multi-round multiple-choice quiz. 
- Producing one universally “correct” visualization. 
 
 

Audience 
ChartWise is designed for undergraduate business, economics, and analytics students as well as early-career professionals who already recognize common chart types but want to improve their visualization judgment in realistic business situations. Teams of three to five are preferred. Players do not calculate statistics or build charts; every number and visual they need is already on screen, so the difficulty stays centered on deciding what information a business audience actually needs to see.
Existing solutions and issues Traditional visualization lecture Students can memorize rules such as “bar for comparison” and “line for time,” but those rules do not resolve situations in which two technically valid visualizations communicate different information.
Spreadsheet exercise 
Building charts can shift attention toward formulas, formatting, labels, and software mechanics. The judgment itself becomes secondary.
Asking generative AI 
A student could ask, “What chart should I use to compare World Cup ticket prices across cities?” A model may reasonably recommend a bar chart, but that does not settle what the bars should represent: an average, a minimum, a maximum, or the full range. ChartWise:
The Average Trap makes that second-level decision the task. 
Assumptions 
- Players will often prefer a visually cleaner chart when both options appear reasonable. 
- Players may initially treat an average as automatically representative. 
- Requiring one defended recommendation will make players focus on information loss rather than chart-name recall. 
- Students can discuss the visualization effectively without constructing it themselves. 
Constraints 
- Runs in a browser with no install beyond icerynk. 
- 15 minutes including debrief; teams of three to five. 
- All evidence for the decision fits on one screen; no arithmetic is required from players. 
- The displayed dataset is simplified for teaching purposes. 
- Buildable by a small team in about two weeks. 
Key use cases 
- Understand the manager's request within 90 seconds. 
- Compare two plausible visualizations built from the same underlying data. 
- Identify what information each visualization preserves or removes. 
- Debate the trade-off between simplicity and completeness. 
- Submit one visualization recommendation and defend the decision. 
The card 
Field 
Entry 
Title 
ChartWise 
Subtitle 
The Average Trap — Your manager wants one chart for the executive meeting. Decide what the chart can afford to hide.
Summary 
ChartWise is a business data visualization sim that helps business students and early-career professionals practice visualization judgment in realistic workplace situations. In The Average Trap, the room receives the same World Cup ticket-pricing data presented through two plausible visualizations:
an average-price chart and a minimum-to-maximum range chart. The team must decide which visualization to send to management and defend what information it preserves.
Learning objective 
Recognize when averaging hides the business insight the audience needs, and defend a visualization that preserves meaningful variation.
Duration 
13-15 minutes 
Team size 
3-5; solo possible but not preferred Result One defended visualization Tags Data judgment; visual communication; business analysis; audience awareness Cover image alt text A team of business analysts comparing two ticket-price charts on a large screen before an executive presentation.
 

The run 
Beat 
Minutes 
What the room sees 
What the room does 
1 · The Request 
3 
Manager message + simplified city ticket-price data Identify what management is actually asking to understand 2 · The Choice 6 Average-price chart and min-to-max range chart Compare what each chart preserves or hides; debate one recommendation 3 · The Decision 3 Final submission screen Choose one recommendation and submit a one-sentence justification
 
Beat 1 · The Request 
Tomorrow's executive meeting includes a short discussion of World Cup ticket pricing. I want one chart that shows where the gap between affordable and premium ticket options is largest across host cities. Keep it simple enough for one presentation slide.
City 
Minimum Price 
Maximum Price 
City A 
$120 
$480 
City B 
$180 
$390 
City C 
$100 
$650 
City D 
$240 
$510 
City E 
$150 
$420 
 
The figures are illustrative rather than official ticket prices. The sim does not highlight the phrase “gap between affordable and premium ticket options”; the room has to identify it.
Beat 2 · The Choice 
Option A is a clean ranked bar chart with one average ticket price per city. Option B is a range chart that preserves the low and high ticket prices for each city. Both are plausible; the room must decide which one better serves the manager's question.
Beat 3 · The Decision The team submits exactly one recommendation and a one-sentence justification: send the average chart, send the range chart, or refuse both and request a revised visualization.
The limit 
One submission. Once the recommendation is sent, the team cannot change it. 
The tempting wrong move Choose the average-price chart because it is cleaner and more executive-friendly. That chart is useful for a different question - which cities are generally more expensive - but it removes the exact min-to-max gap the manager asked to compare.
The endings 
- Send the Average - prioritize simplicity; debrief asks what became easier and what disappeared. 
- Preserve the Range - prioritize variation; debrief asks whether the added complexity was justified. 
- Refuse Both - request a revised chart; debrief asks what the replacement must preserve. 
Research 
Domain research 
WHEN CAN AN AVERAGE HIDE THE BUSINESS INSIGHT? 
An average is useful when the business question concerns overall level or a typical value. It becomes less useful when the question concerns variation, range, extremes, or the gap between low and high values. Here, the manager explicitly wants the affordable-to- premium gap, so showing only an average removes both endpoints needed to answer the question.
WHY IS WORLD CUP TICKET PRICING A GOOD CASE? 
Ticket pricing naturally offers several valid summaries for the same city: low-end price, premium price, category prices, average price, and price range. That makes it possible to present two reasonable-looking charts without making one of them obviously wrong.
Model research 
WHAT DOES A BARE MODEL PRODUCE? 
I tested the following bare prompt in OpenRouter using Claude Opus 5 (model ID: anthropic/claude-opus-5) on August 3, 2026: 
Design a 15-minute simulation that teaches business students how to choose the right data visualization. 
The model produced “Chart Triage at Northwind Beverages,” a fast simulation with five executives, five chart-selection rounds, a scoring system, a chart-family lookup rule, a misleading-chart twist, headline writing, and a debrief. The complete unedited response is included in AI_Outputs/Output1_Claude_Raw_Response.txt and the original OpenRouter text log.

Part 7 · Why this beats just asking AI The bare prompt Design a 15-minute simulation that teaches business students how to choose the right data visualization.
What it produced 
The model created a rapid chart-triage exercise in which five executives each request a different chart. Students are first given a rule that maps the verb in a business question to a chart family, then earn points for choosing the expected chart type and writing a “so- what” headline. The raw output is included unchanged in AI_Outputs/Output1_Claude_Raw_Response.txt.
Where it fell short 
The model's line 
What is wrong with it How I know “Five executives are messaging you at once, each wanting one chart.” Creates five separate decisions instead of one shared decision.
The course template requires one decision and three beats.
“Underline the verb in the request. The verb picks the chart.” Gives the decision rule before students exercise judgment; later rounds become recall.
In my visualization work, the harder issue is what information to preserve, not simply bar vs. line.
Five rounds + headlines + lie factor + misleading axes + scoring + correlation warnings Attempts to teach several capabilities in 15 minutes.
The course template requires one thing to learn. 
 
What I supplied that it could not I supplied a specific decision from my own visualization work: when comparing World Cup ticket prices across host cities, an average can produce a clean chart while hiding the gap between low-end and premium tickets. This changed the sim from “Which chart family matches this question?” to “What information can this visualization afford to hide?” The correction log The model proposed I changed it to Why Five visualization-selection rounds One ticket-pricing decision Keep the sim centered on one judgment Five unrelated executive requests One manager request Create one shared question for the room to debate Chart-family lookup framework Two plausible charts from the same data Create disagreement instead of recall Correct/incorrect scoring Three defensible endings Preserve judgment and ambiguity Many visualization concepts One idea: averages can hide meaningful variation Fit the 15-minute scope
 
The test a reader can run Give a general-purpose AI model the same ticket-price data and ask two questions: (A) “Which cities have the highest typical ticket prices?” and (B) “Which cities have the widest gap between affordable and premium ticket options?” Then ask whether those questions should necessarily use the same visualization. If the model recommends different treatments, that confirms the sim's central point: the business question changes what information a chart must preserve. If it recommends the same treatment without addressing the difference, the gap in the default answer is visible immediately.
Part 8 · Generative AI outputs Field Output 1 Output 2 What it is Initial simulation concept Cover image for ChartWise: The Average Trap Modality Text Image Exact model ID anthropic/claude-opus-5 recraft/recraft-v4.1-pro-vector Date generated August 3, 2026 August 3, 2026 Prompt used Bare prompt shown above Exact first and revision prompts reproduced below and preserved in the image log What I rejected first Five-round quiz structure, lookup rule, and excessive concepts The charts were not visually distinct enough; the “average” chart looked stacked, the range chart was ambiguous, and several labels were unreadable.
What I edited afterwards Reduced to one decision, three beats, and one learning objective Changed the left visual to one solid average bar per city and the right visual to a true min-to-max range; simplified labels and composition.
 
Output 2 · Exact prompt used First generation:
Create a 16:9 landscape cover image for a business analytics classroom simulation called “The Average Trap.” Show a small team of junior business analysts in a modern meeting room preparing for an executive presentation. A large screen should be the main visual focus. On the screen, show two contrasting data visualization concepts side by side: on the left, a simple bar chart with one average ticket price per city; on the right, a minimum-to-maximum range chart showing low and high ticket prices for each city. The analysts should appear to be discussing which visualization is more useful. Clean professional business-school aesthetic, polished editorial illustration, modern but realistic, minimal clutter, clear data visualization elements, suitable as a course simulation cover image. No brand logos, no FIFA logo, no stock-market screens, no futuristic holograms, no excessive text.
Revision: 

Revise the cover image for “The Average Trap.” Keep the same professional business-school illustration style and 16:9 layout. 
Make the large presentation screen the main visual focus. On the left, show a very simple bar chart with exactly one solid bar per city representing average ticket price. On the right, show a true minimum-to-maximum range chart using a horizontal line or dumbbell/range marker for each city, with a clear low endpoint and high endpoint. Make the contrast between “average” and “range” immediately understandable. Use only 4–5 city labels and make all text clean and readable. Remove any stacked bars, ambiguous chart elements, gibberish labels, or extra dashboard details. Keep the three analysts discussing the choice, but make them secondary to the charts. No logos, no FIFA branding, no stock-market visuals.
Disclosure 
Claude Opus 5 (anthropic/claude-opus-5) generated the initial text-based simulation concept. Recraft V4.1 Pro Vector (recraft/recraft- v4.1-pro-vector) generated the cover-image drafts. Both outputs were reviewed, rejected or revised where needed, and disclosed in the submitted logs.
