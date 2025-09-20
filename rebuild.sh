#!/bin/bash
set -e

# Clean old builds
rm -rf dist/ build/ *.egg-info

# Build new distribution
pyproject-build

# Reinstall locally for testing
pipx install --force dist/*.whl

echo "✅ Build successful and installed locally."

# Check for publish flag
if [[ "$1" == "--publish" ]]; then
    echo "🚀 Uploading to PyPI..."
    python3 -m twine upload dist/*
    echo "🎉 Published to PyPI successfully!"
elif [[ "$1" == "--test" ]]; then
    echo "🧪 Uploading to TestPyPI..."
    python3 -m twine upload --repository testpypi dist/*
    echo "✅ Published to TestPyPI!"
else
    echo "ℹ️ Skipping publish. Run './rebuild.sh --publish' to deploy, or './rebuild.sh --test' to TestPyPI."
fi
