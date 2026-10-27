#!/usr/bin/env sh
set -eu

image="${1:-portfolio:local}"
output="${2:-evidence/sbom}"
mkdir -p "$output"
syft "$image" -o "spdx-json=$output/image.spdx.json"
syft "$image" -o "cyclonedx-json=$output/image.cyclonedx.json"
echo "SBOMs written to $output"
