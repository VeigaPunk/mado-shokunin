# ExecToolLedger — is the live-state tool ledger true? (round 47, w2 falsify)

Target: considerthese proposal 2, object of review
`.ufo/waves/round-47/w1/ScrToolLedger/ledger.md`
(sha256 `91ec6bcb9119925bfa80b241b3fdeb4972c1b421a818be928f1579614d0376b6`, committed at
`9bddd6ac`; seat base `c24adef2`). Everything below was measured on the lane at `9bddd6ac`, read-only.

## 1. Bottom line

**The ledger's skeleton is sound and its content is not.**

- Sound, verified here: all 10 receipt paths exist at the base and at HEAD; every stated round equals the
  round in the receipt's own path (0 wrong); every one of the 8 `ok`/`stale` byte bindings re-derives from
  `sha256sum` (0 wrong); the declared status of all 14 §8 rows equals the derived one; the §9 pristine
  line and controls A and C reproduce exactly.
- Not sound: **10 of the 14 rows carry at least one statement a reader cannot verify as written** —
  4 rows have a substantive error (wrong "last live run", wrong absence, a failure recorded as a design
  outcome, a misnamed journal unit) and 6 rows have quote-only errors (a verdict fragment that is not in
  the receipt it is attributed to). Four rows are clean: `options`, `verify`, `action-plan`, `assessment`.
- The document's own headline — "*1 host-facing instrument with no live receipt at all: `mado-globals.py`*"
  — is false: a committed live run of that instrument exists (H2). Its own §9 demonstration prints a count
  that contradicts the seat's own receipt (H5). Its proposed criterion's checker cannot falsify the
  status it most needs to falsify, `none` (H6).

Counted answer to "how many rows are wrong": **10/14** (4 substantive + 6 quote-only). If only
substantive errors are counted: **4/14**.

## 2. What I checked, per row (the assignment's four steps)

1. **receipt path exists in git** — `git cat-file -e` at `c24adef2` and at `HEAD`, for all 10 receipt
   paths the tables name: 10/10 present at both.
2. **the round** — the round stated in the row (`· rNN ·`) against the round in the receipt's path:
   14/14 rows agree.
3. **the verdict text** — every fragment the row displays, tested verbatim against the locator the row
   names, then against the whole file: **8 of 21 fragments fail** (`receipts/quote-fidelity.txt`).
4. **`--selftest`** — run for all 14 instruments at HEAD (`receipts/selftests.txt`): 10 pass, 1 is
   checkout-dependent (red in a clone), 3 instruments have no selftest at all.

```
$ python3 -I .ufo/waves/round-47/w2/ExecToolLedger/check-rows.py --repo .
ROW	mado-eventq.py	.ufo/waves/round-38/receipts/eventq-live.txt	yes	yes	r38	r38	yes	ok	ok	ok	no-flag
...
ROWS=14 row-level-mismatch=0
$ python3 -I .ufo/waves/round-47/w2/ExecToolLedger/check-fragments.py --repo .
FRAGMENTS total=21 not_verbatim_at_locator=8
```

`check-rows.py` re-derives steps 1–3 for the *structure*; it prints `row-level-mismatch=0`, which is the
point: the ledger's arithmetic is right, and that is why none of the holes below were caught by it.

## 3. Row matrix

