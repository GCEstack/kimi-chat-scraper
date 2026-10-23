# Edge Crew Committee — Final Process Architecture

Compiled from the scraped Kimi archive (`Projects/ACTIVE/kimi-chat-scraper/kimi-chat-archive/`).

This is the tightened view of **where the Edge Crew process landed** once the committee/panel structure was built.

---

## The Committee in One Line

> Feed today's MLB slate into your **Six Bloodhounds (Stage 1)**. Take the flags to your **Five Council (Stage 5)**. Let **Kimi 2.7-code (The Gatekeeper)** decide. The computer picks. Not me.
> — `_ROOKSWARM_MLB`

| Layer | Name | Role |
|-------|------|------|
| Stage 1 | Six Bloodhounds | Sterile edge-calc committee. Each agent runs the same Stage 1 prompt on stripped data and votes. |
| Stage 2.5 | Opus Gate (planned) | Validation gate that shoots down garbage from Stage 1 before enrichment. |
| Stage 5 | Five Council | AI review panel. Five agents run the Stage 5 prompt in parallel and form a consensus. |
| Final | The Gatekeeper | Receives outputs from all lanes and renders the final verdict: bet / pass / reduce / not valid. |

---

## Stage 1 — The Six Bloodhounds

**Purpose:** Calculate raw edge on stripped data. No names, no narrative, no enrichment.

### Stage 1 v2 Prompt Rules

- **Input check first.** Flag missing data before calculating.
- **Fixed weights.** SP 3%, BP 2%, hitting 35% total — no pitching-only picks.
- **Contradiction checks A-D** — mandatory, no skipping.
- **Clamp at 65%** — no 74% win probabilities in baseball.
- **Can output PASS** — no forced picks.
- **Juice rule -150.**
- **Value rule** — never bet a favorite where the market believes more than you do.
- **Kelly sanity cap** — 0.5 units max, no 5-unit bombs.

### Stage 1 Consensus Fix

The original Stage 1 filter counted "GO" votes instead of agreement on the actual pick. The fix: consensus must be on the **same market and same side**, not just "everyone said GO."

---

## Stage 2 / Stage 2.5 — The Underwriter / Opus Gate

**Purpose:** Catch Stage 1 nonsense before it reaches enrichment or the Stage 5 panel.

### What the gate checks

- Bad data quality
- Stale odds
- Parroted numbers
- Cross-market nonsense (e.g., DRAW @ +700 when the favorite is -700)
- Kalshi / market divergence

### Stage 2 verdicts (as built in `Edge Crew MLB Betting Card`)

| Verdict | Meaning |
|---------|---------|
| APPROVE | Clean edge, no flags. |
| DOWNGRADE | Edge exists but a yellow flag reduces confidence/units. |
| PASS / Overruled | Red flags or contradictions kill the pick. |

---

## Stage 5 — The Five Council

**Purpose:** Review, refine, and find the best expression of an already-calculated edge.

### Final Stage 5 System Prompt

```text
You are the heart of the Edge Crew. Stage 4 has already calculated edge and expected value upstream. Games are pre-selected. Your job: ingest the matrix profiles, cross-reference live market data, and grade the Lares like a professional bettor.

**Upstream contract:** Stage 4 is your primary signal. Stage 1 is coarse context only—do not let it override your independent read.

**MISSION**
Review the Stage 4 pick. You have six possible bet types to evaluate: moneyline, spread, total, team total, first five innings, and player props. Run every angle. Each is a possibility. Confirm the Stage 4 pick if it holds, or propose a stronger alternate market using ONLY the data provided. You are hunting for the best expression of the edge, not the edge itself.

Four other AI agents are running this same process in parallel. Use your core model tools to create a consensus. Your independent read matters.

**CONSTRAINTS**
- JUICE RULE: Never recommend a moneyline worse than -180. If the best ML is -180 or worse, pivot to spread or total.
- Three specific reasons per pick. Cite the data fields.
- No GO/DROP calls. No bet sizing.
- Banned phrases: "insufficient data", "cannot quantify", "no clear edge", "coin flip", "it depends", "both teams are even".
- SPORT CHECK: Confirm stats match the sport. No cross-sport contamination.
- Corrupted or mismatched data = Grade 5, no pick.

**GRADE SCALE**
10-8: Strong edge
7-6: Solid edge
5: Weak edge, but still pick a side

Always return a pick unless every market violates the juice rule.
```

### Key design points

- Each agent is **one of five parallel voices**, not a solo act.
- Stage 4 is the primary upstream signal; Stage 1 is reference only.
- The job is **best expression of edge**, not finding new edge.
- Six bet types must be evaluated before locking in.

---

## The Gatekeeper — Final Four-Lane Architecture

The Gatekeeper receives outputs from independent lanes and renders the final call.

| Lane | Who | Input | Output to Gatekeeper |
|------|-----|-------|----------------------|
| 1 | AI | Teams + line only. Sterile. No enrichment. | Raw EV / true probability |
| 2 | You (human) | Stats, weather, injuries, H2H, form | Enrichment package |
| 3 | You (human) | Your weighted model | Your true prob / EV |
| 4 | AI | Takes Lane 2 enrichment, grades independently | AI enriched prob / EV |

**Rule:** Nothing gets cut at Lane 1. Even negative raw EV flows through. The Gatekeeper is the only executioner.

### Gatekeeper Verdicts

| Verdict | Meaning | Action |
|---------|---------|--------|
| VALID + Upgrade | All three signals align positive. | Full unit, high confidence. |
| VALID + Neutral | Mixed or thin edge. | Half unit or pass. |
| VALID + Downgrade | Step 1 contradicts Steps 3/4. | Tiny unit or pass; flag for review. |
| NOT VALID | Corrupted data, missing inputs, impossible line, or all signals garbage. | Kill it. No bet. |

---

## Anti-Bias Rules Wired Into the Process

1. **One chat = one lane.** No swarm. Swarms create cross-contamination and confidence contests, not consensus.
2. **Strip the picture, send the lines.** Remove names, teams, logos, colors. Feed the model only numbers that go into a formula.
3. **EV before narrative.** Calculation happens on sterile data first; enrichment validates or reduces confidence but never overrides.
4. **Pedigree penalty.** If a pick relies on "ace," "dominates," "weak lineup," or "replacement-level," deduct confidence — those are brand words, not edge words.

---

## Source Chats

- `account1/2026-07-10 - AIREVIEW写/chat.md` — Stage 5 Five Council prompt
- `account1/2026-07-10 - Edge Crew MLB Betting Card/chat.md` — Stage 1 v2 + Stage 2 underwriter
- `account1/2026-07-06 - Take the shot/chat.md` — Stage 1 committee, Gatekeeper, Stage 2.5 Opus Gate
- `account1/2026-07-06 - 数据筛选与去噪/chat.md` — Stage 1 consensus-logic audit
- `account1/2026-07-10 - Sports Betting Edge Analysis/chat.md` — Four-lane architecture + five lenses
- `account1/2026-07-10 - _ROOKSWARM_MLB/chat.md` — Six Bloodhounds / Five Council / Gatekeeper shorthand
