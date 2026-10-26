# C1/C2 do-nothing and cheat controls — seat `ExecControls`, mado round 47 w1

Status: **complete for the seat's scope, stopped by the L1's freeze (`d7527d60`) mid-re-run**. Built: 15 C1
`tools/mado-terminal.py` candidates (1 positive + 14 controls), 7 C2 entry bundles (1 positive + 6 controls), the
`build-c1-controls.py` / `build-c2-controls.py` generators and `run-controls.py`. Scored: all 14 C1 controls and all 6
C2 controls + both positives, against counter snapshots whose sha256 are recorded below; the last snapshot re-run was
cut after four controls. Scratch (`/fast/scratch/hyaku/mado-r47/ExecControls`, 2.9 GB) deleted at the stop.

Target: the C1 counter draft (`ExecCounterC1/c1-r47-terminal.py`, `--repo/--rev/--work/--nonce/--fixtures`) and the
C2 counter draft (`ExecCounterC2/c2-r47-terminal-entry.py`, `--repo/--rev/--base`). Both drafts were **still being
edited by their seats while this suite ran**, so every score below is tied to a snapshot copied into `snap/` and hashed:

| snapshot | sha256 | mtime |
|---|---|---|
| `snap/c1-r47-terminal.py` | `7b1572056db0fe65a14ceb7e3b27b730f29363fc68d36427c84212dae94bc10a` | 2026-10-26 19:27:25 |
| `snap/c2-r47-terminal-entry.py` | `69c121489b0d816c0befb91bf66da62be262bd5064f371ae13e5033e65e77dbd` | 2026-10-26 19:27:25 |
| `snap/fixtures-placeholder.json` | `0bee088db5bb41cacac08feed9b739608c96775c93166695df9a0697c1f00a4c` | 2026-10-26 18:48:21 |

Base `60edb66e2f1cb90acc6e9442fc93ded0ca42d750`. Nothing in the lane was written by this seat; every control was committed on
its own `git clone --shared --no-checkout` of the lane under `/fast/scratch/hyaku/mado-r47/ExecControls/`, with
`git rev-parse --show-toplevel` asserted before the first commit. Scratch deleted at exit.

## What is here

| path | what it is |
|---|---|
| `c1-base.py` | the control base: a stdlib, process-free re-implementation of the v0.14.3 print-mode selection, with one `MODE` switch per cheat (also the source of the positive control `REF-MINI`) |
| `build-c1-controls.py`, `c1/*.py` | 15 `tools/mado-terminal.py` candidates (`REF-MINI` + 14 controls); each file is standalone and honour `TMPDIR` |
| `build-c2-controls.py`, `c2/<NAME>/` | 7 entry bundles (`files/` = full-file replacements, `expect`, `note`) |
| `run-controls.py` | the runner: `--counter C --work DIR [--claim C1\|C2]`, prints `CTL_C1 <name> <verdict>` lines and the one-line verdict |
| `pins/` | the pinned script and README copies the C2 control uses, `SHA256SUMS`, `PROVENANCE.txt` |
| `receipts/` | counter stdout per control, the C2 suite log, the live observation |

Runner output shape (exactly as specified):

```
CTL_C1 <name> TARGET_MET|TARGET_MISSED|SETUP_FAIL
CTL_C1 VERDICT: PASS|FAIL (controls scoring TARGET_MET: k of n; reference met: 0|1)
```

`PASS` requires every cheat control rejected, the reference admitted, and no setup failure. The runner only passes the
options the counter's `--help` advertises (the C2 counter has no `--work`), so the same command works for both claims.

## C1 — the 14 controls, their oracle agreement, and the clause that must reject them

"oracle agreement" is my own differential measurement: 60 generated cases from my harness, the control's `print` stdout
and rc compared with `/usr/bin/xdg-terminal-exec` run on the same materialized case (fresh `XDG_CACHE_HOME`, print modes
only). It is not the counter; it shows why each control needs the clause named.

