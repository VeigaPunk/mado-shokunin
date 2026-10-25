#!/usr/bin/env python3
"""ExecStubFidelity: stub-vs-real `hyprctl getoption -j` byte-shape fidelity.

Real bytes come from the host binary (read-only verb). Stub bytes come from the
counter's own STUB (quality/counters/c1-r40-live.py, imported, not copied).
The reference tool's native_query and the BASE tool's load_live are exercised
against the REAL bytes (replayed through a fake binary and a JSON file).
"""
import importlib.machinery
import importlib.util
import json
import os
import subprocess
import sys
import tempfile

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
COUNTER = os.path.join(LANE, "quality/counters/c1-r40-live.py")
REFTOOL = os.path.join(LANE, ".ufo/waves/round-40/c1/ctl-ref-tool.py.txt")
BASE = os.path.join(LANE, ".ufo/waves/round-40/w1/ExecStubFidelity/base-mado-options.py")
OUT = os.path.dirname(os.path.abspath(__file__))
REAL_HYPRCTL = "/usr/bin/hyprctl"

# 12 keys: 3 int, 2 float, 3 str, 4 custom; plus one absent key.
KEYS = [
    ("animations:enabled", "int"),
    ("general:border_size", "int"),
    ("group:groupbar:text_color", "int"),
    ("decoration:blur:brightness", "float"),
    ("cursor:zoom_factor", "float"),
    ("general:layout", "str"),
    ("input:kb_model", "str"),
    ("misc:font_family", "str"),
    ("general:col.active_border", "custom"),
    ("general:gaps_in", "custom"),
    ("group:col.border_locked_active", "custom"),
    ("group:groupbar:font_weight_active", "custom"),
    ("misc:zz-no-such-option-r40", "absent"),
]


def load(path, name):
    spec = importlib.util.spec_from_loader(
        name, importlib.machinery.SourceFileLoader(name, path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def real_reply(key):
    p = subprocess.run([REAL_HYPRCTL, "getoption", "-j", key],
                       capture_output=True)
    return p.returncode, p.stdout, p.stderr


def record_of(key, raw):
    """The counter's stub table record for a real reply (form+value+set)."""
    if raw.strip() == b"no such option":
        return None
    rec = json.loads(raw)
    form = [f for f in ("int", "float", "str", "custom") if f in rec][0]
    return {"option": key, form: rec[form], "set": rec["set"]}


def main():
    counter = load(COUNTER, "c1_counter")
    ref = load(REFTOOL, "ctl_ref_tool")
    tmp = tempfile.mkdtemp(prefix="stubfid-")
    report = {"real": {}, "stub": {}, "byte_equal": {}, "deltas": []}

    table = {}
    real_bytes = {}
    for key, form in KEYS:
        rc, out, err = real_reply(key)
        real_bytes[key] = out
        report["real"][key] = {"rc": rc, "len": len(out), "repr": repr(out),
                               "stderr": repr(err)}
        with open(os.path.join(OUT, "real-%s.bin" % key.replace(":", "_")),
                  "wb") as fh:
            fh.write(out)
        table[key] = record_of(key, out)

    # --- stub bytes: counter's own STUB, table built from the real values
    stub = counter.make_stub(tmp, "stub", table, mode="ok")
    for key, form in KEYS:
        p = subprocess.run([stub, "getoption", "-j", key], capture_output=True)
        report["stub"][key] = {"rc": p.returncode, "len": len(p.stdout),
                               "repr": repr(p.stdout)}
        report["byte_equal"][key] = p.stdout == real_bytes[key]
        if p.stdout != real_bytes[key]:
            report["deltas"].append({"key": key, "form": form,
                                     "real": repr(real_bytes[key]),
                                     "stub": repr(p.stdout)})

    # --- reference tool parses the REAL bytes (replay binary = verbatim copy)
    replay_dir = os.path.join(tmp, "replay")
    os.makedirs(replay_dir)
    for key, form in KEYS:
        safe = key.replace(":", "_")
        with open(os.path.join(replay_dir, safe), "wb") as fh:
            fh.write(real_bytes[key])
    replay = os.path.join(replay_dir, "hyprctl")
    with open(replay, "w") as fh:
        fh.write("#!%s\nimport os,sys\n"
                 "p=os.path.join(os.path.dirname(os.path.abspath(__file__)),"
                 "sys.argv[3].replace(':','_'))\n"
                 "sys.stdout.buffer.write(open(p,'rb').read())\n"
                 % sys.executable)
    os.chmod(replay, 0o755)
    ref_parse = {}
    for key, form in KEYS:
        try:
            ref_parse[key] = repr(ref.native_query(replay, key))
        except Exception as exc:                        # noqa: BLE001
            ref_parse[key] = "RAISED %s: %s" % (type(exc).__name__, exc)
    report["ref_tool_parses_real_bytes"] = ref_parse

    # --- BASE tool: no --live/--hyprctl/--probe; load_live on native replies
    base = load(BASE, "base_tool")
    base_live = {}
    native_file = os.path.join(tmp, "native.json")
    with open(native_file, "w") as fh:
        json.dump({k: json.loads(v) for k, v in real_bytes.items()
                   if v.strip() != b"no such option"}, fh)
    try:
        base.load_live(native_file)
        base_live["load_live"] = "accepted"
    except Exception as exc:                            # noqa: BLE001
        base_live["load_live"] = "REJECTED %s: %s" % (type(exc).__name__, exc)
    p = subprocess.run([sys.executable, "-I", BASE, "--home", tmp, "--live"],
                       capture_output=True, text=True)
    base_live["--live"] = {"rc": p.returncode,
                           "stderr_tail": p.stderr.strip().splitlines()[-1:]}
    p = subprocess.run([sys.executable, "-I", BASE, "--home", tmp,
                        "--hyprctl", "x"], capture_output=True, text=True)
    base_live["--hyprctl"] = {"rc": p.returncode,
                              "stderr_tail": p.stderr.strip().splitlines()[-1:]}
    report["base_tool"] = base_live

    # --- stub shape capability probes (shapes the real binary emits)
    probes = {}
    special = {
        "float-6dp": {"option": "x", "float": 0.6, "set": True},
        "set-false": {"option": "x", "int": 0, "set": False},
        "str-empty": {"option": "x", "str": "", "set": True},
        "str-nonascii": {"option": "x", "str": "Sans\u00e9\u4e2d", "set": True},
        "str-quote": {"option": "x", "str": 'a"b\\c', "set": True},
        "str-newline": {"option": "x", "str": "a\nb", "set": True},
        "int-big": {"option": "x", "int": 4294967295, "set": True},
        "float-exp": {"option": "x", "float": 1e-05, "set": True},
        "order-form-first": {"int": 1, "option": "x", "set": True},
    }
    for name, rec in special.items():
        d = counter.make_stub(tmp, "p-" + name, {"x": rec}, mode="ok")
        p = subprocess.run([d, "getoption", "-j", "x"], capture_output=True)
        probes[name] = repr(p.stdout)
    d = counter.make_stub(tmp, "p-absent", {}, mode="ok")
    probes["absent"] = repr(subprocess.run(
        [d, "getoption", "-j", "x"], capture_output=True).stdout)
    report["stub_probes"] = probes

    report["stub_argv_contract"] = {
        "bad-argv": repr(subprocess.run(
            [d, "getoption", "x"], capture_output=True).stdout),
    }

    print(json.dumps(report, indent=1))
    subprocess.run(["rm", "-rf", tmp])
    return 0


if __name__ == "__main__":
    sys.exit(main())
