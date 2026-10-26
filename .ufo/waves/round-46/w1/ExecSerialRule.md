Seat ExecSerialRule — D2 prose serial rule for the session-material gate

Target: round-45 closure item D2 (`corpus/lessons/round-45-verifier-spotcheck.md` §6 item 2) —
"teach the session-material gate a prose serial rule". Delivered as an advisory copy; the frozen
gate, the counters, the registrations and the reference are untouched.

Status: complete, no lane commit. Verdict: rule implemented, shown able to fail on the 24 held
files and to pass on a projected tree, with a measured false-positive rate of zero on the whole
tracked tree at the tip.

The serial value never appears in this directory. It was read once per command from
`hyprctl monitors all -j` into a shell/Python variable that was never echoed; every artefact here
holds paths, line numbers, counts and a run-length shape mask. Proof: `receipts/seat-scan.txt` —
scanning every byte of this seat with both rules and the live value reports 0 files.

## 1. What landed

| path | what |
|---|---|
| `.ufo/waves/round-46/w1/ExecSerialRule/gate.py` | extended copy of `quality/check-session-material.py` (991 lines; 22 original selftest cases preserved, 23 added). Frozen original sha256 `889f8f05…`; copy sha256 `a36224e2…`. |
| `.ufo/waves/round-46/w1/ExecSerialRule/receipts/` | 14 receipts + `commands.sh` + `verify-quote.py`, all value-free. |

Diff surface against the frozen original: one docstring section (R5/R6, `--scope`, `--rules`,
FP statement, limits), two constants (`SERIAL_PROSE_RE`, `HOST_CMD`/`SERIAL_MIN`), `R5`/`R6` in
`RULES`, `_shape_mask`/`serials_from_json`/`host_serials`/`_parse_rules` helpers, R5/R6 blocks at
the end of `scan_blob`, a `paths`/`scope`/`serials`/`rules` parameter chain through
`list_tree`/`run`, `--scope`/`--rules`/`--serial-from-host` in `main`, and the new selftest
fixtures/cases. No existing rule's logic, message or exit code changed.

## 2. R5_SERIAL_PROSE — the rule

Pattern (a monitor-serial / EDID shape standing as a whole token):

```
(?<![0-9A-Za-z])[0-9]{2,6}[A-Z]{3,8}[0-9]{3,7}(?![0-9A-Za-z])
```

Digit-run, then capital-run, then digit-run; no alphanumeric neighbour, so `X<token>` glued to a
prefix and tokens inside longer identifiers do not match. It runs on any text blob in scope, so it
also closes the R3 hole for a `serial` JSON value that has no identifying key (case
`r5-json-serial-without-ident`).

**False-positive rate on the whole tracked tree** (rev `4d22eeb`, 17305 tracked files, 68953
distinct upper-or-digit tokens found in 4-32 character alphanumeric runs, `receipts/sweep.txt`):

| measurement | result |
|---|---|
| rule as implemented, through the shipped code at `4d22eeb`, `b22ea56`, `e0be61e` | 24 tokens in 24 carrier files, **0 tokens / 0 files elsewhere** |
| analytic sweep, identical bounds (`receipts/sweep.txt`) | 1 matching distinct token, 24 files |

The shipped-code run is the authoritative count (it uses the real regex, including the 6-digit
first-run ceiling the sweep capped at 5); the sweep is the sensitivity analysis below. **FP = 0
tokens, 0 files.**

The threshold is not a knife edge; the sweep moves one bound at a time:

| variant | carrier files | other files |
|---|---|---|
| start run `[0-9]{2,5}`, caps `[A-Z]{2,8}`, end run `[0-9]{2,6}` | 24 | 8 |
| start `[0-9]{2,5}`, caps `[A-Z]{3,8}`, end `[0-9]{2,6}` | 24 | 1 |
| start `[0-9]{2,5}`, caps `[A-Z]{3,8}`, end `[0-9]{3,7}` | 24 | 0 |
| start `[0-9]{4,7}`, any caps, any end | 0 | 2 at a 2-digit end run, 0 otherwise (the carrier's first run is 3 digits, so this bound misses it) |
| caps `[A-Z]{6,8}` | 0 | 0 (misses the carrier) |

The chosen form keeps a margin on all three runs: the carrier's runs are 3 digits / 5 capitals /
4 digits, inside `2..6` / `3..8` / `3..7`. A wider cap bound (`[A-Z]{2,8}` with a 2-digit end run)
is where the first false positive appears, at 8 files.

Why a new rule is needed at all: the frozen gate's R3 is key-driven — its docstring scopes it to
"a JSON object with a non-empty `serial` plus a non-empty `description`, `make` or `model`"
(`quality/check-session-material.py:26-28`), `_monitor_reason` requires exactly that
(`:102-108`), and the scan is called with the key prefilter `"serial"` plus the three identity
keys (`:222-224`). Prose has no such object, so all 24 carriers
pass it: the frozen gate's 97 findings cover 95 distinct paths and intersect the carriers in 0
files (`receipts/frozen-gate-tip.txt`).

Findings carry `count=`, plus `shapes=` as a **run-length** digit/capital mask (`9x3+Ax5+9x4`),
never the token. The mask is delimited on purpose: a plain character mask would itself read back
as a serial-shaped token and poison any receipt that quoted the finding (found in this seat's own
first receipts and fixed before the runs above).

Declared residuals: a serial written in lowercase, with separators, with a capital run of two or
fewer, or ending in fewer than three digits is **not** matched by R5 — R6 covers those; and a
non-serial token of the same shape **is** matched (today: none in this tree).

## 3. R6_SERIAL_EXACT — `--serial-from-host`

Reads `hyprctl monitors all -j` (one read, the only non-git subprocess the gate starts), extracts
every non-empty `serial` of length >= 4, and counts each as a plain substring in every blob in
scope — shape-independent, and blind-provider-free because it comes from the compositor. Output is
`count=` and `sources=` only. Failure paths are exit 2, never a silent pass: binary missing,
non-zero exit, non-JSON, or no non-empty serial. It is refused when `--rules` excludes it, and
`--rules` including it without the flag is refused too. The parsing half
(`serials_from_json`) is unit-tested offline against a synthetic dump, an empty/blank serial, a
too-short serial and garbage.

## 4. Demonstration

| what | command shape | result | receipt |
|---|---|---|---|
| frozen gate is blind to it | `quality/check-session-material.py --repo . --rev 4d22eeb` | `findings=97` over 95 distinct paths, exit 1, **overlap with the 24 carriers = 0** | `frozen-gate-tip.txt` |
| carriers | `git grep -n -F <value> 4d22eeb` | **24 files, 1 line each**: 3 under `corpus/knowledge/` (`config-health-report-r3.md:149`, `hyprctl-verification-layer.md:153`, `hyprland-config-plane.md:184`) + 21 copies under `.ufo/waves/round-32/…` and `.ufo/waves/round-37/…` | `serial-carriers.txt` |
| **fails** at the tip, historical scope | `gate.py --repo . --rev 4d22eeb --serial-from-host --rules R5_SERIAL_PROSE,R6_SERIAL_EXACT` | `R5_SERIAL_PROSE=21 R6_SERIAL_EXACT=21`, `files=17070 findings=42`, exit 1 | `tip-scope-ufo-r5-r6.txt` |
| **fails** at the tip, whole tree | same `--scope all` | `R5=24 R6=24`, `files=17305 findings=48`, exit 1 | `tip-scope-all-r5-r6.txt` |
| the leak predates the round | same at base `b22ea56` | `R5=24 R6=24`, `files=17306 findings=48`, exit 1 | `base-scope-all-r5-r6.txt` |
| still exact at the round-46 freeze/controls HEAD | same at `e0be61e` | `R5=24 R6=24`, `files=17340 findings=48`, exit 1; the 24 are the same carriers, **0 new** since `4d22eeb` | `head-r46-r5-r6.txt` |
| additive, not a rewrite | tip `--scope all`, all six rules | `findings=150` = 97 (`.ufo` pre-existing) + 5 (outside `.ufo`, pre-existing) + 48 new; R1/R2/R3/R4 unchanged | `tip-scope-all-all-rules.txt` |
| **passes** on a projected tree | clone at `4d22eeb`, 24 files rewritten (`24 insertions(+), 24 deletions(-)`), 0 residual occurrences, `--scope all --serial-from-host --rules R5_SERIAL_PROSE,R6_SERIAL_EXACT` | `files=17305 findings=0`, **exit 0** | `projected-scope-all-r5-r6.txt` |
| the pass is the rule's, not the tree's | same projection, all six rules | `findings=102` = 150 − 48; R5/R6 absent | `projected-scope-all-all-rules.txt` |
| selftest | `gate.py --selftest` | `passed=45/45 failed=0` (22 original + 23 new), exit 0 | `selftest.txt` |
| the gate does not trip itself | `scan_blob(gate.py, serials=<value>)` | R1/R2/R3 fire on its own fixtures exactly as the frozen original does; **R5 and R6 absent**; value not in bytes | `self-scan.txt` |
| this seat is value-free | scan every seat file with R5+R6 and the live value | `files_hit=0` over 18 files | `seat-scan.txt` |
| the one quoted sentence is real | `receipts/verify-quote.py` | quote 14 words, found in the frozen file's lines 26-28, frozen sha256 still `889f8f05…` | `verify-quote.txt` |

Fixture repos were `mktemp -d` under `/fast/scratch/hyaku/mado-r46/ExecSerialRule`, each asserted
with `git -C … rev-parse --show-toplevel` before the one commit under a scratch identity. Scratch
is deleted at the end; nothing here cites a scratch or `/tmp` path as evidence.

## 5. D2's own correction (M45-2 undercount)

M45-2 named **one** held file; the serial is in **24**:

| scope | files | lines |
|---|---|---|
| `corpus/knowledge/` | 3 | `:149`, `:153`, `:184` |
| `.ufo/waves/round-32/` | 18 | same three lines, 6 copies (assimilation, c1/controls ×2, scratch/fixtures ×3) |
| `.ufo/waves/round-37/` | 3 | same three lines, 1 copy |

All 24 are pre-existing: `git diff 0c89478 4d22eeb | grep -c -F <value>` = 0, and the rule reports
the same 24 at base `b22ea56`. So the undercount is a *count* defect, not a round-45 introduction,
and round 45's data commit is not the source.

## 6. Risks, blockers, and what this seat did not do

- **Removal is not this seat's move.** The 24 carriers stay exactly as they are; a projection is a
  commit the L1 must decide (history rewrite stays the operator's call, as closure D2 says).
- The gate copy is **advisory until the L1 integrates it** into `quality/check-session-material.py`.
  If it is integrated, D3 (a registry row in `SKILL.md`) still applies to the whole gate, and
  `--scope all` will surface **5 additional pre-existing findings outside `.ufo/`** (R1 +1, R2 +3,
  R3 +1) that the historical scope never reported — triage budget, not a new leak.
- R5 is a **shape** rule with a declared blind spot (§2); the exact mode is the backstop and needs
  the host, so an offline CI run gets R5 only.
- `--serial-from-host` costs one compositor read; on a headless runner it exits 2 by design. It
  must not be wired into a gate that would then be red for the wrong reason.
- No tool installed (no package transaction, no `uv`/`npm` install): Python 3 stdlib and `git`
  were enough. No host mutation, no Wayland client, only the allowed `hyprctl monitors all -j`
  read. No lane git mutation: nothing was added, committed or checked out in the lane.
