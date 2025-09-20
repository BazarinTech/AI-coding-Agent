#!/bin/bash
rm -rf dist/ build/ *.egg-info
pyproject-build
pipx install --force dist/*.whl
