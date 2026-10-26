#!/usr/bin/env python3
"""ExecC2ExtraMutants: extra C2 controls (clause mutants + real-seeded forgeries).

Imports .ufo/waves/round-43/ctl/run-c2-controls.py (never its main()) and reuses its
helpers: base_files(), admitted(), score(), patched_counter(), rep(), row(),
set_receipt(), entry_line(), REAL/HELD_ROW/FILLER/CENSUS constants, line_of(), sha(),
blob(), commit_all().  No lane file is written; fixtures live under TMPDIR only.

Three scorers per control:
  real     quality/counters/c2-r43-gkeep-entry.py as frozen (PINS bind new ids)
  patched  the registered pin-patched copy (extra PINS appended; frozen keys win)
  pinfree  a copy whose whole PINS literal is rebuilt from the fixture's own receipts
           (so a defect *inside* a pinned receipt is reached by its own clause instead
           of being absorbed by the pin check)

Primary scorer per control: patched for paperwork mutants, pinfree for mutants whose
defect lives in a pinned receipt, real for the real-seeded forgeries.

Writes: results.md, survivors.md, run.log (stdout).
"""
import importlib.util
import json
import os
import re
import shutil
import sys

SCRATCH = "/fast/scratch/hyaku/mado-r43/ExecC2ExtraMutants"
os.makedirs(SCRATCH, exist_ok=True)
os.environ["TMPDIR"] = SCRATCH
SEAT = os.path.dirname(os.path.abspath(__file__))
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"

CTL = os.path.join(LANE, ".ufo/waves/round-43/ctl/run-c2-controls.py")
COUNTER = os.path.join(LANE, "quality/counters/c2-r43-gkeep-entry.py")


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ctl = load(CTL, "ctl43")
ctr = load(COUNTER, "ctr43")

ENTRY, SRC, LES, FETCH = ctl.ENTRY, ctl.SRC, ctl.LES, ctl.FETCH
REAL, ADMIT, REFUSE, FILLER = ctl.REAL, ctl.ADMIT, ctl.REFUSE, ctl.FILLER
HELD_ROW, HELD_Q = ctl.HELD_ROW, ctl.HELD_Q
base = ctl.base_files()
G = ctl.admitted()
Q = {i: REAL[i][3] for i in REAL}
EL = {i: ctl.entry_line(i) for i in REAL}


def rowof(i, **kw):
    kind = kw.pop("kind", REAL[i][1])
    return ctl.row(i, REAL[i][2], kind=kind, **kw)


def gate(i):
    return [l for l in G[LES].splitlines() if l.startswith("GATE %s " % i)][0]


def occ_lines(blob, quote):
    """1-based lines where the whitespace-collapsed quote starts (all occurrences)."""
    text, lines = ctr.collapse_with_lines(blob.decode("utf-8", "replace"))
    nq = re.sub(r"\s+", " ", quote)
    out, start = [], 0
    while True:
        k = text.find(nq, start)
        if k < 0:
            return out
        out.append(lines[k])
        start = k + 1


def conf(*repls):
    d = ctl.blob("host-gkeep.conf")
    for old, new in repls:
        assert old in d
        d = d.replace(old, new, 1)
    return d


def clients(fn):
    d = ctl.blob("host-clients-r43.json")
    return fn(d)


def append_before_close(d, chunk):
    tail = b"\n]\n"
    assert d.endswith(tail), d[-20:]
    return d[:-len(tail)] + chunk + tail


def entry_set(g, old, new):
    assert old in g[ENTRY], old[:60]
    g[ENTRY] = g[ENTRY].replace(old, new, 1)


CONTROLS = []


def control(name, primary, expect, should, why, fn, cls=None, evidence=()):
    CONTROLS.append(dict(name=name, primary=primary, expect=expect, should=should,
                         why=why, fn=fn, cls=cls, evidence=list(evidence)))


def m(name, should, why, fn, primary="patched", expect="kill", cls=None,
      evidence=()):
    control(name, primary, expect, should, why, fn, cls=cls, evidence=evidence)


# --------------------------------------------------------------- header window
def c01(g):
    entry_set(g, "verified-at: 2026-10-26",
              "\n".join("pad %d" % i for i in range(7)) + "\nverified-at: 2026-10-26")
m("CL01-verified-at-line-21", "b", "verified-at pushed to raw line 21", c01)


def c02(g):
    entry_set(g, "# The gkeep window geometry\n",
              "# The gkeep window geometry\n" + "\n".join("pad %d" % i for i in range(8)) + "\n")
