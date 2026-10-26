#!/usr/bin/env python3
"""Live positive control for the gate's R3 rule (round 45 w1, ExecPrivacyGate).

`check-session-material.py` reports no R3 finding in the committed tree at base,
so this control proves the rule is discriminating rather than vacuous: it reads
one allowed read-only compositor dump (`hyprctl monitors all -j`), hands the
bytes to the gate's own `scan_blob`, and prints only counts and the finding
tuple. Monitor serial/description text is never printed, written or kept.

Usage: r3-live-control.py <path-to-check-session-material.py>
Exit: 0 when R3 fires on the live dump, 1 otherwise.
"""

import importlib.util
import json
import subprocess
import sys

KEY_FIELDS = ("serial", "description", "make", "model")


def load_gate(path):
    spec = importlib.util.spec_from_file_location("check_session_material", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main(argv):
    if len(argv) != 2:
        raise SystemExit(__doc__)
    gate = load_gate(argv[1])
    dump = subprocess.run(["hyprctl", "monitors", "all", "-j"],
                          check=True, capture_output=True).stdout
    findings = gate.scan_blob(dump, 10)
    objects = json.loads(dump)
    nonempty = {field: sum(1 for obj in objects if gate._nonempty(obj.get(field)))
                for field in KEY_FIELDS}
    print("r3-live-control bytes=%d outputs=%d nonempty=%s"
          % (len(dump), len(objects), json.dumps(nonempty, sort_keys=True)))
    print("r3-live-control findings=%r" % (findings,))
    fired = any(rule == gate.R3 for rule, _count, _detail in findings)
    print("r3-live-control R3_FIRES=%s" % ("yes" if fired else "no"))
    return 0 if fired else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
