#!/bin/bash
set -euo pipefail

# Load shared logger
source "$(dirname "$0")/lib/logger.sh"

# Trap ERR and report line number
trap 'log "ERROR" "Unexpected error at line $LINENO — aborting"' ERR

# ── Argument validation ──────────────────────────────────────────────────────
if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <project_name> [num_files]" >&2
  exit 1
fi

project_name=$1
num=${2:-3}

log "INFO" "Starting project setup"
log "INFO" "Project name: $project_name"
log "INFO" "Number of files: $num"

# ── Guard: project must not already exist ────────────────────────────────────
if [[ -d "$project_name" ]]; then
  log "ERROR" "Directory '$project_name' already exists — refusing to overwrite"
  exit 1
fi

# ── Create project structure ─────────────────────────────────────────────────
mkdir -p "$project_name"

# Use a subshell so cd does not affect the caller's working directory
(
  cd "$project_name"
  log "INFO" "Project directory created: $(pwd)"

  for ((i = 1; i <= num; i++)); do
    touch "file${i}.txt"
    log "INFO" "Created file${i}.txt"
  done
)

log "INFO" "Setup completed successfully"
