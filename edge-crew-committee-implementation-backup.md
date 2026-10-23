# Edge Crew Committee — Implementation Backup

Raw snapshot of the implementation conversation and code changes that followed the architecture design.

---

## Bloodhound Consensus Code Snippet

```python
# Step 5: Compute consensus on same-market + same-side
consensus = _compute_bloodhound_consensus(validated_votes, game)

consensus["filter_models"] = validated_votes
consensus["bloodhound_mode"] = True

logger.info(
    "[BLOODHOUND] %s @ %s: verdict=%s market=%s side=%s grade=%d confidence=%d",
    away, home,
    consensus.get("verdict"),
    consensus.get("bet_type"),
    consensus.get("team"),
    consensus.get("score", 0),
    consensus.get("confidence", 0),
)

return consensus


def _compute_bloodhound_consensus(
    votes: List[Dict[str, Any]],
    game: Dict[str, Any],
) -> Dict[str, Any]:
    """Compute consensus from Bloodhound votes.

    Same-market + same-side agreement required.
    Groups by (market, side) and finds the strongest group.
    """
    if not votes:
        return {
            "verdict": "F",
            "score": 0,
            "team": "",
            "line": "",
            "reason": "No valid picks",
            "agreement_level": "SPLIT",
        }

    # Group by market|side
    from collections import defaultdict

    groups = defaultdict(list)
    for vote in votes:
        market = vote.get("best_market", "ML")
        side = vote.get("best_side", "PASS")
        key = f"{market}|{side}"
        groups[key].append(vote)

    # Find strongest group
    if not groups:
        return {
            "verdict": "F",
            "score": 0,
            "team": "",
            "line": "",
            "reason": "No valid picks",
            "agreement_level": "SPLIT",
        }

    # Rank groups by vote count, then by highest grade
    ranked = sorted(
        groups.items(),
        key=lambda item: (len(item[1]), max(v.get("grade", 0) for v in item[1])),
        reverse=True,
    )

    top_key, top_votes = ranked[0]
    market, side = top_key.split("|", 1)

    # Check for tie
    if len(ranked) > 1:
        runner_up_votes = ranked[1][1]
        if len(runner_up_votes) == len(top_votes):
            # Tie — no clear signal
            return {
                "verdict": "C",
                "score": 0,
                "team": "",
                "line": "",
                "reason": "Tie between competing signals",
                "agreement_level": "SPLIT",
            }

    # Compute average grade/confidence from top group
    avg_grade = round(sum(v.get("grade", 0) for v in top_votes) / len(top_votes), 1)
    avg_confidence = round(sum(v.get("confidence", 0) for v in top_votes) / len(top_votes))

    # Get most common line/odds from top group
    lines = [v.get("line") for v in top_votes if v.get("line") is not None]
    line = max(set(lines), key=lines.count) if lines else None

    odds = [v.get("odds") for v in top_votes if v.get("odds") is not None]
    price = int(max(set(odds), key=odds.count)) if odds else None

    # Build reasoning from best graded vote
    best_vote = max(top_votes, key=lambda v: v.get("grade", 0))
    reasoning = best_vote.get("reasoning", "")

    # Count GO vs PASS
    go_count = sum(1 for v in top_votes if v.get("verdict") == "GO")
    total_count = len(top_votes)

    # Map grade to letter
    if avg_grade >= 8:
        grade_letter = "A"
    elif avg_grade >= 6:
        grade_letter = "B"
    elif avg_grade >= 5:
        grade_letter = "C"
    elif avg_grade >= 1:
        grade_letter = "D"
    else:
        grade_letter = "F"

    # Resolve team name for output
    team = side
    if game:
        if side == "HOME":
            team = game.get("homeTeam") or game.get("home_team") or "Home"
        elif side == "AWAY":
            team = game.get("awayTeam") or game.get("away_team") or "Away"

    return {
        "verdict": grade_letter,
        "grade_letter": grade_letter,
        "grade": avg_grade,
        "bet_type": market,
        "team": team,
        "line": line if line is not None else "",
        "price": str(price) if price is not None else "",
        "score": avg_grade,
        "confidence": avg_confidence,
        "consensus_count": go_count,
        "total_go": total_count,
        "engine_agreement": go_count == total_count,
        "low_confidence": go_count < 3,
        "reason": f"{go_count}/{total_count} Bloodhounds agree on {market} {side}",
        "reasoning": reasoning,
        "agreement_level": "CONSENSUS" if go_count == total_count else "ALIGNED",
        "data_gaps": [],
        "risk_flags": [],
        "priority_tier": "TIER_1_TRACK" if avg_grade >= 8 else "TIER_2_STANDARD",
    }


def _filter_result_to_vote(filter_result: Dict[str, Any], mode: str = "standard") -> Dict[str, Any]:
    """Convert a legacy filter_result dict into a vote shape for consensus."""
    return {
        # ...
    }
```

