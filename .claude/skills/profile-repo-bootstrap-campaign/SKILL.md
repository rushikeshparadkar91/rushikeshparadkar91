---
name: profile-repo-bootstrap-campaign
description: >-
  The decision-gated, phased campaign for shipping the FIRST profile README to the
  currently EMPTY repository rushikeshparadkar91/rushikeshparadkar91 (verified empty
  2026-07-14 — zero commits, zero refs). Load this skill when: the repo has no commits;
  "README not showing on profile" and the repo is empty; you are asked to "bootstrap",
  "ship the profile", "create the first README", "do the first push", or "get something
  live on github.com/rushikeshparadkar91"; or you are deciding WHAT to ship first
  (static README vs badges vs stats vs Actions). Do NOT load for day-to-day edits to an
  already-shipped README — this campaign EXPIRES the moment `git ls-remote origin`
  returns any refs.
---

# Profile Repo Bootstrap Campaign: from empty repo to shipped profile README

## EXPIRY NOTICE — read this before anything else

This campaign's premise is: **the repository is empty** (zero commits, zero branches,
zero refs), verified 2026-07-14. The whole campaign expires the moment that stops being
true. Check the premise NOW:

```
git ls-remote origin
```

- **EXPECTED (premise holds):** no output, exit code 0. Proceed with Phase 0.
- **If any refs are printed:** the repo is no longer empty. THE CAMPAIGN'S PREMISE IS
  STALE. Stop. Re-read the repo state (`git fetch origin && git branch -r`,
  `git log --oneline -20 origin/HEAD` if it exists), then update or retire this skill
  via `profile-repo-change-control`. Do not "run the campaign anyway".
- **If the command errors (exit nonzero, e.g. auth or network failure):** you cannot
  distinguish "empty" from "no access". Go to `profile-repo-debugging-playbook` and
  resolve access first.

Jargon, defined once:
- **Refs** — git's named pointers (branches, tags). An empty repo has none.
- **Unborn branch** — a local branch name that exists but has no commits yet
  (`git status` says "No commits yet"). Normal state in a fresh clone of an empty repo.
- **Default branch** — the branch GitHub shows by default and reads the profile README
  from. Model knowledge (2026-07-14): the FIRST branch pushed to an empty GitHub repo
  becomes its default branch.
- **Gate** — a checkpoint with an EXPECTED observation. You do not pass a gate on hope;
  you pass it on the stated observation. **No reader of this skill is authorized to
  skip a gate for any mutating git action.** If a gate fails, follow its branch
  instruction; never improvise a push.

Authoring note (honesty record): in the session that authored this skill (2026-07-14),
NO push to the repo's default branch was performed. The repo was still empty when this
file was written. Phases 3–6 below are therefore prescriptive, not a replay of history.

## The campaign at a glance

| Phase | Goal | Pass gate |
|---|---|---|
| 0 | Confirm premise, identity, remote | `git ls-remote origin` empty + exit 0 |
| 1 | Draft minimal README on a work branch | `README.md` exists at repo root, non-empty |
| 2 | Local validation with scripts | Audit script exits 0 |
| 3 | Review and land via change control | Reviewed; change-control checklist passed |
| 4 | First push (default-branch decision FIRST) | `git ls-remote origin` now non-empty |
| 5 | Live verification | README visible at https://github.com/rushikeshparadkar91 |
| 6 | Promote shipped state to golden state | Golden state recorded per validation-and-qa |

## Phase 0 — Preflight

**Step 0.1 — Confirm the empty-repo premise.**

```
git ls-remote origin
echo "exit=$?"
```

EXPECTED: no ref lines, `exit=0`.
- If refs appear → premise stale; see EXPIRY NOTICE above. Stop.
- If exit nonzero → access problem, not emptiness. Consult
  `profile-repo-debugging-playbook`; also see `profile-repo-build-and-env` for
  clone/remote mechanics.

