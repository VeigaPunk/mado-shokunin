# ExecRefCompare (w1, round 47) — differential fuzz of the real xdg-terminal-exec

Target (pinned, re-hashed this seat):
`/usr/bin/xdg-terminal-exec`, 1499 lines,
sha256 `89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac`.

## Files written (all new, all inside this seat)

| path | what |
|---|---|
| `.ufo/waves/round-47/w1/ExecRefCompare/fuzz.py` | grammar fuzzer: random XDG trees + 23 families of one-token mutations; clusters outcomes, reports intra-family flips |
| `.ufo/waves/round-47/w1/ExecRefCompare/probe.py` | 79 minimal targeted cases, one per behaviour, in the frozen fixture schema |
| `.ufo/waves/round-47/w1/ExecRefCompare/findings.md` | 22 findings, each with its script locators, a minimal case JSON and the observed stdout/rc |
| `.ufo/waves/round-47/w1/ExecRefCompare/verify_findings.py` | re-hashes the target, re-derives every cited line, re-checks every inline case against the receipts |
| `.ufo/waves/round-47/w1/ExecRefCompare/receipts/` | `cases.jsonl` (730 exact cases+expect), `probes.tsv`, `probe-cases/*.json`, `flips.tsv` (44), `families.tsv`, `clusters.tsv`, `runs.tsv`, `cache.tsv`, `expansion.txt` (XTE_DEBUG path expansions), `locators.txt` (357 cited lines), `summary.json` |

No tracked file was touched; nothing outside this seat dir and
`.ufo/waves/round-47/w1/ExecRefCompare.md` was written. No git/jj mutation, no package install,
no terminal launched, no compositor write. `xdg-terminal-exec` was only ever invoked with a
`--print-*` option and a fresh empty `XDG_CACHE_HOME` inside scratch.

## Behaviour established (809 case-runs in the final campaign, plus 10 debug replays)

Sorted by how much they should disturb a naive re-implementation (details + cases in findings.md):

1. **Shadowing, not overriding** (F-01): a higher-priority entry that fails validation removes the ID
   entirely — the system copy is never tried, result `rc=1` with no terminal. (`unalias` at :1085 runs
   before the entry is validated; the fallback list has the ID twice at :790.)
2. **A listed ID that fails consumes its own fallback** (F-02): `Alacritty.desktop:New` with no
   declared action ⇒ `rc=1`, not "the action is ignored".
3. **Duplicate keys are conjunctive** (F-03): every `Categories`/`Exec` line must pass; a later bad
   `Exec` or `Categories` kills an entry whose earlier line was fine.
4. **Key matching is prefix matching** (F-04): `ExecFoo=`, `CategoriesFoo=`, `HiddenFoo=`,
   `TryExecX=`. `Hidden` is exactly `true` — `Hidden=True` does not hide (F-06).
5. **Unreadable list file aborts everything** (F-10), while an unreadable entry is skipped.
6. **`--print-path` mangles any path containing `/./`** (F-16) and can print a non-existent path.
7. **Empty elements in `XDG_*_DIRS` become root paths** `/xdg-terminals.list`, `/applications/`
   (F-21); an empty-but-set variable is replaced by the default, not by "none" (F-22).
8. **Fallback order is reverse readdir order** (F-09): same tree, different creation order, different
   terminal. Judge fixtures must not depend on it.
9. **`Exec` parsing fails open** (F-11): unclosed quote, `%Z`, a second `%f` are passed through raw.
10. **Space-form options are swallowed and become the command** (F-18): `--dir /x` ⇒ `-e /x`.

Also documented: print-mode output order/delimiters/cache asymmetry (:1457 vs :1374-:1383), prepend
order (F-19), `execarg` compat default + first-directive-wins (F-20), CRLF/BOM handling (F-13),
action groups (F-14), find filter incl. the dotfile-in-subdir asymmetry (F-08), show-in rules only on
fallback (F-07).

## Verification actually run

`python3 verify_findings.py --write-locators` → `ALL CHECKS PASSED`
(target sha256 OK; 0 placeholders; 25 inline cases byte-equal to the receipt expects; 357 cited lines
each re-derived from the pinned file; 72 mentioned case ids all present in the receipts).

## Risks

- Fallback ordering was measured on /fast/scratch only; other filesystems may return a different
  readdir order (flagged in findings §7.1 rather than asserted as universal).
- `stderr` was not modelled as contract (the judge compares stdout + rc); three findings quote stderr
  only as corroboration.
- One seed for the random half (`--seed 20261026`); the family half is deterministic.

## Blockers

None.
