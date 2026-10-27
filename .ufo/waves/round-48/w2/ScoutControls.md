# ScoutControls — w2 (FALSIFY): inventory of w1 C1/C2 controls vs registration's mandatory list

Seat `ScoutControls`, wave w2, round 48, policy v1. Leaf seat; nothing outside
`.ufo/waves/round-48/w2/ScoutControls/` and `/fast/scratch/hyaku/mado-r48/ScoutControls/` was written.
Freeze under attack: lane commit `3e6c848a0e1bbc9c7058226b86d0faefc5351c9d`
("round-48: freeze v1 - registration, counters c1-r48/c2-r48 + warm fixtures, XKB pins+receipt,
w1 evidence (41 seats), controls, L1 reference + drafts").

**Axes named.** (1) *Coverage*: does the w1 control set match the registration's mandatory list, and
was each control re-scored against the frozen instruments? (2) *Survivor resistance*: does any
skip/mutant control (or class) meet the frozen counter? (3) *Evidence integrity*: do the w1 reports
match their own outputs? (4) *Repairability*: is each defect fixable before data (L1 may re-register
pre-data) or a tradeoff the judge must reject?

## 1. Frozen instruments (what "frozen" means here)

| artifact | sha256 | note |
|---|---|---|
| `quality/counters/c1-r48-terminal-cache.py` | `2a7d03d96d6ea5489fecc110de8d29b83d6c3d2d6abd4e5d4138096d01ccddd4` | == `.ufo/waves/round-48/l1-draft/c1-r48-terminal-cache.py` |
| `quality/counters/c2-r48-xkb-entry.py` | `4a0e6924eada0d12c70b4ce6e681a118896b93532e280ea3c15cc148b794a9f1` | == `l1-draft/c2-r48-xkb-entry.py`; differs from w1 draft |
| `quality/counters/c1-r48-fixtures.json` (warm, 204) | `4d946bd7934d4afc40d16676a300a7a10ee077404a2d51e289d9db871cb311aa` | == counter's `SHA256_WARM` |
| `quality/counters/c1-r47-fixtures.json` (cold, 190) | `4836cc1d9e493af7bf15fa52f6e6855fe71c5c27911880847da668e1e313dd86` | == counter's `SHA256_COLD` |
| `.ufo/waves/round-47/fetch/xdg-terminal-exec` (C1 pin) | `89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac` | == registration |
| `registration.md` | `a3ac7e70a9e393c368bc327237c4dd3b6746cfaf235ef5667482bdb6f2fe6162` | v1 |
| `claims.md` | `cc01009bb4bf1c2e36920811bdfac3e496bcdbfcccea29f194dc0adf949591f8` | v1 |

Frozen C1 counter vs w1 draft (`.ufo/waves/round-48/w1/ExecCounterC1/c1-r48-terminal-cache.py`,
sha `8db736a7ed147cc6b7e5091f713d2e0cee781d435a9b69dee2a5433450207ed7`): `SELFTEST_MIN` 30→60;
`after` schema gains `modes`/`cache_lines`/`cache_sub`/`cache_append` (w1 finding F2 adopted);
strace trip parser hardened against bwrap attach noise (`???`/`<... resumed>` lines excluded);
`files_order` materialization (readdir determinism); pre-gate death now `cache=-` not `absent`.
Frozen C2 counter vs w1 draft (sha `1fb235b2a92ea024171652801429e636868ee1758c76a31d2cce929099c28941`):
**new clause `r`** (re-runs `xkbcli compile-keymap` positive + 3 negative probes, byte-compares
digest/rc) and a keymap-digest line filter in clause d/f extraction. Consequence: **every w1 C2
control was scored against a different instrument than the frozen one.**

## 2. C1 control inventory (registration: 20 controls, `reference.py` must meet, every skip/mutant must miss)

Registration's list maps 1:1 onto `.ufo/waves/round-48/w1/ExecControlsC1/controls/` (20 files,
sha256 in `w1/ExecControlsC1/receipts/artifact-hashes.txt`): base→`base.py`,
always-cold→`always-cold-but-home.py`, trust-any→`trust-any.py`, name-only→`hash-names.py`,
hash-no-date→`hash-no-date.py`, hash-no-total→`hash-no-total.py`, ignores-enable→`cache-ignores-enable.py`,
no-line-limit→`no-line-limit.py`, delegate-ls→`delegate-ls.py`, md5-subprocess→`md5-subproc.py`,
constant-cache-explain→`explain-cache-const.py`, constant-cmd-explain→`explain-cmd-const.py`,
writes-cache→`writes-cache.py`, desktop-lowercase→`mut-desktop-lower.py`,
command-v-omission→`mut-no-command-v.py`, cache-fallback→`mut-cache-fallback.py`,
EOF/terminator mutants→`mut-eof-terminator.py`+`mut-terminator-contains.py`,
warm-args→`mut-warm-ignores-args.py`, plus positive `reference.py`. **None missing.**