Why this exact command: it is the discriminating test found in this repo's real
investigation (see `profile-repo-failure-archaeology`, entry dated 2026-07-14).
`git fetch origin` against an empty remote is a silent no-op (exit 0, no output) and is
easy to misread as a network failure; `git ls-remote` separates "empty" (exit 0, no
output) from "no access" (error).

**Step 0.2 — Confirm you are in the right clone on an expected branch.**

```
git remote -v
git status --short --branch
```

EXPECTED: remote named `origin` pointing at the profile repo; status shows
"No commits yet" on your branch (unborn branch — normal here).
- If `origin` is missing or points somewhere else → fix per
  `profile-repo-build-and-env` before continuing.
- If `git log` errors with `fatal: your current branch ... does not have any commits
  yet` (exit 128) at any point → that is the documented unborn-branch behavior, not a
  corruption. Carry on.

**Step 0.3 — Confirm commit identity.**

```
git config user.name
git config user.email
```

EXPECTED: both print a sensible value. If empty → set them (this configures your local
identity; it is not a repo mutation):

```
git config user.name  "Your Name"
git config user.email "rushikeshparadkar91@gmail.com"
```

## Phase 1 — Drafting: minimal viable README on a work branch

**Fenced-off wrong path:** do NOT start with automation, stats cards, or scheduled
workflows. The profile is unshipped; the first deliverable is a static README that
renders. Heavy machinery before a static baseline gives you nothing to diff against
and nothing to fall back to. Automation comes later via the solution menu (below) and
only through `profile-repo-change-control`.

**Step 1.1 — Get on a work branch.** Never work on the intended default branch
directly.
- Claude sessions: use the `claude/*` branch already assigned to the session
  (`git status --short --branch` shows it).
- Humans: create a feature branch:

```
git checkout -b feat/initial-readme
```

EXPECTED: `git status` shows the new branch, still "No commits yet".

**Step 1.2 — Write the minimal README.** Content template and house style live in
`profile-repo-docs-and-writing`; follow it. Minimal viable content is: name, role,
links. Nothing dynamic. Example skeleton (replace placeholders — do not ship
placeholders):

```
# Hi, I'm <Name> :wave:

<One-line role/description.>

- <Link 1: e.g. LinkedIn / portfolio>
- <Link 2: e.g. email>
```

Constraints (Model knowledge, 2026-07-14; details in `github-profile-reference`):
- File must be `README.md` at the REPO ROOT (not in a subdirectory).
- Renders as GitHub Flavored Markdown; `<script>`/`<iframe>`/`<style>` are stripped.
- The profile renders it only when the repo is PUBLIC and the file is on the DEFAULT
  branch and non-empty.

GATE 1: `README.md` exists at the repo root and is non-empty:

```
test -s README.md && echo OK
```

EXPECTED: `OK`. If not → you created it in the wrong place or it is empty; fix before
Phase 2.

## Phase 2 — Local validation

Run the repo's tested diagnostics instead of eyeballing. From the repo root:

```
python3 .claude/skills/profile-repo-diagnostics-and-tooling/scripts/readme-audit.py README.md
echo "exit=$?"
```

EXPECTED: `exit=0`.
- If nonzero → read the findings the script prints and fix each one, then re-run until
  exit 0. Do not proceed to review with a failing audit.
- If the script is missing at that path → list
  `.claude/skills/profile-repo-diagnostics-and-tooling/scripts/` and consult
  `profile-repo-diagnostics-and-tooling` for the current script names and their
  interpretation guides (e.g. `repo-state.sh` for repo state checks).

## Phase 3 — Review and land via change control

**Fenced-off wrong path:** never merge your own unreviewed work, and NEVER your own
unreviewed automation. All landing goes through `profile-repo-change-control`:
branch naming, change classification (this campaign's Phase 1 output is a CONTENT
change), and review gates are defined there. Content changes must also pass the
pre-merge checklist in `profile-repo-validation-and-qa` (evidence standards: what
counts as proof the change works).

GATE 3: the change has been reviewed per change control and the validation checklist is
green. Only then continue to Phase 4. This gate is not skippable by the reader of this
skill under any circumstances.

## Phase 4 — First push mechanics

