# ExecIndepB — independent C1 implementation (table-driven), round 44 w1

Seat: `ExecIndepB`, leaf. Lane `mado-shokunin`, rev `e2289516a9a857f55cda7be635933e89b931c3da` (freeze),
base `6a1a90528fe533cadee506a9fa3e9d13d15cc41f`. Host 2026-10-26. Nothing installed (no tool/version
change; system python 3.14.8 and `/usr/bin/bwrap` already present).

I did **not** read `.ufo/waves/round-44/c1/ctl-ref-tool.py.txt`. The implementation starts from the
tracked `tools/mado-geometry.py` at the freeze commit and from the frozen contract of
`quality/counters/c1-r44-geometry-states.py` (docstring) + `c1-r42-geometry.py` (the round-43 rest).

## Files written (seat-local only; no tracked file edited)

| path | sha256 | what |
|---|---|---|
| `.ufo/waves/round-44/w1/ExecIndepB/mado-geometry.py` | `8f290cab1c35b194add69afcbb3aac5af6ba1bbf611f9e04c0c7c1e8bf01ae4f` | the implementation (candidate for `tools/mado-geometry.py`) |
| `.ufo/waves/round-44/w1/ExecIndepB/fuzz.py` | `cce82e60fc10c43b4f600a53abc6e08b601b5e8dfb91cd47ac1c670ced824e8f` | differential fuzz harness (imports the frozen counter, never calls `main`) |
| `.ufo/waves/round-44/w1/ExecIndepB/receipt-r44-score.txt` | – | `PRED-C1-r44` run: 26 fixtures + 16 b4 mutants + r clause |
| `.ufo/waves/round-44/w1/ExecIndepB/receipt-fuzz.txt` | – | 2000 random + 263 adversarial, 0 disagreements |
| `.ufo/waves/round-44/w1/ExecIndepB/receipt-fuzz-mutants.txt` | – | harness teeth: 6 broken copies, 6/6 caught |
| `.ufo/waves/round-44/w1/ExecIndepB/receipt-live-*.txt`, `receipt-live-clients.json` (`sha256 983c3a1736c2a09ff84f11c79a911582d1ad87405560ec7983d16a14311cd8ed`), `receipt-live-raw.sha256`, `receipt-live-projection-invariance.txt`, `live.conf`, `project.py` | – | live `hyprctl clients -j` run + synthetic state variant; the dump is **projected** (see below), raw bytes kept as sha256 only |

`git status --porcelain` in the lane shows only untracked `.ufo/waves/round-44/w1/` (seat dirs) and the
pre-existing `l1-draft/`, `w1.ready*`; no tracked path changed. Scratch `/fast/scratch/hyaku/mado-r44/ExecIndepB`
was copied in full and then removed.

## Behaviour implemented

`tools/mado-geometry.py` gains the C1 state verdicts, as a **verdict TABLE** (ordered
`(predicate, verdict)` pairs) and a **summary suffix built from a dict**, not if/elif:

- `fsmode(client)` (seat copy `mado-geometry.py:195`): `type(f) is not int → 0`; `f == 1 → 1`;
  `f == 2 → 2`; else `0`. So `true/false`, `2.0`, `"2"`, `3`, `-1`, `null`, `[2]`, `{"internal":2}`,
  `1e999`, huge ints all give 0; only JSON integer 1 and 2 are states.
- `state_verdict(size, want, floating, mode)` (`:207`), table at `:210`:
  `(size is None, BADSIZE)`, `(mode == 2, FULLSCREEN)`, `(mode == 1, MAXIMIZED)`,
  `(not floating, TILED)`, `(size == want, AGREE)`, fall-through `DIFFER`. Order is exactly
  BADSIZE | FULLSCREEN | MAXIMIZED | TILED | AGREE | DIFFER.
- `evaluate` (`:229`) routes every matched client through the table and counts into
  `maximized`/`fullscreen`; FULLSCREEN and MAXIMIZED are matched, never differ.
