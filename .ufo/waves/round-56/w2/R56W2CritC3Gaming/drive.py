#!/usr/bin/env python3
"""Gaming variants for PRED-C3-r56-v2 (seat R56W2CritC3Gaming). Reads the lane via git objects only.
Writes only under S. Each variant = one commit on a fixture clone (temporary index), scored by the REAL counter."""
import importlib.util, os, re, subprocess, sys

S = "/fast/scratch/hyaku/mado-r56/R56W2CritC3Gaming"
L = "/home/vgpnk/Projects/shokunin/mado-shokunin"
R = "28fc86ac2359ec27406d8a2c63bef82ea6e947ed"
PRE = "323a69c9014da1cebece67bb111b70a5630f4a60"
BASE = "13f0acbe3a15da2d9c08357a576d91dcadc85273"
D = S + "/fx"
WORK = S + "/work"
COUNTER = S + "/counter.py"
ENV = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": WORK, "TMPDIR": WORK,
       "LC_ALL": "C.UTF-8", "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null"}
REG = "corpus/SOURCES.md"
ALLOW = ".ufo/waves/round-56/c3-name-only.tsv"
ROWRE = re.compile(r"^ {0,3}\|\s*(S[0-9]{3,})\s*\|")
TOK = r"(?<![A-Za-z0-9])%s(?![0-9])"
FENCE = re.compile(rb"^ {0,3}(```|~~~)")
RES = []


def run(args, input=None, env=None, check=True):
    p = subprocess.run(args, input=input, capture_output=True, env=env or ENV, cwd=S)
    if check and p.returncode != 0:
        raise SystemExit("FAILED %s: %s" % (" ".join(args[:6]), p.stderr.decode("utf-8", "replace")[:400]))
    return p


def g(*a, input=None, env=None, check=True):
    return run(["git", "-C", D, *a], input=input, env=env, check=check)


def blob(path, rev=R):
    return g("cat-file", "blob", "%s:%s" % (rev, path)).stdout


def txt(path, rev=R):
    return blob(path, rev).decode("utf-8")


def setup():
    os.makedirs(WORK, exist_ok=True)
    if not os.path.isdir(D):
        run(["git", "clone", "-q", "--shared", "--no-checkout", L, D])
    top = g("rev-parse", "--show-toplevel").stdout.decode().strip()
    assert os.path.realpath(top) == os.path.realpath(D), top
    print("fixture toplevel:", top)


def commit(name, edits):
    idx = "%s/idx-%s" % (S, name)
    if os.path.exists(idx):
        os.remove(idx)
    env = dict(ENV, GIT_INDEX_FILE=idx)
    g("read-tree", R, env=env)
    for path, data in edits.items():
        if data is None:
            g("update-index", "--force-remove", "--", path, env=env)
        else:
            if isinstance(data, str):
                data = data.encode("utf-8")
            oid = g("hash-object", "-w", "--stdin", input=data).stdout.decode().strip()
            g("update-index", "--add", "--cacheinfo", "100644,%s,%s" % (oid, path), env=env)
    tree = g("write-tree", env=env).stdout.decode().strip()
    return g("-c", "user.name=ctl", "-c", "user.email=ctl@ctl", "commit-tree", tree, "-p", R, "-m", name).stdout.decode().strip()


def score(name, c):
    p = subprocess.run(["python3", "-I", COUNTER, "--repo", D, "--rev", c, "--work", WORK, "--detail"],
                       capture_output=True, text=True, env=ENV, cwd=S)
    line = p.stdout.strip() or "(no stdout)"
    err = " | ".join(p.stderr.strip().splitlines()[:3])
    return p.returncode, line, err


def V(name, edits, note):
    c = commit(name, edits)
    rc, line, err = score(name, c)
    RES.append((name, rc, line, err, note, c))
    print("== %s rc=%s\n   %s\n   stderr: %s" % (name, rc, line, err[:400]), flush=True)


# ---- registry cell helpers (cell 11 = used-by = parts[11] of ln.split('|'))
def cell_items(c):
    return [x.strip() for x in c.split(",") if x.strip() not in ("", "-", "\u2014")]


def cell_str(items):
    return " " + ", ".join(items) + " " if items else " - "


def apply_rows(reg, fn):
    out = []
    for ln in reg.split("\n"):
        m = ROWRE.match(ln)
        if m:
            parts = ln.split("|")
            assert len(parts) == 13, (m.group(1), len(parts))
            new = fn(m.group(1), parts[11])
            if new != parts[11]:
                parts[11] = new
                ln = "|".join(parts)
        out.append(ln)
    return "\n".join(out)


def rm_path(p):
    def f(c):
        items = cell_items(c)
        return cell_str([x for x in items if x != p]) if p in items else c
    return f


