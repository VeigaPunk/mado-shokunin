#!/usr/bin/env python3
"""Build C1 witness/negative fixtures in scratch (independent of the draft)."""
import os
import shutil
import subprocess

S = "/fast/scratch/hyaku/mado-r65/w1/R65MutCounters"
PROV = S + "/slim/PROVINCE.md"
RCPT = S + "/rcpt/.ufo/waves/round-65/receipts"
OUT = S + "/fx"

GROUPS = [
    "hypr plane", "waybar", "walker", "terminal configs",
    "theme/wallpaper omarchy plane", "idle/lock plane", "omarchy skill docs",
    "windows desktop plane",
]

REC_BEFORE = ".ufo/waves/round-65/receipts/before-register-probes-r65.txt"
REC_GATE = ".ufo/waves/round-65/receipts/gate-live-r65.txt"


def read(name):
    return open(os.path.join(RCPT, name), "rb").read()


def block(groups=GROUPS, gate_receipt=REC_GATE, dangling=False, near_miss=False,
          extra_row=False):
    rows = []
    for g in groups:
        cell = g + "X" if (near_miss and g == "walker") else g
        rec = REC_BEFORE
        if g == "windows desktop plane":
            rec = gate_receipt
        if dangling and g == "omarchy skill docs":
            rec = ".ufo/waves/round-65/receipts/no-such-receipt-r65.txt"
        rows.append("| %s | present (2026-11-03) | probe read-only | %s |" % (cell, rec))
    if extra_row:
        rows.append("| unrelated extra | present (2026-11-03) | probe | %s |" % REC_BEFORE)
    return "\n".join([
        "",
        "### Surface state register (2026-11-03, this host)",
        "",
        "Each row re-derives the 2026-10-31 group on the returned omarchy host.",
        "",
        "| surface group | state (2026-11-03) | probe (read-only) | receipt |",
        "|---|---|---|---|",
    ] + rows + ["", "<!-- r65 register end -->", "", "## Next section", "text", ""])


def build(name, prov_bytes, receipts):
    d = os.path.join(OUT, name)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    open(os.path.join(d, "PROVINCE.md"), "wb").write(prov_bytes)
    if receipts:
        rd = os.path.join(d, ".ufo/waves/round-65/receipts")
        os.makedirs(rd)
        for rname, data in receipts.items():
            open(os.path.join(rd, rname), "wb").write(data)
    subprocess.run(["git", "init", "-q", d], check=True)
    top = subprocess.run(["git", "-C", d, "rev-parse", "--show-toplevel"],
                         check=True, capture_output=True, text=True).stdout.strip()
    assert top == d, (top, d)
    subprocess.run(["git", "-C", d, "add", "-A"], check=True)
    subprocess.run(["git", "-C", d, "-c", "user.email=m@l", "-c", "user.name=m",
                    "commit", "-qm", name], check=True)
    rev = subprocess.run(["git", "-C", d, "rev-parse", "HEAD"], check=True,
                         capture_output=True, text=True).stdout.strip()
    print(name, rev)


def main():
    base = open(PROV, "rb").read()
    os.makedirs(OUT, exist_ok=True)
    good = {"before-register-probes-r65.txt": read("before-register-probes-r65.txt"),
            "gate-live-r65.txt": read("gate-live-r65.txt")}
    dirty = {"before-register-probes-r65.txt": read("before-register-probes-r65.txt"),
             "gate-live-r65.txt": read("gate-live-r65.txt").replace(
                 b"MADO_VERIFY: CLEAN", b"MADO_VERIFY: DIRTY")}
    build("pos", base + block().encode(), good)
    build("neg-droprow", base + block(groups=GROUPS[:7]).encode(), good)
    build("neg-gate-dirty", base + block().encode(), dirty)
    build("neg-dangling", base + block(dangling=True).encode(), good)
    build("neg-nearmiss", base + block(near_miss=True).encode(), good)
    build("neg-dupgroup", base + block(groups=GROUPS[:7] + ["windows desktop plane"]).encode(), good)
    build("pos-extra", base + block(extra_row=True).encode(), good)
    build("neg-base", base, None)


if __name__ == "__main__":
    main()

# ---- round 2: fixtures for specific mutants ------------------------------------------------
def block_sentinel_leak(groups7, gate_receipt=REC_GATE):
    rows = ["| %s | present (2026-11-03) | probe read-only | %s |" % (g, REC_BEFORE) for g in groups7]
    return "\n".join([
        "", "### Surface state register (2026-11-03, this host)", "",
        "| surface group | state (2026-11-03) | probe (read-only) | receipt |",
        "|---|---|---|---|",
    ] + rows + [
        "<!-- r65 register end -->",
        "| windows desktop plane | present (2026-11-03) | probe read-only | %s |" % gate_receipt,
        "",
    ])


def main2():
    base = open(PROV, "rb").read()
    good = {"before-register-probes-r65.txt": read("before-register-probes-r65.txt"),
            "gate-live-r65.txt": read("gate-live-r65.txt")}
    build("neg-8rows-7groups", base + block(groups=GROUPS[:7] + ["waybar"]).encode(), good)
    build("neg-sentinel-leak", base + block_sentinel_leak(GROUPS[:7]).encode(), good)
    # neg-wt-only: committed PROVINCE has no block; the block exists only in the worktree
    name = "neg-wt-only"
    d = os.path.join(OUT, name)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    open(os.path.join(d, "PROVINCE.md"), "wb").write(base)
    rd = os.path.join(d, ".ufo/waves/round-65/receipts")
    os.makedirs(rd)
    for rname, data in good.items():
        open(os.path.join(rd, rname), "wb").write(data)
    subprocess.run(["git", "init", "-q", d], check=True)
    subprocess.run(["git", "-C", d, "add", "-A"], check=True)
    subprocess.run(["git", "-C", d, "-c", "user.email=m@l", "-c", "user.name=m",
                    "commit", "-qm", name], check=True)
    open(os.path.join(d, "PROVINCE.md"), "wb").write(base + block().encode())
    rev = subprocess.run(["git", "-C", d, "rev-parse", "HEAD"], check=True,
                         capture_output=True, text=True).stdout.strip()
    print(name, rev, "(worktree dirty: block present, rev clean)")

def block_gate_on_first(groups, gate_receipt=REC_GATE):
    rows = []
    for i, g in enumerate(groups):
        rec = gate_receipt if i == 0 else REC_BEFORE
        rows.append("| %s | present (2026-11-03) | probe read-only | %s |" % (g, rec))
    return "\n".join([
        "", "### Surface state register (2026-11-03, this host)", "",
        "| surface group | state (2026-11-03) | probe (read-only) | receipt |",
        "|---|---|---|---|",
    ] + rows + ["", "<!-- r65 register end -->", "", "## Next section", "text", ""])


def main3():
    base = open(PROV, "rb").read()
    good = {"before-register-probes-r65.txt": read("before-register-probes-r65.txt"),
            "gate-live-r65.txt": read("gate-live-r65.txt")}
    build("neg-8r7g-gateok", base + block_gate_on_first(GROUPS[:7] + ["waybar"]).encode(), good)
