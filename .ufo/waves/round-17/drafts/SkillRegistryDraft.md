# SkillRegistryDraft (round 17) — proposed SKILL.md registry rows

Status: DRAFT for L1 integration. Not applied to `SKILL.md`. Target insertion: after the
`mado-round16-measure` row (SKILL.md line 545), before the blank line that precedes
`Round-16 classifier limit:` (line 547). Column shape copied from the rows at SKILL.md lines 532-545
(8 columns: name | gate/probe | entry command | verdict map | self-test command / spelling |
pinned-value path | write scope | owner).

Source-state note: at drafting time `tools/mado-tripwire.py`, `.ufo/waves/round-17/tripwire/core/`,
`.ufo/waves/round-17/tripwire/compound/`, and `.ufo/waves/round-17/label-check.py` /
`label-claims.json` did not yet exist in the lane. Paths below are the spec'd paths; L1 must confirm
them after the producing seats land. Nothing here was executed.

| name | gate/probe | entry command | verdict map | self-test command / spelling | pinned-value path | write scope | owner |
|---|---|---|---|---|---|---|---|
| mado-tripwire | gate | `python3 -I tools/mado-tripwire.py --scan PATH [PATH ...] [--permit CLASS ...]` (PATH = a `*.jsonl` file or a directory searched recursively for `*.jsonl`; post-hoc scan of OMP session JSONL, assistant `toolCall` bash/eval inputs only) | 0 clean (no unpermitted finding; first line `MADO_TRIPWIRE: clean`); 1 failed (at least one unpermitted finding; `MADO_TRIPWIRE: findings`); 2 could-not-evaluate (no `.jsonl` found, unreadable file, invalid JSON line, or usage; `MADO_TRIPWIRE: could_not_evaluate`); exit 2 wins over 1 | `python3 -I tools/mado-tripwire.py --selftest .ufo/waves/round-17/tripwire/core` and `python3 -I tools/mado-tripwire.py --selftest .ufo/waves/round-17/tripwire/compound`; selftest: 0 all cases pass, 1 any case fails, 2 malformed `expected.json` | `tools/mado-tripwire.py` (class and rule tables, `sudo` wrapper rule, redaction and 240-char truncation); per-fixture `expected.json` in `.ufo/waves/round-17/tripwire/core/` and `.ufo/waves/round-17/tripwire/compound/` (synthetic fixtures, no real transcript bytes) | read-only: reads only the JSONL paths named on the command line; never executes or inspects anything else; selftest self-invokes with `sys.executable -I` on fixture paths only; no interception, prevention, or host repair | mado |
| mado-label-check | probe | `python3 -I .ufo/waves/round-17/label-check.py` (reads `.ufo/waves/round-17/label-claims.json`; checks each claim's doc line and receipt token at the stated revision via `git show`) | 0 all claims `ok` (`LABEL_SUMMARY: k/n`, k = n); 1 any claim `MISMATCH`; 2 could-not-evaluate (malformed claims, missing revision, or usage); other could-not-evaluate. Probe output is a label audit, not a product or desktop-health verdict | — (probe; no selftest defined in the round-17 spec; seeded claims serve as the red control, the R16-V1 line that must MISMATCH, and a green control) | `.ufo/waves/round-17/label-claims.json` (seed claims: round-16 lesson line 131 against `.ufo/waves/round-16/evidence/frozen-tampered.json`, expected token `snapshot_tampered`, recorded receipt token `frozen_error`) | read-only: `git show` of committed bytes at the claimed revision; no gate execution, host, device, or config access; writes nothing | mado |

Limit (post-hoc only): `mado-tripwire` runs after the fact, classifies only bash/eval `toolCall` commands the assistant issued, and cannot intercept, block, or repair the host.
Transcripts are mutable host files, bound only by the digests and byte counts in `.ufo/waves/round-17/evidence/session-index.json` (pending); a changed file fails its digest and is not thereby clean.
Tool results, user text, and `thinking`/`text` blocks are not inspected; a clean scan means no listed pattern matched in the named files (unlisted wrappers are not classified), not no host mutation.
`mado-label-check` verifies only that a cited receipt contains the cited token at the stated revision, not the claim's meaning.
Registration is not verification; the round report must cite the actual self-invocations and observed exit codes.
