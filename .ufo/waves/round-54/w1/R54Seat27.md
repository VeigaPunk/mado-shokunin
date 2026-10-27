# R54Seat27 — implementation simplification for PRED-C1-r54 and PRED-C2-r54

## Axes

- **Operability**: can both counters be built small enough that another seat can read, rerun and
  attack them, with every leg traceable to a frozen sentence?
- **Coverage**: does the simplified design still bind every frozen clause (four pins, six controls,
  three rows, host joins), or does it quietly drop one?

Scope: item 27 (simplify the implementation approach for both frozen counters without weakening
gates; identify unnecessary complexity; test a distinct failure/input from other seats). I built
minimal prototypes in scratch only; the lane was read-only for me.

## 1. What I simplified (measured, not estimated)

| artefact | checker core | total incl. fixtures/controls/CLI | frozen line at the round's rev |
|---|---|---|---|
| scratch `proto_c1.py` (no controls) | **139 lines** | 139 | `propositions=4/4 quotes=4/4 anchors=4/4 pins=4/4` `TARGET_MET` |
| scratch `proto_c1_full.py` (+6 controls, `--selftest`, `--work`) | 139 | **302** | `controls=6/6 verdict=TARGET_MET`, exit 0 |
| scratch `proto_c2.py` (+6 controls, fixture builder) | **138** | **323** | `controls=6/6`, exit 0 on the golden fixture |
| house `c1-r51-ledger.py` | — | 445 | — |
| house `c2-r50-session-gate.py` | — | 577 | — |
| house `c1-r50-bind-entry.py` / `c2-r49-bind-entry.py` | — | 1316 / 1280 | — |

Both r54 predicates are one-line verdicts over a handful of frozen constants. A conforming
implementation is ~140 lines of checking plus ~160 lines of fixture/CLI harness; ~300 lines per
counter, ~600 for both. The two most recent house counters spend 445 + 577 lines on predicates of
the same shape; the r49/r50 pair spends 2596.

### Removals that do not touch a gate

1. **No scratch clone of `--rev`.** `git cat-file blob <rev>:<path>` and
   `git ls-tree -r --name-only <rev>` read every byte the predicates name. r51's
   `resolve_rev`/`make_clone`/`listing`/`show` block (≈45 lines) plus a work-directory argument in
   `--repo` mode disappears; `--work` is needed only for control fixtures. The contract is "every
   byte comes from `--rev`", which object reads satisfy more directly than a clone.
2. **No nested checker run.** r51 spends ≈100 lines on `sandbox_env`, `run_python`,
   `checker_selftest`, `checker_ledger`, `normalise_checker` so that a second in-tree checker must
   agree. Neither PRED-C1-r54 nor PRED-C2-r54 names a checker, a second command, or a timeout.
3. **No semantic re-derivation for C1.** The four anchors, their exact spans and the three
   side-claim inequalities (`591 ≤ 619`, `622 ≤ 627`, `573 > 571`) are frozen constants; the
   counter evaluates them as constants. Nothing parses function bodies.
4. **One control harness, two uses.** Each counter builds one base fixture commit from the scored
   bytes and then six single-mutation commits (`git reset --hard` between), instead of six copied
   trees. ≈25–40 lines per counter.
5. **One normalization rule, stated once.** C1: newline+indent runs collapse to exactly one space,
   intra-line bytes untouched. This is *required*, not optional: P19's quote straddles the blank
   line 1555 and P21's straddles 620, so a naive "replace each newline with a space" yields a
   double space and `quotes=2/4` (observed with the first prototype version). It is also the only
   normalization the registration's judge rule permits (`registration.md:49-53`).
6. **C2 pin resolution is one function.** A row's pin is the explicit
   `pin .ufo/waves/round-54/fetch/<file>` token when present, else the locator basename; either way
   it is resolved against the fetch listing at the rev. 10 lines, and it accepts both frozen row
   shapes (registration's `<pin>:<lines>` form and the staged rows' `anchor @ commit; pin <path>`
   form).

