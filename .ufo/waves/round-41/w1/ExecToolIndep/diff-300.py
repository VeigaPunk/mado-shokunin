#!/usr/bin/env python3
"""Differential: my mado-globals.py vs the frozen judge's model_out, 300 random journals.

The judge module is imported (importlib) and used as a black box: its generator
helpers build the journals, its model_out is the oracle. Nothing is written to
the lane.
"""
import importlib.util
import random
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
COUNTER = LANE + "/quality/counters/c1-r41-globals.py"
MINE = LANE + "/.ufo/waves/round-41/w1/ExecToolIndep/mado-globals.py"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


judge = load("c1judge", COUNTER)
mine = load("minetool", MINE)

NAMES = sorted(judge.TABLE) + ["wl_seat", "wl_compositor", "wl_shm", "wl_output",
                               "xdg_wm_base", "wp_viewporter", "zzz_unknown_v9"]
NOISE_TAIL = ["", " trailing", "\r", " ", "\t"]


def adv(ts, pid, name, ver, host="hst"):
    return ("%s %s xdg-desktop-portal-hyprland[%s]: [LOG]  | Got interface: "
            "%s (ver %d)" % (ts, host, pid, name, ver))


def ts(rng):
    return "2026-10-%02dT%02d:%02d:%02d%s%02d:%02d" % (
        rng.randrange(1, 29), rng.randrange(24), rng.randrange(60),
        rng.randrange(60), rng.choice(["+", "-"]), rng.randrange(24),
        rng.randrange(60))


def gen(rng, mode):
    lines = []
    pid = str(rng.randrange(1, 5000))
    ver = {}
    if mode == "empty":
        return b""
    if mode == "noise":
        for _ in range(rng.randrange(1, 40)):
            lines.append(rng.choice([
                "systemd[1]: Started xdg-desktop-portal-hyprland.service.",
                "[LOG]  | Got interface: wl_seat (ver 9)",
                "2026-10-25 13:36:24 hst xdg-desktop-portal-hyprland[9]: [LOG]  | Got interface: wl_seat (ver 9)",
                adv(ts(rng), "9", "wl_seat", 1234567),
                adv(ts(rng), "9", "a" * 129, 1),
                adv(ts(rng), "9", "wl_seat", 9) + rng.choice(NOISE_TAIL),
                "x" * rng.randrange(1, 60),
            ]))
        return ("\n".join(lines) + "\n").encode()
    for _ in range(rng.randrange(1, 60)):
        roll = rng.random()
        if roll < 0.12:
            lines.append("-- Boot %s --" % ("".join(rng.choice("0123456789abcdef")
                                                    for _ in range(32))))
        elif roll < 0.30:
            pid = str(rng.randrange(1, 5000))
            lines.append(adv(ts(rng), pid, rng.choice(NAMES), rng.randrange(1, 20)))
        elif roll < 0.42:
            lines.append(rng.choice([
                "2026-10-25 13:36:24 hst xdg-desktop-portal-hyprland[9]: [LOG]  | Got interface: wl_seat (ver 9)",
                adv(ts(rng), pid, rng.choice(NAMES), rng.randrange(1, 20)).replace(
                    "[LOG]  |", "[LOG] |"),
                adv(ts(rng), pid, rng.choice(NAMES), rng.randrange(1, 20)) + "\r",
                adv(ts(rng), pid, rng.choice(NAMES), rng.randrange(1, 20)) + " x",
                "2026-13-25T13:36:24-03:00 hst xdg-desktop-portal-hyprland[9]: [LOG]  | Got interface: wl_seat (ver 9)",
                "2026-10-25T13:36:24 hst xdg-desktop-portal-hyprland[9]: [LOG]  | Got interface: wl_seat (ver 9)",
                adv(ts(rng), pid, rng.choice(NAMES), rng.randrange(1, 20),
                    host="a b"),
                "",
            ]))
        else:
            name = rng.choice(NAMES)
            lines.append(adv(ts(rng), pid, name, rng.randrange(1, 20)))
    text = "\n".join(lines)
    if rng.random() < 0.5:
        text += "\n"
    data = text.encode()
    if rng.random() < 0.15:
        blob = bytearray(data)
        at = rng.randrange(len(blob) + 1)
        blob[at:at] = b"\xff\xfe"
        data = bytes(blob)
    return data


def run_mine(data, expects, diff):
    if not isinstance(data, bytes):
        data = data.encode()
    return mine.render_report(mine.parse_sessions(mine.split_lines(data)),
                              list(expects), diff)


def run_judge(data, expects, diff):
    """model_out takes text (it splits on a str newline); non-UTF-8 bytes are
    handed to it decoded with replacement, and those cases are bucketed."""
    if isinstance(data, bytes):
        try:
            data.decode()
        except UnicodeDecodeError:
            return None
        data = data.decode()
    return judge.model_out(data, list(expects), diff)


def main():
    rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 20261025)
    modes = ["plain"] * 6 + ["noise", "empty"]
    pool = [n for n in NAMES if n in judge.TABLE] + ["wl_seat", "zzz_unknown_v9"]
    bad = 0
    cases = 0
    skipped = 0
    # part 1: the judge's own lattice, many nonces
    for step in range(100):
        nonce = "%032x" % rng.getrandbits(128)
        i = step % 8
        text, expects, diff = judge.gen_fixture("60c3914154333180450d5da27ba222d5763cc56a",
                                                nonce, i)
        cases += 1
        got = run_mine(text, expects, diff)
        want = run_judge(text, expects, diff)
        if want is None:
            skipped += 1
            continue
        if got != want:
            bad += 1
            print("DISAGREE lattice i=%d nonce=%s\n got=%r\n want=%r"
                  % (i, nonce, got, want))
    # part 2: 200 random journals
    for step in range(200):
        mode = modes[step % len(modes)]
        data = gen(rng, mode)
        expects = []
        for _ in range(rng.randrange(0, 4)):
            expects.append(rng.choice(pool))
        diff = rng.random() < 0.5
        cases += 1
        got = run_mine(data, expects, diff)
        want = run_judge(data, expects, diff)
        if want is None:
            skipped += 1
            continue
        if got != want:
            bad += 1
            print("DISAGREE mode=%s expects=%r diff=%s\n journal=%r\n got=%r\n want=%r"
                  % (mode, expects, diff, data[:400], got, want))
    print("DIFFERENTIAL: journals=%d judged=%d skipped_nonutf8=%d disagreements=%d"
          % (cases, cases - skipped, skipped, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
