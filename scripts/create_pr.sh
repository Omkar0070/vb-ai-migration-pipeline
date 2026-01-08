#!/bin/bash
set -e

# Configure git identity
git config user.name "github-actions"
git config user.email "github-actions@github.com"

# Create or reset generated branch
git checkout -B cs_generated_v1

# Add only generated files
git add cs_generated_v1

# If no changes, exit cleanly
if git diff --cached --quiet; then
  echo "No generated code changes. Skipping commit and PR."
  exit 0
fi

# Commit and push
git commit -m "AI: Convert VB to C#"
git push origin cs_generated_v1 --force

# Create PR only if it doesn't already exist
if gh pr view cs_generated_v1 --base vb_banking_v1 > /dev/null 2>&1; then
  echo "PR already exists. Skipping creation."
else
  gh pr create \
    --base vb_banking_v1 \
    --head cs_generated_v1 \
    --title "AI: VB → C# Conversion" \
    --body "Automated VB to C# conversion via GitHub Actions"
fi
