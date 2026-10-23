# Edge Crew — Data Reconciliation: Gate Needs vs. Current Mapping

## Data Requirements

| Gate Needs | Mapped Now? | Status |
|------------|-------------|--------|
| Odds (ML/total/spread) + timestamp | ✅ odds JSON | HAVE — but odds_history is thin (68 rows); line-move tracking needs the scheduled pulls writing history every time |
| Probable starters + ERA | ⚠️ home/away_sp_* | BROKEN TRUST — stale projections, zero confirmations, duplicate-day bug |
| Starter CONFIRMED flag | ❌ | GAP — the late pass + ESPN-first fix fills this |
| Injuries | ✅ home/away_injuries | HAVE |
| Form: record, L5, streak | ✅ | HAVE |
| Bullpen ERA + tired flag | ✅ | HAVE |
| Pitcher last-5 game logs | ❌ | GAP — you hand-pulled these all night (Woo's splits, Littell's streak, Rodriguez's form). This is the single biggest hole. The matrix needs sp_last5 computed from game logs |
| Team splits (vs LHP/RHP, home/away) | ❌ | GAP — the Tigers RL decision died here |
| Final scores | ❌ | GAP — no reconciliation, no auto-grading, no trend answers |
| Model grades | ⚠️ phase_snapshot | HAVE the structure — but grading must fire on schedule, not on request |

## The Schedule (for Kimi Code)

| Time | Action |
|------|--------|
| 6:00 AM PT | EARLY pull — odds + injuries + form + bullpens + SP projections → grades fire → status line |
| First pitch −2h, rolling | LATE pull — SP confirm (ESPN first), lineups, odds refresh → re-grade if starter changed → status line |
| Every pull | Writes: source stamp, odds_history row, enrichment_runs log |
| Post-final | Score capture → reconciliation |

## The Only Real Building

The two new computed fields — `sp_last5` and team splits — are the only real building. Everything else is scheduling and wiring.
