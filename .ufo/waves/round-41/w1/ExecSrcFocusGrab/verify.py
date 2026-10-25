#!/usr/bin/env python3
"""Verify every quote in facts.md against the staged receipts.

For each table row `fact | quote | file:line | sha256`:
  * sha256 of the file equals the row's hash and the pinned expected hash;
  * the quote occurs on exactly that line (whitespace-normalised);
  * the quote is <= 25 words;
  * additionally report whether the quote also survives the C2 counter's
    normalisation (`norm()`: strip script/style, strip tags, unescape, collapse
    whitespace) and is 3-25 words - i.e. usable verbatim as a `## Gate` quote.

Exit 0 iff every row verifies. Prints one line per row: verdict, file:line,
word count, gate-readiness, sha256 prefix.
"""
import hashlib
import html
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FETCH = HERE.parents[1] / "fetch"
FACTS = HERE / "facts.md"

EXPECTED = {
    "focus-grab-v1.xml":
        "0bc60c14d27f9079e0d1d9d706f91e67ad7da585f3b7f34ff7186a376c0285b4",
    "Hyprland-FocusGrab.cpp":
        "53b762f7149bf1c3105ec1da2137d02cc7bece90043d9a2ce253a784b092aff1",
    "Hyprland-FocusGrab.hpp":
        "dce47251853f8d95eeec0eb357665efdceccd52b111e633c56412e5c55103421",
}

ROW = re.compile(r"^(?P<file>[A-Za-z0-9_.-]+):(?P<line>\d+)$")


def norm(text):
    text = re.sub(r"<script.*?</script>|<style.*?</style>", " ", text,
                  flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", "", text)
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


def ws(text):
    return re.sub(r"\s+", " ", text).strip()


def structural_checks(raw):
    """Shape assertions the facts table's summary depends on."""
    fails = 0
    xml = raw["focus-grab-v1.xml"]
    ifaces = re.findall(r'<interface name="([^"]+)" version="(\d+)"', xml)
    if ifaces != [("hyprland_focus_grab_manager_v1", "1"),
                  ("hyprland_focus_grab_v1", "1")]:
        print(f"FAIL xml interfaces {ifaces}")
        fails += 1
    else:
        print(f"OK   xml interfaces={[n for n, _ in ifaces]} versions="
              f"{[v for _, v in ifaces]}")
    reqs = re.findall(r'<request name="([^"]+)"', xml)
    if reqs != ["create_grab", "destroy", "add_surface", "remove_surface",
                "commit", "destroy"]:
        print(f"FAIL xml requests {reqs}")
        fails += 1
    else:
        print(f"OK   xml requests={reqs}")
    evs = re.findall(r'<event name="([^"]+)"', xml)
    if evs != ["cleared"]:
        print(f"FAIL xml events {evs}")
        fails += 1
    else:
        print(f"OK   xml events={evs}")
    for name in ("Hyprland-FocusGrab.cpp", "Hyprland-FocusGrab.hpp"):
        n = raw[name].count("touch")
        if n != 0:
            print(f"FAIL {name} mentions 'touch' {n}x")
            fails += 1
        else:
            print(f"OK   {name} mentions 'touch' 0x")
    for token in ("<enum", "error", "since="):
        n = xml.count(token)
        if n != 0:
            print(f"FAIL xml mentions {token!r} {n}x")
            fails += 1
        else:
            print(f"OK   xml mentions {token!r} 0x")
    return fails


def main():
    raw = {}
    hashes = {}
    for name, want in EXPECTED.items():
        path = FETCH / name
        if not path.is_file():
            print(f"FAIL missing receipt {path}")
            return 1
        data = path.read_bytes()
        got = hashlib.sha256(data).hexdigest()
        hashes[name] = got
        raw[name] = data.decode("utf-8", "replace")
        if got != want:
            print(f"FAIL sha256 {name}: got {got} want {want}")
            return 1
        print(f"receipt {name} sha256={got} bytes={len(data)}")

    rows = []
    for lineno, line in enumerate(FACTS.read_text(encoding="utf-8").splitlines(), 1):
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != 4:
            continue
        m = ROW.match(cells[2])
        if not m or not cells[1].startswith("`") or not cells[1].endswith("`"):
            continue
        rows.append((lineno, cells[0], cells[1][1:-1], m["file"], int(m["line"]),
                     cells[3].strip("`")))

    if not rows:
        print("FAIL no table rows parsed")
        return 1

    bad = structural_checks(raw)
    gate_ready = []
    for facts_line, fact, quote, name, target, row_hash in rows:
        if name not in EXPECTED:
            print(f"FAIL facts.md:{facts_line} unknown file {name}")
            bad += 1
            continue
        if row_hash != hashes[name]:
            print(f"FAIL facts.md:{facts_line} row sha256 {row_hash} != file sha256")
            bad += 1
            continue
        lines = raw[name].splitlines()
        if not 1 <= target <= len(lines):
            print(f"FAIL {name}:{target} out of range (file has {len(lines)} lines)")
            bad += 1
            continue
        actual = ws(lines[target - 1])
        q = ws(quote)
        words = len(q.split())
        on_line = q in actual
        in_norm = q in norm(raw[name])
        gate = in_norm and 3 <= words <= 25
        if not on_line:
            print(f"FAIL {name}:{target} quote not on that line: {q!r}")
            bad += 1
            continue
        if words > 25:
            print(f"FAIL {name}:{target} quote has {words} words (>25)")
            bad += 1
            continue
        print(f"OK   {name}:{target} words={words:<2} gate={'yes' if gate else 'no ':3} "
              f"norm={'yes' if in_norm else 'no '} sha={hashes[name][:12]} :: {q[:70]}")
        if gate:
            gate_ready.append((name, target, words, q))

    print()
    print(f"checked={len(rows)} failed={bad} gate_ready={len(gate_ready)}")
    print("gate-ready quotes (3-25 words, present in the counter's normalised text):")
    for name, target, words, q in gate_ready:
        print(f"  {name}:{target} words={words} :: {q}")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
