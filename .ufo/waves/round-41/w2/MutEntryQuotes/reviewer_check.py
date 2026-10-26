#!/usr/bin/env python3
"""MutEntryQuotes reviewer script for round-41 DATA bytes.

Cross-checks the landed entry/README/registry/lesson numbers and labels against
the committed receipts, the freeze commit, and each other - the mechanical part
of the human-style review that PRED-C2-r41-v2 does not perform.

Usage:
  reviewer_check.py --repo <clone-or-lane> [--rev REV] [--tree <mutant-dir>]

Without --tree the four governed files are read from REV via git show
(default rev: the round-41 data commit).  With --tree they are read from that
directory (mutated bytes); receipts still come from the repo at REV.
Prints one `FAIL <check>: <detail>` line per violation; exit 1 iff any FAIL.
"""
import argparse, hashlib, os, re, subprocess, sys

ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
REV_DEFAULT = "07f2641696b5ac73de1404ea737a9f27e9819aa1"
BASE_DEFAULT = "ab2bfaab661c846d1de9d58c01651cd156a13949"
FREEZE = "60c3914154333180450d5da27ba222d5763cc56a"
ENTRY = "corpus/knowledge/hyprland-focus-grab-r41.md"
SOURCES = "corpus/SOURCES.md"
LESSON = "corpus/lessons/round-41.md"
README = "corpus/README.md"
FETCH = ".ufo/waves/round-41/fetch/"
W1 = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-41/w1"
ADV_RE = re.compile(r"([0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}[+-][0-9]{2}:[0-9]{2}) (\S+) "
                    r"xdg-desktop-portal-hyprland\[([0-9]+)\]: \[LOG\]  \| "
                    r"Got interface: ([A-Za-z0-9_]{1,128}) \(ver ([0-9]{1,6})\)")
