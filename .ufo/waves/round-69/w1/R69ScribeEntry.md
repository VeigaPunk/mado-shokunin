# R69ScribeEntry — claim-C2 knowledge entry draft (round 69, w1)

## Deliverables (absolute paths, sha256, size)

| path | sha256 | size |
|---|---|---|
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-69/w1/R69ScribeEntry/draft/corpus/knowledge/gate-guard-dominance-r69.md` (243 lines) | `c7a2dc30fd1c6b8ec324f944a9eaf459f6d97e763f75ac8759fab16c9ac78a89` | 17935 B |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-69/w1/R69ScribeEntry/draft/corpus/README-index-row-r69.txt` (8 lines, supplementary) | `bc30932e1727fe1eb999626ac222aad1973725a6731d44f086afa5104e7ea1a3` | 1887 B |
| `.../R69ScribeEntry/receipts/fetch-git-adoc.txt` | `d8e88ea0bf84ba6d9eec54618f4bd54cd81d535f5f26e1abd308e042bb68adca` | — |
| `.../R69ScribeEntry/receipts/r68-on-r69-controls.txt` | `830bba7fbe29c3fcad206607b05fcde9c5d688cc889c3270d5c222fbbea14d17` | — |
| `.../R69ScribeEntry/receipts/proto-at-base.txt` | `d4736099063d478599472dbb0130891435b211f22fe0931a685753ebe3b62bab` | — |
| `.../R69ScribeEntry/receipts/proto-controls.txt` | `85def7124273036384997759d88c91f93178ae1a2f528b551766e210e43f9925` | — |
| `.../R69ScribeEntry/receipts/proto-boundary-probes.txt` | `70a1bd7cf2f3c437b3653d7fb1e048267ab2db71fb79893da873dab95917f52f` | — |
| `.../R69ScribeEntry/receipts/check107-fixture.txt` | `da816436b95f34981fe83026afb0098db255da5d0678e580c1e421ebfe6ce5df` | — |
| `.../R69ScribeEntry/receipts/index-row-fixture.txt` | `d755dad4ed3b68021a21165ca071cccaaa87605d411573d52ff783d5cef5ba9e` | — |

No production path was written; the lane worktree is untouched outside
`.ufo/waves/round-69/w1/R69ScribeEntry/` and this report.

## Entry contents (all numbers measured, not restated)

1. **r68 gap.** The round-68 classifier's presence test accepts four constructions that deliver
   nothing to a child: `value-position-only`, `dead-branch-only`, `uncalled-helper`,
   `overwritten-env`. Measured `7/11` twice: the pre-freeze receipt
   (`control-baseline-r69.txt:33-46`) and my own re-run of
   `quality/counters/c2-r68-reader-guard.py` on the frozen JSON.
2. **Key position.** Four accepted constructions (dict-literal key, subscript store on an
   env-named mapping, `update`/`setdefault` keyword, `dict(KEY=…)` keyword) against the
   rejected value position.
3. **Dominance.** Three flows (inline `env=`; env-named binding or local producer with no
   intervening unguarded rebinding; one-hop argument into a local function whose env-named
   parameter reaches the call) plus the literal-false and prose exclusions.
4. **Eleven frozen cases** in a table, each with reader/guard and what it pins.
5. **Population.** 20 `quality/check-*.py`, 13 readers, 13 guarded, 0 unguarded at
   `04093b83f73a841117d3b31dbb2a6063f4f2a454`; the seven non-readers and thirteen readers
   named; what stays outside (`quality/counters/*`, `tools/*`, shell instruments, r67's
   82/79/3 lexical census).
6. **Limits.** Single module/one hop, no alias-attribute-container flow, no path sensitivity
   beyond literal-false, existential per-file ordering, call-shape (not execution) delivery,
   value not interpreted (`=0` also disables), no authenticity, no protection for an
   already-rewritten repo.
