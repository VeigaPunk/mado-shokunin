# Lessons — mado, round 41

Round intent: registration `.ufo/waves/round-41/registration.md` (freeze `60c3914154333180450d5da27ba222d5763cc56a`,
base `ab2bfaab661c846d1de9d58c01651cd156a13949`, the round-40 tip). Host `2026-10-25`, Hyprland 0.56.2
(`efb50993780079460b0cbed1363e2166a2de1d9f`), xdph v1.4.1 (held row S037, `corpus/SOURCES.md:49`). C1 lands `tools/mado-globals.py`
(operability, capability acquisition): a read-only census of the globals the compositor advertised to its desktop portal,
read from the user journal — sessions, per-global version and count, a fixed class decision table, `--diff`,
`--expect NAME`, `--live` (one allowlisted program, exact argv, bounded output), `--selftest`; target
`fixtures=24/24 verdict=TARGET_MET` under `PRED-C1-r41-v1`, base `0/24 tool=absent` (`receipts/c1-before-base.txt`).
C2 admits `corpus/knowledge/hyprland-focus-grab-r41.md` (coverage, sourced): the Hyprland focus-grab protocol as a
focus-control surface — the compositor-side semantics, its advertisement on this host (own-work journal census), a real
client's grab lifecycle, the rule-level counterpart; target `admitted=1/1` under `PRED-C2-r41-v1` (clauses a–i), base
`0/1` (`receipts/c2-before-base.txt`).

Shape: **two v1 waves** — `w1` of 34 seats (build + first falsifiers, dispatched at `cd950ec`:
`round-41: wave w1 spec and dispatch (34 seats)`, `w1-spec.json` `items` length 34), `w2` the residual call. Lane axes
this round: **operability** and **coverage**; every published axis ties at its maximum at base (`receipts/axis-base.txt`:
navigation 58/58, calibration 55/55, operability 12/12, `MADO_AXIS checked=3 mismatched=0 rev=ab2bfaa…`), so each is a
lowest axis and the stagnation nudge is not needed.

**Freeze/dispatch conflict, recorded verbatim (not repaired here).** The frozen registration's shape line
(`registration.md:4`) reads "Shape: one v2 wave `w1` of 64 seats (policy v2, band 64–128), no residual call, round total
64.", while the dispatched wave is 34 seats in `w1` of two v1 waves (`w1-spec.json`; commit `cd950ec`). The registration
is frozen and is not edited; if the shape line binds, the L1 re-registers as `registration-v2.md` before any data commit
and discloses the order, as the registration's own residual clause and round 40 both do. Mistake M41-5 carries this.

<!-- Shape of the Gate lines, kept OUTSIDE ## Gate on purpose (placeholders are not landable text in the section):
     one line per CITED id, column 0, exactly one per id — "GATE <id> receipt=.ufo/waves/round-41/fetch/<file> sha256=<64 lowercase hex> quote=\"<3-25 words>\""
     (PRED-C2-r41-v1 clause d: receipt committed at REV under .ufo/waves/round-41/fetch/, >= 512 bytes, sha256 equal to the bytes,
     path/sha256/quote distinct per id, quote present in the receipt's normalized text — tags/scripts/styles stripped, entities
     decoded, whitespace collapsed — and 3-25 words; clause g binds each Gate quote to the entry line that names the id).
     The seven lines in the section carry digests recomputed from the committed bytes (`quotes.py`: gates=7 bad=0). -->

<!-- Conditional Gate lines, landable as column-0 lines only. (1) S037: entry draft A cites the held row, so the final lesson needs this line AND the receipt committed byte-identically first (1442 B, verified against .ufo/waves/round-41/w1/ScrEntryA/s037-installed-version.txt) — GATE S037 receipt=.ufo/waves/round-41/fetch/xdph-installed-version.txt sha256=4294737aa884fd84c2e2a6bf642efa71c281bc480df4f07eb64009d812157ea8 quote="%NAME% xdg-desktop-portal-hyprland %VERSION% 1.4.1-2" . (2) S290: only if the entry cites input-capture-v1.xml — GATE S290 receipt=.ufo/waves/round-41/fetch/input-capture-v1.xml sha256=fff89f6f9de622fefa1a62a6e6970f76683b6328454565583046abebcfe2c360 quote="This protocol is a bridge of the XDG input capture to the compositor." -->

