#!/usr/bin/env python3
"""Critic's C1 checker, written ONLY from registration.md section 'C1 autoreload entry' (+ claims-frozen C1 line).

Usage: python3 -I c1_check.py --repo DIR --rev REV --work DIR
Prints one MADO_AUTORELOAD_ENTRY line; exit 0 only on TARGET_MET, 1 on a miss, 2 on a setup error.
Git objects only (ls-tree / cat-file). Frozen facts come from frozen-tables.json at --rev (sha checked).
"""
import argparse, fnmatch, hashlib, json, os, re, subprocess, sys

TABLES = ".ufo/waves/round-56/frozen-tables.json"
TABLES_SHA = "d50d2b7b16506c50cb44358d4284e4f0eb0d14e433594d068a0fbe74c5edf9af"
README = "corpus/README.md"
SOURCES = "corpus/SOURCES.md"
OPENED = "2026-10-28"
ID_RE = re.compile(r"^\| ?([KH][0-9]{2}) ?\|")
REG_RE = re.compile(r"^ {0,3}\|\s*S[0-9]{3,}\s*\|")
FENCE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
TOK_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]{3,}")
NUM_RE = re.compile(r"(?<![A-Za-z0-9_])[0-9]+(?![A-Za-z0-9_])")
USED_RE = re.compile(r"corpus/knowledge/[A-Za-z0-9_.-]+\.md")
URL_RE = re.compile(r"https?://\S+")


def setup(msg):
    sys.stderr.write(f"c1_check: setup: {msg}\n")
    sys.exit(2)


def env_for(work):
    return {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": work, "TMPDIR": work,
            "GIT_CONFIG_NOSYSTEM": "1", "LC_ALL": "C"}


def blob_at(repo, env, rev, path):
    r = subprocess.run(["git", "-C", repo, "ls-tree", "-z", rev, "--", path], capture_output=True, env=env)
    if r.returncode != 0 or not r.stdout:
        return None
    for rec in r.stdout.split(b"\0"):
        if not rec:
            continue
        meta, _, p = rec.partition(b"\t")
        mode, typ, sha = meta.decode().split()
        if p.decode() != path or typ != "blob" or mode not in ("100644", "100755"):
            return None
        return subprocess.run(["git", "-C", repo, "cat-file", "blob", sha], capture_output=True, env=env).stdout
    return None


def row_cells(line):
    """Registry row cells (11) or None."""
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    return [c.strip() for c in s.split("|")]


def registry_rows(text):
    out = {}
    for line in text.split("\n"):
        if REG_RE.match(line):
            cells = row_cells(line)
            out.setdefault(cells[0], []).append(cells)
    return out


