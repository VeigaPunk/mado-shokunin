# ExecIndepB — second implementation of C1 (`tools/mado-monitors.py`)

Round 45, w1, lane `mado-shokunin`. Seat target: an independent rebuild of the frozen C1 contract with different
author habits, scored at seeds 45, 3 and 99.

## Result

- Deliverable: `.ufo/waves/round-45/w1/ExecIndepB/mado-monitors.py` — 848 lines, stdlib only (`json math os re stat
  struct sys`); no subprocess, no socket, no PATH lookup.
- Selftest: `MADO_MONITORS_SELFTEST: 55/55 passed` (47 report cases + 6 setup-path cases + `--config -` + a full CLI run).
- `PRED-C1-r45` in a scratch clone of the freeze commit plus my commits, at seeds 45 / 3 / 99:
  `fixtures=49/49 selftest=ok readonly=ok tool=present verdict=TARGET_MET`, rev
  `811bc81eceeb64002968a2b8f472751f67548ebd` (receipts/c1-score-3seeds.txt, 147 fixture clause lines).
- Reproduce: the scored rev lives in a scratch clone that seat hygiene deletes; the scored blob is sha256
  `fb7868847fa40db1244ba80968c1a8c094346fc0750c3ac7848c7ca5afdb0c11`, so copying `.ufo/waves/round-45/w1/ExecIndepB/mado-monitors.py` to `tools/mado-monitors.py` in a clone of `22a8dedd` and
  rerunning the command above reproduces the score.
- Failing fixtures: **none at any seed**, so there are no fixture rulings to report (tool vs contract).
- Live host join, read-only (`hyprctl monitors all -j` piped, never stored): `AGREE` / `verdict=OK`, exit 0, byte-identical
  as the reference's own lines for a live host dump (receipts/live-host-join.txt).

## Disclosure: this seat saw the reference body

I read the frozen docstring as instructed; then, while orienting in `.ufo/waves/round-45/l1-draft/`, I read the rest of
the reference implementation (lines 124-532 of that file) before writing my copy. This seat is therefore a **second
implementation with reference view, not a blind one**: the "two independent authors" argument cannot rest on this seat
alone. What still holds: a different structure (`Rule` class with slots/clone, table-driven `VALUE_KEYS`,
`HEAD_HANDLERS` and `CHECKS` dispatch, `read_file` separated from the stdin `slurp`, integer divisibility with an
explicit `close_enough` tolerance helper); my own selftest cases; and every behavioural difference from the reference
found by differential probing and ruled against the docstring text, not against the reference.

## Divergences from the reference, each ruled

**D1 — zero-sized live output with an explicit scale.** *Reference:* no scale compare when live `width` or `height` is
<= 0. *Mine:* compares (0/S is whole, so E = S). Evidence receipts/differential-edges.txt:3-7 (rule `1.25`, live `0x0`,
mine `differ=mode,scale`, ref `differ=mode`), :24-28, and 31 of 1200 fuzz cases in two families, all zero-size.
*Ruling: contract, not tool* — the text makes E = S when both quotients are whole and reserves "not compared" for the
divisor search (quotes Q1/Q6 below); the reference carries an undeclared `w > 0 and h > 0` guard. Degenerate dumps only;
both score 49/49.

**D2 — two dump entries sharing the name of a mirror target.** *Reference:* first integer `id` among all entries named
M. *Mine:* the first entry named M, whose `id` must be an integer. Evidence receipts/differential-edges.txt:8-12 (mine
`differ=mirror`, ref `AGREE`). *Ruling: ambiguous; mine is the literal reading* — Q2 says "the dump output named M",
singular; wording proposed in A2.

**D3 — a live integer beyond double range.** *Reference:* crashes on `width = 10**400` (`OverflowError: int too large to
convert to float`, empty stdout, exit 1 — receipts/differential-edges.txt:13-17). *Mine:* the scale cannot be established,
so it is not compared; `differ=mode`, documented output. *Ruling: contract, not a crash* — the wrong-type clause (Q5) does not cover a correctly typed
integer, so the contract does not authorise a stack trace; wording proposed in A4. This reference defect is invisible to
the 49 fixtures and would ride into `tools/mado-monitors.py` if the reference were installed verbatim.

**D4 — `--config -`.** My first build treated any `-` path as stdin, so `--config -` silently read the already consumed
dump stream. The docstring binds stdin to `--monitors -` only (Q7) and makes any other missing path `unreadable`.
*Fixed*: my tool and the reference now both print `MADO_MONITORS: SETUP unreadable`, rc 2, for `--config -` with no such
file. *Ruling: tool defect, fixed.* It also shows a hole in the fixture set: no fixture passes `-` as a config.

