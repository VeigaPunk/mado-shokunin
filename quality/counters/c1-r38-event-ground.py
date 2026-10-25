#!/usr/bin/env python3
"""PRED-C1-r38-v3 — event-socket delivery ground admitted into the corpus (v3).

Round-38 v3 of the round-37 instrument, repaired against the wave-1 cribs
recorded in `corpus/lessons/round-37.md` M37-5 (routed defect; v2 stays frozen
beside it, never edited). Clauses a–g are v2's; the v3 additions are h–l:

  h  pin binding — every cited S-id must name, in `## Gate` of
     corpus/lessons/round-37.md, a `GATE` line whose (receipt path, sha256)
     equals the frozen pin for that id: a file under
     `.ufo/waves/round-37/fetch/` with the digest measured when the L1 opened
     the source. Only pin-matching Gate lines count for d, f and g. A receipt
     that is the entry itself, a fabricated id, or a same-path receipt with a
     different digest cannot be bound (v2 F1).
  i  quote floor — a Gate quote is not a bare surface token (no frozen token,
     no `<id>` token) and is at least 3 words or at least 24 characters
     (v2 F2: `"e"` and `MAX_QUEUED_EVENTS` satisfied d and g).
  j  unique row — every cited id has exactly one `## Registry` row (v2 F3: an
     appended contradicting row passed c alongside the held one).
  k  header values — `verified-at:` carries a YYYY-MM-DD date and `recheck:`
     carries an ISO date, an `NNd` count, or a `on-*` cadence (v2 accepted `x`).
  l  lineage — the entry carries the package's claim content, not only its
     wiring: a normalized (id-free, case/*/` -insensitive) scan must find at
     least four of seven frozen claim phrases for the package entry, or two of
     three frozen mechanism phrases for the observability entry (v2 F6: the
     refused r28 measurement pasted verbatim met the target; k3 passed by
     lifting the receipt's own wording). This is a floor, not a proof of
     comprehension: the residual crib that states real quotes and mechanism
     phrases without doing the work is the same accept-path tradeoff the
     round-37 clause test recorded — it is reported, not hidden.

All other rules are v2's: a new-since-base entry, mined `## Registry` rows
with `used-by` naming the entry, a `## Coverage map` row, frozen surface
tokens present in the entry and in a bound receipt, and OBS lines naming each
cited id next to one of its located Gate quotes.

Precondition (exit 2 when false): no corpus/knowledge/ file at BASE contains
any frozen surface token — the ground is unheld at the base.

Target: admitted == 2 -> TARGET_MET, exit 0; otherwise TARGET_MISSED, exit 1.
Setup or usage errors exit 2. Git runs with every ambient GIT_* variable
removed, so the caller's environment cannot redirect the repository.
"""
import argparse
import hashlib
import os
import re
import subprocess
import sys

PRED = "PRED-C1-r38-v3"
BASE_DEFAULT = "b4e47e980bfb0cbc8a4e788f59a41db858751fd8"
TARGETS = {
    "corpus/knowledge/event-delivery-limits-r26.md":
        ("MAX_QUEUED_EVENTS", "overflowed event queue"),
    "corpus/knowledge/event-queue-observability-r37.md":
        ("debug:disable_logs", "m_logsEnabled"),
}
LESSON = "corpus/lessons/round-37.md"
ROW_RE = re.compile(r"^ {0,3}\|\s*(S\d{3,})\s*\|")
GATE_RE = re.compile(r'^GATE (S\d{3,}) receipt=(\S+) sha256=([0-9a-f]{64}) quote="(.+)"\s*$')
ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}

