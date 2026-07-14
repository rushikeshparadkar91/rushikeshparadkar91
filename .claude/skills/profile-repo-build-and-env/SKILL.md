---
name: profile-repo-build-and-env
description: >
  Environment setup and publish-pipeline guide for the GitHub profile repository
  rushikeshparadkar91/rushikeshparadkar91. Load this skill when you need to: clone or
  re-clone the repo, set up a working environment from scratch, understand why a fresh
  clone looks empty, understand unborn-branch / empty-remote git behavior, make the
  first push, or trace how a README change actually reaches the live profile page
  (push → render pipeline). Also load it before trusting network access inside a Claude
  remote session for this project.
---

# Profile repo: build & environment

## What you are working on

`rushikeshparadkar91/rushikeshparadkar91` is a **GitHub profile repository**: a repo whose
name exactly matches the owner's username. When it has a public default branch with a
non-empty `README.md` at the root, GitHub renders that README at the top of
https://github.com/rushikeshparadkar91.

**Central fact (verified 2026-07-14): the repository is EMPTY.** Zero commits, zero
branches, zero refs on `origin`. There is no build system, no test suite, no CI, and no
git history. "Building" this project means: get a working clone, author markdown, and
push it. There is nothing to compile.

Jargon, defined once:

| Term | Meaning |
|---|---|
| **Empty repo** | A repo created on GitHub that has never received a push. `git ls-remote origin` prints nothing. |
| **Unborn branch** | A local branch name that exists but points at no commit yet (`git status` says "No commits yet"). Every clone of an empty repo starts on one. |
| **Default branch** | The branch GitHub shows by default and reads the profile README from. An empty repo has none until the first push. |
| **camo** | GitHub's image-proxying CDN. All images in rendered READMEs are served (and cached) through it. |

## Cloning

### On a normal developer machine

```bash
git clone https://github.com/rushikeshparadkar91/rushikeshparadkar91.git
# or SSH:
git clone git@github.com:rushikeshparadkar91/rushikeshparadkar91.git
```

While the repo is empty, `git clone` succeeds but warns
`warning: You appear to have cloned an empty repository.` That warning is **expected and
harmless** in the current state.

### In a Claude remote session

The repo arrives **pre-cloned** at the session's repo root. `origin` points at a
session-local authenticated proxy, **not** at github.com directly. Do not copy that
remote URL anywhere, do not hardcode it in scripts, and do not "fix" it — always address
the remote as `origin`. On any other machine, reconstruct the remote from the public
URLs above.

## Empty-repo / unborn-branch mechanics (all verified 2026-07-14 in-session)

These are the behaviors that make a fresh clone of this repo look "broken". They are
normal. Real command output observed against this repo:

1. **`git status`** on the pre-cloned repo:

   ```
   On branch claude/skill-library-handoff-2jwx7q
   No commits yet
   nothing to commit (create/copy files and use "git add" to track)
   ```

   "No commits yet" == unborn branch.

2. **`git log`** on an unborn branch fails loudly:

   ```
   fatal: your current branch 'claude/skill-library-handoff-2jwx7q' does not have any commits yet
   ```

   Exit code **128**. This is not corruption — there is simply no history to show.

3. **`git ls-remote origin`** against the empty remote: **no output, exit 0.**
   Empty output with a zero exit code is the signature of an empty repo. (An access or
   network problem makes `ls-remote` print an error and exit nonzero — that difference
   is the fastest discriminating test; see the debugging playbook.)

4. **`git fetch origin`** against the empty remote: silent no-op, **exit 0, no output**,
   and `git branch -r` stays empty afterward. Easy to misread as a network failure. It
   is not one — there are no refs to fetch.

## How the first push works

Model knowledge (2026-07-14), platform behavior not verifiable from this sandbox:
**the first branch pushed to an empty GitHub repo becomes its default branch.** So the
branch name used for the genesis push is a real decision, not a detail — whatever you
push first (e.g. `main`) is what GitHub will read the profile README from.

Do not perform the genesis push casually. The push itself must go through change
control — see the `profile-repo-change-control` skill, and the
`profile-repo-bootstrap-campaign` skill for the full phased plan from empty repo to
shipped README.

## Push → profile-render pipeline

