package main

import (
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
)

func TestTriageHandler(t *testing.T) {
	body := `{"id":"CVE-DEMO-TEST","title":"Fictional vulnerable component","cvss":9.8,"knownExploited":true,"internetExposed":true,"reachable":true,"assetCriticality":"critical","fixAvailable":true}`
	request := httptest.NewRequest(http.MethodPost, "/api/v1/triage", strings.NewReader(body))
	response := httptest.NewRecorder()

	triageHandler(response, request)

	if response.Code != http.StatusOK {
		t.Fatalf("expected 200, got %d: %s", response.Code, response.Body.String())
	}
	if !strings.Contains(response.Body.String(), `"humanReviewRequired":true`) {
		t.Fatalf("response does not require human review: %s", response.Body.String())
	}
}

func TestTriageHandlerRejectsUnknownInput(t *testing.T) {
	request := httptest.NewRequest(http.MethodPost, "/api/v1/triage", strings.NewReader(`{"id":"test","cvss":5,"unexpected":true}`))
	response := httptest.NewRecorder()

	triageHandler(response, request)

	if response.Code != http.StatusBadRequest {
		t.Fatalf("expected 400, got %d", response.Code)
	}
}

func TestSecurityHeaders(t *testing.T) {
	handler := securityHeaders(http.HandlerFunc(func(response http.ResponseWriter, _ *http.Request) {
		response.WriteHeader(http.StatusNoContent)
	}))
	response := httptest.NewRecorder()
	handler.ServeHTTP(response, httptest.NewRequest(http.MethodGet, "/", nil))

	if response.Header().Get("X-Content-Type-Options") != "nosniff" {
		t.Fatal("missing nosniff header")
	}
	if response.Header().Get("Content-Security-Policy") == "" {
		t.Fatal("missing content security policy")
	}
}