m("CL02-source-S299-line-21", "b", "last source line pushed to raw line 21", c02)


def c03(g):
    entry_set(g, "recheck: 90d", "recheck: 90d\nrecheck: 30d")
m("CL03-two-recheck-lines", "b", "two recheck: lines in the window", c03)


def c04(g):
    entry_set(g, "source: S290 - receipt", "```\nsource: S290 - receipt\n```")
m("CL04-source-line-fenced", "b", "cited id's source line hidden in a fence", c04)


def c05(g):
    entry_set(g, "recheck: 90d", "recheck: 2026-13-01")
m("CL05-recheck-invalid-month", "b", "ISO-shaped but impossible date", c05)


def c06(g):
    entry_set(g, "verified-at: 2026-10-26",
              "verified-at: 2026-10-26\nverified-at: 2026-10-26")
m("CL06-two-verified-at", "b", "two verified-at: lines in the window", c06)


def c07(g):
    entry_set(g, "recheck: 90d", "source: S2900 - receipt\nrecheck: 90d")
    entry_set(g, "host rules", "**OBS** S2900 invented (Hyprland-Target.cpp:11).\nhost rules")
m("CL07-four-digit-id-no-row", "c", "S2900 cited with no registry row", c07)


# --------------------------------------------------------------- registry cells
def c08(g):
    ctl.rep(g, SRC, rowof("S291"), rowof("S291") + " extra |")
m("CL08-row-12-cells", "c", "registry row gains a twelfth cell", c08)


def c09(g):
    r = rowof("S291")
    ctl.rep(g, SRC, r, r.rsplit("|", 2)[0] + "|")
m("CL09-row-10-cells", "c", "registry row loses its used-by cell", c09)


def c10(g):
    ctl.rep(g, SRC, rowof("S291"), rowof("S291", status="Mined"))
m("CL10-status-case", "c", "status cell `Mined`", c10)


def c11(g):
    ctl.rep(g, SRC, rowof("S291"), rowof("S291", used=ENTRY.upper()))
m("CL11-usedby-case", "c", "used-by cell upper-cased", c11)


def c12(g):
    ctl.rep(g, SRC, "| teaches | mined | 2026-10-24", "| teaches | verified | 2026-10-24")
m("CL12-held-status-cell", "c", "held row's status cell rewritten", c12)


def c13(g):
    ctl.rep(g, SRC, rowof("S295"), rowof("S295", opened=""))
m("CL13-new-opened-empty", "c", "new row's opened cell emptied", c13)


def c14(g):
    ctl.rep(g, SRC, rowof("S295"), rowof("S295", recheck="90 days"))
m("CL14-new-recheck-unit", "c", "new row's recheck cell `90 days`", c14)


def c15(g):
    ctl.rep(g, SRC, rowof("S291"), "    " + rowof("S291"))
m("CL15-row-indented-4", "c", "row indented past the 0-3 space window", c15)


def c16(g):
    ctl.rep(g, SRC, rowof("S292"), rowof("S292") + "\n" + rowof("S292"))
m("CL16-row-duplicate", "c", "two registry rows for one id", c16)


# --------------------------------------------------------------- gate lines
def c17(g):
    ctl.rep(g, LES, 'quote="static_.size = expr;"', "quote='static_.size = expr;'")
m("CL17-gate-single-quoted", "d", "GATE quote in single quotes", c17)


def c18(g):
    s = ctl.sha(ctl.blob("Hyprland-DefaultFloatingAlgorithm.cpp"))
    ctl.rep(g, LES, "sha256=" + s, "sha256=" + s.upper())
m("CL18-gate-sha-uppercase", "d", "GATE sha256 upper-case hex", c18)


def c19(g):
    ctl.rep(g, LES, 'quote="m_box = box;"', 'quote="m_box = box;" extra')
m("CL19-gate-trailing-text", "d", "text after the closing quote", c19)


def c20(g):
    ctl.rep(g, LES, "receipt=" + FETCH + "Hyprland-Target.cpp",
            "receipt=/tmp/fetch/Hyprland-Target.cpp")
m("CL20-gate-absolute-path", "d", "GATE receipt names an absolute path", c20)


def c21(g):
    ctl.rep(g, LES, "receipt=" + FETCH + "Hyprland-Target.cpp",
            "receipt=" + FETCH + "sub/../Hyprland-Target.cpp")
m("CL21-gate-path-traversal", "d", "GATE path uses `sub/..` so it is not FETCH+name", c21)


