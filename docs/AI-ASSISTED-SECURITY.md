# AI-assisted security triage

This is a new public reference implementation. It does not claim to be an
export of a private application's AI feature.

The design is offline-first and safe by default:

- deterministic policy calculates the authoritative priority;
- an optional OpenAI-compatible endpoint may add a short explanation;
- the model cannot change priority, accept risk or close a finding;
- only the supplied finding context is sent to the configured endpoint;
- timeouts and parsing failures fall back to offline mode;
- every disposition remains `pending-human-review`.

Run the offline path:

```bash
python3 tools/ai-triage/triage.py tools/ai-triage/sample-finding.json
```

For an explicitly approved local or hosted provider, set `LLM_ENDPOINT`,
`LLM_MODEL`, and optionally `LLM_API_TOKEN`. Do not send secrets, customer data
or unredacted evidence to a third-party model.
