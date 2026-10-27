# MutC1Tool — C1 warm-cache mutation test (W2 FALSIFY)

Round 48, wave `w2`, seat `MutC1Tool`. Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`, base
`579f694b45c797a9c39761fdb4f9e0a1b71b3585`, frozen instruments read from `quality/counters/`, draft bytes from
`.ufo/waves/round-48/l1-draft/`. I wrote only `.ufo/waves/round-48/w2/MutC1Tool/` and this report; nothing tracked in
the lane, the registry, the counters, the draft or a sibling seat was touched.

**Target of the seat.** Does the frozen C1 predicate (`PRED-C1-r48`) reject a plausible tool that gets one warm-cache
rule wrong? One behaviour mutated at a time, eight mutants of the l1-draft tool, each scored by the frozen counter
verbatim.

## 1. Result

* Baseline (the l1-draft `tools/mado-terminal.py`, unmutated): `cold=190/190 warm=204/204 explained=394/394
  generated=230/230 selftest=ok readonly=ok tool=present verdict=TARGET_MET` (nonce 4848, exit 0, 147 s).
  The instrument and the draft are sound, so a surviving mutant is a real gap.
* **7 of 8 mutants are killed; 1 survives with `TARGET_MET`.** The survivor is `m4-break-cmdv`: `_execable()` returns
  existence instead of `os.access(..., os.X_OK)`, i.e. the tool treats `command -v <cached cmd>` as a *PATH/existence*
  question instead of an *executability* question. It meets every clause, on two nonces.
* **Survivor → fixture gap (G1, §4).** No fixture, and no generator case, in the frozen set ever makes a candidate
  command exist without the executable bit, so the pin's `command -v` gate (pin x:274 for the cache, x:964 for
  `Exec[0]`) is unscored on both the warm and the cold path. A one-fixture, one-digest repair, measured: with it the
  draft stays `TARGET_MET` and `m4` becomes `TARGET_MISSED` on `w` and `x`.

## 2. Method

Every count ran on scratch repos, never on the lane:

* `D=$(mktemp -d -p /fast/scratch/hyaku/mado-r48/MutC1Tool/m) && git -C "$D" init -q`, then the counter's own
  dependency closure copied in at the frozen bytes — `tools/mado-terminal.py` (l1-draft), `quality/counters/
  {c1-r48-terminal-cache.py, c1-r48-fixtures.json}` (l1-draft), `quality/counters/c1-r47-fixtures.json` and
  `.ufo/waves/round-47/fetch/xdg-terminal-exec` (lane sha256 `89f2be9a…`, asserted equal to the counter's
  `PIN_SHA256`). `git rev-parse --show-toplevel` asserted `= D` before every commit.
  A whole-lane `git clone` was rejected: the lane tracks files above 1 MiB, which the mandated per-file guard kills
  (`error: unable to write file … huge_bash_eval_comment.jsonl`), so the replay tree holds exactly the bytes the
  counter reads (`rev`/`blob` for the tool, `beside()` for fixtures, `lane_root()/PIN_REL` for the pin).
* Each mutant: `git clone -q --shared` of that base repo, one `edit`, `git commit`; `python3 -I -c
  'compile(open(...).read(),...)'` syntax check; then the frozen counter
  `python3 -I quality/counters/c1-r48-terminal-cache.py --repo <mutant> --rev HEAD --work <scratch> --nonce 4848`.
  The eight runs were issued concurrently (32-core host, 282 s wall). Nothing but the tool's one rule differed
  (`git diff --numstat` 1–3 lines per mutant; `diffs/*.diff`).
* File-size guard, recorded honestly: `ulimit -f 2048` (1 MiB/file) is the writer bound for everything I authored
  (largest authored file 76 037 B, `out/m3-never-warm.txt`). The frozen counter itself copies `/usr/bin/gawk`
  (1 274 872 B) into its sandbox, so the counter invocation runs under `ulimit -f 16384`; the largest file anywhere in
  my scratch is that gawk copy (1 274 872 B), total scratch 19 MiB (2 GB budget). Scratch was removed after the
  receipts were copied (`§7`).

## 3. Mutants and clause results (frozen counter, nonce 4848, exit code in parentheses)

| # | mutant (one rule undone) | diff | s | f | w | x | g | r | verdict |
|---|---|---|---|---|---|---|---|---|---|
| — | baseline (l1-draft tool) | — | ok 69/69 | 190/190 | 204/204 | 394/394 | 230/230 | 0 | **MET** (0) |
| m1 | `skip-hash`: cache accepted without comparing `gen_hash()` | `if self.gen_hash() != fields[0] or not self.command_v(fields[1]):` → `if not self.command_v(fields[1]):` | fail 67/69 | 190/190 | **190/204** | **351/394** | 230/230 | 0 | MISSED (1) |
| m2 | `trust-cache`: hash checked, cached command not resolved | same line → `if self.gen_hash() != fields[0]:` | fail 68/69 | 190/190 | **202/204** | **390/394** | 230/230 | 0 | MISSED (1) |
| m3 | `never-warm`: `select()` never reads the cache | `read_cache()` branch → `self.cache = "absent"` | fail 59/69 | 190/190 | **144/204** | **240/394** | **210/230** | 0 | MISSED (1) |
| **m4** | **`break command -v`: existence instead of executability** | `return os.access(p, os.X_OK)` → `return True` | ok 69/69 | 190/190 | 204/204 | 394/394 | 230/230 | 0 | **MET (0)** |
| m5 | `line50`: cache line cap trips at 51, not 50 | `if n == 50:` → `if n == 51:` | fail 68/69 | 190/190 | 204/204 | **393/394** | 230/230 | 0 | MISSED (1) |
| m6 | `ignore-cached-args`: hit loads id/path/action only | `… = fields[2:10]` → `… = fields[2:5]` | fail 67/69 | 190/190 | **186/204** | 394/394 | **226/230** | 0 | MISSED (1) |
| m7 | `lower-desktop`: hash of the lowercased desktop | `…XDG_CURRENT_DESKTOP", "")` → `….lower()` | ok 69/69 | 190/190 | **145/204** | **308/394** | **218/230** | 0 | MISSED (1) |
| m8 | `force-hit`: any parsed cache reports `cache=hit` (selection still cold) | +`if self.cache != "absent": self.cache = "hit"` | ok 69/69 | 190/190 | 204/204 | **330/394** | 230/230 | 0 | MISSED (1) |

`m4` re-scored at nonce 777001: `cold=190/190 warm=204/204 explained=394/394 generated=230/230 selftest=ok
readonly=ok tool=present verdict=TARGET_MET` — the survival is nonce-independent, and by construction (`§4`).

Killing fixtures (exact lists in `out/*.txt`, counts here):

| mutant | w failures | first ids | x failures |
|---|---|---|---|
| m1 | 14 | M-12, M-16, v2-wi-04-entry-deleted, v2-wi-15-data-home, v2-wi-22-apps-dir-renamed, v2-wi-25-dir-entry-became-dir, v2-mf-03/04/06/07/08/14/15, v2-mf-18-exec-empty-11 | 43 |
| m2 | 2 | M-06, v2-wi-17-exec-stub-gone | 4 (those two + v2-wi-29-cache-line2-empty, v2-wi-30-cache-line2-gone) |
| m3 | 60 | every WARM-DIFFERS hit (W-03…W-14, v2-wd-*) + v2-ws hits | 154 |
| m4 | — | — | — |
| m5 | 0 | — | 1: M-17 (want `invalid`, got `stale`) |
| m6 | 18 | W-06, W-07, v2-wd-06/07/08/09/10/20/24/27/29/32/33/36, v2-ws-06/07/13, v2-mf-28-crlf-accepted | 0 |
| m7 | 59 | every primed hit (hash rebuilt from the lowered desktop) | 86 |
| m8 | 0 | — | 64: every fixture whose state is not `hit`/`absent` |

## 4. G1 — surviving realistic mutant: `m4` (executability vs existence), and the measured repair

**The rule m4 breaks.** The pin gates a cache on `[ "$XTE__HASH" = "$xte__cached_hash" ] && command -v
"$xte__cached_cmd" > /dev/null` (pin x:274) and an entry on `command -v "$XTE__EXEC0" > /dev/null` (pin x:964). Bash's
`command -v` succeeds only for an *executable* file; m4 accepts any existing non-directory. Realistic trigger: the
terminal binary exists but lost `+x` (a package update, a restored backup, a chmod) — exactly the class of stale cache
the claim is about, and one the md5 cannot see because the hash covers only the list and application paths.

**Why the frozen suite cannot see it.**

* Fixtures: the only `after.modes` in the whole 204-item warm set is `v2-wi-21-mode-change`
  (`{"home/.local/share/applications/foot.desktop": 489}` — a `.desktop` file, not a command), and the 190 cold
  fixtures carry no `after` at all. No fixture writes a path that is also a candidate command
  (`files ∩ exec = ∅` in both sets).
* Generators: `add_execs()` chmods every generated binary 0755, `gen_case`/`gen_warm_case`/`gen_warm_text` never
  remove or demote a mode, and `corrupt_cache()` uses `foot`/`x` as line 2 of caches that are already invalid for
  other reasons. So no nonce can produce the case (m4 also passed `g` 230/230 at two nonces).

**Measured repair (one fixture, one digest).** `probe/proposed-fixture-W-GAP-CMDV-NONEXEC.json`, built from the frozen
`W-10` (a primed hit: warm `foot`, cold `kitty`) plus one `after` key:

```json
"after": {"files": {"home/.config/hyprland-xdg-terminals.list": "kitty.desktop\nfoot.desktop\n"},
          "modes": {"bin/foot": "420"}, "mtime": 1600000000},
"state": "stale", "class": "WARM-SAME", "expect": {"rc": 0, "stdout": "kitty\n"}, "cold": {"rc": 0, "stdout": "kitty\n"}
```

`bin/foot` still exists and the hash is unchanged (it never covers `bin/`); the terminator and the field lines are
untouched, only the exec bit moves. Measured through the counter's own machinery (`probe/gap-cmdv.py`, which calls
`Box`/`prepare`/`run_case`/`explain_case`):

```
draft : w_ok=True  state=stale oracle=(0,'kitty\n') cold=(0,'kitty\n') x_ok=True
mutant: w_ok=False state=stale oracle=(0,'kitty\n') cold=(0,'kitty\n')
        x_why=explain got=('foot.desktop', '…/foot.desktop', 'foot', 'hit', 'OK', 0)
                    want=('kitty.desktop', '…/kitty.desktop', 'kitty', 'stale', 'OK', 0)
```

Scored by a probe copy of the frozen counter whose *only* edit is `SHA256_WARM` → the 205-item file
sha256 `a0893b5b…` (`probe/instrument-patch.txt`; no clause, threshold, pin or nonce touched):

```
draft : cold=190/190 warm=205/205 explained=395/395 generated=230/230 … verdict=TARGET_MET      (out/gap-draft.txt)
m4    : cold=190/190 warm=204/205 explained=394/395 generated=230/230 … verdict=TARGET_MISSED   (out/gap-m4.txt)
        clause=w fixture=W-GAP-CMDV-NONEXEC FAIL oracle=(0,'kitty\n') tool=(0,'foot\n')
        clause=x fixture=W-GAP-CMDV-NONEXEC FAIL
```

The added fixture passes its own premise (state `stale`, cold twin recorded, `WARM-SAME` requires cold == expect) —
the run reported no `SETUP`. The draft tool stays `TARGET_MET` on the larger set, so the repair does not narrow the
predicate and does not ask the draft to change.

**Cold side, same rule.** `probe/gap-execmode-cold.py` (one tree, no cache: `foot.desktop` then `kitty.desktop`,
`bin/foot` 0644, `bin/kitty` 0755):

```
draft : f_ok=True  state=absent oracle=(0,'kitty\n')
mutant: f_ok=False state=absent oracle=(0,'kitty\n') tool=(0,'foot\n')
```

The pin skips the entry whose `Exec` word does not resolve (x:964) and selects `kitty`; m4 selects `foot`. The cold
set is frozen as "the 190 unchanged round-47 fixtures", so I do **not** recommend adding this case; the warm fixture
alone kills m4 and keeps clause `f` byte-identical.

**Recommendation to the L1 (pre-data, allowed by registration.md).** Re-register the C1 instrument as a new version
before any data commit: 205 warm fixtures (the frozen 204 + `W-GAP-CMDV-NONEXEC`), `SHA256_WARM` updated, then re-run
the complete control set (`w1/ExecControlsC1`'s 20 controls) plus `reference.py`, `base`, `always-cold` against it.
If instead the L1 accepts the registration as frozen, record explicitly that the executability half of `command -v`
is an admitted residual — the claim text ("the cached command resolves") is then stronger than what the predicate
measures. I did not narrow the predicate: this is reported as a pre-data hole, and the frozen bytes were scored
unmodified in every row of §3.

## 5. Secondary teeth observations (non-blocking; the mutants are killed, but by less than one would assume)

* **T1 — the 50-line cap is scored as a label, not as an answer.** `m5` (`n == 50` → `n == 51`) misses on exactly one
  fixture, `M-17`, and `w` stays 204/204 and `g` 230/230. `M-17` is a *literal* 50-line cache, terminator on line 50,
  hash `"0"*32`: anything that reads it is `stale`, so the correct `invalid` and the mutant's `stale` yield the same
  cold answer. `corrupt_cache()`'s line-limit case is the same shape (62 lines, hash 0, invalid either way). Making the
  cap answer-bearing needs a cache whose hash is valid: prime a hit whose cached selection differs from cold (the
  `W-10` shape), then pad the cached command so the terminator sits on line 50 — the pin calls the cache invalid and
  prints the cold selection, the off-by-one accepts it and prints the cached command, padding lines included.
* **T2 — clause `x` cannot see the cached argument fields.** `m6` (drops `execarg/appidarg/titlearg/dirarg/holdarg`
  from a hit) scores `x` 394/394: `explain` compares selected/path/cmd/cache/verdict, and `cmd` is the cache's line 2,
  not the argument words. `w` (18 fixtures) and `g` (4) kill it, so the instrument is safe, but a reader who trusts
  `x` to cover "the whole cached command" would over-read it.
* **T3 — the line-2 gate has two answer-level fixtures.** `m2` (hash checked, cached command not resolved) is killed
  by `w` on `M-06` and `v2-wi-17-exec-stub-gone` only; `v2-wi-29-cache-line2-empty` and `v2-wi-30-cache-line2-gone`
  are answer-inert (the cached entry equals the cold entry) and only move the state label. Sufficient, but thin: the
  strong pair both work by *removing* the binary (`exec_remove`), not by demoting it.
* **T4 — a pure state-label lie is invisible to `w` and `g`.** `m8` (`cache=hit` whenever a cache parses) is killed
  by `x` alone (64 fixtures) with `w` 204/204 and `g` 230/230. Correct, because `x` is in the predicate; noted so the
  freeze does not read `w` as a state clause.
* **T5 — clause `s` is not the only kill, and must not be relied on.** Five mutants also break the tool's own
  hermetic selftest (`m1` 67/69, `m2` 68/69, `m3` 59/69, `m5` 68/69, `m6` 67/69), and a submitter tunes its own
  selftest. Excluding `s`, the fixture clauses still kill `m1`, `m2` (thinly), `m3`, `m6`, `m7`; `m5` only through
  `x`; `m4` not at all. `m3`'s own count is also 59/69, below the `N ≥ 60` floor as well as not `N/N`, so a coherent
  never-warm tool has to carry its own suite of warm-shaped cases to clear `s`.

## 6. What the frozen set does carry (so the report is not one-sided)

All 190 cold fixtures are untouched and `m4` is the only cold-side hole found. The warm set is genuinely
answer-carrying where it counts: `m3` (60 w-failures), `m7` (59) and `m1` (14) are killed by *output*, on both root
variants, with `readonly=ok` and `trips=0` in every run; the state ladder (`hit 90 / stale 47 / invalid 17 /
disabled 5 / absent 40`) is exercised by `x` on 394 fixtures; `WARM-DIFFERS` (48) and the primed `after`-edit family
carry the warm-vs-cold distinction the claim needs.

## 7. Evidence inventory (all paths under `.ufo/waves/round-48/w2/MutC1Tool/`)

| file | what it is |
|---|---|
| `out/base.txt` | baseline counter output, `verdict=TARGET_MET`, nonce 4848 |
| `out/m{1..8}-*.txt` | the eight mutant counter outputs (clause lines + final line) |
| `out/m4-n777001.txt` | m4 at a second nonce: `TARGET_MET` again |
| `out/gap-draft.txt`, `out/gap-m4.txt` | the 205-fixture probe instrument: draft MET, m4 MISSED |
| `clause-summary.txt` | `clause=a/s/f/w/x/g/r` + final line of all 12 runs, prefixed by run |
| `diffs/*.diff` | the eight one-rule patches, as applied |
| `mutant-sha256.txt` | sha256 of every mutant tool (draft `1dfde36c…`; m1 `981a2d5d…`, m2 `a5d8d21d…`, m3 `506c4708…`, m4 `9c70fbf2…`, m5 `4509b096…`, m6 `e57e0512…`, m7 `4c440ac7…`, m8 `b1b81996…`) |
| `probe/gap-cmdv.py`, `probe/gap-cmdv.json` | warm-side probe and its measured record |
| `probe/gap-execmode-cold.py`, `probe/gap-execmode-cold.json` | cold-side probe and its measured record |
| `probe/proposed-fixture-W-GAP-CMDV-NONEXEC.json` | the fixture clause `w` would need, exactly as measured |
| `probe/instrument-patch.txt` | the single `SHA256_WARM` edit of the probe counter and why nothing else changed |
| `run.sh` | reproduction: base repo, baseline score, eight mutants, nine counters (nonce 4848) |

Scratch `/fast/scratch/hyaku/mado-r48/MutC1Tool/` (19 MiB peak, largest file the counter's `gawk` copy, 1 274 872 B)
held the repos, the fixture trees and the runs; receipts were copied here before it was removed. `/tmp` was not used.

## 8. Risks and blockers

No blocker; nothing here prevents the wave from closing. The one decision the L1 owns is G1: re-register the C1
instrument with the added warm fixture (recommended, measured to keep the draft `TARGET_MET` and to reject m4) or
freeze as-is and record the executability half of `command -v` as a residual of `PRED-C1-r48`. I did not score the
frozen instrument with modified fixture bytes: every §3 row used the frozen counter and the frozen 204/190 sets.