| # | instrument | receipt | round | byte binding | verdict text | substantive error | verdict |
|---|---|---|---|---|---|---|---|
| 1 | `mado-eventq.py` | ✓ | ✓ r38 | ok | **✗** | **✗ H1, H7** | **WRONG** |
| 2 | `mado-options.py` | ✓ | ✓ r40 | ok | ✓ | — | clean |
| 3 | `mado-globals.py` | none | — | — | — | **✗ H2** | **WRONG** |
| 4 | `mado-geometry.py` | ✓ | ✓ r44 | ok | **✗** | — | **WRONG (quote)** |
| 5 | `mado-monitors.py` | ✓ | ✓ r45 | ok | **✗** | **✗ H1** | **WRONG** |
| 6 | `mado-devices.py` | ✓ | ✓ r46 | ok | **✗** | — | **WRONG (quote)** |
| 7 | `mado-verify.sh` | ✓ | ✓ r12 | stale ✓ | ✓ | — | clean |
| 8 | `mado-tripwire.py` | ✓ | ✓ r19 | stale ✓ | **✗** | — | **WRONG (quote)** |
| 9 | `mado-binds.py` | ✓ | ✓ r25 | stale ✓ | **✗** | — | **WRONG (quote)** |
| 10 | `mado-anims.py` | ✓ | ✓ r26 | ok | **✗** | — | **WRONG (quote)** |
| 11 | `mado-wsrules.py` | ✓ | ✓ r27 | ok | **✗** | — | **WRONG (quote)** |
| 12 | `mado-action-plan.py` | none | — | — | ✓ (exercise) | — | clean |
| 13 | `mado-assessment.py` | none | — | — | ✓ (EXIT=0) | — | clean |
| 14 | `mado-evidence-audit.py` | none | — | — | **✗** | **✗ H4** | **WRONG** |

## 4. Holes

### H1 — "last live run" is wrong for two rows; the search rule never looks in `w1/` seat dirs

The ledger's §1 defines its own search as *"any committed file, narrowed by the tool's verdict token … or
by its own filename, then confirmed by reading the receipt's tool hash"*. Its absence receipt
(`.ufo/waves/round-47/w1/ScrToolLedger/receipts/absence.txt:17-41`) shows what it actually searched: four
directory shapes (`*/receipts/`, `*/evidence/`, `*/fetch/`, `.ufo/evidence/`). It never searched
`.ufo/waves/round-NN/w1/` or `w2/`, where the adversarial seats leave their live runs. Three committed
live runs live there.

**1a. `mado-monitors.py` — row says r45, a r46 live run at the *current bytes* exists.**

```
$ grep -n 'hyprctl monitors all -j |' .ufo/waves/round-46/w1/ExecW2Monitors/live-runs.txt
32:$ hyprctl monitors all -j | python3 -I mado-monitors-tip.py --monitors - --config ~/.config/hypr/monitors.conf
$ sed -n '2,3p;35p' .ufo/waves/round-46/w1/ExecW2Monitors/live-runs.txt
# blob 551eceefa1ad8d6b3aed2694dcfb68f816c2e48e ; sha256 of the extracted file:
2f007417ae9efa43c7c3e5bcf8e88710fb6cd6c856e49b4084c742a7ecff5609  mado-monitors-tip.py
MADO_MONITORS: lines=1 ... outputs=1 matched=1 unruled=0 agree=1 differ=0 ... verdict=OK
$ sha256sum tools/mado-monitors.py
2f007417ae9efa43c7c3e5bcf8e88710fb6cd6c856e49b4084c742a7ecff5609  tools/mado-monitors.py
$ git log -1 --format='%h %ad' --date=iso -- .ufo/waves/round-46/w1/ExecW2Monitors/live-runs.txt
7f793280 2026-10-26 18:16:50 -0300
```

The cited r45 receipt is timestamped `2026-10-26T16:46:59-03:00`
(`.ufo/waves/round-45/receipts/live-monitors-host-r45.txt:1`), so the r46 run is later and at the same
bytes: the row should read r46 and the verdict `OK` (which it is — the value is right, the pointer is not).

**1b. `mado-eventq.py` — row says r38, a r39 live census at the *same bytes* exists.**

