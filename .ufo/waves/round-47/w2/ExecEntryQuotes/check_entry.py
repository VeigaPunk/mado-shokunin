#!/usr/bin/env python3
"""ExecEntryQuotes - independent falsification of EVERY quote and locator of the
round-47 entry draft.

Target : .ufo/waves/round-47/w1/ScrEntry/entry.md
Pins   : the COMMITTED fetch pins at the frozen claim d7527d6
         (.ufo/waves/round-47/fetch/), read revision-addressed exactly as the frozen
         counter quality/counters/c2-r47-terminal-entry.py reads them.

Layers
  L1  locator well-formedness: every `name:a[-b]` resolves to a fetch pin and stays
      inside its line count; a locator naming a lane file is checked against the
      committed lane file at REV instead.
  L2  clause-d mirror (the frozen predicate's own semantics): every backticked or
      double-quoted span of 2..25 words immediately followed by `, loc` / ` at loc` /
      `(loc)` must occur verbatim (whitespace-collapsed, word-bounded) inside its pin,
      with at least one occurrence line inside [a,b].
  L3  clause-e mirror: >= 6 numbered steps, every step citing a script range in range.
  L4  stricter than the counter: a span hung on a locator whose text IS verbatim in
      the pin must be verbatim AT the cited range; a code span that is not verbatim
      must have all its pin tokens on the cited lines; a function name within 160
      characters before a multi-line script range must name the function whose body
      is that range.
  L5  census recomputation of every number on the "Census of the pinned bytes" line.
  L6  w1's own receipts re-run independently, plus the coverage gap of w1's claim
      (locators.txt `119 checked / 0 mismatched`, quotes.txt `10/10`).
  L7  pin reachability of every pin path the entry names, and of the digests it states.
  L8  mutation self-test: injected defects must be caught and the unmutated copy must
      reproduce the baseline finding set.

Exit 0 only when a mutation-free entry yields no HARD finding.
"""
import ast
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile

LANE = '/home/vgpnk/Projects/shokunin/mado-shokunin'
REV = 'd7527d608ad2b2e3cc398fdde34db7947b254a1a'
FETCH = '.ufo/waves/round-47/fetch/'
ENTRY_RELPATH_IN_LANE = '.ufo/waves/round-47/w1/ScrEntry/entry.md'
ENTRY = os.path.join(LANE, ENTRY_RELPATH_IN_LANE)

# ---- frozen counter semantics, re-implemented from quality/counters/c2-r47-terminal-entry.py
EXTS = (".md", ".bats", ".list", ".scd", ".py", ".xml", ".cpp", ".hpp", ".h",
        ".conf", ".txt", ".desktop", ".sh", ".json", ".toml")
LOC_RE = re.compile(r"(?<![\w./-])([A-Za-z0-9._/-]+):(\d+)(?:-(\d+))?(?!\d)")
QUOTE_RE = re.compile(
    r"(?:`([^`\n]{2,600})`|\"([^\"\n]{2,600})\")"
    r"\s*(?:,\s*| at\s+|,\s*\(|\(\s*)([A-Za-z0-9._/-]+:\d+(?:-\d+)?)")
LOC_SKIP = ("sha256", "sha1", "sha512", "md5", "https", "http")


def norm_q(s):
    return re.sub(r"\s+", " ", s).strip()


def is_word(c):
    return c.isalnum() or c == "_"


def collapse(text):
    out, lines, prev = [], [], True
    for ln, line in enumerate(text.split("\n"), 1):
        for ch in line + "\n":
            if ch.isspace():
                if not prev:
                    out.append(" ")
                    lines.append(ln)
                    prev = True
            else:
                out.append(ch)
                lines.append(ln)
                prev = False
    return "".join(out), lines


