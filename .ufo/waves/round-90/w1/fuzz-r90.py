#!/usr/bin/env python3
"""Round-90 C1 differential fuzz: candidate mado-portals.c1.py vs the oracle.

Generates seeded random dir-mode and xdg-mode fixtures (host descriptors,
synthetic descriptors, GKeyFile configs with random escaping/whitespace/
duplication/CRLF, random XDG_CURRENT_DESKTOP strings), labels every case with
controls/portal-oracle-r90.py (the production /usr/lib/xdg-desktop-portal on a
private activation-free bus), runs the candidate through its CLI, and compares
per interface the backend list AND the reason.

Verdict mapping (per the seat spec): the oracle prints no decision line for an
interface it does not serve, so an oracle pick of [] with no reason accepts the
candidate reasons "none-key" and "no-backend".

Modes:
  (default)   generate -> labelled -> compare -> write a summary + raw
              disagreements JSON under --scratch-root.
  --verify F  label an existing case file (with id/mode/desktop/files) and
              compare; used to re-check hand-minimised disagreements.

Everything writable lives under --scratch-root.  Read-only host access is the
portal configuration chain and the lane.
"""
from __future__ import annotations

import argparse
import json
import os
import random
import shutil
import subprocess
import sys
import tempfile

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
ORACLE = LANE + "/.ufo/waves/round-90/controls/portal-oracle-r90.py"
CANDIDATE = LANE + "/.ufo/waves/round-90/build/mado-portals.c1.py"
HOST_PORTALS = "/usr/share/xdg-desktop-portal/portals"

IMPL = "org.freedesktop.impl.portal."
IFACE_NAMES = [
    "Lockdown", "Access", "Settings", "FileChooser", "AppChooser", "Print",
    "Notification", "Inhibit", "Screenshot", "Background", "Wallpaper",
    "Account", "Email", "Secret", "GlobalShortcuts", "DynamicLauncher",
    "ScreenCast", "RemoteDesktop", "Clipboard", "InputCapture", "Usb",
]
IFACES = [IMPL + n for n in IFACE_NAMES]
SEED = 900150031

DESKTOP_BASES = ["Hyprland", "KDE", "GNOME", "sway", "XFCE"]
INVALID_TOKENS = ["bad/val", "Hypr.land", "My.Desk", "x.y", "a b", " ", "\t"]
SYNTH_NAMES = ["alpha", "beta", "gamma", "delta", "epsilon", "zeta", "eta",
               "theta", "kappa", "lambda", "mako", "swayfc", "gtk2", "kde", "Zeta"]


def load_host_portals() -> dict[str, str]:
    out = {}
    for name in sorted(os.listdir(HOST_PORTALS)):
        if name.endswith(".portal"):
            with open(os.path.join(HOST_PORTALS, name), encoding="utf-8") as fh:
                out[name[:-len(".portal")]] = fh.read()
    return out


# ---------------------------------------------------------------- case generation
def rand_desktop(rng: random.Random) -> str | None:
    r = rng.random()
    if r < 0.06:
        return None
    if r < 0.10:
        return ""
    n = rng.choice([1, 1, 1, 2, 2, 3])
    toks = []
    for _ in range(n):
        q = rng.random()
        if q < 0.10:
            toks.append(rng.choice(INVALID_TOKENS))
        elif q < 0.16:
            toks.append("")
        else:
            tok = rng.choice(DESKTOP_BASES)
            if rng.random() < 0.25:
                tok = tok.upper()
            elif rng.random() < 0.10:
                tok = tok.lower()
            toks.append(tok)
    return ":".join(toks)


def valid_desktops(value: str | None) -> list[str]:
    """Mirror of xdp-portal-config.c:126-147 + get_current_lowercase_desktops."""
    if not value:
        return []
    out = []
    for tok in value.split(":"):
        if tok and all(c.isascii() and (c.isalnum() or c in "-_") for c in tok):
            out.append(tok.lower())
    return out


