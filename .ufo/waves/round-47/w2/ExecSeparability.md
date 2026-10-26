# ExecSeparability — C1/C2 separability, both ways, on the frozen instruments (round 47, w2)

**Verdict: separability holds in both directions on the frozen bytes, and both claims are simultaneously reachable at
the freeze. One registered artifact does not transfer: the C2 positive control built by `ctl/c2/build-control.py` is
MISSED at the frozen revision (clause e), because it is built at BASE where the freeze's second byte-identical script
pin does not exist. One leniency found in clause e/c/d (line bound is one past EOF).**

Instrument state used: freeze `d7527d60` (counters, 190 C1 fixtures, pins, L1 reference), base `60edb66e`; C1 judge pin
`fetch/xdg-terminal-exec` sha256 `89f2be9a65deb8…`; L1 reference sha256 `762d042c96e7…` (blob `ee46a8a6` at the freeze,
byte-equal to the working-tree draft); pin tarball `v0.14.3` sha256 `82ac2dfdb357…` (fetched, verified, `pins.txt`).
Nothing was installed; no resolver was run except by the counters inside bwrap.

## The four summary lines (both trees at the frozen rev)

```
# C1 on tool-only  (freeze + reference at tools/mado-terminal.py, commit 543e07b9)      c1-tool-only.txt
PRED-C1-r47: fixtures=190/190 explained=190/190 generated=150/150 selftest=ok readonly=ok tool=present verdict=TARGET_MET rev=543e07b9c4456387e61f1448caeee9e661f2cf6d nonce=3734215788
# C2 on tool-only                                                                      c2-tool-only.txt
PRED-C2-r47: admitted=0/1 verdict=TARGET_MISSED rev=543e07b9c4456387e61f1448caeee9e661f2cf6d      (clause=a entry_absent)
# C1 on entry-only (C2 POS transplanted to the freeze, commit 22fbc51b)                c1-entry-only.txt
PRED-C1-r47: fixtures=0/190 explained=0/190 generated=0/150 selftest=fail readonly=fail tool=absent verdict=TARGET_MISSED rev=22fbc51b23b0480d7875d92eca0f2866f24393d1 nonce=2440397234
# C2 on entry-only                                                                     c2-entry-only.txt
PRED-C2-r47: admitted=1/1 verdict=TARGET_MET rev=22fbc51b23b0480d7875d92eca0f2866f24393d1
```

Cross terms: BASE both MISSED (`c1-base.txt`, `c2-base.txt`); the C2 POS *as built at BASE* `4a7f9528` is C2-MET /
C1-MISSED (`c2-control-base.txt`, `c1-control-base.txt`); the same POS *transplanted to the freeze* `cabe264e` is
C2-**MISSED** (`c2-ctl-transplanted-freeze.txt`, hole F1); entry-only plus a garbage tool `ec64c2c1` is C2-MET
(`c2-garbage-tool.txt`); both claims `b492ea5c` is C1-MET and C2-MET (`c1-both.txt`, `c2-both.txt`).

## Holes (a hole found before data re-registers v2)

**F1 — clause e binds to the alphabetically first byte-identical script pin; the frozen POS control is MISSED at the
frozen rev.** Reproduce: `repro.sh` (POS as built → MET at BASE; `git diff BASE..HEAD | git apply` onto a `d7527d60`
clone → MISSED, `clause=e step_without_script_range` on lines 15-21, `script_cited=0`, `script=xdg-terminal-exec:1500`).
Cause, from `probe-clause-e.txt` (importlib on the counter): the tree holds `fetch/xdg-terminal-exec` (freeze) and
`fetch/xdgte-xdg-terminal-exec` (control), both `89f2be9a…`; `clause_e` (`quality/counters/c2-r47-terminal-entry.py:519-546`)
takes `sorted(...)[0]`, and `resolve_pin` (`:302-315`) prefers the exact alias, so 7/7 steps resolve to the wrong copy.
Renaming only those seven tokens to the freeze name flips the identical tree to `admitted=1/1` (`22fbc51b`).
Live exposure: the w1 drafts use the freeze names (`w1/ScrEntry/entry.md` cites `xdg-terminal-exec:<n>` throughout;
`w1/ScrRows/rows.md` cites `fetch/xdg-terminal-exec`, `fetch/README.md`), so the drafted data should pass — but the
registered "POS admitted" receipt is base-specific and the clause rejects an entry that cites a correctly-pinned
byte-identical copy under any alias. v2 fix: accept a locator resolving to **any** fetch copy whose sha256 is
`SCRIPT_SHA`, and take `nlines` from the copy the locator resolves to.

**F2 — the pin line bound is one past EOF, so a chain step citing a nonexistent line satisfies clause e.** `nlines` is
`len(blob.split("\n"))` = 1500 for the 1499-line script. An appended 8th step whose only locator is
`xdg-terminal-exec:1500` gives `steps=8 script_cited=8 … admitted=1/1` (`c2-clone-vac1500.txt`); `:1501` gives
`step_without_script_range line=22`, `e:0` (`c2-clone-vac1501.txt`). The same `plines` bound guards clause c anchors
and clause d locators, so `<last+1>` is "inside its line count" there too (a quote still fails on content).
Fix: subtract the trailing newline before comparing.

**F3 (observation, no clause affected)** — `ctl/c2/build-control.py:259-300` defines `write_tool()` (a double that
answers `explain --observed`) and `main()` never calls it; its docstring still describes the pre-freeze clause f ("the
landed tool must reproduce the receipt"). `build_tree()` also leaves an empty untracked `tools/`. The POS entry's live
paragraph still says "the landed tool's verdict" in a tree with no tool. Delete both in v2 so no later editor re-couples
C2 to C1.

**F4 (cosmetic)** — the control's quote table maps nine spans but the body substitutes eight (`qb133` unused), so the
builder's "quotes 9" log is one higher than the entry; the counter's `clause=d quotes=8` is right.

## Static basis for separability

C2 has exactly two subprocess sites, both `git` (`c2-r47-terminal-entry.py:157,162`), no `bwrap`, and names the tool
only in its own docstring (`:73`). C1 never names `corpus`/`knowledge`/the entry (`grep` → none). Both directions are
also shown black-box: C2 MET with a tool that prints `NONSENSE`, C1 MET with the entry present and without it.

## Retained evidence (seat dir `.ufo/waves/round-47/w2/ExecSeparability/`)

`findings.md` (full write-up with commands and outputs), `repro.sh` (runs everything), `pins.txt`, `trees.txt`
(commit ids and what each tree holds), `probe-clause-e.txt`, and the counter transcripts `c1-tool-only.txt`,
`c2-tool-only.txt`, `c1-entry-only.txt`, `c2-entry-only.txt`, `c1-both.txt`, `c2-both.txt`, `c1-base.txt`,
`c2-base.txt`, `c1-control-base.txt`, `c2-control-base.txt`, `c2-ctl-transplanted-freeze.txt`,
`c2-garbage-tool.txt`, `c2-clone-vac1500.txt`, `c2-clone-vac1501.txt`, `c2-oob-1500.txt`, `oob-note.txt`.

## Not established

No data commit exists; every line above is a synthetic tree at the freeze or at BASE. F1 does not show the drafted
entry fails — it shows the control does not transfer and that a byte-identical alias flips clause e. One host only
(this host's bash/find/awk/tr as judge); no cross-host drift comparison was attempted.