7. **Sourced ground.** S438, fetched twice byte-identical: sha256
   `050c5330f1a231be22bee3db27c7ef90d8ba22bb7bd6c72c8bab462f6f0a1f79`, 47005 bytes, 1212
   lines, HTTP 200. Quotes at 1-based lines **180-181** ("This is equivalent to exporting the
   `GIT_NO_REPLACE_OBJECTS` environment variable with any value.") and **928-929** ("Setting
   and exporting this environment variable tells Git to ignore replacement refs and do not
   replace Git objects."). One held row used: S436 at `git-replace.adoc:34`.

## Findings (new, actionable)

- **Three coverage gaps in the frozen 11, found while writing the table** (the declaration is
  frozen; these are reported, not changed):
  1. **No case isolates flow (c).** The committed prototype does implement it — probe
     `one-hop-argument-env` → `(True, True)` — but the set contains no such case.
  2. **No *positive* case isolates the plain dict-literal key.** The only key-position dict
     literal is `overwritten-env`'s first binding, whose case is expected unguarded for the
     rebinding.
  3. **`expect_reader` is true for all eleven cases.** The control set scores only the guard
     predicate; a change to the reader vocabulary would not be caught by it.
- **Prototype over-includes as the launch any call whose arguments carry a literal `git` argv**
  (probe `one-hop-argv-parameter` → `(True, True)`, even though the callee's own
  `subprocess.run(cmd, …)` never shows a literal). Recorded as a Limit; the frozen cases do not
  contradict it.
- **Dominance is existential per file** in the prototype: first guarded use wins, a later
  unguarded rebinding followed by another call is not unset (probe `rebind-after-first-use` →
  `(True, True)`); a key stored after the use is not counted (`late-key-after-use` →
  `(True, False)`). Recorded as a Limit.
- **`dict.update(env, KEY="1")` is not recognized** (only the method form on an env-named
  receiver): probe `mutating-call-not-env-named` → `(True, False)`. Recorded as a Limit.

No conflict with the frozen declaration or the control receipt: my independent runs reproduce
`controls=7/11` (r68) and `11/11` (prototype), and `population=20 readers=13 guarded=13
unguarded=0` at the base revision.

## Integration requirements for the L1

1. **S438 anchor must cover `git.adoc:180` and `git.adoc:928`** (the entry pins those two single
   lines in its K rows). The form I validated with criterion 107 is
   `git.adoc:178-182,927-929`. It must name **no `pin <path>`** — the adoc is not in the lane
   tree; a pin makes `check-anchor-cover.py` read `<rev>:Documentation/git.adoc` and fail
   `absent` (same convention r67 records at `replace-ref-citation-boundaries-r67.md:164-167`).
   The row itself is seat `R69ScribeRowLesson`'s artifact; this is the constraint it must meet.
2. **The entry lands a new `corpus/knowledge/*.md`, so it needs exactly one coverage-map row in
   `corpus/README.md`.** `quality/check-index.py` fails with a gap otherwise (checked its
   docstring: "every admitted `corpus/knowledge/*.md` note has exactly one index row").
   I drafted the row at `draft/corpus/README-index-row-r69.txt` and validated it in a fixture
   (`MADO_INDEX: indexed=1/1 missing=0`, rc 0; `MADO_INDEX_ROWS: rows=1 errors=0 warns=0`,
   rc 0).
3. **The entry names `quality/counters/c2-r69-guard-dominance.py`** (line 3 recheck and §7
   Gate). If the landed counter has a different path, those two mentions must be renamed; the
   entry says "absent at the base revision", which is the declaration's own statement.
4. The control-JSON digest quoted in §7 (`975ca3ba…`) is the frozen one and must not be
   updated even if the file is re-serialized.
5. If the r69 counter's reader vocabulary differs from r68's, the entry's §5 sentence "reader
   side unchanged" stays true only for the frozen numbers; the prototype's wider verb list
   measures the same 13 readers at `04093b83` (measured), so the count is safe either way.

## Commands run (exact; rc)

```
curl -sSfL -o git.adoc  https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/git.adoc   rc=0
curl -sSfL -o git.adoc.2 -w 'http_code=%{http_code}\n' <same url>                                   rc=0, http_code=200
sha256sum git.adoc git.adoc.2 ; cmp git.adoc git.adoc.2                                             rc=0, byte-identical
wc -l -c git.adoc                                                                                   1212 47005
python3 quality/counters/c2-r68-reader-guard.py --repo <lane> --rev 04093b83… \
  --controls .ufo/waves/round-69/controls/c2-controls-r69.json --scratch-root $S/r68              rc=1  (7/11, expected)
python3 .ufo/waves/round-69/proto/c2-classify.proto.py <lane> 04093b83…                            rc=0  (20/13/13/0)
python3 score_controls.py      (prototype × 11 frozen cases)                                       rc=0  (11/11)
python3 probe.py              (8 boundary snippets, evidence only)                                 rc=0
python3 quality/check-anchor-cover.py --repo $S/fixture.oc8m --rev HEAD \
  --entry corpus/knowledge/gate-guard-dominance-r69.md --work $S/anchor-work                       rc=0  CHECK107 rows=3 covered=3 miss=0 verdict=OK
python3 quality/check-index.py --root $S/fixture2.TknM                                             rc=0  indexed=1/1
python3 quality/check-index-rows.py --root $S/fixture2.TknM                                        rc=0  rows=1 errors=0 warns=0
```

The criterion-107 run **against the lane** (NOT run — the draft is uncommitted; for the L1 after
the row and entry land):

```
python3 quality/check-anchor-cover.py --repo . --rev <measured-content> \
  --entry corpus/knowledge/gate-guard-dominance-r69.md --work <scratch>/anchor-r69-entry
```

Line count of the entry: `243`; `wc -c` 17935.

## Bounds observed

- Leaf seat: no subagent dispatch.
- Wrote only `.ufo/waves/round-69/w1/R69ScribeEntry/**` and this report. No commit, push, stage,
  stash, checkout, switch or reset; no git/jj mutation in the lane or any sibling; fixtures used
  `mktemp -d` under scratch with `rev-parse --show-toplevel` asserted before the first commit and
  an explicit `-c user.name/-c user.email` identity.
- Did not read or touch the declaration, control JSON or baseline receipt except as read-only
  inputs; no re-scope, no target narrowing.
- No desktop/compositor/session/socket/service probe; no pacman transaction; **no tool installs**
  (nothing was needed — python3 + curl + git sufficed; no uv/npx/binary download).
- Scratch `/fast/scratch/hyaku/mado-r69/R69ScribeEntry/` (fetch bytes, fixtures, anchor work
  dirs) removed with `rm -rf` before yield; verified absent.
