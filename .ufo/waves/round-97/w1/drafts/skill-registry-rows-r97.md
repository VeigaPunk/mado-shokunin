# SKILL.md registry rows for round 97 (draft)

Table shape (the registry's 8 columns, unchanged):

```
| name | gate/probe | entry command | verdict map | self-test command / spelling | pinned-value path | write scope | owner |
```

Rows are appended at the end of the registry table (after `mado-r95-selftest-kills` / the round-95
rows), in the order below. ASCII only; the existing rows keep their own characters.

## 0. What is already there at base (measured)

At base `e6152b58` the registry holds **one** of the four round-96 artifacts' rows:
`| mado-mimetext | probe | ...` (`SKILL.md` line 887, added by `5dd921b3`, the round-96 C1 landing).
The other three have zero rows:

```
git show HEAD:SKILL.md | grep -c "mado-mimetext"        # 1
git show HEAD:SKILL.md | grep -c "c1-r96-magictext"     # 0
git show HEAD:SKILL.md | grep -c "c2-r96-selftest-kills" # 0
git show HEAD:SKILL.md | grep -c "check-receipt-presence.json" # 0
```

So the C2 declaration's "0 -> 4 rows" is a `1 -> 4` move at this base (finding routed in the seat
report). Do not add a second `mado-mimetext` row; the three rows below plus the strength-row
amendment are what closes the gap.

## 1. The three missing round-96 rows

```
| mado-r96-magictext | gate | `python3 -I quality/counters/c1-r96-magictext.py --repo . --rev REV --base-rev 9f029f46f01f6cd3a1d29ac39bb548498a1d0c3d --cases .ufo/waves/round-96/controls/magictext-cases-r96-frozen.json --expect-cases-sha256 4b3645ae83f6bb1822ebdacd4e42c2dc0fdd152bdca8fc4ff558985052f1d565 --mutants .ufo/waves/round-96/controls/magictext-mutants-r96-frozen.json --expect-mutants-sha256 f8d461e8bd4d4d6a6f813bf63fc547e74cdf6c5f7a386c536d62633cb18b806a --oracle-src .ufo/waves/round-95/controls/mimesniff-oracle-r95.c --expect-oracle-sha256 99df35f8b3fd7005f30789f8866984a1bbceaff8dc6c1d326f0132eb7b4d124a --fresh-gen .ufo/waves/round-96/controls/magictext-fresh-r96.py --expect-fresh-gen-sha256 32d38edfb2cff57de3d89297ffaf1bd781d730b7be502fbfa62efa38de0815da --host-list .ufo/waves/round-95/controls/mimesniff-host-files-r95.txt --expect-host-list-sha256 9d5947a70d112796f39c3e309c5a25e5ff333b5ebeb51867ebe748af1135ba87 --host-db .ufo/waves/round-96/controls/host-text-db-r96.json --expect-host-db-sha256 9c411d2af41ac283fb7d229152f0b7b28b7854eabd057135a225762389d1ddd7 --expect-tool-sha256 d5f174fc33d0b1f1847897a8e63724c7112137c1bf58a89508d1c1c13b857cbd --expect-mimeglob-sha256 65f80a6cb1551bb722ae7608df04fb17deba1b5cd05bef6f7fdd79bed76e2453 --forgery .ufo/waves/round-96/controls/forgery-ctypes-r96.py --expect-forgery-sha256 06800cd141a18548c63701a44f9cab70e2c90f0f316fb6f24d0c06fca079fd97 --scratch-root DIR` (the round-96 declaration's command, verbatim; `--base-rev` and every pin are its cells) | 0 `MADO_MAGICTEXT_COUNT: TARGET_MET` (frozen cases exact over the 16 classes `header sect value mask word range indent order drop multi glob alias fallback zerosize mode desktop` with `classes == 16/16`, the fresh seeded leg exact, the host leg over the cache-free text copy, every mutant killed with a kill per class, each control behind, the selftest green); 1 `MADO_MAGICTEXT_COUNT: TARGET_MISSED`; 2 `MADO_MAGICTEXT_COUNT: SETUP_ERROR` (a pin mismatch is setup, never a miss); 3 `DRAFT` with `--draft-tool PATH` | `python3 -I quality/counters/c1-r96-magictext.py --selftest` (round 97, contract 3): its own checks over the committed fixtures under `.ufo/waves/round-97/selftest-fixtures/`, asserting per check an exit code and a stable finding id; prints `MADO_COUNTER_SELFTEST_FAIL: <id>` per failing check and `MADO_COUNTER_SELFTEST: checks=N failed=0` (N >= 6) on stdout, exit 0 green / 1 failed / 2 could-not-evaluate; its production path is byte-unchanged when `--selftest` is not given | the `--expect-*-sha256` values above (cases, mutants, oracle, fresh generator, host list, host db, tool, mimeglob, forgery), taken from `.ufo/waves/round-96/claims-declaration-r96.md` section C1 | caller-declared scratch only; git reads at `--rev`; extracted child runs under an audit-hook launcher with an empty `PATH` | mado |
```

