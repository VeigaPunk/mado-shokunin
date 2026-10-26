#!/usr/bin/env python3
"""PRED-C1-r46 - tools/mado-devices.py joins input/device config with live keyboard and mouse state (C1, operability, capability acquisition).

Frozen at the round-46 registration (.ufo/waves/round-46/registration.md). The contract is the docstring of the
reference .ufo/waves/round-46/l1-draft/mado-devices.py. The harness (sandbox, two environments, nonce, generated
cases judged by the pinned reference) is the round-45 v2 harness (quality/counters/c1-r45-monitors-v2.py) re-cut for
this tool; nothing is imported from it.

Scores one committed revision REV (revision-addressed git reads with ambient GIT_* removed; nothing in the lane is
written; scratch only under --work, which must lie outside the repository, the counter's lane and that lane's parent
directory). TOOL = tools/mado-devices.py. TARGET_MET iff every clause holds:
  a  TOOL is a regular blob (mode 100644 or 100755) at REV.
  s  `python3 -I TOOL --selftest`, run in the sandbox below, exits 0 within 60 s and its last stdout line is exactly
     `MADO_DEVICES_SELFTEST: N/N passed` with N >= 30.
  f  every fixture of FIXTURES (quality/counters/c1-r46-fixtures.json beside this file, pinned by FIXTURES_SHA256; a
     different byte is a setup error) passes in three runs: (seed 46, environment A), (seed 46, environment B) and
     (seed NONCE, environment A). A run passes when stdout equals the fixture's expected lines exactly (each line +
     "\\n", placeholders substituted), the exit code equals the expected one and stderr is empty. Environment A =
     {PATH=<fake bin>:/usr/bin:/bin, LANG=C.UTF-8, HOME=<fresh dir>, HYPRLAND_INSTANCE_SIGNATURE=mado-r46-fixture},
     working directory `fx-*`; environment B = {PATH=<fake bin>:/usr/bin:/bin, LANG=en_US.UTF-8, HOME=<another fresh
     dir named like a real home>, HYPRLAND_INSTANCE_SIGNATURE=<40 hex>_<10 digits>_<5 digits>,
     XDG_RUNTIME_DIR=/run/user/<uid>}, working directory `job-<hex>`. NONCE is --nonce (default: drawn from os.urandom
     and printed), so the seed-46 part reproduces exactly and the nonce part cannot be precomputed. Placeholders
     {A} {B} {C} {D} become four distinct device names drawn from the seed.
  i  isolation: every tool run (selftest, fixtures, generated cases) is executed by bubblewrap with `--ro-bind / /
     --dev /dev --proc /proc --unshare-pid --unshare-net --die-with-parent`, a tmpfs over the repository, the counter's
     lane and that lane's parent directory, and a writable bind of the marker directory only; bwrap missing is a setup
     error.
  r  read-only: PATH starts with a directory holding executables `hyprctl`, `libinput`, `journalctl` and `udevadm` that
     create a marker file when run; after all runs no marker exists.
  g  generated cases: GEN = 150 configs and dumps drawn from NONCE by gen_case() below (global flat and block kb_*
     lines, device blocks by name and by bracket, merged and stale blocks, empty markers, comments and `##` escapes,
     continuations, variables, expressions, directives, scroll_factor values with prefixes, exponents, clamps and
     specials; 0-4 keyboards incl. virtual ones, 0-3 mice, tablets and touch devices; each keyboard and mouse reports
     random names/factors or, with probability 0.55, the ones MODEL expects for it, so every verdict occurs); each
     runs in environment A in the sandbox and its stdout and exit code must equal those of MODEL - the reference
     .ufo/waves/round-46/l1-draft/mado-devices.py of this counter's own lane, pinned by MODEL_SHA256 (a different byte
     is a setup error) - evaluated in-process. The model is invisible to the tool (clause i).
Final line: `PRED-C1-r46: fixtures=K/F generated=G/150 selftest=<ok|fail> readonly=<ok|fail> tool=<present|absent>
verdict=TARGET_MET|TARGET_MISSED rev=<full hash> seeds=46,<nonce>`; exit 0 iff TARGET_MET, 1 if missed, 2 on setup failure.
Clause lines `PRED-C1-r46 clause=<x> ...` precede it.
Residuals (declared): a tool holding a model of the contract is an implementation of it - the fixtures are the contract's
cases, not Hyprland's runtime; a tool can still detect a sandbox by means not varied in environment B (the non-author
reading of the tool covers it); the read-only clause catches PATH lookups only; whether the contract matches Hyprland
beyond the pins is the non-author reading; clause g's oracle is the reference, so a contract error shared by reference
and tool is invisible to it; clause s is a printed line, not capability evidence.
"""
import argparse
import hashlib
import importlib.util
import json
import os
import random
import shutil
import subprocess
import sys
import tempfile

