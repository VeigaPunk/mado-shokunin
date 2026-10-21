# Round 21 W1 — committed fixture corpus freeze

## Scope and behavior

Created the reproducible freezer at `/tmp/mado-r21-corpus-external/.ufo/waves/round-21/corpus/freeze_corpus.py` and materialized its snapshot at `/tmp/mado-r21-corpus-external/.ufo/waves/round-21/corpus/snapshot/`.

The script pins source commit `794aaeb22b4bf35b2482a6779733b69343baff5b`, inventories its complete recursive Git tree, and includes every distinct path recorded as a regular blob (`100644` or `100755`) with the case-sensitive `.jsonl` suffix. It reads each selected blob with `git show`; it does not inspect detector output or use file contents, local worktree state, or sessions to determine eligibility. Identical bytes at different paths remain separate snapshot entries. The snapshot contains raw files under `snapshot/files/<repository-relative-path>` and `snapshot/manifest.json` records each path, exact path bytes, source mode, Git blob OID, byte size, and SHA-256, along with the inclusion rule and aggregate payload counts.

The manifest explicitly identifies this as the committed lane transcript **fixture corpus**, not a private live-session corpus. Fixture snippets were treated as inert bytes and never executed. Fail-closed materialization caps are 10,000 files, 32 MiB per file, and 256 MiB total payload; crossing a cap aborts publication rather than filtering the population.

## Retained evidence

- Source commit: `794aaeb22b4bf35b2482a6779733b69343baff5b`.
- Manifest-derived population: **1,356 paths**, **17,478,844 payload bytes** (manifest size excludes the manifest itself).
- Manifest SHA-256 from the freezer's successful materialization output: `8e1cf206c85563b418630ef1d094559a9522431ff4e077ca1b51f249436a1377`.
- The first and last manifest paths are `.ufo/waves/round-17/tripwire/compound/abs-path-pacman.jsonl` and `.ufo/waves/round-20/w2/ScribeTrendDraft/fetch/receipts.jsonl`; these are boundary examples, not an eligibility boundary.
- The freezer completed with exit status 0 and printed the same count, payload size, and manifest digest. No classifier or gate was invoked or measured.

## Risks and limits

- The explicit size/count caps are operational safeguards; if a later source commit exceeds them, this freezer fails closed and must not be changed to silently omit files.
- This records a frozen committed fixture population only. It makes no claim about the private live-session corpus or classifier behavior.
- No LSP-capable tool was exposed in this session. The addition is standalone and changes no existing symbols or callsites, so there was no supported symbol refactor to perform.
- No tests, linters, formatters, builds, classifier measurements, or tool installations were run/performed. The freezer was executed only to create the requested artifact.

## Files changed

- `/tmp/mado-r21-corpus-external/.ufo/waves/round-21/corpus/freeze_corpus.py`
- `/tmp/mado-r21-corpus-external/.ufo/waves/round-21/corpus/snapshot/manifest.json`
- `/tmp/mado-r21-corpus-external/.ufo/waves/round-21/corpus/snapshot/files/` — the 1,356 distinct path entries described by the manifest.