def iface_list(rng: random.Random, style: str) -> str:
    names = rng.sample(IFACE_NAMES, rng.choice([0, 1, 2, 3, 4, 6]))
    vals = [IMPL + n for n in names]
    if style == "foreign" and vals:
        vals[0] = "org.kde.Foo"
    elif style == "short" and vals:
        vals[0] = names[0]
    elif style == "escaped" and vals:
        vals[0] = vals[0] + "\\;x"
    sep = ";" if rng.random() < 0.75 else "; "
    out = sep.join(vals)
    if rng.random() < 0.35:
        out += ";"
    return out


def usein_list(rng: random.Random) -> str:
    toks = []
    for _ in range(rng.choice([0, 1, 2, 2, 3, 4])):
        if rng.random() < 0.12:
            toks.append(rng.choice(["My.Desk", "x.y", "a b", ""]))
        else:
            tok = rng.choice(["Hyprland", "KDE", "GNOME", "sway", "XFCE", "wlroots",
                              "gnome", "kde", "HYPRLAND", "gnome-classic"])
            if rng.random() < 0.15:
                tok = tok.upper()
            toks.append(tok)
    out = ";".join(toks)
    if rng.random() < 0.4:
        out += ";"
    return out


def descriptor(rng: random.Random, src: str, style: str) -> str:
    iface_styles = ["normal", "normal", "normal", "normal", "foreign", "short",
                    "escaped", "empty"]
    istyle = rng.choice(iface_styles)
    ifaces = "" if istyle == "empty" else iface_list(rng, istyle)
    dbus_choices = [
        f"org.freedesktop.impl.portal.desktop.{src}",
        f"org.freedesktop.impl.portal.desktop.{src}",
        f"org.example.{src}",
        "org.freedesktop.secrets",
        f"org.freedesktop.impl.portal.desktop.{src}2",
    ]
    if rng.random() < 0.10:
        dbus = rng.choice(["kde", "org", "org..a", "org.a.", "org.a b",
                           "org.1a.b", "org.a-", ""])
    else:
        dbus = rng.choice(dbus_choices)
    usein = usein_list(rng) if rng.random() < 0.70 else None
    lines = ["[portal]", f"DBusName={dbus}", f"Interfaces={ifaces}"]
    if usein is not None:
        lines.append(f"UseIn={usein}")

    if style == "no_dbusname":
        lines = [ln for ln in lines if not ln.startswith("DBusName=")]
    elif style == "no_interfaces":
        lines = [ln for ln in lines if not ln.startswith("Interfaces=")]
    elif style == "wrong_group":
        lines[0] = "[Portal]"
    elif style == "usein_bad_escape":
        lines = [ln for ln in lines if not ln.startswith("UseIn=")]
        lines.append("UseIn=kde\\q")
    elif style == "usein_trailing_backslash":
        lines = [ln for ln in lines if not ln.startswith("UseIn=")]
        lines.append("UseIn=kde\\")
    elif style == "usein_empty":
        lines = [ln for ln in lines if not ln.startswith("UseIn=")]
        lines.append("UseIn=")
    elif style == "usein_locale":
        lines = [ln for ln in lines if not ln.startswith("UseIn=")]
        lines.append("UseIn[en]=Hyprland")
    elif style == "dup_dbusname":
        i = [k for k, ln in enumerate(lines) if ln.startswith("DBusName=")][0]
        lines.insert(i + 1, f"DBusName=org.freedesktop.impl.portal.desktop.{src}x")
    elif style == "comment":
        lines.insert(1, "# synthetic descriptor")
    elif style == "iface_bad_escape" and ifaces:
        i = [k for k, ln in enumerate(lines) if ln.startswith("Interfaces=")][0]
        lines[i] = lines[i] + "\\q;"
    elif style == "crlf":
        return "\r\n".join(lines) + ("\r\n" if rng.random() < 0.5 else "")
    return "\n".join(lines) + ("\n" if rng.random() < 0.85 else "")


