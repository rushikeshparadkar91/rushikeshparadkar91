---
name: profile-repo-docs-and-writing
description: >-
  House style guide for rushikeshparadkar91/rushikeshparadkar91. Load this
  skill when writing or editing the profile README (tone, structure, section
  template, badge policy, evidence-linked claims), when authoring or amending
  any SKILL.md in this library (voice, tables, date-stamping, mandatory
  sections, one-home-per-fact rule), or when deciding whether content is
  appropriate for a public-facing personal page (external positioning:
  no unverifiable claims, credentials, private contact info, or
  employer-confidential material).
---

# Docs and Writing — House Style

**Status: FOUNDING style guide, effective 2026-07-14.** No README exists yet
(the repo is empty as of 2026-07-14 — zero commits; verify with
`git ls-remote origin`), so this document DEFINES the initial house style
rather than describing an existing one. It is amendable via
`profile-repo-change-control`; until amended, it is binding on all README
content and all skill-library edits.

## 1. README content principles

**Audience**: recruiters and potential collaborators skimming for roughly
10 seconds. Write for the skim first; depth is optional and linked, never
front-loaded.

| Principle | Rule | Why |
|---|---|---|
| Lead with who/what | The first visible line states who the owner is and what they do. No banner-first, no greeting-only openers | The 10-second skim starts at the top |
| Scannable sections | Short sections with clear headings; bullets over paragraphs; one idea per bullet | Skimmers read headings and the first bullet |
| Every badge earns its place | A badge appears only if it communicates something a skimmer needs AND stays accurate without manual upkeep. No badge walls | Badge walls read as noise and rot silently |
| No unevidenced claims | Do not claim a skill, project, or achievement that cannot be linked to evidence (a repo, a post, a verifiable profile). If it can't be linked, it doesn't go in | Mirrors this project's no-oversell doctrine (see `profile-repo-change-control`) |
| Keep it current or keep it timeless | Anything that dates ("currently building X") must either be maintained or rewritten in timeless form | A stale "currently" line is worse than none |

Pre-publish checklist for README content:

- [ ] First line answers "who is this and what do they do".
- [ ] Every claim of skill/project links to evidence.
- [ ] Every badge individually justified (would a skimmer miss it?).
- [ ] Nothing violates §3 (external positioning).
- [ ] Passes the verification steps in `profile-repo-validation-and-qa`.

## 2. README section template

Founding template (defined 2026-07-14, not yet instantiated — the repo has no
README). Use it as the starting skeleton; sections marked *optional* may be
dropped, and any structural departure goes through change control.

```markdown
# Hi, I'm <Name>

<One sentence: role/craft + current focus. Evidence-linkable, no adjectives
you can't back.>

## What I work on

- <Area or project — link to the repo/post that proves it>
- <Area or project — link>

## Selected work

| Project | What it is | Link |
|---|---|---|
| <name> | <one line> | <URL> |

## How to reach me

- <Public, deliberate channels only — e.g., GitHub, LinkedIn, a public
  website. See the external positioning rules before adding anything.>

<!-- optional -->
## Currently

- <Only if you commit to keeping it fresh; otherwise delete this section.>
```

Formatting rules for the README itself: plain GFM first; sanitized-HTML
tricks (e.g., `<details>`) only when GFM cannot express the layout — see
`github-profile-reference` §2 for what survives sanitization. Prefer absolute
raw URLs for images per `github-profile-reference` §3.

## 3. External positioning

This is a **public-facing personal page**. Anyone — recruiters, strangers,
scrapers — can read it. Hard rules, not style preferences:

- Never publish unverifiable claims (titles, affiliations, or achievements
  that can't be checked).
- Never publish credentials, tokens, or keys of any kind.
- Never publish private emails or phone numbers. Contact channels must be
  public and deliberate.
- Never publish employer-confidential information: internal project names,
  unreleased work, org details, or anything covered by an NDA.
- When in doubt, leave it out — removal after indexing/scraping does not undo
  exposure.

## 4. Skill-library maintenance style

Rules for writing and amending any `.claude/skills/*/SKILL.md` in this repo:

| Rule | Detail |
|---|---|
| Imperative runbook voice | Write instructions as commands to a zero-context mid-level engineer or Sonnet-class model: "Run X", "Check Y". Not "one might consider" |
| Tables and checklists | Prefer a table or checklist over prose whenever the content is enumerable |
| Define jargon once | First use of a term of art (GFM, camo, default branch, unborn branch) gets a one-line definition in that skill; later uses go bare |
| Date-stamp volatile facts | Any fact that can change (repo state, platform behavior, third-party services) carries its as-of date, e.g. "(2026-07-14)" |
| Label fact classes | Distinguish verified-in-session, model-knowledge, and candidate facts, following the labeling scheme in `github-profile-reference` |
| Mandatory sections | Every skill MUST contain a "When NOT to use this skill" section (pointing at the correct sibling) and a final "Provenance and maintenance" section with one-line re-verification commands |
| One home per fact | Each fact lives in exactly ONE skill; every other skill that needs it cross-references by skill name and section instead of restating it. Duplicated facts drift |
| Frontmatter | YAML with `name:` matching the directory name and a trigger-rich `description:` saying exactly when to load the skill |
| No invention | No invented history, incidents, metrics, or configs. The repo's emptiness (as of 2026-07-14) is stated plainly wherever relevant |
| Copy-pasteable commands | Commands must run as written from the repo root; refer to the remote as `origin`, never a session-specific URL or absolute sandbox path |

Amendment procedure: skill edits are governance-class changes and go through
`profile-repo-change-control` like any other change.

## When NOT to use this skill

- Platform facts (what GFM renders, how camo caches, display conditions) →
  `github-profile-reference`.
- Whether a change may land at all, and how → `profile-repo-change-control`.
- Proving a written change actually works → `profile-repo-validation-and-qa`.
- Getting the first README shipped from the current empty state →
  `profile-repo-bootstrap-campaign`.

## Provenance and maintenance

Authored 2026-07-14 at repository genesis as the FOUNDING style guide — there
was no prior README or style practice to describe (repo verified empty that
day via `git ls-remote origin`, which returned zero refs). All rules here are
definitions made effective 2026-07-14, not descriptions of precedent.

One-line re-verification commands:

| Fact | Command |
|---|---|
| README still absent / now present | `git ls-remote origin` (empty output = no README anywhere) — once refs exist: `git fetch origin && git show origin/HEAD:README.md \| head -5` |
| Skill library contents | `ls .claude/skills/` from the repo root |
| This guide still the current style authority | Check `profile-repo-change-control` records for amendments dated after 2026-07-14 |

Amendments to this skill go through `profile-repo-change-control`.
