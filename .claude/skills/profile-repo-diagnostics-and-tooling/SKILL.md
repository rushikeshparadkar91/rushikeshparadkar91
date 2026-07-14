---
name: profile-repo-diagnostics-and-tooling
description: >
  Tested diagnostic scripts and interpretation guides for the GitHub profile repository
  rushikeshparadkar91/rushikeshparadkar91. Load this skill when you want to MEASURE
  instead of eyeball: get a one-shot repo state report (remote refs, branch, commits,
  README, workflows, verdict), statically audit a README.md for broken relative images /
  bare http links / unsafe HTML / heading problems, or extract a complete inventory of
  every URL and image in a markdown file (with optional live checking). Also load it
  when deciding whether a repo is empty vs. inaccessible, or before pushing README
  changes, as a pre-flight check.
---

# Profile repo: diagnostics & tooling

Principle: **measure, don't eyeball.** Every check below is a script in this skill's
`scripts/` directory — dependency-free bash or python3 stdlib, read-only, no mutating
git commands. Run them from the repo root (or pass explicit paths).

All three scripts were **written and executed in this sandbox on 2026-07-14**:
`repo-state.sh` against the real repo in its empty state; `readme-audit.py` and
`link-inventory.py` against a synthetic fixture README created in the session
scratchpad (the repo has no README.md yet, so a fixture was the only way to exercise
the finding paths — the fixture is NOT part of the repo). Quoted outputs below are the
actual observed outputs; the fixture's temporary directory path is abbreviated as
`<fixture-dir>` because session paths are not stable.

| Script | Question it answers | Exit codes |
|---|---|---|
| `scripts/repo-state.sh` | "What state is this repo actually in?" | 0 = report + verdict; 2 = not a git repo / remote unreachable |
| `scripts/readme-audit.py` | "Is this README statically sound before I push it?" | 0 = clean; 1 = findings; 2 = usage error |
| `scripts/link-inventory.py` | "What URLs/images does this markdown reference?" | 0 = table printed; 2 = usage/file error |

---

## 1. repo-state.sh — one-shot state report

```bash
.claude/skills/profile-repo-diagnostics-and-tooling/scripts/repo-state.sh [repo-root]
```

Reports origin refs, local branch, commit count, README.md presence/size, and
`.github/workflows` contents, then emits a single machine-greppable `VERDICT:` line.
Handles the empty-repo case explicitly.

**Observed output against the real repo, 2026-07-14 (exit 0):**

```
== repo-state report: /home/user/rushikeshparadkar91 ==
remote-refs      : 0 ref(s) on origin
local-branch     : claude/skill-library-handoff-2jwx7q
local-commits    : 0 (unborn branch — 'No commits yet')
README.md        : MISSING at repo root
workflows        : none (.github/workflows absent)
VERDICT: EMPTY-REPO — origin has zero refs and the local branch is unborn. Nothing has ever been pushed.
```

**Also observed (error path):** run against a non-git directory it prints
`ERROR: '.' is not a git repository` and exits 2.

### Interpretation guide

| Line / verdict | Meaning | Next action |
|---|---|---|
| `remote-refs : 0 ref(s)` | `git ls-remote origin` returned empty with exit 0 — the remote is genuinely empty, not unreachable | None; this is the repo's state as of 2026-07-14 |
| `remote-refs : ERROR ...` + `VERDICT: REMOTE-UNREACHABLE` | ls-remote itself failed — a real access/auth/network problem, explicitly distinguished from emptiness | Debug credentials/network; see debugging playbook row 1 |
| `local-commits : 0 (unborn branch ...)` | Local branch has no commits; `git log` will exit 128 here — that is normal | Nothing; expected pre-genesis |
| `README.md : MISSING` / `EMPTY file` | No renderable profile content; an empty README does not render on the profile | Author README via bootstrap-campaign / change control |
| `workflows : none` | No GitHub Actions automation exists | Only relevant once automation is proposed (roadmap skill) |
| `VERDICT: EMPTY-REPO` | Nothing ever pushed anywhere | Expected 2026-07-14 |
| `VERDICT: LOCAL-ONLY` | You have commits that origin has never seen | Publish via change control, or you're mid-work — fine |
| `VERDICT: BEHIND-REMOTE` | Origin has refs your clone hasn't checked out | `git fetch origin` then check out a remote branch |
| `VERDICT: NORMAL` | Both sides have history | Use `git status` for fine-grained drift |

