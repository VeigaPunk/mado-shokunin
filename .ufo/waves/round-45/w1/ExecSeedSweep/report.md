# ExecSeedSweep — PRED-C1-r45 determinism and seed independence (round 45, w1)

Seat: ExecSeedSweep (leaf). Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Freeze `22a8dedd02f507689c567777e0f20b5e645c8ce0`; base `0c89478af821a6424c9ac922eafe02e39630cf4f`.
Scratch: `/fast/scratch/hyaku/mado-r45/ExecSeedSweep` (deleted at seat end; receipts below are in this directory).

Target set by the seat spec: a scratch clone with the reference `.ufo/waves/round-45/l1-draft/mado-monitors.py`
installed as `tools/mado-monitors.py` (committed there), the C1 counter at seeds 1..150 plus 3 runs at seed 45
with `PYTHONHASHSEED=0/1/random`, every non-MET seed attributed to a fixture and a mechanism, and one run timed.

**Answer: no non-MET seed exists. 1000/1000 seeds MET, 150/150 repeat runs MET, 150/150 replay-identical.
There is no seed to attribute, and the analysis below shows why none is reachable.**

## What was run

| item | command | rev / pinned object |
|---|---|---|
| pos clone | `git clone -q --shared --no-checkout <lane> $D; git -C $D checkout -q --detach 22a8dedd; cp l1-draft/mado-monitors.py $D/tools/; git -C $D add -A; git -C $D -c user.name=… commit` | `979fcfc0f013905898dacafed6d441651ffc0c09` |
| tool blob | `sha256sum $D/tools/mado-monitors.py` | `c6ac5fc2d35e40b34dcf031940222fbe5ec5f0ce4b07d6a41866b196843726be` (= l1-draft byte-for-byte, `cmp` clean) |
| frozen counter | `sha256sum quality/counters/c1-r45-monitors.py` | `c69ddee44a9fa3c442b910541038a9440ac72c2b5f21fe4899cb8f5df9213f34` |
| score | `python3 -I …/c1-r45-monitors.py --repo $D --rev HEAD --work $S/work --seed N` | `-I` throughout, as the counter's own contract runs |

## Findings

### F1 — seeds 1..150: 150/150 TARGET_MET, exit 0, fixtures 49/49 each (target)

`seq 1 150 | xargs -P 12`, one counter process per seed, shared `--work` (each run makes its own `mkdtemp`).
Every run: `fixtures=49/49 selftest=ok readonly=ok tool=present verdict=TARGET_MET`, exit 0. No `FAIL` line in
any of the 150 logs, no non-empty stderr. Receipt: `sweep-reference.txt` (lines 5-154).

### F2 — seeds 151..1000 (extension): 850/850 TARGET_MET

Same command over 151..1000: 850 exit 0, all `fixtures=49/49 … verdict=TARGET_MET`, 0 FAIL lines, 0 stderr
bytes. Total across F1+F2: **1000/1000 seeds MET**. Receipt: `sweep-reference.txt` (lines 155-1004); wall 91.9 s
at `-P 12`.

### F3 — PYTHONHASHSEED 0/1/random at seed 45: 123/123 MET, all logs byte-identical

3 named runs (0, 1, random) plus 40 further runs per setting (120): all `fixtures=49/49 … TARGET_MET`,
exit 0. All 123 full logs hash to the same md5 `706fcfd5b947c687f925666f197f7f56`; the bare-run log
(no `--seed`, i.e. default 45) is that same file, so the default-seed reproduction demanded by registration
D4 is measured, not assumed. Receipt: `hash-battery.txt`.

Note the mechanism: the counter is invoked `python3 -I`, and **`-I` sets `ignore_environment`, so
`PYTHONHASHSEED` is not inherited by the counter or by the tool it forks**. Measured on this host:

    PYTHONHASHSEED=0 python3 -I -c … -> ignore_environment 1 hash 2071948775076071683
    PYTHONHASHSEED=0 python3 -I -c … -> ignore_environment 1 hash 6278822340334659941  # different, same env

So the three named runs measure the same distribution as unpinned runs; hash-order determinism therefore had
to be established directly, which F4 does.

### F4 — the hash pin is irrelevant because nothing iterates unordered

