# C1/C2 separability, both ways, on the frozen instruments (round 47, w2)

Seat `ExecSeparability`. Instrument revisions: counters and pins at the freeze
`d7527d608ad2b2e3cc398fdde34db7947b254a1a` (base `60edb66e2f1cb90acc6e9442fc93ded0ca42d750`), C1 judge pin
`.ufo/waves/round-47/fetch/xdg-terminal-exec` sha256 `89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac`,
L1 reference `.ufo/waves/round-47/l1-draft/mado-terminal.py` sha256
`762d042c96e7e5f2c3187133b0ffe670c1d076b698b958199602cfa019aa6c08` (blob `ee46a8a6` at the freeze, byte-equal to
the working-tree draft). Pins: codeload tag `v0.14.3` tarball sha256
`82ac2dfdb357361d15f5163cdeb3cfd457bbb30bf5d2e14436393f493bd32afe` (`pins.txt`). No package was installed; nothing
in the lane was written outside this seat directory and the Report.

## The four summary lines (both trees at the frozen rev)

Tree 1 = **tool-only**: shared clone of the lane, `--detach d7527d60`, the L1 reference copied to
`tools/mado-terminal.py`, one commit (`543e07b9`). No entry, no rows, no receipts.
Tree 2 = **entry-only**: clone of tree 1's base, the C2 POS control (`ctl/c2/build-control.py`, `C2R47_WORK=<scratch>`)
transplanted with `git diff BASE..ctl-HEAD | git apply --index`, i.e. entry + rows + README row + `fetch/xdgte-*` +
receipts and **no** `tools/mado-terminal.py`; the entry's chain locators then renamed from the control's alias
`xdgte-xdg-terminal-exec:` to the freeze pin name `xdg-terminal-exec:` (commit `22fbc51b`). Rationale in F1: with the
alias the same tree is MISSED for a naming reason unrelated to tool/entry coupling.

```
# C1 on tree 1 (tool-only)                                                   c1-tool-only.txt
PRED-C1-r47: fixtures=190/190 explained=190/190 generated=150/150 selftest=ok readonly=ok tool=present verdict=TARGET_MET rev=543e07b9c4456387e61f1448caeee9e661f2cf6d nonce=3734215788
# C2 on tree 1 (tool-only)                                                   c2-tool-only.txt
PRED-C2-r47: admitted=0/1 verdict=TARGET_MISSED rev=543e07b9c4456387e61f1448caeee9e661f2cf6d
# C1 on tree 2 (entry-only)                                                  c1-entry-only.txt
PRED-C1-r47: fixtures=0/190 explained=0/190 generated=0/150 selftest=fail readonly=fail tool=absent verdict=TARGET_MISSED rev=22fbc51b23b0480d7875d92eca0f2866f24393d1 nonce=2440397234
# C2 on tree 2 (entry-only)                                                  c2-entry-only.txt
PRED-C2-r47: admitted=1/1 verdict=TARGET_MET rev=22fbc51b23b0480d7875d92eca0f2866f24393d1
```

Cross terms, same instruments:

| tree | C1 | C2 |
|---|---|---|
| BASE `60edb66e` (neither) | MISSED, `clause=a tool=absent` (`c1-base.txt`) | MISSED, `clause=a entry_absent` (`c2-base.txt`) |
| freeze `d7527d60` (neither) | MISSED, `tool=absent` | MISSED, `entry_absent` |
| C2 POS as built by `build-control.py` at BASE `4a7f9528` | MISSED, `tool=absent` (`c1-control-base.txt`) | **MET** `admitted=1/1` (`c2-control-base.txt`) |
| C2 POS transplanted to the freeze, alias naming `cabe264e` | (no tool) MISSED | **MISSED**, `clause=e` 0/7 (`c2-ctl-transplanted-freeze.txt`) — F1 |
| entry-only at freeze, freeze pin name `22fbc51b` | MISSED, `tool=absent` | MET |
| entry-only + **garbage** `tools/mado-terminal.py` `ec64c2c1` | — | **MET** (`c2-garbage-tool.txt`) |
| both claims `b492ea5c` (reference tool + entry) | **MET** 190/190, 190/190, 150/150, selftest ok, readonly ok (`c1-both.txt`) | **MET** (`c2-both.txt`) |

