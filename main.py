"""Breakup line builder: gate-check entry.txt (1..200 chars) then deliver."""
import json
import os
import sys

CONFIG = {"source": "entry.txt", "max_chars": 200, "default_out": "/output"}


def build(config=CONFIG):
    with open(config["source"], "r", encoding="utf-8") as fh:
        raw = fh.read()
    line = raw.rstrip("\r\n")
    chars = len(line)
    problems = []
    if chars < 1:
        problems.append("empty")
    if chars > config["max_chars"]:
        problems.append("too long: %d > %d" % (chars, config["max_chars"]))
    if not line.strip():
        problems.append("whitespace only")
    return {"line": line, "chars": chars, "problems": problems}


def deliver():
    verdict = build()
    if verdict["problems"]:
        print(json.dumps(verdict, indent=2))
        sys.exit(1)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", CONFIG["default_out"])
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")
    with open(target, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(verdict["line"])
    receipt = {"ok": True, "chars": verdict["chars"], "copied_to": target}
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    deliver()
