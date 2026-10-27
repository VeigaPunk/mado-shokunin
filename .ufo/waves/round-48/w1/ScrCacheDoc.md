# ScrCacheDoc — C1 docstring: the warm-cache contract text (round 48 w1)

**Delivered.** `.ufo/waves/round-48/w1/ScrCacheDoc/docstring.md` — a drop-in replacement for the `Cache` paragraph at
`tools/mado-terminal.py:82-85`, a new round-48 out-of-contract list, the six collateral docstring edits the contract
forces, a round-48 `PROVINCE.md` refinement line, an implementation-obligation list, ten findings, and the receipt
index. Every statement carries a computed `x:N` of the pinned resolver. Backed by `probe.sh` (regenerates the receipts)
and `verify-quotes.sh` (re-checks every literal quote and locator: 45 checks, exit 0, `receipts/quotes.txt`).

Pin: `.ufo/waves/round-47/fetch/xdg-terminal-exec`, sha256
`89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac` — identical to `/usr/bin/xdg-terminal-exec`
(`receipts/warm-cache.txt`, first block).

## Gates

- No frozen counter was run or scored (w1 rule). `quality/`, the fixtures, the judge, the registry, `README.md`,
  `LOG.md`, `SCORECARD.md`, `PROVINCE.md` and the tool were not edited.
- No installs, no pacman, no compositor verb, no terminal launched, no host config or cache written. Every
  `xdg-terminal-exec` call used `--print-cmd` with `XDG_CACHE_HOME` inside this seat's scratch; the host's
  `~/.cache/xdg-terminal-exec` was never touched. `bwrap` was used once, read-only, to hide `/etc` for an ownership
  render.

## Touched surfaces

- Lane: `.ufo/waves/round-48/w1/ScrCacheDoc/` (`docstring.md`, `probe.sh`, `verify-quotes.sh`, `receipts/`) and this
  report. Nothing else.
- Scratch: `/fast/scratch/hyaku/mado-r48/ScrCacheDoc` (fixture tree, < 1 MB), removed before finishing.

## Conflicts to report verbatim (for the canonical judge)

1. **`/disable_cache` cannot disable the read.** The brief says the cache is honoured "(hit / out-of-date / invalid /
   disabled via XTE_CACHE_ENABLED or /disable_cache)". Measured: the read gate is `x:1179` and it runs before any list
   is read (`x:1167` make_paths, `x:1181-1200` the cold branch); the directives are parsed in `read_config_paths`
   (`x:376-384`) which is only reached cold (`x:1198`). A valid cache therefore hits with `/disable_cache` present and
   the list never read. The directive only decides the SAVE side: a cold run that reaches `x:1455-1458` removes the file
   (`x:302`, `x:336-337`). Receipt: adding `/disable_cache` to the list changed the list's size/mtime, so the hash
   changed ("cache is out-of-date"), the cold path ran, the directive was found, the file was removed
   (`receipts/warm-cache.txt`, `/disable_cache` block). **Consequence:** `cache=disabled` must be defined on
   `XTE_CACHE_ENABLED` alone, or `explain` will label a hit "disabled". The draft does that and keeps the save
   consequence as prose.
2. **`--test` also writes the cache.** The brief says "Only a cold run that reaches :1455 (print-cmd or a launch) writes
   the cache". `save_cache "$1" &` (`x:1455-1458`) precedes the test-mode branch (`x:1460-1466`), so a cold `--test`
   saves too. Priming with `--print-cmd` is unaffected; the counter must not treat `--test` as read-only. (Code fact;
   `--test` was not executed, by host guard.)
