# w2 / RevErrataR45 — R4b append proof re-run + negative controls (falsify)

Seat: RevErrataR45 (w2, FALSIFY). Attack: the R4b round-45 errata append (`.ufo/waves/round-48/w1/ExecErrataR45/block.md`)
must keep the frozen round-45 C2 counters' TARGET_MET verdict after an append-only edit, and invalid wording must miss.
Instruments: `quality/counters/c2-r45-monitor-entry.py` (PRED-C2-r45, sha256 `34fcc783b6e652b44f751fceb3af71626868d265758a6657f2af409cc75c51f6`)
and `quality/counters/c2-r45-monitor-entry-v2.py` (PRED-C2-r45-v2, sha256 `ba19bee12030fa6c0d0ec310b718c0c4278b3c14bdf9b9f708ef256f9783da4f`),
both byte-equal to the round-48 freeze commit `3e6c848a0e1bbc9c7058226b86d0faefc5351c9d` (`git diff 579f694b..3e6c848a -- <counters>` empty).
Block sha256 `7865c15e07bce4a3e63d11372909d71ef89e47f7e8f94e7bc3568e47c179ae22`, 51 lines. Landed entry at all three scored revisions:
sha256 `128df1bd1055fcbb09f611c48286cd013e9d8bade992f4c17e81ba0615bb9c7b`.

## Method (and the forced deviation from W1's script)

W1's committed `counter-append-test.sh` was re-run verbatim first, under this seat's required writer bound
(`ulimit -f 2048` = 1 MiB/file). It aborted at clone checkout: the lane tree has 20,996 files, the git index exceeds
1 MiB, and checkout/index writes died with `error: unable to write file .ufo/waves/round-21/...`,
`fatal: sha1 file .../.git/index.lock write error: File too large` (W1 and the L1 receipt ran without that bound).
I therefore re-executed the script's exact logic index-free (`receipts/driver2.sh`, preserved):

- `git clone -q --shared --bare` (objects via alternates; no worktree, no index);
- appended states built with plumbing only — `show base:ENTRY` + `cat block`, `hash-object -w`,
  three-level `ls-tree <dir>/` + `mktree` + `commit-tree -p base` (assert root tree changed);
- counters run rev-addressed on the bare clone (`python3 -I <counter> --repo $B --rev <rev>` — both counters read
  only `git show rev:path`, no worktree reads);
- the locator verifier ran on a synthesized read-only tree (verifier-read paths copied from the clean lane worktree,
  entry synthesized to the appended bytes, `.git` file pointing at the bare clone);
- control-1 used W1's own transform (the source id `(S303)` put back into E6).