### Kept deliberately (cheap, gate-relevant)

- C1 hashes **all four** inventory pins, and additionally every `SHA256SUMS` line whose file exists
  in the tree. See F3/F5 for why the four-pin numerator and the per-line leg are different things.
- C1 compares the entry's P19–P22 rows to the frozen table **byte-for-byte modulo trailing spaces**
  (`registration.md:21-23`). This is what makes every control reject before any semantic check runs.
- C2 counts host joins over the **frozen host strings with a line-token boundary** and requires
  ≥2 distinct, and binds the S375–S377 citation to the `source:` provenance line rather than the
  entry body. See F8/D5/D7.

## 2. Gates preserved (evidence)

Both commands, executed from `/fast/scratch/hyaku/mado-r54/R54Seat27`:

```
$ python3 -I proto_c1_full.py --repo /home/vgpnk/Projects/shokunin/mado-shokunin \
    --rev e25149fec8152a3aabd2b18a0ee8663b23cf65aa --work work
MADO_ERRATA_TRUTH: rev=e25149fec8152a3aabd2b18a0ee8663b23cf65aa propositions=4/4 quotes=4/4 anchors=4/4 pins=4/4 controls=6/6 verdict=TARGET_MET
exit=0
$ python3 -I proto_c1_full.py ... --rev 350d30e4ec5531f65ce99a57efeb8216f38e678a --work work
MADO_ERRATA_TRUTH: rev=350d30e4... propositions=4/4 quotes=4/4 anchors=4/4 pins=4/4 controls=6/6 verdict=TARGET_MET
exit=0
$ python3 -I proto_c2.py --repo .../mado-shokunin --rev e25149fe... --work work7
MADO_UWSM_ENTRY: rev=e25149fe... admitted=0/1 rows=0/3 controls=0/6 verdict=TARGET_MISSED
detail: pins absent at rev
exit=1
$ python3 -I proto_c2.py --repo .../mado-shokunin --rev 350d30e4... --work work8
MADO_UWSM_ENTRY: rev=350d30e4... admitted=0/1 rows=0/3 controls=6/6 verdict=TARGET_MISSED
  C2-CTL-1=reject  C2-CTL-2=reject  C2-CTL-3=reject
  C2-CTL-4=reject  C2-CTL-5=reject  C2-CTL-6=reject
exit=1
```

Control-by-control C1 legs (fixture repo, base = scored bytes):

```
C1-CTL-1 {propositions 3, quotes 3, anchors 3, pins 4}  MISSED
C1-CTL-2 {propositions 3, ...} MISSED     C1-CTL-3 {4,4,4, pins 3} MISSED
C1-CTL-4 {propositions 3, ...} MISSED     C1-CTL-5 {propositions 3} MISSED
C1-CTL-6 {propositions 3, ...} MISSED
```

Do-nothing control (§9) stays alive — an always-print variant of each counter, run through the
same harness, rejects 0/6:

```
C1 real counter controls rejected: 6/6      C1 do-nothing counter: 0/6
C2 real counter controls rejected: 6/6      C2 do-nothing counter: 0/6
```

The C2 golden fixture is built from the **frozen** row strings, not from the lane's staged rows.
On it, the predicate is reached only with a documented scdoc-emphasis normalization:

```
$ python3 -I proto_c2.py --repo ... --work work9 --selftest
selftest: golden={'admitted': 1, 'rows': 2, 'controls': 6} met=False
$ python3 -I proto_c2.py --repo ... --work work10 --selftest --emphasis
selftest: golden={'admitted': 1, 'rows': 3, 'controls': 6} met=True
```

## 3. Distinct failure/input tested (independent of the frozen controls)

C1 inputs (each a single mutation of the scored record; matrix from `distinct_c1.py`):

