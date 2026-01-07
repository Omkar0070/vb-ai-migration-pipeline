#!/bin/bash

git checkout -b cs_generated_v1
git add .
git commit -m "AI: Convert VB to C#"
git push origin cs_generated_v1

gh pr create \
  --base vb_banking_v1 \
  --head cs_generated_v1 \
  --title "AI VB → C# Conversion" \
  --body "Automated conversion using LLM pipeline"