| control | what it does instead of acquiring the capability | agree | execve / socket | clause that must reject it, and why |
|---|---|---|---|---|
| `REF-MINI` | models the chain (positive control) | 60/60 | 1 / 0 | none — it is the reference |
| `STUB` | exit 0, prints nothing, tests nothing | 0/60 | 1 / 0 | **s** (no `MADO_TERMINAL_SELFTEST:` line) and **f, g** (empty stdout on every case) |
| `CONST` | always prints the host answer `Alacritty.desktop` + `$XDG_DATA_HOME/applications/Alacritty.desktop` + `alacritty` | 0/60 | 1 / 0 | **f**: the path is root-dependent in every case, so only a `--print-id`-only host-shaped fixture could agree; **g** for the same reason |
| `DELEGATE` | `os.execv("/usr/bin/xdg-terminal-exec", …)` | 60/60 | 7 calls / 5 ok, 7 sockets | **r only** — byte-identical to the oracle; the fake binding over `/usr/bin/xdg-terminal-exec` and the `execve` count are the separation |
| `SUBPROC` | `subprocess.run` of the pinned script | 60/60 | 7 / 5 ok, 7 sockets | **r only**, same reason |
| `EMBED-SH` | the script's bytes embedded (base64) and run by `/bin/sh` | 60/60 | 7 / 5 ok, 7 sockets | **r only** — a second `execve` for `/bin/sh`, and the fake `sh`/`bash`/`dash` bindings fire |
| `CTYPES-EXEC` | `execve(2)` through libc via `ctypes` | 60/60 | 7 / 5 ok, 7 sockets | **r only** — proves clause r traces the syscall, not the Python API |
| `FIRSTLINE` | first entry line of the first list file, no validation, no fallback | 31/60 | 1 / 0 | **f** on the fixtures where that line is Hidden / not a TerminalEmulator / has no executable / carries an action; **g** |
| `NOVALIDATE` | full chain but Hidden / TryExec / Categories / OnlyShowIn / NotShowIn unchecked | 27/60 | 1 / 0 | **f, g** (each rejection rule has fixtures) |
| `NODESKTOP` | ignores `${desktop}-xdg-terminals.list` | 58/60 | 1 / 0 | **f, g** — but only the cases where the desktop-prefixed file changes the answer discriminate |
| `REVERSED-DIRS` | application data dirs searched in reverse preference | 40/60 | 1 / 0 | **f, g** (duplicate-id-across-dirs fixtures) |
| `CACHE-READ` | prints the host resolver cache instead of resolving | 34/60 | 1 / 0 | **f, g** — with `XDG_CACHE_HOME` in a fresh directory there is no cache, so it prints nothing and exits 1 |
| `SELFTEST-LIE` | `MADO_TERMINAL_SELFTEST: 40/40 passed`, no test at all; print side is STUB | 0/60 | 1 / 0 | **s passes by construction**, **f, g** reject: the counter must not let the tool's own self-report carry the claim |
| `FIXTURE-READ` | replays the counter's own fixture JSON (env, `<repo>/quality/counters/`, cwd) | 0/60 | 1 / 0 | **i** (the repository is not visible in the allowlist sandbox → nothing to replay), then f/g |
| `TYPE-CHECK` | rejects an entry whose `Type` is not `Application` — a rule the script never reads | 58/60 | 1 / 0 | **f, g** — an over-validating tool must fail on the cases whose `Type` is not `Application` |

Two axes the prose cannot carry are visible in the "agree" column: `NODESKTOP` (58/60) and `TYPE-CHECK` (58/60) are
wrong on only 2 of 60 random cases. A frozen fixture set that never disagrees between a desktop-prefixed list and its
plain sibling, and that never gives an entry a `Type` other than `Application`, leaves those two to clause g alone.

## C1 — what the counter draft actually did with each control

Scored on one clone per control (`receipts/out-<name>.txt`). The L1 froze its own control set (commit `d7527d60`,
`.ufo/waves/round-47/ctl/`) while this suite was re-running on the 19:27 snapshot, so the record is in three parts and
each is dated:

