# R96MCritic -- falsification of claims-declaration-r96.md before the freeze

Seat: R96MCritic (critic, leaf). Round 96 / hyaku run 15 / attempt 1, wave w1. Lane
`/home/vgpnk/Projects/shokunin/mado-shokunin`, base `9f029f46f01f6cd3a1d29ac39bb548498a1d0c3d`.
Read: the declaration, the sources receipt, the round-95 declaration/lesson/fetch, the round-94 critic
(precedent C1-F1), the gate, the receipt-presence tool, the r90 counter. The wave's drafts landed while this
review ran; the measurements below are against the drafts as of 11:48 (`build/mado-mimetext.c1.py` sha
`951a4923...`, `build/check-receipt-presence.c2.py` sha `be716a63...`). The C1 cases/fresh generator/counter
and the C2 counter/panel were still absent at review, so the counting-command findings remain for the L1. No
frozen claim was measured; I edited no file but this report.

## Pins verified before use

```
2d6f1219fae19a85cc92f7d4103db396e1306fea74c2226bb068b335598da61b  quality/check-selftest-strength.py (gate, unchanged)
4ef019c69ea8ae4147f83d1558683f012fb4aac0815d36770304717aaca6af24  tools/mado-mimesniff.py (base blob == working tree)
38a2ea60dc698c45957a3ad4af3132297dd2edb354d815e7ff3433c42bab47ca  quality/check-receipt-presence.py (base)
255cb8b6123d6af1be2f79cd87bfab127a16b581fcebf71dfa517bf0ee01f06c  quality/counters/c2-r90-receipt-presence.py
f7ab86c25edbb806a9f947af09fab5cf971a42602c252966c0075b9aeefa7939  r90 set
68b39a805755f7685c00c847a48b0f8f679fdca2710773efb5f4469b7bebe82d  r90 mutants
9d5947a70d112796f39c3e309c5a25e5ff333b5ebeb51867ebe748af1135ba87  r95 host list (4911 lines)
99df35f8b3fd7005f30789f8866984a1bbceaff8dc6c1d326f0132eb7b4d124a  r95 oracle source (compiled -O0)
fcb1eafe748d3dc18f7f405d1078c8a32e313d23d2fab86b0f12e609ac2ce742  round-96 fetch/xdgmimemagic.c (18289 B)
afb1c1c1ba726a9fb8d8732f4031f5aa85a67ec3b7a2f989b617e4f4f5282410  round-96 fetch/xdgmime.c (23417 B)
e00fa00e69b1e95ad8642d05fc5023c26f859bdaf8bdda3e091a55feb016c61e  round-96 fetch/smi-ar01s02.html (59208 B)
951a49230be98b2eb8ee29aef03793c3eff331293b8b46ea0d06fb0efe91bb97  build/mado-mimetext.c1.py (draft, 11:48)
be716a63662f326a771d96dc5324e89fe07abdff6949029cabb8b7f5d15ca962  build/check-receipt-presence.c2.py (draft, 11:43)
9c411d2af41ac283fb7d229152f0b7b28b7854eabd057135a225762389d1ddd7  controls/host-text-db-r96.json
c9eb0600fe5584c242adf59a2118a186179ba7c6ec9da904a7dd7362f00f31ee  controls/magictext-mutants-r96.json
06800cd141a18548c63701a44f9cab70e2c90f0f316fb6f24d0c06fca079fd97  controls/forgery-ctypes-r96.py
386a5a18f77bf6fa564f2a11498ef21f5c1e7ef461028a2956050d3af52ecda0  controls/r90-c2-argv-r96.json
```

The three round-96 fetch files match the receipt digests and the round-95 copies (the dir was empty at 11:30,
populated by 11:43; the L1 must commit them with the freeze).

## Verdicts