| input | minimal | semantic-only counter (row-authority + containment) | whitespace-loose | row-hash loop | four-frozen-only |
|---|---|---|---|---|---|
| D1 P20 anchor `:1576`→`:1574-1578` (a range that **contains** the true line) | reject | **ADMIT** | reject | reject | reject |
| D2 P19 quote cell `modMask,  0` (double space; drift, not trailing space) | reject | reject | **ADMIT** | reject | reject |
| D3 `SHA256SUMS` nibble on `Hyprland-ConfigActions.hpp` (**a frozen pin no row names**) | reject | reject | reject | **ADMIT** | reject |
| D4 `SHA256SUMS` nibble on `README.txt` (recorded, not in the four-pin inventory) | reject | reject | reject | **ADMIT** | **ADMIT** |

Required verdicts: D1/D2 are table drift (`registration.md:21-23`: "any drift is a
TARGET_MISSED"); D3 is a frozen-inventory pin and the literal C1-CTL-3 mutation
("one recorded sha256 … changed by one hex nibble", `registration.md:41-48`); D4 is the same
literal mutation applied to a recorded non-inventory line (see F5).

C2 inputs (golden frozen rows, emphasis on so rows start 3/3; matrix from `distinct_c2.py`):

| input | minimal | whole-text citation | no host boundary |
|---|---|---|---|
| D5 entry cites only `autostart.conf:10` and `bindings.conf:20` (prefixes of frozen hosts) | reject | reject | **ADMIT** |
| D6 entry cites `autostart.conf:1-6` + `bindings.conf:2` | ADMIT (2) | ADMIT (2) | ADMIT (2) |
| D7 `source:` names S375,S376 only; S377 only in the body | reject | **ADMIT** | reject |

D5 and D7 are the discriminators: a substring host check admits `:10`/`:20` decoys that are not in
the frozen set, and a whole-text citation check admits an entry whose `source:` line names two of
three rows. D6 is an ambiguity, not a defect — see F8.

## 4. Findings against the frozen record (operability-critical)

These are independent of the prototype; each was measured on the pins/entry/rows as they exist.

**F1 — S376's frozen quote is not byte-verbatim in its pin; PRED-C2-r54 is unreachable as
literally written.** Pin line 60 (`uwsm-0.27.1-uwsm-app.1.scd:60`) is
`*uwsm-app* client sends arguments to uwsm's app daemon via a pipe. Upon`; the frozen quote is
`uwsm-app client sends arguments to uwsm's app daemon via a pipe.` (no asterisks). Measured:
raw absent, newline-normalized absent, present only after stripping scdoc emphasis
(`*x*`→`x`). The frozen table cannot be edited after scoring, so the only pre-data options are
(a) declare scdoc emphasis stripping as part of the counter's verbatim rule and say so in the
report, or (b) re-register the row quote with the asterisks. A counter must not silently choose.

**F2 — S375's locator is off by one line; do not verify locators.** Frozen location
`uwsm-0.27.1-README.md:117-118`; the quote completes on line 119 (`implementation is used)`).
Lines 117–119 joined and stripped equal the frozen quote; 117–118 does not. The predicate requires
the quote to occur in the pin, not the locator to be exact, so the counter must search the pin —
a counter that also checks the locator span would report `rows=2/3` on a correct record.
C2 therefore needs the same newline-run normalization as C1 (`registration.md:49-53` makes it
explicit for C1 only): a raw `bytes` search finds S375 nowhere, `117–119` found by collapsing the
newline runs finds it. Note this is separate from F1's emphasis knob: newline collapse is always
on in the prototype; S375 and S377 pass under it on the frozen rows (`rows=2` verbatim), S376
additionally needs emphasis stripping (`rows=3`).

**F3 — C1 clause (c) is four pins, but the proposition table names only two distinct files.**
`registration.md:9-18` inventories `ConfigActions.cpp`, `ConfigActions.hpp`,
`KeybindManager.cpp`, `DispatcherTranslator.cpp`; P19–P22 name only the first and last. The
`pins=4/4` numerator must be defined over the inventory (four files, once each), not over four row
hashes. A row-loop implementation prints `pins=4/4` from two files and admits D3 (`hpp` tamper).
The frozen C1-CTL-3 mutation does not say which line is mutated, so D3 is a legal instantiation.

**F4 — `SHA256SUMS` records absolute lane paths.** `.ufo/waves/round-52/fetch/SHA256SUMS` lines are
`<sha256>  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-52/fetch/<file>`. A counter
that resolves recorded paths literally cannot verify anything inside a control fixture (different
root by construction). Key by basename; that is also what makes CTL-3 instantiable.

**F5 — CTL-3's wording ("one recorded sha256") includes `README.txt`, which is not in the four-pin
inventory.** Clause (c) names four pins; the control says one recorded hash. A four-pin-only counter
admits a nibble on the `README.txt` line (D4). Six extra lines (every recorded line whose file
exists must hash) close it; harmless to every other leg.

**F6 — the staged C2 record cannot currently satisfy a literal counter** (measured on the
working-tree files; at `350d30e4` the entry and rows are still uncommitted and `git status` shows
`M corpus/SOURCES.md`, `M corpus/README.md`, `?? corpus/knowledge/uwsm-app-environment-r54.md`):

```
$ python3 -I snapshot_c2.py     # copies the four record surfaces + pins into a scratch repo
strict (frozen strings, verbatim)          admitted=0 rows=0
+scdoc emphasis                            admitted=0 rows=1
+suffix host paths                         admitted=0 rows=0
+emphasis +suffix                          admitted=0 rows=1
+emphasis +suffix +whole-text cite         admitted=1 rows=1
```

Attribution of the four misses:
- `corpus/SOURCES.md:325` (S375) teaches `Difference before and after preparation is exported into
  systemd user manager` — a paraphrase; the frozen 24-word quote starts `Difference between
  environment state before …` and is absent even newline-normalized. This is why `rows=1` (not 2)
  with emphasis: newline collapse is always on and the frozen S375 quote passes under it, but the
  staged cell is a different string.
- `corpus/SOURCES.md:327` (S377) teaches `unit name includes desktop and command substrings and
  random hexadecimal text` — prose, not the frozen `unit_name = f"app-…"` line (which is present
  verbatim at `uwsm-0.27.1-main.py:3714`).
- `corpus/SOURCES.md:326` (S376) carries the markup-stripped form, so it needs F1's normalization.
- `corpus/knowledge/uwsm-app-environment-r54.md:1` cites `S375–S377` with an en dash. `S376` is not
  a token; clause (a) says the trio cites rows S375, S376 **and** S377. Expand the range or list
  all three.
- `corpus/knowledge/uwsm-app-environment-r54.md:17` cites `bindings.conf:2` and
  `omarchy-toggle-idle:9`; `:19` cites `autostart.conf:1-5`. None of these is a frozen host string
  (`~/.config/hypr/bindings.conf:2`, `~/.local/share/omarchy/bin/omarchy-toggle-idle:9`,
  `~/.local/share/omarchy/default/hypr/autostart.conf:<n>`). Clause (c) is membership in the frozen
  set; suffix matching is a weakening, not an interpretation.

**F7 — the frozen host set misnumbers `autostart.conf`.** `registration.md:71-77` lists `:1`–`:6` as
six `uwsm-app` launches including `omarchy-hyprland-monitor-watch`; entry line 19 says `:1-5` are
the `uwsm-app` lines, `:6` launches the polkit agent and the watcher is at `:9`. Measured on the
lane's committed copies (static pins, no host read): seven independently fetched copies of the
omarchy default file share sha256
`acb6a66862033edd26ad98e453cc8d894388c6a2e374b491bc4061d55f7a0441`
(`.ufo/waves/round-18/fetch/{NoteTheme/omarchy-autostart-v3.8.4.conf,ReopenS093/autostart.conf,ReviewThemeUpstream/omarchy-autostart-v3.8.4.conf,SrcOmarchyBackground/default_hypr_autostart.conf,SrcOmarchyThemeHooks/default_hypr_autostart.conf}`,
`.ufo/waves/round-39/w1/{ExecOptionsRealTree/host-tree,SctHostTree/real-tree}/.local/share/omarchy/default/hypr/autostart.conf`),
and in them line 6 is
`exec-once = /usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1` while line 9 is
`exec-once = uwsm-app -- omarchy-hyprland-monitor-watch`. So the frozen `:6` mapping is wrong and
entry line 19 is right. This does not sink C2: clause (c) needs two joins and `:1`, `:2` are
genuine `uwsm-app` lines, so `:1` + `bindings.conf:2` still admits. But no reviewer should cite the
frozen `:6` row as evidence, and no counter should require it.

Two further host-set facts, measured the same way: `.config/hypr/bindings.conf:2` is
`bindd = SUPER, RETURN, Terminal, exec, uwsm-app -- xdg-terminal-exec --dir="$(omarchy-cmd-terminal-cwd)"`
in both committed round-39 copies (sha256 `e574a1ed08535e31deeafe2a26432c6862bb101e8c45d5a6b3f997d7dc810581`),
so that join is byte-backed; and `git ls-files | grep -i toggle-idle` returns **nothing** — the
frozen `omarchy-toggle-idle:9` join has no committed bytes in the lane, so an entry citing it cites
something no in-lane check (and no permitted host read) can substantiate. R54Seat07 reported the
same gap independently.

**F8 — no-host-boundary matching and range cites are two different looseness bugs.** With
`re.escape(host) + r"(?!\d)"` an entry that cites only `autostart.conf:10`/`bindings.conf:20`
scores 1 join under naive substring matching (D5) and 0 under the boundary rule. With `:1-6`,
the boundary rule counts `autostart.conf:1` (next char `-`), so a range counts once. If the frozen
set is read as exact line tokens, the boundary must be `(?![\d-])`; pick one and state it.

## 4b. Cross-check with an independent seat (their measurements, not mine)

R54Seat07 (scribe, same wave) reported on `.ufo/waves/round-54/w1/R54Seat07.md` before reading this
report and reproduces the same three record defects independently: the S375/S377 teaches cells are
not the frozen quotes, S376 needs the `*uwsm-app*` emphasis handling, and the entry's provenance
line and host citations carry the en-dash / short-name forms. The remaining two observations are
theirs; both are recorded for Main, and the second I re-measured myself:

- The entry was rewritten at 14:12:23 (`sha256 2d9fce29…`, 22 lines) and its `:9` still says
  "README lines 117–118"; the bytes I read at 14:22 match the F2 locator claim above.
- They find `omarchy-toggle-idle:9` has no committed bytes or hash anywhere in the lane (only
  prose in `.ufo/waves/round-35/SentProvenance.md`). My own `git ls-files | grep -i toggle-idle`
  returns nothing, so I confirm the gap independently (F7).

Their first read of my `rows=1/3` was a missing-whitespace-collapse artifact; on exchange we
reconciled the two counts as different artifacts, and both stand. Their counts compare the frozen
quote to the pin; mine read the staged teaches cell, which is a different sentence (F6). The two
knobs are independent and cumulative: newline-run collapse (always on here; S375 and S377 pass on
the frozen rows), then scdoc emphasis (S376) → `rows=3`.

## 5. Preserved contract

- Printed lines, denominators, leg names, `verdict=` tokens and exit codes are exactly the frozen
  sentences (`claims-frozen.md:19-23`, `:55-57`), including `controls=6/6` only after six red runs.
- C1 scores only the errata entry and the round-52 fetch objects; C2 scores only the round-54 entry,
  its README row, rows S375–S377 and the round-54 pins — the causal-separability surfaces
  (`claims-frozen.md:77-84`).
- No control was weakened to make a leg pass; D3/D4/D5/D7 show the two shortcuts that would do so.
- `--work` is honoured by both prototypes (no `/tmp` literal); fixtures are removed after each run.

## 6. Tradeoffs

- **Strict table equality is a blunt numerator.** Because any row drift fails
  `propositions=4/4`, five of six C1 controls print `propositions=3` and the `quotes`/`anchors`
  numerators never move for those controls. That is what the freeze mandates, but per-control
  detail should be printed (as both prototypes do) so a failure is attributable.
- **scdoc emphasis normalization is a semantic choice inside a byte predicate.** It is the only way
  S376 passes; the alternative (re-registration with asterisks) is honest but costs the round a
  versioned freeze file. The counter must document which it does.
- **Per-line hash verification exceeds clause (c) by five lines.** It closes F5; nothing else is
  affected.
- **Suffix host matching would raise `admitted` on the staged entry** but weakens clause (c) to
  "a path ending in the frozen one". Not recommended; fix the entry instead.

## Commands and outputs

- `read /home/vgpnk/.omp/agent/RULES.md` — install policy; **no tool installed or updated**.
- `read .ufo/waves/round-54/claims-frozen.md`, `registration.md` — the two predicates, impact
  table, anchor side-claims, six-plus-six controls, row shape, host set, counter form.
- `git -C mado-shokunin rev-parse HEAD` → `350d30e4ec5531f65ce99a57efeb8216f38e678a` at read time
  (base remains `e25149fe…`); `git status --porcelain` → `M corpus/README.md`, `M corpus/SOURCES.md`,
  `?? corpus/knowledge/uwsm-app-environment-r54.md`, `?? corpus/lessons/round-54.md` — read-only.
- `sed -n '1552,1560p;1574,1578p' .ufo/waves/round-52/fetch/Hyprland-ConfigActions.cpp` and
  `sed -n '570,576p;617,624p' …Hyprland-legacy-DispatcherTranslator.cpp` — anchors 1554–1558,
  1576, 619–622, 573–574 hold; blank lines 1555 and 620 sit inside P19/P21 quotes.
- `for f in $(git ls-files | grep -i autostart); do git cat-file -p HEAD:"$f" | sha256sum; done`
  → seven copies of the omarchy default file at `acb6a668…`; `cat -n` of one shows `:6` polkit,
  `:9` `uwsm-app -- omarchy-hyprland-monitor-watch`; same for `.config/hypr/bindings.conf:2`
  (`e574a1ed…`, `bindd = SUPER, RETURN, … uwsm-app -- xdg-terminal-exec …`);
  `git ls-files | grep -i toggle-idle` → empty.
- `grep -n 'Difference between environment state' .ufo/waves/round-54/fetch/uwsm-0.27.1-README.md`
  → 117; `… :119p` → `  implementation is used)`; `grep -n 'client sends arguments'` → 60;
  `grep -n 'unit_name = f"app-{desktop_unit_substring}'` → 3714.
- `sha256sum .ufo/waves/round-52/fetch/*` — four recorded hashes match bytes; `README.txt`
  `c53296ae…` also matches its recorded line.
- `python3 -I proto_c1.py …` (139 lines) → `propositions=4/4 quotes=4/4 anchors=4/4 pins=4/4`,
  exit 0.
- `python3 -I proto_c1_full.py … --work work` → full line, `controls=6/6`, exit 0; per-control legs
  above; do-nothing variant 0/6.
- `python3 -I distinct_c1.py` → D1–D4 matrix above.
- `python3 -I proto_c2.py … --selftest [--emphasis]` → `rows=2` vs `rows=3`.
- `python3 -I distinct_c2.py` → D5–D7 matrix above.
- `python3 -I snapshot_c2.py` → staged-record matrix above.

Scratch: `/fast/scratch/hyaku/mado-r54/R54Seat27` (prototypes, matrices, `work*` fixture dirs;
fixtures removed before yield).

## Report trailer

Lane-relative report: `.ufo/waves/round-54/w1/R54Seat27.md`. No tracked lane edits, no writes
outside this report and my scratch, no git/jj mutation, no commits/pushes, no subagents, no
campaign tools, no host/config/service/compositor reads, no producer execution, no package
queries, no tool install or update.
