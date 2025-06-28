#!/bin/bash
set -e
source ./cli_config.sh

timestamp=$(date +%Y%m%d_%H%M%S)
out_dir="scratchpads/$timestamp"
mkdir -p "$out_dir"

for prompt in prompts/*.md; do
  step_name=$(basename "$prompt" .md)
  echo "Running $prompt..."
  claude -p @"$prompt" --json > "$out_dir/${step_name}.json"
done
