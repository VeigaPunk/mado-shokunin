# ExecCaptureStable — stability of the committed native capture (C1 clause k)

Seat: ExecCaptureStable (wave w1, round 40). Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Base `9fc511ddce708327377161202f358ce37dc266ba`; freeze `5e7e88525cc539563de7746361b2650802e81809`.
Lane HEAD during the run: `e2b51d3b3f79768282914d57c1fa32cc85dcb06a`.

**Result: zero keys changed. Zero form alterations. The three fresh sweeps are byte-identical to
each other and byte-identical to the committed capture `1fe39c05…`.**

## What this attacks / supports

- **Supports** C1 clause k — `quality/counters/c1-r40-live.py:598-615` (`capture_ok`): "the
  native-capture receipt at REV holds the four forms the counter's stub emits and 70 non-blank
  lines" (`c1-r40-live.py:58-59`). Clause k is a static byte test; this seat shows the bytes it
  tests are *reproducible from the live compositor*, not a one-off snapshot.
- **Attacks** the assumption behind `registration.md:5-7` ("Any later change to a counter, a
  control, the capture or a declared target is a new predicate"): a capture that drifted between
  sweeps would make the frozen artifact an accident of timing. It does not drift.
- **Attacks** the gradient-angle-inheritance fact used by the C1 conversion model (provisional
  fact 5: the theme's single-colour `col.active_border` reads `ffe68e0d 45deg` because the
  defaults tree declared a 45deg gradient first). The inherited angle reproduces identically in
  all three sweeps, so it is a stable property of the loaded config, not a transient.

## Method (exact commands)

1. Key list, from the tool under test, not from the capture:
   `python3 -I tools/mado-options.py --home "$HOME"` → 70 rows, 70 unique keys, exit 0
   (`static-table.json`, `keys.txt`; stderr empty).
   The key sequence is **identical** to the `option` sequence of the committed capture, and the
   key *sets* of the static table, the committed capture and every fresh sweep are equal
   (checked both directions: no missing, no extra).
2. Three sweeps, one minute apart, one `hyprctl getoption -j KEY` per key in key-file order,
   recording `key \t rc \t reply-text` (`capture.sh`):
   ```
   for i in 1 2 3; do
     while IFS= read -r k; do
       out=$(hyprctl getoption -j "$k" 2>&1); rc=$?
       printf '%s\t%s\t%s\n' "$k" "$rc" "$out" >> cap$i.raw
     done < keys.txt
     [ $i -lt 3 ] && sleep 60
   done
   ```
3. Comparison (`compare.py`, stdlib only, exit 0): per key, compare `rc`, exact reply text, the
   native form, `set`, and the value — committed vs cap1, cap2, cap3, and all three pairwise.
4. Clause k re-run against the three fresh payload files by importing the frozen counter's own
   `capture_ok` (`importlib`; the module is `__main__`-guarded at `c1-r40-live.py:685-690`), so the
   check is the frozen predicate's code, not a re-implementation.

Only compositor verbs used in this seat: `hyprctl getoption -j <key>` (210 calls) and
`hyprctl version` (1 call). No `keyword`, `dispatch`, `reload`, `setprop`, `--batch`. No socket,
no input injection, no service, no config-tree write.

## Evidence

### Spacing and identity

| sweep | start (UTC, in-sweep) | file mtime (local, -0300) | lines | sha256 |
|---|---|---|---|---|
| cap1 | `2026-10-25T20:49:11Z` | `17:49:11.470399596` | 70 | `b30528b62fbaaac4264078ef9bd25f98ecf05e308f905b0a36f94593751715e8` |
| cap2 | `2026-10-25T20:50:11Z` | `17:50:11.666582784` | 70 | `b30528b62fbaaac4264078ef9bd25f98ecf05e308f905b0a36f94593751715e8` |
| cap3 | `2026-10-25T20:51:11Z` | `17:51:11.855767568` | 70 | `b30528b62fbaaac4264078ef9bd25f98ecf05e308f905b0a36f94593751715e8` |

Observed spacing from mtimes: **60.196 s** (cap1→cap2) and **60.189 s** (cap2→cap3); start stamps
are exactly 60 s apart. `cap1.raw == cap2.raw == cap3.raw` (same sha256, `diff` empty, 6646 B each).

Honest defect in my own harness: `capture.sh:21` used `bc`, which is not installed on this host,
so the recorded `dur=` field is `0.00s` and the per-sweep duration was **not** measured
(`timings.txt` carries the three start/end stamps and line counts only). Spacing is therefore
evidenced by the start stamps and file mtimes, not by a computed duration. `bc` was not installed
to fix this: not needed for the claim, and the host package manager is paused.

### Payload identity with the committed capture

The reply column of each sweep, extracted verbatim (`awk -F'\t' '{print $3}'`), reproduces the
committed file exactly:

```
1fe39c0528f1b11d7f69bf41ac236f39ff6e00b9b8a275f4e94b06c5189b4b25  cap1.jsonl
1fe39c0528f1b11d7f69bf41ac236f39ff6e00b9b8a275f4e94b06c5189b4b25  cap2.jsonl
1fe39c0528f1b11d7f69bf41ac236f39ff6e00b9b8a275f4e94b06c5189b4b25  cap3.jsonl
1fe39c0528f1b11d7f69bf41ac236f39ff6e00b9b8a275f4e94b06c5189b4b25  .ufo/waves/round-40/c1/native-capture.jsonl
```

`diff -q` each → no difference (4740 B each). This is stronger than a semantic match: the
compositor's own formatting (`"set": true }`, space before the brace) is reproduced, so the
committed capture was a verbatim sweep and has not been reformatted, re-ordered or hand-edited
anywhere in its 70 lines.

### Per-key comparison: the requested answer

`compare.py` output (exit 0): `TOTAL_DIFF_ROWS=0`.

```
== structural ==
all three captures: 70 unique keys, same order and set as committed
== cap1 vs committed: 0 differing key(s) ==
== cap2 vs committed: 0 differing key(s) ==
== cap3 vs committed: 0 differing key(s) ==
== cap1 vs cap2: 0 differing key(s) ==
== cap2 vs cap3: 0 differing key(s) ==
== cap1 vs cap3: 0 differing key(s) ==
```

**Keys whose reply changed between captures: none (0 of 70).**
**Keys whose change alters the form: none (0 of 70)** — vacuous because no reply changed at all,
and independently confirmed by the form census below.

Exact-text check (not just parsed equality), per sweep: `exact_text_identical=70/70`,
`whitespace_only=0`, `semantic_diff=0`.

### Form / set / exit-code censuses (identical in all four artifacts)

| artifact | int | float | custom | str | set=true | set=false | rc≠0 |
|---|---|---|---|---|---|---|---|
| committed | 44 | 5 | 13 | 8 | 70 | 0 | n/a |
| cap1 | 44 | 5 | 13 | 8 | 70 | 0 | none |
| cap2 | 44 | 5 | 13 | 8 | 70 | 0 | none |
| cap3 | 44 | 5 | 13 | 8 | 70 | 0 | none |

All 210 calls returned exit 0, so no key fell through to the `no such option` text form in any
sweep (the capture was never partially degraded), and no key ever reported `set:false` — which is
what a compositor restart onto a default config would have produced. Every declared key stayed
explicitly set for the whole window.

### Clause k re-run on the fresh captures

Using the frozen predicate's own function `capture_ok` (`c1-r40-live.py:598-615`, `FORMS` at
`c1-r40-live.py:99`):