**D5 — E as double vs f32.** *Reference:* rounds the found 1/120 multiple to 32 bits. *Mine:* keeps the double. Probe E
(razor band, `scale=1.33343333`) is SAME; a flip needs |live − E| within ~6e-8 of 1e-4. *Ruling: contract silent* —
Q1/Q6 never say f32 for E; wording A5.

**D6 — unknown key on a line whose MODE/POSITION/SCALE is also unmodelled.** Both implementations validate values first
(→ `unsupported`); the prose puts the key loop first (Q3) and value validation later (Q4), which reads the other way.
Probes D and D2 (`3440x1440@100Hz ... wat, 1`; `transform, 9, wat, 1`) are SAME: both tools sit on one side of an
undecided sentence. *Ruling: ambiguous*; wording A3.

## Ambiguous sentences and proposed wording

Each quote is verbatim, <= 25 words, on the cited line of `.ufo/waves/round-45/l1-draft/mado-monitors.py`; locators are
`grep -n`, and receipts/quotes-verified.txt is the script output that greps this report and the source.

- **A1 zero width/height (D1).** Q1 (:70) "the expected scale E is Hyprland's correction of S for the live `width` and";
  Q6 (:73) "none found means the scale is not compared."
  Proposed: "A live `width` or `height` of 0 is divided like any other integer (0/S is whole), so E = S and the field is
  compared; only the 1/120 search falling through all 89 steps skips the field." If the reference's skip is intended,
  write instead: "when live `width` or `height` is 0 the scale field is not compared."
- **A2 duplicate mirror target (D2).** Q2 (:75) "`mirrorOf` is the decimal `id` of the dump output named M".
  Proposed: "the first dump element whose `name` is M; if that element's `id` is not an integer the mirror field fails."
- **A3 unknown key vs unmodelled value (D6).** Q3 (:46) "any other key adds one to `badrules` and the rule is not added" against Q4 (:54) "SCALE or transform VALUE outside these forms makes the line `unsupported` (not modelled)."
  Proposed: "fields are validated left to right — MODE, POSITION, SCALE, then each KEY/VALUE pair — and the first failure
  decides: an unknown key is `badrules`, an out-of-form value is `unsupported`."
- **A4 integers outside double range (D3).** Q5 (:77) "A live value that is missing or of the wrong JSON type (integers for width, height, x, y, transform, id;". Proposed: "an integer too large for double arithmetic is not of the wrong type: the scale correction finds no divisor, so the scale is not compared; every other field is compared normally."
- **A5 rounding of E (D5).** Proposed: "E is the double `K/120` (or `(K±i)/120`) as computed; it is not rounded to 32
  bits."
- **A6 `-` for `--config` (D4).** Q7 (:28) "stdin, `--monitors -`, is read at most 1048577 bytes". Proposed: "`-` means
  standard input only as the `--monitors` value; as a `--config` value it is an ordinary path."

## Evidence

- receipts/c1-score-3seeds.txt — three `PRED-C1-r45` runs (seeds 45, 3, 99) at rev `811bc81`, 49/49 fixtures each,
  with the a/s/f/r clause lines.
- receipts/differential-edges.txt — 24 hand-built edge probes against the reference (SAME/DIFF per case) plus a
  1200-case differential fuzz (seed 4517; 31 differing cases, two families, both zero-size).
- receipts/live-host-join.txt — host `DP-1` join for my tool and for the reference (AGREE/OK, exit 0); the dump was
  piped and never written, so no serials or descriptions were kept.
- receipts/quotes-verified.txt — Q1-Q7 checked twice: present on the cited source line, present here.
- verify-quotes.py — the checker (locators computed by grep, not typed).
- diff-probe.py, diff-fuzz.py — the differential harnesses whose output receipts/differential-edges.txt keeps.
- Nothing else was written in the lane: this report, the tool copy, the two harnesses, `verify-quotes.py` and the receipts. No package,
  tool or version was installed (no uv/pip/npm/pacman), no network use, no compositor mutation; reads were
  `os.stat`/`open` of files and one piped `hyprctl monitors all -j`.

## Risks

- R1 the independence caveat above: treat this as one implementation plus a second reviewer's reading, not as author
  diversity.
- R2 A1 and A2 are invisible to the 49 fixtures: whichever tool the L1 installs passes the counter, so the wording, not
  the score, must decide them.
- R3 the reference (therefore the likely shipped tool) crashes on a correctly typed huge integer `width`; my tool does
  not. C1 cannot measure that difference.
- R4 the fixture set never exercises `--config -`, a `-`-named path, or duplicate dump names, so the frozen counter
  cannot separate the readings in A1/A2/A6.

## Blockers

None.