```
$ sed -n '1,2p' .ufo/waves/round-39/w1/ExecEventqSnapshot/eventq-live-census.txt
# eventq-live-census.txt — census-only live snapshot, 2026-10-25
# tool_sha256=436f550e9939a783b7b95d154d099b788ad9daaed2282e19de89413e39371f24
$ sed -n '9p' .ufo/waves/round-39/w1/ExecEventqSnapshot.md
- Command: `python3 -I tools/mado-eventq.py --snapshot-out /tmp/eventq-live-census.txt` (lane cwd), exit 0. Live output: 2 clients …
$ sha256sum tools/mado-eventq.py
436f550e9939a783b7b95d154d099b788ad9daaed2282e19de89413e39371f24  tools/mado-eventq.py
```

The census header carries the tool's own sha; the verdict (`CLEAN`) is in the seat report at `:9`, not in
the snapshot file, which is why a token-grep (`MADO_EVENTQ:`) misses it — the seat's rule requires the
*filename* branch too, and the filename (`eventq-live-census.txt`) matches the `*eventq-live*` branch the
ledger itself names in §1.

### H2 — `mado-globals.py` is not "none": a committed live run of the instrument exists

The ledger's F1 and its §3 count say the instrument has **no live receipt at all**. It has one.

```
$ sed -n '1,11p;21p;89p' .ufo/waves/round-41/w1/ExecLiveHost/live-census.txt
MADO_GLOBALS live census — host receipt for C1 (round 41, wave w1, seat ExecLiveHost)
tool:            w1/ExecLiveHost/mado-globals.py (byte copy of .ufo/waves/round-41/c1/ctl-ref-tool.py.txt)
tool sha256:     61f101aed8897e43a3c4b1ce792d82a0acd29d73fbdb929f4279a57fdf3130f0
command form:    journalctl --user -u xdg-desktop-portal-hyprland --no-pager -o short-iso
B. RUN 1 OF `python3 -I mado-globals.py --live --diff`  (exit 0) — verbatim
MADO_GLOBALS: sessions=2 latest_pid=1952 interfaces=63 classes=… expected_missing=- verdict=OK
$ sha256sum tools/mado-globals.py
8db1334035962bf8623244570b7e58e3af8a9e2520dd8f83cd0434a8a9a49795  tools/mado-globals.py
```

Three identical `--live` runs (rc 0/0/0, `live-census.txt:16`), the real portal journal, the tool hash on
line 5. Under the ledger's own §1 rule this is a live receipt, and the correct row status is **`stale`**
(the receipt ran `61f101ae`, the file is `8db13340`) — the same class the ledger already applies to
`verify`, `tripwire` and `binds`.

The narrower reading the ledger never states — "*the delivered `tools/mado-globals.py` bytes were never run
live*" — is true (`git log -- tools/mado-globals.py` has exactly two touches, `07f26416` and `6fd22346`,
and neither file is `61f101ae`). So the sentence that is wrong is the *classification*, not the fact that
the current bytes lack a live run. As written ("no live receipt at all", "none"), a reader concludes no
live evidence exists anywhere, and the count in §3 ("**1** … with no live receipt at all") is wrong.

### H3 — 8 of 21 displayed verdict fragments are not in the receipts they name

`receipts/quote-fidelity.txt` (from `check-fragments.py`) tests every displayed fragment verbatim:

| row | displayed fragment | at its locator |
|---|---|---|
| eventq | `subscribers=2 overflow=0 write_fail=0 markers_observable=no` | absent from the file (`lagging=0 missing_client=-` intervenes) |
| geometry | `rules=1 clients=3 matched=0 differ=0` | absent (`float_rules=1 other=1 unsupported=0` … intervene) |
| monitors | `outputs=1 matched=1 agree=1 differ=0` | absent (`unruled=0` intervenes) |
| devices | `keyboards=10 agree=9 virtual=1 mice=4 mice_differ=0 differ=0` | absent (`differ=0 fallback=0` intervene) |
| tripwire | `live_probe 3, vcs_write 164` | absent, and the counts are on `:7`, not the `:6` the row locates |
| binds | `cases_pass=41/41 verdict=TARGET_MET` | absent at `:50` (`embed_hits=0` intervenes) |
| anims | `CASES 41/41` | **nowhere in the lane**; the receipt says `cases_pass=41/41 verdict=TARGET_MET` at `:51` |
| wsrules | `cases_pass=41/41 TARGET_MET` | absent (`verdict=` intervenes) |