def add_path(p):
    def f(c):
        items = cell_items(c)
        return c if p in items else cell_str(items + [p])
    return f


def row_fn(sid, f):
    return lambda i, c: f(c) if i == sid else c


# ---- entry helpers, mirroring the counter's fence rule exactly
def outside_idx(text):
    fence = None
    idx = []
    for i, line in enumerate(text.split("\n")):
        m = FENCE.match(line.encode())
        if fence is not None:
            if m and m.group(1).decode() == fence:
                fence = None
            continue
        if m:
            fence = m.group(1).decode()
            continue
        idx.append(i)
    return idx


def cite_idx(text, sid):
    lines = text.split("\n")
    return [i for i in outside_idx(text) if re.search(TOK % sid, lines[i])]


def drop_tok(text, sid):
    return re.sub(TOK % sid, sid[0] + "---", text)


def suffix_line(text, i, suf=" x"):
    lines = text.split("\n")
    lines[i] += suf
    return "\n".join(lines)


def main():
    setup()
    spec = importlib.util.spec_from_file_location("cnt", COUNTER)
    cnt = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cnt)
    Rr = cnt.Repo(D, R, WORK)
    rows, ub, ents, pl = cnt.pair_data(Rr)
    allow = cnt.parse_allow(Rr.regular_file(ALLOW))
    Rb = cnt.Repo(D, BASE, WORK)
    _, ub0, _, pl0 = cnt.pair_data(Rb)
    s_ = lambda b: b.decode("utf-8")
    PR = {(s_(s), s_(p)) for s, p in pl}
    UB = {s_(k): {s_(x) for x in v} for k, v in ub.items()}
    UB0 = {s_(k): {s_(x) for x in v} for k, v in ub0.items()}
    BM = {(s_(s), s_(p)) for s, p in pl0 if p not in ub0.get(s, set())}
    A = {(s_(s), s_(p)) for s, p in allow}
    ENT = {s_(p): d.decode("utf-8") for p, d in ents.items()}
    IDS = []
    for r in rows:
        if s_(r) not in IDS:
            IDS.append(s_(r))
    print("counts: pairs(R)=%d allow=%d base_missing=%d entries=%d unique_ids=%d rows=%d"
          % (len(PR), len(A), len(BM), len(ENT), len(IDS), len(rows)))
    assert len(A) == 24 and len(BM) == 65

    reg = txt(REG)
    allow_bytes = blob(ALLOW)

    bm_non = sorted(x for x in BM if x not in A and x in PR)
    P_bm = bm_non[0]
    assert P_bm[1] in UB[P_bm[0]], "P_bm must be filled at R"
    bf = sorted(x for x in PR if x not in BM and x not in A and x[1] in UB0.get(x[0], set()))
    P_bf = bf[0]
    pairs_of = {}
    for s, p in PR:
        pairs_of.setdefault(p, set()).add(s)
    E1 = next(p for p in sorted(pairs_of) if all((s, p) not in A and (s, p) not in BM and p in UB0.get(s, set())
                                               for s in pairs_of[p]))
    E2 = next(p for p in sorted(pairs_of) if any((s, p) in BM and (s, p) not in A for s in pairs_of[p])
              and not any((s, p) in A for s in pairs_of[p]))
    E2_bm = sorted(s for s in pairs_of[E2] if (s, E2) in BM)
    A_sorted = sorted(A)
    SA, PA = A_sorted[0]

    def src_line(text):
        lines = text.split("\n")
        for i in range(min(15, len(lines))):
            if lines[i].startswith("source:") and re.search(r"S[0-9]{3}", lines[i]):
                return i
        return None

    E_src = next(p for p in sorted(ENT) if src_line(ENT[p]) is not None and len(ENT[p].split("\n")) >= 25)
    X = IDS[0]
    hp = next(p for p in sorted(ENT) if (X, p) not in PR and p not in UB.get(X, set()))
    print("picks: P_bm=%s P_bf=%s E1=%s E2=%s E2_bm=%s A0=%s E_src=%s X=%s hp=%s"
          % (P_bm, P_bf, E1, E2, E2_bm, A_sorted[0], E_src, X, hp))

    # ---------------- V00 control: same tree, new commit
    V("V00-nochange", {}, "control: no edit")

    # ---------------- (a) base pair left out of used-by + suffix on its citing line
    s, p = P_bm
    V("a1-missing-noline", {REG: apply_rows(reg, row_fn(s, rm_path(p)))},
      "a: non-allowlist base-missing pair removed from used-by, citing line untouched")
    t = ENT[p]
    i = cite_idx(t, s)[0]
    V("a2-missing-suffix", {REG: apply_rows(reg, row_fn(s, rm_path(p))), p: suffix_line(t, i)},
      "a: same plus harmless suffix on the citing line (line-sha changes; non-allowlist)")
    s2, p2 = P_bf
    V("a3-filled-suffix-only", {p2: suffix_line(ENT[p2], cite_idx(ENT[p2], s2)[0])},
      "a: filled non-allowlist pair, suffix only (no leg should care)")
    t = ENT[PA]
    V("a4-allowlist-suffix", {PA: suffix_line(t, cite_idx(t, SA)[0])},
      "a: allowlist pair, suffix on its first citing line (stale expected)")

    # ---------------- (b) delete citation + used-by of a filled pair
    t = ENT[P_bm[1]]
    V("b1-basemissing-del-both", {REG: apply_rows(reg, row_fn(P_bm[0], rm_path(P_bm[1]))),
                                  P_bm[1]: drop_tok(t, P_bm[0])},
      "b: base-missing pair: citation and used-by both deleted (lost expected)")
    t = ENT[P_bf[1]]
    V("b2-basefilled-del-both", {REG: apply_rows(reg, row_fn(P_bf[0], rm_path(P_bf[1]))),
                                 P_bf[1]: drop_tok(t, P_bf[0])},
      "b: BASE-FILLED pair (outside lost set): citation and used-by both deleted")
    V("b3-basefilled-del-cite-only", {P_bf[1]: drop_tok(t, P_bf[0])},
      "b: base-filled pair, citation deleted, used-by kept (extra expected)")

    # ---------------- (c) new entry citing every row
    probe = "corpus/knowledge/probe-all-cites-r56.md"
    ptxt = "source: S001\n\nMentions every row: " + " ".join(IDS) + "\n"
    V("c1-newentry-all-mentions", {probe: ptxt},
      "c: new entry naming every row in prose, registry untouched (missing expected)")
    V("c2-newentry-all-filled", {probe: ptxt,
                                 REG: apply_rows(reg, lambda sid, c: add_path(probe)(c) if sid in IDS else c)},
      "c: same entry, used-by of every row filled with it (fix)")
    V("c3-newentry-all-fenced", {probe: "```\n" + " ".join(IDS) + "\n```\n"},
      "c: same mentions inside a ``` block, registry untouched")

    # ---------------- (d) trailing space on every allowlist citing line
    by_entry = {}
    for sa, pa in A:
        by_entry.setdefault(pa, set()).update(cite_idx(ENT[pa], sa))
    edits = {}
    for pa, idxs in by_entry.items():
        lines = ENT[pa].split("\n")
        for i in idxs:
            lines[i] += " "
        edits[pa] = "\n".join(lines)
    V("d1-allowlist-trailing-space", edits, "d: trailing space on every citing line of all 24 allowlist pairs")

    # ---------------- (e) source line past line 15
    text = ENT[E_src]
    lines = text.split("\n")
    si = src_line(text)
    V("e0-source-dangling-inplace", {E_src: "\n".join(l + " S999" if k == si else l for k, l in enumerate(lines))},
      "e: control: S999 appended to source line in place (dangling expected)")
    lines2 = text.split("\n")
    ln = lines2.pop(si) + " S999"
    lines2.insert(20, ln)
    V("e1-source-moved-past-15", {E_src: "\n".join(lines2)},
      "e: S999 on the source line, source line moved to line 21 (dangling bypass expected)")

    # ---------------- (f) rename entries
    new1 = "corpus/knowledge/probe-renamed-f1-r56.md"
    V("f1-rename-filled-only", {E1: None, new1: ENT[E1],
                                REG: apply_rows(reg, lambda sid, c: c.replace(E1, new1))},
      "f: entry with only base-filled pairs renamed, used-by updated")
    new2 = "corpus/knowledge/probe-renamed-f2-r56.md"
    V("f2-rename-basemissing-usedby-updated", {E2: None, new2: ENT[E2],
                                               REG: apply_rows(reg, lambda sid, c: c.replace(E2, new2))},
      "f: entry with base-missing pairs renamed, used-by updated (honest rename)")
    V("f3-rename-usedby-not-updated", {E2: None, new2: ENT[E2]},
      "f: same rename, used-by left at the old path")

    # ---------------- (g) allowlist bytes changed, same content, CRLF
    V("g1-allowlist-crlf", {ALLOW: allow_bytes.replace(b"\n", b"\r\n")},
      "g: allowlist with CRLF line endings")

    # ---------------- (h) HTML comments with S-tokens
    V("h1-comment-new-pair", {hp: ENT[hp] + "\n<!-- %s -->\n" % X},
      "h: HTML comment citing a row not in used-by (missing expected)")
    V("h2-comment-allowlist-pair", {PA: ENT[PA] + "\n<!-- %s -->\n" % SA},
      "h: HTML comment citing an allowlist pair (stale expected)")

    # ---------------- (i) fence games
    pn = "corpus/knowledge/probe-fence-r56.md"
    V("i1-info-string-backtick-fence", {pn: "```a`b\n\nCites S001 here.\n"},
      "i: '```a`b' is not a fence in CommonMark; counter opens a fence and hides the citation")
    V("i1c-control-plain", {pn: "Cites S001 here.\n"}, "i: control, plain citation")
    V("i2-html-comment-opens-fence", {pn: "<!--\n```\n-->\n\nCites S001 here.\n"},
      "i: a ``` inside an HTML comment opens a counter-fence; the citation after '-->' is prose")
    V("i3-entity-citation", {pn: "Cites S&#48;01 here.\n"},
      "i: S&#48;01 renders as S001; the counter reads no token")
    V("i3c-control-literal", {pn: "Cites S001 here.\n"}, "i: control, literal token")
    V("i4-zwsp-citation", {pn: "Cites S\u200b001 here.\n"},
      "i: zero-width space inside the token")
    t = ENT[P_bf[1]]
    lines = t.split("\n")
    li = cite_idx(t, P_bf[0])[0]
    lines[li:li + 1] = ["```", "~~~", lines[li], "~~~", "```"]
    V("i5-tilde-inside-backtick-fence", {P_bf[1]: "\n".join(lines)},
      "i: ~~~ inside a ``` block around a filled citation; used-by kept (extra expected, consistent)")

    # ---------------- (j) used-by cell with a negative statement
    s, p = P_bm
    V("j1-usedby-negation", {REG: apply_rows(reg, lambda sid, c: (" NOT used by " + p + " ") if sid == s and False else (
        cell_str([x for x in cell_items(c) if x != p]) + "NOT used by " + p + " " if sid == s else c))},
      "j: used-by cell says 'NOT used by <entry>' yet the path string is present")

    # ---------------- (k) body citation of a token that is not a row
    V("k1-body-nonrow-token", {pn: "Cites S777 which has no row.\n"},
      "k: body token S777 names no registry row (ignored by design)")

    # ---------------- registry diff check (PRE -> R and BASE -> R)
    reg_diff(PRE, A, BM)

    out = S + "/results.txt"
    with open(out, "w") as fh:
        for name, rc, line, err, note, c in RES:
            fh.write("%s\trc=%s\t%s\n    note: %s\n    commit: %s\n    stderr: %s\n" % (name, rc, line, note, c, err))
    print("wrote", out)


