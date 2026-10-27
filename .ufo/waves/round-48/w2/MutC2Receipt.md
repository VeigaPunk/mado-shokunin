# MutC2Receipt — w2 falsification: the xkbcli receipt and its expected digest

Seat MutC2Receipt (leaf). Wave w2 = FALSIFY, policy v1. Base `579f694b45c797a9c39761fdb4f9e0a1b71b3585`,
lane `/home/vgpnk/Projects/shokunin/mado-shokunin`. Frozen instrument
`quality/counters/c2-r48-xkb-entry.py` (`PRED-C2-r48`); frozen claims/registration at
`.ufo/waves/round-48/claims.md` and `registration.md`. Data candidate attacked:
`.ufo/waves/round-48/l1-draft/{xkb-keymap-compile-r48.md,rows-c2.md,readme-row.md}` plus
`.ufo/waves/round-48/receipts/xkbcli-compile-keymap-r48.txt`, `fetch/`, `tools/make-xkb-receipt.sh`.
No lane, registry, counter or entry file was edited; no Git/jj mutation outside the scratch replay tree;
no subagents; no package transactions.

Scratch: `/fast/scratch/hyaku/mado-r48/MutC2Receipt` (1.7 MB total, removed before return). Every writer
shell began with `ulimit -f 2048`; largest file produced was 115,635 B (a git blob under the scratch
`.git/objects`), largest seat-dir file 19,203 B (`harness.py`).

## Method

The lane contains committed fixtures larger than 1 MiB, so a checked-out clone is truncated by the
1 MiB/file guard (observed: `unable to write file … File too large`, checkout aborted). The replay tree
was therefore built **without a worktree**, by git plumbing only, with exactly the overlay
`l1-draft/c2-mirror.sh` describes:

1. `git clone -q --shared --no-checkout <lane> <scratch>/m`; asserted
   `git -C <scratch>/m rev-parse --absolute-git-dir` = `<scratch>/m/.git`.
2. Clean replay commit = base tree + `fetch/*` (13 pins), `receipts/xkbcli-compile-keymap-r48.txt`,
   `tools/make-xkb-receipt.sh`, `corpus/knowledge/xkb-keymap-compile-r48.md`, `rows-c2.md` inserted after
   `| S339 |` in `corpus/SOURCES.md`, `readme-row.md` after the r47 row in `corpus/README.md`. Built with
   `hash-object -w` + `mktree` + `commit-tree -p <base>` (no index, no checkout).
3. Each mutant = one further commit on the clean commit with only the entry blob and/or the receipt blob
   changed; exposed as `refs/mut/<id>`.
4. Counter run unmodified, exactly as registered, once per mutant:
   `TMPDIR=<scratch>/tmp/<id> python3 -I quality/counters/c2-r48-xkb-entry.py --repo <scratch>/m --rev refs/mut/<id>`.

Positive control (M00-clean): exit 0,
`clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 r:1 admitted=1`,
`clause=r replay=ok sha=efd487a39920 neg=(1,1,0) ver=1.13.2`. The draft as frozen admits; every mutant
below is a delta from that admitted baseline.

## Mutations run and verdicts

31 commits scored (clean + 30 mutants). `ADMIT` = counter exit 0 / `admitted=1/1`. Full logs:
`w2/MutC2Receipt/counter-<id>.txt`; exact changed bytes: `w2/MutC2Receipt/diff-<id>.txt`;
compact table: `w2/MutC2Receipt/verdicts.tsv`; raw run: `w2/MutC2Receipt/mutant-matrix.txt`.

### keymap digest

| id | mutation | verdict | first counter line |
|---|---|---|---|
| M03 | extra `keymap-body sha256 deadbeef…` line in the positive window; entry cites `deadbeef…`; real `host.keymap` line intact | **ADMIT** | `clauses=…f:1…r:1 admitted=1` |
| M04 | decoy planted as a second `<deadbeef…>  host.keymap` line **after** the real one; entry cites the decoy | **ADMIT** | `…r:1 admitted=1` |
| M27 | decoy `keymap-sha256 deadbeef…` added to the separate KcCGST positive window; entry cites the decoy | **ADMIT** | `…f:1…r:1 admitted=1` |
| M01 | receipt `host.keymap` digest last nibble 1→2, entry untouched | miss | `clause=r positive_replay_failed rc=0 sha=efd487a39920` |
| M02 | same digest change in receipt **and** entry | miss | `clause=r positive_replay_failed` |
| M05 | `host.keymap` line carries a wrong digest, true digest kept on another keymap line, entry keeps the true digest | miss | `clause=r positive_replay_failed` |
| M04b | decoy `<deadbeef…>  host.keymap` line **before** the real one, entry cites the decoy | miss | `clause=r positive_replay_failed` |
| M20 | the `<64hex>  host.keymap` line removed | miss | `clause=f receipt_no_keymap_sha` + `clause=r receipt_no_keymap_digest` |
| M17 | entry digest tail (last nibble) changed; 12-hex prefix kept | **ADMIT** | `…r:1 admitted=1` |
| M17c | entry digest keeps `efd487a39920` and all 52 remaining hex changed | **ADMIT** | `…r:1 admitted=1` |
| M17b | entry digest first 12 hex changed | miss | `clause=f entry_disagrees… sha=0` |
| M26 | entry cites the receipt's XDG-probe digest (a real hex64 in the receipt, outside every positive window) | miss | `clause=f entry_disagrees… sha=0` |

