# PRED-C1-r50 port changes (round-49 `quality/counters/c2-r49-bind-entry.py` → seat draft)

`port-diff.txt` is `diff -u quality/counters/c2-r49-bind-entry.py .ufo/waves/round-50/w1/ExecCounterC1R50/c1-r50-bind-entry.py`
(188 lines, 13 hunks). Every changed line, with its reason:

| port line(s) | round-49 text | round-50 text | reason |
|---|---|---|---|
| 2 | `PRED-C2-r49 … (C2, coverage, sourced)` | `PRED-C1-r50 … (C1, coverage, sourced)` | predicate name for the round-50 freeze; the claims make this the C1 (coverage, sourced) move of round 50 |
| 4-6 | round-49 freeze / `w1/ExecCounterC2` / BASE `03e4ae76…` | round-50 freeze / `w1/ExecCounterC1R50` / BASE `8ae47b95…` | new base (lane tip at round-50 start) and this seat's provenance; records that PRED-C2-r49 was never attacked (round-49 w2 never ran) |
| 7 | `ENTRY = corpus/knowledge/hyprland-bind-key-match-r49.md` (docstring) | `…-r50.md` | entry path re-opened this round |
| 10 | `.ufo/waves/round-49/fetch/` (docstring) | `.ufo/waves/round-50/fetch/` | pins for round 50 live under the round-50 wave dir |
| 38-39 | clause c: `round-49 fetch pin` / `.ufo/waves/round-49/fetch/<path>` | `round-50 …` / `.ufo/waves/round-50/fetch/<path>` | rows must bind this round's pins, not the round-49 copies |
| 57 | clause d: `(round-49, or the round-46 pin …)` | `(round-50, …)` | quote locators resolve against the round-50 pins (round-46 held pin unchanged) |
| 67 | clause e: `(round-49 head row or the held round-46 row)` | `(round-50 head row …)` | same, for the step-grounded quotes |
| 71-72 | clause f: `.ufo/waves/round-49/receipts/<file>` | `.ufo/waves/round-50/receipts/binds-live-r50.txt` | receipt dir re-pointed **and** the capture's name pinned (round-50 receipt name pattern; see `RECEIPT_NAME`) |
| 95 | clause i: `corpus/lessons/round-49.md` | `corpus/lessons/round-50.md` | the Gate lives in this round's lesson |
| 100-105 | clause i GROUND `("xkb_state_key_get_one_sym", "m_xkbSymState", …)` | `("xkb_state_key_get_layout", "m_modifiersState", …)` + rationale | both old terms now occur under `corpus/` at the new base (round-49 closure text quotes them), so clause i's "no match at BASE" would fail for a reason unrelated to the entry; replacements are source-derived names of the same mechanism, absent at base (see the GROUND table in the report) |
| 131 | `Final line: PRED-C2-r49: …` | `PRED-C1-r50: …` | emitted predicate name |
| 159-167 | `PRED`, `ENTRY`, `LESSON`, `FETCH`, `RECEIPTS`, `BASE_DEFAULT` | `PRED-C1-r50`, `…-r50.md`, `corpus/lessons/round-50.md`, `.ufo/waves/round-50/fetch/`, `.ufo/waves/round-50/receipts/`, `8ae47b95…` | the operative re-point; `BASE_DEFAULT` also makes the default `--base` the round-50 base |
| 177-178 | `GROUND` tuple | new tuple | matches the clause i text above |
| 200-202 | — | `RECEIPT_NAME = re.compile(r"^binds-live-r50\.txt$")` | round-50 receipt name pattern named in the seat spec; clause f/r may not score any other file under the receipts dir |
| 334-347 | `locators()`: digest prefixes skipped only | also skips a token with no `[a-z_]` | **repair F1** (see report): round-49 clause d read the mask-histogram band `0:23` as a locator, resolved it to the pin whose stem contains `0` (`binds-live-r49`, 17 lines) and failed clause d on a legitimate table row |
| 736-741 | clause f iterated every cited receipt | filters to `RECEIPT_NAME`, prints `clause=f receipt_name=[…] want=…` when none matches | enforce the round-50 receipt name; the diagnostic names every receipt the entry cites |
| 1126 | clause r iterated every cited receipt | same filter | clause r replays only the pinned capture |
| 1246-1254 | no-pins short-circuit printed `CLAUSES = "a:1 c:0"` and dropped the clause b it had just computed | builds the vector from what was evaluated: `a:1 b:<computed> c:0` | **repair F5** (w1/ExecControlsC1R50 control-vector report): with the round-50 `fetch/` empty, a control run stops after c, and the old literal made a b failure read as a c failure. d..r are still not scored, and the vector names only a/b/c, so it claims nothing it did not run |

Unchanged by design (byte-identical, meaning unchanged): `HELD = ("S319",)`, `HELD_FETCH = ".ufo/waves/round-46/fetch/"`
(held row and its round-46 pin), `MIN_ID = 352`, `MIN_SOURCES = 3`, `MIN_RECEIPT/MAX_RECEIPT`, `OPENED = "2026-10-27"`,
`HYPRLAND_COMMIT`, `HYPRLAND_VERSION`, `FORMS`, `TAGS`, `BRANCH_REFS`, `EXTS`, `LOC_*`, `QUOTE_RE`, `RAW_RE/GH_RE/GL_RE`,
`TOPICS` and clause j, `clause_c/d/e/g/h/i/j` bodies, `tmp_root()` (TMPDIR required, `/tmp` refused), `live_binds()`
(clean `HOME`/`XDG_*`, `XDG_RUNTIME_DIR`+`HYPRLAND_INSTANCE_SIGNATURE` inherited, JSON never printed), `main()`,
exit codes 0/1/2.

`MIN_ID = 352` was kept because the registry still tops at S351 at the new base:
`git show 8ae47b95:corpus/SOURCES.md | grep -oE '^ {0,3}\| *S[0-9]{3,}' | tail -1` → `| S351`.
