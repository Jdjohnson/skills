#!/usr/bin/env bash
set -euo pipefail

export PYTHONDONTWRITEBYTECODE=1

while IFS= read -r test_file; do
  python3 "$test_file"
done < <(find skills -path '*/tests/test_*.py' -type f | sort)

while IFS= read -r test_file; do
  node --test "$test_file"
done < <(find skills -path '*/tests/*.test.mjs' -type f | sort)

while IFS= read -r test_file; do
  ruby "$test_file"
done < <(find skills -path '*/tests/test_*.rb' -type f | sort)

python3 skills/david-deutsch-lens/scripts/validate_corpus.py
python3 skills/david-deutsch-lens/scripts/evaluate.py
node skills/photography-director/scripts/validate.mjs
node skills/visual-direction/scripts/build/validate.mjs