# Frozen pin table: id -> (receipt path, sha256), the receipts the L1 opened in
# round 37 (digests recorded in corpus/lessons/round-37.md `## Gate`). A Gate
# line matches clause d only when both cells equal these bytes.
PINS = {
    "S189": (".ufo/waves/round-37/fetch/S189.bin",
             "eea605dfe5ce09e1f92a67ec478bf61a19894c6e0ee3302c0393521a2ee9540d"),
    "S201": (".ufo/waves/round-37/fetch/S201.bin",
             "799bf02f6d18ae041ee95e136505ac98190890200c702e29791d446278bb4f9e"),
    "S212": (".ufo/waves/round-37/fetch/S212.bin",
             "1e19d92638e7923f0e72f6e65c83f579e32b41d588d166d6efef543c3f97d7e9"),
    "S213": (".ufo/waves/round-37/fetch/S213.receipt.txt",
             "1c1b0ce149ecd7b1d20b0a83f266197c89c9f5334d17dc035fe499d93272ce58"),
    "S214": (".ufo/waves/round-37/fetch/S214.bin",
             "d04e3a2fe5c73ad8684377856ce8301e493929ed9f391e405fde4975eaf6b868"),
    "S215": (".ufo/waves/round-37/fetch/S215.bin",
             "a76f05079454e1f6d4402144e1673cc1cb890d285fbeb947d5afdb004ad97754"),
    "S216": (".ufo/waves/round-37/fetch/S216.bin",
             "74833ecbf0e2b6f8ad84345ac0716a3295a0e347420a188be0ab4f6a684af7c0"),
    "S217": (".ufo/waves/round-37/fetch/S217.bin",
             "aeb07ba1ba1fd5cfdb75aaf7434910c887096c24952f1a6788f71a4d7dbe78fe"),
}
# Clause l: normalized (lowercased, ids and *` stripped) claim phrases whose
# presence shows the package's ground was carried, not only its wiring.
LINEAGE = {
    "corpus/knowledge/event-delivery-limits-r26.md": (4, [
        "queue",
        "cap",
        "removed",
        "writeoffset",
        "eagain",
        "partial writes are resumed",
        "1024",
    ]),
    "corpus/knowledge/event-queue-observability-r37.md": (2, [
        "null channel",
        "returns before",
        "core-logger",
    ]),
}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
RECHECK_RE = re.compile(r"^(\d{4}-\d{2}-\d{2}|\d+d|on-[a-z-]+)$")


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
        for toks in TARGETS.values():
            held += [f"{path}:{t}" for t in toks if t in body]
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
        c = dict.fromkeys("abcdefghjkl", 0)
        c["a"] = int(body is not None and show(repo, base, path) is None)
        body = body or ""
        head = body.splitlines()[:15]
        src_lines = [l for l in head if re.match(r"^[-* ]*source *:", l)]
        ids = sorted(set(re.findall(r"\bS\d{3,}\b", " ".join(src_lines))))
        c["b"] = int(bool(ids)
                     and any(re.match(r"^[-* ]*verified-at *:", l) for l in head)
                     and any(re.match(r"^[-* ]*recheck *:", l) for l in head))
        c["c"] = int(bool(ids) and all(
            # registry rows are unique per id and must bind the entry in used-by
            len(rows.get(i, [])) == 1 and (
                lambda r: len(r) == 11 and r[7] == "mined"
                          and path in [u.strip() for u in r[10].split(",")]
            )(rows[i][0])
            for i in ids))
        # k: header values actually parse
        ver = [l.split(":", 1)[1].strip() for l in head if re.match(r"^[-* ]*verified-at *:", l)]
        rec = [l.split(":", 1)[1].strip() for l in head if re.match(r"^[-* ]*recheck *:", l)]
        c["k"] = int(bool(ver) and bool(rec)
                     and all(DATE_RE.match(v.split()[0] if v.split() else "") for v in ver)
                     and all(RECHECK_RE.match(r.split()[0] if r.split() else "") for r in rec))
        # h+j: pin-bound, unique-row Gate wiring
        h_ok = bool(ids)
        j_ok = bool(ids)
        pin_gates = {}
        for i in ids:
            pin = PINS.get(i)
            good = []
            for rpath, digest, quote in gates.get(i, []):
                if pin and (rpath, digest) == pin and quote_floor_ok(quote, tokens):
                    good.append((rpath, digest, quote))
            pin_gates[i] = good
            h_ok = h_ok and bool(good)
            j_ok = j_ok and len(rows.get(i, [])) == 1
        c["h"] = int(h_ok)
        c["j"] = int(j_ok)
        # d+f+g scored only on pin-matching Gate lines
        receipts = []
        d_ok = g_ok = bool(ids)
        lines = body.splitlines()
        for i in ids:
            good = stated = False
            for rpath, digest, quote in pin_gates.get(i, []):
                blob = show(repo, rev, rpath, binary=True)
                if (blob is not None and hashlib.sha256(blob).hexdigest() == digest
                        and len(quote.split()) <= 25 and quote.encode() in blob):
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
