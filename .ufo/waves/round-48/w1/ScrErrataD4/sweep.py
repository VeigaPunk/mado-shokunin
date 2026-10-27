#!/usr/bin/env python3
"""Round-48 w1 seat ScrErrataD4 - D4 locator sweep.

Recomputes, from the pinned bytes, every `terminal-route-r17.md:N[-M]` locator that appears in
  - corpus/knowledge/xdg-terminal-selection-r47.md   (the round-47 entry)
  - corpus/lessons/round-47-verifier-spotcheck.md    (the round-47 verifier lesson)
and reports MATCH / MISMATCH against the sentence the citing line claims, plus one
DEFECT-MENTION (the lesson line that *quotes* the entry's wrong locator in order to route it).

No line number in the output is typed: locators are parsed out of the citing files by regex over
real `grep -n` output, and every source range (bullet, [UNK] sentence start, sentence end) is
computed by scanning the source file.  Only the *claim keys* (short phrases that occur verbatim in
the citing lines), the *anchor strings* (verbatim phrases of the source, must resolve to exactly
one line) and the quotes used by the draft erratum are typed; each is re-resolved before use, and a
typed phrase that no longer exists aborts the run.

Usage: sweep.py <lane-root> <out-receipt>
"""
import re
import subprocess
import sys
from pathlib import Path

SRC = "corpus/knowledge/terminal-route-r17.md"
ENTRY = "corpus/knowledge/xdg-terminal-selection-r47.md"
LESSON = "corpus/lessons/round-47-verifier-spotcheck.md"
REG = ".ufo/waves/round-47/registration.md"

# claim key (verbatim in the citing line) -> (anchor phrase in the source, related sentence anchor).
# Both anchors must be unique in the source.  The primary anchor is the sentence the citing line's
# claim names - for "launch half" that is the "at launch; no launcher ran" clause of r17:144-145, the
# range round-47 registration.md:16-19 itself calls the round-17 [UNK] and splits into selection/launch
# halves.  The related anchor is the neighbouring [UNK] that asks the process-start question in its own
# words (r17:128-130); it is recorded, never scored, so the label question stays visible without
# turning a consistent locator into a defect.
CLAIMS = [
    ("selection half", "whether the resolver actually picks", None),
    ("launch half", "that entry over the system one at launch; no launcher ran",
     "Whether a terminal process actually started"),
    ("helper", "value from `omarchy-cmd-terminal-cwd` is valid", None),
    ("Ground: at base", "whether the resolver actually picks", None),
    ("base ground", "whether the resolver actually picks", None),
    ("on ground held", "whether the resolver actually picks", None),
]

# the lesson line that routes this defect quotes the wrong locator on purpose; it is not a citation
DEFECT_MENTION_KEY = "4. D4:"

# quotes the draft erratum uses: (file, start, end, verbatim span, used-in-erratum.md)
# `used=True` spans are additionally checked by verify.py to appear in erratum.md, so the draft can
# only quote text that the receipt has already verified against the pinned bytes.
QUOTES = [
    (SRC, 144, 145, "[UNK] whether the resolver actually picks that entry over the system one at launch; no launcher ran.", False),
    (SRC, 144, 145, "that entry over the system one at launch; no launcher ran", True),
    (SRC, 128, 130, "Whether a terminal process actually started from that selection", True),
    (SRC, 128, 130, "no launcher ran in this round", True),
    (SRC, 149, 150, "[UNK] Whether the `--dir=` value from `omarchy-cmd-terminal-cwd` is valid at launch time. The helper is not run.", False),
    (SRC, 149, 150, "[UNK] Whether the `--dir=` value from `omarchy-cmd-terminal-cwd` is valid at launch time.", True),
    (SRC, 149, 150, "The helper is not run.", True),
    (ENTRY, 76, 76, "The selection half of the round-17 `[UNK]`", False),
    (ENTRY, 76, 76, "corpus/knowledge/terminal-route-r17.md:144-145", False),
    (ENTRY, 88, 88, "not that a terminal process starts from it under the hotkey", False),
    (ENTRY, 88, 88, "terminal-route-r17.md:144-145 launch half", False),
    (ENTRY, 95, 95, "Whether the `--dir=` value from `omarchy-cmd-terminal-cwd` resolves at launch time stays `[UNK]`", False),
    (ENTRY, 95, 95, "terminal-route-r17.md:150-151, helper not run", False),
    (ENTRY, 95, 95, "resolves at launch time stays `[UNK]`", True),
    (LESSON, 139, 140, "Limits cites `terminal-route-r17.md:150-151` for the helper `[UNK]`", False),
    (LESSON, 139, 140, "sits at `:149-150`", True),
    (REG, 16, 19, 'launch half ("at launch") stays `[UNK]`', True),
]

