#!/usr/bin/env python3
"""PRED-C2-r38-v1 — request-socket contract ground admitted into the corpus.

Counts, at one committed revision, the three frozen target entries that land
the request socket's operational contract — its published flags, the live
bound in the host's own accept loop, and the upstream ceilings — on coverage
ground the lane did not hold at the round base. An entry counts only when
every clause holds:

  a  the entry exists at REV and did not exist at BASE
  b  its first 15 lines carry `source:`, `verified-at:` (a YYYY-MM-DD date)
     and `recheck:` (an ISO date, `NNd`, or a `on-*` cadence); the `source:`
     lines name at least one S-id
  c  every cited S-id has exactly one `## Registry` row of corpus/SOURCES.md
     with 11 cells, status `mined`, and `used-by` naming the entry
  d  every cited S-id names, in `## Gate` of corpus/lessons/round-38.md, a
     `GATE` line whose (receipt path, sha256) equals the frozen pin for that
     id — a committed receipt under `.ufo/waves/round-38/fetch/` bound to the
     bytes the L1 opened; only pin-matching Gate lines count for d, f and g
     (the v2 hole M37-5 named: any committed file, including the entry
     itself, satisfied the digest check)
  e  a `## Coverage map` table row of corpus/README.md names
     `knowledge/<basename>` in its first cell
  f  each of the entry's frozen surface tokens occurs in the entry and in at
     least one receipt its bound Gate lines pin
  g  the entry states its evidence: for every cited S-id, the body carries
     one of that id's located Gate quotes verbatim (a located quote is not a
     bare surface token and is at least 3 words or 24 characters) and at
     least one `**OBS**` line naming the id
  l  lineage: a normalized (id-free, case/*/` -insensitive) scan finds the
     frozen claim content — at least NEED of the frozen phrases — so the
     package's ground was carried, not only its citation wiring

Precondition (exit 2 when false): no corpus/knowledge/ file at BASE contains
any frozen surface token — the ground is unheld at the base.

Target: admitted == 3 -> TARGET_MET, exit 0; otherwise TARGET_MISSED, exit 1.
Setup or usage errors exit 2. Git runs with every ambient GIT_* variable
removed, so the caller's environment cannot redirect the repository.
"""
import argparse
import hashlib
import os
import re
import subprocess
import sys

PRED = "PRED-C2-r38-v1"
BASE_DEFAULT = "f6e3247f73152a39afb86066af48f3cedf95fb0a"
TARGETS = {
    "corpus/knowledge/hyprctl-flags-r28.md":
        ("select instance", "force state refresh"),
    "corpus/knowledge/request-socket-live-bound-r8.md":
        ("poll(pollfds", "1023"),
    "corpus/knowledge/request-limits-upstream-r31.md":
        ("REQUEST_LIMIT", "FOLLOW_QUEUE_LIMIT"),
}
LESSON = "corpus/lessons/round-38.md"
ROW_RE = re.compile(r"^ {0,3}\|\s*(S\d{3,})\s*\|")
GATE_RE = re.compile(r'^GATE (S\d{3,}) receipt=(\S+) sha256=([0-9a-f]{64}) quote="(.+)"\s*$')
ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}

PINS = {
    "S158": (".ufo/waves/round-38/fetch/S158.bin",
             "798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa"),
    "S187": (".ufo/waves/round-38/fetch/S187.bin",
             "136e5511fba5524a5cb1685668429ee28f7a2710c70104441eeb2b674f6a37a4"),
    "S221": (".ufo/waves/round-38/fetch/S221.bin",
             "35046ba0dc1dd1db4b1e8548e7e6a0be9f0ffc0051c055f66ddee5451879d30a"),
    "S253": (".ufo/waves/round-38/fetch/S253.bin",
             "3ba8e461bd466a8a716a7a29a2a917d94a4d9af6fb87904a2c76978f4833d6cf"),
    "S258": (".ufo/waves/round-38/fetch/stat-sockets.txt",
             "fcc608203f66879f469b61761619e555e04b67127f215d495bd35b9b27421928"),
    "S277": (".ufo/waves/round-38/fetch/S277.bin",
             "ff561fe0d09641db41729fc3f02238cb128313ad0365d819f91097df472781e6"),
}

LINEAGE = {
    "corpus/knowledge/hyprctl-flags-r28.md": (3, [
        "output in json",
        "select instance",
        "force state refresh",
        "dispatched by the compositor synchronously",
    ]),
    "corpus/knowledge/request-socket-live-bound-r8.md": (3, [
        "temporal",
        "five-second",
        "synchronously",
        "1023",
        "no length prefix",
    ]),
    "corpus/knowledge/request-limits-upstream-r31.md": (3, [
        "1 mib",
        "64 kib",
        "accumulated request",
        "queued",
        "later",
    ]),
}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
RECHECK_RE = re.compile(r"^(\d{4}-\d{2}-\d{2}|\d+d|on-[a-z-]+)$")
SURFACE_TOKENS = ("select instance", "force state refresh", "poll(pollfds",
                  "REQUEST_LIMIT", "FOLLOW_QUEUE_LIMIT")


class Setup(Exception):
    pass


def git(repo, *args, binary=False):
    p = subprocess.run(["git", "-C", repo, *args], capture_output=True, env=ENV)
    if p.returncode != 0:
        return None
    return p.stdout if binary else p.stdout.decode("utf-8", "replace")


