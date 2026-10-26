| mutant | category | pristine | successor | delta |
|---|---|---|---|---|
| exclusive-bounds | range-inclusion | selftest+control | selftest+control |  |
| half-open-bounds | range-inclusion | selftest+control | selftest+control |  |
| no-reversed-normalisation | range-inclusion | selftest | selftest |  |
| upper-plus-one | range-inclusion | selftest | selftest |  |
| range-slice-offbyone | range-inclusion | SURVIVED | selftest | **killed now** |
| comma-to-semicolon | range-inclusion | selftest+control | selftest+control |  |
| token-len-2 | token-length | selftest | selftest |  |
| token-len-4 | token-length | SURVIVED | selftest | **killed now** |
| token-lower-boundary | token-length | SURVIVED | selftest | **killed now** |
| token-insensitive | token-length | selftest | selftest |  |
| attr-before-inclusive | attribution | SURVIVED | selftest | **killed now** |
| attr-after-exclusive | attribution | SURVIVED | selftest | **killed now** |
| attr-after-first | attribution | selftest | selftest |  |
| attr-before-farthest | attribution | selftest | selftest |  |
| support-any | attribution | selftest+control | selftest+control |  |
| cited-offbyone | attribution | selftest | selftest |  |
| resolve-no-basename | name-resolution | selftest | selftest |  |
| resolve-always | name-resolution | selftest+control | selftest+control |  |
| id-re-digit-lead | name-resolution | SURVIVED | selftest | **killed now** |
| locator-no-lookbehind | name-resolution | SURVIVED | selftest | **killed now** |
| locator-no-lookahead | name-resolution | SURVIVED | selftest | **killed now** |
| frag-keep-empty | fragment-detection | selftest | selftest |  |
| frag-no-closing-tick | fragment-detection | selftest+control | selftest+control |  |
| no-re-escape | fragment-detection | SURVIVED | SURVIVED | still survives |
| ranges-group-lazy | fragment-detection | selftest+control | selftest+control |  |
| nofrag-renamed | verdict-string | selftest | selftest |  |
| verdict-lowercase-ok | verdict-string | selftest | selftest |  |
| summary-dropped | verdict-string | control | selftest+control |  |
| summary-swapped | verdict-string | SURVIVED | selftest | **killed now** |
| miss-count-nofrag | verdict-string | selftest | selftest |  |
| exit-always-zero | exit-codes | selftest+control | selftest+control |  |
| usage-returns-one | exit-codes | selftest | selftest |  |
| selftest-allows-args | exit-codes | selftest | selftest |  |
| teeth-identity-flip | selftest-teeth | selftest | selftest |  |
| teeth-one-direction | selftest-teeth | SURVIVED | selftest | **killed now** |
| verdicts-regex-nofrag | selftest-teeth | selftest | selftest |  |
| selftest-min-cases-dropped | selftest-teeth | SURVIVED | selftest | **killed now** |

totals: pristine killed=25/37 survived=12 | successor killed=36/37 survived=1