**WARNING GATE — decide the default branch name BEFORE pushing.** Model knowledge
(2026-07-14): the first branch pushed to an empty GitHub repo becomes the repo's
DEFAULT branch, and the profile README renders only from the default branch. If you
push your work branch first, `feat/initial-readme` (or `claude/...`) becomes the
default — probably not what you want.

Decision to record (in the change-control record) before any push: the intended
default branch name. Convention: `main`.

**Step 4.1 — Put the reviewed commit on the intended default branch name locally.**
Assuming the reviewed work is on your work branch and the intended default is `main`:

```
git branch -m main        # if renaming your reviewed work branch in place, OR
git checkout -b main      # if branching off the reviewed tip
```

Pick one; EXPECTED: `git status --short --branch` shows `main` with your reviewed
commit(s) (`git log --oneline` shows them).

**Step 4.2 — Push the default branch FIRST.**

```
git push -u origin main
```

EXPECTED: push succeeds, output ends with `main -> main` and sets upstream.
- If rejected/auth error → do not retry blindly; consult
  `profile-repo-build-and-env` (push mechanics) and `profile-repo-debugging-playbook`.

**Step 4.3 — Verify refs now exist.**

```
git ls-remote origin
```

EXPECTED: NOW non-empty — at least `refs/heads/main` and a `HEAD` line pointing at it.
- If `HEAD` does not resolve to your intended default branch → fix the default branch
  in GitHub repo settings (Settings → Branches → Default branch) before Phase 5,
  because the profile reads the README from the default branch only.

Note: from this moment the EXPIRY NOTICE at the top of this skill is triggered — the
repo is no longer empty. Finish Phases 5–6, then update this skill's status via
`profile-repo-change-control`.

## Phase 5 — Live verification

Open https://github.com/rushikeshparadkar91 and confirm the README content renders at
the top of the profile page.

Rules of evidence (per `profile-repo-validation-and-qa`):
- A manual view is acceptable ONLY as the final check on top of passing scripts
  (Phase 2). It never replaces them.
- Model knowledge (2026-07-14): README changes usually appear within seconds;
  camo-proxied images can lag minutes to hours.

If the README does NOT show:
- Confirm the repo is PUBLIC (a private profile repo renders nothing). Check
  Settings → General → Danger Zone → visibility, or ask the owner.
- Confirm `README.md` is at the root of the DEFAULT branch and non-empty
  (`git ls-remote origin HEAD` + `git show origin/main:README.md` after a fetch).
- Then go to the symptom→triage table in `profile-repo-debugging-playbook`
  ("README not showing").

GATE 5: README visibly rendered on the profile page AND Phase 2 scripts pass on the
shipped commit.

## Phase 6 — Promotion: record the first golden state

Record the shipped state as the repository's FIRST golden state, following the
procedure in `profile-repo-validation-and-qa` (what to snapshot, where to record it).
Minimum facts to record: the commit SHA (`git rev-parse origin/main` after fetch), the
date, the audit-script version/output, and the observation "README renders on
profile". This gives every future change a known-good baseline to diff against.

## Ranked solution menu — WHAT to ship (in order)

Doctrine: no oversell. Nothing on this menu is "adopted" until it has been proven per
its listed proof obligation and landed via `profile-repo-change-control`. Options B–D
are CANDIDATES, none present in this repo today (2026-07-14). Long-horizon planning
for B–D lives in `profile-repo-roadmap-and-method`.

### A. Static minimal README — DO THIS FIRST (lowest risk)
- Prerequisites: none. This is Phases 1–6 above.
- Failure modes: wrong branch pushed first (default-branch trap, Phase 4); repo
  private; README not at root.
- Proof before "done": Phase 5 gate passed; golden state recorded.

### B. Badges via shields.io
- Prerequisites: A is live. Model knowledge (2026-07-14): shields.io serves stateless
  SVG badges from `img.shields.io`; third-party service.
- Failure modes: third-party outage renders broken images; GitHub proxies images
  through its camo CDN, so a fixed badge can look stale for minutes to hours.
