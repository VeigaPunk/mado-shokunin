# mado round 96 — claims declaration (DRAFT until the L1 freeze commit)

Lane `mado`, round 96, hyaku run 15. Base revision `9f029f46f01f6cd3a1d29ac39bb498a1d0c3d` (branch `master`,
the lane's tip at round start; `jj-lane.sh state` prints `ahead=0 behind=0`). Axes owned: coverage + operability
(desktop and compositor craft). Two claims, distinct axes, causally separable.

This file is the declaration **as the wave reads it**. The `## Freeze` block at the end pins every input by sha256
and lists the findings folded in before the freeze; the predicate sentences below do not change after the freeze.

**Axis selection.** Every owned axis sits at 10 in `SCORECARD.md` (rounds 87–95), so the lowest-axis duty is a tie;
the stagnation nudge is **not claimed** (capabilities entered at rounds 88–95). C1 moves coverage on a surface the
coverage map does not hold; C2 moves operability on the last gate-compatible tool without a kill-set.

---

## C1 — coverage (new surface): the TEXT MIME database's magic step

**Surface.** GLib 2.90.1's `g_content_type_guess` answers from the text database mode when no reachable
`mime.cache` loads: `xdgmime.c` reads `DIR/mime/magic` (with `globs`/`globs2`, `aliases`, `subclasses`, `icons`)
instead of the cache, and the magic step is `xdgmimemagic.c`'s parser+matcher over the `MIME-Magic\0\n` file
format. Round 94 modelled the **name** step in both modes; round 95 modelled the magic step in **cache** mode and
refused text mode (`tools/mado-mimesniff.py` exits 3 UNSUPPORTED). The text magic database is therefore the one
named frontier of the r95 entry that stays open, and at base **no lane tool reads it**.

**Candidate.** `tools/mado-mimetext.py` (frozen candidate bytes at the freeze) — read-only; given `FILE...`, an
optional `--name`, and the XDG roots (`--data-home`, `--data-dirs`, `--home`, and their `-unset` forms as in
`tools/mado-mimesniff.py`), prints what `g_content_type_guess(name-or-NULL, data, len, &uncertain)` returns: the
type and the uncertain flag, one `MADO_MIMETEXT:` line per input, plus `MADO_MIMETEXT_DIRS: mode=text|none …`.
It loads `tools/mado-mimeglob.py` (round 94, unchanged, pinned by sha) from its own directory for the text name
step; its `--selftest` exercises only the magic-text step and does not import that sibling.

**Rules modelled** (each with an S-row or a frozen oracle-labelled case): the 12-byte `MIME-Magic\0\n` gate
(`_xdg_mime_magic_read_from_file`, `xdgmimemagic.c:801-819`); `[priority:type]` sections
(`:230-281`); matchlet lines `indent>offset=<len16 BE><value>` with optional `&mask`, `~word_size` (0|1|2|4;
2/4 values AND masks are LE byte-swapped at parse; `value_length % word_size != 0` → ERROR only for word > 1;
`~0` is accepted and compared as word size 1, `:440-443`+`:476-478`) and `+range` (`:301-514`); parse errors drop the
whole section (`:283-300`, `:749-801`), and for the `value_length % word_size != 0` error the newline is already consumed
(`:464`), so the error path eats the *next* line too — normally the next section's header (R96MProbeC1 D1, measured); matchlets kept in file order and matched with
child-indent nesting (`:557-588`: a held matchlet recurses only when the next matchlet sits at **exactly indent+1**;
a jump skips the subtree, and a child holds when any one child at that level holds); match list ordered by priority descending, ties in file order, first match wins
(`:596-629`, `:652-700`); the data compare's bounds rule `i + value_length > len` → FALSE, range loop from offset
to offset+range_length-1 (`:515-556`); the EOF corners: a final matchlet line without its newline is discarded while the
section survives, a value/mask cut short by EOF is the EOF state (earlier matchlets stay live), and an over-declared
length swallows the rest of the file (R96MProbeC1 D3); the fallback (`xdgmimeint.c:176-190`, round 95) and the guess combination
with the name types (`gcontenttype-fdo.c`, round 95); the UNKNOWN test is **pointer identity** (`:591`, `:628`,
`:655`), so a magic section typed `application/octet-stream` is a real match (uncertain 0, no `looks_like_text`, no
desktop rewrite); the fallback's single-byte binary set is `{00-07,0b,0e-1f}` (`08` and `0c` are text, `0b` binary),
and an empty `XDG_DATA_DIRS` element contributes no dir (`xdgmime.c:246-250`). Text mode has no `priority > 0` gate (unlike the cache
reader), so a priority-0 section is a live match. The spec's magic-deleteall marker `>0=__NOMAGIC__`
(`ar01s02.html:445-446`) has no implementation in GLib 2.90.1 and is matched as a literal value — a named
departure the entry records. The `mime_types` elimination loop is **not** in the surface
(`xdgmime_get_mime_type_for_data` passes `NULL, 0`, `xdgmime.c:535`).

**Predicate PRED-C1-r96-v1** (the same sentence here, in the counter's docstring and in the receipt label):
> `TARGET_MET` iff, at `--rev`, `tools/mado-mimetext.py` is the frozen candidate (`tool_sha256 ==
> --expect-tool-sha256`, printed `tool_pin=ok`) and, run under an empty `PATH` through the audit launcher with the
> structural allowlist (no process, socket, network or non-libc dynamic import), it answers (i) every frozen case
> exactly (`correct == cases`), with the per-class census equal to the declared `CLASSES` — `header sect value mask word range indent
> order drop multi glob alias fallback zerosize mode desktop` (16 classes, ≥8 cases each) — and `classes == 16/16`; (ii) every fresh seeded input exactly (`fresh == fresh_total`, ≥120 inputs);
> (iii) every host file over the host's own text database exactly (`host == host_total`, ≥1500 paths, the
> round-95 committed list): the counter copies the eight `/usr/share/mime` text files named by the frozen
> `--host-db` manifest to a scratch root, verifies every per-file sha256 and `mime_cache_in_copy == 0`, prints
> `host_db=ok files=8`, and no `mime.cache` is reachable in any dir it scores; (iv) every frozen mutant is killed and every class kills at least one mutant
> (`killed == mutants`, `class_kills == 16/16`); (v) the controls stay behind: the do-nothing instrument (the
> round-95 tool, which refuses text mode) `0`, the fallback-only naive model `< cases`, the memoriser `0` on
> fresh, and a library-asking forgery rejected by the structural conjunct/audit (`audit_denials > 0`); and
> (vi) the candidate's `--selftest` is green (`checks=N failed=0`). rc 0 TARGET_MET, 1 TARGET_MISSED,
> 2 SETUP_ERROR.

**Counting command** (replayed verbatim by the L1 before the receipt lands; every argument named):

```sh
python3 -I quality/counters/c1-r96-magictext.py --repo . \
  --rev <C1-measured-rev> --base-rev 9f029f46f01f6cd3a1d29ac39bb548498a1d0c3d \
  --cases .ufo/waves/round-96/controls/magictext-cases-r96-frozen.json --expect-cases-sha256 4b3645ae83f6bb1822ebdacd4e42c2dc0fdd152bdca8fc4ff558985052f1d565 \
  --mutants .ufo/waves/round-96/controls/magictext-mutants-r96-frozen.json --expect-mutants-sha256 f8d461e8bd4d4d6a6f813bf63fc547e74cdf6c5f7a386c536d62633cb18b806a \
  --oracle-src .ufo/waves/round-95/controls/mimesniff-oracle-r95.c --expect-oracle-sha256 99df35f8b3fd7005f30789f8866984a1bbceaff8dc6c1d326f0132eb7b4d124a \
  --fresh-gen .ufo/waves/round-96/controls/magictext-fresh-r96.py --expect-fresh-gen-sha256 32d38edfb2cff57de3d89297ffaf1bd781d730b7be502fbfa62efa38de0815da \
  --host-list .ufo/waves/round-95/controls/mimesniff-host-files-r95.txt --expect-host-list-sha256 9d5947a70d112796f39c3e309c5a25e5ff333b5ebeb51867ebe748af1135ba87 \
  --host-db .ufo/waves/round-96/controls/host-text-db-r96.json --expect-host-db-sha256 9c411d2af41ac283fb7d229152f0b7b28b7854eabd057135a225762389d1ddd7 \
  --expect-tool-sha256 d5f174fc33d0b1f1847897a8e63724c7112137c1bf58a89508d1c1c13b857cbd --expect-mimeglob-sha256 65f80a6cb1551bb722ae7608df04fb17deba1b5cd05bef6f7fdd79bed76e2453 \
  --forgery .ufo/waves/round-96/controls/forgery-ctypes-r96.py --expect-forgery-sha256 06800cd141a18548c63701a44f9cab70e2c90f0f316fb6f24d0c06fca079fd97 \
  --scratch-root <SCRATCH>
```

**Before → after.** At base `git cat-file -e <base>:tools/mado-mimetext.py` is absent and the r95 tool refuses
text mode (`MADO_MIMESNIFF: UNSUPPORTED text mode`, 0 scored inputs): **0/0 → cases/0**. The measured after is
the frozen case total with every leg exact.

**Cheap no-work controls (committed before the freeze):**
- do-nothing: `tools/mado-mimesniff.py` at base over the frozen cases **restricted to `db_mode == "text"`**
  (the only population where it must refuse) → 0 correct; the counter prints both counts.
- naive: a fallback-only model (the 128-byte binary/text rule, no magic parse) → strictly fewer than the total.
- memoriser: a model that returns the frozen case labels by input hash → 0 on the fresh leg.
- forgery: a wrapper that asks the installed library/`file(1)` → rejected by the structural conjunct/audit.

**Named limits (declared with the claim).** Text mode only (a loadable `mime.cache` in any reachable dir is
cache mode → exit 3, round 95 owns that answer); `for_data`'s input only (the `mime_types` elimination loop of
`xdg_mime_get_mime_type_for_file` is outside, as its caller passes `NULL, 0`); `max_extent`/buffer truncation is
outside (the caller passes the bytes); labels come from the installed glib2 2.90.1-1 and shared-mime-info
2.5.1-2 (a distro patch would be scored as upstream); the recursion depth refusal (>4096) is declared, not
measured against a stack.

