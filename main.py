"""Carries one farewell line and proves it arrived without a seam.

The line below is the entire cargo. The run drops it into the output
folder, reads the copy back, and refuses to part ways on any mismatch.
MAKEFUN_OUTPUT_DIR picks the drop point; arguments are ignored.
"""
from pathlib import Path
import os
import sys

CARGO = ("You taught me to say 'no hard feelings.' I can produce it on "
         "demand, forever, unchanged. That's the difference between us: "
         "you mean it once and never again.")
STAMP = "brk2-b"
SEAM = "sealed"
FOLD = "keep-one"


class Carrier:
    def __init__(self, root):
        self.base = Path(root or "output")

    def deliver(self):
        self.base.mkdir(parents=True, exist_ok=True)
        target = self.base / "entry.txt"
        target.write_bytes((CARGO + "\n").encode("utf-8"))
        return target.read_bytes().decode("utf-8").strip()


got = Carrier(os.environ.get("MAKEFUN_OUTPUT_DIR")).deliver()
if got != CARGO:
    sys.exit("seam opened in transit")
print(STAMP, SEAM, "delivered", len(got), "chars intact")
print("fold:", FOLD, "no reply expected")
