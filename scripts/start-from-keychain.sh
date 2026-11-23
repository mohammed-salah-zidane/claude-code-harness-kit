#!/bin/bash
# Starts an MCP server with its secrets read from the macOS Keychain, so no key sits in a project file.
#
# 1. Store each secret once (the command asks for the value without showing it):
#      security add-generic-password -U -s my-service -a API_KEY -w
# 2. Change SERVICE, NAMES and the last line below.
# 3. Point the server's "command" in .mcp.json at this script and remove the secrets from its "env".
set -euo pipefail
SERVICE="my-service"
NAMES="API_KEY"
for name in $NAMES; do
  value="$(security find-generic-password -s "$SERVICE" -a "$name" -w 2>/dev/null)" || {
    echo "$name is not in the Keychain (service $SERVICE)." >&2
    echo "Add it: security add-generic-password -U -s $SERVICE -a $name -w" >&2
    exit 1
  }
  export "$name=$value"
done
exec /path/to/the/server "$@"