```
cap1.jsonl: clause_k capture_ok = True  bytes=4740
cap2.jsonl: clause_k capture_ok = True  bytes=4740
cap3.jsonl: clause_k capture_ok = True  bytes=4740
committed: clause_k capture_ok = True  bytes= 4740
```

Each fresh sweep independently satisfies clause k (70 non-blank lines, each a JSON object with
`option`+`set`+exactly one of the four forms, union of forms = `{int,float,str,custom}`).

### The gradient keys (highest-risk values), stable across all three sweeps

```
{"option": "decoration:shadow:color", "custom": "ee1a1a1a 0deg", "set": true }
{"option": "general:col.active_border", "custom": "ffe68e0d 45deg", "set": true }
{"option": "general:col.inactive_border", "custom": "aa595959 0deg", "set": true }
{"option": "group:col.border_active", "custom": "ffe68e0d 45deg", "set": true }
{"option": "group:col.border_locked_active", "custom": "ee33ccff ee00ff99 45deg", "set": true }
{"option": "group:groupbar:col.active", "custom": "40000000 0deg", "set": true }
{"option": "group:groupbar:col.inactive", "custom": "20000000 0deg", "set": true }
```

Identical text in cap1/cap2/cap3. The inherited `45deg` on the three angle-less redeclarations
(`general:col.active_border`, `group:col.border_active`, `group:col.border_locked_active`)
reproduces every sweep — the provisional fact's inheritance rule is exercised on a value that was
in fact present, and the "angle only when a `deg` token is present" handler is not being fed a
different token set between sweeps. Also stable: the three empty `str` values
(`input:kb_model`, `input:kb_rules`, `input:kb_variant` = `""`) and the float set
(`0.6 / 0.75 / 0.0 / 0.4 / 0.49`), so neither empty-string rendering nor float formatting drifted.

