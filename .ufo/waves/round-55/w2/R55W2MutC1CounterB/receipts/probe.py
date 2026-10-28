import importlib.util, json, os, sys
REPO = "/fast/scratch/hyaku/mado-r55/R55W2MutC1CounterB/repo"
WORK = "/fast/scratch/hyaku/mado-r55/R55W2MutC1CounterB/work/probe"
M = "/fast/scratch/hyaku/mado-r55/R55W2MutC1CounterB/mutants/"
ORIG = REPO + "/quality/counters/c1-r55-kbd-entry.py"
spec = importlib.util.spec_from_file_location("orig", ORIG)
orig = importlib.util.module_from_spec(spec); spec.loader.exec_module(orig)
tb = open(REPO + "/.ufo/waves/round-55/frozen-tables-v2.json", "rb").read()
c = orig.valid_shape(json.loads(tb.decode()))
pins = {n: open(REPO + "/" + c["pin_dir"] + "/" + n, "rb").read() for n in c["pin_sha256"]}
base = WORK + "/b"; os.makedirs(base, exist_ok=True)
def good(): return orig.good_files(tb, pins, c)
def srcmap(f, fn):
    t = orig.text_of(f[orig.SOURCES_PATH])
    f[orig.SOURCES_PATH] = "\n".join(fn(l) if l.startswith("| S378 |") else l for l in t.split("\n")).encode()
def run(script, files):
    D = orig.build_repo(base, "p", files)
    rc, out, err = orig.run_counter(script, D, "HEAD", base + "/w")
    return (out.strip() or "rc=%d stderr=%s" % (rc, err.strip()[-100:])).replace("MADO_KBD_ENTRY: rev=HEAD ", "")
P = {}
P["P0 good tree"] = (lambda f: None, "orig")
P["P1 frozen commit shortened to 7 hex in tables (M02)"] = (
    lambda f: f.__setitem__(orig.TABLES_PATH, json.dumps({"c1": dict(json.loads(tb.decode())["c1"], commit=c["commit"][:7])}).encode()), "m02")
P["P2 S378 registry URL without frozen commit (M03)"] = (
    lambda f: srcmap(f, lambda l: l.replace(c["commit"], "0" * 40)), "m03")
P["P3a K02 proposition 39 chars (M05)"] = (
    lambda f: orig.edit_row(f, "K02", "Synthetic proposition for K02 long enough for the forty character floor", "P" * 39), "m05")
P["P3b K02 proposition 40 chars (M05 boundary pass)"] = (
    lambda f: orig.edit_row(f, "K02", "Synthetic proposition for K02 long enough for the forty character floor", "P" * 40), "m05")
P["P4a H04 proposition 19 chars (M06)"] = (
    lambda f: orig.edit_row(f, "H04", "Synthetic host proposition H04 ok", "H" * 19), "m06")
P["P5 provenance source S-id 4 digits S3160 (M07)"] = (
    lambda f: orig.edit(f, orig.ENTRY_PATH, "source: S316, S317, S318, S319, S052, S378, S379, S380", "source: S3160"), "m07")
P["P6 S378 registry row compact pipes |S378| (M08)"] = (
    lambda f: srcmap(f, lambda l: l.replace("| S378 | ", "|S378| ", 1)), "m08")
P["P7 K02 proposition with leading space (M14)"] = (
    lambda f: orig.edit_row(f, "K02", "| K02 | Synthetic", "| K02 |  Synthetic"), "m14")
P["P8 S378 new row tier B (M15)"] = (
    lambda f: srcmap(f, lambda l: l.replace("| code | A | scope", "| code | B | scope", 1)), "m15")
P["P9 S378 new row opened 2026-10-27 (M16)"] = (
    lambda f: srcmap(f, lambda l: l.replace("| mined | 2026-10-28 |", "| mined | 2026-10-27 |", 1)), "m16")
P["P10 extra non-id line 'K03 extra' after K03 row (M20)"] = (
    lambda f: orig.edit(f, orig.ENTRY_PATH, orig.row_of(f, "K03") + "\n", orig.row_of(f, "K03") + "\n| K03 extra | prose note |\n"), "m20")
P["P11 K02 source cell S316x (M22 equivalence probe)"] = (
    lambda f: orig.edit_row(f, "K02", "| S316 |", "| S316x |"), "m22")
for name, (mut, mname) in P.items():
    files = good(); mut(files)
    o = run(ORIG, files)
    files2 = good(); mut(files2)
    m = run(M + mname + ".py", files2) if mname != "orig" else o
    print("%-58s ORIG: %s\n%-58s MUT %s: %s" % (name, o, "", mname, m))
    print()

# P12: pin bytes whose anchored line for K04 no longer holds the frozen quote (pin hash now mismatches)
files = good(); pb = dict(pins); name = "Hyprland-InputManager.cpp"
pb[name] = pins[name].replace(b"std::max(0, REPEATRATE);", b"std::max(0, REPEATRATEX);")
files2 = orig.good_files(tb, pb, c)
o = run(ORIG, files2); m = run(M + "m24.py", orig.good_files(tb, pb, c))
print("%-58s ORIG: %s\n%-58s MUT m24: %s\n" % ("P12 pin line for K04 altered, hash now mismatched (M24)", o, "", m))

# P13: non-new Hyprland pin (K01 -> Hyprland-InputManager.cpp, source S316): S316 registry URL without frozen commit
def s316(l): return l.replace(c["commit"], "0" * 40) if l.startswith("| S316 |") else l
f13 = good(); t13 = orig.text_of(f13[orig.SOURCES_PATH]); f13[orig.SOURCES_PATH] = "\n".join(s316(l) for l in t13.split("\n")).encode()
f13b = good(); f13b[orig.SOURCES_PATH] = f13[orig.SOURCES_PATH]
print("%-58s ORIG: %s\n%-58s MUT m03: %s\n" % ("P13 non-new pin S316 registry URL without commit (M03)", run(ORIG, f13), "", run(M + "m03.py", f13b)))
