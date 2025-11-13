#!/bin/bash
# Wrapper script to run infobus with proper Cairo library paths on macOS

export DYLD_FALLBACK_LIBRARY_PATH="/opt/homebrew/lib:/opt/homebrew/opt/cairo/lib:/opt/homebrew/opt/libffi/lib"

# Run infobus with all arguments passed through
uv run infobus "$@"