* Tool source census (`grep`-equivalent count over `tools/mado-monitors.py`): `set(` 0, `frozenset` 0,
  `.items()` 0, `.keys()` 0, `random` 0. All output-bearing containers are lists or insertion-ordered dicts
  (`KEYS` tuple, `rules` list, dump order preserved).
* Direct test: all 49 fixtures run through the tool with `PYTHONHASHSEED=0` and `PYTHONHASHSEED=1`, `-I`
  **dropped** so the variable is honoured: 0/49 differ in stdout, stderr or exit code.
* Counter process itself under `PYTHONHASHSEED=0` vs `1` (no `-I`): full logs md5-identical
  (`logs/nohI/hs0.log` == `hs1.log`).

Receipt: `determinism-checks.txt` items 5-7, `hash-battery.txt`.

### F5 — replay and environment determinism: byte-identical logs

* Seeds 1..150 scored a second time: **150/150 logs byte-identical** to the first sweep (`cmp` loop).
* Default seed == explicit `--seed 45`: byte-identical logs.
* `GIT_DIR=/nonexistent GIT_WORK_TREE=/nonexistent GIT_INDEX_FILE=/nonexistent` → `TARGET_MET` (the counter
  strips ambient `GIT_*`, `ENV_GIT`), and running from `/` → `TARGET_MET`.
* Same name triple from two seeds (533 and 579 both `A=USB-C-6 B=DVI-D-3 C=eDP-7`, different `{D}`): both
  `TARGET_MET`, i.e. the description never changes a verdict on its own.

Receipt: `determinism-checks.txt` 1-4 and 8.

### F6 — why no seed can fail: the name space has no reachable collision class

The counter derives `{A} {B} {C}` from 6 prefixes × digits 1-9 (54 candidates) **without replacement**
(`names()`: `while len(picked) < 3: … if n not in picked`), and `{D}` = vendor + 6 chars from
`A-Z0-9` (no hyphen, no space except after the vendor). Census over all 1000 seeds
(`collision-census.txt`):

* duplicate name events: **0**;
* a name that is a prefix of another name: **0** (all names are `prefix + one digit`, so cross-prefix
  prefixes cannot occur and digits are single);
* a name inside the description: **0** — every output name contains `-`, no description does, so
  `description.startswith(selector)` and `selector == name` cannot be perturbed by `{D}`;
* a description containing a *placeholder* or vice versa: impossible, placeholders are brace-delimited and
  no substituted value contains `{`/`}`;
* **substring** (neither prefix nor equal): **13 events in 1000 seeds**, all of the single form
  `DP-n` ⊂ `eDP-n` — seeds 36, 40, 140, 201, 316, 430, 444, 540, 714, 755, 849, 890, 992;
* distinct name triples 999/1000 (seeds 533/579 share one), distinct descriptions 1000/1000.

The substring class cannot change a verdict, because rule selection is exact equality or `desc:` prefix
(`effective()`), never substring — measured at the 13 substring seeds themselves (all `TARGET_MET`), and at
seed 36 explicitly (`A=DP-5 B=eDP-1 C=DP-1`: the `DP-1`/`eDP-1` pair is present and the run is clean).

### F7 — the seed sweep does have teeth, but a single default seed does not

To test that seed variation discriminates *anything*, one mutant clone was scored: the reference with line
354 `elif sel == name:` → `elif sel in name:` (selector matched by substring instead of equality; nothing
else changed). Rev `b42dd109`, tool sha256 `73b202af5628df28a31845c785036f97ef3d288bfb3ea327b6c8671ff1fcbce8`,
one-line diff in `mutant-diff.txt`.

* **Survives the default seed**: at seed 45 the mutant scores `fixtures=49/49 … TARGET_MET`, exit 0.
* Swept 1..1000: dies at exactly **7 seeds — 40, 140, 430, 444, 714, 849, 992** (`47/49`, exit 1):
  * seeds 40/140/714/992 (`B` ⊂ `A`): `mirror-agree` and `mirror-missing` — output `eDP-n` takes rule 2
    instead of rule 1 (`name="eDP-4" rule=2 differ=mirror verdict=DIFFER`);
  * seeds 430/444/849 (`C` ⊂ `A`): `fallback-first-empty-and-named` and `unruled-only` — rule `DP-n` matches
    live output `eDP-n`, turning the expected `UNRULED` / `NO_MATCHING_MONITOR` into `DIFFER`.
