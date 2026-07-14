---
name: profile-repo-validation-and-qa
description: >-
  Defines what counts as EVIDENCE that a change to
  rushikeshparadkar91/rushikeshparadkar91 actually worked. Load this skill
  before merging or declaring any change done: it gives the evidence
  hierarchy (script output > reproducible git/API checks > manual
  screenshot), the pre-merge checklist per change class (content vs
  automation), the acceptance rule (verification commands recorded in the
  PR/commit description), the certified-artifact inventory (currently
  empty), and the procedure for adding new checks. Also load it when
  someone claims "it works" without recorded evidence, or when defining
  the first golden state for the README.
---

# Validation and QA — What Counts as Evidence

A change to this repository is not done when it is written; it is done when
its stated verification passes and the evidence is recorded. This skill
defines the evidence standard.

Context (verified 2026-07-14): the repository is EMPTY — zero commits, zero
branches, zero refs (`git ls-remote origin` returns nothing with exit 0).
Everything below therefore applies first to the bootstrap changes that will
create the initial content, and then to all changes after.

## 1. The evidence hierarchy

When claiming a change worked, cite the strongest available tier. Lower tiers
supplement; they do not replace higher ones that are available.

| Tier | Evidence type | Properties | Example |
|---|---|---|---|
| 1 (strongest) | Output of a tested script from `profile-repo-diagnostics-and-tooling/scripts/` | Deterministic, repeatable, interpretation guide ships with the script | `readme-audit.py` run exits 0 with zero findings |
| 2 | A reproducible read-only git or API check, command and output recorded verbatim | Anyone can re-run it and compare | `git ls-remote origin` now lists `refs/heads/main`; `git show origin/main:README.md \| head -1` shows the expected first line |
| 3 (weakest) | Screenshot or manual view of the live profile page | Not reproducible, subject to caching (camo images can be hours stale — see `github-profile-reference` §3), observer-dependent | Screenshot of https://github.com/rushikeshparadkar91 showing the README |

Rules:

- Tier 3 is a **last resort** and is **never sufficient alone for automation
  changes** (workflows, scheduled jobs). An automation change needs tier 1 or
  tier 2 evidence that the automation itself behaves, not just that the page
  looks right once.
- Tier 3 IS the only way to confirm final live rendering of the profile page,
  so content changes typically end with a tier 3 check — after tiers 1–2 pass.
- "I looked at it and it seemed fine" with no recorded command or capture is
  tier 0: not evidence.

## 2. Pre-merge checklist by change class

Change classes follow `profile-repo-change-control` (content vs automation vs
governance).

### Content change (README, images, links)

- [ ] `readme-audit` passes — the audit script in
      `profile-repo-diagnostics-and-tooling/scripts/` runs with zero findings.
      (If that script does not exist yet in your checkout, that is expected at
      genesis — see §4 — and you must fall back to tier 2 checks and say so.)
- [ ] All links resolve: extract links (diagnostics tooling) and confirm each
      returns a non-error response, or record why a link cannot be checked
      from the current environment (e.g., network policy — verified blocked
      for docs.github.com in the authoring sandbox on 2026-07-14).
- [ ] The Markdown renders correctly in a Markdown preview (any GFM-capable
      previewer) — tables, task lists, and any sanitized-HTML elements look
      as intended. GFM specifics: `github-profile-reference` §2.
- [ ] Content complies with `profile-repo-docs-and-writing` (evidence-linked
      claims, external positioning rules).

### Automation change (workflows, scheduled jobs, scripts)

- [ ] Workflow YAML validates — at minimum parses as YAML
      (`python3 -c "import yaml,sys; yaml.safe_load(open(sys.argv[1]))" <file>`),
      and preferably passes a dedicated workflow linter if one has been added
      to diagnostics tooling.
- [ ] Dry-run where possible: run the workflow's script locally with
      side-effects disabled, or trigger a manual `workflow_dispatch` run on a
      branch, and record the output.
