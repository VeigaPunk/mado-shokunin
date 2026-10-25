# ScribeQuality — round 37 wave 1 (scribe)

Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`, HEAD `80b83c856b8cad60b88e63d8d3ab06b1d8dfea5b`.
Assignment: `.ufo/waves/round-37/w1/prompts/ScribeQuality.md`. This seat drafts QUALITY.md criteria 62 and 63.

## Behavior

- Draft written: `.ufo/waves/round-37/w1/scratch/ScribeQuality/criteria.md`
  (sha256 `c4a3e5e1add75ec8a3c6ed3d147001b5527428b839d98ff93243d38ab686315d`), two numbered lines, `62.` and `63.`.
- The drafts follow the house style of `corpus/QUALITY.md:362-369` (criteria 56–61). Each one is a single numbered paragraph containing the rule, a round application with path:line pointers, a `Check:` command that shows a violation, an `Extends criterion N` link, a `Limit:`, and a closing `(lesson: …)` anchor.
- `corpus/QUALITY.md` was not edited. The closer appends the drafts. `grep -E '^[0-9]+\. ' corpus/QUALITY.md | tail -1` → `61.`, and the count is `61`, so 62 and 63 are the next free numbers.

## Gates

| item | command | quoted output | verdict |
|---|---|---|---|
| Round-30 citation rubric on the draft | `grep -cE '^[0-9]+\. ' F; grep -cE '^[0-9]+\. .*lessons/' F; grep -cE '\(lesson: lessons/[^)]*\)$' F` | `2` / `2` / `2` | PASS |
| Lesson anchor for 62 resolves in the named file (criterion 54) | `grep -n '^## Wave-2 falsifications applied as errata$' corpus/lessons/round-35.md` | `178:## Wave-2 falsifications applied as errata` | PASS |
| Lesson anchor for 63 resolves | `grep -n '^5\. \*\*R5' corpus/lessons/round-36-verifier-spotcheck.md` | `141:5. **R5 — one observable is a worktree reading.** …` | PASS |
| Round-35 null-channel withdrawal exists | `rg -n -i 'null channel\|null-channel' corpus/ …` | `corpus/lessons/round-35.md:184: journal's zero \`omarchy-toggle\` count is a null channel`; `corpus/knowledge/idle-lock-never-asked-r12.md:46: a zero \`omarchy-toggle\` count is a null-channel reading, not a negative` | PASS |
| Logger gate, S214 | `sed -n '1,60p' fetch/S214.bin` | `:15 if (!m_logsEnabled)` `:16 return;` `:32 m_logger.setEnableStdout(true);` `:47 m_logger.setEnableStdout(!*PDISABLELOGS && *PENABLESTDOUT);` `:48 m_logsEnabled = !*PDISABLELOGS;` | PASS (matches the freeze claim) |
| Marker lines, S189 | `sed -n '150,180p' fetch/S189.bin` | `:155 Log::logger->log(Log::ERR, "Socket2 fd {} failed writing event: …` `:175 Log::logger->log(Log::ERR, "Socket2 fd {} overflowed event queue, removing", …` | PASS |
| Receipt digests | `sha256sum fetch/S213.receipt.txt fetch/S214.bin fetch/S189.bin` | `1c1b0ce1…2ce58`, `d04e3a2f…f6b868`, `eea605df…540d`; S214 matches `renumber-map.md:24` `d04e3a2f…f6b868` | PASS |
| S213 log counts reproduce (read-only file read) | `wc -l`, `grep -cE '^[A-Z]+ \]'`, `grep -cE '^ERR \]'`, origin histogram, marker greps on the session log | `27331`; core `21`; core ERR `0`; last core line `21`; `21 DEBUG ]`, `27280 DEBUG from aquamarine ]`, `31 ERR from aquamarine ]`; markers `0`, `0`; config-load lines `12 18` | PASS (identical to S213) |
| Live option (read verb) | `hyprctl getoption debug:disable_logs -j`; `hyprctl version -j` | `{"option":"debug:disable_logs","int":1,"set":false}`; `"tag": "v0.56.2"`, `"commit": "efb50993…"` | PASS |
| 62's `Check:` runs as written (criterion 61) | `awk -v p=18 'NR>p && /^ERR \]/' <log> \| wc -l`; `awk -v p=18 'NR>p && /^[A-Z]+ \]/' <log> \| wc -l` | `0`; `3` | PASS. The command runs, and the probe is 0, so the zero is refused. |
| 63's `Check:` runs as written | `git grep -nE '"(status\|diff)", *"--\|git (status\|diff) --' HEAD -- quality/ tools/` | 3 hits, all `quality/check-evidence-pointers.py` (`:23`, `:171`, `:172`) | PASS (no false positives at HEAD) |
| 63's round-36 application | `git ls-tree --name-only HEAD -- .ufo/waves/round-36/receipts/`; `git show HEAD:…/before-pointers.txt` | five receipts, no porcelain witness; `:4 # inherited_dirty=10 …`; `:12 PRED-PTR-r36-v1 … inherited_dirty=0 …` | PASS. R5 still stands at HEAD. |

