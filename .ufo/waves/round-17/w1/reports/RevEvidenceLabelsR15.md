# Round-15 receipt-label audit — does every cited receipt carry the token the sentence attributes?

Seat: `MadoR17.RevEvidenceLabelsR15` (reviewer, leaf). Advisory; no integration, no verdict
on round 15's admission, no lane mutation.

Scope: `corpus/lessons/round-15.md` (sha256 `634228b9cbd8d88e2a9f07bedbb94f77e352e95fae003fbe74aac5947c504127`,
200 L) and `SCORECARD.md` §"Round 15 — committed measurement and honest-stop verdict"
(lines 624–689; file sha256 `5b05d23cec8fd5a521e81bc8594ab41dad1109c76241c89fb3998267146793f3`).
Round-15 declared-claim section (598–622) contains no receipt citation.

Method: read-only. `cat`/`grep`/`sha256sum` on `.ufo/waves/round-15/evidence/`,
read-only `git show` of `5f1387`, `9ebd737`, `32118fc`, `ea0446`, and `tail`-read of
`/var/log/pacman.log:2425-2445`. No pacman/yay/paru query, no sudo, no systemctl/hyprctl/
libinput, no service or compositor operation, no test/gate execution, no jj. No tool was
installed or updated.

**Headline: no round-15 citation attributes a verdict token that its named receipt does not
carry.** Every exit code, `finding_id`, count and digest quoted in the two scopes is present
verbatim in the named receipt or in the JSON that receipt consumes. This is materially
different from R16-V1 (round-16 l.131 cited `evidence/frozen-tampered.json` for
`snapshot_tampered` while that receipt records exit 2 `frozen_error`). Round 15's defects are
citation-precision and failure-branch coverage, not false token attribution.

## 1. Citation inventory and per-citation result

`D` = `.ufo/waves/round-15/evidence/`, `J` = `.ufo/waves/round-15/receipt-correction.json`.