* The measured set equals the analytic set `{C in A} ∪ {B in A}` computed over `names(1..1000)`
  (`C_in_A = [430,444,849]`, `B_in_A = [40,140,714,992]`), so the discrimination is fully explained — no
  unexplained residual.

Receipt: `mutant-substring.txt`.

Consequence for the claim: the seeded fixture set catches selector-confusion defects at 0.7% of seeds. A
default-seed run is *not* evidence that such a defect is absent; the sweep is, at some seed. The 49 fixtures
themselves never pin an `eDP-n`/`DP-n` pair in a harmful role, so the discrimination comes from the seed, not
from the fixture design.

### F8 — timing (one run)

5 serial runs at seed 45, same clone and work dir: **1067, 1087, 1101, 1112, 1139 ms** (median 1101 ms,
range 72 ms); the session's first run measured 803 ms. One score = 1 selftest invocation + 49 tool
invocations inside 49 fresh fixture dirs (10 s timeout each, never approached); ≈ 21 ms per invocation.
Parallel throughput on 32 cores, `-P 12`: 150 seeds in 14.9 s, 850 seeds in 91.9 s. Fleet load (60+ peer
seats) was present during measurement — treat ±10% as noise. Receipt: `timing.txt`.

## Risks and residuals

1. **Discrimination is seed-fractional.** F7 shows 7/1000 seeds catch an exact-vs-substring selector defect.
   A reading of `PRED-C1-r45` as "the fixture set encodes exact-match semantics" holds only through the
   seed; the fixtures encode it at a rate, not at every seed.
2. **Seed independence covers names only.** `{A} {B} {C} {D}` are the only seed-derived bytes; modes,
   positions, scales, transforms, `desc:` text layout and every setup path are fixed text. 1000 green seeds
   say nothing about those dimensions.
3. **Hash determinism is established by construction, not by pinning.** `-I` makes `PYTHONHASHSEED`
   ineffective for the scored processes (F3); the evidence is F4's structural census plus the 123 identical
   logs. A future counter that iterated a set would not be covered by those three named runs.
4. **`names()` stability rests on CPython's Mersenne Twister** (`random.Random(seed).choice/randint/shuffle`).
   Only interpreter 3.14.8 was exercised here; the seed→names mapping is not contractually frozen across
   Python versions. `name-anchors.txt` records seeds 1/36/40/45/46/140/150/430/444/714/849/992 as an anchor
   table for a later interpreter change.
5. **Timing is fleet-load dependent** (F8), single host, single filesystem (`/fast`).
6. Advisory only (no frozen file touched): a fixture `monitor = DP-1, 1920x1080@60, 0x0, 1` with dump
   `[eDP-1]` gives the reference `UNRULED` / `NO_MATCHING_MONITOR` / rc 3 and the substring mutant
   `AGREE` / `OK` / rc 0 (`advisory-probe.txt`) — i.e. one such fixture would catch that defect class at
   every seed while keeping the reference MET. Registering it is the L1's call, not this seat's.

## Scope, safety, tooling

* Wrote only `.ufo/waves/round-45/w1/ExecSeedSweep/` (this report and receipts) and
  `.ufo/waves/round-45/w1/ExecSeedSweep.md`. No lane file, no frozen counter/control/registration/reference,
  no fleet file, no `.ufo/state`, no git index of the lane.
* Fixture repos: two clones under `/fast/scratch/hyaku/mado-r45/ExecSeedSweep`, each `git rev-parse
  --show-toplevel` asserted equal to its own dir before the commit, commits with a scratch identity only.
* Host: no pacman, no compositor call, no `hyprctl` at all in this seat (the counter's own fake PATH stubs
  are internal to it and left no marker — every scored run logged `readonly=ok`). No Wayland client, no
  session material read.
* Tooling installed: none. Python 3.14.8 (system) only.
* Scratch deleted at seat end (`/fast/scratch/hyaku/mado-r45/ExecSeedSweep` removed after the receipts above
  were copied here).

## Receipts in this directory

`sweep-reference.txt` (1000 seed verdicts) · `hash-battery.txt` · `determinism-checks.txt` ·
`collision-census.txt` · `name-anchors.txt` · `mutant-substring.txt` · `mutant-diff.txt` ·
`advisory-probe.txt` · `timing.txt`.
