# R100MScoutHarm - C2 reconnaissance: the harm-watch gate's timing surface

Seat `R100MScoutHarm` (scout), round 100, wave w1, 2026-11-08. Read-only reconnaissance; no lane
file, tool, quality or corpus path was written. Scratch `$HYAKU_SCRATCH/mado-r100/R100MScoutHarm`
(`/fast/scratch/hyaku/mado-r100/R100MScoutHarm`), deleted before yield.

Snapshot. Read at base `43309e6a`; the lane tip moved to `219e14f4` mid-seat (the L1 landed the
round-100 C1+C2 artifacts, including a new `quality/harm-watch.py`), so every statement below names
the bytes it was measured on:

| artifact | bytes measured | sha256 |
|---|---|---|
| `quality/harm-watch.py` at `3b69f041` (the round-99 pin) | r99 gate | `37a0544b160d9c5c5568fc45f9ed309f41b36fb093983313d72699423b4165b9` |
| `quality/harm-watch.py` at the tip (`219e14f4`, worktree) | r100 gate, byte-identical to `build/harm-watch.py` | `2d604f7b654f2e2710b612358fedf81fc028dddd47fd0934d9f82c065b226167` |
| `.ufo/waves/round-99/controls/harm-panel-r99.json` | frozen 28-leg panel | `160763ce7aa447016bad8e5b2c5a7c25f8866b1e8724d8eb0b75d8abb1dae39a` |
| `.ufo/waves/round-100/controls/harm-panel-r100.json` | timeout-only re-freeze | `6d259164de900f9997d399a75a234bef5f46cc39006b046979bd05b57f7e65ac` |
| `quality/counters/c2-r99-harm-watch.py` | the round-99 counter | `ebde11a3033f01d48b85b592e29cc24f355572bd2d0ae85a23154b970e45115a` |
| `quality/counters/c2-r100-harm-watch.py` at the tip | landed r100 counter (**not** the `build/` draft) | `b7d2d32ef8fcffb14fba10fd2dba8917f44ee6e81c898beba5911323f53d4076` |
| `.ufo/waves/round-100/build/c2-r100-harm-watch.py` | the seat draft the mutation tester anchored | `e4741843278efaf6715b70246dbe82a6c92852bffd14de97a672ef78182ac253` |

Transcript: `.ufo/waves/round-100/receipts/scout-harm-r100.txt` (every line below is that receipt).

Line numbers are for the **round-99 gate** (`3b69f041`, 604 lines) unless a section says "landed
r100 gate" (63 lines changed; the delta is enumerated in section 6).

---

## 1. (a) Every place a leg's wall time could be recorded

The gate has exactly one subprocess boundary, so there is exactly one wall-time surface; the
question is which of its code paths carry the number out.

| # | site (r99 gate) | what it is | carries time today |
|---|---|---|---|
| T1 | `:197-198` `subprocess.Popen(argv, cwd=repo, ...)` | the spawn; the only place a leg's clock starts | no |
| T2 | `:203` `p.communicate(timeout=timeout)` | the normal completion path | no |
| T3 | `:205-220` `except subprocess.TimeoutExpired:` - killpg (`:207`), re-`communicate` (`:212`), `p.kill/p.wait` (`:215-216`), `rc = 124` (`:219`), `detail = "timeout-after-%ss"` (`:220`) | the timeout path; the *only* duration the gate states today, and only as the cap, not as elapsed | only as `timeout-after-Ns` inside `detail` |
| T4 | `:199-201` `except OSError` -> `{"rc": 127, "detail": "spawn-failed"}` | spawn failure | no |
| T5 | `:192`, `:194` the two early `setup` returns (`scratch-root-required`, any `safe_scratch_dir` refusal) | refused before the spawn | no (and no clock has started) |
| T6 | `:223-231` the per-leg log writer (`<scratch-root>/<id>.log`, written **after** `communicate`) | the only durable per-leg record; it already writes `$ argv`, stdout, stderr and `--- rc=N ---` | no - `:229` writes rc only |
| T7 | `:232-233` the `run_leg` return dict | the in-memory record the panel consumes | no |
| T8 | `:306-308` the human `LEG` line | the line the round-100 claim names | no |
| T9 | `:311-315` the `--json` leg object appended to `results` | the json record the round-100 claim names | no |
| T10 | `:317-326` and `:329-335` the two json blobs and the summary line | aggregate records; a per-leg total could be summed here, but a *per-leg* value cannot be invented at this level | no |

