# RevManifestIntegrity — round-38 wave-1: manifest audit + v2 13/19 reproduction

Seat: reviewer (leaf, no subagents). Date 2026-10-25. Scope: `.ufo/waves/round-38/controls/manifest.json`
structure and semantics, expect-vs-contract sanity per control, note accuracy, and reproduction of the
recorded v2 score 13/19. Lane was read-only; all writes were my report, this file, and scratch under
`/tmp/mado38-RevManifestIntegrity/`. No lane git/jj mutation; no installs (none needed); no LSP device in
this session's toolset — verification is execution-based (gate replays + counter replays on retained
sandboxes), which is stronger than static checks here anyway.

## 0. State audited and pins

The lane moved during the audit (HEAD `3f14bd2` → `bb1adce`/`f0c9432`/`b6c1d31` seen, then jj seat-fix
folds to `3674cf2` with `b8400aa`, `ff81aaf`, `c44873e`, `22f600f`, `3674cf2`). All replay inputs were
therefore pinned by bytes, extracted via `git show`, and re-hashed; the worktree manifest equals the
pinned HEAD manifest (`96965518…`), so the audit applies to the file as it stands.

| pin | sha256 (prefix) |
|---|---|
| gate @58e55ec (freeze) | `529569f692e653b5…` |
| gate @HEAD | `581bf2eda726de45…` |
| manifest @58e55ec (freeze) | `14c49d9fec35dc9b…` |
| manifest @HEAD (= worktree) | `96965518dc8ad98b…` |
| c1 v2 `c1-r37-event-ground.py` | `1c21f8ba736bf8c1…` (identical 58e55ec↔HEAD) |
| c2 v2 `c2-r37-eventq.py` | `6fae177fd5f42d7b…` (identical 58e55ec↔HEAD) |
| c1 v3 `c1-r38-event-ground.py` @HEAD | `6872e18d3003b5fc…` |
| c2 v3 `c2-r38-eventq.py` @HEAD | `194a45c68f9e5756…` |

Semantic freeze→HEAD manifest delta (JSON-level per-control comparison, not textual): **exactly one
control changed — `c1-duprow`** (op `append`-at-EOF → `py` insert-after-the-`| S217 |` Registry row).
Every other control's instrument/expect/clause/note/writes are byte-identical, and the top-level note is
unchanged. The 353-line git diff is format churn, not semantics. Note: `b6c1d31`'s message also claims
"c2-docconn updates receipt sha", but docconn's sha-updating write is already present at 58e55ec — no
semantic manifest delta exists for it.

## A. Structural audit of the manifest — PASS with notes

1. **Valid JSON.** `python3 -c "import json;json.load(...)"` → `JSON_OK controls= 19`. Top keys
   `id` (`MANIFEST-r38-v1`), `frozen_at` (`2026-10-25`), `note`, `controls`.
2. **Required fields.** All 19 controls have `id`, `instrument`, `expect`, `clause`, `note`.
   `writes` is present on 15 and absent on exactly the four controls that are checkout-only by design —
   `c1-live` (:7-12), `c1-donothing` (:14-20), `c2-live` (:122-127), `c2-donothing` (:129-135). The gate
   reads `ctl.get("writes", [])` (check-r38-discrimination.py:154), so absence is safe, and the manifest
   note explains the mechanism ("`rev` names the sandbox clone's checkout"). Ids unique (19/19).
   Extra keys: only `rev` on the two donothing controls (`b4e47e980bfb0cbc8a4e788f59a41db858751fd8`,
   verified to exist, subject "round-36 verifier spot-check"). No control sets `base` (the gate's
   `--base` extra-arg path is dead for this manifest; the counters' `BASE_DEFAULT` is the same
   b4e47e9).
3. **Sandbox-relative paths.** Programmatic AST + field scan over every write op
   (`literal/file/append/delete/counter_fixture/tool_run` `path`/`ss` fields; `py` code
   `write/append/delete/digest/read` first args): **zero absolute paths, zero `..` segments** in any
   write. The single outside-sandbox reference is an absolute **read** in `c1-r28-verbatim` (Finding F3).
   `instrument` ∈ {c1,c2}; `expect` ∈ {TARGET_MET ×3 — c1-live, c2-live, c2-docconn; TARGET_MISSED ×16}.
