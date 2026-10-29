# Gate mutation sweep r8 — mado-verify.sh, post-hardening re-cut (M8-1, round 8)

Date 2026-10-14 (training round 8, lane M8-1). Opt-in #4: the recorded
T6-1 ten-defect spec re-run against the gate **after** the round-6
hardening, at the revision live at dispatch. **Headline: killed 10 /
survived 0 / inconclusive 0 — kill-rate 100 % (10/10), control GREEN,
`MUTATE_RESTORE: OK`, target sha before = after.** Marks: **O** =
observation (command output / file:line re-quoted); **I** = inference;
**U** = unknown. Single host (bash 5.3.15, Linux 7.2.3-arch1-3,
2026-10-14), single sweep seat (tameshi's harness, read-only).

## 0. Request (service-optin-protocol shape; owner = requester = this lane)

    mode:       service, self-run — the sweep seat is tameshi's tool, used
                read-only; absorption stays with the gate's owner (this lane)
    target:     tools/mado-verify.sh @ sha256 90d50cdd…a3100bd, 75 771 B,
                1 755 newlines (last line unterminated), mtime 15:31:57 −03:00,
                HEAD 0c20a76 (round 7); tree porcelain-clean at open
    suite:      bash "$MUTANT" --selftest — prints its own count (89/89 green)
                + verdict; hermetic; no substrate read
    spec:       recorded T6-1 spec sha256 c7ee75b9…1dd8 (10 defects, clauses
                A–F); refused verbatim on the live bytes (9 non-unique
                anchors, measured §3) → re-cut sha256 85d946d7…6b01, same ten
                defects, anchors widened to the live code sites
    evidence:   this note   scratch: /tmp/w8-mado-m8-1/*

Harness pin, measured: `tameshi-shokunin/tools/mutate-and-run.sh` sha256
`cf41efaa8be5f52d92bf7806ddb3a99a031547bf12a6811b8ef45bce37242c75`, 1 341 L.

## 1. Headline (O)

Command (scratch `/tmp/w8-mado-m8-1/`; log `sweep/sweep-recut2.log`):

    bash tameshi-shokunin/tools/mutate-and-run.sh \
      --target mado-shokunin/tools/mado-verify.sh \
      --defects /tmp/w8-mado-m8-1/spec/mado-verify.defects.recut.spec \
      --suite 'bash "$MUTANT" --selftest' \
      --workdir /tmp/w8-mado-m8-1/sweep/work-recut2 --label mado-verify-r8-posthardening

- `MUTATE_DATE: 2026-10-14T19:14:28Z`; `MUTATE_TARGET: … sha256=90d50cdd…`;
  `MUTATE_SPEC: … defects=10`; rc 0.
- `CONTROL: GREEN (exit=0 duration-ms=1441 pristine-sha256=90d50cdd…)` with
  `MADO_SELFTEST: 89/89 assertions passed`.
- **`MUTATE: DONE (target=mado-verify-r8-posthardening defects=10 killed=10
  survived=0 inconclusive=0 kill-rate=100%)`**, rc 0.
- `MUTATE_RESTORE: OK (target-sha256 before=90d50cdd… after=90d50cdd…
  pristine-sha256=90d50cdd…)`; the gate file re-hashed after the runs: unchanged.

Rate path for the same spec: round-5 revision `d7edaab4` **4/10 (40 %)** →
hardened `c4c1afb7` **10/10 (100 %)** → live `90d50cdd` **10/10 (100 %)**.
No survivor ⇒ no hardening gap; the round-6 hardening target holds at the
post-round-7 revision.

## 2. Per-defect verdicts (O; failing labels verbatim from `work-recut2/evidence/<id>.out`)

| # | clause | injected defect (live line on 90d50cdd) | verdict | failing assertions (passed/failed of 89) |
|---|---|---|---|---|
| D1 | A verdict token | file-plane `CLEAN` → `OK` (`:1745`) | KILLED | `A: CLEAN verdict (missing: MADO_VERIFY: CLEAN)` (88/1) |
| D2 | B UNKNOWN arm | UNKNOWN guard dropped (`:1743`) | KILLED | `C: exit 1 got '0' want '1'` · `C: DIVERGED verdict` · `C: no fake CLEAN` · `E ×3` (83/6) |
| D3 | B status vocabulary | skipped-live row `SKIP`→`PASS` (`:1245`) | KILLED | `A (live layer not executed) (want row live.plane SKIP)` (88/1) |
| D4 | C exit map | DIVERGED `exit 1`→`0` (`:1755-1756`) | KILLED | `B/C/E/H/I: exit 1 (got '0' want '1')` (84/5) |
| D5 | C exit map | failing `--selftest` returns 1 not 2 (`:696-697`) | KILLED | `F: failing selftest exits 2 (got '1' want '2')` (88/1) |
| D6 | D census | `xdph` dropped from the local inventory (`:1179`) | KILLED | `B (want row hypr.local.inventory FAIL)` (88/1) |
| D7 | D census | include-graph `-ne`→`-lt` (`:1140-1141`) | KILLED | `H: exit 1` · `H: DIVERGED` · `H (exact census, no tolerance)` · `H: no fake CLEAN` (85/4) |
| D8 | E sha comparison | sha pin always "matches" (`:1230-1231`) | KILLED | `A: sha pin names the round-1 pin (fixture cannot match it)` (88/1) |
| D9 | E boundary proof | boundary always byte-identical (`:1394-1395`) | KILLED | `I: exit 1` · `I: DIVERGED` · `I (safety row, FAIL direction)` · `I: no fake CLEAN` (85/4) |
| R1 | F reader fallback | tomllib-unavailable arm PASS not UNKNOWN (`:1307-1308`) | KILLED | `E (reader fallback) (want row walker.config UNKNOWN)` (88/1) |

Same ten verdicts, same clauses, same kill mechanisms as the recorded
round-6 table (`gate-mutation-proof.md` §1) — the round-7 addition
(`+569/−0`, verify path byte-identical) did not lose or weaken a kill.

## 3. Why the spec was re-cut, and the re-cut itself (O)

The recorded spec is **refused verbatim on the live bytes** — measured, not
argued (`sweep/refusal-recorded.log`):

    APPLY FAIL id=D1 line=6 old-string-count=2 expected=1
    … D2 2 · D3 2 · D5 15 · D6 2 · D7 2 · D8 2 · D9 2 · R1 2 …
    MUTATE: SETUP (spec/preparation failed for 9 defect(s); no suite run)

Cause (O): round 7 embedded the spec itself in the gate (heredoc
`:784-827`), so nine of ten anchors now occur twice — once at the code
site, once inside the embedded spec text; `  return 2` occurs 15 times
(the round-7 suites added 13 more). Only D4 (`"$reason"\nexit 1`) is
count 1 on the live bytes and was kept verbatim.

The re-cut (`/tmp/w8-mado-m8-1/spec/mado-verify.defects.recut.spec`, sha256
`85d946d7905d8c92826323858721ed711752fb0db4d317ccb8c1be127ef86b01`, 3 166 B)
keeps the ten clauses and semantic edits; each anchor is widened by adjacent
live lines to uniqueness: D1 `printf '…` prefix; D2 `+ next line`; D3
`+ "  else"`; D5 `echo "fixtures kept: $T"` + line; D6 `LOCAL=` prefix;
D7 `local i` + line; D8 `sha=$(sha256sum …)` + line; D9
`after=$(boundary_hash …)` + line; R1 `elif [ "$PY_TOML" = 0 ]` + line.
Pre-flight (the harness's own helper, all ten): `APPLY OK id=… old-count=1`
— the ten mutants are single-line semantic edits at the intended sites
(diffs rendered and eyeballed; e.g. D2 drops exactly the UNKNOWN guard,
D9 swaps the comparison, not the row). This is a **derived** spec: its
mutant bytes differ from the recorded spec's for nine defects (anchor
context), so verdict equivalence is argued defect-by-defect, never by sha
identity (`spec/mado-verify.defects.spec` — the recorded spec — was
extracted from the gate's heredoc and its sha re-checked against
`c7ee75b9…1dd8` before use).

In-lane incident I0 (O, recorded): this lane's first spec write emitted the
anchors character-separated (a bug in the re-cut writer, joined twice). The
harness refused it before any suite run — `APPLY FAIL … old-string-count=0`
for all ten, `MUTATE: SETUP`, rc 2 — which is the tool's uniqueness assertion
doing its job on a malformed spec, not a gate finding. Fixed in-lane; the
runs quoted in §1–§2 used the corrected spec.

## 4. Incident I1 — the live gate moved mid-sweep (O; recorded, not smoothed)

A reproducibility re-run (same spec, same suite, `sweep/sweep-rerun.log`,
`MUTATE_DATE 19:15:38Z`) reproduced all ten verdicts KILLED on the frozen
copy but ended **`MUTATE_RESTORE: DRIFT`** → `MUTATE: SETUP (byte-identity
proof failed…)`, rc 2, so it is not a headline:

    MUTATE_RESTORE: DRIFT (target-sha256 before=90d50cdd… after=05c52e14…
      pristine-sha256 before=90d50cdd… after=90d50cdd…)

The harness's pristine copy is intact (its own before = after); the **live
file** moved while the sweep ran. Measured sequence (`sha256sum`, sample times
in UTC): `90d50cdd…` (my sweep start, 19:14:28Z; before = after through
19:14:44Z) → `05c52e14…` (19:16:14Z) → `e7834b54…` (76 227 B, 1 760 newlines,
mtime 19:16:07Z, `git status` ` M`, `git diff --stat` +12/−7) → `6ea07110…`
(2 006 newlines, mtime 19:16:42Z) → `33b2e704…` (2 007 newlines, mtime
19:17:21Z) — still moving at this note's write. A
concurrent round-8 lane is editing the gate in flight; the harness's
target-sha fence is the write-fencing evidence, and this lane touched none
of these revisions. The headline §1 is per-revision and stays tied to
`90d50cdd…`. The widened
revision needs its own re-cut **after it lands** — the gate's own
instruction (`--regression` header, REGRESSION_RECUT) and this plan's
stage (a) say the same.

## 5. Spot-checks (three, all re-run 2026-10-14)

1. **Baseline + pins.** `bash tools/mado-verify.sh --selftest` →
   `MADO_SELFTEST: 89/89 assertions passed`, rc 0 (1.3 s); gate sha
   `90d50cdd…` and harness sha `cf41efaa…` measured before and after every
   run, unchanged; `git status --porcelain` empty at open (a foreign
   `plans/round-9.plan.md` and later `plans/round-8-record-draft.md`
   appeared mid-lane — other lanes' untracked files, not this lane's writes).
2. **Harness proof lines.** Control GREEN (`89/89`) with
   `pristine-sha256=90d50cdd…`; `MUTATE_RESTORE: OK` before = after =
   `90d50cdd…`; the ten evidence files `work-recut2/evidence/{control,D1…R1}.out`
   carry the failing-case labels quoted in §2. Fixture cleanup: the ten
   `/tmp/w5-mado-m52-selftest.*` dirs named by **this** run were removed by
   exact path (prefix-guarded); 140 foreign dirs left untouched.
3. **Reproducibility re-run** (§4): the same ten KILLED verdicts again from a
   fresh workdir — with the DRIFT fence firing on the moved live file, which
   is both a reproduction and a negative control for the pin discipline.

## 6. Unknowns

- **U1** — single host/toolchain (the harness's own U5 shape).
- **U2** — the re-cut's nine widened anchors make its mutant bytes differ from
  the recorded spec's; equivalence is argued per defect from the live-site
  diff, not proven by byte identity.
- **U3** — the exit-flatten family stays a harness boundary (exit-only
  adjudication, `gate-mutation-proof.md` §3) — unchanged by this sweep.
- **U4** — the 51 `hypr-live` row sites remain outside this suite's reach;
  the round-8 plan's stage (a) widening is the vehicle, and this table must be
  re-cut after that lands (I1).
- **U5** — the gate's own `--regression` mode replays the derived `c4c1afb7`
  revision, not the live one — a separate, internal measurement; not re-run
  by this lane.
- **U6** — the two mid-lane untracked files (`plans/round-9.plan.md`,
  `plans/round-8-record-draft.md`) are other writers'; this lane did not read
  or touch them.

## 7. Recommendation

None for the gate at `90d50cdd…` — the sweep found no survivor and no
hardening gap. One open item: re-cut this spec at the landed (widened)
revision per REGRESSION_RECUT once round 8's stage (a) stops moving; the
round-6 residuals (rc-6 arm, exit-flatten family, live-plane body) stay as
recorded there.