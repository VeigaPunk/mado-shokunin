#!/usr/bin/env python3
"""Falsify05 reference implementation of the FROZEN C2 counter predicate (round 52).

Purpose: falsification harness, not a lane artifact. It implements the mechanically
checkable half of the frozen C2 clause and nothing else:

  registration.md C2: "A counter checks proposition count, row/pin/quote bindings and
  index; outside reviewer judges source truth."
  claims-frozen.md C2: "each material factual proposition maps to a pinned source quote
  <=25 words and explicit support rationale. A new committed counter checks proposition
  count, row/pin/quote bindings and complete mapping"

Directory-parameterised (no git, no vcs, no network):
  --root DIR       tree holding corpus/ and pins/   (the "revision" under test)
  --base DIR       tree of the frozen base revision (no-work control)
  --entry REL      entry path relative to root
  --format json|text

Clauses:
  index     entry is named by a corpus/README.md table row
  absent    entry file absent + no index row at base  -> control TARGET_MISSED
  count     >=4 proposition rows in the entry's proposition table
  bind      per row: S### row exists, opened=OPENED, status=mined; pin named in the
            pin manifest and present under pins/; quote <=25 words and verbatim
            (whitespace-collapsed) inside the cited line span; rationale non-empty
  complete  variant A (declared): every proposition row carries a row/pin/quote/rationale
            variant B (sentence): every substantive declarative sentence of the body is
            named by some proposition row (extraction rule the harness states explicitly)

Exit 0 only when every enabled clause passes.
"""
import argparse
import json
import os
import re
import sys

OPENED = "2026-10-27"
MAX_QUOTE_WORDS = 25
MIN_PROPS = 4
MIN_RATIONALE_WORDS = 4

CELL = re.compile(r"^S(\d{3,})$")


def collapse(s):
    return re.sub(r"\s+", " ", s or "").strip()


def words(s):
    return collapse(s).split()


def cells_of(row):
    return [c.strip() for c in row.strip().strip("|").split("|")]


def is_rule(cells):
    return bool(cells) and all(re.fullmatch(r":?-{2,}:?", c or "") for c in cells)


def clean(cell):
    return re.sub(r"[`*\s]+", "", cell or "")


def read_lines(path):
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        return fh.read().splitlines()


def unfenced(lines):
    out, fence = [], False
    for line in lines:
        if line.lstrip().startswith("```"):
            fence = not fence
            continue
        if not fence:
            out.append(line)
    return out


def tables(lines):
    """[(header cells, [row cells])] for consecutive pipe blocks (fences excluded)."""
    blocks, cur = [], []
    for line in unfenced(lines):
        if line.strip().startswith("|"):
            cur.append(line.strip())
            continue
        if len(cur) >= 2:
            blocks.append(cur)
        cur = []
    if len(cur) >= 2:
        blocks.append(cur)
    for block in blocks:
        cells = [cells_of(r) for r in block]
        yield cells[0], [c for c in cells[1:] if not is_rule(c)]


# ---------------------------------------------------------------- registry / manifest

def registry(path):
    rows, header = {}, None
    for line in read_lines(path):
        s = line.strip()
        if not s.startswith("|"):
            continue
        cells = cells_of(s)
        if header is None:
            low = [c.lower() for c in cells]
            if low and low[0] == "id" and "status" in low and "opened" in low:
                header = low
            continue
        if is_rule(cells):
            continue
        m = CELL.match(clean(cells[0]))
        if not m:
            continue
        rows["S" + m.group(1)] = dict(zip(header, cells))
    if header is None:
        raise SystemExit("registry header not found: %s" % path)
    return rows


def manifest(entry_lines):
    """pin -> {row,file}. Header cell 0 starts with 'pin'."""
    rowkeys = ("row", "rows", "s-row", "srow", "registry row", "source row", "sid", "id")
    out = {}
    for header, rows in tables(entry_lines):
        if not header:
            continue
        low = [clean(c).lower() for c in header]
        if not re.match(r"pin\b", low[0]):
            continue
        ridx = next((i for i, c in enumerate(low) if c in rowkeys), None)
        for cells in rows:
            name = re.sub(r"[`*\s]+", "", cells[0] if cells else "")
            if not name:
                continue
            declared = clean(cells[ridx]) if ridx is not None and ridx < len(cells) else ""
            out[name] = {"row": declared if re.fullmatch(r"S\d{3,}", declared) else ""}
    return out


# ---------------------------------------------------------------- proposition table

PROP_HEADERS = ("#", "id", "prop", "proposition")


