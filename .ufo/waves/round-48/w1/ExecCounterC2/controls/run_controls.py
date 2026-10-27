#!/usr/bin/env python3
"""Run PRED-C2-r48 on the POS tree and every control; assert each fails on its clause."""
import os
import re
import subprocess
import sys

S = "/fast/scratch/hyaku/mado-r48/ExecCounterC2"
REPO = os.path.join(S, "repo")
COUNTER = ("/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-48/w1/"
           "ExecCounterC2/c2-r48-xkb-entry.py")
BASE = "579f694b45c797a9c39761fdb4f9e0a1b71b3585"
TARGET = {"QUOTE": "d", "RANGE": "d", "BRANCH": "c", "PIN": "c", "HELD": "h",
          "RECEIPT-absent": "f", "RECEIPT-contradicts": "f", "NOSTEPS": "e"}
ORDER = ["BASE", "POS"] + list(TARGET)


def revs():
    out = {}
    with open(os.path.join(S, "revs.txt")) as fh:
        for line in fh:
            name, rev = line.split()
            out[name] = rev
    return out


def run(rev, base=BASE):
    p = subprocess.run(["python3", COUNTER, "--repo", REPO, "--rev", rev,
                        "--base", base], capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def clauses(text):
    m = re.search(r"clauses=((?:[a-i]:\d ?)+)", text)
    if not m:
        return None
    return dict(x.split(":") for x in m.group(1).split())


def main():
    rev = revs()
    log = []
    fail = []
    pos_vec = None
    live_rc = ("/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-48/w1/"
               "ExecXkbLive/receipts/xkb-live.txt")
    if os.path.exists(live_rc):
        with open(live_rc, "rb") as fh:
            live_bytes = fh.read()
    else:
        live_bytes = None
    for name in ORDER:
        if name == "BASE":
            rc, text = run(BASE)
        elif name == "POS":
            rc, text = run(rev["POS"])
        else:
            rc, text = run(rev[name])
        log.append("==== %s rc=%d\n%s" % (name, rc, text))
        if name == "POS":
            if rc != 0 or "admitted=1/1" not in text:
                fail.append("POS not admitted rc=%d" % rc)
            pos_vec = clauses(text)
            continue
        if name == "BASE":
            if rc != 1 or "clause=a entry_absent" not in text:
                fail.append("BASE not rejected at clause a")
            continue
        if rc != 1 or "admitted=0/1" not in text:
            fail.append("%s not rejected rc=%d" % (name, rc))
        vec = clauses(text)
        tgt = TARGET[name]
        if vec is None or vec.get(tgt) != "0":
            fail.append("%s did not fail clause %s: %s" % (name, tgt, vec))
        if vec and pos_vec:
            flipped = sorted(k for k in pos_vec if pos_vec[k] != vec.get(k))
            log.append("---- %s target=%s flipped=%s" % (name, tgt, flipped))
    # setup precondition: base == rev
    rc, text = run(rev["POS"], base=rev["POS"])
    log.append("==== SETUP rc=%d\n%s" % (rc, text))
    if rc != 2 or "precondition_failed" not in text:
        fail.append("SETUP not exit 2: rc=%d" % rc)

    def git(*args):
        p = subprocess.run(["git", "-C", REPO, *args], capture_output=True, text=True)
        if p.returncode != 0:
            raise SystemExit("git %s: %s" % (" ".join(args), p.stderr))
        return p.stdout.strip()

    def commit_from(base_rev, branch, msg, mutate):
        git("checkout", "-q", "-B", branch, base_rev)
        mutate()
        git("add", "-A")
        git("-c", "user.name=ExecCounterC2", "-c", "user.email=exec@local",
            "-c", "commit.gpgsign=false", "commit", "-q", "-m", msg)
        return git("rev-parse", "HEAD")

    if live_bytes is not None:
        import hashlib
        live_sha = hashlib.sha256(live_bytes).hexdigest()
        target = os.path.join(REPO, ".ufo/waves/round-48/receipts/xkb-live.txt")

        def put_live():
            with open(target, "wb") as fh:
                fh.write(live_bytes)
        live_rev = commit_from(rev["POS"], "pos-live", "POS-LIVE: live receipt bytes",
                               put_live)
        rc, text = run(live_rev)
        log.append("==== POS-LIVE (%s) rc=%d\n%s" % (live_sha, rc, text))
        if rc != 0 or "admitted=1/1" not in text:
            fail.append("POS-LIVE not admitted rc=%d" % rc)
        live_vec = clauses(text)

        def flip_variant():
            with open(target) as fh:
                lines = fh.read().splitlines(True)
            out = []
            for line in lines:
                if "unknown-variant" in line and "rc=1" in line:
                    line = line.replace("rc=1", "rc=0", 1)
                out.append(line)
            with open(target, "w") as fh:
                fh.writelines(out)
        rev_c = commit_from(live_rev, "ctl-live-contradicts",
                            "control LIVE-receipt-contradicts", flip_variant)
        rc, text = run(rev_c)
        log.append("==== LIVE-receipt-contradicts rc=%d\n%s" % (rc, text))
        if rc != 1 or clauses(text) is None or clauses(text).get("f") != "0":
            fail.append("LIVE-receipt-contradicts did not fail clause f")

        def entry_digest():
            path = os.path.join(REPO, "corpus/knowledge/xkb-keymap-compile-r48.md")
            with open(path) as fh:
                t = fh.read()
            with open(path, "w") as fh:
                fh.write(t.replace("efd487a39920152354f0", "deadbeefdeadbeefdead", 1))
        rev_e = commit_from(live_rev, "ctl-live-entrydigest",
                            "control LIVE-entry-disagrees", entry_digest)
        rc, text = run(rev_e)
        log.append("==== LIVE-entry-disagrees rc=%d\n%s" % (rc, text))
        if rc != 1 or clauses(text) is None or clauses(text).get("f") != "0":
            fail.append("LIVE-entry-disagrees did not fail clause f")
    # POS minimality: the commit touches only the entry, rows, README, receipt, pins
    stat = subprocess.run(["git", "-C", REPO, "show", "--name-only", "--format=",
                           rev["POS"]], capture_output=True, text=True).stdout
    want = sorted([
        "corpus/knowledge/xkb-keymap-compile-r48.md",
        "corpus/SOURCES.md", "corpus/README.md",
        ".ufo/waves/round-48/receipts/xkb-live.txt",
        ".ufo/waves/round-48/fetch/libxkbcommon-rules.c",
        ".ufo/waves/round-48/fetch/libxkbcommon-context.c",
        ".ufo/waves/round-48/fetch/xkeyboard-config-symbols-br",
    ])
    got = sorted(x for x in stat.split() if x)
    log.append("==== POS FILES\n%s" % "\n".join(got))
    if got != want:
        fail.append("POS tree not minimal: %s" % got)
    out = os.path.join("/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-48/"
                       "w1/ExecCounterC2/receipts")
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "controls.txt"), "w") as fh:
        fh.write("\n".join(log) + "\n")
    if fail:
        print("CONTROLS FAILED")
        for f in fail:
            print(" -", f)
        return 1
    print("CONTROLS OK: POS admitted, BASE clause a, 8 controls on their clauses, SETUP exit 2")
    return 0


if __name__ == "__main__":
    sys.exit(main())
