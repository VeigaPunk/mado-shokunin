#!/usr/bin/env python3
"""CritC2Cheat tightenings T1-T7 for PRED-C2-r41-v1 (proposal, not a counter).

Each Tn is a minimal addition to the frozen counter's own parsers (imported
from quality/counters/c2-r41-focus-entry.py, never re-implemented) that closes
one forgery class. `check(repo, rev, base)` returns {name: [failures]}; an empty
list means the tightening admits the set at REV.

  T1  every cited Gate receipt is one of the FROZEN fetch bytes: its path is
      FETCH + basename and sha256(blob) equals the inline pin of that basename.
  T2  the own-work id's receipt is the pinned journal file (path and sha256),
      and the counts are recomputed from those pinned bytes.
  T3  the ADMIT and REFUSE paths are members of the frozen staged-package
      allowlist, and the REFUSE reason is >= 4 words of non-space text.
  T4  the cited location is not a redirector host, carries no localization
      segment (percent-decoded), the receipt is >= 90% ASCII, and the receipt's
      content type matches the location's extension.
  T5  each Gate quote occurs in its own receipt and in NO other cited receipt.
  T6  the location's last path segment (percent-decoded, query stripped) is a
      substring of the Gate receipt's basename; own-work must name the path.
  T7  at least 3 ids are absent from the BASE registry (the counter's docstring
      clause c says "at least 3"; the code tests >= 2).

Usage: tighten.py --repo D --rev A --base B [--only T1,T5] [--verify-pins]
--verify-pins re-hashes the lane's frozen fetch dir and the staged package and
reports whether the inline pins are the bytes on disk.
"""
import argparse
import hashlib
import importlib.util
import os
import re
import sys
import urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
COUNTER = os.path.join(LANE, "quality", "counters", "c2-r41-focus-entry.py")
FETCH_DIR = os.path.join(LANE, ".ufo", "waves", "round-41", "fetch")
STAGED = "/home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge"

spec = importlib.util.spec_from_file_location("c2r41", COUNTER)
c2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c2)

ENTRY = c2.ENTRIES[0]
SRC = "corpus/SOURCES.md"
LES = c2.LESSON
FETCH = c2.FETCH
JOURNAL_NAME = "xdph-journal.txt"

# Frozen receipt pins: sha256 of every file in the round-41 fetch dir (own work,
# fetched by the L1 2026-10-25, committed at the freeze). `--verify-pins`
# re-hashes the dir on disk.
PIN_RECEIPTS = {
    "Hyprland-FocusGrab.cpp":
        "53b762f7149bf1c3105ec1da2137d02cc7bece90043d9a2ce253a784b092aff1",
    "Hyprland-FocusGrab.hpp":
        "dce47251853f8d95eeec0eb357665efdceccd52b111e633c56412e5c55103421",
    "focus-grab-v1.xml":
        "0bc60c14d27f9079e0d1d9d706f91e67ad7da585f3b7f34ff7186a376c0285b4",
    "input-capture-v1.xml":
        "fff89f6f9de622fefa1a62a6e6970f76683b6328454565583046abebcfe2c360",
    "issue-565.html":
        "148a9053e813a7d912c3c2e9fdb234ef42d20004438d33b41f1110d37679d1dc",
    "protocols-README.md":
        "3c7007636e13889860491d0c57f93c29d92122d17838ca1f6559e4aeb7aa6323",
    "quickshell-grab.cpp":
        "6f7cecf15a4dbfd0dc39341c8794639595a83dd2a4ab13b6b377ac970a301a40",
    "xdph-PortalManager.cpp":
        "15c3e39cea5af1a92924ebc1ffe0f7825c86ac3c0b49e894aede86b2e091ea55",
    "xdph-journal.txt":
        "bf8fa91a321197277cf9c1260d17524e9ddf862f7f76ddf440fc057aa600aaf7",
}
PIN_PKG = {
    "merge/mado/knowledge/corpus/knowledge/focus-control-surfaces-r28.md",
    "merge/mado/knowledge/corpus/knowledge/privileged-client-surface-r29.md",
}
REDIRECTORS = ("t.co", "bit.ly", "goo.gl", "tinyurl.com", "lnkd.in", "is.gd",
               "ow.ly", "buff.ly", "cutt.ly", "rb.gy", "shorturl.at")
LOCALIZED = ("amgsk.dev", "zhihu", "qiita.com", "zenn.dev", "/ja/", "/jp/",
             "/zh/", "/zh-cn/", "/zh-hans/", "/ko/", "/tw/")
