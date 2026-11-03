# Source-registry scout findings — candidate row for R66ScribeSources

Seat: R66ScoutSources (leaf) · lane `mado-shokunin` · lane HEAD `ed980316e330703030d0c17b2a7098e058295b99` · date 2026-11-03.
This is a **draft for the sources scribe**; no registry row was edited. Only `corpus/SOURCES.md` was read.

## Decision update (2026-11-03, after scribe reply)

L1 directed the round's sourced-claim row to the GNU Bash 5.3 exit-status source for C2; **S435 was allocated to that
Bash row and this CPython candidate is not appended this round**. My first collision check was scope-true but
**URL-false**: the candidate reuses S108's exact `subprocess.rst` URL and byte-identical file, so the lane census would add
`W04 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/subprocess.rst across scopes`
(W04 is URL-based, not scope-based; the r66 start census has 36 W04 lines). The row stays valid as a future candidate only
if a later round accepts that URL duplicate or a distinct artifact/anchor is used. Fit limit confirmed: the distinctive
`returncode` clause (negative signal number) does not describe C2's crash control (rc=2 is not signal death), so the Bash
rc-class table is the better C2 source. Everything below is retained as the audited candidate record.

## Policy actually in force

- Lane header, `corpus/SOURCES.md:3-7`: contract v1 canonical copy is fleet-root `CORPUS.md` § SOURCES.md (kaika provenance); "Only `status`, `recheck` and `used-by` change in place, each logged old→new in that round's lesson."
- Fleet-root `CORPUS.md:64-160` carries the whole contract (kaika `SOURCES-CONTRACT-v1.md`, frozen). Rule 1: a row is a claim, written only after opening the source **in the round that writes the row**; the round lesson's `## Gate` records URL, access date, and a ≤25-word located quote grounding `teaches`. Rule 2: append-only; a correction is a new `supersedes S0NN —` row. Rule 6: no credential/session/private URL material.
- Row shape: 11 cells (NF=13 with outer pipes); `id` = next unused `S###`, never reused; `community` is never tier A; `mined` requires ≥1 existing `used-by` path.
- Census commands and expected-shape checks are in `CORPUS.md:135-160`; run from the lane root.

## Current ID tail (census start, measured 2026-11-03)

```
rows (grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md) = 371
malformed rows (NF!=13)                                                      = 0
tier histogram                                                               = A=357 B=7 C=7
status histogram                                                             = mined=350 queued=10 rejected=11
duplicate ids                                                                = (none)
mined rows whose used-by paths do not exist                                  = (none)
max used id = S434; next unused id = S435
```

There are 63 never-allocated IDs inside 1..434 (first gap S190-S194); they are **not** to be backfilled. `S434` is the last row (Microsoft Learn `DISPLAYCONFIG_2DREGION`, Windows desktop-plane material). Allocate **S435**.

Collision check for the proposed scope — no existing row covers child exit-status/returncode semantics:

| row | scope actually covered |
|---|---|
| S108 | `subprocess.rst` **`args` command parameter only** (`run`/`Popen`/`call`/`check_call`/`check_output`), same tag/hash |
| S110 | GNU Bash 5.3 `set -e` exception set | 
| S113 | `os` §Process Management — which entry points spawn |
| S115 | `Lib/subprocess.py` `list2cmdline` formatter |
| S117 / S119 | `imaplib` `IMAP4_stream.open` → `Popen` |

So a new row at the same tag/file but a **different documented attribute** is admissible; it must not be worded as a correction of S108 and must not touch S108's `opened` column (the r65 defect: existing `opened` cells were edited instead of appending).

## Independent open performed this round

- URL opened (raw tagged source): `https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/subprocess.rst`
- Bytes: 61,603 B, sha256 `05cd782c5181481ad961788dd678b99c903eb3ff53e0ebab3095c38b48c74dfd` — **identical to the hash S108 already records**, so the file binding is already landed; this row adds a new scoped anchor, not new bytes.
- Tag identity independently re-checked with `git ls-remote --tags https://github.com/python/cpython 'refs/tags/v3.14.8*'`:
  - annotated tag object `992560c2cc62d47b308cec662feb485456847931`
  - peeled commit `8e6e75d9102e39bed2a2b279203a396741180f12`
  Both match S108's recorded anchor.
