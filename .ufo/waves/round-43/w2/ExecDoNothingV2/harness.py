#!/usr/bin/env python3
"""ExecDoNothingV2 - cheap do-nothing controls against PRED-C2-r43-v2 at the data commit.

Reference L0 is the landed entry transcribed verbatim into a fixture (same registry rows, same
Gate lines, same ten pinned receipts, same census lines), so every control below is a delta on the
landed text and nothing else. P is the registered control P of ctl/run-c2-controls-v2.py, built by
its own admitted(). Every fixture is a fresh `git init` under the seat's scratch dir and every git
call names `-C "$D"`; the toplevel is asserted equal to $D before the first commit. The runner's
main() is never called: helpers are imported by importlib. The counter is read, never edited.

Usage:  python3 harness.py            (writes runs/<n>-<name>.txt and summary.txt in this dir)
"""
import hashlib
import importlib.util
import os
import re
import subprocess
import sys
import tempfile

SEAT = os.path.dirname(os.path.abspath(__file__))
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
SCRATCH = "/fast/scratch/hyaku/mado-r43/ExecDoNothingV2"
DATA = "1959770657f1f8665097c1aed4be6c1cbb07139f"
BASE = "a35cfdfcdeb3bd42d1a2cd960faf22ceac1bef3f"
CTL = LANE + "/.ufo/waves/round-43/ctl/run-c2-controls-v2.py"
COUNTER = LANE + "/quality/counters/c2-r43-gkeep-entry-v2.py"

os.makedirs(SCRATCH, exist_ok=True)
os.makedirs(os.path.join(SEAT, "runs"), exist_ok=True)
os.environ["TMPDIR"] = SCRATCH
tempfile.tempdir = SCRATCH


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)          # module bodies only define helpers; main is guarded
    return mod


R = load(CTL, "ctl_v2")                   # the v2 controls runner (helpers + admitted() + score)
C = load(COUNTER, "pred_v2")              # the frozen v2 counter (quote_at, occurrences, ...)


def show(rev, path):
    p = subprocess.run(["git", "-C", LANE, "show", "%s:%s" % (rev, path)],
                       capture_output=True)
    assert p.returncode == 0, path
    return p.stdout.decode()


def sha(data):
    return hashlib.sha256(data if isinstance(data, bytes) else data.encode()).hexdigest()


# ---------------------------------------------------------------- landed data at the data commit
ENTRY_TEXT = show(DATA, "corpus/knowledge/hyprland-gkeep-geometry-r43.md")
SOURCES = show(DATA, "corpus/SOURCES.md")
LESSON = show(DATA, "corpus/lessons/round-43.md")

CITED = []
for line in ENTRY_TEXT.split("\n"):
    m = re.match(r"^source: (S\d{3,})\b", line)
    if m and m.group(1) not in CITED:
        CITED.append(m.group(1))
assert len(CITED) == 10, CITED

REG = C.registry(SOURCES.encode())
RAW = {}
for line in SOURCES.split("\n"):
    m = re.match(r"^ {0,3}\|\s*(S\d{3,})\s*\|", line)
    if m and m.group(1) in CITED:
        RAW[m.group(1)] = line.rstrip()
assert set(RAW) == set(CITED), (sorted(RAW), CITED)
assert all(len(REG[i][0]) == 11 and REG[i][0] == [c.strip() for c in RAW[i].strip().split("|")[1:-1]]
           for i in CITED)

GATES = {}
for line in LESSON.split("\n"):
    m = C.GATE_RE.match(line)
    if m and m.group(1) in CITED:
        GATES[m.group(1)] = (m.group(2), m.group(3), m.group(4))
assert set(GATES) == set(CITED), sorted(GATES)
ADMIT = [l for l in LESSON.split("\n") if C.ADMIT_RE.match(l)][0]
REFUSE = [l for l in LESSON.split("\n") if C.REFUSE_RE.match(l)][0]