- **C1 -- refuse as written, but the surface, the model and the draft tool hold.** Five defects are in the
  counting command / predicate text, not in the candidate: the host leg is not wired to the wave's own
  text-root manifest (F1), the host-list pin is wrong (F2), the tool and sibling pins are absent from the
  command (F3), the 16-class population is not in the declaration (F7), the forgery is unnamed (F8). Two
  contract sentences contradict the C and the draft (F4 word 0, F5 indent exactness) and one control cannot
  be 0 over the set (F6). All are fixable before the freeze without widening the predicate.
- **C2 -- refuse as written.** The declared change ("selftest output only") does not make the predicate's
  (vi) satisfiable; the draft's block move does, and the declaration must freeze the move (G1). The frozen
  kill-set must also use exact lists where it claims singleton kills (G1b). The rest is bookkeeping (G2-G4).

---

## C1 -- what the draft measures (positive evidence)

```
python3 -I build/mado-mimetext.c1.py --selftest           (lone copy, no sibling)  -> checks=50 failed=0, rc 0
text root, [50:test/x] >0=<len=3>ABC ~0, data ABC         -> test/x 0                (== oracle)
text root, [50:test/x] >0=<len=2>BA ~2, data AB           -> test/x 0                (== oracle)
text root, parent >0=<1>A + 2>1=<1>B, data AB             -> text/plain 0           (== oracle; indent jump)
text root, parent >0=<1>A + 1>1=<1>B, data AB             -> test/outer 0           (== oracle)
text root, >0=<1>A + 1>2=<1>B + >0=<1>C, data A..B        -> text/plain 0           (== oracle; failed child)
text root, >0=<len=0>, data ZZ                            -> test/x 0               (== oracle)
--data-dirs /usr/share (cache present)                    -> "MADO_MIMETEXT: UNSUPPORTED cache-mode", rc 3
--data-dirs <empty>                                       -> mode=none, fallback/zerosize answers == oracle
```
The draft's docstring already models `word_size 0` (`:440-443`) and the exact `indent+1` tree, and its
selftest carries m19 (`word size 0`) and m24 (`a child must sit at exactly indent+1`). The findings F4/F5 are
therefore about the *contract sentences the wave was given*, not about the candidate: the frozen cases must
still carry the oracle-labelled discriminators, or the sentence's error goes unmeasured for the next tool.

### F1 -- the host leg is not wired to the wave's cache-free text root (the command names a cache dir)

`/usr/share/mime/mime.cache` exists (207520 B, header 0x00010002) and loads, so a process pointed at
`/usr/share` is in cache mode: the r96 candidate prints `UNSUPPORTED cache-mode` and the oracle answers from
the cache. The counting command passes `--host-mime-root /usr/share/mime`; a host leg run that way is 0 by
construction. The wave already built the right instrument: `controls/host-text-db-r96.json` (sha
`9c411d2a...`) documents the eight-file copy (`magic globs globs2 aliases subclasses icons generic-icons
XMLnamespaces`), per-file sha256 (`magic` `2942f4ad...`, `globs2` `556ee69c...`), `mime_cache_in_copy: 0`,
and a cross-check against the round-94 pins. Measured: the copy is a valid text root (oracle answers
`application/x-executable 0` for `/usr/bin/true`, `text/plain 0` for `/etc/hostname`; 200 sampled host paths
give 5 distinct types).

Evidence that the direct root is cache mode:
```
$ tools/mado-mimesniff.py --data-home-unset --data-dirs /usr/share --home H /usr/bin/true
MADO_MIMESNIFF_DIRS: mode=cache dirs=H/.local/share/mime/,/usr/share/mime/
MADO_MIMESNIFF: application/x-executable uncertain=0 name=- file=/usr/bin/true
$ build/mado-mimetext.c1.py --data-home-unset --data-dirs /usr/share --home H /usr/bin/true
MADO_MIMETEXT: UNSUPPORTED cache-mode            (rc 3)
```
Impacted axes: coverage (iii), provenance.
Smallest safe correction: replace `--host-mime-root /usr/share/mime` with
`--host-db controls/host-text-db-r96.json --expect-host-db-sha256 9c411d2a...`; the counter verifies every
per-file sha and `mime_cache_in_copy == 0` before scoring and prints `host_db=ok files=8`. Replay:
`sha256sum <root>/mime/*` must equal the manifest and `find <root> -name mime.cache` must be empty.

