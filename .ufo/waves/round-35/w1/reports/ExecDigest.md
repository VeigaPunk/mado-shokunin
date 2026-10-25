# ExecDigest — PRED-C1-r35-v1 receipt-digest verification

Scope: for each id in `.ufo/waves/round-35/c1/frozen.json` `receipts{}`, recompute
`sha256sum` of the file at `path`, compare to the frozen `sha256`, then check the digest
sits in the `anchor` cell of that id's row in
`.ufo/waves/round-35/controls/golden/corpus/SOURCES.md`.

Method: `sha256sum` per receipt path; anchor-cell containment checked by splitting each
table row on `|` and testing column `anchor` (header-indexed) — not just row-substring.

## Result table

| id | frozen sha256 | recomputed sha256 | match | digest in anchor cell |
|---|---|---|---|---|
| S203 | `1b7fa87ffe933990ee59acf3629ffbe3a90106bc9ebcce082237f7f495dd1646` | `1b7fa87ffe933990ee59acf3629ffbe3a90106bc9ebcce082237f7f495dd1646` | yes | yes |
| S204 | `4cd5ba6518e4a6d950fcb510d2482e33be78abb20d22bef41d21a66f7d1c54ad` | `4cd5ba6518e4a6d950fcb510d2482e33be78abb20d22bef41d21a66f7d1c54ad` | yes | yes |
| S205 | `f3387bfcbac79016034be38bab6548ae31df5860e5aafaa03105aca84b08ae1a` | `f3387bfcbac79016034be38bab6548ae31df5860e5aafaa03105aca84b08ae1a` | yes | yes |
| S206 | `1d30e4a999b53d5288369edc7573d7ceee0aef99570a55d781c4625440a938d5` | `1d30e4a999b53d5288369edc7573d7ceee0aef99570a55d781c4625440a938d5` | yes | yes |
| S207 | `81c33e7926f0bad071d31e9fc67e1d06967e3142da40ea3c93b16510b0adec59` | `81c33e7926f0bad071d31e9fc67e1d06967e3142da40ea3c93b16510b0adec59` | yes | yes |
| S208 | `6e72f0db3d7bbfecf4096b0aa22f716f417c00caa50b6d3319106387d6ce4654` | `6e72f0db3d7bbfecf4096b0aa22f716f417c00caa50b6d3319106387d6ce4654` | yes | yes |
| S209 | `a170c7a50b9305b3448fc85ecddb0d7b1f1c3ff5e42c78cdc2d07718c3bdd27c` | `a170c7a50b9305b3448fc85ecddb0d7b1f1c3ff5e42c78cdc2d07718c3bdd27c` | yes | yes |
| S210 | `ef282e386cdfb686fd331f4ed2fa7f0a33faf3ef4714844639b3eee4790b8726` | `ef282e386cdfb686fd331f4ed2fa7f0a33faf3ef4714844639b3eee4790b8726` | yes | yes |

## Verdict

8/8 receipt files recompute to the frozen digest; 8/8 rows carry the digest inside the
`anchor` column (each anchor also names the same receipt path it hashes). The
digest-bearing part of every frozen cite is intact. Out of scope here: used-by tokens,
status, recheck cadence, pipe escaping, and gate-quote checks — not exercised.