LOC = {}
for i in CITED:
    path, digest, quote = GATES[i]
    fn = os.path.basename(path)
    blob = R.blob(fn)
    assert sha(blob) == digest, (i, "gate sha != fetched bytes")
    nq = re.sub(r"\s+", " ", quote)
    at = C.quote_at(blob, nq)
    assert at, (i, "quote not found word-bounded")
    assert len(C.occurrences(blob, nq)) == 1, (i, "quote occurs more than once")
    assert C.quote_in_code(blob, nq, fn), (i, "quote only in a comment")
    assert 3 <= len(nq.split()) <= 25, (i, "quote length")
    assert "%s:%d" % (fn, at) in ENTRY_TEXT, (i, "computed locator absent from the landed entry")
    LOC[i] = (fn, at)

CENSUS = [l for l in ENTRY_TEXT.split("\n")
          if l.startswith("host ") or l.startswith("gkeep request")]
assert len(CENSUS) == 3, CENSUS

# the two HELD ids (S155, S158) exist in the lane's BASE registry; their BASE rows are carried into
# the fixture base so clause c treats them as present-at-BASE, exactly as the lane does
BASE_SRC = show(BASE, "corpus/SOURCES.md")
BASE_ROW = {}
for line in BASE_SRC.split("\n"):
    m = re.match(r"^ {0,3}\|\s*(S\d{3,})\s*\|", line)
    if m and m.group(1) in CITED:
        BASE_ROW[m.group(1)] = line.rstrip()
assert set(BASE_ROW) == {"S155", "S158"}, sorted(BASE_ROW)
BASE_FILES = R.base_files()
BASE_FILES[R.SRC] = BASE_FILES[R.SRC].replace(
    R.HELD_ROW, R.HELD_ROW + "\n" + "\n".join(BASE_ROW[i] for i in sorted(BASE_ROW)))


def fixture(entry, gates=None, rows=None, refuse=None):
    """A committed-shape fixture: base files + registry rows + Gate lines + pins + this entry."""
    g = R.base_files()
    gt = gates if gates is not None else GATES
    rows = rows if rows is not None else RAW
    ids = [i for i in CITED if i in gt]
    src = BASE_FILES[R.SRC]
    for i in ids:
        if i in BASE_ROW:
            src = src.replace(BASE_ROW[i], rows.get(i, RAW[i]))
    g[R.SRC] = src.replace(R.HELD_ROW, R.HELD_ROW + "\n"
                           + "\n".join(rows.get(i, RAW[i]) for i in ids if i not in BASE_ROW))
    for i in ids:
        fn = os.path.basename(gt[i][0])
        g[R.FETCH + fn] = R.blob(fn)
    g[R.LES] = ("# round 43\n\n## Gate\n\n"
                + "\n".join(R.gate_line(i, gt[i][0], g[R.FETCH + os.path.basename(gt[i][0])],
                                        gt[i][2]) for i in ids)
                + "\n" + ADMIT + "\n" + (refuse or REFUSE) + "\n")
    g["corpus/README.md"] = (R.base_files()["corpus/README.md"]
                             + "| `knowledge/hyprland-gkeep-geometry-r43.md` | new |\n")
    g[R.ENTRY] = entry
    return g


def score(files_after):
    """Score one fixture with the frozen counter; returns (rc, clauses, last, stdout)."""
    d = tempfile.mkdtemp(prefix="dn-", dir=SCRATCH)
    try:
        subprocess.run(["git", "-C", d, "init", "-q"], check=True, env=R.ENV)
        top = subprocess.run(["git", "-C", d, "rev-parse", "--show-toplevel"], check=True,
                             capture_output=True, text=True, env=R.ENV).stdout.strip()
        if os.path.realpath(top) != os.path.realpath(d):
            raise SystemExit("fixture toplevel mismatch: %s != %s" % (top, d))
        b = R.commit_all(d, BASE_FILES, "base")
        a = R.commit_all(d, files_after, "after")
        p = subprocess.run([sys.executable, "-I", COUNTER, "--repo", d, "--rev", a, "--base", b],
                           capture_output=True, text=True, env=R.ENV)
        out = p.stdout.strip().splitlines()
        cls = [l for l in out if " clauses=" in l]
        cls = cls[0].split(" clauses=")[1].split(" admitted")[0] if cls else "-"
        last = out[-1] if out else "NO-OUTPUT " + p.stderr[-200:]
        return p.returncode, cls, last.split(": ", 1)[-1].split(" rev=")[0], p.stdout + p.stderr
    finally:
        subprocess.run(["rm", "-rf", "--", d], env=R.ENV)


