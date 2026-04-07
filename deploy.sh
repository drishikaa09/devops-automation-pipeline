#!/bin/bash
set -euo pipefail

# Load shared logger
source "$(dirname "$0")/lib/logger.sh"

# Trap ERR and report line number
trap 'log "ERROR" "Unexpected error at line $LINENO — aborting"' ERR

# ── Argument validation ──────────────────────────────────────────────────────
if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <repo_url>" >&2
  exit 1
fi

repo=$1

log "INFO" "Starting deployment"
log "INFO" "Repository: $repo"

# ── Clone ────────────────────────────────────────────────────────────────────
git clone "$repo"
folder=$(basename "$repo" .git)

log "INFO" "Repository cloned into: $folder"

# ── Run application (subshell keeps cwd clean) ───────────────────────────────
(
  cd "$folder"

  if [[ -f "app.py" ]]; then
    log "INFO" "app.py detected"

    if ! command -v python3 &>/dev/null; then
      log "ERROR" "python3 not found — cannot run application"
      exit 1                    # exits the subshell, which exits the script via set -e
    fi

    log "INFO" "Executing app.py"
    python3 app.py

  elif [[ -f "package.json" ]]; then
    log "INFO" "package.json detected"

    if ! command -v node &>/dev/null; then
      log "ERROR" "node not found — cannot run application"
      exit 1
    fi

    log "INFO" "Running npm start"
    npm start

  else
    log "WARN" "No recognised entry point found (app.py / package.json)"
  fi
)

log "INFO" "Deployment completed"
