# SimplifierEvidence — PRED-C1-r33-v1 / PRED-C2-r33-v1 one-command re-derivation

Scope: read-only audit of whether a closure can re-derive each after-state with ONE command
over committed bytes. Registration not edited. All outputs below were re-executed at write
time (2026-10-24), not copied.

## C1 — re-derivable: YES

Command:

```sh
python3 -I .ufo/waves/round-33/c1/count.py --root . --frozen .ufo/waves/round-33/c1/frozen.json
```

Inputs, all committed or landing-committed bytes (verified via `git ls-files`):

- `.ufo/waves/round-33/c1/frozen.json` — tracked; carries the cite set, blob paths, sha256
  digests, quote strings, and the target triple.
- `.ufo/waves/round-33/c1/count.py` — tracked; `-I` isolates from site/env; no network; no
  writes.
- `corpus/SOURCES.md` — tracked.
- Entry files `corpus/knowledge/waybar-module-text-route-r25.md`,
  `corpus/knowledge/event-delivery-limits-r26.md` — NOT in the tree yet (grep: no such file;
  absent from `git ls-files` and from the corpus/knowledge listing). The after-state includes
  creating both; once committed they are read from the tree like everything else.
- Fetch blobs — all four tracked: `.ufo/waves/round-33/fetch/{S190,S191,S197}.bin` and
  `.ufo/waves/round-32/fetch/S189.bin` (round-32 path, already landed).

Re-derivation proof, executed now:

- Live tree (after-state pending): `closed_entries=0 closed_rows=0 open_cites=4
  verdict=TARGET_MISSED`, exit 1.
- Golden scratch `.ufo/waves/round-33/controls/golden`: `closed_entries=2 closed_rows=4
  open_cites=0 verdict=TARGET_MET`, exit 0.

Enumeration check: the counter loops over exactly the frozen entries/ids (S190, S191, S197,
S189) from frozen.json; every frozen cite is individually tested (quote equality, 1–25 word
bound, `quote.encode() in blob` substring, sha256 against the frozen digest, first SOURCES row
prefix `| <id> |` with the entry path in its last used-by column). `open_cites=0` therefore
enumerates "every frozen cite closed" — no wildcard. A `predicate-drift` guard byte-compares
frozen.json's predicate string to the one compiled into count.py, so counter and registration
cannot silently diverge.

Caveat (not a failure): `--root .` reads the worktree, not HEAD. Re-derivation "over committed
bytes" means running it in a clean checkout of the landing rev; untracked scratch cannot affect
it because the counter opens only the enumerated paths.

## C2 — re-derivable: YES

Command:

```sh
python3 -I .ufo/waves/round-33/c2/count.py --repo . --scorecard SCORECARD.md
```

Inputs: SCORECARD.md (tracked; the verdict line is part of the after-state — currently absent,
see below) and the measurement half, which is genuinely committed-bytes-only: `git archive
d9ed38166cc3be8ef4c52b41d66ad94010feb047 corpus` → tar extract → the r32 counter embedded
verbatim in count.py (no external file to drift). The rev resolves and is an ancestor of HEAD
(`git merge-base --is-ancestor` → ok; HEAD `9a46ccf3282117f960b8d53cd71599a91f388ee3`).
Env deps: git, tar, bash, grep, awk — all present; the run below proves them.

Re-derivation proof, executed now:

- Current SCORECARD.md: `claim_mismatch=1 reason=absent verdict=TARGET_MISSED`, exit 1 (the
  `r33-claim-verdict:` line is not yet appended).
- Honest control `.ufo/waves/round-33/controls/c2-honest-card.md`: `claim_mismatch=0
  reason=match published=7 measured=7 verdict_word=honest-stop
  rev=d9ed38166cc3be8ef4c52b41d66ad94010feb047 verdict=TARGET_MET`, exit 0.

Enumeration check: "last line matching" is enumerated — the scan keeps the final regex match
in SCORECARD, anchored `^…$` with `verdict=(\S+)` and a 40-hex rev. "A missing line" →
`reason=absent` exit 1; "a wrong N" → mismatch exit 1; rev inequality → mismatch exit 1.
Same worktree caveat as C1 for the SCORECARD read.

## Universal words not enumerated

- FLAG — "Every scored axis is tied at 1.0" (registration preamble): neither counter reads the
  axis table; this universal is machine-unenumerated. It sits outside both PRED iff-clauses, so
  it is context, not a re-derivation gap — but nothing counts it.
- FLAG (minor, C1) — "the registry row for that id": `row_for` returns the FIRST matching row;
  a second, non-conforming row for the same id is invisible to the counter. Same for the
  used-by check being substring-based (`entry_rel in used_by(row)`), so a superstring path
  would also pass.
- Enumerated, no flag needed: C1 "Extra `source:` lines do not change the count" — count.py
  contains no `source:` parsing (verified over the full file) and the committed receipt
  `controls/c1-extra-source.txt` shows MET exit 0 with the extra line. C1 "Anything else is an
  honest stop" — enumerated as the exit-code complement (0 only on exact target equality; 2
  usage also ≠ MET). C2 "any verdict word other than honest-stop" — enumerated as strict
  case-sensitive equality; "Honest-Stop" would be an honest stop, consistent with the kill
  rule.
- Neither PRED text itself contains the tokens all/every/complete; the universals live in the
  registration prose and the `open_cites=0` target, which the counter does enumerate.

## Verdict

Both after-states are one-command re-derivable over committed bytes at the landing rev: C1 via
the c1 counter (tree inputs enumerated, digest-pinned), C2 via the c2 counter (archive-based
measurement at the ancestor rev d9ed38166cc3be8ef4c52b41d66ad94010feb047, embedded r32
counter). Flags: the axis-tie sentence is unenumerated context; the registry first-row/substring
nits are cosmetic and do not break the registered kill rule.
