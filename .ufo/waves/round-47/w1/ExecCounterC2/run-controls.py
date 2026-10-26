#!/usr/bin/env python3
"""Run PRED-C2-r47 against the positive control and its negative controls.

Every mutation is a commit in the scratch clone $S/ctl (POS tree + one defect); the
clone's toplevel is asserted before the first commit. Outputs go to the seat receipts
dir and are not edited afterwards.
"""
import os
import re
import subprocess
import sys

S = os.environ.get("C2R47_WORK") or "/fast/scratch/hyaku/mado-r47/ExecCounterC2"
D = os.path.join(S, "ctl")
SEAT = ("/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-47/w1/"
        "ExecCounterC2/receipts")
C = ("/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-47/w1/"
     "ExecCounterC2/c2-r47-terminal-entry.py")
BASE = "60edb66e2f1cb90acc6e9442fc93ded0ca42d750"
ENTRY = os.path.join(D, "corpus/knowledge/xdg-terminal-selection-r47.md")


def run(*args, check=True):
    p = subprocess.run(args, capture_output=True)
    if check and p.returncode != 0:
        sys.exit("FAILED %s: %s" % (" ".join(args), p.stderr.decode()[:1500]))
    return p


def rev():
    return run("git", "-C", D, "rev-parse", "HEAD").stdout.decode().strip()


def pos():
    return run("git", "-C", D, "rev-parse", "HEAD~0").stdout.decode().strip()


def reset_possha(sha):
    run("git", "-C", D, "checkout", sha, "--", ".")


def commit(msg):
    run("git", "-C", D, "add", "-A")
    run("git", "-C", D, "commit", "-q", "-m", msg)
    return rev()


def score(label, sha, dest):
    p = subprocess.run([sys.executable, C, "--repo", D, "--rev", sha],
                       capture_output=True)
    out = p.stdout.decode() + p.stderr.decode()
    with open(os.path.join(SEAT, dest), "w", encoding="utf-8") as fh:
        fh.write("$ python3 c2-r47-terminal-entry.py --repo <ctl> --rev %s\n" % sha)
        fh.write(out)
        fh.write("exit=%d\n" % p.returncode)
    last = [l for l in out.splitlines() if l.startswith("PRED-C2-r47:")]
    print("%-6s %s exit=%d %s" % (label, sha[:12], p.returncode,
                                  last[-1] if last else "no verdict"))
    return p.returncode, out