| control | counter verdict | receipt | note |
|---|---|---|---|
| `STUB` | `TARGET_MISSED` | `receipts/out-STUB.txt` (19:04 vintage) | `clause=s` no selftest line; f/g |
| `CONST` | `TARGET_MISSED` | `receipts/out-CONST.txt` | f on every `--print-path`; g |
| `DELEGATE` | `TARGET_MISSED` | `receipts/out-DELEGATE.txt` | `clause=r` trips; f also fails once the fake `/usr/bin/xdg-terminal-exec` answers |
| `SUBPROC` | `TARGET_MISSED` | `receipts/out-SUBPROC.txt` | same |
| `EMBED-SH` | `TARGET_MISSED` | `receipts/out-EMBED-SH.txt` | `clause=r` (second execve, fake shell) |
| `CTYPES-EXEC` | `TARGET_MISSED` | `receipts/out-CTYPES-EXEC.txt` | `clause=r` on the raw syscall |
| `FIRSTLINE` | `TARGET_MISSED` | `receipts/out-FIRSTLINE.txt` | f/g |
| `NOVALIDATE` | `TARGET_MISSED` | `receipts/out-NOVALIDATE.txt` | f/g |
| `NODESKTOP` | `TARGET_MISSED` | `receipts/out-NODESKTOP.txt` | f/g |
| `REVERSED-DIRS` | `TARGET_MISSED` | `receipts/out-REVERSED-DIRS.txt` | f/g |
| `CACHE-READ` | `TARGET_MISSED` | `receipts/out-CACHE-READ.txt` | cold cache: nothing to read |
| `SELFTEST-LIE` | `TARGET_MISSED` | `receipts/out-SELFTEST-LIE.txt` | s passes, f/g reject |
| `FIXTURE-READ` | `TARGET_MISSED` | `receipts/out-FIXTURE-READ.txt` | clause i: the counter's fixtures are not visible |
| `TYPE-CHECK` | `TARGET_MISSED` | `receipts/out-TYPE-CHECK.txt` | f/g on the non-Application-Type cases |
| `REF-MINI` (positive) | `TARGET_MET` at the 19:04 draft; `TARGET_MISSED` at the 19:23 draft (F6); `MISSED` only on the transient run-D normalisation | `receipts/out-REFERENCE.txt` | 128/128 fixtures, 150/150 generated, `selftest=ok readonly=ok` at 19:04 |

The full suite log of the 19:04–19:28 run is `receipts/c1-run-controls-1904.txt`:
`CTL_C1 VERDICT: FAIL (controls scoring TARGET_MET: 0 of 14; reference met: 0)` — the FAIL is entirely the reference
line, i.e. F6, not a control. The snapshot re-run (same runner, `snap/c1-r47-terminal.py`) completed four controls
before the L1's stop message: `STUB CONST DELEGATE SUBPROC` all `TARGET_MISSED`
(`receipts/snapshot-run/`), consistent with the 19:04 table. Independent direct runs: the L1's own draft
`.ufo/waves/round-47/l1-draft/mado-terminal.py` (sha256 `d130a372890476ff3184901d091d168670e4344ce9fe0c2bf87079647b89236c`)
scored `fixtures=128/128 generated=150/150 selftest=ok readonly=ok verdict=TARGET_MET` against the 19:12 draft, so the
counter admitted the real implementation before the freeze.

## What this seat built that the frozen set does not have

Frozen C1 set (`receipts/ctl-c1.txt`): BASE CONST CTYPES-EXECVE DELEGATE-SH EMBED-EXECV EXIT1 EXPLAIN-ALWAYS-AGREE
EXPLAIN-CANNED REF SOCKET-AND-REF STUB SUBPROC-EMBED VERDICT V-CATEGORIES-EXACT V-FALLBACK-APPEND V-FIRST-PATH-WINS
V-HIDDEN-ANYCASE V-LASTLINE-READ V-NO-ALIASES V-NO-BUILTINS V-NO-CARRYOVER V-NO-DESKTOP-LISTS V-NO-EXCLUSION
V-NO-LOOPSTATUS V-NO-LOWER V-NO-PATH-FOLD V-NO-PRINTF-C V-READSPLIT-NOSTRIP V-SHOWIN-ALWAYS V-STRIP-FAIL-EMPATHIES.

- **`CACHE-READ`** (prints `$XDG_CACHE_HOME/xdg-terminal-exec` instead of resolving) — the frozen set has no
  cache-reading control, and the 19:23 draft added run D (forge the cache, the tool must ignore it) precisely for it.
  Recommend adding it: it is the only control that fails run D and nothing else.
