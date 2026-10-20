# ScribeQuality — criteria 29 and 30 drafted; both red-by-evidence, neither checker landed, and the post-fix round-19 harness is still red on its absent-target arm

Scope: draft text only, at `.ufo/waves/round-20/w1/drafts/ScribeQuality.md` (sha256 `ace2f6ffea1f3d0223ec9666ff23c0b990a90b48499003b4c62cb279f5016c2b`). No checker, harness or lane tracked file was written. Lane HEAD is detached; `refs/heads/master` = `e629f731172b8238caffe50f152217ce56535fb4`; round-19 tip `b435568540f9a28f4f7bb902af8dbe6a5b084dfe`.

## Findings

**F1 — Criterion 29 (fail-closed isolation harness) drafted; red at round-19 shape, not run by this seat.**
- Red artifact: the first `/tmp/sgp/inns.sh`, written at transcript `/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR19/MadoR19.SentinelGatePath.jsonl` line 33 (transcript sha256 `f7f7b4814724d3d894eef234046e5d24a313f9ec64d81668da6b6daaccf73ff7`). The heredoc is 441 bytes, sha256 `b09e07723c09a65d14f1c81c51fc58177afae214794e804e63dc73f92357e75f`. Its arming loop is `[ -e "$p" ] && mount --bind … && echo "armed $p"`, then `set +e` and `"$@"`. Under `set -e`, a failed non-final `&&` member does not stop the script, so the payload runs after a refused mount. The round-19 report records the outcome: `/usr/bin/hyprctl probe` ran, `unknown request`, rc=0 (`.ufo/waves/round-19/w2/reports/SentinelGatePath.md`, Incident section).
- Post-fix file: `/tmp/sgp/inns.sh` equals the line-36 heredoc, 744 bytes, sha256 `59b234934b266861ba89f764d8f37ca5e1911cbbf6f61ce53867e8d3e107ac80` (checked by `cmp`-equivalent sha256 comparison in this seat). It exits 99 or 98 on mount or `cmp` failure, but still has `[ -e "$p" ] || continue`, which silently skips an absent target. Under the draft's own clause ("a missing or unverified target is a setup failure"), the post-fix file is **red** on that arm. Expected by reading only; not run.
- The round-20 `gen_w1.py` names an `evidence/inns-r19-shape.sh` written by another seat. If that file is byte-equal to the 441-byte heredoc above (sha `b09e0772…`), it can serve as the red fixture. This seat did not inspect it.

**F2 — Criterion 30 (re-derived stated counts) drafted; three round-19 counts re-derived by this seat (read-only).** Command results, all against committed bytes:
- `SCORECARD.md:1167` (b435568) says "5/13 name S096 on the crediting line". Re-derived with `git show b435568:<path>` over the 13 files that contain `2.17.0` at `9c54c56` and a same-line `2.17.2` + `\bS096\b` rule: **8/13** (SKILL.md, corpus/README.md, remaining-planes-census, walker-deep-r9, walker-deep, walker-live-surface, walker-route-r18, tools/mado-verify.sh). First-matching-line rule: **6/13**. This matches the closure's R19-V2 figures (8/13, 6/13).
- `SCORECARD.md:1225` (b435568) says "the ten old OM10 assertions". `git show 9c54c56:tools/mado-verify.sh | grep -oE '"OM10[^"]*"'`: **9** occurrences, `| sort -u`: **8** distinct (the label `OM10: the UNKNOWN names the rc` appears twice). At b435568 the same grep gives 14 (OM10A 6 + OM10B 8), consistent with the closure.
- `corpus/lessons/round-19-verifier-spotcheck.md:125` says "lesson prose **155 transcripts**" against the committed receipt. `.ufo/waves/round-19/evidence/final/tripwire-seat-scan.txt` (sha256 `9572d2a655d1e06aef73b4e87edb713e9486be1f0e9a8f92ed98bb42830e3139`) carries a JSON object with **154** `files` entries. The 155 figure is not reproduced by the receipt. I did not locate the lane report that originally wrote "155".

**F3 — Counter arithmetic.** Read-only regex count of `git show e629f73:corpus/QUALITY.md`: 28 numbered criteria, 20 with `lessons/` on the numbered line (matches the closure's 20/28). The draft's 29 and 30 each carry `lessons/` on their numbered line, giving 30/22 — the C2 pre-registered target (22/30). Computed by this seat with the same regex; `measure.py` itself was not run.

**F4 — Citation deviation.** The assignment fixes the parenthetical as `(lesson: lessons/round-20.md#mistakes M2; outside lessons/round-19-verifier-spotcheck.md R19-V4)`. I used it exactly for 29. For 30 I added R19-V2 and R19-V5 to the outside list, because the S096 and OM10 counts are routed there (R19-V2, R19-V5) and R19-V4 covers only the 155/154 receipt. The `M2` anchor is unverified: `corpus/lessons/round-20.md` does not exist at `e629f73`. L1 must confirm the mistake number when the lesson lands.

## Gates checked
- QUALITY.md numbering: 28 existing criteria; 29 and 30 continue the sequence; no line in the draft starts with a digit other than the criterion lines (checked by the regex above).
- House style: one numbered line, `Runnable check:` indented on the next line, red, green, `Limit:` — matches criteria 27–28.

## Not done (by design)
- No harness was executed and no checker run. The red for criterion 29 is expected by reading; the canary design is specified in the draft and is not verified.
- No checker, registry JSON (`count-claims.json`) or `harness-fail-closed.py` was written; both are planned paths.
- No live host probe, package query, `hyprctl`, `sudo`, `systemctl`, or gate run. Host bytes were not read; the only host-adjacent reads were `/tmp/sgp/inns.sh` (scratch file, bytes only).
- No lane file was edited. Only `drafts/` and `reports/` under `.ufo/waves/round-20/w1/` were created.

## Limits
- [UNK] Whether the RevengeInnsHarness `evidence/inns-r19-shape.sh` is byte-faithful to the transcript heredoc; not checked.
- [UNK] The lane report that originally wrote "155 transcripts" was not located in the tree; only the closure's quotation (`corpus/lessons/round-19-verifier-spotcheck.md:125`) was checked.
- The S096 any-line and first-line rules are my reading of the closure's "registered version+source regex" (same-line `2.17.2` + `\bS096\b`); the registered regex text itself was not located.
- Criterion 29 leaves open whether a skipped absent target is acceptable. The draft counts it as red; the lane must decide before the check is written.
- `corpus/QUALITY.md` at `e629f73` was read via `git show`; the working-tree copy was not compared.

## Installs
none