```
| mado-r96-selftest-kills | gate | `python3 -I quality/counters/c2-r96-selftest-kills.py --repo . --rev REV --panel .ufo/waves/round-96/controls/selftest-panel-r96-frozen.json --expect-panel-sha256 4332b488309309b81eccccabaff9322c5b7a54fcedd74079b58f50926f773982 --expect-gate-sha256 2d6f1219fae19a85cc92f7d4103db396e1306fea74c2226bb068b335598da61b --expect-kills-sha256 305d735fd665ad87566c7983f4e9163eaf323ad1ddb7a99a907e507c8a617495 --control-kills .ufo/waves/round-96/build/check-receipt-presence-draft.kills.json --expect-control-sha256 0c233a47b9d0b855ed92991079399c1e6cf32848d4016081057c569ea3aed0c7 --r90-argv .ufo/waves/round-96/controls/r90-c2-argv-r96.json --expect-r90-argv-sha256 386a5a18f77bf6fa564f2a11498ef21f5c1e7ef461028a2956050d3af52ecda0 --scratch-root DIR` (the round-96 declaration's command, verbatim) | 0 `MADO_SELFTEST_KILLS: TARGET_MET` (the round-93 gate unchanged at its pinned sha; the kill-set pinned and bound to the tool's sha; the unmodified tool prints `OK` and its selftest is `checks=6` with the six declared labels; every neutralisation and hand weakening flagged; every neutral edit still `OK`; the do-nothing, always-`OK` and always-`WEAK` controls behind; a singleton kill per label; the gate's `--selftest` green; the round-90 leg `MADO_RECEIPT_PRESENCE: TARGET_MET` at `--rev`); 1 `MADO_SELFTEST_KILLS: TARGET_MISSED`; 2 `MADO_SELFTEST_KILLS: SETUP_ERROR` | `python3 -I quality/counters/c2-r96-selftest-kills.py --selftest` (round 97, contract 3): its own checks over the committed fixtures under `.ufo/waves/round-97/selftest-fixtures/`, asserting per check an exit code and a stable finding id; prints `MADO_COUNTER_SELFTEST_FAIL: <id>` per failing check and `MADO_COUNTER_SELFTEST: checks=N failed=0` (N >= 6), exit 0/1/2; its production path is byte-unchanged | the panel, the first-draft kill-set control and the round-90 argv file above, each sha-pinned; `quality/check-selftest-strength.py` at the round-93 sha `2d6f1219...da61b`; `quality/selftest-kills/check-receipt-presence.json` at `305d735f...617495` | caller scratch only; git reads at `--rev`; extracted child runs | mado |
```

