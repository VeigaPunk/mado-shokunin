#!/usr/bin/env python3 -I
"""Independent C1 checker, written by seat R56RevC1Contract from registration.md section C1 ONLY.

Not the lane counter (quality/counters/... is absent at base). Reads git objects at --rev only.
Output: one MADO_AUTORELOAD_ENTRY line. Exit 0 TARGET_MET, 1 miss, 2 setup error.
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys

TABLES_SHA = "d50d2b7b16506c50cb44358d4284e4f0eb0d14e433594d068a0fbe74c5edf9af"
ENTRY = "corpus/knowledge/hyprland-config-autoreload-r56.md"
TABLES = ".ufo/waves/round-56/frozen-tables.json"
PIN_DIR = ".ufo/waves/round-56/fetch"
README = "corpus/README.md"
SOURCES = "corpus/SOURCES.md"
DATE = "2026-10-28"
IDENT = re.compile(r"[A-Za-z_][A-Za-z0-9_]{3,}")
DIGITS = re.compile(r"(?<![A-Za-z0-9_])[0-9]+(?![A-Za-z0-9_])")
ROWID = re.compile(r"^ {0,3}\|\s*S[0-9]{3,}\s*\|")


def fail(reason, code=2):
    sys.stderr.write(f"c1check: {reason}\n")
    sys.exit(code)


def env_for(work):
    return {"PATH": "/usr/bin:/bin", "HOME": work, "TMPDIR": work,
            "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null", "LC_ALL": "C"}


class Repo:
    def __init__(self, repo, rev, work):
        self.repo = repo
        self.env = env_for(work)
        r = self.git("rev-parse", "--verify", "--quiet", rev + "^{commit}")
        if r.returncode != 0:
            fail(f"rev {rev!r} does not resolve in {repo!r}")
        self.sha = r.stdout.decode().strip()

    def git(self, *args):
        return subprocess.run(["git", "-C", self.repo, *args], capture_output=True, env=self.env)

    def blob(self, path):
        """Regular blob (100644/100755) at self.sha, else None (absent, symlink, dir, submodule)."""
        out = self.git("ls-tree", "-z", self.sha, "--", path)
        if out.returncode != 0 or not out.stdout:
            return None
        meta, _, name = out.stdout.rstrip(b"\0").partition(b"\t")
        if name.decode("utf-8", "replace") != path:
            return None
        mode, typ, sha = meta.split()
        if mode not in (b"100644", b"100755") or typ != b"blob":
            return None
        return self.git("cat-file", "blob", sha.decode()).stdout


def load_frozen(repo):
    raw = repo.blob(TABLES)
    if raw is None:
        return None, "tables_absent"
    if hashlib.sha256(raw).hexdigest() != TABLES_SHA:
        return None, "tables_sha"
    return json.loads(raw.decode("utf-8")), None


def registry_rows(text):
    """Return {id: [cells]} for registry rows; 11 cells required (setup error otherwise)."""
    rows = {}
    for line in text.split("\n"):
        if not ROWID.match(line):
            continue
        inner = line.strip()[1:-1]
        cells = [c.strip() for c in inner.split("|")]
        sid = cells[0]
        rows.setdefault(sid, []).append(cells)
    return rows


def source_cell_ok(cells, pin, pins_suffix, rev_rule, entry, sid_expected=None):
    if cells is None or len(cells) != 11:
        return False
    if cells[7] != "mined" or cells[3] not in ("A", "B") or cells[8] != DATE:
        return False
    urls = re.findall(r"https?://\S+", cells[1])
    if not urls:
        return False
    url = urls[-1]
    suffix = pins_suffix[pin]
    if not url.endswith("/" + suffix):
        return False
    token = rev_rule["Hyprland-*"] if pin.startswith("Hyprland-") else rev_rule[pin]
    if token not in url:
        return False
    if entry not in cells[10]:
        return False
    return True


def scope_ok(anchor, pin_suffix, pin, line):
    base = os.path.basename(pin_suffix[pin])
    key = base + ":"
    start = 0
    while True:
        idx = anchor.find(key, start)
        if idx < 0:
            return False
        rest = anchor[idx + len(key):]
        pos = 0
        while True:
            m = re.match(r"([0-9]+)(?:-([0-9]+))?", rest[pos:])
            if not m:
                break
            lo = int(m.group(1))
            hi = int(m.group(2)) if m.group(2) else lo
            if lo <= line <= hi:
                return True
            pos += m.end()
            c = re.match(r"\s*,\s*", rest[pos:])
            if not c:
                break
            pos += c.end()
        start = idx + len(key)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--quote-leg", choices=["frozen", "carried"], default="frozen",
                    help="frozen = registration text as written; carried = alternative reading (witness only)")
    a = ap.parse_args()
    if not os.path.isabs(a.repo) or not os.path.isabs(a.work):
        fail("usage: --repo and --work must be absolute")
    os.makedirs(a.work, exist_ok=True)
    repo = Repo(a.repo, a.rev, a.work)

    tables, err = load_frozen(repo)
    if tables is None:
        fail(f"frozen tables: {err}")
    c1 = tables["c1"]
    K = c1["k"]
    H = c1["h"]
    rows = {r["id"]: r for r in K + H}
    k_ids = [f"K{i:02d}" for i in range(1, 31)]
    h_ids = [f"H{i:02d}" for i in range(1, 4)]

    missed = []
    entry_raw = repo.blob(ENTRY)
    entry_present = entry_raw is not None
    if not entry_present:
        missed.append("entry_absent")
    text = entry_raw.decode("utf-8", "replace") if entry_present else ""
    lines = text.split("\n")

    # registry and README are read regardless of the entry (not entry-dependent)
    src_raw = repo.blob(SOURCES)
    registry = registry_rows(src_raw.decode("utf-8", "replace")) if src_raw else {}
    readme_raw = repo.blob(README)
    readme_lines = readme_raw.decode("utf-8", "replace").split("\n") if readme_raw else []
    index_hits = [l for l in readme_lines if l.startswith("| `" + "knowledge/hyprland-config-autoreload-r56.md" + "`")]
    if len(index_hits) != 1:
        missed.append("index")

    # pin_hash (all pins listed in the frozen tables)
    pin_ok = True
    pins_all = dict(c1["pin_sha256"])
    pins_all.update(c1["host_pin_sha256"])
    pin_blobs = {}
    for pin, want in pins_all.items():
        b = repo.blob(PIN_DIR + "/" + pin)
        pin_blobs[pin] = b
        if b is None or hashlib.sha256(b).hexdigest() != want:
            pin_ok = False
    if not pin_ok:
        missed.append("pin_hash")

    # tables_sha holds (checked above by load_frozen; reported as a leg)

    # prov
    prov_ok = False
    if entry_present:
        head = lines[:30]
        src_idx = [i for i, l in enumerate(head) if l.startswith("source:")]
        ver_idx = [i for i, l in enumerate(head) if l.strip() == "verified-at: " + DATE]
        rec_idx = [i for i, l in enumerate(head) if l.startswith("recheck:")]
        if src_idx and len(ver_idx) == 1 and len(rec_idx) == 1:
            if max(src_idx) < ver_idx[0] < rec_idx[0]:
                src_ids = set()
                for i in src_idx:
                    src_ids |= set(re.findall(r"(?<![A-Za-z0-9])S[0-9]{3}(?![0-9])", head[i]))
                k_cited = {r["sid"] for r in K}
                prov_ok = all(s in registry for s in src_ids) and k_cited <= src_ids
    if not prov_ok and entry_present:
        missed.append("prov")

    if not entry_present:
        # entry-dependent legs are not evaluated; only registry/README/pin/table legs run
        n_new = 0
        for sid in c1["new_row_ids"]:
            rr = registry.get(sid, [])
            cells = rr[0] if len(rr) == 1 and len(rr[0]) == 11 else None
            n_new += 1 if source_cell_ok(cells, c1["rows"][sid], c1["pin_suffix"], c1["rev_rule"], ENTRY) else 0
        if n_new != 8 and "new_rows" not in missed:
            missed.append("new_rows")
        out_missed = [x for x in dict.fromkeys(missed) if not x.startswith(("row:", "quote:", "host:", "source_cell:", "scope:", "tok:", "num:", "prov"))]
        ok = False
        print(f"MADO_AUTORELOAD_ENTRY: rev={a.rev} rows=0/30 hosts=0/3 sources=0/30 scope=0/30 content=0/33 "
              f"new_rows={n_new}/8 verdict=TARGET_MISSED missed={','.join(out_missed)}")
        sys.exit(1)

    # row grammar: candidate lines outside fences and HTML comments
    cand = {}
    in_fence, fence_ch, in_comment = False, "", False
    for line in lines:
        if in_comment:
            if "-->" in line:
                in_comment = False
            continue
        fm = re.match(r"^ {0,3}(```|~~~)", line)
        if fm:
            if not in_fence:
                in_fence, fence_ch = True, fm.group(1)
            elif fm.group(1) == fence_ch:
                in_fence = False
            continue
        if in_fence:
            continue
        if "<!--" in line and "-->" not in line:
            in_comment = True
            continue
        m = re.match(r"^\| (K\d\d|H\d\d) \|", line)
        if m:
            cand.setdefault(m.group(1), []).append(line)

    row_ok, prop_of, quote_of, src_of = {}, {}, {}, {}
    for rid in k_ids + h_ids:
        r = rows[rid]
        cs = cand.get(rid, [])
        ok = False
        if len(cs) == 1:
            line = cs[0]
            if line.endswith(" |") and line.count("|") == 6 and line.startswith("| "):
                cells = line[2:-2].split(" | ")
                if len(cells) == 5 and cells[0] == rid:
                    prop, src, pinln, qcell = cells[1], cells[2], cells[3], cells[4]
                    src_shape = bool(re.fullmatch(r"S[0-9]{3}", src)) if rid.startswith("K") else src == "host"
                    minlen = 40 if rid.startswith("K") else 20
                    if (src_shape and pinln == f"{r['pin']}:{r['line']}" and qcell == "`" + r["quote"] + "`"
                            and len(prop) >= minlen and prop == prop.strip()):
                        ok = True
                        prop_of[rid] = prop
                        src_of[rid] = src
                        quote_of[rid] = qcell[1:-1]
        row_ok[rid] = ok
    # tok/num use the row's quote cell (structurally parsed), not only the frozen one
    row_struct = {}
    for rid in k_ids + h_ids:
        cs = cand.get(rid, [])
        if len(cs) == 1 and cs[0].startswith("| ") and cs[0].endswith(" |"):
            cells = cs[0][2:-2].split(" | ")
            if len(cells) == 5 and cells[0] == rid and cells[4].startswith("`") and cells[4].endswith("`") and len(cells[4]) >= 2:
                row_struct[rid] = (cells[1], cells[4][1:-1])
    props = list(prop_of.values())
    for rid, p in prop_of.items():
        if props.count(p) > 1:
            row_ok[rid] = False
    a_rows = 0
    for rid in k_ids:
        if not row_ok[rid]:
            missed.append(f"row:{rid}")
    for rid in h_ids:
        if not row_ok[rid]:
            missed.append(f"row:{rid}")

    # quote:<id> and host:<id>
    quote_ok = {}
    for rid in k_ids + h_ids:
        r = rows[rid]
        b = pin_blobs.get(r["pin"])
        ln = b.split(b"\n") if b is not None else []
        qtext = r["quote"]
        if a.quote_leg == "carried":
            qtext = row_struct.get(rid, (None, None))[1]
        ok = qtext is not None and b is not None and 0 < r["line"] <= len(ln) and qtext.encode() in ln[r["line"] - 1]
        quote_ok[rid] = ok
        if not ok:
            missed.append(f"quote:{rid}")
    host_ok = {}
    for rid in h_ids:
        r = rows[rid]
        b = pin_blobs.get(r["pin"])
        ln = b.split(b"\n") if b is not None else []
        carried = row_struct.get(rid, (None, None))[1]
        host_ok[rid] = (b is not None and carried is not None and 0 < r["line"] <= len(ln)
                        and carried.encode() in ln[r["line"] - 1])
        if not (row_ok[rid] and quote_ok[rid] and host_ok[rid]):
            missed.append(f"host:{rid}")

    # source_cell and scope (K rows)
    pins_suffix = c1["pin_suffix"]
    rev_rule = c1["rev_rule"]
    src_ok, scope_pass = {}, {}
    for rid in k_ids:
        r = rows[rid]
        cells = None
        rr = registry.get(r["sid"], [])
        if len(rr) == 1 and len(rr[0]) == 11:
            cells = rr[0]
        ok = (cells is not None and src_of.get(rid) == r["sid"]
              and source_cell_ok(cells, r["pin"], pins_suffix, rev_rule, ENTRY))
        src_ok[rid] = bool(ok)
        if not ok:
            missed.append(f"source_cell:{rid}")
        sc = bool(cells is not None and scope_ok(cells[5], pins_suffix, r["pin"], r["line"]))
        scope_pass[rid] = sc
        if not sc:
            missed.append(f"scope:{rid}")

    # tok and num (K and H)
    content = 0
    tok_num = {}
    for rid in k_ids + h_ids:
        r = rows[rid]
        if rid not in row_struct:
            tok_num[rid] = False
            missed.append(f"tok:{rid}")
            missed.append(f"num:{rid}")
            continue
        prop, q = row_struct[rid]
        tok = bool(set(IDENT.findall(prop)) & set(IDENT.findall(q)))
        allowed = set(DIGITS.findall(q)) | {str(r["line"]), "0", "1", "2", "3"}
        for o in K + H:
            if o["pin"] == r["pin"] and o["id"] != rid:
                allowed.add(str(o["line"]))
        num = all(d in allowed for d in DIGITS.findall(prop))
        if not tok:
            missed.append(f"tok:{rid}")
        if not num:
            missed.append(f"num:{rid}")
        tok_num[rid] = tok and num
        if tok_num[rid]:
            content += 1

    # new_rows
    m_new = 0
    for sid in c1["new_row_ids"]:
        pin = c1["rows"][sid]
        rr = registry.get(sid, [])
        cells = rr[0] if len(rr) == 1 and len(rr[0]) == 11 else None
        if source_cell_ok(cells, pin, pins_suffix, rev_rule, ENTRY):
            m_new += 1
    if m_new != len(c1["new_row_ids"]):
        missed.append("new_rows")

    a_rows = sum(1 for rid in k_ids if row_ok[rid] and quote_ok[rid])
    b_hosts = sum(1 for rid in h_ids if row_ok[rid] and quote_ok[rid] and host_ok[rid])
    c_src = sum(1 for rid in k_ids if src_ok[rid])
    d_scope = sum(1 for rid in k_ids if scope_pass[rid])
    missed_u = []
    for x in missed:
        if x not in missed_u:
            missed_u.append(x)
    ok = (a_rows == 30 and b_hosts == 3 and c_src == 30 and d_scope == 30
          and content == 33 and m_new == 8 and not missed_u)
    verdict = "TARGET_MET" if ok else "TARGET_MISSED"
    print(f"MADO_AUTORELOAD_ENTRY: rev={a.rev} rows={a_rows}/30 hosts={b_hosts}/3 sources={c_src}/30 "
          f"scope={d_scope}/30 content={content}/33 new_rows={m_new}/8 verdict={verdict} "
          f"missed={','.join(missed_u) if missed_u else 'none'}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
