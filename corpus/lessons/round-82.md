# mado round 82 — the client's own band, and the tray plane in the runbook (2026-11-04, hyaku run 15)

Claims: **C1 coverage** — a declared dynamic layer band (`height = 0` horizontal, `width = 0`
vertical) is modelled through a declared `--allocation` map instead of refused: forty-seven frozen
cases (the thirty-nine round-81 cases carried parsed-equal plus eight), thirty-four named mutations
killed 34/34, the held round-81 tool `base_correct=39/47`, tool selftest 133/133; **C2 operability** —
the read-only runbook gains the tray plane (`busctl --user list` watcher owner, the watcher's
interface census, and the method table that census prints): twenty-nine cases / twenty-nine rows /
twenty-nine anchors, `control_new=0/3`, twenty-five matcher mutants killed (the held r81 instrument
exits 2 at this tree, `control-c2-held-instrument-r82.txt`). Freeze
`780c30fcae12d74ce8ab3b871a0888696c2415d9`; base `6ea2386d49318a5f223097c78b5fe79c31b064f8`.
Declaration: `.ufo/waves/round-82/claims-declaration-r82.md`. Measured receipts:
`.ufo/waves/round-82/receipts/measurement-c1-r82.txt` (rev `780c30fc`) and
`measurement-c2-r82.txt` (rev `89acb06c`, after erratum E1's redaction of the three new C2
fixture tokens; the receipt prints controls sha `07599b24…` and `tree=bound`).

## Mistakes

| id | class | evidence pointer | captured-by | fix (shown able to fail) |
|---|---|---|---|---|
| M82-1 | dead branch presented as a rule: `band_of`'s "the declaration wins" arm was unreachable on every call path, because both callers guarded the axis (`axis == 0`) before calling the resolver — so the rule the resolver documented was not a rule the model ran | the mutant is exactly that arm: `quality/counters/c1-r82-allocation-band.py:129-131` replaces `    if spec[axis] > 0:\n        return spec[axis]` with `    if False:\n        return spec[axis]`; the pre-repair call shape reached `band_of` only when the band axis was 0 (`declared_box` guarded `height == 0`; the composition guarded `bar_spec[band_axis] == 0`), so the branch could not fire. Re-run by this seat in scratch, importing the frozen counter's `run_cases` over the frozen 47 cases: old shape + mutant = **47/47** (not killed), old shape unmutated = 47/47, frozen shape + mutant = **12/47** (killed), frozen shape unmutated = 47/47 | nothing in the model path: under the old call shape the 47 cases score 47/47 with the mutant applied. The tool's own selftest does call `band_of` directly and would fail on the mutant (`132/133`, "the vertical band axis is the width", this seat), but the counter runs `--selftest` only on the unmutated tool (`quality/counters/c1-r82-allocation-band.py:455-458`), so no scored run consumed that signal; `measurement-c1-r82.txt:76` is the only scored reader of the arm | the resolver is the single entry point for the band axis (`tools/mado-barfoot.py:479-482`, composition at `:803`), and the selftest pins the order (`:1493-1499`, "a declared band is not overridden by the allocation"). Shown able to fail: the frozen counter kills the mutant at 12/47 (`measurement-c1-r82.txt:76`), the mutant fails that selftest 132/133 when run directly, while the same mutant survives 47/47 under the old call shape — the difference is the call shape, not the case set |
| M82-2 | source-name substitution: the freedesktop wiki page for the watcher spells the bus name `org.freedesktop.StatusNotifierWatcher`, and the round's rows bind the KDE spelling the host advertises — registering that page as the row's source would have licensed a name it does not contain | `.ufo/waves/round-82/fetch/S482.xml:3` (`<interface name="org.kde.StatusNotifierWatcher">`, methods `:6`/`:10`, property `:17`) against the page-head sentence carried in the registry's rejected row (`corpus/SOURCES.md:435`: "There will be a single org.freedesktop.StatusNotifierWatcher service instance registered on the session") | the source was opened before the row was written (the round's §2b rule): the page's own text contradicted the intended quoted name, so the row was not written from it | S482 is the KDE interface XML (`:3`) and S483 is registered `rejected` with the flip. Shown able to fail: the registry's own status cell says `rejected`, and the two committed files carry visibly different spellings of the same interface |

**Candidate (b), examined and not admitted.** The round's dispatch also named anchor drift as a
candidate: `alloc-axis-lost` and `alloc-composition-ignored` reporting `reason=anchor-absent` after
the M82-1 refactor. No lane byte shows that event. The only `reason=anchor-absent` lines are the
base control's — `control-c1-r82-at-base.txt:76-81`, all six `alloc-*` mutants — and the base tool
is the held r81 model with no allocation input at all (`:83`, `rule=held-r81-model(no-allocation-input)`),
so absence there is the do-nothing control's definition, not drift. At the freeze both anchors are
present and the mutants die: `alloc-axis-lost correct=43/47 killed=yes`
(`measurement-c1-r82.txt:78`) and `alloc-composition-ignored correct=46/47 killed=yes`
(`:81`). If a pre-freeze sandbox run did report the two anchors absent, that transcript is not in
the lane and must be pinned before it becomes a lesson row; the counter's anchor check
(`quality/counters/c1-r82-allocation-band.py:301`) is the reader that would catch it, but only after
a full run.