- [ ] Rollback plan stated IN the PR/commit description: the exact command or
      revert that undoes the change, and how you'd know it needs undoing.
- [ ] The ~60-day scheduled-workflow inactivity disable is acknowledged for
      any `on: schedule:` workflow (see `github-profile-reference` §5), with a
      stated mitigation or an explicit acceptance of the risk.

### Governance change (skill edits, process changes)

- [ ] Complies with the maintenance style in `profile-repo-docs-and-writing` §4.
- [ ] Cross-references to sibling skills still point at real skills
      (`ls .claude/skills/`).

## 3. Acceptance discipline

**A change is DONE only when its stated verification commands pass.**

Procedure:

1. Before implementing, write down the verification commands that will define
   done for the change.
2. Implement.
3. Run the commands. If any fails, the change is not done — no exceptions, no
   "will verify after merge".
4. Record **both the command and its output** (verbatim or trimmed with an
   ellipsis note) in the PR description or commit message body.
5. A reviewer (or future maintainer) must be able to re-run the same commands
   and get the same result.

A PR/commit with no recorded verification is treated as unverified regardless
of what its description asserts.

## 4. Certified inventory

**EMPTY as of 2026-07-14.** No golden artifacts exist yet — the repository has
zero commits, so nothing has ever been verified, certified, or shipped. Do not
cite any "known-good" prior state; there is none.

**Jargon — golden artifact / golden state**: a specific, committed artifact
whose verification evidence is recorded, which subsequent changes are compared
against.

What would qualify as the FIRST golden artifact: a root `README.md` on the
default branch that (a) passes the diagnostics audit script (e.g.,
`readme-audit.py`) with zero findings, with the run recorded, and (b) is
confirmed displaying correctly on the live profile page (tier 3 check,
performed after tiers 1–2). When that exists, update this section — via
`profile-repo-change-control` — to record the commit hash, the audit output,
and the date. Until then, this inventory stays honestly empty.

## 5. Adding new checks

New verification checks are welcome but disciplined:

1. **Where they live**: scripts go in
   `.claude/skills/profile-repo-diagnostics-and-tooling/scripts/` — one home
   for all measurement tooling. Do not scatter ad-hoc check scripts elsewhere
   in the repo.
2. **Tested before cited**: a check must be run at least once against a known
   input, with its observed output recorded in the diagnostics skill's
   interpretation guide, BEFORE any PR cites it as evidence. An untested
   checker is not evidence of anything.
3. **Added via change control**: introducing or modifying a check is a
   governance/automation change and goes through
   `profile-repo-change-control`. This skill's checklists are then amended to
   reference the new check.

## When NOT to use this skill

- Running or interpreting the measurement scripts themselves →
  `profile-repo-diagnostics-and-tooling`.
- Deciding whether a change is allowed and how it lands (branching, review,
  classification) → `profile-repo-change-control`.
- Diagnosing why something is broken (as opposed to proving something works)
  → `profile-repo-debugging-playbook`.
- Writing the content being validated → `profile-repo-docs-and-writing`.

## Provenance and maintenance

Authored 2026-07-14 at repository genesis. The certified inventory is empty
because the repo is empty — verified that day: `git ls-remote origin` returned
zero refs (exit 0), and the GitHub REST API (authenticated MCP, earlier in the
authoring session) returned `409 Git Repository is empty`. No verification
history predates this document.

One-line re-verification commands:

| Fact | Command |
|---|---|
| Repo still empty / first push landed | `git ls-remote origin` (no output = still empty) |
| Diagnostics scripts available | `ls .claude/skills/profile-repo-diagnostics-and-tooling/scripts/` from the repo root |
| Certified inventory still empty | Search this file's §4 for recorded commit hashes (none = still empty) |
| Live profile rendering (tier 3) | Open https://github.com/rushikeshparadkar91 in a browser — manual, weakest tier |

Amendments to this skill go through `profile-repo-change-control`.
