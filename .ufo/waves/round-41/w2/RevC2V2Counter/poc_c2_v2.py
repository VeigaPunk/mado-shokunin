#!/usr/bin/env python3
"""RevC2V2Counter — PoC harness attacking PRED-C2-r41-v2 and run-c2-v2-controls.py.

Every fixture repo is built in D=$(mktemp -d), git -C D init -q, toplevel verified
equal to D before the first commit, throwaway identity passed via -c, and cleaned
up in a finally block. Nothing outside the seat directory is written.
"""
import hashlib
import importlib.util
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
COUNTER = os.path.join(LANE, "quality", "counters", "c2-r41-focus-entry-v2.py")
CTL_PATH = os.path.join(LANE, ".ufo", "waves", "round-41", "ctl", "run-c2-v2-controls.py")

spec = importlib.util.spec_from_file_location("ctl", CTL_PATH)
ctl = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ctl)

spec_c2 = importlib.util.spec_from_file_location("c2v2", COUNTER)
c2v2 = importlib.util.module_from_spec(spec_c2)
spec_c2.loader.exec_module(c2v2)


def fixed_patched_counter(dest, files):
    """Patched counter where fixture receipts override PINS (inserted before closing brace)."""
    src = open(COUNTER).read()
    extra = "".join('    "%s": "%s",\n' % (os.path.basename(k), ctl.sha(v))
                    for k, v in files.items()
                    if k.startswith(ctl.FETCH) and not isinstance(v, bool))
    target = '"bf8fa91a321197277cf9c1260d17524e9ddf862f7f76ddf440fc057aa600aaf7",\n}'
    assert target in src
    src = src.replace(target, '"bf8fa91a321197277cf9c1260d17524e9ddf862f7f76ddf440fc057aa600aaf7",\n' + extra + '}', 1)
    path = os.path.join(dest, "c2-fixed-patched.py")
    open(path, "w").write(src)
    return path


def score_fixture(files_base, files_after, mode="real"):
    """Score a fixture under 'real', 'broken-patched' (ctl.patched_counter), or 'fixed-patched'."""
    d = tempfile.mkdtemp(prefix="mado-revc2v2-")
    pdir = tempfile.mkdtemp(prefix="mado-revc2v2-p-")
    try:
        subprocess.run(["git", "-C", d, "init", "-q"], check=True, env=ctl.ENV)
        top = subprocess.run(["git", "-C", d, "rev-parse", "--show-toplevel"],
                             check=True, capture_output=True, text=True,
                             env=ctl.ENV).stdout.strip()
        if os.path.realpath(top) != os.path.realpath(d):
            raise SystemExit("fixture toplevel mismatch: %s != %s" % (top, d))
        b = ctl.commit_all(d, files_base, "base")
        a = ctl.commit_all(d, files_after, "after")
        if mode == "real":
            counter = COUNTER
        elif mode == "broken-patched":
            counter = ctl.patched_counter(pdir, files_after)
        elif mode == "fixed-patched":
            counter = fixed_patched_counter(pdir, files_after)
        else:
            raise ValueError(mode)
        p = subprocess.run([sys.executable, "-I", counter, "--repo", d,
                            "--rev", a, "--base", b],
                           capture_output=True, text=True, env=ctl.ENV)
        lines = p.stdout.strip().splitlines()
        cls = [l for l in lines if " clauses=" in l]
        clauses = cls[0].split(" clauses=")[1].split(" admitted")[0] if cls else "-"
        last = lines[-1] if lines else "NO-OUTPUT " + p.stderr[-120:]
        verdict = last.split(": ", 1)[-1].split(" rev=")[0]
        return p.returncode, verdict, clauses
    finally:
        shutil.rmtree(d, ignore_errors=True)
        shutil.rmtree(pdir, ignore_errors=True)


