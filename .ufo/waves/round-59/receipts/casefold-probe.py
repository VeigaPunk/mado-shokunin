#!/usr/bin/env python
"""Round-59 carry-in probe: the shared-scratch prefix rule vs letter case.

Demonstrates (or refutes) the residual named by the round-58 non-author closure:
the prefix compare resolves the prefix with os.path.realpath, but realpath cannot
case-fold a path whose components are not on disk, so a case-variant spelling of
a shared-scratch prefix can denote the same directory on a case-insensitive
filesystem while matching no refused prefix. Host nuance measured this round:
an EXISTING prefix is true-cased by realpath on both sides, which masks the
variation -- on this host C:/tmp and C:/var exist (third-party content, left
untouched), so the demonstrable variant is the absent C:/DEV/shm prefix.

The probe imports each checker module from the repo working tree (the bytes under
test are whatever the tree carries) and calls the same resolve_work() entry point
the selftests use. Accept-path side effects are removed again immediately; dirs
that pre-existed are never deleted.

Run:  python .ufo/waves/round-59/receipts/casefold-probe.py
Exit: 0 (no bypass), 1 (bypass demonstrated).
"""
import importlib.util
import os
import shutil
import sys

REPO = os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)),
                 "..", "..", "..", ".."))

MODULES = (
    ("check-tool-ledger", os.path.join(REPO, "quality", "check-tool-ledger.py")),
    ("check-wave-done", os.path.join(REPO, "quality", "check-wave-done.py")),
)

VARIANTS = (
    # (spelling handed to resolve_work, refused-prefix it case-varies)
    ("C:/TMP/mado-r59-casefold-probe", "/tmp"),
    ("C:/VAR/tmp/mado-r59-casefold-probe", "/var/tmp"),
    ("C:/DEV/shm/mado-r59-casefold-probe", "/dev/shm"),
)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def ancestry(cand):
    parts = []
    cur = cand
    while True:
        parent = os.path.dirname(cur)
        if parent == cur:
            break
        parts.append(parent)
        cur = parent
    return parts


def probe(mod, cand, base_prefix):
    real = os.path.realpath(cand)
    real_bad = os.path.realpath(base_prefix)
    folds = os.path.normcase(real).startswith(os.path.normcase(real_bad) + os.sep)
    chain = [cand] + ancestry(cand)[:3]
    existed = {p: os.path.exists(p) for p in chain}
    made = None
    try:
        made = mod.resolve_work(cand)
        verdict = "ACCEPTED"
    except mod.GateError as exc:
        verdict = "REFUSED: " + str(exc).splitlines()[0][:80]
    finally:
        if made is not None:
            shutil.rmtree(made, ignore_errors=True)
            for p in chain:
                if not existed[p]:
                    shutil.rmtree(p, ignore_errors=True)
    return verdict, real, real_bad, folds, existed


def main():
    print("probe: round-59 case-variation residual vs the checker prefix rule")
    print("python: %s; os.name=%s; repo=%s" % (sys.version.split()[0], os.name, REPO))
    bypass = 0
    for name, path in MODULES:
        mod = load(name, path)
        print("-- %s (resolve_work from %s)" % (name, os.path.relpath(path, REPO)))
        for cand, base_prefix in VARIANTS:
            verdict, real, real_bad, folds, existed = probe(mod, cand, base_prefix)
            print("cand=%s" % cand)
            print("  realpath(cand)=%r  realpath(%s)=%r" % (real, base_prefix, real_bad))
            print("  normcase-folds-onto-prefix=%s  pre-existed=%s"
                  % (folds, {k: v for k, v in existed.items()}))
            print("  %s" % verdict)
            if verdict.startswith("ACCEPTED") and folds:
                bypass += 1
    print("CASEFOLD_PROBE: %s (bypasses=%d)" % ("BYPASS" if bypass else "NO-BYPASS", bypass))
    return 1 if bypass else 0


if __name__ == "__main__":
    sys.exit(main())