- Proof before adopting: badge URL returns SVG when fetched directly; README with the
  badge passes Phase 2 audit; rendered profile shows the badge after camo cache warms.

### C. Stats cards (e.g. github-readme-stats)
- Prerequisites: A is live; accept a third-party dependency. Model knowledge
  (2026-07-14): the public github-readme-stats instance is rate-limited and cached.
- Failure modes: rate limiting makes cards intermittently blank — and a screenshot of
  a working card is NOT validation (it proves one lucky fetch, not reliability);
  self-hosting removes the rate limit but adds an ops surface (see roadmap).
- Proof before adopting: card URL fetched successfully on several occasions across
  hours (not one screenshot); documented fallback behavior when the card fails to
  load; landed via change control.

### D. Actions-driven dynamic README sections
- Prerequisites: A is live; B/C experience helpful; a reviewed workflow file under
  `.github/workflows/`. Highest risk — this is unreviewed-automation territory, and
  change control classifies it as an AUTOMATION change with stricter review.
- Failure modes: Model knowledge (2026-07-14): GitHub disables scheduled workflows
  after ~60 days without repo activity, so "set and forget" silently dies; a buggy
  workflow can commit garbage to the default branch — which is the live profile.
- Proof before adopting: the falsifiable milestone in
  `profile-repo-roadmap-and-method` — the workflow has run on schedule at least 3
  consecutive times with the README diff showing updated content each time.

## Fenced-off wrong paths (explicit)

| Wrong path | Why it is wrong | Do instead |
|---|---|---|
| Commit directly to the default branch | Bypasses review; the default branch IS the live profile | Work branch + change control (Phases 1, 3) |
| Push before deciding the default branch name | First pushed branch becomes default (Model knowledge 2026-07-14); profile reads only from default | Phase 4 warning gate |
| Ship scheduled workflows before a static README is live | No baseline, no fallback, automation risk on an unshipped profile | Option A first, D last |
| Trust a stats-card screenshot as validation | Proves one fetch, not reliability under rate limits | Option C proof obligation |
| Skip a gate on a mutating git action | Gates exist because each one caught or prevents a real failure mode | Gates are mandatory for every reader |
| Treat `git fetch` silence as network failure | Empty remote fetch is a silent no-op (observed 2026-07-14) | Discriminate with `git ls-remote origin` |

## When NOT to use this skill

- Repo already has commits/refs → this campaign has EXPIRED; use
  `profile-repo-change-control` for landing changes and
  `profile-repo-validation-and-qa` for verifying them.
- You need clone/push/environment mechanics in isolation →
  `profile-repo-build-and-env`.
- Something is broken and you're triaging a symptom →
  `profile-repo-debugging-playbook`.
- You're planning future dynamic-content directions, not shipping today →
  `profile-repo-roadmap-and-method`.
- You need platform facts (what makes a profile README render, GFM rules, caching) →
  `github-profile-reference`.
- You're writing README prose/templates → `profile-repo-docs-and-writing`.

## Provenance and maintenance

- Premise (repo EMPTY) verified 2026-07-14 in the authoring session:
  `git ls-remote origin` → no output, exit 0; GitHub API returned
  `409 Git Repository is empty`; local clone contained only `.git/` on an unborn
  branch. **Re-verify the premise every time this skill is loaded:**
  `git ls-remote origin` (empty + exit 0 = premise holds; any refs = skill expired,
  update via change control).
- No push to the repo's default branch was performed in the authoring session
  (2026-07-14); Phases 3–6 are prescriptive.
- Platform facts (first-push-sets-default, render conditions, camo caching, ~60-day
  scheduled-workflow disable, shields.io/github-readme-stats behavior) are Model
  knowledge (2026-07-14), NOT re-verifiable from the authoring sandbox
  (docs.github.com blocked). Re-verify from an unrestricted machine:
  `https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/customizing-your-profile/managing-your-profile-readme`
- Diagnostics script path re-check:
  `ls .claude/skills/profile-repo-diagnostics-and-tooling/scripts/`
- All edits to this skill go through `profile-repo-change-control`.
