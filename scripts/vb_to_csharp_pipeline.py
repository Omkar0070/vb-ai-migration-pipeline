#!/usr/bin/env python3

#!/usr/bin/env python3

import os
import sys
from pathlib import Path
from openai import OpenAI

print("=== MULTI-FORMAT → C# PIPELINE STARTED ===")

# -----------------------------------
# Validate Input
# -----------------------------------
if len(sys.argv) < 2:
    print("❌ No source file provided")
    print("Usage: python code_to_csharp_pipeline.py <source_file>")
    sys.exit(1)

SRC_FILE = Path(sys.argv[1])

if not SRC_FILE.exists():
    print(f"❌ File not found: {SRC_FILE}")
    sys.exit(1)

# -----------------------------------
# Initialize OpenAI Client
# -----------------------------------
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# -----------------------------------
# Output Directory
# -----------------------------------
OUT_DIR = Path("cs_generated_v1")
OUT_DIR.mkdir(exist_ok=True)

print("Processing:", SRC_FILE)

# -----------------------------------
# Prompt Builder
# -----------------------------------
def build_prompt(code: str, file_type: str) -> str:
    if file_type == "vb":
        return f"""
Convert the following VB.NET code line by line into C#.

Rules:
- Use standard C# syntax
- Preserve logic exactly
- Do NOT include markdown formatting
- Do NOT include ``` or language identifiers
- Return ONLY valid C# code

VB.NET code:
{code}
"""
    elif file_type == "fox":
        return f"""
Convert the following Visual FoxPro (VFP) code into modern C#.

Rules:
- Preserve business logic
- Map FoxPro constructs to C# equivalents
- Replace database commands with repository/service patterns where needed
- Do NOT include markdown formatting
- Do NOT include ``` or language identifiers
- Return ONLY valid C# code

Visual FoxPro code:
{code}
"""
    else:
        raise ValueError("Unsupported source file type")

# -----------------------------------
# Sanitize Markdown
# -----------------------------------
def sanitize_code(code: str) -> str:
    """
    Remove markdown code fences and stray backticks.
    """
    lines = code.strip().splitlines()

    # Remove starting fence
    if lines and lines[0].strip().startswith("```"):
        lines = lines[1:]

    # Remove ending fence
    if lines and lines[-1].strip().startswith("```"):
        lines = lines[:-1]

    # Remove any remaining triple backticks in content
    cleaned = "\n".join(line.replace("```", "") for line in lines).strip()

    return cleaned

# -----------------------------------
# Convert Source → C#
# -----------------------------------
def convert_to_csharp(source_code: str, source_type: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": build_prompt(source_code, source_type)}],
        temperature=0,
    )

    raw_code = response.choices[0].message.content.strip()
    clean_code = sanitize_code(raw_code)

    return clean_code

# -----------------------------------
# Validate Output
# -----------------------------------
def validate_csharp_file(file_path: Path):
    if not file_path.exists():
        print("❌ Validation failed: output file does not exist")
        sys.exit(1)

    if file_path.stat().st_size == 0:
        print("❌ Validation failed: output file is empty")
        sys.exit(1)

    content = file_path.read_text(encoding="utf-8")

    if "```" in content:
        print("❌ Validation failed: markdown formatting detected")
        sys.exit(1)

    print("✅ Validation passed for", file_path.name)

# -----------------------------------
# Main Pipeline
# -----------------------------------
try:
    ext = SRC_FILE.suffix.lower()

    if ext == ".vb":
        source_type = "vb"
        relative_path = SRC_FILE.relative_to("src/vb")
    elif ext == ".prg":
        source_type = "fox"
        relative_path = SRC_FILE.relative_to("src/fox")
    else:
        print(f"⚠ Skipping unsupported file type: {SRC_FILE}")
        sys.exit(0)

    # Read source file
    source_code = SRC_FILE.read_text(encoding="utf-8")

    # Convert to C#
    csharp_code = convert_to_csharp(source_code, source_type)

    # Preserve folder structure
    output_file = OUT_DIR / relative_path.with_suffix(".cs")
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Write output
    output_file.write_text(csharp_code, encoding="utf-8")

    print("Generated:", output_file)

    # Validate output
    validate_csharp_file(output_file)

    print("=== PIPELINE SUCCESS ===")

except Exception as e:
    print("❌ Pipeline failed:", str(e))
    sys.exit(1
