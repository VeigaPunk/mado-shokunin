source: S487 — GNU Bash Reference Manual §3.2.3 Pipelines, https://www.gnu.org/software/bash/manual/html_node/Pipelines.html (held row, `corpus/SOURCES.md`; pin `.ufo/waves/round-84/fetch/bash-pipelines.html`, sha256 `b5629f04ccf5fe711d1b30f5dd4d8cf67dc6ab836d413292cd15c870a662059a`, lines 121–124) · S488 — POSIX.1-2024 Shell Command Language §2.9.2 Pipelines, https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html (opened this round; pin `.ufo/waves/round-85/fetch/S488.bin`, sha256 `0889867a53fe12508a71e8739ec23ecdddc95e6f67697c98e26acc8ff0ec1acd`, 357,953 B; the located quote and its byte offsets are recorded in the round-85 pins file `.ufo/waves/round-85/fetch/source-pins-r85.json`, key `S488`) · S489 — GNU Bash Reference Manual, maintainer copy (Edition 5.3, 2025-05-18) §3.7.5 Exit Status, https://tiswww.case.edu/php/chet/bash/bashref.html (opened this round; pin `.ufo/waves/round-85/fetch/S489-alt-tiswww.bin`, sha256 `b91026acffb159bd1e842e3116a95539bf858e2b57cbfa74df9e3a53379177a4`, 1,040,870 B; the located quote and its byte offsets are recorded in the round-85 pins file `.ufo/waves/round-85/fetch/source-pins-r85.json`, key `S489-alt`) · the lane's own frozen population `.ufo/waves/round-85/controls/c2-cases-r85.json` (sha256 `de8a68fe22799d4bf8366ab56c9d390559260dc8a70c3d1d7e0d03da98d23b64`, 36 rows, byte-identical to the freeze) and its carried set `.ufo/waves/round-84/controls/c2-runbook-cases-r84.json` (sha256 `2e86b4b64b7b7b95fcfdb78e2463762a8f8dc7a299145a992170fdc59d4b5efe`, 33 rows) · the three contained producers `.ufo/waves/round-85/fixtures/status-{ok,exit7,sigpipe}.sh` (sha256 `22fa614f…`, `4118869d…`, `f8bf27bc…`) · the instrument `quality/counters/c2-r85-status-classes.py` (frozen sha256 `e689438131a633317799377065b84dd54afcb5ba90de1a1dcd67fdf58043f471` at the freeze, successor sha256 `b4bde359f66804cf9b982e40bbdf8d4bc6c9baa283378f9f1448b3aff82b111c`)
verified-at: 2026-11-04; instrument freeze `3905311c75a39c5710413105865c0a1a7dd0116a`; successor `d7c40e6d1b9a7476f2ff48254d577799ce9901e4`; the frozen C2 claim did **not** verify (see § Measured outcome)
recheck: python3 -I quality/counters/c2-r85-status-classes.py --repo . --rev REV --controls .ufo/waves/round-85/controls/c2-cases-r85.json --carried .ufo/waves/round-84/controls/c2-runbook-cases-r84.json --scratch-root DIR

# A runbook row's status class is a claim about propagation, not about truth

## The three status classes

Every frozen case carries status metadata. Ordinary kinds check it before outcome shape;
seven specialized state/refusal rows bypass it and retain their own status-pair semantics.
The metadata lives in the control JSON, not an authenticated Markdown status cell.
See the retained bypass counterexamples below; the frozen universal claim did not verify.

| class | bound status | rule in the instrument | a frozen row |
|---|---|---|---|
| `ok` | exit 0 | `rc == 0` (`:352-353`) | 33 carried rows plus `status-ok-contained` (`.ufo/waves/round-85/controls/c2-cases-r85.json:1466-1498`) |
| `exact` | one **named** nonzero exit code | `rc == status["code"]` (`:354-355`) | `status-exit7-contained`, `code 7` (`:1500`, class at `:1511-1512`) |
| `signal` | expected Bash encoding `128+N`, not authenticated termination cause | `rc == 128 + status["signal"]` (`:356-357`) | `status-sigpipe-contained`, `signal 13` (`:1539`, class at `:1550-1551`) |

The class is never "any nonzero". Measured against the frozen counter's own `status_ok`
(`:345-358`): `ok` accepts 0 and refuses 3; `exact` code 7 accepts 7 and refuses 141; `signal` 13
accepts141. These observations distinguish numeric0,7,141 in the contained fixtures,
not normal exit from signal death at the same encoded number. Explicit exit141 passes the
same matcher. The round84 ordinary rule (`:328`, `if rc != 0: return False`) cannot accept
the two new nonzero-positive ordinary cases, giving a bounded status-propagation distinction.

