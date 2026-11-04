# R75ExecC1 — independent C1 execution

## Axes and scope
Calibration: challenge-bound kill credit and green outcome. Operability/no-harm: observe all three assigned legs without repairing production files. Only C1 was measured by this seat; C2 and the global no-harm gate were not run.

Read the frozen declaration and all three committed baseline/measurement receipts; none was rewritten. Measured revision: `def73656c94f0e88bd671cfb4a65124338261722`; held baseline: `b149d2ece1a6d75f5738aa8bf4a9493f1a9c7da6`.

## Observed results

| Command | rc | Contract/tally last line | Unexpected output |
|---|---:|---|---|
| Frozen C1 counting command | 0 | `MADO_R75_HARNESS_WITNESS: cases=11 correct=11 base_correct=6 verdict=TARGET_MET rev=def73656c94f0e88bd671cfb4a65124338261722` | None observed |
| Successor on real lane | 0 | `MADO_R75_LANDING_CONTROLS: selftest=62/62 mz=pass mr=pass killed=2/2 baseline=0/2 witness=ok verdict=TARGET_MET rev=def73656c94f0e88bd671cfb4a65124338261722` | None observed |
| Successor harness selftest | 0 | `MADO_R75_HARNESS_SELFTEST: 20/20 assertions passed` | None observed |

The counting command's final line matches the declaration's required sentence, including the frozen revision. All eleven candidate decisions match their frozen labels; the held harness matches six. The five separated modes are uppercase-echo, stale-witness, absent-witness, wrong-witness and last-wins-wrong. No leg was dead or absent; no error text occurred in the captured merged stdout/stderr.

## Exact invocations

Working directory for each command: `/home/vgpnk/Projects/shokunin/mado-shokunin`.

```sh
python3 -I quality/counters/c1-r75-harness-witness.py --repo . --rev def73656c94f0e88bd671cfb4a65124338261722 --base-rev b149d2ece1a6d75f5738aa8bf4a9493f1a9c7da6 --controls .ufo/waves/round-75/controls/c1-harness-cases-r75.json --scratch-root /fast/scratch/hyaku/mado-r75/R75ExecC1/run
```

```sh
python3 -I quality/counters/c1-r75-landing-controls.py --repo . --rev def73656c94f0e88bd671cfb4a65124338261722 --scratch-root /fast/scratch/hyaku/mado-r75/R75ExecC1/real
```

```sh
python3 -I quality/counters/c1-r75-landing-controls.py --selftest --scratch-root /fast/scratch/hyaku/mado-r75/R75ExecC1/selftest
```

The three commands ran concurrently, once each, with distinct scratch roots. Full stdout and stderr were captured together without filtering; exit status is retained separately, so the receipt's last line remains its contract/tally line.

## Real-lane evidence

```text
MADO_R75_CHALLENGE source=secrets.token_hex(8) length=16 generation_sha256=b6108c86e8e03befce50256e2381ec08f199a1ab7fe192aeedef70459c45857d rev=def73656c94f0e88bd671cfb4a65124338261722
MADO_R75_EXTRACT path=quality/landing-counters.sh bytes=16165 sha256=b0612f111f3b676ffe42694c19802a34a623cc22076f32cf0ab750b803c73f1f
MADO_R75_EXTRACT path=quality/counters/c3-r56-used-by.py bytes=21326 sha256=f54423eb8ab24eeb5a8cd51f2d38408fe02054797ba841c3940cde28d3903b3f
MADO_R75_EXTRACT path=quality/check-tool-ledger.py bytes=40636 sha256=1c96c4cfd69ad97fbfc9174c9fe4d27b1d157df69cbcbc2451067f1374febdfb
MADO_R75_EXTRACT path=tools/mado-receipt-citecheck.py bytes=10822 sha256=3b61fa42b77e9c8065ab05668247c330b537910b06f7209caba7afbd0b102ad0
MADO_R75_EXTRACT rev=def73656c94f0e88bd671cfb4a65124338261722 files=4
MADO_R75_SELFTEST instrument=quality/landing-counters.sh rc=0 summary=62/62 green=yes
MADO_R75_MUTANT M-Z path=quality/landing-counters.sh clause_count=1 recipe=clause-delete removed='[ "$citations" -gt 0 ] && ' from_sha256=b0612f111f3b676ffe42694c19802a34a623cc22076f32cf0ab750b803c73f1f rc=1 failed_assertions=3 assertions=59/62 killed=yes sha256=6d1a73b14c6e17cedf5cd6399fe58de246591682cb3a3518a2c7163711738216
MADO_R75_GUARDS citecheck=1 usedby=1 ledger=1
MADO_R75_R_CONTROL fixture_rev=b2ace7c1e9d9dac0ebeaa276ca40e6d7bd0d99c6 real_tree=a82978be5fa20eb69fee0a6fbe51a99c37bc6a3e forged_tree=1b37d99db3872339180cf844ef9a05a3737bfb71 forged_visible=yes guarded_visible=no
MADO_R75_CHILD_ENV no_replace_objects=absent keys=GIT_CONFIG_GLOBAL,GIT_CONFIG_NOSYSTEM,GIT_CONFIG_SYSTEM,GIT_TERMINAL_PROMPT,HOME,LC_ALL,MADO_LANDING_NONCE,PATH,TMPDIR GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_SYSTEM=/dev/null GIT_TERMINAL_PROMPT=0 HOME=/fast/scratch/hyaku/mado-r75/R75ExecC1/real/r72-c1/home LC_ALL=C MADO_LANDING_NONCE=edfbce65b456d5b3 PATH=/home/vgpnk/.local/share/mise/installs/node/latest/bin...(22 dirs) TMPDIR=/fast/scratch/hyaku/mado-r75/R75ExecC1/real/r72-c1/home
MADO_R75_R_CHILD role=unmutated rc=1 verdict=TARGET_MISSED missing=1 control=green
MADO_R75_MUTANT M-R path=tools/mado-receipt-citecheck.py guard_count=1 recipe=line-delete removed_line='            env=dict(os.environ, GIT_NO_REPLACE_OBJECTS="1"),\n' from_sha256=3b61fa42b77e9c8065ab05668247c330b537910b06f7209caba7afbd0b102ad0 rc=0 verdict=TARGET_MET missing=0 forged_credit=yes killed=yes sha256=414ca759232a3d31451f86060f4b0ba3382dd151f4bffe797793cb2ced5cee11
MADO_R75_LANDING_CONTROLS: selftest=62/62 mz=pass mr=pass killed=2/2 baseline=0/2 witness=ok verdict=TARGET_MET rev=def73656c94f0e88bd671cfb4a65124338261722
```

