# ConnCrossClaim — C1/C2 cross-claim & shared-assumption check (round 45, w1)

Seat: ConnCrossClaim (leaf; no subagents). Lane: mado-shokunin.
Claim pair: C1 operability (`tools/mado-monitors.py`) and C2 coverage
(`corpus/knowledge/hyprland-monitor-rule-r45.md`), both frozen at
22a8dedd02f507689c567777e0f20b5e645c8ce0 / base 0c89478af821a6424c9ac922eafe02e39630cf4f.

## 1. Result summary

Register separability holds in both directions (registration.md:57-60). Each counter
passes on a tree carrying only the other claim's artifact and fails on a tree with
only its own artifact; the two counters read disjoint paths (evidence in §2, §3).
The two claims share a small set of pinned Hyprland facts (the 60 Hz default, the
1 Hz bound, the 1/120 step and 89-step search, the eight-key line grammar, the JSON
field set). A repo-level pin deviation is caught by C2 but invisible to C1 (tree
D/E, §4); a pin that is wrong against upstream reality would silently corrupt both
claims together and neither counter would blink — the live host receipt is the only
pin-independent evidence, and it exercises one case (§5).

## 2. Causal separability — experiment

Scratch clones under /fast/scratch/hyaku/mado-r45/ConnCrossClaim (deleted at the
end; full counter transcripts copied to this seat dir):

| Tree | HEAD | contents | C1 counter | C2 counter |
|---|---|---|---|---|
| A | 0163904a4d5307e587d8b0ebe867714b68fc4368 | freeze + `tools/mado-monitors.py` (reference bytes, sha256 c6ac5fc2…) | **TARGET_MET** rc=0: fixtures=49/49 selftest=ok readonly=ok tool=present | TARGET_MISSED rc=1: clauses a-j all 0, admitted=0/1 |
| B | 7dc09f54ecc9bb5ff9765844b34929c12db69380 | freeze + `build-pos.py` data only (entry, S302-S310, lesson Gate, README row) | TARGET_MISSED rc=1: tool=absent fixtures=0/49 | **TARGET_MET** rc=0: clauses a:1…j:1, admitted=1/1 |

Evidence: `c1-A.out`, `c2-A.out`, `c1-B.out`, `c2-B.out`, `trees.txt` in this dir.
Tree construction followed the pinned fixture recipe (mktemp/git clone --shared/
top-level assert before commit; identity seat@scratch.invalid).

Why the counters are disjoint by construction:

- C1's counter reads only `tools/mado-monitors.py` at REV (ls-tree + show) and a
  scratch workdir; clause a/s/f/r never touch corpus/, fetch/ or the registry
  (quality/counters/c1-r45-monitors.py:325-368).
- C2's counter reads ENTRY, `corpus/SOURCES.md` (REV and BASE), the lesson's `## Gate`,
  `corpus/README.md` and `.ufo/waves/round-45/fetch/` — never tools/
  (quality/counters/c2-r45-monitor-entry.py:411-632, 635-657).
- Neither counter reads the other claim's artifact: A passes C1 with no entry; B
  passes C2 with no tool.

## 3. Shared assumptions — one fact, two encodings