## Findings

1. **F1: S213's journal probe uses the wrong class; the reading stands.** The receipt checks the journal with an aquamarine string (`probe_string: "drm: getCurrentCRTC: No CRTC 0" in_log=7 in_unit_journal=0`). The journal does carry the core logger:
   - `journalctl --user -u wayland-wm@hyprland.desktop.service --no-pager -q -o cat | grep -cE '^[A-Z]+ \]'` → `42`, all of them `DEBUG ]`.
   - The core lines sit at journal lines 41–61 and 401–421, with config loads at `52 58 412 418`. That is two starts, each ending three lines after its second config load, the same shape as the session log.
   - Logger.cpp explains this: `:32` turns stdout on at init, and `:47` turns it off once the config is read.
   - Core `ERR` lines in the journal: `awk '/^ERR \]/' | wc -l` → `0`.

   So "the journal never carries core-logger lines" would be false. The correct refusal is narrower: neither channel carries any core-logger line after the config applies `disable_logs`, and neither carries any core `ERR` line at all. Criterion 62 states it that way, and it rules that a probe from another logger does not qualify. Disposition: recorded for the C1 entry author and the errata seat. S213's conclusion, that a zero cannot distinguish "never overflowed" from "not logged", is unaffected.
2. **F2: Plain `git status` writes the index.** `tools/mado-verify.sh:3668` reads "Never \`git status\`/\`fetch\` on the checkout (index stat-cache refresh, …)". Criterion 63 therefore prescribes `GIT_OPTIONAL_LOCKS=0` for the witness. Bounds incident on this seat: early in the run I ran `git status --porcelain | wc -l` in LANE (output `0`). Afterwards, `stat -c '%y %s' .git/index` read `2026-10-25 09:12:59.919986844 -0300 1484400`, which is inside this seat's run window. I cannot tell whether my command or a sibling refreshed the index stat cache. Index content is not changed by a stat refresh, and no staging or other git or jj mutation was run.
3. **F3: The round-37 lesson anchor is owed.** Criterion 62 cites the round-35 anchor that exists today and puts its round-37 grounds in-line as receipt paths (S189, S213, S214, `renumber-map.md:22`). If the round-37 lesson gains an `M37-x` for the null channel, the closer should add `lessons/round-37.md#mistakes M37-x` to the `(lesson: …)` parenthesis. I did not cite that anchor because the file does not exist yet.

## Touched surfaces

- Written: `.ufo/waves/round-37/w1/scratch/ScribeQuality/criteria.md` and this report.
- Read only: `corpus/QUALITY.md`, `corpus/lessons/round-35.md`, `corpus/lessons/round-36.md`, `corpus/lessons/round-36-verifier-spotcheck.md`, `corpus/knowledge/idle-lock-never-asked-r12.md`, `quality/check-evidence-pointers.py`, `tools/mado-verify.sh`, `SCORECARD.md`, `.ufo/waves/round-36/receipts/before-pointers.txt`, `.ufo/waves/round-37/fetch/{S189.bin,S213.receipt.txt,S214.bin}`, `.ufo/waves/round-37/assimilation/renumber-map.md`, the session log (counts only), and the unit journal (counts and line numbers only; no line reproduced).
- Host: only the `hyprctl` read verbs `getoption` and `version`. No socket connection was made, and nothing was dispatched, set or reloaded.

## Out of scope

- Appending 62 and 63 to `corpus/QUALITY.md` (production file; closer).
- Repairing S213's journal probe or `quality/check-evidence-pointers.py` (routed per criterion 52, not patched).

## Tooling

None installed or upgraded.

## Artifacts

- `.ufo/waves/round-37/w1/scratch/ScribeQuality/criteria.md`
- `.ufo/waves/round-37/w1/reports/ScribeQuality.md`
