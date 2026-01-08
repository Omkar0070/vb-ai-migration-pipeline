
import sys
import os
from pathlib import Path
from openai import OpenAI

# Ensure API key exists
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY not set")

client = OpenAI(api_key=api_key)

vb_file = Path(sys.argv[1])

# Load prompt
prompt_path = Path("prompts/vb-to-csharp-v1.md")
prompt_template = prompt_path.read_text()

vb_code = vb_file.read_text()
prompt = prompt_template.replace("{{VB_CODE}}", vb_code)

# Call OpenAI
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.1,
    max_tokens=1500
)

csharp_code = response.choices[0].message.content.strip()

# Hard validation
if not csharp_code:
    raise RuntimeError("OpenAI returned empty output")

if "class" not in csharp_code:
    raise RuntimeError(f"Invalid C# output:\n{csharp_code}")

# Output file path
out_root = Path("cs_generated_v1")
relative = vb_file.relative_to("src/vb").with_suffix(".cs")
out_file = out_root / relative
out_file.parent.mkdir(parents=True, exist_ok=True)

# Write generated code
out_file.write_text(csharp_code)

print(f"[OK] Converted {vb_file}")
