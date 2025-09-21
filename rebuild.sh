#!/bin/bash
set -e

# Clean old builds
rm -rf dist/ build/ *.egg-info

# Auto-bump version if publishing
if [[ "$1" == "--publish" ]]; then
    echo "🔢 Auto-bumping version in pyproject.toml..."
    # Extract current version
    CURRENT_VERSION=$(grep -E '^version\s*=' pyproject.toml | sed -E 's/version\s*=\s*"(.*)"/\1/')
    echo "Current version: $CURRENT_VERSION"

    # If version ends with .postN, bump N
    if [[ "$CURRENT_VERSION" =~ (.*)\.post([0-9]+)$ ]]; then
        BASE=${BASH_REMATCH[1]}
        NUM=${BASH_REMATCH[2]}
        NEXT=$((NUM + 1))
        NEW_VERSION="${BASE}.post${NEXT}"
    else
        # If no .post suffix, add .post1
        NEW_VERSION="${CURRENT_VERSION}.post1"
    fi

    # Replace in pyproject.toml
    sed -i "s/version = \"${CURRENT_VERSION}\"/version = \"${NEW_VERSION}\"/" pyproject.toml
    echo "✅ Updated version to: $NEW_VERSION"
fi

# Build new distribution
pyproject-build

# Reinstall locally for testing
pipx install --force dist/*.whl

echo "✅ Build successful and installed locally."

# Use venv python if available
PYTHON=${VIRTUAL_ENV:-$(which python)}

# Check for publish flag
if [[ "$1" == "--publish" ]]; then
    echo "🚀 Uploading to PyPI..."
    $PYTHON -m twine upload dist/*
    echo "🎉 Published to PyPI successfully!"
elif [[ "$1" == "--test" ]]; then
    echo "🧪 Uploading to TestPyPI..."
    $PYTHON -m twine upload --repository testpypi dist/*
    echo "✅ Published to TestPyPI!"
else
    echo "ℹ️ Skipping publish. Run './rebuild.sh --publish' to deploy, or './rebuild.sh --test' to TestPyPI."
fi
