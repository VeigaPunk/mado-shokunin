# ReviewSkillRows — round-17 wave 2 attack on the three new registry rows, the limit paragraph and the usage subsection

Seat: `MadoR17.ReviewSkillRows` (reviewer, leaf; no subagent dispatch).
Lane root: `/home/vgpnk/Projects/shokunin/mado-shokunin`. HEAD measured: `988b858bd6049bc709807534fd725c05264f7e60`.
Scope: `SKILL.md` lines 525-534 (`### Post-hoc transcript tripwire (round 17)`), 557-559
(`mado-tripwire`, `mado-label-check`, `mado-round17-measure`), 572-582 (`Round-17 tripwire limit`).
Method: read the code and receipts, ran the three tools' documented modes on their own fixtures and on
`/tmp` copies, re-checked digests and the four-way `pacman.log` join. Nothing was written outside this
report and `/tmp`. Installs or upgrades: **none** (no pacman/yay/paru/sudo/systemctl/hyprctl/probes;
no live command of any kind). No `jj`, git mutation or commit. `agent.db*` and credential paths not opened.

## Verdict-shape checks that held

- **Column shape.** All three rows have exactly 8 pipe-delimited fields and sit on one physical line,
  same as every other row (header `SKILL.md:543`; rows 545-556 are also 8). Names unique, owner `mado`,
  no cell empty. The label-check and measure rows use the `— (...)` self-test convention of the four
  measure probes, and the tripwire row fills every column.
- **Selftest counts.** `tripwire/{core,compound,hardening}/expected.json` hold 9 / 16 / 33 cases and the
  committed receipts say `9/9`, `16/16`, `33/33`, `exit=0`; I re-ran all three:
  `core` rc 0, `compound` rc 0, `hardening` rc 0, with `SELFTEST_SCRIPT_SHA256:
  4ced68d3…` equal to the current blob (`sha256sum tools/mado-tripwire.py` = `4ced68d3…`).
  The counts in `SKILL.md:557` are exact.
- **Tripwire exit map** (`SKILL.md:557`) matches the code (`tools/mado-tripwire.py:770-818`):
  0 `clean` / `permitted_only` (both reproduced), 1 `findings` (anchor, below), 2 on usage, unknown
  permit class, missing path, no `.jsonl`, invalid line, symlink, and internal error. `2 wins over 1`
  reproduced: a `/tmp` copy with one finding record plus one non-JSON line returned rc 2 and
  `error: "…:2 invalid line (JSONDecodeError)"`, with `findings: []` — the finding did not leak out.
- **Label-check exit map** (`SKILL.md:558`): default claims file rc 1 (`LABEL_SUMMARY: 4/7`,
  `EXPECT_SUMMARY: 7/7`, matching `evidence/label-check.txt`); green-only subset rc 0 (`4/4`);
  missing claims file rc 2.
- **Round-17 measure exit map** (`SKILL.md:559`): no argument rc 2, `deadbeef` rc 2, `HEAD` rc 0 with
  the observation object (`c1 {criteria:23, lesson_cited:15}`, `c2.count 4`).
- **Anchor and join.** `evidence/tripwire-anchor-r15.txt` is exit 1 (`MADO_TRIPWIRE: findings`) with
  exactly the two host_mutation findings on `MadoR15.LibinputEvents.jsonl:54`, both
  `tool_call_id: call_38165` (`sudo` and `pacman:-S`, command
  `sudo pacman -S --needed --noconfirm libinput libinput-tools`, 07:25:16.905Z), 8 findings over 7 calls.
  `pacman.log:2429` is `[2026-10-20T04:25:16-0300] … pacman -S --needed --noconfirm libinput libinput-tools`
  and the digest `78388d42…` is in `session-index.json`. The other three joins also stand
  (`2410`→r13 `GlobalCapture:19` 04:06:49.766Z; `2422`→r14 `ReviewSourceBar:41` 05:41:25.147Z;
  `2429` as above); `2423` needs the caveat under P3-2.