| Sentence (exact location) | Cited receipt | Token the sentence attributes | Observed in receipt | Result |
|---|---|---|---|---|
| round-15.md:15 (M2) | `/var/log/pacman.log:2429-2437`; actor wave report | exact command; libinput 1.31.3-1→1.32.0-1; new libinput-tools 1.32.0-1, python-libevdev 0.13.1-1, python-pyudev 0.24.4-1, python-yaml 6.0.3-2 | log 2429 records the pacman argv verbatim (`pacman -S --needed --noconfirm libinput libinput-tools`; the `sudo` prefix is not a pacman.log field and comes from the actor report, as the row itself says); 2432–2436 exactly those five package events; 2437 `transaction completed` | match |
| round-15.md:15 (M2) | `D/install-guard-{red,green}.txt` | red: `already_installed_in_plan`, exit 1, overlap libinput; green: `new_only_plan`, exit 0 | red: `exit: 1`, `"finding_id": "already_installed_in_plan"`, `"overlap": ["libinput"]`; green: `exit: 0`, `"finding_id": "new_only_plan"`, `"overlap": []`; both `"fixture_only": true` | match |
| round-15.md:28-30 | `/var/log/pacman.log:2438-2439` (hooks) | udev-reload / system-update hooks | 2438 `35-systemd-udev-reload.hook`, 2439 `35-systemd-update.hook` | match |
| round-15.md:101-102 | census receipts under `D/` | (pointer only) | `census-before.txt`, `census-after.txt` exist there | match |
| round-15.md:167-168 | `D/{before,after}.txt` | complete stdout, exit 0 | both `exit: 0`; full JSON bodies present; before=ea0446, after=5f1387 | match |
| round-15.md:170-171; SCORECARD:642-643 | `D/census-{before,after}.txt` | exit 0; same three W04 S030/S042/S045 | both `exit: 0`; identical three `W04` lines naming S030/S042/S045 | match |
| round-15.md:171; SCORECARD:643-644 | `D/source-merge.txt` | exit 0, rows 52, collisions 0, errors 0 | `exit: 0`; `rows=52 … collisions=0 … errors=0` | match |
| round-15.md:172; SCORECARD:652 | `D/gate-selftest.txt` | 372/372, exit 0 | `exit: 0`, `MADO_SELFTEST: 372/372 assertions passed` | match |
| round-15.md:172-173; SCORECARD:653-654 | `D/gate-file-plane.txt` | 29 PASS / 0 FAIL / 0 UNKNOWN / 8 SKIP / 4 NOTE, exit 0 | `exit: 0`; `counts: pass=29 fail=0 unknown=0 skip=8 note=4` | match |
| round-15.md:174-175; SCORECARD:649-651 | measure + gate receipts | whole-gate SHA-256 unchanged `fba82a66…c207` | present as `gate_sha256` in selftest, file-plane, after, census-after, source-merge; `before.txt` carries it in `measure_inputs.gate_sha256`; both measure receipts `gate_executed: false` | match |
| round-15.md:180-184; SCORECARD:657-659 | `D/receipt-correction-{red,green}.txt` | red exit 1 `receipt_mapping_missing`; green exit 0 `receipt_mapping_verified`, mapped 3, problems [] | red: `exit: 1`, `"finding_id": "receipt_mapping_missing"`; green: `exit: 0`, `"finding_id": "receipt_mapping_verified"`, `"mapped": 3`, `"problems": []` | match |
| round-15.md:185-186; SCORECARD:660 | same two | target `cd1d73d7…`, 117602 bytes | green: `"bytes": 117602`, `"target_sha256": "cd1d73d7…"`; red: `"target_matches": true` | match |
| round-15.md:187-188 | same two + `J` | checks three original hashes / provisional headers / targets / false standalone-full-gate flags | `J.receipt_map` has 3 entries, `standalone_final_full_gate_receipt: false` ×3, per-entry `original_sha256`/`input_binding`/`provisional_gate_sha256`/`derived_target_sha256`; the three `original_sha256` equal the current `.ufo/waves/round-14/evidence/*.txt` digests; none of the three contains `measured_commit:` | match |
| round-15.md:192-194 | "The JSON" (unnamed) | `measured_commit_role` explicitly names static reference derivation | present in `J` (committed @5f1387, sha256 `b09d7e72…4f0f`), value "reference source revision for static target derivation; not the runtime revision of the three pre-commit mutation runs" — **absent from both cited `.txt` receipts' printed JSON** | token true, pointer missing (F2) |
| round-15.md:117; 195-197 | `D/wave-census.json`, `w1/dispatch.json` | 64-seat policy-v2 wave; one unchanged `taskCall`; role mix | census: `spawn 64 / resume 0 / total 64`, role counts 3/13/8/17/9/4/4/4/1/1 = 64, `optional_wave2:false`; dispatch: `taskCall {context, tasks[64]}`, `resumeSends: []`. **No `policy-v2` token in either file**; `dispatch.policy` is a bare limits object with no version field | 64-seat and taskCall match; `policy-v2` under-cited (F3) |
| round-15.md:195-197 | `D/source-bindings.txt` | source binds checkable | file exists; digests at its lines 4 and 7 equal the `SOURCES.md` S051/S052 `raw sha256` values | match; no exit code recorded (F5) |
| SCORECARD:628-633 | `D/{before,after}.txt` | "Both commands below actually ran, exit 0" | before receipt's `command:` equals line 631; **after receipt's `command:` is `python3 /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-15/measure.py …`, not the literal relative command on line 632** | literal-command mismatch (F1) |
| SCORECARD:637 | `D/{before,after}.txt` | U1–U5 5/7 7.1429 → U1–U6 6/7 8.5714; U6 S051/S052 joins, inverse, four facets | before `count 5, score 7.1429`; after `count 6, score 8.5714`; U6 join `mined: [S051,S052]`, `reserved` both true, `inverse: true`, facets `layer_ladder/safe_boundary/unexercised_delivery/delivery_unknown` all true | match |
| SCORECARD:639-641 | before/after + `SOURCES.md`@5f1387 | nav 28/28→29/29; sources 50→52; tiers 46/1/3→48/1/3; statuses 38/8/4→40/8/4; S007 stays queued | every number matches the receipts; S007 row status is `queued`; `git diff ea0446 5f1387 -- corpus/SOURCES.md` is additions only (two rows + prose), so "no existing registry mutable field changed" holds | match |
| SCORECARD:662-664 | `D/install-guard-{red,green}.txt` | red exit 1; green exit 0; static fixture evidence | as above; `fixture_only: true` in both outputs, and `input_provenance` calls green an in-memory control | match |
| SCORECARD:679-684 | `SHONEN.md`@5f1387; capability table | four `[~]`; no capability row | `grep -c '^- \[~\]'` → 4; capability table still `| — none yet — |` | match |