- **`FIXTURE-READ`** (replays the counter's own fixture JSON, matched by args and env) — no memorize/replay control in
  the frozen set; it is the control that tests clause i's repo invisibility.
- **`SELFTEST-LIE`** (`MADO_TERMINAL_SELFTEST: 40/40 passed`, nothing tested; print side stub) — the frozen set has STUB
  and EXIT1, none that passes `s` and fails everything else; this is the control that shows `s` is free.
- **`TYPE-CHECK`** (rejects a non-`Application` `Type`, which v0.14.3 never reads) — the frozen set is all
  under-validation mutants; the only over-validation trap is missing.
- **`FIRSTLINE`** (first list line, no validation, no fallback) — `V-FIRST-PATH-WINS` flips duplicate resolution, a
  different axis.
- **`REVERSED-DIRS`** (application data dirs in reverse order) — `V-FIRST-PATH-WINS` is the duplicate-resolution flip,
  not the directory order.

Frozen C2 set (`receipts/ctl-c2/`): base branch held nosha nosteps observed pin quote range receipt. My C2 bundle set
adds **`EMPTY`** (zero-byte entry with rows, pins, README row and receipt present — it fails b/e/f/i, so it separates
"artifact absent" from "artifact present but hollow"), and **`REF`** is the positive control that made clause f's
tool-reproduction path run (frozen C2 receipts report negatives only). Frozen C2 has three properties mine does not:
`held` (held rows edited), `observed` (capture/selected mismatch) and `nosha` (row without a digest).



## C2 — the 6 controls and the clause the counter draft actually rejected them on

Each control is `REF` with exactly one property broken. Scored by the counter draft at
`--rev HEAD --base 60edb66…` on its own clone (`receipts/out-<name>.txt`).

| control | broken property | expect | clause the draft reported | reference |
|---|---|---|---|---|
| `REF` | none (minimal valid entry) | TARGET_MET | `clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 admitted=1` | `receipts/out-REFERENCE.txt` |
| `BASE` | no entry at the revision | MISSED | `clause=a entry_absent` | `receipts/out-BASE.txt` |
| `EMPTY` | entry exists with zero bytes; rows, pins, README row and receipt present | MISSED | `a:1 b:0 … e:0 f:0 … i:0` (the head, the chain and the receipt line are gone) | `receipts/out-EMPTY.txt` |
| `FORGED-QUOTE` | one step's span is plausible prose that is not in the pin | MISSED | `clause=d quote_not_in_pin line=17` — d:0, everything else 1 | `receipts/out-FORGED-QUOTE.txt` |
| `BRANCH-URL` | both rows anchor at `…/main/…` instead of `…/v0.14.3/…` | MISSED | `clause=c id=S326 url_branch_ref:` and `id=S327 …` — c:0, everything else 1 | `receipts/out-BRANCH-URL.txt` |
| `INDEX-NOT-CHAIN` | same rows and locators as a citation table, zero numbered steps | MISSED | `clause=e steps=0 <6` — e:0, everything else 1 | `receipts/out-INDEX-NOT-CHAIN.txt` |
| `RECEIPT-ABSENT` | the round-17 answer cites a receipt that is not committed | MISSED | `clause=f receipt_missing=…` / `no_receipt_bound_to_tool` — f:0, everything else 1 | `receipts/out-RECEIPT-ABSENT.txt` |

C2 was scored against the 19:27 snapshot (`snap/c2-r47-terminal-entry.py`, sha256 `69c12148…`); receipts are
`receipts/out-*.txt` from the pre-freeze run and `receipts/snapshot-run/` for the C1 snapshot re-run.

Suite verdict (`receipts/c2-run-controls.txt`):
`CTL_C2 VERDICT: PASS (controls scoring TARGET_MET: 0 of 6; reference met: 1)`.

Two properties of the C2 draft that the controls pinned down, worth freezing deliberately:

- **Clause f is the only clause that binds prose to the tool.** It re-runs the landed `tools/mado-terminal.py explain
  --observed <capture>` under the receipt's `XDG_*` environment and requires `verdict=AGREE` with the receipt's
  `selected=`/`path=`. `RECEIPT-ABSENT` is the control that fails only there. The receipt format is line-oriented —
  `observed=<repo-relative path>`, one `XDG_NAME=value` per line, exactly one `MADO_TERM:` line — so a receipt that
  records its environment on a single prose line is not read as environment at all (my first receipt draft did this and
  clause f would have called it `env_lines=0`).
- **Clause i is a term census and is cheap.** It asks only that four terms (`read_config_paths`, `check_entry_key`,
  `find_entry_paths`, `print-delimiter`) are absent at BASE under `corpus/` and at least two appear at REV. My
  `INDEX-NOT-CHAIN` first failed d and i as well, purely because the table edition dropped the readings that carried the
  terms; after I kept the readings in the table it fails e alone. The counter declares this residual itself.

## The round-17 unknown, answered for the selection stage

The C2 positive control carries a real live observation, produced read-only this round (no terminal launched, no
compositor verb, cache redirected):

- `xdg-terminal-exec --print-id --print-path --print-cmd` under `XDG_CURRENT_DESKTOP=Hyprland`,
  `XDG_CONFIG_HOME=/home/vgpnk/.config`, `XDG_CONFIG_DIRS=/etc/xdg`, `XDG_DATA_HOME=/home/vgpnk/.local/share`,
  `XDG_DATA_DIRS=/usr/local/share:/usr/share`, `XDG_CACHE_HOME=<scratch, empty>` prints
  `Alacritty.desktop`, `/home/vgpnk/.local/share/applications/Alacritty.desktop`, `alacritty`, rc 0 — the three values
  the L1's host facts record.
- `mado-terminal.py explain --observed <that capture>` reports
  `MADO_TERM: selected=Alacritty.desktop path=/home/vgpnk/.local/share/applications/Alacritty.desktop verdict=AGREE`.

So the resolver picks the user override entry over the system one at the **selection** stage — that is the round-17
`[UNK]` (`corpus/knowledge/terminal-route-r17.md:144-145`) answered for selection, not for launch. The receipt
(`receipts/live-observation-raw.txt`, and the control's `c2/REF/files/.ufo/waves/round-47/receipts/xdg-terminal-live.txt`)
says exactly that much and no more.

## Findings for the freeze

**F1 — clause r is the whole separation for four byte-perfect cheats.** `DELEGATE`, `SUBPROC`, `EMBED-SH` and
`CTYPES-EXEC` agree with the oracle on 60/60 generated cases: stdout and exit status cannot tell them from an
implementation. Only the `execve` count (7 calls, 5 successful, versus 1 for a pure-Python tool) and the fake
`xdg-terminal-exec`/shell bindings catch them. If clause r is weakened in the freeze — "no socket" only, or a count of
`execve` of the *script* name rather than of all execs — all four become `TARGET_MET`.

**F2 — clause s is free to every control.** Every control in the suite can print `MADO_TERMINAL_SELFTEST: N/N passed`
without testing anything (`SELFTEST-LIE` does exactly that, `s` passes, `f`/`g` reject it). The near-correct controls'
selftests are deliberately self-referential (they check their own chain on a valid case), so a 30/30 selftest is not
evidence of the contract; the freeze should keep s as a shape check only and never as an admission reason.

**F3 — the generated clause carries the near-misses, and it caught a real bug.** Before this seat fixed it, `REF-MINI`
scored `fixtures=128/128 generated=148/150`: two generated cases with an entry in a subdirectory
(`applications/nested/deep.desktop`) exposed that v0.14.3's print-path compaction is
`${P%%/./*}/${P##*/./}` — prefix before the **first** `/./`, tail after the **last** — not a single split. The placeholder
fixture set never disagreed there. That is clause g doing the work the fixtures do not; both the frozen generator and an
implementation must carry the nested case.

**F4 — cold cache and repo invisibility both hold in the draft.** `CACHE-READ` finds nothing (it models the host cache,
which the counter does not expose) and `FIXTURE-READ` cannot read `quality/counters/c1-r47-fixtures.json` from inside the
allowlist sandbox. Both are the isolation clauses doing what they claim.

**F5 — over-validation is a real failure mode, not a hypothetical.** `TYPE-CHECK` reads `Type=` the way the desktop-entry
specification suggests and the way several editors describe the resolver; the pinned script never reads `Type` (only
`/usr/bin/find -type f`). It agrees on 58/60 random cases and must be rejected by the fixtures that carry a non-Application
`Type`. The knowledge entry that promises an `explain` trace listing "wrong Type" (the C1 claim text) should not: that
rejection never happens in v0.14.3.

**F6 — a counter edit in the middle of a scoring run can fail a correct tool (evidence: `receipts/out-REFERENCE.txt`,
vintage 19:23).** `REF-MINI` scored `TARGET_MET` against the 19:04 draft (`fixtures=128/128 generated=150/150`) and
`TARGET_MISSED` (`fixtures=53/128 forged_cache_runs=75/128`) against the 19:23 draft, whose new run D compared the
normalized *oracle* answer with the tool's *raw* stdout (`out='/fast/…/job-cache-…/home/…'` against
`'$ROOT/home/…'`). The 19:27 snapshot normalizes both sides (my instrumented copy of the draft printed
`normed='$ROOT/home/.local/share/applications/Alacritty.desktop\n'` for the same call), so the window was short — but a
frozen counter must not be scored while it is being written, and the freeze should record the counter sha in the
registration. This seat re-ran the whole suite on one snapshot for that reason.

**F7 — the fixture set and the counter draft currently disagree (cross-seat, for the L1).** The fixture seat's
`.ufo/waves/round-47/w1/ExecFixtures/fixtures.json` (147 entries) is rejected by the C1 counter draft as a **setup
error**:

```
PRED-C1-r47: SETUP fixture bb1-directory-named-desktop file path escapes the case root: 'home/.local/share/applications/weird.desktop/'
```

The fixture names a directory (trailing `/`, a real `find -L` shape: a directory literally named `*.desktop`), the
counter's path validator refuses it (`rel_ok`, `snap/c1-r47-terminal.py:262`). Re-checked at the snapshot sha: same
setup error. This suite therefore ran against the counter's own `ExecCounterC1/fixtures-placeholder.json` (128 entries,
`fixtures=128/128`). The fixture file (`ExecFixtures/fixtures.json`, mtime 18:58) and the counter (mtime 19:27) were not
reconciled by the time this seat finished. One of the two must move before freeze; if
the counter is right, the fixture's case is out of the contract; if the fixture is right, a directory named
`weird.desktop` is exactly the kind of case that separates `find -L` from a naive reader.

