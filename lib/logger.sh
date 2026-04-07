#!/bin/bash
log() {
  local level=$1
  local message=$2
  echo "{\"timestamp\":\"$(date -Iseconds)\",\"level\":\"$level\",\"message\":\"$message\"}"
}