Evidence state per control (as found, before my runs):

* w1 local pin-judged loop, 23 fixtures (`receipts/<control>.txt`, all 20 + 6 refA mutants +
  `refA`): reference MEETS; all 19 skip/mutants MISS; `writes-cache` misses **only** via tree
  fingerprint (its clauses f=x=r=w=0 — the loop's trace cannot see the write; w1 finding F4).
* w1 draft-counter pass: **incomplete**. Only 8 controls have a draft verdict
  (`base`, `always-cold-but-home`, `cache-ignores-enable`, `delegate-ls`, `explain-cache-const`,
  `hash-names`, `hash-no-date`, `reference` — all TARGET_MISSED except reference TARGET_MET);
  `explain-cmd-const`'s draft section is a **crash traceback** (`FileNotFoundError` in
  `tempfile._mkstemp`, no verdict line); the other 11 were never reached ("cut" in
  `w1/ExecControlsC1.md`, consistent with the missing draft sections).
* L1 pre-freeze re-score against the frozen counter + merged 204-fixture set
  (`.ufo/waves/round-48/receipts/l1-c1-*.txt`): **only `base` and `reference`**.
  `l1-c1-base-final.txt` (`cb112888…`) TARGET_MISSED ✓; `l1-c1-ref-final.txt` (`4b748fcc…`)
  TARGET_MET ✓. The other **18 controls have no frozen-set re-score** — the registration's
  "20 controls must be re-scored against this frozen merged fixture set" is only 2/20 done.

My w2 re-scores (frozen counter, nonce 4848, scratch clone of freeze commit; recipe
`l1-draft/c1-score.sh`; harness copy in `receipts/score-one.sh`):

| control | frozen-counter verdict | receipt (sha256) |
|---|---|---|
| `always-cold-but-home` | TARGET_MISSED (warm=139/204, explained=231/394, selftest=fail) ✓ required | `receipts/frozen-score-alwayscold.txt` `d500b18b…` |
| `trust-any` | TARGET_MISSED (warm=184/204, explained=340/394, selftest=fail) ✓ required | `receipts/frozen-score-trustany.txt` `01f4daf9…` |
| `writes-cache` (committed bytes) | TARGET_MISSED (warm=197/204, explained=380/394, selftest=fail) — misses on 6 HOME-UNSET fixtures + `L1-10-desk-echo-n-edit` + 14 explain cases + 43/43 selftest; **readonly=ok, trips=0** | `receipts/frozen-score-writecache.txt` `f264e1d3…` |
| **writes-v2 probe** (see F1) | **TARGET_MET** — cold=190/190 warm=204/204 explained=394/394 generated=230/230 selftest=ok **readonly=ok** | `receipts/frozen-score-writesv2.txt` `b2d1d7d4…`, probe `receipts/writes-v2-probe.py` `dbe2bb73…` |

Note: every w1-era control byte fails frozen clause `s` on its own (selftest line reads 43/43 <
SELFTEST_MIN 60); the re-scores above still exercise f/w/x/g/r behavior past it.

## 3. C2 control inventory (registration: positive minimal-entry tree admits; named mutants reject)

`w1/ExecCounterC2/receipts/controls.txt` (sha `11a3be3d…`, full captured output) + `digests.txt`
(sha `dadfe06d…`) record **14 runs, all against the w1 draft counter** `1fb235b2…` (no clause r):
BASE rc=1 (a) · POS rc=0 admitted · QUOTE rc=1 (d) · RANGE rc=1 (d) · BRANCH rc=1 (c) · PIN rc=1
(c) · HELD rc=1 (h) · RECEIPT-absent rc=1 (f) · RECEIPT-contradicts rc=1 (f) · NOSTEPS rc=1 (e) ·
SETUP rc=2 (precondition) · POS-LIVE rc=0 admitted · LIVE-receipt-contradicts rc=1 (f) ·
LIVE-entry-disagrees rc=1 (f); POS-RENAME rc=0 admitted in `receipts/pos-rename.txt`. Every
intended-clause rejection lands on its clause (only PIN and HELD cascade into d/e, declared
intended in `w1/ExecCounterC2.md`).