Every listed C1 behavior and its C2 counterpart derive from the same pinned source
line. Computed locators (grep -n on the pins; line_keys verified by re-running the
counter's own host_census arithmetic):

| Fact | Pin (fetch/) | C1 encoding | C2 encoding |
|---|---|---|---|
| 60 Hz default | Hyprland-MonitorRule.hpp:46 `float m_refreshRate = 60; // Hz` | l1-draft/mado-monitors.py:11 "a rule without `@RATE` requests 60 Hz"; kill control K03 (ctl-c1.txt) | census default_refresh=60; surface default-60 anchor (c2 counter:328,361) |
| 1 Hz closeness bound | Hyprland-Monitor.cpp:837 `!DELTALESSTHAN(bestMode->refreshRate / 1000.f, RULE->m_refreshRate, 1))` | docstring:67-68 `\|refreshRate\| - RATE\| < 1.0`; K04 | census refresh_tolerance=1; surface closeness (c2 counter:330,363) |
| 1/120 step, 89-step search | Hyprland-Monitor.cpp:1001 `float searchScale = std::round(m_scale * 120.0);`, :1010 `for (size_t i = 1; i < 90; ++i)` | docstring:12-13 "nearest multiple of 1/120…searching 89 steps up and down", :70-73; K05 | census scale_step=1/120 scale_search=89; surface scale-search (c2 counter:331,336,364) |
| eight-key line grammar; unknown key drops rule | Hyprland-legacy-ConfigManager.cpp:1293-1387 (line_keys=8) | docstring:44-47 "any other key adds one to badrules and the rule is not added"; K10 | census line_keys=8; surfaces handle-monitor/invalid-syntax (c2 counter:338-346,357-358) |
| erase-on-add; newest match wins; empty-selector fallback | Hyprland-MonitorRuleManager.cpp:38,96 | docstring:6-8,55-56; K06/K07 | surfaces add-erase/get-reverse (c2 counter:359-360) |
| selector match: exact name, `desc:` prefix on short/long description | Hyprland-Monitor.cpp:1201-1206,255-256 | docstring:59-63; K11 | surface selector (c2 counter:362) |
| JSON fields; `all` lists disabled; refreshRate 5 decimals | Hyprland-HyprCtl.cpp:242,320 | dump schema the tool consumes (name/width/height/refreshRate/x/y/scale/transform/disabled/mirrorOf) | census json_refresh_decimals=5; surfaces json-refresh/monitors-all (c2 counter:332,365-366) |
| explicit position applied as written | Hyprland-MonitorPositionController.cpp:27 | position compare only for explicit X/Y (docstring:69) | surface explicit-position (c2 counter:367) |
| number test clamp | hyprutils-String.cpp:50,59 | `S < 0.25 becomes 1.0` (docstring:52) | surface is-number (c2 counter:368) |
| `sdr_eotf` line-key divergence | wiki-Monitors.md:253 vs legacy ConfigManager.cpp:1351-1379 | docstring:34-35 | surface wiki-sdr-eotf; entry §5 INF (c2 counter:370) |

C1's executable contract and C2's entry are therefore two encodings of the same
pinned fact set; the values 60 / 1 / 120 / 89 / 8 / 5 appear in both.

## 4. One wrong pin — counter-level behavior (empirical)

Tamper experiment: change one byte in the frozen receipt
`.ufo/waves/round-45/fetch/Hyprland-MonitorRule.hpp` ("// Hz" -> "// hz",
sha256 b01d31a… -> edba8623…; the PINS table stays frozen).

- Tree D = B + tampered pin (302027d505…): C2 flips MET -> TARGET_MISSED rc=1.
  Clause d fails for S305 (receipt sha256 vs GATE line vs PINS), pulling e/g/h/i/j
  down; surface default-60 anchor_count=0 (the anchor text is gone). `c2-D.out`.
- Tree E = A + tampered pin (21a7ea92…): C1 stays **TARGET_MET** rc=0, identical
  to tree A (fixtures=49/49). C1's counter never reads fetch/. `c1-E.out`.

So within the counters' own trust model, C2 is the integrity guard for the pinned
receipts; C1 has no channel to detect a pin deviation (c1-r45-monitors.py:325-368
touches only the TOOL blob and the scratch workdir). This is an asymmetry, not a
contradiction: C1's residual already declares the pins are the non-author reading
(registration.md:33).

## 5. One wrong pin — the shared point of failure (what NO counter catches)

Both counters treat the frozen PINS table (c2-r45-monitor-entry.py:96-118 and the
GATE digests) as the trust root. No clause re-derives a pin against upstream
reality — a receipt fetched from the wrong commit, wrong URL, or hashed after
tampering satisfies every check. If one pin is wrong that way, both claims are
corrupted together, silently:

- C1's tool would mis-model real Hyprland (e.g. a wrong default refresh, tolerance,
  scale-correction factor, or key grammar) while still passing its 49 self-contained
  fixtures — the fixtures are the contract's cases, not Hyprland's runtime
  (registration.md:32-33).
- C2's entry would document the wrong behavior while still satisfying clauses a-j —
  the census is "bookkeeping of pinned bytes" and clause j binds locator+keyword,
  not truth of the sentence (registration.md:54-55, c2-r45-monitor-entry.py:62-65).

The only pin-independent evidence in the round is the live host receipt
(receipts/live-monitors-host-l1.txt): one output (DP-1), one rule (@100, scale 1,
transform 0, position 0x0, mirror none) — AGREE/OK. It cannot distinguish a wrong
60 Hz default, a wrong tolerance, a wrong correction factor, or a wrong key
grammar (no fractional scale, no 60 Hz rule, no exotic key exercised). If a pin
were wrong, the union of C1+C2 would have no failing check; the live run is the
only potential tripwire and it is too narrow to catch any of the shared numbers.

Shared lifecycle: C1 and C2 pin the same efb50993 snapshot, so a Hyprland/
hyprutils update invalidates both together; both recheck triggers (90d, or package
update on the host) cover both claims at once.

## 6. Limits

- The tamper experiment mutates one byte; observed failures are sha-driven (clause
  d) plus the default-60 anchor text loss. No C1-relevant fixture changes when a
  pin changes, by construction.
- I did not re-fetch upstream files: "wrong against reality" is analyzed
  structurally, not demonstrated (the pins in fetch/ match the frozen sha256 table
  at the freeze commit).
- Host reads used: none beyond the counter runs (python3/git only); no tools
  installed, no package transactions, no input injection, no Wayland client.

## 7. Handoff to main agent

- Verified only in scratch; no lane content was edited beyond this seat dir.
- Suggested checks for main: re-run `c1-r45-monitors.py --repo <A> --rev HEAD` and
  `c2-r45-monitor-entry.py --repo <B> --rev HEAD` from the receipts if desired; the
  trees live under /fast/scratch/hyaku/mado-r45/ConnCrossClaim until cleanup.
