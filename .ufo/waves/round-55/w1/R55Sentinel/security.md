# Round 55 w1 — R55Sentinel security and privacy review

Lane HEAD `dbc2eefe`; freeze commit `54dacbd` is an ancestor. Scope: committed pins, C2 fixtures, hold-out isolation, host reads, C2 tool contract (registration §C2). Evidence: `receipts.txt` in this directory. Shape only: no value that I judged secret is printed.

## Verdict

- Pins and fixtures: no secret-shaped content. Clean.
- Hold-out isolation: **defect**. The sealed reveal path `fixtures/c2-holdout` is committed in five files, and the contract says seats are not told the path (F1).
- Host reads in this seat: read-only verbs only. Clean.
- C2 contract: the 1048576-byte bound covers regular-file size only when enforced by a bounded read, not `st_size`. Special files are covered by the regular-file rule only if the open is non-blocking. Symlinks, aggregate input, argv-supplied names, JSON depth/digit limits and encoding are not covered by the text and need explicit rules (F2–F4).

## 1. Pins and fixtures (secret shape)

| Object | Bytes | sha256 (prefix) | Result |
|---|---|---|---|
| `fetch/host-input.conf` | 1584 | `3769c92a…` | equals `frozen-tables.json` pin hash and live `~/.config/hypr/input.conf` (cmp identical). Contents: keyboard layout and options, repeat, numlock, touchpad, two windowrules. No key/token/password/cert markers. Two long tokens, both `wiki.hypr.land` URL paths. |
| `fetch/host-getoption.json` | 179 | `5557e28f…` | three records (`option`, `int`, `set`). Clean. |
| `fixtures/c2/F01–F18` | — | — | Long-token hits are repository-relative paths in `args.json`. No key material, no `/home/vgpnk` strings, no non-ASCII or control bytes. |
| `ctl/*.py` | — | — | No secret-shaped content. |

Privacy note (low, not a defect against the contract): the committed host pin publishes the operator's keyboard layout (`kb_layout = br`), touchpad settings and window-class rules. The contract requires this input, so it stays; the L1 should know it is in the repository history.

## 2. Hold-out location (F1, medium)

The contract (registration §C2, and §Seat boundaries) says the hold-out is "not a seat input", "seats are not told its path", and the L1 holds it "outside the repo". Committed files still name the location:

- `frozen-tables.json:301` (54dacbd): `"holdout_dir": ".ufo/waves/round-55/fixtures/c2-holdout"`
- `registration.md:108` (54dacbd): reveal destination `fixtures/c2-holdout/`
- `make-w1-spec.py:52` (dbc2eefe): builder prompt for R55ExecC2Harness
- `w1-spec.json:94` (dbc2eefe): same builder prompt, committed after the freeze
- `w1-dispatch.json:367` (dbc2eefe): same builder prompt

Effect: the builder seat R55ExecC2Harness was handed the reveal path, and every seat that reads the committed dispatch can read it. Lane `fixtures/` holds only `c2/`, so no hold-out content is in the lane. I did not open or search for the path (the only action was `find fixtures -maxdepth 2` and grep of committed text for the name).

Smallest remediation (for the L1; not applied, because the contract is frozen): confirm the builder seat did not touch any `c2-holdout` location; treat the path as disclosed in the integration receipt; have the L1 keep the hold-out's actual location outside anything a seat can derive from the committed name; do not reuse the name for a new reveal.

## 3. Commitment strength (F5, informational)

`holdout_commit_sha256` is a commitment, not a secret. The hold-out fixtures are short keyboard configs; a seat that knows the grammar can enumerate candidate bytes and test them against `1275d7f8…`. This is the attack surface R55CritHoldout is assigned to; I record it here so the C2 review does not assume the commitment hides the content.

## 4. Host reads (seat context)

Run by this seat, all read-only (outputs in `receipts.txt`):

- `sha256sum ~/.config/hypr/input.conf`, `cmp` against the pin, `wc -l`
- `hyprctl version`
- `hyprctl getoption input:repeat_rate -j`, `input:repeat_delay -j`, `input:numlock_by_default -j`
- `hyprctl devices -j`, written to the seat scratch, with keys listed only. Its 14 `address` fields were not copied; the file was deleted with the scratch.

No `hyprctl keyword`, `dispatch`, `source`, `reload`, `bind` or `call` was run. Across the lane, every `hyprctl keyword|dispatch|source` mention I found is prose (prohibitions, or research notes about the Hyprland source). The live values match the pin (40 / 250 / 1), so the pin is current.

## 5. C2 tool contract — risks and bounds

Covered by the contract text: `--config`/`--getoption` read only named files; regular-file check (directory, FIFO, non-regular → `unreadable`); 1048576-byte file bound → `too_large`; usage on any other argv shape; `bool` excluded from `int`; no subprocess, socket or write.

Covered only if the implementation follows a rule the text does not state:

