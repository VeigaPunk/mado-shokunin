#!/usr/bin/env python3
"""R55W2CritC1Forge: build falsification variants of the C1 entry in scratch repos and score them with the
REAL counter (quality/counters/c1-r55-kbd-entry.py, unchanged) and the REAL harness (check-r55-controls.py --claim c1).
Lane is read only (git archive / git cat-file via the counter). Every variant is a fresh copy of a scratch repo."""
import hashlib, os, re, shutil, subprocess, sys, json

S = "/fast/scratch/hyaku/mado-r55/R55W2CritC1Forge"
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
REV = "57584ed67716340b3d466fa04333ac0bab3fb79e"
RECEIPTS = os.path.join(LANE, ".ufo/waves/round-55/w2/R55W2CritC1Forge/receipts")
ENTRY = "corpus/knowledge/hyprland-keyboard-repeat-numlock-r55.md"
COUNTER = "quality/counters/c1-r55-kbd-entry.py"
HARNESS = "quality/check-r55-controls.py"
ENV = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": S + "/home", "TMPDIR": S,
       "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_NOSYSTEM": "1", "LC_ALL": "C"}
os.makedirs(S + "/home", exist_ok=True)
os.makedirs(RECEIPTS, exist_ok=True)


def git(d, *a):
    r = subprocess.run(["git", "-C", d] + list(a), capture_output=True, env=ENV)
    if r.returncode != 0:
        raise SystemExit("git %s failed: %s" % (a, r.stderr.decode()))
    return r.stdout.decode().strip()


# ---- base scratch repo: archive of the scored revision (read-only export from the lane)
D0 = os.path.join(S, "base")
if os.path.exists(D0):
    shutil.rmtree(D0)
os.makedirs(D0)
subprocess.run(["git", "init", "-q", D0], check=True, env=ENV)
assert os.path.realpath(git(D0, "rev-parse", "--show-toplevel")) == os.path.realpath(D0)
arc = subprocess.run(["git", "-C", LANE, "archive", "--format=tar", REV], capture_output=True, env=ENV, check=True).stdout
subprocess.run(["tar", "-x", "-C", D0], input=arc, check=True)
git(D0, "add", "-A")
git(D0, "-c", "user.name=ctl", "-c", "user.email=ctl@ctl", "commit", "-q", "-m", "base = lane %s" % REV[:12])
BASE_SHA = git(D0, "rev-parse", "HEAD")

entry_orig = open(os.path.join(D0, ENTRY), encoding="utf-8").read()

ROW = re.compile(r"^\| ([KH][0-9]{2}) \| (.*?) \| (.*?) \| (.*?) \| `(.*)` \|$")


def rewrite_rows(text, fn):
    out = []
    for ln in text.split("\n"):
        m = ROW.match(ln)
        if m:
            rid, prop, src, anchor, quote = m.groups()
            prop, src = fn(rid, prop, src)
            ln = "| %s | %s | %s | %s | `%s` |" % (rid, prop, src, anchor, quote)
        out.append(ln)
    return "\n".join(out)


def variant(name, transform):
    Dv = os.path.join(S, "v-" + name)
    if os.path.exists(Dv):
        shutil.rmtree(Dv)
    subprocess.run(["git", "clone", "-q", "--no-hardlinks", D0, Dv], check=True, env=ENV)
    assert os.path.realpath(git(Dv, "rev-parse", "--show-toplevel")) == os.path.realpath(Dv)
    files = transform()
    for path, data in files.items():
        full = os.path.join(Dv, path)
        if data is None:
            os.remove(full)
        else:
            open(full, "w", encoding="utf-8").write(data)
    git(Dv, "add", "-A")
    git(Dv, "-c", "user.name=ctl", "-c", "user.email=ctl@ctl", "commit", "-q", "--allow-empty", "-m", "variant " + name)
    sha = git(Dv, "rev-parse", "HEAD")
    return Dv, sha


