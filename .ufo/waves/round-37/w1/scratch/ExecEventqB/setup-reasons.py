#!/usr/bin/env python3
"""Scratch harness: drive every SETUP reason and edge path of candidate B from files and env only."""
import os
import subprocess
import sys

TOOL, WORK = sys.argv[1], sys.argv[2]
os.makedirs(WORK, exist_ok=True)
S2 = "/run/user/1000/hypr/HIS/.socket2.sock"
HDR = "Netid State  Recv-Q Send-Q Local Address:Port  Peer Address:Port Process\n"
LISTEN = f'u_str LISTEN 0 10 {S2} 1001 * 0 users:(("Hyprland",pid=1619,fd=33))\n'
SRV = f'u_str ESTAB 0 4352 {S2} 2001 * 3001 users:(("Hyprland",pid=1619,fd=250))\n'
CLI = 'u_str ESTAB 2048 0 * 3001 * 2001 users:(("Web Content",pid=9,fd=7))\n'
ORPHAN = f'u_str ESTAB 0 0 {S2} 2002 * 3999 users:(("Hyprland",pid=1619,fd=251))\n'
NOUSER = f'u_str ESTAB 0 0 {S2} 2003 * 3003 users:(("Hyprland",pid=1619,fd=252))\n' \
    'u_str ESTAB 5 0 * 3003 * 2003\n'
LISTEN_B = LISTEN.replace("/HIS/", "/HIS2/").replace(" 1001 ", " 1009 ")


def put(name, text):
    p = os.path.join(WORK, name)
    with open(p, "w") as f:
        f.write(text)
    return p


ok_ss = put("ok.ss", HDR + LISTEN + SRV + CLI + ORPHAN + NOUSER)
two_ss = put("two.ss", HDR + LISTEN + LISTEN_B)
bad_ss = put("bad.ss", "garbage\n")
nolisten_ss = put("nolisten.ss", HDR + SRV + CLI)
log = put("h.log", "")
jr = put("j.txt", "")
rt_empty = os.path.join(WORK, "rt-empty")
os.makedirs(os.path.join(rt_empty, "hypr"), exist_ok=True)
rt_two = os.path.join(WORK, "rt-two")
for d in ("a", "b"):
    os.makedirs(os.path.join(rt_two, "hypr", d), exist_ok=True)
emptybin = os.path.join(WORK, "emptybin")
os.makedirs(emptybin, exist_ok=True)
base_env = {k: v for k, v in os.environ.items()}
F = ["--log", log, "--journal-file", jr, "--disable-logs", "0"]


def env(**kw):
    e = dict(base_env)
    for k, v in kw.items():
        if v is None:
            e.pop(k, None)
        else:
            e[k] = v
    return e


CASES = [
    ("usage", ["--disable-logs", "2"], {}, "SETUP usage"),
    ("ss_file_unreadable", ["--ss-file", os.path.join(WORK, "nope"), *F], {}, "SETUP ss_file_unreadable"),
    ("ss_unavailable", F, dict(PATH=emptybin), "SETUP ss_unavailable"),
    ("ss_unparseable", ["--ss-file", bad_ss, *F], {}, "SETUP ss_unparseable"),
    ("socket2_not_listening", ["--ss-file", nolisten_ss, *F], {}, "SETUP socket2_not_listening"),
    ("socket2_not_listening(--socket2)", ["--ss-file", ok_ss, "--socket2", "/x/.socket2.sock", *F], {},
     "SETUP socket2_not_listening"),
    ("socket2_ambiguous", ["--ss-file", two_ss, *F], {}, "SETUP socket2_ambiguous"),
    ("no_runtime_dir", ["--ss-file", ok_ss, "--journal-file", jr, "--disable-logs", "0"],
     dict(XDG_RUNTIME_DIR=None), "SETUP no_runtime_dir"),
    ("instance_missing", ["--ss-file", ok_ss, "--journal-file", jr, "--disable-logs", "0"],
     dict(XDG_RUNTIME_DIR=rt_empty, HYPRLAND_INSTANCE_SIGNATURE="bogus"), "SETUP instance_missing"),
    ("no_instance", ["--ss-file", ok_ss, "--journal-file", jr, "--disable-logs", "0"],
     dict(XDG_RUNTIME_DIR=rt_empty, HYPRLAND_INSTANCE_SIGNATURE=None), "SETUP no_instance"),
    ("instance_ambiguous", ["--ss-file", ok_ss, "--journal-file", jr, "--disable-logs", "0"],
     dict(XDG_RUNTIME_DIR=rt_two, HYPRLAND_INSTANCE_SIGNATURE=None), "SETUP instance_ambiguous"),
    ("log_unreadable", ["--ss-file", ok_ss, "--log", os.path.join(WORK, "nope.log"), "--journal-file", jr,
                        "--disable-logs", "0"], {}, "SETUP log_unreadable"),
    ("journal_file_unreadable", ["--ss-file", ok_ss, "--log", log, "--journal-file",
                                 os.path.join(WORK, "nope.j"), "--disable-logs", "0"], {},
     "SETUP journal_file_unreadable"),
    ("journal_unavailable", ["--ss-file", ok_ss, "--log", log, "--disable-logs", "0"], dict(PATH=emptybin),
     "SETUP journal_unavailable"),
    ("snapshot_unwritable", ["--ss-file", ok_ss, *F, "--snapshot-out", os.path.join(WORK, "no/dir/s.txt")], {},
     "SETUP snapshot_unwritable"),
    ("observable_unknown", ["--ss-file", ok_ss, "--log", log, "--journal-file", jr], dict(PATH=emptybin),
     "markers_observable=unknown verdict=CLEAN"),
    ("edges", ["--ss-file", ok_ss, *F], {}, "subscribers=3 overflow=0 write_fail=0 lagging=2"),
]

fails = 0
for name, args, e, want in CASES:
    p = subprocess.run([sys.executable, "-I", TOOL, *args], capture_output=True, text=True, env=env(**e))
    lines = p.stdout.splitlines()
    want_rc = 0 if name in ("observable_unknown", "edges") else 2
    good = p.returncode == want_rc and any(want in l for l in lines) and \
        (want_rc == 0 or (len(lines) == 1 and "verdict=" not in p.stdout))
    fails += not good
    print(f"case={name} rc={p.returncode} ok={int(good)} :: {lines[-1] if lines else '<no stdout>'}")
    if name == "edges":
        for l in lines[:3]:
            print("   ", l)
print(f"setup_harness fails={fails}/{len(CASES)}")
sys.exit(1 if fails else 0)
