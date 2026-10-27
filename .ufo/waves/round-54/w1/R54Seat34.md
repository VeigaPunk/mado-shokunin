# R54Seat34 — C1 source pins: exact-byte review (scribe seat, leaf member)

Round: 54 (mado, hyaku run 10), wave `w1`. Lane root: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Base / scored revision: `e25149fec8152a3aabd2b18a0ee8663b23cf65aa` (`git rev-parse HEAD` in the lane = same).
Governing documents: `.ufo/waves/round-54/registration.md`, `.ufo/waves/round-54/claims-frozen.md`.

## Behavior

Read-only byte review of the four round-52 C1 pins and of the P19–P22 anchor coordinates frozen in
`registration.md:27-33` / `:35-40`. No tree, pin, counter or entry was edited. Nothing was fetched:
all evidence is local committed bytes plus read-only `git cat-file` reads of `e25149fe`.

**Attacked predicate** — C1 clause (a) "each … Quote cell occurring verbatim and contiguous in the
round-52 pin named by its Pin:anchor cell" (`claims-frozen.md:23-27`), clause (b) the four anchor
side-claims (`registration.md:35-40`), clause (c) "each of the four pins' bytes hash to the round-52
recorded sha256" (`claims-frozen.md:29-30`), judged by the normalizer rule of
`registration.md:50-53` ("exact byte contiguity after single-space normalization of interior newlines
ONLY where the frozen quote itself carries a newline (P19/P21/P22 are single logical lines)").

## Commands actually run

```
cd /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-52/fetch
sha256sum Hyprland-ConfigActions.cpp Hyprland-ConfigActions.hpp \
          Hyprland-KeybindManager.cpp Hyprland-legacy-DispatcherTranslator.cpp README.txt
# a83abeb57175e65908d8d67ddc9802310134e5a4752fa3764f980401b48a7637  Hyprland-ConfigActions.cpp
# 746c6f517620eb039afbfbb9a4a0e2d5ba1c5eb117bcc8f396173f63091b7073  Hyprland-ConfigActions.hpp
# 8d8f35fc84c4a2f8de63ac2bf6f6531c651c6fa6d37b1aac7c8fc5d9342d4e40  Hyprland-KeybindManager.cpp
# 7248cbb89f898c783c50c89d068df9821a6b38aeb6abeb6064e92c1610fbe771  Hyprland-legacy-DispatcherTranslator.cpp
# c53296aeafcdd746ececcb183bcffaf76467a9917db46ae5dc5591bcde674ad0  README.txt

cd /home/vgpnk/Projects/shokunin/mado-shokunin
git rev-parse HEAD                                   # e25149fec8152a3aabd2b18a0ee8663b23cf65aa
git cat-file -p e25149fe:.ufo/waves/round-52/fetch/SHA256SUMS | cat -A   # 5 lines, absolute paths
git status --porcelain -- .ufo/waves/round-52/fetch \
    corpus/knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md       # empty, rc=0

python3 -I /fast/scratch/hyaku/mado-r54/R54Seat34/reproduce.py           # appendix A
```

Output of the consolidate script (verbatim, `python 3.14.8`):

```
HASH Hyprland-ConfigActions.cpp match=True worktree_eq_gitobj=True
HASH Hyprland-ConfigActions.hpp match=True worktree_eq_gitobj=True
HASH Hyprland-KeybindManager.cpp match=True worktree_eq_gitobj=True
HASH Hyprland-legacy-DispatcherTranslator.cpp match=True worktree_eq_gitobj=True
SUMS file exists: True | .txt exists: False | abs_paths: True
P19 pin=Hyprland-ConfigActions.cpp 1554-1558 raw_substr=False q_has_newline=False v3=False v4=True shrink_lo=False shrink_hi=False blanks=[1555] uniq_in_collapsed_doc=1
P20 pin=Hyprland-ConfigActions.cpp 1576-1576 raw_substr=True q_has_newline=False v3=True v4=True blanks=[] uniq_in_collapsed_doc=1
P21 pin=Hyprland-legacy-DispatcherTranslator.cpp 619-622 raw_substr=False q_has_newline=False v3=False v4=True shrink_lo=False shrink_hi=False blanks=[620] uniq_in_collapsed_doc=1
P22 pin=Hyprland-legacy-DispatcherTranslator.cpp 573-574 raw_substr=False q_has_newline=False v3=True v4=True shrink_lo=False shrink_hi=False blanks=[] uniq_in_collapsed_doc=1
sendKeyboardMods lines: [1485, 1554, 1576]
P20 quote count in ConfigActions: 1
P19 quote in Hyprland-ConfigActions.hpp: raw=0
P19 quote in Hyprland-KeybindManager.cpp: raw=0
P19 quote in Hyprland-legacy-DispatcherTranslator.cpp: raw=0
ROW P19 cols=7 pin=Hyprland-ConfigActions.cpp anchor=1554-1558 quote_eq_frozen=True words=16 bytes=182
ROW P20 cols=7 pin=Hyprland-ConfigActions.cpp anchor=1576-1576 quote_eq_frozen=True words=4 bytes=45
ROW P21 cols=7 pin=Hyprland-legacy-DispatcherTranslator.cpp anchor=619-622 quote_eq_frozen=True words=13 bytes=115
ROW P22 cols=7 pin=Hyprland-legacy-DispatcherTranslator.cpp anchor=573-574 quote_eq_frozen=True words=12 bytes=80
```

(`v3` = per-line indent strip, blank line kept as `""`, one-space join. `v4` = per-line indent strip,
blank lines dropped, one-space join. `raw_substr` = literal byte substring of the quote in the pin.)

## Findings

### F1 — pins: 4/4 hashes match, worktree == git object at base (no discrepancy)

All four recorded sha256 in `registration.md:14-19` equal the actual bytes, and each pin's worktree
bytes are byte-identical to `git cat-file -p e25149fe:.ufo/waves/round-52/fetch/<pin>`
(`worktree_eq_gitobj=True`). The committed `SHA256SUMS` at base is also worktree-identical
(`916bf8df3c2ed43b…`). `git status --porcelain` over the pin dir and the entry is empty — the pins the
counter will read at `--rev e25149fe` are the pins this review hashed. Registry rows agree:
`corpus/SOURCES.md:320` (S370, `7248cbb8…`) and `:321` (S371, `a83abeb5…`).

### F2 — anchor line numbers: 4/4 correct, each span minimal and unique (no discrepancy)

| prop | pin | anchor | minimal? | unique in collapsed doc |
|---|---|---|---|---|
| P19 | `Hyprland-ConfigActions.cpp` | 1554–1558 | `1555-1558` ✗, `1554-1557` ✗ | 1 |
| P20 | `Hyprland-ConfigActions.cpp` | 1576 | single line | 1 |
| P21 | `Hyprland-legacy-DispatcherTranslator.cpp` | 619–622 | `620-622` ✗, `619-621` ✗ | 1 |
| P22 | `Hyprland-legacy-DispatcherTranslator.cpp` | 573–574 | `574` ✗, `573` ✗ | 1 |

Side-claims hold on the bytes: `591 ≤ 619` (591 is `static SDispatchResult sendkeystate(`), `622 ≤ 627`
(627 is the closing `}` of `sendkeystate`), `573 > 571` (571 is the `}` closing the `for (xkb_keycode_t
kc = keycode_min; …)` scan opened at 565), P22 sits inside `sendshortcut` (opens 531, closes 589) and
P21 inside `sendkeystate` — matching the entry's Support cells (entry lines 19–20). Both P19/P20 sites
sit inside `ActionResult Actions::pass(uint32_t modMask, uint32_t key, std::optional<PHLWINDOW> w)` at
1530, inside S371's declared window `ConfigActions.cpp:1530-1616`; P21/P22 sit inside S370's declared
window `DispatcherTranslator.cpp:531-627`. No off-by-one drift in any coordinate.

Discrimination check: `sendKeyboardMods` occurs three times (1485, 1554, 1576) but
`sendKeyboardMods(0, 0, 0, 0);` occurs exactly once, at 1576 — so the frozen `:1576` anchor is
discriminating for P20, and `C1-CTL-2` (1576→1575) lands on a blank line, which cannot satisfy the
quote. `C1-CTL-6`'s required verdict is reachable: the P19 quote is absent (`raw=0`) from `.hpp`,
`KeybindManager.cpp` and `DispatcherTranslator.cpp`.

### F3 — HIGH, freeze/operability: the "verbatim contiguous" rule cannot admit P19/P21/P22 as written

`registration.md:50-53` permits normalization "ONLY where the frozen quote itself carries a newline";
it states P19/P21/P22 are single logical lines. None of the four frozen quotes contains `\n`
(`q_has_newline=False` for all four). Yet the four quotes do **not** occur as literal byte substrings
in their pins:

- P19: `raw_substr=False`, and the span needs *both* per-line indent stripping *and* removal of the
  blank line 1555. A newline→space join that keeps the blank line yields a double space:
  `…0, 0, 0);  if (S.m_passPressed == 1) {` (`v3=False`), one byte off the frozen quote at the seam
  (P19 quote bytes 182).
- P21: `raw_substr=False`, same blank-line-620 seam (`v3=False`).
- P22: `raw_substr=False` (`v3=True`, no blank line — it needs indent stripping only).
- P20: the only quote that is a literal substring (`raw_substr=True`).

Consequence for the frozen predicate: a counter implementing the judged rule literally (and a fortiori
one implementing plain byte contiguity) prints `quotes=1/4` → `verdict=TARGET_MISSED`. Only a
normalizer that strips each line's indentation **and drops blank lines** reaches `quotes=4/4`. The
frozen text does not name that policy, and `C1-CTL-1` ("not contiguous → quotes≤3/4", `registration.md:42`)
rests on the same unstated policy — so the green/red split of the whole C1 control set is currently
normalizer-defined, not contract-defined. This is a pre-data freeze gap: it must be resolved by the
canonical planner (new versioned registration or an explicit normalizer ruling), never by a seat
editing `registration.md`/`claims-frozen.md` after scoring. **Recommendation (for the planner, not
acted on here):** freeze the comparator as "join the anchor span's lines after stripping each line's
leading/trailing whitespace and discarding empty lines with one U+0020, then require exact equality
of the resulting byte string" — the `v4` column above is exactly that semantics and yields 4/4.

### F4 — MEDIUM, artifact naming: the C1 sums file is `SHA256SUMS`, not `SHA256SUMS.txt`

`registration.md:12` says the C1 hashes come "from its committed `SHA256SUMS.txt`".
`.ufo/waves/round-52/fetch/` contains `SHA256SUMS` (814 bytes, 5 rows, no `.txt`);
`SHA256SUMS.txt` does not exist there (`SUMS file exists: True | .txt exists: False`). By contrast
`.ufo/waves/round-54/fetch/` really does contain `SHA256SUMS.txt`, so the two inventories disagree on
the filename and a counter/control harness that opens the literal path fails on C1 while succeeding on
C2. `claims-frozen.md:81` writes the C1 input only as "`(+SHA256SUMS)`", which is the correct name.

Secondary provenance smell in the same file: all five rows carry absolute host paths
(`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-52/fetch/…`), so the sums are tied to
this checkout path rather than to relative member names; `sha256sum -c` from the fetch dir works here
only because the path happens to resolve. It also records `README.txt`, which the frozen table does
not cover (harmless, but means "pins=4/4" cannot be derived from the sums file's row count — it is 5).

### F5 — MEDIUM, contract shape: "byte-for-byte against THIS table" is not literally satisfiable

`registration.md:22-23` says the counter extracts the entry's P19–P22 rows and checks them against the
frozen table "byte-for-byte modulo trailing spaces". The shapes differ: the frozen table has 4 columns
(`registration.md:25`: `ID | Pin file | Anchor | Quote`), the entry rows have 7
(`corpus/knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md:15`, rows 17–20:
`ID | Supersedes | Proposition | Source row | Pin:anchor | Quote (≤25 words) | Support`), and the entry
combines pin and anchor into one cell (`Hyprland-ConfigActions.cpp:1554-1558`) where the frozen table
splits them (`Hyprland-ConfigActions.cpp` + `:1554-1558`). A literal whole-row comparison can never
pass; the counter must decompose columns and compare the four cells ID/Pin/Anchor/Quote only. All four
decomposed cells currently agree with the freeze (`quote_eq_frozen=True` for P19–P22; anchors
`1554-1558`, `1576-1576`, `619-622`, `573-574`; quote word counts 16/4/13/12, all ≤25). Note the two
headers also disagree on the Quote column's qualifier ("verbatim, contiguous" vs "≤25 words").

### F6 — ADVISORY, over-admission path in the comparator (distinct input from other seats)

Tested in memory against P22 (`sendshortcut: key not found`): a comparator that compares *both* sides
with whitespace runs removed (a common shortcut for "ignore formatting") admits a semantically
different string literal — rewriting the frozen quote's `"sendshortcut: key not found"` to
`"sendshortcut:keynotfound"` compares equal under whitespace-stripping, while exact/`v4` comparison
rejects it. `C1-CTL-1`, `key - 9`, `!= 1` and a reordered-call variant are all rejected under `v4`
(`v4_span==q:False` and absent from the collapsed document), so an exact-string `v4` comparator is
both sufficient and tight; a whitespace-insensitive one is not. Not actable by this seat — recorded for
the counter's builder and its `--selftest`.

## Gates

No gate was run by this seat. `bash tools/mado-verify.sh --selftest` (harm watch,
`claims-frozen.md:86`) is main-agent territory and was not invoked; no counter exists yet
(`--selftest` of `c1-r54-*` is a builder artifact). No package query, install or update was performed
(`python3 3.14.8` was already present at the documented interpreter path); no domain, host, config,
service or compositor read occurred.

## Touched surfaces

- Written: this report only, `.ufo/waves/round-54/w1/R54Seat34.md`.
- Scratch: `/fast/scratch/hyaku/mado-r54/R54Seat34/` (three check scripts + appendix-A reproducer),
  created and removed before yield; nothing under `/tmp`.
- Reads: the four pins + `SHA256SUMS` + `README.txt` under `.ufo/waves/round-52/fetch/`, the errata
  entry, `corpus/SOURCES.md` rows S370/S371, `registration.md`, `claims-frozen.md`, and read-only
  `git cat-file`/`rev-parse`/`status` on the lane repo. No working-tree, index, ref or object write.
- No fleet-root, sibling, source-repo (`~/Projects/shokuknow`) or PATH-directory write.

## Out of scope (not done, not claimed)

- No statement about upstream bytes at `efb50993780079460b0cbed1363e2166a2de1d9f`: the pins' provenance
  beyond the local pin↔`SHA256SUMS`↔git-object chain is unverified offline (no domain reads allowed).
  `fetch/README.txt` itself says it is "not fetched bytes" — its own sha256 is recorded in the sums but
  it carries no independent anchor.
- The C2 pins (`uwsm-*`, `SHA256SUMS.txt`, `S375–S377`) were listed only to contrast filenames; their
  hashes, quotes and host joins were not reviewed here.
- No counter was built or run, no control was executed, no mutated tree was created (no git fixtures),
  and no fix was applied.
- This seat is a leaf scribe inside the producing lane: it is **not** the non-author reviewer that the
  entry's own Limits section (`…-errata-r53.md:24`) requires, and its findings do not discharge
  `M53-4` or any registration predicate.

## Appendix A — reproducer (as run; `python3 -I`, no writes)

```python
#!/usr/bin/env python3
"""R54Seat34 — reproduce every number in w1/R54Seat34.md. Read-only."""
import hashlib, os, re, subprocess, sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
FETCH = LANE + "/.ufo/waves/round-52/fetch"
ENTRY = LANE + "/corpus/knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md"
BASE = "e25149fec8152a3aabd2b18a0ee8663b23cf65aa"
REC = {
 "Hyprland-ConfigActions.cpp": "a83abeb57175e65908d8d67ddc9802310134e5a4752fa3764f980401b48a7637",
 "Hyprland-ConfigActions.hpp": "746c6f517620eb039afbfbb9a4a0e2d5ba1c5eb117bcc8f396173f63091b7073",
 "Hyprland-KeybindManager.cpp": "8d8f35fc84c4a2f8de63ac2bf6f6531c651c6fa6d37b1aac7c8fc5d9342d4e40",
 "Hyprland-legacy-DispatcherTranslator.cpp": "7248cbb89f898c783c50c89d068df9821a6b38aeb6abeb6064e92c1610fbe771",
}
PROPS = [  # id, pin, lo, hi, frozen quote
 ("P19", "Hyprland-ConfigActions.cpp", 1554, 1558,
  "g_pSeatManager->sendKeyboardMods(modMask, 0, 0, 0); if (S.m_passPressed == 1) { "
  "if (!isMouse) g_pSeatManager->sendKeyboardKey(S.m_timeLastMs, key - 8, "
  "WL_KEYBOARD_KEY_STATE_PRESSED);"),
 ("P20", "Hyprland-ConfigActions.cpp", 1576, 1576,
  "g_pSeatManager->sendKeyboardMods(0, 0, 0, 0);"),
 ("P21", "Hyprland-legacy-DispatcherTranslator.cpp", 619, 622,
  "auto result = sendshortcut(modifiedArgs); if (keyState == 2 && result.success) "
  "result = sendshortcut(modifiedArgs);"),
 ("P22", "Hyprland-legacy-DispatcherTranslator.cpp", 573, 574,
  'if (!keycode) return {.success = false, .error = "sendshortcut: key not found"};'),
]
rd = lambda n: open(f"{FETCH}/{n}", "rb").read()
lines = lambda n: rd(n).decode().split("\n")

print("PY", sys.version.split()[0])
for n, rec in REC.items():
    got = hashlib.sha256(rd(n)).hexdigest()
    obj = subprocess.run(["git", "-C", LANE, "cat-file", "-p",
                          f"{BASE}:.ufo/waves/round-52/fetch/{n}"],
                         capture_output=True, check=True).stdout
    print(f"HASH {n} match={got == rec} worktree_eq_gitobj={obj == rd(n)}")

print("SUMS file exists:", os.path.exists(FETCH + "/SHA256SUMS"),
      "| .txt exists:", os.path.exists(FETCH + "/SHA256SUMS.txt"),
      "| abs_paths:", all(l.split("  ", 1)[1].startswith("/")
                          for l in rd("SHA256SUMS").decode().strip().splitlines()))

for pid, pin, lo, hi, q in PROPS:
    L = lines(pin)
    span = L[lo - 1:hi]
    v4 = " ".join(x.strip() for x in span if x.strip())
    v3 = " ".join(x.strip() for x in span)
    print(f"{pid} pin={pin} {lo}-{hi} raw_substr={q.encode() in rd(pin)} "
          f"q_has_newline={chr(10) in q} v3={v3 == q} v4={v4 == q} "
          f"blanks={[lo + i for i, x in enumerate(span) if not x.strip()]} "
          f"uniq_in_collapsed_doc={' '.join(x.strip() for x in L if x.strip()).count(q)}")

ca = rd("Hyprland-ConfigActions.cpp").decode()
print("sendKeyboardMods lines:", [ca[:i].count("\n") + 1 for i in range(len(ca))
                                  if ca.startswith("sendKeyboardMods", i)])
print("P20 quote count in ConfigActions:", ca.count("sendKeyboardMods(0, 0, 0, 0);"))
for pin in REC:
    if pin == "Hyprland-ConfigActions.cpp":
        continue
    print(f"P19 quote in {pin}: raw={rd(pin).decode().count(PROPS[0][4])}")

rows = [l.rstrip("\n") for l in open(ENTRY, encoding="utf-8")
        if l.startswith("| P1") or l.startswith("| P2")]
for r in rows:
    c = [x.strip() for x in r.strip().strip("|").split("|")]
    m = re.match(r"(.+):(\d+)(?:-(\d+))?$", c[4])
    q = c[5].strip("`")
    frozen = next((p[4] for p in PROPS if p[0] == c[0]), None)
    print(f"ROW {c[0]} cols={len(c)} pin={m.group(1)} anchor={m.group(2)}-{m.group(3) or m.group(2)} "
          f"quote_eq_frozen={q == frozen} words={len(q.split())} bytes={len(q.encode())}")
```

Additional one-off checks used for F2/F6 (not in the reproducer, outputs quoted in the findings):
per-line `repr()` dumps of `ConfigActions.cpp:1548-1585` and
`DispatcherTranslator.cpp:565-599,610-630`; the four normalization variants
`v1="".join(span)`, `v2=" ".join(span)`, `v3`, `v4`; and the whitespace-stripping comparator
`re.sub(r"\s+","",s)` applied to both the P22 span and the tampered string literal.
