# mado round 96 — claims declaration (DRAFT until the L1 freeze commit)

Lane `mado`, round 96, hyaku run 15. Base revision `9f029f46f01f6cd3a1d29ac39bb498a1d0c3d` (branch `master`,
the lane's tip at round start; `jj-lane.sh state` prints `ahead=0 behind=0`). Axes owned: coverage + operability
(desktop and compositor craft). Two claims, distinct axes, causally separable.

This file is the declaration **as the wave reads it**. The freeze commit (later in the round) replaces every
`<pending-w1>` with the measured sha256 and appends a `## Freeze` block; the predicate sentences below do not
change after the freeze. Findings the wave folds in are listed in the freeze block with their source seat.

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
(`:230-281`); matchlet lines `indent>offset=<len16 BE><value>` with optional `&mask`, `~word_size` (1/2/4,
LE byte-swap at parse, `value_length % word_size != 0` → ERROR) and `+range` (`:301-514`); parse errors drop the
whole section to the next newline (`:283-300`, `:749-801`); matchlets kept in file order and matched with
child-indent nesting (`:557-588`); match list ordered by priority descending, ties in file order, first match wins
(`:596-629`, `:652-700`); the data compare's bounds rule `i + value_length > len` → FALSE, range loop from offset
to offset+range_length-1 (`:515-556`); the fallback (`xdgmimeint.c:176-190`, round 95) and the guess combination
with the name types (`gcontenttype-fdo.c`, round 95). The `mime_types` elimination loop is **not** in the surface
(`xdgmime_get_mime_type_for_data` passes `NULL, 0`, `xdgmime.c:535`).

**Predicate PRED-C1-r96-v1** (the same sentence here, in the counter's docstring and in the receipt label):
> `TARGET_MET` iff, at `--rev`, `tools/mado-mimetext.py` is the frozen candidate (`tool_sha256 ==
> --expect-tool-sha256`, printed `tool_pin=ok`) and, run under an empty `PATH` through the audit launcher with the
> structural allowlist (no process, socket, network or non-libc dynamic import), it answers (i) every frozen case
> exactly (`correct == cases`), with the per-class census equal to the declared `CLASSES` (16 classes, ≥8 cases
> each) and `classes == 16/16`; (ii) every fresh seeded input exactly (`fresh == fresh_total`, ≥120 inputs);
> (iii) every host file over the host's own text database exactly (`host == host_total`, ≥1500 paths, the
> round-95 committed list); (iv) every frozen mutant is killed and every class kills at least one mutant
> (`killed == mutants`, `class_kills == 16/16`); (v) the controls stay behind: the do-nothing instrument (the
> round-95 tool, which refuses text mode) `0`, the fallback-only naive model `< cases`, the memoriser `0` on
> fresh, and a library-asking forgery rejected by the structural conjunct/audit (`audit_denials > 0`); and
> (vi) the candidate's `--selftest` is green (`checks=N failed=0`). rc 0 TARGET_MET, 1 TARGET_MISSED,
> 2 SETUP_ERROR.

**Counting command** (replayed verbatim by the L1 before the receipt lands; every argument named):

```sh
python3 -I quality/counters/c1-r96-magictext.py --repo . \
  --rev <C1-measured-rev> --base-rev 9f029f46f01f6cd3a1d29ac39bb498a1d0c3d \
  --cases .ufo/waves/round-96/controls/magictext-cases-r96-frozen.json --expect-cases-sha256 <pending-w1> \
  --mutants .ufo/waves/round-96/controls/magictext-mutants-r96-frozen.json --expect-mutants-sha256 <pending-w1> \
  --oracle-src .ufo/waves/round-95/controls/mimesniff-oracle-r95.c --expect-oracle-sha256 99df35f8b3fd7005f30789f8e6984a1bbceaff8dc6c1d326f0132eb7b4d124a \
  --fresh-gen .ufo/waves/round-96/controls/magictext-fresh-r96.py --expect-fresh-sha256 <pending-w1> \
  --host-list .ufo/waves/round-95/controls/mimesniff-host-files-r95.txt --expect-host-list-sha256 9d5947a7ba87 \
  --host-mime-root /usr/share/mime --scratch-root <SCRATCH>
```

**Before → after.** At base `git cat-file -e <base>:tools/mado-mimetext.py` is absent and the r95 tool refuses
text mode (`MADO_MIMESNIFF: UNSUPPORTED text mode`, 0 scored inputs): **0/0 → cases/0**. The measured after is
the frozen case total with every leg exact.

**Cheap no-work controls (committed before the freeze):**
- do-nothing: `tools/mado-mimesniff.py` at base over the frozen cases → 0 correct (refusal).
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

**Change (declared).** `quality/check-receipt-presence.py`'s *selftest output only*: one line per failing check,
`RECEIPT_PRESENCE_SELFTEST: FAIL <label>` with six distinct labels (`OK-rc`, `OK-lines`, `MISSING-rc`,
`MISSING-lines`, `SETUP-rc`, `SETUP-lines`), the detail moved to a `RECEIPT_PRESENCE_SELFTEST_DETAIL:` line the
gate ignores, and the result line unchanged (`RECEIPT_PRESENCE_SELFTEST: checks=6 failed=N`). The tool's main
path (its CLI, verdict lines, exit codes) is **byte-unchanged**, and the round-90 C2 counter re-run at the new
revision is the leg that proves it (the counter reads the tool at `--rev`, `c2-r90-receipt-presence.py:156`).

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
  --panel .ufo/waves/round-96/controls/selftest-panel-r96-frozen.json --expect-panel-sha256 <pending-w1> \
  --expect-gate-sha256 2d6f1219fae19a85cc92f7d4103db396e1306fea74c2226bb068b335598da61b \
  --expect-kills-sha256 <pending-w1> \
  --control-kills .ufo/waves/round-96/build/check-receipt-presence-draft.kills.json --expect-control-sha256 <pending-w1> \
  --r90-argv .ufo/waves/round-96/controls/r90-c2-argv-r96.json --expect-r90-argv-sha256 <pending-w1> \
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