def reg_ok(rows, sid, entry, pin_suffix_for_pin, rev_token):
    """registry-row legs shared by source_cell and new_rows (status, tier, opened, URL, used-by)."""
    rs = rows.get(sid, [])
    if len(rs) != 1 or len(rs[0]) != 11:
        return False, None
    c = rs[0]
    if c[7] != "mined" or c[3] not in ("A", "B") or c[8] != OPENED:
        return False, c
    urls = URL_RE.findall(c[1])
    if not urls:
        return False, c
    url = urls[-1]
    if not url.endswith("/" + pin_suffix_for_pin) or rev_token not in url:
        return False, c
    if entry not in USED_RE.findall(c[10]):
        return False, c
    return True, c


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--work", required=True)
    a = ap.parse_args()
    os.makedirs(a.work, exist_ok=True)
    env = env_for(a.work)
    tb = blob_at(a.repo, env, a.rev, TABLES)
    if tb is None:
        setup("frozen-tables.json absent at rev")
    missed = []
    if hashlib.sha256(tb).hexdigest() != TABLES_SHA:
        missed.append("tables_sha")
    T = json.loads(tb)
    c1 = T["c1"]
    ENTRY = c1["entry"]
    pin_dir = c1["pin_dir"]
    pin_suffix = c1["pin_suffix"]
    rev_rule = c1["rev_rule"]
    K = c1["k"]
    H = c1["h"]
    sid_of = {k["id"]: k["sid"] for k in K}
    rows_pin = c1["rows"]
    new_ids = c1["new_row_ids"]

    def token_for(pin):
        for pat, tok in rev_rule.items():
            if fnmatch.fnmatch(pin, pat):
                return tok
        return None

    # pins
    pin_text = {}
    pin_ok = True
    for pin, want in list(c1["pin_sha256"].items()) + list(c1["host_pin_sha256"].items()):
        b = blob_at(a.repo, env, a.rev, f"{pin_dir}/{pin}")
        if b is None or hashlib.sha256(b).hexdigest() != want:
            pin_ok = False
        if b is not None:
            pin_text[pin] = b.decode("utf-8", "replace").split("\n")
    if not pin_ok:
        missed.append("pin_hash")

    # registry
    sb = blob_at(a.repo, env, a.rev, SOURCES)
    rows = registry_rows(sb.decode("utf-8", "replace")) if sb is not None else {}

    # README index
    rb = blob_at(a.repo, env, a.rev, README)
    idx_lines = [l for l in (rb or b"").decode("utf-8", "replace").split("\n")
                 if l.startswith("| `knowledge/hyprland-config-autoreload-r56.md`")]
    if len(idx_lines) != 1:
        missed.append("index")

    # entry
    eb = blob_at(a.repo, env, a.rev, ENTRY)
    entry_text = eb.decode("utf-8", "replace") if eb is not None else None
    if entry_text is None:
        missed.append("entry_absent")
        lines = []
    else:
        lines = entry_text.split("\n")

    # rows of the entry (outside fences and HTML comments)
    cand = {}
    if entry_text is not None:
        fence = None
        in_comment = False
        for line in lines:
            if fence is None and not in_comment:
                m = FENCE_RE.match(line)
                if m:
                    fence = m.group(1)[0]
                    continue
                if "<!--" in line and "-->" not in line:
                    in_comment = True
                    continue
                mm = ID_RE.match(line)
                if mm:
                    cand.setdefault(mm.group(1), []).append(line)
            elif fence is not None:
                m = FENCE_RE.match(line)
                if m and m.group(1)[0] == fence:
                    fence = None
            elif in_comment and "-->" in line:
                in_comment = False

    frozen = {r["id"]: r for r in K + H}
    parsed = {}  # id -> dict(prop, src, pinline, quote)
    rowleg_bad = set()
    for rid, r in frozen.items():
        lst = cand.get(rid, [])
        if len(lst) != 1:
            rowleg_bad.add(rid)
            continue
        line = lst[0]
        prefix = f"| {rid} | "
        ok = line.startswith(prefix) and line.endswith(" |") and len(line) >= len(prefix) + 4
        if not ok:
            rowleg_bad.add(rid)
            continue
        inner = line[2:-2]
        cells = inner.split(" | ")
        if len(cells) != 5 or any("|" in c for c in cells):
            rowleg_bad.add(rid)
            continue
        cid, prop, src, pinline, qcell = cells
        want_src_ok = (re.fullmatch(r"S[0-9]{3}", src) is not None) if rid.startswith("K") else src == "host"
        pin = r["pin"]
        if cid != rid or not want_src_ok or pinline != f"{pin}:{r['line']}" or qcell != "`" + r["quote"] + "`":
            rowleg_bad.add(rid)
            continue
        if prop != prop.strip() or len(prop) < (40 if rid.startswith("K") else 20):
            rowleg_bad.add(rid)
            continue
        parsed[rid] = {"prop": prop, "src": src, "quote": r["quote"]}
    # duplicate propositions
    seen = {}
    for rid, p in parsed.items():
        seen.setdefault(p["prop"], []).append(rid)
    for prop, ids in seen.items():
        if len(ids) > 1:
            rowleg_bad.update(ids)
            parsed = {k: v for k, v in parsed.items() if k not in ids}

    row_legs = {}
    for rid in frozen:
        row_legs[f"row:{rid}"] = rid not in rowleg_bad
    if rowleg_bad:
        for rid in sorted(rowleg_bad):
            missed.append(f"row:{rid}")

    # quote legs
    quote_ok = {}
    for rid, r in frozen.items():
        lines_p = pin_text.get(r["pin"])
        ok = lines_p is not None and 1 <= r["line"] <= len(lines_p) and r["quote"] in lines_p[r["line"] - 1]
        quote_ok[rid] = ok
        if not ok:
            missed.append(f"quote:{rid}")

    # host legs (H): quote carried by row must be substring of host pin line
    host_b = 0
    for r in H:
        rid = r["id"]
        ok_row = rid in parsed
        q = parsed[rid]["quote"] if ok_row else None
        hl = pin_text.get(r["pin"])
        host_ok = bool(ok_row and hl is not None and 1 <= r["line"] <= len(hl) and q in hl[r["line"] - 1])
        if not host_ok:
            missed.append(f"host:{rid}")
        if ok_row and quote_ok[rid] and host_ok and row_legs[f"row:{rid}"]:
            host_b += 1

    # K row registry legs
    src_c = 0
    scope_d = 0
    for r in K:
        rid, sid, pin, line = r["id"], r["sid"], r["pin"], r["line"]
        suffix = pin_suffix[pin]
        tok = token_for(pin)
        ok, c = reg_ok(rows, sid, ENTRY, suffix, tok)
        src_ok = ok and rid in parsed and parsed[rid]["src"] == sid
        if src_ok:
            src_c += 1
        else:
            missed.append(f"source_cell:{rid}")
        scope_ok = False
        if c is not None:
            anchor = c[5]
            base = suffix.rsplit("/", 1)[-1]
            for m in re.finditer(re.escape(base) + ":", anchor):
                mm = re.match(r"[0-9]+(?:-[0-9]+)?(?:\s*,\s*[0-9]+(?:-[0-9]+)?)*", anchor[m.end():])
                if not mm:
                    continue
                for loc in mm.group(0).split(","):
                    loc = loc.strip()
                    lo, _, hi = loc.partition("-")
                    hi = hi or lo
                    if int(lo) <= line <= int(hi):
                        scope_ok = True
        if scope_ok:
            scope_d += 1
        else:
            missed.append(f"scope:{rid}")

    # tok / num legs for K and H rows
    content_e = 0
    other_lines = {}
    for r in K + H:
        other_lines.setdefault(r["pin"], []).append(r["line"])
    for r in K + H:
        rid = r["id"]
        if rid not in parsed:
            missed.append(f"tok:{rid}")
            missed.append(f"num:{rid}")
            continue
        prop, q = parsed[rid]["prop"], parsed[rid]["quote"]
        tok_ok = bool(set(TOK_RE.findall(prop)) & set(TOK_RE.findall(q)))
        qruns = set(NUM_RE.findall(q))
        allowed_lines = {str(x) for x in other_lines[r["pin"]]}
        allowed = qruns | allowed_lines | {str(r["line"]), "0", "1", "2", "3"}
        num_ok = all(n in allowed for n in NUM_RE.findall(prop))
        if not tok_ok:
            missed.append(f"tok:{rid}")
        if not num_ok:
            missed.append(f"num:{rid}")
        if tok_ok and num_ok:
            content_e += 1

    # prov legs: first 30 lines
    prov_ok = False
    if entry_text is not None:
        head = lines[:30]
        si = [i for i, l in enumerate(head) if l.startswith("source:")]
        vi = [i for i, l in enumerate(head) if l == "verified-at: " + OPENED]
        ri = [i for i, l in enumerate(head) if l.startswith("recheck:")]
        if si and len(vi) == 1 and len(ri) == 1 and max(si) < vi[0] < ri[0]:
            src_sids = set()
            for i in si:
                src_sids.update(re.findall(r"(?<![A-Za-z0-9])S[0-9]{3}(?![0-9])", head[i]))
            regs_ok = all(s in rows for s in src_sids)
            need = {sid_of[k] for k in sid_of}
            prov_ok = regs_ok and need <= src_sids
    if not prov_ok and entry_text is not None:
        missed.append("prov")

    # new rows S383..S390
    new_m = 0
    for sid in new_ids:
        pin = rows_pin[sid]
        ok, _c = reg_ok(rows, sid, ENTRY, pin_suffix[pin], token_for(pin))
        if ok:
            new_m += 1
    if new_m != len(new_ids):
        missed.append("new_rows")

    a_rows = sum(1 for r in K if f"row:{r['id']}" not in [m for m in missed if m == f"row:{r['id']}"] and r["id"] in parsed and quote_ok[r["id"]])
    b_hosts = host_b
    met = (a_rows == 30 and b_hosts == 3 and src_c == 30 and scope_d == 30 and content_e == 33 and new_m == 8 and not missed)
    missed_u = []
    for m in missed:
        if m not in missed_u:
            missed_u.append(m)
    print(f"MADO_AUTORELOAD_ENTRY: rev={a.rev} rows={a_rows}/30 hosts={b_hosts}/3 sources={src_c}/30 scope={scope_d}/30 "
          f"content={content_e}/33 new_rows={new_m}/8 verdict={'TARGET_MET' if met else 'TARGET_MISSED'} "
          f"missed={','.join(missed_u) if missed_u else 'none'}")
    sys.exit(0 if met else 1)


if __name__ == "__main__":
    main()
