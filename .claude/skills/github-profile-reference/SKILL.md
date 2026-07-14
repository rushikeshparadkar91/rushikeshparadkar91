---
name: github-profile-reference
description: >-
  Domain knowledge pack for the special GitHub profile repository
  (rushikeshparadkar91/rushikeshparadkar91). Load this skill when you need
  platform facts: when and why the profile README displays or hides, the
  default-branch rule for empty repos, GitHub Flavored Markdown (GFM)
  rendering behavior in profile READMEs (tables, task lists, emoji
  shortcodes, sanitized HTML), image handling via the camo proxy, relative
  vs absolute image URLs, the third-party badge/stats ecosystem
  (shields.io, github-readme-stats), or GitHub Actions basics for public
  repos including the scheduled-workflow inactivity disable. Also load it
  to check which facts are verified in-session vs model knowledge vs mere
  candidates.
---

# GitHub Profile Repository — Reference

Domain knowledge a mid-level engineer typically lacks about GitHub's special
profile repository feature, scoped to how it applies to THIS repository.

## Read this first: the three fact classes

Every fact in this skill belongs to exactly one class. Do not treat a lower
class as a higher one.

| Class | Meaning | How to trust it |
|---|---|---|
| **VERIFIED-IN-SESSION (2026-07-14)** | Observed directly with a read-only command in the authoring sandbox on 2026-07-14 | Re-run the recorded command; it should reproduce |
| **MODEL-KNOWLEDGE (2026-07-14)** | GitHub platform behavior as of the authoring model's training data. docs.github.com was unreachable from the authoring sandbox (verified policy 403), so it could NOT be re-verified at authoring time | Re-verify against https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/customizing-your-profile/managing-your-profile-readme before relying on it for an irreversible action |
| **CANDIDATE** | A third-party option that COULD be adopted here. Not a decision, not present in the repo | Adoption requires change control (see `profile-repo-change-control`) |

### Verified-in-session facts (2026-07-14)

- The repository `rushikeshparadkar91/rushikeshparadkar91` is **EMPTY**: zero
  commits, zero branches, zero refs. Evidence: `git ls-remote origin` returns
  no output with exit 0; the GitHub REST API (via authenticated MCP earlier in
  the authoring session) returned `409 Git Repository is empty`.
- The local clone is on an **unborn branch** ("No commits yet").
- From the authoring sandbox, `docs.github.com` is blocked by network policy
  (CONNECT 403) and unauthenticated `api.github.com` returns HTTP 403. Platform
  facts below therefore could not be re-verified at authoring time.

Everything in the sections that follow is **Model knowledge (2026-07-14) —
docs.github.com unreachable from the authoring sandbox (verified policy 403)**
unless marked otherwise. Canonical re-verification URL for all of it:
https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/customizing-your-profile/managing-your-profile-readme

## 1. How the special profile repository works

*Model knowledge (2026-07-14) — docs.github.com unreachable from the authoring
sandbox (verified policy 403). Re-verify:
https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/customizing-your-profile/managing-your-profile-readme*

**Jargon — default branch**: the branch GitHub treats as the repository's
primary branch (what you see first on the repo page, and where the profile
README is read from).

Display conditions — ALL four must hold before the README appears at the top
of https://github.com/rushikeshparadkar91:

| # | Condition | Status in this repo (verified 2026-07-14) |
|---|---|---|
| 1 | Repo is named exactly the username (`rushikeshparadkar91`) | Holds — the repo exists under that name |
| 2 | Repo is public | Existence confirmed via authenticated API; visibility not independently re-verified in-session |
| 3 | `README.md` exists at the ROOT of the DEFAULT branch | Does NOT hold — repo is empty |
| 4 | The README is non-empty | Does NOT hold — no README exists |

Hiding the profile README later: make the repo private, rename it, or
remove/empty the README. Any one suffices.

**Default-branch rule for empty repos**: the FIRST branch pushed to an empty
GitHub repository becomes its default branch. Because this repo is empty as of
2026-07-14, the very first push decides where the profile README must live.
Push deliberately (see `profile-repo-bootstrap-campaign` for the campaign and
`profile-repo-build-and-env` for push mechanics).

Propagation: README changes usually appear on the profile page within seconds;
camo-proxied images (see §3) can stay stale for minutes to hours.

## 2. GFM rendering in profile READMEs

*Model knowledge (2026-07-14) — docs.github.com unreachable from the authoring
sandbox (verified policy 403). Re-verify:
https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/customizing-your-profile/managing-your-profile-readme*

**Jargon — GFM**: GitHub Flavored Markdown, GitHub's Markdown dialect.

What works in a profile README:

- **Tables** — pipe syntax renders normally.
- **Task lists** — `- [ ]` / `- [x]` render as checkboxes (read-only in a README).
- **Emoji shortcodes** — `:wave:` renders as the emoji.
- **Sanitized HTML subset** — inline HTML is allowed but sanitized. `<script>`,
  `<iframe>`, and `<style>` are stripped. Commonly surviving elements include
  `<img>`, `<a>`, `<details>`/`<summary>`, `<sub>`/`<sup>`, `<br>`, and
  `align` attributes on some elements. If a layout depends on CSS or JS, it
  will not work — design within plain GFM plus the sanitized subset.

