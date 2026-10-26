#!/usr/bin/env python3
"""Round-44 C2 do-nothing controls for the frozen PRED-C2-r44 counter. Each control is committed in a
throwaway clone under --work (git clone --shared; every git call names -C <clone>; fixture identity
only inside the clone, verified by rev-parse --show-toplevel). None may reach TARGET_MET.
Usage: run-c2-controls.py --repo LANE --base BASE --work SCRATCHDIR"""
import argparse, os, shutil, subprocess, sys

ENTRY = "corpus/knowledge/hyprland-gkeep-size-request-r44.md"
STAGED = "/home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge/gkeep-client-size-request-r12.md"
PKG = "merge/mado/knowledge/corpus/knowledge/"
GATE_TAIL = ("\n## Gate\n\nADMIT %sgkeep-client-size-request-r12.md as %s\n"
             "REFUSE %sgkeep-rendered-geometry-record-r13.md reason=journal route rests on unpinned sources until a pinned log exists\n"
             % (PKG, ENTRY, PKG))
README_ROW = "| `knowledge/hyprland-gkeep-size-request-r44.md` | control row | - |\n"
SHELL = """# gkeep size request (control: header and census only)

source: S164
source: S298
source: S299
source: S300
source: S301
verified-at: 2026-10-26
recheck: 30d

gkeep client default_size=420x500 size_request_calls=0 application_id=org.omarchy.gkeep
hyprland sendWindowSize xdg_setSize=1 x11_configure=1
"""


def g(d, *a):
    return subprocess.run(["git", "-C", d, *a], capture_output=True, text=True,
                          env={k: v for k, v in os.environ.items() if not k.startswith("GIT_")})


def control(repo, base, work, name, files, append):
    d = os.path.join(work, name)
    shutil.rmtree(d, ignore_errors=True)
    subprocess.run(["git", "clone", "-q", "--shared", "--no-checkout", repo, d], check=True)
    assert g(d, "rev-parse", "--show-toplevel").stdout.strip() == os.path.realpath(d)
    g(d, "checkout", "-q", "--detach", base)
    for path, text in files.items():
        p = os.path.join(d, path)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "w").write(text)
    for path, text in append.items():
        open(os.path.join(d, path), "a").write(text)
    g(d, "add", "-A")
    r = g(d, "-c", "user.name=ctl", "-c", "user.email=ctl@scratch.invalid", "commit", "-q", "-m", name)
    assert r.returncode == 0, r.stderr
    return d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--base", required=True)
    ap.add_argument("--work", required=True)
    a = ap.parse_args()
    counter = os.path.join(a.repo, "quality", "counters", "c2-r44-gkeep-size-request.py")
    os.makedirs(a.work, exist_ok=True)
    lesson = "corpus/lessons/round-44.md"
    runs = [("C2-BASE", a.repo, a.base)]
    runs.append(("C2-STAGED-COPY", control(a.repo, a.base, a.work, "staged-copy",
                 {ENTRY: open(STAGED).read(), lesson: "# round 44\n" + GATE_TAIL},
                 {"corpus/README.md": README_ROW}), "HEAD"))
    runs.append(("C2-SHELL", control(a.repo, a.base, a.work, "shell",
                 {ENTRY: SHELL, lesson: "# round 44\n" + GATE_TAIL},
                 {"corpus/README.md": README_ROW}), "HEAD"))
    wrong = 0
    print("CTL_C2: base=%s controls=%d (do-nothing: base, staged r12 copied verbatim, header+census shell)" % (a.base, len(runs)))
    for name, repo, rev in runs:
        p = subprocess.run([sys.executable, "-I", counter, "--repo", repo, "--rev", rev, "--base", a.base],
                           capture_output=True, text=True)
        lines = p.stdout.strip().splitlines()
        cl = next((l for l in lines if " clauses=" in l), "-")
        met = p.returncode == 0
        wrong += met
        print("CTL_C2 %s rc=%d %s | %s | %s" % (name, p.returncode, "WRONG" if met else "ok",
              cl.split(" clauses=")[-1] if cl != "-" else "-", lines[-1] if lines else ""))
    for name, repo, rev in runs[1:]:
        shutil.rmtree(repo, ignore_errors=True)
    print("CTL_C2 VERDICT: %s (controls scoring TARGET_MET: %d of %d)" % ("PASS" if not wrong else "FAIL", wrong, len(runs)))
    return 1 if wrong else 0


if __name__ == "__main__":
    sys.exit(main())
