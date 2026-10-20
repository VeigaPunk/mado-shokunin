# ReopenPyShlexSub — partly falsified: S107 and S108 re-verify byte-for-byte and support the shlex.join / keyword-args claims; the only mismatch is the note/SKILL list that cites S105–S107 for `json.dumps`, which no SOURCES row covers.

## Scope and method

Lane tip `a4046a8` (`round-20: lesson R19-V2 sentence carries S096 on its tally line`). Read-only git in the lane; all executable work in `/tmp/mado-r20w2-ReopenPyShlexSub` (`git clone` of the lane, `origin` removed, HEAD `a4046a8216080d4004de3f268c62cf142095ac07`, no tracked modifications). The four rows/Gate-line files I quote are committed at that tip: `git diff --stat a4046a8 -- corpus/SOURCES.md corpus/lessons/round-20.md SKILL.md corpus/knowledge/tripwire-precision-r20.md` is empty.

Fetched each pinned URL twice with `curl` (`-sSL --max-time 60`, tag URL and peeled-commit URL) into `.ufo/waves/round-20/w2/ReopenPyShlexSub/fetch/`; 9 receipts in `fetch/receipts.jsonl` (`mado-fetch-receipt-v1`), every body re-hashes to its receipt (8 mine + the wave-1 `SrcPyShlex` 4 re-checked OK). Command used for the re-hash check: a Python loop over each receipt reading `bytes`/`sha256`/`http_status`/`final_url`; all printed `OK`. My w2 fetch bodies are untracked because the w2 tree is not committed; in the wave-1 fetch dir `.ufo/waves/round-20/fetch/.gitignore:2:*` ignores the bodies while `receipts.jsonl` is committed.

## S107 — `corpus/SOURCES.md:119`, Gate `corpus/lessons/round-20.md:44`

| check | observed |
|---|---|
| `sha256sum Doc/library/shlex.rst` | `819c6e6fab583c8d30e32950591ed1fda2b552cebcbfadc5d1619e3e35ea03b0`, 17,867 B — equals row, wave-1 receipt, and tag/commit fetches |
| `sha256sum Lib/shlex.py` | `aeda1c54188363d907654a19d338e5961416ebec2e2f506afab19be61ada8120`, 13,756 B — equals row |
| host `/usr/lib/python3.14/shlex.py` | same `aeda1c…`; host Python is 3.14.8 |
| `git ls-remote https://github.com/python/cpython refs/tags/v3.14.8 'refs/tags/v3.14.8^{}'` | `992560c2cc62d47b308cec662feb485456847931 refs/tags/v3.14.8` and `8e6e75d9102e39bed2a2b279203a396741180f12 refs/tags/v3.14.8^{}` — exactly the row's annotated tag object / peeled commit |
| commit-pinned raw fetches at `8e6e75d9…` | same sha256 as the tag fetches for all four files (rst/py) |
| Gate quote `:39` | line 39 is `   Concatenate the tokens of the list *split_command* and return a string.`; after RST de-markup the quoted sentence is present, 11 words (<= 25) |
| row quotes `:39-40`, `:46-47`, `:317` | exact in the fetched bytes (row quote retains `*split_command*` and `:func:`split``); `join` is `:315-317`, returns `' '.join(quote(arg) for arg in split_command)` |
| execution path | `quote` (`shlex.py:320-338`) only string-tests and quotes; `grep -n 'subprocess\|os\.system\|popen\|exec' shlex.py` → no match. The row's stated limit ("does not establish how the returned string is later used") is accurate |

Tool-side confirmation (clone tool sha256 `9613f510…`, equal to the a4046a8 committed tool): `CasePureFormatters--shlex-join.jsonl` → `MADO_TRIPWIRE: clean`, exit 0; `CaseShadowing--shlex-join-as-run.jsonl` (import alias `from shlex import join as run`) → clean, exit 0; my fixture `shlex.join(split_command=['sudo','pacman','-S','hyprland'])` → clean, exit 0. No finding/row appeared, which is what the note/SKILL claim predicts.

## S108 — `corpus/SOURCES.md:120`, Gate `corpus/lessons/round-20.md:45`

| check | observed |
|---|---|
| `sha256sum Doc/library/subprocess.rst` | `05cd782c5181481ad961788dd678b99c903eb3ff53e0ebab3095c38b48c74dfd`, 61,603 B — equals row, wave-1 receipt, and tag/commit fetches |
| `sha256sum Lib/subprocess.py` | `7fa4af83422024a19e64a80937f6c8094244c3397372a495b348dfbe44a5dd72`, 90,748 B — equals row |
| host `/usr/lib/python3.14/subprocess.py` | same `7fa4af…`; host Python is 3.14.8 |
| tag pin | same `992560c2…` / `8e6e75d9…` pair as S107; commit-pinned raw fetches agree |
| Gate quote `:43` | line 43 is `   Run the command described by *args*.  Wait for command to complete, then`; after de-markup the quote is present, 6 words (<= 25) |
| row quotes `:43`, `:900-901` | exact in the fetched bytes; row's cited lines `run :513-514`, forwarding `:555`, `Popen.__init__ :817-818`, `call :388/:396`, `check_call :405/:415-417`, `check_output :424/:473-474` all land on the stated code |
| probe `probe-kwargs.py` | worktree sha256 `42ee139265b51ac18b13b6c9bd0741975d25252a3c45ccaaba6548bd5c4c72c4` — equals the row's pin; copied to `/tmp` and re-run (`python3 -I`), output identical to `probe-kwargs.out`; stub `Popen`, no process created |
| all five entry points | my `/tmp/.../probe/probe-all.py` (stub `Popen`, host 3.14.8): `run`, `call`, `Popen`, `check_output`, `check_call` with `args=[…]` all deliver `{'args': [...]}` to `Popen`; `check_call` on rc 3 raises with `cmd=['example-prog']` — the row's `kwargs.get("args")` claim holds |

