# ScrSerialCorrection — round-45 closure D2: the M45-2 correction

Seat `w1/ScrSerialCorrection` (leaf; no dispatch, no background jobs). Round 46, 2026-10-26. Lane
`/home/vgpnk/Projects/shokunin/mado-shokunin`, HEAD `e0be61e4` at start and end of my work (read-only on it).
Axes: **count fidelity**, **locator precision**, **provenance/age**, **published extent**, **capture boundary**, **safety
(no serial in any artifact)**. Delivered: `.ufo/waves/round-46/w1/ScrSerialCorrection/correction.md` — the append-only
block for `corpus/lessons/round-45.md` M45-2 plus its evidence header. I edited no tracked file (seat bounds).

## Behavior

The serial was read live from `hyprctl monitors all -j` (the allowed read; the signature comes from
`/run/user/1000/hypr/efb50993…_1793027319_436109330`) into a variable and used only as a `git grep -c -F` / `git grep -n`
needle. Every printed line below is a count or a path; the value never appears in this report, in `correction.md`, in a
receipt, or in any command output. One stray store I made early (`/fast/scratch_serial.tmp`) was deleted immediately, before
any other step; nothing else wrote the value outside the grep needles. The seat's reproducible driver is
`w1/ScrSerialCorrection/verify.py` (`python3 -I verify.py`, read-only on the lane, reads the serial fresh each run).

M45-2's sentence ("and held `corpus/knowledge/hyprctl-verification-layer.md:153` has carried it since round 2",
`corpus/lessons/round-45.md:50`, 9 words) is right about that file and wrong as a count. The serial sits in **24 tracked
files, one occurrence each**:

| class | files | where |
|---|---|---|
| held entries | 3 | `corpus/knowledge/config-health-report-r3.md:149`, `corpus/knowledge/hyprctl-verification-layer.md:153`, `corpus/knowledge/hyprland-config-plane.md:184` |
| wave copies | 21 | 6 fixture trees under `.ufo/waves/round-32/` (18 files: `assimilation/validate`, `c1/controls/a-rows-only`, `c1/controls/b-entries-only`, `scratch/MutExistingGates/fixtures/tree-m1`, `tree-m2`, `tree-m2b`) + 1 under `.ufo/waves/round-37/` (`w1/scratch/ScribeRows/validate`, 3 files) |

All 21 copies are **byte-identical blobs** of the three held entries at `4d22eeb` (`git rev-parse <rev>:<path>`, 21/21), so
they are one carrier decision repeated by a fixture generator, not 21 independent leaks.

## Gates and checks run

| check | command | observed |
|---|---|---|
| seat verification | `python3 -I verify.py` (seat dir) | `VERIFY: checks=29 failed=0 verdict=PASS` |
| spread, five revisions | `git grep -c -F "$S" <rev> -- .` and `-- . ':!.ufo'` | `0c89478`, `4d22eeb`, `b22ea56`, `8c5434c6`, `e0be61e4`: `files=24 occurrences=24 held=3` each — round 45 **and** round 46 introduced none |
| introduction | `git log --all --reverse -S<serial> -- .` | 9 count-changing commits: held 1 at `65a2254d`, 2 at `e1e1bb77`, 3 at `f9f58c0e` (all 2026-10-14); wave copies 24 at `f5910876` (2026-10-24) → 18 at `48f9fe09` → 21 at `f6ae0c36` (2026-10-25) |
| published extent | `git ls-remote --heads --tags`, then `git grep -c -F "$S" <sha>` per ref | 11 heads; `master` 24 files, the 8 `cursor/*` + `devin/wiki-link` + `wip/operator-save-20261023` heads 3 files each (their trees predate the wave copies); all commits present locally |
| capture boundary | `python3 -I quality/check-session-material.py --repo . --rev e0be61e4` | exit 1, `files=17101 findings=97`, `carrier_findings=0` — no finding names any of the 24 |
| redaction of the round-45 seat file | `git grep -c -F "$S" 4d22eeb -- .ufo/waves/round-45/w1/ExecLiveHost/verify-quotes.py` | exit 1, 0 occurrences; file present — M45-2's remedy holds |
| untracked tree | `git ls-files --others --exclude-standard` + bytewise scan | 891 untracked lane files at the final run, 0 carriers (count drifts as wave seats write) |
| fleet index | `git -C <fleet> grep -c -F "$S"`; `git -C <fleet> ls-files mado-shokunin \| wc -l` | 0 carriers / 0 indexed paths: the lane is a nested repo, so the fleet index cannot see it — the 24 are lane-tracked |