DESC_STYLES = (["normal"] * 6 + ["comment", "dup_dbusname", "no_dbusname",
                                 "no_interfaces", "wrong_group",
                                 "usein_bad_escape", "usein_bad_escape",
                                 "usein_trailing_backslash", "usein_empty",
                                 "usein_locale", "iface_bad_escape", "crlf"])


def config_value(rng: random.Random, pool: list[str]) -> str:
    toks = []
    for _ in range(rng.choice([0, 1, 1, 2, 2, 3])):
        q = rng.random()
        if q < 0.55 and pool:
            tok = rng.choice(pool)
        elif q < 0.68:
            tok = "none"
        elif q < 0.78:
            tok = "*"
        elif q < 0.86:
            tok = "nosuch"
        elif q < 0.92:
            tok = ""
        else:
            tok = rng.choice(["KDE", " gtk", "gtk ", "None"])
        esc = rng.random()
        if esc < 0.06:
            tok = tok + "\\s"
        elif esc < 0.09:
            tok = tok + "\\;gtk"
        elif esc < 0.11:
            tok = tok + "\\\\"
        elif esc < 0.13:
            tok = tok + "\\q"
        toks.append(tok)
    out = ";".join(toks)
    if rng.random() < 0.25:
        out += ";"
    if rng.random() < 0.15:
        out = " " + out
    return out


def config_text(rng: random.Random, pool: list[str], desktops: list[str],
                style: str) -> str:
    lines: list[str] = []
    if rng.random() < 0.25:
        lines.append("# generated config")
    if rng.random() < 0.20:
        lines.append("")
    group = rng.choice(["[preferred]", "[preferred]", "[preferred]  ",
                        "  [preferred]", "[preferred]\t", "[Preferred]",
                        "[other]"])
    if style == "key_before_group":
        lines.append("default=" + config_value(rng, pool))
    lines.append(group)
    keys = []
    for _ in range(rng.choice([0, 1, 2, 2, 3, 3, 4, 5])):
        q = rng.random()
        if q < 0.45:
            key = "default"
        elif q < 0.72:
            key = IMPL + rng.choice(IFACE_NAMES)
        elif q < 0.84:
            key = rng.choice(IFACE_NAMES)
        elif q < 0.92:
            key = "Default"
        else:
            key = "default[en]"
        sep = rng.choice(["=", "=", " = ", " =\t", "= "])
        lines.append(key + sep + config_value(rng, pool))
        keys.append(key)
        if rng.random() < 0.12 and keys:
            lines.append(rng.choice(keys) + "=" + config_value(rng, pool))
    if rng.random() < 0.10 and keys:
        lines.append(rng.choice(keys) + "=" + config_value(rng, pool))
    if style == "garbage":
        lines.append(rng.choice(["nonsense", "=x", "[preferred] x",
                                 "key with space", "default"]))
    if rng.random() < 0.10:
        lines.append("[other]")
        lines.append("default=" + config_value(rng, pool))
    if rng.random() < 0.12:
        lines.append(group)
        lines.append("default=" + config_value(rng, pool))
    text = "\n".join(lines)
    if rng.random() < 0.18:
        text = text.replace("\n", "\r\n")
    if rng.random() < 0.80:
        text += "\r\n" if "\r\n" in text else "\n"
    return text


CFG_STYLES = ["normal"] * 8 + ["key_before_group", "garbage", "garbage"]


