#!/usr/bin/env python3
"""RerunC2Data independent recomputation of the C2 Gate bindings.

Written from scratch by seat RerunC2Data: it does NOT import, exec or copy any
function of quality/counters/c2-r43-gkeep-entry-v2.py (that counter was read
only to learn which obligations the receipt claims). It re-derives, for every
`GATE <id>` line of corpus/lessons/round-43.md `## Gate` at a revision:

  * that the id has exactly one GATE line, inside the section;
  * the sha256 of the pinned receipt blob at that revision (and its git mode);
  * the number of word-bounded occurrences of the Gate quote in the receipt's
    whitespace-collapsed text;
  * the 1-based line of the receipt on which the first word-bounded occurrence
    starts;
  * whether every unfenced entry line (other than a `source:` line) that names
    the id carries the quote and the `<receipt basename>:<line>` locator, and
    the raw 1-based line numbers of those entry lines;
  * that no other cited receipt holds the same quote word-bounded.

Usage: indep_gate_check.py <repo> <rev> [<entry path>] [<lesson path>]
Exit 0 when every cited id agrees, 1 on any disagreement, 2 on a setup error.
"""
import hashlib
import re
import subprocess
import sys

ENTRY = "corpus/knowledge/hyprland-gkeep-geometry-r43.md"
LESSON = "corpus/lessons/round-43.md"
GATE_RE = re.compile(r'^GATE (S\d+) receipt=(\S+) sha256=([0-9a-f]{64}) quote="(.*)"$')


def git(repo, *args):
    p = subprocess.run(["git", "-C", repo] + list(args), capture_output=True)
    if p.returncode != 0:
        return None
    return p.stdout


def section(text, heading):
    out, on = [], False
    for line in text.splitlines():
        if line.startswith("## "):
            if on:
                break
            on = line.strip() == heading
            continue
        if on:
            out.append(line)
    return out


def unfence_numbered(text):
    """(line number, line) of every line outside fenced code blocks."""
    out, fenced = [], False
    for n, line in enumerate(text.splitlines(), 1):
        if re.match(r"^ {0,3}(```|~~~)", line):
            fenced = not fenced
            continue
        if not fenced:
            out.append((n, line))
    return out


def isw(ch):
    return ch.isalnum() or ch == "_"


def collapse(text):
    """Whitespace-collapsed text plus the 1-based source line per character."""
    chars, where, prev_space = [], [], True
    for ln, line in enumerate(text.split("\n"), 1):
        for ch in line:
            if ch.isspace():
                if not prev_space:
                    chars.append(" ")
                    where.append(ln)
                    prev_space = True
            else:
                chars.append(ch)
                where.append(ln)
                prev_space = False
        if not prev_space:  # the line break is itself whitespace
            chars.append(" ")
            where.append(ln)
            prev_space = True
    while chars and chars[-1] == " ":
        chars.pop()
        where.pop()
    return "".join(chars), where


def hits(collapsed, quote):
    """Offsets of every word-bounded occurrence of quote in collapsed."""
    out, i = [], 0
    while True:
        k = collapsed.find(quote, i)
        if k < 0:
            return out
        before = collapsed[k - 1] if k else " "
        after = collapsed[k + len(quote)] if k + len(quote) < len(collapsed) else " "
        if not (isw(quote[0]) and isw(before)) and \
                not (isw(quote[-1]) and isw(after)):
            out.append(k)
        i = k + 1