LOC_RE = re.compile(r"terminal-route-r17\.md:(\d+)(?:-(\d+))?")
RANGE_RE = re.compile(r":(\d+)-(\d+)")


def load(root, rel):
    return (root / rel).read_text(encoding="utf-8", errors="replace").splitlines()


def norm(root, rel, a, b):
    lines = load(root, rel)[a - 1:b]
    return re.sub(r"\s+", " ", " ".join(x.strip() for x in lines)).strip()


def grep_n(root, rel, pattern, fixed=True):
    p = subprocess.run(["grep", "-nF" if fixed else "-nE", "-e", pattern, rel],
                       cwd=root, capture_output=True, text=True)
    out = []
    for line in p.stdout.splitlines():
        n, _, text = line.partition(":")
        out.append((int(n), text))
    return out


def bullets(lines):
    """Ranges (1-based, inclusive) of '- ' bullets; a blank line or the next bullet ends one."""
    out = []
    starts = [i for i, t in enumerate(lines) if t.startswith("- ")]
    for s in starts:
        end = len(lines) - 1
        for i in range(s + 1, len(lines)):
            if lines[i].strip() == "" or lines[i].startswith("- "):
                end = i - 1
                break
        while end > s and lines[end].strip() == "":
            end -= 1
        out.append((s + 1, end + 1))
    return out