def prop_table(entry_lines):
    """The proposition->source table, or (None, reason).

    Frozen predicate has no declared column layout; the harness accepts any table whose
    header names a proposition column and a quote column, which is the loosest faithful
    reading of 'record a proposition->source table'.
    """
    for header, rows in tables(entry_lines):
        low = [clean(c).lower() for c in header]
        pidx = next((i for i, c in enumerate(low)
                     if c.startswith("prop") or c in ("claim", "statement")), None)
        qidx = next((i for i, c in enumerate(low) if c.startswith("quot")), None)
        if pidx is not None and qidx is not None:
            return header, low, [(i, cells) for i, cells in enumerate(rows)], (pidx, qidx)
    return None, None, None, None


# ---------------------------------------------------------------- clauses

def clause_index(root, entry_rel):
    readme = os.path.join(root, "corpus", "README.md")
    if not os.path.exists(readme):
        return False, "readme=absent"
    name = os.path.basename(entry_rel)
    for _header, rows in tables(read_lines(readme)):
        for cells in rows:
            if any(name in c and "knowledge/" in c for c in cells):
                return True, "index_row=%s" % collapse(cells[0] if cells else name)
    return False, "index_row=absent"


def clause_absent(base, entry_rel):
    """No-work control: entry absent at base and not indexed at base."""
    if os.path.exists(os.path.join(base, entry_rel)):
        return False, "entry_present_at_base"
    ok, detail = clause_index(base, entry_rel)
    if ok:
        return False, "indexed_at_base:%s" % detail
    return True, "entry_absent_and_unindexed_at_base"


def clause_count(entry_lines):
    header, _low, rows, idx = prop_table(entry_lines)
    if header is None:
        return False, "prop_table=absent"
    prows = [cells for _i, cells in rows]
    return (len(prows) >= MIN_PROPS,
            "props=%d min=%d" % (len(prows), MIN_PROPS))


def quote_location(path, quote):
    """Line number where the collapsed quote starts in the pin file, or None."""
    q = collapse(quote)
    lines = read_lines(path)
    joined, spans = "", []
    for i, line in enumerate(lines, 1):
        t = collapse(line)
        if not t:
            continue
        spans.append((len(joined), i))
        joined += t + " "
    pos = joined.find(q)
    if pos < 0:
        return None
    line_no = 1
    for start, i in spans:
        if start <= pos:
            line_no = i
        else:
            break
    return line_no


def span_of(path, first, last):
    lines = read_lines(path)
    if first < 1 or first > len(lines):
        return None
    return "\n".join(lines[first - 1:min(last, len(lines))])


def pin_index(root):
    pdir = os.path.join(root, "pins")
    return {n: os.path.join(pdir, n) for n in sorted(os.listdir(pdir))} if os.path.isdir(pdir) else {}


def resolve_pin(token, pins):
    """pin file for a cell/file token: exact, case-only, then suffix-stem (house style)."""
    base = token.rsplit("/", 1)[-1]
    if base in pins:
        return base
    cands = [k for k in pins if k.lower() == base.lower()]
    if len(cands) == 1:
        return cands[0]
    stem = base.rsplit(".", 1)[0].lower()
    ext = base.rsplit(".", 1)[-1].lower() if "." in base else ""
    cands = [k for k in pins if k.rsplit(".", 1)[0].lower().endswith("-" + stem)]
    same = [k for k in cands if k.rsplit(".", 1)[-1].lower() == ext]
    if len(same) == 1:
        return same[0]
    stem2 = stem.replace("-", "")
    cands2 = [k for k in pins if k.rsplit(".", 1)[0].lower().replace("-", "").endswith(stem2)
              and k.rsplit(".", 1)[-1].lower() == ext]
    if len(cands2) == 1:
        return cands2[0]
    return cands[0] if len(cands) == 1 else ""


ANCHOR_FILE = re.compile(r"([A-Za-z0-9._/-]+\.(?:cpp|hpp|h|md|rst|txt))")


