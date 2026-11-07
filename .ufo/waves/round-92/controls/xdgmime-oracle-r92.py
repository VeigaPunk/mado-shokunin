#!/usr/bin/env python3
"""Round-92 C1 oracle — label xdg-mime cases with the installed xdg-utils' own answer.

A case is a JSON object:
  id, group            stable name and family
  files                {relpath: spec} materialised under a fresh root; spec is one of
                       {"text": str} (UTF-8), {"b64": str} (raw bytes), {"dir": true},
                       {"symlink": target} (target may use {ROOT}); optional "mode" (octal string)
  env                  {NAME: VALUE}; "{ROOT}" in a value is replaced by the root's absolute path.
                       This is the whole environment (`env -i`); PATH must be present.
  types                MIME types asked, one `xdg-mime query default TYPE` run each
  expect               {type: {"default": str|None, "rc": int}} — written by this oracle only
The command runs with the root as its working directory.  `default` is stdout with one trailing
newline removed (None when stdout is empty); stdout bytes that are not UTF-8 are kept with
surrogateescape.  The oracle pins /usr/bin/xdg-mime by sha256 at the caller (the counter).

  xdgmime-oracle-r92.py label --in CASES --out CASES --scratch DIR   (writes expect for every case)
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

XDG_MIME = "/usr/bin/xdg-mime"


def sha(p: str) -> str:
    return hashlib.sha256(open(os.path.realpath(p), "rb").read()).hexdigest()


def sub(v: str, root: str) -> str:
    return v.replace("{ROOT}", root)


def materialise(case: dict, root: str) -> None:
    items = sorted(case.get("files", {}).items(), key=lambda kv: (0 if kv[1].get("dir") else 1, kv[0]))
    for rel, spec in items:
        p = os.path.join(root, rel)
        if spec.get("dir"):
            os.makedirs(p, exist_ok=True)
            continue
        os.makedirs(os.path.dirname(p) or root, exist_ok=True)
        if "symlink" in spec:
            os.symlink(sub(spec["symlink"], root), p)
            continue
        data = base64.b64decode(spec["b64"]) if "b64" in spec else spec["text"].encode("utf-8", "surrogateescape")
        with open(p, "wb") as fh:
            fh.write(data)
    for rel, spec in items:
        if "mode" in spec and "symlink" not in spec:
            os.chmod(os.path.join(root, rel), int(spec["mode"], 8))


def env_of(case: dict, root: str) -> dict:
    return {k: sub(v, root) for k, v in case["env"].items()}


def run_one(env: dict, root: str, t: str) -> dict:
    r = subprocess.run([XDG_MIME, "query", "default", t], cwd=root, env=env, capture_output=True, timeout=60)
    out = r.stdout
    if out.endswith(b"\n"):
        out = out[:-1]
    d = None if r.stdout == b"" else out.decode("utf-8", "surrogateescape")
    return {"default": d, "rc": r.returncode}


def restore_modes(root: str) -> None:
    for d, dirs, files in os.walk(root):
        for n in dirs:
            try:
                os.chmod(os.path.join(d, n), 0o755)
            except OSError:
                pass


def label_case(case: dict, scratch: str) -> dict:
    root = tempfile.mkdtemp(prefix="o", dir=scratch)
    try:
        materialise(case, root)
        env = env_of(case, root)
        return {t: run_one(env, root, t) for t in case["types"]}
    finally:
        restore_modes(root)
        shutil.rmtree(root, ignore_errors=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["label"])
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--scratch", required=True)
    a = ap.parse_args()
    doc = json.load(open(a.inp, encoding="utf-8"))
    os.makedirs(a.scratch, exist_ok=True)
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=8) as ex:
        labs = list(ex.map(lambda c: label_case(c, a.scratch), doc["cases"]))
    for c, lab in zip(doc["cases"], labs):
        c["expect"] = lab
    doc["oracle"] = {"xdg_mime_sha256": sha(XDG_MIME)}
    with open(a.out, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, indent=1, ensure_ascii=True)
        fh.write("\n")
    print(f"labelled {len(doc['cases'])} cases")
    return 0


if __name__ == "__main__":
    sys.exit(main())