```
| mado-receipt-presence-kills | gate | `python3 -I quality/check-selftest-strength.py --tool quality/check-receipt-presence.py --kills quality/selftest-kills/check-receipt-presence.json [--scratch-root DIR] [--timeout S] [--allow-sha-drift]` | 0 `SELFTEST_STRENGTH: OK ... kills=7 held=7 survived=0 wrong_check=0` (each of the 7 kill mutants fails exactly its named set of the 6 declared selftest checks); 1 `WEAK` with one `SURVIVED <id>` per surviving or mis-failing mutant; 2 setup error (unreadable tool or kill-set, a kill whose `find` does not occur exactly once in the non-selftest prefix, a selftest not green before mutation, a sha drift without `--allow-sha-drift`) | the gate's own `--selftest`: `python3 -I quality/check-selftest-strength.py --selftest`, which prints `SELFTEST_STRENGTH_SELFTEST: checks=11 failed=0` (measured at base); the data file declares `tool`, `tool_sha256`, `selftest_argv`, the two line prefixes, `selftest_checks=6` and 7 `kills` | `quality/selftest-kills/check-receipt-presence.json` (its `tool_sha256` must equal `quality/check-receipt-presence.py`'s sha at the measured revision; the round-96 C2 counter pins the file's sha) | read-only: git reads, a scratch copy of the tool per mutant; writes nothing in the repo | mado |
```

And amend `mado-selftest-strength`'s (TOOL, KILLSET) list: append

```
, (`quality/check-receipt-presence.py`, `quality/selftest-kills/check-receipt-presence.json`, 7 kills; round 96)
```

