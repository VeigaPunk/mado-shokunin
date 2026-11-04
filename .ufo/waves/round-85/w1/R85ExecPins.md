# R85ExecPins — round-85 primary source pins

Seat: R85ExecPins. Owns: `.ufo/waves/round-85/fetch/` and this report. Scratch was under `/fast/scratch/hyaku/mado-r85/R85ExecPins/` and was removed before yield.

## Pins (committed bytes under fetch/)

| source | URL | status | pinned file | sha256 | bytes | fetches |
|---|---|---|---|---|---|---|
| S488 POSIX.1-2024 Shell & Utilities | https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html | 200 x2, byte-identical | `fetch/S488.bin` | 0889867a53fe12508a71e8739ec23ecdddc95e6f67697c98e26acc8ff0ec1acd | 357953 | both 200 |
| S489 GNU Bash Reference Manual §3.7.6 | https://www.gnu.org/software/bash/manual/html_node/Exit-Status.html | **UNREACHABLE — not pinned** | none | — | — | 5 attempts, curl rc 28 (connect timeout) |
| S489-alt Bash Reference Manual §3.7.5 (Chet Ramey copy, Edition 5.3) | https://tiswww.case.edu/php/chet/bash/bashref.html | 200 x2, byte-identical | `fetch/S489-alt-tiswww.bin` | b91026acffb159bd1e842e3116a95539bf858e2b57cbfa74df9e3a53379177a4 | 1040870 | both 200 |

Fetch command: `curl -sSL --max-time 60`. Fetch times (UTC): S488 20:06:43; S489 GNU 20:07:41, 20:08:53, 20:09:53, 20:10:53; S489-alt 20:14:48, 20:14:51.

GNU endpoint failure: DNS resolves www.gnu.org to 209.51.188.116 and 2001:470:142:5::116; TCP connect to :443 times out on both addresses (`curl: (28) Connection timed out after 60001 milliseconds`), reproduced over 5 attempts across about three minutes. The S488 host answered in the same window. No quote was taken from the GNU page.

Substitution: L1 directed S489-alt, a different URL on a different host (maintainer copy), not a re-fetch of the GNU URL. The S489-alt section number is 3.7.5, not 3.7.6. The declaration's locator should be corrected or the substitution declared.

## Grounding quotes (each ≤25 words)

**(a) pipeline exit status = last command's status** — S488, pinned `fetch/S488.bin`
- byte offsets **133030–133104**
- quote (12 words): "The exit status of the last (rightmost) command specified in the pipeline."
- context: table row "pipefail Enabled = no, Begins with ! = no" (the default-off rule). POSIX.1-2024 also defines `pipefail` (enabled case derives status from all commands). Do not state "last command" as universal.

**(b) command killed by signal N → 128+N** — S489-alt, pinned `fetch/S489-alt-tiswww.bin`
- byte offsets **239046–239200** (raw span includes `<var>` HTML tags and one newline)
- quote (21 words, tag-stripped, newline normalised): "When a command terminates on a fatal signal whose number is N, Bash uses the value 128+N as the exit status."

**Not grounded by S488 for 128+N:** S488 says only "greater than 128" for signal termination.
- S488 byte offsets **109001–109128**
- quote (23 words, newline normalised): "Otherwise, if the command terminated due to the receipt of a signal, the shell shall assign it an exit status greater than 128."
- The C2 `signal` class (128+N) must rest on S489-alt (or S489 once retrieved), not on S488.

## Fetch-twice result
- S488: both fetches byte-identical (357953 bytes, same sha256); pin = fetch 2.
- S489-alt: both fetches byte-identical (1040870 bytes, same sha256); pin = fetch 2.
- S489 GNU: no bytes, no comparison possible.

## Harm / scope
- Only `fetch/` and this report were written in the lane. No sibling, operator, state, MANIFEST, or fleet-root file was touched. No git commands were run. No tools were installed.
- A supplementary bash-5.2 `bashref.texi` (ftp.gnu.org tarball, 10950833 bytes) was downloaded to scratch only for corroboration. Lines 3538–3539 carry the same 128+N sentence. It is NOT pinned and must not be cited as S489.

## Locator note for L1
- The fetched POSIX page anchors Pipelines as **2.9.2** (`tag_19_09_02`), not 2.9.3. The `pipefail` option is present in POSIX.1-2024.

## Files
- `.ufo/waves/round-85/fetch/S488.bin`
- `.ufo/waves/round-85/fetch/S489-alt-tiswww.bin`
- `.ufo/waves/round-85/fetch/source-pins-r85.json`
- `.ufo/waves/round-85/w1/R85ExecPins.md` (this file)

## Remaining gap
- S489 (GNU URL) not retrieved. The S489-alt pin fills the 128+N grounding. L1 must decide whether the declaration accepts that substitution.