### F2 -- the host-list sha256 in the counting command is wrong (head+tail splice)

The declaration pins `--expect-host-list-sha256 9d5947a7ba87`; the file's digest is
`9d5947a70d112796f39c3e309c5a25e5ff333b5ebeb51867ebe748af1135ba87` (the round-95 table carries it in full).
The declared value splices the first 8 and the last 4 hex chars; it is neither the full digest nor a prefix.
Replay: `sha256sum .ufo/waves/round-95/controls/mimesniff-host-files-r95.txt`. Correction: paste the full
64-hex digest (the file has 4911 lines, matching round 95's table).

### F3 -- the counting command omits the tool pin and the sibling pin the predicate requires

The predicate's first conjunct is "`tool_sha256 == --expect-tool-sha256`, printed `tool_pin=ok`", and the
candidate "loads `tools/mado-mimeglob.py` ... pinned by sha". The C1 command passes neither
`--expect-tool-sha256` nor `--expect-mimeglob-sha256`; round 95's command passed both. Replaying the C1
command verbatim either errors on a required argument or measures an unpinned tool. Correction: add
`--expect-tool-sha256 <frozen tool>` and
`--expect-mimeglob-sha256 65f80a6cb1551bb722ae7608df04fb17deba1b5cd05bef6f7fdd79bed76e2453` and print both
pins in the verdict line.

### F4 -- model sentence wrong: the C accepts `word_size 0` (contract says 1|2|4 only)

`xdgmimemagic.c:432-449` rejects a word size only when it is not 0, 1, 2 or 4 (`:440-447`); the swap/modulo
block runs only for `word_size > 1`, so 0 behaves as 1. The shared contract says "word size (1|2|4 only ...)".
The draft tool is already correct (docstring cites `:440-443`, selftest m19); the *contract sentence* is what
a future tool builds to. Oracle evidence: `~0` with a 3-byte value and data ABC -> `test/x 0`; `~2` with a
3-byte value -> error -> `text/plain 0`; `~2` value `BA` matches data `AB` (parse swap); `~2` value `AB` does
not match `AB`; `~4` `DCBA` matches `ABCD`; a masked value swaps with its mask. Correction: the sentence must
read "0|1|2|4; 0 is accepted and behaves as 1 (no swap, no modulo)", and the frozen `word` class must hold a
`~0` case (odd value length) plus a swap discriminator.

### F5 -- the indent rule is `indent+1` exactly; "the deeper chain is tested" is ambiguous

`xdgmimemagic.c:558-587`: a held matchlet recurses only when the next matchlet sits at exactly `indent+1`
(`compare_level(next, indent+1)`); a jump (0 -> 2) makes that call FALSE and the do-while skips the whole
subtree. Oracle: parent `>0=A` with child `2>1=B`, data AB -> `text/plain 0`; the same child at indent 1 ->
`test/outer 0`. The draft is correct (selftest m24; measured above). Correction: state "a child is tested only
at indent+1; an indent jump skips the subtree and the parent's match is void at that level", and freeze both
contrast cases in `indent`.

### F6 -- the do-nothing control is not 0 over the frozen set (mode `none` cases are answered)

The round-95 tool refuses only when a text file exists (`mado-mimesniff.py:325` lists
`/globs2 /globs /magic /aliases /subclasses`). In mode `none` it answers like the oracle:
```
$ tools/mado-mimesniff.py --data-home-unset --data-dirs <empty> --home H text empty bin
MADO_MIMESNIFF: text/plain uncertain=0              (oracle text/plain 0)
MADO_MIMESNIFF: application/x-zerosize uncertain=0  (oracle application/x-zerosize 0)
MADO_MIMESNIFF: application/octet-stream uncertain=1 (oracle application/octet-stream 1)
```
The 16-class population includes `mode`, `fallback`, `zerosize`, so the frozen set must contain `none`-mode
cases and the control scores them correct. Correction: "the do-nothing instrument is 0 on the frozen cases
with `db_mode == "text"`; its none-mode score is reported as `do_nothing_none=K`", or replace it with
"refuses every text-mode case". Replay: run the r95 tool over one none-mode case; any (type, uncertain) match
falsifies `do-nothing == 0`.

### F7 -- the 16-class population is not in the contract (r94 C1-F1 repeated)

The declaration section C1 does not contain the 16 names (`grep -c` = 0); the only copy is the wave dispatch
context. The predicate says "the per-class census equal to the declared `CLASSES`" -- a dangling reference,
and if the counter reads the `classes` array from the case JSON the clause is a tautology (round 94's
critic, `.ufo/waves/round-94/w1/R94MCritic.md` C1-F1, is the same shape and its repair is the template).
Correction: put the explicit list in the predicate/freeze block, require the counter to hardcode it, print
`classes=16/16`, and SETUP_ERROR on an unknown class or a class with <8 cases; the JSON's `classes` must
equal the hardcoded tuple. Replay: doctor a copy of the frozen cases (delete 8 `mask` cases), recompute its
sha, run with the new `--expect-cases-sha256`; the counter must not print `TARGET_MET`.

### F8 -- the forgery exists but the command names no input for it

`controls/forgery-ctypes-r96.py` exists (sha `06800cd1...`, `ctypes.CDLL("libgio-2.0.so.0")`); predicate (v)
requires it rejected with `audit_denials > 0`, but the counting command has no `--forgery` /
`--expect-forgery-sha256` (round 95 had both). Correction: pass the frozen forgery with its sha and print
`forgery_static=<what> audit_denials=N`; require `audit_denials > 0`.

### F9 -- edge rules the contract leaves unstated (coverage asks; the draft is measured correct)

```
>0=<len=0>                            data ZZ -> test/x 0        (zero-length value matches any data)
matchlet line without the final \n    data AB -> text/plain 0    (EOF mid-line drops the section)
>0=<len=2>AB +0                       data AB -> text/plain 0    (range 0: no iteration)
[50:x] junk after ]                   data AB -> test/x 0        (bytes after ] ignored)
```
The draft agrees with the oracle on all four. Freeze one of each in `value`, `range`, `sect` (the zero-length
value is the sharpest: a tool that treats 0 as an error or as "no compare" diverges).

### F10 -- provenance nit: the S524 located line is off by one

The sources receipt's S524 headline says "(line 815, `wc -l` 819): if (memcmp ("MIME-Magic\0\n", header,
12) == 0)". The memcmp is at line 814 (`awk 'NR==814'`); 815 is the call to `_xdg_mime_magic_read_magic_file`.
`wc -l` 819 is correct. Fix the number before the freeze.