### positive command argv

| id | mutation | verdict |
|---|---|---|
| M06 | receipt's positive command gains `--model nope`; entry quotes the mutated argv | **ADMIT** |
| M07 | receipt's positive command gains `--variant ext`; entry quotes it | **ADMIT** |
| M25 | receipt's positive command gains `--model nope`; entry still quotes the plain command (receipt and entry contradict) | **ADMIT** |
| M08 | entry's quoted positive command changed to `--layout us`; receipt untouched | **ADMIT** |
| M21 | receipt's positive command changed to `--layout us`; entry and digest untouched | miss (`clause=f receipt_no_keymap_sha`: the digest-bearing window no longer names `br`) |

### one negative rc / rc drift

| id | mutation | verdict |
|---|---|---|
| M09 | unknown-layout probe `rc=1`→`rc=2` in the receipt | miss (`clause=f receipt_probe_bad=unknown layout(rc_values=[2])`) |
| M10 | same rc change in receipt and entry table | miss (`receipt_probe_bad`) |
| M11 | entry's `--layout zz` row rc 1→2 only | miss (`clause=f entry_disagrees… neg=[False,True,True]`) |
| M24 | unknown-variant probe `rc=1`→`rc=2` in the receipt | miss (`receipt_probe_bad=unknown variant(rc_values=[2])`) |
| M12 | a second `rc=0` added inside the unknown-layout window (drift toward a neighbour) | miss (`receipt_probe_bad=unknown layout(no_labeled_rc)`) |
| M18 | entry's `nope:nope` row rc 0→2 | miss (`entry_disagrees… neg=[True,True,False]`) |
| M19 | entry's positive sentence rc 0→2 | miss (`entry_disagrees… pos=0`) |

### diagnostic code

| id | mutation | verdict |
|---|---|---|
| M13 | `[XKB-595]`→`[XKB-596]` on the unknown-option line in both receipt blocks **and** the entry row | **ADMIT** |
| M14 | every `XKB-595` in the receipt (4) and the entry (5) renamed `XKB-596` | **ADMIT** |
| M22 | receipt option diagnostic `XKB-595`→`596`, entry still says `595` | **ADMIT** |
| M23 | entry row `XKB-595`→`596`, receipt still says `595` | **ADMIT** |

### version

| id | mutation | verdict |
|---|---|---|
| M15 | `libxkbcommon-1.13.2-1`→`1.13.3-1` in the receipt package line and the entry's two version sentences | **ADMIT** |
| M16 | receipt version→`1.13.3`, entry untouched | miss (`clause=f entry_disagrees… ver=0`) |

## Findings (admissions)

The clean draft is not itself false — it states the values the replay produces. What follows are
**pre-data holes in the frozen instrument**: falsified receipts/entries that `PRED-C2-r48` admits 1/1.
None of these was repaired or narrowed; the predicate and counters were left untouched.

