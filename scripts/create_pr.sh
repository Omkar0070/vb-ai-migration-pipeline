#!/bin/bash
set -e

# Configure git identity for GitHub Actions
git config user.name "github-actions"
git config user.email "github-actions@github.com"

# Create and switch to generated branch
git checkout -B cs_generated_v1

# Add generated files
git add cs_generated_v1

git commit -m "AI: Convert VB to C#" || echo "Nothing to commit"

# Push using GitHub token
git push origin cs_generated_v1 --force

# Create PR using GitHub CLI
gh pr create \
  --base vb_banking_v1 \
  --head cs_generated_v1 \
  --title "AI: VB → C# Conversion" \
  --body "Automated VB to C# conversion via GitHub Actions"