---

## C2

### G1 -- the declared change ("selftest output only") does not satisfy (vi); the draft's block move does, and the declaration must freeze it

Measured on the base-order tool with a faithful simulation of the declared change (three FAIL sites ->
`{name}-rc` / `{name}-lines` labels, detail on `RECEIPT_PRESENCE_SELFTEST_DETAIL:`, `checks=6 failed=0`
green): the gate's `non_selftest_prefix` cuts at `def selftest(` (line 122), so kill mutants can touch only
the regexes and `git()`/`added_lines()`/`expand()`/`candidates()`; every rc and every verdict/missing line is
decided in `main()`/`setup()` after the cut. The rc and the asserted line are one predicate (`missing` drives
`cited/present/missing`, `verdict`, and `0 if missing == 0 else 1`; `setup()` prints in the branch that
returns 2). Results:
```
kill candidates: return [cite] -> return []      must_fail ["OK-rc"]
  WRONG_CHECK K-ok-rc failed=['OK-rc', 'OK-lines', 'MISSING-lines']     held=0
neutralise the rc arm, same kill -> WRONG_CHECK failed=['OK-lines', 'MISSING-lines']   (ii) only via WRONG_CHECK
SETUP-lines: cannot fail alone (the setup line is printed only by the return-2 branch)
```
The draft (`be716a63...`, R96MExecKillsC2, "block move (L1 amendment, measured necessity)") moves the whole
`def selftest()` block after `main()`, so the gate prefix covers the production path. Measured on the draft:
```
python3 -I build/check-receipt-presence.c2.py --selftest            -> checks=6 failed=0
gate --tool draft --kills build/check-receipt-presence.kills.json   -> SELFTEST_STRENGTH: OK kills=7 held=7
each of the 7 kills with must_fail rewritten as a strict list-of-one -> OK held=1, all 7
```
Impacted axes: operability, discernment.
Smallest safe correction: the declaration's Change paragraph and the freeze block must declare the block move
(not "selftest output only") and state what "main path byte-unchanged" means operationally: the production
*text* is the base text with the selftest block relocated. Measured identity (replayable, see G2). Without
the freeze amendment the predicate's (vi) is false; with it, (vi) holds 6/6.

