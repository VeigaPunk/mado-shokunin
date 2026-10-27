#!/usr/bin/env python3
"""Counter self-test (scratch harness, not the counter): a tool that IS the judge must score TARGET_MET.

Replaces the counter's Box with one that answers every clause from the pinned judge itself, so this checks
the scoring plumbing (fixtures/generated/selftest/refusal/verdict arithmetic) on the positive path, which no
available draft tool can do yet. Usage: counter-selftest.py <counter.py> <repo> <rev> <work> <nonce>.
"""
import importlib.util
import os
import sys
import tempfile


def load(path):
    spec = importlib.util.spec_from_file_location("c1r49", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    counter, repo, rev, work, nonce = sys.argv[1:6]
    m = load(counter)

    class JudgeBox:
        def __init__(self, workdir, tool):
            self.work = workdir
            self.tool = tool
            self.trips = []
            self.stdlib = os.path.dirname(os.path.realpath(os.__file__))
            self.libs = []
            self.judge = m.Judge(workdir)

        def run(self, keymap_path, args, timeout=120, writes_ok=False):
            if args and args[0] == "--selftest":
                return 0, "MADO_KEYSYM_SELFTEST: 25/25 passed\n", ""
            if "--keysym" not in args or "--disable-compose" not in args:
                return 2, "", "usage\n"
            arg = args[args.index("--keysym") + 1]
            rc, out = self.judge.run(keymap_path, arg)
            return rc, out.decode("utf-8", "surrogateescape"), ""

    m.Box = JudgeBox
    w = tempfile.mkdtemp(dir=work, prefix="sim-")
    rc = m.score(repo, rev, w, int(nonce))
    print("sim rc=%d" % rc)
    return rc


if __name__ == "__main__":
    sys.exit(main())
