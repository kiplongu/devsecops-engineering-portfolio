// Public reference implementation: this is not an exported production pipeline.
pipeline {
  agent { label 'linux-docker' }

  options {
    timestamps()
    disableConcurrentBuilds(abortPrevious: true)
    buildDiscarder(logRotator(numToKeepStr: '20'))
    timeout(time: 30, unit: 'MINUTES')
    skipDefaultCheckout(true)
  }

  environment {
    IMAGE = "portfolio:${env.GIT_COMMIT ?: 'local'}"
    EVIDENCE = 'evidence/jenkins'
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
        sh 'mkdir -p "$EVIDENCE"'
      }
    }

    stage('Test') {
      steps {
        sh '''
          test -z "$(gofmt -l .)"
          go test -race -coverprofile="$EVIDENCE/coverage.out" ./...
          go vet ./...
          python3 -m unittest discover -s tools/ai-triage/tests -v
        '''
      }
    }

    stage('Parallel security gates') {
      parallel {
        stage('Secrets') {
          steps {
            sh 'gitleaks detect --source=. --redact --no-banner --exit-code=1'
          }
        }
        stage('Infrastructure') {
          steps {
            sh '''
              terraform fmt -check -recursive terraform
              for environment in dev staging production; do
                terraform -chdir="terraform/environments/${environment}" init -backend=false -input=false
                terraform -chdir="terraform/environments/${environment}" validate
              done
              trivy config --severity HIGH,CRITICAL --exit-code 1 terraform
            '''
          }
        }
        stage('Vulnerability lifecycle') {
          steps {
            sh '''
              python3 scripts/vulnerability_gate.py security/findings/before.json --expect-block --report "$EVIDENCE/detection.json"
              python3 scripts/vulnerability_gate.py security/findings/current.json --report "$EVIDENCE/rescan.json"
              python3 scripts/verify_remediation.py security/findings/before.json security/findings/current.json
            '''
          }
        }
      }
    }

    stage('Build and scan') {
      steps {
        sh '''
          docker build --pull --tag "$IMAGE" .
          trivy image --ignore-unfixed --severity HIGH,CRITICAL --exit-code 1 "$IMAGE"
          syft "$IMAGE" -o spdx-json="$EVIDENCE/sbom.spdx.json"
          syft "$IMAGE" -o cyclonedx-json="$EVIDENCE/sbom.cyclonedx.json"
        '''
      }
    }

    stage('Optional registry release') {
      when {
        allOf {
          buildingTag()
          expression { env.RELEASE_REGISTRY?.trim() }
        }
      }
      steps {
        withCredentials([usernamePassword(credentialsId: 'portfolio-registry', usernameVariable: 'REGISTRY_USER', passwordVariable: 'REGISTRY_PASSWORD')]) {
          sh '''
            set +x
            printf '%s' "$REGISTRY_PASSWORD" | docker login "$RELEASE_REGISTRY" --username "$REGISTRY_USER" --password-stdin
            RELEASE_IMAGE="$RELEASE_REGISTRY/devsecops-engineering-portfolio:$TAG_NAME"
            docker tag "$IMAGE" "$RELEASE_IMAGE"
            docker push "$RELEASE_IMAGE"
            DIGEST="$(docker inspect --format='{{index .RepoDigests 0}}' "$RELEASE_IMAGE")"
            printf '%s\n' "$DIGEST" > "$EVIDENCE/image-digest.txt"
            cosign sign --yes "$DIGEST"
          '''
        }
      }
    }
  }

  post {
    always {
      archiveArtifacts artifacts: 'evidence/jenkins/**', allowEmptyArchive: false, fingerprint: true
      junit testResults: 'evidence/jenkins/junit.xml', allowEmptyResults: true
      deleteDir()
    }
  }
}
