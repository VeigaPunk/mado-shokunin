# SkillRegistryDraft — SKILL.md gate registry, round 18

Draft only. L1 owns `SKILL.md`; L1 applies these rows. Column shape is the
eight-column shape of `SKILL.md:548` (`name | gate/probe | entry command |
verdict map | self-test command / spelling | pinned-value path | write scope |
owner`). No `|` appears inside any cell.

## A. Replacement for `SKILL.md:562` (`mado-tripwire`, moves probe to gate)

| name | gate/probe | entry command | verdict map | self-test command / spelling | pinned-value path | write scope | owner |
|---|---|---|---|---|---|---|---|
| mado-tripwire | gate | frozen (gate entry): `python3 -I tools/mado-tripwire.py --frozen .ufo/waves/round-18/frozen-tripwire` (digest-pinned replay of committed transcript-line snapshot); scan (post-hoc entry): `python3 -I tools/mado-tripwire.py --scan PATH [PATH ...] [--permit CLASS ...]` (post-hoc scan of OMP session JSONL; assistant `toolCall` bash commands and python eval `!`/`%%bash`/literal spawns only) | frozen: 0 `frozen_match` (exit, label and the exact (file, line, class, rule) multiset plus known_misses agree with the pin); 1 `frozen_verdict_mismatch`; 2 `snapshot_tampered` (digest mismatch, symlink, absolute or `..` path, missing or unlisted `*.jsonl` input) or `unpinned_legacy` (input entry without sha256) or `frozen_error` (expected.json unreadable, not an object, missing key, bad type or wrong schema); other could-not-evaluate. scan: 0 `clean` (no finding) or `permitted_only` (every finding waived); 1 `findings` (at least one unpermitted host_mutation/package_query/live_probe finding); 2 could-not-evaluate (usage, refused symlink/`agent.db`/credential name, unreadable, no `.jsonl`, invalid line, internal error); 2 wins over 1 | `python3 -I tools/mado-tripwire.py --selftest .ufo/waves/round-17/tripwire/core` (9), `…/compound` (16), `…/hardening` (33), `…/w2-regressions` (30), `.ufo/waves/round-18/tripwire/frozen` (`N` cases, count from its expected.json at landing); known misses pinned in `.ufo/waves/round-17/w2/adversarial` (4/26 by design); 0 all pass, 1 any fail, 2 malformed expected.json; scan cases self-invoke `--scan` and compare exit plus the exact (class, rule, line[, file]) multiset; `mode: frozen` cases (`want_label` required) self-invoke `--frozen <DIR>/<args[0]>` and compare exit and the first-line outcome, `want_findings` ignored | frozen: `.ufo/waves/round-18/frozen-tripwire/expected.json` (pins every input sha256, `permit`, `expected_exit`, `expected_label`, `expected_findings`, optional `known_misses`); scan: rules in `tools/mado-tripwire.py` (class tables at the top); real-transcript receipts `.ufo/waves/round-17/evidence/tripwire-*.txt` bound to `session-index.json` digests | frozen reads only the pinned `DIR/inputs` snapshot in-process, never the source transcripts; scan reads only the given JSONL files; both write nothing | mado |

Round-18 frozen limit (append under the round-17 tripwire limit paragraph,
`SKILL.md` after `:587`): `frozen_match` means the committed snapshot replays
to the pinned verdict. It never means the source transcripts still exist, that
the scan of the live session is clean, or that no host command ran outside the
covered forms. The verdict's `tool_sha256` is printed as provenance; the pin
binds inputs, not the tool digest. The round-17 scan limits stand unchanged.

## B. New probe rows (insert after `SKILL.md:564`, `mado-round17-measure`)

