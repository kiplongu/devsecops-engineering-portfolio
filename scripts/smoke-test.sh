#!/usr/bin/env sh
set -eu

base_url="${BASE_URL:-http://127.0.0.1:8080}"
curl --fail --silent --show-error "${base_url}/healthz" | grep -q '"healthy"'
curl --fail --silent --show-error -X POST "${base_url}/api/v1/triage" \
  -H 'Content-Type: application/json' \
  --data-binary @tools/ai-triage/sample-finding.json | grep -q '"humanReviewRequired":true'
printf '%s\n' "Smoke tests passed for ${base_url}."