## Gate

GATE S283 receipt=.ufo/waves/round-41/fetch/focus-grab-v1.xml sha256=0bc60c14d27f9079e0d1d9d706f91e67ad7da585f3b7f34ff7186a376c0285b4 quote="This interface restricts input focus to a specified whitelist of surfaces"
GATE S284 receipt=.ufo/waves/round-41/fetch/Hyprland-FocusGrab.cpp sha256=53b762f7149bf1c3105ec1da2137d02cc7bece90043d9a2ce253a784b092aff1 quote="m_grab->m_keyboard = true;"
GATE S285 receipt=.ufo/waves/round-41/fetch/quickshell-grab.cpp sha256=6f7cecf15a4dbfd0dc39341c8794639595a83dd2a4ab13b6b377ac970a301a40 quote="the protocol will always send cleared() when the grab is deactivated,"
GATE S286 receipt=.ufo/waves/round-41/fetch/xdph-PortalManager.cpp sha256=15c3e39cea5af1a92924ebc1ffe0f7825c86ac3c0b49e894aede86b2e091ea55 quote="Got interface: {} (ver {})"
GATE S287 receipt=.ufo/waves/round-41/fetch/issue-565.html sha256=148a9053e813a7d912c3c2e9fdb234ef42d20004438d33b41f1110d37679d1dc quote="Tried to set workspace silent rule to a nofocus window!"
GATE S288 receipt=.ufo/waves/round-41/fetch/protocols-README.md sha256=3c7007636e13889860491d0c57f93c29d92122d17838ca1f6559e4aeb7aa6323 quote="for grabbing input focus, primarily for complex context menus"
GATE S289 receipt=.ufo/waves/round-41/fetch/xdph-journal.txt sha256=bf8fa91a321197277cf9c1260d17524e9ddf862f7f76ddf440fc057aa600aaf7 quote="Got interface: hyprland_focus_grab_manager_v1 (ver 1)"

ADMIT merge/mado/knowledge/corpus/knowledge/focus-grab-protocol-live-on-host-r14.md as corpus/knowledge/hyprland-focus-grab-r41.md
REFUSE merge/mado/knowledge/corpus/knowledge/privileged-client-surface-r29.md reason=generic Wayland analysis, one truncated quote, no measurement and no host state
REFUSE merge/mado/knowledge/corpus/knowledge/focus-control-surfaces-r28.md reason=section 3 rests on a localized (Japanese) documentation channel, outside PROVINCE.md

