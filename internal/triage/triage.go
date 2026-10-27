package triage

import (
	"errors"
	"math"
	"strings"
)

type Finding struct {
	ID               string  `json:"id"`
	Title            string  `json:"title"`
	CVSS             float64 `json:"cvss"`
	KnownExploited   bool    `json:"knownExploited"`
	InternetExposed  bool    `json:"internetExposed"`
	Reachable        bool    `json:"reachable"`
	AssetCriticality string  `json:"assetCriticality"`
	FixAvailable     bool    `json:"fixAvailable"`
}

type Assessment struct {
	ID                  string   `json:"id"`
	RiskScore           int      `json:"riskScore"`
	Priority            string   `json:"priority"`
	Reasons             []string `json:"reasons"`
	RecommendedAction   string   `json:"recommendedAction"`
	HumanReviewRequired bool     `json:"humanReviewRequired"`
}

func Assess(finding Finding) (Assessment, error) {
	if strings.TrimSpace(finding.ID) == "" || strings.TrimSpace(finding.Title) == "" {
		return Assessment{}, errors.New("id and title are required")
	}
	if math.IsNaN(finding.CVSS) || finding.CVSS < 0 || finding.CVSS > 10 {
		return Assessment{}, errors.New("cvss must be between 0 and 10")
	}
	criticality := strings.ToLower(strings.TrimSpace(finding.AssetCriticality))
	if criticality != "low" && criticality != "medium" && criticality != "high" && criticality != "critical" {
		return Assessment{}, errors.New("assetCriticality must be low, medium, high, or critical")
	}

	score := int(math.Round(finding.CVSS * 6))
	reasons := []string{"CVSS contributes the technical severity baseline"}
	if finding.KnownExploited {
		score += 20
		reasons = append(reasons, "known exploitation increases urgency")
	}
	if finding.InternetExposed {
		score += 10
		reasons = append(reasons, "internet exposure increases attack likelihood")
	}
	if finding.Reachable {
		score += 10
		reasons = append(reasons, "the vulnerable path is reachable")
	}
	criticalityWeight := map[string]int{"low": 0, "medium": 5, "high": 10, "critical": 15}
	score += criticalityWeight[criticality]
	if criticality == "high" || criticality == "critical" {
		reasons = append(reasons, "the affected asset has high business criticality")
	}
	if score > 100 {
		score = 100
	}

	priority := "low"
	action := "Track remediation in the normal maintenance cycle."
	switch {
	case score >= 85:
		priority = "critical"
		action = "Escalate immediately, apply a tested fix or compensating control, then rescan."
	case score >= 65:
		priority = "high"
		action = "Assign an owner and remediate within the high-risk SLA, then rescan."
	case score >= 40:
		priority = "medium"
		action = "Plan remediation, validate exposure, and verify the fix in the next release."
	}
	if !finding.FixAvailable && (priority == "critical" || priority == "high") {
		action = "Apply a documented compensating control, monitor exposure, and reassess when a fix is available."
	}

	return Assessment{ID: finding.ID, RiskScore: score, Priority: priority, Reasons: reasons,
		RecommendedAction: action, HumanReviewRequired: true}, nil
}
