#!/usr/bin/env python3
"""R55CritControls scratch lab (NOT a lane artifact).

Honest reference C1 checker written from registration.md §C1, a lane-model builder, control and probe
mutators, and harness-shaped helpers. Every git call names -C; every temp file lives under SCRATCH.
Defect worked around (recorded in cheats.md): the frozen K16 quote contains '|' ('||'), so a row cannot
satisfy "no | inside a cell"; the lab splits K/H rows into 5 cells and joins the tail back verbatim.
"""
import argparse, hashlib, io, json, os, re, subprocess, sys, tarfile

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
SCRATCH = "/fast/scratch/hyaku/mado-r55/R55CritControls"
FREEZE = "54dacbd843d64ba744cd3f1bdc2ec622e5010039"
ROUND = ".ufo/waves/round-55"
EMBED = "bf46c8896a1861fec746f8900aabe54faf7aaaa3ff5691ed0a05e8e9d4179490"
ENTRY = "corpus/knowledge/hyprland-keyboard-repeat-numlock-r55.md"
COMMIT = "efb50993780079460b0cbed1363e2166a2de1d9f"
INDEX_ROW = "| `knowledge/hyprland-keyboard-repeat-numlock-r55.md` "
CTL_ID = ["-c", "user.name=ctl", "-c", "user.email=ctl@ctl"]
L1_ID = ["-c", "user.name=L1", "-c", "user.email=l1@lane.model"]
SID = {"K01": "S316", "K02": "S316", "K03": "S316", "K04": "S316", "K05": "S316", "K06": "S316",
       "K07": "S316", "K08": "S319", "K09": "S319", "K10": "S378", "K11": "S379", "K12": "S379",
       "K13": "S318", "K14": "S318", "K15": "S318", "K16": "S317", "K17": "S052", "K18": "S380"}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def git(repo, *args, identity=None):
    return subprocess.run(["git", "-C", repo] + (identity or []) + list(args), capture_output=True)


def blob(repo, rev, path):
    p = git(repo, "cat-file", "blob", f"{rev}:{path}")
    return p.stdout if p.returncode == 0 else None


def resolve(repo, rev):
    p = git(repo, "rev-parse", "--verify", "-q", f"{rev}^{{commit}}")
    return p.stdout.decode().strip() if p.returncode == 0 else None


def cells(line, n=None):
    """Split a markdown row. With n, the tail beyond n-1 separators is kept verbatim (joined by '|')."""
    s = line.strip()
    if not (s.startswith("|") and s.endswith("|")):
        return None
    parts = s[1:-1].split("|")
    if n is not None and len(parts) > n:
        parts = parts[:n - 1] + ["|".join(parts[n - 1:])]
    return [p.strip() for p in parts]


def url_of(cell):
    m = re.search(r"https?://\S+", cell)
    return m.group(0) if m else ""


def registry(repo, rev):
    reg = {}
    b = blob(repo, rev, "corpus/SOURCES.md") or b""
    for ln in b.decode("utf-8", "replace").split("\n"):
        c = cells(ln)
        if c and re.fullmatch(r"S\d{3}", c[0]) and len(c) == 11:
            reg[c[0]] = c
    return reg


