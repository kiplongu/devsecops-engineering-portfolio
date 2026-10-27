#!/usr/bin/env python3
"""Verify that every baseline finding has durable rescan evidence."""

import json
import sys
from pathlib import Path


def main(before_path, after_path):
    before = json.loads(Path(before_path).read_text())
    after = json.loads(Path(after_path).read_text())
    current = {item["id"]: item for item in after.get("findings", [])}
    failures = []
    for original in before.get("findings", []):
        item = current.get(original["id"])
        if not item:
            failures.append(f"{original['id']}: missing from rescan")
            continue
        verification = item.get("verification", {})
        if item.get("status") != "verified":
            failures.append(f"{original['id']}: status is not verified")
        if item.get("installedVersion") != item.get("fixedVersion"):
            failures.append(f"{original['id']}: fixed version is not installed")
        if not verification.get("rescanPassed") or not verification.get("verifiedAt") or not verification.get("evidence"):
            failures.append(f"{original['id']}: rescan evidence is incomplete")
    if failures:
        print("Remediation verification failed:\n- " + "\n- ".join(failures), file=sys.stderr)
        return 1
    print(f"Verified remediation and rescan evidence for {len(before.get('findings', []))} findings.")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: verify_remediation.py BEFORE AFTER", file=sys.stderr)
        sys.exit(2)
    sys.exit(main(sys.argv[1], sys.argv[2]))