`grep -rn 'CASES 41/41' .ufo corpus` returns the ledger line itself and nothing else — the token is
invented. The other seven are compressions: every token is true, the string as printed is not in the
receipt. The ledger's closing claim — "*Each quoted fragment in this file was checked against its source
line by `receipts/verify-quotes.txt` (`QUOTES total=20 missing=0`)*" — is therefore false for the text the
reader sees: `verify-quotes.txt:2-6` certifies *different* strings (e.g. for eventq it certifies
`… write_fail=0 lagging=0`, a string the ledger does not display). A receipt that checks a string other
than the one printed is the failure mode criterion 24 exists for.

### H4 — `mado-evidence-audit.py`: a red exercise recorded as "by design", and unreproducible either way

Row §2c: "*`same file, evidence-audit-selftest block, EXIT=2` (`could-not-evaluate`, by design for that
case)*". The receipt's line is `{"code": 2, "error": "FileNotFoundError", …}` — a missing file, not a
designed outcome; the round-46 seat that produced that receipt filed it as a defect
(`.ufo/waves/round-46/w1/ExecHarmBase/baseline.md:161-170`, "*cannot be reproduced from committed bytes …
two fixture directories are empty and therefore cannot be committed*").

I reproduced both sides:

```
# a fresh clone of the lane at c24adef2 (what any reader gets):
$ python3 -I cl/tools/mado-evidence-audit.py --selftest cl/.ufo/waves/round-22/audit/fixtures ; echo rc=$?
{"authority": …, "code": 2, "error": "FileNotFoundError", …}
rc=2
# the lane working tree (where the two empty dirs exist, untracked):
$ python3 -I tools/mado-evidence-audit.py --selftest .ufo/waves/round-22/audit/fixtures ; echo rc=$?
{"authority": …, "cases": [ … ]}
rc=0
```

So the row records a state that depends on whether someone has run the tool before in that checkout. For a
ledger whose question is "*would this instrument work if I ran it*", that is the one row where the answer
is "only here".

### H5 — §9's control B prints a count that contradicts the seat's own receipt

ledger.md §9 (control B): `LEDGER: ok=7 stale=3 none=3 missing=0 …` — `missing=0` after deleting a row.

```
$ python3 -I check-ledger.py --repo <lane> --ledger <ledger copy with the globals row removed>
MISSING mado-globals.py
LEDGER: ok=7 stale=3 none=3 missing=1 mismatch=0 unbound=0 missing_receipt=0 instruments=14
rc=1
```

The seat's own receipt agrees with my run, not with the ledger:
`.ufo/waves/round-47/w1/ScrToolLedger/receipts/check-ledger.txt:13-15` prints `missing=1`, while
`ledger.md:283` prints `missing=0`. §9 calls that block "Raw output: `receipts/check-ledger.txt`", and
§6 of the same document (`ledger.md:214-215`) says the deleted-row copy "reads `missing=1`, exit 1". So the
document contradicts itself in the one block that proves its criterion can fail, and the version printed in
§9 is the wrong one.

### H6 — the proposed criterion cannot falsify `none`, and its `--rev` mode reads the worktree

Two experiments on the seat's own checker (`receipts/checker-probes.txt`):

```
# (a) a FALSE none row — eventq's receipt is committed and bound, and I declare the row none:
$ python3 -I check-ledger.py --repo <lane> --ledger led-falsenone.md
LEDGER: ok=6 stale=3 none=5 missing=0 mismatch=0 unbound=0 missing_receipt=0 instruments=14
rc=0
# (b) --rev mode at c24adef2, in a clone, with one receipt deleted from the worktree only:
$ git -C cl cat-file -e c24adef2:.ufo/waves/round-25/evidence/c1-after-v4-ef94763c.txt && echo present
present
$ python3 -I check-ledger.py --repo cl --rev c24adef2 --ledger led-base.md
MISSING-RECEIPT mado-binds.py .ufo/waves/round-25/evidence/c1-after-v4-ef94763c.txt
LEDGER: ok=7 stale=2 none=4 missing=0 mismatch=0 unbound=0 missing_receipt=1 instruments=14
rc=1
```

Cause, in the checker's own lines (`check-ledger.py:122,125`):

```
        if declared == "none":
            counts["none"] += 1
            continue                       # <- a none row is never re-derived
        rpath = os.path.join(repo, receipt)  # <- worktree, even when --rev is given
```

Criterion 91 promises "*it is the only one that makes the absence of live evidence visible*" and promises
re-derivation "*from `sha256sum` of the tool at `<REV>`*". The first is exactly the status the checker
skips; the second holds for the tool bytes but not for the receipt. H2 is the live instance: a wrong
`none` that the criterion's checker certifies.

### H7 — the `eventq` row misnames the journal unit it reads

Row: "reads … `journalctl --user -u hyprland`". The tool queries a different unit:

```
$ grep -n 'wayland-wm@hyprland.desktop.service' tools/mado-eventq.py
68:    --journal-file   `journalctl --user -u wayland-wm@hyprland.desktop.service
91:UNIT = "wayland-wm@hyprland.desktop.service"
```

No unit named `hyprland` exists on this host, so a reader who follows the row queries nothing and concludes
the journal plane is empty. Minor in size, central in kind: this is the column that exists to say what the
instrument reads.

### H8 — F5's process counts do not reproduce, and the receipt names no command

F5: "*Checked by counting `subprocess`/`Popen` sites and reading each one (`receipts/live-receipt-paths.txt`)*",
with `eventq 8`, `globals 6`, `options 7`, `tripwire 20`, `geometry/monitors/devices 0`.

```
$ for t in eventq globals options tripwire; do printf '%s %s\n' $t "$(grep -c subprocess tools/mado-$t.py)"; done
eventq 5
globals 6
options 7
tripwire 15
```

Two of the four reproduce, two do not (8 vs 5, 20 vs 15); the receipt names no command that yields its
numbers, which is QUALITY criterion 10 ("`<n> — <command> <date>`") applied to the lane's own paperwork.
The *conclusion* of F5 survives independently: the only real `subprocess.run` in `mado-tripwire.py` is at
`:3320`, inside `run_selftest` (`:3281`), so the scan path starts nothing; geometry/monitors/devices carry
no `subprocess` at all.

## 5. What the ledger gets right (do not re-register these)

- 10/10 receipt paths committed at base and HEAD; 14/14 rounds match their paths.
- 8/8 byte bindings re-derive: `eventq` `436f550e`, `options` `63b5ebd9`, `geometry` `1da3ddaed`,
  `monitors` `2f007417`, `devices` `3a803689` = current bytes; `verify` `050efc72`, `tripwire`
  `cd9da20c`, `binds` `0cda0e6f` = current bytes but the receipts recorded older ones (`stale`, correctly).
- §9's pristine line, control A and control C reproduce byte-for-byte.
- F4's "harness scratch is gone" is true today (`/fast/scratch/hyaku/mado-r26/wlroots/build`,
  `…/mado-r25-oracle-slots`, `…/mado-r27-oracle-slots` all absent), and the counters do name those paths
  (`receipts/live-receipt-paths.txt:25-27`).
- F2's "receipts-only search finds 4 of 10" reproduces exactly (`live-receipt-paths.txt:2-12`) — with the
  caveat that the true number of live receipts for these instruments is at least 13 (H1, H2).
- "Next free criterion number is 91" is true (`corpus/QUALITY.md` ends at 90), and the README insertion
  point (after `## Province routes — choose a surface` at `corpus/README.md:81`, before `## Frontier` at
  `:107`) exists as described.
