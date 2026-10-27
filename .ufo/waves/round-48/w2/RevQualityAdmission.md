# w2 / RevQualityAdmission — hostile closure checklist on both frozen predicates

Scope: reproduce both frozen counters before/after on scratch clones built from committed bytes only; positive + do-nothing control each; hostile tampers; held-axis/corpus no-harm; separability. Leaf seat; no subagents; lane untouched. Scratch `/fast/scratch/hyaku/mado-r48/RevQualityAdmission/` (peak 807 MB, removed at end; receipts copied to `w2/RevQualityAdmission/`). This is a checklist, not an admission ruling.

## Inputs verified before any run

- [x] Freeze commit `3e6c848a` (HEAD), base `579f694b`; `claims.md`/`registration.md` read first.
- [x] `l1-draft/c1-r48-terminal-cache.py` = frozen `quality/counters/` bytes = `2a7d03d9…`; same for `c2-r48-xkb-entry.py` = `4a0e6924…`; `c1-r48-fixtures.json` = `4d946bd7…` = counter's `SHA256_WARM`. Overlay is byte-identical to the frozen instruments.
- [x] Pin `89f2be9a65deb8df…` = `.ufo/waves/round-47/fetch/xdg-terminal-exec` bytes = counter `PIN_SHA256`.
- [x] Clone toplevel asserted before every commit (`git rev-parse --show-toplevel` = clone dir); all commits in scratch clones only (`bd063a23` c1-before overlay, `522337b7` c1-after overlay, `4837dfc7` c2 mirror, `eab71a6b`/`e7c0ac9a` tampers, reset back).

## C1 `PRED-C1-r48` (counter at freeze commit, nonce 4848 = L1's nonce)