---

## Integration in `run_slate_filter`

```python
# NEW: Bloodhounds path (sterile input, 6 parallel models)
if _use_bloodhounds() and not fast_mode:
    logger.info("[FILTER] Running BLOODHOUND Stage-1 panel for %s", sport_upper)

    tasks = [
        _run_bloodhounds_for_game(g, semaphore, sport_upper, gatekeeper_client)
        for g in slate_games
    ]

    bloodhound_batches = await asyncio.gather(*tasks)

    for game, result_or_err in zip(slate_games, bloodhound_batches):
        away = game.get("awayTeam") or game.get("away_team") or "Away"
        home = game.get("homeTeam") or game.get("home_team") or "Home"

        if isinstance(result_or_err, Exception):
            logger.error("[FILTER] bloodhound failed for %s vs %s: %s", away, home, result_or_err)
            verdict: Dict[str, Any] = {
                "verdict": "F",
                "grade_letter": "F",
                "bet_type": "",
                "line": "",
                "score": 0,
                "confidence": 0,
                "consensus_count": 0,
                "engine_agreement": False,
                "low_confidence": True,
                "reason": f"Bloodhound error: {result_or_err}",
                "agreement_level": "SPLIT",
                "data_gaps": [],
                "risk_flags": [],
                "priority_tier": "TIER_4_DROP",
                "filter_models": [],
            }
        else:
            verdict = result_or_err

        _attach_filter_result(game, verdict)
        logger.info(
            "[FILTER] %s @ %s: verdict=%s bet_type=%s team=%s line=%s price=%s confidence=%s reason=%s",
            away, home,
            verdict.get("verdict"),
            verdict.get("bet_type"),
            verdict.get("team"),
            verdict.get("line"),
            verdict.get("price"),
            verdict.get("confidence"),
            verdict.get("reason"),
        )
```

---

## Phase 2 Completion Summary

**Files Created:**
1. `app/services/data_stripper.py` — sterile HOME/AWAY + odds
2. `app/services/stage1_rules.py` — validation rules (juice -180, input check, contradictions, clamp, value rule, Kelly cap)
3. `app/ai_slate_filter/bloodhound_prompts.py` — Bloodhound prompt + schema

**Files Modified:**
4. `app/ai_slate_filter/filter.py` — Bloodhound integration

---

## Bloodhound Flow

1. Strip game → HOME/AWAY + odds only (no names, stats, narrative)
2. Check input gaps
3. Run 6 Bloodhounds in parallel → each examines ALL markets
4. Validate each vote (rules: juice, contradiction, value, Kelly)
5. Consensus → same market + same side
6. Output → best market, side, grade 1-10, confidence, reasoning

---

## How to Enable

```bash
# Set environment variable to use Bloodhounds instead of committees
export EC4_USE_BLOODHOUNDS=true

# Or in code:
os.environ["EC4_USE_BLOODHOUNDS"] = "true"
```

---

## Key Rules Enforced

| Rule | Description |
|------|-------------|
| Juice -180 | Never recommend moneyline worse than -180 |
| Input check | Models flag missing data themselves |
| Contradictions A-D | market vs line, side vs prob, juice vs grade |
| Clamp at 65% | For MLB, cap win probability at 65% |
| Value rule | Never bet favorite where market believes more than you do |
| Kelly cap | Cap at 0.5 units, no 5-unit bombs |
| Consensus | Same market + same side required (not just GO votes) |

---

## Decision: Skip Opus Gate, Keep the Helper

**Original plan:** Phase 3 — build Stage 2.5 Opus Gate for validation between enrichment and grading.

**User decision:** Skip Opus Gate. Use the existing helper instead.

**The helper:** The Haiku weight adjuster already in `phase_controller.py`:

```python
_PROFILE_HAIKU_CFG = {
    "display": "Haiku Weight Helper",
    "deployment": "anthropic/claude-haiku-4.5",
    # ...
}

async def _build_effective_weights_for_game(game, sport_upper, client):
    """Generate per-profile effective weights, falling back to baseline."""
    base_weights = _get_base_profile_weights(sport_upper)
    return await build_effective_weights(game, base_weights, client)
```

**Final architecture:**

```
Stage 1 (Bloodhounds) → Stage 2 (enrichment) → Haiku weight helper → Stage 4 (deterministic with adjusted weights) → Stage 5 (Five Council) → Gatekeeper
```

The Haiku helper adjusts profile weights (`sintonia`, `edge`, `standard`, `expected_value`, `renzo`) based on the enrichment before Stage 4 grading. No separate Opus Gate.
