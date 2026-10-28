# R55Sentinel — round 55 w1 report

Deliverable: `.ufo/waves/round-55/w1/R55Sentinel/security.md` (full review). Receipts: `.ufo/waves/round-55/w1/R55Sentinel/receipts.txt`.

## What I did

1. Read the committed pins `fetch/host-input.conf` and `fetch/host-getoption.json`, the fixture tree `fixtures/c2/`, and the `ctl/` stubs. Shape-scanned them for key, token, password, certificate and home-path markers, long tokens, and non-printable bytes. Result: nothing secret-shaped.
2. Checked that the pins match `frozen-tables.json` (sha256 `3769c92a…`, `5557e28f…`) and that the live `~/.config/hypr/input.conf` is byte-identical to the committed pin.
3. Ran read-only host verbs only (see below).
4. Grepped committed round-55 files (at `54dacbd` and at HEAD `dbc2eefe`) for the hold-out terms and the literal path `c2-holdout`. Did not open or search for any hold-out file.
5. Reviewed registration §C2 against the sibling draft `w1/R55ExecTool1/mado-kbdopts.py` (untracked, read only), and probed it from my scratch with my own files: special files, symlinks, the size boundary, `/proc`, argv output, JSON depth and digit limits, bool, aggregate input.
6. Removed my scratch after writing receipts.

## Commands and decisive output (trimmed)

```
sha256sum fetch/host-input.conf fetch/host-getoption.json
3769c92ab7660f1795cb6d0af1bcc5a5614a299b29ae8358d1b85936bdd47bf4  fetch/host-input.conf
5557e28f101946af19fe56fe6ec7b75e60df540c078daddec2d0512938e6eab6  fetch/host-getoption.json
cmp ~/.config/hypr/input.conf fetch/host-input.conf  -> identical
hyprctl version                       -> Hyprland 0.56.2 ... commit efb50993780079460b0cbed1363e2166a2de1d9f clean
hyprctl getoption input:repeat_rate -j           -> int=40, rc=0
hyprctl getoption input:repeat_delay -j          -> int=250, rc=0
hyprctl getoption input:numlock_by_default -j    -> int=1, rc=0
hyprctl devices -j                    -> rc=0; keys keyboards,mice,switches,tablets,touch; 10 keyboards
git grep -F 'c2-holdout' HEAD -- .ufo/waves/round-55  -> 5 committed files (listed below)
git diff --stat 54dacbd HEAD -- .ufo/waves/round-55   -> 5 files, 1025 insertions, all post-freeze generator/spec/dispatch/registry files
python3 -I mado-kbdopts.py --config /dev/zero         -> MADO_KBDOPT: SETUP unreadable   rc=2
python3 -I mado-kbdopts.py --config <symlink->FIFO>   -> MADO_KBDOPT: SETUP unreadable   rc=2 (no hang)
python3 -I mado-kbdopts.py --config <1048576 bytes>   -> rc=0
python3 -I mado-kbdopts.py --config <1048577 bytes>   -> MADO_KBDOPT: SETUP too_large   rc=2
/proc/self/status: os.stat st_size=0, read length 1528
git diff --name-only 54dacbd HEAD -- .ufo/waves/round-55  -> make-w1-spec.py, w1-dispatch.json, w1-run.err (empty), w1-spec.json, w1/swarm-registry.json; all post-freeze, 1025 insertions
--getoption 100000-deep nesting in an object        -> SETUP bad_json rc=2, no traceback
--getoption "int" with 5000 digits                  -> SETUP bad_json rc=2
--getoption "int": true                             -> ignored, live=? UNKNOWN
```

Hyprctl verbs run by this seat: `version`, `getoption … -j` (three), `devices -j`. None of keyword, dispatch, source, reload, bind, call. Every `hyprctl keyword|dispatch|source` string in the lane is prose.

## Defects and ambiguities (with input that shows them)

- **D1 (medium): hold-out location is committed and was given to a builder seat.** The contract says seats are not told the hold-out path. Committed files name it: `frozen-tables.json:301` (`holdout_dir`), `registration.md:108`, `make-w1-spec.py:52`, `w1-spec.json:94` and `w1-dispatch.json:367` (builder prompt for R55ExecC2Harness, committed at `dbc2eefe` after the freeze). Lane `fixtures/` contains only `c2/`. Remediation for the L1: confirm the builder did not touch any `c2-holdout` location; record the disclosure in integration; do not reuse the name.
- **D2 (contract gap): regular-file check is not enough.** Needed rules: non-blocking open before the type check (R1); symlink policy (R3); bounded read instead of `st_size` (R4, `/proc` reports 0); JSON depth and int-digit failures must map to `bad_json`, not an uncaught exception (R6, R7); encoding of the getoption file (R9). The sibling draft already implements R1, R4, R6, R7 and R9; the contract text does not.
- **D3 (low): argv output injection.** `--keyboard NAME` is printed verbatim, so a newline forges an output line (R10). Rule needed.
- **D4 (low): aggregate input unbounded.** The 1048576-byte bound is per file. No total cap (R5). The L1 must document the argv-bounded total or amend the contract; a total cap would add a fifth SETUP reason.
- **D5 (informational): commitment strength.** `holdout_commit_sha256` is a hash of short configs and can be tested by enumeration (§3 of security.md).
- **D6 (low, privacy): committed host pin** publishes keyboard layout and input settings. Required by the contract; noted only.

Not defects: pins, fixtures and `ctl/` contain no secret-shaped content; the live input.conf matches the pin; the pin hashes match `frozen-tables.json`.

## Deliverables

- `.ufo/waves/round-55/w1/R55Sentinel/security.md`
- `.ufo/waves/round-55/w1/R55Sentinel/receipts.txt`
- `.ufo/waves/round-55/w1/R55Sentinel.md` (this file)

No tracked file was edited. No git or jj mutation. No commits or pushes. No subagents, background jobs or installs. Scratch: `/fast/scratch/hyaku/mado-r55/R55Sentinel/`, removed before yield.

## Not verified

- The hold-out directory's real state on the host: not checked, by rule.
- The sibling draft tool is untracked and may change; my probes ran it read-only and only against my own files.
- Recommendations R3 (symlink) and R5 (aggregate) are not decided by the contract.
- The "handed to builder" statement rests on the committed dispatch text; I did not confirm delivery.
