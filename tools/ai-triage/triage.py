#!/usr/bin/env python3
"""Offline-first, human-reviewed vulnerability triage reference.

The deterministic result is authoritative. An optional OpenAI-compatible model
may add a short analyst narrative, but it cannot change priority or approval.
"""

import argparse
import json
import os
import urllib.error
import urllib.request
from pathlib import Path


def deterministic_assessment(finding):
    cvss = float(finding.get("cvss", 0))
    score = round(cvss * 6)
    reasons = [f"CVSS {cvss:.1f} establishes the technical baseline"]
    factors = (
        ("knownExploited", 20, "known exploitation exists"),
        ("internetExposed", 10, "the affected asset is internet exposed"),
        ("reachable", 10, "the vulnerable code path is reachable"),
        ("fixAvailable", -5, "a supported fix is available"),
    )
    for key, weight, reason in factors:
        if finding.get(key):
            score += weight
            reasons.append(reason)
    criticality = str(finding.get("assetCriticality", "medium")).lower()
    score += {"low": 0, "medium": 5, "high": 10, "critical": 15}.get(criticality, 5)
    score = max(0, min(score, 100))
    label = "critical" if score >= 85 else "high" if score >= 65 else "medium" if score >= 40 else "low"
    return {"id": finding.get("id"), "riskScore": score, "priority": label, "reasons": reasons,
            "humanReviewRequired": True, "decision": "pending-human-review"}


def llm_narrative(finding, assessment):
    endpoint = os.getenv("LLM_ENDPOINT", "").strip()
    if not endpoint:
        return None, "offline-mock"
    prompt = {
        "model": os.getenv("LLM_MODEL", "local-security-model"),
        "temperature": 0,
        "messages": [
            {"role": "system", "content": "Explain the supplied vulnerability decision in at most three sentences. Do not change its priority, invent evidence, or approve risk."},
            {"role": "user", "content": json.dumps({"finding": finding, "deterministicAssessment": assessment})},
        ],
    }
    request = urllib.request.Request(endpoint, data=json.dumps(prompt).encode(), method="POST",
                                     headers={"Content-Type": "application/json"})
    token = os.getenv("LLM_API_TOKEN", "").strip()
    if token:
        request.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            payload = json.loads(response.read())
        narrative = payload.get("choices", [{}])[0].get("message", {}).get("content")
        if not isinstance(narrative, str) or not narrative.strip():
            raise ValueError("provider returned no narrative")
        return narrative.strip()[:2000], "optional-llm"
    except (OSError, ValueError, KeyError, json.JSONDecodeError, urllib.error.URLError) as error:
        return None, f"offline-fallback: {type(error).__name__}"


def run(finding):
    assessment = deterministic_assessment(finding)
    narrative, mode = llm_narrative(finding, assessment)
    return {**assessment, "mode": mode, "analystNarrative": narrative,
            "reviewNotice": "A security professional must review evidence and approve the final disposition."}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("finding", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run(json.loads(args.finding.read_text()))
    rendered = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered)
    print(rendered, end="")


if __name__ == "__main__":
    main()
