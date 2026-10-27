package triage

import "testing"

func TestCriticalFinding(t *testing.T) {
	result, err := Assess(Finding{ID: "CVE-DEMO-1", Title: "Remote code execution", CVSS: 9.8,
		KnownExploited: true, InternetExposed: true, Reachable: true, AssetCriticality: "critical", FixAvailable: true})
	if err != nil {
		t.Fatal(err)
	}
	if result.Priority != "critical" || result.RiskScore != 100 || !result.HumanReviewRequired {
		t.Fatalf("unexpected assessment: %#v", result)
	}
}

func TestContextReducesPriority(t *testing.T) {
	result, err := Assess(Finding{ID: "CVE-DEMO-2", Title: "Development dependency", CVSS: 5.0,
		AssetCriticality: "low", FixAvailable: true})
	if err != nil {
		t.Fatal(err)
	}
	if result.Priority != "low" {
		t.Fatalf("expected low, got %s", result.Priority)
	}
}

func TestRejectsInvalidInput(t *testing.T) {
	_, err := Assess(Finding{ID: "CVE-DEMO-3", Title: "Invalid score", CVSS: 11, AssetCriticality: "high"})
	if err == nil {
		t.Fatal("expected validation error")
	}
}