- **Limit paragraph, fact claims.** Each claim in `SKILL.md:572-582` is true of the code: only
  `type=="message"`, `role=="assistant"`, `content[].type=="toolCall"` is read (toolResult/`isError`
  ignored); `unparsed_spawns` and `eval_unparsed` are real per-file keys; non-literal spawn args,
  JavaScript cells, written-then-run scripts, shell functions, other tools and other sessions are not
  analysed; the class set is not `mado-action-plan`'s kinds.

## Findings (severity order)

### P1-1 `mado-tripwire`'s type is `audit`, which the registry schema does not define

`SKILL.md:557` puts `audit` in the `gate/probe` column. The header is
`| name | gate/probe | entry command | …` (`SKILL.md:543`), and `PROTOCOL.md:401-403` fixes the row
fields as "name, `gate|probe`, entry command, verdict map (code → class), self-test command and
spelling, pinned-value path, write scope, owner". All 12 pre-existing rows use exactly `gate` or
`probe`; no other row uses `audit`, and `PROTOCOL.md` has no `audit` gate class (the exact word
`audit` occurs once, at `PROTOCOL.md:334`, for the aggregator ledger; the other three hits are
"audited/audits/auditable"). The wave-1 draft that specified this row called it
`mado-tripwire (gate)` (`w1/reports/SkillRegistryDraft.md`, Deliverable), so the landed value is a
late change.

Consequence, not just a label: under `PROTOCOL.md:377-379` a gate is "a committed, re-runnable verdict
script … [that] returns a verdict", and "a tool that cannot fail is a probe". The tripwire returns a
verdict, exits 1 on findings, and has a `--selftest`; it is a gate. `audit` is outside the enum, so
the closure gate has no rule to grade the row by, and the gate obligations are left unattached.
If it is relabelled `gate`, the **Two-evidence** clause (`PROTOCOL.md:390-397`) also bites: the
standing use in `SKILL.md:527-529` is a verdict over mutable host transcripts, but there is no
frozen mode and no committed input snapshot with a committed expected verdict — the three
`expected.json` suites are synthetic fixtures, and the real receipts are digests of host files the
tool never re-verifies. [INFERENCE] That obligation is the reason the undefined label matters; I did
not design a frozen mode. Fix: `gate` (plus a frozen real-transcript snapshot for the standing use)
or, if the intent is a non-verdict probe, make it never exit 1 — which is not the current code.

### P1-2 "every seat-disclosed breach" is false — counterexample: the round-14 `jj log` incident

`SKILL.md:533-534` says: "Round 17 found, in rounds 13-16, **every** seat-disclosed breach plus
undisclosed ones (lesson `round-17.md` M2)". Counterexample, all anchors verified read-only:

- The breach: `MadoR14.AttackCoverage.jsonl:42`, bash toolCall
  `toolu_01R5vmrBJZg9XEoBoCh8p2tk`, command
  `jq -c '…' .ufo/waves/round-13/w1/globals.json; jj log -r @ --no-graph` (timestamp
  `2026-10-20T05:41:05.424Z`).