## Sweep for further mistakes

1. **Marker sweep.** `grep -n 'TODO\|FIXME\|XXX' tools/mado-barfoot.py
   quality/counters/c1-r82-allocation-band.py quality/counters/c2-r82-runbook.py` → no output
   (exit 1, 2026-11-04 at the content tip). No deferred-work marker sits in the frozen instruments.
2. **Dead keys, C1.** The nine case keys (`name`, `config`, `layers`, `monitors`, `monitor`,
   `rules`, `surfaces`, `allocation`, `expect`) are all read by `case_files`/`expected_ok`/
   `run_cases`; the fourteen `expect` keys (`rc`, `error`, `stage`, `box`, `boxes`, `reserved`,
   `band`, `expected`, `attributed`, `gt`, `attr`, `attr_ns`, `ls`, `verdict`) are all read by
   `expected_ok` against `parse_result`. No dead key. One dead branch: `case_files` supports
   `layers_raw`, but no case in the 47 carries it.
3. **Dead keys, C2.** The ten case keys are `name`, `argv`, `kind`, `value`, `skill_anchor`,
   `samples`, `negatives`, `frozen`, `fixtures`, `tool`. `tool` occurs on the four refusal cases
   and is read by nothing in `quality/counters/c2-r82-runbook.py` (the tree binding at `:656-660`
   pins `tools/mado-barfoot.py` wholesale; execution uses `case["argv"]` at `:685-697`) — a dead
   key on 4/29 cases. The nested `rc`/`out` of `samples` and `negatives` are both read
   (`:447-451`). Document-level `lane`/`round` are unread metadata.
4. **Unused mutants.** Every one of the 34 C1 and 25 C2 mutants is scored by the counter it lives
   in; at the freeze the kill receipts print 34/34 and 25/25 (`measurement-c1-r82.txt:48-81`,
   `measurement-c2-r82.txt:31-55`), and every C1 anchor occurs exactly once in the frozen tool
   (the counter refuses otherwise, `:299-301`).

## Gate (sources opened this round)

