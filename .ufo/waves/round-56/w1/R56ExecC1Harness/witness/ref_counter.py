#!/usr/bin/env python3
"""WITNESS reference counter for testing r56_ctl_c1.py (NOT the real quality/counters/c1-r56-autoreload-entry.py).

Implements registration.md section C1 as literally as possible, with ONE declared choice: `quote:<id>` also fails
when the row's own quote cell differs from the frozen quote (otherwise control 8 `edited-quote` could only surface
as `row:K05`, never as the required `quote:K05` leg - see the report, ambiguity A1).
"""
import argparse, hashlib, json, os, re, subprocess, sys

TABLES = ".ufo/waves/round-56/frozen-tables.json"
TABLES_SHA = "d50d2b7b16506c50cb44358d4284e4f0eb0d14e433594d068a0fbe74c5edf9af"
ID_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]{3,}")
NUM_RE = re.compile(r"(?<![A-Za-z0-9_])[0-9]+(?![A-Za-z0-9_])")
REG_RE = re.compile(r"^ {0,3}\|\s*S[0-9]{3,}\s*\|")
FENCE = re.compile(r"^ {0,3}(```|~~~)")


class Setup(Exception):
    pass


def g(repo, rev, *a, check=True):
    env = {"PATH": os.environ["PATH"], "HOME": os.environ.get("TMPDIR", "/"), "GIT_CONFIG_GLOBAL": "/dev/null"}
    p = subprocess.run(["git", "-C", repo, *a], capture_output=True, env=env)
    if check and p.returncode:
        raise Setup(p.stderr.decode())
    return p.stdout


def blob(repo, rev, path):
    out = g(repo, rev, "ls-tree", "-z", rev, "--", path)
    if not out.strip(b"\0"):
        return None
    meta = out.split(b"\0")[0].decode()
    mode, typ, rest = meta.split(" ", 2)
    if typ != "blob" or mode not in ("100644", "100755"):
        return None
    # a path crossing a symlinked directory is absent: ls-tree of such a path is empty already
    return g(repo, rev, "cat-file", "blob", rest.split("\t")[0])


