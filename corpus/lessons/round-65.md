# mado round 65 — lesson

author: mado L1 lane (integrated from wave w1 seat reports; the non-author closure verifies this round)
date: 2026-11-03
frozen contract: `.ufo/waves/round-65/claims-declaration-r65.md` (commit `cb63ab13`)
base: `524fa1f90b1f2de44b3019bacf833d54e0af13a0`

## Context

The omarchy Linux host returned in run 15 after rounds 57-64 ran on a Windows host. Every
omarchy-era freshness and operability rubric had been dormant since r57/r58, and the
2026-10-31 surface-state register still said the omarchy surfaces were absent. This round
re-observed the host read-only and built the two instruments the standing landing check
needed.

## Mistakes

- **M65-1 — stale host-state register carried as current.** Class: record currency.
  Evidence: `PROVINCE.md` (before round 65) — `grep -c 'absent (2026-10-31)' PROVINCE.md` → 7; the
  live host on 2026-11-03 had every omarchy surface present (receipt
  `.ufo/waves/round-65/receipts/before-state-r65.txt`, register probes
  `.ufo/waves/round-65/receipts/before-register-probes-r65.txt`). Captured-by: none — no
  criterion compared a register's observation date with the live host, so the 2026-10-31
  block stood unre-derived for eight rounds. Fix: the 2026-11-03 register block re-derived
  row by row; the frozen counter `quality/counters/c1-r65-register.py` checks it.
  Fix can fail: at base the counter prints `TARGET_MISSED` rc=1
  (`control-c1-c2-base-r65.txt`); the seat's negative fixture with the windows row deleted
  prints `groups=7/8 TARGET_MISSED` rc=1 (`R65ExecC1Counter/evidence-transcript.txt`, case c).

- **M65-2 — a shape-valid register accepts forged state cells.** Class: counter design
  (a gate that checks shape and receipt existence but not row truth). Evidence:
  `R65RevRegister/a3-forge.sh` — a fixture block whose eight state cells are all false but
  whose receipt pointer resolves to a real gate receipt → `MADO_R65_REGISTER: rows=8
  groups=8/8 receipts=1 resolved=1 gate=ok verdict=TARGET_MET` rc=0. Captured-by: none
  (the predicate defines the register as the observed state; git objects at `--rev` cannot
  prove row truth). Fix: NOT applied this round. The counter stays as frozen. The row-truth
  gap is accepted with a reviewer cross-check (the reviewer's independent re-derivation of
  all eight rows reproduced, zero disagreements) and routed as a frozen-counter amendment
  for round 66: exactly-one heading (the block finder is first-match), a per-row receipt
  pointer, and the gate leg required in the live receipt
  (`gate-live-r65.txt`, not the file-plane receipt). Those clauses sit outside the frozen
  letter and change a rule after scoring, so they wait.

- **M65-3 — the drafted landing instrument was green while it was unsound.** Class: instrument
  hermeticity and vacuous green. Evidence (critic, `R65CriticInstrument/report.md`):
  B1 the citecheck leg read the worktree (an uncommitted receipt flipped the verdict); B2 the
  citecheck leg returned TARGET_MET on an empty evidence set (`files=0 citations=0`, rc=0);
  B4 ambient `GIT_DIR` redirected the nav and citecheck legs (`GIT_DIR=<empty repo>`: nav
  rc 0→1, citecheck rc 0→2 at the same rev). The draft's own selftest did not catch any of
  the three (it passed the draft at 19/19). Captured-by: none — the selftest asserted that
  each leg ran and reported an rc, not that the leg's green meant evidence. Fix applied:
  `unset GIT_*` at the top of `quality/landing-counters.sh` and `env` without `GIT_*` for
  every leg child in the driver; the citecheck leg refuses rc=0 with `citations=0`; a landing
  run refuses a dirty receipts tree. Fix can fail: the all-green selftest shim (a10/a11) went
  RED the moment the citation guard landed (the stub printed no citecheck line); the stub
  was corrected to emit one, and the selftest is 19/19 rc=0 after. The guard is therefore
  observed to fire on the empty case.
  Residue, named and not fixed: critic S5 (red and crash both exit 1), mutation survivors
  I1 (citecheck leg skipped with rc forced 0 is not caught by a7), I7 (default receipts tree
  pinned to round 64 is not caught) and I9 (used-by sibling absence reads as red, not as a
  crash). Routed to round 66.

- **M65-4 — the frozen declaration named the wrong column.** Class: spec premise. Evidence:
  `claims-declaration-r65.md` says "recheck cells logged old→new (S028 2026-10-19 →
  2026-11-03)". In `corpus/SOURCES.md` the S028 and S097 `recheck` cell is the symbolic
  `on-release`; the dates sit in the `opened` column (`R65RevFrontier` defect 1, F3).
  Captured-by: none (the declaration was written before the row was re-read). Fix: the
  `opened` cells of S028 and S097 were updated to the 2026-11-03 re-open date, the recheck
  cells left at `on-release`, and the change logged here. The census stays exit 0 at both
  ends (`census-start-r65.txt`, `census-mid-r65.txt`); the F3 seat's mirror-tree proof showed
  validate `--file` on a bare copy gives false E11 and is not evidence on its own.

