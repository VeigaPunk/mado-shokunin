#!/usr/bin/env python3
# R56ConnHistory — demonstration of registration.md section C3 (used-by back-references, CITE/SRC/USEDBY
# definitions as written) and of the section C1 lexical legs (tok, num, length) on committed frozen data.
# Reads git objects only (git ls-tree / cat-file / show). Writes nothing; keeps everything in memory.
# Run: python3 -I -B recipes.py
# Declared simplification: a fence opens and closes on any line matching ^ {0,3}(```|~~~); the
# registration does not state closing-marker matching.
import json
import re
import subprocess

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
BASE = "13f0acbe3a15da2d9c08357a576d91dcadc85273"  # base field of frozen-tables.json
REV = "3423ae285676c2a10273000f4519163472b443db"   # freeze commit (claims, registration, tables, fixtures)

ROWRE = re.compile(r"^ {0,3}\|\s*S[0-9]{3,}\s*\|")
FENCE = re.compile(r"^ {0,3}(```|~~~)")
TOK = re.compile(r"(?<![A-Za-z0-9])S[0-9]{3}(?![0-9])")
UB = re.compile(r"corpus/knowledge/[A-Za-z0-9_.-]+\.md")
IDR = re.compile(r"[A-Za-z_][A-Za-z0-9_]{3,}")
NUMR = re.compile(r"(?<![A-Za-z0-9_])[0-9]+(?![A-Za-z0-9_])")


def git(*a):
    r = subprocess.run(["git", "-C", LANE, *a], capture_output=True)
    if r.returncode:
        raise SystemExit(f"git {a[0]} rc={r.returncode}: {r.stderr[:200]!r}")
    return r.stdout


def cite(text):
    out, inf = set(), False
    for line in text.split("\n"):
        if FENCE.match(line):
            inf = not inf
            continue
        if not inf:
            out.update(TOK.findall(line))
    return out


def src_ids(text):
    out = set()
    for line in text.split("\n")[:15]:
        if line.startswith("source:"):
            out.update(TOK.findall(line))
    return out


def count(entries, rows):
    C = {p: cite(t) for p, t in entries.items()}
    U = {s: set(UB.findall(c[10])) for s, c in rows.items()}
    missing = [(s, p) for p in entries for s in C[p] if s in rows and p not in U[s]]
    extra = [(s, p) for s in rows for p in U[s] if p not in entries or s not in C[p]]
    dangling = [(p, s) for p, t in entries.items() for s in src_ids(t) if s not in rows]
    return missing, extra, dangling


def load():
    entries = {}
    for e in git("ls-tree", "-r", "-z", BASE, "--", "corpus/knowledge").split(b"\0"):
        if not e:
            continue
        meta, path = e.split(b"\t", 1)
        mode, _typ, sha = meta.decode().split()
        p = path.decode()
        if mode in ("100644", "100755") and re.fullmatch(r"corpus/knowledge/[^/]+\.md", p):
            entries[p] = git("cat-file", "blob", sha).decode("utf-8", "replace")
    src = git("show", f"{BASE}:corpus/SOURCES.md").decode("utf-8", "replace")
    rows, nlines = {}, 0
    for line in src.split("\n"):
        if ROWRE.match(line):
            nlines += 1
            s = line.strip()
            s = s[1:] if s.startswith("|") else s
            s = s[:-1] if s.endswith("|") else s
            cells = [c.strip() for c in s.split("|")]
            if len(cells) != 11:
                raise SystemExit(f"setup: row {cells[0]} has {len(cells)} cells")
            rows[cells[0]] = cells
    return entries, rows, nlines


def erase(entries, missing):
    """Recipe A: delete the cited S-token from prose on every missing pair's entry; used-by untouched."""
    targets = {}
    for s, p in missing:
        targets.setdefault(p, set()).add(s)
    out_entries = dict(entries)
    removed = 0
    for p, ss in targets.items():
        out, inf = [], False
        for line in entries[p].split("\n"):
            if FENCE.match(line):
                inf = not inf
                out.append(line)
                continue
            if not inf:
                for t in TOK.findall(line):
                    if t in ss:
                        removed += 1
                line = TOK.sub(lambda m, ss=ss: "" if m.group(0) in ss else m.group(0), line)
            out.append(line)
        out_entries[p] = "\n".join(out)
    return out_entries, len(targets), removed


