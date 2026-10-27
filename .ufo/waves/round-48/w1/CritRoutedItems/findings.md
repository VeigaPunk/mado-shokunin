# CritRoutedItems findings — routed round-47 closure items at `579f694b` (round-48 base)

Seat: `CritRoutedItems` (leaf). Task: for each routed item (D1-D4, R3, R4b, M47-10, `w2/CritC1Explain.md`,
`w2/SentC1Sandbox.md` F1-F4) check at 579f694b whether it is still open and whether the round-47 drafts it points at
are stale (file changed since). Method: read-only `git log`/`git ls-tree`/`git grep`/`git show` at 579f694b, plus
one fresh read-only run of the tracked session-material gate (`quality/check-session-material.py --rev 579f694b`).
Nothing was written outside this seat dir; no tools installed; no scratch used (no generated files).

**Summary: all nine items are OPEN at base; none of the referenced drafts is stale.**

| item | open? | draft stale? | evidence (one line) |
|---|---|---|---|
| D1 contract narrowing | OPEN | no | landed `tools/mado-terminal.py:85-86` still lists "HOME unset / a FIFO named like a desktop file in a later application dir / symlink loops" as out of contract (exit 2), absent from the frozen reference docstring (`l1-draft/mado-terminal.py`; `registration.md:30`), and no appended lesson line exists (`git grep 'HOME unset' corpus/lessons` hits only the spotcheck lesson) |
| D2 findings=128 unreceipted | OPEN | no | fleet report `.ufo/reports/round-47/mado.md:104` still claims "session-material gate reads `findings=128` at the tip (115 at base)" with no committed receipt (`git grep 'findings=128' 579f694b` → NO-MATCH); fresh read-only re-run prints `SESSION_MATERIAL: files=19969 findings=128 rev=579f694b…` exit 1 — number matches, receipt still absent |
| D3 readdir-order blind spot | OPEN | no | `w2/ExecC1Determinism.md:10` ("clause f/x are blind to the readdir axis, so a tool that sorts directory entries … passes all 190 fixtures and all 190 explain checks") stands: `c1-r47-fixtures.json` frozen & unchanged at d7527d60, no two-valid-candidate-in-one-dir fixture (draft §2: 12 such dirs, losers excluded by another key; tmpfs rebuild byte-identical) |
| D4 erratum off-by-one | OPEN | no | `xdg-terminal-selection-r47.md:95` still cites `terminal-route-r17.md:150-151`; computed locator puts the helper bullet at 149-150 (`grep -n` → 149 "- [UNK] Whether the `--dir=` value …", 150 "launch time. The helper is not run.") and the entry has no `## Errata` section |
| R3 synthetic marker install | OPEN | no | draft marker gate exists (`w1/ExecSessionMarker/check-session-material.py`, 9bddd6ac, selftest 63/63) and w2 attacks exist at base (`MutSessionMarker`/`RevSessionMarker` .md+dir), but the install never landed: `quality/session-material-waivers.txt` ABSENT, tracked gate `quality/check-session-material.py` unchanged since ee6659b9, `SKILL.md:770` still reads "no synthetic marker yet, so a red exit is expected until it lands", gate red at base (findings=128 exit 1) |
| R4b round-45 errata | OPEN | no | `w2/ExecErrataR45.md` H1 (29-67) stands: the drafted block flips PRED-C2-r45 MET→MISSED, `block-fixed.md` keeps MET, and neither landed — target `hyprland-monitor-rule-r45.md` unchanged since ee6659b9 with no `## Errata` section |
| M47-10 fixture schema v2 | OPEN | no | `w2/ExecC1Diff.md` H1/H2/H3 (53/105/140: `find -type f` first-dir bug, `command -v` option-like names, HOME unset) are still outside the frozen fixtures/counter — `c1-r47-fixtures.json`/`c1-r47-terminal.py` unchanged since d7527d60, fixtures carry only files/exec, `gen_case` never draws option-like `Exec`/`TryExec` |
| CritC1Explain explain cmd= | OPEN | no | `w2/CritC1Explain.md:9` pass-mutant proof stands: clause x at `c1-r47-terminal.py:277-290` still compares only `(id, path, verdict, rc)` (`want=(parts[0], parts[1], "OK", 0)`) and the bad capture mutates only the first `.desktop` — the third printed cmd item is never compared |
| SentC1Sandbox F1-F4 | OPEN | no | `w2/SentC1Sandbox.md` F1 (100) / F2 (118) / F3 (128) / F4 (135) all stand against the unchanged frozen instruments: `/fast` stub present+writable vs `registration.md:36` "without … /fast", `/usr/bin` present vs docstring "only: /usr/lib…", host identity, and F4's tool pre-created `<root>/.rw/obs` abort at `c1-r47-terminal.py:279` (`os.makedirs(obs_dir)`) |