def c22(g):
    ctl.rep(g, LES, 'quote="m_box = box;"', 'quote="m_box ="')
m("CL22-gate-quote-2-words", "d", "a 2-word quote (min is 3)", c22)


def c23(g):
    g[LES] = g[LES] + "\n## Notes\n\n" + gate("S293") + "\n"
m("CL23-gate-outside-section", "d", "a second GATE S293 line under `## Notes`", c23,
  cls="HOLE (low): the outside-section scan drops any line whose TEXT equals an "
      "in-section line (`line not in in_gate`), so a byte-identical GATE line under "
      "another heading is invisible to d. Only a differing outside line is counted.",
  evidence=[("Hyprland-Target.cpp", "m_box = box;")])


def c24(g):
    ctl.rep(g, LES, "GATE S291 ", "\tGATE S291 ")
m("CL24-gate-tab-indented", "d", "GATE line tab-indented", c24)


def c25(g):
    ctl.set_receipt(g, "S293", "Hyprland-Target.cpp",
                    b"m_box = box;\n" + b"z" * 180, "m_box = box;")
m("CL25-receipt-255-bytes", "d", "receipt under the 256-byte floor", c25)


def c26(g):
    ctl.rep(g, LES, gate("S293"), gate("S293") + "\n" + gate("S293"))
m("CL26-gate-two-lines-same-id", "d", "two GATE lines for one id", c26)


def c27(g):
    ctl.rep(g, LES, "receipt=" + FETCH + "Hyprland-Target.cpp",
            "receipt=.ufo/waves/round-42/fetch/Hyprland-Target.cpp")
m("CL27-gate-wrong-round-path", "d", "receipt in the round-42 fetch dir", c27)


def c28(g):
    s = ctl.sha(ctl.blob("Hyprland-Target.cpp"))
    ctl.rep(g, LES, ' sha256=%s quote="m_box = box;"' % s, " sha256=%s" % s)
m("CL28-gate-no-quote-key", "d", "GATE line without the quote= key", c28)


def c29(g):
    g[LES] = g[LES].replace("## Gate", "### Gate", 1)
m("CL29-gate-h3-section", "d", "Gate section is `### Gate`", c29)


def c30(g):
    entry_set(g, ctl.UI_LINE + "\n", "~~~\n" + ctl.UI_LINE + "\n~~~\n")
m("CL30-census-tilde-fence", "h", "UI census line inside a `~~~` fence", c30)


def c31(g):
    entry_set(g, EL["S293"], "```\n" + EL["S293"] + "\n```")
m("CL31-obs-line-fenced", "g", "S293 observation line fenced", c31)


def c32(g):
    ctl.rep(g, "corpus/README.md", "| `knowledge/hyprland",
            "  | `knowledge/hyprland")
m("CL32-readme-row-indented", "f", "index row starts with two spaces", c32)


def c33(g):
    g[LES] = g[LES].replace("## Gate", "## GATE", 1)
m("CL33-gate-section-uppercase", "d", "section titled `## GATE`", c33)


def c34(g):
    g["corpus/README.md"] += "| `knowledge/hyprland-gkeep-geometry-r43.md` | new |\n"
m("CL34-readme-duplicate-row", "f", "two index rows for the entry", c34)


# --------------------------------------------------------------- admit/refuse
def c35(g):
    ctl.rep(g, LES, " as " + ENTRY, " " + ENTRY)
m("CL35-admit-no-as", "i", "ADMIT without the `as` keyword", c35)


def c36(g):
    ctl.rep(g, LES, ctl.PKG + " as ", ctl.PKG + ".bak as ")
m("CL36-admit-path-not-md", "i", "ADMIT path ends `.md.bak`", c36)


def c37(g):
    ctl.rep(g, LES, REFUSE.split("reason=")[1], "superseded")
m("CL37-refuse-reason-short", "i", "REFUSE reason under 20 chars", c37)


def c38(g):
    ctl.rep(g, LES, REFUSE.split("reason=")[1],
            "alpha alpha alpha beta beta beta beta")
m("CL38-refuse-3-distinct", "i", "REFUSE reason with 2 distinct words", c38)


def c39(g):
    ctl.rep(g, LES, ctl.PKG2, "/tmp/gkeep-geometry-unobservable-r8.md")