immediately after the `tools/mado-portals.py` entry (the list's last element), keeping the row's own
ellipsis character in the verdict cell untouched.

## 2. The round-97 rows

```
| mado-filetype | probe | `python3 -I tools/mado-filetype.py PATH... [--follow \| --nofollow] [--fast] [--data-home DIR \| --data-home-unset] [--data-dirs COLON_LIST \| --data-dirs-unset] [--home DIR \| --home-unset] [--json]` (needs `tools/mado-mimeglob.py`, `tools/mado-mimesniff.py` and `tools/mado-mimetext.py` beside it; loads them by pinned path) | 0 every path answered (`MADO_FILETYPE: <type> attr=<full\|fast> mode=<follow\|nofollow> path=<escaped>` per path, plus one `MADO_FILETYPE_DIRS: db=<cache\|text\|none>` line); 2 setup error (no PATH) and, per path, `MADO_FILETYPE: ERROR stat path=<escaped>` for a path whose `lstat` fails with an errno other than `EACCES` (the run exits 2; every other path is still printed) | `python3 -I tools/mado-filetype.py --selftest`; prints `MADO_FILETYPE_SELFTEST_FAIL: <label>` per failing check and `MADO_FILETYPE_SELFTEST: checks=N failed=0` (N >= 20) on stdout, exit 0/1 | `.ufo/waves/round-97/claims-declaration-r97.md` section C1 (the model and its named limits); frozen cases/mutants/fresh/host lists under `.ufo/waves/round-97/controls/`, sha-pinned by the C1 counter; oracle `/usr/bin/gio` sha256 `d216426080f847bfccdc7c735a4f349dc74f524530a19e8b1c32d04270cfc462` | read-only: `lstat`/`stat` on the named paths, `mime/` reads under the given roots, and one file open only when the sniff gate permits it; writes nothing | mado |
```

```
| mado-r97-filetype | gate | `python3 -I quality/counters/c1-r97-filetype.py --repo . --rev REV --base-rev e6152b589c2c6a28426c28263c4bcc3c46398be4 --cases .ufo/waves/round-97/controls/filetype-cases-r97-frozen.json --mutants .ufo/waves/round-97/controls/filetype-mutants-r97-frozen.json --genseed .ufo/waves/round-97/controls/filetype-fresh-r97.py --host-list .ufo/waves/round-97/controls/filetype-host-r97.txt --host-db .ufo/waves/round-97/controls/host-db-r97.json --expect-tool-sha256 ... --expect-mimeglob-sha256 ... --expect-mimesniff-sha256 ... --expect-mimetext-sha256 ... --expect-gio-sha256 d216426080f847bfccdc7c735a4f349dc74f524530a19e8b1c32d04270cfc462 --forgery .ufo/waves/round-97/controls/forgery-ctypes-r97.py --scratch-root DIR` (the remaining pins are the freeze block's) | 0 `TARGET_MET` for `pred=PRED-C1-r97-v1` (frozen cases exact over 15 classes with `classes == 15/15`, every mutant killed with a kill per class, the fresh seeded leg exact, the host leg exact, the oracle pinned, each control behind, and the candidate's selftest green); 1 `TARGET_MISSED`; 2 `SETUP_ERROR` (a pin mismatch is setup, never a miss). The counter prints one result line carrying `pred=PRED-C1-r97-v1`; its own token is fixed when the counter lands and the L1 pastes it into this cell | `python3 -I quality/counters/c1-r97-filetype.py --selftest` (contract 3): its own checks under `.ufo/waves/round-97/selftest-fixtures/`, asserting per check an exit code and a stable finding id; prints `MADO_COUNTER_SELFTEST_FAIL: <id>` per failing check and `MADO_COUNTER_SELFTEST: checks=N failed=0` (N >= 6), exit 0/1/2 | `.ufo/waves/round-97/claims-declaration-r97.md` (predicate, counting command, named limits); the six control files under `.ufo/waves/round-97/controls/`, each sha-pinned | caller-declared scratch only; git reads at `--rev`; extracted child runs under an audit-hook launcher | mado |
```

```
| mado-r97-counter-selftest | gate | `python3 -I quality/counters/c2-r97-counter-selftest.py --repo . --rev REV --panel .ufo/waves/round-97/controls/counter-selftest-panel-r97.json --expect-panel-sha256 ... --expect-c1-sha256 ... --expect-c2-sha256 ... --expect-registry-sha256 ... --expect-ledger-sha256 ... --scratch-root DIR` (the pins are the freeze block's) | 0 `TARGET_MET` for `pred=PRED-C2-r97-v1` (both round-96 counters green under `--selftest` with `checks >= 6`, every frozen neutralisation flagged with its declared id, every broken-input mode named with the declared id and exit, the base bytes refusing `--selftest`, an always-OK stub flagged, and the registry rows for the four artifacts re-derived from `SKILL.md`); 1 `TARGET_MISSED`; 2 `SETUP_ERROR`; the counter's own token and predicate string are pasted by the L1 when it lands | `python3 -I quality/counters/c2-r97-counter-selftest.py --selftest` (contract 3): its own checks, same spelling and exits as the row above | `.ufo/waves/round-97/claims-declaration-r97.md` section C2; the panel JSON under `.ufo/waves/round-97/controls/`, sha-pinned; `SKILL.md` and `quality/tool-ledger.md` pinned by the command | caller scratch only; git reads at `--rev`; extracted child runs | mado |
```

## 3. Gate-standard check for these rows

- **registry.** Each row names its instrument, kind, entry command, an exit -> verdict map, a
  self-test command with its exact spelling and result line, the pinned-value path, the write scope
  and the owner.
- **self-test.** All five rows that are gates expose a self-invocation mode that asserts an exit code
  and a stable id per check (contract 3 for the counters; the tool's own `--selftest` for
  `mado-filetype`; the gate's `--selftest` for the kill-set row).
- **pins.** Every row that reads a frozen file names it and its sha; the two round-97 rows take their
  remaining pins from the freeze block rather than restating guesses.
- **write scope.** Every row is read-only toward the host: git reads, scratch copies, and (for
  `mado-filetype`) one gated file open. No row writes configuration, a repo file or a PATH entry.
