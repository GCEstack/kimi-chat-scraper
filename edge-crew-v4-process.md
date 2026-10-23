# Edge Crew v4 — The 7 Steps (Corrected)

This is the corrected mapping of the Edge Crew process.

| Step | Name | What Happens |
|------|------|--------------|
| 0 | Data Enrichment | Raw game data → Matrix JSON (fixtures, stats, lines, weather, injuries, refs) |
| 1 | 5 Committees | 5 blind committees run parallel on same matrix. Each grades A-F on their lens. One F kills it. |
| 2 | Home/Away Lenses | DeepSeek v3 (AWAY) applies bumps (+/- 0.5 to 2.0) with context |
| 4 | EV Calculation | Implied prob vs true prob → Edge % + Kelly sizing |
| 4.5 | Market Verification | CRITICAL: Kalshi and Book must match. Mismatch = auto-kill |
| 5 | Fusion Final Deliberation | 3 AI judges (Prosecutor + Defender + Validator) vote on full slate. 2-1 LOCK = STRONG PLAY |
| 6 | Gatekeeper (Validation Only) | Validates the full panel output. Not a gate — a check. |
| 7 | The Don (Final Veto) | Reviews Fusion output. Locks or vetoes. |

## Key Corrections

- **There is NO Step 3.** An earlier version of this doc listed a "User Interjection (The Don)" mid-pipeline step. That was wrong — there is no user interjection step. The Don appears exactly once, at Step 7, as the final veto. (Step numbering keeps the gap so existing references to Steps 4–7 stay valid.)
- **Step 5 is Fusion Final Deliberation**, not "Five Council grading to pick one." Three AI judges — Prosecutor, Defender, Validator — vote on the full slate. A 2-1 LOCK is a STRONG PLAY.
- **Step 6 is Gatekeeper as validation only.** It checks the panel output for corrupted data, missing inputs, or impossible lines. It does not gate or kill picks.
- **Step 7 is The Don (Final Veto).** The actual final decision. The Don reviews the Fusion output and locks or vetoes.

## Role of the Gatekeeper vs. The Don

| Role | What It Does |
|------|--------------|
| Gatekeeper | Validation only. Catches data errors, contradictions, and invalid outputs before they reach The Don. |
| The Don | Final veto. Sees everything, decides what gets locked and what gets passed. |

## Where Kill Power Lives

| Step | Kill mechanism |
|------|----------------|
| 1 — Committees | One F grade from any committee kills the game |
| 4.5 — Market Verification | Kalshi/Book mismatch = auto-kill |
| 7 — The Don | Final veto on anything Fusion shipped |

The Gatekeeper (Step 6) has **no** kill power. It validates and reports only.
