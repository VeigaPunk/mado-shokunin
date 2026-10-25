#!/usr/bin/env python3
"""RevC1Clause attack-tree builder for PRED-C1-r35-v1.

Constructs scored trees under .ufo/waves/round-35/scratch/RevC1Clause/trees/
attempting to violate individual load-bearing clauses while still printing
TARGET_MET. Frozen counter and frozen.json are only read, never written.
"""
import json
import os
import re
import shutil
from pathlib import Path

WAVE = Path("/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-35")
OUT = WAVE / "scratch" / "RevC1Clause" / "trees"
FETCH = WAVE / "fetch"
FROZEN = json.loads((WAVE / "c1" / "frozen.json").read_text())
ENTRIES = FROZEN["entries"]          # rel path -> [sid, ...]
RECEIPTS = FROZEN["receipts"]        # sid -> {path, sha256}
ALL_SIDS = sorted(RECEIPTS)


def located_line(sid: str) -> str:
    for line in (FETCH / f"{sid}.receipt.txt").read_bytes().split(b"\n"):
        if line.startswith(b"located:"):
            return line.decode()
    raise SystemExit(f"no located line in {sid} receipt")


QUOTES = {sid: located_line(sid) for sid in ALL_SIDS}


def entry_text(ids, extra=""):
    lines = ["# probe entry", ""]
    lines += [f"gate-quote: {sid} {QUOTES[sid]}" for sid in ids]
    if extra:
        lines.append(extra)
    return "\n".join(lines) + "\n"


def row_line(sid, *, recheck="on-change", status="mined", used_by=None,
             teaches="teaches"):
    if used_by is None:
        citing = [rel for rel, ids in ENTRIES.items() if sid in ids]
        used_by = ", ".join(sorted(citing))
    anchor = (f"receipt {RECEIPTS[sid]['path']} "
              f"sha256 {RECEIPTS[sid]['sha256']}")
    cells = [sid, f"src-{sid}", "own-work", "A", "scope", anchor,
             teaches, status, "2026-10-24", recheck, used_by]
    return "| " + " | ".join(cells) + " |"


HEADER = ("| id | source | kind | tier | scope | anchor | teaches | status |"
          " opened | recheck | used-by |\n"
          "|---|---|---|---|---|---|---|---|---|---|---|\n")

DUMMY_S999 = ("| S999 | dummy row | docs | B | dummy | dummy-anchor |"
              " dummy teaches | queued | 2026-10-01 | 30d | — |\n")


def make(name, *, sources_md=None, recheck_over=None, status_over=None,
         used_by_over=None, teaches_over=None, receipt_mut=None,
         entry_extra=None, entry_mut=None, post=None):
    t = OUT / name
    shutil.rmtree(t, ignore_errors=True)
    (t / "corpus" / "knowledge").mkdir(parents=True)
    (t / ".ufo" / "waves" / "round-35" / "fetch").mkdir(parents=True)
    for sid in ALL_SIDS:
        data = (FETCH / f"{sid}.receipt.txt").read_bytes()
        if receipt_mut:
            data = receipt_mut(sid, data)
        (t / ".ufo" / "waves" / "round-35" / "fetch"
         / f"{sid}.receipt.txt").write_bytes(data)
    for rel, ids in ENTRIES.items():
        p = t / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        text = entry_text(ids,
                          extra=(entry_extra or {}).get(rel, ""))
        if entry_mut:
            text = entry_mut(rel, ids, text)
        p.write_text(text)
    if sources_md is None:
        rows = [row_line(sid,
                         recheck=(recheck_over or {}).get(sid, "on-change"),
                         status=(status_over or {}).get(sid, "mined"),
                         used_by=(used_by_over or {}).get(sid),
                         teaches=(teaches_over or {}).get(sid, "teaches"))
                for sid in ALL_SIDS]
        sources_md = HEADER + "\n".join(rows) + "\n"
    (t / "corpus" / "SOURCES.md").write_text(sources_md)
    if post:
        post(t)
    return t


def first_26_words_substr(sid: str) -> str:
    """A contiguous >=26-word substring of the authentic receipt bytes."""
    raw = (FETCH / f"{sid}.receipt.txt").read_bytes()
    line = max(raw.split(b"\n"), key=len)
    ends = [m.end() for m in re.finditer(rb"\S+", line)]
    return line[:ends[25]].decode()


