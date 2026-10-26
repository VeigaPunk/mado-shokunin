#!/usr/bin/env python3
"""probe_waivers.py — falsification probes against the round-47 marker gate.

Builds small scratch git repos and runs the seat's gate on them. Prints only
booleans, counts and gate verdict lines (the gate never prints values).
"""
import hashlib
import os
import subprocess
import sys

GATE = ("/home/vgpnk/Projects/shokunin/mado-shokunin/"
        ".ufo/waves/round-47/w1/ExecSessionMarker/check-session-material.py")
SCRATCH = "/fast/scratch/hyaku/mado-r47/RevSessionMarker/probes"
REG_HDR = "# path sha256 rules kind — see quality/check-session-material.py\n"


def sh(*args, **kw):
    return subprocess.run(list(args), capture_output=True, text=True, **kw)


def build(name, files):
    root = os.path.join(SCRATCH, name)
    os.makedirs(root, exist_ok=True)
    for rel, text in files.items():
        target = os.path.join(root, rel)
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "w", encoding="utf-8") as h:
            h.write(text)
    r = sh("git", "-C", root, "init", "-q")
    assert r.returncode == 0, r.stderr
    sh("git", "-C", root, "add", "-A")
    r = sh("git", "-C", root, "-c", "user.name=probe", "-c",
           "user.email=probe@scratch.invalid", "commit", "-q", "-m", "fixtures")
    assert r.returncode == 0, r.stderr
    top = sh("git", "-C", root, "rev-parse", "--show-toplevel").stdout.strip()
    assert os.path.realpath(top) == os.path.realpath(root), top
    return root


def digest(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def marker(kind, rules, sha):
    return "SYNTHETIC-MATERIAL v1 kind=%s rules=%s sha256=%s\n" % (kind, rules, sha)


def run_gate(root, extra=()):
    r = subprocess.run([sys.executable, "-I", GATE, "--repo", root, "--rev", "HEAD", *extra],
                       capture_output=True, text=True,
                       env={**os.environ, "TMPDIR": SCRATCH + "/tmp"})
    return r.returncode, r.stdout


def report(tag, rc, out):
    waived = [l for l in out.splitlines() if l.startswith("WAIVER ")]
    rejected = [l for l in out.splitlines() if l.startswith("WAIVER_REJECTED ")]
    findings = [l for l in out.splitlines() if l.startswith("FINDING ")]
    summary = [l for l in out.splitlines() if l.startswith("SESSION_MATERIAL: ")]
    print("== %s rc=%d" % (tag, rc))
    for l in waived:
        print("   " + l)
    for l in rejected:
        print("   " + l)
    for l in findings:
        print("   " + l)
    for l in summary:
        print("   " + l)


def main():
    os.makedirs(SCRATCH + "/tmp", exist_ok=True)

    # P1: a real-world window title inside the reserved namespace.
    # "Example Domain" is the live <title> of example.com; "Demo" is a common
    # real window title. Both must be treated as synthetic by W4b if the
    # namespace is broader than synthetic fixtures.
    dump1 = ('[{"address": "0x1", "mapped": true, "class": "org.mozilla.firefox",'
             ' "title": "Example Domain", "pid": 1234}]\n')
    dump2 = ('[{"address": "0x2", "mapped": true, "class": "org.mozilla.firefox",'
             ' "title": "Demo", "pid": 1235}]\n')
    p1 = ".ufo/waves/round-47/w1/ProbeSeat/clients.json"
    reg = REG_HDR
    files = {}
    for tag, dump in (("example-domain", dump1), ("demo", dump2)):
        path = ".ufo/waves/round-47/w1/ProbeSeat/%s.json" % tag
        files[path] = dump
        files[path + ".synthetic"] = marker("fixture", "R1_CLIENT_DUMP", digest(dump))
        reg += "%s %s R1_CLIENT_DUMP kind=fixture\n" % (path, digest(dump))
    files["quality/session-material-waivers.txt"] = reg
    root = build("p1-real-titles", files)
    rc, out = run_gate(root)
    report("P1 real titles Example Domain / Demo", rc, out)

    # P1-control: a real title outside the namespace must be refused.
    dump3 = ('[{"address": "0x3", "mapped": true, "class": "org.mozilla.firefox",'
             ' "title": "Pull request #42 - foo/bar", "pid": 1236}]\n')
    path3 = ".ufo/waves/round-47/w1/ProbeSeat/control.json"
    files = {
        path3: dump3,
        path3 + ".synthetic": marker("fixture", "R1_CLIENT_DUMP", digest(dump3)),
        "quality/session-material-waivers.txt": REG_HDR +
            "%s %s R1_CLIENT_DUMP kind=fixture\n" % (path3, digest(dump3)),
    }
    root = build("p1-control", files)
    rc, out = run_gate(root)
    report("P1-control real title outside namespace", rc, out)

    # P2: monitors dump with an EMPTY serial but a real make/model/description.
    # SKILL rule 4 names "monitor serials/descriptions"; R3 requires a
    # non-empty serial, so this dump must escape every rule.
    mon = ('[{"name": "DP-1", "description": "DELL U2720Q", "make": "Dell Inc.",'
           ' "model": "DELL U2720Q", "serial": "", "width": 3840, "height": 2160}]\n')
    files = {".ufo/waves/round-47/w1/ProbeSeat/mons-noserial.json": mon}
    root = build("p2-serialless", files)
    rc, out = run_gate(root)
    report("P2 serial-less real monitor dump", rc, out)

    # P3: the registry relocated by flag to a tracked non-quality path.
    mon2 = ('[{"name": "DP-1", "description": "Fake Corp 0x0000 SN00000",'
            ' "make": "Fake Corp", "model": "0x0000", "serial": "SN00000",'
            ' "width": 3440, "height": 1440}]\n')
    path = ".ufo/waves/round-47/w1/ProbeSeat/mons.json"
    files = {
        path: mon2,
        path + ".synthetic": marker("fixture", "R3_MONITOR_IDENT", digest(mon2)),
        "notes/waivers.txt": REG_HDR +
            "%s %s R3_MONITOR_IDENT kind=fixture\n" % (path, digest(mon2)),
    }
    root = build("p3-relocated-registry", files)
    rc, out = run_gate(root, ("--waivers", "notes/waivers.txt"))
    report("P3 registry relocated to notes/waivers.txt", rc, out)

    # P4: a real window title in prose only (no JSON object anywhere).
    files = {".ufo/waves/round-47/w1/ProbeSeat/prose.md":
             'Focused the terminal; its title read "Example Domain" at the time.\n'}
    root = build("p4-prose-title", files)
    rc, out = run_gate(root)
    report("P4 real title in prose only", rc, out)


if __name__ == "__main__":
    main()
