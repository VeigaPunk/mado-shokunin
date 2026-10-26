# CritAssimilation — report (mado r43 w2)

Seat: `CritAssimilation` (critic, leaf). Target: the round-43 **assimilation decisions** — the five `ADMIT`/`REFUSE` lines and the
`## Assimilation ledger` of `corpus/lessons/round-43.md` @ `1959770657f1f8665097c1aed4be6c1cbb07139f`, tested against the five decided
staged files (`/home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge/`, read-only), the landed entry
`corpus/knowledge/hyprland-gkeep-geometry-r43.md`, the ten pins, `corpus/SOURCES.md`, `PROVINCE.md`, `MERGE-REPORT.md`, the counter's
`STAGED` set, and the w1 reports. Full findings: `.ufo/waves/round-43/w2/CritAssimilation/findings.md`. Quotes verified by
`verify-quotes.py` → `QUOTES: checked=43 miss=0` (`verify-quotes.txt`). Nothing was judged, admitted, edited, integrated or shipped; the
counter, controls, registration and data commit are untouched.

## Headline

**F1 (high) — the `r30` refusal's flip condition was already met when the ledger was written.** `lesson:49` refuses
`gkeep-element-rules-r30.md` because "the 875x600 explanation rests on a config comment and not on any pinned measurement" and flips "if the
stock floating-tag size is measured or sourced from the shipped config". The shipped config carries it:
`~/.local/share/omarchy/default/hypr/apps/system.conf:4` `windowrule = size 875 600, match:tag floating-window` (with `float on` `:2`,
`center on` `:3`; mtime `2026-10-03`, before the round) — the fact was in the round's own receipts (a pin is one byte copy away, as `S295`
was made), and w1 had already captured it — `w1/ExecLiveHost/live-census.txt:232` and
`w1/ExecLiveHost.md:81`. The ledger did not consume its own round's receipt. Second half: the flip names only the *number*, so it cannot
test the row's other grounds; the shipped bytes also show the "work-around" inference (`r30:27`) is wrong in kind — the rule sizes windows
carrying the `floating-window` **tag**, and the host's gkeep file deliberately does not tag gkeep (`r30:23`, `host-gkeep.conf:2-4`).
Correction: split the row into two claims with one flip each, record the number's flip as fired and source `apps/system.conf` as an own-work
row; keep the "predates the chain / wrong in kind" ground with its own flip.

**F2 (high) — the ADMIT claims "its four-link chain"; the entry manifests three links and an accessor.** `entry:17` says four links; the body
carries the floating-algorithm → target → window legs (`entry:40-46`) and then cites S294 only for the `GEOMETRIC_GOAL` accessor
(`entry:52`, `:19`). Link four — the write `*m_realSize     = x.size();` at `Hyprland-GeometricMovableAnimated.cpp:45`, which the staged
file quotes at `r11:54` — appears in neither the entry nor S294's declared ranges (`:39-41 resize, :53-59 the two animation handles`;
`sources-at-1959770.md:243`, so `:43-46` is absent), although the bytes are in the pin. The entry's §3 INF ("a `clients -j` size equal to
the rule's size says that the compositor's target equals the rule", `entry:56`) needs that write. Correction: append the link with locator
`:43-45` (Gate for S294 stays), or restate `entry:17` to "three-link chain plus the `GEOMETRIC_GOAL` accessor" and downgrade the INF.

**F3 (medium) — `r8`'s flip cannot be evaluated.** `lesson:47` flips "if its identity receipt is re-sourced inside this lane". Literally that
receipt is the private path `r8:8` (`lanes/mado/round8/fetch/…`), which cannot inside this lane exist (package carries no `lanes/` tree;
`git ls-tree -r --name-only HEAD | grep -c 'round8/fetch'` → 0, re-run). As intended (the build identity) it has already fired:
`receipts/live-geometry-host.txt:3` carries `Hyprland 0.56.2 built from branch v0.56.2 at commit efb50993780079460b0cbed1363e2166a2de1d9f
clean`, but no SOURCES row does. The verdict survives on its other grounds (census 3 vs the pinned 4; "Nothing else is missing" refuted), so
this is a record defect: rewrite the flip to name the host build identity as a row, and record that the other grounds are already refuted.