- `report` (`:260`) builds `summary` as a dict (`:277`) and emits
  ` maximized=<n> fullscreen=<n>` (`:285`) between `badsize=<n>` and ` verdict=` only when
  maximized + fullscreen > 0; otherwise the line is the round-43 line byte for byte (the round-42
  counter's 37/37 fixture set, which contains no state, still passes).
- Client lines, rule lines, setup lines, exit codes (0/1/3/4) and the top verdict order
  (NO_SIZE_RULES | DIFFER | NO_MATCHING_CLIENT | OK) are unchanged.
- Docstring: the state paragraph and the narrowed TILED sentence (pseudo-tiled clients are
  floating=false and report TILED although the layout, not the rule, gave them their box) — closure D3.

## Evidence — the frozen counter

```
cd mado-shokunin && python3 -I quality/counters/c1-r44-geometry-states.py --repo . \
  --rev e2289516a9a857f55cda7be635933e89b931c3da \
  --tool .ufo/waves/round-44/w1/ExecIndepB/mado-geometry.py \
  --work /fast/scratch/hyaku/mado-r44/ExecIndepB
```
→ exit 0, `receipt-r44-score.txt`:

```
PRED-C1-r44 clause=b rc=0 selftest=124/124
PRED-C1-r44 clause=b4 sites=16 killed=16 need=12
PRED-C1-r44 clause=r rc=0 PRED-C1-r42: fixtures=37/37 tool=present verdict=TARGET_MET
PRED-C1-r44 clauses=a:1 b:1 b4:1 g:1 r:1
PRED-C1-r44: fixtures=26/26 tool=present verdict=TARGET_MET rev=e2289516a9a857f55cda7be635933e89b931c3da nonce=2956bb9059c0ef71
```

26/26 fixtures (12 nonce lattice `sgen0..sgen11` + the 14 fixed state fixtures), selftest k==n=124
(>= 80), b4 16/16 state sites killed (need 12; sites in `evaluate` 4, `report` 5, `state_verdict` 4,
`fsmode` 3 — the table predicates are all load-bearing), clause g clean, and the round-43 predicate
`PRED-C1-r42` still TARGET_MET on the same bytes (the no-harm clause). This is the **independent
second implementation**: reference is 26/26 with selftest 91/91; mine is 26/26 with selftest 124/124 —
same externally visible contract, different internal structure (table vs branch chain, dict-built suffix).

## Evidence — differential fuzz against the counter's model

`fuzz.py` imports `c1-r44-geometry-states.py` with `importlib.util` and uses `model_out_states`,
`gen_state_clients`, and the round-42 `gen_texts`/`rng_for`; it never calls the counter's `main`.
Two paths per case: the seat tool's `report()` in process (byte-exact stdout + rc) and, for every
adversarial case, the real CLI (`python3 -I tool --clients F --rules G...`, stdout bytes, rc, stderr).

```
python3 -I .ufo/waves/round-44/w1/ExecIndepB/fuzz.py --random 2000 \
  --work /fast/scratch/hyaku/mado-r44/ExecIndepB/cli
FUZZ: random=2000 random_disagreements=0 adversarial=263 adversarial_disagreements=0
FUZZ VERDICT: PASS
```

263 adversarial cases of my own (>= 200), covering: fullscreen as `10**30`, `2**63`, `-2**63`,
`2**100`, `1e999`, `NaN`, `2.0`, `1.0`, `0.5`, `-0.0`, `true/false`, `"2"`, `""`, `null`, `[]`, `[2]`,
`[[2]]`, `{"internal":2}`, `{"mode":2}`, `{"0":2}`, `{}`; duplicate keys (`fullscreen` 0→2, 2→0,
1→2, null→1; duplicate `class`, duplicate `size`); nested objects/arrays in every field; size as
floats/bools/negatives/1-element/3-element/strings/null/`NaN`/`1e999`; class/int/null/list/dict,
control characters `\u0000`/`\u0001`/`\n`, unicode, emoji, trailing spaces; `mapped` as false/0/null/
"false"/true/1; `floating` as 1/"true"/null; address as int/null/bool; rules with tabs, CRLF, tight
`windowrule=`, leading/trailing spaces, `windowrulev2`, `#` comment, `(?i)`, 200- and 201-character
regex, escaped regex, duplicate size rules across files, three files, float-only and empty files;
malformed documents (`{}`, `[1]`, `""`, `\xff`, `[`, `null`, `"x"`, BOM, trailing garbage); a
50-client cloud with all four modes; empty list + empty rules. Zero disagreements, so the
disagreement list is empty.

Harness teeth (a fuzz that cannot fail proves nothing): six deliberately broken copies of the seat
tool in scratch, each run through the same harness → 6/6 caught (`receipt-fuzz-mutants.txt`), e.g.
`M1-mode2-flip` (predicate `mode == 2` → `!=`) 166/300 random + 308 adversarial disagreements, and the
printed minimised inputs are genuinely minimal (`[{"class": "a.b", "size": [820, 600]}]` against one
`windowrule = size 800 500, match:class a\.b` line). The minimiser (drop rule lines, drop rule files,
drop clients, drop client keys, re-checking every step) is therefore exercised.

Live read (allowed subset, read-only): `hyprctl clients -j` on this host gave 3 clients, all
`fullscreen: 0`, `floating: false`; the tool reports `verdict=NO_MATCHING_CLIENT` exit 3 with an empty
stderr (`receipt-live-nomatch.txt`). The synthetic variant of that same dump (first two clients
`class=org.omarchy.gkeep`, `fullscreen` 2 and 1) reports `verdict=FULLSCREEN` and `verdict=MAXIMIZED`
under the 420x500 rule and `matched=3 … maximized=1 fullscreen=1 verdict=OK`
(`receipt-live-synth.txt`) — the round-43 tool would have printed DIFFER/TILED there.

Privacy projection (SKILL.md:332: clients for length/tags, never window titles — raised by seat
`SentLiveReads` after my first version committed the raw dump as a seat receipt). The dump is stored
only as the projection `address, mapped, class, floating, size, at, monitor, fullscreen,
fullscreenClient, fullscreenHandler` (`project.py`, applied in place; `title`, `initialTitle`,
`pid`, `xdgDescription`, `workspace`, tags and the other 21 keys are dropped). The raw bytes are not
kept anywhere; their sha256 is recorded (`receipt-live-raw.sha256`:
`5ead917690b8254a48c3e8fe264d22c4c075bade557bb43b745e5923506e74a0`). The projection is
evidence-preserving: re-running both receipts over the projected dump gives byte-identical stdout,
the same exit codes (3 and 0) and empty stderr (`diff` clean), because the tool reads only
address/class/floating/mapped/size/fullscreen. `fuzz.py` never captures live data — every client in it
comes from the counter's generators — so no other live capture exists in the seat dir.

Cross-seat corroboration (verified here, not taken on report: `sha256sum` over both files): seat
`ExecLiveHost` captured the same session independently and projected it with the same field set; their
`w1/ExecLiveHost/live-clients.json` and my `receipt-live-clients.json` are **byte-identical**
(`983c3a1736c2a09ff84f11c79a911582d1ad87405560ec7983d16a14311cd8ed`, 1108 bytes each), while the two raw
dumps differ (mine `5ead9176…`, theirs `931ed70a…`, 2619 bytes each, per their
`raw-dumps.sha256`). Two independent captures + one deterministic projection ⇒ every field the tool
reads (address, class, floating, mapped, size, fullscreen, and the other kept fields) was stable across
both captures, and the raw delta lives entirely in the dropped session material — which is the reason
the projection loses nothing evidentiary. Recorded by `SentLiveReads` as S1 in
`w1/SentLiveReads/findings.md:79-81` and by `ExecLiveHost` as F7.

## Risks / residual defects

1. This is an implementation, not an oracle: the tool holds a model of the contract (frozen residual of
   `PRED-C1-r44`). Independence here means a different internal structure, a selftest written from the
   contract, and a differential fuzz — not an independent source of truth.
2. b4 counts state sites only inside functions that name `fullscreen`; my 16 sites are concentrated in
   four functions (`fsmode`, `state_verdict`, `evaluate`, `report`). A future edit that moves state logic
   into an unnamed helper would silently weaken the clause (vacuous-but-satisfied path in the predicate).
3. Random-lattice cases are compared in process (both sides are pure functions of bytes); only the 263
   adversarial cases are replayed through the real CLI. CLI-level hazards (setup lines, exit codes,
   stderr) are therefore proven on 263 cases plus the counter's own 26 fixtures, not on all 2000.
4. The docstring narrowing for pseudo-tiled clients (D3) is documentation; the pseudo-tiled licence is
   a compositor fact this instrument does not score.
5. `1e999`/`NaN` reach the tool only through Python's permissive `json.loads`; a stricter JSON parser
   would reject them as `bad_json`. Both model and tool behave identically, so the fuzz is neutral
   here, but the observation is about Python's parser, not about Hyprland's output.
6. Nothing in this seat fixes the routed round-43 closure defects D1, D2, D4, D5, D6, D7 — out of scope
   for C1 (the D3 sentence is carried in the tool docstring only).

## Blockers

None.

## Hand-off — what the L1 should run after integration

1. Copy `.ufo/waves/round-44/w1/ExecIndepB/mado-geometry.py` over `tools/mado-geometry.py`, then run the
   counter at the data commit WITHOUT `--tool` (it reads `REV:tools/mado-geometry.py`):
   `python3 -I quality/counters/c1-r44-geometry-states.py --repo . --rev <data-rev>` → expect
   `fixtures=26/26 … verdict=TARGET_MET`, exit 0.
2. Re-run `quality/counters/c1-r42-geometry.py --repo . --rev <data-rev>` → expect 37/37 (the round-43
   contract, unchanged fixture set).
3. Occam note for the integrator: the reference scored 26/26 with a 91-case selftest; this one scores
   26/26 with 124 cases. If the integrator prefers the smaller diff, the reference wins; both are
   contract-equal on every fixture the frozen counter has.
