---
name: profile-repo-architecture-contract
description: >-
  Load this skill whenever you need the load-bearing design facts of this repository
  before touching anything: what the special GitHub profile repo is, the invariants
  that must hold for the profile README to display, why the first push matters, and
  the known-weak points. Trigger situations: "what is this repo", "why is this repo
  empty", "why isn't the README showing on the profile", "can I rename this repo",
  "can I make this repo private", "which branch should the README live on", "what
  breaks if I change X", onboarding a new session into this repo, or any change that
  could affect repo name, visibility, default branch, or root README.md. Also load it
  before writing any new skill or automation, to avoid violating an invariant.
---

# Profile Repo Architecture Contract

## What this repository IS

This is `rushikeshparadkar91/rushikeshparadkar91` on GitHub — the **special profile
repository**. "Profile repository" means: a repo whose name exactly matches the
owner's username. When such a repo is public and has a non-empty `README.md` at the
root of its default branch, GitHub renders that README at the top of the owner's
profile page (`https://github.com/rushikeshparadkar91`).

Consequence: this repo's `README.md` is a **public-facing artifact**, not internal
documentation. Every change to it is effectively a production deploy to the owner's
public profile.

## Current state (verified 2026-07-14)

| Fact | State on 2026-07-14 | How verified |
|---|---|---|
| Remote refs | **Zero** — the repo is empty (no commits, no branches, no tags) | `git ls-remote origin` returned no output (exit 0); GitHub API returned `409 Git Repository is empty` |
| Default branch | **Does not exist yet** | Follows from zero refs |
| Local clone | Contains only `.git/` plus this skill library under `.claude/` | `ls -la` at the repo root |
| Local branch | Unborn branch (a branch name that exists but has no commits yet); `git status` says "No commits yet" | `git status` |
| Build system / tests / CI / docs / issues | **None exist** | Empty repo; nothing to inspect |

This is repository **genesis**. There is no history to consult. Any claim about
"how things were done before" in this repo is fabricated by definition.

## The display invariants (Model knowledge, 2026-07-14)

STATUS: Model knowledge as of training cutoff Jan 2026; internally consistent but
NOT re-verifiable from this sandbox (docs.github.com is network-blocked here).
Re-verify from an unrestricted machine at:
`https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/customizing-your-profile/managing-your-profile-readme`

ALL of the following must hold simultaneously for the profile README to display:

- [ ] Repo is named **exactly** the username: `rushikeshparadkar91`.
- [ ] Repo is **public**.
- [ ] `README.md` exists at the **root** of the **default branch** (not in a subdirectory, not on a side branch).
- [ ] The README is **non-empty**.

Break any one and the profile README disappears. Deliberate hiding uses the same
levers: make the repo private, rename it, or remove/empty the README.

Supporting platform facts (same Model-knowledge label and re-verification pointer):

| Fact | Implication for this repo |
|---|---|
| README renders as GitHub Flavored Markdown (GFM): tables, task lists, emoji shortcodes like `:wave:`, and a sanitized HTML subset (no `<script>`, `<iframe>`, `<style>`) | Do not build content that depends on scripts or embeds; it will be stripped |
| Images are proxied through GitHub's camo CDN and cached; relative image paths resolve within the repo | For reliability, prefer absolute raw URLs: `https://raw.githubusercontent.com/<user>/<repo>/<branch>/<path>` |
| Profile page caching: README text changes usually appear within seconds; camo-proxied images can stay stale for minutes to hours | "Image looks old" is often a cache artifact, not a failed push |
| GitHub disables scheduled Actions workflows after ~60 days without repo activity | Any future cron-based README automation will silently stop on an inactive repo |

## Why the first push is architecturally significant

**The first branch pushed to an empty GitHub repo becomes its default branch**
(Model knowledge, 2026-07-14 — same re-verification pointer as above).

Because this repo currently has zero refs, the very next successful push is a
one-way architectural decision: it fixes the default branch name, and the default
branch is where the display invariants attach (root `README.md` must live there).
Therefore:

1. Choose the intended long-term default branch name (e.g. `main`) deliberately, before pushing.
2. Do NOT let a working branch (e.g. a `claude/*` session branch) become the default by pushing it first.
3. The first push is a governed change — see `profile-repo-change-control`. Do not ad-hoc it.

## Known-weak points (stated plainly)

| Weakness | Why it matters | Mitigation available today |
|---|---|---|
| No CI, no tests | Nothing mechanically checks a change before it lands; a broken README ships as-is | Manual pre-merge checklist (see `profile-repo-validation-and-qa` if present) |
| Platform behavior unverifiable from this sandbox | docs.github.com → CONNECT 403; unauthenticated api.github.com → HTTP 403 in Claude remote sessions for this project (verified 2026-07-14). Sanctioned API path here is the GitHub MCP tools, when connected | Label platform facts as Model knowledge; re-verify from an unrestricted machine |
| Third-party stats/badge services (shields.io, github-readme-stats, etc.) are external dependencies | If adopted, profile rendering quality depends on services this repo does not control; public instances are rate-limited/cached. None are present in this repo today | Treat as "candidate" only; adopt via change control |
| Rendering can only be confirmed on github.com itself | Local Markdown preview approximates but does not equal GitHub's sanitizer/renderer | Verify on the live profile page after push |
| Empty repo produces misleading tool output | `git fetch` on an empty remote is a silent no-op; `git log` on an unborn branch exits 128 | See `profile-repo-failure-archaeology` entries 2026-07-14-01/03 |

## When NOT to use this skill

- You need to know **how to land a change** (branching, review, gates) → use `profile-repo-change-control`.
- You need the **broader platform/ecosystem knowledge pack** (GFM details, badges, stats cards, Actions ecosystem) → use `github-profile-reference`.
- You are debugging a symptom or recording an investigation → use `profile-repo-debugging-playbook` / `profile-repo-failure-archaeology`.
- You are executing the zero-to-shipped-README campaign → use `profile-repo-bootstrap-campaign`.

## Provenance and maintenance

Compiled 2026-07-14 at repository genesis, from in-sandbox verification plus
labeled model knowledge. Re-verify volatile facts before relying on them:

| Volatile fact | One-line re-verification |
|---|---|
| Repo still empty / default branch existence | `git ls-remote origin | head` (no output + exit 0 = still empty; refs listed = genesis is over, update this skill) |
| Local branch state | `git status && git branch --show-current` |
| Display invariants and default-branch rule | Open `https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/customizing-your-profile/managing-your-profile-readme` from an unrestricted machine |
| Sandbox network policy (docs/api blocked) | `curl -sSI https://docs.github.com -o /dev/null -w '%{http_code}\n'` (403 = still blocked in-sandbox) |
| Live profile rendering | View `https://github.com/rushikeshparadkar91` in a browser after any README change |

Amend this skill only via the process in `profile-repo-change-control`
(governance-and-skills class). Update the state table and date stamps whenever
`git ls-remote origin` stops returning empty.
