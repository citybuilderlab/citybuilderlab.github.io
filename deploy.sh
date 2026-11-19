#!/usr/bin/env bash
# Deploy work/microsite to citybuilderlab/citybuilderlab.github.io and try to enable Pages.
set -euo pipefail
cd /workspace/work/microsite

REPO="citybuilderlab/citybuilderlab.github.io"

# 1) branch + remote
git branch -M main 2>/dev/null || true
if ! git remote get-url origin >/dev/null 2>&1; then
  git remote add origin "https://github.com/${REPO}.git"
fi

# 2) push
git push -u origin main

# 3) try to enable Pages from branch (needs pages:write)
echo "--- pages api ---"
gh api -X POST "repos/${REPO}/pages" \
  -f 'source[branch]=main' -f 'source[path]=/' 2>&1 | head -5 || true

echo "--- pages status ---"
gh api "repos/${REPO}/pages" 2>&1 | head -20 || true