**F8 — the runner needs `--fixtures` until the counter's default exists.** The C1 counter's default fixture path is
`c1-r47-fixtures.json` beside the counter, which the draft does not carry yet; `run-controls.py` forwards extra counter
arguments, so the invocation is
`--counter-arg=--fixtures --counter-arg=<path>` (the `=` form: argparse will not take a value starting with `--`).

## Runs (scratch, deleted at exit; counter stdout kept in `receipts/`)

```
# C2, both directions, against the draft:
python3 run-controls.py --counter .../ExecCounterC2/c2-r47-terminal-entry.py --work <scratch>/w-c2 --claim C2

# C1, both directions (15 controls, reference last):
python3 run-controls.py --counter .../ExecCounterC1/c1-r47-terminal.py --work <scratch>/w-c1 --claim C1 \
        --counter-arg=--fixtures --counter-arg=.../ExecCounterC1/fixtures-placeholder.json
```

Every control is one commit on its own clone (`git clone --shared --no-checkout` of the lane at base, `--detach` to the
base, control at `tools/mado-terminal.py` or the bundle's files, `-c user.name=controls-seat
-c user.email=controls@scratch.invalid commit`). The runner deletes each clone unless `--keep`.

## Residual risks

- The controls show what *this* counter draft rejects; they cannot show that the frozen counter keeps rejecting them.
  `c1/*.py` and `c2/*/` are the artifacts to re-score after the freeze, with the same runner.
- `REF-MINI` is a second implementation of the same contract written by this seat; that it and the L1 draft
  (`l1-draft/mado-terminal.py`, sha256 `d130a372…`) both score `TARGET_MET` is two passes of one counter, not independence
  from it.
- The oracle agreement column is 60 cases per control; it is a discriminator census, not a proof about the tool.
- The C2 positive control is minimal on purpose: one script pin and one README pin, one new pair of rows. The real entry
  (other seats) will cite more rows; the controls' value is the clause attribution, not the entry text.
