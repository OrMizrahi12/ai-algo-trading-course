# Prompts from Lesson 13.1

Start a fresh Claude Code session in your desk folder (`cd ~/trading-desk && claude`), in auto mode, with Obsidian open
beside it on the same vault.

## 1. Design the vault

The prompt we typed, word for word:

```text
We have an Obsidian vault at vault/ (open in Obsidian on the right). Design it as this desk's memory: folders for rules, playbook, market notes, trades, daily notes and lessons, a template for a trade note and a daily note, and a README note that explains how you use each folder. Write the first notes: the rules (copied from our risk limits, marked as read-only for you), two playbook setups we already know (opening range breakout, VWAP reclaim) with links, and today's daily note. Add a skill that tells you how to read and write the vault. Then commit, with the vault in Git.
```

What Claude did on our computer, in order: looked at the repo, the skills and the vault (one combined shell command was
blocked by the guardrail hook because it named guarded files, so it read them one at a time with the Read tool); read the
lab's own definitions of both setups; counted today's heartbeat journal (26 bars, all wait); removed `Welcome.md`; made
`Rules`, `Playbook`, `Market`, `Trades`, `Daily`, `Lessons` and `Templates`; wrote the README note, the two rules notes,
the two setups, the two templates and today's daily note; then asked where the skill should go.

## 2. Where the skill lives

Claude asked:

> Where should the vault skill live? Anything under .claude/skills/ is hashed into the trader's instructions
> (desk/model.py) and loaded as part of its plugin, and today's heartbeat is running now (26 bars so far).

We chose its recommendation, **Outside the trader's skills**: `.claude/vault-skill/vault/SKILL.md`, committed but not in
the hashed folder. Claude then fixed the README note to point there, checked that nothing in the trader's folders had
changed, and committed:

```text
Add the Obsidian vault as the desk's memory, with a vault skill outside the trader's skills
```

If your heartbeat is not running and you don't use one, the question may not come up, or Claude may recommend something
else. Keep the vault skill out of the folder your trader's instructions are built from.

To use the skill in your own interactive sessions (run once, from the desk folder):

```bash
ln -s "$PWD/.claude/vault-skill/vault" ~/.claude/skills/vault
```

## 3. Pause and try

1. Install Obsidian from obsidian.md, and create a vault called `vault` inside your desk folder.
2. Give Claude the design prompt above, and answer its questions.
3. Open a setup note, and follow its links in the graph view.

Done when: the folders, the README note, the rules notes, the two setups and today's daily note show up in Obsidian, and
the vault is committed (`git log -1 --stat` lists the `vault/` files).
