# RerunGateSwap — partial

Seat: `MadoR19.RerunGateSwap`, 2026-10-20. Attacking one item: the
gate-swap receipt (`bash .ufo/waves/round-19/gate-swap.sh REV` vs the committed
`.ufo/waves/round-19/evidence/gate-swap-receipt.txt`) and the claim that round 18
omitted R10. Integrated tip `01b80946d92b26370d3012a7da655d00dd135154`, lane
`/home/vgpnk/Projects/shokunin/mado-shokunin`. Read-only lane: the only lane write
is this report. No git/jj write in the lane; no jj command at all; no live gate.
Selftests were run only as `--selftest` from `/tmp` copies.

**Headline.** The receipt reproduces exactly: same `tool_sha256`, same
`383 passed / 6 failed`, same six failing names, and I rebuilt the fixture
byte-for-byte from the two pinned commits. But the **R10-omission claim is false
as an unqualified statement about round 18**: round-18's own
`W3CriticC1Final.md:188` lists R10 among the six and already labels it
"(pin drift, expected)". Only the narrower SCORECARD sentence fragment it quotes
omitted R10, and that fragment cites the report that names it.

## 1. Reproduction at the tip

```
$ cd /home/vgpnk/Projects/shokunin/mado-shokunin
$ bash .ufo/waves/round-19/gate-swap.sh 01b80946d92b26370d3012a7da655d00dd135154
RECEIPT tool=.ufo/waves/round-19/evidence/gate-swap-d9a5a18.sh tool_sha256=6e6782c30de4b1a2a308e73ede3a1a36eb4b1a6ba6fdd81e69b5cbc84202ac6e measured_commit=01b80946d92b26370d3012a7da655d00dd135154 utc=2026-10-20T18:03:25Z cmd=bash .ufo/waves/round-19/gate-swap.sh 01b80946d92b26370d3012a7da655d00dd135154
# blocks: base=17661e0fa83f978fb659f5bb8fef47f0969f6945:3467-3489 sha256=c86f51b85c9b469409dec4896cf7088ff1fe5d3e3f887fac64b4149ebe939c4a; old=d9a5a18e17cd3a68b52148fcc01c4a30e340ba98:3402-3415 sha256=414bf6ed658c30c6ad3094127e1a85607af51068815268525e422766cdb4e315; fixture_bytes=182300; provisional=0
MADO_SELFTEST: FAILED — 383 passed, 6 failed
  - R10: derived target equals the recorded gate revision (got '88286b3dfa1f39bde12d416c01d6d424c05989a00c315011daff98004ba65c51' want '20714096e1481e92c8f75414968b596b5b7c31cc684c1dd94b9c3edb0f772744')
  - OM9 (a failed show can never be compared) (want row omarchy.skill.vs_head UNKNOWN)
  - OM9: the UNKNOWN names the unreadable path and the producer rc (want row omarchy.skill.vs_head UNKNOWN containing 'cannot read HEAD:default/omarchy-skill/SKILL.md (rc=128)')
  - OM9: no false local-edit claim (unexpected: local edit)
  - OM9: exactly one omarchy UNKNOWN (the failed read) (got '0' want '1')
  - OM9: exactly one omarchy FAIL — the unreproducible sha row (got '2' want '1')
fixtures kept: /tmp/w5-mado-m52-selftest.g5lFCh
exit=2
SCRIPT_RC=0
```

A second run (`/tmp/r19-gateswap-rerun.txt`, utc `18:04:33Z`) was byte-identical
apart from the mktemp path. Diff against the committed receipt, normalising only
the mktemp path (`fixtures kept:`) and `measured_commit` on line 1:

```
$ diff <(sed -e '1s/measured_commit=[0-9a-f]*/measured_commit=REV/' -e 's#fixtures kept: .*#fixtures kept: PATH#' \
        .ufo/waves/round-19/evidence/gate-swap-receipt.txt) \
       <(sed -e '1s/measured_commit=[0-9a-f]*/measured_commit=REV/' -e 's#fixtures kept: .*#fixtures kept: PATH#' \
        /tmp/r19-gateswap-rerun.txt)
1c1
< RECEIPT … measured_commit=REV utc=2026-10-20T17:41:13Z cmd=bash .ufo/waves/round-19/gate-swap.sh df84807d8fc49f5d8fb4ec3060859e5b1992084c
---
> RECEIPT … measured_commit=REV utc=2026-10-20T18:04:33Z cmd=bash .ufo/waves/round-19/gate-swap.sh 01b80946d92b26370d3012a7da655d00dd135154
```

So: identical `tool_sha256`, identical `# blocks:` line, identical six failing
names and got/want digests, identical `exit=2`; line 1 differs only in the
`measured_commit`/`utc`/`cmd` the caller supplies. The fixture and receipt
mtimes were unchanged by my runs (`14:10:26` and `14:41:13` -03), so the script
did not rewrite evidence.