---

## C2 — operability: the last gate-compatible tool becomes guardable and guarded

**Surface.** Round 93's gate `quality/check-selftest-strength.py` (sha256
`2d6f1219fae19a85cc92f7d4103db396e1306fea74c2226bb068b335598da61b`, **unchanged**) guards a tool when a
kill-set names production mutants whose `--selftest` fails exactly the declared check labels. Routed defect 3
(round-95 spot-check) names three unguarded tools; two are structurally outside this gate — `tools/mado-mako.py`
prints its result line to **stderr** (`mado-mako.py:802`) and `tools/mado-verify.sh` is a bash payload whose
result line is `460/460 assertions passed` (`run_selftest` runs `python3 -I` and requires `failed=0`) — and
`tools/mado-mimesniff.py` cannot be copied alone (it imports `mado-mimeglob.py` from its own directory). The
remaining tool is `quality/check-receipt-presence.py` (`checks=6 failed=0`, stdout), and it has **no kill-set**.
It is also not guardable as it stands: its three FAIL lines carry `rc=`/`absent=`/`out=` detail after the check
name (`:152,:157,:196`), so the gate's remainder would be a detail string, not a check label, and its two arms per
case share one name ("OK" twice, `checks=6` over three names).

**Change (declared).** Two structural changes to `quality/check-receipt-presence.py`, both measured against the
gate's own code (`non_selftest_prefix` cuts at the first literal `def selftest(`, `check-selftest-strength.py:73,367`):
(1) the `def selftest()` block moves to the END of the file (after `main()`), because today it sits at line 122 of
327 and leaves only lines 1-121 mutable — a main-path mutant is refused today (`SETUP_ERROR kill … find occurs 0
times in non-selftest code`, measured 2026-11-07 with `cited += 1`); (2) the selftest's OUTPUT: one line per
failing check, `RECEIPT_PRESENCE_SELFTEST: FAIL <label>` with six distinct labels (`OK-rc`, `OK-lines`,
`MISSING-rc`, `MISSING-lines`, `SETUP-rc`, `SETUP-lines`), the detail on a `RECEIPT_PRESENCE_SELFTEST_DETAIL:`
line the gate ignores, and the result line unchanged (`RECEIPT_PRESENCE_SELFTEST: checks=6 failed=N`). The tool's
main-path *behaviour* (CLI, verdict lines, exit codes) is byte-unchanged: operationally, the production text at
the measured revision equals the base production text with the selftest block removed and re-appended after
`main()` (the counter prints the relocation identity and the diff's added/removed line counts), and the round-90
C2 counter re-run at the new revision is the leg that proves the behaviour (it reads the tool at `--rev`,
`c2-r90-receipt-presence.py:156`, `check_sha256` printed).

**Predicate PRED-C2-r96-v1:**
> `TARGET_MET` iff, at `--rev`, the gate is the round-93 frozen gate (`gate_sha256 ==
> --expect-gate-sha256`) and `quality/selftest-kills/check-receipt-presence.json` is the frozen candidate
> (`kills_sha256 == --expect-kills-sha256`), with the kill-set's `tool_sha256` equal to the tool's sha256 at
> `--rev` (`tool_pin=ok`), and: (i) the gate on the unmodified tool prints `OK` and exits 0 and the tool's
> selftest is `checks=6` with the six declared labels; (ii) forcing each of the 6 checks to pass (neutralisation)
> makes the gate print `WEAK` and exit 1, `neutralised_flagged == 6/6`; (iii) every frozen hand weakening of the
> panel (≥30 green weakenings, `--panel`) makes the gate print `WEAK` and exit 1 (`hand_flagged == hand`);
> (iv) every frozen neutral edit (≥4 strength-preserving byte changes, selftest still green) leaves the gate at
> `OK`, exit 0 (`neutral_ok == neutrals`); (v) controls: the do-nothing instrument (flag a variant iff its
> selftest result line changes) flags fewer than (ii)+(iii); an always-`OK` gate flags none of (iii); an
> always-`WEAK` gate fails (i); the round's first-draft tool/kill-set (`--control-kills`, sha-pinned) flags
> strictly fewer hand weakenings (`control_hand_flagged < hand`); (vi) every one of the 6 labels has a singleton
> kill; (vii) the gate's `--selftest` exits 0; and (viii) the main-path leg: the round-90 C2 counter
> (`--r90-argv`, sha-pinned, `--rev` substituted) prints `MADO_RECEIPT_PRESENCE: TARGET_MET` at `--rev`.

**Counting command:**

```sh
python3 -I quality/counters/c2-r96-selftest-kills.py --repo . \
  --rev <C2-measured-rev> \
  --panel .ufo/waves/round-96/controls/selftest-panel-r96-frozen.json --expect-panel-sha256 4332b488309309b81eccccabaff9322c5b7a54fcedd74079b58f50926f773982 \
  --expect-gate-sha256 2d6f1219fae19a85cc92f7d4103db396e1306fea74c2226bb068b335598da61b \
  --expect-kills-sha256 305d735fd665ad87566c7983f4e9163eaf323ad1ddb7a99a907e507c8a617495 \
  --control-kills .ufo/waves/round-96/build/check-receipt-presence-draft.kills.json --expect-control-sha256 0c233a47b9d0b855ed92991079399c1e6cf32848d4016081057c569ea3aed0c7 \
  --r90-argv .ufo/waves/round-96/controls/r90-c2-argv-r96.json --expect-r90-argv-sha256 386a5a18f77bf6fa564f2a11498ef21f5c1e7ef461028a2956050d3af52ecda0 \
  --scratch-root <SCRATCH>
```

**Before → after.** At base the tool's FAIL labels are detail strings, no kill-set exists and no instrument sees
a weakened assertion: **hand weakenings flagged 0/≥30 → ≥30/≥30**, neutralisations **0/6 → 6/6**, singleton
labels **0/6 → 6/6**, with the round-90 main-path leg green at the new revision.

**Controls (committed before the freeze):** the first-draft kill-set (the wave's own candidate before closing
kills) must flag strictly fewer hand weakenings; a blanket kill-set whose mutants fail every check must flag fewer
than the frozen set; an empty kill-set flags none.

**Named limits.** The kill-set proves each committed kill is still caught by the same checks, not that the
selftest is complete; the panel's weakenings are the wave's design set (unseen weakening families are not
measured); `tools/mado-mako.py`, `tools/mado-mimesniff.py` and `tools/mado-verify.sh` stay unguarded, with the
structural reason measured and recorded (`structural_refusals`), and closing them needs a gate predicate change
carrying the round-93/94/95 counters re-anchored (QUALITY 153/155), which this round does not attempt.

## Separability

C1's counter (`c1-r96-magictext.py`) reads only `tools/mado-mimetext.py` + its frozen inputs and runs at the C2
tip (no C2 bytes are read). C2's counter (`c2-r96-selftest-kills.py`) reads only the gate, the tool and the
kill-set and runs at the C1 tip; it does not read `tools/mado-mimetext.py`. Each claim is measured at both
revisions (at-C2-tip and at-C1-tip), and each counter SETUP_ERRORs (never passes) where its own frozen inputs are
absent — the base has neither tool nor kill-set, which is the declared "before".

## Sourced claim

C1 is the round's sourced claim: its entry cites the rows opened this round for `xdgmimemagic.c` (S-numbered at
the freeze) plus held S519/S520/S505/S516/S518/S523. Every new row is opened by the L1 before the freeze with
HTTP 200, `url_effective`, sha256 and a ≤25-word located quote; the scribe's entry cites them by id.

