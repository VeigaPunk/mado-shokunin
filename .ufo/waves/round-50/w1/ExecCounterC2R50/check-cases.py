#!/usr/bin/env python3
"""check-cases.py — the counter's embedded v2 case list against the v2 bytes at base.

Re-derives the v2 selftest case names from
``git show <BASE_REV>:quality/check-session-material.py`` (never the working
tree), then compares three things: the sorted list the v2 gate prints, the seat
file ``v2-selftest-cases.txt`` (with its pinned sha256), and the tuple embedded
in ``c2-r50-session-gate.py``. Exits 0 when all three agree and the gate bytes
still hash to ``BASE_GATE_SHA256``.

Usage:
  python3 -I check-cases.py --repo MADO_LANE --work DIR
"""

import argparse
import hashlib
import importlib.util
import os
import re
import subprocess
import sys

TOOL = "check-cases.py"
BASE_REV = "8ae47b957034ae21012bbf09173cca2c48be345e"
BASE_GATE_SHA256 = "82c9053ae2e8b7db2fb8c0e195c32b8b151a593cf9412dcae3589427ac2dfa6f"
V2_CASE_NAMES_SHA256 = "38a8b2c647665b68ae4d3b7692e7ffaf9ca959fc1cdfe03b21deb5bd8097e725"
GATE_REL = "quality/check-session-material.py"
CASE_RE = re.compile(r"^SELFTEST (?:ok|FAIL) case=(\S+)")
FORBIDDEN_WORK = ("/tmp", "/var/tmp", "/dev/shm")
HERE = os.path.dirname(os.path.realpath(__file__))
sys.dont_write_bytecode = True  # never litter the seat dir with a __pycache__


def _refuse(path):
    real = os.path.realpath(os.path.abspath(path))
    for bad in FORBIDDEN_WORK:
        if real == bad or real.startswith(bad + os.sep):
            sys.stderr.write("%s: error: %r is under %s\n" % (TOOL, path, bad))
            raise SystemExit(2)


def main(argv=None):
    parser = argparse.ArgumentParser(prog=TOOL)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--work", required=True)
    args = parser.parse_args(argv)
    _refuse(args.work)
    work = os.path.realpath(os.path.abspath(args.work))
    for leaf in ("home/.cache", "home/.config", "home/.local/share",
                 "home/.local/state", "tmp"):
        os.makedirs(os.path.join(work, leaf), exist_ok=True)
    env = {
        "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
        "HOME": os.path.join(work, "home"),
        "XDG_CACHE_HOME": os.path.join(work, "home", ".cache"),
        "XDG_CONFIG_HOME": os.path.join(work, "home", ".config"),
        "XDG_DATA_HOME": os.path.join(work, "home", ".local", "share"),
        "XDG_STATE_HOME": os.path.join(work, "home", ".local", "state"),
        "TMPDIR": os.path.join(work, "tmp"),
        "LC_ALL": "C",
    }

    show = subprocess.run(["git", "-C", args.repo, "show",
                           "%s:%s" % (BASE_REV, GATE_REL)],
                          capture_output=True, env=env)
    if show.returncode != 0:
        sys.stderr.write("%s: error: git show failed: %s\n"
                         % (TOOL, show.stderr.decode("utf-8", "replace").strip()[:300]))
        return 2
    gate_bytes = show.stdout
    gate_sha = hashlib.sha256(gate_bytes).hexdigest()
    gate = os.path.join(work, "base-gate.py")
    with open(gate, "wb") as handle:
        handle.write(gate_bytes)
    proc = subprocess.run([sys.executable, "-I", gate, "--selftest"],
                          capture_output=True, env=env, cwd=work)
    out = proc.stdout.decode("utf-8", "replace")
    gate_names = sorted(CASE_RE.match(line).group(1)
                        for line in out.splitlines() if CASE_RE.match(line))

    seat_file = os.path.join(HERE, "v2-selftest-cases.txt")
    with open(seat_file, "rb") as handle:
        file_bytes = handle.read()
    file_sha = hashlib.sha256(file_bytes).hexdigest()
    file_names = sorted(line for line in file_bytes.decode("utf-8").splitlines() if line)

    spec = importlib.util.spec_from_file_location(
        "counters", os.path.join(HERE, "c2-r50-session-gate.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    embedded = sorted(module.V2_CASE_NAMES)

    checks = {
        "base_gate_sha": gate_sha == BASE_GATE_SHA256,
        "file_sha": file_sha == V2_CASE_NAMES_SHA256,
        "gate_selftest_clean": proc.returncode == 0,
        "file_eq_gate": file_names == gate_names,
        "embedded_eq_file": embedded == file_names,
        "embedded_sha": hashlib.sha256(
            ("\n".join(embedded) + "\n").encode()).hexdigest() == V2_CASE_NAMES_SHA256,
    }
    print("CASES: base_rev=%s base_sha=%s selftest_rc=%d gate_cases=%d"
          % (BASE_REV, gate_sha, proc.returncode, len(gate_names)))
    print("CASES: file=%s file_cases=%d embedded=%d file_sha=%s"
          % (os.path.basename(seat_file), len(file_names), len(embedded), file_sha))
    print("CASES: " + " ".join("%s=%s" % (key, "yes" if ok else "no")
                               for key, ok in checks.items()))
    ok = all(checks.values()) and len(gate_names) == 69
    print("CASES: verdict=%s" % ("OK" if ok else "MISMATCH"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