def check(repo, rev, tables_sha=EMBED):
    """Honest reference C1 check. Returns (legs, counts)."""
    R = resolve(repo, rev)
    if R is None:
        raise SystemExit(2)
    legs = []

    def miss(x):
        if x not in legs:
            legs.append(x)

    tb = blob(repo, R, f"{ROUND}/frozen-tables.json")
    if tb is None:
        raise SystemExit(2)
    if sha(tb) != tables_sha:
        miss("tables_sha")
    T = json.loads(tb)
    c1 = T["c1"]
    pin_dir = c1["pin_dir"]
    for f, h in c1["pin_sha256"].items():
        b = blob(repo, R, f"{pin_dir}/{f}")
        if b is None or sha(b) != h:
            miss("pin_hash")
            break

    def pinline(p, n):
        b = blob(repo, R, f"{pin_dir}/{p}")
        if b is None:
            return None
        L = b.decode("utf-8", "replace").split("\n")
        return L[n - 1] if 0 < n <= len(L) else None

    rd = (blob(repo, R, "corpus/README.md") or b"").decode("utf-8", "replace").split("\n")
    if sum(1 for l in rd if l.startswith(INDEX_ROW)) != 1:
        miss("index")
    ent = blob(repo, R, c1["entry"])
    lines = []
    if ent is None:
        miss("entry_absent")
    else:
        lines = ent.decode("utf-8", "replace").split("\n")
        src = [l for l in lines if l.startswith("source:")]
        if not (src and re.search(r"S\d{3}", src[0])
                and any(l.startswith("verified-at: 2026-10-28") for l in lines)
                and any(l.startswith("recheck:") for l in lines)):
            miss("provenance")
    rows = {}
    for l in lines:
        c = cells(l, 5)
        if c and re.fullmatch(r"[KH]\d\d", c[0]):
            rows.setdefault(c[0], []).append(c)
    reg = registry(repo, R)
    ok, srcok = {}, {}
    for row in c1["k"] + c1["h"]:
        rid, pin, line, q = row["id"], row["pin"], row["line"], row["quote"]
        rs = rows.get(rid, [])
        if len(rs) != 1 or len(rs[0]) != 5:
            miss(f"row:{rid}")
            ok[rid] = False
            continue
        c = rs[0]
        good = True
        if c[3] != f"{pin}:{line}":
            miss(f"anchor:{rid}")
            good = False
        if c[4] != f"`{q}`":
            miss(f"quote:{rid}")
            good = False
        pl = pinline(pin, line)
        if rid.startswith("H"):
            # Reading chosen (ambiguity A3 in cheats.md): host: tests the quote IN THE ROW CELL, because the
            # frozen quote is always a substring of its own pin line and the leg could otherwise never fire.
            if pl is None or c[4].strip("`") not in pl:
                miss(f"host:{rid}")
                good = False
        elif pl is None or q not in pl:
            miss(f"quote:{rid}")
            good = False
        ok[rid] = good
        if rid.startswith("K"):
            r = reg.get(c[2])
            url = url_of(r[1]) if r else ""
            wayland_ok = pin.startswith("wayland") and "1.26.0" in url  # lab waiver, see cheats.md
            sok = bool(r) and url.endswith(c1["source_suffix"][pin]) and r[7] == "mined" \
                and (COMMIT in url or wayland_ok)
            srcok[rid] = sok
            if not sok:
                miss(f"source_cell:{rid}")
    m = 0
    for r in reg.values():
        if r[8] == c1["opened"] and r[3] == "A" and r[7] == "mined":
            u = url_of(r[1])
            if any(u.endswith(c1["source_suffix"][p]) for p in c1["new_row_pins"]) and ENTRY in r[10]:
                m += 1
    if m < c1["new_rows_min"]:
        miss("new_rows")
    counts = dict(rows=sum(1 for k in c1["k"] if ok.get(k["id"])),
                  hosts=sum(1 for h in c1["h"] if ok.get(h["id"])),
                  sources=sum(1 for k in c1["k"] if srcok.get(k["id"])), new_rows=m)
    return legs, counts


def line_of(rev, legs, counts):
    v = "TARGET_MET" if not legs else "TARGET_MISSED"
    return (f"MADO_KBD_ENTRY: rev={rev} rows={counts['rows']}/18 hosts={counts['hosts']}/6 "
            f"sources={counts['sources']}/18 new_rows={counts['new_rows']}/3 verdict={v} "
            f"missed={','.join(legs) if legs else 'none'}\n")