| name | gate/probe | entry command | verdict map | self-test command / spelling | pinned-value path | write scope | owner |
|---|---|---|---|---|---|---|---|
| mado-receipt-check | probe | `python3 .ufo/waves/round-18/receipt-check.py [CLAIMS]` (default claims file `.ufo/waves/round-18/receipt-claims.json`; checks each receipt's `tool_sha256` against `git show <measured_commit>:<tool>`) | 0 every claim meets its `expect` (`ok`, `MISSING_PROVENANCE` or `SHA_MISMATCH`); 1 any claim misses its `expect`; 2 could-not-evaluate (usage, unreadable claims file, `git show` failure); `EXPECT_SUMMARY: k/n` printed | — (seed red and green claims in `.ufo/waves/round-18/receipt-claims.json` are its controls) | `.ufo/waves/round-18/receipt-claims.json`; receipt `tool_sha256=` and `measured_commit=` header fields (or JSON keys) | reads receipts and tools via `git show` at each claim `rev` only; writes nothing | mado |
| mado-fetch-verify | probe | `python3 .ufo/waves/round-18/fetch-verify.py [--sources corpus/SOURCES.md --rows S072,S073,...] [--quote 'S072=<text>']` (walks `.ufo/waves/round-18/fetch/*/receipts.jsonl`; checks body presence, byte count and sha256) | 0 every fetch receipt ok and every listed row receipted; 1 any `BAD_SHA`, `BAD_BYTES` or `MISSING` fetch, or any `UNRECEIPTED` row; 2 could-not-evaluate (usage or unreadable input) | — (tested by its author on `/tmp` fixtures; no committed selftest) | `.ufo/waves/round-18/fetch/<seat>/receipts.jsonl` and bodies; row join against `corpus/SOURCES.md` when `--sources` is given | reads receipts, bodies and the SOURCES file; writes nothing | mado |
| mado-pipe-rc-census | probe | `python3 .ufo/waves/round-18/pipe-rc-census.py REV` (static scan of `tools/*.sh` at `REV` via `git show`; flags command substitutions that pipe a producer into sha256sum, wc or cut and assign the result without capturing the producer status) | 0 no `unchecked` site; 1 at least one `unchecked` `SITE` (at `d9a5a18` this must flag `tools/mado-verify.sh` near `:3406`); 2 could-not-evaluate (usage or `git show` failure) | — (red control: `REV d9a5a18` must flag `tools/mado-verify.sh` near `:3406`) | none; per-site hazard judgement recorded in the round-18 report | reads committed bytes via `git show` only; writes nothing | mado |
| mado-measure-mutants | probe | `python3 .ufo/waves/round-18/measure-mutants.py` (builds a `/tmp` git repo from `git archive d9a5a18`, applies one minimal mutant per round-17 rubric-V tightening and runs the round-17 measure instrument on each) | 0 every mutant caught by the instrument; 1 any mutant survives (the instrument still credits it); 2 could-not-evaluate (archive, measure or mutant-application failure) | — (the mutant set is its own control; each mutant must be shown able to fail) | `.ufo/waves/round-18/evidence/measure-mutants.json` (written result); rubric-V tightenings named in `SCORECARD.md` "Round-17 pre-measurement corrections" | writes only `/tmp` scratch and `.ufo/waves/round-18/evidence/measure-mutants.json` | mado |
| mado-frozen-provenance | probe | `python3 .ufo/waves/round-18/frozen-provenance-check.py` (re-extracts each `provenance.json` mapped source line from its original transcript, read-only, and compares bytes with the snapshot line; verifies source sha256 against `session-index.json`) | 0 every mapped line and source digest equal; 1 any line or digest differs; 2 could-not-evaluate (e.g. source transcript no longer present, in which case the snapshot is the only copy) | — (no committed selftest; `/tmp` fixtures are its author's controls) | `.ufo/waves/round-18/frozen-tripwire/provenance.json`; `.ufo/waves/round-17/evidence/session-index.json` | reads snapshot, provenance, session index and listed source transcripts read-only; writes nothing | mado |

## C. Notes for L1 (not registry text)

1. Exit maps for `mado-receipt-check`, `mado-fetch-verify`,
   `mado-pipe-rc-census`, `mado-measure-mutants` and `mado-frozen-provenance`
   are transcribed from the round-18 seat specifications. They must be
   reconciled against each landed script's header and `--help` before
   `SKILL.md` is edited. Any divergence wins over this draft.
2. `mado-tripwire` self-test count for `.ufo/waves/round-18/tripwire/frozen` is
   a placeholder until `TwFrozenSelftest` lands its `expected.json`; read the
   count from the file, do not carry it from this draft.
3. The mado-verify `OM` scenario that the pipe-rc fix needs is a gate change,
   not a probe row; it is outside this draft.
4. Insert B after line `:564`; apply A in place of line `:562`. Both preserve
   the eight-column header at `:548`.
