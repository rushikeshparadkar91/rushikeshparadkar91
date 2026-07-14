#!/usr/bin/env bash
# repo-state.sh — one-shot, read-only state report for the profile repo.
# Usage: ./repo-state.sh [path-to-repo-root]   (default: current directory)
# Exit codes: 0 = report produced (verdict line says what state was found)
#             2 = not a git repository / remote unreachable (real access error)
# Read-only: runs no mutating git commands.
set -u

REPO="${1:-.}"
cd "$REPO" 2>/dev/null || { echo "ERROR: cannot cd to '$REPO'"; exit 2; }

if ! git rev-parse --git-dir >/dev/null 2>&1; then
  echo "ERROR: '$REPO' is not a git repository"
  exit 2
fi

echo "== repo-state report: $(pwd) =="

# --- remote refs ---
LSREMOTE_OUT="$(git ls-remote origin 2>&1)"
LSREMOTE_EXIT=$?
if [ $LSREMOTE_EXIT -ne 0 ]; then
  echo "remote-refs      : ERROR (git ls-remote origin failed, exit $LSREMOTE_EXIT)"
  echo "remote-error     : $LSREMOTE_OUT"
  echo "VERDICT: REMOTE-UNREACHABLE — this is an access/network problem, NOT an empty repo."
  exit 2
fi
REF_COUNT=$(printf '%s' "$LSREMOTE_OUT" | grep -c . || true)
echo "remote-refs      : $REF_COUNT ref(s) on origin"
[ "$REF_COUNT" -gt 0 ] && printf '%s\n' "$LSREMOTE_OUT" | sed 's/^/  ref: /'

# --- local branch + commit count ---
BRANCH="$(git branch --show-current 2>/dev/null || echo '(detached)')"
echo "local-branch     : ${BRANCH:-'(detached)'}"
if git rev-parse HEAD >/dev/null 2>&1; then
  COMMITS=$(git rev-list --count HEAD)
  echo "local-commits    : $COMMITS on HEAD"
else
  COMMITS=0
  echo "local-commits    : 0 (unborn branch — 'No commits yet')"
fi

# --- README.md ---
if [ -f README.md ]; then
  SIZE=$(wc -c < README.md | tr -d ' ')
  echo "README.md        : present, ${SIZE} bytes"
  [ "$SIZE" -eq 0 ] && echo "README.md-warn   : EMPTY file — an empty README does not render on the profile"
else
  echo "README.md        : MISSING at repo root"
fi

# --- workflows ---
if [ -d .github/workflows ]; then
  WF=$(find .github/workflows -maxdepth 1 -name '*.yml' -o -maxdepth 1 -name '*.yaml' 2>/dev/null | sort)
  if [ -n "$WF" ]; then
    echo "workflows        :"
    printf '%s\n' "$WF" | sed 's/^/  /'
  else
    echo "workflows        : .github/workflows exists but contains no *.yml/*.yaml"
  fi
else
  echo "workflows        : none (.github/workflows absent)"
fi

# --- verdict ---
if [ "$REF_COUNT" -eq 0 ] && [ "$COMMITS" -eq 0 ]; then
  echo "VERDICT: EMPTY-REPO — origin has zero refs and the local branch is unborn. Nothing has ever been pushed."
elif [ "$REF_COUNT" -eq 0 ]; then
  echo "VERDICT: LOCAL-ONLY — you have local commits but origin has zero refs. Nothing is published yet."
elif [ "$COMMITS" -eq 0 ]; then
  echo "VERDICT: BEHIND-REMOTE — origin has refs but your local branch is unborn. Check out a remote branch."
else
  echo "VERDICT: NORMAL — both origin and local have history. Compare refs above with 'git status' for drift."
fi
exit 0
