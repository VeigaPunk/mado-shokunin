# ReviewRegistry — report (mado round 13, w1)

Full draft with registry rows, the exit-code mode table, census commands, and source opens: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-13/w1/ReviewRegistry.md`. This report carries the findings only. Read-only seat; no gate, build, test, or lint run; no shared file edited.

## Findings, by severity

**F1 — High. Closure defect: no gate registry at the registry home.**
- `grep -c '^## Gate registry' /home/vgpnk/Projects/shokunin/mado-shokunin/SKILL.md` → `0`; gate/probe rows → `0`.
- PROTOCOL.md:398 (`/home/vgpnk/Projects/shokunin/PROTOCOL.md`, last touch `7c5b34f`, tree clean): "a child lane's *registry home* is its own `SKILL.md`."
- PROTOCOL.md:420-421: "closure grades no gate conformant until its registry row exists at the lane's *registry home*."
- Fix: add a `## Gate registry` section to `SKILL.md` before `## Evidence trail & sources` (:399), with the three rows in the draft. No code change.

**F2 — High. Mutable fleet dependency and stale harness pin.**
- Regression mode consumes `tameshi-shokunin/tools/mutate-and-run.sh`, resolved from `$MADO_R7_FLEET` or `MADO_VERIFY_HARNESS` (HEAD `tools/mado-verify.sh:1508`).
- The gate prints the harness sha "provenance, not gated" (HEAD `:1520-1521`). `HARNESS_SHA_RECORDED` is `b56c6e57…` (HEAD `:1295`) and is never compared.
- Harness history (`git log -- tools/mutate-and-run.sh`, tameshi HEAD `8742f5d`):
  - `4494715` (2026-10-14 15:17 −0300) → `b56c6e57…` (recorded pin);
  - `9f1d3c3` (16:06) → `cf41efaa…`;
  - `606716f` (18:28) → `75ed934d…` (current HEAD and working tree).
- `corpus/knowledge/gate-standing-use.md` §5 item 5 says "sha `cf41efaa…242c75` today, unchanged since the round-8 freeze." A later harness commit (`606716f`) superseded that point-in-time claim. The note was not re-measured.
- Fix: the regression row names the harness dependency and its current sha; each regression line is read against that sha. PROTOCOL.md:391-392 is quoted, not invented: "A gate whose verdict depends on a mutable fleet artifact also ships a run over a committed input snapshot with its committed expected verdict." Whether that binds the regression row is the lane's call.

**F3 — Medium. A plain verdict does not name its gate revision.**
- `VERSION_STR` (HEAD `:77`) is `mado-verify.sh v1 (mado-shokunin round 5 / M5-2)`, with no sha.
- The revision appears only in snapshot receipts (`# gate-sha256:`) and the `REGRESSION_TOOL` line.
- PROTOCOL.md:393: "A verdict names the revision it was measured against."
- Fix: the registry row points to the snapshot receipt as the revision-bearing route. Do not change `VERSION_STR`: standing-use §5 item 7 says it is load-bearing for the pin.

**F4 — Medium. Exit 2 means four different things across modes.**
- verify: usage error only → could-not-evaluate.
- `--selftest`: failing suite (`MADO_SELFTEST: FAILED`, HEAD `:1214-1217`) → could-not-evaluate, not failed. A red self-test is not `1`.
- `--regression`: SETUP or usage → could-not-evaluate.
- `--snapshot-diff`: SETUP or usage → could-not-evaluate (`:2062-2063`).
- Fix: one registry row per entry mode, with the per-mode map in the draft.

**F5 — Low. Verify exit 1 covers UNKNOWN as well as FAIL.**
- Header `:12-13`: "1 = DIVERGED (a check FAILed, or a required check was UNVERIFIABLE)".
- The fleet fixes `1` as failed, so the map is conformant. An environment-blocked run still reads as failed.
- Fix: the verify row carries a note that the counts line separates FAIL from UNKNOWN.

**F6 — Medium. Stale protocol anchors in lane docs.**
- Lane docs cite PROTOCOL.md `:328-358`, `:360-408`, and `:382-385`.
- At the current fleet tree: §Evidence is `:343-373`, §Gate standard `:375-424`, Registry bullet `:398-406`.
- Fix: the registry section cites PROTOCOL.md by heading.

**F7 — Info. Pin coupling with the in-flight census edit.**
- `PIN_MADO` (HEAD `:1293`) hashes the gate with the R7 and R8 marker blocks excised (standing-use §5 item 6).
- The in-flight census change in `verify()` (HEAD `:2168`) lies outside those blocks, so it moves the pin. `--regression` will read SETUP until re-cut (standing-use §5 item 2).
- The row says the pinned-value path is the whole file, minus the excised blocks.

## Residual risk

- The exit table is static, read from HEAD `ea798ad0`. The working copy is changing under GateImplement (sha `3fb2a695…` at read time). Re-check the table after that lands.
- Whether `--regression` PASSes against harness `75ed934d…` is unknown; it was not run.
- Python-helper exits `3/4/5` (in heredocs) were not traced to the script exit. Any path that reaches it would be a sixth code outside the map.

## Verification gaps (for L1 to run once)

- `grep -c '^## Gate registry' SKILL.md` must read `1` after the draft lands, and the three rows must match the mode table.
- `bash tools/mado-verify.sh --selftest` (lane root), and `--regression` only if the harness sha is recorded with the result.
- Re-grep the symbols `EXPECT`, `LOCAL`, `verify()`, `PIN_MADO` in the landed tree; line numbers will move.

## Tooling record

No tools installed or updated. Nothing to record under the operator directive.
