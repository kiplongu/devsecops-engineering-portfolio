#!/usr/bin/env sh
set -eu

echo '== Go source =='
test -z "$(gofmt -l .)"
go test ./...
go vet ./...

echo '== Python policy and AI tests =='
python3 -m unittest discover -s tools/ai-triage/tests -v
python3 scripts/vulnerability_gate.py security/findings/before.json --expect-block >/dev/null
python3 scripts/vulnerability_gate.py security/findings/current.json >/dev/null
python3 scripts/verify_remediation.py security/findings/before.json security/findings/current.json

echo 'All locally available validation passed.'