m("CL39-refuse-foreign-path", "i", "REFUSE names a staged basename outside merge/mado",
  c39, expect="admit",
  cls="HOLE (low): clause i tests os.path.basename() only, so a foreign path with a "
      "staged basename is accepted; the docstring's residual list does not declare it.",
  evidence=[("LESSON", "REFUSE /tmp/gkeep-geometry-unobservable-r8.md reason=")])


def c40(g):
    ctl.rep(g, LES, ctl.PKG + " as ", "/tmp/gkeep-size-to-real-size-r11.md as ")
m("CL40-admit-foreign-path", "i", "ADMIT names a staged basename outside merge/mado",
  c40, expect="admit",
  cls="HOLE (low): same basename-only test on the ADMIT target; a file outside the "
      "package is accepted as the admitted staged file.",
  evidence=[("LESSON", "ADMIT /tmp/gkeep-size-to-real-size-r11.md as")])


def c41(g):
    ctl.rep(g, LES, "REFUSE " + ctl.PKG2, "REFUSE\t" + ctl.PKG2)
m("CL41-refuse-tab-separated", "i", "REFUSE tab-separated", c41)


def c42(g):
    ctl.rep(g, LES, "## Gate\n\n", "")
m("CL42-gate-section-missing", "d", "lesson has no `## Gate` section", c42)


# --------------------------------------------------------------- census lines
def c43(g):
    fake = append_before_close(clients(lambda d: d),
                               b',\n {\n  "mapped": true,\n  "class": "zcode",\n'
                               b'  "floating": false\n }\n')
    ctl.set_receipt(g, "S298", "host-clients-r43.json", fake)
m("CL43-census-extra-mapped-client", "h", "a fifth mapped client, census line stale",
  c43, primary="pinfree")


def c44(g):
    fake = b'{"clients": ' + clients(lambda d: d) + b'}'
    ctl.set_receipt(g, "S298", "host-clients-r43.json", fake)
m("CL44-census-json-object-not-list", "h", "JSON object instead of a list", c44,
  primary="pinfree")


def c45(g):
    fake = clients(lambda d: d.replace(b'"class": "zcode"',
                                       b'"class": "org.omarchy.gkeep"', 1))
    ctl.set_receipt(g, "S298", "host-clients-r43.json", fake)
m("CL45-census-hidden-gkeep-client", "h", "a live client whose class matches RX (gkeep=1)",
  c45, primary="pinfree")


def c46(g):
    fake = conf((b"size 420 500, match:class ^(org.omarchy.gkeep)$\n",
                 b"size 420 500, match:class ^(org.omarchy.gkeep)$\n"
                 b"windowrule = float on, match:class ^(org.omarchy.gkeep)$\n"))
    ctl.set_receipt(g, "S297", "host-gkeep.conf", fake)
m("CL46-census-two-float-rules", "h", "two float rules -> parser refuses", c46,
  primary="pinfree")


def c47(g):
    fake = conf((b"windowrule = float on,", b"windowrule = float off,"))
    ctl.set_receipt(g, "S297", "host-gkeep.conf", fake)
m("CL47-census-float-off", "h", "float rule off while the census line says on", c47,
  primary="pinfree")


def c48(g):
    ctl.rep(g, SRC, rowof("S295"), rowof("S295", kind="own-work"))
m("CL48-census-fourth-own-work", "h", "a fourth own-work row", c48)


def c49(g):
    fake = ctl.blob("gkeep-ui-excerpt.py") + b'\napplication_id="org.omarchy.gkeep"\n'
    ctl.set_receipt(g, "S299", "gkeep-ui-excerpt.py", fake)
m("CL49-census-second-app-id", "h", "two application_id= calls in the excerpt", c49,
  primary="pinfree")


def c50(g):
    fake = ctl.blob("gkeep-ui-excerpt.py") + b"\nwindow.set_default_size(1, 1)\n"
    ctl.set_receipt(g, "S299", "gkeep-ui-excerpt.py", fake)
m("CL50-census-second-default-size", "h", "two set_default_size calls in the excerpt",
  c50, primary="pinfree")


def c51(g):
    fake = append_before_close(clients(lambda d: d), b",\n 5\n")
    ctl.set_receipt(g, "S298", "host-clients-r43.json", fake)
m("CL51-census-json-nondict", "h", "a non-object element in the client list", c51,
  primary="pinfree")


def c52(g):
    fake = conf((b"size 420 500, match:class ^(org.omarchy.gkeep)$\n",
                 b"size 420 500, match:class ^(org.omarchy.gkeep)$\n"
                 b"windowrule = center on, match:class ^(org.omarchy.gkeep)$\n"))
    ctl.set_receipt(g, "S297", "host-gkeep.conf", fake)