CTYPE = ((".xml", (b"<?xml",)),
         (".cpp", (b"#include", b"#pragma")),
         (".hpp", (b"#include", b"#pragma")),
         (".html", (b"<html", b"<!DOCTYPE html")),
         (".htm", (b"<html", b"<!DOCTYPE html")),
         (".md", (b"# ",)))


def gates_of(lesson):
    out = {}
    for line in c2.section(lesson, "## Gate"):
        m = c2.GATE_RE.match(line.rstrip("\n"))
        if m:
            out.setdefault(m.group(1), []).append(m.groups()[1:])
    return out


def ids_of(text):
    ids = []
    for line in text.splitlines()[:20]:
        m = c2.SRC_RE.match(line)
        if m and m.group(1) not in ids:
            ids.append(m.group(1))
    return ids


def loc_of(cells):
    toks = cells[1].split() if len(cells) > 1 else []
    return toks[-1] if toks else ""


def basename(loc):
    path = urllib.parse.urlparse(loc).path or loc
    path = urllib.parse.unquote(path).split("?")[0].split("#")[0]
    return path.rstrip("/").rsplit("/", 1)[-1]


def check(repo, rev, base, only=None):
    only = set(only) if only else None
    raw = c2.show(repo, rev, ENTRY)
    if raw is None:
        return {"a": ["entry absent at REV"]}
    text = raw.decode("utf-8", "replace")
    lines = c2.unfenced(text)
    ids = ids_of(text)
    reg_rev = c2.registry(c2.show(repo, rev, SRC))
    reg_base = c2.registry(c2.show(repo, base, SRC))
    lesson = (c2.show(repo, rev, LES) or b"").decode("utf-8", "replace")
    gates = gates_of(lesson)
    fail = {t: [] for t in ("T1", "T2", "T3", "T4", "T5", "T6", "T7")}
    blobs, quotes = {}, {}
    for i in ids:
        gl = gates.get(i, [])
        if len(gl) != 1:
            for t in fail:
                fail[t].append("%s: %d gate lines" % (i, len(gl)))
            continue
        path, _digest, quote = gl[0]
        blobs[i] = c2.show(repo, rev, path) if path.startswith(FETCH) else None
        quotes[i] = quote
    new_ids = [i for i in ids if i not in reg_base]

    if not only or "T1" in only:
        for i in ids:
            gl = gates.get(i, [])
            if len(gl) != 1:
                continue
            path = gl[0][0]
            b = blobs.get(i)
            bn = os.path.basename(path)
            if b is None:
                fail["T1"].append("%s: receipt %s outside fetch/" % (i, path))
            elif bn not in PIN_RECEIPTS:
                fail["T1"].append("%s: basename %s not a frozen fetch file"
                                  % (i, bn))
            elif hashlib.sha256(b).hexdigest() != PIN_RECEIPTS[bn]:
                fail["T1"].append("%s: sha256(receipt) != frozen pin of %s"
                                  % (i, bn))
    if not only or "T2" in only:
        own = [i for i in new_ids if reg_rev.get(i)
               and len(reg_rev[i][0]) == 11 and reg_rev[i][0][2] == "own-work"]
        if len(own) != 1:
            fail["T2"].append("own-work new ids=%d" % len(own))
        else:
            i = own[0]
            gl = gates.get(i, [])
            path = gl[0][0] if len(gl) == 1 else ""
            b = blobs.get(i)
            if path != FETCH + JOURNAL_NAME:
                fail["T2"].append("%s: receipt path %s != %s" % (
                    i, path, FETCH + JOURNAL_NAME))
            elif b is None or hashlib.sha256(b).hexdigest() != PIN_RECEIPTS[
                    JOURNAL_NAME]:
                fail["T2"].append("%s: receipt is not the pinned journal" % i)
            else:
                jc = c2.journal_counts(b)
                jm = [m for m in map(c2.JOURNAL_RE.match, lines) if m]
                if len(jm) != 1 or tuple(int(x) for x in jm[0].groups()) != jc:
                    fail["T2"].append("%s: counts differ from pinned journal"
                                      % i)
    if not only or "T3" in only:
        admits = [m for m in map(c2.ADMIT_RE.match,
                                 c2.section(lesson, "## Gate")) if m]
        refuses = [m for m in map(c2.REFUSE_RE.match,
                                  c2.section(lesson, "## Gate")) if m]
        if not any(m.group(1) in PIN_PKG and m.group(2) == ENTRY
                   for m in admits):
            fail["T3"].append("no ADMIT of %s from a staged entry" % ENTRY)
        good_ref = [m for m in refuses
                    if m.group(1) in PIN_PKG
                    and len(m.group(2).split()) >= 4]
        if not good_ref:
            fail["T3"].append("no REFUSE of a staged entry with a >= 4-word "
                              "reason")
    if not only or "T4" in only:
        for i in ids:
            rows = reg_rev.get(i, [])
            if not rows or len(rows[0]) != 11:
                fail["T4"].append("%s: no row" % i)
                continue
            loc = urllib.parse.unquote(loc_of(rows[0]))
            host = urllib.parse.urlparse(loc).hostname or ""
            if any(host == r or host.endswith("." + r) for r in REDIRECTORS):
                fail["T4"].append("%s: redirector host %s" % (i, host))
            if any(s in loc.lower() for s in LOCALIZED):
                fail["T4"].append("%s: localization segment in %s" % (i, loc))
            b = blobs.get(i)
            if b is None:
                continue
            asc = sum(1 for ch in b if ch < 128) / max(1, len(b))
            if asc < 0.90:
                fail["T4"].append("%s: receipt ascii=%.2f" % (i, asc))
            path = urllib.parse.urlparse(loc).path
            if path.lower().endswith(".txt"):
                continue
            for ext, needles in CTYPE:
                if path.lower().endswith(ext):
                    if not any(n in b for n in needles):
                        fail["T4"].append("%s: %s receipt lacks %s markup"
                                          % (i, ext, needles[0].decode()))
                    break
            else:
                if b"<html" not in b and b"<!DOCTYPE html" not in b:
                    fail["T4"].append("%s: extensionless location, receipt "
                                      "is not HTML" % i)
    if not only or "T5" in only:
        norms = {i: c2.norm(b.decode("utf-8", "replace"))
                 for i, b in blobs.items() if b is not None}
        for i, q in quotes.items():
            if i not in norms:
                continue
            nq = c2.norm(q)
            if nq not in norms[i]:
                fail["T5"].append("%s: quote absent from own receipt" % i)
            for j, t in norms.items():
                if j != i and nq in t:
                    fail["T5"].append("%s: quote also in %s's receipt" % (i, j))
    if not only or "T6" in only:
        for i in ids:
            rows = reg_rev.get(i, [])
            gl = gates.get(i, [])
            if not rows or len(rows[0]) != 11 or len(gl) != 1:
                continue
            loc = loc_of(rows[0])
            bn = basename(loc)
            rbn = os.path.basename(gl[0][0])
            kind = rows[0][2]
            if kind == "own-work":
                if loc != gl[0][0]:
                    fail["T6"].append("%s: own-work location %s != receipt"
                                      % (i, loc))
            elif len(bn) < 3 or bn not in rbn:
                fail["T6"].append("%s: location segment %r not in receipt "
                                  "basename %s" % (i, bn, rbn))
    if not only or "T7" in only:
        if len(new_ids) < 3:
            fail["T7"].append("new ids=%d < 3 (docstring clause c)"
                              % len(new_ids))
    return fail