Not-run / not-at-freeze items:

* **README and census mutants do not exist.** `registration.md` ("Before") names
  "base, quote/range/pin/receipt/held/steps/**README/census** mutants reject" in that order; the w1
  spec (`make-w1-spec.py` → ExecCounterC2 task) and `controls/build_controls.py` build no README-row
  or census-term mutant (`README_ROW` appears only in the POS build). Clauses g and i have positive
  coverage only.
* **No positive control was scored against the frozen C2 counter.** The freeze commit carries
  `receipts/l1-c2-before-base.txt` (`6c0cf68a…`, base → TARGET_MISSED, fails at clause a) but **no
  C2 positive receipt**, while the freeze checklist requires "C1 and C2 base/positive-control
  receipts". The frozen counter's added clause `r` has never been exercised by any schematic
  control. (Post-freeze w2 sibling `MutC2OneByte/receipts/M0_base_overlay.log` shows the frozen
  counter admitting the l1-draft data overlay incl. `clause=r replay=ok` — the instrument works,
  but that is w2 evidence, not a freeze artifact.)
* All 14 w1 runs predate the frozen counter's digest-filter change (lines 656-659), so even the
  rerun controls' clause-f parsing is unexercised on the frozen bytes.

## 4. Findings

**F1 (critical, pre-data hole — survivor).** The frozen C1 counter cannot see a tool that writes.
The tool tree's `.rw` is mounted `--ro-bind` for tool runs (`c1-r48-terminal-cache.py:279`), so a
`save_cache` attempt dies with EROFS; the trace set counts only
`execve|execveat|socket|socketpair|connect` (`:334`); no tree fingerprint before/after exists
(w1 finding F4's proposals were **not** adopted — verified by diff and by grep for
fingerprint/openat/tmpfs-empty checks). Proof: `writes-v2-probe.py`
(`dbe2bb73…`) = the L1 reference (which passes, `l1-c1-ref-final.txt`) plus a 10-line
`save_cache` model that opens `$XDG_CACHE_HOME/xdg-terminal-exec` for writing and swallows
`OSError`; scored against the frozen counter it returns
`cold=190/190 warm=204/204 explained=394/394 generated=230/230 selftest=ok readonly=ok
verdict=TARGET_MET` (`frozen-score-writesv2.txt`). Registration rule violated: "every skip/mutant
must miss, and a control that meets triggers a fixture/counter repair before freeze." The
committed `writes-cache.py` bytes miss for unrelated reasons (old selftest count, HOME-UNSET
deltas on the new merged fixtures), which masks the class survivor. **Smallest safe correction
(pre-data):** fingerprint the materialized tool tree (path,size,mtime) before/after every tool run
and fail the run on any delta, or add `openat` with `O_WRONLY|O_CREAT|O_TRUNC` to the traced set,
then re-score `writes-cache` (must MISS on the write clause). Do not narrow the predicate to
excuse the write: the contract says "writes nothing".

**F2 (coverage gap).** 18 of the 20 registration-mandated C1 controls lack a frozen-set re-score;
15 remain after my three. Their w1-era misses were measured on 23 local fixtures against the draft
counter; the merged set adds L1-*, v2-hu-*, v2-rd-*, v2-wi-*, v2-ws-* classes on which control
behavior is unverified (my three re-scores each failed on merged-set fixtures the 23-case set never
had). L1 must re-run the complete 20 against the frozen counter pre-data (registration explicitly
reserves this: "only before data may L1 re-register … and re-run the complete control set").

**F3 (freeze artifact gap, C2).** No C2 positive-control receipt at the freeze; clause r
unexercised by any control; README/census mutants named in the registration's reject list were
never built. Fixable pre-data: score the frozen counter on the POS tree (ExecCounterC2's scratch
revs are gone, but `receipts/pos-*.md|txt` hold the exact bytes — rebuild is ~30 lines per
`controls/build_controls.py`), add README-row and census-term mutants, and land the positive
receipt in `receipts/`.