def occurrences(blob, nq):
    text, lines = collapse(blob.decode("utf-8", "replace"))
    out, start = [], 0
    while True:
        k = text.find(nq, start)
        if k < 0:
            return out
        before = text[k - 1] if k > 0 else " "
        after = text[k + len(nq)] if k + len(nq) < len(text) else " "
        if not (is_word(nq[0]) and is_word(before)) and not (is_word(nq[-1]) and is_word(after)):
            out.append(lines[k])
        start = k + 1


def locators(line):
    out = []
    for token, a, b in LOC_RE.findall(line):
        name = token.rsplit("/", 1)[-1].lower()
        if name in LOC_SKIP or re.fullmatch(r"[0-9a-f]{6,}", name):
            continue
        out.append((token, int(a), int(b) if b else int(a)))
    return out


def loc_items(line):
    """[(start, end, name, a, b)] locator ranges with their positions on the line."""
    out = []
    for m in LOC_RE.finditer(line):
        token, a, b = m.group(1), m.group(2), m.group(3)
        base = token.rsplit("/", 1)[-1].lower()
        if base in LOC_SKIP or re.fullmatch(r"[0-9a-f]{6,}", base):
            continue
        out.append((m.start(), m.end(), token, int(a), int(b) if b else int(a)))
    return out


def stem(base):
    b = base.rsplit("/", 1)[-1].lower()
    for ext in EXTS:
        if b.endswith(ext):
            return b[:-len(ext)]
    return b


def pin_index(pins):
    by_base = {}
    for name in pins:
        by_base.setdefault(name.rsplit("/", 1)[-1], []).append(name)
    return by_base


def resolve_pin(token, pins, by_base):
    base = token.rsplit("/", 1)[-1]
    if token in pins:
        return token
    if base in by_base and len(by_base[base]) == 1:
        return by_base[base][0]
    s = stem(base)
    if not s:
        return None
    cands = [n for n in pins if s in stem(n) or stem(n) in s]
    return cands[0] if len(cands) == 1 else None


def scan_spans(line):
    """[(start, end, text)] for markdown code spans, honouring backtick runs."""
    spans, i, n = [], 0, len(line)
    while i < n:
        if line[i] != '`':
            i += 1
            continue
        j = i
        while j < n and line[j] == '`':
            j += 1
        run = j - i
        k, close = j, -1
        while k < n:
            k = line.find('`' * run, k)
            if k < 0:
                break
            e = k
            while e < n and line[e] == '`':
                e += 1
            if e - k == run:
                close = e
                break
            k = e
        if close < 0:
            i = j
            continue
        spans.append((i, close, line[j:k]))
        i = close
    return spans


def git(*args):
    p = subprocess.run(["git", "-C", LANE, *args], capture_output=True,
                       env={k: v for k, v in os.environ.items() if not k.startswith("GIT_")})
    return p.stdout if p.returncode == 0 else None


def committed_pins():
    out = {}
    listing = (git("ls-tree", "-r", REV, FETCH) or b"").decode()
    for row in listing.splitlines():
        meta, path = row.split("\t", 1)
        mode, kind, sha = meta.split()
        if kind != "blob":
            continue
        out[path[len(FETCH):]] = git("show", "%s:%s" % (REV, path)) or b""
    return out


def lane_blob(path):
    b = git("show", "%s:%s" % (REV, path))
    return b.decode("utf-8", "replace").split("\n") if b is not None else None


