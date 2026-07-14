---
name: profile-repo-roadmap-and-method
description: >-
  The roadmap of CANDIDATE future directions for the profile repo
  rushikeshparadkar91/rushikeshparadkar91 (dynamic README via scheduled Actions,
  stats/metrics cards, self-hosted stats, README as living index of pinned projects)
  plus the METHOD for turning any idea into an adopted change: hypothesis with
  predicted observables stated BEFORE running anything, one mechanism explaining ALL
  observations, adversarial refutation pass, lifecycle candidate → experiment →
  adopted/retired. Load this skill when: asked "what should we do next", "should we
  add stats/badges/automation", "make the README dynamic", "is this idea worth it";
  when evaluating an experiment's results; or when deciding whether to adopt or retire
  a change. Do NOT load for shipping the first README to the still-empty repo — that
  is profile-repo-bootstrap-campaign.
---

# Roadmap and Method: candidate directions, and the discipline for adopting them

Baseline fact (verified 2026-07-14): this repository is EMPTY — no commits, no CI, no
workflows, no README. Everything in the roadmap half of this skill is therefore a
**CANDIDATE**: an idea nobody has decided to do, let alone done. Nothing here is a
commitment, a plan of record, or a description of existing functionality. The starting
asset this repo actually has is a governed skill library with tested diagnostics
(`profile-repo-diagnostics-and-tooling`) and a change-control process
(`profile-repo-change-control`). Every candidate below builds on that asset, not on
imagined infrastructure.

Prerequisite for ALL candidates: a static README shipped via
`profile-repo-bootstrap-campaign`. Do not start any candidate before that campaign's
Phase 6 (golden state recorded) is complete.

Jargon, defined once:
- **CANDIDATE** — labeled idea; not decided, not started, not promised.
- **Falsifiable milestone** — a "you have a result when…" statement specific enough
  that a specific observation could prove it FALSE.
- **Discriminating experiment** — a test whose possible outcomes separate two
  competing explanations (each outcome is only compatible with one of them).
- **Adversarial pass** — a second session or agent whose explicit job is to try to
  refute your conclusion, not to confirm it.

---

## Half A — ROADMAP (all items CANDIDATE, none decided, 2026-07-14)

### CANDIDATE 1: Dynamic README via scheduled GitHub Actions

- **Why the naive approach fails/risks:** "add a cron workflow and forget it" dies
  silently — Model knowledge (2026-07-14): GitHub disables scheduled workflows after
  ~60 days without repo activity. Also, the workflow commits to the default branch,
  which IS the live profile, so a bug ships garbage publicly with no review.
- **This repo's starting asset:** the governed skill library — change control
  classifies workflow files as AUTOMATION changes with stricter review, and the
  diagnostics scripts give a machine check of the README after each bot commit.
- **First three concrete steps in this repo:**
  1. Draft `.github/workflows/update-readme.yml` on a branch (never on default) with
     the smallest possible job: update one clearly-delimited section of README.md.
  2. Add a post-update check to the job: run
     `.claude/skills/profile-repo-diagnostics-and-tooling/scripts/readme-audit.py README.md`
     and fail the job on nonzero exit, so a bad bot edit never lands.
  3. Land via `profile-repo-change-control` as an AUTOMATION change; record in the
     change record who watches the first scheduled runs and the ~60-day-inactivity
     expiry risk.
- **You have a result when…** the workflow has run on schedule at least 3 consecutive
  times AND the README diff shows updated content each time (check: the Actions run
  list shows 3+ scheduled successes; `git log -p -- README.md` shows a distinct bot
  commit per run). Any missed scheduled run or empty diff falsifies the milestone.

### CANDIDATE 2: Stats/metrics integration (e.g. github-readme-stats cards)

- **Why the naive approach fails/risks:** "paste the card URL and screenshot it" —
  Model knowledge (2026-07-14): the public github-readme-stats instance is
  rate-limited and cached, so cards go intermittently blank; GitHub proxies README
  images through its camo CDN, which can serve stale images for minutes to hours. One
  successful screenshot proves one lucky fetch, nothing more.
- **This repo's starting asset:** the validation doctrine
  (`profile-repo-validation-and-qa`): evidence standards already define why a
  screenshot is insufficient, and the diagnostics scripts can extract and check the
  README's links/image URLs mechanically.