def gen_cases(n: int, seed: int, host: dict[str, str], clean: bool = False) -> list[dict]:
    rng = random.Random(seed)
    desc_styles = [s for s in DESC_STYLES if not clean or s not in
                   ("usein_bad_escape", "usein_trailing_backslash")]
    cases: list[dict] = []
    host_names = sorted(host)
    for idx in range(n):
        mode = "dir" if rng.random() < 0.68 else "xdg"
        desktop = rand_desktop(rng)
        desktops = valid_desktops(desktop)
        files: dict[str, str] = {}
        available: list[str] = []

        if mode == "dir":
            chosen_host = rng.sample(host_names, rng.choice([0, 0, 1, 2, 2, 3, 4]))
            for src in chosen_host:
                files[src + ".portal"] = host[src]
                available.append(src)
            n_syn = rng.choice([0, 1, 1, 2, 2, 3, 4])
            for src in rng.sample(SYNTH_NAMES, n_syn):
                if src in available and rng.random() < 0.7:
                    continue
                files[src + ".portal"] = descriptor(rng, src, rng.choice(desc_styles))
                if src not in available:
                    available.append(src)
            n_cfg = rng.choice([0, 1, 1, 2, 2, 3])
            names = [d + "-portals.conf" for d in desktops]
            names += ["portals.conf"]
            rng.shuffle(names)
            for name in names[:n_cfg]:
                if name in files:
                    continue
                pool = available + ["nosuch", "unknown"] if rng.random() < 0.9 else available
                files[name] = config_text(rng, pool, desktops, rng.choice(CFG_STYLES))
        else:
            n_cfg_dirs = rng.choice([1, 1, 2])
            n_data_dirs = rng.choice([1, 2, 2, 3])
            n_syn = rng.choice([0, 1, 2, 2, 3])
            for src in rng.sample(SYNTH_NAMES, n_syn):
                layer = rng.choice(["data_home", "data_dirs"])
                sub = "xdg-desktop-portal/portals/" + src + ".portal"
                if layer == "data_home":
                    rel = "data_home/" + sub
                else:
                    rel = "data_dirs/%d/%s" % (rng.randrange(n_data_dirs), sub)
                files[rel] = descriptor(rng, src, rng.choice(desc_styles))
                available.append(src)
            if rng.random() < 0.30:
                src = rng.choice(host_names)
                layer = rng.choice(["data_home", "data_dirs"])
                sub = "xdg-desktop-portal/portals/" + src + ".portal"
                rel = ("data_home/" + sub if layer == "data_home"
                       else "data_dirs/%d/%s" % (rng.randrange(n_data_dirs), sub))
                files[rel] = descriptor(rng, src, rng.choice(["normal"] if clean else ["normal", "usein_bad_escape"]))
            available += [s for s in host_names if s not in available]
            n_cfg = rng.choice([0, 1, 2, 2, 3])
            name_choices = [d + "-portals.conf" for d in desktops] + ["portals.conf"]
            rng.shuffle(name_choices)
            for name in name_choices[:n_cfg]:
                layer = rng.choice(["config_home", "config_dirs", "config_dirs",
                                    "data_home", "data_dirs"])
                sub = "xdg-desktop-portal/" + name
                if layer == "config_home":
                    rel = "config_home/" + sub
                elif layer == "config_dirs":
                    rel = "config_dirs/%d/%s" % (rng.randrange(n_cfg_dirs), sub)
                elif layer == "data_home":
                    rel = "data_home/" + sub
                else:
                    rel = "data_dirs/%d/%s" % (rng.randrange(n_data_dirs), sub)
                if rel in files:
                    continue
                pool = available + ["nosuch", "unknown"]
                files[rel] = config_text(rng, pool, desktops, rng.choice(CFG_STYLES))
            case = {"id": f"g{idx:04d}", "mode": mode, "desktop": desktop,
                    "files": files, "n_config_dirs": n_cfg_dirs,
                    "n_data_dirs": n_data_dirs}
            cases.append(case)
            continue
        cases.append({"id": f"g{idx:04d}", "mode": mode, "desktop": desktop,
                      "files": files})
    return cases


# ---------------------------------------------------------------- fixture + candidate
def path_count(case: dict, prefix: str) -> int:
    n = 0
    for rel in case["files"]:
        parts = rel.split("/")
        if parts[0] == prefix and len(parts) > 1:
            n = max(n, int(parts[1]) + 1)
    return n