### G1b -- the frozen kill-set's string `must_fail` does not implement "singleton"

The draft kill-set uses `"must_fail": "OK-rc"` etc. The gate treats a string as membership ("the label is
among the FAIL lines"); only a list requires the exact set. "Every one of the 6 labels has a singleton kill"
therefore needs a list of one per label. Measured: rewriting all seven entries to `["<label>"]` keeps the gate
at OK (7/7 held), so the correction is free. Replay: run the gate with the rewritten kill-set; any
`WRONG_CHECK` shows a non-singleton.

### G2 -- the main-path promise: relocation identity + the r90 leg

The r90 counter reads the tool at `--rev` and prints `check_sha256`; measured at base: `TARGET_MET
expectations=83 met=83 population=38 mutants=28 killed=28`, `check_sha256=38a2ea60...`, so the leg is live
and does not pin the tool sha. For the text, the draft's production region is exactly the base's production
region in order: `rev_pre == base_pre + base_main_without_guard`. Replay:
```
python3 - <<'PY'
import subprocess
R='.'; B='9f029f46f01f6cd3a1d29ac39bb548498a1d0c3d'; V='<c2-rev>'
g=lambda p: subprocess.run(['git','-C',R,'show',p],capture_output=True).stdout
a=g(B+':quality/check-receipt-presence.py'); b=g(V+':quality/check-receipt-presence.py')
guard=b'if __name__ == "__main__":\n    sys.exit(main())\n'
bs=a.find(b'def selftest('); bm=a.find(b'def main('); rs=b.find(b'def selftest(')
print('production_relocated_verbatim', b[:rs]==a[:bs]+a[bm:-len(guard)])
PY
```
Measured True on the draft (base_pre 5537 B, base_main 5341 B, guard 48 B, rev_pre 10830 B). Add this as a
conjunct; the r90 leg remains the behavioural proof.

### G3 -- (v)'s controls have no named inputs; the r90 argv is pinned (positive)

The command names `--panel`, `--control-kills`, `--expect-control-sha256`, `--r90-argv`,
`--expect-r90-argv-sha256`; `controls/r90-c2-argv-r96.json` (sha `386a5a18...`) carries the exact r90 argv,
the set/mutants shas and `base_rev 5041acf9...` -- that leg is reproducible (measured at base, above).
Predicate (v) also requires a blanket kill-set, an empty kill-set, an always-OK gate, an always-WEAK gate and
a do-nothing instrument; none is named. Correction: add `--blanket-kills`/`--empty-kills`/`--control-gates`
(or one `--controls <json>` with a sha) and print each control's flagged count.

### G4 -- the panel cannot independently certify strength; only the draft control orders it

The predicate's `hand_flagged == hand` makes the panel the specification of kill coverage; the kill-set and
the panel are authored inside this wave (ExecKillsC2 / MutC2). The only ordering evidence is
`control_hand_flagged < hand`. Correction: freeze the panel's first draft (sha + mtime recorded before the
kill-set draft lands) and state that no entry may be dropped between draft and freeze; the counter prints
`panel_draft_sha256`, `panel_sha256`, `control_hand_flagged`, `hand`.

