import sys
import os
from pathlib import Path
import openai

openai.api_key = os.environ.get("OPENAI_API_KEY")

if not openai.api_key:
    raise RuntimeError("OPENAI_API_KEY not set")

vb_file = Path(sys.argv[1])

prompt_path = Path("prompts/vb-to-csharp-v1.md")
prompt_template = prompt_path.read_text()

vb_code = vb_file.read_text()
prompt = prompt_template.replace("{{VB_CODE}}", vb_code)

response = openai.ChatCompletion.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.1,
    max_tokens=2000
)

csharp_code = response.choices[0].message.content.strip()

# Basic sanity check
if "class" not in csharp_code:
    raise RuntimeError("Invalid C# output from OpenAI")

# Output path
out_root = Path("cs_generated_v1")
relative = vb_file.relative_to("src/vb").with_suffix(".cs")
out_file = out_root / relative
out_file.parent.mkdir(parents=True, exist_ok=True)

out_file.write_text(csharp_code)

print(f"[OK] Converted {vb_file}")