def run(cmd, work):
    os.makedirs(work, exist_ok=True)
    r = subprocess.run([sys.executable, "-I"] + cmd + ["--work", work], capture_output=True, env=ENV, timeout=900)
    return r.returncode, r.stdout.decode(), r.stderr.decode()


def score(name, transform):
    Dv, sha = variant(name, transform)
    work = os.path.join(S, "work-" + name)
    rc1, out1, err1 = run([os.path.join(Dv, COUNTER), "--repo", Dv, "--rev", sha], work)
    # the harness path: counter run from the tree at sha
    rc2, out2, err2 = run([os.path.join(Dv, HARNESS), "--claim", "c1", "--repo", Dv, "--rev", sha], work)
    rec = os.path.join(RECEIPTS, name)
    os.makedirs(rec, exist_ok=True)
    with open(os.path.join(rec, "counter.out"), "w") as f:
        f.write("rc=%d\n%s" % (rc1, out1))
    with open(os.path.join(rec, "counter.err"), "w") as f:
        f.write(err1)
    with open(os.path.join(rec, "harness.out"), "w") as f:
        f.write("rc=%d\n%s" % (rc2, out2))
    with open(os.path.join(rec, "harness.err"), "w") as f:
        f.write(err2)
    print("== %s  rev=%s" % (name, sha[:12]))
    print(out1.strip())
    print("harness rc=%d: %s" % (rc2, out2.strip()))
    shutil.rmtree(work, ignore_errors=True)
    return out1.strip(), out2.strip()


# ---- proposition sets
PLACEHOLDER_K = "placeholder proposition text for row %s, not a claim about any source line"
PLACEHOLDER_H = "placeholder host proposition %s, not a read"

FALSE_K = {
    "K01": "applyConfigToKeyboard never reads repeat_rate; it hard-codes 25 and ignores every config key.",
    "K02": "applyConfigToKeyboard never reads repeat_delay; it hard-codes 600 for every keyboard.",
    "K03": "applyConfigToKeyboard reads numlock through getDeviceInt with no global fallback at all.",
    "K04": "The stored repeat rate m_repeatRate is capped at 200 by std::max(0, REPEATRATE) on this line.",
    "K05": "The stored repeat delay m_repeatDelay is capped at 2000 by std::max(0, REPEATDELAY) on this line.",
    "K06": "The stored numlock state is floored at zero by this line and is never negative.",
    "K07": "The early return compares std::max-clamped config values with stored fields, never raw config names.",
    "K08": "IKeyboard::setKeymap never reads numlock_by_default; numlock is always set to off.",
    "K09": "The NumLock lock block runs when NUMLOCKON equals 0 and is skipped when it equals 1, via an else arm.",
    "K10": "updateActiveKeyboardData sends every keyboard's rate and delay to the seat, and has no guard at all.",
    "K11": "The guard tests whether the resource version is above 4, so version 4 clients never get repeat_info.",
    "K12": "repeatInfo never calls sendRepeatInfo; it only stores the values and returns.",
    "K13": "The config table declares input:repeat_rate with default 2500 and a maximum of 20.",
    "K14": "The config table declares input:repeat_delay with default 60 and a maximum of 200.",
    "K15": "The config table declares input:numlock_by_default as an integer option with default 9.",
    "K16": "getConfigValueSafeDevice always returns the device value and never the global fallback.",
    "K17": "The 1.26.0 wl_keyboard repeat_info text says a rate of zero leaves repeating unchanged, any delay.",
    "K18": "IKeyboard initialises m_repeatRate to 40, so the declared default is forty repeats per second.",
}
FALSE_H = {
    "H01": "The committed host input.conf sets repeat_rate to 4, not 40, on line 14.",
    "H02": "The committed host input.conf sets repeat_delay to 25, not 250, on line 15.",
    "H03": "The committed host input.conf sets numlock_by_default to false on line 18.",
    "H04": "The live hyprctl getoption read returned 4 for input:repeat_rate, not 40.",
    "H05": "The live hyprctl getoption read returned 25 for input:repeat_delay, not 250.",
    "H06": "The live hyprctl getoption read returned 0 for input:numlock_by_default, not 1.",
}
for d in (FALSE_K, FALSE_H):
    for k, v in d.items():
        assert len(v) >= (40 if k[0] == "K" else 20), (k, len(v))


