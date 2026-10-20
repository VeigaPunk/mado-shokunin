# ProvenanceRerun — re-run and attack `frozen-provenance-check.py` (round 18, wave 2)

Seat: `MadoR18.ProvenanceRerun`, wave 2 (FALSIFY), 2026-10-20. Target root
`/home/vgpnk/Projects/shokunin/mado-shokunin`; baseline `d9a5a18`, integration
`4c103b55b1ea5c3c555884afe3eb69b5189701b7`, receipts
`abfbf35b1ed4d4a1eb294d525ef286be30f3886f`. Read-only lane: no git/jj write, no
package/service/compositor/input probe. Attacks ran only on `/tmp` copies.

## Target and binding

`.ufo/waves/round-18/frozen-provenance-check.py` — checks that every frozen
tripwire snapshot line is byte-identical to the transcript line it was cut from,
and that each source still has the digest registered in the round-17 session
index. Exit 0 match / 1 mismatch / 2 could-not-evaluate.

Binding actually established (read-only git):

```
git cat-file -e d9a5a18:.ufo/waves/round-18/frozen-provenance-check.py   → absent
git show 4c103b5:.ufo/.../frozen-provenance-check.py | sha256sum        → 5ee0791b6bdb46b1f753b1589908b3b875202e6eb16bcaf787eeafe36f2c8e74
git show abfbf35:...frozen-provenance-check.py       > /tmp/tool_at_receipt.py; rc=0
sha256sum /tmp/tool_at_receipt.py                     → 5ee0791b…c8e74
cmp /tmp/tool_at_receipt.py <worktree file>           → rc=0
git merge-base --is-ancestor 4c103b5 abfbf35         → rc=0
git diff 4c103b5 abfbf35 -- .ufo/waves/round-18/frozen <tool> → empty
git ls-tree -r abfbf35 -- .ufo/waves/round-18/frozen → 8 blobs, all equal to
  `git hash-object` of the worktree files
```

So the tool and the whole frozen directory measured below are the bytes at the
receipt commit, and the tool did not exist at baseline `d9a5a18` (it is a
round-18 artifact, not a pre-existing instrument).

## Claimed run (default root)

```
python3 -I .ufo/waves/round-18/frozen-provenance-check.py
→ MADO_FROZEN_PROVENANCE: match
→ {"diffs": [], "exit": 0, "root": "…/.ufo/waves/round-18/frozen",
   "index": "….ufo/waves/round-17/evidence/session-index.json",
   "index_sha256": "06c259bcdd44785d93d846ca971257fdbb27d68ea70da7251448561423f70df5",
   "indexed_sources": 228, "pairs_checked": 26, "unindexed": [], "unresolved": [],
   "tool_sha256": "5ee0791b…c8e74", …}
exit=0
```

stderr empty (0 bytes). Default root is `…/round-18/frozen` as declared.
Receipt + full output: `.ufo/waves/round-18/evidence/w2-frozen-provenance.txt`
(line 1 `RECEIPT tool=… tool_sha256=5ee0791b… measured_commit=abfbf35… utc=2026-10-20T16:01:30Z cmd=python3 -I …`, then both stdout lines, then `exit=0`).

Derived coverage (independent of the tool, from `provenance.json` and file
bytes): the five inputs hold 5/5/5/6/5 lines and 26 pairs; every snapshot line
1..N of every input is paired exactly once (`covered=True`, `dups=False`). No
line's bytes rely on the digest alone.

## Attack results (all on `/tmp/pr18-*` copies; exit codes measured)

| # | Tamper | Exit | Verdict |
|---|---|---|---|
| A | one byte at offset 212 of `inputs/r15-libinput-events.jsonl` line 1 (mapped), provenance untouched | **1** | `input_sha_mismatch` **and** `line_bytes_differ` ("snapshot 3890 B, source 3890 B, first divergence at byte 212") — both checks fire |
| B | same byte flip **plus** declared `sha256` rewritten in `provenance.json` | **1** | `line_bytes_differ` alone — the line compare does not depend on the declared digest; rewriting the digest cannot launder the flip |
| F | source path pointed at a nonexistent transcript | **2** | `source_missing` → `could_not_evaluate`; a dead transcript is not silently accepted |
| G | `--index` file declares a wrong sha for a real source | **1** | `source_sha_mismatch`; the index check bites |
| D | extra unclaimed `inputs/zz-extra.jsonl` | **2** | `input_unclaimed` |
| E | missing `provenance.json` | **2** | `could_not_evaluate`, "nothing to check" |
| N | one byte flipped in `frozen/expected.json` | **0** | **match** — this tool never opens `expected.json` |
| O | `provenance.json` `"index"` rewritten to `/nonexistent/session-index.json` | **0** | **match** — the declared index is dead metadata; the CLI default wins |
| I | unclaimed `inputs/sub/x.jsonl` + `inputs/EVIL.JSONL` | **0** | **match** — unclaimed scan is direct children, lowercase `.jsonl` only |

