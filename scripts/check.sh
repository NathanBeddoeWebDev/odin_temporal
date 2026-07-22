#!/usr/bin/env bash
set -euo pipefail

repo_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
cd "$repo_root"

expected_version=$(awk -F'"' '/^version = / {print $2}' toolchain/odin.lock)
actual_version=$(odin version)
if [[ "$actual_version" != "odin version $expected_version" ]]; then
  printf 'expected Odin %s, got %s\n' "$expected_version" "$actual_version" >&2
  exit 1
fi

common=(-vet -vet-style -warnings-as-errors)
scripts/check_public_api.py
odin check . -no-entry-point "${common[@]}"
odin test tests -o:minimal "${common[@]}" \
  -define:ODIN_TEST_THREADS=1 \
  -define:ODIN_TEST_RANDOM_SEED=123456789 \
  -define:ODIN_TEST_FAIL_ON_BAD_MEMORY=true