FUNC_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)\(\)\s*\{?\s*$")


def function_bodies(script_lines):
    starts = [(m.group(1), i) for i, ln in enumerate(script_lines, 1)
              if (m := FUNC_RE.match(ln))]
    bodies = {}
    for idx, (name, s) in enumerate(starts):
        nxt = starts[idx + 1][1] if idx + 1 < len(starts) else len(script_lines) + 1
        e = None
        for j in range(nxt - 1, s - 1, -1):
            if script_lines[j - 1].strip() == "}":
                e = j
                break
        bodies[name] = (s, e)
    return bodies


FINDINGS = []


def note(kind, line, detail, hard=True):
    FINDINGS.append((kind, line, detail, hard))


def check_text(text, pins, by_base, bodies, script, verbose=False):
    """All L1-L4 rules over one entry text; returns the set of finding kinds."""
    lines = text.split("\n")
    kinds = set()

    def add(kind, ln, detail, hard=True):
        kinds.add(kind)
        if verbose:
            note(kind, ln, detail, hard)

    nscript = len(script)
    for ln, line in enumerate(lines, 1):
        for token, a, b in locators(line):
            pint = resolve_pin(token.rsplit(":", 1)[0], pins, by_base)
            if pint is None:
                add("LOCATOR_UNRESOLVED", ln, token, hard=False)
                continue
            plines = len(pins[pint].decode("utf-8", "replace").split("\n"))
            if a < 1 or b < a or b > plines:
                add("LOCATOR_OUT_OF_PIN", ln, "%s (%s has %d lines)" % (token, pint, plines))
        for m in QUOTE_RE.finditer(line):
            span = m.group(1) if m.group(1) is not None else m.group(2)
            token = m.group(3)
            q = norm_q(span)
            words = len(q.split())
            if words < 2:
                continue
            pint = resolve_pin(token.rsplit(":", 1)[0], pins, by_base)
            if pint is None:
                add("QUOTE_LOCATOR_UNRESOLVED", ln, "%s span=%r" % (token, q[:60]))
                continue
            rng = re.match(r".+:(\d+)(?:-(\d+))?$", token)
            a, b = int(rng.group(1)), int(rng.group(2) or rng.group(1))
            at = occurrences(pins[pint], q)
            if words > 25:
                add("QUOTE_TOO_LONG", ln, "%d words %r" % (words, q[:60]))
            elif not at:
                add("QUOTE_NOT_IN_PIN", ln, "pin=%s %r" % (pint, q[:80]))
            elif not any(a <= x <= b for x in at):
                add("QUOTE_OUT_OF_RANGE", ln, "pin=%s %r at=%s range=%d-%d"
                    % (pint, q[:60], at[:4], a, b))

        spans = scan_spans(line)
        for tokpos, tokend, token, a, b in loc_items(line):
            pint = resolve_pin(token, pins, by_base)
            if pint is None:
                continue
            pl = pins[pint].decode("utf-8", "replace").split("\n")
            rng_text = "\n".join(pl[a - 1:b]) if 1 <= a <= b <= len(pl) else ""
            before = [(s, e, t) for (s, e, t) in spans if e <= tokpos and tokpos - e < 200]
            # function-name binding for a multi-line script range
            if pint == "xdg-terminal-exec" and b > a and (b - a) >= 20:
                for s, e, t in reversed(before):
                    if tokpos - e > 160:
                        break
                    name = t.strip()
                    if name in bodies:
                        bs, be = bodies[name]
                        if (a, b) != (bs, be):
                            add("FUNC_RANGE_MISMATCH", ln,
                                "`%s` cited %d-%d, body %d-%d" % (name, a, b, bs, be))
                        break
            if not before:
                continue
            s, e, sp = before[-1]
            gap = line[e:tokpos]
            if not re.fullmatch(r"[\s(,\-–—:]*", gap) or len(gap) > 12:
                continue
            codeish = bool(re.search(r"[$={}()\[\]<>\*_\"'\\]|--", sp)) or len(sp.split()) >= 2
            if not codeish:
                continue           # a bare key/option word is a gloss, not a quote
            at_pin = occurrences(pins[pint], norm_q(sp))
            if at_pin:
                if not any(a <= x <= b for x in at_pin):
                    add("SPAN_VERBATIM_OFF_RANGE", ln, "`%s` verbatim at %s, cited %s:%d-%d"
                        % (sp[:50], at_pin[:4], pint, a, b))
                continue
            toks = [t for t in re.findall(r"[A-Za-z_][A-Za-z0-9_]{2,}", sp)]
            absent = [t for t in toks if t not in rng_text]
            if absent and len(absent) < len(toks):
                else_where = {t: occurrences(pins[pint], t)[:3] for t in absent}
                add("SPAN_TOKEN_NOT_ON_CITED_LINES", ln,
                    "`%s` cited %s:%d-%d missing %s (elsewhere %s)"
                    % (sp[:50], pint, a, b, absent, else_where), hard=False)

        # L4b: a multi-word span that IS verbatim in a pin but carries no locator
        attached = {sp for (s, e, sp) in spans
                    if any(abs(lp - e) <= 16 and
                           re.fullmatch(r"[\s(,\-\u2013\u2014:]*(?:at\s+)?", line[e:lp])
                           for lp, _le, _t, _a, _b in loc_items(line))}
        for s, e, sp in spans:
            if sp in attached or len(norm_q(sp).split()) < 3:
                continue
            home = {n: occurrences(pins[n], norm_q(sp))[:3] for n in pins}
            home = {n: v for n, v in home.items() if v}
            if home:
                add("QUOTE_NOT_LOCATED", ln, "`%s` verbatim in %s" % (sp[:44], home),
                    hard=False)
    return kinds


def main():
    pins = committed_pins()
    by_base = pin_index(pins)
    entry_lines = open(ENTRY, encoding="utf-8").read().split("\n")
    text = "\n".join(entry_lines)
    script = pins["xdg-terminal-exec"].decode("utf-8", "replace").split("\n")
    nscript = len(script)
    bodies = function_bodies(script)

    print("== pins at %s ==" % REV[:12])
    for n, b in sorted(pins.items()):
        print("  %-28s %-5d lines sha256=%s" % (
            n, len(b.decode('utf-8', 'replace').split("\n")), hashlib.sha256(b).hexdigest()))
    print("  script line count seen by the counter (split('\\n')) = %d" % nscript)

    # ---------------- L1/L2/L3/L4
    print("\n== L1-L4 (counter mirror + stricter) ==")
    kinds = check_text(text, pins, by_base, bodies, script, verbose=True)
    nloc = sum(len(locators(l)) for l in entry_lines)
    nq = sum(1 for l in entry_lines for m in QUOTE_RE.finditer(l)
             if len(norm_q(m.group(1) if m.group(1) is not None else m.group(2)).split()) >= 2)
    steps = [(ln, l) for ln, l in enumerate(entry_lines, 1) if re.match(r"^\d+\.\s", l)]
    cited = sum(1 for ln, l in steps
                if any(resolve_pin(t.rsplit(":", 1)[0], pins, by_base) == "xdg-terminal-exec"
                       and 1 <= a <= b <= nscript for t, a, b in locators(l)))
    print("  locators=%d  clause-d quotes(2..25w)=%d  steps=%d script_cited=%d"
          % (nloc, nq, len(steps), cited))
    if len(steps) < 6:
        note("TOO_FEW_STEPS", 0, str(len(steps)))
    if cited != len(steps):
        for ln, l in steps:
            if not any(resolve_pin(t.rsplit(":", 1)[0], pins, by_base) == "xdg-terminal-exec"
                       and 1 <= a <= b <= nscript for t, a, b in locators(l)):
                note("STEP_WITHOUT_SCRIPT_RANGE", ln, l[:70])
    for ln, line in enumerate(entry_lines, 1):
        for m in QUOTE_RE.finditer(line):
            span = m.group(1) if m.group(1) is not None else m.group(2)
            q = norm_q(span)
            if len(q.split()) < 2:
                continue
            pint = resolve_pin(m.group(3).rsplit(":", 1)[0], pins, by_base)
            rng = re.match(r".+:(\d+)(?:-(\d+))?$", m.group(3))
            a, b = int(rng.group(1)), int(rng.group(2) or rng.group(1))
            at = occurrences(pins[pint], q) if pint else []
            print("  quote line %-3d %-18s %2dw %-14s %r"
                  % (ln, pint or "UNRESOLVED", len(q.split()),
                     "AT_RANGE" if any(a <= x <= b for x in at) else
                     ("NOT_IN_PIN" if not at else "OUT_OF_RANGE"), q[:64]))

    # ---------------- L5 census
    print("\n== L5 census of the pinned bytes ==")
    raw = "\n".join(script)
    wc = len(script) - 1 if script and script[-1] == "" else len(script)
    census = {
        "script_lines": wc,
        "functions": sum(1 for ln in script if FUNC_RE.match(ln)),
        "directives": len(re.findall(r"^\s*/[a-z_]+(?::\*:\*)?\)", raw, re.M)),
        "print_data_kinds": sum(1 for k in ("id", "path", "content", "cmd")
                                if re.search(r'XTE__PRINT_DATA="\$XTE__PRINT_DATA ' + k + '"', raw)),
        "cache_header_fields": len(re.findall(r"^\s+\d+\) xte__cached_", raw, re.M)),
        "cache_hash_format": int(re.search(r"^\s*echo (\d+)$", raw, re.M).group(1)),
        "data_side_list_slots_per_data_dir": len(re.findall(
            r"XTE__CONFIGS=.*XDG_DATA_DIRS|xdg-terminal-exec/\$\{xte__desktop\}|xdg-terminal-exec/xdg-terminals\.list", raw)) and 2 or 0,
    }
    claimed = {}
    for line in entry_lines:
        if line.startswith("xdg-terminal-exec script_lines="):
            claimed = {k: int(v) for k, v in re.findall(r"([a-z_]+)=(\d+)", line)}
    print("  claimed    : %s" % claimed)
    print("  recomputed : %s" % census)
    for k, v in claimed.items():
        if census.get(k) != v:
            note("CENSUS_MISMATCH", 0, "%s claimed %d, recomputed %s" % (k, v, census.get(k)))
    if not claimed:
        note("CENSUS_LINE_MISSING", 0, "no census line found")

    # ---------------- L6 w1 receipts
    print("\n== L6 w1 receipts re-run ==")
    w1 = os.path.join(LANE, '.ufo/waves/round-47/w1/ScrEntry')
    tree = ast.parse(open(os.path.join(w1, 'verify_locators.py')).read())
    checks = None
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", "") == "checks":
            checks = ast.literal_eval(node.value)
    readme = pins["README.md"].decode("utf-8", "replace").split("\n")
    bad = [(f, n, sub) for f, n, sub in checks
           if n > len(script if f == 'S' else readme) or sub not in (script if f == 'S' else readme)[n - 1]]
    print("  their locator probes=%d, failing now=%d (receipt claims 119 checked / 0 mismatched)"
          % (len(checks), len(bad)))
    for b in bad:
        note("W1_PROBE_FAILS", 0, "%s:%d %r" % b)
    probed = {('R' if f == 'R' else 'S', n) for f, n, _ in checks}
    toks = []
    for ln, line in enumerate(entry_lines, 1):
        for t, a, b in locators(line):
            key = 'R' if t.rsplit(':', 1)[0].lower().startswith('readme') else 'S'
            toks.append((key, t, a, b))
    uncovered = [t for t in toks if not any(k == t[0] and t[2] <= n <= t[3] for k, n in probed)]
    print("  distinct locators=%d, with NO w1 probe line inside their range=%d"
          % (len(toks), len(uncovered)))
    for t in uncovered[:20]:
        print("    uncovered %s" % (t,))
    qsrc = open(os.path.join(w1, 'verify_quotes.py')).read()
    w1q = len(re.findall(r"\(\s*'[a-z0-9-]+',\s*'[SR]',", qsrc))
    print("  their quote probes=%d ; clause-d quotes in the entry=%d" % (w1q, nq))
    w1q_pairs = set(re.findall(r"\(\s*'([a-z0-9-]+)',\s*'([SR])',\s*(\d+),\s*(\d+),", qsrc))
    w1_ranges = {(p, int(a), int(b)) for _lab, p, a, b in w1q_pairs}
    uncovered_q = []
    for ln, line in enumerate(entry_lines, 1):
        for m in QUOTE_RE.finditer(line):
            span = m.group(1) if m.group(1) is not None else m.group(2)
            q = norm_q(span)
            if len(q.split()) < 2:
                continue
            tok = m.group(3)
            pint = resolve_pin(tok.rsplit(":", 1)[0], pins, by_base)
            if pint is None:
                continue
            key = ('R' if pint == 'README.md' else 'S',)
            rng = re.match(r".+:(\d+)(?:-(\d+))?$", tok)
            a, b = int(rng.group(1)), int(rng.group(2) or rng.group(1))
            if not any(p == key[0] and a <= x <= b for p, x, y in w1_ranges):
                uncovered_q.append((ln, pint, a, b, q[:46]))
    print("  clause-d quote sites with NO w1 quote probe: %d" % len(uncovered_q))
    for u in uncovered_q:
        print("    uncovered quote %s" % (u,))
    if nq > w1q:
        note("W1_QUOTE_COVERAGE_GAP", 0,
             "w1 verified %d quotes, the entry carries %d clause-d quotes; sites: %s"
             % (w1q, nq, [(u[0], u[1], u[2]) for u in uncovered_q]))

    # ---------------- L7 reachability
    print("\n== L7 pin paths and digests named by the entry ==")
    named = set()
    for ln, line in enumerate(entry_lines, 1):
        for s, e, t in scan_spans(line):
            if 'pins/' in t or 'fetch/' in t:
                named.add((ln, t))
        for m in re.finditer(r"\.ufo/waves/round-47/[A-Za-z0-9._/-]+", line):
            named.add((ln, m.group(0)))
    for ln, path in sorted(named):
        here = os.path.dirname(ENTRY)
        cands = {'as-written-from-entry': os.path.normpath(os.path.join(here, path)),
                 'lane-root': os.path.normpath(os.path.join(LANE, path)),
                 'upstream-pin': os.path.normpath(os.path.join(LANE, '.ufo/waves/round-47/w1/ScrEntry', path))}
        hit = [k for k, v in cands.items() if os.path.exists(v)]
        print("  line %-3d %-58s resolves=%s" % (ln, path, hit or "NO"))
        if not hit:
            note("PIN_PATH_UNRESOLVABLE", ln, path)
    for ln, line in enumerate(entry_lines, 1):
        for m in re.finditer(r"sha256[: ]+([0-9a-f]{64})", line):
            dg = m.group(1)
            match = [n for n, b in pins.items() if hashlib.sha256(b).hexdigest() == dg]
            print("  line %-3d digest %s.. -> fetch pin %s" % (ln, dg[:12], match or "NONE"))
            if not match:
                note("DIGEST_NOT_A_FETCH_PIN", ln, dg)

    # lane-file locators (not fetch pins): terminal-route-r17.md, host config
    print("\n== L7b locators that name lane/host files ==")
    for ln, line in enumerate(entry_lines, 1):
        for token, a, b in locators(line):
            if resolve_pin(token.rsplit(":", 1)[0], pins, by_base):
                continue
            base = token.rsplit("/", 1)[-1]
            blobs = [p for p in ('corpus/knowledge/terminal-route-r17.md',)
                     if p.rsplit('/', 1)[-1] == base]
            host = None
            if base == 'bindings.conf':
                h = os.path.join(os.path.expanduser('~/.config/hypr'), base)
                host = open(h, encoding='utf-8', errors='replace').read().split('\n') if os.path.exists(h) else None
            for path in blobs:
                lb = lane_blob(path)
                if lb is None:
                    note("LANE_FILE_MISSING", ln, path)
                    continue
                ok = 1 <= a <= b <= len(lb)
                print("  line %-3d %s:%d-%d  lane file %s lines=%d in_range=%s"
                      % (ln, base, a, b, path, len(lb), ok))
                if not ok:
                    note("LANE_LOCATOR_OUT_OF_RANGE", ln, "%s:%d-%d / %d" % (path, a, b, len(lb)))
                else:
                    for x in range(a, b + 1):
                        print("      %d: %s" % (x, lb[x - 1][:110]))
            if host:
                ok = 1 <= a <= b <= len(host)
                print("  line %-3d %s:%d-%d  host file lines=%d in_range=%s"
                      % (ln, base, a, b, len(host), ok))
                if not ok:
                    note("HOST_LOCATOR_OUT_OF_RANGE", ln, "%s:%d-%d / %d" % (base, a, b, len(host)))
                else:
                    for x in range(a, b + 1):
                        print("      %d: %s" % (x, host[x - 1][:110]))

    # ---------------- L8 mutation self-test
    print("\n== L8 mutation self-test ==")
    tmp = tempfile.mkdtemp(dir=os.environ.get('TMPDIR') or None)
    mutations = [
        ("locator shifted by 1",
         "`IFS=':'` (xdg-terminal-exec:145)", "`IFS=':'` (xdg-terminal-exec:146)"),
        ("quote range moved by 1",
         "even if it's more IO intensive`, xdg-terminal-exec:353",
         "even if it's more IO intensive`, xdg-terminal-exec:354"),
        ("quote word doctored",
         "(`All config files are read immediatelly, rather than on demand, even if it's more IO intensive`",
         "(`All config files are read eagerly, rather than on demand, even if it's more IO intensive`"),
        ("function body range off by 1",
         "`read_entry_path` (xdg-terminal-exec:970-1018)",
         "`read_entry_path` (xdg-terminal-exec:970-1019)"),
        ("locator past pin end",
         "(xdg-terminal-exec:1499)", "(xdg-terminal-exec:1501)"),
        ("OBS quote doctored",
         "`Entries are checked in ascending order of preference, so use last found if duplicate`",
         "`Entries are checked in descending order of preference, so use last found if duplicate`"),
        ("README range one early",
         "README-v0.14.3.md:300-301", "README-v0.14.3.md:298-299"),
        ("function cited at another function's body",
         "`find_entry_paths` turns IDs into paths with one `find` call (xdg-terminal-exec:754-800)",
         "`find_entry_paths` turns IDs into paths with one `find` call (xdg-terminal-exec:1055-1111)"),
    ]
    baseline = check_text(text, pins, by_base, bodies, script)
    print("  baseline kinds: %s" % sorted(baseline))
    ok = True
    for label, old, new in mutations:
        if old not in text:
            print("  ANCHOR-MISSING %s" % label)
            ok = False
            continue
        FINDINGS.clear()
        got = check_text(text.replace(old, new, 1), pins, by_base, bodies, script,
                         verbose=True)
        mutated = {(k, d) for k, ln, d, h in FINDINGS}
        FINDINGS.clear()
        check_text(text, pins, by_base, bodies, script, verbose=True)
        base_set = {(k, d) for k, ln, d, h in FINDINGS}
        caught = mutated - base_set
        print("  %-42s caught=%-5s %s" % (label, bool(caught),
              sorted({k for k, d in caught})))
        if not caught:
            ok = False
            note("SELFTEST_MISSED", 0, label)
    print("  mutation self-test: %s" % ("PASS" if ok else "FAIL"))
    shutil.rmtree(tmp, ignore_errors=True)

    # census mutation is caught by L5, not check_text - test it explicitly
    census_mut = text.replace("script_lines=1499", "script_lines=1498")
    mc = {}
    for line in census_mut.split("\n"):
        if line.startswith("xdg-terminal-exec script_lines="):
            mc = {k: int(v) for k, v in re.findall(r"([a-z_]+)=(\d+)", line)}
    if mc.get("script_lines") != census["script_lines"]:
        print("  %-42s caught=True (L5)" % "census number altered")
    else:
        ok = False
        note("SELFTEST_MISSED", 0, "census number altered")

    # ---------------- L9 host inventory of the selection slots
    print("\n== L9 host slot inventory (read-only, resolver never run) ==")
    envv = {k: os.environ.get(k) for k in
            ("XDG_CONFIG_HOME", "XDG_DATA_HOME", "XDG_CONFIG_DIRS", "XDG_DATA_DIRS",
             "XDG_CURRENT_DESKTOP", "XDG_CACHE_HOME")}
    for k, v in envv.items():
        print("  %-22s %s" % (k, v if v is not None else "<unset>"))
    home = os.path.expanduser("~")
    cfg_home = envv["XDG_CONFIG_HOME"] or home + "/.config"
    cfg_dirs = (envv["XDG_CONFIG_DIRS"] or "/etc/xdg").split(":")
    data_home = envv["XDG_DATA_HOME"] or home + "/.local/share"
    data_dirs = (envv["XDG_DATA_DIRS"] or "/usr/local/share:/usr/share").split(":")
    desks = [d.strip().lower() for d in (envv["XDG_CURRENT_DESKTOP"] or "").split(":")
             if d.strip()]
    slots = []
    for d in [cfg_home] + cfg_dirs:
        for pre in [x + "-" for x in desks] + [""]:
            slots.append(("%s/%sxdg-terminals.list" % (d, pre), "config"))
    for d in data_dirs:
        for pre in [x + "-" for x in desks] + [""]:
            slots.append(("%s/xdg-terminal-exec/%sxdg-terminals.list" % (d, pre), "data"))
    apps = [data_home + "/applications"] + [d + "/applications" for d in data_dirs]
    present = [(p, k) for p, k in slots if os.path.exists(p)]
    print("  list slots in the script's own order: %d, present: %d" % (len(slots), len(present)))
    for p, k in slots:
        print("    %-4s %-62s %s" % (k, p, "PRESENT" if os.path.exists(p) else "-"))
    for a in apps:
        print("    apps %-62s %s" % (a, "PRESENT" if os.path.isdir(a) else "-"))
    entry_host = [l for l in entry_lines if "eight config slots" in l or "data-side one present" in l]
    stated = set()
    for line in entry_host:
        for m in re.finditer(r"[~/][A-Za-z0-9._/~-]*xdg-terminals\.list", line):
            t = m.group(0)
            if t.startswith("~"):
                stated.add(os.path.expanduser(t))
            elif t.startswith(("/usr/", "/etc/", "/home/")):
                stated.add(t)
            else:
                stated.add(home + t)
    print("  entry host inventory names: %s" % sorted(stated))
    for p, k in present:
        if p not in stated:
            note("HOST_SLOT_NOT_NAMED", 0, "%s (%s) exists on this host and the entry's "
                 "host inventory does not name it" % (p, k))
    absent_stated = [p for p, k in slots if p not in present]
    print("  slots the entry's paragraph does NOT name: %s" %
          [p for p in absent_stated if p not in stated][:8])

    # ---------------- summary
    print("\n== SUMMARY ==")
    hard = [f for f in FINDINGS if f[3]]
    soft = [f for f in FINDINGS if not f[3]]
    print("  HARD findings: %d" % len(hard))
    for k, ln, d, _ in hard:
        print("   [%s] line %d: %s" % (k, ln, d))
    print("  SOFT findings: %d" % len(soft))
    for k, ln, d, _ in soft:
        print("   (%s) line %d: %s" % (k, ln, d))
    return 1 if hard else 0


if __name__ == '__main__':
    sys.exit(main())
