import sys, yaml, os
from pathlib import Path

file = sys.argv[1]

with open("config/conversion.yaml") as f:
    cfg = yaml.safe_load(f)

with open(file) as f:
    vb_code = f.read()

# NOTE: Replace below with real OpenAI call
if not vb_code.strip():
    raise Exception("Empty VB file")

target_dir = "cs_generated_v1"
os.makedirs(target_dir, exist_ok=True)

output_file = Path(target_dir) / (Path(file).stem + ".cs")
with open(output_file, "w") as f:
    f.write("// Converted code placeholder")

print(f"[OK] Converted {file}")