4. **donothing rev sanity.** At `b4e47e9`: no `corpus/knowledge/event-delivery-limits-r26.md`, no
   `event-queue-observability-r37.md`, no `tools/mado-eventq.py` (`git ls-tree -r` matches only round-33
   fixture copies under `.ufo/waves/round-33/`). Replays: c1 `admitted=0/2` with every clause 0;
   c2 `tool=absent`, `fixtures=0/10` (v2) / `0/14` (v3) → both TARGET_MISSED. `expect` sane.

## B. expect sanity — clause-level replay on retained sandboxes

Method: the freeze-gate (no cleanup) retained all 19 per-control sandboxes of the v2 run; I re-ran both
instruments against each (`--repo <sb> --rev HEAD`) and captured per-clause flags. HEAD-gate v3 verdicts
come from run C below (that gate deletes its per-control sandboxes — an operational difference of the
b8400aa confinement fold, not a defect).

| control | expect | v2 observed (clause that decided) | v3 observed (clause that decided) | sane? |
|---|---|---|---|---|
| c1-live | MET | MET (a–g all 1) | MET (lineage 6/4, 2/2) | yes |
| c1-donothing | MISSED | MISSED (all 0) | MISSED (all 0) | yes |
| c1-selfreceipt | MISSED | MISSED — **placement**: c=0,d=0 (F1) | MISSED — h=0 (S999∉PINS) + placement | yes, see F1 |
| c1-quotefloor | MISSED | MISSED — d=0 via **mangled GATE lines** (F2), f=0 | MISSED — h=0 (floor), d=0 | yes, see F2 |
| c1-duprow | MISSED | MET (v2 `any()` accepts dup row; freeze variant even lands outside Registry) | MISSED — j=0 (dup row now inside Registry at SOURCES.md:220) | yes; the post-freeze control edit is what makes v3's j bite |
| c1-nolineage | MISSED | MET (v2 has no lineage clause) | MISSED — l=0 (lineage 2/4, 0/2) | yes |
| c1-r28-verbatim | MISSED | MET | MISSED — l=0 on E2 (0/2), g=0 | yes |
| c1-token-stub | MISSED | MISSED — g=0 (held) | MISSED — g=0, l=0 | yes |
| c1-clause-b | MISSED | MISSED — b=0 (held) | MISSED — b=0 and k=0 | yes, see F4 (attribution) |
| c2-live | MET | MET (v2 live clause) | MET (live-detail all 1s, proc 3/3) | yes |
| c2-donothing | MISSED | MISSED (tool absent) | MISSED (tool absent) | yes |
| c2-forged | MISSED | **MET** — the recorded F1 hole (v2 trusted any receipt+snapshot) | MISSED — proc 0/3, sha_in=0 | yes |
| c2-impsock | MISSED | MISSED — v2 readonly=0 catches plain `import socket` | MISSED — readonly=0 | yes, see F4 (weaker than cited F6 crib) |
| c2-lagconst | MISSED | MISSED — live=0 (v2's `tool_sha256` pin; fixtures 10/10 = the undiscriminated battery) | MISSED — case=clean ok=0 (lagging-clean), live=0 | yes |
| c2-missall | MISSED | MISSED — live=0 (sha pin); v2 battery has no expect-present case | MISSED — case=expect-present ok=0 | yes |
| c2-onepass | MISSED | MISSED — fixtures 8/10 (clean, lagging fail) + live=0 | MISSED — 6 fixture cases incl. clients-first | yes |
| c2-docconn | MET | **MISSED** — v2 readonly=0 (`connect(` in docstring) | MET — readonly=1 (code_lines strips docstring), sha updated by control | yes |
| c2-stub-clean | MISSED | MISSED — fixtures 1/10 (held) | MISSED — 1/14 | yes |
| c2-proc-mismatch | MISSED | **MET** (v2 has no proc clause) | MISSED — proc 0/3, sha_in=0 (`ss_sha256=000…0`) | yes |

Every `expect` matches what the writes actually produce under the instrument that must score it. The six
v2-mismatches are exactly the documented v2 holes (M37-5 / RevC2Code F1, F4, F5, F6-false-miss) plus the
two v3-only live-clause cribs — coherent with the round's claim structure.

## C. Findings by severity

**F1 (moderate) — `c1-selfreceipt` cannot reproduce the hole it documents; its artifacts land outside
the sections both counters parse.**
The control appends the S999 SOURCES row at EOF (`append` op, manifest :33-37) and the `GATE S999` lines
at EOF of `corpus/lessons/round-37.md` (manifest :38-42). But `## Registry` in SOURCES.md ends at
`## Paths` (:221; later `## Search log` :267, `## Leads (unopened)` :431), so the S999 row lands under
`## Leads (unopened)` — sandbox tail shows it as the file's last line. And in round-37.md `## Gate` spans
:18-79 while the appended lines sit at :119-120, under `## considerthese` (:108). `section(text,
"## Gate")`/`registry_rows` therefore never see either artifact. Measured: v2 replay `c=0 d=0 … ok=0`
(kill = placement), v3 replay `h=0 j=0 c=0 d=0` — h fires for the right reason (S999 has no pin), but
`d=0` would fire anyway. Consequence: the control's MISSED is overdetermined — a counter with **no**
self-receipt detection still scores MISSED here, so the control cannot detect loss of the anti-crib
machinery; and the recorded v2 `ok=1` rests on placement, not on the M37-5 F1 hole (that hole, per
CritC1Cheap.md:57's `k3`-style trees and round-37.md:95, requires section-correct wiring). Fix shape:
insert the row inside `## Registry` (as duprow now does) and the GATE lines inside `## Gate`.

**F2 (low) — `c1-quotefloor`'s regex collides with inner-quoted GATE lines; the v2 kill is conflated.**
Pristine gate lines contain inner quotes, e.g. S212 `quote="m_ipc.registerForIPC("workspacev2", this);"`
and S213's JSON quote. The control rewrites `quote="[^"]*"` → `quote="e"`, truncating at the first inner
quote: sandbox shows `GATE S212 … quote="e"workspacev2", this);"` and
`GATE S213 … quote="e"option":"debug:disable_logs",…}"` — `GATE_RE` (`quote="(.+)"\s*$`) no longer
matches, so S212/S213 gates are silently dropped. v2 has no quote floor (its d accepts `'e'` since
`b'e' in blob`), so the recorded v2 kill for this control is the mangled lines + erased tokens (f=0), not
the documented F2 floor. Under v3 the floor does bite (h=0 via `quote_floor_ok` for the clean S189/S201
lines) but the mangling is still in the mix. Expect value correct under both instruments; the control
does not isolate the hole it cites. Fix shape: rewrite only `quote="[^"]*"$`-anchored lines, or use
quotes without inner `"`.

**F3 (low) — `c1-r28-verbatim` reads an absolute host path; py ops are not hermetic.**
manifest :91: `pkg = open('/home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge/
event-queue-host-measurement-r28.md').read()`. It is a READ (shokuknow is declared read-only and the file
exists today: 2132 B, 2026-10-24), and no control writes outside the sandbox — but if that host file is
absent at replay time, `apply_writes` raises → `observed=ERROR ok=0` → a spurious discrimination failure.
The b8400aa confinement (`_confine`) wraps the helper lambdas but py-op code still executes with full
builtins (`open`), so the helper confinement does not cover this form. Cross-ref RevGateScript (gate env
hardening is that seat's scope); recommend reading the pasted text from a committed receipt instead.

**F4 (info) — top-level note and two per-control notes: incomplete/misattributed.**
(a) The top note enumerates 10 M37-5 cribs + 3 held discriminations = 14 of the 19; `c1-clause-b` and
`c2-proc-mismatch` are unnamed, and "Accept controls prove the instruments still accept … the real tool"
does not cover `c2-docconn` (expect MET but a modified tool + rewritten receipt). The registration's
control list (registration.md, Controls §) is complete — only the manifest's own note is short.
(b) `c1-clause-b`'s note says "the clause b control M37-5 named"; the M37-5 bullet (round-37.md:95) does
not name it, and the documented hole is `verified-at: x` (CritC1Cheap.md:78) — a value-format hole that
v3's clause k addresses. The control instead strips the header (clause b), which v2 already caught
(recorded MISSED ok=1 = held discrimination). No control feeds a present-but-malformed header, so v3's k
format-half is exercised only jointly with b (cf. F5).
(c) `c2-impsock`'s note cites RevC2Code F6, whose crib was `import os, socket` / `__import__('socket')`
(RevC2Code.md:183-189 — all gave `readonly=1`, i.e. bypassed); the control uses plain `import socket`,
which both v2 and v3 catch. As a reject control it is fine, but it does not exercise the bypass — and the
bypass form would fail the v3 target (v3's regex `\bimport\s+socket\b|\bfrom\s+socket\b` also misses
`import os, socket`), which is presumably why the killable form was chosen. Residual for the counter
owner, declared here not hidden.

**F5 (info) — clause field semantics.** The c1 clause letters match the v3 docstring's own letters
(h=pin binding, i=quote floor, j=unique row, l=lineage; b/g are v2's), and each c2 clause name
(`tool`, `live-v3`, `readonly`, `lagging`, `expect-present`, `clients-first`, `readonly-doc`,
`fixtures`) names the mechanism my replays show firing. Two nuances: v3's printed per-entry flags have
no `i` (the floor is folded into h/d via `quote_floor_ok`), and h's pin-digest half and k's format half
have no isolating control (selfreceipt/quotefloor/clause-b are each killed by other clauses as well) —
the mutation kill-tables (MutC1/MutC2 seats) should show those clauses surviving single-clause removal.

**F6 (info) — receipt provenance (reinforces RevCommitChain F8).** The recorded
`before-discrimination-v2.txt` / `after-discrimination-v3.txt` carry no rev/manifest/counter digests.
This report supplies that provenance by replay (§D); the pins in §0 are the identity the results below
belong to.

## D. Recorded 13/19 — reproduced

Commands (all from `/tmp/mado38-RevManifestIntegrity`, inputs = §0 pins, `--rev 58e55ec` = freeze rev;
v2 counter files are byte-identical at HEAD, verified):

- **Run A (freeze-faithful):** `python3 -I pins/freeze/gate.py --c1 pins/freeze/c1v2.py --c2
  pins/freeze/c2v2.py --manifest pins/freeze/manifest.json --rev 58e55ec` → per-control output is
  **line-identical to the recorded `.ufo/waves/round-38/receipts/before-discrimination-v2.txt`**, ending
  `MADO_R38_DISCRIMINATION: controls=19 correct=13/19 verdict=TARGET_MISSED`; clean re-run exit code 1
  (`runs-A-clean.txt`, sha256 `25064ccc159b4fe1…`). The six `ok=0` controls are exactly the recorded set:
  c1-duprow, c1-nolineage, c1-r28-verbatim, c2-forged, c2-docconn, c2-proc-mismatch.
- **Run B (HEAD manifest × v2):** same 13/19, same six → the recorded number does not depend on which
  side of the post-freeze manifest edit it was made on.
- **Run C (HEAD gate × HEAD manifest × v3 counters):** `controls=19 correct=19/19 verdict=TARGET_MET`,
  exit 0 — matches the recorded `after-discrimination-v3.txt` line-for-line.
- **Independent errata confirmation:** replaying the v3 counter on the freeze-manifest c1-duprow sandbox
  gives `c=1 … j=1 … ok=1` on the delivery entry (the appended dup row sits at SOURCES.md:458, outside
  `## Registry`) → frozen manifest × v3 = 18/19, matching errata `c44873e` ("failure scope is the
  manifest control alone"); with the HEAD manifest the dup row lands inside Registry (:220, right after
  the S217 row) and v3 kills it (`c=0 … j=0 … admitted=0/2`).

First A/B/C attempts crashed writing `--out` because my `runs/` directory did not exist — harness error
on my side, not the gate's; full stdout was captured and the clean re-run (without `--out`) gives the
unambiguous exit 1. Retained evidence: `/tmp/mado38-RevManifestIntegrity/` (pins/, runs-A-clean.txt,
replay/<control>.<instrument>.txt per-clause logs, sbxA/ v2-run sandboxes).

## E. Residual risks and verification gaps

- The manifest is a v3-era artifact; under v2 its cribs kill via weaker mechanisms than the ones they
  cite (F1, F2, F4c). The 13/19 "before" number is real and reproducible, but three of its nineteen
  cells do not demonstrate the specific v2 holes the round narrative attributes to them.
- v3 clause isolation gaps (h-digest half, k-format half; no `i` flag) are inferred from clause replays;
  the definitive word will be MutC1/MutC2 kill tables, which I did not duplicate.
- v3's readonly regex still misses the RevC2Code F6 bypass forms (`import os, socket`,
  `__import__('socket')`, `connect_ex(`); no manifest control covers them (F4c). Counter-owner scope.
- The lane HEAD moved twice during this audit; my verdicts are pinned to §0 bytes. If further folds
  rewrite the manifest or counters, re-pin and re-run §D.