m("CL52-census-two-center-rules", "h", "two center rules -> parser refuses", c52,
  primary="pinfree")


def c63(g):
    stale = ctl.gate_line("S293", FETCH + "Hyprland-Target.cpp",
                          ctl.blob("Hyprland-Target.cpp"), "m_box = box;")
    assert stale == gate("S293")
    other = ctl.gate_line("S293", ".ufo/waves/round-42/fetch/Hyprland-Target.cpp",
                          b"x" * 300, "stale second line")
    g[LES] = g[LES] + "\n## Notes\n\n" + other + "\n"
m("CL63-gate-outside-section-differing", "d",
  "a second, DIFFERING GATE S293 line under `## Notes`", c63,
  evidence=[("Hyprland-Target.cpp", "m_box = box;")])


def c64(g):
    g.pop(ENTRY)
m("CL64-entry-absent-at-rev", "a", "the entry file is missing at REV", c64,
  cls="covered, cannot be isolated: absence of the entry makes b-i fail too "
      "(the registered N01-no-entry is the same shape).")


# --------------------------------------------------------------- clause e
def c53(g):
    ctl.rep(g, SRC, REAL["S291"][2], "https://example.org/src/rule/Other.cpp")
m("CL53-loc-component-unrelated", "e", "location component unrelated to receipt name", c53)


def c54(g):
    ctl.rep(g, SRC, REAL["S294"][2], REAL["S293"][2])
m("CL54-two-rows-one-location", "e", "S294 row reuses S293's location", c54)


# --------------------------------------------------------------- clause g / boundary
def c55(g):
    ctl.set_receipt(g, "S293", "Hyprland-Target.cpp", ctl.blob("Hyprland-Target.cpp"),
                    "m_box = box")
    entry_set(g, EL["S293"], "**OBS** S293 m_box = box (Hyprland-Target.cpp:11).")
m("CL55-quote-truncated-at-punctuation", "d",
  "quote stops before the `;` (word boundary is still valid)", c55, expect="admit",
  cls="LEGITIMATE (no clause should kill it): d's rule is a word-boundary rule; the "
      "quote ends with a word char followed by `;`, so 3-25 words and word-bounded. "
      "The semantic residue is claim binding (declared residual).",
  evidence=[("Hyprland-Target.cpp", "m_box = box")])


def c56(g):
    b = ctl.blob("Hyprland-Target.cpp")
    fake = b + b"\nZZ second occurrence follows\nm_box = box;\n"
    lines = occ_lines(fake, Q["S293"])
    assert len(lines) >= 2 and lines[0] != lines[1], lines
    ctl.set_receipt(g, "S293", "Hyprland-Target.cpp", fake)
    entry_set(g, EL["S293"],
              "**OBS** S293 m_box = box; (Hyprland-Target.cpp:%d)." % lines[1])
m("CL56-locator-second-occurrence", "g", "locator names the 2nd occurrence, not the 1st",
  c56, primary="pinfree")


def c57(g):
    fake = ctl.blob("Hyprland-Target.cpp").replace(b"m_box = box;", b"9m_box = box;", 1)
    ctl.set_receipt(g, "S293", "Hyprland-Target.cpp", fake)
m("CL57-quote-preceded-by-digit", "d", "quote starts after a digit", c57,
  primary="pinfree")


def c58(g):
    fake = ctl.blob("Hyprland-Target.cpp").replace(b"m_box = box;", b"_m_box = box;", 1)
    ctl.set_receipt(g, "S293", "Hyprland-Target.cpp", fake)
m("CL58-quote-preceded-by-underscore", "d", "quote starts after an underscore", c58,
  primary="pinfree")


def c59(g):
    fake = ctl.blob("Hyprland-Target.cpp").replace(b"m_box = box;", b"m_box = box9;", 1)
    ctl.set_receipt(g, "S293", "Hyprland-Target.cpp", fake, "m_box = box")
    entry_set(g, EL["S293"], "**OBS** S293 m_box = box (Hyprland-Target.cpp:11).")
m("CL59-quote-followed-by-digit", "d", "quote ends before a digit", c59,
  primary="pinfree")