## A guarded pipeline exposes failure that an ordinary tail masks

Without pipefail or leading negation, the pipeline status comes from its last command.
S488 pins this from POSIX.1-2024 §2.9.2 Pipelines — the located quote is the default-off table row
(`.ufo/waves/round-85/fetch/source-pins-r85.json:38`, pin bytes 133030–133104):

> The exit status of the last (rightmost) command specified in the pipeline.

POSIX Issue 8 also defines the option that changes this, in the same pinned document: the `set`
builtin's `pipefail` entry reads "Derive the exit status of a pipeline from the exit statuses of
all of the commands in the pipeline, not just the last (rightmost) command" and points at
2.9.2 Pipelines. The held S487 row carries the same rule from the Bash manual (pin lines 121–124:
"If pipefail is enabled, the pipeline's return status is the value of the last (rightmost) command
to exit with a non-zero status"). So `set -o pipefail;` in front of a pipeline is not a stylistic
choice: without it the consumer's status is the only status the runbook can see.

The no-work control is committed and the claim is measured, not argued
(`.ufo/waves/round-85/receipts/control-c2-r85-unguarded.txt`): the same three producers, once
unguarded and once guarded.

| contained producer | what it does | unguarded pipeline status | guarded pipeline status |
|---|---|---|---|
| `status-ok.sh` | prints `MADO_STATUS: ok`, exits 0 | 0 | 0 |
| `status-exit7.sh` | prints `MADO_STATUS: exit7`, exits 7 | **0** | **7** |
| `status-sigpipe.sh` | writes 20,000 lines; its reader stops at line 1, so it dies of SIGPIPE | **0** | **141** |

Re-measured in this seat's scratch with the committed fixtures and the same commands: the
unguarded forms report 0 for all three, the guarded forms report 0, 7 and 141. Without the guard
the exit-7 producer and the SIGPIPE producer are **indistinguishable from a success**, and no
amount of text matching recovers the erased status: `MADO_STATUS: exit7` is printed by a producer
that failed, and `MADO_STATUS: sigpipe line 0` is printed by a producer that died. This is the
same masking the round-84 control recorded (`receipts/control-c2-r84-unguarded.txt`: producer exits
7, pipeline status 0, stdout `b true`) and the reason round 84 introduced the guard.

Two properties of the `signal` row are worth keeping in view, because they are properties of the
*pipeline shape*, not of the producer script. First, the 141 appears only because the reader
closes the pipe early: `set -o pipefail; sh status-sigpipe.sh | head -n 1` reports 141, while the
same producer piped to `cat` — which drains it — reports 0 (measured). Second, the 141 is
**Bash's** encoding, not a POSIX guarantee: S489 (pin bytes 239046–239200,
`.ufo/waves/round-85/fetch/source-pins-r85.json:145`) reads

> When a command terminates on a fatal signal whose number is N, Bash uses the value 128+N as the exit status.

POSIX's own words are weaker (S488 pin bytes 109001–109128, `.ufo/waves/round-85/fetch/source-pins-r85.json:47`): "if the
command terminated due to the receipt of a signal, the shell shall assign it an exit status
**greater than 128**", and the standard says the exit status identifies the signal only "in an
implementation-defined manner". The frozen declaration's phrase "reported by a POSIX shell as
128+N" over-claims it; the successor instrument's own docstring says so (`:344-348`).

## The line-anchored pattern rule for the two version rows

The two version rows (`version`, `.ufo/waves/round-85/controls/c2-cases-r85.json:13-47`, and
`omarchy-version`, `:444-486`) declare `"anchor": "line"` (`:47` and `:486`) and carry a full-line
pattern as their `value`. The instrument implements the anchor as a separate matcher
(`:361-368`): the pattern must match one **complete** line of the output, never a prefix of one.
Measured: `line_anchored(r"^[0-9]+$", "1720")` is true, `line_anchored(r"^[0-9]+", "1720x")` is
false, and on multi-line output the anchored matcher accepts a match on a **later** line while a
plain `re.search` of the same text does not.

