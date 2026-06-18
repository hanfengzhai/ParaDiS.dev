#!/usr/bin/env bash
# Install tracked hooks from .githooks/ into .git/hooks/
set -euo pipefail

repo_root="$(git rev-parse --show-toplevel)"
cd "$repo_root"

mkdir -p .git/hooks
for hook in .githooks/*; do
  [[ -f "$hook" ]] || continue
  name="$(basename "$hook")"
  install -m 755 "$hook" ".git/hooks/$name"
  echo "installed .git/hooks/$name"
done