## Frontier step (rides inside the claim cap)

- `corpus/SOURCES.md` curated: new rows for the text magic parser (GLib 2.90.1 `xdgmimemagic.c`), the text
  database load order (held `xdgmime.c` re-opened), and the shared-mime-info `MIME-Magic` format page if a 200
  locator exists (else the row is rejected with reason). Census before/after: `sources-census.sh validate --root
  /home/vgpnk/Projects/shokunin mado` (start rc 0, `mado ok`, 458 rows).
- One mistake mined into `corpus/lessons/round-96.md` `## Mistakes` with class · evidence · captured-by · fix.
- `considerthese/2026-11-07.md` (operator-authored; read-only) — at most one unimplemented proposal mined, or a
  report line saying none fits.
- Assimilation (`merge/mado/`): read-only check; `Assimilation: none` unless a staged theme lands on this plane.

## Report extras

Trend verdicts per LEARNING.md; `Stale-lane` line; tool installs (none planned); cross-domain evidence item.

## Freeze

Frozen 2026-11-07 by the L1 `MadoR96`, after the w1 seats settled. The predicate sentences above are the frozen
predicate (`PRED-C1-r96-v1`, `PRED-C2-r96-v1`); the pins below are the bytes the counters read. `<C1-measured-rev>`
and `<C2-measured-rev>` are the two landing commits (C1: `tools/mado-mimetext.py` + its counter + the frozen inputs;
C2: `quality/check-receipt-presence.py` + its kill-set + its counter); their hashes are recorded in `SCORECARD.md`
and `LOG.md`, because a commit cannot contain its own hash.

