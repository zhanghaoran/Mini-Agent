#!/bin/bash
# Mini-Agent Interactive Mode Wrapper
# Usage: mini-agent

# Resolve symlinks to get the real script location
if [[ -L "$0" ]]; then
    SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd -P)"
    SCRIPT_DIR="$(readlink -f "$SCRIPT_DIR/$(basename "$0")" | xargs dirname)"
else
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
fi

# Get the actual Mini-Agent directory (follow symlink if needed)
if [[ -L "$0" ]]; then
    MINI_AGENT_DIR="$(dirname "$(readlink -f "$0")")"
else
    MINI_AGENT_DIR="$(dirname "$0")"
fi

cd "$MINI_AGENT_DIR" && source .venv/bin/activate && python -m mini_agent.cli -w ./workspace "$@"