def show(repo, rev, path, binary=False):
    return git(repo, "show", f"{rev}:{path}", binary=binary)


def section(text, heading):
    out, inside = [], False
    for line in text.splitlines():
        if line.strip() == heading:
            inside = True
            continue
        if inside and line.startswith("## "):
            break
        if inside:
            out.append(line)
    return out


def registry_rows(text):
    rows = {}
    for line in section(text, "## Registry"):
        m = ROW_RE.match(line)
        if m:
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            rows.setdefault(m.group(1), []).append(cells)
    return rows


def norm(text):
    return re.sub(r"[*`]", "", re.sub(r"\bS\d{3,}\b", " ", text.lower()))


def quote_floor_ok(quote, tokens):
    if quote.strip() in tokens or re.fullmatch(r"S\d{3,}", quote.strip()):
        return False
    return len(quote.split()) >= 3 or len(quote) >= 24


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--base", default=BASE_DEFAULT)
    a = ap.parse_args()
    repo = os.path.abspath(a.repo)
    rev = git(repo, "rev-parse", "--verify", f"{a.rev}^{{commit}}")
    base = git(repo, "rev-parse", "--verify", f"{a.base}^{{commit}}")
    if not rev or not base:
        raise Setup("unresolvable revision")
    rev, base = rev.strip(), base.strip()

    base_files = git(repo, "ls-tree", "-r", "--name-only", base, "--", "corpus/knowledge") or ""
    held = []
    for path in base_files.split():
        body = show(repo, base, path) or ""
        held += [f"{path}:{t}" for t in SURFACE_TOKENS if t in body]
    if held:
        raise Setup("ground_held_at_base " + ",".join(held))

    sources = show(repo, rev, "corpus/SOURCES.md") or ""
    rows = registry_rows(sources)
    lesson = show(repo, rev, LESSON) or ""
    gates = {}
    for line in section(lesson, "## Gate"):
        m = GATE_RE.match(line.strip())
        if m:
            gates.setdefault(m.group(1), []).append(m.groups()[1:])
    readme = show(repo, rev, "corpus/README.md") or ""
    map_cells = [l.strip().strip("|").split("|")[0] for l in section(readme, "## Coverage map")
                 if l.strip().startswith("|")]

    admitted = 0
    for path, tokens in TARGETS.items():
        body = show(repo, rev, path)
        c = dict.fromkeys("abcdefgl", 0)
        c["a"] = int(body is not None and show(repo, base, path) is None)
        body = body or ""
        head = body.splitlines()[:15]
        src_lines = [l for l in head if re.match(r"^[-* ]*source *:", l)]
        ids = sorted(set(re.findall(r"\bS\d{3,}\b", " ".join(src_lines))))
        ver = [l.split(":", 1)[1].strip() for l in head if re.match(r"^[-* ]*verified-at *:", l)]
        rec = [l.split(":", 1)[1].strip() for l in head if re.match(r"^[-* ]*recheck *:", l)]
        c["b"] = int(bool(ids) and ver and rec
                     and all(DATE_RE.match(v.split()[0] if v.split() else "") for v in ver)
                     and all(RECHECK_RE.match(r.split()[0] if r.split() else "") for r in rec))
        c["c"] = int(bool(ids) and all(
            len(rows.get(i, [])) == 1
            and len(rows[i][0]) == 11 and rows[i][0][7] == "mined"
            and path in [u.strip() for u in rows[i][0][10].split(",")]
            for i in ids))
        receipts = []
        d_ok = g_ok = bool(ids)
        lines = body.splitlines()
        for i in ids:
            pin = PINS.get(i)
            good = stated = False
            for rpath, digest, quote in gates.get(i, []):
                if pin is None or rpath != pin[0] or (pin[1] is not None and digest != pin[1]):
                    continue
                blob = show(repo, rev, rpath, binary=True)
                if (blob is not None and hashlib.sha256(blob).hexdigest() == digest
                        and len(quote.split()) <= 25 and quote.encode() in blob
                        and quote_floor_ok(quote, tokens)):
                    good = True
                    receipts.append(blob)
                    stated = stated or quote in body
            d_ok = d_ok and good
            g_ok = g_ok and stated and any("**OBS**" in l and re.search(rf"\b{i}\b", l) for l in lines)
        c["d"] = int(d_ok)
        c["g"] = int(g_ok)
        base_name = "knowledge/" + path.rsplit("/", 1)[1]
        c["e"] = int(any(base_name in cell for cell in map_cells))
        c["f"] = int(all(t in body and any(t.encode() in b for b in receipts) for t in tokens))
        need, phrases = LINEAGE[path]
        hits = sum(1 for p in phrases if p in norm(body))
        c["l"] = int(hits >= need)
        ok = int(all(c.values()))
        admitted += ok
        print(f"{PRED} entry={path} " + " ".join(f"{k}={v}" for k, v in c.items())
              + f" ids={','.join(ids) or '-'} lineage={hits}/{need} ok={ok}")

    verdict = "TARGET_MET" if admitted == len(TARGETS) else "TARGET_MISSED"
    print(f"{PRED} admitted={admitted}/{len(TARGETS)} verdict={verdict} rev={rev} base={base}")
    return 0 if verdict == "TARGET_MET" else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Setup as e:
        print(f"{PRED} SETUP {e}")
        sys.exit(2)
