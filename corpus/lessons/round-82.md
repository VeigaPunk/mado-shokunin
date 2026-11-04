# mado round 82 — the client's own band, and the tray plane in the runbook (2026-11-04, hyaku run 15)

Claims: **C1 coverage** — a declared dynamic layer band (`height = 0` horizontal, `width = 0`
vertical) is modelled through a declared `--allocation` map instead of refused: forty-seven frozen
cases (the thirty-nine round-81 cases carried parsed-equal plus eight), thirty-four named mutations
killed 34/34, the held round-81 tool `base_correct=39/47`, tool selftest 133/133; **C2 operability** —
the read-only runbook gains the tray plane (`busctl --user list` watcher owner, the watcher's
interface census, and the method table that census prints): twenty-nine cases / twenty-nine rows /
twenty-nine anchors, `control_new=0/3`, twenty-five matcher mutants killed. Freeze
`780c30fcae12d74ce8ab3b871a0888696c2415d9`; base `6ea2386d49318a5f223097c78b5fe79c31b064f8`.
Declaration: `.ufo/waves/round-82/claims-declaration-r82.md`.

## Mistakes

| id | class | evidence pointer | captured-by | fix (shown able to fail) |
|---|---|---|---|---|
| M82-1 | dead branch presented as a rule: `band_of`'s "the declaration wins" arm was unreachable on every call path, because both callers guarded `axis == 0` before calling it — so the rule the resolver documented was not a rule the model ran | the first sandbox run printed `MADO_R82_MUTANT: name=alloc-explicit-overridden correct=47/47 killed=no`, i.e. deleting `if spec[axis] > 0: return spec[axis]` changed nothing; `declared_box` had `if pos in ("top","bottom") and height == 0: height = band_of(...)` and the composition had `if bar_spec[band_axis] == 0: ...` | nothing until the mutant kill count ran: the counter's `killed` clause is the only reader of that branch, and it was the last line of a full 50 s run; the tool's own selftest called `band_of` directly, so it passed (`133/133`) while the model never exercised the arm | `declared_box` now resolves the band axis through `band_of` unconditionally and the composition does the same, so the arm is live; shown able to fail: the mutant now dies (`killed=yes`) and the case `alloc-explicit-ignored` separates it (declared 26 + allocation 40 must stay 26) |
| M82-2 | anchor drift under refactor, again: the M82-1 repair rewrote the two call sites, and two mutant anchors still quoted the pre-repair text, so a full run reported `correct=0/47 killed=no reason=anchor-absent` for `alloc-axis-lost` and `alloc-composition-ignored` and the contract fell to `killed=32` | `.ufo/waves/round-82/receipts/` first sandbox runs (not committed; the lane commit `780c30fc` carries the repaired anchors); the counter's anchor-absent message is the pointer | the counter's anchor existence check (`if own_source.count(anchor) != 1: reason=anchor-absent`) — but only after a full run, not before it; nothing checked anchors at the same time as the code edit | both anchors re-pointed to the refactored lines (`height = band_of(bar, allocation) if pos in ("top","bottom") else bar["height"]`, `bar_spec[band_axis] = band_of(bar_spec, allocation)`) and verified to occur exactly once; shown able to fail: each mutant now scores 43/47 and 46/47 with `killed=yes`, and the contract reads 34/34 |
| M82-3 | source-name substitution: the freedesktop wiki page for the watcher spells the bus name `org.freedesktop.StatusNotifierWatcher`, and the round's rows require the KDE spelling the host advertises — registering that page as the row's source would have licensed a name it does not contain | `.ufo/waves/round-82/fetch/S482.html` (page head: "There will be a single org.freedesktop.StatusNotifierWatcher service instance registered on the session") against `.ufo/waves/round-82/fetch/S482.xml:3` (`<interface name="org.kde.StatusNotifierWatcher">`) | the source was opened before the row was written (this round's own §2b rule: a row is written only after its source is opened); the page's text contradicted the intended quoted name | the KDE interface XML at tag `v6.2.0` is S482 and the wiki page is S483 `rejected` with the reason and the flip recorded; shown able to fail: S483's status cell names the freedesktop spelling and the census accepts it as a rejection, not as a grounding row |

Sweep for a fourth: `grep -n 'TODO\|FIXME\|XXX' tools/mado-barfoot.py quality/counters/c1-r82-allocation-band.py quality/counters/c2-r82-runbook.py` → no output (2026-11-04, at the freeze). Second sweep (dead keys in the new control sets): every key of the eight new C1 cases is read by `case_files`/`expected_ok` (`name`, `config`, `layers`, `monitors`, `monitor`, `surfaces`, `allocation`, `expect`) and every key of the three new C2 cases by `case_correct` (`name`, `argv`, `kind`, `value`, `skill_anchor`, `samples`, `negatives`); `python3 -c "…set(case)-KNOWN"` prints nothing for all eleven. Third sweep (unused mutants): every one of the 34 + 25 mutants is scored by the counter it lives in, and every anchor was verified to occur exactly once at the freeze.

## Gate (sources opened this round)

Census at round start `6ea2386d` → 415 registry rows,
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
/home/vgpnk/Projects/shokunin mado` exit 0 (standing W04 duplicate-URL warnings, W01 S277;
`receipts/census-start-r82.txt`). At the round-82 content tip → 418 rows (415 + S481 + S482 +
S483-rejected), exit 0. Two rows added as `mined` and one as `rejected`; no older row's
`status`/`recheck`/`used-by` cell moved.

| row | source and locator (opened 2026-11-04) | status | located quote (≤25 words) | what it licenses / does not |
|---|---|---|---|---|
| S481 | https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/protocols/wlr-layer-shell-unstable-v1.xml — `set_size` `:122-142`, clause `:347-348`; sha256 `87e0b9c8…`, 19326 B (`.ufo/waves/round-82/fetch/S481.xml`) | mined (new) | `If the width or height arguments are zero, it means the client should decide its own window dimension.` (at `:347-348`) | that a zero width/height is the client's size, so the band is the client's allocation; it does not say what waybar sends on this host, and it is the protocol the pinned Hyprland tree vendors, not a version read off the host |
| S482 | https://raw.githubusercontent.com/KDE/kstatusnotifieritem/v6.2.0/src/org.kde.StatusNotifierWatcher.xml — whole file, interface `:3`, methods `:6`/`:10`, property `:17`; sha256 `19df7f18…`, 1151 B (`.ufo/waves/round-82/fetch/S482.xml`) | mined (new) | `interface name="org.kde.StatusNotifierWatcher"` (at `:3`) | the KDE-owned bus name and its two register methods, which the round's three rows bind; it does not say the host's waybar owns that name (the live `busctl` read does) |
| S483 | https://www.freedesktop.org/wiki/Specifications/StatusNotifierItem/StatusNotifierWatcher/ — page head, 6395 B, sha256 `f22928e1…` (`.ufo/waves/round-82/fetch/S482.html`) | rejected | `There will be a single org.freedesktop.StatusNotifierWatcher service instance registered on the session` (at the page head) | REJECTED as a grounding row: it names the freedesktop-prefixed bus name, which the round's rows would contradict; flip: re-point a row at the freedesktop spelling on a host that advertises it, or a revision-pinned page that uses the KDE spelling |

Assimilation: **none** this round. The staged package `/home/vgpnk/Projects/shokuknow/merge/mado/`
was built against a 192-row registry; `comm -12` of the lane's ids and the package's staged ids
still collides (the round-81 count was 94), and no staged entry touches this round's ground (the
declared allocation or the tray plane). `Assimilation: none` is reported; the flip is unchanged from
round 81: adopt both `host-bar-producers-r28` and its parent after the host config is re-read and
the ids are renumbered by document.

## Next round

C1's next finite ground is the extra surface's dynamic band (a `--surfaces` allocation field) and
the fractional scale, both of which need a declaration-grammar change before a case can exist; C2's
is the tray item count (`RegisteredStatusNotifierItems`) once the host has at least one item, or the
`StatusNotifierHost` registration as a second state pair.