def dir_lists(case: dict) -> tuple[int, int]:
    n_cfg = max(path_count(case, "config_dirs"), case.get("n_config_dirs", 0), 1)
    n_data = max(path_count(case, "data_dirs"), case.get("n_data_dirs", 0), 1)
    return n_cfg, n_data


def materialise(case: dict, root: str) -> None:
    if case["mode"] == "dir":
        base = os.path.join(root, "portals")
        os.makedirs(base, exist_ok=True)
        for rel, text in case["files"].items():
            p = os.path.join(base, rel)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "w", encoding="utf-8", newline="") as fh:
                fh.write(text)
    else:
        for rel, text in case["files"].items():
            p = os.path.join(root, "x", rel)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "w", encoding="utf-8", newline="") as fh:
                fh.write(text)


def candidate_argv(case: dict, root: str) -> list[str]:
    argv = ["python3", "-I", CANDIDATE, "--json"]
    if case["desktop"] is None:
        argv.append("--desktop-unset")
    else:
        argv += ["--desktop", case["desktop"]]
    if case["mode"] == "dir":
        argv += ["--portal-dir", os.path.join(root, "portals")]
    else:
        n_cfg, n_data = dir_lists(case)
        cfg = ":".join(os.path.join(root, "x", "config_dirs", str(i)) for i in range(n_cfg))
        data = ":".join(os.path.join(root, "x", "data_dirs", str(i)) for i in range(n_data))
        argv += ["--config-home", os.path.join(root, "x", "config_home"),
                 "--config-dirs", cfg,
                 "--data-home", os.path.join(root, "x", "data_home"),
                 "--data-dirs", data,
                 "--sysconfdir", "/etc", "--datadir", "/usr/share"]
    return argv


def run_candidate(case: dict, root: str) -> dict:
    materialise(case, root)
    env = {"PATH": "/usr/bin:/bin", "HOME": os.path.join(root, "home"),
           "LC_ALL": "C", "TZ": "UTC"}
    os.makedirs(env["HOME"], exist_ok=True)
    try:
        proc = subprocess.run(candidate_argv(case, root), env=env, cwd=root,
                              capture_output=True, text=True, timeout=30)
    except subprocess.TimeoutExpired:
        return {"error": "candidate timeout"}
    if proc.returncode != 0:
        return {"error": f"candidate exit {proc.returncode}: {proc.stderr[-500:]}"}
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError as e:
        return {"error": f"candidate json: {e}: {proc.stdout[:200]}"}


# ---------------------------------------------------------------- comparison
def compare(label: dict, cand: dict) -> list[dict]:
    diffs = []
    opicks = label.get("oracle", {})
    oreasons = label.get("oracle_reason", {})
    cpicks = cand.get("picks", {})
    creasons = cand.get("reasons", {})
    for iface in IFACES:
        o = opicks.get(iface, [])
        c = cpicks.get(iface, [])
        orsn = oreasons.get(iface)
        crsn = creasons.get(iface)
        if o == [] and c == []:
            if orsn is None and crsn in ("none-key", "no-backend"):
                continue
            if orsn == crsn:
                continue
            diffs.append({"interface": iface, "oracle_picks": o, "candidate_picks": c,
                          "oracle_reason": orsn, "candidate_reason": crsn})
            continue
        if o != c:
            diffs.append({"interface": iface, "oracle_picks": o, "candidate_picks": c,
                          "oracle_reason": orsn, "candidate_reason": crsn})
            continue
        if orsn is not None and orsn != crsn:
            diffs.append({"interface": iface, "oracle_picks": o, "candidate_picks": c,
                          "oracle_reason": orsn, "candidate_reason": crsn})
    return diffs