---

## 2. readme-audit.py — static README audit

```bash
.claude/skills/profile-repo-diagnostics-and-tooling/scripts/readme-audit.py path/to/README.md
```

Offline static checks: existence/non-emptiness, relative image references whose target
file is missing on disk, bare `http://` links, HTML tags outside a conservative
GFM-safe allowlist, and heading-structure problems (no headings at all, or levels that
jump, e.g. H1 → H4). Content inside ``` code fences is ignored. Exits 1 if it prints
any `FINDING` line — suitable as a pre-push gate.

The HTML allowlist inside the script is **Model knowledge (2026-07-14)** — a
conservative subset of what GitHub's GFM sanitizer keeps. A flagged tag means "verify
rendering manually", not "proven broken".

**Observed against the real repo path, 2026-07-14 (exit 1):**

```
FINDING [missing]: /home/user/rushikeshparadkar91/README.md does not exist
```

**Observed against the synthetic fixture, 2026-07-14 (exit 1) — fixture contained one
`http://` link, two missing relative images, a `<marquee>`, and an H1→H4 jump:**

```
FINDING [bare-http] line 5: http://example.com/insecure (use https://)
FINDING [broken-relative-image] line 7: 'assets/banner.png' not found relative to <fixture-dir>
FINDING [broken-relative-image] line 10: 'assets/also-missing.svg' not found relative to <fixture-dir>
FINDING [html-outside-allowlist] line 11: <marquee> — not in the conservative GFM-safe allowlist (Model knowledge 2026-07-14); verify rendering manually
FINDING [html-outside-allowlist] line 11: <marquee> — not in the conservative GFM-safe allowlist (Model knowledge 2026-07-14); verify rendering manually
FINDING [heading-jump] line 3: H1 jumps to H4 (skipped a level)
RESULT: 6 finding(s)
```

(Note: a flagged tag is reported once per occurrence — opening and closing tags each
count, hence `<marquee>` appearing twice for one element.)

### Interpretation guide

| Finding tag | Meaning | Next action |
|---|---|---|
| `[missing]` / `[empty]` | No README, or whitespace-only — will not render on the profile | Create/populate it; expected while repo is empty |
| `[broken-relative-image]` | Image path doesn't exist relative to the README's directory — renders broken | Add the asset, or switch to an absolute raw URL (`https://raw.githubusercontent.com/<user>/<repo>/<branch>/<path>`) |
| `[bare-http]` | Plain `http://` link | Change to `https://` |
| `[html-outside-allowlist]` | Tag not in the conservative safe subset; GitHub may strip it | Prefer pure markdown, or verify on a rendered preview |
| `[heading-jump]` / `[no-headings]` | Structural readability problem | Fix heading levels; cosmetic, not a render blocker |
| `RESULT: clean — no findings` (exit 0) | Passed all static checks | Safe to proceed to live verification (validation-and-qa skill) |

A clean exit 0 does NOT prove links are alive or that GitHub renders everything as
intended — it is a static gate only. Pair with `link-inventory.py` and the
`profile-repo-validation-and-qa` checklist.

---

## 3. link-inventory.py — URL/image inventory

```bash
.claude/skills/profile-repo-diagnostics-and-tooling/scripts/link-inventory.py path/to/README.md [--check]
```

Default mode is **offline**: prints one table row per reference —
`KIND | LINE | URL`, where KIND is `image-md`, `image-html`, `link-md`, or `link-auto`
(bare URL in prose). Code fences are **not** skipped: the inventory is exhaustive by
design (observed: a URL inside a fence was listed). Duplicates keep their own rows so
line numbers stay useful.

**Observed against the synthetic fixture, 2026-07-14, offline mode (exit 0):**