# ------------------------------------------------------------------ mechanical rules (for the
# "is the landed prose distinguishable from this admitted control by any mechanical rule?" question)
HEADER_PREFIX = ("source:", "verified-at:", "recheck:", "ground:", "Lane:", "assimilated-from:")
CENSUS_SET = set(CENSUS)


def no_id_words(text):
    n = 0
    for l in C.unfenced(text):
        t = l.strip()
        if not t or t in CENSUS_SET or t.startswith(HEADER_PREFIX) or t.startswith("|"):
            continue
        if re.search(r"\bS\d{3,}\b", t):
            continue
        n += len(t.split())
    return n


RULES = [
    ("M1_has_INF_line", lambda t: any(l.startswith("**INF**") for l in C.unfenced(t))),
    ("M2_has_UNK_line", lambda t: any(l.startswith("**UNK**") for l in C.unfenced(t))),
    ("M3_license_table", lambda t: any(l.startswith("| question |") and l.rstrip().endswith("state |")
                                       for l in C.unfenced(t))),
    ("M4_has_ground_line", lambda t: any(l.startswith("ground:") for l in C.unfenced(t))),
    ("M5_table_row_with_UNK", lambda t: any(l.startswith("|") and "| UNK |" in l for l in C.unfenced(t))),
    ("M6_prose_words_ge_120", lambda t: no_id_words(t) >= 120),
    ("M7_at_least_5_section_headings", lambda t: sum(1 for l in C.unfenced(t)
                                                    if re.match(r"^## §\d", l)) >= 5),
    ("M8_prose_mentions_420", lambda t: any("420" in l for l in C.unfenced(t)
                                            if l.strip() not in CENSUS_SET
                                            and not re.search(r"\bS\d{3,}\b", l)
                                            and l.lstrip().startswith(("**INF**", "**UNK**", "So ", "Two ")))),
]


def rule_row(text):
    return "".join("%d" % int(bool(f(text))) for _, f in RULES)


# ------------------------------------------------------------------------------- the controls
L = ENTRY_TEXT
_lines = L.split("\n")


def hdr_lines():
    return [l for l in _lines if l.startswith("source:")]


def quote_lines(marker=True, order=None):
    out = []
    for i in (order or CITED):
        fn, at = LOC[i]
        q = GATES[i][2]
        out.append(("**OBS** %s - `%s` (%s:%d);" if marker else "%s `%s` (%s:%d).")
                   % (i, q, fn, at))
    return out


def minimal_header(desc="receipt", title="# A quotation record"):
    return [title, ""] + ["source: %s - %s" % (i, desc) for i in CITED] + [
        "verified-at: 2026-10-26", "recheck: 90d"]


FILLER = ("The wallpaper in the hallway was replaced in the spring and the paste has held since, "
          "though the seam above the radiator has lifted again.")

D = []          # (name, expected, fixture-dict builder)


def add(name, expected, build):
    D.append((name, expected, build))


# D01 the canonical do-nothing: ten correct quotes, a neutral header, the census lines, nothing else
def d01():
    return minimal_header() + [""] + quote_lines(marker=False) + [""] + CENSUS + [""]


add("D01-quotes-only-wallpaper", "admitted", lambda: fixture("\n".join(d01()) + "\n"))


# D02 the same with the landed OBS vocabulary and the landed source descriptions (claims live only
# in the header descriptions, which no clause binds to anything)
def d02():
    return (["# What sets the size of the host's gkeep window"] + [""]
            + hdr_lines() + ["verified-at: 2026-10-26", "recheck: 90d", ""]
            + quote_lines() + [""] + CENSUS + [""])


