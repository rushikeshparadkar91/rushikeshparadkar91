---
name: profile-repo-failure-archaeology
description: >-
  Load this skill in two situations. (1) You just finished a non-trivial
  investigation in this repo — a confusing symptom, a dead end, a trap, a "why is
  this empty/broken/missing" hunt — and must record it: this file holds the strict
  entry template and appending rules. (2) You are STARTING an investigation and want
  to check whether the symptom was already explained — read the chronicle below
  first. Trigger phrases: "we've seen this before?", "log this finding",
  "post-mortem", "why did git log fail", "fetch did nothing", "is the repo empty or
  do I lack access", "record what we learned", "add an archaeology entry".
---

# Profile Repo Failure Archaeology

## Honest preface

This chronicle begins at **repository genesis, 2026-07-14**. The repo
`rushikeshparadkar91/rushikeshparadkar91` was empty on that date (zero commits,
zero branches; evidence in entry 2026-07-14-01), so there is **no prior history
to mine** — no old incidents, no legacy post-mortems, no previous maintainers'
notes. Everything below was observed first-hand in the 2026-07-14 authoring
session. Any entry claiming to predate 2026-07-14 is fabricated and must be
removed via change control.

"Archaeology" here means: the append-only record of investigations — including
dead ends — kept so future sessions do not re-dig the same holes.

## The chronicle (canonical entries)

### Entry 2026-07-14-01 — Maintainer expected a project; found an empty clone

- **Symptom:** An incoming maintainer expected working project content; the local clone contained nothing but `.git/`.
- **Root cause:** The profile repo had been created on GitHub but never received a push. It was genuinely empty — not a partial clone, not an access problem.
- **Evidence:** `git ls-remote origin` produced no output (exit 0); GitHub REST API (via the authenticated GitHub MCP connector) returned `409 Git Repository is empty`; `list_branches` returned `[]`; `ls -la` at the repo root showed only `.git/`.
- **Status:** RESOLVED (documented). The empty state is now the recorded baseline; the fix path is the governed first push (see `profile-repo-bootstrap-campaign`).

### Entry 2026-07-14-02 — Could not verify GitHub docs from the sandbox

- **Symptom:** Attempts to load docs.github.com and unauthenticated api.github.com from the Claude remote session failed.
- **Root cause:** Session network policy for this project denies docs.github.com (CONNECT 403) and disables unauthenticated api.github.com (HTTP 403 "GitHub access is not enabled for this session"). Not a GitHub outage, not a DNS/TLS problem.
- **Evidence:** `curl -sSI https://docs.github.com -o /dev/null -w '%{http_code}\n'` → 403 via proxy CONNECT denial; unauthenticated `curl -sS https://api.github.com` → HTTP 403 with the session-policy message.
- **Status:** RESOLVED (documented). Workaround: use the GitHub MCP tools when connected, or verify docs from an unrestricted machine. Platform facts in this skill library are therefore labeled "Model knowledge (2026-07-14)".

### Entry 2026-07-14-03 — Trap: git behaves misleadingly on unborn branch + empty remote

- **Symptom:** `git log` failed with exit 128; `git fetch origin` "succeeded" but appeared to do nothing; `git branch -r` stayed empty. Easily misread as a broken clone or a network failure.
- **Root cause:** Expected git behavior at genesis. An **unborn branch** (a checked-out branch name with no commits yet) makes `git log` exit 128 with `fatal: your current branch 'X' does not have any commits yet`. Fetching from an **empty remote** is a silent no-op (exit 0, no output), so `git branch -r` correctly lists nothing.
- **Evidence:** `git log` → exit 128 with the message above; `git fetch origin` → exit 0, no output; `git branch -r` → empty. Discriminating test: `git ls-remote origin` — an **empty repo** exits 0 with no output, whereas **no access** errors out. This is the fastest way to distinguish "empty repo" from "no access".
- **Status:** RESOLVED (documented discriminating test: `git ls-remote origin`).

<!-- APPEND NEW ENTRIES BELOW THIS LINE. Never edit or delete entries above it. -->

## The strict entry template

Copy exactly; fill every field; no field may be omitted or left vague.

```markdown
### Entry YYYY-MM-DD-NN — <one-line title in plain words>

- **Symptom:** What was observed, verbatim where possible (exact error text, exit code, blank output).
- **Root cause:** The single confirmed cause. If unconfirmed, write "UNCONFIRMED —" plus the leading hypothesis and what would confirm it.
- **Evidence:** The exact reproducible command(s) run and what they returned. A reader must be able to re-run these.
- **Status:** One of RESOLVED (documented) | OPEN | DEAD END (documented). Add one clause: the fix, the next step, or why the path was abandoned.
```

Numbering: `YYYY-MM-DD` is the date the investigation concluded; `NN` is a
two-digit sequence within that date (01, 02, ...), continuing from the highest
existing number for that date.

## Rules for appending

| # | Rule |
|---|---|
| 1 | **Every non-trivial investigation gets an entry** — anything that took more than one obvious command to explain, changed your mental model of the repo, or would trap the next session. |
| 2 | **Dead ends are entries too.** Status `DEAD END (documented)`, with why the path was abandoned. An undocumented dead end will be re-explored by the next session at full cost. |
| 3 | **Entries are append-only.** Never rewrite, merge, renumber, or delete an existing entry. To correct one, append a new entry that references it (e.g. "supersedes 2026-07-14-02"). |
| 4 | **Every entry needs reproducible evidence commands.** "It didn't work" is not evidence; "`git ls-remote origin` → no output, exit 0" is. If the evidence is a tool/API response, quote the status code and message. |
| 5 | **No invented entries.** Only record what actually happened in a real session, with commands actually run. No hypothetical or illustrative incidents — the template above is the only permitted hypothetical text. |
| 6 | **Appending is a change like any other.** Land it via the process in `profile-repo-change-control` (governance-and-skills class): `claude/*` branch, PR, review. Do not push chronicle edits straight to the default branch. |
| 7 | **Facts not verifiable in-sandbox** must be labeled `Model knowledge (YYYY-MM-DD)` with a re-verification pointer, exactly as elsewhere in this library. |

## When NOT to use this skill

- You are mid-investigation and need **triage steps** (symptom → discriminating experiment tables for "README not showing", "images stale", "workflow not firing", "empty-clone confusion") → use `profile-repo-debugging-playbook`. Come back here to record the outcome.
- You need **repo invariants or platform facts** → use `profile-repo-architecture-contract` or `github-profile-reference`.
- You need to know **how a change (including a chronicle append) lands** → use `profile-repo-change-control`.

## Provenance and maintenance

Chronicle founded 2026-07-14 at repository genesis with exactly three entries,
all observed first-hand in that session. Re-verify volatile facts:

| Volatile fact | One-line re-verification |
|---|---|
| Repo emptiness (baseline of entry 01) | `git ls-remote origin | head` (no output + exit 0 = still empty; refs listed = update entry cross-references, not the entry itself) |
| Sandbox network policy (entry 02) | `curl -sSI https://docs.github.com -o /dev/null -w '%{http_code}\n'` (403 = still blocked) |
| Unborn-branch behavior (entry 03) | `git log` on a freshly `git init`-ed directory reproduces the exit-128 message |
| Platform docs pointer | `https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/customizing-your-profile/managing-your-profile-readme` from an unrestricted machine |

Amend this skill's rules/template only via `profile-repo-change-control`.
The chronicle section itself is append-only per Rule 3.
