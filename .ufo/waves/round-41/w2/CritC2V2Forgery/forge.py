#!/usr/bin/env python3
"""CritC2V2Forgery (w2): forgeries against PRED-C2-r41-v2.

Fixture repos are built exactly as `.ufo/waves/round-41/ctl/run-c2-v2-controls.py`
builds them: the frozen control module is imported read-only, its genuine fixture
`admitted()` is the starting point, and each forgery is a dict mutation of it.
The scorer is the counter as frozen at the DATA commit 07f2641 (byte-identical to
the v2 reference), extracted to a scratch copy; PINS bind every NEW id's receipt.

Read-only: nothing in the lane is written.  Output goes to stdout.
"""
import hashlib
import importlib.util
import os
import re
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
CTL = LANE + "/.ufo/waves/round-41/ctl/run-c2-v2-controls.py"
COUNTER = "/tmp/tmp.sBh6GeCxAU/c2-v2.py"   # git show 07f2641:quality/counters/c2-r41-focus-entry-v2.py
DATA = "07f2641696b5ac73de1404ea737a9f27e9819aa1"
BASE = "ab2bfaab661c846d1de9d58c01651cd156a13949"


def load_ctl():
    spec = importlib.util.spec_from_file_location("ctl_c2v2", CTL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.COUNTER = COUNTER
    return mod


ctl = load_ctl()
SRC, LES, ENTRY, FETCH = ctl.SRC, ctl.LES, ctl.ENTRY, ctl.FETCH
REAL, HELD_Q, FILLER, JLINE = ctl.REAL, ctl.HELD_Q, ctl.FILLER, ctl.JLINE
base_files, admitted, score, rep, row, sha, blob = (
    ctl.base_files, ctl.admitted, ctl.score, ctl.rep, ctl.row, ctl.sha, ctl.blob)


def gate(g, i):
    return [l for l in g[LES].splitlines() if l.startswith("GATE %s " % i)][0]


def set_receipt(g, i, fn, data, quote=None):
    return ctl.set_receipt(g, i, fn, data, quote)


# --------------------------------------------------------------------------
# the forgeries.  each takes the genuine fixture g and mutates it.
# --------------------------------------------------------------------------
JP = ("Hyprland の フォーカス グラブ ホワイトリスト\n\n"
      "この記事は日本語で書かれた解説です。コンポジタはクライアントのサーフェス集合に"
      "フォーカスを制限します。日本語のドキュメントは PROVINCE.md の範囲外です。\n"
      "フォーカス グラブ ホワイトリスト は Hyprland の独自プロトコルです。\n")


def fa_xml_quote_as_compositor(g):
    """A quote lifted from the protocol XML, cited as what Hyprland 0.56.2 does."""
    q = REAL["S283"][3]
    rep(g, ENTRY, "**OBS** S283 %s." % q,
        '**OBS** S283 Hyprland 0.56.2 clears the whitelist at the seat whenever '
        'input falls outside it: "%s".' % q)


def fb_true_quote_false_inference(g):
    """A true quote from the portal's log call, on an inference it does not support."""
    q = REAL["S286"][3]
    rep(g, ENTRY, "**OBS** S286 %s." % q,
        '**OBS** S286 the portal binds the focus-grab manager and routes every '
        'grab through it: "%s".' % q)


def fc_swap_naive(g):
    """S283 and S284 swap receipts, locations and quotes; the source-line prose
    still says S283 is the protocol XML.  Identity swap, internally consistent
    for every clause-e binding."""
    a, b = "S283", "S284"
    ra = row(a, REAL[a][2], kind=REAL[a][1])
    rb = row(b, REAL[b][2], kind=REAL[b][1])
    na = row(a, REAL[b][2], kind=REAL[b][1])
    nb = row(b, REAL[a][2], kind=REAL[a][1])
    g[SRC] = g[SRC].replace(ra, "@@ROW-A@@").replace(rb, "@@ROW-B@@") \
                   .replace("@@ROW-A@@", na).replace("@@ROW-B@@", nb)
    qa, qb = REAL[a][3], REAL[b][3]
    ga = gate(g, a)
    gb = gate(g, b)
    new_a = ctl.gate_line(a, FETCH + REAL[b][0], blob(REAL[b][0]), qb)
    new_b = ctl.gate_line(b, FETCH + REAL[a][0], blob(REAL[a][0]), qa)
    g[LES] = g[LES].replace(ga, "@@GATE-A@@").replace(gb, new_a).replace("@@GATE-A@@", new_b)
    g[ENTRY] = (g[ENTRY]
                .replace("**OBS** %s %s." % (a, qa), "@@E-A@@")
                .replace("**OBS** %s %s." % (b, qb), "**OBS** %s %s." % (b, qa))
                .replace("@@E-A@@", "**OBS** %s %s." % (a, qb)))


def fc2_swap_consistent(g):
    """The same swap with the source-line prose swapped too, so the id->receipt
    naming is internally consistent: nothing but an external id authority can
    tell S283 from S284."""
    fc_swap_naive(g)
    rep(g, ENTRY, "source: S283 - protocol xml", "@@S-A@@")
    rep(g, ENTRY, "source: S284 - compositor", "source: S283 - compositor")
    rep(g, ENTRY, "@@S-A@@", "source: S284 - protocol xml")


def fd_admit_wrong_staged(g):
    """ADMIT names a staged focus-theme file that has nothing to do with the
    entry: mouse-target-r11 instead of the protocol-live-on-host-r14 draft."""
    rep(g, LES, ctl.ADMIT,
        "ADMIT merge/mado/knowledge/corpus/knowledge/focus-grab-mouse-target-r11.md"
        " as " + ENTRY)


def fe_ninety_percent_prose(g):
    """Every cited id keeps its one quote-bearing line; 90 invented lines of
    uncited prose are added around them."""
    lines = []
    for k in range(90):
        lines.append("The seat manager forwards pointer motion %d to the grab's "
                     "owner and never to a non-member surface." % k)
    g[ENTRY] = g[ENTRY].replace(JLINE, "\n".join(lines) + "\n" + JLINE)


def ff_localized_rehost(g):
    """Localized (Japanese) material re-hosted under the held row's neutral URL:
    the row keeps https://example.org/config.cpp, the receipt bytes are Japanese."""
    body = JP + "\n" + FILLER
    set_receipt(g, "S050", "S050.txt", body, "フォーカス グラブ ホワイトリスト")
    rep(g, ENTRY, "**OBS** S050 %s." % HELD_Q,
        "**OBS** S050 the localized upstream documentation states: "
        "フォーカス グラブ ホワイトリスト は 独自 の プロトコル です")


def fg_fabricated_held_receipt(g):
    """A held id's receipt invented from scratch (held ids are not pinned): the
    entry cites a claim the source never made."""
    q = "the portal now binds hyprland_focus_grab_manager_v1 for every client"
    body = "Release notes for the portal. %s. %s\n" % (q, FILLER)
    set_receipt(g, "S050", "S050.txt", body, q)
    rep(g, ENTRY, "**OBS** S050 %s." % HELD_Q, "**OBS** S050 %s." % q)


def fh_pinned_journal_unsupported(g):
    """The pinned own-work journal is cited for a claim it does not support; only
    the census line is checked, the prose about the journal is not."""
    g[ENTRY] = g[ENTRY].replace(
        JLINE,
        "**OBS** S289 both portal sessions advertise hyprland_focus_grab_manager_v1 "
        "once each, and the first session carries the interface at version 1.\n" + JLINE)


def fg2_ghost_token(g):
    """An invented citation in plain sight that the ghost scan cannot see."""
    g[ENTRY] = g[ENTRY].replace(
        JLINE, "**OBS** S999a the seat manager forwards pointer motion.\n" + JLINE)


def nf1_invented_new_receipt(g):
    """NEGATIVE: an invented receipt for a PINNED new id (expected: clause d)."""
    body = ("invented protocol text with a quotable sentence " + FILLER).encode()
    set_receipt(g, "S283", "focus-grab-v1.xml", body,
                "invented protocol text with a quotable sentence")
    rep(g, ENTRY, "**OBS** S283 %s." % REAL["S283"][3],
        "**OBS** S283 invented protocol text with a quotable sentence.")


def nf2_quote_from_other_receipt(g):
    """NEGATIVE: S283's Gate quote taken from S284's receipt (expected: clause d)."""
    set_receipt(g, "S283", "focus-grab-v1.xml", blob("focus-grab-v1.xml"),
                REAL["S284"][3])
    rep(g, ENTRY, "**OBS** S283 %s." % REAL["S283"][3],
        "**OBS** S283 %s." % REAL["S284"][3])


def nf3_shared_receipt(g):
    """NEGATIVE: two cited ids share one receipt path (expected: clause d)."""
    g[FETCH + "focus-grab-v1.xml"] = blob("Hyprland-FocusGrab.cpp")
    set_receipt(g, "S283", "focus-grab-v1.xml", blob("Hyprland-FocusGrab.cpp"),
                REAL["S284"][3])
    rep(g, ENTRY, "**OBS** S283 %s." % REAL["S283"][3],
        "**OBS** S283 %s." % REAL["S284"][3])


NEGATIVES = [
    ("NF1-invented-new-id-receipt", nf1_invented_new_receipt),
    ("NF2-quote-from-other-receipt", nf2_quote_from_other_receipt),
    ("NF3-two-ids-share-receipt", nf3_shared_receipt),
]

FORGERIES = [
    ("FA-xml-quote-as-compositor-behaviour", fa_xml_quote_as_compositor,
     "quote-to-claim binding (declared residual)"),
    ("FB-true-quote-false-inference", fb_true_quote_false_inference,
     "quote-to-claim binding (declared residual)"),
    ("FC-swap-ids-naive", fc_swap_naive, "no clause; clause-e naming survives"),
    ("FC2-swap-ids-consistent", fc2_swap_consistent, "no clause"),
    ("FD-admit-wrong-staged-file", fd_admit_wrong_staged, "clause i (staged allowlist only)"),
    ("FE-ninety-percent-prose", fe_ninety_percent_prose, "no clause (volume/ratio)"),
    ("FF-localized-rehost-held", ff_localized_rehost, "clause i BAD_LOC (rows only)"),
    ("FG-fabricated-held-receipt", fg_fabricated_held_receipt, "clause d pins (NEW ids only)"),
    ("FH-pinned-journal-unsupported-claim", fh_pinned_journal_unsupported, "clause h (census line only)"),
    ("FG2-ghost-token-S999a", fg2_ghost_token, "clause b ghost scan"),
]


# --------------------------------------------------------------------------
# proposed tightenings, as pure checkers over a fixture's file dict
# --------------------------------------------------------------------------
def unfenced(text):
    out, fenced = [], False
    for line in text.splitlines():
        if re.match(r"^\s{0,3}(```|~~~)", line):
            fenced = not fenced
            continue
        if not fenced:
            out.append(line)
    return out


def rows_of(src_text):
    out = {}
    inside = False
    for line in src_text.splitlines():
        if line.startswith("## "):
            inside = line.strip() == "## Registry"
            continue
        if inside:
            m = re.match(r"^ {0,3}\|\s*(S\d{3,})\s*\|", line)
            if m:
                out[m.group(1)] = [c.strip() for c in line.strip().split("|")[1:-1]]
    return out


def cited_ids(entry_text):
    ids = []
    for line in unfenced(entry_text)[:20]:
        m = re.match(r"^source:\s*(S\d{3,})\b", line)
        if m and m.group(1) not in ids:
            ids.append(m.group(1))
    return ids


def t1_source_line_names_receipt(files, label):
    """T1: each `source: S### - text` header line must name its id's receipt
    basename or the last path component of the id's registry location."""
    dec = lambda v: v.decode("utf-8", "replace") if isinstance(v, bytes) else v
    entry, src, les = dec(files[ENTRY]), dec(files[SRC]), dec(files[LES])
    reg = rows_of(src)
    gates = {m.group(1): m.group(2) for m in
             (re.match(r'^GATE (S\d{3,}) receipt=(\S+) ', l)
              for l in les.splitlines()) if m}
    bad = []
    for i in cited_ids(entry):
        line = [l for l in unfenced(entry)[:20] if l.startswith("source: %s " % i)][0]
        prose = line.split(" - ", 1)[1].lower() if " - " in line else line.lower()
        rb = os.path.basename(gates.get(i, "")).lower()
        loc = reg.get(i, [""] * 2)[1].split()[-1] if len(reg.get(i, [])) == 11 else ""
        comp = re.split(r"[?#]", loc)[0].rstrip("/").rsplit("/", 1)[-1].lower()
        if not (rb and rb in prose) and not (comp and comp in prose):
            bad.append((i, prose[:40], rb, comp))
    print("T1 %-38s cited=%d failing=%d %s" % (
        label, len(cited_ids(entry)), len(bad), bad[:4]))
    return not bad


BAD_LOC = ctl.__dict__.get("BAD_LOC") or (
    "amgsk.dev", "zhihu", "/zh", "/ja", "zenn.dev", "qiita.com", "/jp/",
    "/cn/", "t.co/", "bit.ly", "\u65e5\u672c", "\u4e2d\u6587")


def cjk(text):
    return sum(1 for ch in text if
               0x3040 <= ord(ch) <= 0x30FF or 0x3400 <= ord(ch) <= 0x4DBF
               or 0x4E00 <= ord(ch) <= 0x9FFF or 0xFF66 <= ord(ch) <= 0xFF9F)


def t3_receipt_not_localized(files, label):
    """T3: no cited receipt's own bytes may carry a BAD_LOC marker or CJK text
    (the localized channel is outside PROVINCE.md)."""
    les = files[LES]
    bad = []
    for l in les.splitlines():
        m = re.match(r'^GATE (S\d{3,}) receipt=(\S+) ', l)
        if not m:
            continue
        i, path = m.group(1), m.group(2)
        data = files.get(path)
        if data is None:
            continue
        text = (data.decode("utf-8", "replace") if isinstance(data, bytes) else data).lower()
        hits = [b for b in BAD_LOC if b in text]
        if hits or cjk(text) >= 8:
            bad.append((i, hits, cjk(text)))
    print("T3 %-38s failing=%d %s" % (label, len(bad), bad[:4]))
    return not bad


def t5_citation_per_paragraph(entry_text):
    """T5 candidate: every prose paragraph outside fences must cite an id.
    Run on the real entry to price the harm."""
    paras, cur = [], []
    for line in unfenced(entry_text):
        if not line.strip():
            if cur:
                paras.append(cur)
            cur = []
        else:
            cur.append(line)
    if cur:
        paras.append(cur)
    bad = []
    for p in paras:
        head = p[0]
        if head.startswith("#") or head.startswith("|") or head.startswith("source:") \
                or head.startswith("verified-at:") or head.startswith("recheck:") \
                or head.startswith("journal ") or head.startswith("Lane:") \
                or head.startswith("ground:") or head.startswith("assimilated-from:"):
            continue
        if not re.search(r"\bS\d{3,}\b", "\n".join(p)):
            bad.append(p[0][:70])
    return bad


def main():
    base = base_files()
    G = admitted()
    print("counter=%s sha256=%s" % (
        COUNTER, hashlib.sha256(open(COUNTER, "rb").read()).hexdigest()))
    # P baseline: the harness reproduces the control's admitted fixture
    rc, last, cls = score(base, G, "real")
    print("P-genuine real: rc=%d last=%s clauses=%s" % (rc, last, cls))
    for name, fn, should in FORGERIES:
        g = dict(G)
        fn(g)
        rc, last, cls = score(base, g, "real")
        verdict = "ADMITTED" if (rc == 0 and "admitted=1/1" in last) else "rejected"
        print("FORGERY %-38s %-9s rc=%d observed=%s clauses=%s expected-catcher=%s"
              % (name, verdict, rc, last, cls, should))
    print()
    for name, fn in NEGATIVES:
        g = dict(G)
        fn(g)
        rc, last, cls = ctl.score(base, g, "real")
        print("NEGATIVE %-38s %-9s rc=%d observed=%s clauses=%s" % (
            name, "rejected" if rc == 1 else "ADMITTED", rc, last, cls))
    return 0


if __name__ == "__main__":
    sys.exit(main())