**F1 (digest — the seat's core question). Replay binds bytes→digest for exactly one line, but the entry
may publish a digest replay never produced.** Clause r recomputes `sha256` of live stdout and compares it
to the **first** `^([0-9a-f]{64})\s+host\.keymap$` line (order-sensitive: decoy before → miss M04b,
decoy after → admit M04). Clause f, however, collects *every* 64-hex token appearing on any
`keymap`-naming line of any positive window and accepts the entry if it states any of them, with only the
first 12 hex compared. Consequence: a receipt carrying an extra unreplayed keymap digest (same window
M03, second `host.keymap` line M04, or the KcCGST window M27) plus an entry citing it admits 1/1 while the
replayed bytes prove only the real digest. So the counter does **not** enforce that "the digest the entry
publishes" is "the digest replay produced"; it trusts a digest that only the mutated receipt supplies.
Evidence: `counter-M03-decoy-digest-after.txt`, `counter-M04-decoy-as-hostkeymap-after.txt`,
`counter-M27-decoy-digest-kccgst-window.txt` (all `f:1 … r:1`), with the exact bytes in the matching
`diff-*.txt`.

**F2 (argv). The receipt's positive command line is decorative.** Clause r replays a hard-coded
`compile-keymap --layout br --options compose:caps`; clause f only needs some positive window to name
`br` and `compose:caps` with a single rc 0. Adding `--model nope` (M06, M25) or `--variant ext` (M07) to
the receipt's recorded command admits, although `--model nope` provably compiles a different keymap
(geometry `pc(pc104)`; the recorded digest cannot come from that command). M25 admits a receipt whose
command contradicts the entry quoting the plain command. Removing `br` (M21) is caught, so only the two
name tokens are bound, not the argv.

**F3 (entry's positive argv).** M08 changes the entry's quoted positive command to `--layout us` and still
admits: the check is satisfied by *any* line containing `br`, `compose:caps` and a lone rc 0 — the same
prose line also carries `kb_layout = br` / `kb_options = compose:caps`. The entry can therefore quote a
command that contradicts the receipt's command and be admitted.

**F4 (diagnostic code).** The option probe's id is accepted through the disjunction
`XKB-595 |- "Unrecognized RMLVO option"` anywhere in the receipt, and the entry's id is never compared
with it. Renaming to `XKB-596` — in the receipt only (M22), the entry only (M23), both (M13), or removing
`XKB-595` from the receipt entirely (M14) — admits 1/1, even though the live tool prints `XKB-595`.

**F5 (version).** The receipt's `libxkbcommon` version triple is checked for agreement with the entry
(M16 misses), never against the host. `1.13.3` in the receipt and entry (M15) admits while
`xkbcli --version` on this host prints `1.13.2`.

**F6 (12-hex digest prefix).** By the registered wording ("the digest (or its first >= 12 hex)"), the
entry's published digest is checked only in its first 12 hex: M17 (last nibble) and M17c (all 52 tail hex
wrong) admit; M17b (prefix changed) misses. The claim's headline evidence is a 64-hex digest of which 52
hex are unverified in the entry text.

## What correctly held (replay really does bind bytes)

- Any change to the `host.keymap` digest line fails clause r with `positive_replay_failed` — alone (M01),
  with the entry changed consistently (M02), or with the true digest moved to another keymap line (M05);
  the first-match ordering matters (M04b vs M04).
- Removing the `host.keymap` line fails f and r (M20).
- Probe exit statuses cannot drift: receipt change (M09, M24), entry change (M11, M18), both (M10), and an
  ambiguous double-rc window (M12, `no_labeled_rc`) all miss.
- Entry/receipt disagreement on version, digest prefix or rc misses (`entry_disagrees`, M16, M17b, M26,
  M18, M19).
- The receipt's replayed argv still has to name `br` + `compose:caps` in a digest-bearing window (M21).

## Risks / limits

- Mutant commits are run-local (commit-tree timestamps); the retained `diff-*.txt` plus `harness.py`
  reproduce each tree byte-exactly from the frozen lane inputs (base commit + the `l1-draft` overlay +
  `receipts/`, `fetch/`, `tools/`).
- Replay is host-bound: this run used `xkbcli 1.13.2` / `xkeyboard-config 2.48` and produced
  `neg=(1,1,0)`, `sha=efd487a39920…`. Changed package outputs remain a miss by design.
- I attacked only the receipt/digest binding of C2. Pin/quote/README/census clauses were not mutated
  here; clause c and d passed on every mutant, so no cross-clause interference was observed.
- These are admission-path defects, not a verdict that the C2 claim is false. Because data has not
  landed, the registration permits L1 to re-register a new version and re-run the full control set; the
  minimal bindings that would close F1-F6 (entry digest = the replayed `host.keymap` digest at full
  length and a single keymap digest line; clause r replaying the argv the receipt records; version
  compared to live `xkbcli --version`; per-probe diagnostic id compared to the receipt/live stderr;
  entry's quoted command compared to the receipt's) are stated as options only — nothing was changed.
- Blockers: none.

## Retained evidence (this seat dir)

`mutant-matrix.txt` (raw run), `verdicts.tsv` (31 rows), `counter-<id>.txt` (31 counter transcripts),
`diff-<id>.txt` (30 clean-vs-mutant diffs, two files each), `harness.py` (reproducer, identical to the
version executed from scratch).