| # | Risk | Contract coverage | Needed rule | Evidence (draft tool, read-only probes) |
|---|---|---|---|---|
| R1 | Stat-then-open race: a regular file is swapped for a FIFO between check and open, so the read blocks | "non-regular path" only | Open with `O_NONBLOCK`, then check `fstat` mode on the descriptor before any read | Draft does this; `--config <symlink→FIFO>` returns `unreadable` in 5 s timeout, no hang |
| R2 | Special files: char device, FIFO, directory, stdin pipe | covered by "non-regular" | Same as R1 | `/dev/zero` → `unreadable`, rc 2 |
| R3 | Symlinks: contract silent | not covered | Decide explicitly. Recommended: follow symlinks, but check the target type on the descriptor (R1). Draft accepts symlink→regular file | `link.conf→ok.conf` → accepted, rc 0 |
| R4 | Size from `st_size`: procfs/sysfs report size 0 or 4096 while content differs, so a `st_size` check lets arbitrarily large content through | "a file over 1048576 bytes" does not say how size is measured | Bounded read of at most 1048577 bytes, reject if more; never trust `st_size` | `/proc/self/status`: `st_size=0`, read length 1528. Exactly 1048576 accepted; 1048577 → `too_large` |
| R5 | Aggregate input: N `--config` files of 1 MiB each, no total cap | not covered | Explicit rule needed. A total cap would add a fifth SETUP reason, so the L1 must either accept the argv-bounded total and document it, or amend the contract | 20 × 1 MiB: 0.027 s; 200 small: 0.017 s. Argv (~2 MiB ARG_MAX) bounds the count, so practical risk is low |
| R6 | JSON depth bomb in `--getoption`: nesting past the parser recursion limit raises `RecursionError`, which is not `ValueError`; a naive `except ValueError` gives a traceback and rc 1 | "not a JSON object → bad_json"; depth not stated | Catch `RecursionError` as `bad_json` (or state a depth bound). Draft catches it | 100000-deep nesting in an object → `SETUP bad_json`, rc 2, no traceback |
| R7 | Huge integer literal: Python int-digit limit raises `ValueError` | not covered; a valid JSON object with an integer that Python will not parse | Rule needed: parse failure → `bad_json` (draft) or ignore the record. Pick one and state it | 5000-digit `"int"` → `SETUP bad_json`, rc 2 |
| R8 | NaN/Infinity: not valid JSON, so draft maps to `bad_json` | silent (object that is "not a JSON object" vs. record with non-integer int) | State it. Strict reading supports `bad_json` | Draft `parse_constant` raises → `bad_json` |
| R9 | Encoding of `--getoption`: contract says UTF-8 with replacement for config only | silent for getoption | State: getoption decoded strictly, failure → `bad_json` (draft does this) | — |
| R10 | Output injection via `--keyboard NAME`: NAME is printed verbatim; a newline in NAME forges a `MADO_KBDOPT: DONE` line | NAME unrestricted | Rule: NAME must not contain bytes < 0x20 or 0x7F (or must be printed escaped); otherwise usage. Draft prints verbatim | `--keyboard $'x\nMADO_KBDOPT: DONE … live=AGREE'` → forged line on stdout, rc 0 |
| R11 | `--keyboard '*'` collides with the default row | silent | State that the row is printed identically; ambiguity only | Not exploitable |
| R12 | Config content echo: device names and values never reach stdout | implicit in the output grammar | State it. Verified in draft: output carries only argv NAMEs and integers | Draft code review |
| R13 | Output of partial results before a later setup failure | "Setup failure: stdout exactly" | Rule: buffer all output and write only on success (draft does) | — |
| R14 | Unexpected exceptions (`MemoryError`, `BrokenPipeError` from `| head`) give rc 1 that the harness reads as a verdict miss | exit code rule covers only 0 and 2 | Rule: catch all exceptions to rc 2 with a setup reason, or document | Not triggered in probes |
| R15 | `--config` path traversal: no sandbox | argv is trusted | Accept. The tool's only information channel is integers parsed from any readable file, so the oracle is existence, size class and integer values; no content echo. The harness must pass only lane-relative committed paths | `--config /proc/self/status` → accepted, 25 defaults, no content echo |

## 6. Findings list

- **F1 (medium)** Hold-out path committed and handed to a builder seat: §2.
- **F2 (medium, implementation)** R1, R4, R6, R7 need explicit rules before the counter's C2 control can be trusted; the draft already has them.
- **F3 (low)** R10 output injection via argv. Rule needed.
- **F4 (low)** R5 aggregate input unbounded. L1 decides: document or amend.
- **F5 (informational)** Commitment brute-forceability: §3.
- **F6 (low, privacy)** Host pin publishes keyboard layout and input settings: §1.
- **Not a finding** Pins, fixtures, ctl files and host reads are clean; no secret-shaped content, no non-read host verb.

## 7. Not verified

- The hold-out directory's real state on this host: not checked, by rule.
- The draft tool is a sibling's untracked file; I ran it read-only from the scratch directory against my own probe files. Its final committed form may differ.
- Symlink policy (R3) and aggregate policy (R5) are recommendations; the contract text does not decide them.
- No tools were installed or upgraded.
