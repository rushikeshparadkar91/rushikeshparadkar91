---
name: profile-repo-debugging-playbook
description: >
  Symptom→triage playbook for the GitHub profile repository
  rushikeshparadkar91/rushikeshparadkar91. Load this skill when something looks broken:
  a clone appears empty, git log dies with "does not have any commits yet", git fetch
  returns nothing, the README is not showing on the profile page, profile images are
  stale or broken, a scheduled GitHub Actions workflow stopped firing, or a badge/stats
  card renders as a broken image. Gives the first discriminating experiment for each
  symptom, how to read every outcome, and which wrong debugging paths to avoid.
---

# Profile repo: debugging playbook

Method: for every symptom, run **one cheap discriminating experiment first** — a single
command whose outcomes cleanly split the hypothesis space — before touching credentials,
config, or content. Jargon is defined in `profile-repo-build-and-env`; the short
version: an **empty repo** has zero refs on `origin`; an **unborn branch** is a local
branch with no commits yet; **camo** is GitHub's caching image proxy.

**State of the world when this playbook was written (2026-07-14): the repo is empty.**
Rows 1–3 below were hit and verified in this session against the real repo. Rows 4–8
are platform failure modes labeled Model knowledge (2026-07-14); they cannot occur
until the repo has content, but they are the realistic next failures.

## Triage table

| # | Symptom | First discriminating experiment | Outcomes → interpretation | Fix / escalation |
|---|---|---|---|---|
| 1 | Fresh clone contains no files; "where is the project?" | `git ls-remote origin` | **Empty output + exit 0** → the remote repo is genuinely empty; nothing was ever pushed. **Error + nonzero exit** → access/auth/network problem. | Empty: expected state as of 2026-07-14; to add content, see `profile-repo-bootstrap-campaign`. Error: fix credentials/network; in a Claude session remember `origin` is a session proxy. |
| 2 | `git log` fails: `fatal: your current branch '<X>' does not have any commits yet` (exit 128) | `git status` | "No commits yet" → unborn branch; the error is **normal**, there is no history to show. Anything else → investigate separately. | No fix needed. History will exist after the first commit. Do not re-clone, do not fsck. |
| 3 | `git fetch origin` prints nothing; `git branch -r` empty; "is the network down?" | `git ls-remote origin` | Empty output + exit 0 → remote is empty; fetch had nothing to transfer (verified: fetch exits 0 silently). Error → real connectivity/auth problem. | Empty: nothing to do. Error: only NOW debug network/credentials. |
| 4 | README pushed but not appearing on https://github.com/rushikeshparadkar91 — Model knowledge (2026-07-14) | Check the five display conditions in order: repo name == username exactly; repo public; `README.md` at repo **root**; on the **default branch**; non-empty. `git ls-remote origin` shows which branches exist; the repo's GitHub settings page shows default branch + visibility. | The first condition that fails is your cause. All five hold → wait ~1 min and hard-refresh; text normally appears within seconds. | Fix the failing condition (rename, make public, move/populate README, change default branch). Still broken with all five green → GitHub-side issue; check githubstatus.com from an unrestricted machine. |
| 5 | Image in README shows an OLD version after an update — Model knowledge (2026-07-14) | Open the image's `camo.githubusercontent.com` URL (from the rendered page's HTML) and compare with the raw source URL. | Raw URL new, camo URL old → camo cache staleness; can persist minutes to hours. Raw URL also old → your push didn't change what you think it changed. | Cache: wait, or change the image URL (new filename / cache-busting query param) to force a new camo entry. Wrong content: fix and re-push. |
| 6 | Relative image renders broken on the profile — Model knowledge (2026-07-14) | Does the path exist in the repo at the default branch? `git ls-tree -r <default-branch> --name-only \| grep <path>` | Missing → broken reference. Present but still flaky in some contexts → relative-path resolution issue. | Use an absolute raw URL: `https://raw.githubusercontent.com/rushikeshparadkar91/rushikeshparadkar91/<branch>/<path>`. Run `readme-audit.py` (diagnostics skill) to catch these before pushing. |
| 7 | Scheduled workflow (`on: schedule:`) silently stopped running — Model knowledge (2026-07-14) | In the repo's Actions tab: is there a banner saying scheduled workflows were disabled due to inactivity? Check the last run date. | Banner / last activity >~60 days ago → GitHub auto-disabled it (happens after ~60 days without repo activity). Recent activity but no runs → workflow file or cron syntax problem. | Disabled: re-enable in the Actions tab and make a commit to reset the clock. Syntax: validate the YAML and cron expression. (No workflows exist in this repo as of 2026-07-14.) |
| 8 | Badge or stats card (shields.io, github-readme-stats) shows as broken/placeholder — Model knowledge (2026-07-14) | Load the image URL **directly** in a browser (unrestricted machine — sandbox HTTPS is policy-filtered and 403s are misleading). | Direct load fails → third-party outage or rate limit (the public github-readme-stats instance is rate-limited/cached); not your README. Direct load works → your markdown/URL is malformed. | Outage/rate limit: wait, or self-host the stats card. Malformed: fix the URL; `link-inventory.py` (diagnostics skill) lists every URL for checking. |