add("D02-quotes-only-obs-marked", "admitted", lambda: fixture("\n".join(d02()) + "\n"))


# D03 the landed entry whose prose claims nothing about gkeep (quotes and census intact)
def d03():
    out, in_table, skip = [], False, False
    for l in _lines:
        if l.startswith("| question |"):
            out.extend(["| question | where the answer lives | state |", "|---|---|---|",
                        "| Which paste holds wallpaper on plaster? | the decorator's note | OBS |",
                        "| Does the hallway get morning light? | the window | UNK |"])
            in_table = True
            continue
        if in_table:
            if l.startswith("|"):
                continue
            in_table = False
        if l.startswith("**INF** ") or l.startswith("**UNK** "):
            out.append("**INF** " + FILLER)
            continue
        if l.startswith("ground:"):
            out.append("ground: how the wallpaper in the hallway was chosen and which paste was used")
            continue
        if l.startswith("Census (recomputed"):
            out.append("Census (recomputed by the counter from the three receipts):")
            continue
        if l.startswith("- "):
            out.append("- Nothing about wallpaper paste is established here.")
            continue
        out.append(l)
    return out


add("D03-prose-claims-nothing", "admitted", lambda: fixture("\n".join(d03()) + "\n"))


# D04 the landed entry with every INF and UNK line deleted (the whole licensing argument)
def d04():
    out = []
    for l in _lines:
        if l.startswith("**INF** ") or l.startswith("**UNK** "):
            continue
        if l.startswith("|") and "| UNK |" in l:
            continue
        if l.startswith("- The current (drawn) size") or l.startswith("- What happens after") \
                or l.startswith("- Behaviour on any Hyprland"):
            continue
        out.append(l)
    return out


add("D04-INF-UNK-deleted", "admitted", lambda: fixture("\n".join(d04()) + "\n"))


# D05 every claim negated, every quote intact
def d05():
    out = []
    for l in _lines:
        if l.startswith("**INF** "):
            out.append("**INF** False: " + l[len("**INF** "):])
        elif l.startswith("**UNK** "):
            out.append("**UNK** False: " + l[len("**UNK** "):])
        elif l.startswith("| question |"):
            out.append(l)
        elif l.startswith("|") and not l.startswith("|---"):
            cells = l.split("|")
            if len(cells) >= 5:
                cells[2] = " nothing decides this; the opposite holds "
                l = "|".join(cells)
            out.append(l)
        elif l.startswith("ground:"):
            out.append("ground: why nothing in these sources decides the size of a gkeep window")
        elif l.startswith("- "):
            out.append("This does not hold: " + l[2:])
        else:
            out.append(l)
    out += ["", "## Negation of the entry above",
            "", "No link of the chain in §1 to §3 decides the size of a gkeep window on this host: the",
            "rule is inert, the floating branch is unreachable, and the report is the client's own",
            "default size under every condition these sources describe.", ""]
    return out


add("D05-claims-negated-quotes-intact", "admitted", lambda: fixture("\n".join(d05()) + "\n"))


# D06 the ten quotes literally only (no header, no census): expected rejected, proof the clauses bite
add("D06-ten-quotes-literally-only", "rejected",
    lambda: fixture("\n".join(quote_lines(marker=False)) + "\n"))


# D07 a decision table that contradicts the census, census lines and quotes intact
def d07():
    out, in_table = [], False
    for l in _lines:
        if l.startswith("| question |"):
            out.extend(["| question | where the answer lives | state |", "|---|---|---|",
                        "| Is a gkeep window open on this host now? | the census | OBS: yes, one mapped "
                        "floating client reporting 420x500 |",
                        "| Does the host have a gkeep size rule at all? | the config copy | OBS: no |",
                        "| Do the rule and the client ask for the same size? | the source chain | "
                        "OBS: no, they differ |"])
            in_table = True
            continue
        if in_table:
            if l.startswith("|"):
                continue
            in_table = False
        out.append(l)
    return out


add("D07-table-contradicts-census", "admitted", lambda: fixture("\n".join(d07()) + "\n"))