- **First three concrete steps in this repo:**
  1. On a branch, add ONE stats card to a clearly-delimited README section.
  2. Fetch the card URL directly (e.g. `curl -sS -o /dev/null -w "%{http_code}\n" "<card-url>"`)
     at several separated times across a day; record the results in the change record.
  3. Write down the degraded-mode behavior (what the profile looks like when the card
     fails to load) before requesting review via `profile-repo-change-control`.
- **You have a result when…** the card URL has returned HTTP 200 with SVG content on
  checks spread across at least 24 hours (not one burst), the README passes the audit
  script, and the rendered profile shows the card. Repeated non-200s or blank cards
  falsify it — then either retire the candidate (document in
  `profile-repo-failure-archaeology`) or escalate to CANDIDATE 3.

### CANDIDATE 3: Self-hosted stats to remove the third-party dependency

- **Why the naive approach fails/risks:** self-hosting (Model knowledge 2026-07-14:
  github-readme-stats is self-hostable) removes the shared rate limit but replaces a
  dependency with an OPS SURFACE: a deployment that can go down, needs a token with
  the right scopes, and now has its own failure modes. Naively deploying "because the
  public instance rate-limits" without first PROVING the rate limit is your problem
  (CANDIDATE 2's measurements) is solving an unconfirmed problem.
- **This repo's starting asset:** CANDIDATE 2's recorded fetch measurements — if they
  exist, they are the evidence that decides whether this candidate is worth it at all.
- **First three concrete steps in this repo:**
  1. Confirm the prerequisite evidence exists: CANDIDATE 2's change record shows
     repeated public-instance failures. No evidence → stop; this candidate is premature.
  2. Document the chosen hosting target and its token/scope requirements in a design
     note on a branch (a governance/automation change per change control).
  3. Stand up the instance, point ONE card at it in a branch's README, and run the
     same multi-hour fetch checks as CANDIDATE 2 against the self-hosted URL.
- **You have a result when…** the self-hosted card passes the same 24-hour fetch
  criterion that the public instance FAILED, and the switchover lands via change
  control with the verification commands recorded. If the self-hosted instance is not
  measurably more reliable than the public one, retire the candidate and record why.

### CANDIDATE 4: Profile README as a living index of pinned projects

- **Why the naive approach fails/risks:** a hand-maintained project list rots — links
  break and descriptions drift, and nothing detects it. The failure is silent because
  a stale-but-rendering README looks fine at a glance. (Automating the list re-invokes
  all of CANDIDATE 1's risks.)
- **This repo's starting asset:** the diagnostics scripts' link extraction/checking
  (see `profile-repo-diagnostics-and-tooling`) — rot can be MEASURED instead of
  noticed by accident.
- **First three concrete steps in this repo:**
  1. On a branch, add a delimited "Projects" section to README.md listing each project
     with a one-line description and link, per `profile-repo-docs-and-writing` style.
  2. Run the diagnostics link extraction over README.md and record the checked-URL
     list and results in the change record.
  3. Land via change control, and add a recurring re-check note (manual cadence first;
     automation only via CANDIDATE 1's path).
- **You have a result when…** the section is live on the profile AND a link re-check
  run at least two weeks later still passes (or its failures were detected by the
  script rather than by a visitor). A visitor-reported dead link that the process
  missed falsifies the maintenance claim.

---

## Half B — METHOD: how an idea becomes an adopted change here

The discipline, in order. Skipping a step is how unproven changes end up live on a
public profile page.

### B.1 State the hypothesis BEFORE running anything

Write down, before any command is run:
1. The hypothesis, in one sentence.
2. The predicted observables — numbers or concrete outcomes you expect to see if the
   hypothesis is true (e.g. "the card URL will return HTTP 200 on 10/10 fetches over
   24h", "the workflow will produce 3 scheduled runs with non-empty README diffs").
3. What observation would REFUTE it.

A prediction written after seeing the data is not a prediction. If you cannot state a
refuting observation, the idea is not yet testable — sharpen it first.

### B.2 One mechanism must explain ALL observations — including negatives

When interpreting results, the accepted explanation must account for every
observation, including the absent/negative ones (the command that printed nothing, the
error that did NOT occur). If your mechanism explains the successes but you have to
shrug at one anomaly, you do not have the mechanism yet.

### B.3 Adversarial pass

Before promoting a conclusion, assign a second session or agent an explicit refutation
brief: "here is the claim, here is the evidence, try to break it — propose at least
one alternative mechanism and the experiment that would discriminate." The conclusion
survives only if the adversary's alternatives are ruled out by evidence, not by
preference. Record the adversarial pass's outcome in the change record.

### B.4 Lifecycle

| Stage | Meaning | Where it lives |
|---|---|---|
| **candidate** | Idea with a written hypothesis and falsifiable milestone; no repo changes | This skill's roadmap |
| **experiment** | Running on a BRANCH, gated — never on the default branch; predictions written per B.1 | Branch + change record |
| **adopted** | Landed via `profile-repo-change-control`, with the verification commands RECORDED in the change record so anyone can re-run them | Default branch |
| **retired** | Refuted or abandoned — documented in `profile-repo-failure-archaeology` with the evidence, so nobody re-fights it | Failure archaeology |

Rules:
- candidate → experiment requires the B.1 write-up.
- experiment → adopted requires the milestone met, the adversarial pass (B.3)
  survived, and change control's review gates passed.
- experiment → retired is a SUCCESS of the method, not a failure of the person.
  Retire loudly (archaeology entry with evidence), never silently.
- No stage transition routes around `profile-repo-change-control`.

### B.5 Worked example — the one real case (2026-07-14)

This is the only real investigation this repo has; it is reproduced here exactly
because it exercised every step above. Do not treat any other example in this file as
having happened.

- **Symptom:** an incoming maintainer expected a project and found a clone containing
  only `.git/`; `git log` failed with exit 128
  (`fatal: your current branch ... does not have any commits yet`); `git fetch origin`
  returned silently (exit 0, no output) and `git branch -r` stayed empty.
- **Hypothesis 1 (initial):** "the clone failed / network issue is hiding the content."
  Predicted observable if true: remote queries error out or time out.
- **Discriminating experiment:** `git ls-remote origin`. Outcomes separate the two
  explanations cleanly: no access → the command ERRORS; empty repo → the command
  exits 0 with NO output.
- **Observation:** empty output, exit 0. Hypothesis 1 REFUTED — the remote was
  reachable and answered; it simply had zero refs.
- **Hypothesis 2 (accepted mechanism):** "the repository was created on GitHub but
  never received a push." This one mechanism explains ALL observations, including the
  negatives: the GitHub API's `409 Git Repository is empty`, the empty branch list
  (`[]`), the silent no-op fetch, the unborn local branch, and the exit-128 `git log`.
  Nothing is left unexplained.
- **Lifecycle outcome:** resolved and documented (see
  `profile-repo-failure-archaeology`); the discriminating test was promoted into the
  preflight gate of `profile-repo-bootstrap-campaign`.

That promotion is the method working end to end: hypothesis → discriminating
experiment → single mechanism covering all evidence → the finding institutionalized
where it prevents the next person's confusion.

## When NOT to use this skill

- Shipping the FIRST README to the empty repo → `profile-repo-bootstrap-campaign`
  (the executable campaign; this skill is planning and discipline).
- Landing any concrete change → `profile-repo-change-control`.
- Triaging a live symptom → `profile-repo-debugging-playbook`.
- Recording a finished investigation → `profile-repo-failure-archaeology`.
- Verifying a change worked / evidence standards → `profile-repo-validation-and-qa`.
- Platform facts about profile READMEs, Actions, badges → `github-profile-reference`.

## Provenance and maintenance

- Repo emptiness (the reason every roadmap item is CANDIDATE) verified 2026-07-14.
  Re-verify: `git ls-remote origin` (empty + exit 0 = still empty). Once the repo is
  non-empty, re-read the prerequisite line at the top of Half A but the candidates
  remain candidates until individually promoted per B.4.
- Platform facts — ~60-day scheduled-workflow disablement, github-readme-stats public
  instance rate-limiting and self-hostability, camo image caching — are Model
  knowledge (2026-07-14), not re-verifiable from the authoring sandbox
  (docs.github.com blocked). Re-verify from an unrestricted machine:
  `https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/customizing-your-profile/managing-your-profile-readme`
- The worked example in B.5 is this repo's ONLY real case (2026-07-14). Do not add
  worked examples that did not happen; append new real ones as they occur, via
  `profile-repo-change-control`, with evidence in `profile-repo-failure-archaeology`.
- Diagnostics script names/paths re-check:
  `ls .claude/skills/profile-repo-diagnostics-and-tooling/scripts/`
- No candidate in Half A had been started as of 2026-07-14.