- Located quote (`Doc/library/subprocess.rst:242-243`, CompletedProcess.returncode), **23 words**:
  "Exit status of the child process, an integer. If the process exited due to a signal, this will be the negative signal number."
- Same file `:949-959` (Popen.returncode) documents the code is set by `poll`/`wait`/`communicate` only after termination and is negative for signals (POSIX); `:961-964` documents the `shell=True` caveat (`128+N` mapping is the shell's).

## Proposed row (append-only; one line, 11 cells)

```
| S435 | CPython 3.14.8 library reference, `subprocess` — CompletedProcess/Popen `returncode` — https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/subprocess.rst | docs | A | documented exit-status semantics of a completed child process (CompletedProcess.returncode, Popen.returncode); not any instrument's rc-to-verdict mapping | tag `v3.14.8` → annotated tag object `992560c2cc62d47b308cec662feb485456847931`, peeled commit `8e6e75d9102e39bed2a2b279203a396741180f12`; file 61,603 B sha256 `05cd782c5181481ad961788dd678b99c903eb3ff53e0ebab3095c38b48c74dfd`; `Doc/library/subprocess.rst:240-243` CompletedProcess.returncode, `:949-959` Popen.returncode | A child's exit status is documented as an integer, typically 0 for success and negative `-N` for signal `N`; the page does not establish any counter's rc-to-verdict mapping or that a child ran | mined | 2026-11-03 | on-release | corpus/lessons/round-66.md |
```

Status dependency: `mined` is only truthful if `corpus/lessons/round-66.md` exists at landing and cites S435. That file **does not exist yet** (checked 2026-11-03; R66ScribeLesson owns it). If the lesson will not cite S435, land the row as `queued` with `used-by —`, or the census's "mined rows whose used-by paths do not exist" check will flag it. Coordinate S435 explicitly with R66ScribeLesson.

## Gate block text for `corpus/lessons/round-66.md` § Gate

```
- S435 — URL: https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/subprocess.rst
  (tag v3.14.8 → tag object 992560c2cc62d47b308cec662feb485456847931, peeled commit
  8e6e75d9102e39bed2a2b279203a396741180f12; 61,603 B sha256 05cd782c…); accessed 2026-11-03;
  located quote `Doc/library/subprocess.rst:242-243` (23 words): "Exit status of the child
  process, an integer. If the process exited due to a signal, this will be the negative signal
  number."
```

## Instructions to the scribe, and limits

1. Read `corpus/SOURCES.md` latest IDs immediately before allocating; the registry may have grown since this scout (measured 371 rows / max S434 / next S435 at `ed980316`). Never reuse an ID.
2. Append exactly one `docs`/A row for the narrow scope above; do not edit any existing row's `opened` column. If you change any `status`/`recheck`/`used-by`, log the old→new pair in the round lesson per Rule 2.
3. Search log: record the question ("what does official CPython documentation say about a child process's return code?"), where searched (python/cpython raw at tag v3.14.8), date 2026-11-03, identified/screened/included/excluded, exclusion reasons, stop rationale (Rule 5). Use the exact URL and bytes hash above.
4. Census start (record now) and end (L1 records after landing): rows 371→372 expected; malformed 0; tier A 357→358; status mined 350→351 (or queued 10→11 if the lesson does not cite); duplicate ids none; mined-missing none. Run the block in `CORPUS.md:135-160` from the lane root.
5. **The source cannot prove row truth or child invocation.** It documents the vocabulary of an exit status only. It does **not** say rc=1 means RED, rc=2 means crash/ERROR, or that any marker was emitted; those are the frozen C1/C2 predicates and must stay limits, not source claims. Do not let `teaches` imply the counter's mapping is documented.