def main():
    OUT.mkdir(parents=True, exist_ok=True)

    # 1. Sanity: minimal honest tree -> expect TARGET_MET.
    make("golden-lite")

    # 2. break clause 7 (digest-match): S203 receipt bytes tampered; anchor
    #    still carries the spec-recorded sha256, which is no longer the
    #    sha256 of the file at the named path. -> expect TARGET_MET.
    make("break-digest-append",
         receipt_mut=lambda sid, d: d + b"\n# tampered byte\n"
         if sid == "S203" else d)

    # 3. break clauses 7+8 (digest-match + gate-quote-substring): every
    #    receipt replaced by fabricated bytes containing only the quote.
    # 11b-11d. clause 2, file==registry reading: a second row-shaped line
    #     carrying S203 that ROW_RE cannot see -> human sees two rows
    #     carrying the id, counter sees one.
    rows_base = "\n".join(row_line(sid) for sid in ALL_SIDS)
    make("att-row-bom-dup",
         sources_md=HEADER + rows_base + "\n\ufeff" + row_line("S203") + "\n")
    make("att-row-quote-dup",
         sources_md=HEADER + rows_base + "\n> " + row_line("S203") + "\n")
    make("att-row-indent-dup",
         sources_md=HEADER + rows_base + "\n    " + row_line("S203") + "\n")

    #    quote is still a substring of the file bytes; anchors still carry
    #    the spec sha256 (not the files' sha256); the authentic receipts
    #    are absent entirely. -> expect TARGET_MET.
    make("break-digest-fabricate",
         receipt_mut=lambda sid, d:
         b"# fabricated receipt body for " + sid.encode() + b"\n"
         + QUOTES[sid].encode() + b"\n")

    # 4. break clause 6 (recheck-valid): recheck '2026-02-30' matches the
    #    ISO shape but is not a calendar date (census epoch() -> E09).
    make("break-recheck-iso", recheck_over={"S203": "2026-02-30"})

    # 5. break clause 2 (row-unique): registry section exists but holds
    #    only a dummy S999 row; all eight cited rows sit under '## Notes',
    #    so per the fleet contract (census E12) zero registry rows carry
    #    each id -> expect TARGET_MET.
    rows = "\n".join(row_line(sid) for sid in ALL_SIDS)
    make("break-row-unique-section",
         sources_md="## Registry\n\n" + HEADER + DUMMY_S999 +
                    "\n## Notes\n\n" + HEADER + rows + "\n")

    # 6. clause-8-adjacent 'exactly one gate-quote line': shadow line with
    #    no space after the colon is invisible to the counter.
    make("att-quote-shadow",
         entry_extra={"corpus/knowledge/idle-lock-never-asked-r12.md":
                      "gate-quote:S203 shadow quote for the same id"})

    # 7-10. clause 1 (entry-regular) enforcement probes -> expect MISSED.
    def post_symlink(t):
        p = t / "corpus" / "knowledge" / "idle-lock-never-asked-r12.md"
        p.unlink()
        os.symlink("../SOURCES.md", p)
    make("att-entry-symlink", post=post_symlink)

    def post_dirsymlink(t):
        kd = t / "corpus" / "knowledge"
        real = t / "corpus" / "knowledge-real"
        real.mkdir()
        for rel in ENTRIES:
            os.rename(kd / Path(rel).name, real / Path(rel).name)
        kd.rmdir()
        os.symlink("knowledge-real", kd)
    make("att-entry-dir-symlink", post=post_dirsymlink)

    def post_hardlink(t):
        p = t / "corpus" / "knowledge" / "idle-lock-offered-in-the-bar-r15.md"
        os.link(p, t / "corpus" / "knowledge" / "twin.md")
    make("att-entry-hardlink", post=post_hardlink)

    def post_fifo(t):
        p = t / "corpus" / "knowledge" / "idle-lock-never-asked-r12.md"
        p.unlink()
        os.mkfifo(p)
    make("att-entry-fifo", post=post_fifo)

    # 11. clause 2 enforcement probe: duplicate S203 row -> MISSED.
    rows_dup = HEADER + "\n".join(row_line(sid) for sid in ALL_SIDS) + \
        "\n" + row_line("S203") + "\n"
    make("att-row-duplicate", sources_md=rows_dup)

    # 12-13. clause 3 probes: literal and escaped pipe inside a cell.
    make("att-row-pipe",
         teaches_over={"S203": "teaches with a literal | pipe"})
    make("att-row-escpipe",
         teaches_over={"S203": r"teaches with an escaped \| pipe"})

    # 14. clause 4 probe: extra used-by token -> MISSED.
    make("att-usedby-extra",
         used_by_over={"S203": "corpus/knowledge/idle-lock-never-asked-r12.md"
                       ", corpus/knowledge/idle-lock-offered-in-the-bar-r15.md"})

    # 15. clause 4 edge: duplicated token collapses in set -> MET (clause
    #     'token set' still satisfied; documents set semantics).
    make("att-usedby-dup",
         used_by_over={"S203": "corpus/knowledge/idle-lock-never-asked-r12.md"
                       ", corpus/knowledge/idle-lock-never-asked-r12.md"})

    # 16. clause 5 probe: status 'Mined' -> MISSED.
    make("att-status-case", status_over={"S203": "Mined"})

    # 17. clause 6 probe: recheck failing all three forms -> MISSED.
    make("att-recheck-symbolic-bad", recheck_over={"S203": "TBD?"})

    # 18. clause 8 probe: quote not in receipt -> MISSED.
    def mut_absent(rel, ids, text):
        if rel != "corpus/knowledge/idle-lock-never-asked-r12.md":
            return text
        return text.replace(
            f"gate-quote: S203 {QUOTES['S203']}",
            "gate-quote: S203 this text does not occur in the receipt")
    make("att-quote-absent", entry_mut=mut_absent)

    # 19. clause 9 probe: 26-word contiguous receipt substring -> MISSED.
    def mut_26(rel, ids, text):
        if rel != "corpus/knowledge/idle-lock-never-asked-r12.md":
            return text
        return text.replace(
            f"gate-quote: S203 {QUOTES['S203']}",
            f"gate-quote: S203 {first_26_words_substr('S203')}")
    make("att-quote-26", entry_mut=mut_26)

    # 20. clause 9 probe: empty quote -> MISSED.
    def mut_empty(rel, ids, text):
        if rel != "corpus/knowledge/idle-lock-never-asked-r12.md":
            return text
        return text.replace(
            f"gate-quote: S203 {QUOTES['S203']}", "gate-quote: S203 ")
    make("att-quote-empty", entry_mut=mut_empty)

    print("built", len(list(OUT.iterdir())), "trees under", OUT)


if __name__ == "__main__":
    main()