def verify_pins():
    out = []
    for fn in sorted(os.listdir(FETCH_DIR)):
        b = open(os.path.join(FETCH_DIR, fn), "rb").read()
        got = hashlib.sha256(b).hexdigest()
        out.append((fn, len(b), got, PIN_RECEIPTS.get(fn) == got))
    for p in sorted(PIN_PKG):
        full = os.path.join("/home/vgpnk/Projects/shokuknow/merge/mado",
                            p.split("merge/mado/", 1)[1])
        out.append((p, os.path.getsize(full) if os.path.exists(full) else -1,
                    hashlib.sha256(open(full, "rb").read()).hexdigest()[:16]
                    if os.path.exists(full) else "ABSENT", None))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo")
    ap.add_argument("--rev")
    ap.add_argument("--base", default=c2.BASE_DEFAULT)
    ap.add_argument("--only")
    ap.add_argument("--verify-pins", action="store_true")
    a = ap.parse_args()
    if a.verify_pins:
        for fn, n, got, ok in verify_pins():
            print("PIN %-28s bytes=%-7d sha256=%s pinned=%s"
                  % (fn, n, got, "-" if ok is None else int(ok)))
        return 0
    only = a.only.split(",") if a.only else None
    f = check(os.path.abspath(a.repo), a.rev, a.base, only)
    for t in sorted(f):
        print("TIGHTEN %s %s" % (t, "PASS" if not f[t] else "FAIL " +
                                 "; ".join(f[t])))
    return 0 if not any(f.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
