---
name: profile-repo-change-control
description: >-
  Load this skill before landing ANY change in this repository — content, automation,
  or governance. Trigger situations: "commit this", "push this", "merge this", "ship
  the README", "add a workflow", "edit a skill", "can I push straight to main", "what
  branch should I use", the first-ever push to this empty repo, force-push or history
  rewrite requests, or any request to bypass review ("just push it directly"). Also
  load it when creating or amending any SKILL.md, since skills are governed artifacts.
  If a proposed action touches the default branch, repo visibility, repo name, or
  .github/workflows, this skill is mandatory reading first.
---

# Profile Repo Change Control

## Founding statement — read this first

This repository has **no history**: as of 2026-07-14 it is empty (zero commits,
zero branches — evidence: `git ls-remote origin` returned nothing; GitHub API
returned `409 Git Repository is empty`). There is therefore no inherited process
to follow. **This document DEFINES the initial change-control regime.** It is the
project's founding governance, effective 2026-07-14, and it is amendable — but
only via its own process (see "Amending a skill file" below).

**No skill, script, automation, or session convention may route around this
process.** If another document conflicts with this one, this one wins until
amended.

Definitions used below:
- **Default branch**: the branch GitHub treats as the repo's primary branch; the profile README must live at its root (see `profile-repo-architecture-contract`). It does not exist yet — the first push creates it.
- **PR (pull request)**: GitHub's review-and-merge mechanism for landing a branch into another branch.
- **Force-push**: `git push --force`/`--force-with-lease`; rewrites the remote branch's history destructively.

## Change classification

Classify every change before starting work. If a change spans classes, apply the
strictest applicable gates.

| Class | What it covers | Examples |
|---|---|---|
| **profile-content** | Anything rendered on the public profile | `README.md`, images/assets it references |
| **automation-workflows** | Anything that executes | `.github/workflows/*.yml`, scripts, scheduled jobs, hooks |
| **governance-and-skills** | The rules and the skill library itself | `.claude/skills/**`, this document, repo settings (name, visibility, default branch, branch protection) |

## Gates per class

