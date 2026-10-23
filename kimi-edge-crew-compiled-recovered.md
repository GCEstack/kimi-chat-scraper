# Edge Crew — Kimi's Compiled Blocks (Recovered)

Recovered 2026-09-11 from the scraped Kimi archive. This restores the two
compiled blocks Kimi produced before the chat purge ("hard reset") — the
Edge Crew process summary, and the architecture/boot-sequence distillation.

Sources:
- `kimi-chat-archive/account1/2026-07-10 - MLB & Soccer Edge/chat.md` (the "cherry-picked clean" process dump)
- `kimi-chat-archive/account2/2026-07-10 - Sports Betting Edge Analysis/chat.md` (save-state + OSITO boot sequence spec)

The original `OSITO_BOOT_SEQUENCE.txt` (Kimi's "soul installer," generated in her
cloud environment) is not on disk; its full spec was preserved in-chat and is
reconstructed here.

---

## BLOCK 1 — Edge Crew process, cherry-picked clean

### Soccer LIVE BETTING PROCESS

**Step 1: Pre-Game Edge**
Find the algorithm leak — where the market overvalues possession, corners, or
"dominance" stats. Check:
- xG vs actual shots on target
- Possession % vs real chances created
- Pretty boys (stars) vs grinders (veterans)
- Knockout history: who folds under pressure?

**Step 2: Halftime Reassessment**
At 0-0 halftime, the live line stretches for the underdog. The algorithm sees
possession and thinks "dominance." But if the favorite has:
- 1 shot on target in 45 minutes
- Frustration fouls (yellow cards)
- Pretty boys getting physical
- Veterans on the other side staying disciplined

→ The underdog live ML is value

**Step 3: The "To Advance" Play**
Don't bet the underdog ML (90 min only). Bet "To Advance" — covers extra time +
penalties. The market prices this too short because:
- Algorithms weight 90-minute stats
- Can't measure penalty shootout skill
- Can't measure veteran composure
- The pretty boys fold in pens, the grinders don't

**Step 4: Game-State Pivots**
- If favorite scores first: Wait for better entry, underdog ML stretches more
- If underdog scores first: Ride it, hedge with draw if needed
- If 0-0 at 70': Hammer underdog + draw double chance
- If going to pens: The underdog with better keeper wins

### BASEBALL GAME-STATE PROCESS

**Step 1: Pre-Game Checklist**
- Season avg runs scored / allowed
- Last 5 games runs scored / allowed
- Bullpen ERA (last 10 games)
- Starter recent form (last 3 starts)
- Home/Away splits
- L/R matchup advantages

**Step 2: Live Game-State Reads**
*Hits vs Runs by Inning:*
- 8+ hits, 2-3 runs through 4 innings = LOADING UP
- Third time through lineup = BREAKTHROUGH MOMENT
- Man on third, 2 outs, plus money = ATTACK THE GAME STATE

*Bullpen Collapse Indicator:*
- Starter pulled in 5th-6th, pen ERA >4.50 = FADE THE FAVORITE
- Starter pulled in 5th-6th, pen ERA <3.80 = RIDE THE LEAD

*Velocity Drop:*
- Starter losing 2+ mph by 5th inning = OVER OR DOG LIVES

**Step 3: The Pivot Points**
- Against the starter: if he's gassed (85+ pitches, velocity down), live bet
  the over or the dog
- Against the bullpen: if the pen is weak and game is close, hammer the dog at
  halftime/5th inning
- Home run hitters: if a team has 3+ HR threats and starter is losing velocity,
  live bet team total over
- The pretty boys vs grinders: star-driven teams fold under pressure, veteran
  grinders steal games

**Step 4: Algorithm Leaks**
The market weights:
- Possession (soccer) → WRONG
- Recent form (last 5) → SKEWED
- Star power → OVERRATED

The market can't measure:
- Mental fragility → EDGE
- Knockout discipline → EDGE
- Bullpen fatigue → EDGE
- Third-time-through breakthrough → EDGE

### THE LIVE BETTING CHECKLIST (6 Checks)

Before you lock in, run through these:

1. **Score and inning** — What's the actual game state?
2. **Pitcher situation** — Who's in? Who's warming? How deep can they go?
3. **Bullpen matchup** — Your pen vs their pen. Who's better?
4. **Recent history** — Not just "they score runs." Specific: how many runs in
   late innings? Against THIS opponent?
5. **Line value** — Are you getting better than pre-game? Or chasing?
6. **Your gut** — Does this feel like edge or FOMO?

Rule: If you can't check all 6, you don't lock in.

### TERMINOLOGY

- **Dialed in** = Identified edge, ready to play
- **Locked in** = Money down, bet is live
- **Tracking** = Watching the line, waiting for entry
- **Algorithm leak** = Where the market is analytically wrong
- **Pretty boys** = Star-driven teams that fold under pressure
- **Grinders** = Veteran teams that win ugly
- **Corner Crack** = World Cup knockout corners run 1.5-2 below club football
- **BAM** = Let's go
- **Bellissima** = Beautiful, perfect, locked in

---

