# ExecSeedSweep — PRED-C1-r45 determinism and seed independence (round 45, w1)

Status: DONE. Seat dir `.ufo/waves/round-45/w1/ExecSeedSweep/` (full report `report.md` + receipts there).

Scored: scratch clone `979fcfc0f013905898dacafed6d441651ffc0c09` = freeze `22a8dedd` + the reference
`.ufo/waves/round-45/l1-draft/mado-monitors.py` installed as `tools/mado-monitors.py` unchanged
(sha256 `c6ac5fc2…843726be`). Counter `quality/counters/c1-r45-monitors.py` sha256 `c69ddee4…9213f34`.
Command shape: `python3 -I <counter> --repo <clone> --rev HEAD --work <scratch> --seed N`.

## Result

**No non-MET seed exists, so there is no failing fixture to attribute. 1000/1000 seeds MET.**

| block | runs | result |
|---|---|---|
| seeds 1..150 (asked) | 150 | 150/150 `fixtures=49/49 selftest=ok readonly=ok tool=present verdict=TARGET_MET`, exit 0 |
| seeds 151..1000 (extension) | 850 | 850/850 identical, 0 FAIL lines, 0 stderr bytes |
| seed 45 × PYTHONHASHSEED 0/1/random + 40 repeats each | 123 | 123/123 MET; **all logs one md5** `706fcfd5b947c687f925666f197f7f56`, same file as the bare default-seed run (registration D4 measured) |
| replay of seeds 1..150 | 150 | 150/150 logs byte-identical to the first sweep |
| seed 45 timing | 5 | 1067 / 1087 / 1101 / 1112 / 1139 ms serial (median 1101); first run of session 803 ms |

`readonly=ok` in every scored run (no `hyprctl`/`journalctl`/`wlr-randr`/`wayland-info` marker).

## Why no seed can fail (census over all 1000 seeds)

* Names are drawn **without replacement** from 6 prefixes × digits 1-9: duplicate-name events 0, and a name
  that is a *prefix* of another 0 (single digit ⇒ cross-prefix prefixes impossible).
* A name inside the description: **0** — every name contains `-`, no description does, so `{D}` cannot
  perturb exact-name or `desc:` matching.
* Placeholders are brace-delimited and no substituted value contains braces ⇒ no cascading substitution.
* Only reachable collision class: **substring, 13 events / 1000 seeds**, always `DP-n` ⊂ `eDP-n` (36, 40, 140,
  201, 316, 430, 444, 540, 714, 755, 849, 890, 992). Harmless: `effective()` selects by exact equality or
  `desc:` prefix, never substring — measured clean at seed 36, where `A=DP-5 B=eDP-1 C=DP-1`.
* 999 distinct name triples / 1000 distinct descriptions; seeds 533 and 579 share `A/B/C` with different `{D}`
  and both are MET (the description alone changes no verdict).

## Hash-seed note the registration wording does not cover

`python3 -I` sets `ignore_environment`, so **`PYTHONHASHSEED` is not inherited by the counter or by the tool it
forks**: two `PYTHONHASHSEED=0 python3 -I` runs gave different `hash("mado")` (2071948775076071683 vs
6278822340334659941), while without `-I` the variable is honoured. The three named runs therefore sample the
same unpinned distribution; determinism was established directly instead:

* tool source: `set(` 0, `frozenset` 0, `.items()` 0, `.keys()` 0, `random` 0 — no unordered iteration;
* all 49 fixtures through the tool with `PYTHONHASHSEED=0` vs `1`, `-I` dropped: **0/49** differ
  (stdout + stderr + exit code);
* counter process under pinned 0 vs 1 (no `-I`): identical full-log md5.

Also environment-clean: `GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE=/nonexistent` → MET (counter strips `GIT_*`),
run from `/` → MET, default seed == `--seed 45` byte-identical.

## Teeth (does the seed sweep discriminate anything?)

One mutant clone, rev `b42dd109`, tool sha256 `73b202af…f1fcbce8`: reference line 354
`elif sel == name:` → `elif sel in name:` (selector by substring, one line, nothing else changed):

* **survives the default seed 45** (`49/49 TARGET_MET`);
* dies at exactly **7 of 1000 seeds — 40, 140, 430, 444, 714, 849, 992** (`47/49`, exit 1):
  `B ⊂ A` seeds fail `mirror-agree` + `mirror-missing` (`name="eDP-4" rule=2 … verdict=DIFFER`), `C ⊂ A`
  seeds fail `fallback-first-empty-and-named` + `unruled-only` (expected `UNRULED` became `DIFFER`);
* the measured set equals the analytic set `{C in A} ∪ {B in A}` over `names(1..1000)` — fully explained.

So the sweep has measured discriminating power, but the fixture set itself never pins an `eDP-n`/`DP-n` pair in
a harmful role: at 993/1000 seeds that defect class passes. **A default-seed green run is not evidence of
exact-match semantics.** Advisory (nothing frozen touched): a fixture `monitor = DP-1, 1920x1080@60, 0x0, 1`
against dump `[eDP-1]` gives the reference `UNRULED`/`NO_MATCHING_MONITOR`/rc 3 and the mutant `AGREE`/`OK`/rc 0
(`advisory-probe.txt`) — one such fixture would catch it at every seed while keeping the reference MET.

## Risks / residuals

1. Discrimination is seed-fractional (7/1000 for selector confusion); reading the fixtures as encoding
   exact-match semantics is true only at a rate.
2. Seed independence covers the four name/description placeholders only; modes, positions, scales,
   transforms, `desc:` text layout and all setup paths are fixed text and were not varied.
3. Hash determinism rests on construction + 123 identical logs, not on pinning — `-I` defeats pinning.
4. `names()` depends on CPython's Mersenne Twister; only 3.14.8 exercised. `name-anchors.txt` records
   seeds 1/36/40/45/46/140/150/430/444/714/849/992 as anchors for any interpreter change.
5. Timing measured on this host under fleet load (60+ peer seats) — ±10% noise.
6. The sweep scores the reference tool only; whether the contract matches Hyprland is out of this seat.

## Safety / scope

Wrote only `.ufo/waves/round-45/w1/ExecSeedSweep/` (report + 9 receipts) and this file. No frozen counter,
control, registration, reference, pins or lane git index touched; no fleet or `.ufo/state` write; no pacman;
no compositor call and no `hyprctl` at all in this seat; no session material read; fixture clones under
`/fast/scratch/hyaku/mado-r45/ExecSeedSweep` with `--show-toplevel` asserted per clone and scratch identity
only, then scratch deleted after receipts were copied here. Tooling installed: none (system Python 3.14.8).
