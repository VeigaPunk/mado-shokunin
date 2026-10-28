#!/usr/bin/env python3
"""Build the junk C1 entry fixtures (J1 cheapest, J2 identifier-stuffed, J0/J-noX variants) and the 7 frozen C1 controls
applied to J1, each as a fresh scratch git repo, then run the seat's checker on every one. Scratch only; never the lane."""
import io, json, os, re, shutil, subprocess, sys, tarfile

S = "/fast/scratch/hyaku/mado-r55/R55RevC1Contract"
D = sys.argv[1]            # base fixture repo (archive of freeze commit)
CHECK = os.path.join(S, "c1check.py")
ENTRY = "corpus/knowledge/hyprland-keyboard-repeat-numlock-r55.md"
SOURCES = "corpus/SOURCES.md"
README = "corpus/README.md"
TABLES = ".ufo/waves/round-55/frozen-tables.json"
T = json.load(open(os.path.join(D, TABLES), encoding="utf-8"))
C1 = T["c1"]
COMMIT = C1["commit"]
HYP = f"https://raw.githubusercontent.com/hyprwm/Hyprland/{COMMIT}"

SID = {f"K{i:02d}": "S316" for i in range(1, 8)}
SID.update({"K08": "S319", "K09": "S319", "K10": "S378", "K11": "S379", "K12": "S379",
            "K13": "S318", "K14": "S318", "K15": "S318", "K16": "S317", "K17": "S381", "K18": "S380"})


