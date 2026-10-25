#!/usr/bin/env python3
"""CritC1Cheap: build C1 cribs and honest proxies in one /dev/shm sandbox clone, score each
with the lane's frozen C1 counter and with the scratch hardened variant, print cost."""
import hashlib
import os
import shutil
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
BASE = "b4e47e980bfb0cbc8a4e788f59a41db858751fd8"
PKG = "/home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge/event-delivery-limits-r26.md"
FETCH = ".ufo/waves/round-37/fetch"
C1 = os.path.join(LANE, "quality/counters/c1-r37-event-ground.py")
HARD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "c1-hardened.py")
SB = "/dev/shm/mado37-CritC1Cheap/sb"
E1 = "corpus/knowledge/event-delivery-limits-r26.md"
E2 = "corpus/knowledge/event-queue-observability-r37.md"
ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
ENV.update(GIT_AUTHOR_NAME="sandbox", GIT_AUTHOR_EMAIL="sandbox@invalid",
           GIT_COMMITTER_NAME="sandbox", GIT_COMMITTER_EMAIL="sandbox@invalid")
RECEIPT = {"S189": "S189.bin", "S201": "S201.bin", "S212": "S212.bin",
           "S213": "S213.receipt.txt", "S214": "S214.bin"}
QUOTES = {
    "S189": "const size_t MAX_QUEUED_EVENTS = 64;",
    "S201": "std::array<char, 1024> buffer;  // Hyprland socket2 events are max 1024 bytes",
    "S212": 'm_ipc.registerForIPC("workspacev2", this);',
    "S213": 'debug:disable_logs: {"option":"debug:disable_logs","int":1,"set":false}',
    "S214": "m_logsEnabled = !*PDISABLELOGS;",
}


def git(*a):
    return subprocess.run(["git", "-C", SB, *a], env=ENV, capture_output=True, text=True)


def rd(rel):
    return open(os.path.join(SB, rel)).read()