def clause_bind(root, entry_lines, pin_scope="strict", quote_scope="anchor"):
    header, low, rows, idx = prop_table(entry_lines)
    if header is None:
        return False, ["prop_table=absent"]
    pidx, qidx = idx
    rest = [i for i in range(len(low)) if i not in (pidx, qidx)]
    ridx = next((i for i in rest if low[i] in ("row", "s-row", "srow", "registry row")), None)
    pinidx = next((i for i in rest if low[i].startswith("pin")), None)
    ratidx = next((i for i in rest if low[i].startswith(("rat", "reason", "why"))), None)

    reg = registry(os.path.join(root, "corpus", "SOURCES.md"))
    man = manifest(entry_lines)
    pins = pin_index(root)
    details, okall, prev = [], True, ""

    for n, cells in rows:
        tag = "p%d" % (n + 1)
        bad = []
        prop = cells[pidx] if pidx < len(cells) else ""
        quote = (cells[qidx] if qidx < len(cells) else "").strip().strip("`").strip()
        rowid = clean(cells[ridx]) if ridx is not None and ridx < len(cells) else ""
        raw_pin = cells[pinidx] if pinidx is not None and pinidx < len(cells) else ""
        pin = re.sub(r"[`*\s]+", "", raw_pin)
        rationale = cells[ratidx] if ratidx is not None and ratidx < len(cells) else ""

        if not prop:
            bad.append("prop_empty")
        if not rowid:
            bad.append("row_empty")
        else:
            meta = reg.get(rowid)
            if meta is None:
                bad.append("row_absent:%s" % rowid)
            else:
                if clean(meta.get("status", "")).lower() != "mined":
                    bad.append("row_status")
                if clean(meta.get("opened", "")) != OPENED:
                    bad.append("row_opened:%s" % clean(meta.get("opened", "")))

        loc = re.search(r"([A-Za-z0-9._/-]+):(\d+)(?:-(\d+))?", pin)
        file_tok, first, last = "", 0, 0
        if loc:
            file_tok, first = loc.group(1), int(loc.group(2))
            last = int(loc.group(3)) if loc.group(3) else first
        elif re.match(r"^:(\d+)(?:-(\d+))?$", pin):
            first = int(pin[1:].split("-")[0])
            last = int(pin.split("-")[1]) if "-" in pin else first
            if pin_scope == "inherit":
                file_tok = prev.rsplit("/", 1)[-1]
            elif pin_scope == "anchor" and rowid in reg:
                m = ANCHOR_FILE.search(reg[rowid].get("anchor", ""))
                file_tok = m.group(1) if m else ""
            if not file_tok and pin_scope != "strict":
                bad.append("pin_unresolved")
            elif pin_scope == "strict":
                bad.append("pin_path_absent:%s" % pin)
        else:
            bad.append("pin_cell_unparsed:%s" % (pin or "-"))

        pin_file = resolve_pin(file_tok, pins) if file_tok else ""
        if file_tok and not pin_file:
            bad.append("pin_absent:%s" % file_tok)
        prev = pin_file or prev

        if pin_file and pin_file in man and man[pin_file]["row"] and rowid \
                and man[pin_file]["row"] != rowid:
            bad.append("pin_row_mismatch")

        if not quote:
            bad.append("quote_empty")
        else:
            qw = len(words(quote))
            if qw > MAX_QUOTE_WORDS:
                bad.append("quote_words:%d" % qw)
            if not first:
                bad.append("pin_span_absent")
            else:
                if not pin_file:
                    bad.append("pin_line_out_of_range")
                elif quote_scope == "file":
                    at = quote_location(pins[pin_file], quote)
                    if at is None:
                        bad.append("quote_not_at_pin")
                    elif not (first <= at <= last):
                        bad.append("quote_elsewhere:%d" % at)
                else:
                    span = span_of(pins[pin_file], first, last)
                    if span is None:
                        bad.append("pin_line_out_of_range")
                    elif collapse(quote) not in collapse(span):
                        bad.append("quote_not_at_pin")
        if len(words(rationale)) < MIN_RATIONALE_WORDS:
            bad.append("rationale_short")

        state = "ok" if not bad else ",".join(bad)
        okall = okall and not bad
        details.append("%s row=%s pin=%s qw=%d %s" % (tag, rowid or "-", pin or "-",
                                                      len(words(quote)), state))
    return okall, details


