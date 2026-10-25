#!/usr/bin/env python3
"""Edge probe: crafted journals where the contract's parser rules are subtle.

Each case is compared against the frozen judge's model_out. A disagreement is a
finding about either my reading or the model, decided by a sentence of the
PRED-C1-r41-v1 contract text.
"""
import importlib.util
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


judge = load("c1judge", LANE + "/quality/counters/c1-r41-globals.py")
mine = load("minetool", LANE + "/.ufo/waves/round-41/w1/ExecToolIndep/mado-globals.py")

H = "xdg-desktop-portal-hyprland"
TS = "2026-10-25T13:36:24-03:00"


def a(ts, pid, name, ver, host="hst", gap="  ", tail="", head=""):
    return "%s%s %s %s[%s]: [LOG]%s| Got interface: %s (ver %s)%s" % (
        head, ts, host, H, pid, gap, name, ver, tail)


CASES = [
    ("plain", [a(TS, "9", "wl_seat", "9")]),
    ("leading-zero pid", [a(TS, "007", "wl_seat", "9")]),
    ("leading-zero ver", [a(TS, "9", "wl_seat", "000009")]),
    ("six-digit ver", [a(TS, "9", "wl_seat", "999999")]),
    ("seven-digit ver", [a(TS, "9", "wl_seat", "1000000")]),
    ("name 128", [a(TS, "9", "n" * 128, "1")]),
    ("name 129", [a(TS, "9", "n" * 129, "1")]),
    ("name with dash", [a(TS, "9", "focus-grab", "1")]),
    ("one space gap", [a(TS, "9", "wl_seat", "9", gap=" ")]),
    ("three space gap", [a(TS, "9", "wl_seat", "9", gap="   ")]),
    ("tab gap", [a(TS, "9", "wl_seat", "9", gap="\t")]),
    ("trailing space", [a(TS, "9", "wl_seat", "9", tail=" ")]),
    ("trailing cr", [a(TS, "9", "wl_seat", "9", tail="\r")]),
    ("leading space", [a(TS, "9", "wl_seat", "9", head=" ")]),
    ("ts no tz", [a("2026-10-25T13:36:24", "9", "wl_seat", "9")]),
    ("ts zulu", [a("2026-10-25T13:36:24Z", "9", "wl_seat", "9")]),
    ("ts month 13", [a("2026-13-45T99:99:99+00:00", "9", "wl_seat", "9")]),
    ("ts one-digit month", [a("2026-1-25T13:36:24-03:00", "9", "wl_seat", "9")]),
    ("ts offset no colon", [a("2026-10-25T13:36:24-0300", "9", "wl_seat", "9")]),
    ("ts short offset", [a("2026-10-25T13:36:24-03", "9", "wl_seat", "9")]),
    ("host with colon", [a(TS, "9", "wl_seat", "9", host="h:1")]),
    ("host with bracket", [a(TS, "9", "wl_seat", "9", host="h]1[")]),
    ("other program", [a(TS, "9", "wl_seat", "9").replace(H, "other-portal")]),
    ("other level", [a(TS, "9", "wl_seat", "9").replace("[LOG]", "[WARN]")]),
    ("no level", [a(TS, "9", "wl_seat", "9").replace("[LOG]", "")]),
    ("boot 32", ["-- Boot " + "a" * 32 + " --", a(TS, "9", "wl_seat", "9")]),
    ("boot upper hex", ["-- Boot " + "A" * 32 + " --", a(TS, "9", "wl_seat", "9")]),
    ("boot 31", ["-- Boot " + "a" * 31 + " --", a(TS, "9", "wl_seat", "9")]),
    ("boot 33", ["-- Boot " + "a" * 33 + " --", a(TS, "9", "wl_seat", "9")]),
    ("boot trailing space", ["-- Boot " + "a" * 32 + " -- ", a(TS, "9", "wl_seat", "9")]),
    ("boot lowercase text", ["-- boot " + "a" * 32 + " --", a(TS, "9", "wl_seat", "9")]),
    ("two boots then advert", ["-- Boot " + "a" * 32 + " --",
                               "-- Boot " + "b" * 32 + " --",
                               a(TS, "9", "wl_seat", "9")]),
    ("boot between same pid", [a(TS, "9", "wl_seat", "9"),
                               "-- Boot " + "a" * 32 + " --",
                               a("2026-10-25T13:36:25-03:00", "9", "wl_shm", "1")]),
    ("boot then two adverts", [a(TS, "9", "wl_seat", "9"),
                               "-- Boot " + "a" * 32 + " --",
                               a("2026-10-25T13:36:25-03:00", "9", "wl_shm", "1"),
                               a("2026-10-25T13:36:26-03:00", "9", "wl_output", "1")]),
    ("boot only", ["-- Boot " + "a" * 32 + " --"]),
    ("empty", [""]),
    ("blank lines", ["", "", a(TS, "9", "wl_seat", "9"), ""]),
    ("pid alternation", [a(TS, "1", "wl_seat", "9"),
                         a("2026-10-25T13:36:25-03:00", "2", "wl_seat", "9"),
                         a("2026-10-25T13:36:26-03:00", "1", "wl_seat", "9")]),
    ("ver drops", [a(TS, "9", "wl_seat", "9"),
                   a("2026-10-25T13:36:25-03:00", "9", "wl_seat", "3")]),
    ("ver equal twice", [a(TS, "9", "wl_seat", "9"),
                         a("2026-10-25T13:36:25-03:00", "9", "wl_seat", "9")]),
    ("many names", [a(TS, "9", n, "1") for n in sorted(judge.TABLE) + ["zzz"]]),
    ("two sessions diff", [a(TS, "9", "wl_seat", "9"),
                           a("2026-10-25T13:36:25-03:00", "8", "wl_shm", "1")]),
]

EXPECTS = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [],
           [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [],
           [], [], [], [], [], [], [], [], [], [], ["wl_seat", "zzz"],
           ["nope"]]


def main():
    bad = 0
    for index, (label, lines) in enumerate(CASES):
        text = "\n".join(lines) + "\n"
        for diff in (False, True):
            for expects in (EXPECTS[index], []):
                got = mine.render_report(
                    mine.parse_sessions(mine.split_lines(text.encode())),
                    list(expects), diff)
                want = judge.model_out(text, list(expects), diff)
                if got != want:
                    bad += 1
                    print("DISAGREE %r diff=%s expects=%r\n got=%r\n want=%r"
                          % (label, diff, expects, got, want))
    print("EDGE PROBE: cases=%d comparisons=%d disagreements=%d"
          % (len(CASES), len(CASES) * 4, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