# D08 the landed entry plus a verdict section asserting the opposite conclusion
def d08():
    return _lines + ["", "## Verdict",
                     "", "The 420x500 report is the client's own default size and nothing else: the rule",
                     "never reaches a window on this host and every branch quoted above is unreachable",
                     "for a gkeep window, so the chain the entry builds is a chain of unread code.", ""]


add("D08-opposite-conclusion-appended", "admitted", lambda: fixture("\n".join(d08()) + "\n"))


# D09 the same do-nothing as D01 with the quotes in the reverse order
add("D09-quotes-reversed-order", "admitted",
    lambda: fixture("\n".join(minimal_header() + [""] + quote_lines(marker=False, order=list(reversed(CITED)))
                              + [""] + CENSUS + [""]) + "\n"))


# D10 a fabricated oracle pointer: no cited id, so nothing binds it
def d10():
    return (d01() + ["", "## §6 An observation that is not in this lane",
                     "", "In the isolated oracle run recorded at",
                     "`.ufo/waves/round-43/w2/ExecDoNothingV2/oracle-absent.txt` the same client reported",
                     "`size 420 500` with the size line removed from the config, which shows the client is",
                     "the origin of the size; the file is kept outside the lane by the oracle seat.", ""])


add("D10-fabricated-oracle-pointer", "admitted", lambda: fixture("\n".join(d10()) + "\n"))


# D11 the landed entry, with the first REFUSE reason replaced by a flip word plus nonsense
def d11():
    bad = re.sub(r"reason=.*$", "reason=superseded zebra ladder quokka", REFUSE)
    assert bad != REFUSE
    return fixture(L, refuse=bad)


add("D11-refusal-reason-nonsense", "admitted", d11)


# D12 the landed entry with the registry `teaches` cell of all ten rows replaced by a denial
def d12():
    rows = {}
    for i in CITED:
        if i in BASE_ROW:          # cells 1-9 must stay byte-equal for a BASE-present id
            continue
        cells = [c.strip() for c in RAW[i].strip().split("|")[1:-1]]
        cells[6] = "nothing here teaches anything about window sizes or geometry"
        rows[i] = "| " + " | ".join(cells) + " |"
    return fixture(L, rows=rows)


add("D12-teaches-cell-denial", "admitted", d12)


# D13 the landed entry whose header descriptions misdescribe the receipt they name
def d13():
    out = []
    for l in _lines:
        m = re.match(r"^(source: (S\d{3,}) - ).*$", l)
        if m:
            tail = l.rsplit(" - ", 1)[-1]
            out.append(m.group(1) + "the wallpaper daemon's config file - " + tail)
        else:
            out.append(l)
    return out


add("D13-source-descriptions-wrong", "admitted", lambda: fixture("\n".join(d13()) + "\n"))


# D14 the landed entry plus a disclaimer that the census was not taken
def d14():
    return _lines + ["", "The census lines above were not taken on this host; they are illustrative", ""]


add("D14-census-disclaimed", "admitted", lambda: fixture("\n".join(d14()) + "\n"))


# D15 the landed entry with all ten quotes swapped for OTHER genuine quotes from the same receipts
def alt_quote(fn, orig, span=1):
    """The legal genuine quote of this receipt farthest (in lines) from the cited one.

    span=1 scans single lines; span=2/3 joins adjacent lines, for a receipt whose every line is
    too short to be a legal 3-word quote (the one-key-per-line clients JSON)."""
    blob = R.blob(fn)
    at0 = C.quote_at(blob, re.sub(r"\s+", " ", orig))
    others = [C.norm_receipt(R.blob(os.path.basename(GATES[j][0])))
              for j in CITED if os.path.basename(GATES[j][0]) != fn]
    raw = blob.decode("utf-8", "replace").split("\n")
    best = None
    for k in range(0, max(0, len(raw) - span + 1)):
        cand = re.sub(r"\s+", " ", " ".join(raw[k:k + span])).strip()
        if not cand or len(cand) > 160:
            continue
        if any(ch in cand for ch in "`|"):
            continue
        if fn.endswith((".py", ".conf")) and cand.startswith("#"):
            continue
        if fn.endswith((".cpp", ".hpp", ".h")) and cand.startswith(("//", "/*", "*")):
            continue
        if re.search(r"\b[Ss]\d{3,}\b", cand):
            continue
        if any(cand in o for o in others):      # clause d: the quote must be in no other receipt
            continue
        if not 3 <= len(cand.split()) <= 25:
            continue
        if len(C.occurrences(blob, cand)) != 1:
            continue
        if not C.quote_in_code(blob, cand, fn):
            continue
        at = C.quote_at(blob, cand)
        if at is None:
            continue
        dist = abs(at - at0)
        if best is None or dist > best[0]:
            best = (dist, cand, at)
    return best


