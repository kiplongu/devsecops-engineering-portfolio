.PHONY: test format-check build run smoke vulnerability-demo validate

test:
	go test -race ./...
	python3 -m unittest discover -s tools/ai-triage/tests -p 'test_*.py'

format-check:
	test -z "$$(gofmt -l cmd internal)"

build:
	docker build -t devsecops-portfolio-app:local .

run: build
	docker run --rm -p 8080:8080 devsecops-portfolio-app:local

smoke:
	bash scripts/smoke-test.sh

vulnerability-demo:
	python3 scripts/vulnerability_gate.py security/findings/before.json --expect-block
	python3 scripts/vulnerability_gate.py security/findings/current.json
	python3 scripts/verify_remediation.py security/findings/before.json security/findings/current.json

validate:
	bash scripts/validate.sh