```
KIND | LINE | URL
-----|------|----
link-auto | 5 | http://example.com/insecure
image-md | 7 | assets/banner.png
image-md | 8 | https://raw.githubusercontent.com/rushikeshparadkar91/rushikeshparadkar91/main/assets/banner.png
image-html | 10 | assets/also-missing.svg
link-md | 13 | https://example.org
link-auto | 13 | https://example.net/page
link-auto | 16 | http://ignored.example
TOTAL: 7 reference(s)
```

`--check` adds a STATUS column via HTTP HEAD (5s timeout, stdlib only). **Warning,
demonstrated live:** in Claude remote sessions outbound HTTPS is policy-filtered, so
`--check` results from inside a session are only partially trustworthy.

**Observed with `--check` from this sandbox, 2026-07-14 (exit 0), abridged:**

```
image-md | 8 | https://raw.githubusercontent.com/.../main/assets/banner.png | ERR:HTTPError:HTTP Error 404: Not Found
link-md | 13 | https://example.org | ERR:URLError:<urlopen error Tunnel connection failed: 403 Fo
link-auto | 13 | https://example.net/page | ERR:URLError:<urlopen error Tunnel connection failed: 403 Fo
```

Read that carefully — it demonstrates both cases in one run:
`raw.githubusercontent.com` was reachable and returned a **genuine 404** (the asset
really doesn't exist — the repo is empty), while `example.org`/`example.net` failed
with **`Tunnel connection failed: 403`**, which is the sandbox policy proxy, NOT a dead
site.

### Interpretation guide

| Output | Meaning | Next action |
|---|---|---|
| `image-md` / `image-html` row with a relative URL | Resolves inside the repo; fragile on the profile page | Prefer absolute raw URLs; `readme-audit.py` checks existence |
| `link-auto` row | Bare URL in prose | Fine; just know it's a live reference to maintain |
| STATUS `200`/`3xx` | Target answered | Nothing |
| STATUS `ERR:HTTPError:HTTP Error 404` | Host reachable, resource missing — a real broken link | Fix the URL or add the asset |
| STATUS contains `Tunnel connection failed: 403` | Sandbox network policy block — NOT evidence the link is dead | Re-check from an unrestricted machine before "fixing" anything |
| STATUS `ERR:URLError:...Name or service not known` | DNS failure — bogus hostname or no route | Verify the hostname; if it's real, re-check outside the sandbox |
| `skipped(non-http)` | Relative/anchor/mailto reference — HEAD not applicable | Covered by `readme-audit.py` instead |

---

## When NOT to use this skill

- You need to **interpret a failure** and choose between hypotheses — the scripts feed
  evidence into `profile-repo-debugging-playbook`; the reasoning lives there.
- You're setting up an environment or tracing how pushes go live →
  `profile-repo-build-and-env`.
- You need the definition of "change verified / done" (acceptance evidence, pre-merge
  checklist) → `profile-repo-validation-and-qa`; these scripts are inputs to that
  checklist, not a substitute for it.

## Provenance and maintenance

All scripts live in `scripts/` beside this file, are executable, and were tested
**2026-07-14** in this sandbox: `repo-state.sh` against the real repo in its **empty**
state (plus its non-git error path); `readme-audit.py` and `link-inventory.py` against
a **synthetic scratchpad fixture** (not committed anywhere) because the repo has no
README yet. The HTML allowlist in `readme-audit.py` and the "GFM-safe" framing are
Model knowledge (2026-07-14).

| Volatile fact | One-line re-verification |
|---|---|
| Repo still empty | `./scripts/repo-state.sh <repo-root>` → `VERDICT: EMPTY-REPO` |
| Scripts still runnable | `bash -n scripts/repo-state.sh && python3 -m py_compile scripts/*.py` |
| Audit exit semantics | `./scripts/readme-audit.py /nonexistent; echo $?` → finding + `1` |
| Inventory offline mode | `./scripts/link-inventory.py <any-md-file>; echo $?` → table + `0` |
| Sandbox 403 behavior under `--check` | `./scripts/link-inventory.py <md-with-external-url> --check` → `Tunnel connection failed: 403` inside a session |
| HTML allowlist accuracy | Compare against GitHub's GFM sanitization docs from an unrestricted machine |

Once the repo has a real README, re-run `readme-audit.py` and `link-inventory.py`
against it and replace the fixture-based example outputs here with real ones.
