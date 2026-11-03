#!/usr/bin/env python3
"""fixture-c1.py — r66 C1 control matrix for a register counter (mutation seat).

Builds one fixture git repo with four revisions (genuine + three controls), runs the
counter under test at each rev, and reports correct/4 by exit code.

    python3 fixture-c1.py --counter PATH --work DIR [--label NAME]

Contract under test (PRED-C1-r66): duplicate returned-host heading, a row with no
receipt while other rows resolve, and a file-plane-only CLEAN receipt instead of the
exact live CLEAN line must each exit 1; the genuine register must exit 0.
Writes only under --work. Every git call uses -C and the toplevel is asserted before
the first commit. No worktree reads by the counter are needed.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys

HEADING = "### Surface state register (2026-11-03, this host re-observed; fixture)"
SENTINEL = "<!-- r65 register end -->"
LIVE_LINE = "MADO_VERIFY: CLEAN (52 pass, 8 notes; file + live planes verified read-only)"
FILE_LINE = "MADO_VERIFY: CLEAN (29 pass, 4 notes; file plane only - live layer skipped: --no-live)"
R = ".ufo/waves/round-65/receipts/"
GROUPS = (
    "hypr plane",
    "waybar",
    "walker",
    "terminal configs",
    "theme/wallpaper omarchy plane",
    "idle/lock plane",
    "omarchy skill docs",
    "windows desktop plane",
)


def run(argv, cwd=None, env=None):
    return subprocess.run(argv, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          env=env, text=True)


def git(repo, *args):
    return run(["git", "-C", repo, *args])


def row(group, receipts):
    return "| %s | present (2026-11-03) | probe-%s | %s |" % (group, group.replace(" ", "-"),
                                                             " ".join(receipts))


def block(rows, heading=HEADING, sentinel=SENTINEL):
    lines = [heading, "", "| surface group | state (date) | probe | receipt |",
             "| --- | --- | --- | --- |"]
    lines.extend(rows)
    lines.append("")
    lines.append(sentinel)
    return "\n".join(lines)


def genuine_rows(missing_receipt=False):
    out = []
    for group in GROUPS:
        if group in ("hypr plane", "waybar", "walker", "idle/lock plane"):
            receipts = [R + "before-register-probes-r65.txt", R + "gate-live-r65.txt"]
        elif group in ("terminal configs", "theme/wallpaper omarchy plane"):
            receipts = [R + "gate-fileplane-r65.txt", R + "before-register-probes-r65.txt"]
        elif group == "omarchy skill docs":
            receipts = [R + "before-register-probes-r65.txt", R + "gate-fileplane-r65.txt"]
        else:
            receipts = [R + "windows-plane-absence-r65.txt"]
        if missing_receipt and group == "walker":
            receipts = []
        out.append(row(group, receipts))
    return out


def receipts(genuine_live=True):
    return {
        R + "before-register-probes-r65.txt": "# probe log\nfixture\n",
        R + "gate-live-r65.txt": (LIVE_LINE if genuine_live else FILE_LINE) + "\n",
        R + "gate-fileplane-r65.txt": FILE_LINE + "\n",
        R + "windows-plane-absence-r65.txt": "# absence log\nfixture\n",
    }


def build_repo(repo):
    if os.path.exists(repo):
        shutil.rmtree(repo)
    os.makedirs(repo)
    g = git(repo, "init", "-q")
    assert g.returncode == 0, g.stderr
    top = git(repo, "rev-parse", "--show-toplevel").stdout.strip()
    assert top == os.path.realpath(repo), (top, repo)
    revs = {}

    def commit(name, province, receipt_map):
        for rel, text in receipt_map.items():
            path = os.path.join(repo, rel)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(text)
        with open(os.path.join(repo, "PROVINCE.md"), "w", encoding="utf-8") as fh:
            fh.write(province)
        git(repo, "add", "-A")
        c = git(repo, "-c", "user.name=mado-r66-mut", "-c",
                "user.email=mut@example.invalid", "-c", "commit.gpgsign=false",
                "commit", "-q", "-m", name)
        assert c.returncode == 0, c.stderr
        revs[name] = git(repo, "rev-parse", "HEAD").stdout.strip()

    gen = "# PROVINCE\nfixture lane\n\n" + block(genuine_rows()) + "\n"
    commit("genuine", gen, receipts(True))

    dup = ("# PROVINCE\nfixture lane\n\n" + block(genuine_rows()) + "\n\n"
           + block(genuine_rows(), heading=HEADING + " (duplicate record)") + "\n")
    commit("dup-heading", dup, receipts(True))

    norow = "# PROVINCE\nfixture lane\n\n" + block(genuine_rows(missing_receipt=True)) + "\n"
    commit("missing-row-receipt", norow, receipts(True))

    plane = "# PROVINCE\nfixture lane\n\n" + block(genuine_rows()) + "\n"
    commit("fileplane-only", plane, receipts(False))

    # Auxiliary probe (not one of the three published controls): the exact live line exists
    # only in a non-live receipt, so a counter that ignores the live PATH must reject.
    wrong = receipts(True)
    wrong[R + "gate-live-r65.txt"] = "# live gate\n"
    wrong[R + "gate-fileplane-r65.txt"] = LIVE_LINE + "\n"
    commit("live-line-wrong-receipt", plane, wrong)
    return revs


def parse_verdict(out):
    for line in out.splitlines():
        if "verdict=TARGET_MET" in line:
            return "TARGET_MET"
        if "verdict=TARGET_MISSED" in line:
            return "TARGET_MISSED"
    return ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--counter", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--label", default="counter")
    args = ap.parse_args()
    work = os.path.realpath(args.work)
    os.makedirs(work, exist_ok=True)
    repo = os.path.join(work, "repo")
    revs = build_repo(repo)
    counter = os.path.realpath(args.counter)
    expectations = {
        "genuine": (0, "accept"),
        "dup-heading": (1, "reject"),
        "missing-row-receipt": (1, "reject"),
        "fileplane-only": (1, "reject"),
    }
    results = {}
    correct = 0
    aux = {}
    for name in ("genuine", "dup-heading", "missing-row-receipt", "fileplane-only"):
        proc = run([sys.executable, counter, "--repo", repo, "--rev", revs[name]], cwd=work)
        want_rc, want = expectations[name]
        ok = proc.returncode == want_rc
        # A verdict token, when printed, must agree with the exit status.
        verdict = parse_verdict(proc.stdout)
        if verdict:
            ok = ok and ((verdict == "TARGET_MET") == (proc.returncode == 0))
        correct += int(ok)
        results[name] = {
            "rev": revs[name],
            "want": want,
            "want_rc": want_rc,
            "rc": proc.returncode,
            "verdict": verdict,
            "correct": ok,
            "stdout": proc.stdout.strip(),
            "stderr": proc.stderr.strip(),
        }
        print("%s\t%s\twant=%s rc=%d\tgot_rc=%d\tverdict=%s\t%s"
              % (args.label, name, want, want_rc, proc.returncode, verdict or "-",
                 "CORRECT" if ok else "WRONG"))
    # Auxiliary probe, reported separately from the frozen 4/4 count.
    proc = run([sys.executable, counter, "--repo", repo,
                "--rev", revs["live-line-wrong-receipt"]], cwd=work)
    aux_ok = proc.returncode == 1
    aux["live-line-wrong-receipt"] = {
        "want": "reject", "want_rc": 1, "rc": proc.returncode,
        "verdict": parse_verdict(proc.stdout), "correct": aux_ok,
        "stdout": proc.stdout.strip(), "stderr": proc.stderr.strip(),
    }
    print("%s\taux-live-line-wrong-receipt\twant=reject rc=1\tgot_rc=%d\t%s"
          % (args.label, proc.returncode, "CORRECT" if aux_ok else "WRONG"))
    summary = {"label": args.label, "counter": counter, "repo": repo, "revs": revs,
               "correct": correct, "total": 4, "results": results, "aux": aux}
    out = os.path.join(work, "c1-matrix-%s.json" % args.label)
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=1, sort_keys=True)
    print("%s\tTOTAL\t%d/4\t%s" % (args.label, correct, out))
    return 0 if correct == 4 else 1


if __name__ == "__main__":
    sys.exit(main())