Census at round start (2026-11-04): base `6ea2386d` → **415 registry rows**
(`git show 6ea2386d:corpus/SOURCES.md | grep -c '^| S'`);
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
/home/vgpnk/Projects/shokunin mado` → exit 0 with one standing warning, `W04 S477 duplicate url
…/tests/desktop/Reserved.cpp across scopes` (`receipts/census-start-r82.txt`). At the content tip
`3ec7fb75` → **418 rows** (415 + S481 + S482 + S483-rejected). No older row's
`status`/`recheck`/`used-by` cell moved.

| row | source and locator (opened 2026-11-04) | status | located quote (≤25 words) | what it licenses / does not |
|---|---|---|---|---|
| S481 | https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/protocols/wlr-layer-shell-unstable-v1.xml — `set_size` `:122-137` (zero clause sentence `:128-129`), `configure` `:327-353` (zero-size sentence `:347-348`); sha256 `87e0b9c8…`, 19326 B (`.ufo/waves/round-82/fetch/S481.xml`) | mined (new) | `If the width or height arguments are zero, it means the client should decide its own window dimension.` (at `:347-348`) | that a zero width/height delegates the size to the client, so the band is the client's allocation; it does not say what waybar sends on this host, and it is the protocol the pinned Hyprland tree vendors, not a version read off the host. The same file's `set_size` zero clause sentence (`:128-129`) says the compositor assigns and informs; both point the same way |
| S482 | https://raw.githubusercontent.com/KDE/kstatusnotifieritem/v6.2.0/src/org.kde.StatusNotifierWatcher.xml — whole file 1151 B, interface `:3`, methods `:6`/`:10`, property `:17`; sha256 `19df7f18…` (`.ufo/waves/round-82/fetch/S482.xml`) | mined (new) | `interface name="org.kde.StatusNotifierWatcher"` (at `:3`) | the KDE-owned bus name and its two register methods, which the round's three rows bind; it does not say the host's waybar owns that name (the live `busctl` read does) |
| S483 | https://www.freedesktop.org/wiki/Specifications/StatusNotifierItem/StatusNotifierWatcher/ — page head, 6395 B, sha256 `f22928e1…` (`.ufo/waves/round-82/fetch/S482.html`) | rejected | `There will be a single org.freedesktop.StatusNotifierWatcher service instance registered on the session` (at the page head) | REJECTED as a grounding row: it names the freedesktop-prefixed bus name, which the round's rows would contradict; flip: re-point a row at the freedesktop spelling on a host that advertises it, or a revision-pinned page that uses the KDE spelling |

**Precision notes (for the L1, not corrections to frozen text).**

- **S481 anchors, verified from `fetch/S481.xml`:** `set_size` opens `:122` and closes
  `</request>` `:137`, its zero-clause sentence is `:128-129`; the `configure` event opens `:327`
  and closes `:353`, its zero-size sentence is `:347-348`. The row first landed (`3ec7fb75`) as
  "`set_size` `:122-142`, clause at `:347-348`" — the span overran the request by five lines and
  the quote belonged to `configure`. A worktree revision at 10:37 (uncommitted, `corpus/SOURCES.md`
  `M`) reads "`set_size` `:122-138` (zero clause `:128-131`) and the `configure` event's zero-size
  sentence `:347-348`" — the split is now right, but the request span still overruns `:137` and the
  quoted sentence ends at `:129`, not `:131`. The row's bytes and hash are right; the verified
  spans above are the ones a re-anchor should use.
- The declaration's S481 locator, `set_size` `:116-123`, matches nothing in the pinned bytes
  (`set_size` opens at `:122`). The claim's substance is unaffected; the line number is not
  re-derivable from `fetch/S481.xml`.
- S483's cited capture `.ufo/waves/round-82/fetch/S482.html` is present in the worktree and
  verifies: 6395 B, sha256 `f22928e1…`, listed in the worktree's `fetch/sha256-r82.txt`. It
  postdates the `3ec7fb75` content commit and was still uncommitted at this writing (worktree
  `??`, sha file ` M`), so the row's citation is valid only once the L1 commits the capture with
  it; the 6395 B and hash reproduce from the URL either way.
- **L1 correction (applied at the round-82 erratum-era commit).** The S481 registry row now reads
  `set_size` `:122-138` (zero clause `:128-131`) and the `configure` event's zero-size sentence
  `:347-348`, and its quote is the `set_size` clause; `corpus/README.md:133,186` were corrected to
  the same anchors. The declaration's `:116-123` locator is frozen and is not rewritten — it is
  disclosed in the round report as declaration anchor drift, with the pinned bytes as the ground.
  The `S482.html` capture and the `fetch/sha256-r82.txt` line are committed with this correction.

Assimilation: **none** this round (the round's §2b record; not re-derived here).

## Next round

C1's next finite grounds are the extra surface whose band is dynamic — today `--allocation` for an
extra's namespace passes the unknown-name check and is inert, not a model
(`corpus/knowledge/bar-footprint-allocation-r82.md` §5.2), so it needs a `--surfaces` allocation
grammar and cases that exercise it — and fractional scale, which needs the monitor and layer spaces
reconciled (§5.3). C2's next ground is the tray item count (`RegisteredStatusNotifierItems`) once
the host has at least one item, or the `StatusNotifierHost` registration as a second state pair.

## Erratum (append-only, round 82)

E1 — the C2 instrument was re-cut after the sentinel's F1/F2 and re-measured at `89acb06c`: the three
new cases' fixtures lost the account name, real bus addresses, UID-derived unit and live PID (control
set sha256 `f64d7d5d…` → `07599b24…`), and `run()` now pins `TMPDIR` to the caller's scratch root
rather than the measured tree (counter sha256 `1e8eb499…` → `a87bceab…`). No case kind, expectation,
carried case, predicate or target moved; the contract line is identical at the new revision. The
carried round-81 `waybar-pgrep` case still carries a live PID and cannot be edited under the
carried-unchanged assertion — a superseding set is the round-83 fix.

E2 — at `12e6ad57` the reviewer's finding was applied: an `--allocation` entry for a surface the
join does not resolve is now a setup refusal instead of an accepted-and-inert entry (tool sha256
`38007528…` → `58ef4f6a…`), and both claims re-measure to the same contract lines at `12e6ad57`.
The runbook's count cells were corrected at `df6c613d` (`tray-methods` 1/3 → 2/3, the carried
`keybindings-chords` 2/7 → 2/8) and `tray-owner`'s PID wording no longer claims a ceiling the
matcher does not enforce; the `--selftest` transcripts now sit under `receipts/`. The frozen
declaration's S481 locator and its pre-erratum controls sha are disclosed, not rewritten.


## Wave-routed defects (append-only, round 82)

- **V7 (high), open.** The C1 counter does not force the declared allocation to be the band source
  (the critic's live-box candidate scores 47/47; no case expects `box=DIFFER`, so
  `tools/mado-barfoot.py:1025` is unexercised). Round 83: an `alloc-live-band-differs` case plus a
  `box-verdict-blind` mutant.
- **V8 (low), open.** The C2 predicate's `control_new=0/3` is tautological by construction; the
  substantive control is the held instrument's setup refusal. Round 83 drops the clause.
- **V9 (low), open.** `--no-mutants` is parsed but unguarded in the C1 counter.
- **V1 (medium), open.** The C1 mutation list omits the vertical band branch (`band_of` for
  left/right); the reviewer's own mutant dies on `alloc-dyn-width-dock`, so the case is live.
- **Fixed in-round:** the inert allocation entry (E2), the two false runbook cells and the
  `tray-owner` PID wording (`df6c613d`), the `--selftest` transcripts (now under `receipts/`), the
  three new-case fixture identifiers and the counter's `TMPDIR` (E1).
