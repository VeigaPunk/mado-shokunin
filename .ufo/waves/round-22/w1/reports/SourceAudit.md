# MadoR22.SourceAudit — audit authority sourced; three representation unknowns open

Wrote `.ufo/waves/round-22/w1/audit-authority.json`: ten located fleet PROTOCOL.md quotes (Evidence and
Gate standards), the actual r19 verifier C3 gap with located quotes, the C2 basis (arithmetic and
evidence-tier disclosure only), four limitations, and three unresolved representation questions. No
production file, fleet file, detector, payload, or gate was touched or run. Only read-only `sha256sum`,
`git ls-files/status/log/rev-parse`, `awk|diff` and `rg` over committed bytes.

## Observed facts (confidence high, digest-pinned in the JSON)

- Fleet `PROTOCOL.md` (sha `886e459b…`, commit `7c5b34f0`, clean): numeric claims carry their counting
  command (`:352`); a tool that cannot fail is a probe (`:377-378`); verdict 0/1/other (`:380-382`);
  self-test asserts exit code and stable finding id with independently committed expected values
  (`:385-388`); self-test green is capability, not measurement (`:390`); digests checked before
  verdicts, edited snapshot = `snapshot_tampered` (`:394-397`); a verdict never stands in for the native
  judge (`:409-411`); integrator verifies committed evidence (`:415-417`). The r19 closure loaded the
  kimi-shokunin copy (sha `622b29a0…`); its Evidence/Gate sections differ only in the Delivery bullet, so
  every quoted clause is identical.
- r19 verifier (`corpus/lessons/round-19-verifier-spotcheck.md`, commit `1f7f995c`): `rejected-harmed`
  (`:9`); C3 six-line target verified but no-harm fails on precision (`:43`); `r13-root.jsonl:4` comes
  from HelperFn rule B alone, 5/6 without it (`:63`); the tip emits it "without a lead marker" (`:81`);
  operability harmed (`:136`); routed R19-V3 "distinguish leads from observed execution" (`:151`).
- The arithmetic gap is real in the artifacts: `tw-recall.py:12-14,73-75` counts a line as detected if
  any finding exists, with no tier and no unparsed counters; `tw-recall-after.txt` reports 6/6 with six
  `{file,line,detected:true}` rows, the lead indistinguishable; the scan receipt has 11 finding rows,
  all counters 0, and no `evidence|basis|lead` key (absence sweep `rg -c` rc=1).

## Inference

- C2 closes only a disclosure gap (registration `:7`; contract `:3`). It cannot establish semantic
  precision (the verifier's frozenset counterexample is a correctly-counted "observed" row) or
  independent admission (PROTOCOL `:409-417`, registration `:10`).

## Unresolved (routed to planner, see JSON `unresolved_for_planner`)

1. Unit: "five observed plus one lead" is line-level (6 lines); the scan is row-level (11 rows = 10
   observed-line rows + 1 lead). The contract's `claim.total` counts rows.
2. A faithful unchanged-row r19 snapshot lacks `evidence` (and, for tw-recall rows, `class`/`command`),
   so under the contract it may evaluate 2 rather than red 1, and the green 5+1 case needs added labels,
   which changes rows.
3. Missing-marker rows: lead, uncertainty bucket, or forced code 2 is unspecified.

## Checks for main

None run (none in scope). Main may re-hash the pinned sources listed in the JSON.

## Installs

None.
