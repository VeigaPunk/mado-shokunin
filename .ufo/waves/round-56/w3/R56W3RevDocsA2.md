# R56W3RevDocsA2 — attempt-1 documentation fixes

Reviewed **0f3a54361a9824484d0801679ceb1fd8ac7c32e1**, not the working tree. Attacked the four named doc surfaces and w2/R56W2RevDocs F1–F6; no frozen predicate changed or rescored.

Axes: source accuracy; read/write-surface fidelity; sample reproducibility; documentation consistency.

## Findings by severity

### D1 — weakens the claim: PROVINCE read-surface fix is incomplete

`/home/vgpnk/Projects/shokunin/mado-shokunin/PROVINCE.md:33` still limits metadata calls to “on those paths only” after listing config/getoption/source files, while describing `--display-root` as only changing printing. The actual tool calls `os.path.realpath(root)` at `tools/mado-watchplan.py:195` even when root is unrelated to that closure.

Input: `--config /fast/scratch/hyaku/mado-r56/R56W3RevDocsA2/missing.conf --display-root /fast/scratch/hyaku/mado-r56/R56W3RevDocsA2/display-only`. The pinned tool exits 0; strace records:
```
newfstatat(AT_FDCWD, "/fast/scratch/hyaku/mado-r56/R56W3RevDocsA2/display-only", ..., AT_SYMLINK_NOFOLLOW) = -1 ENOENT
```
Exact unabridged syscall and command are in `receipts/syscalls.txt` and `receipts/docs-a2.txt`.

One-line correction: “Metadata checks also cover --display-root and path/symlink ancestors during realpath/glob resolution; byte reads remain config/source/getoption only.” The regular-file conditional and per-file cap corrections did land.

### D2 — weakens the claim: tool-ledger write surface disagrees with corrected PROVINCE

`/home/vgpnk/Projects/shokunin/mado-shokunin/quality/tool-ledger.md:129` still says “stdout only” without qualification. `/home/vgpnk/Projects/shokunin/mado-shokunin/PROVINCE.md:33` now correctly discloses the selftest's private temporary writes. Pinned tool lines 400–411 create directories/files/symlinks; lines 549–550 remove them. Executed with seat-local TMPDIR: `MADO_WATCH_SELFTEST: 86/86 assertions passed`, rc 0.

One-line correction: “Normal mode stdout only; --selftest writes only inside a private temporary directory it removes.” Normal prediction remains read-only; this does not falsify PRED-C2-r56-v2, whose selftest is expressly informational.

### D3 — weakens the claim, mild: README retains directory-registration overcompression

`/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/README.md:117` says “which inotify masks are registered for files and directories”; index row :82 likewise associates the regular-file source closure with “file and directory inotify masks.” The entry :42 explicitly says source directories are skipped, not added and not watched; tool :288–289 emits SKIP for them. A directory passed as the main --config can reach the model's directory branch, so this finding is **not** a claim that the branch is globally unreachable. For the normal regular-main-file/source closure described by the README, it still implies directory registrations the source traversal does not produce.

One-line correction: “Which masks the watcher defines for file and directory list entries (source directories are skipped), plus a second target watch for symlinks.”

### D4 — cosmetic: Frontier source inventory remains stale

`/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/README.md:117` names “rows S383-S391,” while the corrected index :82 says S383-S395 and the entry :1 cites S392–S395 for E01/E03–E07. The index fix landed; the parallel Frontier range did not.

One-line correction: “rows S383-S395 plus the host pins”.

## Per-item result / landed fixes

1. **FALSE overall** — Frontier chain and still-open list agree with the entry; source inventory and directory qualification remain D3/D4.
2. **FALSE overall** — PROVINCE config regular-file conditional, single getoption, source closure, 1 MiB/file and selftest exception agree with the implementation; metadata boundary remains D1. Arguments are parsed manually (`parse_args` :105–120), not by argparse.
3. **TRUE** — SKILL :226 now explicitly calls the answer a PREDICTION/model and points at declared divergences. Fresh sample run emits exactly:
```
MADO_WATCH_LIVE: option=misc:disable_autoreload config=0 live=0 verdict=AGREE
MADO_WATCH: DONE watches=40 unsupported=0 errors=0 live=AGREE
```
rc 0; full output byte-identical to canonical `.ufo/waves/round-56/receipts/live-watchplan.txt` (43 lines). No sample/output defect found by that comparison. The unqualified `hyprctl getoption misc:disable_autoreload -j` capture initially failed rc 1 because HYPRLAND_INSTANCE_SIGNATURE is absent; the permitted read-only `hyprctl -i 0 getoption misc:disable_autoreload -j` succeeded and supplied the fresh capture. The tool command itself was the documented command with the pinned executable staged in scratch.
4. **FALSE overall** — ledger and PROVINCE agree on normal prediction, flags and closure; the ledger lacks the now-documented selftest write exception (D2).

W2 F2 (runtime keyword/reload routes traced, not exercised) and F3 (prediction qualifier) are fixed. F1's index/source/host omissions are fixed but its Frontier inventory remains stale. F4/F5/F6 are partially fixed as above. No claim-blocking defect found within this doc-only scope; none of these findings changes frozen predicates.

## Commands, deliverables, limits

Canonical read command: `git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 0f3a54361a9824484d0801679ceb1fd8ac7c32e1:<path>`. Also inspected the actual `371d8234` doc diff and `0f3a5436 --stat`. The exact source/doc lines, commands, decisive outputs and per-item TRUE/FALSE are in:

- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w3/R56W3RevDocsA2/receipts/docs-a2.txt`
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w3/R56W3RevDocsA2/receipts/live-rerun.txt`
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w3/R56W3RevDocsA2/receipts/getoption.json`
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w3/R56W3RevDocsA2/receipts/syscalls.txt`
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w3/R56W3RevDocsA2/receipts/selftest.txt`

LSP device unavailable: reading `xd://lsp` returned “No such tool”; references, definition and diagnostics did not run. Implementation review used canonical blob text plus a syscall reproduction, not text search presented as semantic proof. No /proc reads, config writes, reload, keyword, dispatch or service changes. No tool installed or updated. No clone/archive or git mutations. Only the pinned watchplan runtime was invoked; no alternate runtime, judgment, integration or shipping.

Not run: C1/C2/C3 counters or harnesses, harness/counter write-surface rechecks from the broader w2 F4, full source-to-upstream re-audit, or actual compositor reload behavior. Directory caveat is grounded in the canonical entry and tool, not a new compositor experiment. One host sample does not establish all model branches or saturation.

Self-evaluation: accuracy 4 (metadata syscall reproduced; directory finding intentionally qualified), completeness 4 (all four assigned checks covered; LSP unavailable), clarity 4 (per-item receipt plus severity report), actionability 5 (one-line correction per defect), conciseness 4 (full quotes kept in receipt rather than repeated here); overall 4.2. Main improvement opportunity: use a mounted LSP if available in a future review. Would the user agree: likely, because successful sample reproduction and remaining doc defects are separated.