Binding facts were checked directly (read-only):

```
$ git show df84807d8fc49f5d8fb4ec3060859e5b1992084c:.ufo/waves/round-19/evidence/gate-swap-d9a5a18.sh | sha256sum
6e6782c30de4b1a2a308e73ede3a1a36eb4b1a6ba6fdd81e69b5cbc84202ac6e  -
$ git show 01b80946….ufo/waves/round-19/evidence/gate-swap-d9a5a18.sh | sha256sum   # same
$ git merge-base --is-ancestor df84807 01b80946; echo rc=$?      → rc=0
$ git show df84807:…/gate-swap.sh | sha256sum = 01b80946:… = c3bce9f3…
```

The fixture exists at `df84807` and at tip with `tool_sha256`'s bytes, the
receipt itself is committed at tip, and `df84807` is an ancestor. That is the
criterion-24 shape. (The receipt file is absent at `df84807`; it was added by the
tip commit while binding `measured_commit=df84807`, which carries the fixture —
consistent with `gate-swap.sh`'s own "post-commit re-cut" rule.)

## 2. Independent reconstruction and controls

I did not trust the script's own swap: I rebuilt the fixture from the two pinned
commits and compared.

```
$ git show 17661e0…:tools/mado-verify.sh > /tmp/r19gs/base.sh   → sha256 c9fb0cef3e08…
$ git show d9a5a18…:tools/mado-verify.sh > /tmp/r19gs/old.sh    → sha256 fba82a662795…
$ sed -n '3467,3489p' base.sh | sha256sum  → c86f51b85c9b469409dec4896cf7088ff1fe5d3e3f887fac64b4149ebe939c4a
$ sed -n '3402,3415p' old.sh  | sha256sum  → 414bf6ed658c30c6ad3094127e1a85607af51068815268525e422766cdb4e315
$ python3 -I - <<'PY'   # fixture := base[:3466] + old[3401:3415] + base[3489:]
reconstructed_sha256=6e6782c30de4b1a2a308e73ede3a1a36eb4b1a6ba6fdd81e69b5cbc84202ac6e
committed_sha256=6e6782c30de4b1a2a308e73ede3a1a36eb4b1a6ba6fdd81e69b5cbc84202ac6e
bytes 182300 182300 equal= True
PY
```

Controls (each a `/tmp` copy, `--selftest` only):

```
$ bash /tmp/r19gs/base-copy.sh --selftest
MADO_SELFTEST: 389/389 assertions passed          # rc 0
$ python3 insert harmless comment after base.sh line 10; bash base-edit.sh --selftest
MADO_SELFTEST: FAILED — 388 passed, 1 failed
  - R10: derived target equals the recorded gate revision (got '82b14defcaa7f6e88f94538a10062c23eb9effbf96bdb1b0e355b32aafbe279e' want '20714096e1481e92c8f75414968b596b5b7c31cc684c1dd94b9c3edb0f772744')
```

The harmless-edit control supports the round-19 reading that R10 is an
any-edit identity pin (`PIN_MADO`), not a second behavioural failure of the
swapped block: a comment insertion that cannot change the vs_head behaviour
produces R10 alone. The five OM9 names are therefore the criterion-26 red;
`383 + 6 = 389`; the receipt's `exit=2` is the selftest rc, not a script failure
(script rc 0). Refusal arms also behaved as the w1 report states:
`gate-swap.sh deadbeef` → `REFUSED: cannot resolve 'deadbeef' to a lane commit`,
rc 2; no argument → usage + rc 2.

**Caveat on the base gate (labelling, not binding).** The fixture is built from
`17661e0`'s gate, sha `c9fb0cef…` — which is also the gate at the round-19
baseline `9c54c56` — while the gate at tip is `1036d100…` (the wave-1 443-assertion
gate). So the fixture's `389`-assertion selftest is the pre-wave-1 gate's, not the
tip gate's. The receipt does not claim otherwise (its tool is the fixture), and
`gate-swap.sh`'s header and w1's §2 table call `17661e0` "the landed gate", which
is stale at tip; w1's own Limits do disclose "synthetic gate bytes (`17661e0` +
one `d9a5a18` block)". Mitigating: the exchanged vs_head block is **byte-identical
at tip and base** (both `c86f51b8…`; tip lines 3779-3801), and OM9 assertions are
still present at tip, so the swap still addresses the live block text. Not a
false receipt; a stale label.

## 3. The R10 / round-18 claim — breaks as stated

The w1 report says:

> passes with R10 as the unlisted sixth failure. [INFERENCE] the round-18 prose
> omitted R10; only the count is recorded there, so this cannot be confirmed
> from that note.
> — `.ufo/waves/round-19/w1/reports/GateSwapReceipt.md:121-124`

and round-19 carries the narrower form:

> five OM9 assertions plus `R10` …; round 18's "383/389, five OM9" omitted R10.
> — `corpus/QUALITY.md:199-201` (same at `corpus/lessons/round-19.md:19`)

Reading the two files named by the item:

- **`W3CriticC1Final.md` did not omit R10.**
  `.ufo/waves/round-18/w3/reports/W3CriticC1Final.md:188` (committed at tip):
  `- R10 (pin drift, expected)`, in the same six-name block beginning
  `MADO_SELFTEST: FAILED — 383 passed, 6 failed` (`:186-194`). It also already
  gives the classification the w1 report presents as its own: "pin drift,
  expected". So the clause "the round-18 prose omitted R10" is **false**, and
  "only the count is recorded there / cannot be confirmed" is false for that
  report.
- **`SCORECARD.md`'s red-before sentence did omit R10 from its enumeration**, but
  cites the report that names it:
  `SCORECARD.md:1043-1044` — "Criterion 26's reproducible red is the d9a5a18
  block swapped into the landed gate (383/389, five OM9 failures; w3 report
  `W3CriticC1Final.md`)". `SCORECARD.md:1054` also names R10 in the round-18
  text ("m07 … only by the R10 pin assertion"), though in the MutGateOM context.

Verdict: the sentence in QUALITY/lesson is **true only as a quotation of the
SCORECARD fragment** ("*round 18's '383/389, five OM9'* omitted R10"); read as a
claim about round 18 generally it is false, and w1's `[INFERENCE]` is falsified
by a round-18 report the SCORECARD sentence itself cites. The round-19 texts drop
that citation while keeping the omission charge, which is what turns a defensible
narrow statement into an overclaim. Smallest correction: say "SCORECARD's
red-before sentence omitted R10 from its list (it cites `W3CriticC1Final.md`,
which names it as pin drift)" and delete the `[INFERENCE]` clause in
`GateSwapReceipt.md:122-124`. No numeric claim depends on this; it is an
attribution/novelty defect, not a tally defect.

## 4. Adjacent defect found (not the assigned claim)

The new receipt **is** criterion-24 conformant, but the shipped round-19 claims
file never exercises it. Adding the claim in `/tmp` (receipt read at tip,
`bind_rev=df84807`, `tool=.ufo/waves/round-19/evidence/gate-swap-d9a5a18.sh`,
`expect=ok`):

```
$ python3 -I .ufo/waves/round-18/receipt-check.py /tmp/r19gs/gs-claim.json
RECEIPT r19-gate-swap-recut ok
EXPECT_SUMMARY: 1/1
rc=0
```

but as shipped:

```
$ python3 -I .ufo/waves/round-18/receipt-check.py .ufo/waves/round-19/receipt-claims.json
RECEIPT r19-c26-redbefore-headerless MISSING_PROVENANCE
RECEIPT r19-c26-regression-recut-headerless MISSING_PROVENANCE
RECEIPT r19-tw-recall-before ERROR
RECEIPT r19-fresh-pins-before ERROR
RECEIPT r19-measure-before ok
EXPECT_SUMMARY: 3/5
rc=2
```

There is no `gate-swap-receipt` claim in `.ufo/waves/round-19/receipt-claims.json`
(grep and JSON scan both empty). The QUALITY/lesson sentences stop short of
saying the checker verifies the re-cut, so this is not a false sentence; but the
R18-V2 "applied criterion 24" story is only half-run by its own runnable check:
the red arms are exercised, the replacement receipt is not. [INFERENCE] adding
the claim above (or an equivalent) is what makes the checker, rather than a
reviewer's `git show`, prove the re-cut; the `tool_rev` semantics documented in
the claims file are not read by the unmodified checker (the two ERRORs), which is
RerunReceipts' item, noted here only because it shares this file.

## Limits

- Read-only lane; no commit, no jj command, no live gate. All selftests were
  `/tmp` copies invoked with `--selftest`; `--regression` and the tip gate's
  claimed 443/443 were not run (RerunGate's item).
- I did not investigate why one of my own selftest fixture roots
  (`/tmp/w5-mado-m52-selftest.g5lFCh`) disappeared minutes after the run while a
  second (`…1lScPL`) persisted; the gate prints "fixtures kept" and another seat
  (`MadoR19.MutGateR19`) reported the same disappearance mid-batch. Scratch only,
  not evidence; cause `[UNK]`. No lane path was touched.
- The fixture is synthetic: `17661e0` gate + the `d9a5a18` vs_head block. Its
  389-assertion suite is not the tip gate's 443-assertion suite (see §2); I did
  not rebuild the fixture on the tip gate (that would change the pinned
  `tool_sha256` and is not what the receipt attests).
- R10's got-digest `88286b3d…` is stable across my runs; its derivation was not
  traced into `PIN_MADO` beyond the evidence that an unrelated comment edit moves
  it.
- I did not adjudicate whether C1's numerator should change; this item has no
  effect on it.

## Installs

none.
