# RevLessonCorrections — holds: the round-19 corrections and recorded decisions match the closure and pinned bytes

## Findings

None. The specified correction figures, registry join, suite-edit count, and the checked Decision claims agree with the round-19 closure and committed evidence. No actionable mismatch found.

## Evidence

All counters below were run against a read-only clone at `a4046a8216080d4004de3f268c62cf142095ac07` with origin removed; the counter inputs are committed bytes. No lane files were changed other than this report.

### R19-V2 — S096 counts and five S090-only pointers

The correction at `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/lessons/round-20.md:61-68` matches closure `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/lessons/round-19-verifier-spotcheck.md:59-61`.

Commands and outputs:

```text
python3 -I /tmp/mado-r20w2-RevLessonCorrections/.ufo/waves/round-19/fresh-pins.py b435568540f9a28f4f7bb902af8dbe6a5b084dfe
  denominator=13, current=13, score=10.0

python3 -I /tmp/mado-r20w2-RevLessonCorrections/.ufo/waves/round-20/tally-check.py pointer-token --counter-rev b435568540f9a28f4f7bb902af8dbe6a5b084dfe --rev b435568540f9a28f4f7bb902af8dbe6a5b084dfe --token S096
  denominator=13
  first_line=6/13
  any_line=8/13
```

The generic `fresh-pins.py` 13/13 score counts a qualifying `S###` pointer, not S096 specifically. The S096-specific result is 8/13 on any qualifying line and 6/13 on the first. Its `token_lines=-` rows are precisely the five named in the correction: `arc-synthesis.md:392`, `closeout-r11.md:299`, `config-health-report-r3.md:1009`, `waybar-walker-plane.md:479`, and `waybar-walker-semantics.md:467`. Each inspected line cites S090 and lacks S096. `git diff --exit-code b435568540f9a28f4f7bb902af8dbe6a5b084dfe a4046a8216080d4004de3f268c62cf142095ac07 -- <these five paths>` exited 0; the exact bytes remained unchanged between the measured tip and current tip. As the correction says, this is provenance, not a remeasurement of walker behavior.

SHA-256: `round-20.md` `bf55c34db05e47a1499e67567df0d2a8841a4337da26c25a46a10c03e1e324e0`; closure `round-19-verifier-spotcheck.md` `dcb7a9134022e010ef357a095ded13d15d6f77a9090dc2976f0c9d8090fea0a0`; counter `fresh-pins.py` `a094be019968ef2cff4bf643be5f5f2b62d24b957310a4c0620a0ea2c5bcd789`; `tally-check.py` `21ce9dd57a47d975623aa9ca2bf53c3dadb8fa68b6f066a92461edba2fd2aea4`.

The five source-file hashes (same bytes at `b435568` and `a4046a8`) are: `arc-synthesis.md` `96701cc9878a84702c7ffe8747615f3fefb48438020d8b027b12eda3e4133064`; `closeout-r11.md` `9ae5866af665f1dcc68190896c8fa8d06b1f7d35be5120b0387acc141b02c6bf`; `config-health-report-r3.md` `fc08981003ab03575991dc569604fd7cbd57579d79b15eec3e68a9f543ba849b`; `waybar-walker-plane.md` `0cea1d3d8d2ca4adbddf1d5f4da0d8e8e4449096910a05890ab3b144410cb616`; `waybar-walker-semantics.md` `1d1e785a01ceac5759f3a55c48dedfb59fcc561d8645be925eb954bbd1dc8925`.

### R19-V4 — 154 scanned files

`round-20.md:69-73` corrects the 155 claim, consistent with closure `round-19-verifier-spotcheck.md:125`.

```text
python3 -I /tmp/mado-r20w2-RevLessonCorrections/.ufo/waves/round-20/tally-check.py receipt-files --rev b435568540f9a28f4f7bb902af8dbe6a5b084dfe --path .ufo/waves/round-19/evidence/final/tripwire-seat-scan.txt
  files=154
  distinct_paths=154
  jsonl_paths=154
```

The receipt hash is `9572d2a655d1e06aef73b4e87edb713e9486be1f0e9a8f92ed98bb42830e3139`. The correction also preserves the closure's limits: the written-then-run script was not detected and host state was not independently measured.

### R19-V5 — nine labeled OM10 assertions, eight distinct

`round-20.md:74-75` matches closure `round-19-verifier-spotcheck.md:88`. The committed-byte checker invocation returned:

```text
python3 -I /tmp/mado-r20w2-RevLessonCorrections/.ufo/waves/round-20/tally-check.py selftest-labels --old 9c54c56a6a7528675027b7f628f97a1b8d1b8e8d --new b435568540f9a28f4f7bb902af8dbe6a5b084dfe --label-id OM10
  removed_occurrences=9
  removed_distinct=8
  added_occurrences=0
  added_distinct=0
```

### R19-V6 — registry join yields 25 members without reports

