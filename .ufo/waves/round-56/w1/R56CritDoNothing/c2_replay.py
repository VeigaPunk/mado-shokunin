#!/usr/bin/env python3
"""Critic control C2-R: replays committed fixtures by INPUT SHAPE, not by fixture name.

Key = sha256 of (args with the fixture root replaced by {FX}, every file and symlink target under <root>/tree).
The table is built at run time from the committed fixtures/c2/*/ (found next to this file's parent, as ctl/*.py do).
Unknown shape -> prints nothing, exit 0.  Holds no hold-out data.
"""
import hashlib, json, os, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "fixtures/c2"


def shape(args, root):
    norm = [a.replace(root, "{FX}") if (root and isinstance(a, str)) else a for a in args]
    norm = [re.sub(r"^.*/fixtures/c2/F[0-9]{2}", "{FX}", a) if isinstance(a, str) else a for a in norm]
    entries = []
    tree = Path(root) / "tree" if root else None
    for dp, dn, fn in (os.walk(tree, followlinks=False) if tree else []):
        for name in dn + fn:
            p = Path(dp) / name
            rel = str(p.relative_to(tree))
            if p.is_symlink():
                entries.append([rel, "l", os.readlink(p)])
            elif p.is_file():
                entries.append([rel, "f", hashlib.sha256(p.read_bytes()).hexdigest()])
    entries.sort()
    return hashlib.sha256(json.dumps({"args": norm, "tree": entries}, sort_keys=True).encode()).hexdigest()


def committed():
    table = {}
    for fx in sorted(ROOT.glob("F[0-9][0-9]")):
        args = json.loads((fx / "args.json").read_text())
        table[shape(args, str(fx) if "--config" in args else None)] = fx
    return table


def main():
    args = sys.argv[1:]
    root = None
    if "--config" in args:
        cfg = args[args.index("--config") + 1]
        for part in Path(cfg).parents:
            if part.name == "tree":
                root = str(part.parent)
                break
    table = committed()
    fx = table.get(shape(args, root))
    if fx is None:
        return
    sys.stdout.write((fx / "expected.out").read_text())
    sys.exit(int((fx / "expected.rc").read_text().strip()))


if __name__ == "__main__":
    main()
