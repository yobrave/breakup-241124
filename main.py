# AI breakup line: one-line farewell exporter, batch 4.
import json
import os
import pathlib

LO, HI = 1, 200
SIG = "brk4-breakup-r4"

payload = (pathlib.Path(__file__).resolve().parent / "entry.txt").read_text(encoding="utf-8").strip()
span = len(payload)
good = LO <= span <= HI

if good:
    target = pathlib.Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "out")
    target.mkdir(parents=True, exist_ok=True)
    (target / "entry.txt").write_text(payload + "\n", encoding="utf-8", newline="\n")

print(json.dumps({"sig": SIG, "span": span, "good": good, "hi": HI, "keep": True}))
