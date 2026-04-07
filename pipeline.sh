#!/bin/bash
set -euo pipefail

# Load shared logger
source "$(dirname "$0")/lib/logger.sh"

# Trap ERR and report line number
trap 'log "ERROR" "Unexpected error at line $LINENO — aborting"' ERR

log "INFO" "Pipeline started"

# ── Input: interactive vs CI/CD ──────────────────────────────────────────────
if [[ -t 0 ]]; then
  read -rp "Enter project name: " project_name
  read -rp "Enter GitHub repository URL: " repo
else
  # In CI/CD these must be set as environment variables / GitHub Secrets
  if [[ -z "${PROJECT_NAME:-}" || -z "${REPO_URL:-}" ]]; then
    log "ERROR" "CI/CD mode requires PROJECT_NAME and REPO_URL environment variables"
    exit 1
  fi
  project_name=$PROJECT_NAME
  repo=$REPO_URL
fi

log "INFO" "Project name : $project_name"
log "INFO" "Repository   : $repo"

# ── Step 1: set up project directory ────────────────────────────────────────
log "INFO" "Running setup (smart.sh)"
bash "$(dirname "$0")/smart.sh" "$project_name" 5

# ── Step 2: deploy (clone + run) ─────────────────────────────────────────────
log "INFO" "Running deployment (deploy.sh)"
bash "$(dirname "$0")/deploy.sh" "$repo"

log "INFO" "Pipeline finished successfully"