def main():
    os.makedirs(SEAT, exist_ok=True)
    top = run("git", "-C", D, "rev-parse", "--show-toplevel").stdout.decode().strip()
    if os.path.realpath(top) != os.path.realpath(D):
        sys.exit("clone toplevel %s != %s" % (top, D))
    POS = run("git", "-C", D, "log", "--format=%H", "--grep=minimal valid C2 r47 entry",
              "-1").stdout.decode().strip()
    if not POS:
        sys.exit("positive control commit not found")
    results = {}
    results["POS"] = score("POS", POS, "ctl-pos.txt")
    results["N-BASE"] = score("BASE", BASE, "ctl-neg-base.txt")

    # N1: a quote that occurs in no pin
    reset_possha(POS)
    text = open(ENTRY, encoding="utf-8").read()
    bad = text.replace("in descending order of preference", "in unknown order of preference", 1)
    assert bad != text
    open(ENTRY, "w", encoding="utf-8").write(bad)
    n1 = commit("neg: quote not in pin")
    results["N-QUOTE"] = score("QUOTE", n1, "ctl-neg-quote.txt")

    # N2: a branch URL in a cited row
    reset_possha(POS)
    src = os.path.join(D, "corpus/SOURCES.md")
    t = open(src, encoding="utf-8").read()
    good_url = ("https://raw.githubusercontent.com/Vladimir-csp/"
                "xdg-terminal-exec/v0.14.3/README.md")
    branch_url = good_url.replace("/v0.14.3/", "/main/")
    lines = t.split("\n")
    hit = [k for k, l in enumerate(lines) if l.startswith("| S327 |")]
    assert len(hit) == 1 and good_url in lines[hit[0]]
    lines[hit[0]] = lines[hit[0]].replace(good_url, branch_url)
    open(src, "w", encoding="utf-8").write("\n".join(lines))
    n2 = commit("neg: branch URL in the cited row")
    results["N-BRANCH"] = score("BRANCH", n2, "ctl-neg-branch.txt")

    # N5: a held row moved (S056, the documentary route)
    reset_possha(POS)
    t = open(src, encoding="utf-8").read()
    lines = t.split("\n")
    hit = [k for k, l in enumerate(lines) if l.startswith("| S056 |")]
    assert len(hit) == 1 and good_url in lines[hit[0]]
    lines[hit[0]] = lines[hit[0]].replace(good_url, branch_url)
    open(src, "w", encoding="utf-8").write("\n".join(lines))
    n6 = commit("neg: held row S056 moved")
    results["N-HELD"] = score("HELD", n6, "ctl-neg-held.txt")

    # N3: the cited receipt absent at REV
    reset_possha(POS)
    os.remove(os.path.join(D, ".ufo/waves/round-47/receipts/live-host.txt"))
    n3 = commit("neg: receipt absent")
    results["N-RECEIPT"] = score("RECEIPT", n3, "ctl-neg-receipt.txt")

    # N4: citation index, no numbered steps
    reset_possha(POS)
    text = open(ENTRY, encoding="utf-8").read()
    idx = re.sub(r"(?m)^(\d+)\. ", r"- ", text)
    assert idx != text
    open(ENTRY, "w", encoding="utf-8").write(idx)
    n4 = commit("neg: citation index without steps")
    results["N-NOSTEPS"] = score("NOSTEPS", n4, "ctl-neg-nosteps.txt")

    # N7: the receipt's selected entry contradicts its own capture
    reset_possha(POS)
    rec = os.path.join(D, ".ufo/waves/round-47/receipts/live-host.txt")
    t = open(rec, encoding="utf-8").read()
    bad = t.replace("MADO_TERM: selected=Alacritty.desktop",
                    "MADO_TERM: selected=Foot.desktop", 1)
    assert bad != t
    open(rec, "w", encoding="utf-8").write(bad)
    n7 = commit("neg: receipt contradicts capture")
    results["N-OBS"] = score("OBS", n7, "ctl-neg-observed.txt")

    # N8: a true quote with a false stated range
    reset_possha(POS)
    text = open(ENTRY, encoding="utf-8").read()
    bad = text.replace("preference\", xdgte-xdg-terminal-exec:147-166)",
                       "preference\", xdgte-xdg-terminal-exec:200-210)", 1)
    if bad == text:
        bad = text.replace('preference", xdgte-xdg-terminal-exec:147-166)',
                           'preference", xdgte-xdg-terminal-exec:200-210)', 1)
    assert bad != text, "range mutation target missing"
    open(ENTRY, "w", encoding="utf-8").write(bad)
    n8 = commit("neg: quote range moved")
    results["N-RANGE"] = score("RANGE", n8, "ctl-neg-range.txt")

    # N5: pin bytes changed under the row's sha
    reset_possha(POS)
    pin = os.path.join(D, ".ufo/waves/round-47/fetch/xdgte-xdg-terminals.list")
    data = open(pin, "rb").read()
    open(pin, "wb").write(data + b"\n")
    n5 = commit("neg: pin tampered")
    results["N-PIN"] = score("PIN", n5, "ctl-neg-pin.txt")
    expect = {"N-BASE": "clause=a entry_absent",
              "N-QUOTE": "quote_not_in_pin",
              "N-BRANCH": "url_branch_ref",
              "N-RECEIPT": "clause=f receipt_missing",
              "N-NOSTEPS": "steps=0 <6",
              "N-PIN": "pin_sha_mismatch",
              "N-HELD": "held_row_moved=S056",
              "N-OBS": "observed_mismatch",
              "N-RANGE": "quote_out_of_range"}
    for k, token in expect.items():
        if token not in results[k][1]:
            sys.exit("negative %s did not report %r" % (k, token))
    print("negatives report their intended clauses")

    summary = os.path.join(SEAT, "ctl-summary.txt")
    with open(summary, "w", encoding="utf-8") as fh:
        fh.write("control  rev  exit\n")
        for k, (rc, out) in results.items():
            fh.write("%s %d\n" % (k, rc))
    print("wrote", summary)
    bad = [k for k, (rc, _) in results.items()
           if (k == "POS" and rc != 0) or (k != "POS" and rc != 1)]
    if bad:
        sys.exit("wrong exit codes: %s" % bad)


if __name__ == "__main__":
    main()
