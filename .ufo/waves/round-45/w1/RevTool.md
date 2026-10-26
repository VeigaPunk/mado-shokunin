# Seat RevTool — report (w1, round 45)

Status: DONE. Reviewed `.ufo/waves/round-45/l1-draft/mado-monitors.py` (532 lines) — docstring vs code
sentence-by-sentence, input handling, output injection, exit codes, stdin cap, read-only claim,
selftest teeth — with executed repros and two frozen-counter runs on scratch clones.

Deliverable: `.ufo/waves/round-45/w1/RevTool/review.md` (severity-ranked F1-F7, each with path:line
locators, repro commands, observed output; receipts in `.ufo/waves/round-45/w1/RevTool/receipts/`).

Headline findings:
- F1 MEDIUM: `json.loads` accepts JSON `NaN`; `scale: NaN` false-AGREEs → verdict OK exit 0, against
  docstring:28-29 (bad_json). Not caught by selftest (33/33 unchanged) or the 49 fixtures.
- F2 MEDIUM (teeth): the 1048576-byte cap is enforced nowhere — mutant raising `MAX_BYTES` scores
  `fixtures=49/49 selftest=ok verdict=TARGET_MET` on the frozen counter
  (receipts/counter-m2b-nocap.txt). The reference itself is boundary-correct (1048576 OK; +1
  too_large, file and stdin; /dev/zero bounded).
- F3 LOW/MEDIUM (teeth): selftest has zero bad_json cases; with the shape check disabled it still
  prints 33/33, and `[1, 2]` then crashes rc 1 (DIFFER's code) with a traceback. Counter fixtures do
  catch it. Control mutant M3 (`< 1.0` → `<= 1.0`) fails 32/33 — the selftest is not vacuous.
- F4 LOW: `--monitors -` with closed stdin blocks indefinitely (fd 0 reopened to a blocking char
  device; no SETUP line, no exit; killed at 60 s, receipts/closed-stdin.txt).
- F5 LOW: BOM (first rule silently dropped → NO_RULES), CRLF (all lines unsupported →
  NOT_COMPARED), `$`/`##` in a trailing comment (NOT_COMPARED) — all conform to the docstring's
  letter, none warned about; all fail loud, never silently agree.
- F6 INFO: no output injection found — hostile selectors/names (newlines, NUL, surrogates, forged
  `verdict=` text) stay inside json.dumps quoting; backslash selectors are excluded upstream.
- F7 INFO: docstring conformance otherwise clean (arguments, setup reasons, rule semantics, type
  discipline incl. bool-as-int/float-width, verdict order/exits, 1/120 scale search incl. negative
  candidates unreachable); read-only holds (imports, no bare open(, poisoned-PATH markers absent,
  env -i clean, TMPDIR untouched).

Reference baseline verified directly: selftest `33/33 passed` rc 0; frozen counter on the reference
clone: `fixtures=49/49 selftest=ok readonly=ok verdict=TARGET_MET` (receipts/counter-ref.txt).

Safety: writes only to the seat dir; scratch /fast/scratch/hyaku/mado-r45/RevTool (deleted on
finish); no pacman; no tool installs (system python3 3.14 + git only); throwaway-identity commits
only inside scratch clones; no host-service or compositor mutation (no hyprctl beyond none needed).
LSP: no lsp device mounted in this session — all semantic claims are full-file reads + executed
repros, not index output.

Report: .ufo/waves/round-45/w1/RevTool.md