Tool-side confirmation: `CaseWrapperForms--spawn-kwarg-args.jsonl` (`subprocess.run(args=['pacman','-Q','hyprland'], …)`) → `package_query`, rule `pacman:-Q`, `"evidence": "observed"`, exit 1. The counterfactual ran: tool at `1f7f995` (`git show 1f7f995:tools/mado-tripwire.py`, sha256 `367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d`) on the same fixture → `MADO_TRIPWIRE: clean`, `unparsed_spawns: 1`, exit 0 — i.e. the keyword argv would have been missed before the repair. Alias+keyword (`run = subprocess.run; run(args=[…])`) and `subprocess.run(args=['sudo','systemctl','restart','iwd'])` both produce `observed` findings (package_query / host_mutation). No counterexample found.

## Gate lines

- `corpus/lessons/round-20.md:44` (S107) and `:45` (S108): quotes are present at the stated lines after RST de-markup, 11 and 6 words, both <= 25; sha prefixes `819c6e6f…` and `05cd782c…` equal the rows; tag pins equal.
- The S108 Gate's added note ("keyword `args=` binds the same slot (seat stub-Popen probe)") is **not** established by the `:43` sentence alone; it is established by the row's source lines and the probe, which the parenthetical names. There is no contradiction, but the Gate line is a summary of row evidence, not a claim the quote supports by itself.
- De-markup is the same-file convention, not a deviation unique to these rows: S106's Gate quote de-marks `:meth:`append`` and `*iterable*` (fetched `collections.rst` at the same tag, sha256 `be2f90d1…`, line 461-462, 14 words as stated). Row-level quotes in S107/S108 retain the RST markup and are exact.

## What the note and SKILL say, and whether these rows support it

- `corpus/knowledge/tripwire-precision-r20.md:33-34`: "Keyword argv (`subprocess.run(args=[...])`) is the same command slot as the positional one (S108)." — **supported** by the row (docs signature `run(args, *, …)`, source forwarding, probe) and by my all-five-entry-point probe.
- `SKILL.md:552-553`: pure stdlib callables include `shlex.join` (S105–S107) — **supported for `shlex.join` by S107** (source and tool scans above). SKILL does not cite S108; `grep -n 'S108' SKILL.md` has no match, so there is no SKILL claim about S108 to test beyond the note.
- **Counterexample (the only mismatch):** both `corpus/knowledge/tripwire-precision-r20.md:20` and `SKILL.md:552-553` group `json.dumps` under the S105–S107 citation. S105 is scoped to builtins (`frozenset`, `set`, `tuple`), S106 to `deque`/`Counter`/`namedtuple`, S107 to `shlex.join` only; `grep -n 'json' corpus/SOURCES.md` finds no json-module row (only `MANIFEST.json`/S041/S049/S094/S097 paths). `json.dumps` is in the tool's own `PURE_STDLIB_EXACT` (`tools/mado-tripwire.py:1413`) and my `json.dumps([...])` fixture scans clean, so the *behavior* is right — but the *sourcing* attributed to S105–S107 is not. Fix: add a pinned CPython json docs/source row (S113 is free) or remove `json.dumps` from the S105–S107 parenthetical in both files.

## Limits

- GitHub contents API blob-ID cross-check returned `403` "API rate limit exceeded" (four loop attempts, one retry with User-Agent). Substituted three independent checks: commit-pinned `raw.githubusercontent.com` bytes (same sha256 as tag-pinned), `git ls-remote` tag object → peeled commit, and host-file sha256 equality. API error bodies were not retained.
- `probe-kwargs.py` is untracked: `.ufo/waves/round-20/fetch/.gitignore:2:*`; `git ls-tree -r a4046a8 .ufo/waves/round-20/fetch/SrcPyShlex/` contains only `receipts.jsonl`. The row pins its sha256 and the worktree copy matches; I copied it to `/tmp` and ran it there, but a fresh clone cannot re-run it from committed bytes. The stub-`Popen` probe proves argument binding, not real process semantics; no process was created.
- Gate quotes are RST-de-marked (demonstrated on S106); if the Gate standard is read as byte-verbatim, both quotes differ from the raw file by the emphasis asterisks, with no word difference.
- The rows' own limits remain and are correctly carried: S107 does not establish how the returned string is later used; S108 does not establish that any transcript used the keyword form.
- [UNK] whether `json.dumps` was intentionally listed as a tool-list example with no source row; either way, no SOURCES row covers it.

## Installs

none
