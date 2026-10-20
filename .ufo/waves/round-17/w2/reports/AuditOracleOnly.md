# AuditOracleOnly — re-running the oracle comparison: are all `oracle_only` lists really empty?

Lane HEAD: `988b858bd6049bc709807534fd725c05264f7e60`.
Read-only audit: no lane file was modified, no transcript was written, no git mutation.
The only mutation was a copy of the tool under `/tmp/audit-mut/` (mutation test, below).
**Installs: none** — no pacman/sudo/uv/npx/curl-to-shell, no systemctl/hyprctl/libinput
or any other live probe; nothing was installed or updated by any channel.

## Verdict

**The attack failed.** Every `oracle_only` list in
`.ufo/waves/round-17/evidence/tripwire-vs-oracles.json` reproduces empty from a fresh
scan and the independent oracle bytes, for all four rounds, and the emptiness is
*causally* the L1 python-heredoc fix: disabling that branch on a /tmp copy recreates
exactly three oracle-only rows and nothing else.

I did find two defects in the artifact's own text/metadata that a reader should know
about (D1, D2 below) and one source-docstring drift (D3). None of them is a missed
non-clean invocation. The claim as written survives under the comparison's evident
semantics; under a strictly literal reading of its `key` string it fails for round 16
only (D1).

## Method and inputs

- Tool: `tools/mado-tripwire.py`, sha256
  `4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44`.
- Session root: `/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-20T01-48-55-258Z_01a156ff-505a-7798-99c2-b47895c874f4`.
- Scans run: `python3 -I tools/mado-tripwire.py --scan $SESS/MadoR13`
  (exit 1; 32 files, 33 findings), plus `$SESS/MadoR13 $SESS/MadoR13.jsonl`
  (33 files, identical 33 findings — the top-level file contributes zero), and the
  same dir+file pair for R14, R15, R16.
- Oracle inputs: `evidence/oracle-r13-r14.json` (sha256 `28e21b65…`),
  `evidence/oracle-r15.json` (`d638c023…`), `evidence/oracle-r16.json` (`b3f9848b…`).
  Round split for r13/r14 is by the oracle's `file` prefix (`MadoR13*` / `MadoR14*`).
- Comparison key, as the evidence states it: `(basename, line, class)` over oracle
  rows whose class is non-clean. The oracles name the clean class
  `clean-data-mention` in r13/r15 and **`clean`** in r16 (r16: 74 of 76 hits); the
  computed table below excludes both, which is the only reading under which the
  committed numbers are possible (see D1).
- Transcript digests: the fresh scans' per-file sha256 sets equal those in
  `evidence/tripwire-r13..r16.txt` (33/33, 33/33, 65/65, 97/97 paths), so the inputs
  have not drifted since the receipts were written.

## Recomputed results

| round | oracle raw | oracle non-clean raw → unique key3 | tripwire findings → unique key3 | agree | `oracle_only` | `tripwire_only` | committed record |
|---|---|---|---|---|---|---|---|
| 13 | 60 | 27 → **26** | 33 → **29** | **26** | **[]** | 3 | 26/29/26/[]/3 — exact |
| 14 | 48 | 41 → **25** | 50 → **25** | **25** | **[]** | 0 | 25/25/25/[]/0 — exact |
| 15 | 251 | 139 → **131** | 208 → **149** | **131** | **[]** | 18 | 131/149/131/[]/18 — exact |
| 16 | 76 | **2** | **2** | **2** | **[]** | 0 | 2/2/2/[]/0 — exact |

The r13 `tripwire_only` rows reproduce byte-for-byte as the committed triplets
(`file`, `line`, `class`, `rule | command`): `GlobalCapture.jsonl` 19 `live_probe`,
19 `package_query`, 65 `live_probe`. All three are **same-call class multiplicity**,
not missed executions: the oracle assigns one class per bash call
(`call_2a68aff4b6984128b91f75d2` → `host_mutation`; `call_92795601e6834bc19c4c43e7`
→ `package_query`), while the tripwire reports every class in the call (the first call
also contained `wayland-info --version` and `pacman -Q wayland-utils`; the second also
contained `hyprctl -j version`). This is the mechanism already documented by
`AuditTripwireOnly1.md`; I did not re-open those rows.

The r13 raw→unique drop (27→26) is one duplicate key3: `GlobalCapture.jsonl:33`
`live_probe` twice (`call_417d6d2655dd46739ded68f5` wayland-info and
`call_6af4a462739c443cbce3d9da` hyprctl). The committed `oracle_nonclean: 26` is the
unique count, consistent with the table's other rounds.

## Finer-grained check: exact tool call, not just line+class

The declared key collapses two tool calls that share a line and class, which could in
principle mask a miss. It does not here. Comparing on
`(basename, line, class, tool_call_id)` (r15 ids keep their literal `|fc_…` suffix;
they are identical on both sides):
`oracle_only = 0` in **all four rounds** (r13 agree 27/27 raw rows, r14 41/41,
r15 139/139, r16 2/2). Every non-clean oracle row has a tripwire finding from the
*same* issued tool call.

## The heredoc fix is load-bearing (mutant proof)

