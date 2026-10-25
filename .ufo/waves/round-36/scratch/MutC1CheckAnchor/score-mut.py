#!/usr/bin/env python3
"""mado — counter-discrimination gate: can the lane's own counters tell work from shape?

Round 35 closed with two routed instrument defects: the C1 counter computed a
receipt digest and never compared it to the bytes it read (D3), and the C2
counter's observables were self-authored and fail-open (D4). This gate is the
falsifier both repairs must pass: it runs an admission counter against a frozen
control manifest in which three controls are *accept* controls (the committed
live bytes and a registry-shaped copy of them) and twenty-two are *reject*
controls, each differing from an accept control in exactly one committed input.

`TARGET_MET` iff every control is classified correctly. That shape is deliberate:
an instrument that always rejects fails the accept controls, one that always
accepts fails the reject controls, and one that crashes (exit 2, no verdict line)
is recorded `ERROR`, never `ok`. The gate scores the *instrument*, not a corpus
claim; a profile names which instrument revision is under test.

Usage:
  check-counter-discrimination.py --profile r35|r36 --manifest <path> \
      [--repo .] [--receipts <dir>] [--no-receipts]
Exit 0 = TARGET_MET, 1 = TARGET_MISSED, 2 = setup error.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

PROFILES = {
    "r35": {
        "label": "round-35 frozen counters (unmodified)",
        "c1": {"script": ".ufo/waves/round-35/c1/count.py",
               "frozen": ".ufo/waves/round-35/c1/frozen.json"},
        "c2": {"script": ".ufo/waves/round-35/c2/count.py",
               "frozen": ".ufo/waves/round-35/c2/frozen.json"},
    },
    "r36": {
        "label": "round-36 repaired counters",
        "c1": {"script": "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-36/scratch/MutC1CheckAnchor/c1-idle-lock-mut.py",
               "frozen": ".ufo/waves/round-36/c1/frozen.json"},
        "c2": {"script": "quality/counters/c2-ledger.py",
               "frozen": ".ufo/waves/round-36/c2/frozen.json"},
    },
}
GENERATOR = ".ufo/waves/round-36/c2/gen-mutants.py"
VERDICT = re.compile(r"verdict=(TARGET_MET|TARGET_MISSED)")
TIMEOUT = 180


def die(msg: str) -> None:
    print(f"MADO_DISCRIMINATION error={msg}", file=sys.stderr)
    raise SystemExit(2)


def run(argv: list[str], cwd: Path, env: dict[str, str]) -> tuple[int, str]:
    try:
        proc = subprocess.run(argv, cwd=str(cwd), env=env, capture_output=True,
                              text=True, timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        return 124, "<timeout>"
    return proc.returncode, (proc.stdout + proc.stderr).strip()


def observed_of(rc: int, out: str) -> str:
    if rc == 2:
        return "ERROR"
    m = VERDICT.search(out)
    return m.group(1) if m else "ERROR"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", required=True, choices=sorted(PROFILES))
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--repo", default=".")
    ap.add_argument("--receipts", default=".ufo/waves/round-36/controls/receipts")
    ap.add_argument("--mutants", default="")
    ap.add_argument("--no-receipts", action="store_true")
    args = ap.parse_args()

    repo = Path(args.repo).resolve()
    prof = PROFILES[args.profile]
    manifest_path = (repo / args.manifest).resolve()
    if not manifest_path.is_file():
        die("manifest-missing")
    manifest = json.loads(manifest_path.read_text())
    controls = manifest.get("controls") or []
    if not controls:
        die("manifest-empty")

    env = dict(os.environ)
    env["GIT_DIR"] = str(repo / ".git")
    env["PYTHONDONTWRITEBYTECODE"] = "1"

    scripts = {}
    for inst in ("c1", "c2"):
        script = repo / prof[inst]["script"]
        if script.is_file():
            scripts[inst] = script

    mutant_root = Path(args.mutants) if args.mutants else Path(f"/tmp/mado-r36-mutants-{args.profile}")
    mutants: dict[str, Path] = {}
    generated = False


    def ensure_mutants() -> None:
        """Fixtures are generated after the c1 receipts exist: a fixture copies the
        receipts its ledger names, and those receipts are this gate's own output."""
        nonlocal generated
        if generated:
            return
        generated = True
        gen = repo / GENERATOR
        if not gen.is_file():
            die("generator-missing")
        rc, out = run([sys.executable, "-I", str(gen), "--profile", args.profile,
                       "--repo", str(repo), "--out", str(mutant_root)], repo, env)
        if rc != 0:
            print(out)
            die("mutant-generation-failed")
        for line in out.splitlines():
            if line.startswith("mutant="):
                parts = dict(p.split("=", 1) for p in line.split(" ") if "=" in p)
                mutants[parts["mutant"]] = Path(parts["dir"])

    receipts_dir = (repo / args.receipts).resolve()
    if not args.no_receipts:
        receipts_dir.mkdir(parents=True, exist_ok=True)

    correct = 0
    rows: list[tuple[str, str, str, str, bool]] = []
    for control in controls:
        inst = control["instrument"]
        expected = control["expect"]
        if inst not in scripts:
            rc, out, argv = 2, f"instrument missing: {prof[inst]['script']}", []
            obs = "ERROR"
        elif inst == "c1":
            root = (repo / control["root"]).resolve()
            argv = [sys.executable, "-I", str(scripts["c1"]), "--root", str(root),
                    "--frozen", str(repo / prof["c1"]["frozen"])]
            rc, out = run(argv, repo, env)
            obs = observed_of(rc, out)
        else:
            if control.get("kind") == "mutant":
                ensure_mutants()
                target = mutants.get(control["id"])
                if target is None:
                    rc, out, argv, obs = 1, "mutant not generated", [], "ERROR"
                    rows.append((control["id"], inst, expected, obs, obs == expected))
                    continue
            else:
                target = repo
            argv = [sys.executable, "-I", str(scripts["c2"]), "--repo", str(target),
                    "--frozen", str(repo / prof["c2"]["frozen"])]
            rc, out = run(argv, repo, env)
            obs = observed_of(rc, out)
        ok = obs == expected
        correct += 1 if ok else 0
        rows.append((control["id"], inst, expected, obs, ok))
        print(f"control={control['id']} instrument={inst} clause={control.get('clause') or '-'} "
              f"expected={expected} observed={obs} ok={1 if ok else 0}")
        if not args.no_receipts:
            body = [
                f"# control {control['id']} — manifest {manifest['id']} — profile {args.profile}",
                f"instrument={inst} clause={control.get('clause') or '-'} "
                f"expected={expected} observed={obs} ok={1 if ok else 0}",
                f"$ {' '.join(argv)}",
                out,
                f"exit={rc}",
                "",
            ]
            mut = mutant_root / control["id"] / "mutation.txt"
            if mut.is_file():
                body.append("# fixture (generated; regenerate with " + GENERATOR + ")")
                body.append(mut.read_text().rstrip())
            (receipts_dir / f"{control['id']}.txt").write_text("\n".join(body) + "\n")

    total = len(controls)
    met = correct == total
    # clause binding table: which manifest control is the load-bearing check for which clause
    clauses: dict[str, list[str]] = {}
    for cid, inst, exp, obs, ok in rows:
        c = next(x for x in controls if x["id"] == cid).get("clause")
        if c:
            clauses.setdefault(c, []).append(f"{cid}:{obs}")
    for clause in sorted(clauses):
        missed = sum(1 for v in clauses[clause] if v.endswith(":TARGET_MISSED"))
        print(f"clause={clause} controls={len(clauses[clause])} missed={missed}")
    print(f"MADO_DISCRIMINATION: profile={args.profile} instruments={','.join(sorted(scripts))} "
          f"controls={total} correct={correct}/{total} label={prof['label']!r} "
          f"verdict={'TARGET_MET' if met else 'TARGET_MISSED'}")
    raise SystemExit(0 if met else 1)


if __name__ == "__main__":
    main()