Receipts above are committed at the freeze (`git ls-tree -r --name-only 60c3914 .ufo/waves/round-41/fetch/` lists the nine
files; the seven digests in this section were recomputed from the committed bytes by `quotes.py` → `gates=7 bad=0`). The quotes
are the ones entry draft A carries on its OBS lines (`w1/ScrEntryA/gates.txt`, re-verified here against the receipts); clause g
binds the Gate quote to the entry line that names the id, so if the L1 lands a different draft the quotes are taken from that
draft and `quotes.py` re-run — the invariant is *Gate quote == entry line quote*, not "any substring of the receipt". The final
entry is draft A and cites **eight** ids, so the landed lesson must carry exactly eight GATE lines: the seven above plus S037.
The S037 line is one commit away: the receipt `fetch/xdph-installed-version.txt` does not exist at the freeze (M41-6), and the
exact landable line sits in the comment above the section (1442 B, sha256 `4294737a…`, verified against
`w1/ScrEntryA/s037-installed-version.txt`). S290 is **not** cited by the final entry: do not add its line (it stays in the same
comment only as the form to use if the entry ever changes), and S290's registry row must not list the entry in `used-by`. The
own-work row S289 is the saved journal
(`journalctl --user -u xdg-desktop-portal-hyprland --no-pager -o short-iso` output, 19130 B, 153 lines); the counter's own
parser reads it as `journal sessions=2 adverts=78 interfaces=63 focus_grab=1` (measured this seat with
`c2-r41-focus-entry.py`'s `journal_counts`), and the entry must carry exactly that line, verbatim, once, outside fences
(clause h).

## Assimilation ledger (theme: focus control surfaces; package `merge/mado/`, read-only)

| candidate | scope (PROVINCE) | held | quality bar | verdict |
|---|---|---|---|---|
| `focus-grab-protocol-live-on-host-r14.md` | in (protocol bytes, host journal, client source) | the lane holds no focus-grab text at base (`git grep -lEi 'focus_grab\|focus-grab\|focus grab' ab2bfaa -- corpus PROVINCE.md SKILL.md tools` empty) | its S328–S332 rows are the package's ids with no lane receipt; re-grounded this round as C2 with lane ids S283–S290 | **admitted as the successor** (`ADMIT` above) |
| `privileged-client-surface-r29.md` | in, narrowly | — | one source (a blog post), one truncated quote, no measurement, no host state | **refused** (`REFUSE` above) |
| `focus-control-surfaces-r28.md` §3 | **out** — localized-documentation channel (`PROVINCE.md:75`: "documentation written in a localized channel — is outside the province") | its §1–§2 ground (issue #565, the protocol XML) is re-sourced by S287/S283 from the lane's own receipts | its third source is `amgsk.dev` (`/ja`-channel post); clause i refuses any cited row whose location carries `amgsk.dev` | **refused as written**; the unheld English-channel facts return in the successor |
| the focus-grab r8–r15 series, `compositor-focus-manipulation-literature-r26.md`, `wayland-input-security-literature-r8.md` | in | partly held as literature (r26, r8) | none of their rows is re-grounded this round | not adopted; no row cites them (ScoutPackageFocus owns the residue) |

Id mapping is by document, never arithmetic (`assimilation/id-guard.md`, seat `ExecAssimIdGuard`): the lane registry tops at
S282 (219 rows at base, `git show ab2bfaa:corpus/SOURCES.md | grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'`), and
the new rows continue at S283 in the order `ScrRowsDraft` drafts: focus-grab-v1.xml S283, Hyprland `FocusGrab.cpp` S284,
quickshell `grab.cpp` S285, xdph `PortalManager.cpp` S286, issue #565 S287, hyprland-protocols README S288, the own-work
journal S289, `input-capture-v1.xml` S290. `Hyprland-FocusGrab.hpp` is fetched but carries no id; it is corroboration, not a
row.

## Round-40 closure items (from `corpus/lessons/round-40-verifier-spotcheck.md` §6)

D1 (untracked dispatch marker): round-40's `.ufo/waves/round-40/w1.ready.dispatched` is tracked at HEAD and entered the tree
in this round's freeze commit (`git log -1 -- .ufo/waves/round-40/w1.ready.dispatched` → `60c3914`); the same marker is
untracked again for round 41 — see M41-3.
D2 (tip axis receipt): still open. `git ls-tree -r --name-only ab2bfaa quality/receipts/` lists only
`axis-520c631d2925807aadadb041eeda13f8b829b0c5.txt` (round 36) and `red-axis-publication-stale-at-data-commit.txt`; no
`axis-fb49621…` receipt exists. See M41-4.
D3 (fresh-nonce re-run of the round-40 v2 counters, committed as lane evidence): not done in this wave's receipts — the eight
files under `receipts/` are the freeze's own (base axis, two base counter runs, two control receipts, the census, the suite
baseline, the freeze counter check). The re-run remains a `w2` candidate, not a claim of this lesson.
D4 (SHONEN boxes stay `[~]`): unchanged; the spot-check names SKILL.md decision tables, PROVINCE rows and a cross-domain-bleed
check as the unmeasured items, so nothing is promotable from it.

## Mistakes

**M41-1 - two single-edit mutants of the reference were equivalent; only the two-site edit is killed.** Class: a mutant whose
edit site is duplicated in the reference is not a single-defect mutant — each single edit is a no-op because the sibling site
still performs the work. Evidence: the reference dedupes twice, `c1/ctl-ref-tool.py.txt:139`
(`missing = sorted(set(e for e in expects if e not in names))`) and `:227`
(`lines, code = report(parse(data), sorted(set(args.expect)), args.diff)`); the frozen control row `ctl/run-c1-controls.py:44`
therefore edits both sites. Measured this seat at the freeze rev with the frozen counter: `m09-a-line139.py` (line 139 only) →
`fixtures=24/24 tool=present verdict=TARGET_MET`, rc 0 (nonce `f274be9b2cebe486`); `m09-b-line227.py` (line 227 only) →
`fixtures=24/24 … TARGET_MET`, rc 0 (nonce `c9ea24a7e48b8c7b`); `m09-c-both.py` (both) → `fixtures=23/24 … TARGET_MISSED`,
rc 1 (nonce `fb1f5c8e72297d1e`) — outputs `.ufo/waves/round-41/w1/ScrLessonSkeleton/m09-*.out`, exit codes `m09-rc.txt`, the
mutant sources beside them. The registration calls the 43 mutants "single-defect mutants / single-edit cheats"
(`registration.md:45`); M09 is neither. Captured-by: none — found while authoring the controls before the freeze, and the
registration's wording kept the single-defect reading. Fix: the control row stays a two-site mutant and the redundant dedupe is
named as the reason. Shown able to fail: `receipts/ctl-c1.txt` M09 `fixtures=23/24 … TARGET_MISSED` — the two-site control is
killed, and the two single-site variants above are not.

**M41-2 - ten of the 43 C1 mutants are killed by exactly one fixture.** Class: a one-fixture kill margin — one fixture class
carries ten controls. Evidence: `receipts/ctl-c1.txt` scores M09, M12, M19, M20, M21, M23, M24, M26, M27 and M37 at
`fixtures=23/24` (10 of 43; the next-highest band is 22/24, held by nine mutants: M03, M05, M06, M07, M16, M28, M29, M30,
M38). Captured-by: none — the freeze's own control receipt. Fix: none; this
is a declared limit, not a defect: the fixture lattice on the tree index (QUALITY criterion 65) makes the margin deterministic,
so a future fixture-set edit that drops the carrying class is visible as these ten rows rising. Not shown able to fail: no
control isolates the class; the receipt lines are the measurement.

**M41-3 - the dispatch marker is untracked again, one round after the spot-check routed it.** Class: a driver artifact written
into the wave tree and never committed. Evidence: `GIT_OPTIONAL_LOCKS=0 git status --porcelain` at the lane root →
`?? .ufo/waves/round-41/assimilation/`, `?? .ufo/waves/round-41/w1.ready`, `?? .ufo/waves/round-41/w1.ready.dispatched`
(20 B, `2026-10-25T19:59:05`) and `?? .ufo/waves/round-41/w1/` (the seat tree, untracked until the closure commit; the first
three are driver/L1 artifacts, not seat output); the
round-40 marker is tracked (`git ls-tree -r --name-only HEAD .ufo/waves/round-40/` lists it, committed by `60c3914`).
Captured-by: `round-40-verifier-spotcheck.md` §1 "leftovers" row and §6 item 1 — captured by the closure verifier one round
late, which is why it recurred. Fix: the closure commit carries both markers (as this round's freeze commit did for round 40's),
or the driver stops writing them into the wave tree — the driver is operator-owned, so the lane can only do the first. Not shown
able to fail: the observable is `git status --porcelain -- .ufo/waves/round-41` empty at closure; no instrument asserts it yet.

**M41-4 - a tip observable was claimed without a committed receipt, and the instrument that names the rule is scoped to another
round.** Class: evidence pointer without committed bytes. Evidence: `round-40-verifier-spotcheck.md` §1 defect (b) — the round-40
report cites `MADO_AXIS … rev=fb49621…` but only `receipts/axis-base.txt` is committed; `git ls-tree -r --name-only ab2bfaa
quality/receipts/` lists no round-40 tip transcript; `quality/check-evidence-pointers.py` declares `tip_axis_transcript == 1`
(a committed `quality/receipts/axis-<40hex>.txt` whose `MADO_AXIS:` line reads `mismatched=0 rev=<40hex>`) but reads the
round-36 records only. Captured-by: none in round 40; the conjunct exists and was proved able to miss —
`.ufo/waves/round-36/w1/reports/ExecPtrFixtures.md:45` records `tip_axis_transcript=0 … verdict=TARGET_MISSED`, and
`MutPtrTipAncestor` refuted F48 by showing a non-ancestor and a rev-mismatch receipt are both rejected. Fix: round 41 commits
`quality/receipts/axis-<40hex>.txt` for the tip revision in the same shape as the round-36 file. Shown able to fail:
`ExecPtrFixtures.md:45` (a `tip_axis_transcript=0` receipt) plus the round-36 mutant report.

**M41-5 - the frozen registration's shape line contradicts the dispatched wave.** Class: freeze document versus dispatch
mismatch. Evidence: `registration.md:4` "Shape: one v2 wave `w1` of 64 seats (policy v2, band 64–128), no residual call, round
total 64." against `w1-spec.json` (`items` length 34), commit `cd950ec` "round-41: wave w1 spec and dispatch (34 seats)" and
`w1.ready` (`{"lane":"mado","round":41,"wave":"w1",…}`); 34 is also below the registration's own band floor of 64.
Captured-by: none. Fix: `registration-v2.md` before any data commit, disclosing the order (the registration's residual clause
allows exactly this). Not shown able to fail: no control compares a registration's seat count to the spec's item count.

**M41-6 - the C2 Gate contract demands a round-41 receipt for every cited id, and the frozen fetch set has none for the held row
the entry drafts are told they may cite.** Class: a per-cited-id receipt requirement against a fetch set that covers only new
ids. Evidence: clause d binds the receipt under `.ufo/waves/round-41/fetch/` (`path.startswith(FETCH)` in
`quality/counters/c2-r41-focus-entry.py`), `git ls-tree -r --name-only 60c3914 .ufo/waves/round-41/fetch/` lists nine files
(none for the xdph v1.4.1 release page behind held row S037), and the entry prompts in `w1-spec.json` say "Cite at least one held
id if it fits (S037 xdph release)". Captured-by: none. Fix: the entry either does not cite S037, or the L1 copies the seat's
receipt into `fetch/` byte-identically before the data commit — it exists at
`.ufo/waves/round-41/w1/ScrEntryA/s037-installed-version.txt` (1442 B, sha256 `4294737aa884fd84c2e2a6bf642efa71c281bc480df4f07eb64009d812157ea8`,
quote verified in its normalized text), so the repair is one commit, and the landable GATE line is in the comment above `## Gate`
(data, not predicate, and disclosed). Shown able to fail: `receipts/ctl-c2.txt` controls
`N03-gate-sha-wrong` and `N14-receipt-outside-fetch-with-bytes` both read `clause d:0` — the clause bites on a receipt it cannot
bind.

**M41-7 - the v1 predicates are exposed to falsification after seats have scored them.** Class: a predicate repaired after
scoring (the round-40 M40-5 pattern). Evidence: `registration.md` residual — "The wave may falsify these predicates; if so the L1
re-registers as `registration-v2.md` before any data commit and discloses the order, as round 40 did"; `w1-spec.json` dispatches
five falsifier seats (`RevC1Counter`, `CritC1Cheat`, `MutC1CounterGates`, `ExecC1ExtraMutants`, `ExecC2ExtraMutants`); round-40's
pair `receipts/c1-v1-after-data.txt` (13/13 but `TARGET_MISSED`) versus `receipts/ctl-c1-v2.txt` is the record of the pattern.
Captured-by: PROTOCOL claim-sizing, as M40-5. Fix: none that removes the fact — the disclosure rule (re-register before data,
state both scores at the data tip) is the whole repair. Not a gate; this is a disclosure, as M40-5 was.

**M41-8 - a seat report written under another round's path (M40-6): watch, not a defect this round.** Class: seat path
discipline. Evidence: round-40 lesson M40-6 (`ConnCrossClaim` returned `.ufo/waves/round-49/w1/ConnCrossClaim.md`); the same
seat name is dispatched in `w1-spec.json`, and `.ufo/waves/round-41/w1/ConnCrossClaim.md` exists (104 B) at the right path as of
this seat's read. Captured-by: the wave context's trailer rule ("Every `Report:` trailer path is relative to
`/home/vgpnk/Projects/shokunin/mado-shokunin`"). Fix: the trailer is resolved against the lane root and the file checked at
closure. Not shown able to fail: no instrument asserts it; the round-40 defect was found by a human read of `w1-results.json`.

### QUALITY.md criteria (owned by seat `ScrQualityCriteria`)

No criterion is claimed here. The candidates 69+ drafted by that seat must each cite one M41 id above and name the control that
shows the check can fail: M41-1 (redundant edit site / mutant equivalence, control `ctl-c1.txt` M09), M41-2 (kill margin, the
ten 23/24 rows), M41-3 (untracked driver artifact, closure `git status`), M41-4 (tip receipt, `ExecPtrFixtures.md:45`), M41-5
(registration versus dispatch, none yet), M41-6 (held-id receipt, `ctl-c2.txt` N03/N14), M41-7 (post-scoring predicate,
disclosure only), M41-8 (seat path, none yet).

## considerthese

Seat `ScrConsiderthese` mines at most one still-unimplemented proposal of `considerthese/2026-10-25.md` (round 40 mined proposal
2); the chosen proposal, its ground and the exact text to land go in `.ufo/waves/round-41/w1/ScrConsiderthese/proposal.md` and
land here before the lesson is committed. No proposal is claimed by this skeleton.

## Census and measurements at the data commit

To be filled at the data commit (commands, in the order the round-40 lesson states them):

- Census before (`receipts/census-before.txt`, committed at the freeze): `mado ok`, W04 ×7 (S030, S042, S045, S097, S119, S120,
  S121) + W01 S277, exit 0. Census after: `receipts/census-after.txt`, exit 0 required, warning set unchanged or every new line
  named.
- Registry rows 219 → 219 + n, n = the cited new ids (at most S283–S290); tier A additions counted from the registry.
- Knowledge entries 58 at base (`git ls-tree -r --name-only ab2bfaa corpus/knowledge/ | grep -c '\.md$'`) → 59 with the C2 entry;
  every entry linked from `corpus/README.md` (clause f requires exactly one column-zero index row for the C2 entry).
- `PRED-C1-r41-v1` at the data commit: `fixtures=24/24 verdict=TARGET_MET` with the nonce printed; `PRED-C2-r41-v1`:
  `admitted=1/1 verdict=TARGET_MET`; both re-run at the tip.
- Suite baselines: `receipts/selftest-base.txt` `MADO_SELFTEST: 460/460 assertions passed`; the tip suite run and the tip
  `MADO_AXIS` transcript committed under `quality/receipts/axis-<40hex>.txt` (M41-4).
- The host receipt (`tools/mado-globals.py --live` against the running desktop) is reported, not scored: it is one allowlisted
  program, exact argv, bounded output; the C1 counter's sandbox is the scored boundary.