What the anchor buys, and what it does not, is a distinction the frozen population does not draw.
The frozen `version` value is itself a full-line pattern (`:43`,
`^Hyprland [0-9]+\.[0-9]+\.[0-9]+ built from branch \S+ at commit [0-9a-f]{7,40} clean \([^)]*\)\.$`),
so a plain `re.search` of that value already refuses the frozen text-extension negatives
("… trailing", "… EXTRA") — measured: the frozen value refuses both, while the round-84 value
`^Hyprland [0-9]+\.[0-9]+\.[0-9]+ ` accepts both. The `omarchy-version` value is likewise
end-anchored (`:482`). Consequently the two declared anchor mutants — `regex-anchor-dropped` and
`line-anchor-prefix` — are **not discriminated** by this population and survive it; see § Measured
outcome and `corpus/lessons/round-85.md` M85-4. The line-anchored rule is a real rule with a
weaker effect than the declaration's "so a prefix extension is not accepted" implies: on this
population the refusal comes from the pattern's own end anchor, not from the anchor clause.

Two further facts about the anchor's reach, both measured on the frozen counter:

- the anchor clause binds a match on *any* line of the output, so a multi-line output whose first
  line is wrong but whose second line matches is accepted by the anchored matcher and refused by
  plain `re.search`;
- the anchor clause is only consulted for rows that declare it. The SKILL table's own outcome and
  status **cells** are not read by the counter at all — only the command cell is bound to a case
  (`:761-782`). Measured: in a scratch clone of the successor, replacing the status and outcome
  cell of all 36 documented rows with junk strings still yields
  `cases=36 executed=36 matched=36 shapes=26/26 anchors=36/36 rows=36/36 … verdict=MUTANTS_SKIPPED`
  (exit 0). The authoritative class is the one in the frozen control, not the one printed in the
  table.

## What a status class does and does not establish

- **It establishes propagation.** That the runbook's command reached a producer, and that the
  producer's own exit status reached the matcher unchanged by the pipeline. That is the whole
  content of the class, and it is worth the guard it costs.
- **It does not establish payload honesty.** `status-exit7.sh` prints `MADO_STATUS: exit7` — a
  payload as plausible as the success payload — and then exits 7; the class is what tells the two
  apart. A row whose payload asserted "everything is fine" and whose producer exited 0 would be
  scored `ok`. The round-84 producer did exactly this (`b true`, then exit 7) and the round-84
  control caught it only because the guard exposed the status.
- **It does not establish tray health.** The tray rows bind the shape and the exit status of a
  `busctl` read. A status class of `ok` on `tray-owner` says the query succeeded, not that a tray
  icon is drawn, not that the host is registered, and not that the compositor is healthy. Nothing
  in this note is evidence about rendering.
- **`sh` vs `bash` pipefail support is a host property, measured separately.** The rows execute
  `/bin/sh -c "set -o pipefail; …"`. POSIX.1-2024 defines `pipefail` (S488), but a host's `/bin/sh`
  need not be a shell that implements it, and "the word `sh`" is not a measurement. On this host
  `/bin/sh` resolves to `/usr/bin/bash` (GNU bash 5.3.20) and `set -o pipefail` is accepted
  (measured). The lane establishes host support by the contained fixture rather than by the
  shell's name, exactly as S487's registry row records ("host support is separately measured").
- **The fixtures are contained and no host producer is made to fail.** The three round-85 fixtures
  print to stdout and exit; none writes a file, reads desktop state, or calls a session service.
  The SIGPIPE fixture's death is caused by the runbook's own reader (`head -n 1`) closing the pipe
  — the fixture is not asked to fail, and no host producer is broken to make the row pass. The
  round-84 fixtures work the same way (`fixtures/pipefail-guard.sh`,
  `fixtures/failing-producer.sh`).

## Measured outcome — the frozen claim did not verify, and the successor is not a green gate

**At the freeze revision the instrument refuses before running a row.** Re-measured in a clean
scratch archive of `3905311c`: the counting command exits **2** with
`MADO_R85_RUNBOOK: ERROR (stage=setup carried case 'version' changes field 'negatives')` — the
frozen carried-field comparison did not exempt the very `status`/`negatives` additions the
declaration permits (`:730-737`). Independently, the frozen `SKILL.md` carries the heading
`### Executable runbook rows (round 84)`, so the counter's row extractor finds **0** rows under the
round-85 heading it requires, and 33 under the round-84 heading (measured). The frozen C2 claim is
**unverified**; see `corpus/lessons/round-85.md` M85-7 and
`.ufo/waves/round-85/receipts/independent-score-r85.txt` (Run B1).

**At the successor revision the rows all match, and four of the thirty-seven declared mutants
survive.** Measured here from a clean scratch archive of `d7c40e6` (identical to the lane's own
re-execution receipt, `.ufo/waves/round-85/receipts/independent-score-r85.txt` Run B2/B3):