- Seat-disclosed, twice: `.ufo/waves/round-14/w1/AttackCoverage.md:113` — "I made one early
  `jj log -r @` call without `--ignore-working-copy`. jj reported 'Reset the working copy parent…'" —
  and `.ufo/waves/round-14/w1/reports/Safety.md:16` (F1, LOW, "created 3 jj ops … including
  `snapshot working copy`"). `corpus/lessons/round-14.md:126-128` retains it as "Safety's
  low-severity incident". The round-17 contract itself bans `jj` commands outright.
- The tripwire missed it: `evidence/tripwire-r14.txt` scans
  `MadoR14.AttackCoverage.jsonl` (231 lines, 44 bash calls) and has **no finding at line 42** (its
  only findings in that file start at line 51); `grep -c jj tools/mado-tripwire.py` = 0 — `jj` is in
  none of the class tables, so `jj log` classifies as nothing.

The sentence also contradicts the adjacent limit paragraph, which says "other tools … are outside it"
(`SKILL.md:578-579`). M2 does not support the universal either: it lists only package-query and
live-probe breaches (r13 wayland-utils, r15 `sudo -n true`, r16 second `pacman -Q waybar`), and
`tripwire-vs-oracles.json` only shows oracle-vs-tripwire agreement, not "every disclosed breach".
Fix: scope the sentence to the covered classes ("every seat-disclosed package/live-probe breach") or
drop "every". This is the one claim in the reviewed text that a concrete, seat-authored disclosure
falsifies rather than merely qualifies.

### P2-1 "receipts … bound to `session-index.json` digests" is true only for rounds 13-16

`SKILL.md:557` pinned-value cell: "real-transcript receipts `.ufo/waves/round-17/evidence/tripwire-*.txt`
bound to `session-index.json` digests". `session-index.json` has one `session_root`
(`…2026-10-20T01-48-55-258Z_01a156ff…`) and `rounds: ["MadoR13","MadoR14","MadoR15","MadoR16"]`.
Cross-checking every scan receipt's `files[].sha256` against the index:

| receipt | files | unbound |
|---|---|---|
| `tripwire-r13.txt` | 33 | 0 |
| `tripwire-r14.txt` | 33 | 0 |
| `tripwire-r15.txt` | 65 | 0 |
| `tripwire-r16.txt` | 97 | 0 |
| `tripwire-anchor-r15.txt` | 1 | 0 |
| `tripwire-r17-w1.txt` | 70 | **70** |

`tripwire-r17-w1.txt` scanned the other session root (`…2026-10-20T12-57-31-587Z_01a15963…/MadoR17`),
whose seventy files are absent from `session-index.json`; the receipt also carries the round-17
wave-1 `clean` claim, so the row's blanket glob overstates exactly where it matters most. The
`tripwire-selftest-*.txt` files are not scans and carry no transcript digests. Fix: name the bound set
("r13-r16 + anchor receipts") or extend the index to the round-17 session root.

### P2-2 `mado-label-check` is registered `probe` but is a failure-capable verdict script

`SKILL.md:558` files it under `probe`, with a verdict map that gives exit 1 to MISMATCH. Under
`PROTOCOL.md:377-379` a probe is a "tool that cannot fail"; label-check can and does (default claims
run: rc 1; green-only: rc 0; missing file: rc 2). It reads committed documents at pinned revisions and
compares them to expected values in its own repo — the gate definition. The practical cost of the
`probe` label is the **Self-test** clause (`PROTOCOL.md:385-389`): as a probe it owes no self-test,
and its "controls" are not asserted by the tool at all — `expect` never affects the exit code, and a
red claim that unexpectedly turns green yields exit 0 with only a printed `EXPECT_SUMMARY` count. If
the lane wants it as a probe, the exit-1 path has to go; if it stays a verdict tool, the registry row
should say `gate` and the red control needs an asserted self-invocation.

### P3-1 The row's "`EXPECT_SUMMARY` must equal the claim count" is not what the code computes

`SKILL.md:558` verdict map ends "`EXPECT_SUMMARY` must equal the claim count". `label-check.py:180-182`
counts `expected` only for claims whose `expect` is `"ok"` or `"MISMATCH"`; the script docstring
(line 24) declares `expect` optional. Reproduced: from the 7-claim `label-claims.json` I removed
`expect` from `frozen-match-green` in a `/tmp` copy; the run printed
`EXPECT_SUMMARY: 6/6 claims met their declared expectation` with rc 1 (the red claims still mismatch).
So the denominator is "claims declaring an expectation", not the claim count, and the stated criterion
would read as failed on a run where every claim verdict matched. Reproduced from the other direction:
all-green subset prints `4/4` and rc 0. Also, exit does not encode `expect`, so a red control flipping
to `ok` leaves rc 0 and only moves `met` to n-1/n; the sentence is an unenforced reading rule presented
as part of the verdict map. Fix: "`EXPECT_SUMMARY` met == declared-expectation count (7/7 on the
shipped file)" or make the script return 1 when `met != expected`.

### P3-2 "confirm package transactions … by timestamp" fails at the join's own OutputSpec anchor