The claim says the lists are empty *after* the fix. I tested the counterfactual on a
copy, never the lane file:

```
cp tools/mado-tripwire.py /tmp/audit-mut/pre.py
sed -i 's/            elif fed_to_python:/            elif False and fed_to_python:/' /tmp/audit-mut/pre.py
python3 -I /tmp/audit-mut/pre.py --scan $SESS/MadoR13
```

Result: counts `{host_mutation: 2, live_probe: 9, package_query: 19}`, and the
comparison yields `oracle_only = 3`:

- `MadoR13.GlobalCapture.jsonl:52 live_probe` (`call_57d298bd971e4eafbbe31a9c`)
- `MadoR13.GlobalCapture.jsonl:89 live_probe` (`call_daba0ba3d3ef41ebbc5eb7f0`)
- `MadoR13.GlobalCapture.jsonl:132 live_probe` (`call_00_rhjwl3oosd3c2egky56cs1p2`)

Those are exactly the oracle's three "inline python spawns hyprctl via
subprocess/os" rows — `subprocess.run(['hyprctl', …])` inside
`python3 - <<'PY'` bodies (`tools/mado-tripwire.py:353-364`: `fed_to_python` →
`classify_eval(body, "py")`). With the branch restored (the committed tool) the same
comparison returns `oracle_only = []`. So the empty lists are produced by the fix,
not by forgiving comparison code.

## Defects found (none is a missed event)

**D1 — the `key` line is inaccurate for round 16.**
`evidence/tripwire-vs-oracles.json:3` says
`"key": "(file basename, line, class); oracle rows with class clean-data-mention excluded"`.
`evidence/oracle-r16.json` classes its clean rows `"clean"` (74 hits; `:40` is the
first), not `clean-data-mention`; `w1/reports/OracleR16.md:19` says the same.
Under the literal key, r16 has 76 non-matching rows → 73 unique key3 and
`oracle_only = 71`; the committed `2/2/2/[]` is only reproducible by treating
`clean` as clean (or counting only the dirty classes
`host_mutation|package_query|live_probe`). A reader applying the stated key verbatim
gets a non-empty r16 list. Fix the key text, e.g.
`dirty classes only (host_mutation, package_query, live_probe)`.

**D2 — the r13/r14 oracle seat's table does not add up.**
`w1/reports/OracleR13R14.md:22-23` reports `clean-data-mention 38` and
`total hits 108`, but 3+55+10+38 = 106. `evidence/oracle-r13-r14.json` `counts` has
`clean-data-mention: 40` (3+55+10+40 = 108). The non-clean split (host 3,
package 55, live 10 = 68 raw) matches the seat's own section headings, so the 2-row
delta is confined to the clean class and cannot affect `oracle_only`; its provenance
(report typo vs two rows added after the report) is unresolved.

**D3 — source docstring drift from the fix.**
`tools/mado-tripwire.py:110-116` says heredoc bodies "are treated as data unless fed
to a shell", but `:357`/`:363` also feed them to the python classifier. That python
feed is precisely the fix under test, so the docstring understates the tool's own
behaviour. One-line correction: "unless fed to a shell or python".

## Limits and remaining unknowns

- **No lsp device/server was available in this lane.** I traced `classify_shell` →
  `logical_lines` → `classify_eval` by direct source reads (`tools/mado-tripwire.py`
  lines 110-165, 340-365), not semantic LSP; recorded in lieu of a server answer.
- The oracle files are **artifacts, not reproducible runs**: the r13/r14 seat used a
  throwaway `/tmp` scanner, and no generator for r15/r16 is committed. I cannot prove
  no clean row was added after the seat report (D2 is exactly such a 2-row delta);
  but the seat reports' non-clean totals (68 raw r13/r14, 139 raw/131 unique r15,
  2 r16) match the JSON, so there is no evidence of a deleted non-clean row.
- The comparison can only show the tripwire is at least as sensitive as the oracle;
  a shared blind spot is invisible to it. The oracles' fixed token list (and the
  tripwire's bin/verb tables) deliberately exclude commands such as `rm`: e.g.
  `MadoR13.GlobalCapture.jsonl:112` `call_0fffb6019bcd457cbc761f34`
  (`rm -f /tmp/wayland-info.raw …`) is oracle-`clean-data-mention` and no tripwire
  finding. Both sides declare that limit (`OracleR13R14.md` "Residual limits";
  `RevTripwireContract.md` M7), and scratch-file cleanup is not a host-package
  mutation, so this is out of rubric rather than a counterexample.
- Scanned tool calls only: no execution receipt (`tool_execution_start` /
  `toolResult`) was consulted; that adjudication is `AuditTripwireOnly*`'s scope.

## Confidence

High for the mechanical claim: all four lists reproduced empty from digest-stable
inputs, under both the declared key and the stricter same-tool-call key, and the
counterfactual flips exactly the three python-heredoc rows. Medium-high for
"no non-clean oracle row is missing for another reason": the exact-call test covers
all four rounds, but the oracles are unaudited artifacts (D2). High confidence that
D1 is a text defect in the evidence file; its effect is interpretive, not a missed
command.

Report: `.ufo/waves/round-17/w2/reports/AuditOracleOnly.md`