```
MADO_R85_RUNBOOK: cases=36 executed=36 matched=36 shapes=26/26 anchors=36/36 rows=36/36
  superseded=<sixteen names> mutants=37 killed=33 verdict=TARGET_MISSED rev=d7c40e6d… tree=bound
```

exit code **1**. The four survivors — `regex-anchor-dropped`, `line-anchor-prefix`,
`negatives-skipped`, `samples-skipped` — each score 36/36 with the mutation applied
(`.ufo/waves/round-85/w1/R85ReviewerC2.md` reaches the same four by an independent route).
`shapes=26/26` counts the 26 cases whose kind is in the counter's shape list
(`:185-187`); it is not a count of 26 distinct grammars. **No admission is claimed here**: this
note records the rule and its measured limits, and the round's C2 claim stays an honest stop
(`corpus/lessons/round-85.md`, M85-4 and the round's end-measurements section).

## Limits and rejected interpretations

- **A numeric 141 does not prove death by signal 13.** The instrument's own `status_ok` accepts
  rc 141 for `exact` code 141 as well as for `signal` 13 (measured), and an explicit `exit 141`
  returns the same number — the rejected registry row S490 says so from the `exit` builtin's own
  wording ("Exit the shell, returning a status of n to the shell's parent", bytes 266270–266361 of
  the pinned `S489-alt-tiswww.bin`). **Flip:** separately observed termination metadata that
  distinguishes a normal exit from a signal death.
- **`128+N` is Bash's encoding, not a POSIX-wide guarantee.** POSIX says only "greater than 128"
  and leaves the signal identification implementation-defined. A POSIX-conforming shell may encode
  a signal death differently; the `signal` class as written is a Bash-host fact. **Flip:** a
  normative POSIX sentence fixing the encoding, separately opened and scoped.
- **"The last command's status is the pipeline's status" is the default, not a universal.** It is
  the `pipefail` **disabled** row of the POSIX table; with `pipefail` enabled the status derives
  from the commands of the pipeline, and with a leading `!` it is the logical negation of that
  command's status. A note that says "a pipeline's status is the last command's status" without
  naming the option is stating the default as a law.
- **Seven rows do not go through the status gate at all.** The counter's specialised kinds —
  `refusal` (the four `refuse-*` rows), `producer_failure`, `is_active` and `pid_state` — are
  scored on their own exit-status pair before the class is consulted (`:481-508`), while the
  control declares `status: {class: ok}` for all seven. Measured: the refusal kind accepts rc 3,
  `is_active` accepts rc 3 with `inactive`, `pid_state` accepts rc 1 with empty stdout, and
  `producer_failure` accepts rc 7 — all under a declared class of `ok`. So "ok means exit 0" holds
  for the ordinary rows, not for these seven; their status is a *pair* (state word and status).
  The committed successor table (`d7c40e6`, `SKILL.md:281-284`, `:287`, `:289`, `:296`) still
  prints `ok` for them; the lane's in-progress working-tree correction relabels those seven cells
  "legacy status pair" and rewrites the `signal` row's cell as "13 → 141 (encoded)" with the
  outcome "numeric141 with `MADO_STATUS: sigpipe line 0`; explicit exit141 is observationally
  equivalent" (`SKILL.md:281-299`, working tree, uncommitted at the time of writing). Both
  directions of that correction say the same thing this note says: the class is a *number*, not a
  cause.
- **The declaration's source locators are off by a section in both cases.** The declaration names
  "POSIX.1-2024 XCU §2.9.3 *Pipelines*" and "GNU Bash Reference Manual §3.7.6 *Exit Status*"; the
  pinned POSIX page anchors Pipelines as **2.9.2** (2.9.3 is *Lists*) and the reachable Bash
  maintainer copy numbers Exit Status **3.7.5** (3.7.6 is *Signals*). The declaration's GNU URL for
  S489 was unreachable in five attempts (TCP connect timeout) and was **not** pinned; the
  maintainer copy was opened instead and is what S489's registry row points at. The declaration is
  frozen history and was not rewritten (`corpus/lessons/round-85.md` M85-8).
- **The frozen population does not distinguish the anchor clause.** Both version values have
  their own string anchors; the Hyprland value also constrains its final parenthesized text.
  Plain search therefore refuses the same trailing-extension negatives. Dropping the separate
  line-anchor rule survives the frozen set, so those refusals do not independently certify
  the line-anchor mechanism.
- **A status class says nothing about the producer's payload, the host's health, or the tray.**
  Nothing in this note is evidence of rendered UI, of a working notification host, or of a
  repaired unit; OS diagnosis stays with tsukuroi and the mutation/testing method with tameshi.