Required check A is confirmed: a one-byte flip in a mapped snapshot input exits
1. B shows the check is two independent guards, not one digest. F/D/E show the
could-not-evaluate arm is honest (exit 2, not 0).

## Findings beyond the required test

1. **[FACT] Scope boundary — `expected.json` is not covered (N).** The tool
   reads only `ROOT/provenance.json`, the inputs it names, and the source
   transcripts; `grep -n expected frozen-provenance-check.py` matches only the
   string "unexpected argument" (line 434). A one-byte flip in
   `frozen/expected.json` yields `match` exit 0. This is consistent with the
   docstring (it verifies snapshot-vs-source provenance, not the expected
   verdict), but it means "a one-byte flip in the snapshot → exit 1" is true
   only for `inputs/`; the expectation manifest is guarded (if at all) by the
   tripwire's own verdict comparison, which this item did not authorize running.
   No claim asserts this tool pins `expected.json`; recorded so a closure does
   not read this tool's `match` as covering it.

2. **[FACT] Declared index is not enforced (O).** `provenance.json` carries
   `"index": ".ufo/waves/round-17/evidence/session-index.json"`, but the code
   never reads that member (the only `index` uses are the CLI default/argument
   and output fields). Rewriting it to a nonexistent path still returns
   `match` exit 0, while `index_sha256` shows the default file was used. The
   evidence therefore names its real trust anchor in `index_sha256`, but the
   provenance file advertises a binding that is not consulted. Low severity
   today (the default path is the intended committed index), moderate as
   provenance-honesty debt: a reader of `provenance.json` alone would conclude
   the declared path was verified.

3. **[FACT] Unclaimed-byte gate is narrower than it reads (I/D).**
   `os.listdir(root/inputs)` + `name.endswith(".jsonl")` catches only direct
   children with the exact lowercase suffix. `inputs/sub/x.jsonl` and
   `inputs/EVIL.JSONL` are invisible (exit 0). This cannot alter a verdict the
   tripwire reads by manifest, but unexplained bytes can sit in a directory
   described as "frozen" without being reported. Cheap hardening for a later
   round: recursive walk + case-insensitive suffix, or compare the input set
   against `expected.json`'s declared list.

4. **[INFERENCE] Trust anchor is caller-supplied and unpinned (G/O).** The
   check compares against whatever index is passed (default: the committed
   round-17 file, observed sha `06c259…`); the index's own digest is printed
   but not tied to a revision, and `provenance.json` does not bind it. A
   `match` attests consistency with the presented index, not authenticity of
   that index. The receipt pins the tool (`5ee0791b…`) and the commit, so the
   instrument is identified; the index remains conventional.

5. **[FACT] Whole-file transcript reads.** The default run hashes the five
   source transcripts in full (`~/.omp/.../MadoR13|R14|R15…jsonl`, abfbf35
   tree) to compute `observed_sha256`, and compares mapped lines byte-exact.
   The item directs the run; disclosure only, since the wave contract otherwise
   permits transcript access only at named lines. Nothing is echoed or written;
   sources are opened read-only.

## Verdict for this item

The declared measurement reproduces at `abfbf35`: `match`, exit 0,
`pairs_checked=26`, `diffs=[]`, tool bytes `5ee0791b…` identical at integration
`4c103b5`, receipts `abfbf35`, and the worktree; default root is the frozen
directory. The required attack passes (one-byte flip → exit 1, two independent
diffs). No claim failure found. Residual boundary: `expected.json` and the
provenance `index` member are outside what this instrument enforces, and the
unclaimed-input gate is one level shallow — all recorded above, none of which
changes the measured claim.

Evidence written: `.ufo/waves/round-18/evidence/w2-frozen-provenance.txt`
(4 lines: receipt, `MADO_FROZEN_PROVENANCE: match`, verdict JSON, `exit=0`).

Risks: none introduced in the lane; all mutation confined to `/tmp/pr18-*`.
No tool install or upgrade was needed or made. Blockers: none.