So a minimal correct patch needs exactly two timestamps (`t0` at `run_leg` entry, `t1` after the
last wait) and three carriers (T7 -> T8/T9, and optionally T6). The timeout path (T3) must compute
its elapsed **after** the killpg/re-`communicate` block, not inside `except`, or the leg that killed
the process group reports only the time to the exception.

## 2. (b) The exact current output contract (r99 gate, unchanged by the landed r100 gate)

Measured by running each gate on a two-leg fixture (`fix.json`, one `ok`, one `marker=MISS`) and
capturing `cat -A`-clean bytes: the r99 bytes on the pre-landing tree, the landed r100 bytes below in
section 6. Both printed the same human lines and the same nine top-level keys; they differ only by
the trailing `elapsed_ms=` token and the new per-leg key.

**Human lines, in emission order.**

```
LEG <id> rc=<n> expect=<n> marker=<ok|MISS> <detail>
HARM_WATCH: legs=<N> ok=<M> mismatch=<K>
```

* `rc` is `SETUP` (literal) when `res["rc"]` is `None` (`:307`), otherwise the integer.
* `<detail>` at `:236-255` is one of `ok`, `rc-mismatch`, `marker-missing`,
  `rc-and-marker-mismatch`, `setup:<reason>`; a non-empty `res["detail"]` is appended as
  `detail+"+"+res_detail` unless detail is `ok`, where it replaces it (`:254-255`). So the two
  timeout strings are `rc-and-marker-mismatch+timeout-after-600s` and
  `timeout-after-600s` (the latter when rc and marker both match, which cannot happen at rc 124
  with `expect_rc=0`).
* A setup refusal inside the loop emits an extra line `HARM_WATCH: setup-error leg=<id> detail=<d>`
  (`:317-318`) **in place of the summary**, then exits 2.
* Census/setup findings are `PANEL <ID> <detail>` (`:68-69`), one line each, emitted before any leg.

**`--json` object keys.** The two blobs differ; both are `json.dumps` on one line, printed *after*
the human lines.

* normal exit (`:330-335`): `repo`, `rev`, `panel`, `census` (always `[]`), `legs_run`, `ok`,
  `mismatch`, `legs`, `exit` (0 or 1).
* setup exit 2 (`:319-325`): the same nine keys with `exit: 2` plus `setup_error`.
* per leg object (`:311-315`): `id`, `round`, `rc`, `expect_rc`, `marker_ok`, `ok`, `detail`.

**Summary line** is byte-exact and is what the round-99 counter regexes
(`c2-r99-harm-watch.py:228`, `r"HARM_WATCH: legs=(\d+) ok=(\d+) mismatch=(\d+)"`):
`HARM_WATCH: legs=N ok=M mismatch=K`.

**Exit map.** 0 clean; 1 any leg mismatch (rc or marker); 2 setup, usage, or any census finding
(`PANEL_UNREADABLE` from `:277`, `:282`, `:286`; `PANEL_ONLY_UNKNOWN` `:294`; `PANEL_SETUP`
`:286`, `:596`, `:599`). `--selftest` returns 0 iff `failed == 0` (`:572-576`).

## 3. (c) Every selftest check, and which break if `elapsed_ms` is added

`python3 -I quality/harm-watch.py --selftest` on the r99 bytes: **`checks=26 failed=0`** (measured,
1.9 s). The 27 `record(` call sites at `:428-569` collapse to 26 checks because `json-mode` is
recorded twice (`:549`, `:552`: the `except` branch writes the same name). The landed r100 gate
prints **`checks=33 failed=0`** (measured, 3.0 s, 3 runs).

The checks that assert a `LEG` or summary line by substring are the ones a format change can break.
Three of them hard-code a **trailing** segment, so they break iff the new field is inserted before
the old tail:

| check | line | assertion | breaks on a mid-line `elapsed_ms=`? |
|---|---|---|---|
| `clean-leg-line` | `:432-433` | `"LEG good rc=0 expect=0 marker=ok ok" in out` | **yes** if inserted before `ok` |
| `marker-miss` | `:499-500` | `"LEG good rc=0 expect=0 marker=MISS marker-missing" in out` | **yes** |
| `rc-mismatch` | `:507-508` | `"LEG odd rc=0 expect=1 marker=ok rc-mismatch" in out` | **yes** |
| `timeout` | `:515-516` | `"LEG slow rc=124 expect=0"` + `"timeout-after-1s"` | no (prefix + detail token) |
| `wrong-exactly-one-mismatch` | `:450-452` | `" rc=0 expect=1 "` and the summary | no |
| `clean-summary` / `wrong-exit1` / `dropped-*` / `extra-*` / `duplicate-id` / `round-missing` / `round-empty` / `leg-count` / `rev-substitution` / `rev-no-literal-token` / `scratch-*` / `json-mode` / `panel-unreadable` / `leg-logs-written` / `repo-untouched` / `clean-exit0` / `clean-no-panel-line` | `:428-569` | census, exit codes, substitution, logs | no |

**Measured, not inferred.** I patched the r99 gate two ways in scratch and ran the selftest:

* elapsing **appended last** (`... ok elapsed_ms=34`): `checks=26 failed=0` - clean.
* elapsing **inserted before `<detail>`** (`... marker=ok elapsed_ms=34 ok`): `checks=26 failed=3`,
  `FAIL clean-leg-line`, `FAIL marker-miss`, `FAIL rc-mismatch`.

So the append position is not cosmetic: it is the difference between a green selftest and three
red checks. The landed r100 gate appends last (`:313-315`) and keeps `checks=26`'s checks intact.

Checks a *complete* implementation must add (the claim's words are "present, non-negative,
integer, and monotone across a fixture whose second leg is slower"): the landed r100 gate adds 7
(`clean-elapsed-ms`, `clean-elapsed-ms-second`, `clean-elapsed-ms-integer`, `timeout-elapsed-ms`,
`json-elapsed-ms`, `elapsed-monotone`, `elapsed-human-line` = 33 total). I checked that they bite:
mutating all four `max(0, int((time.monotonic() - t0) * 1000))` sites to `0` yields
`checks=33 failed=2` with `FAIL timeout-elapsed-ms` and `FAIL elapsed-monotone` - the two checks
that would catch a clock that is never read.

## 4. (d) The census findings and the exit map

`census()` is `:77-151`; it runs to completion before any leg (`:278-282`), and **any** finding
exits 2 with no leg started.

| id | site(s) | condition |
|---|---|---|
| `PANEL_UNREADABLE` | `:82`, `:85`, `:88`, `:132` | `legs` not a non-empty list; `rounds` not a non-empty dict; `expect_legs` not an int; a round's ids not a list |
| `PANEL_ROW` | `:94`, `:98`, `:102`, `:104`, `:106`, `:109`, `:111`, `:113` | a row that is not an object, has no id, lacks one of `round`/`argv`/`expect_rc`/`expect_marker`/`note`, has an empty argv list or an empty element, a non-int `expect_rc`, a non-str `expect_marker`, a non-str `round` |
| `PANEL_DUPLICATE` | `:115` | an id seen twice (each occurrence after the first) |
| `PANEL_LEG_UNKNOWN` | `:122`, `:125` | a row id the row's own round does not declare, or a round name no `rounds` key carries |
| `PANEL_LEG_MISSING` | `:136` | a round-declared id with no row |
| `PANEL_ROUND_MISSING` | `:138` | a declared round whose id list is empty |
| `PANEL_LEG_COUNT` | `:149` (inserted at index 0) | row-count delta != 0 **and** != `len(unknown) + dup_surplus - missing` - i.e. only an *unexplained* delta; the net-of-findings rule that makes a dropped-leg panel exactly one finding |
| `PANEL_ONLY_UNKNOWN` | `:294` (not census; `--only` validation) | `--only` id the panel does not declare |
| `PANEL_SETUP` | `:286`, `:596`, `:599` | `SCRATCH` legs with no `--scratch-root`; a missing `--repo/--rev/--panel`; `--repo` not a directory |

Measured on the live bytes: a duplicated row prints exactly `PANEL PANEL_DUPLICATE id=verify_file_plane` and
exits 2; `--only nosuchleg` prints `PANEL PANEL_ONLY_UNKNOWN id=nosuchleg` and exits 2.

`PANEL_ROW` and `PANEL_ONLY_UNKNOWN` are **not** in the `SKILL.md:2985` row's id list (it names only
`PANEL_LEG_COUNT`, `PANEL_DUPLICATE`, `PANEL_ROUND_MISSING`, `PANEL_LEG_UNKNOWN`,
`PANEL_LEG_MISSING`) and `PANEL_UNREADABLE`/`PANEL_SETUP` are only implied there. A round that
freezes a new finding id must re-freeze that row.

