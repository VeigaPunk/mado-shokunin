#!/usr/bin/env python3
"""RevN4Matrix (round-50 w1): independent re-check of the N4 full-matrix receipt.

Item (round-49 w2-items.json line 31, retargeted): verify 98 rows, set equality with the
round-48 summary.json, every value equal, and git diff --stat of round-48 paths between
03e4ae76aff7a4be59cb69970dd553baa319695a (round-49 base) and
8ae47b957034ae21012bbf09173cca2c48be345e (round-49 tip = round-50 base) empty.

Read-only on the lane; writes only its own receipt (arg 1). Run with: python3 -I verify-matrix.py OUT.txt
"""
import hashlib
import json
import re
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
BASE = "03e4ae76aff7a4be59cb69970dd553baa319695a"
TIP = "8ae47b957034ae21012bbf09173cca2c48be345e"
N4 = LANE + "/.ufo/waves/round-49/w1/ExecN4Matrix"
R48 = LANE + "/.ufo/waves/round-48/receipts/v2"
SUM_NAME = "c2v2-revc2counter-summary.json"
MAT_NAME = "c2v2-revc2counter-matrix.txt"
EXPECT_HEADER_SUM_SHA = "f2b6af9bbbc1eee804306941e31af174d7071f4aed8a33f09722e61c9df4106e"
EXPECT_FROZEN_SHA = "ae4ce14c8878bfb9b832cad26d6323fc6372859ad385d7b22522c957ca90e474"
RECOVERED = ("a-rev-base-direct", "a-entry-at-base")
ROW = re.compile(r"^(\S+)\s+(\S+)\s+rc=(\d+)\s+(.*)$")

out_lines = []
fails = []


def say(s=""):
    out_lines.append(s)


def bad(check, detail):
    fails.append(check)
    say(f"FAIL {check}: {detail}")


def ok(check, detail=""):
    say(f"PASS {check}" + (f" {detail}" if detail else ""))