**F4 (report-vs-output mismatches, minor).**
* `w1/ExecControlsC1.md`'s table shows `explain-cmd-const` draft = "MISSED (x)"; its receipt shows
  the draft pass **crashed** (traceback, no verdict). The local-loop MISS (x) is intact; the draft
  cell overstates.
* `receipts/l1-c1-ref-final3.txt` (`af58b0fd…`) records the reference MISSED once
  (`readonly=fail trips=2 ???( <detached …`) — bwrap strace attach noise; the frozen counter's
  hardened trip parser now ignores `???`/`<... resumed>` lines and counts only syscall names
  matching its anchored regex. `l1-c1-ref-final2.txt` passes. As retained, the receipt set both
  shows a false MISS of the mandatory-meeting control and documents the flake's repair; readers
  must take final/final2, not final3.
* Coverage note: w1 §5's `w4-id-path`, `w5-content`, `i8-disabled-env` proposals were adopted
  (`v2-wd-30-print-id-and-path`, `v2-ws-04-content-mut`, `v2-wi-18-cache-disabled-env`); the
  `w7-function-cmd` fixture (cached command = resolver's own `read_cache`, F6) was **not** — no
  frozen fixture mentions `read_cache`, so bash-`command -v`-vs-PATH separation rests on
  `mut-no-command-v` alone. Residual, not a registration violation.

## 5. Evidence index (all sha256)

| path | sha256 |
|---|---|
| `w2/ScoutControls/receipts/frozen-score-alwayscold.txt` | `d500b18b647339f6cb89bab2445fd1600eeda6b10d61d58b5ad4fcd6379f88e2` |
| `w2/ScoutControls/receipts/frozen-score-trustany.txt` | `01f4daf970ccd32bd7ec81849215f130cbf91fdcd57b104c5cd4538bbff9e7ad` |
| `w2/ScoutControls/receipts/frozen-score-writecache.txt` | `f264e1d3de53abdeb1736ea8fff8df8b176932209c6f8e8a236d19dd358bf699` |
| `w2/ScoutControls/receipts/frozen-score-writesv2.txt` | `b2d1d7d458a0550e902c34f4a84f84b1adeb8fa505a1ecfff996bf79c4855efc` |
| `w2/ScoutControls/receipts/writes-v2-probe.py` | `dbe2bb73389c53f945aed7715d1c7fd828fd8c306ccfb7471a9142e037115614` |
| `w2/ScoutControls/receipts/SHA256SUMS` | `48721213cb11b1063cff2822ea5d803ff8e6e7460d0c5e9ac7165ed2e35a0333` |
| `w1/ExecControlsC1.md` / `w1/ExecCounterC2.md` | `9612e410…` / `59180e27…` |
| `w1/ExecControlsC1/receipts/summary.txt` | `63cf46027a20f6e9a67a593df6b55398a209bd80de311e44bc527cc45a1cd973` |
| `w1/ExecCounterC2/receipts/controls.txt` / `digests.txt` | `11a3be3d…` / `dadfe06d…` |
| `receipts/l1-c1-base-final.txt` / `l1-c1-ref-final.txt` / `l1-c1-ref-final3.txt` / `l1-c2-before-base.txt` | `cb112888…` / `4b748fcc…` / `af58b0fd…` / `6c0cf68a…` |
| `receipts/census-before.txt` | `60a3fbbdcd4e641f347e154349506e87d2f55a9c023a0116a5744714039054bc` |

Method notes: re-scores cloned the lane at freeze commit `3e6c848a…` into
`/fast/scratch/hyaku/mado-r48/ScoutControls/<tag>` (`git clone --shared --no-checkout` + path
checkout of `tools quality/counters .ufo/waves/round-47/fetch` — full checkout trips the 1 MiB
file cap on legacy round fixtures), committed the control as `tools/mado-terminal.py`, and ran
`python3 -I quality/counters/c1-r48-terminal-cache.py --repo $D --rev HEAD --work $S/work --nonce 4848`.
Every scoring shell ran `ulimit -f 2048`; the initial temporary harness-file creation shell did
not set the limit before its small 811-byte write (no generated file exceeded 1 MiB). Largest
scoring output file: `frozen-score-alwayscold.txt` source `out.txt` 76,920 B; scratch peaked at
13 MB and was cleaned completely after receipts were copied to the seat dir. No installs, no
pacman, no lane/git mutation, no host changes.