## Findings (each names what it attacks or supports)

1. **D2's count is confirmed and its composition is new.** 24 files = 3 held + 21 copies, not the closure's "21 copies
   under round-32 and round-37, 24 total" only by luck of arithmetic: the split is 18 + 3, i.e. 6 + 1 fixture trees.
   Attacks the closure sentence "21 wave files under `.ufo/waves/round-32/` and round-37/" only in the sense of naming the
   trees; the total agrees (supports D2).
2. **The gate cannot see any of the 24, structurally.** `quality/check-session-material.py:255-256` lists only tracked
   files under `.ufo/` (so the three `corpus/knowledge/` carriers are out of path scope), and R3 matches a JSON object with
   a non-empty `serial` (`:26`, `:223-230`), so prose copies never match. Measured: 0 of 97 findings on a carrier.
   Supports M45-2's `captured-by: none`; supplies the reason a prose rule (D3) is the only thing that could catch it.
3. **The exposure is 11 pushed refs, not one history.** Every remote head carries it (24 files on `master`, 3 on each of ten
   side heads). Removal is therefore a multi-ref rewrite — this is the concrete basis for "removal from pushed history is
   the operator's decision" now stated in the draft block. No lane action can do it, and none was attempted.
4. **Age.** Held carriers since 2026-10-14 (12 days at 2026-10-26), wave copies since 2026-10-24/25 (2 days) — mined into
   the block for considera proposal 3's age count. No round-45/46 introduction (`0c89478` → `e0be61e4` flat at 24).
5. **The drift is in the lesson, not the tree.** `git diff 0c89478 4d22eeb` introduced nothing, and M45-2's own remedy was
   executed (seat file clean at `4d22eeb`); the defect is the count sentence at `round-45.md:49-51`, which is exactly what
   the appended block replaces without touching the remedy.
6. **Observed, not adjudicated:** round-45 closure D4's 4 MB untracked `w1/MutC1Counter/results.json` is absent and
   `results.digest.txt` is present; I did not verify that as D4 closure (not my item) and it carries no serial (scan above).

## Touched surfaces

Written (all inside my seat scope):
`mado-shokunin/.ufo/waves/round-46/w1/ScrSerialCorrection.md` (this report),
`mado-shokunin/.ufo/waves/round-46/w1/ScrSerialCorrection/{correction.md, verify.py, receipts/01-census-4d22eeb.txt,
receipts/02-revs.txt, receipts/03-pickaxe.txt, receipts/04-refs.txt, receipts/05-untracked.txt, receipts/06-gate.txt}`.
Read-only: `corpus/lessons/round-45.md`, `corpus/lessons/round-45-verifier-spotcheck.md`,
`.ufo/waves/round-46/registration.md`, `quality/check-session-material.py`, read-only git on the lane and the fleet,
`hyprctl monitors all -j | version`-class reads only. No git/jj mutation anywhere; no file under `/home/vgpnk/Projects/shokunin`
outside the lane and my seat was created or modified. `/fast/scratch/hyaku/mado-r46/ScrSerialCorrection/` removed at the end
(only `gate.out` lived there; its summary is in the seat receipt).

## Out of scope / handed on

- **Gate prose rule (D3 / D2's second half):** not implemented — seat bounds forbid editing tracked files and the target is
  the correction draft. The block states the boundary and names it as routed; the rule needs a predicate for a bare
  serial-shaped literal in prose plus a fixture pair that fails on the 24 carriers and passes on a scrubbed copy.
- **Pushed-history removal:** operator's decision, stated in the block; needs rewriting all 11 heads.
- **Held-entry rewrite:** not attempted (append-only discipline), and not needed for D2.

## Limits

- The serial is the monitor's current value; if the connector changes, the counts would need a re-run (`verify.py` does that
  from the live read, so a stale count fails loudly rather than silently).
- Ignored paths and anything outside the lane were not scanned; the fleet index holds none of the lane.
- The block's sentence-level claims about the three held entries stop at "each carries the value at the cited line"; I did
  not judge whether their surrounding prose is otherwise safe.

## Tool state

No installs, no upgrades, no pacman (host-wide pause respected). Python 3.14 stdlib only; `git`, `hyprctl` as shipped.

Report: .ufo/waves/round-46/w1/ScrSerialCorrection.md
