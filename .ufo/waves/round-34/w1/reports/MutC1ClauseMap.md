# MutC1ClauseMap — clause-violation map for PRED-C1-r34-v1

Round 34, wave w1, lane mado-shokunin. Counter: `.ufo/waves/round-34/c1/count.py`
(committed, unedited). Frozen spec: `.ufo/waves/round-34/c1/frozen.json`
(predicate `PRED-C1-r34-v1`, frozen quote for S201 is 8 words). Controls under
`.ufo/waves/round-34/controls/` unedited.

Each mutant tree lives at `.ufo/waves/round-34/scratch/MutC1ClauseMap/<name>/`,
built by cloning `controls/golden` and mutating exactly the S201 clause named.
S202 stays closed in every mutant except (b) where the unreadable entry opens
both cites.

Invocation for every case (from `.ufo/waves/round-34/`):

    python3 c1/count.py --root scratch/MutC1ClauseMap/<name> --frozen c1/frozen.json

Golden sanity check re-run at write time:

    $ python3 c1/count.py --root controls/golden --frozen c1/frozen.json
    PRED-C1-r34-v1 closed_entries=1 closed_rows=2 open_cites=0 verdict=TARGET_MET
    exit=0

## (a) fetch file is a symlink — `a-fetch-symlink/`

Mutation: `.ufo/waves/round-34/fetch/S201.bin` replaced by a relative symlink
(`../../../../S201-real.bin`) to real bytes inside the root; `read_regular`
rejects at the lstat link check, blob=None. Only the regular-file/symlink
clause fails for S201.

    PRED-C1-r34-v1 closed_entries=0 closed_rows=1 open_cites=1 verdict=TARGET_MISSED
    exit=1

## (b) entry file is a symlink — `b-entry-symlink/`

Mutation: `corpus/knowledge/waybar-module-text-route-r25.md` replaced by a
relative symlink (`../../held-entry.md`) to identical bytes inside the root;
`read_regular` returns None for the entry, so gate-quote lookup fails for both
ids. Only the entry-regular-file clause fails; fetch bytes, digests, quotes,
and registry rows all still valid.

    PRED-C1-r34-v1 closed_entries=0 closed_rows=0 open_cites=2 verdict=TARGET_MISSED
    exit=1

## (c) fetch file is a hardlink with nlink=2 — `c-fetch-hardlink/`

Mutation: hardlinked `.ufo/waves/round-34/fetch/S201.bin` to `S201-twin.bin`
(root level), giving the fetch inode nlink=2; `read_regular` rejects at
`st.st_nlink != 1`. Bytes, digest, quote, and rows otherwise valid.

    PRED-C1-r34-v1 closed_entries=0 closed_rows=1 open_cites=1 verdict=TARGET_MISSED
    exit=1

## (d) gate-quote line has 26 words — `d-quote-26-words/`

Mutation: prepended `w01 … w18` (18 words) inside the fetched bytes
immediately before the S201 quote and made the entry line
`gate-quote: S201 w01 … w18 $XDG_RUNTIME_DIR/hypr does not exist, falling
back to /tmp/hypr` — exactly 26 words. `found == quote` holds and
`quote in blob` holds; only `len(words) <= 25` fails.

    PRED-C1-r34-v1 closed_entries=0 closed_rows=1 open_cites=1 verdict=TARGET_MISSED
    exit=1

## (e) gate-quote not a contiguous substring of the bytes — `e-quote-not-substring/`

Mutation: replaced the S201 quote span in `S201.bin` with `X`×(same length);
`found == quote` still holds but `quote.encode() in blob` fails. Note: the
sha256 clause necessarily fails too — any byte change large enough to remove
the substring changes the digest; clause (e) is not isolatable in isolation.

    PRED-C1-r34-v1 closed_entries=0 closed_rows=1 open_cites=1 verdict=TARGET_MISSED
    exit=1

## (f) used-by cell names a different path — `f-usedby-wrong-path/`

Mutation: S201 registry row's last cell changed to
`corpus/knowledge/other.md`; `used_by_tokens == {entry_rel}` fails. Row count
still 1, everything else valid.

    PRED-C1-r34-v1 closed_entries=0 closed_rows=1 open_cites=1 verdict=TARGET_MISSED
    exit=1

## (g) two registry rows for the same id — `g-duplicate-row/`

Mutation: duplicated the valid S201 row verbatim in `corpus/SOURCES.md`;
`rows_for` returns 2 rows, `len(rows) == 1` fails even though the duplicated
row itself is well-formed.

    PRED-C1-r34-v1 closed_entries=0 closed_rows=1 open_cites=1 verdict=TARGET_MISSED
    exit=1

## (h) fetch sha256 differs from frozen.json — `h-sha-mismatch/`

Mutation: appended a single `\n` to `S201.bin`; the quote remains a contiguous
substring and every other clause holds; only `digest == fetch["sha256"]` fails.

    PRED-C1-r34-v1 closed_entries=0 closed_rows=1 open_cites=1 verdict=TARGET_MISSED
    exit=1

## Summary

| case | tree | violated check | closed_entries | closed_rows | open_cites | verdict | exit |
|---|---|---|---|---|---|---|---|
| golden | controls/golden | — | 1 | 2 | 0 | TARGET_MET | 0 |
| a | a-fetch-symlink | fetch regular-file (symlink) | 0 | 1 | 1 | TARGET_MISSED | 1 |
| b | b-entry-symlink | entry regular-file (symlink) | 0 | 0 | 2 | TARGET_MISSED | 1 |
| c | c-fetch-hardlink | fetch nlink=1 | 0 | 1 | 1 | TARGET_MISSED | 1 |
| d | d-quote-26-words | 1–25 word bound | 0 | 1 | 1 | TARGET_MISSED | 1 |
| e | e-quote-not-substring | contiguous substring (+sha inseparable) | 0 | 1 | 1 | TARGET_MISSED | 1 |
| f | f-usedby-wrong-path | used-by token = entry path | 0 | 1 | 1 | TARGET_MISSED | 1 |
| g | g-duplicate-row | exactly one registry row | 0 | 1 | 1 | TARGET_MISSED | 1 |
| h | h-sha-mismatch | sha256 = frozen.json | 0 | 1 | 1 | TARGET_MISSED | 1 |

Every clause of the frozen predicate is independently falsifiable by the
counter: each single-clause mutation drops exactly the S201 cite
(S201+S202 in case b) and the counter prints `verdict=TARGET_MISSED`, exit 1.