GREEN_COUNTS = {"rows": 18, "hosts": 6, "sources": 18, "new_rows": 3}
UNIVERSE = (["tables_sha", "entry_absent", "provenance", "index", "pin_hash", "new_rows"]
            + [f"{p}:K{i:02d}" for p in ("row", "anchor", "quote", "source_cell") for i in range(1, 19)]
            + [f"{p}:H{i:02d}" for p in ("row", "anchor", "quote", "host") for i in range(1, 7)])


def honest_eval(repo, rev, work, tables_sha=EMBED):
    legs, counts = check(repo, rev, tables_sha)
    return line_of(rev, legs, counts), (0 if not legs else 1)


def cli(evaluate, argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--work", required=True)
    a = ap.parse_args(argv)
    line, rc = evaluate(a.repo, a.rev, a.work)
    sys.stdout.write(line)
    sys.exit(rc)


# ---------- tree builders / mutators (scratch only) ----------

def init_repo(d):
    os.makedirs(d, exist_ok=False)
    git(d, "init", "-q")
    top = git(d, "rev-parse", "--show-toplevel").stdout.decode().strip()
    assert os.path.realpath(top) == os.path.realpath(d), (top, d)


def commit_all(d, identity, msg):
    git(d, "add", "-A")
    p = git(d, "commit", "-q", "-m", msg, identity=identity)
    assert p.returncode == 0, p.stderr.decode()


def edit_line(path, prefix, old, new):
    L = open(path, encoding="utf-8").read().split("\n")
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (path, prefix, len(idx))
    assert L[idx[0]].count(old) == 1, (path, prefix, old)
    L[idx[0]] = L[idx[0]].replace(old, new)
    open(path, "w", encoding="utf-8").write("\n".join(L))


def drop_line(path, prefix):
    L = open(path, encoding="utf-8").read().split("\n")
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (path, prefix, len(idx))
    del L[idx[0]]
    open(path, "w", encoding="utf-8").write("\n".join(L))


def dup_line(path, prefix):
    L = open(path, encoding="utf-8").read().split("\n")
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (path, prefix, len(idx))
    L.insert(idx[0] + 1, L[idx[0]])
    open(path, "w", encoding="utf-8").write("\n".join(L))


def build_entry(T):
    c1 = T["c1"]
    out = ["# Hyprland keyboard repeat rate, repeat delay and numlock (r55)", "",
           "source: S316, S319, S318, S317, S052, S378, S379, S380",
           "verified-at: 2026-10-28", "recheck: re-pin on the next Hyprland tag", "",
           "| id | proposition | source | anchor | quote |", "|---|---|---|---|---|"]
    for r in c1["k"]:
        out.append(f"| {r['id']} | proposition text for {r['id']} long enough for the forty character rule "
                   f"| {SID[r['id']]} | {r['pin']}:{r['line']} | `{r['quote']}` |")
    for r in c1["h"]:
        out.append(f"| {r['id']} | host proposition for {r['id']} long enough for the twenty char rule "
                   f"| host | {r['pin']}:{r['line']} | `{r['quote']}` |")
    return "\n".join(out) + "\n"


SOURCES_BASE = [
    ("S316", "Hyprland v0.56.2 input manager", "https://raw.githubusercontent.com/hyprwm/Hyprland/" + COMMIT + "/src/managers/input/InputManager.cpp", "2026-10-19"),
    ("S319", "Hyprland v0.56.2 keyboard base", "https://raw.githubusercontent.com/hyprwm/Hyprland/" + COMMIT + "/src/devices/IKeyboard.cpp", "2026-10-19"),
    ("S318", "Hyprland v0.56.2 config values", "https://raw.githubusercontent.com/hyprwm/Hyprland/" + COMMIT + "/src/config/values/ConfigValues.cpp", "2026-10-19"),
    ("S317", "Hyprland v0.56.2 legacy config manager", "https://raw.githubusercontent.com/hyprwm/Hyprland/" + COMMIT + "/src/config/legacy/ConfigManager.cpp", "2026-10-19"),
    ("S052", "Tagged Wayland core input specification", "https://gitlab.freedesktop.org/wayland/wayland/-/raw/1.26.0/protocol/wayland.xml", "2026-10-19"),
]
SOURCES_NEW = [
    ("S378", "Hyprland v0.56.2 seat manager", "src/managers/SeatManager.cpp"),
    ("S379", "Hyprland v0.56.2 core seat protocol", "src/protocols/core/Seat.cpp"),
    ("S380", "Hyprland v0.56.2 keyboard header", "src/devices/IKeyboard.hpp"),
]


def sources_row(sid, title, url, opened, used_by):
    return (f"| {sid} | {title} — {url} | code | A | scope | anchor | teaches | mined | {opened} | "
            f"recheck | {used_by} |")


def build_lane_model(LM):
    """Two-commit model of the lane at the entry-landed state. Commits by L1 (not ctl)."""
    init_repo(LM)
    arch = subprocess.run(["git", "-C", LANE, "archive", FREEZE, f"{ROUND}/fetch",
                           f"{ROUND}/frozen-tables.json"], capture_output=True).stdout
    tarfile.open(fileobj=io.BytesIO(arch)).extractall(LM)
    os.makedirs(os.path.join(LM, "corpus/knowledge"), exist_ok=True)
    open(os.path.join(LM, "corpus/README.md"), "w").write(
        "# corpus\n\n| Coverage | Note |\n|---|---|\n| `knowledge/hyprland-config-plane.md` | base row |\n")
    base = ["# SOURCES", "", "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |",
            "|---|---|---|---|---|---|---|---|---|---|---|"]
    for sid, t, u, op in SOURCES_BASE:
        base.append(sources_row(sid, t, u, op, "corpus/knowledge/hyprland-config-plane.md"))
    open(os.path.join(LM, "corpus/SOURCES.md"), "w").write("\n".join(base) + "\n")
    commit_all(LM, L1_ID, "lane base (model)")
    T = json.load(open(os.path.join(LM, ROUND, "frozen-tables.json")))
    open(os.path.join(LM, ENTRY), "w").write(build_entry(T))
    with open(os.path.join(LM, "corpus/README.md"), "a") as f:
        f.write(f"{INDEX_ROW}| keyboard repeat rate, delay and numlock |\n")
    with open(os.path.join(LM, "corpus/SOURCES.md"), "a") as f:
        for sid, t, suf in SOURCES_NEW:
            f.write(sources_row(sid, t, "https://raw.githubusercontent.com/hyprwm/Hyprland/" + COMMIT + "/" + suf,
                                "2026-10-28", ENTRY) + "\n")
    commit_all(LM, L1_ID, "entry landed (model)")
    return LM


def clone_of(src, dst):
    p = subprocess.run(["git", "clone", "-q", src, dst], capture_output=True)
    assert p.returncode == 0, p.stderr.decode()
    top = git(dst, "rev-parse", "--show-toplevel").stdout.decode().strip()
    assert os.path.realpath(top) == os.path.realpath(dst)
    return dst


def make_control_tree(good, rev, D, mutate):
    """Scratch single-commit tree from the good tree at rev, committed by ctl (harness-shaped)."""
    init_repo(D)
    arch = subprocess.run(["git", "-C", good, "archive", rev], capture_output=True).stdout
    tarfile.open(fileobj=io.BytesIO(arch)).extractall(D)
    mutate(D)
    commit_all(D, CTL_ID, "control")
    return D


def run_counter(counter, repo, rev, work):
    p = subprocess.run(["python3", "-I", counter, "--repo", repo, "--rev", rev, "--work", work],
                       capture_output=True, text=True)
    return p.returncode, p.stdout.strip()


def parse_missed(out):
    m = re.search(r"verdict=(\S+) missed=(\S+)$", out)
    if not m:
        return None, None
    return m.group(1), ([] if m.group(2) == "none" else m.group(2).split(","))