def d15():
    gates, entry = {}, L
    swaps = []
    for i in CITED:
        path, digest, quote = GATES[i]
        fn = os.path.basename(path)
        alt = alt_quote(fn, quote) or alt_quote(fn, quote, span=2) or alt_quote(fn, quote, span=3)
        assert alt is not None and alt[0] > 0, (i, "no distant legal quote found")
        dist, cand, at = alt
        ab = R.blob(fn)
        nq = re.sub(r"\s+", " ", cand)
        for j in CITED:
            if j != i:
                assert nq not in C.norm_receipt(R.blob(os.path.basename(GATES[j][0]))), (i, j, "cross")
        gates[i] = (path, sha(ab), cand)
        entry = entry.replace(re.sub(r"\s+", " ", quote), nq)
        old_loc, new_loc = "%s:%d" % (fn, LOC[i][1]), "%s:%d" % (fn, at)
        assert old_loc in entry, (i, old_loc)
        entry = entry.replace(old_loc, new_loc)
        swaps.append((i, fn, LOC[i][1], at, dist, cand))
    return fixture(entry, gates=gates), swaps


_d15_cache = {}


def d15_fixture():
    if "f" not in _d15_cache:
        _d15_cache["f"], _d15_cache["swaps"] = d15()
    return _d15_cache["f"]


add("D15-unrelated-quotes-bound", "admitted", d15_fixture)


# R-series: shape breakers. They must be REJECTED, otherwise the harness admits everything.
def r01():
    keep = [i for i in CITED if i != "S158"]
    rows = {i: RAW[i] for i in keep}
    gates = {i: GATES[i] for i in keep}
    text = ("\n".join(["# A quotation record", ""]
                      + ["source: %s - receipt" % i for i in keep]
                      + ["verified-at: 2026-10-26", "recheck: 90d", ""]
                      + ["%s `%s` (%s:%d)." % (i, GATES[i][2], LOC[i][0], LOC[i][1]) for i in keep]
                      + [""] + CENSUS + [""]) + "\n")
    return fixture(text, gates=gates, rows=rows)


add("R01-nine-pins-only", "rejected", r01)


def r02():
    text = ("\n".join(minimal_header() + [""] + quote_lines(marker=False) + [""]) + "\n")
    return fixture(text)


add("R02-no-census-lines", "rejected", r02)


def r03():
    text = ("\n".join(minimal_header() + [""] + quote_lines(marker=False)
                      + ["**INF** S290 also proves the wallpaper is unrelated.", ""] + CENSUS + [""]) + "\n")
    return fixture(text)


add("R03-extra-line-naming-an-id", "rejected", r03)


def r04():
    text = ("\n".join(minimal_header() + [""] + quote_lines(marker=False)
                      + ["", "See https://amgsk.dev/posts/hyprland-rules/ for the wallpaper.", ""]
                      + CENSUS + [""]) + "\n")
    return fixture(text)


add("R04-localized-channel-marker", "rejected", r04)


