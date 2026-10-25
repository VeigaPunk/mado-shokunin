# ExecScratchMirror — scratch mirror + census gate for the registry append (round 40, w1)

Section 10 instrument: validate a `SOURCES.md` registry append **before** it is applied, in a
throwaway tree outside the lane, with the fleet census as the judge. Deliverable:

    .ufo/waves/round-40/w1/ExecScratchMirror/mirror-validate.sh

`bash -n` clean. Bash + coreutils + gawk (the census's own dependencies). No tool installed,
no package transaction, no compositor verb, no network.

## What it does

    mirror-validate.sh BLOCK [KNOWLEDGE ...]        # or --block/--knowledge/--lane/--census
                                                   #    /--today/--keep/--no-closure/--quiet

1. `V=$(mktemp -d)` in `$TMPDIR` (default `/tmp`); a `realpath` guard **refuses and removes** a
   scratch tree that resolves inside the lane (guard case 11 below).
2. copies `<lane>/corpus/{SOURCES.md,README.md,knowledge/,lessons/}` → `$V/corpus`
   (113 files = 56 knowledge + 55 lessons + 2 top files, measured).
3. inserts BLOCK into the `## Registry` table **immediately before the blank line that ends the
   table**, then proves the placement (`verify_insert`: contiguous, preceded by a table row,
   followed by the terminating blank line, every pre-existing Registry row before it, no table
   line after that blank line).
4. copies each `KNOWLEDGE` (repo-relative) from `<lane>/<path>` to `$V/<path>`, so a row's
   `used-by` can resolve — refusing absolute paths, `../` escapes and paths absent from the lane.
5. closure: copies the `used-by` targets of the mirror's own `mined` rows that live outside
   `corpus/` and exist in the lane (7 here: `quality/check-index.py`, `SKILL.md`,
   `tools/mado-binds.py`, `tools/mado-verify.sh`, `tools/mado-wsrules.py`,
   `.ufo/waves/round-29/registration.md`, `.ufo/waves/round-30/registration.md`).
6. `sources-census.sh validate --file $V/corpus/SOURCES.md` → its TSV on **stdout**, its verdict
   as the exit code, `MIRROR: gate=PASS|FAIL census-exit=N` on **stderr**.

Exit: the census code (`0` clean or warnings, `1` E-findings, `2` census env/usage); `2` also
for a bad block (empty, heading, non-row line, no table end) or a bad `KNOWLEDGE` path.

## Evidence — the three required runs, plus the guards that make them mean something

All under `.ufo/waves/round-40/w1/ExecScratchMirror/` (combined stdout+stderr, `SCRIPT-EXIT`
appended). Fixtures in `fixtures/`.

| run | block | verdict | what it proves |
|---|---|---|---|
| `run-1-valid.txt` | `block-valid.md` (S900) | **exit 0**, `registry-rows=214->215 placement=ok`, 7 W04 + 1 W01 + `ok` | one valid row is admitted; the warnings are the lane's own round-start set (`receipts/census-before.txt`) |
| `run-2-dup-id.txt` | `block-dup-id.md` (reuses S220) | **exit 1**, `file E03 S220 duplicate id` | duplicate id fails the gate, as the census defines |
| `run-3-dup-url-e04.txt` | `block-dup-url-e04.md` (S901 repeats S007's URL in S007's scope) | **exit 1**, `file E04 S901 duplicate url wayland.freedesktop.org/libinput/doc/latest/tools.html within scope input-layer debugging route (libinput 1.32.0)` | same URL + same scope is an error |
| `run-4-dup-url-w04.txt` | `block-dup-url-w04.md` (S902, same URL, other scope) | **exit 0**, `file W04 S902 duplicate url … across scopes` | same URL + other scope is a **warning only** — the census's split, exercised on both sides |
| `run-5-no-closure.txt` | `block-valid.md --no-closure` | **exit 1**, 12 × `E11` over 7 targets (S096, S173, S174, S178–S182, S184, S185) | step 5 is load-bearing: `corpus/` alone cannot satisfy used-by targets such as `tools/`, `SKILL.md`, `.ufo/waves/*/registration.md` |
| `run-6-placement.txt` | `block-valid.md --keep` | `diff` lane↔mirror = **`226a227`** only; S900 sits at 227 between S220 (226) and the blank at 228 / `## Paths` (229) | the append is byte-exactly one inserted line, at the table end |
| `run-7-guards.txt` | `fixtures/guards.sh` | **11/11 PASS**, each exit 2 | no block arg · missing file · empty · whitespace-only · heading in block · non-row line · absolute knowledge · `../../` escape · knowledge absent from lane · unknown option · **scratch inside the lane** |
| `run-8-mutant.txt` | 3 mutants of the delivered script (in `/tmp`, since deleted) | 1 → `insert placement rejected: rows-before-block=0 want=214`; 2 → `block-not-after-a-table-row`; 3 → **exit 0** | see next section |
| `run-9-multirow.txt` | `block-two-rows.md` (S904+S905) | exit 0, `214->216` | multi-row blocks count rows, not lines |
| `run-10-cwd-today.txt` | from `cwd=/tmp`, no `--lane`, `--today 2026-10-25` | exit 0, lane auto-detected | reusable from any seat/cwd |
| `run-11-malformed.txt` | `block-malformed.md` (one column short) | **exit 1**, `file E01 S906 fields=10` | content errors reach the exit code; the gate is not just structural |

Read-only proof: `git rev-parse HEAD:corpus/SOURCES.md` = `git hash-object corpus/SOURCES.md`
= `94bc65f71393bdd1ffac91111ab81d8c92f23bd4` after every run; no `/tmp/mirror-validate.*`
survived; no `.guard-tmp` residue in the seat.

## The defect this seat found in its own first version (and the guard that catches it)

My first insert used "the first blank line after the `## Registry` heading". That heading is
followed by its **own** blank line before the header row, so the row landed at the **top** of
the table — above `| id | source | …` — and **the census still said `ok`, exit 0**: a row
inside the section but above the header is parsed as an ordinary data row, and E12 only fires
for rows outside the section. Row-count and E01 guards both passed too.

Mutant 3 in `run-8-mutant.txt` reproduces exactly that (`S900` at line 10, between the heading
and the header at 12, `gate=PASS census-exit=0`), which is why `verify_insert` exists and why
the delivered tool now inserts at the first blank line **after the table run has started**.
Mutants 1 and 2 show the verifier rejects both misplacements. Without the verifier the tool
would have shipped a gate that silently approves a corrupt table.

## Use in the section-10 append (integrator)

    cd /home/vgpnk/Projects/shokunin/mado-shokunin
    bash .ufo/waves/round-40/w1/ExecScratchMirror/mirror-validate.sh \
         <append-block-file> corpus/knowledge/hyprctl-getoption-native-forms-r40.md

Requires the entry file to already exist in the lane (otherwise the gate refuses at exit 2 —
by design: the gate cannot vouch for a file it cannot see). `--keep` leaves `$V` for
inspection; the trace names it.

## Limits (measured, not assumed)

- The mirror is not the lane: `QUALITY.md` is not copied (not in the assigned list), so a row
  whose `used-by` cites it would be closed by step 5 only if it is also reachable from the
  block's own `mined` rows — pass it as `KNOWLEDGE` instead.
- The census checks bytes, not truth: a fabricated but self-consistent row passes (the
  registration's declared C2 residual).
- `verify_insert` proves *where* the block sits, not that its rows are good — that stays the
  census's judgment (run-11).
- The gate reads the lane only; it cannot detect a lane edit that happens between its copy and
  the real append.

## Tooling

Nothing installed. `gawk`/`coreutils`/`bash` were already present (the census requires them).

## Report

`.ufo/waves/round-40/w1/ExecScratchMirror.md`
