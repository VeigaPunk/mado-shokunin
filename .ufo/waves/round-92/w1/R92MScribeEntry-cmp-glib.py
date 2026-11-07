#!/usr/bin/env python3
"""Compare the round-91 GLib resolver's answer with the xdg-mime label, per L1 case. DRAFT."""
import base64, json, os, shutil, subprocess, sys, tempfile

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
CASES = LANE + "/.ufo/waves/round-92/controls/xdgmime-cases-r92-l1.json"
GLIB = LANE + "/tools/mado-mime.py"
SCRATCH = "/fast/scratch/hyaku/mado-r92/R92MScribeEntry/cmp"

cases = json.load(open(CASES))["cases"]
os.makedirs(SCRATCH, exist_ok=True)


def sub(v, root):
    return v.replace("{ROOT}", root)


def materialise(case, root):
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
        open(p, "wb").write(data)
    for rel, spec in items:
        if "mode" in spec and "symlink" not in spec:
            os.chmod(os.path.join(root, rel), int(spec["mode"], 8))


rows = []
for c in cases:
    root = tempfile.mkdtemp(prefix="c-", dir=SCRATCH)
    materialise(c, root)
    env = {k: sub(v, root) for k, v in c["env"].items()}
    args = [sys.executable, "-I", GLIB]
    for flag, var in (("--config-home", "XDG_CONFIG_HOME"), ("--config-dirs", "XDG_CONFIG_DIRS"),
                      ("--data-home", "XDG_DATA_HOME"), ("--data-dirs", "XDG_DATA_DIRS"),
                      ("--path", "PATH")):
        if var in env:
            args += [flag, env[var]]
    if "XDG_CURRENT_DESKTOP" in env:
        args += ["--desktop", env["XDG_CURRENT_DESKTOP"]]
    else:
        args += ["--desktop-unset"]
    args += ["--json"] + list(c["types"])
    p = subprocess.run(args, cwd=root, env={"HOME": env.get("HOME", root + "/home"), "PATH": "/usr/bin:/bin"},
                       capture_output=True)
    if p.returncode != 0:
        rows.append({"id": c["id"], "error": p.returncode, "stderr": p.stderr.decode()[:200]})
        shutil.rmtree(root, ignore_errors=True)
        continue
    got = json.loads(p.stdout)
    defaults = {r["type"]: r["default"] for r in got["results"]}
    for t, exp in c["expect"].items():
        rows.append({"id": c["id"], "type": t, "xdg": exp["default"], "glib": defaults.get(t),
                     "same": exp["default"] == defaults.get(t), "xdg_rc": exp["rc"]})
    shutil.rmtree(root, ignore_errors=True)

json.dump(rows, open(SCRATCH + "/cmp.json", "w"), indent=1)
diff = [r for r in rows if not r.get("same")]
print("cases", len(cases), "rows", len(rows), "differ", len(diff), "errors", sum(1 for r in rows if "error" in r))
for r in [x for x in diff if "type" in x]:
    print(f'{r["id"]:46s} {r["type"]:26s} xdg={r["xdg"]!r:34s} glib={r["glib"]!r}')