`round-20.md:76-79` and closure `round-19-verifier-spotcheck.md:127` agree. The committed registry has 86 member keys (`swarm-registry.json:7`; JSON query `.members | length` → `86`). The report directory contains 63 entries (62 Markdown reports plus the registry JSON). Joining sorted registry keys to Markdown report basenames, then taking the reverse difference, returned:

```text
members_without_report=25
reports_without_member=TwMerge
```

The successful join used `LC_ALL=C`, sorted both inputs, and `comm -23`/`comm -13`; an initial default-locale attempt reported unsorted input and was discarded. The registry SHA-256 is `42b4122fb6178af26b637d9344dbc25608619be0b3e3f31cee96c5b33b6597a6`.

### Eight `r20_edit` cases and the Decisions

The final `round-20.md:83-99` claims match the retained evidence:

- `recall-split-final.txt` has `detected_observed=5`, `detected_lead=1`, `undetected=0`, `control_lines=20`, and `control_findings=0`; the rule-B lead remains in findings. The `RevLeadExitSemantics.md:5-13` report explains why moving it to a separate list would make the unchanged recall counter read 5/6.
- The `TwVcsHelp.md:159,169,172-176` empirical table supports the E4 corrections: `git commit -m --help` commits; `jj describe -m --help` returns a missing-value error with no operation; plain `jj git push --dry-run` snapshots, while the `--ignore-working-copy` form does not; and user aliases can execute despite `--help`.
- Both intentionally retained failing cases remain failures in the pinned precision result, not silently rewritten expectations. Extracting their rows from `precision-final.txt` produced `W-CaseWrapperForms-class-method-instance` (`want exit=0`, `got exit=1`, observed `package_query/pacman:-Q`) and `H-AdoptW2-RerunPrecision-corpus-jj-var-verb-help` (`want exit=0`, `got exit=1`, observed `vcs_write/jj:$c`). The `Runner().run([...])` fixture directly passes argv to `subprocess.run` (`CaseWrapperForms--class-method-instance.jsonl:1`); its stated-miss rationale is recorded at `precision/expected.json:1319` and the tool decision at `TwRuleB.md:70`. The alias canary is recorded at `TwVcsHelp.md:175-176`.
- A literal `r20_edit` search of the committed round-19 tripwire expectations found exactly eight entries: one at `r19-bashcvar/expected.json:426` and seven at `r19-helperfn/expected.json:111,121,131,141,165,270,287`. `git diff --unified=1 b435568540f9a28f4f7bb902af8dbe6a5b084dfe a4046a8216080d4004de3f268c62cf142095ac07 -- .ufo/waves/round-19/tripwire/r19-bashcvar/expected.json .ufo/waves/round-19/tripwire/r19-helperfn/expected.json` shows each of those eight changing from clean/empty findings to exit-1 findings. It shows no removed finding; two existing helperfn rows only gain `evidence: lead` (the `pacman:-Q` and `pacman:-Qi` rows). Thus the lesson's “eight” and “two lead markers” are supported.
- The precision expected suite itself is unchanged from pre-measurement `f3da50488661509ce5d144c90f7780f8088e0903` through `a4046a8` (`git diff --exit-code` returned 0), corroborating that the two observed counterexamples were not edited to make the result green.

SHA-256: `r19-bashcvar/expected.json` `e72a97def0c67617984962c4b3276b6127862daa4d48f9dabd5ae845437abbe5`; `r19-helperfn/expected.json` `91e247912827aa5848a7ce87ef7c59273c6681d737f6456d87180f251ded3644`; `precision/expected.json` `1039c4fa6ede43b1f08cca231e6c713aa032722e4955f89dbd8b8f3de092254f`; `precision-final.txt` `629724dce770aad74a4e268fc36a2061d93fcf5f3c8bd77beee777d61f80e98c`; `recall-split-final.txt` `5165b72878feec8c67e20a0ab079db0aaaea358258b8a62fbb965dd91a6df0a2`; `TwVcsHelp.md` `6061158f61a5a6fe0e39c8cc46bba51af7d4c138802f16977a2f0db9aafe8ba2`; `CaseWrapperForms.md` `923474b967b5d1fa9884e1e7c3a6aa2132e23e8ab105271814151a6b46a25656`; `TwRuleB.md` `19a0162378a45de59348815826b2670ca71756d9883d9d881b029eb07c071d3f`.

## Residual risk

[UNK] The full selftest suite, full-corpus scan, and empirical Git/jj harnesses were not rerun for this review. Their relevant committed receipts and reports were read; only the pin, pointer-token, receipt-file, and OM10 label-count subcommands were executed here.

## Limits

Review scope was the two named lesson sections and their specified closure, receipt, registry, fixture, and decision evidence. No host-pause command, live gate, or network fetch was run. The only code executed was the named committed-byte counters in the `/tmp` clone, not in the lane checkout. No tools were installed.

## Installs

none