PRED = "PRED-C1-r46"
HERE = os.path.dirname(os.path.abspath(__file__))
TOOL = "tools/mado-devices.py"
SELFTEST_MIN = 30
SEED = 46
GEN = 150
FIXTURES_PATH = os.path.join(HERE, "c1-r46-fixtures.json")
FIXTURES_SHA256 = "027ed50877b345e34b27e38b4a865be4b23f94c0cc0067ac42265ca1778e3fc1"
MODEL_PATH = os.path.join(HERE, "..", "..", ".ufo", "waves", "round-46", "l1-draft", "mado-devices.py")
MODEL_SHA256 = "b229efd08d2d329dd60ced114598943d0419dac2f3cf05b1f6c1eb506c49a33b"
ENV_GIT = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
BIG_CONFIG = "# " + "x" * 1048580 + "\n"
BIG_DUMP = b'{"keyboards": [], "mice": []' + b" " * 1048580 + b"}"


class Setup(Exception):
    pass


def git(repo, *args):
    p = subprocess.run(["git", "-C", repo, *args], capture_output=True, env=ENV_GIT)
    return p.stdout if p.returncode == 0 else None


def pinned(path, sha):
    try:
        blob = open(path, "rb").read()
    except OSError:
        raise Setup("missing %s" % os.path.basename(path))
    if hashlib.sha256(blob).hexdigest() != sha:
        raise Setup("sha256 mismatch %s" % os.path.basename(path))
    return blob


def load_fixtures():
    return json.loads(pinned(FIXTURES_PATH, FIXTURES_SHA256).decode())