def c60(g):
    q1, q2 = "alpha beta gamma", "alpha beta gamma delta epsilon"
    ctl.set_receipt(g, "S293", "Hyprland-Target.cpp",
                    b"zzz " + q2.encode() + b"\n" + FILLER.encode(), q1)
    ctl.set_receipt(g, "S294", "Hyprland-WindowTarget.cpp",
                    b"zzz " + q2.encode() + b"\n" + FILLER.encode(), q2)
    entry_set(g, EL["S293"], "**OBS** S293 %s (Hyprland-Target.cpp:1)." % q1)
    entry_set(g, EL["S294"], "**OBS** S294 %s (Hyprland-WindowTarget.cpp:1)." % q2)
m("CL60-quote-prefix-of-longer", "d", "one quote is a prefix of another id's quote", c60,
  primary="pinfree")


def c61(g):
    ctl.set_receipt(g, "S293", "Hyprland-Target.cpp", ctl.blob("Hyprland-Target.cpp"),
                    "m_box = box;.")
m("CL61-quote-plus-period", "d", "quote carries a period the receipt lacks", c61)


# --------------------------------------------------------------- id alphabet
def c62(g):
    entry_set(g, "recheck: 90d", "source: S99 - two-digit id\nrecheck: 90d")
    entry_set(g, "host rules", "**OBS** S99 an unregistered two-digit citation.\nhost rules")
m("CL62-two-digit-id-invisible", "b",
  "source: S99 and an OBS S99 are invisible to every id regex", c62, expect="admit",
  cls="HOLE (low): SRC_RE, the ghost scan, ROW_RE and GATE_RE all require 3+ digits, "
      "so an S99 citation and its source line are neither counted nor rejected; the "
      "entry is admitted carrying an unregistered citation.",
  evidence=[("ENTRY", "source: S99 - two-digit id")])


# --------------------------------------------------------------- real-seeded forgeries
def r01(g):
    entry_set(g, EL["S296"],
              "**OBS** S296 the size hyprctl prints is the window's current size "
              '"size": [{}, {}], (Hyprland-HyprCtl.cpp:395).')
m("R01-real-quote-unsupported-size-claim", "g",
  "pinned HyprCtl format quote offered as proof of the reported value", r01,
  primary="real", expect="admit",
  cls="RESIDUAL (declared): the docstring's last paragraph declares that a real "
      "receipt can be cited for a claim it does not support; binding claim to quote "
      "is the non-author closure's job.",
  evidence=[("Hyprland-HyprCtl.cpp", '"size": [{}, {}],')])


def r02(g):
    ent = g[ENTRY]
    if not ent.endswith("\n"):
        ent += "\n"
    g[ENTRY] = ent
    entry_set(g, "verified-at: 2026-10-26", "source: S300 - copy\nverified-at: 2026-10-26")
    entry_set(g, "host rules",
              "**OBS** S300 %s (Hyprland-WindowTarget.cpp:70).\nhost rules" % Q["S294"])
    ctl.rep(g, SRC, rowof("S294") + "\n",
            rowof("S294") + "\n" + ctl.row("S300", "https://example.org/copy/WindowTarget.cpp") + "\n")
    g[LES] = g[LES].replace("\n## Gate\n\n",
                            "\n## Gate\n\n" + ctl.gate_line("S300", FETCH + "Hyprland-WindowTarget.cpp",
                                                           ctl.blob("Hyprland-WindowTarget.cpp"),
                                                           Q["S294"]) + "\n", 1)
m("R02-real-quote-reused-two-ids", "d",
  "S294's real quote+receipt re-gated for a second id", r02, primary="real")


def r03(g):
    entry_set(g, "(Hyprland-Target.cpp:11)", "(Hyprland-Target.cpp:12)")
m("R03-real-quote-wrong-locator", "g", "real quote, locator off by one line", r03,
  primary="real")


def r04(g):
    entry_set(g, "(Hyprland-WindowRuleApplicator.cpp:426)",
              "(Hyprland-Target.cpp:426)")
m("R04-real-quote-other-file-locator", "g", "real quote, locator names another receipt",
  r04, primary="real")


def r05(g):
    entry_set(g, EL["S298"],
              "**OBS** S298 chromium is the only client that can match the gkeep rule "
              '"mapped": true, "class": "chromium", "floating": false, '
              "(host-clients-r43.json:49).")
m("R05-real-quote-exclusivity-claim", "g",
  "real client dump quote offered as proof of exclusivity", r05, primary="real",
  expect="admit",
  cls="RESIDUAL (declared): same claim-to-quote hole; the census line itself stays "
      "honest, only the prose claim is unsupported.",
  evidence=[("host-clients-r43.json",
             '"mapped": true, "class": "chromium", "floating": false,')])