## Interpretation and limits (declared)

- Mechanistically, `hyprctl getoption -j` reads `ConfigManager` values, not runtime window/input
  state, so byte-stability over a 2-minute window with no config reload is the expected result.
  The measurement confirms no reload, no theme switch, no compositor restart and no partial-config
  load occurred during the window; it cannot make the artifact stable across a reload (a theme
  switch would legitimately change values and is exactly the "new predicate" case in
  `registration.md:5-7`).
- Window is ~2 minutes on one host, three sweeps. This is a stability *observation*, not a
  guarantee: a value that changes on a >2-minute period (or on an event I did not trigger, e.g.
  monitor hotplug for `xwayland:force_zero_scaling`) would not be caught here. I deliberately did
  not inject any event — compositor mutation and input injection are forbidden for this seat.
- `hyprctl version` on this host reports `Hyprland 0.56.2 … commit efb50993780079460b0cbed1363e2166a2de1d9f`,
  matching the provisional host fact; the capture is pinned to that build and config state.
- No package was installed or upgraded (the `bc` gap was recorded, not papered over; `pacman` is
  paused host-wide and was not invoked). No tool channel was used this seat.

## Files written (all inside the lane, none tracked)

- `.ufo/waves/round-40/w1/ExecCaptureStable.md` — this report.
- `.ufo/waves/round-40/w1/ExecCaptureStable/cap1.raw`, `cap2.raw`, `cap3.raw` — the three requested
  captures (`key \t rc \t reply`), 70 lines each.
- `.ufo/waves/round-40/w1/ExecCaptureStable/cap1.jsonl`, `cap2.jsonl`, `cap3.jsonl` — reply payloads
  only, each sha256 `1fe39c05…` (byte-identical to the committed capture).
- `.ufo/waves/round-40/w1/ExecCaptureStable/keys.txt`, `static-table.json`, `static-table.err` —
  the 70-key list and the tool run that produced it.
- `.ufo/waves/round-40/w1/ExecCaptureStable/capture.sh`, `compare.py`, `timings.txt` — method and
  its output.

`git status --porcelain` at HEAD `e2b51d3` shows only untracked wave paths
(`.ufo/waves/round-40/w1/`, plus peers' `fetch/`, `assimilation/`, `w1.ready`); no tracked file was
touched, no index mutation, no git/jj write verb was run (read-only `status`, `rev-parse` only).
Scratch: none created outside the seat dir (no `mktemp` needed — no fixture repos in this task).

## Risks

- None to the C1 claim: the committed capture is reproducible byte-for-byte today, and clause k
  holds on each fresh sweep. The only residual is the declared one — the capture's content is a
  function of host config state, so any later reload makes it a different (newly predicated)
  artifact, not a corrupted one.
- Peer note: `w1/ConnSourcePatterns.md:12` already reports the same form census from the committed
  capture; this seat adds the temporal dimension (three sweeps) and the byte-reproduction proof.
  No overlap conflict — I did not edit that file.
