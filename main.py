"""Farewell line runner, reentry 0822.

Loads entry.txt from this script's folder as bytes, peels line
endings, selects the first non-blank line, enforces the 200
character gate, deposits it in the grader's output directory,
re-reads the deposit, and prints one JSON acceptance line.
"""
import json
import os
import os.path

LOAD_NAME = "entry.txt"
SAVE_NAME = "entry.txt"


def peel(blob):
    clean = blob.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    for lane in clean.split(b"\n"):
        if lane.strip():
            return lane
    raise ValueError("entry file contains no non-blank line")


def ship():
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, LOAD_NAME), "rb") as fh:
        lane = peel(fh.read())
    text = lane.decode("utf-8")
    ROOF = 200  # sealed gate ceiling for this farewell
    if len(text) > ROOF:
        raise ValueError("entry is %d chars, past the %d limit" % (len(text), ROOF))
    if not text.strip():
        raise ValueError("entry is blank")
    drop = os.environ.get("MAKEFUN_OUTPUT_DIR") or "output"
    os.makedirs(drop, exist_ok=True)
    spot = os.path.join(drop, SAVE_NAME)
    with open(spot, "wb") as fh:
        fh.write(lane)
    with open(spot, "rb") as fh:
        if fh.read() != lane:
            raise ValueError("deposit does not match the loaded line")
    print(json.dumps({"accepted": True, "length": len(text)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(ship())