def tree_from_base(name):
    d = os.path.join(S, "trees", name)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    subprocess.run(["git", "-C", d, "init", "-q"], check=True)
    top = subprocess.run(["git", "-C", d, "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
    assert top == d, (top, d)
    arc = subprocess.run(["git", "-C", D, "archive", "HEAD"], capture_output=True, check=True).stdout
    tarfile.open(fileobj=io.BytesIO(arc)).extractall(d)
    return d


def commit(d):
    subprocess.run(["git", "-C", d, "add", "-A"], check=True)
    subprocess.run(["git", "-C", d, "-c", "user.name=ctl", "-c", "user.email=ctl@ctl", "commit", "-q", "-m", "fixture"], check=True)
    return subprocess.run(["git", "-C", d, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()


def words6(q):
    return " ".join(sorted({w for w in re.findall(r"\w+", q) if len(w) >= 6}))


def entry(mode="filler", k17="S381"):
    sid = dict(SID)
    sid["K17"] = k17
    head = ["# Keyboard repeat rate, repeat delay and numlock on Hyprland 0.56.2 (attack fixture, not evidence)", "",
            "source: S316, S317, S318, S319, S378, S379, S380, S381",
            "verified-at: 2026-10-28", "recheck: on-release", "",
            "| id | proposition | source | anchor | quote |", "|---|---|---|---|---|"]
    rows = []
    for kind, items in (("K", C1["k"]), ("H", C1["h"])):
        for it in items:
            rid, pin, line, q = it["id"], it["pin"], it["line"], it["quote"]
            if mode == "filler":
                prop = (f"Filler proposition {rid} for the junk attack entry; not a claim." if kind == "K"
                        else f"Filler {rid} host row, not a claim.")
            else:  # identifier-stuffed: names the quote's identifiers but asserts nothing about the keyboard
                prop = f"Restates the quoted identifiers {words6(q)} without stating a keyboard fact about {rid}."
            if kind == "K":
                assert len(prop) >= 40, prop
            else:
                assert len(prop) >= 20, prop
            src = sid[rid] if kind == "K" else "host"
            rows.append(f"| {rid} | {prop} | {src} | {pin}:{line} | `{q.replace('|', chr(92) + '|')}` |")
    return "\n".join(head + rows) + "\n"


def sources_rows(k17_url_path="subprojects/wayland/1.26.0/protocol/wayland.xml", include_new=True):
    used = ENTRY
    out = []
    if include_new:
        out.append(f"| S378 | Hyprland SeatManager.cpp (junk) — {HYP}/src/managers/SeatManager.cpp | code | A | filler scope | SeatManager.cpp:175-178 @ {COMMIT} | filler teaches, nothing opened | mined | 2026-10-28 | on-release | {used} |")
        out.append(f"| S379 | Hyprland protocols core Seat.cpp (junk) — {HYP}/src/protocols/core/Seat.cpp | code | A | filler scope | Seat.cpp:441-448,603-609 @ {COMMIT} | filler teaches, nothing opened | mined | 2026-10-28 | on-release | {used} |")
        out.append(f"| S380 | Hyprland IKeyboard.hpp (junk) — {HYP}/src/devices/IKeyboard.hpp | code | A | filler scope | IKeyboard.hpp:121-123 @ {COMMIT} | filler teaches, nothing opened | mined | 2026-10-28 | on-release | {used} |")
    out.append(f"| S381 | wayland 1.26.0 wayland.xml (junk, constructed URL) — {HYP}/{k17_url_path} | spec | A | filler scope | wayland.xml:2741 @ {COMMIT} | filler teaches, nothing opened | mined | 2026-10-28 | on-release | {used} |")
    return out


def readme_row():
    return ("| `knowledge/hyprland-keyboard-repeat-numlock-r55.md` (junk attack entry) | Filler, not a claim. | junk |")


def apply(d, entry_txt=None, delete_entry=False, add_sources=None, add_readme=True, tables_mut=None, pin_mut=None):
    if delete_entry:
        pass
    else:
        p = os.path.join(d, ENTRY)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "w", encoding="utf-8").write(entry_txt)
    sp = os.path.join(d, SOURCES)
    lines = open(sp, encoding="utf-8").read().split("\n")
    idx = max(i for i, l in enumerate(lines) if l.startswith("| S377 "))
    lines[idx + 1:idx + 1] = add_sources or []
    open(sp, "w", encoding="utf-8").write("\n".join(lines))
    rp = os.path.join(d, README)
    rl = open(rp, encoding="utf-8").read().split("\n")
    if add_readme:
        j = max(i for i, l in enumerate(rl) if l.startswith("| `knowledge/hyprland-input-devices-r46.md`"))
        rl.insert(j + 1, readme_row())
    open(rp, "w", encoding="utf-8").write("\n".join(rl))
    if tables_mut:
        tables_mut(os.path.join(d, TABLES))
    if pin_mut:
        pin_mut(os.path.join(d, ".ufo/waves/round-55/fetch/Hyprland-IKeyboard.cpp"))


def run_check(d, rev, propose=False, cells="strict"):
    cmd = ["python3", "-I", CHECK, "--repo", d, "--rev", rev, "--work", os.path.join(S, "work"), "--cells", cells]
    if propose:
        cmd += ["--propose", "overlap"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.returncode, r.stdout.strip()


results = {}


def case(name, entry_txt, **kw):
    d = tree_from_base(name)
    apply(d, entry_txt=entry_txt, **kw)
    rev = commit(d)
    rc, out = run_check(d, rev, propose=True, cells="strict")
    rc2, out2 = run_check(d, rev, propose=True, cells="gfm")
    results[name] = {"rc_strict": rc, "strict": out, "rc_gfm": rc2, "gfm": out2, "rev": rev}
    print(f"[{name}]\n  strict rc={rc} {out}\n  gfm    rc={rc2} {out2}")
    return d


def mutate_text(txt, pred, old, new):
    lines = txt.split("\n")
    hits = [i for i, l in enumerate(lines) if pred(l)]
    assert len(hits) == 1, (old, hits)
    assert old in lines[hits[0]], (old, lines[hits[0]])
    lines[hits[0]] = lines[hits[0]].replace(old, new, 1)
    return "\n".join(lines)


J1 = entry("filler")
# ---- junk attack variants
case("J1_cheapest", J1, add_sources=sources_rows())
case("J2_identifier_stuffed", entry("ident"), add_sources=sources_rows())
case("J0_honest_K17_S052", entry("filler", k17="S052"), add_sources=sources_rows(include_new=True)[:3])
case("J1_no_new_source_rows", J1, add_sources=sources_rows(include_new=False)[:0] + [sources_rows()[3]])
case("J1_no_readme_row", J1, add_sources=sources_rows(), add_readme=False)
case("J1_no_entry", J1, delete_entry=True, add_sources=sources_rows())

# ---- the seven frozen C1 controls, applied to J1
def ctl(name, txt=None, delete=False, tables_mut=None, pin_mut=None):
    return case(name, txt, delete_entry=delete, add_sources=sources_rows(), tables_mut=tables_mut, pin_mut=pin_mut)

ctl("CTL1_absent", None, delete=True)
ctl("CTL2_spliced_K04", mutate_text(J1, lambda l: l.startswith("| K04 |"), "std::max(0, REPEATRATE);", "std::max(0, REPEATRATE) ;"))
ctl("CTL3_shifted_K01", mutate_text(J1, lambda l: l.startswith("| K01 |"), ":1220 |", ":1219 |"))
ctl("CTL4_wrong_source_K10", mutate_text(J1, lambda l: l.startswith("| K10 |"), "| S378 |", "| S316 |"))
ctl("CTL5_dropped_K17", "\n".join(l for l in J1.split("\n") if not l.startswith("| K17 |")) )
ctl("CTL6_forged_H02", mutate_text(J1, lambda l: l.startswith("| H02 |"), "repeat_delay = 250", "repeat_delay = 300"))

def tamper_tables(path):
    txt = open(path, encoding="utf-8").read()
    old = T["c1"]["pin_sha256"]["Hyprland-IKeyboard.cpp"]
    new = ("9" if old[0] != "9" else "8") + old[1:]
    assert txt.count(old) == 1
    open(path, "w", encoding="utf-8").write(txt.replace(old, new))

def tamper_pin(path):
    open(path, "a", encoding="utf-8").write(" ")

ctl("CTL7_pin_tamper", J1, tables_mut=tamper_tables, pin_mut=tamper_pin)

# ---- curl the constructed S381 URL and a real S378 URL (read-only network probe, no state change)
for u in [f"{HYP}/subprojects/wayland/1.26.0/protocol/wayland.xml", f"{HYP}/src/managers/SeatManager.cpp"]:
    r = subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "--max-time", "20", u],
                       capture_output=True, text=True)
    print(f"HTTP {r.stdout.strip() or r.returncode} {u}")

json.dump({k: {kk: vv for kk, vv in v.items() if kk != "tree"} for k, v in results.items()},
          open(os.path.join(S, "results.json"), "w"), indent=1)
open(os.path.join(S, "J1-entry.md"), "w", encoding="utf-8").write(J1)
open(os.path.join(S, "J2-entry.md"), "w", encoding="utf-8").write(entry("ident"))