3. **HOME unset is conditional, not unconditional.** The brief (and `claims.md:20`, "HOME unset modelled as the pin
   (round-47 D1)") records "pin exit 1, empty stdout". Measured: fatal only where a default must expand —
   `XDG_CONFIG_HOME` unset -> `x:148`, `XDG_DATA_HOME` unset -> `x:166`, `XDG_CACHE_HOME` unset -> `x:172`, each
   `HOME: unbound variable`, rc 1, empty stdout; with all three XDG base variables set, a HOME-less run selects
   normally (rc 0, `foo`). Receipt `receipts/warm-cache.txt`, last block. Both the C1 contract and the D1 lesson line
   need the condition.
4. Minor: the cache line limit leaves 49 usable lines — line 50 is invalid before assignment (`x:239-242`).
5. Minor: the save's newline guard (`x:312-318`) can never match, because the concatenation starts with the 32-hex hash;
   a newline in a field is written and shifts the cached lines.

## Findings (what each attacks or supports)

- **F1** `/disable_cache` is a save-side switch — attacks the brief's "disabled via ... /disable_cache"; evidence
  `x:1179`, `x:1198`, `x:376-384`, `x:336-337`; receipt `receipts/warm-cache.txt`.
- **F2** `--test` writes the cache — attacks the brief's "(print-cmd or a launch)"; evidence `x:1455-1458` before
  `x:1460-1466`.
- **F3** `XTE_CACHE_ENABLED=""` disables the read (`check_bool` rejects the empty string, `x:50-59`) while
  `XTE__CACHE_CONFIGURED=${XTE_CACHE_ENABLED-}` (`x:1174`) reads the environment, so the directive slot stays open; a
  non-empty value freezes both directives (`x:376`, `x:382`).
- **F4** the newline guard `x:312-318` is dead (hash prefix, `x:310`); fixtures may rely on shifted caches.
- **F5** `--print-path` mutates `XTE__ENTRY_PATH` (`x:1341-1343`) before the save (`x:1455`), so line 3 of the cache
  depends on the priming argv.
- **F6** an unreadable cache is a failed read, not fatal: `read_cache` is called in an `if` condition (`x:1179`), so
  errexit is suspended; measured rc 0, cold answer, one "Permission denied" stderr line.
- **F7** HOME unset conditional (conflict 3).
- **F8** no entry-id aliases on the warm path (`x:782` runs only cold, `x:1200`), so `command -v` on a cached command
  (`x:274`) cannot resolve an entry id — a stale class a cold-only model cannot produce.
- **F9** the ls facts the md5 needs, measured (`receipts/ls-listing.txt`): names literal on a pipe; `total` =
  `st_blocks/2`; a broken symlink or loop under `-L` is an all-`?` line with block-relative padding, error on stderr
  only; **any** future mtime takes the year form (no one-hour grace); the six-month boundary lies in
  (15771276 s, 15785676 s); numeric ownership without `/etc` (`bwrap --dev-bind / / --tmpfs /etc` -> `1000 1000`). The
  md5 itself was reproduced byte-exactly from the tree: `33199ac7769c22716123b4a57954ad91`
  (`receipts/warm-cache.txt`, "gen_hash reproduced").
- **F10** what has to move in the tool: `explain`'s vocabulary is `present|absent` (`tools/mado-terminal.py:852-861`)
  and `select()` computes the cache path only after `read_config_paths`/`find_entry_paths`
  (`tools/mado-terminal.py:721-726`).

## Judged-behaviour evidence (warm vs cold)

Same-size, same-minute `Exec=foo` -> `Exec=bar` edit after priming: the warm run prints `foo` with "cache is actual",
the cold run on the same tree prints `bar` (`receipts/warm-cache.txt`). `XTE_CACHE_ENABLED=false` ignores a valid cache
and the cold run removes the file. These are the two fixture classes the brief names, demonstrated on the real script.

## Out of scope (left to other seats / the L1)

- Implementing the contract in `tools/mado-terminal.py`; the fixture schema v2 and the C1 counter; D1's lesson line
  text, D2-D4, R3, R4b, M47-10, `CritC1Explain`, `SentC1Sandbox`; the C2 xkb entry and registry rows S340..; the
  `README.md:110`/`:112` ground-open edits.
- The tool's own selftest (round-47 43/43) was not rerun.
- One open decision for the L1: the draft has the tool render ownership as `ls` does, which needs the passwd/group
  databases visible to it (numeric inside the counter's `/etc`-less sandbox). Making the tool numeric-only would be
  simpler but would misdescribe the host outside a sandbox; the PROVINCE line names the read either way.

## Artifacts

- `.ufo/waves/round-48/w1/ScrCacheDoc/docstring.md` — the deliverable (drop-in text A, B, collateral C, PROVINCE line
  D, obligations E, findings F, receipts G).
- `.ufo/waves/round-48/w1/ScrCacheDoc/probe.sh` — regenerates both behavioural receipts under `$WORK`.
- `.ufo/waves/round-48/w1/ScrCacheDoc/verify-quotes.sh` — 45 quote/locator checks against the pin, the tool docstring
  and `claims.md`; exit 0.
- `.ufo/waves/round-48/w1/ScrCacheDoc/receipts/quotes.txt`, `warm-cache.txt`, `ls-listing.txt`.