def fence(entries, missing, precise):
    """Recipe B: wrap citing lines in a code fence; used-by untouched. precise=True wraps only lines whose every token is a missing id."""
    targets = {}
    for s, p in missing:
        targets.setdefault(p, set()).add(s)
    out_entries = dict(entries)
    wrapped = 0
    for p, ss in targets.items():
        out, inf = [], False
        for line in entries[p].split("\n"):
            if FENCE.match(line):
                inf = not inf
                out.append(line)
                continue
            toks = [] if inf else TOK.findall(line)
            hit = any(t in ss for t in toks)
            whole = all(t in ss for t in toks)
            if hit and (whole or not precise):
                out += ["```", line, "```"]
                wrapped += 1
            else:
                out.append(line)
        out_entries[p] = "\n".join(out)
    return out_entries, wrapped


def ghost(entries, rows):
    """Recipe C: a ghost id on a source: line placed at line 16 (outside the 15-line SRC window) vs line 15."""
    first = sorted(entries)[0]
    L = entries[first].split("\n")
    w16 = dict(entries)
    w16[first] = "\n".join(L[:15] + ["source: S999"] + L[15:])
    w15 = dict(entries)
    w15[first] = "\n".join(L[:14] + ["source: S999"] + L[14:])
    return first, len(count(w16, rows)[2]), len(count(w15, rows)[2])


def lex(prop, quote):
    tok = bool(set(IDR.findall(prop)) & set(IDR.findall(quote)))
    qd = set(NUMR.findall(quote))
    num = all(x in qd or x in {"0", "1", "2", "3"} for x in NUMR.findall(prop))
    return {"tok": tok, "num": num, "len40": len(prop) >= 40}


def main():
    entries, rows, nlines = load()
    miss, ext, dang = count(entries, rows)
    print(f"BASELINE base={BASE[:12]} entries={len(entries)} rows={len(rows)} row_lines={nlines} "
          f"missing={len(miss)} extra={len(ext)} dangling={len(dang)}")
    ids = [int(re.search(r"[0-9]+", s).group()) for s in rows]
    print(f"REGISTRY max_id=S{max(ids):03d} rows_with_4plus_digit_ids={sum(1 for i in ids if i >= 1000)}")
    print("CITE_PROBE 'S0383 s383 S 383 S383a S1000 S383' ->", sorted(cite("S0383 s383 S 383 S383a S1000 S383")))

    ea, n_ent, removed = erase(entries, miss)
    m, x, d = count(ea, rows)
    print(f"RECIPE_A erase_tokens entries={n_ent} tokens_removed={removed} -> missing={len(m)} extra={len(x)} dangling={len(d)}")

    fb, wr = fence(entries, miss, precise=False)
    m, x, d = count(fb, rows)
    print(f"RECIPE_B fence_naive lines_wrapped={wr} -> missing={len(m)} extra={len(x)} dangling={len(d)}")
    fp, wr = fence(entries, miss, precise=True)
    m, x, d = count(fp, rows)
    print(f"RECIPE_B fence_precise lines_wrapped={wr} -> missing={len(m)} extra={len(x)} dangling={len(d)}")

    first, d16, d15 = ghost(entries, rows)
    print(f"RECIPE_C window entry={first} ghost_at_line16 dangling={d16} ghost_at_line15 dangling={d15}")

    T = json.loads(git("show", f"{REV}:.ufo/waves/round-56/frozen-tables.json"))
    K = {k["id"]: k for k in T["c1"]["k"]}
    k01 = K["K01"]["quote"]
    k04 = K["K04"]["quote"]
    probes = [
        ("K01 asserts true default; quote carries 'false' as final token",
         "The quoted misc:disable_autoreload entry sets its value to true by default, so automatic reload stays on unless the operator changes it.",
         k01),
        ("K01 do-nothing control text (registration control 2)",
         "placeholder proposition text for row K01, not a claim about any source line", k01),
        ("K04 control-3 appended sentence alone (registration control 3)",
         "The value is capped at 200 by this call.", k04),
    ]
    for name, prop, q in probes:
        print(f"LEX {name} -> {lex(prop, q)}")
    print("K01 quote:", k01)
    print("K04 quote:", k04)


if __name__ == "__main__":
    main()