| pinned input | path | sha256 |
|---|---|---|
| C1 tool (frozen candidate) | `.ufo/waves/round-96/build/mado-mimetext.c1.py` → `tools/mado-mimetext.py` | `d5f174fc33d0b1f1847897a8e63724c7112137c1bf58a89508d1c1c13b857cbd` |
| C1 cases | `.ufo/waves/round-96/controls/magictext-cases-r96-frozen.json` (284 cases, 423 inputs, 16 classes) | `4b3645ae83f6bb1822ebdacd4e42c2dc0fdd152bdca8fc4ff558985052f1d565` |
| C1 mutants | `.ufo/waves/round-96/controls/magictext-mutants-r96-frozen.json` (84 counted + 13 not-observable with arguments + 13 equivalents, from the wave's 97-mutant set) | `448150e2be7650309d126670413ea0a2d8c11c8c257807014418cf28ac1bc440` |
| C1 fresh generator | `.ufo/waves/round-96/controls/magictext-fresh-r96.py` | `32d38edfb2cff57de3d89297ffaf1bd781d730b7be502fbfa62efa38de0815da` |
| C1 oracle (round 95, reused) | `.ufo/waves/round-95/controls/mimesniff-oracle-r95.c` | `99df35f8b3fd7005f30789f8866984a1bbceaff8dc6c1d326f0132eb7b4d124a` |
| C1 host DB manifest | `.ufo/waves/round-96/controls/host-text-db-r96.json` (8 text files, no cache) | `9c411d2af41ac283fb7d229152f0b7b28b7854eabd057135a225762389d1ddd7` |
| C1 host list (round 95) | `.ufo/waves/round-95/controls/mimesniff-host-files-r95.txt` (4911 paths) | `9d5947a70d112796f39c3e309c5a25e5ff333b5ebeb51867ebe748af1135ba87` |
| C1 forgery control | `.ufo/waves/round-96/controls/forgery-ctypes-r96.py` | `06800cd141a18548c63701a44f9cab70e2c90f0f316fb6f24d0c06fca079fd97` |
| C1 counter | `.ufo/waves/round-96/quality-counters-c1-r96-magictext.py` → `quality/counters/c1-r96-magictext.py` | `9d3e1e76f2acf8c2219dd03157496363ddf9ff1a0089cc9aa090e5d0af42a7f7` |
| C2 tool (frozen candidate) | `.ufo/waves/round-96/build/check-receipt-presence.c2.py` → `quality/check-receipt-presence.py` | `be716a63662f326a771d96dc5324e89fe07abdff6949029cabb8b7f5d15ca962` |
| C2 kill-set | `.ufo/waves/round-96/build/check-receipt-presence.kills.json` → `quality/selftest-kills/check-receipt-presence.json` | `305d735fd665ad87566c7983f4e9163eaf323ad1ddb7a99a907e507c8a617495` |
| C2 first-draft control kill-set | `.ufo/waves/round-96/build/check-receipt-presence-draft.kills.json` | `0c233a47b9d0b855ed92991079399c1e6cf32848d4016081057c569ea3aed0c7` |
| C2 panel | `.ufo/waves/round-96/controls/selftest-panel-r96-frozen.json` (31 hand + 6 neutral) | `4332b488309309b81eccccabaff9322c5b7a54fcedd74079b58f50926f773982` |
| C2 r90 leg argv | `.ufo/waves/round-96/controls/r90-c2-argv-r96.json` | `386a5a18f77bf6fa564f2a11498ef21f5c1e7ef461028a2956050d3af52ecda0` |
| C2 gate (round 93, unchanged) | `quality/check-selftest-strength.py` | `2d6f1219fae19a85cc92f7d4103db396e1306fea74c2226bb068b335598da61b` |
| C2 counter | `.ufo/waves/round-96/quality-counters-c2-r96-selftest-kills.py` → `quality/counters/c2-r96-selftest-kills.py` | `2bd9e5628993ceccf2739d0782a9cef7ff9ed5c6247336f5f3d07188eb4eb895` |

### Findings folded in before the freeze (source seat → change)

- **R96MCritic F1** host leg wired to the cache-free manifest (`--host-db`, per-file pins) instead of a cache dir;
  **F2** host-list pin completed to 64 hex; **F3** tool + mimeglob pins added to the command; **F4** word size set
  corrected to 0/1/2/4; **F5** indent rule stated as exactly `indent+1`; **F6** do-nothing control restricted to
  text-mode cases (none-mode census printed separately); **F7** the 16-class tuple written into the predicate;
  **F8** forgery pinned; **F9** the four edge fixtures added to the case set; **F10** S524/S525 line numbers fixed.
- **R96MProbeC1 D1-D6** folded into the model: the `value_length % word_size` error eats the next line; the EOF
  corners (final matchlet without newline discarded, EOF-truncated value keeps earlier matchlets, over-declared
  length swallows the file); the UNKNOWN test is pointer identity; the fallback's single-byte binary set; an empty
  `XDG_DATA_DIRS` element adds no dir.
- **R96MExecCasesC1** relabelled the five `mode` cases: refusal sentinels only where a **loadable** cache exists
  (`>= 40` bytes, version 1.1/1.2); `mode-06` is text mode and oracle-labelled.
- **R96MMutC1** anchored 97 mutants to the frozen candidate bytes (14 equivalents excluded with arguments); the
  case set was extended by the L1 with its named fixture gaps (284 cases now) and re-labelled by the oracle, which
  killed 84/97. The 13 mutants no frozen case observes are **not counted**, each with the probe fixture that kills
  it named in `not_observable_not_counted` (ten are case gaps routed to round 97; three are contract-level — one
  refusal line per file, exit 3, the DIRS mode line — measured directly but outside per-input labels).
- **R96MReviewC1 F2** memoriser keyed by case identity (mode + env + layout + inputs), so it cannot recall a fresh
  input; **F5** the host leg's table-passability is recorded as a named limit; **F9** the tool docstring's line
  citations are recorded as a defect routed to round 97 (fixing them changes the frozen tool bytes and re-anchors
  every mutant).
- **R96MExecCounterC1** counter rebuilt with `--host-db`/`--forgery`/pins, the loadable-cache rule and the case-keyed
  memoriser; its own smoke-mutant run is a control, not the frozen mutant leg.
- **R96MConnector**: the text MIME database is mado's own (revenger owns `file(1)`/libmagic; no sibling claims
  `mime/magic`); `Assimilation: none` (94 staged-id collisions, none on this plane); considerthese 2026-11-07
  proposal 3 is the round's mined proposal (the oracle-labelled case set is its sweep).
- **R96MScribeEntry**: entry, registry rows, SKILL/PROVINCE rows and the lesson drafted; three receipt corrections
  (oracle pin, S524/S525 lines, fetch provenance) applied.

### Named limits folded into the freeze

- The host leg's 4911-path list and the eight host text files are public and fixed: a precomputed table would pass
  it (R96MReviewC1 F5). The fresh leg is seeded at measurement time and its labels are written outside the audit
  allow, so it is the non-memorisable leg (F6).
- The tool docstring's three line citations are off (R96MReviewC1 F9); the entry's citations are correct. Fixing the
  docstring is routed to round 97 (it changes the frozen bytes and re-anchors the mutant set).
- `--data-home D --data-home-unset` together is accepted and the unset wins (R96MReviewC1 F10, unscored).