def sha256_path(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def git(*args):
    r = subprocess.run(["git", "-C", LANE, *args], capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} rc={r.returncode}: {r.stderr.strip()}")
    return r.stdout


def parse_rows(path):
    rows, footer = [], None
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if line.startswith("#"):
                continue
            m = ROW.match(line)
            if m and not line.startswith("rows "):
                rows.append({"name": m.group(1), "declared": m.group(2),
                             "rc": int(m.group(3)), "last": m.group(4)})
            elif line.startswith("rows "):
                footer = line
    return rows, footer


def main():
    receipt_path = sys.argv[1]

    # ---------- inputs ----------
    full_path = f"{N4}/c2v2-matrix-full.txt"
    frozen_seat = f"{N4}/frozen-c2v2-matrix.txt"
    sum_seat = f"{N4}/source-summary.json"
    sum_r48 = f"{R48}/{SUM_NAME}"
    mat_r48 = f"{R48}/{MAT_NAME}"

    say("# RevN4Matrix round-50 w1 receipt (independent re-check)")
    say("# lane: mado-shokunin; base 03e4ae76aff7a4be59cb69970dd553baa319695a tip 8ae47b957034ae21012bbf09173cca2c48be345e")
    say("")

    # ---------- 0. input identity: seat copies vs round-48 committed originals ----------
    say("## 0. input identity (seat copies vs round-48 committed originals)")
    sha_full = sha256_path(full_path)
    sha_frozen_seat = sha256_path(frozen_seat)
    sha_sum_seat = sha256_path(sum_seat)
    sha_sum_r48 = sha256_path(sum_r48)
    sha_mat_r48 = sha256_path(mat_r48)
    say(f"sha256(c2v2-matrix-full.txt)          = {sha_full}")
    say(f"sha256(frozen-c2v2-matrix.txt [seat]) = {sha_frozen_seat}")
    say(f"sha256(source-summary.json [seat])    = {sha_sum_seat}")
    say(f"sha256({SUM_NAME} [r48]) = {sha_sum_r48}")
    say(f"sha256({MAT_NAME} [r48]) = {sha_mat_r48}")
    ok("matrix-sha-matches-header") if sha_full == "bf496e777c187c6a7c4db8665227321c14072a8d3993071d3c20dc7c6fddff2f" else bad("matrix-sha-matches-header", sha_full)
    ok("frozen-sha-matches-header") if sha_frozen_seat == EXPECT_FROZEN_SHA else bad("frozen-sha-matches-header", sha_frozen_seat)
    ok("summary-sha-matches-header") if sha_sum_seat == EXPECT_HEADER_SUM_SHA else bad("summary-sha-matches-header", sha_sum_seat)
    ok("seat-summary-equals-r48-original") if sha_sum_seat == sha_sum_r48 else bad("seat-summary-equals-r48-original", f"{sha_sum_seat} != {sha_sum_r48}")
    ok("seat-frozen-equals-r48-original") if sha_frozen_seat == sha_mat_r48 else bad("seat-frozen-equals-r48-original", f"{sha_frozen_seat} != {sha_mat_r48}")

    # blob identity at both revs for the two round-48 committed originals + harness
    for p in (f".ufo/waves/round-48/receipts/v2/{SUM_NAME}",
              f".ufo/waves/round-48/receipts/v2/{MAT_NAME}",
              ".ufo/waves/round-48/l1-draft/v2/c2v2-harness-revc2counter.py"):
        b_base = git("rev-parse", f"{BASE}:{p}").strip()
        b_tip = git("rev-parse", f"{TIP}:{p}").strip()
        same = b_base == b_tip
        say(f"blob {p}: base={b_base[:12]} tip={b_tip[:12]} {'SAME' if same else 'DIFFER'}")
        ok(f"blob-unchanged {p}") if same else bad(f"blob-unchanged {p}", f"{b_base} != {b_tip}")
    say("")

    # ---------- 1. git diff of round-48 paths base..tip ----------
    say("## 1. git diff of round-48 paths between base and tip (item requirement: empty)")
    stat = git("diff", "--stat", BASE, TIP, "--", ".ufo/waves/round-48/")
    names = git("diff", "--name-only", BASE, TIP, "--", ".ufo/waves/round-48/")
    ns = [l for l in names.splitlines() if l.strip()]
    say(f"git diff --stat output: {stat!r}")
    say(f"git diff --name-only line count: {len(ns)}")
    ok("diff-stat-round48-empty") if not stat.strip() and not ns else bad("diff-stat-round48-empty", f"changed={ns}")
    # path-set equality under round-48 at both revs
    tree_b = set(git("ls-tree", "-r", "--name-only", BASE, "--", ".ufo/waves/round-48/").splitlines())
    tree_t = set(git("ls-tree", "-r", "--name-only", TIP, "--", ".ufo/waves/round-48/").splitlines())
    say(f"round-48 path count at base={len(tree_b)} tip={len(tree_t)}")
    ok("round48-path-set-equal") if tree_b == tree_t else bad(
        "round48-path-set-equal", f"only-base={sorted(tree_b - tree_t)[:10]} only-tip={sorted(tree_t - tree_b)[:10]}")
    say("")

    # ---------- 2. summary vs full matrix ----------
    with open(sum_seat, encoding="utf-8") as f:
        summary = json.load(f)
    if isinstance(summary, dict):
        recs = summary.get("rows", summary)
        if isinstance(recs, dict):
            recs = list(recs.values())
    else:
        recs = summary
    by_name = {}
    order = []
    for r in recs:
        by_name[r["name"]] = r
        order.append(r["name"])

    rows, footer = parse_rows(full_path)
    say("## 2. full matrix vs round-48 summary.json")
    say(f"matrix rows parsed: {len(rows)}; summary records: {len(recs)}; footer: {footer!r}")
    ok("row-count-98") if len(rows) == 98 else bad("row-count-98", str(len(rows)))
    ok("count-equals-summary") if len(rows) == len(recs) else bad("count-equals-summary", f"{len(rows)} vs {len(recs)}")
    mnames = [r["name"] for r in rows]
    ok("set-equality") if set(mnames) == set(order) else bad(
        "set-equality", f"matrix-only={sorted(set(mnames) - set(order))} summary-only={sorted(set(order) - set(mnames))}")
    dups = sorted({n for n in mnames if mnames.count(n) > 1})
    ok("no-duplicate-names") if not dups else bad("no-duplicate-names", str(dups))
    ok("order-equals-summary") if mnames == order else bad("order-equals-summary", "sequence differs")
    ok("footer-rows-98") if footer == "rows 98" else bad("footer-rows-98", repr(footer))
    vbad = []
    for r in rows:
        s = by_name.get(r["name"])
        if s is None:
            continue
        if (r["declared"], r["rc"], r["last"]) != (s["declared"], s["rc"], s["last"]):
            vbad.append(r["name"])
    ok("row-values-match-summary(all 98)") if not vbad else bad("row-values-match-summary(all 98)", f"mismatched={vbad[:5]}")
    say("")

    # ---------- 3. frozen 96-row matrix ----------
    say("## 3. frozen 96-row round-48 matrix")
    frows, ffooter = parse_rows(frozen_seat)
    has_pos = any(l.startswith("pos rc ") for l in open(frozen_seat, encoding="utf-8", errors="replace"))
    fnames = [r["name"] for r in frows] + (["pos"] if has_pos else [])
    missing = [n for n in order if n not in set(fnames)]
    say(f"frozen data rows: {len(frows)} (+1 pos clauses line); frozen names: {len(fnames)}; missing vs summary: {missing}")
    ok("frozen-row-count-96") if len(fnames) == 96 else bad("frozen-row-count-96", str(len(fnames)))
    ok("frozen-missing-exactly-two") if sorted(missing) == sorted(RECOVERED) else bad("frozen-missing-exactly-two", str(missing))
    # the frozen pos line is the clauses projection (print site 412), recorded by name only
    ok("frozen-pos-line-present") if has_pos else bad("frozen-pos-line-present", "absent")
    # every carried row: declared/rc equal, last is the 96-char truncation of summary last
    tbad = []
    for r in frows:
        s = by_name.get(r["name"])
        if s is None:
            tbad.append(f"{r['name']}: not in summary")
            continue
        if r["declared"] != s["declared"] or r["rc"] != s["rc"]:
            tbad.append(f"{r['name']}: declared/rc differ")
        elif r["last"] != s["last"][: len(r["last"])]:
            tbad.append(f"{r['name']}: last not a prefix of summary last")
    ok("frozen-row-values-consistent") if not tbad else bad("frozen-row-values-consistent", str(tbad[:5]))
    say("")

    # ---------- 4. recovered rows match the receipt's own recovery block ----------
    say("## 4. recovered rows vs the receipt's recovery comments")
    txt = open(full_path, encoding="utf-8").read()
    rbad = []
    for name in RECOVERED:
        row = next((r for r in rows if r["name"] == name), None)
        s = by_name.get(name)
        if row is None or s is None:
            rbad.append(f"{name}: absent")
        elif (row["declared"], row["rc"], row["last"]) != (s["declared"], s["rc"], s["last"]):
            rbad.append(f"{name}: values differ from summary")
        elif f"name={name}" not in txt:
            rbad.append(f"{name}: no recovery comment block")
    ok("recovered-rows-consistent") if not rbad else bad("recovered-rows-consistent", str(rbad))
    say("")

    # ---------- verdict ----------
    say("")
    say(f"RESULT {'PASS' if not fails else 'FAIL'} failures={len(fails)}")
    if fails:
        say("failed checks: " + ", ".join(fails))
    with open(receipt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(out_lines) + "\n")
    print(f"RESULT {'PASS' if not fails else 'FAIL'} failures={len(fails)}; receipt={receipt_path}")
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