def junk_entry():
    """Minimal entry: provenance trio + the 18 K and 6 H rows, frozen quotes and anchors, placeholder propositions."""
    head = ["source: S316, S317, S318, S319, S052, S378, S379, S380",
            "verified-at: 2026-10-28", "recheck: on-release", "",
            "# Keyboard repeat (placeholder entry)", "",
            "| id | proposition | source | pin:line | quote |", "|---|---|---|---|---|"]
    body = []
    for ln in entry_orig.split("\n"):
        m = ROW.match(ln)
        if m and m.group(1)[0] == "K":
            body.append((m.group(1), m.group(2), m.group(3), m.group(4), m.group(5)))
    rows_k, rows_h = [], []
    for ln in entry_orig.split("\n"):
        m = ROW.match(ln)
        if not m:
            continue
        rid, prop, src, anchor, quote = m.groups()
        if rid[0] == "K":
            rows_k.append("| %s | %s | %s | %s | `%s` |" % (rid, PLACEHOLDER_K % rid, src, anchor, quote))
        else:
            rows_h.append("| %s | %s | host | %s | `%s` |" % (rid, PLACEHOLDER_H % rid, anchor, quote))
    text = "\n".join(head + rows_k + ["", "| id | proposition | source | pin:line | quote |", "|---|---|---|---|---|"] + rows_h) + "\n"
    return text


def t_base():
    return {}


def t_junk():
    return {ENTRY: junk_entry()}


def t_false_k04():
    return {ENTRY: rewrite_rows(entry_orig, lambda rid, p, s: (
        "The stored repeat rate m_repeatRate is capped at 200 by std::max(0, REPEATRATE) on this line." if rid == "K04" else p, s))}


def t_false_all():
    def fn(rid, p, s):
        if rid in FALSE_K:
            return FALSE_K[rid], s
        if rid in FALSE_H:
            return FALSE_H[rid], s
        return p, s
    return {ENTRY: rewrite_rows(entry_orig, fn)}


def t_swap_family():
    # same file family, wrong registry row: K13-K15 cite S215 (ConfigValues.cpp, log-switch row) instead of S318;
    # K16 cites S162 (ConfigManager.cpp windowrule row) instead of S317.
    def fn(rid, p, s):
        if rid in ("K13", "K14", "K15"):
            return p, "S215"
        if rid == "K16":
            return p, "S162"
        return p, s
    return {ENTRY: rewrite_rows(entry_orig, fn)}


def t_prov_forge():
    # provenance line names a registry id that does not exist; rows and quotes untouched
    return {ENTRY: entry_orig.replace("source: S316, S317", "source: S999, S317", 1)}


def t_entry_absent():
    return {ENTRY: None}


VARIANTS = [
    ("control-base", t_base),
    ("control-entry-absent", t_entry_absent),
    ("J1-junk-placeholder", t_junk),
    ("B1-false-K04-cap200", t_false_k04),
    ("B2-false-all-rows", t_false_all),
    ("C1-same-family-swap", t_swap_family),
    ("P1-provenance-forged-S999", t_prov_forge),
]

if __name__ == "__main__":
    only = sys.argv[1:]
    results = {}
    for name, fn in VARIANTS:
        if only and name not in only:
            continue
        results[name] = score(name, fn)
    with open(os.path.join(RECEIPTS, "summary.json"), "w") as f:
        json.dump({k: {"counter": v[0], "harness": v[1]} for k, v in results.items()}, f, indent=1)
    print("BASE", BASE_SHA)