## 5. The round-99 panel, re-derived (`harm-panel-r99.json`)

Measured: `timeout_s=600`, `expect_legs=28`, `legs=28`, sha256 `160763ce…e39a`, and the 28 ids in
this order: `verify_selftest, verify_file_plane, index, ledger, mako_selftest, portals_selftest,
mime_selftest, xdgmime_selftest, mimeglob_selftest, mimesniff_selftest, seat_reports_selftest,
receipt_presence_selftest, gate_selftest, gate_seat_reports, gate_mimeglob, gate_portals,
r90c2_receipt_presence, r92_gate_defects, r90c1_portal_routing, r94c1_mimeglob, r94c2_selftest_kills,
r93c2_selftest_strength, r95c1_mimesniff, r95c2_selftest_kills, r96c1_magictext, r96c2_selftest_kills,
r97c1_filetype, r97c2_counter_selftest`. `rounds` declares eight groups (`base` 16, `r90` 2, `r92` 1,
`r93` 1, `r94` 2, `r95` 2, `r96` 2, `r97` 2) and the count is exact.

**Markers that embed a selftest check count - nine legs; a later round that adds a check to any of
these tools must re-freeze these markers.** (These are the *tools'* counts, not the gate's.)

| leg | marker (verbatim) | count I measured today |
|---|---|---|
| `mako_selftest` | `MADO_MAKO_SELFTEST: checks=62 failed=0` | 62 (needs `--scratch-root`) |
| `portals_selftest` | `MADO_PORTALS_SELFTEST: checks=28 failed=0` | 28 |
| `mime_selftest` | `MADO_MIME_SELFTEST: checks=17 failed=0` | 17 |
| `xdgmime_selftest` | `MADO_XDGMIME_SELFTEST: checks=12 failed=0` | 12 |
| `mimeglob_selftest` | `MADO_MIMEGLOB_SELFTEST: checks=19 failed=0` | 19 |
| `mimesniff_selftest` | `MADO_MIMESNIFF_SELFTEST: checks=26 failed=0` | 26 |
| `seat_reports_selftest` | `SEAT_REPORTS_SELFTEST: checks=23 failed=0` | 23 |
| `receipt_presence_selftest` | `RECEIPT_PRESENCE_SELFTEST: checks=6 failed=0` | 6 |
| `gate_selftest` | `SELFTEST_STRENGTH_SELFTEST: checks=11 failed=0` | 11 |

The other 19 markers are count-agnostic (`assertions passed`, `uncovered=0`, `TARGET_MET`,
`SETUP_ERROR ...`, the three `SELFTEST_STRENGTH: OK tool=<path>` lines, etc.) and survive a check
being added. Note the gate's **own** selftest count is *not* a panel marker: nothing in the panel
asserts `HARM_WATCH_SELFTEST: checks=`; only `SKILL.md:2985` states `checks=26`, and it is a prose
claim, not a machine pin (section 8, D4).

## 6. The minimum byte-level change, and the exact new `--json` shape

The minimum that satisfies the frozen sentence (elapsed on the human line **and** a per-leg json
field) without touching a census id, an exit code, or an existing field:

```
--- a/quality/harm-watch.py
+++ b/quality/harm-watch.py
@@ -61,6 +61,7 @@
 import subprocess
 import sys
 import tempfile
+import time                                        # (1) module import

 def run_leg(row, repo, rev, scratch_root, timeout):
+    t0 = time.monotonic()                          # (2) one clock read at entry
     legdir, err = safe_scratch_dir(...)
@@
-    return {"id": row["id"], "rc": rc, "out": out, "err": err, "detail": detail,
-            "legdir": legdir}
+    return {"id": row["id"], "rc": rc, "out": out, "err": err, "detail": detail,
+            "legdir": legdir,
+            "elapsed_ms": max(0, int((time.monotonic() - t0) * 1000))}   # (3) one clock read at exit
@@ run_panel's leg loop
+        elapsed_ms = res.get("elapsed_ms", 0)      # (4) default keeps setup rows shaped
-        line = "LEG %s rc=%s expect=%s marker=%s %s" % (
+        line = "LEG %s rc=%s expect=%s marker=%s %s elapsed_ms=%s" % (     # (5) APPENDED last
             row["id"], rc if rc is not None else "SETUP", row["expect_rc"],
-            "ok" if marker_ok else "MISS", detail)
+            "ok" if marker_ok else "MISS", detail, elapsed_ms)
@@ results.append
+            "elapsed_ms": elapsed_ms,              # (6) new json key, after detail
```

Six hunks, no line deleted, no existing field renamed. Two things this minimal form still needs
for the claim's own words, both of which the landed gate does:

1. **the three non-normal `run_leg` returns** (`:192`, `:194`, `:199-201`) - without them a setup or
   spawn-failed leg lands in `results` via `res.get("elapsed_ms", 0)` and is reported `elapsed_ms=0`,
   which is non-negative and integer but not measured. The landed gate adds the same expression to
   all three (`landed :194-198`, `:203-206`) and one computed `elapsed_ms` before the return
   (`landed :226`), i.e. **four** clock sites, and `mut_zero` (all four -> `0`) is caught by exactly
   two selftest checks (section 3).
2. **the timeout path** - `elapsed_ms` must be computed at `landed :226`, *after* the killpg and the
   30 s re-`communicate`, so a timed-out leg reports `>= timeout*1000`; computing it inside the
   `except` would report only the time to the exception. Measured on the landed gate: a 1 s cap
   fixture reports `elapsed_ms=1004`.

**Exact new `--json` shape** (measured on the landed gate, two-leg fixture, keys in emission order):

```json
{"repo": "…", "rev": "…", "panel": "…", "census": [], "legs_run": 2, "ok": 1, "mismatch": 1,
 "legs": [{"id": "a", "round": "r0", "rc": 0, "expect_rc": 0, "marker_ok": true, "ok": true,
           "detail": "ok", "elapsed_ms": 7},
          {"id": "b", "round": "r0", "rc": 0, "expect_rc": 0, "marker_ok": false, "ok": false,
           "detail": "marker-missing", "elapsed_ms": 3}],
 "exit": 1}
```

The key is appended **after** `detail` in each leg object, so every existing consumer that reads by
key is untouched, and a consumer that compares `json.dumps` byte-for-byte is not. No aggregate
(`total_elapsed_ms`, `max_elapsed_ms`) is added - the round-100 counter derives its maximum from the
timing receipt, not from the gate, and the gate's summary line is byte-identical.

Human line measured on the landed gate: `LEG a rc=0 expect=0 marker=ok ok elapsed_ms=7`. The
`elapsed_ms=` token is the **last** field, which is what keeps the nine marker-bearing panel legs
and the three suffix-asserting selftest checks green (section 3).

## 7. Consumers of the gate inside the lane, and who pins a gate sha256

Searched `tools/ quality/ .ufo/waves/round-99/`, then widened to the whole lane for
`quality/harm-watch.py` and `expect-gate-sha256`.

