# PROVINCE.md round-27 correction draft

## Proposed append-only correction paragraph

**Round-27 correction (append-only; M26-10):** The Round-25 residual correction above is stale as to environment seeding. Since `a496b02a`, `tools/mado-binds.py` does not seed config variables from `os.environ`; an environment-only `$NAME` therefore stays literal, and `source = $VAR` using only an environment value is not followed (unlike hyprlang). Variables declared in the config tree continue to expand. The earlier statement that absolute `source =` paths are followed remains in force; removing the environment seed closes only the environment-derived path outside `--home`.

## Proposed `tools/mado-wsrules.py` inventory row

| `tools/mado-wsrules.py` | reads the bytes of `DIR/.config/hypr/hyprland.conf` under `--home DIR` and every file its `source =` lines reach | writes nothing — stdout only (one JSON array) | mado, round 27 (static prediction of the Hyprland v0.56.2 workspace-rule table from config bytes; not live compositor state) |

## Correction sweep at revision `5ddc5885`

Command run: `git grep -n -i 'environ\|environment' 5ddc5885 -- PROVINCE.md corpus tools/mado-binds.py`.

Relevant `mado-binds.py` references returned:

- `PROVINCE.md:29` — the bind-tool inventory row says “no ... environment beyond `HOME`”; this is consistent with the no-seeding behavior.
- `PROVINCE.md:36-39` — the Round-25 residual correction incorrectly says config variables are seeded from the whole process environment and that `source = $VAR` can leave `DIR`; corrected by the proposed paragraph above.
- `corpus/lessons/round-25-verifier-spotcheck.md:90-93` — historical residual describes absolute/`$VAR` source paths and `os.environ` seeding as out-of-home reads, including the then-sandbox's PATH/HOME environment.
- `corpus/lessons/round-25.md:76-79` — historical residual says the tool seeds variables from the environment and can read outside `--home`.
- `corpus/lessons/round-26-verifier-spotcheck.md:107-119` — M26-10 records the environment-seeding removal at `a496b02a`, the literal-variable/source behavior, and the stale-doc finding.
- `corpus/lessons/round-26-verifier-spotcheck.md:207-213` — §7 routes the docstring and PROVINCE corrections and asks for a correction sweep.
- `corpus/lessons/round-26.md:91-98` — M26-10 errata records the dropped seeding, its fidelity trade, and the route.

The other false-positive hit is `PROVINCE.md:30`, which describes `tools/mado-anims.py`, not `mado-binds.py`. The README/knowledge hits are also unrelated: `corpus/README.md:218` and `corpus/knowledge/animation-table-r26.md:96-98` describe environment-seeded variables as an open limit for the round-26 animation-table route (`tools/mado-anims.py`). Leave these unchanged. No other README or `corpus/knowledge` hit from this sweep identifies bind-tool environment seeding.

## Exact proposed docstring paragraph for `tools/mado-binds.py`

Environment variables are not imported into the config variable table: a `$NAME` supplied only by the process environment stays literal, and `source = $VAR` using only an environment value is not followed (unlike hyprlang). Variables defined in the config tree are still expanded.
