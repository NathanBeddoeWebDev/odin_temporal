#!/usr/bin/env python3
"""Reject drift from the frozen public temporal API."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GOLDEN = ROOT / "api" / "temporal.public-api"
REQUIRE_RESULTS = {
    "compare_instant",
    "compare_local_date",
    "compare_local_date_time",
    "compare_local_time",
    "local_date_from_datetime",
    "local_date_time_from_datetime",
    "local_date_time_to_datetime",
    "local_date_to_datetime",
    "local_time_from_datetime",
    "local_time_to_datetime",
    "offset_date_time_from_time",
    "offset_date_time_from_time_utc",
    "offset_date_time_to_time",
    "validate_local_date",
    "validate_local_date_time",
    "validate_local_time",
    "validate_offset_date_time",
    "validate_utc_offset",
}
SOURCE_LOCATION = re.compile(r" /\* \d+!\d+ \*/")


def documented_api() -> str:
    result = subprocess.run(
        ["odin", "doc", str(ROOT)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode:
        raise SystemExit(result.stdout + result.stderr)
    public = result.stdout.split("\n\tfullpath:\n", 1)[0].rstrip() + "\n"
    return SOURCE_LOCATION.sub("", public)


def main() -> int:
    failures: list[str] = []
    if documented_api() != GOLDEN.read_text():
        failures.append(f"temporal public API differs from {GOLDEN.relative_to(ROOT)}")

    source = "\n".join(path.read_text() for path in sorted(ROOT.glob("*.odin")))
    attributed = set(re.findall(r"@\(require_results\)\s+(\w+)\s+::\s+proc\b", source))
    missing = sorted(REQUIRE_RESULTS - attributed)
    extra = sorted(attributed - REQUIRE_RESULTS)
    if missing:
        failures.append("procedures missing @(require_results): " + ", ".join(missing))
    if extra:
        failures.append("procedures unexpectedly use @(require_results): " + ", ".join(extra))

    if failures:
        print("public API check failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("public temporal API check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