def main():
    if len(sys.argv) < 3:
        print("usage: indep_gate_check.py <repo> <rev> [entry] [lesson]")
        return 2
    repo, rev = sys.argv[1], sys.argv[2]
    entry_path = sys.argv[3] if len(sys.argv) > 3 else ENTRY
    lesson_path = sys.argv[4] if len(sys.argv) > 4 else LESSON

    lesson_blob = git(repo, "show", "%s:%s" % (rev, lesson_path))
    entry_blob = git(repo, "show", "%s:%s" % (rev, entry_path))
    if lesson_blob is None or entry_blob is None:
        print("SETUP missing %s or %s at %s" % (lesson_path, entry_path, rev))
        return 2

    lesson_text = lesson_blob.decode("utf-8", "replace")
    gate_section = section(lesson_text, "## Gate")
    gates, counts, bad = {}, {}, 0
    for line in gate_section:
        if not line.startswith("GATE S"):
            continue
        m = GATE_RE.match(line)
        if not m:
            print("PARSE-FAIL %s" % line[:100])
            bad += 1
            continue
        gates[m.group(1)] = (m.group(2), m.group(3), m.group(4))
        counts[m.group(1)] = counts.get(m.group(1), 0) + 1
    total = sum(1 for l in lesson_text.splitlines() if l.startswith("GATE S"))
    inside = sum(1 for l in gate_section if l.startswith("GATE S"))

    entry_lines = unfence_numbered(entry_blob.decode("utf-8", "replace"))
    print("rev=%s entry=%s lesson=%s gate_ids=%d gate_lines=%d/%d(in section/whole)" % (
        rev, entry_path, lesson_path, len(gates), inside, total))
    if inside != total:
        print("DISAGREE %d GATE line(s) outside ## Gate" % (total - inside))
        bad += 1
    for sid, n in counts.items():
        if n != 1:
            print("DISAGREE %s has %d GATE lines" % (sid, n))
            bad += 1

    for sid in sorted(gates, key=lambda s: int(s[1:])):
        path, declared, quote = gates[sid]
        blob = git(repo, "show", "%s:%s" % (rev, path))
        tree = git(repo, "ls-tree", rev, "--", path)
        if blob is None or not tree:
            print("%s DISAGREE missing receipt=%s at rev" % (sid, path))
            bad += 1
            continue
        mode = tree.split()[0].decode()
        digest = hashlib.sha256(blob).hexdigest()
        q = re.sub(r"\s+", " ", quote).strip()
        collapsed, where = collapse(blob.decode("utf-8", "replace"))
        at = hits(collapsed, q)
        start_line = where[at[0]] if at else 0
        base = path.rsplit("/", 1)[-1]
        locator = "%s:%d" % (base, start_line)
        carriers = [(n, l) for n, l in entry_lines
                    if re.search(r"\b%s\b" % re.escape(sid), l)
                    and not l.startswith("source:")]
        miss_q = [n for n, l in carriers if q not in l]
        miss_loc = [n for n, l in carriers
                    if not re.search(re.escape(locator) + r"(?!\d)", l)]
        ok = (mode == "100644" and digest == declared and len(at) == 1
              and carriers and not miss_q and not miss_loc)
        print("%s sha256=%s mode=%s bytes=%d occ=%d line=%d locator=%s "
              "entry_lines=%s miss_quote=%s miss_locator=%s %s" % (
                  sid, digest, mode, len(blob), len(at), start_line, locator,
                  ",".join(str(n) for n, _ in carriers) or "-",
                  miss_q or "-", miss_loc or "-", "OK" if ok else "DISAGREE"))
        if digest != declared:
            print("  DISAGREE sha256 %s: declared %s" % (sid, declared))
        if len(at) != 1:
            print("  DISAGREE word-bounded occurrences=%d for %s" % (len(at), sid))
        if not carriers:
            print("  DISAGREE no unfenced entry line names %s" % sid)
        if not ok:
            bad += 1

    for sid in sorted(gates, key=lambda s: int(s[1:])):
        q = re.sub(r"\s+", " ", gates[sid][2]).strip()
        for other in gates:
            if other == sid:
                continue
            ob = git(repo, "show", "%s:%s" % (rev, gates[other][0]))
            if ob is None:
                continue
            if hits(collapse(ob.decode("utf-8", "replace"))[0], q):
                print("DISAGREE shared quote: %s also word-bounded in %s"
                      % (sid, other))
                bad += 1

    print("INDEP VERDICT: %s (disagreements=%d)" % (
        "AGREE" if bad == 0 else "DISAGREE", bad))
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
