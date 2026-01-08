import os
import sys
import subprocess
from pathlib import Path
from openai import OpenAI

print("=== VB → C# PIPELINE STARTED ===")

# -------------------------
# CONFIG
# -------------------------
SRC_DIR = Path("src/vb")
OUT_DIR = Path("cs_generated_v1")
BASE_BRANCH = "vb_banking_v1"
GEN_BRANCH = "cs_generated_v1"

OUT_DIR.mkdir(exist_ok=True)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# -------------------------
# UTIL FUNCTIONS
# -------------------------
def run(cmd):
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    if result.returncode != 0:
        print(result.stderr)
        sys.exit(result.returncode)
    return result.stdout.strip()


# -------------------------
# 1️⃣ CONVERT VB → C#
# -------------------------
def convert_vb_to_csharp(vb_code: str) -> str:
    prompt = f"""
Convert the following VB.NET code line by line into C#.
Rules:
- Use standard C# (.NET) syntax
- Preserve logic exactly
- Do not add comments
- Return ONLY valid C# code

VB.NET code:
{vb_code}
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    return response.choices[0].message.content.strip()


print("Scanning VB source folder...")
vb_files = list(SRC_DIR.rglob("*.vb"))

if not vb_files:
    print("❌ No VB files found. Exiting.")
    sys.exit(1)

print("Found VB files:", vb_files)

generated_files = []

for vb_file in vb_files:
    print(f"Processing: {vb_file}")

    vb_code = vb_file.read_text(encoding="utf-8")
    csharp_code = convert_vb_to_csharp(vb_code)

    output_file = OUT_DIR / (vb_file.stem + ".cs")
    output_file.write_text(csharp_code, encoding="utf-8")

    print(f"Generated: {output_file}")
    generated_files.append(output_file)


# -------------------------
# 2️⃣ VALIDATE OUTPUT
# -------------------------
print("\n=== VALIDATING GENERATED FILES ===")

for file in generated_files:
    if not file.exists() or file.stat().st_size == 0:
        print(f"❌ Validation failed: {file}")
        sys.exit(1)
    else:
        print(f"✅ Valid: {file}")

print("All files validated successfully.")


# -------------------------
# 3️⃣ CREATE BRANCH + COMMIT + PR
# -------------------------
print("\n=== CREATING PULL REQUEST ===")

# Configure git user (required for GitHub Actions)
run('git config user.name "github-actions"')
run('git config user.email "github-actions@github.com"')

# Create or reset branch
run(f"git checkout -B {GEN_BRANCH}")

# Add only generated folder
run(f"git add {OUT_DIR}")

# Commit if there are changes
commit_output = subprocess.run(
    "git commit -m \"AI: Convert VB to C#\"",
    shell=True, text=True, capture_output=True
)

if "nothing to commit" in commit_output.stdout.lower():
    print("⚠️ No changes to commit. Skipping PR.")
    sys.exit(0)

print(commit_output.stdout)

# Push branch
run(f"git push origin {GEN_BRANCH} --force")

# Create PR using GitHub CLI
run(
    f'gh pr create '
    f'--base {BASE_BRANCH} '
    f'--head {GEN_BRANCH} '
    f'--title "AI VB → C# Conversion" '
    f'--body "Automated VB to C# conversion using OpenAI pipeline."'
)

print("\n=== PIPELINE COMPLETED SUCCESSFULLY ===")