## Draft staleness (per referenced file, at 579f694b)

- Every referenced w2 draft was created in the single w2-evidence commit `d40189c9` (ExecC1Determinism.md,
  ExecErrataR45.md + block-as-drafted/block-fixed.md, ExecC1Diff.md, CritC1Explain.md, SentC1Sandbox.md,
  MutSessionMarker.md, RevSessionMarker.md) and has never been modified since: `git log --format='%h' 579f694b -- <f>`
  returns exactly one commit each.
- `w1/ExecSessionMarker/check-session-material.py` was created in `9bddd6ac` (w1 evidence), single commit.
- `corpus/knowledge/xdg-terminal-selection-r47.md` was created in `0c699605` (round-47 data), single commit.
- Post-base commit `5ff16742` (round-48 prep: claims, w1 spec/dispatch, census-before) touched only
  `.ufo/waves/round-48/*` — no referenced draft changed after base.
- Targets the drafts describe are byte-unchanged at base: `c1-r47-terminal.py`, `c1-r47-fixtures.json`,
  `registration.md`, `l1-draft/mado-terminal.py` @ d7527d60 (freeze); `hyprland-monitor-rule-r45.md` and
  `quality/check-session-material.py` @ ee6659b9 (round 45); `terminal-route-r17.md` @ f71ccbe5 (round 17).
  No draft is superseded by a later fix.

## Receipts

- `git log` (base-reachable) per referenced file: single/expected commits as above.
- `git show 579f694b:tools/mado-terminal.py | grep -n 'HOME unset|FIFO|symlink loop'` → lines 85-86 (landed docstring);
  same grep on `l1-draft/mado-terminal.py` → code-only `OutOfContract("HOME unset")` at 407, no docstring listing.
- `git grep -n 'findings=128' 579f694b -- .ufo/waves/round-47` → NO-MATCH (D2).
- `git show 579f694b:corpus/knowledge/terminal-route-r17.md | grep -n 'UNK] Whether the `--dir=`'` → 149-150 (D4).
- `git show 579f694b:corpus/knowledge/xdg-terminal-selection-r47.md | grep -n 'Errata|erratum'` → NONE (D4).
- `git show 579f694b:corpus/knowledge/hyprland-monitor-rule-r45.md | grep -n 'Errata|erratum|R4b'` → NONE (R4b).
- `git ls-tree -r --name-only 579f694b | grep -i session-material-waivers` → ABSENT (R3).
- Live read-only gate: `python3 -I quality/check-session-material.py --repo . --rev 579f694b...` →
  `SESSION_MATERIAL_RULES: R1_CLIENT_DUMP=33 R2_PROC_TABLE=36 R3_MONITOR_IDENT=57 R4_HOME_LISTING=2` /
  `SESSION_MATERIAL: files=19969 findings=128 rev=579f694b...` exit 1 (R3 red; D2 number reproduced, still unreceipted).
- `git status --porcelain` after the gate run: no tracked modification (only the round-48 prep untracked files).
- `verify-quotes.sh` (this dir): 10/10 quoted fragments verified by grep at computed locators (`verify: ok=10 fail=0`), including `registration.md:36` "bwrap allowlist root without /usr/bin, /usr/share, /etc, /home, /fast" and the D4 locator pair.
