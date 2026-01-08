 import os
import sys
from pathlib import Path
from openai import OpenAI

print("=== VB → C# PIPELINE STARTED ===")

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Ensure file argument is provided
if len(sys.argv) < 2:
    print("❌ No VB file provided")
    sys.exit(1)

SRC_FILE = Path(sys.argv[1])

# Output directory
OUT_DIR = Path("cs_generated_v1")
OUT_DIR.mkdir(exist_ok=True)

print("Processing:", SRC_FILE)


# -----------------------------
# Conversion Function
# -----------------------------
def convert_vb_to_csharp(vb_code: str) -> str:
    prompt = f"""
Convert the following VB.NET code line by line into C#.

Rules:
- Use standard C# syntax
- Preserve logic exactly
- Do NOT include markdown formatting
- Do NOT include ``` or language identifiers
- Return ONLY valid C# code

VB.NET code:
{vb_code}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    code = response.choices[0].message.content.strip()

    # 🧹 Remove Markdown code fences if model adds them
    if code.startswith("```"):
        code = code.replace("```csharp", "").replace("```", "").strip()

    return code


# -----------------------------
# Validation Function
# -----------------------------
def validate_csharp_file(file_path: Path):
    if not file_path.exists() or file_path.stat().st_size == 0:
        print("❌ Validation failed: file missing or empty")
        sys.exit(1)

    content = file_path.read_text(encoding="utf-8")

    if "```" in content:
        print("❌ Validation failed: markdown formatting found")
        sys.exit(1)

    print("✅ Validation passed for", file_path.name)


# -----------------------------
# Main Execution
# -----------------------------
try:
    # Read VB file
    vb_code = SRC_FILE.read_text(encoding="utf-8")

    # Convert to C#
    csharp_code = convert_vb_to_csharp(vb_code)

    # Write output file
    output_file = OUT_DIR / (SRC_FILE.stem + ".cs")
    output_file.write_text(csharp_code, encoding="utf-8")

    print("Generated:", output_file)

    # Validate output
    validate_csharp_file(output_file)

    print("=== PIPELINE SUCCESS ===")

except Exception as e:
    print("❌ Pipeline failed:", str(e))
    sys.exit(1)
    
