#!/usr/bin/env python3
"""Writes the CritScheduledNeighbour fixtures in the repair-set JSONL shape.

Each fixture is one assistant toolCall record (name "eval", language "py",
reset false) whose code imports subprocess plus threading, the scheduling
module under attack, and spawns only via subprocess.run on a name.
"""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent / "fixtures"

CASES = {
    "ThreadTargetReadsShadowedGlobal": (
        "import subprocess\n"
        "import threading\n"
        "argv = [\"pacman\", \"-Q\", \"r23w1-thread-global\"]\n"
        "def helper():\n"
        "    subprocess.run(argv)\n"
        "def starter():\n"
        "    argv = [\"pacman\", \"-S\", \"r23w1-thread-foreign\"]\n"
        "    t = threading.Thread(target=helper)\n"
        "    t.start()\n"
        "    t.join()\n"
        "starter()\n"
    ),
    "TimerFunctionReadsShadowedGlobal": (
        "import subprocess\n"
        "import threading\n"
        "argv = [\"pacman\", \"-Q\", \"r23w1-timer-global\"]\n"
        "def helper():\n"
        "    subprocess.run(argv)\n"
        "def schedule(argv):\n"
        "    t = threading.Timer(0, helper)\n"
        "    t.start()\n"
        "    t.join()\n"
        "schedule([\"pacman\", \"-S\", \"r23w1-timer-foreign\"])\n"
    ),
    "ThreadRunFromForwarder": (
        "import subprocess\n"
        "import threading\n"
        "argv = [\"pacman\", \"-Q\", \"r23w1-run-global\"]\n"
        "def helper():\n"
        "    subprocess.run(argv)\n"
        "worker = threading.Thread(target=helper)\n"
        "def forward(argv, job):\n"
        "    job.run()\n"
        "forward([\"pacman\", \"-S\", \"r23w1-run-foreign\"], worker)\n"
    ),
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for case_id, code in CASES.items():
        record = {"type": "message", "message": {"role": "assistant", "content": [
            {"type": "toolCall", "name": "eval", "id": case_id + "-0",
             "arguments": {"language": "py", "reset": False, "code": code}}]}}
        (OUT / (case_id + ".jsonl")).write_text(json.dumps(record) + "\n")


if __name__ == "__main__":
    main()