| consumer | path:line | relation to the gate | harmed by a new gate? |
|---|---|---|---|
| the gate itself | `quality/harm-watch.py` | candidate | - |
| **round-99 counter** | `quality/counters/c2-r99-harm-watch.py` | `GATE_REPO_PATH` `:72`; `git show REV:quality/harm-watch.py` `:501`; pin check `:506-507`; blind-patch anchor `BLIND_FROM` `:78` | **no, by construction**: it reads the gate from `--rev` with `git show`, never from the worktree, and its own frozen invocation pins `--rev 3b69f041` where the r99 bytes still exist. **Measured**: `--rev 3b69f041` + pin `37a0544b…` runs; `--rev 219e14f4` + the same pin exits 2 `SETUP_ERROR gate sha256 2d604f7b… != pinned 37a0544b…`. Its selftest is fixture-driven (`MINI_GATE`) and still prints `checks=17 failed=0` on the landed tree. |
| round-99 panel legs | `.ufo/waves/round-99/controls/harm-panel-r99.json` | the 28 legs; two of them (`r94c2_selftest_kills`, `r93c2_selftest_strength`) carry `--expect-gate-sha256 2d6f1219…`, which is the **r93** gate, not this one | no |
| round-99 planted controls | `.ufo/waves/round-99/controls/harm-planted/*.json` (5 files) | byte-frozen panels; two argv rows each name the r93 gate pin | no |
| round-99 mutant population | `.ufo/waves/round-99/controls/harm-mutants-r99.json` | `tool` = `.ufo/waves/round-99/build/harm-watch.py`, `anchor_sha256` = `8ad90bed…` (the *build draft*, not the landed gate), 32 mutants with singleton `find` strings in that draft | **yes, if anyone replays it against the tip**: measured, mutant `leg-line-id-length`'s `find` occurs **0** times in the landed gate (the LEG format changed). The file itself names its anchor, so this is a stale-anchor hazard for a future replay, not a current red. |
| round-100 build draft | `.ufo/waves/round-100/build/harm-watch.py` | the landed gate is byte-identical (`2d604f7b…`) | no |
| **round-100 counter** | `quality/counters/c2-r100-harm-watch.py` (landed) | `GATE_PATH` `:46`; gate bytes `git show` `:135` or worktree `--rev worktree`; pin `:145` | this is the gate's scoring consumer; it pins `--expect-gate-sha256` for the new bytes |
| round-100 declaration | `.ufo/waves/round-100/claims-declaration-r100.md:95-100`, `:136-139` | freezes the counting argv and the `elapsed_ms` sentence | no |
| registry row | `SKILL.md:2985` | states the gate's CLI, exit map, census ids and `HARM_WATCH_SELFTEST: checks=26 failed=0` | **the check count is stale on the landed bytes** (measured 33) |
| registry row | `SKILL.md:2986` | the round-99 counter's frozen argv (`--expect-gate-sha256 37a0544b…`, `--rev REV`) | no (it names the r99 rev's bytes) |
| prose | `SKILL.md:3025-3034`, `PROVINCE.md:624`, `SCOREBOARD`/`SCORECARD.md:5626`, `LOG.md:4700`, `plans/round-99.md:25` | describe the gate | no |
| ledger | `quality/tool-ledger.md:236-237` | rows for `quality/harm-watch.py` and `quality/counters/c2-r99-harm-watch.py` | **the two new r100 counters have no row** (section 8, D2) |
| panel legs that re-enter the gate | panel ids `ledger`, `index` | `quality/check-tool-ledger.py` and `quality/check-index.py` over the measured rev | see D2/D3 |

**Which one pins a gate sha256 and does it read from `--rev`?** The round-99 counter is the one the
brief asks about: `c2-r99-harm-watch.py:501` is
`sh_bytes(["git", "-C", repo, "show", "%s:%s" % (a.rev, GATE_REPO_PATH)])`, and `:506` refuses when
the sha differs from `--expect-gate-sha256`. It **never** reads the worktree (its `--gate PATH` draft
mode is explicitly "never part of the pinned counting command", `:29-33`). So a new gate at a new rev
leaves it unharmed *provided the caller keeps the r99 rev*, which its own frozen argv does. The
failure mode is a **reader** substituting `--rev HEAD` into `SKILL.md:2986`, which now exits 2
(measured). The round-100 counter has the mirror property: it reads the gate with the same
`git show REV:…` and pins the new sha.