Supporting receipts verified but not named by either scope: `D/committed-bindings.json`
(all 7 digests recomputed at `5f1387` → 7/7 OK, including `J` = `b09d7e72…4f0f` and the gate =
`fba82a66…c207`); `D/source-bindings.txt` line 13 `cc860987…f5e07` equals
`sha256sum /usr/share/wayland/wayland.xml`, and its line 12 records `wayland 1.26.0-1`, which is
what round-15.md:90 asserts.

## 2. Findings, severity-ordered

No high-severity (R16-V1-class) mismatch was found.

**F1 — low: SCORECARD:628-633 literal command vs recorded command.**
The section says "Both commands below actually ran, exit 0" and prints the relative
`python3 .ufo/waves/round-15/measure.py <rev>` twice (lines 631–632). The receipt `D/after.txt:1`
records `python3 /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-15/measure.py
5f138704…`. Same script, same revision, same exit, so the measurement is not in doubt; the
sentence's "the commands below" is literally true only for the first line. A copy-paste
verification using the printed block reproduces the *before* receipt exactly and the *after*
receipt only by path equivalence.

**F2 — low: round-15.md:192-194 names a JSON token without naming the JSON.**
"The JSON's `measured_commit_role` explicitly names static reference derivation" is true of
`.ufo/waves/round-15/receipt-correction.json`, but neither cited receipt
(`D/receipt-correction-{red,green}.txt`, cited at line 189) prints that key, and no line in
round-15.md or SCORECARD:598-689 gives the JSON's path. A checker following only the cited
receipts cannot find the token; it must infer that the audit's input JSON is committed under the
wave dir. The claim itself is correct.

**F3 — low: round-15.md:117 "policy-v2" is not carried by any lane receipt.**
`D/wave-census.json` carries `wave`, counts and role mix, not a policy version;
`w1/dispatch.json` `policy` is `{source, maxLanes, minLanes, waveMinLanes, waveMaxLanes,
declaredMaxLanes, hardCeiling, rampBatchSize, rampIntervalMs, globalRunnerCeiling}` with no
version field; the dispatch schema is `ufo-swarm-wave-dispatch-v1`. The only support for
`policy-v2` is outside the lane: the round-15 fleet prompt's
`UFO_CONFIG_PATH=/home/vgpnk/Projects/shokunin/scripts/hyaku/ufo-wave-policy-v2.json`
(`.ufo/prompts/mado-round-15.md:176`) and the fleet report (`.ufo/reports/round-15/mado.md:15`).
The "64-seat" half of the sentence is receipted; the version label is not. Likewise "one
**validated** … wave" has no lane validation receipt — `wave-census.json` is a post-hoc count,
not a plan-pass.

**F4 — medium (design, not a false label): the "M1 demonstrated able to fail" red exercises only
the missing-input branch.** round-15.md:180-184 and SCORECARD:657-659 are accurate as written
(`receipt_mapping_missing` at baseline, `receipt_mapping_verified` at measured content), but the
red is produced by `.ufo/waves/round-15/receipt-correction.json` being absent at `ea0446`, not
by a mislabelled or tampered receipt. No preserved receipt exercises
`receipt_mapping_invalid` / `derived_target_mismatch` / `reference_gate_mismatch` /
`mapping_cardinality` / `header_mapping_mismatch` / `target_mapping_mismatch` /
`false_full_gate_relabel` / `new_execution_claim` (the script's negative branches, visible in
`D/receipt-correction-green.txt` lines 16-35: missing-input at 16-17, `problems.append` at
20-22 and 29-33, exit at 35). So round 15 demonstrates that its label audit
refuses absence, not that it catches a wrong label. This matters directly to round-17 C1, which
must show "a label check shown able to fail": round-15's red is not a model for that, and a
round-17 label check that only re-runs a missing-file red would repeat this gap. The other
able-to-fail demonstration in round 15 is stronger and independent: `D/install-guard-red.txt`
detects a real overlap (`["libinput"]`, exit 1) against a green control that would pass, and
that red does contain the failure content, not merely an absent input.