def run_oracle(cases: list[dict], scratch: str, jobs: int) -> tuple[list[dict], str]:
    os.makedirs(scratch, exist_ok=True)
    cpath = os.path.join(scratch, "cases.json")
    lpath = os.path.join(scratch, "labelled.json")
    with open(cpath, "w", encoding="utf-8") as fh:
        json.dump({"cases": cases}, fh, ensure_ascii=False)
    proc = subprocess.run([sys.executable, ORACLE, "--cases", cpath, "--label", lpath,
                           "--scratch-root", os.path.join(scratch, "work"),
                           "--jobs", str(jobs)],
                          capture_output=True, text=True, timeout=1800)
    if proc.returncode != 0:
        raise SystemExit(f"oracle failed rc={proc.returncode}\n{proc.stdout}\n{proc.stderr[-4000:]}")
    with open(lpath, encoding="utf-8") as fh:
        data = json.load(fh)
    return data["cases"], proc.stdout.strip()


def candidate_batch(labels: list[dict], scratch: str) -> list[dict]:
    from concurrent.futures import ThreadPoolExecutor
    out = [None] * len(labels)

    def one(i_case):
        i, case = i_case
        root = os.path.join(scratch, "cand", f"c{i:05d}")
        os.makedirs(root, exist_ok=True)
        try:
            out[i] = run_candidate(case, root)
        finally:
            shutil.rmtree(root, ignore_errors=True)

    with ThreadPoolExecutor(8) as ex:
        list(ex.map(one, enumerate(labels)))
    return out


def summarise(labels: list[dict], cands: list[dict]) -> tuple[list[dict], int, int]:
    disagreed = []
    agreed = 0
    for label, cand in zip(labels, cands):
        if "error" in cand:
            diffs = [{"interface": "*", "oracle_picks": [], "candidate_picks": [],
                      "oracle_reason": None, "candidate_reason": None,
                      "candidate_error": cand["error"]}]
        else:
            diffs = compare(label, cand)
        if diffs:
            disagreed.append({"label": label, "cand": cand, "diffs": diffs})
        else:
            agreed += 1
    return disagreed, agreed, len(labels) - agreed


# ---------------------------------------------------------------- minimisation
def sig_of(diffs: list[dict]) -> tuple:
    return tuple(sorted(json.dumps({k: d.get(k) for k in
                                    ("interface", "oracle_picks", "candidate_picks",
                                     "oracle_reason", "candidate_reason")},
                                   sort_keys=True) for d in diffs))


def case_variants(case: dict) -> list[dict]:
    """Single-step reductions: drop one file, or drop one line from one file."""
    out = []
    files = case["files"]
    for rel in sorted(files):
        v = dict(case)
        v["files"] = {k: t for k, t in files.items() if k != rel}
        out.append(v)
    for rel in sorted(files):
        lines = files[rel].split("\n")
        if len(lines) <= 1:
            continue
        for i in range(len(lines)):
            v = dict(case)
            v["files"] = dict(files)
            v["files"][rel] = "\n".join(lines[:i] + lines[i + 1:])
            out.append(v)
    return out