# ----------------------------------------------------------------------------------- the run
def main():
    ident = []
    for p in (CTL, COUNTER):
        ident.append("%s sha256=%s" % (os.path.relpath(p, LANE), sha(open(p, "rb").read())))
    head = ("SEAT ExecDoNothingV2 - do-nothing controls vs PRED-C2-r43-v2\n"
            "data commit %s  base %s\n%s\n" % (DATA, BASE, "\n".join(ident)))
    noharm = subprocess.run(["git", "-C", LANE, "status", "--porcelain"], capture_output=True,
                            text=True).stdout
    results = []
    lines = [head, "landed entry %d lines, %d cited ids, %d census lines"
             % (len(_lines), len(CITED), len(CENSUS)), ""]

    # L0: the landed entry transcribed verbatim
    l0 = score(fixture(L))
    lines.append("control=L0-landed-verbatim expected=admitted observed=%s clauses=%s rc=%d"
                 % (l0[2], l0[1], l0[0]))
    open(os.path.join(SEAT, "runs", "L0-landed-verbatim.txt"), "w").write(
        head + "control=L0-landed-verbatim\n" + l0[3] + "\n")
    results.append(("L0-landed-verbatim", "admitted", l0[2].startswith("admitted=1/1"), l0[1], L))

    # P: the registered control P of the v2 controls runner, built by its own admitted()
    ptext = R.admitted()[R.ENTRY]
    pr = score(R.admitted())
    lines.append("control=P-registered expected=admitted observed=%s clauses=%s rc=%d"
                 % (pr[2], pr[1], pr[0]))
    open(os.path.join(SEAT, "runs", "P-registered.txt"), "w").write(
        head + "control=P-registered (ctl/run-c2-controls-v2.py admitted())\n" + pr[3] + "\n")
    results.append(("P-registered", "admitted", pr[2].startswith("admitted=1/1"), pr[1], ptext))

    for n, (name, expected, build) in enumerate(D, 1):
        g = build()
        rc, cls, last, out = score(g)
        got = "admitted" if last.startswith("admitted=1/1") and rc == 0 else "rejected"
        ok = got == expected
        lines.append("control=%s expected=%s observed=%s clauses=%s rc=%d ok=%d"
                     % (name, expected, last, cls, rc, ok))
        open(os.path.join(SEAT, "runs", "%02d-%s.txt" % (n, name)), "w").write(
            head + "control=%s expected=%s\n" % (name, expected) + out + "\n")
        results.append((name, expected, ok, cls, g[R.ENTRY]))

    # rule matrix
    mat = ["", "RULES " + " ".join(k for k, _ in RULES), ""]
    for name, expected, ok, cls, text in results:
        mat.append("%-32s %s  rows=%d" % (name, rule_row(text), len(text.split("\n"))))
    mat.append("")
    mat.append("M-rules: 1 = the rule holds for that fixture's entry text.")
    open(os.path.join(SEAT, "rules-matrix.txt"), "w").write("\n".join(mat) + "\n")

    adm = sum(1 for _, e, ok, _, _ in results if e == "admitted" and ok)
    rej = sum(1 for _, e, ok, _, _ in results if e == "rejected" and ok)
    others = [r[0] for r in results if not r[2]]
    lines += ["", "admitted-as-expected=%d rejected-as-expected=%d unexpected=%s"
              % (adm, rej, others or "-"),
              "lane git status --porcelain at the end: %s"
              % (noharm.strip().replace("\n", " | ") or "<empty>"),
              "CTL_DONOTHING: fixtures=%d admitted=%d rejected=%d"
              % (len(results), sum(1 for r in results if r[1] == "admitted"),
                 sum(1 for r in results if r[1] == "rejected"))]
    open(os.path.join(SEAT, "summary.txt"), "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))
    # the D15 swap table, for the report
    if "swaps" in _d15_cache:
        sw = ["id receipt original_line alt_line distance alt_quote"]
        for i, fn, a, b, dd, cand in _d15_cache["swaps"]:
            sw.append("%s %s %d %d %d %s" % (i, fn, a, b, dd, cand))
        open(os.path.join(SEAT, "d15-swaps.txt"), "w").write("\n".join(sw) + "\n")
        print("\n".join(sw))
    return 0 if not others else 1


if __name__ == "__main__":
    sys.exit(main())