- [x] Positive control (reference draft tool `1dfde36c…`): `cold=190/190 warm=204/204 explained=394/394 generated=230/230 selftest=ok readonly=ok tool=present verdict=TARGET_MET`, exit 0 — byte-equal final line to L1 `l1-c1-ref-rfix.txt`/`l1-c1-ref-final2.txt`.
- [x] Do-nothing control (base tool `b84d5c4f…`, cold-only, warm out of contract): `cold=190/190 warm=134/204 explained=231/394 generated=210/230 selftest=fail readonly=ok verdict=TARGET_MISSED`, exit 1 — counts identical to L1 `l1-c1-base-final.txt` at the same nonce (same judge, no host drift).
- [x] Independent reproduction from committed bytes only (clone = base + overlay; counter read pin/fixtures by hash, tool blob by `git show REV`).
- [x] Nonce-derived generated cases (150+80) judged against the live oracle at count time; not precomputable (`--nonce` rides `clause=meta`).
- [x] Discrimination demonstrated on the merged fixture set: the cold-only base tool fails exactly the warm/explain/selftest clauses (the always-cold/cold-only control class from `ExecControlsC1`; full 20-control re-score remains w1's receipt).
- [x] Separability: counter source has zero `xkb` references; reads no C2 entry/registry/README.

## C2 `PRED-C2-r48`

- [x] Do-nothing control (rev = base, no entry): `clause=a entry_absent`, `admitted=0/1 TARGET_MISSED`, exit 1 — identical to L1 `l1-c2-before-base.txt`.
- [x] Positive control (c2-mirror recipe: entry + rows S340-S350 after S339 + README row + 14 fetch pins + receipt + `make-xkb-receipt.sh`, committed): `clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 r:1 admitted=1/1 verdict=TARGET_MET`, exit 0; live replay `replay=ok sha=efd487a39920 neg=(1,1,0) ver=1.13.2` — live `xkbcli` output digest matches the committed receipt on this host today.
- [x] Tamper T1 — one letter inside a cited quote (`Options can be empty, so resqect…` at `xkbcommon-context-priv.c:218`): `clause=d quote_not_in_pin line=35`, admitted=0, exit 1.
- [x] Tamper T2 — one byte appended to held row S318: `clause=h held_row_moved=S318`, admitted=0, exit 1.
- [x] Held/no-harm: base→admitted diff touches only the 19 new/3 intended paths above; `SOURCES.md` +11 rows, `README.md` +1 row, nothing else; S318/S319 rows, r46 entry (`eccd79a0…` blob-id equal) and round-47 `axis-tip.txt` (`9d2777cd…`) byte-identical base vs head; `quality/` untouched.
- [x] Census: `scripts/sources-census.sh validate` exit 0 on the mirror `SOURCES.md` (pre-existing W01 advisory on S277; W04 filtered per L1 recipe).
- [x] Separability: counter source has zero `mado-terminal` references.

## Findings by severity (no blocking defect found)

1. **MEDIUM (flake, claim-killing direction) — C1 clause r `readonly` has an observed false-trip mode.** L1's own `l1-c1-ref-final3.txt` shows `trips=2 ???( <detached …>` → `TARGET_MISSED` on the same reference that passes in 5 other L1 receipts and in both of my runs. `strace -f` reports detached bwrap/python reaping artifacts no tool code owns. Registration says any non-met result is a miss and fixes no re-run policy; a data-commit scored on such a day would be recorded a miss. Recommendation to L1 (predicate is frozen; informational): if a data-tip run misses with trips consisting only of `<detached …>` lines, one re-run before ruling is consistent with the falsify intent (flake kills nothing that is true).
2. **LOW (declared residual, restate for closure) — C2 trust root is mutual binding, not independent grounding.** Fetch copies and row digests hash each other; no upstream re-hash (`c2` docstring lines 11-13). A synthetic pin+digest pair with a stem-matching name and a tag URL passes c/d; clause r replays compiler behavior, not quote provenance. Already declared in registration residuals; closure should acknowledge it in the C2 admission sentence.
3. **LOW (declared) — C1 oracle-drift check covers variant A recorded `expect` only; variant B is tool-vs-oracle live** (docstring clause f/w). No action; part of the declared judge.
4. **INFO — `beside()` fixture fallback to lane `quality/counters`** is hash-pinned (`Setup` on any other byte), so post-integration runs cannot silently swap fixtures.
5. **INFO — environment note.** Host enforces RLIMIT_FSIZE soft 2048 (1 MiB) on agent shells; git index plumbing and one tracked blob (4,207,542 B round-20 `full-sweep.jsonl`) exceed it, so git plumbing/instrument shells ran `ulimit -f unlimited` (hard limit). Largest file I authored: seat evidence 9,254 B total; largest overlay copy 241,139 B (`c1-r48-fixtures.json`). Scratch peak 807 MB < 2 GB budget; removed.

## Self-authored evidence statement

Everything in `w2/RevQualityAdmission/` is self-authored reproduction output produced this session from committed bytes: the four replay logs (`replay-c1a-clauses`, `replay-c1b-clauses`, `replay-c2-before`, `replay-c2-after`), both tamper logs, `setup-digests.txt`, `largest-files.txt`. Non-self-authored corroboration relied upon: frozen counter/fixture digests, the pin digest, L1's w1 receipts (`l1-c1-base-final`, `l1-c1-ref-rfix`, `l1-c2-before-base`) used only for count-level comparison, and the committed host receipt whose digest clause r re-derived live (`efd487a39920`).

## Verification gaps (not exercised here)

- The 20 w1 C1 control mutants and the C2 POS/8 negative-control trees were not re-scored by this seat (w1 receipts exist; my do-nothing runs cover the cold-only class).
- C1 clause i mount allowlist was not independently probed beyond reading the bwrap argv construction; no `--print-*` live host observation was made (that is the data-commit receipt's obligation, not w2's).
- C2 clause d verbatim matching was exercised via tamper only on one span (18/18 quotes pass in the clean run).