def minimise(raw_paths: list[str], scratch: str, jobs: int, out_path: str) -> int:
    runs = []
    raw = []
    for path in raw_paths:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
        run = data.get("fuzz", {})
        runs.append(run)
        for e in data.get("cases", []):
            e["origin_seed"] = run.get("seed")
            raw.append(e)
    cur = []
    for e in raw:
        cur.append({"id": e.get("origin_case", e["id"]),
                    "origin_case": e.get("origin_case", e["id"]),
                    "origin_seed": e.get("origin_seed"),
                    "mode": e["mode"], "desktop": e["desktop"], "files": e["files"],
                    "target": sig_of(e["diffs"]), "orig_diffs": e["diffs"],
                    "orig_size": {"files": len(e["files"]),
                                  "chars": sum(len(t) for t in e["files"].values())}})
    for rnd in (1, 2):
        batch, owner = [], []
        for ci, c in enumerate(cur):
            variants = [{"files": c["files"]}] + case_variants(c)
            for j, v in enumerate(variants):
                batch.append({"id": f"m{ci:03d}-r{rnd}-{j:03d}", "mode": c["mode"],
                              "desktop": c["desktop"], "files": v["files"]})
                owner.append((ci, j))
        labels, oline = run_oracle(batch, os.path.join(scratch, f"min{rnd}"), jobs)
        cands = candidate_batch(labels, os.path.join(scratch, f"min{rnd}"))
        results: dict[int, list] = {}
        for lab, cand, (ci, j) in zip(labels, cands, owner):
            if "error" in cand:
                diffs = [{"interface": "*", "candidate_error": cand["error"]}]
            else:
                diffs = compare(lab, cand)
            results.setdefault(ci, []).append((j, lab, cand, diffs))
        nxt = []
        for ci, c in enumerate(cur):
            opts = [o for o in results[ci] if o[3]] or results[ci]

            def key(o):
                j, lab, cand, diffs = o
                same = sig_of(diffs) == c["target"]
                size = (sum(len(t) for t in lab["files"].values()), len(lab["files"]))
                return (0 if same else 1, size, j)

            j, lab, cand, diffs = min(opts, key=key)
            nxt.append({"id": c["id"], "origin_case": c["origin_case"],
                        "origin_seed": c["origin_seed"], "mode": lab["mode"],
                        "desktop": lab["desktop"], "files": lab["files"],
                        "target": sig_of(diffs), "orig_diffs": c["orig_diffs"],
                        "orig_size": c["orig_size"], "oracle": lab.get("oracle", {}),
                        "oracle_reason": lab.get("oracle_reason", {}),
                        "candidate": {"picks": cand.get("picks", {}),
                                      "reasons": cand.get("reasons", {})},
                        "diffs": diffs, "variant_index": j})
        cur = nxt
        print(f"MINIMISE round {rnd}: cases={len(cur)} same_signature={sum(sig_of(c['diffs']) == c['target'] for c in cur)}")
    out = {"fuzz": {"runs": runs,
                    "generated": sum(r.get("generated", 0) for r in runs),
                    "labelled": sum(r.get("labelled", 0) for r in runs),
                    "agreed": sum(r.get("agreed", 0) for r in runs),
                    "disagreed": len(cur),
                    "clean_disagreed": sum(r.get("disagreed", 0) for r in runs
                                           if r.get("seed") == 900150034)},
           "cause": ("descriptor UseIn value that fails GKeyFile unescaping: the production "
                     "binary keeps the backend with use_in=NULL, the candidate drops the "
                     "whole descriptor, which also un-shadows host-tail duplicates"),
           "upstream": ["xdg-desktop-portal-1.22.1/src/xdp-portal-config.c:244-249 "
                        "(g_key_file_get_string_list(..., \"UseIn\", NULL, error) leaves "
                        "use_in NULL and g_hash_table_insert still registers the backend)",
                        "xdg-desktop-portal-1.22.1/src/xdp-portal-config.c:195-199 "
                        "(register_portal skips a later file with an already-seen source, "
                        "so a broken-UseIn descriptor still shadows the DATADIR one)",
                        "xdg-desktop-portal-1.22.1/src/xdp-portal-config.c:367-384 "
                        "(load order: XDG data dirs, then DATADIR; XDG_DESKTOP_PORTAL_DIR "
                        "replaces the whole chain)"],
           "candidate_source": "mado-shokunin/.ufo/waves/round-90/build/mado-portals.c1.py:277-280 "
                               "(string_list(g[\"UseIn\"]) raises KeyFileError, caught, "
                               "descriptor skipped)",
           "cases": []}
    for k, c in enumerate(cur, 1):
        entry = {"id": f"f{k:02d}", "origin_case": c["origin_case"],
                 "origin_seed": c["origin_seed"], "mode": c["mode"],
                 "desktop": c["desktop"], "files": c["files"],
                 "oracle": c["oracle"], "oracle_reason": c["oracle_reason"],
                 "candidate": c["candidate"], "diffs": c["diffs"],
                 "original_diffs": c["orig_diffs"],
                 "original_size": c["orig_size"],
                 "minimised": {"files": len(c["files"]),
                               "chars": sum(len(t) for t in c["files"].values()),
                               "signature_preserved": sig_of(c["diffs"]) == c["target"]},
                 "cause": out["cause"], "upstream": out["upstream"]}
        out["cases"].append(entry)
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    print(f"MINIMISE wrote {out_path} cases={len(out['cases'])} "
          f"kept_signature={sum(e['minimised']['signature_preserved'] for e in out['cases'])}")
    return 0



