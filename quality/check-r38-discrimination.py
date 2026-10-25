#!/usr/bin/env python3
"""mado — round-38 discrimination gate: do the v3 counters tell work from crib?

Scores a pair of admission counters against a frozen control manifest of
accept and reject trees. Each control names an instrument (`c1` the event
ground counter, `c2` the eventq census counter), a base revision, and a list
of writes; the gate clones the lane into a sandbox, applies the writes,
commits with a sandbox identity, and runs the instrument against the sandbox
HEAD. A control's `expect` is the verdict the instrument *should* print; the
instrument is scored only on agreement.

  --c1 <counter.py> --c2 <counter.py>   instruments under test
  --manifest <path>                     frozen control manifest (JSON)
  --rev <commit-ish>                    default base revision for controls
                                        without their own `rev` (the round's
                                        data revision for a green run)
  --out <path>                          write one receipt line per control
  --sandbox-root <dir>                  scratch root (default /dev/shm)

TARGET_MET iff every control's observed verdict equals its expected verdict
(MET must exit 0, MISSED exit 1; anything else is ERROR). Exit 0/1; setup 2.
Git runs with every ambient GIT_* variable removed; sandbox commits carry the
identity `sandbox <sandbox@invalid>` and never touch the lane.
"""
import argparse
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

PRED = "MADO_R38_DISCRIMINATION"
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
BASE = "f6e3247f73152a39afb86066af48f3cedf95fb0a"   # lane tip at round-38 freeze
ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
IDENT = ["-c", "user.name=sandbox", "-c", "user.email=sandbox@invalid"]
VERDICT = re.compile(r"verdict=(TARGET_MET|TARGET_MISSED)")


def sh(argv, cwd=None, env=None):
    return subprocess.run(argv, cwd=cwd, env=env or ENV, capture_output=True, text=True)