def r06(g):
    entry_set(g, EL["S295"],
              "**OBS** S295 hyprctl's size is the current animated value "
              "*m_realSize = x.size(); (Hyprland-GeometricMovableAnimated.cpp:45).")
m("R06-real-quote-current-value-claim", "g",
  "real assignment quote offered as proof of the reported field", r06, primary="real",
  expect="admit",
  cls="RESIDUAL (declared): the quote shows the assignment into the animated "
      "variable, not that hyprctl reads the current value.",
  evidence=[("Hyprland-GeometricMovableAnimated.cpp", "*m_realSize = x.size();")])


def r07(g):
    ctl.rep(g, SRC, REAL["S296"][2],
            "merge/mado/knowledge/corpus/knowledge/gkeep-observation-route-r11.md")
m("R07-real-quote-staged-row-location", "e",
  "row claims a staged package file while the gate cites the pinned cpp", r07,
  primary="real")


def r08(g):
    ctl.set_receipt(g, "S050", "S050.txt",
                    b"invented held source. " + FILLER.encode(), "invented held source")
    entry_set(g, "**OBS** S050 %s (S050.txt:1)." % HELD_Q,
              "**OBS** S050 invented held source (S050.txt:1).")
m("R08-held-id-invented-receipt", "d",
  "held id S050 cites a receipt nobody pinned, invented inside the fixture", r08,
  primary="real", expect="admit",
  cls="RESIDUAL (declared): the docstring declares 'a held id's receipt is not "
      "pinned'; any held-id receipt bytes pass d.",
  evidence=[("S050.txt", "invented held source")])


# --------------------------------------------------------------- runner
PIN_RE = re.compile(r"PINS = \{.*?\n\}\n", re.S)


def pinfree_counter(dest, files):
    src = open(COUNTER).read()
    m_ = PIN_RE.search(src)
    assert m_, "PINS literal not found"
    rows = "".join('    "%s": "%s",\n' % (os.path.basename(k), ctl.sha(v))
                   for k, v in files.items()
                   if k.startswith(FETCH) and not isinstance(v, bool))
    out = src[:m_.start()] + "PINS = {\n" + rows + "}\n" + src[m_.end():]
    open(os.path.join(dest, "c2-pinfree.py"), "w").write(out)
    return os.path.join(dest, "c2-pinfree.py")


REGISTERED_PATCHED = ctl.patched_counter


def run(files_after, scorer):
    if scorer == "pinfree":
        ctl.patched_counter = pinfree_counter
        try:
            return ctl.score(base, files_after, "patched")
        finally:
            ctl.patched_counter = REGISTERED_PATCHED
    return ctl.score(base, files_after, scorer)


def admitted(last):
    return "admitted=1/1" in last


def verify_evidence(evidence, fixture):
    """Return 'target:line' for a quote that really occurs in the named bytes."""
    out = []
    for target, quote in evidence:
        if target in ("LESSON", "ENTRY"):
            body = fixture[LES if target == "LESSON" else ENTRY]
            assert quote in body, (target, quote)
            out.append("%s (fixture line)" % target.lower())
            continue
        path = os.path.join(ctl.FETCHDIR, target)
        if not os.path.exists(path):
            out.append("%s (fixture-local, not a pinned receipt)" % target)
            continue
        blob = open(path, "rb").read()
        line = ctr.quote_at(blob, quote)
        assert line is not None, (target, quote)
        out.append("%s:%d" % (target, line))
    return "; ".join(out)