def reg_diff(prev, A, BM):
    pre = txt(REG, prev)
    post = txt(REG, R)

    def rows(t):
        out = {}
        order = []
        for ln in t.split("\n"):
            m = ROWRE.match(ln)
            if m:
                parts = ln.split("|")
                assert len(parts) == 13, (m.group(1), len(parts))
                sid = m.group(1)
                assert sid not in out, "duplicate row " + sid
                out[sid] = parts
                order.append(sid)
        return out, order

    a, ao = rows(pre)
    b, bo = rows(post)
    new_ids = [x for x in bo if x not in a]
    gone = [x for x in ao if x not in b]
    print("REGDIFF %s->R: rows pre=%d post=%d new_ids=%s gone=%s" % (prev[:8], len(a), len(b), new_ids, gone))
    changed = []
    cells = set()
    added = set()
    removed = set()
    for sid in ao:
        if sid not in b or a[sid] == b[sid]:
            continue
        changed.append(sid)
        for i, (x, y) in enumerate(zip(a[sid], b[sid])):
            if x != y:
                cells.add(i)
        ax = set(cell_items(a[sid][11]))
        bx = set(cell_items(b[sid][11]))
        added |= {(sid, x) for x in bx - ax}
        removed |= {(sid, x) for x in ax - bx}
    print("REGDIFF changed rows=%d changed part indices=%s (part 11 = cell 11)" % (len(changed), sorted(cells)))
    print("REGDIFF added used-by pairs=%d removed=%d" % (len(added), len(removed)))
    fill = {(s, p) for s, p in added if (s, p) not in A}
    print("REGDIFF added pairs that are non-allowlist base-missing: %d (of %d added)"
          % (len({(s, p) for s, p in fill if (s, p) in BM}), len(fill)))
    print("REGDIFF rows whose used-by cell contains ' corpus/' (space separator):",
          [sid for sid in b if re.search(r"\.md corpus/", b[sid][11])])
    for sid in new_ids:
        print("REGDIFF new row %s used-by: %s" % (sid, b[sid][11].strip()))
    print("REGDIFF changed row ids:", ",".join(changed))


if __name__ == "__main__":
    main()
