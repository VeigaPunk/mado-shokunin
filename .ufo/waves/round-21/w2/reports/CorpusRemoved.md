# Round 21 W2 — frozen corpus comparator review

## Axes and scope

Axes: corpus membership/completion, input and tool hash identity, finding-delta integrity, and fail-closed error handling. This is a read-only review of `.ufo/waves/round-21/corpus/compare.py` at `f499a8db7171b7476fe9f204ab9edbac5a956fa9`; no production files or fixtures were changed.

Reviewed comparator SHA-256: `9296ab496a1aeb6f06d7665e3a525c06ac7003ce0e58289b065e33a81cad86f5`. Current candidate source SHA-256 (recorded, not executed): `tools/mado-tripwire.py` = `2e152f6dcd9a0d13ffc1d64e88bcc600548e66bd04c34f92dbc5a0808338372d`. `compare.py` is unchanged from the historical run's runner hash. The current manifest bytes match the pinned manifest SHA-256 `8e1cf206c85563b418630ef1d094559a9522431ff4e077ca1b51f249436a1377`; parsed manifest metadata and `files` array both report 1,356 paths, with 1,356 distinct path strings.

LSP was unavailable: `read xd://lsp` returned “No such tool” and listed the mounted devices without an LSP route. Literal grep was used only as fallback for references/schema discovery, not as semantic proof; behavior findings below cite the comparator source directly. No tools were installed. I did not run the comparator, a scanner probe, or a full-corpus scan.

## Findings (severity order)

### High — scanner output is not authenticated; candidate code can forge a complete run

`.ufo/waves/round-21/corpus/compare.py:38-55, 76-86` imports and calls the candidate module inside the worker, then writes the worker protocol to that same process's stdout. The parent captures that stdout and accepts it if the child exits zero, the number of JSON lines equals `len(data['files'])`, and each before/after row has the same path. It does not authenticate that the worker emitted each row or independently compare each output path against the manifest.

[INFERENCE — static attack path, not executed] A candidate module can write 1,356 syntactically valid, manifest-ordered result lines to stdout during import and call `os._exit(0)` before `scan_file` is called. The parent sees a zero exit and a full-length stream; paired path checks cannot distinguish it from worker output. The candidate can therefore fabricate findings (including baseline-equivalent rows if it knows or obtains the baseline) and suppress a real removed/relabelled delta. Count/order checks establish stream shape, not scan completion or provenance. Do not use this comparator as independent evidence against adversarial or stdout-controlling candidate code until the scanner and protocol emitter are separated by a trusted boundary and completion/results are authenticated.

### Medium — reported tool/runner hashes are post-run path hashes, not hashes bound to loaded bytes

At `.ufo/waves/round-21/corpus/compare.py:76-77`, workers resolve and import the tool path; the result hashes `args.before_tool`, `args.after_tool`, and `Path(__file__)` only after both workers finish (`:95-99`). There is no pre-load digest check or immutable byte snapshot. A candidate running in the worker can rewrite its own source (or change a path/symlink between runs); the report then hashes the later bytes rather than necessarily the bytes imported. Thus a result can be attributed to the wrong tool SHA even when the recorded output fields are internally valid. This is a static capability finding; I did not execute a mutating candidate. Bind each digest to the exact bytes loaded before execution and retain that binding in the report.

## What currently fails closed

The pinned manifest hash and per-row file hashes are checked in `manifest()` (`:17-29`); missing/mismatched input files raise instead of silently shrinking the population. On a normal worker path, the worker emits one row per manifest entry. The parent rejects nonzero worker status or a row count different from the pinned manifest (`:73-80`), rejects before/after path-order mismatches (`:84-86`), and treats any per-file error as an error rather than comparing that file as clean (`:87-100`). Error-bearing results return status 1; malformed stdout/JSON, uncaught worker failures, and outer 600-second `TimeoutExpired` abort rather than produce a successful comparison. These checks are useful for accidental failures, provided callers require both a complete report and exit status 0. The high-severity finding above defeats the stdout/count/order checks because the candidate shares the worker's process and output channel.

A weaker resource-boundary caveat: the 15-second `SIGALRM` is installed in the same interpreter as candidate code (`:44-55`), so candidate code can replace the handler or cancel the alarm. The outer 600-second timeout still prevents indefinite parent waiting, but the per-file limit is not an isolation boundary. No timeout-bypass probe was run.

## Historical evidence and verification gaps

The committed `.ufo/waves/round-21/evidence/corpus-comparison.json` records a historical run at `2ac0f9ba69051aea22cab3b6cfebe4d906b72d17`, not the current candidate. Its captured comparator output reports 1,356 files, 834 retained findings, 33 removed/relabelled, 77 added/relabelled, and 108 per-file errors; the receipt's top-level exit is 1. Its `runner_sha256` is the same `9296ab…86f5`; its before/after tool hashes are `a57d4fe9…b5b6458` and `7f41b0e8…83866ea`. This demonstrates that the historical error-bearing run was not reported as successful and that its removed/added arrays were retained in the receipt. It is not evidence of the corrected `f499a8d…` corpus result.

No fresh full-corpus execution was performed, as assigned. I verified the manifest file digest/count and reviewed the source hash-check loop, but did not independently recompute every one of the 1,356 payload-file digests. Current candidate full-corpus loss/relabel/error totals therefore remain unverified; do not carry forward the historical 33/77/108 counts as current results. The comparator itself does not explicitly assert that manifest metadata `file_count` equals `len(files)`, but the currently pinned manifest's observed metadata and array length agree at 1,356.

## Verdict

The path/hash checks and explicit nonzero handling are fail-closed for ordinary incomplete/error runs. However, the shared untrusted worker stdout/process boundary allows a fabricated complete run, and post-run hashes do not bind execution to the reported candidate identity. **Recommendation: comparator output is not sufficient for C1 adjudication against candidate-controlled code until those provenance gaps are closed.** No current corrected-candidate corpus conclusion is made.

Report: .ufo/waves/round-21/w2/reports/CorpusRemoved.md
