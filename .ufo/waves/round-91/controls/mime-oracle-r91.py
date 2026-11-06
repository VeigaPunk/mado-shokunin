#!/usr/bin/env python3
"""Round-91 C1 oracle — label MIME cases with the installed GLib's own answer.

For each case (schema mime-cases-r91-v1) the fixture tree is written under
--scratch-root, and `/usr/bin/gio mime <type>` (ONE argument: the read form;
the two-argument form writes mimeapps.list and is never used) runs with
`env -i` and only these variables: HOME=<fixture>, XDG_CONFIG_HOME,
XDG_CONFIG_DIRS, XDG_DATA_HOME, XDG_DATA_DIRS (all inside the fixture),
PATH (the case's path list; relative entries resolved inside the fixture),
LC_ALL=C, and XDG_CURRENT_DESKTOP when the case sets it.  stdout is parsed into
{default, registered, recommended}; when gio prints no default it prints no
lists, and both are recorded as null.

Case schema (JSON object {"schema": "mime-cases-r91-v1", "cases": [...]}):
  id        unique string
  desktop   XDG_CURRENT_DESKTOP value, or null (unset)
  path      list of PATH entries; relative = inside the fixture
  roots     {"config_home": rel, "config_dirs": [rel...], "data_home": rel, "data_dirs": [rel...]}
  files     {rel path: text | {"text": s, "exec": true} | {"b64": s, "exec": bool} | {"symlink": target} | {"dir": true}}
  types     list of MIME types to ask about
  expect    {type: {"default": id|null, "registered": [...]|null, "recommended": [...]|null}}  (written by --label)

Usage:
  mime-oracle-r91.py --cases IN.json --scratch-root DIR --label OUT.json   label every case
  mime-oracle-r91.py --cases IN.json --scratch-root DIR --check            exit 1 if any stored label differs
Prints `MIME_ORACLE: cases=N types=T gio_sha256=… libgio_sha256=… changed=K` and exits 0/1, 2 on setup error.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

GIO = "/usr/bin/gio"
LIBGIO = "/usr/lib/libgio-2.0.so.0"
DEF = re.compile(r"^Default application for \u201c(.*)\u201d: (.*)$")
NODEF = re.compile(r"^No default applications for \u201c(.*)\u201d$")


def sha(p: str) -> str:
    return hashlib.sha256(open(os.path.realpath(p), "rb").read()).hexdigest()


def materialise(case: dict, root: str) -> None:
    for rel, spec in case.get("files", {}).items():
        if rel.startswith("/") or ".." in rel.split("/"):
            raise ValueError(f"{case['id']}: unsafe path {rel}")
        p = os.path.join(root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        if isinstance(spec, str):
            spec = {"text": spec}
        if spec.get("dir"):
            os.makedirs(p, exist_ok=True)
            continue
        if "symlink" in spec:
            os.symlink(spec["symlink"], p)
            continue
        data = base64.b64decode(spec["b64"]) if "b64" in spec else spec["text"].encode("utf-8")
        with open(p, "wb") as fh:
            fh.write(data)
        os.chmod(p, 0o755 if spec.get("exec") else 0o644)
    r = case["roots"]
    for rel in [r["config_home"], r["data_home"], *r["config_dirs"], *r["data_dirs"]]:
        if rel:
            os.makedirs(os.path.join(root, rel), exist_ok=True)


def abspaths(case: dict, root: str) -> dict:
    r = case["roots"]
    j = lambda rel: rel if rel.startswith("/") else os.path.join(root, rel)
    return {
        "config_home": j(r["config_home"]),
        "config_dirs": ":".join(j(x) for x in r["config_dirs"]),
        "data_home": j(r["data_home"]),
        "data_dirs": ":".join(j(x) for x in r["data_dirs"]),
        "path": ":".join(x if x.startswith("/") else os.path.join(root, x) for x in case["path"]),
    }


def parse(out: str, t: str) -> dict:
    lines = out.splitlines()
    res = {"default": None, "registered": None, "recommended": None}
    if not lines:
        raise ValueError(f"empty gio output for {t}")
    m = DEF.match(lines[0])
    if not m:
        if NODEF.match(lines[0]):
            return res
        raise ValueError(f"unexpected gio output for {t}: {lines[0]!r}")
    res["default"] = m.group(2)
    cur = None
    for ln in lines[1:]:
        if ln == "Registered applications:":
            cur = "registered"; res[cur] = []
        elif ln == "No registered applications":
            res["registered"] = []; cur = None
        elif ln == "Recommended applications:":
            cur = "recommended"; res[cur] = []
        elif ln == "No recommended applications":
            res["recommended"] = []; cur = None
        elif ln.startswith("\t") and cur:
            res[cur].append(ln[1:])
        else:
            raise ValueError(f"unexpected gio line for {t}: {ln!r}")
    return res


def label_case(case: dict, scratch: str) -> dict:
    root = tempfile.mkdtemp(prefix="o", dir=scratch)
    try:
        materialise(case, root)
        a = abspaths(case, root)
        env = {"HOME": root, "XDG_CONFIG_HOME": a["config_home"], "XDG_CONFIG_DIRS": a["config_dirs"],
               "XDG_DATA_HOME": a["data_home"], "XDG_DATA_DIRS": a["data_dirs"], "PATH": a["path"], "LC_ALL": "C"}
        if case.get("desktop") is not None:
            env["XDG_CURRENT_DESKTOP"] = case["desktop"]
        out = {}
        for t in case["types"]:
            r = subprocess.run([GIO, "mime", t], capture_output=True, text=True, env=env, timeout=60, cwd=root)
            if r.returncode != 0:
                raise ValueError(f"{case['id']}: gio mime {t} rc={r.returncode}: {r.stderr.strip()[:200]}")
            out[t] = parse(r.stdout, t)
        return out
    finally:
        shutil.rmtree(root, ignore_errors=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cases", required=True)
    ap.add_argument("--scratch-root", required=True)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--label")
    g.add_argument("--check", action="store_true")
    a = ap.parse_args()
    try:
        os.makedirs(a.scratch_root, exist_ok=True)
        doc = json.load(open(a.cases, encoding="utf-8"))
        cases = doc["cases"]
        ids = [c["id"] for c in cases]
        if len(set(ids)) != len(ids):
            raise ValueError("duplicate case ids")
        changed = 0
        ntypes = 0
        for c in cases:
            lab = label_case(c, a.scratch_root)
            ntypes += len(lab)
            if a.check:
                if c.get("expect") != lab:
                    changed += 1
                    print(f"changed {c['id']}: stored={json.dumps(c.get('expect'))} gio={json.dumps(lab)}")
            else:
                c["expect"] = lab
    except (OSError, ValueError, KeyError, subprocess.TimeoutExpired) as e:
        print(f"MIME_ORACLE: SETUP_ERROR {e}")
        return 2
    if a.label:
        doc["oracle"] = {"gio_sha256": sha(GIO), "libgio_sha256": sha(LIBGIO)}
        with open(a.label, "w", encoding="utf-8") as fh:
            json.dump(doc, fh, indent=1, sort_keys=True)
            fh.write("\n")
    print(f"MIME_ORACLE: cases={len(cases)} types={ntypes} gio_sha256={sha(GIO)} libgio_sha256={sha(LIBGIO)} "
          f"changed={changed}")
    return 1 if changed else 0


if __name__ == "__main__":
    sys.exit(main())