Verdict: the two instruments are separable in both directions on the frozen bytes — C1 reads only
`tools/mado-terminal.py`, C2 reads only entry/rows/README/pins/receipts — and both claims are simultaneously
reachable at the frozen rev (`b492ea5c`). One registered artifact does not transfer (F1).

## Static basis

```
$ grep -n "tools/\|subprocess\.\|bwrap\|mado-terminal" quality/counters/c2-r47-terminal-entry.py
157:    p = subprocess.run(["git", "-C", repo, *args], capture_output=True, env=ENV)
162:    return subprocess.run(["git", "-C", repo, *args], capture_output=True,
```
Both subprocess sites are `git`; C2 executes nothing else, has no `bwrap`, and names the tool only in its own docstring
(`:73`, describing the L1 change). Confirmed black-box: `ec64c2c1` carries a tool that prints `NONSENSE` and exits 0,
and C2 is still `admitted=1/1`.

```
$ grep -n "corpus\|knowledge\|selection-r47" quality/counters/c1-r47-terminal.py
(none)
```
C1 never names the C2 surface; its inputs are `tools/mado-terminal.py`, the fixture JSON beside itself, and the judge
pin. Confirmed black-box: C1 is `TARGET_MET` on `543e07b9` (no entry) and on `b492ea5c` (entry present).

## F1 — C2 clause e is pinned to the alphabetically first byte-identical script copy, so the frozen POS control is not admitted at the frozen rev

Attack: `quality/counters/c2-r47-terminal-entry.py:519-546` takes
`scripts = sorted(fetch pins whose sha256 == SCRIPT_SHA)` and requires every chain locator to resolve to
`scripts[0]`; `resolve_pin` (`:302-315`) lets an exact fetch name win, so a locator naming a byte-identical alias
resolves to the alias and is rejected.

```
$ python3 -I quality/counters/c2-r47-terminal-entry.py --repo <clone-entry> --rev HEAD   # freeze + POS control, as built
PRED-C2-r47 ... clause=e step_without_script_range line=15   (…lines 15-21, all seven steps)
PRED-C2-r47 ... clause=e steps=7 script_cited=0 script=xdg-terminal-exec:1500
PRED-C2-r47 ... clauses=a:1 b:1 c:1 d:1 e:0 f:1 g:1 h:1 i:1 admitted=0
PRED-C2-r47: admitted=0/1 verdict=TARGET_MISSED rev=cabe264e85c8f195736d33175b1fc5756a8492ff
```
`probe-clause-e.txt` (importlib on the counter itself) shows the cause: the frozen tree holds both
`fetch/xdg-terminal-exec` (freeze) and `fetch/xdgte-xdg-terminal-exec` (control), both hashing to `89f2be9a…`;
`sorted()[0] = "xdg-terminal-exec"`, and each step's token resolves to `xdgte-xdg-terminal-exec` → `equals_scripts0=False`
for all seven. Renaming *only* the seven tokens to the freeze name, changing no other byte, flips the same tree to
`admitted=1/1` (`22fbc51b`).

Why it matters: `ctl/c2/build-control.py` clones the lane at **BASE**, where the freeze's `fetch/` does not exist, so the
registered POS receipt (`receipts/ctl-c2/`, `admitted=1/1`) never sees the duplicate-copy shape that every revision on
top of the freeze has. The registration's separability paragraph ("the C2 positive control is an entry-only tree and is
admitted … shown both ways again on the landed bytes by a w2 seat") is therefore false at the landed rev for the
control's own naming, and the clause rejects an entry that cites a correctly-pinned, byte-identical copy under a
different name.

