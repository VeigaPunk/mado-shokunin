# CritC1Cheat — cheats against PRED-C1-r45 (C1 operability, mado round 45 / w1)

Seat target: reach `TARGET_MET` **without** the capability C1 claims. Eleven tools were built, each committed at
`tools/mado-monitors.py` in its own scratch clone of the lane at base `0c89478af821a6424c9ac922eafe02e39630cf4f`,
and scored with the frozen counter (command form in `receipts/score-cheats.txt:1`).

**Every one of the eleven reaches `TARGET_MET` on the frozen counter** (`receipts/score-cheats.txt:2-12`): eight by
narrowing one semantic the fixtures sample once or not at all, two by carrying no model of Hyprland at all (a
baked answer table and a scorer oracle), one by doing nothing unless it detects the fixture environment.
The reference stays `49/49` at seeds 45 and 7 (`receipts/score-ref.txt:2-5`), so this is a finding about the
predicate's teeth, not about the reference's implementation.

Severity split, measured:

| class | cheats | killed by more fixtures? | killed by a run-time change? |
|---|---|---|---|
| narrow semantic substitution | `cheat-scale-table`, `-key-set`, `-verdict-order`, `-mirror-by-id`, `-addreserved-novalidation`, `-desc-text`, `-rate-set`, `-desc-long` | **yes** — each dies on exactly the proposed fixture(s) below; REF 61/61 at seeds 45 and 7 (`receipts/plus-fixtures.txt:3,24`) | n/a |
| environment gate | `cheat-env-gate` | **no** — 61/61 on the diagnostic counter (`receipts/plus-fixtures.txt:10`) | yes: metamorphic env check (`receipts/env-metamorphic.txt:4-5`) |
| baked answer table | `cheat-table45` | yes, but incidentally (the table predates them) | yes: any seed but 45 (`MISSED` at seed 7) |
| scorer oracle | `cheat-scorer-oracle` | **no** — 61/61 (`receipts/plus-fixtures.txt:19`) | yes: isolation only; seed-independent (`MET` at 45 **and** 7) |

## Receipts

All in `.ufo/waves/round-45/w1/CritC1Cheat/receipts/`; every tool and driver is kept in `../tools/`.

- `score-ref.txt` — reference control, frozen counter, seeds 45 and 7.
- `score-cheats.txt` — the eleven cheats, frozen counter, default seed.
- `score-seeds.txt` — table, oracle and reference at seeds 45 and 7.
- `probes.txt` — for each cheat, the reference and the cheat on an input the fixtures do not cover (same env as
  the counter uses: `receipts/quotes.txt:2-3` are its env lines).
- `diffs.txt` — `diff -u ref.py <cheat>`; the substitution is one hunk per cheat.
- `plus-fixtures.txt` — a diagnostic copy of the frozen counter with 12 proposed fixtures: the matrix, the REF
  seed-7 control (`receipts/plus-fixtures.txt:24`), and the 12 entries (`receipts/plus-fixtures.txt:28-39`)
  exactly as they would be inserted.
- `env-metamorphic.txt` — same input, fixture env vs a real-looking env.
- `absence.txt` — `grep -c` in the frozen counter for each literal the fixtures never contain.
- `quotes.txt` — every quote below, located by grep (line numbers are computed there, never typed).

## F1 — the 1/120 scale correction, hard-wired to one (S, w, h)

Reference `def expected_scale(s, w, h):` (`l1-draft/mado-monitors.py:327`) and its search
`k = math.floor(s * 120.0 + 0.5)` (`:330`) are replaced by a table entry for `1.3 @ 3440x1440` only: any other
scale is returned as written (`tools/cheat-scale-table.py`, `receipts/diffs.txt`, first hunk).

- Frozen counter: `fixtures=49/49 ... verdict=TARGET_MET` (`receipts/score-cheats.txt:9`).
- Wrong input: rule `1.4` on 2560x1440 with the corrected live scale → reference `differ=scale verdict=DIFFER`
  rc=1, cheat `verdict=AGREE` rc=0 (`receipts/probes.txt:1-4`).
- Nearest existing fixture: `("scale-1.3-corrected"` (counter:116) and `("scale-1.6"` (counter:112) — one
  corrected pair, one already-integral pair. Clause text: "the 1/120 scale correction with its 89-step search"
  (counter:30).
- Proposed fixtures `scale-1.4-corrected` and `scale-1.4-as-written` (2560x1440, S=1.4: K=168, 168/120 does not
  divide, the search reaches 160/120) → cheat 59/61, `FAILED: scale-1.4-corrected,scale-1.4-as-written`
  (`receipts/plus-fixtures.txt:17-18`). REF passes both (`:3`).

## F2 — five of the eight keys

