# Lesson 14.2 cheat sheet: keep or discard

## Words

| Word | Meaning |
|---|---|
| Promote / demote | Move a lesson into the playbook, or back out of it |
| Sample size | How many trades the evidence rests on |
| Change log | The dated list of rule changes and why: `vault/Changelog/Rules change log.md`, with the numbers and the Git commit |
| Rollback | Take a promoted lesson back out when later trades turn against it; every change is its own Git commit, so it can be undone |
| R | 1% of the account, the money lost if a trade's stop is hit. +2R = made twice what it risked; -1R = lost what it risked |
| Average R | The mean result of a group of trades, in R |
| 95% interval | The range the true value probably lies in. Wide = not known well. Found by bootstrapping: re-drawing the same trades 10,000 times |
| Applied | The trader named the lesson in the `lessons` key of the decision that bought, or of a sell or close of that trade |
| Similar, not applied | Trades that did not name it, made while the lesson was available, in a setup the applied trades also used |

## A lesson's life

proposed (written by the reviewer) -> active (a person approves it; tracking starts on its `activated:` date) ->
promoted (in `Playbook/Promoted lessons.md`) or archived (`Lessons/Archive/`). A promoted lesson can be rolled back.

## The tracker's rules (`desk/lessons.py`)

| Verdict | When |
|---|---|
| PROMOTE | At least 20 applied trades with a result, at least 10 similar ones, and the whole 95% interval of the difference above 0 |
| ARCHIVE | An active lesson with at least 10 applied and 10 similar trades, and the whole interval below 0 |
| ROLLBACK | A promoted lesson: the same test, but only on trades after the promotion day. The earlier trades got it promoted, so they can't also confirm it |
| KEEP | Anything else: not enough evidence yet |

- `uv run -m desk.lessons`: report only, changes nothing.
- `--apply`: makes the changes and writes the change log. `--commit`: also commits them, one commit per lesson.
- Thresholds are constants at the top of `desk/lessons.py`. Only the 20 was asked for; 10, the 10-trade comparison group
  and the 95% interval were Claude's choices.

## Reading the numbers (our seeded demo: every number is made up)

| Run | Lesson | Applied | Similar | Difference (95% interval) | Verdict |
|---|---|---|---|---|---|
| 2026-09-04 | Wait for the retest after a breakout | 30, +0.41R | 21, -0.09R | +0.50R (+0.04 to +0.96) | PROMOTE |
| 2026-09-04 | Skip the first bar after a gap | 8, +0.74R | 43, +0.10R | +0.64R (+0.08 to +1.24) | KEEP: 8 of 20 |
| 2026-10-23 | Wait for the retest (after promotion only) | 13, -0.87R | 14, +0.08R | -0.94R (-1.56 to -0.37) | ROLLBACK |
| 2026-10-23 | Skip the first bar after a gap | 12, +0.24R | 66, -0.04R | +0.28R (-0.33 to +0.89) | KEEP: 12 of 20 |

- The promotion only just cleared 0 (lower bound +0.04R): 20 to 30 trades is thin evidence.
- A lesson that looks great on 8 trades is still held back. Sample size first.

## The review after every 50 trades (`desk/review.py`)

- Splits a block of 50 closed trades by **setup** (from the trade note), **time of day** (morning before 11:00, midday
  11:00 to 13:00, afternoon from 13:00, New York time) and **market regime** (the 15-minute trend at entry: up, down,
  mixed). Every number has its 95% interval.
- A group under 10 trades is "too few to say". A group is "clearly better" or "clearly worse" only if the whole interval
  of its difference from the other trades is above or below 0.
- Many groups are judged at once, so chance alone flags about 1 in 20 of them. With 8 groups, about 0.4 flags are
  expected by luck: one flag in a report like this is a question, not a discovery.
- It decides nothing: it doesn't change any lesson or rule. It never writes seeded data into the real vault.

## Safe defaults

- Not enough data yet is a fine answer.
- The tracker reports by default; apply only after you have read the report.
- Seeded data is always labelled and kept in its own folder.
- No lesson can touch the risk limits or the guardrails from lesson 12.3.

Paper account only. Educational content, not financial advice; nothing here is a promise of profit or a recommendation.