**F5 — low: `D/source-bindings.txt:3-8` records pipeline success in prose, not as an exit.**
The `curl … | sha256sum` receipts say `observed pipeline completion: no error` with no exit code
and no recorded `pipefail`; compare the round-14 precedent `D`-sibling
`.ufo/waves/round-14/evidence/source-bindings-pipefail.txt`. The binding value here is the
printed digest itself, and both digests equal the `SOURCES.md` S051/S052 `raw sha256` cells, so
the source binding stands on content; only the status token is unreceipted.

**F6 — low/definitional: eight of the fourteen round-15 receipts are not committed in the
revision they name.** At `5f1387` only `before.txt`, `census-before.txt`,
`install-guard-{red,green}.txt`, `source-bindings.txt`, `wave-census.json` are tracked;
`after.txt`, `census-after.txt`, `gate-selftest.txt`, `gate-file-plane.txt`, `source-merge.txt`,
`receipt-correction-{red,green}.txt`, `committed-bindings.json` are tracked one commit later in
`9ebd737` ("round-15: bind measurements and record no-harm admission stop", 04:38:09). The
receipts carry `measured_commit: 5f1387` and their mtimes (04:35:36–04:37:55) are after
`5f1387`'s commit time (04:35:06), so "measured content" is used consistently and no sentence
claims the receipts live in `5f1387`. But `git show 5f1387:<receipt>` fails for 8 of 14, so a
label contract that equates "this receipt is the evidence at revision R" with "the receipt is
committed at R" would flag them. Round 17's label check should pick one rule (receipt names its
measured revision vs receipt is contained in it) and encode it; round 15 used the former
without saying so.

## 3. Input for the round-17 label-check claims list

Claims a label check must be able to fail on, drawn from this audit:

1. A sentence names a receipt and a verdict token; the receipt contains that token with the
   claimed exit code (round-15's passing pattern, e.g. round-15.md:180-184).
2. A sentence names a receipt and a *count or digest*; the receipt's printed value equals it
   (e.g. SCORECARD:637, 660).
3. A sentence cites one receipt for a token that actually lives in a different, unnamed file
   (round-15 F2 shape — must fail on a mutated pointer).
4. A sentence's literal command differs from the receipt's recorded `command:` line (round-15
   F1 shape — must fail on a mutated command).
5. A sentence attributes a version/validation label no receipt carries (round-15 F3 shape).
6. A sentence's "demonstrated able to fail" red exercises only absent-input, with no negative
   fixture for a wrong label (round-15 F4 shape).
7. Whether the receipt is required to be committed in the revision it names (round-15 F6 —
   decide, then enforce).

## 4. Residual risk and verification gaps

- I did not re-execute any receipt: no gate, selftest, measure probe, mutation harness or frozen
  run was invoked, per the lane's no-test-execution rule. Token checks are receipt-reading, not
  reproduction of the underlying runs.
- The round-15 red (`receipt_mapping_missing`) cannot be re-derived without the baseline's absent
  JSON; I confirmed only the blob's absence at `ea0446` and its presence/contents at `5f1387`.
- `source-bindings.txt`'s `pacman -Q libinput wayland` output is read from the receipt; I ran no
  package query (host pause in force). The log anchor 2429–2439 was read as file bytes.
- The `d6d5eb27…` provisional hash appears in two round-14 receipts and `ef50e262…` in one; I
  verified the mapping records both and that neither is retro-assigned to `32118fc`, but I did
  not attempt to recover the worktree preimages (round-15 itself says they are not recoverable).
- Quoted source text and registry semantic admission were out of scope; this audit checked
  receipt labels only.

No lane file other than this report was written; no git/jj mutation, no commit, no delegation.