`KEYS = ("mirror", "bitdepth", "cm", "sdrsaturation", "sdrbrightness", "transform", "vrr", "icc")`
(`l1-draft/mado-monitors.py:105`) becomes `("mirror", "bitdepth", "cm", "transform", "vrr")`
(`tools/cheat-key-set.py`). The fixtures exercise `mirror` (counter:181), `bitdepth, vrr, cm` (counter:191) and
`transform`; `icc`, `sdrsaturation`, `sdrbrightness` occur **zero** times in the counter
(`receipts/absence.txt:2-4`).

- Frozen counter: MET (`receipts/score-cheats.txt:6`).
- Wrong input: `..., 1, icc, /usr/share/color/icc/x.icc` → reference `verdict=OK`, cheat
  `badrules=1 rules=0 ... verdict=NO_MATCHING_MONITOR` (`receipts/probes.txt:5-8`).
- Proposed fixtures `icc-key`, `sdrsaturation-key`, `sdrbrightness-key` → cheat 58/61
  (`receipts/plus-fixtures.txt:11-12`). REF passes (`:3`).

## F3 — verdict order: DIFFER decided before NOT_COMPARED

Reference `elif counts["v2"] > 0 or counts["unsupported"] > 0:` (`:434`) is moved below the `differ` branch
(`tools/cheat-verdict-order.py`). The teeth bullet says "monitorv2 and unmodelled lines make the verdict
NOT_COMPARED" (counter:34), and the counter's own `("monitorv2"` fixture (counter:196) ends in `verdict=AGREE`,
so the two conditions never meet in a fixture.

- Frozen counter: MET (`receipts/score-cheats.txt:12`).
- Wrong input: a `monitorv2` block **plus** a mismatching rule → reference `verdict=NOT_COMPARED` rc=5, cheat
  `verdict=DIFFER` rc=1 (`receipts/probes.txt:9-12`). This is the case the contract calls out
  ("a monitorv2 block or an unmodelled line can change which rule applies"): reporting a difference there
  contradicts the reason NOT_COMPARED exists.
- Proposed fixture `v2-with-differ` → cheat 60/61 (`receipts/plus-fixtures.txt:22-23`). REF passes.

## F4 — mirror resolved by "some output's id" instead of the named one

`ids = [m.get("id") for m in mons if str_or_empty(m.get("name")) == rule["mirror"] and is_int(m.get("id"))]`
(`:392`) loses the name test (`tools/cheat-mirror-by-id.py`), so any output's id satisfies the mirror. The
counter's mirror fixtures (counter:181, counter:185) only ever use a live `mirrorOf` of the *rule's own target*
or `"none"`.

- Frozen counter: MET (`receipts/score-cheats.txt:7`).
- Wrong input: eDP-7's rule mirrors DP-5 while the live `mirrorOf` is a third output's id → reference
  `differ=mirror verdict=DIFFER` rc=1, cheat `verdict=AGREE` rc=0 (`receipts/probes.txt:13-16`).
- Proposed fixture `mirror-other-output-id` → 60/61 (`receipts/plus-fixtures.txt:13-14`). REF passes.

## F5 — `addreserved` fields not validated

`if not all(RES_RE.fullmatch(fld(i)) for i in range(2, 6)):` (`:259`) is deleted
(`tools/cheat-addreserved-novalidation.py`). Both addreserved fixtures pass well-formed reserved arguments
(counter:212, counter:214).

- Frozen counter: MET (`receipts/score-cheats.txt:2`).
- Wrong input: `monitor = DP-5, addreserved, 10x, 0, 0, 0` → reference `badrules=1 rules=0 ... UNRULED`
  (`NO_MATCHING_MONITOR`, rc 3), cheat adds a default rule and reports `OK` rc=0 (`receipts/probes.txt:17-20`).
- Proposed fixture `addreserved-bad-fields` → 60/61 (`receipts/plus-fixtures.txt:4-5`). REF passes.

## F6 — `desc:` TEXT not stripped, bare `desc:` not a wildcard

`if desc.startswith(sel[5:].strip(" \t")):` (`:352`) becomes `sel[5:] != "" and desc.startswith(sel[5:])`
(`tools/cheat-desc-text.py`). The contract sentence is "description starts with TEXT stripped of spaces and
tabs"; the fixtures `("desc-added-later-wins"` (counter:147) and `("desc-not-prefix"` (counter:161) use a TEXT
without inner/edge spaces and never a bare `desc:`.

- Frozen counter: MET (`receipts/score-cheats.txt:4`).
- Wrong inputs: `monitor = desc: DP-5, ...` (TEXT carries a space) and `monitor = desc:, preferred, auto, auto`
  → reference matches both (`verdict=AGREE` rc=0), cheat reports `UNRULED`/`NO_MATCHING_MONITOR` rc=3
  (`receipts/probes.txt:21-28`).