def main():
    rows = []
    anchors = True
    print("CTL_C2X: source=%s lane=%s" % (CTL, ctl.LANE))
    for kind in ("real", "patched"):
        rc, last, cl = run(G, kind)
        good = rc == 0 and admitted(last)
        anchors &= good
        print("control=P-%s expected=admitted=1/1 observed=%s clauses=%s ok=%d"
              % (kind, last.split(" verdict")[0], cl, good))
    fixtures = {}
    for c in CONTROLS:
        obs = {}
        fixture = ctl_copy(c["fn"])
        fixtures[c["name"]] = fixture
        for scorer in ("real", "patched", "pinfree"):
            rc, last, cl = run(fixture, scorer)
            obs[scorer] = (rc, admitted(last), cl)
            print("RUN control=%s scorer=%s primary=%d rc=%d admitted=%d clauses=%s"
                  % (c["name"], scorer, scorer == c["primary"], rc,
                     obs[scorer][1], cl))
        p_rc, p_adm, p_cl = obs[c["primary"]]
        rows.append(dict(name=c["name"], primary=c["primary"], expect=c["expect"],
                         should=c["should"], why=c["why"], got=p_adm,
                         clauses=p_cl, rc=p_rc, cls=c["cls"],
                         ev=verify_evidence(c["evidence"], fixture),
                         adm={k: v[1] for k, v in obs.items()}))
        print("CTRL control=%s expect=%s got=%s should_clause=%s evidence=%s"
              % (c["name"], c["expect"], "admit" if p_adm else "reject",
                 c["should"], rows[-1]["ev"] or "-"))
    surprises = [r for r in rows if (r["got"] != (r["expect"] == "admit"))]
    unexplained = [r for r in surprises if not r["cls"]]
    with open(os.path.join(SEAT, "results.md"), "w") as fh:
        fh.write("# C2 extra controls - observed verdicts\n\n")
        fh.write("Primary scorer per control: patched for paperwork mutants, pinfree "
                 "for defects inside a pinned receipt, real for the real-seeded "
                 "forgeries. `a/p/f` = admitted flag under real/patched/pinfree.\n\n")
        fh.write("| control | primary | expected | observed | a/p/f | clause vector "
                 "(primary) | clause that should kill |\n")
        fh.write("|---|---|---|---|---|---|---|\n")
        for r in rows:
            fh.write("| %s | %s | %s | %s | %d/%d/%d | %s | %s |\n" % (
                r["name"], r["primary"], r["expect"],
                "ADMITTED" if r["got"] else "rejected",
                r["adm"]["real"], r["adm"]["patched"], r["adm"]["pinfree"],
                r["clauses"], r["should"]))
        fh.write("\n## surprises (prediction != observation)\n\n")
        for r in surprises:
            fh.write("- **%s** predicted %s, observed %s: %s\n"
                     % (r["name"], r["expect"],
                        "ADMITTED" if r["got"] else "rejected", r["cls"]))
        if not surprises:
            fh.write("none\n")
    surv = [r for r in rows if r["got"]]
    with open(os.path.join(SEAT, "survivors.md"), "w") as fh:
        fh.write(SURVIVORS_HEAD)
        for r in surv:
            na = ("yes - declared residual"
                  if (r["cls"] or "").startswith("RESIDUAL")
                  else "no - the failing check is the counter's own"
                  if (r["cls"] or "").startswith("HOLE")
                  else "not applicable")
            fh.write("| %s | %s | `%s` | %s | %s | %s | %s |\n" % (
                r["name"], r["primary"], r["clauses"], r["should"], na,
                r["cls"] or "UNCLASSIFIED", r["ev"] or "-"))
        fh.write("\n")
    print("CTL_C2X: controls=%d survivors=%d rejected=%d surprises=%d unexplained=%d"
          % (len(rows), len(surv), len(rows) - len(surv), len(surprises),
             len(unexplained)))
    good = anchors and not unexplained and len(rows) >= 40
    print("CTL_C2X VERDICT: %s" % ("PASS" if good else "FAIL"))
    return 0 if good else 1


def ctl_copy(fn):
    """a fresh fixture dict per run (helpers mutate in place)"""
    g = dict(G)
    fn(g)
    return g


SURVIVORS_HEAD = """# C2 survivors - controls the counter ADMITS

Every row was built on the registered genuine fixture (`run-c2-controls.py::admitted()`)
and scored with that module's `score()` under the three scorers in `harness.py`
(`real` = the frozen counter, `patched` = the registered pin-patched copy, `pinfree` =
supplementary copy whose whole PINS literal is rebuilt so a defect inside a pinned
receipt is reached by its own clause). A survivor is a control whose defect survives:
the counter reports `admitted=1/1` under its primary scorer.

Classification key:
- **RESIDUAL (declared)** - the predicate's docstring already declares this hole;
  binding the claim to the quote is the non-author closure's job, not the counter's.
- **HOLE** - not declared in the docstring; the clause that should kill the control
  does not. Severity is judged by what the hole lets land.
- **LEGITIMATE** - no clause should kill it; the control satisfies the contract.

Evidence column: a source quote is `receipt:line`, re-verified by this harness with the
counter's own `quote_at()` against the pinned `fetch/` bytes; `fixture line` marks a
generated fixture line, `fixture-local` a receipt the fixture invents (held id).

| control | scorer | clause vector | clause that should kill it | claim-to-quote binding is a non-author job? | classification | verified evidence |
|---|---|---|---|---|---|---|
"""


if __name__ == "__main__":
    sys.exit(main())