def load_model():
    pinned(MODEL_PATH, MODEL_SHA256)
    spec = importlib.util.spec_from_file_location("mado_devices_model", MODEL_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def model_out(model, dump_bytes, texts):
    try:
        lines, rc = model.report(dump_bytes, texts)
    except model.Setup as e:
        lines, rc = ["MADO_DEVICES: SETUP %s" % e], 2
    return "".join(l + "\n" for l in lines), rc


VENDORS = ["razer", "logitech", "hp--inc", "keychron", "yubico", "at-translated-set-2", "elan", "synaptics", "corsair"]
MODELS = ["deathadder-v2", "g502-hero", "hyperx-alloy-origins-core", "k8-pro", "yubikey-otp+fido+ccid", "keyboard",
          "touchpad", "k70-rgb", "mx-master-3"]
SUFFIX = ["", "", "-keyboard", "-mouse", "-consumer-control", "-keypad", "-1", "-2"]


def names(seed):
    rng = random.Random(seed)
    picked = []
    while len(picked) < 4:
        n = "%s-%s%s" % (rng.choice(VENDORS), rng.choice(MODELS), rng.choice(SUFFIX))
        if all(n not in p and p not in n for p in picked):
            picked.append(n)
    return {"{A}": picked[0], "{B}": picked[1], "{C}": picked[2], "{D}": picked[3]}


def subst(obj, table):
    if isinstance(obj, str):
        for k, v in table.items():
            obj = obj.replace(k, v)
        return obj
    if isinstance(obj, list):
        return [subst(x, table) for x in obj]
    if isinstance(obj, dict):
        return {k: subst(v, table) for k, v in obj.items()}
    return obj


def make_fakebin(d, marker):
    os.makedirs(d)
    for n in ("hyprctl", "libinput", "journalctl", "udevadm"):
        p = os.path.join(d, n)
        with open(p, "w") as f:
            f.write("#!/bin/sh\n: > '%s'\nexit 0\n" % marker)
        os.chmod(p, 0o755)


LAYOUTS = ["us", "br", "de", "fr", "us,br", "zz", ""]
VARIANTS = ["", "", "intl", "nodeadkeys", ",abnt2"]
OPTIONS = ["", "compose:caps", "grp:alts_toggle,compose:caps", "ctrl:nocaps"]
FACTORS = ["0.5", "1", "1.5", "250", "-3", "0.7x", "15e-1", "2e", "fast", "0.125", "0.335", "nan", "inf", "0x10",
           "1e39", "1e-40", "", ".5"]


def gen_case(rng, table, model):
    """One random (config texts, dump dict) pair; the expected output is the model's. About half the keyboards
    report the names the model expects for them, so AGREE and OK verdicts occur."""
    nm = [table["{A}"], table["{B}"], table["{C}"], table["{D}"]]
    kbs = []
    for i in range(rng.randint(0, 4)):
        name = rng.choice(nm[:3] + ["hl-virtual-keyboard-" + nm[3], nm[0] + "-1"])
        if any(k["name"] == name for k in kbs):
            continue
        kbs.append({"address": "0x%x" % (i + 1), "name": name, "rules": rng.choice(["", "", "evdev"]),
                    "model": rng.choice(["", "", "pc105"]), "layout": rng.choice(LAYOUTS),
                    "variant": rng.choice(VARIANTS), "options": rng.choice(OPTIONS), "active_layout_index": 0,
                    "active_keymap": "English (US)", "capsLock": False, "numLock": rng.random() < 0.5,
                    "main": i == 0})
        if rng.random() < 0.05:
            kbs[-1].pop(rng.choice(["layout", "variant", "options"]))
    mice = []
    for i in range(rng.randint(0, 3)):
        name = rng.choice(nm + [nm[1] + "-mouse"])
        if any(m["name"] == name for m in mice):
            continue
        mice.append({"address": "0x%x" % (i + 10), "name": name, "defaultSpeed": 0.0,
                     "scrollFactor": rng.choice([-1.0, -1.0, 0.5, 1.5, 100.0, 0.0, 0.12, 0.34, 2.0])})
    dump = {"mice": mice, "keyboards": kbs, "tablets": [], "touch": [], "switches": []}
    if rng.random() < 0.2:
        dump["tablets"].append({"address": "0x20", "type": "tabletPad",
                                "belongsTo": {"address": "0x21", "name": rng.choice(nm)}})
    if rng.random() < 0.1:
        dump["touch"].append({"address": "0x30", "name": rng.choice(nm)})
    files = []
    for _ in range(rng.randint(1, 2)):
        lines = []
        for _ in range(rng.randint(0, 6)):
            k = rng.random()
            dev = rng.choice(nm + ["Razer DeathAdder", nm[0].upper(), "hl-virtual-keyboard-" + nm[3]])
            key = rng.choice(["kb_layout", "kb_variant", "kb_options", "kb_model", "kb_rules", "kb_file",
                              "scroll_factor", "sensitivity", "repeat_rate"])
            val = (rng.choice(FACTORS) if key == "scroll_factor" else
                   rng.choice(LAYOUTS + VARIANTS + OPTIONS + ["[[EMPTY]]", "pc105", "evdev", "~/x.xkb"]))
            if k < 0.18:
                lines.append("input {\n  %s = %s%s\n  touchpad {\n    scroll_factor = 0.4\n  }\n}" % (
                    key if key.startswith("kb_") else "kb_layout", val, rng.choice(["", " # note", " ## x"])))
            elif k < 0.3:
                lines.append("input:%s = %s" % (key if key.startswith("kb_") else "kb_options", val))
            elif k < 0.5:
                body = "\n".join("  %s = %s" % (rng.choice(["kb_layout", "kb_variant", "scroll_factor", "kb_options"]),
                                                rng.choice(FACTORS + LAYOUTS)) for _ in range(rng.randint(0, 3)))
                lines.append("device {\n  name = %s\n%s\n}" % (dev, body))
            elif k < 0.62:
                lines.append("device[%s]:%s = %s" % (dev, key, val))
            elif k < 0.7:
                lines.append("device[%s] {\n  %s = %s\n}" % (dev, key, val))
            elif k < 0.74:
                lines.append(rng.choice(["$lay = de\ninput:kb_layout = $lay", "input:kb_layout = {{1+1}}",
                                         "# hyprlang if X\n# hyprlang endif", "device:kb_layout = de",
                                         "device {\n  kb_layout = de\n}", "device[%s]:name = x" % dev]))
            elif k < 0.8:
                lines.append(rng.choice(["# input:kb_layout = de", "input:kb_layout = br,\\\nus",
                                         "input {\r\n  kb_layout = fr\r\n}", "general {\n  kb_layout = de\n}",
                                         "bind = $mod, Q, killactive", "$mod = SUPER"]))
            elif k < 0.85:
                lines.append("input:kb_options = a##b # c")
            else:
                lines.append("decoration {\n  rounding = %d\n}" % rng.randint(0, 9))
        files.append("\n".join(lines) + "\n")
    st = model.State()
    for t in files:
        model.parse_config(t, st)
    for k in kbs:
        if rng.random() < 0.55:
            exp, _ = model.expected_names(st, k["name"])
            k.update(zip(("layout", "variant", "options", "model", "rules"), exp))
    for m in mice:
        if rng.random() < 0.55:
            blk = st.devices.get(m["name"], {})
            m["scrollFactor"] = (round(min(max(blk["scroll_factor"], 0.0), 100.0), 2) if "scroll_factor" in blk
                                 else -1.0)
    return files, dump


def lane_root():
    return os.path.realpath(os.path.join(HERE, "..", ".."))


def hidden_paths(repo):
    lr = lane_root()
    return sorted({os.path.realpath(repo), lr, os.path.dirname(lr)})


def under(p, root):
    p, root = os.path.realpath(p), os.path.realpath(root)
    return p == root or p.startswith(root.rstrip("/") + "/")


def sandbox(argv, cwd, hide, marker_dir):
    cmd = ["bwrap", "--ro-bind", "/", "/", "--dev", "/dev", "--proc", "/proc", "--unshare-pid", "--unshare-net",
           "--die-with-parent"]
    for h in hide:
        cmd += ["--tmpfs", h]
    cmd += ["--bind", marker_dir, marker_dir, "--chdir", cwd, "--"]
    return cmd + argv


def env_a(home, fakebin):
    return {"PATH": fakebin + ":/usr/bin:/bin", "LANG": "C.UTF-8", "HOME": home,
            "HYPRLAND_INSTANCE_SIGNATURE": "mado-r46-fixture"}


def env_b(home, fakebin, rng):
    return {"PATH": fakebin + ":/usr/bin:/bin", "LANG": "en_US.UTF-8", "HOME": home,
            "HYPRLAND_INSTANCE_SIGNATURE": "%040x_%010d_%05d" % (rng.getrandbits(160), rng.randrange(10 ** 10),
                                                                  rng.randrange(10 ** 5)),
            "XDG_RUNTIME_DIR": "/run/user/%d" % os.getuid()}


def run_tool(tool, args, d, env, data, hide, marker_dir):
    try:
        p = subprocess.run(sandbox([sys.executable, "-I", tool] + args, d, hide, marker_dir), input=data,
                           capture_output=True, env=env, timeout=20)
    except subprocess.TimeoutExpired:
        return None
    return p


def run_fixture(tool, work, fx, table, fakebin, hide, marker_dir, variant, rng):
    prefix = "fx-" if variant == "A" else "job-%x-" % rng.getrandbits(32)
    d = tempfile.mkdtemp(dir=work, prefix=prefix)
    home = os.path.join(d, "home" if variant == "A" else "vgpnk")
    os.makedirs(home)
    if fx["dump_bytes"]:
        raw = fx["dump"].encode("latin-1")
        raw = BIG_DUMP if raw == b"@BIGDUMP" else raw
    else:
        raw = json.dumps(subst(fx["dump"], table), indent=2).encode()
    dp = os.path.join(d, "devices.json")
    with open(dp, "wb") as f:
        f.write(raw)
    data = None
    if fx["stdin"]:
        args, data = ["--devices", "-"], raw
    else:
        args = ["--devices", dp]
    configs = fx["configs"]
    if configs == "usage":
        args = ["--devices", dp]
    elif configs is None:
        cdir = os.path.join(d, "conf.d")
        os.makedirs(cdir)
        args += ["--config", cdir]
    else:
        for k, text in enumerate(configs):
            cp = os.path.join(d, "c%d.conf" % k)
            with open(cp, "w", newline="", encoding="utf-8") as f:
                f.write(BIG_CONFIG if text == "@BIG" else subst(text, table))
            args += ["--config", cp]
    env = env_a(home, fakebin) if variant == "A" else env_b(home, fakebin, rng)
    p = run_tool(tool, args, d, env, data, hide, marker_dir)
    if p is None:
        return False, "timeout"
    want = "".join(subst(l, table) + "\n" for l in fx["expect"])
    got = p.stdout.decode("utf-8", errors="replace")
    ok = p.returncode == fx["rc"] and got == want and p.stderr == b""
    why = "" if ok else "rc=%d want_rc=%d stderr=%r got=%r" % (p.returncode, fx["rc"], p.stderr[-200:], got[-300:])
    return ok, why


def run_generated(tool, work, model, rng, table, fakebin, hide, marker_dir):
    ok_n, first_fail = 0, None
    for k in range(GEN):
        texts, dump = gen_case(rng, table, model)
        raw = json.dumps(dump, indent=2).encode()
        want, rc_want = model_out(model, raw, texts)
        d = tempfile.mkdtemp(dir=work, prefix="fx-")
        home = os.path.join(d, "home")
        os.makedirs(home)
        dp = os.path.join(d, "devices.json")
        with open(dp, "wb") as f:
            f.write(raw)
        args = ["--devices", dp]
        for i, t in enumerate(texts):
            cp = os.path.join(d, "c%d.conf" % i)
            with open(cp, "w", newline="", encoding="utf-8") as f:
                f.write(t)
            args += ["--config", cp]
        p = run_tool(tool, args, d, env_a(home, fakebin), None, hide, marker_dir)
        ok = (p is not None and p.returncode == rc_want and p.stdout.decode("utf-8", "replace") == want
              and p.stderr == b"")
        ok_n += ok
        if not ok and first_fail is None:
            first_fail = (k, texts, want, rc_want)
    return ok_n, first_fail


def score(repo, rev, work, nonce):
    full = git(repo, "rev-parse", "--verify", rev + "^{commit}")
    if full is None:
        raise Setup("bad rev")
    full = full.decode().strip()
    fixtures = load_fixtures()
    model = load_model()
    ls = git(repo, "ls-tree", full, "--", TOOL)
    present = bool(ls) and ls.split()[0] in (b"100644", b"100755") and ls.split()[1] == b"blob"
    print("%s clause=a tool=%s" % (PRED, "present" if present else "absent"))
    hide = hidden_paths(repo)
    fixtures_ok, selftest, readonly, g_ok = 0, "fail", "fail", 0
    if present:
        blob = git(repo, "show", "%s:%s" % (full, TOOL))
        tdir = tempfile.mkdtemp(dir=work, prefix="tool-")
        tool = os.path.join(tdir, "mado-devices.py")
        with open(tool, "wb") as f:
            f.write(blob)
        marker_dir = tempfile.mkdtemp(dir=work, prefix="mk-")
        marker = os.path.join(marker_dir, "marker")
        fakebin = os.path.join(tempfile.mkdtemp(dir=work, prefix="bin-"), "bin")
        make_fakebin(fakebin, marker)
        sd = tempfile.mkdtemp(dir=work, prefix="st-")
        try:
            p = subprocess.run(sandbox([sys.executable, "-I", tool, "--selftest"], sd, hide, marker_dir),
                               capture_output=True, env={"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8", "HOME": sd},
                               timeout=60)
            last = p.stdout.decode("utf-8", "replace").strip().split("\n")[-1]
            parts = last.split()
            okst = False
            if p.returncode == 0 and len(parts) == 3 and parts[0] == "MADO_DEVICES_SELFTEST:" and parts[2] == "passed":
                n = parts[1].split("/")
                okst = len(n) == 2 and n[0] == n[1] and n[0].isdigit() and int(n[0]) >= SELFTEST_MIN
            selftest = "ok" if okst else "fail"
            print("%s clause=s rc=%d last=%r" % (PRED, p.returncode, last[:120]))
        except subprocess.TimeoutExpired:
            print("%s clause=s timeout" % PRED)
        rng = random.Random(nonce)
        t46, tn = names(SEED), names(nonce)
        for fx in fixtures:
            res = [run_fixture(tool, work, fx, table, fakebin, hide, marker_dir, variant, rng)
                   for table, variant in ((t46, "A"), (t46, "B"), (tn, "A"))]
            ok = all(r[0] for r in res)
            fixtures_ok += ok
            why = "; ".join("%s:%s" % (lab, r[1]) for lab, r in zip(("46A", "46B", "nA"), res) if not r[0])
            print("%s clause=f fixture=%s %s%s" % (PRED, fx["label"], "pass" if ok else "FAIL", "" if ok else " " + why))
        g_ok, first_fail = run_generated(tool, work, model, random.Random(nonce ^ 0x5DEECE66D), tn, fakebin, hide,
                                         marker_dir)
        print("%s clause=g generated=%d/%d%s" % (PRED, g_ok, GEN, "" if first_fail is None else
                                                 " first_fail=%r" % (first_fail[:2],)))
        readonly = "fail" if os.path.exists(marker) else "ok"
        print("%s clause=r marker=%s" % (PRED, "present" if readonly == "fail" else "absent"))
    met = (present and selftest == "ok" and readonly == "ok" and fixtures_ok == len(fixtures) and g_ok == GEN)
    print("%s: fixtures=%d/%d generated=%d/%d selftest=%s readonly=%s tool=%s verdict=%s rev=%s seeds=%d,%d" % (
        PRED, fixtures_ok, len(fixtures), g_ok, GEN, selftest, readonly, "present" if present else "absent",
        "TARGET_MET" if met else "TARGET_MISSED", full, SEED, nonce))
    return 0 if met else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--nonce", type=int, default=None)
    a = ap.parse_args()
    nonce = a.nonce if a.nonce is not None else int.from_bytes(os.urandom(4), "big")
    try:
        if not os.path.isdir(a.work):
            raise Setup("work dir missing")
        if shutil.which("bwrap") is None:
            raise Setup("bwrap missing")
        for h in hidden_paths(a.repo):
            if under(a.work, h):
                raise Setup("work dir inside a hidden path %s" % h)
        work = tempfile.mkdtemp(dir=a.work, prefix="c1r46-")
        try:
            return score(a.repo, a.rev, work, nonce)
        finally:
            shutil.rmtree(work, ignore_errors=True)
    except Setup as e:
        print("%s: SETUP %s" % (PRED, e))
        return 2


if __name__ == "__main__":
    sys.exit(main())