## 8. Current state of the C2 surface at the tip - measured defects the L1 must clear

These are reconnaissance findings, not repairs (my scope is read-only). Every one is a command whose
output is in the receipt.

**D1 - the round-100 panel's `ledger` leg is red at the tip, so `mismatch=0` is unreachable.**
`quality/check-tool-ledger.py --repo . --rev 219e14f4` prints two `uncovered` rows and
`verdict=TARGET_MISSED` (population 201, ledger rows 199), naming
`quality/counters/c1-r100-launchenv-path.py` and `quality/counters/c2-r100-harm-watch.py`. The panel
leg `ledger` at the same rev prints `LEG ledger rc=1 expect=0 marker=MISS rc-and-marker-mismatch`.
Measured directly. Fix is one ledger row per new counter (`quality/tool-ledger.md` is the L1's file).

**D2 - the timing receipt and the counting command must agree on the `TIMING-DONE` line.**
The landed counter's `parse_timing` (`quality/counters/c2-r100-harm-watch.py:76-90`) parses rows and
sets `done` on a `TIMING-DONE` prefix, and `:156-157` refuses with
`SETUP_ERROR timing receipt has no TIMING-DONE line`. At 02:29 the committed receipt had no such line
(`grep -c TIMING-DONE` -> 0) and the counter, run with the pins of that moment, exited
`SETUP_ERROR timing receipt has no TIMING-DONE line`. By 02:35 the line was present
(`grep -c` -> 1) and the *pin* had moved (the file's sha changed from `dd8d9f88…` to `e7280b53…`).
Either way the receipt is being edited after its first pin: whoever freezes the timing pin must
freeze it **after** the last edit, and the receipt must carry `TIMING-DONE` for the landed parser.
(My earlier probe against the *build draft* parser printed `parse_timing -> n=28 max=708014
over600=1` only after I appended `TIMING-DONE` myself - the draft parser returns `None` without it.)

**D3 - `r97c1_filetype` is not reproducible at a long scratch root: its rc depends on the length of
the path passed as `SCRATCH`.**
At `--scratch-root /fast/scratch/hyaku/mado-r100/R100MScoutHarm/panelrun` (68 chars) the leg
returned `rc=2` with `MADO_FILETYPE_COUNT: SETUP_ERROR … OSError: AF_UNIX path too long` from
`.ufo/waves/round-97/controls/filetype-fresh-r97.py:216` (`srv.bind(p)`), while `r92_gate_defects`
in the same run was `rc=0`. The panel declares `expect_rc=0` for that leg, so a long scratch root
turns the panel red through no fault of the gate. The `sun_path` limit I measured on this host is
107 usable bytes (100 and 106 bind OK; 108 and 110 fail with `AF_UNIX path too long`), and the
round-100 timing receipt's own header records a `<S>/scr` scratch root - i.e. the round's timing pass
used a short root and my long one does not reproduce it. **The re-frozen panel must declare a scratch
root that is short enough for `r97c1_filetype`**, or the leg's expectation must be declared
path-dependent. Same class as the r99 cap: an undeclared input (here the scratch path length, there
the wall-clock cap) that the predicate does not read.

**D4 - `SKILL.md:2985` still states `HARM_WATCH_SELFTEST: checks=26 failed=0`; the landed gate prints
`checks=33 failed=0`.** Measured both. Not machine-pinned (no gate reads the registry row's count),
so it is a record defect, not a red; but criterion 171's spirit (a row's pins are re-derived from the
artifact) applies to a row's counts too.

**D5 - the round-100 `c2-gate-r100.txt` receipt names a panel sha (`bec81a3e…`) that is not the
committed panel's (`6d259164…`).** The seat wrote it before the L1's timeout re-freeze; a reader who
takes the receipt's pin gets `SETUP_ERROR panel sha256`. The panel's *content* is correct (28 leg rows
byte-identical to r99, `timeout_s` 600 -> 3600, all other keys equal - I compared the parsed objects),
so this is a pin-freshness defect, exactly M99-1's class.

**D6 - the round-100 panel's leg set is the round-99 set, so the panel does not watch the round-100
instruments.** The declaration says "unchanged leg set, re-frozen cap", which is what the bytes do;
consequence: neither `quality/counters/c1-r100-launchenv-path.py` nor
`quality/counters/c2-r100-harm-watch.py` is replayed by the panel. That is a declared design choice,
named here so the choice is visible, not a defect against the frozen sentence.

**D7 - `max_elapsed_ms > 600000` is at the edge of its own measurement.** The committed timing
receipt's maximum is `r92_gate_defects elapsed_ms=708014`; the conjunct passes by 108 s (18 %). The
same leg measured `467 s` wall for me in a two-leg run at load average ~110-250, i.e. the receipt's
708 s is load-dependent by >50 %. The frozen sentence is satisfied today, but the headroom in the
*conjunct* (not the cap) is thin: one quieter host re-measurement of the timing receipt could put the
maximum under 600 s and flip `max_gt_600s` and `control_ge_1` together. The L1 should freeze the
timing receipt it actually re-runs at committed bytes, and say so.

## 9. Answers, in one place

1. **Wall-time sites**: one boundary (`:197` Popen), five return paths (`:192`, `:194`, `:199`,
   `:203`, `:205-220`), three carriers (return dict `:232`, LEG line `:306`, json leg `:311`), one
   durable record (`:223-231` leg log). Ten sites, table in section 1.
2. **Output contract**: `LEG <id> rc expect marker detail` + `HARM_WATCH: legs ok mismatch`,
   `PANEL <ID> <detail>` before any leg, nine json keys at the top level (ten on setup) and seven per
   leg; exit 0/1/2 as in section 2.
3. **Selftest**: 26 checks on r99 bytes, 33 on the landed bytes; exactly three (`clean-leg-line`,
   `marker-miss`, `rc-mismatch`) break on a mid-line insertion, measured with a patched copy; none
   break on an append.
4. **Census**: eight parser-level ids + `PANEL_ONLY_UNKNOWN` + `PANEL_SETUP`, exit 2 for all, table
   in section 4.
5. **r99 panel**: `timeout_s=600`, `expect_legs=28`, 28 ids listed, nine count-bearing markers
   tabled - those nine must be re-frozen by any round that changes those tools' check counts.
6. **Minimum change**: six hunks (import `time`, `t0`, elapsed on the return, LEG append, json key,
   the `res.get` default), plus the three non-normal returns and the post-kill timeout read; new json
   leg key `elapsed_ms` appended after `detail`, no aggregate key, summary and census byte-identical.
7. **Consumers**: the r99 counter (harmless - `git show --rev`; measured), the r100 counter (the
   scorer), the two registry rows, the ledger rows, the r99 mutant population (stale anchor:
   `leg-line-id-length` find count 0 on the tip), and no other lane instrument reads the gate bytes.

## 10. Remaining unknowns

* I did not re-run the full 28-leg panel end to end at the tip (host load ~110-250 on 32 cores; the
  two-leg run took 467 s wall, and the only-census legs are cheap). The per-leg facts above are
  measured; the aggregate `mismatch=0` is not, and D1 already shows it cannot be reached at the tip.
* I did not finish the `r97c1_filetype` leg at a scratch root short enough to reproduce `rc=0`; the
  length threshold and the failure mode are measured, the exact minimum root length for that leg's
  generator (`<root>/c1r97-XXXXXXXX/case-NNN/s.sock`, ~30 bytes of suffix) is not.
* I did not execute the r99 counter to completion against its pinned rev (it spawns the 28 legs; my
  run was killed at the 300 s budget). Its gate-byte behaviour is measured directly (section 7), and
  its selftest is green at the tip.
* The r100 counter's end-to-end verdict was not observed against the committed pins; my run was
  interrupted at the 280 s budget after the pin moved under it (D2). The conjunct values it will
  emit are derivable from the receipt (`timing_legs_timed=28`, `max_elapsed_ms=708014`,
  `control_600s_would_mismatch=1`, `panel_timeout_s=3600`), but I did not observe the line.
* No tool was installed or upgraded this round (nothing was needed; all work is stdlib Python plus
  read-only `git`).

Report: .ufo/waves/round-100/w1/R100MScoutHarm.md