- `selftest=62/62`: the extracted landing instrument's own assertion summary, not the successor harness's standalone selftest tally. Its child exited 0 and its summary was green.
- `mz=pass`: deleting the unique zero-citation guard clause produced 59/62 with three failing assertion details (child rc 1); arithmetic plus the run's exact challenge echo earned M-Z kill credit.
- `mr=pass`: the inherited replacement-ref pair discriminated the real and forged trees. The unmutated child returned rc 1 / TARGET_MISSED / missing=1; removing the replacement-object guard returned rc 0 / TARGET_MET / missing=0, exposing forged credit and killing M-R.
- `witness=ok`: the last parsed 16-hex witness from the unmutated instrument matched this run's challenge byte-for-byte. It authenticates the echo, not the truth of the assertions. The printed nonce is a generated test challenge, not credential/session material.
- `killed=2/2 baseline=0/2`: both inherited defect recipes were applicable and killed. The baseline field is the inherited fixed contract baseline, not this seat's 6/11 held-fixture score.
- Standalone successor `--selftest`: `MADO_R75_HARNESS_SELFTEST: 20/20 assertions passed`, rc 0.

## Retained evidence and boundaries

All evidence lives in `.ufo/waves/round-75/w1/R75ExecC1/`:

- `counting.txt`, `counting.rc`: complete counting stdout+stderr and rc 0.
- `real.txt`, `real.rc`: complete real-lane stdout+stderr and rc 0.
- `selftest.txt`, `selftest.rc`: complete standalone tally stdout+stderr and rc 0.

Files changed: only those six evidence files and this explicitly assigned advisory report. No production instrument, corpus, committed receipt, global configuration or external substrate was edited. No tools were installed or upgraded. No LSP interface was available in the mounted tool inventory; this read-only execution needed no symbol refactor. Scratch was removed after the retained receipts were written.

Risks/limits: eleven fixtures are rule separators, not general fault coverage; an assertion liar that echoes the current challenge remains accepted by design (`liar-success`). One real-lane run demonstrates this revision's execution, not all runtime conditions. The parent owns global integration/no-harm gate execution. Blockers: none.

## Output self-evaluation

| Axis | Score | Evidence / improvement |
|---|---:|---|
| Accuracy | 5 | Exact retained outputs and process return codes ground each result. |
| Completeness | 5 | Three requested legs, full evidence, field meanings and command table included. |
| Clarity | 4 | Long contract lines make the table wide; plain receipts remain available. |
| Actionability | 5 | Exact commands, revision pins and receipt paths allow parent review. |
| Conciseness | 4 | Real-lane evidence is duplicated here and in its full receipt for direct review. |

Overall: 4.6/5. Improvement: use linked plain receipts when reviewing on a narrow display; avoid duplicating the evidence in downstream summaries. Self-check: the requested observed results and explicit limits support this assessment.