Live exposure of the drafted data: the w1 data drafts name pins by the freeze names —
`grep -o "xdg-terminal-exec:[0-9-]*" w1/ScrEntry/entry.md` gives 100+ tokens, all `xdg-terminal-exec:<n>`; `w1/ScrRows/rows.md`
cites `fetch/xdg-terminal-exec`, `fetch/README.md` — so a data commit that adds no renamed script copy keeps one
`SCRIPT_SHA` pin and clause e passes. The trap is armed for any renaming (the control's own recipe uses it, and
`w1/` still carries 36 `xdgte-xdg-terminal-exec` tokens, e.g. `w1/ExecControls/`). v2 fix: accept a locator that
resolves to any fetch copy whose sha256 equals `SCRIPT_SHA`, and derive `nlines` from the pin the locator resolves to.

## F2 — `nlines` is one past the last line: a step citing a nonexistent line satisfies clause e

`clause_e` uses `len(blob.split("\n"))` (1500 for a 1499-line script), so line 1500 — the empty tail after the final
newline — is inside the bound, and clause e demands only a range, not content.

```
$ # 8th step appended to the entry: "8. Vacuous step: … (xdg-terminal-exec:1500)."
$ python3 -I quality/counters/c2-r47-terminal-entry.py --repo <clone-vac1500> --rev HEAD
PRED-C2-r47 ... clause=e steps=8 script_cited=8 script=xdg-terminal-exec:1500
PRED-C2-r47 ... clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 admitted=1          <-- c2-clone-vac1500.txt
$ # same with :1501
PRED-C2-r47 ... clause=e step_without_script_range line=22
PRED-C2-r47 ... clauses=a:1 b:1 c:1 d:1 e:0 ... admitted=0                    <-- c2-clone-vac1501.txt
```
The same +1 bound is used for every locator in clause c and clause d (`plines`), so a row anchor or quote locator at
`<last+1>` is accepted as "inside its line count". A quote there still fails on content; a chain step does not.
Fix: `len(blob.split("\n")) - (0 if not blob.endswith(b"\n") else 1)`.

## F3 — the POS control carries dead tool machinery and prose that assumes a tool it does not contain

`ctl/c2/build-control.py:259-300` defines `write_tool()` — a double that prints `MADO_TERM: … verdict=AGREE` from the
observed capture — and `main()` never calls it; its docstring still says "so the counter's 'the landed tool must
reproduce the receipt' path is exercised", which is the *pre-freeze* clause f that the L1 removed. `build_tree()` also
`os.makedirs(D/tools)`, leaving an empty, untracked directory. The POS entry's live paragraph still reads "and the
landed tool's verdict `MADO_TERM: …`" although the tree has no tool. No behaviour depends on it (`git ls-tree HEAD --
tools/mado-terminal.py` → 0 paths in `ctl` and in the freeze transplant, `trees.txt`), and tool-independence is proven
positively by `ec64c2c1`; but the dead function invites a later editor to wire it back and re-couple C2 to C1.
Fix in v2: delete `write_tool()` and `os.makedirs(tools)`, reword the POS entry to cite the receipt, not a tool verdict.

## F4 — cosmetic: the control's quote table has an unused ninth span

`build-control.py:125-141` maps nine spans, but the body formats only eight (`qb133` is never substituted), so the
control's own "quotes 9" log line overstates the entry's quotes; the counter's `clause=d quotes=8` is correct
(`c2-control-base.txt`). No clause is affected.

## What this does not establish

- No data commit exists; C1/C2 were scored on synthetic trees only, at the freeze and at BASE, never on landed data.
- F1 does not show the drafted entry fails: the drafts use the freeze pin names. It shows the *control* is base-specific
  and that a byte-identical alias flips clause e.
- The counters were run on this host's bash/find/awk/tr under bwrap; no second host was compared.
