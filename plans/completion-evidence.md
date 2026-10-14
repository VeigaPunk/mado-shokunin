# mado-shokunin — completion pack: rounds 2–11

Audit input for the parent, written by lane PACK-M during the round-11 wave
(2026-10-14). One line per round (round · axis · headline · commit hash ·
verifier names), the SHONEN status, and the debts. Nothing is re-adjudicated
here: every headline is a pointer into the round's landed record (LOG.md,
SCORECARD.md move-log, `plans/round-N-record-draft.md`, `reports/`); every
number stays in its record unless tagged [O] with its command. This lane
wrote only this file (dispatch scope; the round's LOG.md/SCORECARD.md appends
belong to this wave's record lane, not to this pack). Read-only elsewhere; no
secrets read; no external sites. Counts by `wc -l`; the repo's notes/records
end without a trailing newline, so editor views are +1 (same convention as
every prior round).

State at this write [O]: HEAD `f7bfc9f` ("probation round 10 (training r9):
see LOG"); `git status --porcelain` → ` M SKILL.md` + `?? corpus/knowledge/
closeout-r11.md` (both concurrent-lane work in flight; the closeout file
appeared during this pack's own write window). Rounds 2–10 are committed;
round 11's execution is in flight and uncommitted (its plan is pre-committed
inside `f7bfc9f`, blob `2fd871cb…`). The gate is unmoved since round 9
[O: `git show HEAD:tools/mado-verify.sh | sha256sum` → `93e43f8f…`,
`| wc -l` → 3,231 — round 10 did not touch it]. Commit hashes derived with
`git log --format='%h %H %s'` (7-char short form; full hashes in the
appendix).

Round labels [I]: commit subjects label rounds 4–10 "(training r3)" …
"(training r9)" (round N = training r(N−1)); round 11 = training r10, the
final, per `plans/round-11.plan.md:14-20`. Rounds 2–3 are committed without a
training label. The foundation round 1 (`65a2254`) and the mint `74d3b7b`
precede this table; the SHONEN closure commit `c03c249` sits between rounds 5
and 6 (an arc event, not a round row).

## One line per round

| Round | Axis | Headline | Commit | Verifiers |
|---|---|---|---|---|
| 2 | depth | Live-verification layer: `hyprctl-verification-layer.md` 280 L — 56 `getoption` + 9 non-getoption claim→live pairs, census 0 mismatch (6 ownership proofs); `keybind-rule-semantics.md` 315 L — 192/192 binds reconciled live, 24-dispatcher inventory; round-1 notes get R2-E errata ×4/2/4 (mako 50→119 B corrigendum; orphan `envs.conf`); SKILL 186→240 L (claim routing + 6 safety rules) | `e1e1bb7` | scribe re-verification (MADO-SCR re-run; SCORECARD.md:13 carries the commands); **no audit verdict recorded in-repo** (LOG.md:151-153) |
| 3 | depth + coverage | Waybar/walker semantics (455 L, 89 rows / 19 modules; RTMIN delivery caught=45); e2e config-health report (550 L; 20 claim families; 57/57 `getoption` 0 mismatch; F1–F10 = 1×S1 + 2×S2 + 7×S3); SKILL 240→396 L; no-oral-context executor test verdict "Sufficient" (MADO-R3-4); SHONEN.md regenerated to the canonical seed 2×[x]/2×[~] | `f9f58c0` | MADO-R3-4 (non-author executor lane) · scribe MADO-B4 re-run 15:38–15:47 UTC (`/tmp/mado-b4-r3b/verify.log`); audits not in-repo (LOG.md:280-282) |
| 4 (r3) | depth + calibration | Idle/lock plane (355 L); box-3 CLOSED (VER-M3 — config-health report reproduces); box-4 stays [~] (VER-M4 — §8 re-run wanted); non-author reproduction package | `3d9ba45` | VER-M3 · VER-M4 (partial; no report file in `reports/`) |
| 5 (r4) | operability + calibration | First gate `tools/mado-verify.sh` (selftest + live verdict); walker-deep note; box-4 CLOSED by VER-M4B — **PROBATION COMPLETE 4/4** | `eead56b` | VER-M4B; 32-lane wave; cross-lane verification incidents recorded (LOG.md:295) |
| 6 (r5) | operability | Gate proven to fail, then hardened: selftest 28→53; hardened gate kills 10/10 of tameshi's mutants; omarchy drift-watch + remaining-planes census | `c8f6667` | VER-M6 · AUD-M6 (no report files in `reports/`; LOG.md:296) |
| 7 (r6) | operability + coverage | `--regression` mode shipped (replays the round-6 case at the gate's own recorded revision `c4c1afb7…`; tameshi spec `c7ee75b9…`; 10/10, restore OK; selftest 53→89); theme/wallpaper plane; walker live surface | `0c20a76` | VER-M7 (no report file) · AUD-M7 (`reports/r7-aud-m7.md`) |
| 8 (r7) | operability + freshness | Post-hardening sweep vs the 10/10 expectation; drift-watch arm + snapshot-diff mode; zero config mutation held | `12c8f08` | VER-M8 (`reports/r8-ver-m8.md`) · AUD-M8 (`reports/r8-aud-m8.md`) |
| 9 (r8) | coverage + operability | Theme plane as gate arms (10 rows, T1–T9, 27 sites; pin re-cut `d2bcdb31…`→`dc7c4141…`); walker deep-r9 note; snapshot-diff first real receipt (`MADO_DIFF: CHANGED` — rows 31→41, appeared=10); walker live rows did NOT land | `de22dfd` | VER-M9 (`reports/r9-ver-m9.md`) · AUD-M9 (`reports/r9-aud-m9.md`) |
| 10 (r9) | calibration + operability | Arc synthesis `corpus/knowledge/arc-synthesis.md` (387 L; ladder 28→268 CONFIRMED cell-for-cell; landed name supersedes the plan's `ten-round-synthesis.md`); standing-use note `corpus/knowledge/gate-standing-use.md` (361 L); regression-mode cadence receipt | `f7bfc9f` | VER-M10 cell-for-cell (`reports/r10-ver-m10.md`) · AUD-M10 (`reports/r10-aud-m10.md`) |
| 11 (r10, final) | calibration + freshness | In flight at this write — the closeout: verify the round-10 handoff, settle every open item, freeze the revision, commit the arc-end record (charter (a)/(b)/(c), `plans/round-11.plan.md:175-274`); `corpus/knowledge/closeout-r11.md` untracked and in flight; no closeout content consumed by this pack | — (no round-11 commit at this write; HEAD `f7bfc9f`; round-11 plan blob `2fd871cb…` pre-committed there) | not yet landed; planned seats per `plans/round-11.plan.md:347-353`; in-flight lane scratch observed under `/tmp/w11-*` (`w11-m11-1`, `w11-mado-m11-4`, `w11-scr-m11`, `w11-ver-m11-poll`) |

## SHONEN status

`SHONEN.md` (12 L) — the probation checklist; **all four boxes `[x]`**, each
with a named non-author verifier; last touched by `c03c249` (2026-10-14
14:34:46 −03:00, "boxes 3-4 closed with named non-author verifier
attributions (VER-M3, VER-M4B) — PROBATION COMPLETE 4/4") and unchanged since
[O — `git log -- SHONEN.md`; `grep -c '^- \[x\]' SHONEN.md` → 4]:

- SKILL craft — **MADO-R3-4** (non-author executor lane; SKILL `ef4c29e3…`
  396 L frozen at the round-3 commit `f9f58c0`).
- End-to-end task — **VER-M3** (round-3 config-health report reproduced from
  the reproduction package).
- No-oral-context — **MADO-R3-4** (per-step sufficiency, verdict "Sufficient,
  end-to-end, against the version read").
- PROVINCE accuracy — **VER-M4B** (§8 re-run + full province re-verification;
  receipt `corpus/knowledge/province-accuracy-selfaudit.md`; the box line
  carries the lane-asserted caveat).

Probation bar (≥3 verified rounds, round-0 commit `74d3b7b`) satisfied by
round 5 (`eead56b`, "PROBATION COMPLETE 4/4"); rounds 6–10 proceeded as
training rounds. Round 11's plan charters the arc's end and hands over — no
promotion or retirement claim is made in-repo; promotion stays the
operator/gate decision, never self-declared (`plans/round-11.plan.md:255-274`).
Whether a fleet roster row exists is outside this repo — unknown here.

## Debts

### Open at round-10 close (round-11's charter; in flight, NOT landed at this write)

- a. **`corpus/lessons/` = 0 entries** [O: `ls -A corpus/lessons | wc -l` →
  0] — the round-1 promise, unpaid across all rounds. Round-11's charter
  names the lessons entry (or the recorded refusal, with a non-author
  spot-check) at (b): `plans/round-11.plan.md:230-244`; round-10's charter
  was `lessons/round-10.md` with a `## Gate` section (round-10 draft §1.6).
- b. **README coverage map: 8 note rows vs 21 committed notes → 13 unrowed**
  [O: `grep -c '^|' corpus/README.md` → 10 (= header + separator + 8 rows);
  `git ls-tree HEAD corpus/knowledge/ | wc -l` → 21]. Ready row texts sit in
  the drafts (round-10 draft §1.6, :246-280); round 10 read 8 rows / 19 notes
  / 11 unrowed — re-measured here, not recited.
- c. **SCORECARD rows 4–10 abbreviated** (`SCORECARD.md:16-22`; full row
  texts in the drafts, round-10 draft :258-260); the final row (frozen gate
  revision + synthesis + standing-use note) is owed.
- d. **LOG rounds 4–10 are one-liners** (`LOG.md:294-301`; the only full lane
  entry is round-7's M7-1 at `:297`); the round-11 (arc-end) entry is owed.
- e. **Draft ⟨PENDING⟩ sets unfilled** [O: `grep -c PENDING` → r7 13 · r8 19
  · r9 19 · r10 22]; r4 5 / r5 3 / r6 8 at the round-10 reading (round-10
  draft :263-265). Two prepared closure blocks were never applied (:266-271);
  closures stay appended, never edits.
- f. **`walker-deep.md` §10/§11 errata owed** (routed): file 617 L /
  `0982ba066c72575a…` unchanged since round 7 [O, worktree]; the route is
  `walker-live-surface.md` §5's ledger (round-10 draft :272-275).
- g. **Theme record-level errata route**: `theme-wallpaper-plane.md` §10
  (`:362`, append-only) — no repo-level errata block exists (round-10 draft
  :274-275).
- h. **Residual ledger at gate `93e43f8f…`** (round-10 draft §3.3, each item
  with its re-grep command): `VERSION_STR` still "round 5 / M5-2" OPEN; base
  `--help` omits the three modes OPEN; rc-6 arm of `row_from_rc` OPEN
  (mapped, no pin/test); bad `MADO_VERIFY_LIVE` usage arm unasserted;
  `--root`-no-value arm unasserted; boundary combined-hash prefix
  unasserted; **hypr-live stubs J/K/L** OPEN (0 stub sites); **walker
  live-surface rows** OPEN (`grep -c 'walker.sock'` → 0); **theme live rows
  exempted by name** (`theme.wallpaper.live`, `theme.name.display_agree`;
  plane comment `tools/mado-verify.sh:3002-3012`); **theme-clause covering
  mutant** FINDING — regression spec byte-identical `c7ee75b9…` (10
  defects), T1–T9 the only kill vehicles, the covering mutant owed by the
  sweep lane (round-6 reading rule 2).
- i. **The five live rows carried together**: theme ×2 exempted by name +
  walker ×3 not landed (`plans/round-11.plan.md:132-135`; the ledger's
  open/exempted split recorded, not smoothed).
- j. **The r9-aud citation at `SKILL.md:1314`** cites `7ad8eccdd8d213a5…`;
  the landed blob reads `866272eeda09bc08…` (166 L / 15,580 B). Registered
  append-only in the round-10 SKILL append (`SKILL.md:1500-1506` at this
  write); the `:1314` block stays unedited by design
  (`plans/round-11.plan.md:121-127`).
- k. **Round-10's own record stays a draft**: `plans/round-10-record-draft.md`
  (799 L) committed with its D1–D5 ⟨PENDING⟩ slots unfilled and the v2-append
  placeholder; its LOG entry is a one-liner (`LOG.md:301`). The round-10
  clauses that DID land: (a10) synthesis at `arc-synthesis.md` (387 L),
  (b10) `gate-standing-use.md` (361 L) [O, `wc -l` at `f7bfc9f`]; (c10) the
  record family is the unpaid remainder.
- l. **Operator channel**: `grep -ci mado ../.ufo/l0-questions.md` → 0 at
  this write (shape-only) — no question owed an answer; a mid-round filing is
  named, never answered here.

### Sibling/fleet-owned, recorded-not-absorbed

- tameshi's mutation harness `tools/mutate-and-run.sh` (`cf41efaa…242c75` as
  printed by mado's `--regression`): provenance, not gated; a needed change
  is a recommendation to that lane (`plans/round-11.plan.md:297-303`).
- The regression spec pin `c7ee75b9…1dd8` (tameshi 10-defect spec, round 7)
  — cross-lane input, owned by tameshi.
- The omarchy skill/checkout is read-only documentation surface
  (`PROVINCE.md:10-11`); drift findings are operator-facing.

### Unknown registers (stand as written)

- In-note unknowns, none re-adjudicated here: `hyprland-config-plane.md` §12
  (hypridle stop cause; grok-bot autostart [UNK]); `keybind-rule-semantics.md`
  §4.6 (opacity anomaly cause; F2 age ordering); `hyprctl-verification-layer.md`
  §10; `waybar-walker-semantics.md` §9 (11); `walker-deep.md` /
  `walker-deep-r9.md` / `walker-live-surface.md`; `theme-wallpaper-plane.md`;
  `idle-lock-plane.md`; `remaining-planes-census.md`.
- Closeout-level unknowns (`plans/round-11.plan.md:324-345`): what each
  residual's terminal disposition becomes; whether a non-author seat exists
  for the final lessons entry (the lane's own subagent does not count);
  whether historical gate revisions still run faithfully (else
  [OBS-record]); whether the harness moves mid-round; whether the operator
  files an entry; whether the gate moves during round 11; whether an
  independent verifier/auditor seats the closeout.

### Resolved by commit `f7bfc9f` [O]

- Round-10 landed: `LOG.md` +1 · `SCORECARD.md` +1 · `SKILL.md` +90/−1 ·
  `corpus/knowledge/arc-synthesis.md` (387 L) · `corpus/knowledge/
  gate-standing-use.md` (361 L) · `plans/round-10-record-draft.md` (799 L) ·
  `plans/round-11.plan.md` (352 L) · `reports/r10-aud-m10.md` (160 L) ·
  `reports/r10-ver-m10.md` (156 L).
- The landed synthesis path diverges from the plan's predicted
  `ten-round-synthesis.md` — recorded, not smoothed (round-10 draft §6(b),
  :747-752).
- The round-10 SKILL append registers the `:1314` citation correction (debt
  j) and the superseded closing frame.

## Appendix — full commit hashes (`git rev-parse`)

| Round | Commit |
|---|---|
| 2 | `e1e1bb77f9cfa7f770e061cf5f3d9eb4f4c5a4fe` |
| 3 | `f9f58c0efd5daedf7d29036478d17e5b42f26822` |
| 4 | `3d9ba4559438b4c07d0c56328e1c4b7b5c4d7e1e` |
| 5 | `eead56b20ad2b28299ae4fa623d52a99b44c743c` |
| 6 | `c8f6667f31e52b2978c7f0556c5517b6d8b58f41` |
| 7 | `0c20a76fa5ff985047c8ca2d455c75179c3dd0d1` |
| 8 | `12c8f08a35537b7d53b8e0252459dec16e550079` |
| 9 | `de22dfdedc941563cc102781d3936cef9580e74b` |
| 10 | `f7bfc9fe149bc94057323964e7cb0411f6f89e25` |
| 11 | — (in flight; no commit at this write) |

Context commits: mint `74d3b7bacab1c8eb2300b82d39eb0fcadf62db12` · round 1
`65a2254dbaaf139a3783d2438711b69d82d91f59` · SHONEN closure
`c03c2490df67adc78d4299955089e64d4cc60204`.

Sources read by this lane (all read-only): `LOG.md`, `SCORECARD.md`,
`SHONEN.md`, `MINT.md`, `PROVINCE.md`, `AGENTS.md`, `SKILL.md` (point
samples), `plans/round-2.plan.md`, `plans/round-11.plan.md`,
`plans/round-7…10-record-draft.md`, `reports/` (7 files), `corpus/README.md`,
`corpus/knowledge/` listings + `walker-deep.md` sha, `git log` / `git show` /
`git rev-parse` / `git status` in this repo, and shape-only reads of the
sibling lane scratch under `/tmp/w11-*`. Nothing under `~/.config`,
`~/.local`, or the omarchy checkout was touched; no session command run.