- `PROVINCE.md:20-32` (the instrument table) and the operator commands in §2a all resolve: every flag the
  ledger prints exists in the tool (`--ss-file`, `--journal-file`, `--snapshot-out`, `--home`, `--getoption`,
  `--live`, `--clients`, `--rules`, `--monitors`, `--config`, `--devices`, `--scan`, `--no-live`, `--selftest`).

## 6. What a v2 of this ledger (or of criterion 91) has to change

Not done here — the L1 integrates; this is the falsify wave's repair list.

1. Search `.ufo/waves/round-NN/w1|w2/` too, or state the search rule as "receipt-shaped files only" and
   accept that "last live run" means "last *receipted* live run" (then H1a/H1b are not errors, but the
   rows must not say "last live run").
2. Derive `none` instead of asserting it: a `none` row must be accompanied by the absence command and its
   output (the seat's `absence.txt` does this for globals and got it wrong); or make the checker re-run it.
3. Print quotes by copy, never by compression — or drop the quotation marks and call them summaries, and
   make `verify-quotes.txt` check the strings the document actually prints (it currently checks others).
4. Never record a red exercise as "by design" without the tool's own label for it; record
   `FileNotFoundError` as what it is and note the checkout dependence.
5. Fix §9's control-B line to the receipt's `missing=1`, or stop calling §9's transcript "raw output".
6. The checker: re-derive `none`; read receipts through `git show <rev>:<receipt>` in `--rev` mode; match
   the sha only where the receipt *records* it (a bare hex match passes any receipt that cites the digest).
7. `eventq`'s journal unit; F5's two counts (with their command).

## 7. Retained evidence (all under `.ufo/waves/round-47/w2/ExecToolLedger/`)

| file | what is in it |
|---|---|
| `check-rows.py` → `receipts/row-checks.txt` | per-row re-derivation: receipt presence at base/HEAD, stated vs path round, recorded sha vs current bytes, declared vs derived status, `--selftest` rc + last line |
| `check-fragments.py` → `receipts/quote-fidelity.txt` | all 21 displayed verdict fragments vs the locator the row names, then vs the whole file |
| `receipts/selftests.txt` | the 14 `--selftest` runs at HEAD with exit codes, the no-flag messages, and the two gates that need a fixtures argument |
| `receipts/later-live-runs.txt` | the three live runs the ledger missed (monitors r46, eventq r39, globals r41) with hashes, dates and commits |
| `receipts/checker-probes.txt` | pristine, §9 controls A/B/C, false-`none`, and `--rev`-worktree experiments on `check-ledger.py` |
| `receipts/f5-counts.txt` | F5's process counts re-derived, the enclosing def of tripwire's only `subprocess.run`, and the journal unit `eventq` actually queries |
| `findings.json` | machine-readable rows, counts and holes |

Scratch (`/fast/scratch/hyaku/mado-r47/ExecToolLedger/`, including the `--shared` clone used for the
`--rev` probe) is deleted at the end of this seat; every command in this report re-derives from the lane
alone.

## 8. Limits

- I read verdict text; I did not re-run any live host probe, so "the receipt says X" is not "X is true of
  the host today". The only executions were `--selftest` runs and the two gate selftests named in §4/H4.
- `mado-verify.sh` was run with `--selftest` only (460/460); its live mode was not run (host guard).
- The census denominators in §7 of the ledger (1515 files / 89 receipts dirs at 18:48) are now
  1843 / 108 because other seats kept writing; the ledger dates them and calls them a moving target, so I
  do not count that as an error.
- "Wrong" in §3 means "a statement in the row that a reader cannot verify as written from the cited
  evidence". A quote-only error does not change the underlying fact; I separated the two so the L1 can
  weigh them differently.
