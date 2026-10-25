# RevC1ClauseImpl — clause-by-clause review of `.ufo/waves/round-34/c1/count.py`

Reviewed against the frozen predicate sentence (count.py:21-29, matched byte-for-byte to
`c1/frozen.json["predicate"]` at line 129). Frozen spec: one entry
(`corpus/knowledge/waybar-module-text-route-r25.md`) carrying ids `S201`, `S202`; two fetches
with sha256s; two quotes. Target `{closed_entries:1, closed_rows:2, open_cites:0}`.

## Clause verdicts

| Clause | Verdict | Lines | Notes |
|---|---|---|---|
| (a) entry & fetch are regular files | FAITHFUL | 66, plus call sites 133, 139, 145 | `read_regular` requires `S_ISREG` on the final component for every path read. Entry non-regular ⇒ `entry_bytes is None` ⇒ `entry_closed=False` (141,163) and per-id `ok` fails via 151. |
| (b) neither is a symlink | FAITHFUL (stricter) | 59-60, 50-51, 69 | `lstat` rejects symlink at **every** component, not just the leaf — a superset of "neither is a symlink". Root itself must be a non-symlink dir (50-51). `O_NOFOLLOW` re-checks the leaf at open (69). |
| (c) nlink == 1 | FAITHFUL | 66 | `st.st_nlink != 1` rejects. Applied uniformly to entry and fetch since both go through `read_regular`. |
| (d) every component inside scored root | FAITHFUL (stricter, one caveat) | 41, 43-45, 53-65, 50-51 | Rejects absolute/`\\`-prefixed rels (41), `.`/`..`/empty parts (44), non-dir intermediates (63), symlink intermediates (59). Stricter than literal clause: an in-root `..` (e.g. `a/../b`) would satisfy "stays inside" but is rejected — safe direction. Caveat: TOCTOU — `lstat` walk (56) then `os.open` (69) re-resolves; only `O_NOFOLLOW` on the leaf is atomic. Static predicate ⇒ low risk, noted. |
| (e) fetch bytes read with O_NOFOLLOW | FAITHFUL (stricter) | 69 | `os.open(cur, O_RDONLY | O_NOFOLLOW)` — applied to entry too, a superset. |
| (f) sha256 == digest in c1/frozen.json | FAITHFUL comparison; path pin WEAKER | 146, 155; flag at 122, 125 | `sha256(blob).hexdigest() == fetch["sha256"]` is correct. But the frozen file is taken from `--frozen` argv (122,125); the code does not pin it to `c1/frozen.json`. Clause is "the digest in c1/frozen.json" — code trusts the operator to pass that path. Weaker than literal; likely intended per CLI contract. |
| (g) entry contains a 1-25-word gate-quote line that is a contiguous substring of the fetch bytes | FAITHFUL (stricter) | 108-116, 147-148, 152-154 | `gate_quote` finds lines starting `gate-quote: {sid} `, returns None if **zero or ≥2** such lines (113-114) — stricter than "contains a line". Payload must equal the frozen quote exactly, incl. trailing whitespace (152: `found == quote`), split()-word count 1-25 (153), `quote.encode() in blob` for substring (154). Exact-equality against the frozen quote is stricter than "a line that is a substring" but consistent with the spec's quote table. |
| (h) registry row lists entry path as a whole used-by token | FAITHFUL (stricter) | 88-96, 157 | Last `|` cell split on `,` into stripped tokens (96); `used_by_tokens(rows[0]) == {entry_rel}` requires the entry path be a whole token — and the **only** token. Clause says "lists ... as a whole used-by token"; `== {entry_rel}` also excludes other tokens. Stricter; probably intended by "the registry row ... lists the entry path". Cell-last convention is [INFERENCE] of the registry format — a table whose used-by column isn't last would misparse. |
| (i) exactly one registry row for the id | FAITHFUL | 99-105, 156 | `rows_for` collects lines matching `^ {0,3}\|(S\d+)\|` for that sid; `len(rows) == 1` enforces exactly one. Predicate's definite article ("the registry row") ⇒ stricter reading is correct. Rows must come from `corpus/SOURCES.md` read through the same `read_regular` gauntlet (133) — note: if SOURCES.md fails the gauntlet it silently decodes as `""` and every row check fails, counting cites open rather than erroring. Faithful for counting, but an unreadable registry is indistinguishable from a registry with 0/2 rows. |
| (j) target triple | FAITHFUL | 30, 131-132, 166-170, 176 | `closed_entries==1 AND closed_rows==2 AND open_cites==0` checked against `EXPECTED_TARGET`, which itself is drift-verified against `spec["target"]` (131). Exit 0/1 wired at 176. `closed_entries` semantics: entry counts closed only when readable AND all its ids closed (141, 159-165) — matches "closed cite" aggregation. |

## Unimplemented clauses

None. All ten clauses have corresponding code.

## Deviations flagged

1. **(f) path pin**: `--frozen` is argv, not hard-pinned to `c1/frozen.json` (count.py:122,125). Invocation discipline substitutes for the literal clause.
2. **(h) singleton used-by**: `== {entry_rel}` rejects rows that correctly list the entry path alongside other tokens (157). If the clause intends membership, code is stricter.
3. **(d) `..` ban**: rejects in-root `..` that the literal clause would admit (44). Safe direction.
4. **(e)/(d) TOCTOU**: component `lstat` walk then `os.open` re-resolve (56→69); `O_NOFOLLOW` guards only the leaf atomically. Acceptable for a static tree.
5. **SOURCES.md failure mode**: unreadable registry ⇒ `open_cites` rather than exit 2 (133-134). Counting stays conservative.
6. **MAX_BYTES=8_000_000** (31, 80-81): fetches >8MB are counted open — an unstated resource bound stricter than any clause.
7. `spec["fetches"][sid]` / `spec["quotes"][sid]` / `fetch["sha256"]` (143-144, 155) can `KeyError` on a malformed frozen spec → traceback + exit 1. Target-miss either way, but ugly channel; `predicate`/`target` are drift-checked, the rest aren't.