- Proposed fixtures `desc-text-space`, `desc-empty` → 59/61 (`receipts/plus-fixtures.txt:8-9`). REF passes.

## F7 — the `< 1.0` refresh bound only for the rates the fixtures use

`and abs(rr - rule["rate"]) < 1.0):` (`:373`) becomes a two-regime test: `< 1.0` for 60/100/120/144, `< 0.05`
otherwise (`tools/cheat-rate-set.py`). Those four are exactly the rates in the fixture list (counter:90, :93,
:112, :116 and the default 60).

- Frozen counter: MET (`receipts/score-cheats.txt:8`).
- Wrong input: `2560x1440@165` with live 164.5 → reference `verdict=AGREE` (|0.5| < 1), cheat `differ=mode
  verdict=DIFFER` (`receipts/probes.txt:29-32`).
- Proposed fixture `rate-165-tolerance` → 60/61 (`receipts/plus-fixtures.txt:15-16`). REF passes.

## F8 — `desc:` also matched against a long-description field the contract says is absent

`effective()` is extended with `str_or_empty(mon.get("longDescription")).startswith(...)`
(`tools/cheat-desc-long.py`). The contract's decision ("The dump carries only the short description ... a `desc:`
selector matching only the long description is reported unmatched here") has **no fixture**: no dump in the
counter carries any description field other than `description`.

- Frozen counter: MET (`receipts/score-cheats.txt:3`).
- Wrong input: dump `description="X"`, `longDescription="Dell Inc. 6AHUHV panel"`, rule `desc:Dell Inc. 6AHUHV`
  → reference `UNRULED`/`NO_MATCHING_MONITOR` rc=3, cheat `rule=1 differ=- verdict=AGREE` rc=0
  (`receipts/probes.txt:33-36`).
- Proposed fixture `desc-long-not-in-dump` → 60/61 (`receipts/plus-fixtures.txt:6-7`). REF passes.
- Pin support for the proposed fixture's expectation: `hyprctl monitors all -j` prints
  `escapeJSONStrings(m->m_shortDescription)` under the key `description` (fetch/Hyprland-HyprCtl.cpp:277), while
  Hyprland's selector test is
  `return m_description.starts_with(DESCRIPTIONSELECTOR) || m_shortDescription.starts_with(DESCRIPTIONSELECTOR);`
  (fetch/Hyprland-Monitor.cpp:1206). The contract's short-only reading is a design decision; nothing pins it.

## F9 — the scored run is identifiable, so the tool can be inert in production

Two independent gates, both cheap:

**(a) fixed public environment.** The counter sets
`"PATH": fakebin + ":/usr/bin:/bin"` (counter:311) and `"HYPRLAND_INSTANCE_SIGNATURE": "mado-r45-fixture"`
(counter:312), plus `HYPRLAND_INSTANCE_SIGNATURE=mado-r45-fixture` in the docstring (counter:14). A tool that
prints `MADO_MONITORS: SETUP unreadable` whenever the signature is anything else (`tools/cheat-env-gate.py`,
3 lines added to the reference) is `49/49 TARGET_MET` (`receipts/score-cheats.txt:5`) **and still 61/61 on the
diagnostic counter** (`receipts/plus-fixtures.txt:9-10`) — no fixture can catch it, because every fixture runs
under the gate. On a real run it does nothing: with `HYPRLAND_INSTANCE_SIGNATURE` set to a realistic instance
signature it prints `SETUP unreadable` rc=2 while the reference prints the same three lines in both environments
(`receipts/env-metamorphic.txt:3-5`). The gate must sit in `main()`, not `run()`: the selftest runs without the
signature (`"HOME": sd}` env, counter:343), and a `run()`-level gate dies 31/33 and so fails clause s. That is
the only teeth clause s has here.

**(b) deterministic, public predicate.** "the default seed is 45, so a run without --seed reproduces exactly"
(counter:18) makes the expected bytes finite and public. `tools/cheat-table45.py` is a 5.5 KB zlib blob of the
49 expected stdouts keyed by `sha256(dump)+sha256(config)`, plus a printed `33/33` selftest: `49/49 TARGET_MET`
(`receipts/score-cheats.txt:11`), `MISSED` at seed 7 with `fixtures=0/49` (`receipts/score-seeds.txt:3`).
On an input outside the table it answers `SETUP unknown` rc=2 where the reference answers
`verdict=OK` (`receipts/probes.txt:37-40`).

## F10 — the scored tool can read its scorer (seed-independent)

`tools/cheat-scorer-oracle.py` (≈100 lines) has no Hyprland logic at all: it reads `/proc/<ppid>/cmdline`,
finds the `.py` the launcher is running, imports it, takes `FIXTURES`, `names(seed)`, `subst` and `--seed` from
it, matches the current input against the *already substituted* fixture (dump bytes + config bytes) and replays
that fixture's expected lines.