Model knowledge (2026-07-14) — GitHub platform behavior; re-verify at
https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/customizing-your-profile/managing-your-profile-readme
(note: that URL is unreachable from Claude remote sessions — see traps below).

```
edit README.md → commit → push to default branch on origin
   → GitHub renders README.md as GitHub Flavored Markdown (GFM)
   → profile page https://github.com/rushikeshparadkar91 updates
```

- Display conditions — ALL must hold: repo named exactly the username; repo **public**;
  `README.md` at the **root** of the **default branch**; README **non-empty**.
- Text changes usually appear on the profile within seconds of the push.
- Images are proxied through camo and cached: image changes can lag by minutes to hours
  even after the markdown text has updated.
- GFM sanitizes HTML (no `<script>`, `<iframe>`, `<style>`); tables, task lists, and
  emoji shortcodes (`:wave:`) work.

## Known traps in Claude remote sessions (verified 2026-07-14 in this sandbox)

Outbound network is policy-filtered. Observed in this session:

| Attempt | Observed result | Consequence |
|---|---|---|
| `curl https://docs.github.com/...` | CONNECT 403 (policy denial) | GitHub docs are **unreachable** from the sandbox. Cite them as pointers; verify from an unrestricted machine. |
| Unauthenticated `api.github.com` | HTTP 403 "GitHub access is not enabled for this session" | The public REST API is unreachable without the GitHub MCP connector. Do not diagnose this 403 as a repo problem. |
| Sanctioned path | GitHub MCP tools, when connected | Use MCP for any GitHub API question from inside a session. |

Corollary: any script that fetches URLs (link checking, badge probing) may return 403
from inside a session **because of policy, not because the target is down**.

## From-scratch checklist

| # | Step | Command | Expected while repo is empty (2026-07-14) |
|---|---|---|---|
| 1 | Clone (normal machine) | `git clone https://github.com/rushikeshparadkar91/rushikeshparadkar91.git` | Succeeds with "cloned an empty repository" warning |
| 1' | Clone (Claude session) | none — pre-cloned; remote is `origin` | Repo root present; `origin` is a session proxy |
| 2 | Confirm identity of remote | `git remote -v` | One remote named `origin` |
| 3 | Confirm repo state | `git ls-remote origin` | **No output, exit 0** (empty repo) |
| 4 | Confirm local state | `git status` | "No commits yet" (unborn branch) |
| 5 | Do NOT panic at | `git log` (exit 128), silent `git fetch`, empty `git branch -r` | All normal for an empty repo |
| 6 | One-shot state report | run `repo-state.sh` from the diagnostics skill | `VERDICT: EMPTY-REPO` |
| 7 | Author content | edit `README.md` at repo root | n/a (nothing to build) |
| 8 | Publish | via change control only — see `profile-repo-change-control` / `profile-repo-bootstrap-campaign` | First pushed branch becomes the default branch |
| 9 | Verify render | open https://github.com/rushikeshparadkar91 from an unrestricted machine | README appears at top of profile |

## When NOT to use this skill

- Something is **failing or looks wrong** and you need symptom→cause triage →
  use `profile-repo-debugging-playbook`.
- You want to **measure** the repo/README state with tested scripts instead of running
  ad-hoc commands → use `profile-repo-diagnostics-and-tooling`.
- You are planning the actual genesis push / first README → use
  `profile-repo-bootstrap-campaign` (via change control).

## Provenance and maintenance

Verified in-session on **2026-07-14** against the real repo unless labeled
"Model knowledge (2026-07-14)". Re-verify each volatile fact in one line:

| Fact | Re-verification command |
|---|---|
| Repo is empty (zero refs) | `git ls-remote origin` → empty output, exit 0 |
| Local branch unborn | `git status` → "No commits yet" |
| `git log` fails on unborn branch | `git log; echo $?` → fatal message, 128 |
| `git fetch` silent no-op | `git fetch origin && git branch -r` → no output |
| Sandbox blocks GitHub docs/API | `curl -sSI https://docs.github.com/ ; curl -sS https://api.github.com/` → 403s |
| Profile README display rules | https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/customizing-your-profile/managing-your-profile-readme (from an unrestricted machine) |
| First push creates default branch | Same docs page; or observe after genesis push |

If any check disagrees with this file (e.g. the repo is no longer empty), update this
skill in the same change that lands the new state.