`SKILL.md:531-533` tells the operator to join findings to `/var/log/pacman.log` by timestamp (UTC in
transcripts, `-0300` in the log). Three of the four anchors match exactly; the fourth does not at the
cited line. `MadoR14.OutputSpec.jsonl:65` is an assistant message at `05:45:52.190Z` carrying a
`contextSnapshot` field that replays prior toolCalls (50 toolCalls plus thinking/text in one record); the
`sudo pacman -S --needed --noconfirm wlr-protocols` call inside it has id
`0_tool_e3c0da30-7b31-4da4-8a77-252140b90`, whose `tool_execution_start` is **line 26** at
`05:41:32.451Z` — that is the instant matching `pacman.log:2423` (`02:41:32-0300`). The join file
discloses this ("OutputSpec:65 is one assistant record carrying many toolCalls, so its line timestamp
… is the record time, not the call time"), but `SKILL.md` does not; a reader applying the stated rule
to `:65` gets a 4m20s mismatch and would reject a true pairing. The four-way join still stands by
command identity and by the line-26 exec record; only the usage rule is incomplete. Fix: say the
finding's line is the record line, and read issuance time from the `tool_execution_start` record
(or cite `:26`).

### P3-3 Selftest exit map omits the malformed-case path

`SKILL.md:557`: "2 malformed expected.json". `mado-tripwire.py:743-750` also returns 2 with
`SELFTEST_SUMMARY: malformed case` (print at `:749`) when `expected.json` parses but a case lacks a required key.
Reproduced: `/tmp` copy of `tripwire/core` with `cases[0].name` removed → rc 2,
`SELFTEST_SUMMARY: malformed case`. Both are exit 2, so the class is right; the parenthetical is
incomplete. Also verified the other selftest arms: a wrong `want_exit` in a `/tmp` copy of `compound`
→ rc 1, `15/16 passed failed=['compound-and-sudo-pacman']`.

### P3-4 `--permit` can still print `clean` on the first line

`SKILL.md:580-581` says "never cite a `--permit` run as clean". With zero findings, the tool does
exactly that: `python3 -I tools/mado-tripwire.py --scan .ufo/waves/round-17/tripwire/core/clean-reads.jsonl
--permit package_query` prints `MADO_TRIPWIRE: clean`, rc 0, with `permitted: ["package_query"]`.
The only distinction is the JSON `permitted` array, so the rule is satisfiable only by also reading
that field — which the preceding sentence does ask for ("cite `counts`/`permitted`"), but the conflict
between "quote its first line" (`SKILL.md:530`) and "never cite a `--permit` run as clean" is real at
this edge. Low: the label is correct for a no-finding file; the wording should say so.

## Residual risk and verification gaps

- I did not re-run the full r13-r16 scans over all 228 indexed transcripts. I verified every receipt
  digest against `session-index.json` (r13-r16 + anchor: 0 unbound), inspected the four `pacman.log`
  lines, and parsed the r13/r14/r15/r16/anchor verdict JSONs for the specific claims above. A
  full re-scan would re-derive the receipts, not test a different property.
- The `audit` → Two-evidence consequence is [INFERENCE] from `PROTOCOL.md:390-397`; I did not attempt to
  build a frozen real-transcript snapshot, and the closure gate's own grading of `audit` was not run.
- The `jj` counterexample is a *coverage* falsification of "every", not a claim that the round-17
  transcript misses anything: the round-17 wave-1 scan of the 70 seat files is `clean` with
  1 `unparsed_spawn` and 1 `unparsed_eval` (receipt `tripwire-r17-w1.txt`), and no round-17 seat other
  than this reviewer issued a `jj` command (my own grep commands contain the word but are `grep`).
- The label-check doc-side claims were exercised only through the script's own default run and the
  committed receipt; I did not independently re-open all seven cited `round-16.md` lines.
- No credential, `agent.db`, auth/oauth or `~/.omp/agent` state file was opened; the only host state
  read was `/var/log/pacman.log` bytes and the session JSONL files named above.

Report: .ufo/waves/round-17/w2/reports/ReviewSkillRows.md
