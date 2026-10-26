# ExecSeparability — C1/C2 separability, both directions, on fixture commits (round 44, w2)

Seat: ExecSeparability. Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`. Data commit
`e46789213830597348fe96a351ae004d10587385`, base `6a1a90528fe533cadee506a9fa3e9d13d15cc41f`, registration
`registration-v2.md` (freeze `03fa5c618b089064a657b3d79d3d4272ae4b6894`).

**Result: separability holds in both directions.** With `tools/mado-geometry.py` reverted to the base bytes and the
rest of the data commit intact, C2 is still `admitted=1/1 TARGET_MET` (exit 0) while C1 drops to `15/26
TARGET_MISSED` (exit 1); with the C2 corpus surface reverted to base and the tool intact, C1 is still `26/26
TARGET_MET` (exit 0) while C2 is `admitted=0/1 TARGET_MISSED` (exit 1). Neither counter moves when only the other's
input changes, and each of C2's four corpus surfaces was separately shown to be load-bearing.

## Method and reproducibility

Three scratch clones, deleted at the end of this seat; the recipes and patches are kept here:

    git clone -q --shared <lane> $D && git -C $D rev-parse --show-toplevel   # == $D
    git -C $D checkout -q e46789213830597348fe96a351ae004d10587385           # then revert, then commit inside $D only

Fixture commits (created inside the clones only; the lane's index, jj and git were never mutated):

| fixture | commit | recipe: the tree is the data commit `e4678921` with this one change | evidence kept |
|---|---|---|---|
| A | `5e29d7130acfce4245fb54ef3bef573cffe9e4ab` | `tools/mado-geometry.py` ← base `6a1a905` bytes (sha256 `e3c2e471505932f797a98ee2aa9ab1b04fc919f2140509282ef8472498135a99`), C2 corpus untouched | `fixtures/fixture-A.patch` |
| B | `bca065770f317ff2735acb77518f4dc1b55572ed` | entry and `corpus/lessons/round-44.md` absent, `corpus/SOURCES.md` and `corpus/README.md` ← base, tool untouched | `fixtures/fixture-B.patch` |
| C | `ba1fd7a8ad54d5dd7ce87e4ee5da13befc0d0dd0` | whole lane tree ← base, then the data tool only (`git diff --name-only 6a1a905 ba1fd7a8` lists exactly `tools/mado-geometry.py`) | `fixtures/fixture-C.txt` (recipe) |
| E | `f378443a70ae55eb4a02adcc77bf6091da63e73c` | only the README index row at `corpus/README.md:72` deleted | `fixtures/fixture-E.patch` |
| F | `0d108530a00f8b36acfac114153326957a6d32cf` | only `corpus/SOURCES.md` ← base | `fixtures/fixture-F.patch` |
| G | `44b217df6acea9a8f04d9222ca3f0a39ec301ae3` | only `corpus/lessons/round-44.md` deleted | `fixtures/fixture-G.patch` |
| H | `b33cbd323fc122c158c52b2eb692d31ec0739176` | only `quality/counters/c1-r42-geometry.py` deleted at REV | `fixtures/fixture-H.patch` |
| I | `65efe9f636cf445ca9e6a31665b46aaa5abd829c` | `SKILL.md`, `PROVINCE.md`, `corpus/QUALITY.md`, `SCORECARD.md`, `LOG.md` ← base and `quality/ratio-domain-meta.py` deleted; entry, registry, lesson, README and pins intact | `fixtures/fixture-I.patch` |

Counting commands (cwd = the lane, so the counter bytes are the lane's own; `--repo` addresses the fixture clone):

    python3 -I quality/counters/c1-r44-geometry-states-v2.py --repo <clone> --rev <fixture> --work <scratch>
    python3 -I quality/counters/c2-r44-gkeep-size-request-v2.py --repo <clone> --rev <fixture>

Every receipt in `receipts/` carries the counter's own `EXIT=` line. C1 receipts are nonce-sensitive; the five whose
`EXIT=` line was lost when the outer shell died were replayed with their recorded `--nonce` and compared byte for byte
with the original before the exit code was kept (replay identical in all five cases). `verify-quotes.sh` re-derives
every quoted locator below by grepping the receipts (`verification.txt`, `VERDICT: PASS`).

## Matrix (every cell executed in this seat)

| rev | what is reverted | C1 | C2 |
|---|---|---|---|
| `e4678921` data | — | `PRED-C1-r44-v2: fixtures=26/26 tool=present verdict=TARGET_MET rev=e46789213830597348fe96a351ae004d10587385 nonce=f2730a25f35cc26a` — exit 0 | `PRED-C2-r44-v2: admitted=1/1 verdict=TARGET_MET rev=e46789213830597348fe96a351ae004d10587385` — exit 0 |
| A `5e29d71` | the tool → base | `PRED-C1-r44-v2: fixtures=15/26 tool=present verdict=TARGET_MISSED rev=5e29d7130acfce4245fb54ef3bef573cffe9e4ab nonce=e2ab528a4a6b2f13` — exit 1; clauses `PRED-C1-r44-v2 clauses=a:1 b:0 b4:0 b5:0 e:1 g:1 r:1` | **`PRED-C2-r44-v2: admitted=1/1 verdict=TARGET_MET rev=5e29d7130acfce4245fb54ef3bef573cffe9e4ab` — exit 0**, `PRED-C2-r44-v2 hyprland-gkeep-size-request-r44.md clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 j:1 admitted=1` |
| B `bca0657` | entry, lesson, rows, README → base | **`PRED-C1-r44-v2: fixtures=26/26 tool=present verdict=TARGET_MET rev=bca065770f317ff2735acb77518f4dc1b55572ed nonce=72e611b0ab42860c` — exit 0** | `PRED-C2-r44-v2: admitted=0/1 verdict=TARGET_MISSED rev=bca065770f317ff2735acb77518f4dc1b55572ed` — exit 1 |
| C `ba1fd7a` | everything → base, tool kept | `PRED-C1-r44-v2: fixtures=26/26 tool=present verdict=TARGET_MET rev=ba1fd7a8ad54d5dd7ce87e4ee5da13befc0d0dd0 nonce=9c234cbf35500ada` — exit 0 | `PRED-C2-r44-v2: admitted=0/1 verdict=TARGET_MISSED rev=ba1fd7a8ad54d5dd7ce87e4ee5da13befc0d0dd0` — exit 1 |
| E `f378443` | only the README index row | not run (see S3) | `PRED-C2-r44-v2 hyprland-gkeep-size-request-r44.md clauses=a:1 b:1 c:1 d:1 e:1 f:0 g:1 h:1 i:1 j:1 admitted=0` — exit 1 |
| F `0d10853` | only `corpus/SOURCES.md` | not run (see S3) | `PRED-C2-r44-v2 hyprland-gkeep-size-request-r44.md clauses=a:1 b:1 c:0 d:1 e:0 f:1 g:1 h:1 i:1 j:1 admitted=0` — exit 1 |
| G `44b217d` | only the lesson | not run (see S3) | `PRED-C2-r44-v2 hyprland-gkeep-size-request-r44.md clauses=a:1 b:1 c:1 d:0 e:0 f:1 g:0 h:0 i:0 j:1 admitted=0` — exit 1 |
| H `b33cbd3` | the round-42 counter absent at REV | `PRED-C1-r44-v2: fixtures=26/26 tool=present verdict=TARGET_MET rev=b33cbd323fc122c158c52b2eb692d31ec0739176 nonce=06290a51fc261998` — exit 0 | not run (see S3) |
| I `65efe9f` | the C1-riding docs → base, C2 surfaces intact | not run (see S3) | `PRED-C2-r44-v2: admitted=1/1 verdict=TARGET_MET rev=65efe9f636cf445ca9e6a31665b46aaa5abd829c` — exit 0 |
| `6a1a905` base | both surfaces absent | `PRED-C1-r44-v2: fixtures=13/26 tool=present verdict=TARGET_MISSED rev=6a1a90528fe533cadee506a9fa3e9d13d15cc41f nonce=973c7468182135f9` — exit 1 | `PRED-C2-r44-v2: admitted=0/1 verdict=TARGET_MISSED rev=6a1a90528fe533cadee506a9fa3e9d13d15cc41f` — exit 1 |

## Findings

**S1 — C2 does not depend on C1's implementation ("tool reverted" direction). Severity: assertion supported.**
At A the tool at REV is the base tool (sha256 `e3c2e471…35a99`, the round-43 bytes) and C2 still reports
`PRED-C2-r44-v2: admitted=1/1 verdict=TARGET_MET rev=5e29d7130acfce4245fb54ef3bef573cffe9e4ab` with every clause at 1
(`receipts/c2-A.txt:28-29`, exit 0 recorded). C1 on the same commit loses exactly the state half of the contract:
`PRED-C1-r44-v2 clauses=a:1 b:0 b4:0 b5:0 e:1 g:1 r:1` (`receipts/c1-A.txt:34`). The C2 pass cannot therefore be an
artefact of the new tool, and the C1 verdict is not propped up by the corpus.

**S2 — C1 does not depend on C2's landed corpus ("corpus reverted" direction). Severity: assertion supported.**
At B the entry, the lesson, the S298-S301 and S164 registry rows and the README index row are all at base, and C1 still
reports `PRED-C1-r44-v2: fixtures=26/26 tool=present verdict=TARGET_MET rev=bca065770f317ff2735acb77518f4dc1b55572ed nonce=72e611b0ab42860c`
(exit 0), while C2 falls to `PRED-C2-r44-v2: admitted=0/1 verdict=TARGET_MISSED rev=bca065770f317ff2735acb77518f4dc1b55572ed`.
The stronger form C holds too: the entire lane tree is base except the one tool file (`git diff --name-only
6a1a905 ba1fd7a8` lists exactly `tools/mado-geometry.py`) and C1 is still
`PRED-C1-r44-v2: fixtures=26/26 tool=present verdict=TARGET_MET rev=ba1fd7a8ad54d5dd7ce87e4ee5da13befc0d0dd0 nonce=9c234cbf35500ada`.
Nothing outside `tools/mado-geometry.py` carries C1's PASS — in particular not SKILL.md, PROVINCE.md, QUALITY.md
criteria 82-84, SCORECARD.md, LOG.md, `quality/ratio-domain-meta.py` or the live host receipt, which agrees with
registration v2's "the SKILL/PROVINCE rows are documentation riding with C1 and are not scored".

**S3 — C1 reads exactly one path from REV, C2 exactly five. Severity: assertion supported (static and dynamic).**
Static: the only revision-addressed read of repo content in C1 is the tool —
`src = open(args.tool, "rb").read() if args.tool else old.git(repo, "show", "%s:%s" % (rev, TOOL))`
(`quality/counters/c1-r44-geometry-states-v2.py:418`). C2's repo reads are `FETCH + rname` (`:380`), the entry
(`:408`), a FETCH blob (`:488`), `corpus/SOURCES.md` at REV and BASE (`:669-670`), `corpus/lessons/round-44.md`
(`:671`) and `corpus/README.md` (`:672`). Dynamic: A moves C1 only, B moves C2 only. That is why C1 was not run on
E, F, G, I and C2 not on H: those fixtures revert only the other predicate's input.

**S4 — each of C2's corpus surfaces is separately load-bearing, and the non-corpus docs are inert to it. Severity:
assertion supported.** Removing only the README index row costs clause f and nothing else
(`PRED-C2-r44-v2 hyprland-gkeep-size-request-r44.md clauses=a:1 b:1 c:1 d:1 e:1 f:0 g:1 h:1 i:1 j:1 admitted=0`,
exit 1); reverting only `corpus/SOURCES.md` costs c and e
(`PRED-C2-r44-v2 hyprland-gkeep-size-request-r44.md clauses=a:1 b:1 c:0 d:1 e:0 f:1 g:1 h:1 i:1 j:1 admitted=0`);
deleting only the lesson costs d, e, g, h and i but not j
(`PRED-C2-r44-v2 hyprland-gkeep-size-request-r44.md clauses=a:1 b:1 c:1 d:0 e:0 f:1 g:0 h:0 i:0 j:1 admitted=0`);
and putting the five C1-riding docs back to base while entry, registry, lesson, README and pins stay at data leaves C2
at `PRED-C2-r44-v2: admitted=1/1 verdict=TARGET_MET rev=65efe9f636cf445ca9e6a31665b46aaa5abd829c` (exit 0). C2's
verdict is a function of its four corpus files plus the pins, and of nothing else in the data commit.

**S5 — OPEN predicate observation (severity LOW; no round-44 verdict changes; reported, not re-registered).**
Registration v2's Separability sentence ("C1's counter reads only the tool and the round-42 counter") is true but does
not say where the round-42 counter is read from: it is `OLD_PATH = os.path.join(HERE, "c1-r42-geometry.py")`
(`quality/counters/c1-r44-geometry-states-v2.py:80`), loaded through `importlib` (`:82`) and run against `--repo repo
--rev rev` from that same lane directory (`:339`) — that is, from the scoring lane's checkout, never from `REV`.
Fixture H measures the consequence: deleting `quality/counters/c1-r42-geometry.py` at the revision under test leaves C1
at `PRED-C1-r44-v2: fixtures=26/26 tool=present verdict=TARGET_MET rev=b33cbd323fc122c158c52b2eb692d31ec0739176 nonce=06290a51fc261998`,
the same verdict as the data run. A revision that tampered with the round-42 counter or with the model of the contract
would not be caught by clause r, because both come from the lane's working tree at scoring time. For round 44 this
cannot move a booked number: the data commit changes no counter at all (the `quality/counters/` diff from the freeze
`03fa5c61` to `e4678921` is empty; the only `quality/` addition is `quality/ratio-domain-meta.py`), and
`verify-quotes.sh` re-checks that count on every run. Suggested sharpening for a future registration, the L1's call
after data: state that C1 binds the tool at REV and the round-42 counter as checked out in the scoring lane.

**S6 — the C1 fixture share is nonce-dependent, its verdict is not. Severity: informational, matches the declared
residual.** The base tool scored 15/26 on the run nonce
(`PRED-C1-r44-v2: fixtures=15/26 tool=present verdict=TARGET_MISSED rev=5e29d7130acfce4245fb54ef3bef573cffe9e4ab nonce=e2ab528a4a6b2f13`),
13/26 at nonce `0000000000000001`
(`PRED-C1-r44-v2: fixtures=13/26 tool=present verdict=TARGET_MISSED rev=5e29d7130acfce4245fb54ef3bef573cffe9e4ab nonce=0000000000000001`)
and 15/26 at nonce `0000000000000002`
(`PRED-C1-r44-v2: fixtures=15/26 tool=present verdict=TARGET_MISSED rev=5e29d7130acfce4245fb54ef3bef573cffe9e4ab nonce=0000000000000002`),
all exit 1; the registration's `11/26` for base is the same class of number on a different draw. Nothing in this seat
treats the share as a fixed value, and no verdict depends on it.

## What this does not claim

- The round's own before-receipts were not re-run; the base row above is my own run
  (`PRED-C1-r44-v2: fixtures=13/26 tool=present verdict=TARGET_MISSED rev=6a1a90528fe533cadee506a9fa3e9d13d15cc41f nonce=973c7468182135f9`,
  `PRED-C2-r44-v2: admitted=0/1 verdict=TARGET_MISSED rev=6a1a90528fe533cadee506a9fa3e9d13d15cc41f`) and agrees in
  verdict with the frozen round receipts `.ufo/waves/round-44/receipts/c1-v2-before-base.txt` (11 of 26 fixtures,
  `TARGET_MISSED`, `exit=1`) and `.ufo/waves/round-44/receipts/c2-v2-before-base.txt` (`admitted=0/1`,
  `TARGET_MISSED`, `exit=1`).
- Fixture commits live in scratch clones that are deleted; their hashes are citable only together with the kept
  patches (`fixtures/`) or the recipes, which rebuild the trees from the lane's own commits.
- No build, lint, test or formatter gate was run (the parent owns post-integration gates). No package was installed,
  no pacman transaction, no host-service or compositor mutation, no Wayland connection; `bubblewrap 0.13.1` and the
  lane's stdlib-only counters were used as found. No writes outside this seat directory, no mutating git in the lane or
  the fleet — the only commits are inside `/fast/scratch/hyaku/mado-r44/ExecSeparability/clone{,2,3}`, now deleted.

## Files in this seat

- `ExecSeparability.md` — this report.
- `receipts/c1-*.txt` (8 runs) and `receipts/c2-*.txt` (9 runs) — 17 counter runs in all (data, A with three nonces,
  B, C, E, F, G, H, I, base), each with its `EXIT=` line.
- `fixtures/fixture-{A,B,E,F,G,H,I}.patch` (diff from the data commit), `fixtures/fixture-C.txt` (recipe) and
  `fixtures/fixture-*.txt` (commit, recipe, file list versus the data commit).
- `verify-quotes.sh`, `verification.txt` — quote locators, exit codes, no-counter-changed and fixture-evidence checks.