**F4 (medium) — the `obs-route-r11` flip points away from its own reason and is already literally true.** Reason (`lesson:48`, true: exactly
one `source:` line, `obs:8`) is redundancy; the flip is "if an independent witness for the observation route is added" — adding witnesses
makes the file *more* redundant, and this round added them (S296 census; the oracle read at `w1/ExecOracleGkeep/20-observation.txt:7`).
`MERGE-REPORT.md:136` keeps a refused row frozen "until the stated reason is cleared", so the record now holds a fired flip with an unmoved
verdict. Correction: flip on the *surviving* witness (S158's GOAL read / the entry's §5 census), not on the supply of witnesses.

**F5 (medium) — `r10`'s refusal is correct but understated, and its flip's trigger is adjudicated only in an unadopted file.** The reason is
TRUE of the file (`r10:45-47`, "whatever the client actually used"); the pinned write (`:45`) refutes it. Uncited: the oracle experiment —
a client whose own buffer is 200×200 (`w1/ExecOracleGkeep/20-observation.txt:19`) still reports `"size": [420, 500]` under the host rules —
an experimental falsifier, stronger than the source argument the row gives. The flip's trigger ("the client's acknowledgement") is exactly
what `r13:39` pins the other way ("it cannot substitute a different number"), and r13 is left as residue (`lesson:81`) with no
cross-reference from the r10 row. Correction: cite the oracle receipt and the `onAck` cross-reference in the r10 row.

**F6 (low) — three residue-row cells are wrong or unsupported.** (a) "three journal sweeps" (`lesson:81`): r15's decisive source is a
lane-artifact grep (`r15:7`), not a journal — two journal sweeps plus one artifact sweep (r13 `:12`, r14 `:9`); "the map-time DEBUG log" is a
line in S319, not a source. (b) The r14 scope cell says "in" flatly and drops w1's boundary ("borders on tsukuroi's journal ground",
`survey.md:95`), on the row that would authorise a later adoption; the lane's own journal instrument is bounded to one unit
(`PROVINCE.md:31`). (c) r9's held cell "partly held as prose (no lane row cites it)" (`lesson:79`) is unlocatable: no base lane text carries
r9's claim; the nearest prose says the opposite (`config-drift-r12-at-base.md:116`, "gkeep rule bodies and their per-window effects remain
unexamined").

**F7 (medium) — "admitted as the successor" narrows the file's headline without recording it.** r11's title says "so the rendered geometry is
settled" (`r11:2`, `:66`); the entry answers "Is the GOAL the size drawn on screen?" with UNK (`entry:27`) and opens "What this entry does
not establish" with the drawn size (`entry:78`). The entry is right; but the merge appends and keeps the staged reading
(`MERGE-REPORT.md:133`), so both texts will stand with no ledger line choosing. Correction: record in the ADMIT row that the entry keeps the
four-link mechanism and narrows "settled" to "the GOAL equals the rule; the drawn size remains UNK".

## What I checked and found sound

ADMIT sourcing (4/5 pins by file identity; every r11 quote in the pinned bytes: DefaultFloatingAlgorithm `:55`, `:60`, `:96`; Target `:10`,
`:11`; WindowTarget `:50`, `:71`); the base-holdings grep re-runs (rc=1, no hits); the entry's "no read verb exposes CURRENT" holds in the
pinned HyprCtl (`GEOMETRIC_GOAL` only, lines 426-428/447-448); the held-row choice for S155/S158 is supported (S158 already cited by
`rule-attribution-r24.md`); province fit of the five decided files holds (source-read precedent `rule-attribution-r24.md`; app half as chain
evidence, `host-bar-producer-census-r40.md:37`); and the ledger covers all 11 files in the counter's `STAGED` set
(`c2-r43-gkeep-entry-v2.py:92`) across nine rows, so no candidate is silently undecided (an earlier reading of mine suggested four were
missing; the table continues past r12 — corrected before writing).

## Safety / tooling

No host or compositor mutation; no `hyprctl`; no Wayland/socket connection; only read-only file reads (`grep`, `sed`, `stat`, `git show`) —
the host config reads were `~/.config/hypr/hyprland.conf` and the read-only `~/.local/share/omarchy/` checkout. Read-only git only; no
mutating git/jj anywhere. `/home/vgpnk/Projects/shokuknow` read-only. Writes only under
`.ufo/waves/round-43/w2/CritAssimilation/` and this file. No tool installed (none needed). Scratch
`/fast/scratch/hyaku/mado-r43/CritAssimilation` was created empty and removed at finish; nothing left on disk.
