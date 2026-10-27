# CritC1Args — adversarial ARG review (round 50 w1)

## Verdict
No mismatch found in 5,005 argument comparisons. This supports the landed `tools/mado-keysym.py` ARG resolution for the tested host `xkbcli-how-to-type` 1.13.2 and compiled `us` keymap; it does not prove all ARGs, keymaps, or future library versions.

## Reproduction and evidence
- Host judge: `/usr/lib/xkbcommon/xkbcli-how-to-type`, sha256 `f6c0b122ad90c9e30086653517c51f4b2203b6c7c07bcbc89c71e55ab2927e54`.
- Keymap: generated with `env -i PATH=/usr/bin HOME="$S/home" XDG_CACHE_HOME="$S/cache" XDG_CONFIG_HOME="$S/config" XDG_DATA_HOME="$S/data" XDG_STATE_HOME="$S/state" xkbcli compile-keymap --layout us`.
- For every ARG, compared `(returncode, stdout bytes)` from judge `--keymap=<keymap> --disable-compose --keysym ARG` against the landed Python tool with identical options and isolated HOME/XDG environment.
- Result: `pairs=5005 mismatches=0 rc_pairs=[('(0, 0)', 556), ('(2, 2)', 4449)]`.
- Corpus included all decimal `0x1000000..0x10000ff` plus 0x spellings; `0x1000100`, `0x110ffff`, `0x1fffffff`, `0x20000000`, decimal 536870911/536870912; `U` and lowercase `u` patterns spanning 1..9 hex positions and Unicode/surrogate/overflow boundaries; case variants of `XF86_`; digit names 0..9; `NoSymbol`; whitespace, signs, trailing/leading whitespace, non-ASCII; plus deterministic random structured strings until 5,000 unique ARGs.
- Embedded NUL: not testable in argv because POSIX `execve` strings cannot contain NUL.

## Findings / axes
No defect to route. Supports C1 instrument ARG handling at the coverage/operability boundary; no claim about keymap traversal or the frozen counter. Unexercised space remains, notably all 2,638 names and exhaustive decimal/hex forms; this is a bounded adversarial sample, not exhaustive proof.

## Smallest safe correction
None indicated by this sweep. Preserve the existing parser; do not alter behavior based on an unobserved mismatch.
