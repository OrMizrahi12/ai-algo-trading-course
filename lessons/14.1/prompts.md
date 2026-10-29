# Lesson 14.1 prompts

Everything typed in the lesson, in order. Lines that start with `/` are Claude Code commands. One interactive Claude Code
session in `~/trading-desk` (auto mode), with Obsidian open on the desk's vault beside it. Paper account only.

## 1. Ask for the review gate

```text
/clear
```

```text
After every closed trade, the desk must review it before it may trade again. When a trade closes, wake Claude with the trade and the bars since entry, run the post-trade-review skill, write the review into the trade note and one tagged lesson into vault/Lessons. In the executor, refuse any new entry until the last closed trade has its review, and tell the trader why when an entry is refused. Add tests for the gate.
```

On our computer Claude worked for 10 minutes 28 seconds. It read the desk (the trade tracker, the executor, the note
writer from lesson 13.2); the shell guard from lesson 12.3 blocked one read because it named the hook file, so Claude
skipped that file. It built the gate into the journal, the gates, the executor, the heartbeat and the snapshot, the
review writer into `desk/scribe.py`, and the tests. 272 tests passed (249 before). It did not run a real `claude -p`
review yet, and it said so. It also noted that it had not gated the MCP server.

## 2. Close the MCP door

```text
Gate the MCP server too: the same review rule must hold for every way to buy. Then run all the tests and commit.
```

Claude first isolated the MCP tests from the real journal, then made `place_bracket` read the heartbeat's journal and
refuse a buy while the last closed trade has no review (`close_position` is never blocked). 273 tests passed, and
everything went into one commit.

## 3. Replay a closed trade

We filmed on a Saturday, with the market closed, so we replayed one trade:

```text
The market is closed today, so show me the gate on a replayed trade. In a temporary copy of the desk, journal one made-up closed SPY trade, then: try a buy and show the refusal the trader would see, run the real review with claude -p, and show the review in the trade note and the lesson it wrote. Then try the buy again. Keep the real journal and vault untouched, but copy the test notes into vault/Trades and vault/Lessons with TEST in their names so I can open them in Obsidian.
```

What happened, in four steps: (1) a made-up trade, 10 shares at 603.86, closed by hand at 603.91 (0.01R); (2) a buy
before the review was refused, no order sent, and the snapshot's `entry_review_gate` told the trader why; (3) the real
review loaded the `post-trade-review` skill, classified the trade "bad trade good result" (the stop was 6.86 below the
entry, the target only 2.14 above, which breaks "target at least 2x the stop distance") and wrote one proposed lesson;
(4) the same buy was allowed and filled. All prices are made up. The risk seatbelt also cut the fake trader's 50 shares
to 10.

```text
Good. Delete the two TEST notes now.
```

## Pause and try

1. Ask Claude for a review gate like ours, in the executor, with tests.
2. Make sure every way to buy goes through it, the MCP server too.
3. Replay one made-up closed trade, and watch the refusal, the review and the lesson.

You're done when a buy before the review is refused, the same buy after it goes through, and your vault holds one
proposed lesson.