def load_counter(path):
    spec = importlib.util.spec_from_file_location("counter_mod", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def apply_writes(sb, writes, ctx):
    # Confined file primitives (SentManifestScope HIGH): every path resolves
    # against the sandbox and must stay inside it; the env carries no
    # subprocess/os/sys — py controls get re/json/hashlib (hashlib-free,
    # digest is a helper) and the confined lambdas only.
    env = {
        "sb": sb,
        "write": lambda rel, s: _write(sb, rel, s),
        "append": lambda rel, s: _append(sb, rel, s),
        "delete": lambda rel: os.remove(_confine(sb, rel)),
        "read": lambda rel: open(_confine(sb, rel), "rb").read(),
        "digest": lambda rel: hashlib.sha256(_read(sb, rel)).hexdigest(),
        "re": re,
        "json": json,
        "hashlib": hashlib,
    }
    for step in writes:
        kind = step["op"]
        if kind == "literal":
            _write(sb, step["path"], step["text"])
        elif kind == "file":
            _write(sb, step["path"], open(_confine(ctx["controls_dir"], step["src"]), "rb").read())
        elif kind == "append":
            _append(sb, step["path"], step["text"])
        elif kind == "delete":
            os.remove(_confine(sb, step["path"]))
        elif kind == "counter_fixture":
            mod = ctx["counters"][step["counter"]]
            _write(sb, step["path"], getattr(mod, step["attr"]).encode())
        elif kind == "tool_run":
            tool = _read(sb, "tools/mado-eventq.py")
            toolp = os.path.join(ctx["scratch"], "tool.py")
            _write(ctx["scratch"], "tool.py", tool)
            d = os.path.join(ctx["scratch"], "toolrun")
            os.makedirs(d, exist_ok=True)
            for rel, name in (("ss.txt", "ss.txt"), ("hyprland.log", "hyprland.log"),
                              ("journal.txt", "journal.txt")):
                if rel == "ss.txt":
                    data = _read(sb, step["ss"])
                else:
                    data = b""
                open(os.path.join(d, name), "wb").write(data)
            p = subprocess.run([sys.executable, "-I", toolp, "--ss-file", os.path.join(d, "ss.txt"),
                                "--log", os.path.join(d, "hyprland.log"), "--journal-file",
                                os.path.join(d, "journal.txt"), "--disable-logs", step.get("dl", "1")],
                               capture_output=True, text=True, cwd=d)
            body = f"tool_sha256={hashlib.sha256(tool).hexdigest()}\n" + p.stdout + f"exit={p.returncode}\n"
            _write(sb, step["path"], body.encode())
        elif kind == "py":
            exec(step["code"], env)
        else:
            raise SystemExit(f"{PRED} SETUP unknown op {kind}")


def _confine(root, rel):
    base = os.path.realpath(root)
    p = os.path.realpath(os.path.join(base, rel))
    if p != base and not p.startswith(base + os.sep):
        raise ValueError(f"path escapes sandbox: {rel}")
    return p


def _read(sb, rel):
    return open(_confine(sb, rel), "rb").read()


def _write(sb, rel, data):
    p = _confine(sb, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    mode = "wb" if isinstance(data, (bytes, bytearray)) else "w"
    with open(p, mode) as f:
        f.write(data)


def _append(sb, rel, text):
    with open(_confine(sb, rel), "a") as f:
        f.write(text)


def observed(rc, out):
    m = VERDICT.search(out)
    if not m:
        return "ERROR"
    want_rc = 0 if m.group(1) == "TARGET_MET" else 1
    return m.group(1) if rc == want_rc else "ERROR"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--c1", required=True)
    ap.add_argument("--c2", required=True)
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--out")
    ap.add_argument("--sandbox-root", default=None)
    a = ap.parse_args()
    manifest = json.load(open(a.manifest))
    controls = manifest["controls"]
    counters = {"c1": load_counter(a.c1), "c2": load_counter(a.c2)}
    ctx = {"controls_dir": os.path.dirname(os.path.abspath(a.manifest)),
           "scratch": None, "counters": counters}
    root = tempfile.mkdtemp(prefix="mado38-dsc-", dir=a.sandbox_root or None)
    ctx["scratch"] = root
    lines = []
    correct = 0
    for ctl in controls:
        cid, inst = ctl["id"], ctl["instrument"]
        rev = ctl.get("rev", a.rev)
        sb = os.path.join(root, cid)
        p = sh(["git", "clone", "-q", "--shared", LANE, sb])
        if p.returncode != 0:
            lines.append(f"control={cid} instrument={inst} expected={ctl['expect']} observed=ERROR ok=0 note=clone-failed")
            continue
        # sparse: controls only ever touch corpus/, tools/, quality/ and this
        # round's wave dir — the full wave history is GBs per clone.
        sh(["git", *IDENT, "sparse-checkout", "init", "--cone"], cwd=sb)
        sh(["git", *IDENT, "sparse-checkout", "set",
            "corpus", "tools", "quality", ".ufo/waves/round-38"], cwd=sb)
        p = sh(["git", *IDENT, "checkout", "-q", rev], cwd=sb)
        if p.returncode != 0:
            lines.append(f"control={cid} instrument={inst} expected={ctl['expect']} observed=ERROR ok=0 note=checkout-failed")
            continue
        try:
            apply_writes(sb, ctl.get("writes", []), ctx)
        except Exception as e:
            lines.append(f"control={cid} instrument={inst} expected={ctl['expect']} observed=ERROR ok=0 note=write-failed:{e}")
            continue
        sh(["git", *IDENT, "add", "-A"], cwd=sb)
        p = sh(["git", *IDENT, "commit", "-qm", f"control {cid}", "--allow-empty"], cwd=sb)
        script = a.c1 if inst == "c1" else a.c2
        extra = ["--base", ctl["base"]] if inst == "c1" and ctl.get("base") else []
        p = subprocess.run([sys.executable, "-I", script, "--repo", sb, "--rev", "HEAD", *extra],
                           capture_output=True, text=True, env=ENV)
        out = (p.stdout + p.stderr).strip()
        obs = observed(p.returncode, out)
        ok = obs == ctl["expect"]
        correct += ok
        lines.append(f"control={cid} instrument={inst} expected={ctl['expect']} observed={obs} ok={int(ok)}")
        shutil.rmtree(sb, ignore_errors=True)
    for l in lines:
        print(l)
    met = correct == len(controls)
    summary = f"{PRED}: controls={len(controls)} correct={correct}/{len(controls)} verdict={'TARGET_MET' if met else 'TARGET_MISSED'}"
    print(summary)
    if a.out:
        with open(a.out, "w") as f:
            f.write("\n".join(lines) + "\n" + summary + "\n")
    shutil.rmtree(root, ignore_errors=True)
    return 0 if met else 1


if __name__ == "__main__":
    sys.exit(main())