| Gate | profile-content | automation-workflows | governance-and-skills |
|---|---|---|---|
| Develop on a non-default branch | Required | Required | Required |
| Land via PR (never direct commit to default branch, once it exists) | Required | Required | Required |
| Human review before merge | Required (it is the owner's public face) | Required — **no unreviewed automation, ever** | Required |
| Render/behavior verification before merge | Preview Markdown; after merge, confirm on the live profile page | Dry-run or manual `workflow_dispatch` run before enabling any schedule | Confirm skill loads and does not contradict siblings or this document |
| Invariant check (name, visibility, root README on default branch) | Required if the change touches README location/emptiness | Required if the workflow writes to the README or default branch | Required if repo settings change |
| Note in `profile-repo-failure-archaeology` | Only if the change followed a non-trivial investigation | Same | Same |

## Branch-then-review discipline

1. **Never commit directly to the default branch once it exists.** All work lands via PR from a topic branch.
2. **Claude sessions develop on `claude/*` branches.** This is grounded in this session's own convention — the authoring session itself runs on the unborn branch `claude/skill-library-handoff-2jwx7q` (verify: `git branch --show-current`). Human topic branches may use any clear prefix (e.g. `feat/`, `fix/`), but `claude/*` is reserved for Claude sessions.
3. **The first push is special.** Because the first branch pushed to an empty GitHub repo becomes the default branch (Model knowledge, 2026-07-14 — re-verify at `https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/customizing-your-profile/managing-your-profile-readme`), the first push must be the deliberately chosen default branch (e.g. `main`), pushed by or with the explicit approval of the owner — never a `claude/*` working branch pushed first by accident. See `profile-repo-bootstrap-campaign` for the full sequence.
4. One logical change per branch/PR. Do not bundle a README rewrite with a new workflow.

Pre-merge checklist (every PR):

- [ ] Change classified (table above) and strictest gates identified.
- [ ] Branch is not the default branch; Claude work is on `claude/*`.
- [ ] Diff reviewed by a human (the owner, at this project's current single-maintainer scale).
- [ ] Display invariants from `profile-repo-architecture-contract` still hold after the change.
- [ ] No non-negotiable (below) is violated.
- [ ] Volatile facts touched by the change carry a date stamp.

## The non-negotiables, with rationale

Each rationale below is reasoned from this repo's structure — not from past
incidents, because no history exists to cite.

| Rule | Rationale |
|---|---|
| **Never force-push the default branch.** | The profile README is the owner's public face, and in a repo with no CI and no tests, git history is the **only audit trail** — the sole record of what was public when, and the only rollback mechanism. Rewriting it destroys both. |
| **No unreviewed automation.** | A scheduled workflow runs unattended and writes to the public profile; a broken one silently rots — and GitHub disables schedules after ~60 days of repo inactivity (Model knowledge, 2026-07-14), so failure modes are quiet by design. Review is the only checkpoint an unattended job ever gets. |
| **Never make the repo private, rename it, or empty the root README without explicit owner sign-off.** | Any one of these three actions instantly removes the README from the public profile (display invariants — see `profile-repo-architecture-contract`). They are one-click outage buttons. |
| **No skill or automation may route around change control.** | A rule that can be bypassed by writing a new rule is not a rule. Skills instruct future sessions; a skill that licenses direct pushes would launder violations into "documented process". |
| **No fabricated history, incidents, or metrics anywhere in the repo.** | The skill library's authority rests entirely on being verifiable; one invented fact poisons trust in all of them. Everything is either verified-with-command or labeled "Model knowledge (date)". |
| **First push only lands the deliberately chosen default branch.** | It permanently fixes the default branch on an empty repo (Model knowledge, 2026-07-14); recovering from a wrong choice requires settings surgery on a live public profile. |

## Amending a skill file (including this one)

Skills are **governance-and-skills** class. To amend one:

1. Branch (`claude/*` for Claude sessions).
2. Edit the `SKILL.md`; update its "Provenance and maintenance" section and date stamps; keep `name:` equal to the directory name.
3. Check the cross-reference map: do sibling skills still point at the right place? Update "When NOT to use this skill" sections if scope moved.
4. If amending **this** document: state in the PR description which rule/gate changed and why. The non-negotiables table may only be weakened with explicit owner approval recorded in the PR.
5. PR + human review + merge, like any other change. A skill edit that lands without this path is invalid and should be reverted via a follow-up PR (not a force-push).

## When NOT to use this skill

- You need to know **what must stay true** (invariants, weak points) rather than **how a change lands** → use `profile-repo-architecture-contract`.
- You need to know **what evidence proves a change worked** (pre-merge verification detail, rendering checks) → use `profile-repo-validation-and-qa`.
- You are writing or styling README/skill **content** → use `profile-repo-docs-and-writing`.
- You are executing the first-push campaign itself → use `profile-repo-bootstrap-campaign` (it operates within, never around, this process).

## Provenance and maintenance

Founding version authored 2026-07-14 at repository genesis. No prior process
existed; nothing here is inherited. Re-verify volatile facts:

| Volatile fact | One-line re-verification |
|---|---|
| Repo still empty / default branch now exists | `git ls-remote origin | head` (output listing refs means the default branch exists — the "once it exists" clauses are now live) |
| Current session branch convention | `git branch --show-current` (expect a `claude/*` name in Claude sessions) |
| Default-branch-on-first-push rule; scheduled-workflow disabling (~60 days) | `https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/customizing-your-profile/managing-your-profile-readme` from an unrestricted machine |
| Whether branch protection exists on the default branch | GitHub repo settings UI, or GitHub MCP tools when connected (unauthenticated api.github.com is blocked in this sandbox, verified 2026-07-14) |

Amend only via the process defined in this document. Effective 2026-07-14.