- **M65-5 — the wave's own selftest counts differ from the recorded ones; not a defect.**
  Class: host-gated count, recorded so no later reader mistakes it for drift. Evidence:
  `quality/check-tool-ledger.py` `SELFTEST_CHECKS = 55 if os.name == "nt" else 54` and
  `quality/check-wave-done.py` `63 if os.name == "nt" else 62`. The round-64 receipts are
  from Windows (55/55, 63/63); this host is POSIX (54/54, 62/62). Captured-by: the code
  itself. No fix needed.

## Gate

S028 — Hyprland v0.56.2 release (re-opened 2026-11-03, this round)
- URL: https://github.com/hyprwm/Hyprland/releases/tag/v0.56.2
- Access date: 2026-11-03
- Located quote (2 words): "Fixes backported" — release body heading `<h2>Fixes backported</h2>`
  in `div.markdown-body[data-test-selector="body-content"]` (scout `R65ScoutSources`,
  `gate-quotes.md`).
- Upstream state: tag date 2026-08-05 (`<relative-time datetime="2026-08-05T14:14:01Z">`),
  unchanged; the backported window-rule fix is listed. Nothing recorded in the row changed.
- Recheck (old→new): `opened` 2026-10-19 → 2026-11-03; `recheck` `on-release` unchanged.

S097 — omarchy v3.8.4 matte-black theme payload (re-opened 2026-11-03, this round)
- URL: https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/themes/matte-black/colors.toml
- Access date: 2026-11-03
- Located quote (3 words): `background = "#121212"` at `themes/matte-black/colors.toml:4`
  (scout `gate-quotes.md`).
- Digests: fetched raw `colors.toml` sha256 `dbdd13a629aac86daa0f01ad03b66429d9e4b303758ea464c8bcc917a5601786`
  equals the row's recorded value; `cmp` against the host
  `~/.config/omarchy/current/theme/colors.toml` → rc=0 (the file the row's 12-byte host
  payload claim covers). `git ls-remote refs/tags/v3.8.4` agrees with the recorded tag commit.
- Recheck (old→new): `opened` 2026-10-20 → 2026-11-03; `recheck` `on-release` unchanged.

No new rows were appended this round. Staged rows: none (`R65RevFrontier` F4: the
`merge/mado/SOURCES.append.md` staged set is empty to the lane's collision guard;
`diff --cached` rc=0, 0 files).

## Frontier

- Census: start exit 0 (`census-start-r65.txt`); after the two opened-cell edits exit 0
  (`census-mid-r65.txt`); round end exit 0 (`census-end-r65.txt`).
- Sourced claim: C1 rests on S028 and S097, both opened this round (Gate above).
- Assimilation: none. The `merge/mado/` package (147 rows / 69 entries, first staged id S203)
  is reachable; the connector seat found no theme that fits C1 or C2. The closest clusters
  (idle-lock; host bar/producer state) are surface-state claims pre-dating this host's
  re-derivation, so they stay held back until a later round re-observes them.
- Considerthese: no new adoptable proposal (`R65ConnSiblings` S4; the nine files were screened
  2026-11-01 and none has changed since).

## Notes for round 66

1. Land the M65-2 amendment (exactly-one heading; per-row receipt; live gate receipt) as a
   frozen-counter change with its own declared control.
2. Close the M65-3 residue: a7 must prove each leg child actually ran, the default receipts
   tree must be pinned, and the used-by sibling absence must be distinguishable from red.
3. The windows desktop plane stays not re-derivable on this host (no PowerShell here); its
   row cites the committed absence receipt and does not claim a re-derivation.

## Landing addendum

- Historical register correction: M65-1's phrase "factually wrong" means unrefreshed
  for the returned host, not that dated Windows observations were false. Those
  observations are preserved. The register already carried re-derivation probes;
  this round exercised them on the returned host.
- Measurement-output recursion: the first measurement wrote its own output inside
  the receipts scope. The new dirty-tree refusal correctly fired (C2 landing=2),
  and citecheck detected the uncommitted output's self-citation. Fix: measurement
  outputs live outside the scanned receipts tree. This fix was demonstrated able
  to fail (first receipt red) and then green without changing code or predicate:
  `.ufo/waves/round-65/measurement-first-r65.txt` and `measurement-final-r65.txt`.
- At measured `c6b8ec301ac54c2c082ad228cbacabecbd15b48e`, C1 and C2 are both
  TARGET_MET rc=0. C2 selftest 19/19; four legs rc=0; ledger 106/106;
  citation check files=8 citations=10 resolved=10 missing=0. The gate selftest
  re-derived at 460/460 on Linux; no gate bytes changed.
- Census end is stored outside the scanned receipts scope at
  `.ufo/waves/round-65/census-end-r65.txt` (the earlier Frontier reference to
  `receipts/census-end-r65.txt` is superseded by this path). Likewise the
  mid receipt is `receipts/census-mid-r65.txt`.
- F4 clarification: no staged package rows were selected for adoption; the
  package itself does contain rows. The lesson's phrase "staged set empty"
  refers only to this round's selection, not the package's contents.
