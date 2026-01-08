import sys
import os
from pathlib import Path
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

if not os.environ.get("OPENAI_API_KEY"):
    raise RuntimeError("OPENAI_API_KEY not set")

vb_file = Path(sys.argv[1])

# Load prompt
prompt_template = Path("prompts/vb-to-csharp-v1.md").read_text()
vb_code = vb_file.read_text()

prompt = prompt_template.replace("{{VB_CODE}}", vb_code)

# Call OpenAI
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.1,
    max_tokens=2000,
)

csharp_code = response.choices[0].message.content.strip()

# Validate output
if not csharp_code or "class" not in csharp_code:
    raise RuntimeError("Invalid or empty C# output from OpenAI")

# Write output
out_root = Path("cs_generated_v1")
relative = vb_file.relative_to("src/vb").with_suffix(".cs")
out_file = out_root / relative
out_file.parent.mkdir(parents=True, exist_ok=True)
out_file.write_text(csharp_code)

print(f"[OK] Converted {vb_file}")
