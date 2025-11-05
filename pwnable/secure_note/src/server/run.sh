#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"

# Name of the published single-file executable. The publish step produces a single file with the assembly name.
APP="./app/server" # adjust if published filename is different

# If FIX_SHARED_NOTES==1 then keep the existing shared notes behavior
if [ "${FIX_SHARED_NOTES:-}" = "1" ]; then
  export NOTES_DIR="/home/e4syctf/notes"
  mkdir -p "$NOTES_DIR"
  exec socat TCP-LISTEN:9999,reuseaddr,fork EXEC:"env NOTES_DIR=$NOTES_DIR $APP",pty,stderr
else
  # For each spawned process, create a per-process unique temporary notes directory
  # socat will spawn this script per connection, so this directory is unique per connection
  UNIQUE_DIR="/tmp/notes-$(date +%s)-$$-$RANDOM"
  mkdir -p "$UNIQUE_DIR"
  export NOTES_DIR="$UNIQUE_DIR"
  exec socat TCP-LISTEN:9999,reuseaddr,fork EXEC:"env NOTES_DIR=$NOTES_DIR $APP",pty,stderr
fi