SENT_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z`(])")


def body_sentences(entry_lines):
    """Substantive declarative sentences of the prose body.

    Stated extraction rule (the frozen predicate does not name one):
      - fenced blocks, table rows, headings and list items are dropped;
      - lines carrying a source:/held:/lane:/round:/base:/verified-at:/recheck:/ground:/
        census:/exit=/obs marker are dropped (provenance, not propositions);
      - wrapped lines of one paragraph are joined before sentence splitting;
      - sentences with >=8 words are kept.
    """
    paras, buf = [], []
    for line in unfenced(entry_lines):
        s = line.strip()
        skip = (not s or s.startswith("#") or s.startswith("|") or s.startswith("- ")
                or re.match(r"(source|held|lane|round|wave|base|verified-at|recheck|ground|"
                            r"census|exit|obs)\b\s*[:=]", s, re.I))
        if skip:
            if buf:
                paras.append(" ".join(buf))
                buf = []
            continue
        buf.append(s)
    if buf:
        paras.append(" ".join(buf))
    out = []
    for para in paras:
        for sent in SENT_SPLIT.split(para):
            sent = collapse(sent)
            if len(words(sent)) >= 8:
                out.append(sent)
    return out


def clause_complete(entry_lines):
    header, _low, rows, idx = prop_table(entry_lines)
    if header is None:
        return False, "declared: prop_table=absent", "sentence: n/a"
    pidx, _qidx = idx
    declared_props = [collapse(cells[pidx]) for _i, cells in rows if pidx < len(cells)]
    declared_ok = all(declared_props)

    sents = body_sentences(entry_lines)
    mapped, fuzzy = 0, 0
    for sent in sents:
        stoks = {t.lower() for t in re.findall(r"[A-Za-z0-9_]{2,}", sent)}
        exact = any(sent in p or p in sent for p in declared_props)
        near = False
        for p in declared_props:
            ptoks = {t.lower() for t in re.findall(r"[A-Za-z0-9_]{2,}", p)}
            if stoks and ptoks:
                j = len(stoks & ptoks) / len(stoks | ptoks)
                if j >= 0.6:
                    near = True
                    break
        mapped += 1 if exact else 0
        fuzzy += 1 if (exact or near) else 0
    sentence_ok = bool(sents) and mapped == len(sents)
    return (
        declared_ok,
        "declared: every table proposition non-empty=%s (n=%d)" % (declared_ok, len(declared_props)),
        "sentence: mapped=%d/%d substantive sentences (exact=%d, jaccard>=0.6=%d)"
        % (fuzzy, len(sents), mapped, fuzzy),
    )


def run(root, base, entry_rel, do_complete, pin_scope="strict", quote_scope="anchor"):
    root, base = os.path.abspath(root), os.path.abspath(base)
    path = os.path.join(root, entry_rel)
    res = {"root": root, "base": base, "entry": entry_rel}

    res["absent"] = dict(zip(("ok", "detail"), clause_absent(base, entry_rel)))
    if not os.path.exists(path):
        res["index"] = {"ok": False, "detail": "entry=absent"}
        res["count"] = {"ok": False, "detail": "entry=absent"}
        res["bind"] = {"ok": False, "detail": ["entry=absent"]}
        res["complete"] = {"ok": False, "detail": "entry=absent"}
        res["admitted"] = False
        return res

    lines = read_lines(path)
    res["index"] = dict(zip(("ok", "detail"), clause_index(root, entry_rel)))
    res["count"] = dict(zip(("ok", "detail"), clause_count(lines)))
    ok, detail = clause_bind(root, lines, pin_scope, quote_scope)
    res["bind"] = {"ok": ok, "detail": detail}
    if do_complete:
        d_ok, d_detail, s_detail = clause_complete(lines)
        res["complete"] = {"ok": d_ok, "detail": d_detail, "sentence_variant": s_detail}
        res["sentence_variant_ok"] = "pass" if s_detail.startswith("sentence: mapped=") and \
            s_detail.split("mapped=")[1].split("/")[0] == s_detail.split("/")[1].split()[0] else "fail"
    res["admitted"] = all(res[k]["ok"] for k in ("index", "count", "bind")) and \
        (res.get("complete", {}).get("ok", True))
    return res


def main(argv):
    ap = argparse.ArgumentParser(description="Falsify05 frozen-C2 reference counter")
    ap.add_argument("--root", required=True)
    ap.add_argument("--base", required=True)
    ap.add_argument("--entry", required=True, help="entry path relative to root")
    ap.add_argument("--no-complete", action="store_true")
    ap.add_argument("--format", choices=("json", "text"), default="text")
    ap.add_argument("--pin-scope", choices=("strict", "inherit", "anchor"),
                    default="strict", help="how a shorthand `:N-M` pin cell is resolved")
    ap.add_argument("--quote-scope", choices=("anchor", "file"), default="anchor",
                    help="anchor: quote must sit inside the cited span; file: anywhere in the pin")
    ap.add_argument("--dump-sentences", action="store_true",
                    help="list the sentence-variant universe and mapping state")
    a = ap.parse_args(argv)
    res = run(a.root, a.base, a.entry, not a.no_complete, a.pin_scope, a.quote_scope)
    if a.dump_sentences:
        path = os.path.join(os.path.abspath(a.root), a.entry)
        lines = read_lines(path)
        _h, _l, rows, idx = prop_table(lines)
        props = [collapse(cells[idx[0]]) for _i, cells in rows] if rows else []
        for i, sent in enumerate(body_sentences(lines), 1):
            state = "mapped" if any(sent in p or p in sent for p in props) else "UNMAPPED"
            print("S%02d %s %s" % (i, state, sent))
    if a.format == "json":
        print(json.dumps(res, indent=2))
    else:
        for k in ("absent", "index", "count", "bind", "complete"):
            v = res.get(k)
            if v is None:
                continue
            if isinstance(v["detail"], list):
                print("%-9s ok=%d" % (k, v["ok"]))
                for d in v["detail"]:
                    print("          %s" % d)
            else:
                print("%-9s ok=%d %s" % (k, v["ok"], v["detail"]))
                if "sentence_variant" in v:
                    print("%-9s %s" % ("strong", v["sentence_variant"]))
        print("admitted=%d" % (1 if res["admitted"] else 0))
    return 0 if res["admitted"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