def main():
    root = Path(sys.argv[1]).resolve()
    out = Path(sys.argv[2]).resolve()
    src = load(root, SRC)
    bs = bullets(src)

    def bullet_of(n):
        for a, b in bs:
            if a <= n <= b:
                return (a, b)
        return None

    def resolve_anchor(anchor):
        hits = grep_n(root, SRC, anchor)
        if len(hits) != 1:
            sys.exit(f"anchor {anchor!r} resolves to {len(hits)} lines, need exactly 1")
        return hits[0][0]

    rec = []
    w = rec.append

    w("D4 sweep - every terminal-route-r17.md locator in the round-47 entry and lesson")
    w("method: locators parsed from grep -n output of the citing files; source ranges computed")
    w("sources (sha256, lines):")
    for rel in (SRC, ENTRY, LESSON):
        h = subprocess.run(["sha256sum", rel], cwd=root, capture_output=True, text=True).stdout.split()[0]
        w(f"  {h}  {rel}  lines={len(load(root, rel))}")
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, capture_output=True, text=True).stdout.strip()
    w(f"lane HEAD at sweep: {head}")
    w("")

    findings = []
    for rel in (ENTRY, LESSON):
        w(f"=== locators in {rel} ===")
        w("$ grep -nE 'terminal-route-r17\\.md:[0-9]+(-[0-9]+)?' " + rel)
        hits = grep_n(root, rel, r"terminal-route-r17\.md:[0-9]+(-[0-9]+)?", fixed=False)
        for n, text in hits:
            w(f"{n}: {text.strip()[:200]}")
        w("")

        for n, text in hits:
            for m in LOC_RE.finditer(text):
                a = int(m.group(1))
                b = int(m.group(2)) if m.group(2) else a
                if DEFECT_MENTION_KEY in text:
                    # the line quotes the wrong locator in order to route it; its own assertion is a
                    # bare `:N-M` range, usually on the following line.  Strip every full
                    # terminal-route-r17.md locator from the paragraph, then read the bare ranges.
                    para = norm(root, rel, n, min(n + 3, len(load(root, rel))))
                    bare = RANGE_RE.findall(LOC_RE.sub("", para))
                    if not bare:
                        sys.exit(f"no bare correction range in the {rel}:{n} paragraph")
                    sa, sb = (int(bare[-1][0]), int(bare[-1][1]))
                    blk = norm(root, SRC, sa, sb)
                    ok = "omarchy-cmd-terminal-cwd" in blk
                    w(f"DEFECT-MENTION file={rel} citing_line={n} quoted_locator={a}-{b} "
                      f"asserted_range={sa}-{sb} asserted_range_has_helper_anchor={ok} verdict={'CONFIRMED' if ok else 'WRONG'}")
                    w(f"EXCERPT quoted={a}-{b} begin")
                    for k in range(a, b + 1):
                        w(f"{k}| {src[k - 1]}")
                    w("EXCERPT end")
                    w("")
                    findings.append(("DEFECT-MENTION", rel, n, a, b, (sa, sb), None, None))
                    continue
                claim = anchor_phrase = related_phrase = None
                for key, anch, relanch in CLAIMS:
                    if key in text:
                        claim, anchor_phrase, related_phrase = key, anch, relanch
                        break
                if claim is None:
                    w(f"UNCLASSIFIED citing={rel}:{n} cited={a}-{b}")
                    findings.append(("UNCLASSIFIED", rel, n, a, b, None, None, None))
                    continue
                anchor_line = resolve_anchor(anchor_phrase)
                bl = bullet_of(anchor_line)
                start = anchor_line
                for k in range(anchor_line, bl[0] - 1, -1):
                    if "[UNK]" in src[k - 1]:
                        start = k
                        break
                end = bl[1]
                for k in range(start, bl[1] + 1):
                    s = src[k - 1].strip()
                    if s.endswith(".") or s.endswith(";") or s.endswith(":"):
                        end = k
                        break
                verdict = "MATCH" if (a == start and b <= end and b >= anchor_line) else "MISMATCH"
                w(f"CITING file={rel} citing_line={n} cited={a}-{b} claim={claim!r} "
                  f"anchor_line={anchor_line} sentence_start={start} bullet={bl[0]}-{bl[1]} "
                  f"corrected={start}-{end} verdict={verdict}")
                if related_phrase:
                    rl = resolve_anchor(related_phrase)
                    rb = bullet_of(rl)
                    rs = rl
                    for k in range(rl, rb[0] - 1, -1):
                        if "[UNK]" in src[k - 1]:
                            rs = k
                            break
                    w(f"RELATED file={rel} citing_line={n} anchor_line={rl} sentence={rs}-{rb[1]} "
                      f"also_cited={'yes' if (a <= rl <= b) else 'no'}")
                w(f"EXCERPT cited={a}-{b} begin")
                for k in range(a, b + 1):
                    w(f"{k}| {src[k - 1]}")
                w("EXCERPT end")
                w(f"EXCERPT corrected={start}-{end} begin")
                for k in range(start, end + 1):
                    w(f"{k}| {src[k - 1]}")
                w("EXCERPT end")
                w("")
                findings.append((verdict, rel, n, a, b, (start, end), anchor_phrase, anchor_line))

    w("=== quotes used by the draft erratum (verbatim span inside the cited line range) ===")
    for rel, a, b, span, used in QUOTES:
        blk = norm(root, rel, a, b)
        words = len(span.split())
        inside = span in blk
        w(f'QUOTE src={rel}:{a}-{b} words={words} inside={str(inside).lower()} used={str(used).lower()} quote="{span}"')
        if not inside:
            sys.exit(f"quote not verbatim in {rel}:{a}-{b}: {span!r}")
        if words > 25:
            sys.exit(f"quote over 25 words ({words}): {span!r}")
    w("")

    cites = [f for f in findings if f[0] in ("MATCH", "MISMATCH")]
    mism = [f for f in cites if f[0] == "MISMATCH"]
    mentions = [f for f in findings if f[0] == "DEFECT-MENTION"]
    w(f"TOTAL citing_locators={len(cites)} match={len(cites) - len(mism)} mismatch={len(mism)} "
      f"defect_mentions={len(mentions)}")
    for f in mism:
        w(f"WRONG citing={f[1]}:{f[2]} cited={f[3]}-{f[4]} corrected={f[5][0]}-{f[5][1]}")
    for f in mentions:
        w(f"MENTION file={f[1]}:{f[2]} quoted={f[3]}-{f[4]} asserted={f[5][0]}-{f[5][1]}")
    w("")
    out.write_text("\n".join(rec) + "\n", encoding="utf-8")
    print("\n".join(rec[-9:]))


if __name__ == "__main__":
    main()