## Wrong paths — explicitly fenced off

- **An empty `git fetch` is NOT a network failure.** Do not start debugging
  credentials, proxies, or DNS before running `git ls-remote origin`. Verified
  2026-07-14: against this empty repo, `fetch` exits 0 with no output.
- **`git log` exit 128 on an unborn branch is NOT repo corruption.** Do not run
  `git fsck`, do not re-clone, do not delete `.git`. It is the documented response to
  "no commits yet" (verified in-session).
- **A 403 from inside a Claude remote session is NOT proof a URL is dead.** Session
  network policy blocks `docs.github.com` (CONNECT 403) and unauthenticated
  `api.github.com` (verified 2026-07-14). Re-test from an unrestricted machine or via
  the GitHub MCP tools before declaring anything down.
- **Do not "fix" the `origin` URL in a Claude session.** It intentionally points at a
  session proxy. Rewriting it to a github.com URL breaks the session's authentication.
- **Do not debug README rendering by repeatedly force-pushing tweaks.** Run the five
  display conditions (row 4) once, in order; and remember image staleness (row 5) is a
  cache, not your markdown.

## Escalation

If a discriminating experiment produces an outcome not listed here, record it —
symptom, command, exact output, interpretation — as a new entry via
`profile-repo-failure-archaeology`, which owns the incident chronicle and its template.

## When NOT to use this skill

- Nothing is broken and you're setting up a clone or tracing the publish pipeline →
  use `profile-repo-build-and-env`.
- You want scripted, repeatable measurement (repo state report, README static audit,
  link inventory) rather than one-off triage → use `profile-repo-diagnostics-and-tooling`.
- You're recording or consulting the history of past incidents →
  `profile-repo-failure-archaeology`.

## Provenance and maintenance

Rows 1–3 and the sandbox-network fence were observed against the real repo on
**2026-07-14**. Rows 4–8 are Model knowledge (2026-07-14). One-line re-verification:

| Fact | Re-verification command |
|---|---|
| Empty repo signature | `git ls-remote origin; echo $?` → no output, `0` |
| Unborn-branch `git log` failure | `git log; echo $?` → fatal "does not have any commits yet", `128` |
| Silent fetch on empty remote | `git fetch origin && git branch -r` → no output |
| Sandbox policy 403s | `curl -sSI https://docs.github.com/` → 403 |
| Profile display conditions (row 4) | https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/customizing-your-profile/managing-your-profile-readme (unrestricted machine) |
| ~60-day scheduled-workflow disable (row 7) | GitHub Actions docs on `schedule` events (unrestricted machine) |

Once the repo is no longer empty, rows 1–3 change from "current state" to "historical
trap" — update the preamble in the same change that lands content.
