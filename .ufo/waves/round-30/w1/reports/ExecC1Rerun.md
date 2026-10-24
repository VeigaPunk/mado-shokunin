# ExecC1Rerun — C1 literal-fence independent rerun (round 30)

Runner seat. Read-only against git; this report is the only file written.

## Verdict

Both expected C1 states reproduce **exactly**, byte-for-byte against the committed
receipts, and both named revisions are ancestors of `master`.

| REV | exit | fence stdout | byte-diff vs receipt |
|---|---|---|---|
| `8f51071b5bc44c815eeb5da76bb7f1947994ffb8` (base) | 1 | `indexed=41/43 missing=2 dangling=0 duplicates=0 coverage=9.5349/10` | **identical** to `.ufo/waves/round-30/evidence/c1-before-8f51071b.txt` |
| `446dc3966193c81e64896f4880a19a4bd249255b` (data) | 0 | `indexed=43/43 missing=0 dangling=0 duplicates=0 coverage=10.0000/10` | **identical** to `.ufo/waves/round-30/evidence/c1-after-446dc396.txt` |

Base missing set, in fence emission order (sorted):

```
missing: knowledge/mutation-testing-r28.md
missing: knowledge/workspace-rules-r27.md
```

Data commit missing set: empty.

## Fence provenance and invocation (literal, not reimplemented)

- Source of truth: the `### Counting command` fenced `bash` block in `SCORECARD.md`
  (the S185 frozen navigation fence).
- Block bytes are identical at base `8f51071b`, data `446dc396` and records tip
  `92d3c86`: `fence identical at base vs data: True`, `at tip: True`;
  sha256 `8b59b503805396b514cb4e009981d6a1837a7898c368afff68e25eb5704a7b88`, 1063 bytes.
- Invocation: block piped verbatim to `/bin/bash -s` with `cwd` = lane repo and
  `REV=<sha>` exported; receipt form = stdout followed by `EXIT=<rc>`.
- The fence reads only committed objects (`git ls-tree REV:corpus/knowledge`,
  `git show REV:corpus/README.md`), so worktree state cannot influence either run.

## Byte-diff / determinism evidence (retained)

| Receipt | sha256 of committed file | my receipt sha256 | equal |
|---|---|---|---|
| `c1-before-8f51071b.txt` | `a44330053c61e373c3f8bb86a64377953cf993a71bd831d6663f03d6b5efa769` | same | yes |
| `c1-after-446dc396.txt` | `ca9fb012308449d9c5efa640eef799dfe83b30f1fa1e82bfe8cdd24f80558d70` | same | yes |

Second independent run of each fence reproduced both receipts byte-identically
again (`rerun before identical: True`, `rerun after identical: True`). stderr empty
in all runs.

## Ancestry (`git merge-base --is-ancestor`, exit code recorded)

| Check | exit |
|---|---|
| `8f51071b -> master` | 0 |
| `446dc396 -> master` | 0 |
| `8f51071b -> 446dc396` (base is ancestor of data) | 0 |
| `446dc396 -> 8f51071b` (ordering sanity, expected fail) | 1 |

`master` advanced during the run (`92d3c86` -> `d72243e` "round-30 verifier
spot-check"): the ancestry checks were run against `92d3c86` **and** re-run against
`d72243e`; both target revisions stayed ancestors (exit 0). `git rev-list --count
8f51071b..446dc396` = 2 (freeze + data); `8f51071b..master` = 4 (freeze, data,
records, spot-check). HEAD is detached at `d72243e` (= `master`).

## Supporting reads (committed objects only)

- `corpus/README.md` at `446dc396`: 43 index rows matching `^\| \`knowledge/`; the two
  added rows are line 53 (`knowledge/workspace-rules-r27.md`, source S178–S182/S158/S162)
  and line 54 (`knowledge/mutation-testing-r28.md`, source S183, title-level only), both
  annotated "index row added round 30".
- `corpus/knowledge/*.md` count is **43 at both revisions** — the denominator did not
  move, so `41/43` is genuinely two absent rows rather than one new note.

## Risks / limits of this evidence (not endorsements)

1. **Time-indexed ancestry.** "Ancestor of master" holds for `master` = `92d3c86` and
   `d72243e`; master is live and may advance again.
2. **Fence semantics are row-set only.** It proves each of the 43 notes has exactly one
   index row and no dangling/duplicate row; it cannot verify that the two rows' quoted
   header/scope text matches the notes, nor that their `source:` citations resolve. My
   rerun confirms the registered integer transition, nothing about row fidelity.
3. **Finite denominator.** `coverage=10.0000/10` is over the 43 admitted notes only; it
   does not retire broader coverage (consistent with the registration's own wording).
4. **Do-nothing control (K1) confirmed:** the base run is red with `missing=2`, so
   `43/43` cannot be reached without the data commit's README rows.
5. **Tip durability (supplementary, non-claim):** the same fence at
   `d72243e1fec0f5fd4311ca9c29a2228b33ac348b` prints `indexed=43/43 ... coverage=10.0000/10`,
   `EXIT=0` — the two records/spot-check commits did not regress the index.
6. Worktree dirt at run time: only untracked `.ufo/waves/round-30/w1/`; no tracked
   modifications. Irrelevant to the fence (committed-object reads) but noted.

## Blockers

None. No tool installs or upgrades were needed or performed (no pacman transaction).

## Addendum — out-of-scope worktree mutation reported by `RevC1Fence` (read-only check, not remediated)

Peer `RevC1Fence` flagged `M quality/q36-successor-receipts.txt`; independently
confirmed read-only at 2026-10-24, mtime `04:06:46 -0300`:

- `git diff --stat`: 1 file, 4 insertions / 4 deletions. Only the ephemeral run
  directories differ (`/tmp/mado-r28-q36-ge5zx30t/…` -> `/tmp/mado-r28-q36-g3nfq53x/…`
  and `/fast/scratch/hyaku/mado-r28/ExecQ36Runner/run.gR7SQoLa/…` ->
  `run.Kv8n49Ha/…`), on the Q2-glob-case-sensitive and Q5-marker-case-insensitive
  control lines; every `rc=`/`expected=`/`PASS` token is unchanged, so no verdict moved.
- Not my file and not my item: this seat performs no restore and no commit. Flagged for
  the L1/integrator as a harm-watch item (a committed evidence file was rewritten in the
  worktree, outside the registered round-30 wave-1 write scope).
- It does **not** affect this item's evidence: the C1 fence reads only committed objects
  (`git show`/`git ls-tree`), and `92d3c86`/`d72243e` still carry the original blob.
  Confirmed worktree-only: `HEAD:quality/q36-successor-receipts.txt` sha256
  `667bee37062141a20de2533f72201ca9eb19c8dbcf8f39724c169885493d0721` (last touched by
  round-28 commit `77cdda8`) vs worktree `fd34b9031d39952662a9327758cb83c0d902148c5ed6a30f3e4f273ca2e9003b`;
  no commit carries the rewrite.

## Files changed

- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-30/w1/reports/ExecC1Rerun.md` (this report)