Scratch `/fast/scratch/hyaku/mado-r48/RevErrataR45/` created explicitly, `trap 'rm -rf -- "$S"' EXIT`,
`ulimit -f 2048` in every writer shell. Largest file written all run: 213,593 B (scratch pin copy; deleted);
largest surviving evidence file 15,857 B. Scratch verified empty after the run. The lane was never written;
the pre-existing dirty `corpus/knowledge/hyprland-monitor-rule-r45.md` in the lane worktree (L1's pending data edit)
is exactly the block append (51 insertions, 0 deletions), and its content hash equals my plumbing-built appended blob.

## Results — append proof (before / after)

Command shape: `python3 -I <counter> --repo <bare clone> --rev <rev>`; appended commit = landed entry + block.

| revision | phase | PRED-C2-r45 | PRED-C2-r45-v2 | appended commit |
|---|---|---|---|---|
| `4d22eeb66c28` (round-45 tip) | before | MET, exit 0, clauses a-j all 1 | MET, exit 0 | — |
| `4d22eeb66c28` + block | after | **MET, exit 0** | **MET, exit 0** | `8a6ae3dff439a594da343f8ee68cab1c44bcf936` |
| `579f694b45c7` (round-48 base) | before | MET, exit 0 | MET, exit 0 | — |
| `579f694b45c7` + block | after | **MET, exit 0** | **MET, exit 0** | `e8a5b8d032a0b681261cb247353651b4901455f5` |
| `3e6c848a0e1b` (round-48 freeze) | before | MET, exit 0 | MET, exit 0 | — |
| `3e6c848a0e1b` + block | after | **MET, exit 0** | **MET, exit 0** | `d49a49148b4a3048fb621f9c6fca23c98150edf6` |

Appended entry at every revision: 158 lines, sha256 `73a6c4ace54592c9b75848a89b5d96e6362ca893ec202c256695586f8b1ffa0e`
— byte-identical to W1's committed proof and to the L1's pending data bytes. No clause moved in any of the six runs.

## Results — six locators

Full `verify-locators.py` (W1's committed checker) on the appended trees, exit 0, `RESULT: checks_failed=0` at both
`579f694b…+block` and `3e6c848a…+block` (full transcripts in `receipts/verify-locators-w2-<rev>.txt`):

- E1 ×10 citation checks (Hyprland-Monitor.cpp:302/:389/:275/:283/:286/:264/:108/:271/:275-287,
  Monitor-efb5099.hpp:357), anchors `m_enabled = true;`, `if (monitorRule.m_disabled) {`, `m_enabled = false;` all cited OK;
- E2 receipt-line locators: draft receipt lines 1/4, landed receipt lines 3/4/7/8/9 (`verdict=AGREE`, `verdict=OK`,
  `exit=0`, tool shas `c6ac5fc2…` absent / `2f007417…` present) all OK;
- E3 ×4 (`DELTALESSTHAN` macro at Hyprland-macros.hpp:40 anchor cited OK; :836-837, :838-839, :903);
- E4 ×3 (a9902ea: 29 files, legacy ConfigManager.cpp −2184 deletions, raw file `404: Not Found`,
  `enum eConfigManagerType` at hpp:27-28, only `CONFIG_LUA` left);
- E5 ×4 (aqua Output.hpp:258, DRM.cpp:2101 sole `description` assigner, Wayland/Headless/Output createOutput carry none);
- E6 ×2 (MONITOR_FIELDS[] at LuaBindingsConfigRules.cpp:80, lua ConfigManager.cpp:809-810);
- plus: 14/14 round-45 pins byte-identical to `fetch-sha256.txt`, all five wording tripwires OK, all negative probes OK,
  landed-prefix fact OK.

## Results — negative controls (invalid wording must miss)

All appended at the freeze revision, both counters scored on the resulting commit:

| wording | v1 | v2 | failing clause |
|---|---|---|---|
| S-id put back in E6 (W1 control) | MISSED exit 1 | MISSED exit 1 | g:0 both |
| round-47 block as drafted (W1 control) | MISSED exit 1 | MISSED exit 1 | g:0 both |
| census contradiction `default_refresh=59 refresh_tolerance=3` (w2 mutant) | MISSED exit 1 | MISSED exit 1 | h:0 both |
| BAD_LOC marker `bit.ly` (w2 mutant) | MISSED exit 1 | MISSED exit 1 | i:0 both |
| foreign fenced block (w2 mutant) | MET exit 0 | MISSED exit 1 | v2 b:0 (T3) |

## Findings

1. **No falsification.** The R4b append keeps the frozen round-45 counters' verdict at every scored revision
   (before/after identical, all clauses 1), and the landed bytes are identical to W1's proof and to L1's pending data.
2. **Invalid wording misses** in every class the instruments declare: uncited source id (g), census-value
   contradiction (h), BAD_LOC marker (i), foreign fence (v2 b/T3). W1's two controls reproduce exactly.
3. **Residual, declared, not a defect in the current instrument set:** PRED-C2-r45 (v1) admits a foreign fenced
   block; it was superseded by PRED-C2-r45-v2 precisely for that class (T3), and the v2 counter — the operative
   instrument — misses it. If any integration still cites v1 as authority for the round-45 entry, cite v2.
4. **Execution constraint worth remembering:** any seat bound of 1 MiB/file makes worktree checkouts/commits of this
   lane impossible (index ≈ >1 MiB over 20,996 files); plumbing-only commits in a shared bare clone are the
   reproduction path (driver preserved in `receipts/driver2.sh`).

## Evidence files (this seat)

- `receipts/counter-append-test-w2.txt` — full counter matrix (baselines, appends, 5 negative wordlings)
- `receipts/verify-locators-w2-579f694b45c797a9c39761fdb4f9e0a1b71b3585.txt` — locator check, exit 0, 0 fails
- `receipts/verify-locators-w2-3e6c848a0e1bbc9c7058226b86d0faefc5351c9d.txt` — locator check at freeze, exit 0, 0 fails
- `receipts/driver2.sh` — the exact index-free driver (scratch deleted by its own trap)

No installs were performed; no pacman transaction was run. No tracked lane file, registry, counter, fixture or
sibling path was written.