def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--scratch-root", required=True)
    ap.add_argument("--seed", type=int, default=SEED)
    ap.add_argument("--cases", type=int, default=480)
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--verify")
    ap.add_argument("--clean", action="store_true",
                    help="suppress descriptors with unparseable UseIn escapes")
    ap.add_argument("--minimise", nargs="+", help="raw disagreement JSON files to minimise")
    ap.add_argument("--out")
    ap.add_argument("--summary")
    a = ap.parse_args()
    S = os.path.abspath(a.scratch_root)
    os.makedirs(S, exist_ok=True)
    host = load_host_portals()

    if a.minimise:
        dest = a.out or os.path.join(S, "fuzz-r90-disagreements.json")
        return minimise(a.minimise, os.path.join(S, "min"), a.jobs, dest)

    if a.verify:
        with open(a.verify, encoding="utf-8") as fh:
            raw = json.load(fh)
        cases = raw["cases"] if isinstance(raw, dict) else raw
        labels, oline = run_oracle(cases, os.path.join(S, "verify"), a.jobs)
        cands = candidate_batch(labels, os.path.join(S, "verify"))
        print(oline)
        bad = 0
        for label, cand in zip(labels, cands):
            diffs = compare(label, cand) if "error" not in cand else [{"interface": "*", "candidate_error": cand["error"]}]
            print(f"CASE {label['id']}: {'AGREE' if not diffs else 'DISAGREE ' + json.dumps(diffs, ensure_ascii=False)}")
            bad += bool(diffs)
        print(f"VERIFY cases={len(labels)} disagree={bad}")
        return 0 if bad == 0 else 3

    cases = gen_cases(a.cases, a.seed, host, a.clean)
    labels, oline = run_oracle(cases, os.path.join(S, "run"), a.jobs)
    cands = candidate_batch(labels, os.path.join(S, "run"))
    disagreed, agreed, ndis = summarise(labels, cands)
    print(oline)
    print(f"FUZZ seed={a.seed} generated={len(cases)} labelled={len(labels)} "
          f"agreed={agreed} disagreed={ndis}")
    out = {"fuzz": {"seed": a.seed, "generated": len(cases), "labelled": len(labels),
                    "agreed": agreed, "disagreed": ndis},
           "cases": []}
    for k, d in enumerate(disagreed, 1):
        label = d["label"]
        entry = {"id": f"f{k:02d}", "origin_case": label["id"],
                 "mode": label["mode"], "desktop": label["desktop"],
                 "files": label["files"],
                 "oracle": label.get("oracle", {}),
                 "oracle_reason": label.get("oracle_reason", {}),
                 "candidate": {"picks": d["cand"].get("picks", {}),
                               "reasons": d["cand"].get("reasons", {})},
                 "diffs": d["diffs"]}
        if "error" in d["cand"]:
            entry["candidate"]["error"] = d["cand"]["error"]
        out["cases"].append(entry)
    dest = a.out or os.path.join(S, "fuzz-r90-disagreements.json")
    with open(dest, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    if a.summary:
        with open(a.summary, "w", encoding="utf-8") as fh:
            json.dump(out["fuzz"], fh, indent=1)
            fh.write("\n")
    print(f"WROTE {dest} disagreements={len(out['cases'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
