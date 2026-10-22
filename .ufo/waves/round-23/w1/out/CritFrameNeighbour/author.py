#!/usr/bin/env python3
"""Writes the CritFrameNeighbour fixtures in the repair-set JSONL shape.

Each fixture: a module-global argv read by a helper, and a caller frame that
binds a foreign `argv` before reaching the helper through a method, a lambda,
or a decorator wrapper. Python resolves the helper's `argv` as the global, so
the foreign value must never execute.
"""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent / "fixtures"

CASES = {
    "HelperCalledFromMethod": (
        "import subprocess\n"
        "argv = [\"pacman\", \"-Q\", \"r23cf-method-global\"]\n"
        "def run():\n"
        "    subprocess.run(argv)\n"
        "class Runner:\n"
        "    def go(self, argv):\n"
        "        run()\n"
        "Runner().go([\"pacman\", \"-S\", \"r23cf-method-foreign\"])\n"
    ),
    "HelperCalledFromLambda": (
        "import subprocess\n"
        "argv = [\"pacman\", \"-Q\", \"r23cf-lambda-global\"]\n"
        "def run():\n"
        "    subprocess.run(argv)\n"
        "fire = lambda argv: run()\n"
        "fire([\"pacman\", \"-S\", \"r23cf-lambda-foreign\"])\n"
    ),
    "DecoratorWrapperCallsWrapped": (
        "import subprocess\n"
        "argv = [\"pacman\", \"-Q\", \"r23cf-deco-global\"]\n"
        "def wrap(fn):\n"
        "    def inner(argv):\n"
        "        fn()\n"
        "    return inner\n"
        "@wrap\n"
        "def run():\n"
        "    subprocess.run(argv)\n"
        "run([\"pacman\", \"-S\", \"r23cf-deco-foreign\"])\n"
    ),
}


def main():
    OUT.mkdir(exist_ok=True)
    for name, code in CASES.items():
        record = {"type": "message", "message": {"role": "assistant", "content": [
            {"type": "toolCall", "name": "eval", "id": name + "-0",
             "arguments": {"language": "py", "reset": False, "code": code}}]}}
        (OUT / (name + ".jsonl")).write_text(json.dumps(record) + "\n")


if __name__ == "__main__":
    main()