def rows_of(lines):
    rows, fence, com = {}, None, False
    for i, l in enumerate(lines):
        if com:
            if "-->" in l:
                com = False
            continue
        m = FENCE.match(l)
        if fence:
            if m and m.group(1) == fence:
                fence = None
            continue
        if m:
            fence = m.group(1)
            continue
        r = re.match(r"^\|\s*([KH][0-9]{2})\s*\|", l)
        if r:
            rows.setdefault(r.group(1), []).append(l)
        k = l.rfind("<!--")
        if k >= 0 and l.find("-->", k) < 0:
            com = True
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True); ap.add_argument("--rev", required=True); ap.add_argument("--work", required=True)
    a = ap.parse_args()
    os.makedirs(a.work, exist_ok=True)
    rev = a.rev
    tb = blob(a.repo, rev, TABLES)
    if tb is None:
        raise Setup("tables absent")
    missed = []
    if hashlib.sha256(tb).hexdigest() != TABLES_SHA:
        missed.append("tables_sha")
    t = json.loads(tb)["c1"]
    entry_p = t["entry"]
    pins = {}
    pin_ok = True
    for name, h in t["pin_sha256"].items():
        b = blob(a.repo, rev, t["pin_dir"] + "/" + name)
        pins[name] = b
        if b is None or hashlib.sha256(b).hexdigest() != h:
            pin_ok = False
    for name, h in t["host_pin_sha256"].items():
        b = blob(a.repo, rev, t["pin_dir"] + "/" + name)
        pins[name] = b
        if b is None or hashlib.sha256(b).hexdigest() != h:
            pin_ok = False
    if not pin_ok:
        missed.append("pin_hash")
    pin_lines = {n: (b.decode("utf-8", "replace").split("\n") if b is not None else None) for n, b in pins.items()}

    reg = blob(a.repo, rev, "corpus/SOURCES.md")
    reg_rows = {}
    if reg is None:
        raise Setup("registry absent")
    for l in reg.decode().split("\n"):
        if REG_RE.match(l):
            cells = [c for c in l.strip()[1:-1].split("|")]
            if len(cells) != 11:
                raise Setup("registry row with %d cells" % len(cells))
            reg_rows.setdefault(cells[0].strip(), []).append([c.strip() for c in cells])

    def source_cell(sid, pin):
        r = reg_rows.get(sid, [])
        if len(r) != 1:
            return False
        c = r[0]
        if c[7] != "mined" or c[3] not in ("A", "B") or c[8] != "2026-10-28":
            return False
        urls = re.findall(r"https?://\S+", c[1])
        if not urls:
            return False
        url = urls[-1]
        rr = t["rev_rule"]
        tok = rr["man7-inotify.7.html"] if pin == "man7-inotify.7.html" else rr["Hyprland-*"]
        if not url.endswith("/" + t["pin_suffix"][pin]) or tok not in url:
            return False
        return entry_p in re.findall(r"corpus/knowledge/[A-Za-z0-9_.-]+\.md", c[10])

    def scope(sid, pin, line):
        c = reg_rows[sid][0]
        base = t["pin_suffix"][pin].rsplit("/", 1)[-1]
        for m in re.finditer(re.escape(base) + ":", c[5]):
            rest = c[5][m.end():]
            lm = re.match(r"\s*([0-9]+(?:-[0-9]+)?(?:\s*,\s*[0-9]+(?:-[0-9]+)?)*)", rest)
            if not lm:
                continue
            for part in lm.group(1).split(","):
                part = part.strip()
                lo, _, hi = part.partition("-")
                if int(lo) <= line <= int(hi or lo):
                    return True
        return False

    eb = blob(a.repo, rev, entry_p)
    rows_a = hosts_b = src_c = scope_d = content_e = new_m = 0
    if eb is None:
        missed.insert(0, "entry_absent")
    else:
        lines = eb.decode("utf-8", "replace").split("\n")
        head = lines[:30]
        idx = {k: next((i for i, l in enumerate(head) if l.startswith(k)), None) for k in ("source:", "verified-at: 2026-10-28", "recheck:")}
        prov_ok = None not in idx.values() and idx["source:"] < idx["verified-at: 2026-10-28"] < idx["recheck:"] \
            and sum(1 for l in head if l.startswith("verified-at: 2026-10-28")) == 1
        srcset = set()
        for l in head:
            if l.startswith("source:"):
                srcset |= set(re.findall(r"S[0-9]{3,}", l))
        if not prov_ok or any(s not in reg_rows for s in srcset):
            missed.append("prov")
        cited = set()
        rows = rows_of(lines)
        props = {}
        for rid, ls in rows.items():
            for l in ls:
                if l.startswith("| ") and l.endswith(" |") and len(l[2:-2].split(" | ")) == 5:
                    props.setdefault(l[2:-2].split(" | ")[1], []).append(rid)
        idxrows = [l for l in (blob(a.repo, rev, "corpus/README.md") or b"").decode().split("\n")
                   if l.startswith("| `" + entry_p.replace("corpus/", "", 1) + "`")]
        if len(idxrows) != 1:
            missed.append("index")
        k_lines = {}
        for r in t["k"]:
            k_lines.setdefault(r["pin"], set()).add(r["line"])
        for r in t["k"] + t["h"]:
            rid, isk = r["id"], r["id"].startswith("K")
            ok_row = False
            row_quote = None
            ls = rows.get(rid, [])
            if len(ls) == 1 and ls[0].startswith("| ") and ls[0].endswith(" |"):
                cells = ls[0][2:-2].split(" | ")
                if len(cells) == 5 and not any("|" in c or "\\" in c for c in cells):
                    prop = cells[1]
                    want_src = r["sid"] if isk else "host"
                    q = cells[4]
                    row_quote = q[1:-1] if len(q) >= 2 and q[0] == "`" and q[-1] == "`" and q[1:-1].count("`") == 0 else None
                    ok_row = (cells[0] == rid and cells[2] == (cells[2] if isk and re.fullmatch(r"S[0-9]{3}", cells[2]) else "host")
                              and (isk or cells[2] == "host") and cells[3] == "%s:%d" % (r["pin"], r["line"])
                              and row_quote is not None
                              and len(prop) >= (40 if isk else 20) and prop == prop.strip() and len(props.get(prop, [])) == 1)
                    if isk:
                        cited.add(cells[2])
            if not ok_row:
                missed.append("row:" + rid)
            pl = pin_lines.get(r["pin"])
            quote_ok = ok_row and pl is not None and r["line"] <= len(pl) and r["quote"] in pl[r["line"] - 1] and row_quote == r["quote"]
            if not quote_ok and ok_row:
                missed.append("quote:" + rid)
            if not ok_row:
                continue
            tok_ok = bool(set(ID_RE.findall(prop)) & set(ID_RE.findall(r["quote"])))
            allowed = set(NUM_RE.findall(r["quote"])) | {str(r["line"])} | {str(x) for x in k_lines.get(r["pin"], ())} | {"0", "1", "2", "3"}
            num_ok = all(n in allowed for n in NUM_RE.findall(prop))
            if not tok_ok:
                missed.append("tok:" + rid)
            if not num_ok:
                missed.append("num:" + rid)
            if tok_ok and num_ok:
                content_e += 1
            if isk:
                sc_ok = cells[2] == r["sid"] and source_cell(cells[2], r["pin"])
                if sc_ok:
                    src_c += 1
                else:
                    missed.append("source_cell:" + rid)
                if cells[2] in reg_rows and scope(cells[2], r["pin"], r["line"]):
                    scope_d += 1
                else:
                    missed.append("scope:" + rid)
            else:
                hp = pin_lines.get(r["pin"])
                if hp is not None and row_quote is not None and row_quote in hp[r["line"] - 1] and quote_ok:
                    hosts_b += 1
                else:
                    missed.append("host:" + rid)
            if quote_ok and isk:
                rows_a += 1
        for sid in t["new_row_ids"]:
            if source_cell(sid, t["rows"][sid]):
                new_m += 1
        if new_m < 8:
            missed.append("new_rows")
        if any(s not in srcset for s in cited):
            if "prov" not in missed:
                missed.append("prov")
    ok = not missed
    print("MADO_AUTORELOAD_ENTRY: rev=%s rows=%d/30 hosts=%d/3 sources=%d/30 scope=%d/30 content=%d/33 new_rows=%d/8 verdict=%s missed=%s"
          % (rev, rows_a, hosts_b, src_c, scope_d, content_e, new_m, "TARGET_MET" if ok else "TARGET_MISSED", "none" if ok else ",".join(missed)))
    return 0 if ok else 1


try:
    sys.exit(main())
except Setup as e:
    sys.stderr.write("setup: %s\n" % e)
    sys.exit(2)