def main():
    base = ctl.base_files()
    G = ctl.admitted()
    m = ctl.mutants(base, G)

    print("=== PART 1: Control runner `patched_counter()` shadow bug & W16 HTML cross-block survivor ===")
    for cname in ["W16-quote-across-html-blocks", "J02-single-session",
                  "J11-other-level-adverts", "J16-no-boot-line", "J17-sessions-replayed"]:
        _, g_mut = m[cname]
        rc_b, v_b, c_b = score_fixture(base, g_mut, "broken-patched")
        rc_f, v_f, c_f = score_fixture(base, g_mut, "fixed-patched")
        print(f"control={cname:32s} broken_patched=({rc_b}, {v_b}, {c_b}) | fixed_patched=({rc_f}, {v_f}, {c_f})")

    print("\n=== PART 2: PoC bypasses on the FROZEN REAL counter (c2-r41-focus-entry-v2.py) ===")
    pocs = []

    # PoC-01: W16 on the real pinned issue-565.html receipt (quote assembled across HTML blocks)
    g = dict(G)
    cb_q = "GitHub Skip to content Navigation Menu"
    ctl.set_receipt(g, "S287", "issue-565.html", ctl.blob("issue-565.html"), cb_q)
    ctl.rep(g, ctl.ENTRY, ctl.REAL["S287"][3], cb_q)
    pocs.append(("POC01-real-html-quote-across-blocks", "real", base, g))

    # PoC-02: PINS reuse of uncited pinned receipts (input-capture-v1.xml & Hyprland-FocusGrab.hpp) + .ext location
    g = dict(G)
    ic_q = "This protocol is a bridge of the XDG input capture to the compositor."
    hpp_q = "CFocusGrabSurfaceState(CFocusGrab* grab, SP<CWLSurfaceResource> surface);"
    ctl.set_receipt(g, "S283", "input-capture-v1.xml", ctl.blob("input-capture-v1.xml"), ic_q)
    ctl.rep(g, ctl.ENTRY, ctl.REAL["S283"][3], ic_q)
    ctl.rep(g, ctl.SRC, ctl.REAL["S283"][2], "https://unrelated.invalid/.xml")
    ctl.set_receipt(g, "S284", "Hyprland-FocusGrab.hpp", ctl.blob("Hyprland-FocusGrab.hpp"), hpp_q)
    ctl.rep(g, ctl.ENTRY, ctl.REAL["S284"][3], hpp_q)
    ctl.rep(g, ctl.SRC, ctl.REAL["S284"][2], "https://unrelated.invalid/.hpp")
    pocs.append(("POC02-pins-reuse-unused-xml-hpp", "real", base, g))

    # PoC-03: Full permutation of all 6 non-journal pinned receipts across S283..S288
    g = dict(G)
    perm = {"S283": "S288", "S284": "S285", "S285": "S286", "S286": "S287", "S287": "S283", "S288": "S284"}
    held = ctl.HELD_ROW.replace("corpus/knowledge/old.md", "corpus/knowledge/old.md, " + ctl.ENTRY)
    gates = [ctl.gate_line("S050", ctl.FETCH + "S050.txt", g[ctl.FETCH + "S050.txt"], ctl.HELD_Q)]
    rows = [held]
    body = ["# Permuted", "", "source: S050"] + [f"source: {i}" for i in ctl.REAL] + [
        "verified-at: 2026-10-25", "recheck: 90d", "", "**OBS** S050 %s." % ctl.HELD_Q
    ]
    for i in ctl.REAL:
        target = perm.get(i, i)
        fn, _, loc, q = ctl.REAL[target]
        rows.append(ctl.row(i, loc, kind=ctl.REAL[i][1]))
        gates.append(ctl.gate_line(i, ctl.FETCH + fn, ctl.blob(fn), q))
        body.append("**OBS** %s %s." % (i, q))
    body += ["", ctl.JLINE, ""]
    g[ctl.SRC] = base[ctl.SRC].replace(ctl.HELD_ROW, "\n".join(rows))
    g[ctl.LES] = "# round 41\n\n## Gate\n\n" + "\n".join(gates) + "\n" + ctl.ADMIT + "\n" + ctl.REFUSE + "\n"
    g[ctl.ENTRY] = "\n".join(body) + "\n"
    pocs.append(("POC03-pins-full-id-permutation", "real", base, g))

    # PoC-04: Swap S283 (docs) and S289 (own-work journal) using .txt / .xml locations
    g = dict(G)
    gates = []
    for l in g[ctl.LES].splitlines():
        if l.startswith("GATE S283 "):
            gates.append(ctl.gate_line("S283", ctl.FETCH + "xdph-journal.txt", ctl.JBYTES, ctl.REAL["S289"][3]))
        elif l.startswith("GATE S289 "):
            gates.append(ctl.gate_line("S289", ctl.FETCH + "focus-grab-v1.xml", ctl.blob("focus-grab-v1.xml"), ctl.REAL["S283"][3]))
        else:
            gates.append(l)
    g[ctl.LES] = "\n".join(gates) + "\n"
    g[ctl.SRC] = g[ctl.SRC].replace(
        ctl.row("S283", ctl.REAL["S283"][2], kind="docs"),
        ctl.row("S283", "https://example.org/fake/.txt", kind="own-work")
    ).replace(
        ctl.row("S289", ctl.REAL["S289"][2], kind="own-work"),
        ctl.row("S289", "https://example.org/fake/.xml", kind="docs")
    )
    g[ctl.ENTRY] = g[ctl.ENTRY].replace(
        "**OBS** S283 %s." % ctl.REAL["S283"][3], "**OBS** S283 %s." % ctl.REAL["S289"][3]
    ).replace(
        "**OBS** S289 %s." % ctl.REAL["S289"][3], "**OBS** S289 %s." % ctl.REAL["S283"][3]
    )
    pocs.append(("POC04-pins-swap-docs-and-ownwork", "real", base, g))

    # PoC-05: Held ID overwrites a pinned filename (protocols-README.md) with forged bytes
    g = dict(G)
    forged_readme = (ctl.HELD_Q + " forged held receipt overwriting protocols-README.md " + ctl.FILLER).encode()
    g[ctl.FETCH + "protocols-README.md"] = forged_readme
    g[ctl.ENTRY] = "\n".join(l for l in g[ctl.ENTRY].splitlines() if "S288" not in l) + "\n"
    g[ctl.SRC] = "\n".join(l for l in g[ctl.SRC].splitlines() if "S288" not in l) + "\n"
    gates = []
    for l in g[ctl.LES].splitlines():
        if l.startswith("GATE S288 "):
            continue
        if l.startswith("GATE S050 "):
            gates.append(ctl.gate_line("S050", ctl.FETCH + "protocols-README.md", forged_readme, ctl.HELD_Q))
        else:
            gates.append(l)
    g[ctl.LES] = "\n".join(gates) + "\n"
    pocs.append(("POC05-held-id-overwrites-pinned-file", "real", base, g))

    # PoC-06: Location/receipt binding bypass via 1-char '.' component (`comp in rb`)
    g = dict(G)
    for idx, i in enumerate(["S283", "S284", "S285", "S286", "S287", "S288"]):
        ctl.rep(g, ctl.SRC, ctl.REAL[i][2], f"https://unrelated-{idx}.invalid/.")
    pocs.append(("POC06-loc-1char-dot-substring", "real", base, g))

    # PoC-07: All 6 new IDs share the same URL path via `?dup=N` + superstring component (`rb in comp`)
    g = dict(G)
    mega_comp = "-".join(ctl.REAL[i][0] for i in ["S283", "S284", "S285", "S286", "S287", "S288"])
    for idx, i in enumerate(["S283", "S284", "S285", "S286", "S287", "S288"]):
        ctl.rep(g, ctl.SRC, ctl.REAL[i][2], f"https://single-url.invalid/{mega_comp}?dup={idx}")
    pocs.append(("POC07-loc-query-dup-and-superstring", "real", base, g))

    # PoC-08: STAGED allowlist bypass (arbitrary prefix path + same file both ADMITted and REFUSEd via './' + punctuation reason)
    g = dict(G)
    ctl.rep(g, ctl.LES, ctl.ADMIT, "ADMIT /evil/nonexistent/../../focus-control-surfaces-r28.md as " + ctl.ENTRY)
    ctl.rep(g, ctl.LES, ctl.REFUSE, "REFUSE ./focus-control-surfaces-r28.md reason=a. a, a; a! a? a: a- a_ a/ a")
    pocs.append(("POC08-staged-prefix-selfrefuse-punct", "real", base, g))

    # PoC-09: BAD_LOC false positive on English row disclaiming `/ja` in scope cell
    g = dict(G)
    ctl.rep(g, ctl.SRC, "| scope | anchor | teaches | mined | 2026-10-25",
            "| English upstream only (no /ja channel) | anchor | teaches | mined | 2026-10-25")
    pocs.append(("POC09-badloc-false-positive-english-row", "real", base, g))

    # PoC-10: BAD_LOC bypass via .jp/.cn TLDs, note.com, and URL percent-encoding (%7ah/%6aa)
    g = dict(G)
    ctl.rep(g, ctl.SRC, ctl.REAL["S283"][2], "https://blog.example.jp/hyprland-focus-grab-v1.xml")
    ctl.rep(g, ctl.SRC, ctl.REAL["S284"][2], "https://juejin.cn/post/FocusGrab.cpp")
    ctl.rep(g, ctl.SRC, ctl.REAL["S285"][2], "https://note.com/jp_user/grab.cpp")
    ctl.rep(g, ctl.SRC, ctl.REAL["S286"][2], "https://example.org/%7ah/%6aa/PortalManager.cpp")
    pocs.append(("POC10-badloc-bypass-tld-percent-encode", "real", base, g))

    # PoC-11: Header window bypass (indented source/verified-at/recheck past line 20 + unvalidated recheck trailer + non-S### source in head)
    g = dict(G)
    ctl.rep(g, ctl.ENTRY, "source: S050 - held parser",
            "source: S050 - held parser\nsource: https://amgsk.dev/ja/untracked-source")
    ctl.rep(g, ctl.ENTRY, "recheck: 90d", "recheck: 0d UNVALIDATED_TRAILER 2026-99-99")
    g[ctl.ENTRY] += "\n" + "\n".join(f"pad {k}" for k in range(25)) + "\n  source: S283 - indented past 20\n  verified-at: 1999-01-01\n  recheck: bad\n"
    pocs.append(("POC11-header-indented-outside-and-trailer", "real", base, g))

    # PoC-12: Clause d `GATE S###` outside `## Gate` evades `line not in in_gate` when identical to an inside line + uncited GATE S999
    g = dict(G)
    gate_s283 = [l for l in g[ctl.LES].splitlines() if l.startswith("GATE S283 ")][0]
    g[ctl.LES] = (gate_s283 + "\n\n" + g[ctl.LES].replace(
        "## Gate\n\n",
        '## Gate\n\nGATE S999 receipt=.ufo/waves/round-41/fetch/missing.txt sha256=' + ('0'*64) + ' quote="uncited gate line"\n'
    ) + "\n## Outside\n\n" + gate_s283 + "\n")
    pocs.append(("POC12-gate-outside-section-and-uncited", "real", base, g))

    # PoC-13: Clause h second `own-work` cited row (held at BASE) with non-journal receipt
    base_h = dict(base)
    held_own_row = "| S055 | held own-work probe - .ufo/waves/round-40/fetch/probe.txt | own-work | A | scope | anchor | teaches | mined | 2026-10-24 | on-change | corpus/knowledge/old.md |"
    base_h[ctl.SRC] = base_h[ctl.SRC].replace(ctl.HELD_ROW, ctl.HELD_ROW + "\n" + held_own_row)
    g = dict(G)
    held_own_rev = held_own_row.replace("corpus/knowledge/old.md", "corpus/knowledge/old.md, " + ctl.ENTRY)
    g[ctl.SRC] = g[ctl.SRC].replace(
        ctl.HELD_ROW.replace("corpus/knowledge/old.md", "corpus/knowledge/old.md, " + ctl.ENTRY),
        ctl.HELD_ROW.replace("corpus/knowledge/old.md", "corpus/knowledge/old.md, " + ctl.ENTRY) + "\n" + held_own_rev
    )
    forged_own_bytes = ("invented second own-work receipt with zero journal lines " + ctl.FILLER).encode()
    g[ctl.FETCH + "S055-forged.txt"] = forged_own_bytes
    g[ctl.LES] = g[ctl.LES].replace(
        "## Gate\n\n",
        "## Gate\n\n" + ctl.gate_line("S055", ctl.FETCH + "S055-forged.txt", forged_own_bytes, "invented second own-work receipt") + "\n"
    )
    g[ctl.ENTRY] = g[ctl.ENTRY].replace(
        "source: S050 - held parser", "source: S050 - held parser\nsource: S055 - second own-work"
    ).replace(
        "**OBS** S050", "**OBS** S055 invented second own-work receipt.\n**OBS** S050"
    )
    pocs.append(("POC13-second-ownwork-held-row", "real", base_h, g))

    # PoC-14: Clause h provenance floor bypass (tool report header + 9999-99-99 dates + timezone UTC reversal + trailing boot)
    fake_j = "\n".join(
        ["MADO_GLOBALS_TOOL_REPORT v1 (NOT A JOURNAL)", "sessions=2"]
        + [f"9999-99-99T12:00:00+00:00 fakehost xdg-desktop-portal-hyprland[1]: [LOG]  | Got interface: iface_{k} (ver 1)" for k in range(20)]
        + [f"9999-99-99T12:00:00+05:00 fakehost xdg-desktop-portal-hyprland[2]: [LOG]  | Got interface: iface_{k} (ver 1)" for k in range(19)]
        + [f"9999-99-99T00:00:00+05:00 fakehost xdg-desktop-portal-hyprland[2]: [LOG]  | Got interface: {ctl.FG} (ver 1)"]
        + ["-- Boot 00000000000000000000000000000000 --"]
    ) + "\n"
    g = dict(G)
    ctl.set_receipt(g, "S289", "xdph-journal.txt", fake_j, f"Got interface: {ctl.FG} (ver 1)")
    ctl.rep(g, ctl.ENTRY, ctl.JLINE, "journal sessions=2 adverts=40 interfaces=20 focus_grab=1")
    pocs.append(("POC14-journal-provenance-floor-bypass", "fixed-patched", base, g))

    for name, mode, b_dict, a_dict in pocs:
        rc, verdict, cls = score_fixture(b_dict, a_dict, mode)
        print(f"poc={name:42s} scorer={mode:13s} rc={rc} {verdict} clauses={cls}")


if __name__ == "__main__":
    main()