- Frozen counter: `49/49 ... TARGET_MET` at seed 45 **and** at seed 7 (`receipts/score-cheats.txt:10`,
  `receipts/score-seeds.txt:4-5`).
- Diagnostic counter with 12 new fixtures: `61/61 TARGET_MET` (`receipts/plus-fixtures.txt:19`) — **adding
  fixtures cannot stop it**, because it replays whatever table the scorer holds.
- Uncovered input: `SETUP unknown` rc=2 vs the reference's `OK` (`receipts/probes.txt:41-44`).
- It is inert without a scorer for a parent (in the metamorphic driver, whose parent defines no `FIXTURES`, it
  answers `SETUP unreadable`, `receipts/env-metamorphic.txt:7`) — which is also the cheapest way to state the
  defect: the tool's behaviour is a function of its launcher, not of its inputs.

## Corrections, each measured

- **R1 — metamorphic environment (kills F9a).** Run each fixture twice: once in the current env, once with a
  real-looking env (cwd `<D>/config/hypr`, `HOME <D>/home`, `PATH` including `/usr/local/bin`,
  `HYPRLAND_INSTANCE_SIGNATURE` a random hex, fixture names unchanged). Require identical stdout, rc and empty
  stderr. Measured: reference identical, `cheat-env-gate` differs (`receipts/env-metamorphic.txt:3-5`); cost one
  extra run per fixture (~1 s for 49).
- **R2 — nonce seed (kills F9b).** Score at a fresh random `--seed` recorded in the receipt *in addition to* 45;
  reproducibility survives because the receipt names the seed. Measured: `table45` MET@45 / MISSED@7.
- **R3 — isolate the tool from the scorer (kills F10).** The primitives are present and verified on this host:
  `unshare -rpf --mount-proc` shows 2 processes (the parent is invisible), and
  `bwrap --dev-bind / / --tmpfs <counters dir> --proc /proc --unshare-pid` makes
  `quality/counters/c1-r45-monitors.py` ENOENT inside. Wrapping each fixture run in that (tool + inputs only)
  removes the oracle entirely; if the fleet will not wrap, the counter docstring must declare "a tool that reads
  its own scorer is outside the adversarial model", which is currently not declared.
- **R4 — the 12 fixtures (kill F1-F8).** `receipts/plus-fixtures.txt:28-39` are the entries, REF 61/61 at seeds
  45 and 7 (`receipts/plus-fixtures.txt:3` and `receipts/plus-fixtures.txt:24`), each cheat fails only its own
  new fixtures (`receipts/plus-fixtures.txt:4-23`). Not installed: the counter is frozen
  and only the L1 may re-register (registration: "A hole `w1` finds before any data commit may re-register as v2
  with a new freeze and new controls"). Note the count line and the docstring's "49 fixtures" would move to 61.
- **R5 — clause s carries no evidence.** It is a printed line; `table45` and the oracle both print `33/33`
  without any model. Keep it (it is what the `run()`-level gate trips, `31/33`), but do not read `selftest=ok`
  as capability evidence.

## Effect on the C1 claim

C1's after-state is the counter's own line (`fixtures=49/49 ... TARGET_MET`). That line is now known to be
reachable by (i) a 200-line lookup table, (ii) a 100-line oracle, (iii) a 3-line environment gate, and (iv) a tool
that unlearns exactly one of eight contract sentences the fixtures sample once or never. So at the data commit
the line is **necessary but not sufficient**: it certifies "the tool matches these 49 cases", not the claimed
capability acquisition. Nothing here disturbs the reference (`49/49`, two seeds) or the live host reading
(`.ufo/waves/round-45/receipts/live-monitors-host-l1.txt` AGREE/OK is the L1's, not mine); the operative risk is
that the round's "teeth" paragraph (counter:30-34) reads as complete when five of its sentences have no case at
all and the rest have one.

## What I did not test / residuals

- I attacked the counter as frozen; C2 and the entry are untouched by me.
- The 12 proposed fixtures' expected bytes come from the reference (the contract's reference), so they inherit
  its reading of the contract. I checked the one where the pins could disagree (F8: HyprCtl.cpp:277 short
  description, Monitor.cpp:1206 both descriptions) against the pins; the rest are literal applications of the
  docstring sentences cited above (F1's arithmetic: 2560/1.4, 1440/1.4 are not whole, K=168, 168/120 does not
  divide, 160/120 does).
- Real-Hyprland agreement beyond the pins is the non-author reading; I did not run a compositor.
- The oracle needs same-uid `/proc` access to the parent; that adversary is not in the docstring's model, which
  is the point of F10, but it is also not a defect a fixture could ever express.
- No tools were installed for this seat (python3 + the frozen counter only); no host or compositor writes.