BOOT_RE = re.compile(r"-- Boot ([0-9a-f]{32}) --")
WORD = {"no": 0, "zero": 0, "one": 1, "once": 1, "two": 2, "three": 3, "four": 4, "five": 5,
        "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10}
fails = []


def fail(check, detail):
    fails.append((check, detail))


def git(repo, *args):
    p = subprocess.run(["git", "-C", repo, *args], capture_output=True, env=ENV)
    return p.stdout if p.returncode == 0 else b""


def load(repo, rev, rel, tree):
    if tree:
        return open(os.path.join(tree, rel), encoding="utf-8").read()
    return git(repo, "show", "%s:%s" % (rev, rel)).decode("utf-8", "replace")


def receipt(repo, rev, name):
    return git(repo, "show", "%s:%s" % (rev, FETCH + name))


def unfenced(text):
    out, f = [], False
    for line in text.splitlines():
        if re.match(r"^\s{0,3}(```|~~~)", line):
            f = not f
            continue
        if not f:
            out.append(line)
    return out


def section_of(lines):
    sec, out = None, []
    for l in lines:
        m = re.match(r"^## §(\d+)", l)
        if m:
            sec = m.group(1)
        out.append(sec)
    return out


def journal_stats(blob):
    text = blob.decode("utf-8", "replace")
    sessions, cur, changed = [], None, False
    for line in text.split("\n"):
        if BOOT_RE.fullmatch(line):
            changed = True
            continue
        m = ADV_RE.fullmatch(line)
        if not m:
            continue
        pid, name = m.group(3), m.group(4)
        if cur is None or changed or pid != cur["pid"]:
            cur = dict(pid=pid, adverts=0, names=set(), focus_adverts=0,
                       focus_lines=0, first=m.group(1))
            sessions.append(cur)
            changed = False
        cur["adverts"] += 1
        cur["names"].add(name)
        if "focus" in line:
            cur["focus_lines"] += 1
        if name == "hyprland_focus_grab_manager_v1":
            cur["focus_adverts"] += 1
    if not sessions:
        return None
    last = sessions[-1]
    return dict(sessions=len(sessions),
                adverts=sum(s["adverts"] for s in sessions),
                distinct=len(last["names"]),
                focus=last["focus_adverts"],
                focus_occurrences=last["focus_lines"],
                slice_adverts=sessions[0]["adverts"],
                lines=len(text.rstrip("\n").split("\n")),
                bytes=len(blob))


def cited_rows(entry, sources):
    ids = set(re.findall(r"^source: (S\d{3,})", entry, re.M))
    out = []
    for l in sources.splitlines():
        cells = [c.strip() for c in l.split("|")[1:-1]]
        if len(cells) == 11 and cells[0] in ids:
            out.append((cells[0], cells))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=None)
    ap.add_argument("--rev", default=REV_DEFAULT)
    ap.add_argument("--base", default=BASE_DEFAULT)
    ap.add_argument("--tree", default=None)
    a = ap.parse_args()
    repo = a.repo
    entry = load(repo, a.rev, ENTRY, a.tree)
    readme = load(repo, a.rev, README, a.tree)
    sources = load(repo, a.rev, SOURCES, a.tree)
    lesson = load(repo, a.rev, LESSON, a.tree)
    jl = lesson.split("## Gate", 1)[1].split("\n## ", 1)[0] if "## Gate" in lesson else lesson

    jr = journal_stats(receipt(repo, a.rev, "xdph-journal.txt"))
    pm = receipt(repo, a.rev, "xdph-PortalManager.cpp").decode("utf-8", "replace")
    xml = receipt(repo, a.rev, "focus-grab-v1.xml").decode("utf-8", "replace")
    inst = receipt(repo, a.rev, "xdph-installed-version.txt")
    n_branches = len(re.findall(r"INTERFACE ==", pm))
    if jr is None:
        fail("C1-census", "journal unparseable")

    # C1: census numbers everywhere vs the journal receipt
    m = re.search(r"^journal sessions=(\d+) adverts=(\d+) interfaces=(\d+) focus_grab=(\d+)$",
                  "\n".join(unfenced(entry)), re.M)
    if not m or [int(x) for x in m.groups()] != [jr["sessions"], jr["adverts"], jr["distinct"], jr["focus"]]:
        fail("C1-census-line", "entry census %s vs journal S=%d A=%d D=%d F=%d"
             % (m.groups() if m else None, jr["sessions"], jr["adverts"], jr["distinct"], jr["focus"]))

    def prose(text, pat, want, label):
        m = re.search(pat, text, re.M)
        got = None
        if m:
            g = m.group(1)
            got = WORD.get(g.lower(), None)
            if got is None and g.isdigit():
                got = int(g)
        if got != want:
            fail(label, "claims %r, receipt says %s" % (m.group(1) if m else None, want))

    prose(entry, r"its (\w+|\d+) adverts are a lower bound", jr["slice_adverts"], "C1-slice-adverts")
    prose(entry, r"with (\w+|\d+) adverts and closes", jr["slice_adverts"], "C1-slice-adverts-2")
    prose(entry, r"(\w+|\d+) distinct names, no name advertised twice", jr["distinct"], "C1-distinct")
    prose(entry, r"`focus` occurs exactly (\w+|\d+), on the advert line",
          jr["focus_occurrences"], "C1-focus-occurrences")
    prose(entry, r"census is one host, one day, (\w+|\d+) portal sessions", jr["sessions"], "C1-sessions")
    prose(readme, r"(\w+|\d+) globals in the latest portal session", jr["distinct"], "C1-readme-globals")
    prose(readme, r"(no|one|two|\d+) focus-grab manager advert", jr["focus"], "C1-readme-adverts")
    m = re.search(r"journal \(`journalctl[^\)]*`, (\d+) B, (\d+) lines\)", jl)
    if m:
        if int(m.group(1)) != jr["bytes"]:
            fail("C1-lesson-journal-B", "claims %s B, journal is %d B" % (m.group(1), jr["bytes"]))
        if int(m.group(2)) != jr["lines"]:
            fail("C1-lesson-journal-lines", "claims %s lines, journal has %d" % (m.group(2), jr["lines"]))
    m = re.search(r"\| S289 [^\n]*?(\d+) lines,", sources)
    if not m or int(m.group(1)) != jr["lines"]:
        fail("C1-reg-lines", "S289 anchor claims %s lines, journal has %d"
             % (m.group(1) if m else None, jr["lines"]))

    # C2: receipt metadata in registry anchors and lesson prose
    for rid, cells in cited_rows(entry, sources):
        anch = cells[5]
        mm = re.search(r"(\d+) B sha256 ([0-9a-f]{64})", anch)
        path = re.search("(" + re.escape(FETCH) + r"[\w.-]+)", anch)
        if mm and path:
            blob = receipt(repo, a.rev, os.path.basename(path.group(1)))
            if len(blob) != int(mm.group(1)):
                fail("C2-size", "%s anchor claims %s B, receipt is %d B" % (rid, mm.group(1), len(blob)))
            if hashlib.sha256(blob).hexdigest() != mm.group(2):
                fail("C2-sha", "%s anchor sha mismatches its receipt" % rid)
    m = re.search(r"xdph-installed-version\.txt`, (\d+) B,", jl)
    if not m or int(m.group(1)) != len(inst):
        fail("C2-lesson-size", "lesson claims %s B, installed-version receipt is %d B"
             % (m.group(1) if m else None, len(inst)))

    # C3: 'the N pre-wave receipts' vs cited gate receipts present at the freeze
    gates = re.findall(r"^GATE (S\d+) receipt=\S*/([\w.-]+) ", jl, re.M)
    ls = git(repo, "ls-tree", "-r", "--name-only", FREEZE, "--", FETCH).decode()
    frozen = {os.path.basename(l) for l in ls.splitlines()}
    n_frozen_cited = len({b for _, b in gates} & frozen)
    m = re.search(r"the (\w+|\d+) pre-wave receipts", jl)
    got = WORD.get(m.group(1).lower()) if m else None
    if got != n_frozen_cited:
        fail("C3-freeze-count", "lesson claims %s pre-wave receipts; %d cited receipts sit at the freeze"
             % (got, n_frozen_cited))

    # C4: label discipline - INF carries Basis:, OBS does not; §6 state vs body
    lines = unfenced(entry)
    secs = section_of(lines)
    for l in lines:
        if l.startswith("**OBS**") and "Basis:" in l:
            fail("C4-obs-basis", "OBS line with Basis: %r" % l[:60])
        if l.startswith("**INF**"):
            q = re.search(r'"([A-Za-z][^"]{10,})"', l)
            if q and len(q.group(1).split()) >= 4:
                fail("C4-inf-quote", "INF line carries a verbatim receipt quote: %r" % l[:60])
    for l in lines:
        if not re.match(r"^\| What |\| When |\| Is |\| Does |\| Who |\| How ", l):
            continue
        cells = [c.strip() for c in l.strip().strip("|").split("|")]
        if len(cells) != 3:
            continue
        q, where, state = cells
        st = state.split()[0].rstrip(",")
        ids = sorted(set(re.findall(r"\bS\d{3,}\b", where)))
        secm = re.search(r"§(\d+)", where)
        if not ids or not secm or st not in ("OBS", "INF", "UNK"):
            continue
        sec = secm.group(1)
        body_hit = any(secs[i] == sec and re.search(r"\b%s\b" % id_, ln)
                       and ln.startswith("**%s**" % st) for i, ln in enumerate(lines) for id_ in ids)
        if not body_hit:
            fail("C4-table-state", "%r state %s but no **%s** line in §%s names any of %s"
                 % (q[:40], st, st, sec, ids))

    # C5: ADMIT target must be named by the entry's assimilated-from line
    m = re.search(r"^ADMIT \S*/([\w.-]+\.md) as ", jl, re.M)
    af = re.search(r"^assimilated-from:(.*)$", entry, re.M)
    if not m or not af or m.group(1) not in af.group(1):
        fail("C5-admit-from", "ADMIT %s not named in assimilated-from"
             % (m.group(1) if m else None))

    # C6: round coherence
    mr = re.search(r"Round: (\d+)\.", entry)
    if not mr or mr.group(1) != "41":
        fail("C6-round", "entry says Round: %s" % (mr.group(1) if mr else None))
    if "(MADO-R41-1, round 41" not in readme:
        fail("C6-round", "README row round marker moved")

    # C7: registry vocabulary for cited rows (kind, tier, recheck class vs BASE)
    base_src = git(repo, "show", "%s:%s" % (a.base, SOURCES)).decode("utf-8", "replace")
    vocab = set()
    for l in base_src.splitlines():
        c = [x.strip() for x in l.split("|")[1:-1]]
        if len(c) == 11 and re.match(r"^S\d+$", c[0]):
            mm = re.match(r"^(\d+d|on-[a-z-]+|\d{4}-\d{2}-\d{2})", c[9])
            vocab.add(mm.group(1) if mm else c[9].split()[0])
    for rid, cells in cited_rows(entry, sources):
        if cells[2] not in ("docs", "code", "spec", "community", "own-work"):
            fail("C7-kind", "%s kind cell %r" % (rid, cells[2]))
        if cells[3] not in ("A", "B"):
            fail("C7-tier", "%s tier cell %r" % (rid, cells[3]))
        key = cells[9].split()[0]
        if key not in vocab:
            fail("C7-recheck-vocab(weak)", "%s recheck %r is not a class used at BASE" % (rid, cells[9]))
    mh = re.search(r"^recheck:\s*(\S+)", entry, re.M)
    if mh and mh.group(1) not in vocab:
        fail("C7-entry-recheck-vocab(weak)", "entry recheck %r is not a class used at BASE" % mh.group(1))

    # C5b: every staged file named in assimilated-from is dispositioned (ADMIT or REFUSE) in the Gate
    if af:
        dispositioned = {os.path.basename(m.group(1)) for m in re.finditer(r"^(?:ADMIT|REFUSE) (\S+\.md)", jl, re.M)}
        for name in re.findall(r"merge/mado/[\w./-]*?([\w.-]+\.md)\b", af.group(1)):
            if name not in dispositioned:
                fail("C5b-disposition", "assimilated-from names %s but no ADMIT/REFUSE line names it" % name)

    # C8: bind-branch count, receipt is arbiter for entry AND registry
    prose(entry, r"a fixed set of (\w+|\d+) named branches", n_branches, "C8-entry-branches")
    m = re.search(r"which (\w+|\d+) it binds", sources)
    got = WORD.get(m.group(1).lower(), m.group(1)) if m else None
    if got != n_branches:
        fail("C8-registry-branches", "S286 scope says %r branches, receipt has %d `INTERFACE ==` branches"
             % (got, n_branches))

    # C9: README issue number vs registry S287 locator
    m1 = re.search(r"\(issue (\d+)\)", readme)
    m2 = re.search(r"\| S287 \| [^|]*issues/(\d+)", sources)
    if m1 and m2 and m1.group(1) != m2.group(1):
        fail("C9-issue", "README says issue %s, S287 locator says %s" % (m1.group(1), m2.group(1)))

    # C12: the grep exit-code claim vs the actual receipt bytes
    m = re.search(r"`grep -in focus` over `PortalManager\.cpp` exits (\d+)", entry)
    if m:
        gr = subprocess.run(["grep", "-in", "focus", "/dev/stdin"], input=pm.encode(),
                            capture_output=True)
        if int(m.group(1)) != gr.returncode:
            fail("C12-exit-code", "entry claims grep exits %s, receipt bytes give rc=%d"
                 % (m.group(1), gr.returncode))

    # C10: entry §1 protocol table kinds vs the XML receipt grammar
    if '<request name="add_surface"' not in xml:
        fail("C10-xml", "add_surface not a request in receipt")
    if '<event name="cleared"' not in xml:
        fail("C10-xml", "cleared not an event in receipt")
    if not re.search(r"\| `add_surface\(surface: wl_surface\)` \| request \|", entry):
        fail("C10-table-kind", "add_surface row kind is not 'request'")
    if not re.search(r"\| `cleared` \| event \|", entry):
        fail("C10-table-kind", "cleared row kind is not 'event'")

    # C11 (weak): lesson M41-N refs exist in some w1 report
    if os.path.isdir(W1):
        for tok in set(re.findall(r"M41-\d+", jl)):
            hits = any(tok in open(os.path.join(W1, f), encoding="utf-8", errors="replace").read()
                       for f in os.listdir(W1) if f.endswith(".md"))
            if not hits:
                fail("C11-m41-ref(weak)", "%s not found in any w1 report" % tok)

    for check, detail in fails:
        print("FAIL %s: %s" % (check, detail))
    print("%d violation(s)" % len(fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