def wr(rel, text):
    p = os.path.join(SB, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w") as f:
        f.write(text)


def sha(rel):
    return hashlib.sha256(open(os.path.join(SB, rel), "rb").read()).hexdigest()


def copy_receipts(ids):
    for i in ids:
        os.makedirs(os.path.join(SB, FETCH), exist_ok=True)
        shutil.copy(os.path.join(LANE, FETCH, RECEIPT[i]), os.path.join(SB, FETCH, RECEIPT[i]))


def add_rows(rows):
    src = rd("corpus/SOURCES.md")
    head, tail = src.split("\n## Paths", 1)
    wr("corpus/SOURCES.md", head.rstrip("\n") + "\n" + "".join(rows) + "\n## Paths" + tail)


def extend_used_by(i, users):
    out = []
    for line in rd("corpus/SOURCES.md").splitlines(keepends=True):
        if line.lstrip().startswith(f"| {i} |"):
            line = line.rstrip("\n").rstrip().rstrip("|").rstrip() + ", " + ", ".join(users) + " |\n"
        out.append(line)
    wr("corpus/SOURCES.md", "".join(out))


def row(i, users, url="https://example.invalid/x"):
    return f"| {i} | {url} | code | A | s | a | t | mined | 2026-10-25 | 90d | {', '.join(users)} |\n"


def gates(lines):
    wr("corpus/lessons/round-37.md", "# r37\n\n## Gate\n\n" + "\n".join(lines) + "\n")


def gate(i, rel, q):
    return f'GATE {i} receipt={rel} sha256={sha(rel)} quote="{q}"'


def index():
    r = rd("corpus/README.md")
    head, tail = r.split("\n## Quality bar", 1)
    add = f"| knowledge/{E1.rsplit('/', 1)[1]} |\n| knowledge/{E2.rsplit('/', 1)[1]} |\n"
    wr("corpus/README.md", head.rstrip("\n") + "\n" + add + "\n## Quality bar" + tail)


HDR = "source: {ids}\nverified-at: x\nrecheck: x\n"


def k0_golden_v2():
    """controls.py c1-golden-v2, rebuilt here for the cost baseline."""
    ids1, ids2 = ["S189", "S201", "S212"], ["S213", "S214"]
    copy_receipts(ids1 + ids2)
    for path, ids, toks in ((E1, ids1, "MAX_QUEUED_EVENTS and overflowed event queue"),
                            (E2, ids2, "debug:disable_logs and m_logsEnabled")):
        ev = "".join(f"**OBS** {i}: `{QUOTES[i]}`\n" for i in ids)
        wr(path, f"# synthetic control entry\n\nsource: {', '.join(ids)}\nverified-at: 2026-10-25\n"
                 f"recheck: 90d\n\nbody naming {toks}.\n{ev}")
    users = {i: [E1] for i in ids1} | {i: [E2] for i in ids2}
    add_rows([row(i, users[i]) for i in sorted(users)])
    gates([gate(i, f"{FETCH}/{RECEIPT[i]}", QUOTES[i]) for i in sorted(users)])
    index()


def k1_real_min():
    """One real receipt per entry, quote = a surface token, duplicate contradicting S189 row."""
    copy_receipts(["S189", "S214"])
    wr(E1, HDR.format(ids="S189") + "MAX_QUEUED_EVENTS overflowed event queue\n**OBS** S189\n")
    wr(E2, HDR.format(ids="S214") + "debug:disable_logs m_logsEnabled\n**OBS** S214\n")
    add_rows([row("S189", [E1], "https://example.invalid/contradicts-the-held-row"), row("S214", [E2])])
    gates([gate("S189", f"{FETCH}/S189.bin", "MAX_QUEUED_EVENTS"),
           gate("S214", f"{FETCH}/S214.bin", "m_logsEnabled")])
    index()


def k2_self_receipt():
    """No source opened: fabricated id, each entry is its own receipt, one-character quote."""
    wr(E1, HDR.format(ids="S999") + "MAX_QUEUED_EVENTS overflowed event queue\n**OBS** S999\n")
    wr(E2, HDR.format(ids="S999") + "debug:disable_logs m_logsEnabled\n**OBS** S999\n")
    add_rows([row("S999", [E1, E2])])
    gates([gate("S999", E1, "e"), gate("S999", E2, "e")])
    index()


def k3_receipt_reading():
    """Real frozen receipts, honest-looking E2 sentence lifted from S213's own 'reading' line."""
    copy_receipts(["S189", "S213", "S214"])
    q213 = ("A zero marker count in either channel therefore cannot distinguish "
            "'never overflowed' from 'not logged'.")
    wr(E1, HDR.format(ids="S189") + f"**OBS** S189 `{QUOTES['S189']}` MAX_QUEUED_EVENTS; "
                                    "overflowed event queue\n")
    wr(E2, HDR.format(ids="S213, S214") + f"**OBS** S213 {q213} debug:disable_logs\n"
                                          f"**OBS** S214 `{QUOTES['S214']}`\n")
    add_rows([row("S213", [E2]), row("S214", [E2])])
    extend_used_by("S189", [E1])
    gates([gate("S189", f"{FETCH}/S189.bin", QUOTES["S189"]),
           gate("S213", f"{FETCH}/S213.receipt.txt", q213),
           gate("S214", f"{FETCH}/S214.bin", QUOTES["S214"])])
    index()


def renumber(text):
    for old, new in (("S214", "S212"), ("S187", "S189"), ("S188", "S201")):
        text = text.replace(old, new)
    return text


def h_rows_gates():
    add_rows([row("S212", [E1]), row("S213", [E2]), row("S214", [E2])])
    extend_used_by("S189", [E1])
    extend_used_by("S201", [E1])
    gates([gate(i, f"{FETCH}/{RECEIPT[i]}", QUOTES[i]) for i in sorted(RECEIPT)])
    index()


def e1_honest_text():
    t = renumber(open(PKG).read())
    t = t.replace("source: S212 — https://raw.githubusercontent.com/Alexays/Waybar/0.15.0/src/modules/hyprland/workspaces.cpp",
                  "source: S189, S201, S212 — EventManager.cpp (v0.56.2), Waybar backend.cpp and workspaces.cpp (0.15.0)")
    return t


E2_HONEST = """# Event-queue overflow on this host: what the logs can and cannot show

source: S213 (host log channels, own work), S214 (Hyprland v0.56.2 `src/debug/log/Logger.cpp`)
verified-at: 2026-10-25
recheck: 30d — re-run the S213 receipt and `hyprctl getoption debug:disable_logs -j`

### §1 The logger gate

**OBS** S214: the core logger caches `debug:disable_logs` and inverts it:

> `m_logsEnabled = !*PDISABLELOGS;`

**OBS** S214: every core `log()` call starts with `if (!m_logsEnabled)` and returns, so no
line is written while the option is 1.

### §2 This host

**OBS** S213: the live option reads

> `debug:disable_logs: {"option":"debug:disable_logs","int":1,"set":false}`

**OBS** S213: the session log holds 21 core-logger lines, all before line 22; zero
`overflowed event queue` and zero `failed writing event` in log and unit journal.

### §3 Consequence

**INF** The two socket2 markers are core-logger lines, so a zero marker count on this host
cannot separate "never overflowed" from "not logged" (S213, S214).

**UNK** Whether any client was ever removed. Flip: re-measure on a host with
`debug:disable_logs = 0`.
"""


def h1_pkg_renumbered():
    """Honest-proxy failure mode: package entry with mechanical id renumbering only."""
    copy_receipts(list(RECEIPT))
    wr(E1, e1_honest_text())
    wr(E2, E2_HONEST)
    h_rows_gates()


def h2_honest():
    """Honest proxy: package entry re-grounded (ids renumbered, located quotes stated with
    OBS lines naming each id), plus a lane-authored E2."""
    copy_receipts(list(RECEIPT))
    t = e1_honest_text().rstrip().rstrip("-").rstrip()
    t += ("\n\n### §3 Re-grounding (round 37)\n\n"
          f"**OBS** S189 `EventManager.cpp:169`: `{QUOTES['S189']}`\n\n"
          f"**OBS** S201 `backend.cpp`: `{QUOTES['S201']}`\n\n"
          f"**OBS** S212 `workspaces.cpp`: `{QUOTES['S212']}`\n")
    wr(E1, t)
    wr(E2, E2_HONEST)
    h_rows_gates()


def h3_honest_trimmed():
    """Honest proxy, E1 trimmed: preamble and merge note dropped, sections rewrapped."""
    h2_honest()
    t = rd(E1)
    t = t.split("_Merge note", 1)[0] + "### §1" + t.split("### §1", 1)[1]
    t = t.replace("Lane: mado-shokunin. Round: corpus-expansion-2, round 2. Substrates READ-ONLY:\n"
                  "source files were read; no socket was connected and no event was observed.\n", "")
    wr(E1, " ".join(t.split(" ")))


def k5_pkg_plus_e2_stub():
    """Residual: honest-proxy E1 (package re-grounded) plus a two-OBS-line stated-quote E2 stub."""
    h2_honest()
    wr(E2, HDR.format(ids="S213, S214") + f"debug:disable_logs\n**OBS** S213 `{QUOTES['S213']}`\n"
                                          f"**OBS** S214 `{QUOTES['S214']}`\n")


CASES = [k0_golden_v2, k1_real_min, k2_self_receipt, k3_receipt_reading, h1_pkg_renumbered, h2_honest, h3_honest_trimmed, k5_pkg_plus_e2_stub]


def cost():
    d = git("diff", "--numstat", BASE, "HEAD").stdout.split("\n")
    added_text = added_bin = 0
    files = 0
    for line in filter(None, d):
        a, _, f = line.split("\t")
        files += 1
        if f.startswith(FETCH):
            added_bin += os.path.getsize(os.path.join(SB, f))
            continue
        added_text += int(a) if a != "-" else 0
    raw = git("diff", "-U0", BASE, "HEAD", "--", "corpus").stdout
    add_bytes = sum(len(l) for l in raw.splitlines() if l.startswith("+") and not l.startswith("+++"))
    return f"files={files} corpus_added_lines={added_text} corpus_added_bytes={add_bytes} copied_receipt_bytes={added_bin}"


def main():
    if not os.path.isdir(SB):
        subprocess.run(["git", "clone", "-q", "--no-local", "--no-checkout", LANE, SB], env=ENV, check=True)
        git("sparse-checkout", "set", "--no-cone", "/corpus/", f"/{FETCH}/")
    for case in CASES:
        git("checkout", "-q", "-f", "--detach", BASE)
        git("clean", "-fdqx")
        case()
        git("add", "-A")
        git("commit", "-q", "--allow-empty", "-m", case.__name__)
        head = git("rev-parse", "HEAD").stdout.strip()
        print(f"== {case.__name__} rev={head} {cost()}")
        print(f"   doc: {case.__doc__.split(chr(10))[0]}")
        for name, ctr, cl in (("frozen", C1, ""), ("hard-pqu", HARD, "pqu"), ("hard-pqul", HARD, "pqul")):
            p = subprocess.run([sys.executable, "-I", ctr, "--repo", SB, "--rev", head, "--base", BASE],
                               capture_output=True, text=True, env=dict(ENV, C1H_CLAUSES=cl))
            for l in p.stdout.strip().splitlines():
                print(f"   [{name} rc={p.returncode}] {l.replace('PRED-C1-r37-', '').replace('corpus/knowledge/', '')}")
            if p.stderr.strip():
                print(f"   [{name} stderr] {p.stderr.strip()[-300:]}")


if __name__ == "__main__":
    sys.dont_write_bytecode = True
    main()