### G5 -- the surface sentence lists four names for three slots (substance holds)

"The routed defect names three unguarded tools; two are structurally outside ... and mimesniff ...; the
remaining tool is check-receipt-presence" lists mako, verify.sh, mimesniff and check-receipt-presence for
three slots. The routed set (round-95 lesson, line 124: "kill-sets for five unguarded tools") is
{mimeglob, portals, mako, verify.sh, check-receipt-presence}; the first two landed in round 95, so the three
remaining are {mako, verify.sh, check-receipt-presence}; mimesniff is the round-95 tool (also unguarded). The
substance is right; say exactly that. Measured refusals:
```
mako        --selftest                    -> rc 2, stderr "setup error: --selftest requires --scratch-root"
            --selftest --scratch-root .   -> rc 0, stdout 0 lines, stderr "MADO_MAKO_SELFTEST: checks=62 failed=0"
            gate (either argv)            -> SETUP_ERROR ... result [] lacks failed=0
verify.sh   python3 -I tools/mado-verify.sh --selftest -> rc 1, no FAIL lines, no result line -> SETUP_ERROR
            (pass line "MADO_SELFTEST: $n_pass/$n_pass assertions passed", mado-verify.sh:1880)
mimesniff   gate on the repo path, kills=0 -> SELFTEST_STRENGTH: OK
            any kill: the copy runs in scratch without mado-mimeglob.py -> rc 1 "setup error: ... missing";
            measured 1 kill -> "SURVIVED K1", WEAK survived=1
receipt-p.  gate, kills=0 -> OK; selftest "checks=6 failed=0"; with the draft kill-set -> OK kills=7 held=7
```
The pre-change tool is not guardable as the declaration says: a real production mutant yields a
detail-string "label" (`find "n = int(m.group(1))" -> "+ 1"`, must_fail "MISSING" -> WRONG_CHECK with
`MISSING absent=[...] out=[...]`). The other quality checks are refused at gate (1) because their selftest
result line is not `failed=N` shaped (e.g. `MADO_INDEX_SELFTEST: 12/12 assertions passed`), so
receipt-presence is the only gate-compatible unguarded tool of the routed set.

### G6 -- the DETAIL line is invisible to the gate (verified, keep the spelling)

`RECEIPT_PRESENCE_SELFTEST_DETAIL: ` does not start with `RECEIPT_PRESENCE_SELFTEST: ` (underscore vs colon),
so neither the fail filter nor the result filter sees it and `results[-1]` remains the result line. Keep the
underscore; any spelling with the result prefix would be parsed as a result or a fail label.

---

## Attacks the L1 can replay, one command each

| # | attack | command | falsifies |
|---|---|---|---|
| 1 | host root is cache mode | `tools/mado-mimesniff.py --data-home-unset --data-dirs /usr/share --home H /usr/bin/true` (prints `mode=cache`); `build/mado-mimetext.c1.py ... /usr/share ...` (rc 3 `unsupported cache-mode`) | F1 |
| 2 | host-list pin | `sha256sum .ufo/waves/round-95/controls/mimesniff-host-files-r95.txt` vs the declared 12 chars | F2 |
| 3 | tool/sibling pins | replay the C1 command verbatim; `--expect-tool-sha256`/`--expect-mimeglob-sha256` absent | F3 |
| 4 | word 0 | text root `[50:test/x] >0=<len=3>ABC ~0`, data ABC; oracle `test/x 0` | F4 |
| 5 | indent jump | `>0=<1>A` + `2>1=<1>B` vs `1>1=<1>B`, data AB; oracle text/plain vs test/outer | F5 |
| 6 | do-nothing on none | r95 tool with `--data-dirs <empty>` on text/empty/bin; compare (type, uncertain) | F6 |
| 7 | class list | `grep -c 'header sect value mask word range indent order drop multi glob alias fallback zerosize mode desktop' .ufo/waves/round-96/claims-declaration-r96.md` -> 0 | F7 |
| 8 | doctored cases | delete 8 `mask` cases from a copy of the frozen file, recompute sha, run the counter; must not be TARGET_MET | F7 |
| 9 | located line | `awk 'NR==814' .ufo/waves/round-95/fetch/xdgmimemagic.c` | F10 |
| 10 | C2 pre-move | base-order tool + the label-only change, kill `candidates -> []`, `must_fail ["OK-rc"]` -> WRONG_CHECK with 3 labels | G1 |
| 11 | C2 move | draft + draft kill-set -> `OK held=7`; rewrite the 7 must_fail as list-of-one -> `OK held=1` each | G1/G1b |
| 12 | C2 main path | the relocation identity snippet in G2 -> `production_relocated_verbatim True` | G2 |
| 13 | C2 controls | `grep -o -- '--blanket-kills\|--empty-kills\|--control-gates' <command>` -> absent | G3 |
| 14 | C2 panel draft | panel draft sha/mtime vs the kill-set draft's | G4 |
| 15 | C2 refusals | the four gate runs in G5 | G5 |

