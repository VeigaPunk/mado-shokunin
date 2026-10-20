# ReviewReceipt — rendered report (mado-r14-w1, seat MadoR14.ReviewReceipt)

**Status: advisory, rejected design.** Parent integration decision: no receipt wrapper ships; H1–H4 and M1–M8 are not adopted as gate changes. Retained as record only.

Full findings with line anchors: `.ufo/waves/round-14/w1/ReviewReceipt.md`. Same content; this copy is the rendered report.

Verdict: the planned receipt wrapper is not implementable as written. Blocking: H1 refusal exit 2 collides with child exit 2; H2 digest comparison can fail open (never fall back to a literal `unavailable`); H3 the wrapper cannot receipt uncommitted gate edits this round; H4 generic COMMAND output persistence breaches the data fence. Round-13 missing-header case (R13-V3): `gate-selftest.txt` carries no revision or gate digest and its binding is recovered only from external records (`95cbc41`, `59cfbdc`, `7dcb785` all appear). The receipt header must carry revision, resolved SHA, whole-file gate digest and `exit=N`.

## Severity-ordered findings

| ID | Sev | Finding | Evidence |
|---|---|---|---|
| H1 | High | Refusal exit 2 = child exit 2; need `RECEIPT: REFUSED` marker and file-absence rule | `tools/mado-verify.sh:12-13`, `:1903,:1913,:2024`; `w1/ReviewRegistry.md:83` (F4) |
| H2 | High | Digest fails open: `unavailable` fallback compares SAME; `git show \| sha256sum` masks git failure | `mado-verify.sh:2006-2008`, `:2091`, `:2208-2211`, `:3153`; `harness.sh:924` |
| H3 | High | Uncommitted gate edits cannot match REV; needs explicit decision (commit or expected-digest mode) | spec GateImplement; contract no-commit |
| H4 | High | Generic COMMAND output persisted; breaches session/identity fence | `corpus/lessons/round-13.md:13` (M4); `.gitignore:1` |
| M1 | Med | Stable receipt text undefined; `elapsed_seconds` nondeterministic; reuse `tool:`/`gate-sha256:`; pick `exit=N` | `round-13/evidence/gate-selftest.txt:8-9`; `round-14/evidence/census-before.txt:2`; `mado-verify.sh:2013-2014` |
| M2 | Med | Whole-file digest vs regression pin `PIN_MADO` are different digests; name the header digest | `mado-verify.sh:1823,:2006`; `w1/ReviewRegistry.md:86` (F7) |
| M3 | Med | TOCTOU mid-run; create race (`[ -e ]` then write); reserve `--output` with O_EXCL before COMMAND | `mado-verify.sh:1901,:2021` |
| M4 | Med | Exit precedence: signal → 128+N; never mask nonzero child rc with 0 | spec exit propagation |
| M5 | Med | Gate-only rule rc∈{0,1} must not be inherited silently | `mado-verify.sh:1909-1915` |
| M6 | Med | Capture vs pass-through; gate merges streams and loses newlines | `mado-verify.sh:1906-1908`, `:1182` |
| M7 | Med | `--snapshot` already is a v1 receipt; extend it or justify a second format | `mado-verify.sh:1851-1855`, `:2011-2036` |
| M8 | Med | Receipt binds gate bytes, not verdict or cross-revision output equality (R13-V2) | `mado-verify.sh:83` (`ROOT=$HOME`); `round-13-verifier-spotcheck.md:204` |
| L1 | Low | Undefined lane root and `--output` base | spec |
| L2 | Low | Selftest must cover unresolvable REV, missing blob/gate, existing output, signal, mid-run change, non-hex digest; define "stable ids" | spec selftest sentence |
| L3 | Low | Red-before evidence absent; round-13 `UnboundLocalError` shows selftests catch real defects only when run | `round-13/evidence/frozen-selftest.txt:5-16` |
| L4 | Info | `git show` drops exec mode | `harness.sh:1489` |

## Axes

- **Coverage:** the wrapper adds R13-V3 coverage only if H2, H3 and M2 are resolved. A receipt that can say SAME for two `unavailable` digests adds no coverage.
- **Operability:** H1 and M4 decide whether a red run can be told apart from a refusal. M1 decides whether two receipts can be diffed.

## Residual risk and gaps

- No digest computed; current gate whole-file sha256 is unknown [UNK].
- `receipt.py` not yet present; re-review on landing.
- No selftest executed; refusal and mid-run paths unexercised [UNK].
- No external sources opened; no tools installed or updated.

## Checks for main agent (L1, once)

1. Resolve H1, H3, H4 before accepting the builder's `receipt.py`.
2. Decide M7 (extend `--snapshot` or new format).
3. Run `receipt.py --selftest` once red-before (broken digest compare) and green-after; assert every L2 case.
4. Treat `committed-bindings.json` digests as provenance only.