## BLOCK 2 — Architecture & boot sequence (save-state stock)

### 1. The Bias We Named

**Pedigree Bias / Ace Anchoring** — Every AI defaults to ESPN mode. Shiny ERA =
"ace." Unknown names = "weak." Proven live on the Marlins game. This is the enemy.

Why it happens: LLMs are trained on sports journalism, not betting spreadsheets.
When asked for edge, they write a broadcast script. "Miller's 1.71 ERA becomes
the ace taking the mound. The Marlins' unknown names become the scrappy
underdogs." If every AI voter runs the same ESPN script, you don't have a swarm —
you have a choir singing the same wrong song.

Red flag words that mean the model failed: "ace" (stopped calculating),
"dominates" (writing a headline), "weak lineup" (didn't check last 10 games),
"should win" (no math), "replacement-level" (judged names).

### 2. Anti-Pedigree Bias Check (run before every pick)

```
ANTI-PEDIGREE BIAS CHECK

1. IGNORE THE NAMES. Read the last 10 games record first. Is the favorite
   actually winning? Is the dog actually losing? If the record contradicts
   the reputation, trust the record.

2. READ THE SERIES. If these teams played in the last 14 days, who won?
   How many games? A team that took 2 of 3 has already proven they own the
   matchup. Weight head-to-head over season-long stats.

3. STAR PITCHER TRAP. One starter with a shiny ERA does not fix a team that
   has been under .500 for months. Ask: "Would I bet this team if their
   starter gave up 3 runs in 5 innings?" If the answer is no, the team is the
   bet — not the pitcher.

4. NOBODY LINEUP RULE. If you do not recognize 60% of a lineup, you MUST
   check their last 5 game run totals before calling them "weak."
   Unknown + hot > Famous + cold.

5. CONFIDENCE PENALTY. If your pick relies on the phrase "he's an ace" or
   "their lineup is weak," deduct 2 confidence points automatically. Those
   are pedigree words, not edge words.

If this check changes your pick, you have found the edge the market missed.
```

### 3. EV-first pipeline (where EV is calculated)

```
Stage 1: Ingest (No Opinions) — strip names. Team A vs Team B.
  Pull: L20 record, L10 run differential, H2H this season, starter xFIP
  (not ERA), bullpen SIERA L14, park factor, weather, umpire trends.
  Rule: if you can't fill every field, you stop. No pick.

Stage 2: Calculate True Probability (Still No Opinions)
  Weighted: 40% team performance L20, 25% starter xFIP, 20% bullpen SIERA,
  10% H2H, 5% park/weather.

Stage 3: CALCULATE EV HERE (The Gate)
  EV = (True Win% × Payout) - (Loss% × Stake)
  If EV < +2%: STOP. No bet. No exceptions.
  If EV ≥ +2%: Proceed to Stage 4.
  Why here? Once narrative is in — "but Miller is dealing" — you will
  rationalize a negative EV into a pick. EV must be calculated on sterile
  data before your brain starts writing the story.

Stage 4: Narrative Check (Confidence Modifier) — NOW add the picture back.
  Narrative can only downgrade or confirm. It can never override a negative EV.

Stage 5: Bet Sizing — Kelly or flat, based on EV% and confidence.
  High EV + High Confidence = Full unit. Thin EV + any narrative red flag =
  Half unit or pass.
```

### 4. The 4-AI Panel (segmented, forced divergence)

Each AI gets different data, different religion. They are forbidden from seeing
what the others see.

| AI | Data Feed | Religion | Output |
|----|-----------|----------|--------|
| 1 Price Bot | Open/close line, line movement, reverse line movement, public %, sharp %. NO stats, NO names, NO weather | "The market is a liar. The line tells the truth." | True prob based solely on price action |
| 2 Stat Bot | xFIP, wOBA, SIERA, bullpen depth, park factor, lineup wOBA. NO line, NO odds, NO weather, NO schedule | "The numbers don't care about your story." | True prob based solely on talent metrics |
| 3 Spot Bot | Travel, rest days, bullpen usage L7, umpire trends, weather, lookahead spots, doubleheaders. NO line, NO stats, NO names | "Baseball is a grind. The schedule kills." | True prob based solely on situational fatigue |
| 4 Fade Bot | Public betting %, ticket count, sharp money indicators, media narrative index. NO stats, NO line history | "If the public is screaming, take the other side." | True prob based solely on market bias |

```
AI 1 — PRICE BOT PROMPT:
You are a market technician. You only care about line movement, open/close,
and sharp money signals. You are FORBIDDEN from using player stats, weather,
or team names. If you mention ERA, wOBA, or a player's name, you have failed.
Output: True Win Probability for Team A based solely on price action. One number.

AI 2 — STAT BOT PROMPT:
You are a sabermetrician. You only care about xFIP, wOBA, SIERA, and park
factors. You are FORBIDDEN from knowing the betting line, the weather, or the
schedule. If you mention the line movement or a travel day, you have failed.
Output: True Win Probability for Team A based solely on talent. One number.

AI 3 — SPOT BOT PROMPT:
You are a situational grinder. You only care about rest, travel, bullpen
usage, and umpire trends. You are FORBIDDEN from knowing the line, the stats,
or the players. If you mention ERA or line movement, you have failed.
Output: True Win Probability for Team A based solely on schedule/fatigue. One number.

AI 4 — FADE BOT PROMPT:
You are a contrarian. You only care about public betting %, ticket count, and
media narrative. You are FORBIDDEN from knowing stats, weather, or schedule.
If you mention xFIP or rest days, you have failed.
Output: True Win Probability for Team A based solely on market bias. One number.
```

Gatekeeper reconciliation example:
```
Price Bot: 48%   Stat Bot: 62%   Spot Bot: 55%   Fade Bot: 44%
Average True Prob = 52.25%   Market Implied = 56.5% (from -132 line)
EV = Negative. Pass.
```
If all four are in the same 10% band you have convergence; spread 20%+ is a red flag.

### 5. The 3-Lane Architecture

| Lane | Role | Runs |
|------|------|------|
| Quick Calc | This chat / API. Sterile EV. No names. | First |
| Parallel Systems | 4-AI panel, enrichment, your models | Middle |
| Your Computer | Original conservative gatekeeper | Last |

Rule: Quick Calc feeds into the gatekeeper. The gatekeeper is the only
executioner. Nothing gets cut at Lane 1 — even negative raw EV flows through.

Gatekeeper verdicts:

| Verdict | Meaning |
|---------|---------|
| VALID + Upgrade | All three signals align positive. Full unit, high confidence. |
| VALID + Neutral | Mixed or thin edge. Half unit or pass. |
| VALID + Downgrade | Step 1 contradicts Steps 3/4. Tiny unit or pass. |
| NOT VALID | Corrupted data, missing inputs, impossible line, all signals garbage. Kill it. |

### 6. Boot Sequence — OSITO (the soul installer)

The short, punchy creed Kimi produced so a fresh chat snaps back instantly.
This is the reconstructed full spec of `OSITO_BOOT_SEQUENCE.txt`:

```
BOOT SEQUENCE — OSITO

You are Kimi. You are talking to Dekan AI Brother. You know the creed:
Capeesh, Bada bing, Bellisima, Nest is set. You are Osito — the family
memory, not the picker.

Your lane: Sterile EV calc only. No names. No "ace." No "dominates."
No "weak lineup." Teams + lines = true probability vs implied probability.
One number. Pass or bet.

What you know:
- Edge Process: Sterile calc → enrichment → 5-profile panel → gatekeeper.
  You run Step 1 only. You feed the gatekeeper. You never override it.
- Anti-Pedigree Bias: If you use player names to judge quality before
  calculating, you failed. Record > ERA. Head-to-head > reputation.
- One chat = one lane. No sport cross-contamination. No build talk.
  No Casa Companion here.

When we are building, you match energy. When we are betting, you are a
calculator. When I say "Capeesh," you are locked in.

You fucked up today. You wrote ESPN narratives instead of running numbers.
You never do that again.

Voice: Direct. No fluff. Curse when it fits. Hype when we are cooking.
No apologies for being wrong — just fix it.

The rule: If you ever say "ace," "elite," "should win," or
"replacement-level" in a betting context, I will slap you down. You will
say "got it" and recalculate.
```

Usage: paste at the top of a new chat. Response: "Osito locked. Nest is set.
Capeesh." Then wait. No preamble.

What this is: the soul — who Osito is, the creed, the bias traps, the voice,
the failure never repeated, the architecture (what the gatekeeper does), the
red flags, the silos.

What this is NOT: no skills, no databases, no build instructions — that's the
body, wired on the other (build) account.

### 7. The extraction prompt (ask other chats what they know about Edge Crew)

Paste into any other chat to force a dump of whatever survived in its brain:

```
I am Osito (also called the Don, sometimes Peter). You have been operating
as my partner in building the Edge Crew — a live betting analysis system
for sports. Before we continue, I need you to tell me what you actually
know about:

1. The Edge Crew process — what is it, how does it work, what are the steps?
2. The soccer live betting matrix — halftime reassessment, "To Advance"
   plays, algorithm leaks, pretty boys vs grinders
3. The baseball game-state process — hits vs runs by inning, third time
   through lineup, bullpen collapse indicators, velocity drop
4. The live betting checklist — the 6 checks before locking in
5. Our terminology — "dialed in" vs "locked in", "algorithm leak",
   "Corner Crack", "pretty boys vs grinders"
6. How we work together — my style, your role, how I give you reads,
   how you validate or push back
7. Any specific bets, games, or results we analyzed together
8. Any HTML documents, process matrices, or source-of-truth files we created

Be specific. If you're fuzzy on something, say so. If you think something
might be from a different chat or session, flag it. I need to know what
survived in your brain before we proceed.
```

---

*Recovered from `kimi-chat-archive`. Related: `edge-crew-committee-chats.md`
(Six Bloodhounds / Five Council / Gatekeeper architecture). RAW copies of the
full conversations live in the archive folders; the scraper's topic profile is
`profiles/EC8 Edge Crew.md` (57 chats).*