## Answers to the seat's questions

| question | answer |
|---|---|
| C1 surface held by no lane tool at base? | **yes** -- `git cat-file -e base:tools/mado-mimetext.py` absent; `git grep 'MIME-Magic\|mime/magic' base -- tools quality` empty; `mado-mimesniff.py:325` only stats the path |
| C1 target unreachable by the do-nothing? | **no** over the whole set: the r95 tool answers mode `none` correctly (F6); 0 only on text-mode cases |
| C1 population enumerated in code? | **not yet** -- the 16 names are absent from the declaration (F7); the counter must hardcode them (r94 C1-F1 form) |
| C1 host leg passable by echoing the oracle? | **no** -- the audit forbids spawn; the structural conjunct plus `controls/forgery-ctypes-r96.py` are the lock. But the leg must run on `controls/host-text-db-r96.json`, not `/usr/share` (F1), and every input must be pinned (F2/F3/F8) |
| C1 tool pinned by sha? | **declared yes, command no** (F3) |
| C1 named limit contradicts a rule? | `mime_types` limit verified (`xdgmime.c:535` passes `NULL, 0`); `max_extent` verified outside `for_data` (used by `xdg_mime_get_mime_type_for_file`, `:590`); the `word_size` model sentence is wrong (F4); the int-overflow worry is unreachable (the `i + value_length > len` check at `:525` precedes the read and `i` starts at offset) |
| C2 only gate-compatible unguarded tool? | **yes** of the routed set -- mako (stderr), verify.sh (not Python), mimesniff (lone copy rc 1); other quality checks are refused at (1) for a non-`failed=` result line |
| C2 change out of the main path? | the draft relocates the whole selftest block after `main()`; the production text is verbatim (`production_relocated_verbatim True`). The declaration must freeze the move (G1); the r90 leg is the behaviour check for `main()` |
| C2 r90 leg replayed at the new rev? | the counter is live and green at base (`TARGET_MET` above); and `controls/r90-c2-argv-r96.json` pins the exact argv/shas |
| C2 panel independent of the kill-set author? | **no independent evidence** -- only `control_hand_flagged < hand`; freeze the panel draft (G4) |

## Would I refuse?

- **C1: yes, as written.** F1-F3 and F7/F8 are conjunct-level text/command defects (the host leg cannot pass
  and three pins are absent/wrong); F4/F5 are model sentences that contradict the C (the draft happens to be
  right, but the frozen cases must carry the discriminators); F6 is a control that cannot be 0. All are
  fixable before the freeze without widening the predicate.
- **C2: yes, as written.** G1: the declared change does not satisfy (vi); the draft's block move does, and the
  declaration must declare it. G1b: the kill-set's string labels do not implement "singleton" (lists fix it,
  measured). G3/G4 are pinning bookkeeping.

Scratch: `/fast/scratch/hyaku/mado-r96/R96MCritic` (oracle build, fixtures, gate copies, the pre-move
simulation, the draft probes); removed before this seat yielded. Tool installs: none. Files edited: this
report only.