Checklist before shipping HTML in the README:

- [ ] No `<script>`, `<iframe>`, or `<style>` anywhere.
- [ ] Layout degrades gracefully if an HTML attribute is stripped.
- [ ] Rendering confirmed per `profile-repo-validation-and-qa` (markdown
      preview, then live check).

## 3. Image handling

*Model knowledge (2026-07-14) — docs.github.com unreachable from the authoring
sandbox (verified policy 403). Re-verify:
https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/customizing-your-profile/managing-your-profile-readme*

**Jargon — camo**: GitHub's anonymizing image proxy. Every external image in
rendered Markdown is rewritten to a `camo.githubusercontent.com` URL and
cached there.

Consequences:

| Behavior | Implication for this repo |
|---|---|
| Camo caches images | An updated image at the same URL can show a stale version for minutes to hours. To bust the cache, change the URL (e.g., a query param or new filename) |
| Relative image paths resolve within the repo | `![x](assets/pic.png)` works on the repo page, but for reliability across contexts prefer absolute raw URLs |
| Absolute raw URL form | `https://raw.githubusercontent.com/<user>/<repo>/<branch>/<path>` — pin `<branch>` to the default branch once one exists |

As of 2026-07-14 this repo has NO images and NO assets directory — the rules
above apply to future content.

## 4. Third-party ecosystem catalog

**None of these are present in this repo as of 2026-07-14; all are candidates,
not decisions.** Adopting any of them goes through `profile-repo-change-control`.
The rows below are *Model knowledge (2026-07-14) — docs.github.com unreachable
from the authoring sandbox (verified policy 403); re-verify each project's own
docs plus
https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/customizing-your-profile/managing-your-profile-readme*.

| Candidate | What it is | Key caveats |
|---|---|---|
| shields.io badges (`img.shields.io`) | Stateless SVG badges (language, license, social counts) generated per-request from URL parameters | Third-party availability dependency; images pass through camo caching (§3); every badge must earn its place per `profile-repo-docs-and-writing` |
| anuraghazra/github-readme-stats | Self-hostable stats cards (contribution stats, top languages) rendered as SVG images | Public instance is rate-limited and cached — cards can be stale or intermittently fail; self-hosting shifts the burden to you |
| GitHub Actions scheduled workflows | `.github/workflows/*.yml` with `on: schedule:` cron, regenerating README sections (recent posts, activity) on a timer | Requires a rollback plan and dry-run per `profile-repo-validation-and-qa`; subject to the inactivity disable in §5 |

## 5. GitHub Actions basics for public repos

*Model knowledge (2026-07-14) — docs.github.com unreachable from the authoring
sandbox (verified policy 403). Re-verify:
https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/customizing-your-profile/managing-your-profile-readme*

- Actions minutes are **free for public repositories**.
- Workflows live at `.github/workflows/*.yml` on the default branch.
- **Inactivity disable**: GitHub disables SCHEDULED workflows after roughly
  **60 days without repository activity**. A "set and forget" cron workflow on
  a dormant profile repo WILL silently stop. Mitigations (all candidates):
  keep the repo active, re-enable manually when notified, or have the workflow
  make commits that count as activity.
- No workflows exist in this repo as of 2026-07-14 (verified: repo is empty).

## When NOT to use this skill

- Deciding what this repo's invariants ARE (as opposed to what the platform
  does) → `profile-repo-architecture-contract`.
- Actually taking the repo from empty to a shipped README →
  `profile-repo-bootstrap-campaign`.
- Writing or styling README content → `profile-repo-docs-and-writing`.
- Verifying that a change worked → `profile-repo-validation-and-qa`.
- Debugging "README not showing" symptoms → `profile-repo-debugging-playbook`.

## Provenance and maintenance

Authored 2026-07-14 at repository genesis (repo empty, zero commits). Sources:
the session ground-truth brief plus model knowledge as labeled per section.
No platform fact here was re-verifiable in the authoring sandbox
(docs.github.com CONNECT 403; unauthenticated api.github.com HTTP 403 —
both verified in-session 2026-07-14).

One-line re-verification commands:

| Fact | Command |
|---|---|
| Repo still empty / refs present | `git ls-remote origin` (no output + exit 0 = empty; refs listed = no longer empty; error = access problem) |
| Local branch state | `git status` (look for "No commits yet") |
| docs.github.com reachability from current environment | `curl -sSI https://docs.github.com/ -o /dev/null -w '%{http_code}\n'` |
| All platform facts (display rules, GFM, camo, Actions disable) | Open https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/customizing-your-profile/managing-your-profile-readme from an unrestricted machine |
| Ecosystem candidates still exist / unchanged | Check https://shields.io and https://github.com/anuraghazra/github-readme-stats from an unrestricted machine |

Amendments to this skill go through `profile-repo-change-control`.
