# ReopenS173 — re-open of draft row S173, plus S158/S162 used-by quote checks

Date: 2026-10-23. Scope: re-open contract for draft SOURCES row S173 (hyprlang v0.6.8 `src/config.cpp`, w1 `SrcHyprlangExpr`); for existing rows S158 and S162 (used-by extended to `corpus/knowledge/animation-table-r26.md`), check the extension's quotes against the row's pinned bytes. Reviewer seat: read/fetch/verify only — no lane edits beyond this report, no product/counter/harness runs.

## Verdicts

- `REOPEN S173 agree`
- `REOPEN S158 quotes agree` — four SrcHyprctlAnims quotes verify against the row's pinned bytes; one low-severity anchor-coverage observation.
- `REOPEN S162 quotes agree` — three ConfigManager.cpp quotes verify against the row's pinned bytes; the fourth quote is genuine but rests on a URL no row pins (provenance gap, see findings).

## S173 re-open

Row under test (`.ufo/waves/round-26/drafts/sources-rows.md`): `src/config.cpp:619-667,755-827,983-986 @ 3a1c1b25b059dae2c6bbc46991562ba1158d125c, sha256:fa1b6898f2f1676de73220450f18f09603f0c3f8833e4c0a7c42c12aebe1de3e, 43049 B`.

Fetch (ordinary, `curl -fsSL`):

```sh
timeout 120 curl -fsSL https://raw.githubusercontent.com/hyprwm/hyprlang/v0.6.8/src/config.cpp -o /fast/scratch/hyaku/mado-r26/reopen/ReopenS173.bin
timeout 120 curl -fsSL https://raw.githubusercontent.com/hyprwm/hyprlang/v0.6.8/tests/config/config.conf -o /fast/scratch/hyaku/mado-r26/reopen/ReopenS173-config.conf.bin
```

Results (`sha256sum`, `wc -c`):

| File | sha256 | bytes | row match |
|---|---|---|---|
| `src/config.cpp` | `fa1b6898f2f1676de73220450f18f09603f0c3f8833e4c0a7c42c12aebe1de3e` | 43049 | sha ✓, bytes ✓ |
| `tests/config/config.conf` | `96f3ad75dbbaa31c381f6f481dd1f7893b9402c15d8c5b62ddf6bfc0bd9fa7c2` | 3517 | equals w1 report's table (not pinned by the row — see finding) |

Tag identity: read-only `git ls-remote https://github.com/hyprwm/hyprlang.git refs/tags/v0.6.8` from `/tmp` (git env vars unset) → `3a1c1b25b059dae2c6bbc46991562ba1158d125c refs/tags/v0.6.8` — matches the row's `@` commit.

Anchors honest in the fetched bytes: `619-667` is `parseExpression` (comment at 620-621 says only `+ - * /`, one operator per expression; operands resolved by variable lookup then `std::stof`); `755-827` is the `parseLine` expression scan with the preceding-backslash odd/even escape count and `std::format("{}", RESULT.value())` substitution; `983-986` is the `Config error at line {}` propagation into `impl->parseError`. `wc -l` = 1158 lines on the fetched bytes.

### Quote re-checks (SrcHyprlangExpr.md, independent re-run)

Method: decode fetched bytes as UTF-8; collapse both quote and text with `re.sub(r'\s+', ' ', s)`; require the collapsed quote to be a substring of (a) the whole file and (b) the cited line range; report whitespace-separated word count. Driver: `/fast/scratch/hyaku/mado-r26/reopen/check_quotes.py`, run as `timeout 60 prlimit --as=4000000000 python3 -I check_quotes.py`, exit 0.

| # | Citation | Quote (first words) | substring | at cited lines | words (≤25) |
|---|---|---|---|---|---|
| q1 | `src/config.cpp:630` | `return std::unexpected("Invalid expression type: …` | ✓ | ✓ | 9 |
| q2 | `tests/config/config.conf:17` | `$EXPR_VAR = {{MY_VAR + 2}}` | ✓ | ✓ | 5 |
| q3 | `tests/config/config.conf:20` | `testEscapedExpr = \{{testInt + 7}}` | ✓ | ✓ | 5 |
| q4 | `src/config.cpp:786-791` | `if (!RESULT.has_value()) { result.setError(RESULT.error()); …` | ✓ | ✓ | 18 |

Cross-check of report's marker claim: `{{` matches in fetched `config.conf` occur only at lines 17–32 — consistent with the report's "hits only in `config.conf` at lines 17-32".

### Finding S173-1 (low — row completeness)

The landed draft row pins only `src/config.cpp`, yet two of the w1 report's four quotes (q2, q3) rest on `tests/config/config.conf` — the w1 report's own proposed 11-cell row did carry that pin (`config.conf:17-32`, sha256 `96f3ad75…`, 3517 B). My fresh fetch reproduces that digest exactly, so the quotes are genuine, but the row as written leaves two of its supporting quotes outside its pinned provenance. Recommend adding the `config.conf` pin to the row's provenance cell (as the w1 proposal had it) or dropping q2/q3 from the note's citations. Not verdict-breaking: the row's stated URL/digest/anchors all re-open clean.

## S158 used-by extension (`+ corpus/knowledge/animation-table-r26.md`)

Pinned bytes re-fetched fresh to `/fast/scratch/hyaku/mado-r26/reopen/S158.bin`:

```sh
timeout 120 curl -fsSL https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/debug/HyprCtl.cpp -o S158.bin
```

→ sha256 `798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa`, 97582 B — equals the row's pin exactly.

All four `SrcHyprctlAnims.md` quotes verify (substring of pinned bytes, at cited lines, ≤25 words):

| # | Citation | Quote | substring | at cited lines | words |
|---|---|---|---|---|---|
| q1 | `HyprCtl.cpp:947` | `ret += "[[";` | ✓ | ✓ | 3 |
| q2 | `HyprCtl.cpp:964` | `ret += ",\n[";` | ✓ | ✓ | 3 |
| q3 | `HyprCtl.cpp:951-956` | node fields block (`"name": "{}" … "style": "{}"`) | ✓ | ✓ | 12 |
| q4 | `HyprCtl.cpp:970-974` | bezier fields block (`"X0": {:.2f}` …) | ✓ | ✓ | 10 |

### Observation S158-1 (low — anchor coverage, not a byte defect)

The extension's cited range is `animationsRequest` at `HyprCtl.cpp:927-985` (quotes at 947, 951-956, 964, 970-974; `animations` registration at 2018). The row's anchor cell lists `346-484, 613-630, 647-723, 1463-1645, 2003-2044` — `927-985` falls outside every anchor range (the 2018 registration is inside `2003-2044`). The whole-file sha256 pins the bytes regardless, so the quotes are pinned-content-verified; but if the ledger's convention is that anchors name what the row vouches for, the anchor cell should be extended with `927-985` when the used-by extension lands.

## S162 used-by extension (`+ corpus/knowledge/animation-table-r26.md`)

Pinned bytes re-fetched fresh to `/fast/scratch/hyaku/mado-r26/reopen/S162.bin`:

```sh
timeout 120 curl -fsSL https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/ConfigManager.cpp -o S162.bin
```

→ sha256 `9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b`, 90963 B — equals the row's pin exactly.

Quotes 2–4 of `SrcAnimConfig.md` verify against the pinned bytes at their cited lines:

| # | Citation | Quote (first words) | substring | at cited lines | words |
|---|---|---|---|---|---|
| q2 | `ConfigManager.cpp:1434-1438` | `if (!Config::animationTree()->nodeExists(ANIMNAME)) …` | ✓ | ✓ | 24 |
| q3 | `ConfigManager.cpp:1457-1467` | `return "invalid speed"; } } else { speed = 10.f; …` | ✓ | ✓ | 24 |
| q4 | `ConfigManager.cpp:1469-1478` | `Config::animationTree()->setConfigForNode(ANIMNAME, enabledInt, …` | ✓ | ✓ | 20 |

### Finding S162-1 (medium-low — unpinned provenance for one quote)

Quote 1 (`CVarList(const std::string& in, const size_t lastArgNo = 0, const char delim = ',', const bool removeEmpty = false);`) is from `include/hyprutils/string/VarList.hpp:14 @ hyprutils v0.14.2` — a different repository's header, which **no** `corpus/SOURCES.md` row pins (`grep VarList corpus/SOURCES.md` → no matches). Fresh fetch:

```sh
timeout 120 curl -fsSL https://raw.githubusercontent.com/hyprwm/hyprutils/v0.14.2/include/hyprutils/string/VarList.hpp -o hyprutils-varlist.bin
```

→ sha256 `9ad2fcbd5de691166b7db95de09b6bd054c9b4313deb3187e84c914dab74fc43`, 1883 B — equals the digest the w1 report recorded; the quote verifies at line 14 (✓ substring, ✓ at cited line, 18 words). The quote itself is genuine; the gap is that the animation note would cite bytes no ledger row pins. Recommend either a new SOURCES row for the hyprutils VarList header (the report's recorded digest is reproducible) or citing only the ConfigManager.cpp quotes in the note.

### Observation S162-2 (low — anchor coverage, not a byte defect)

The extension's new-use ranges are `287-309` (callback error conversion), `612-613` (handler registrations — inside the row's `590-623` anchor), and `1389-1479` (bezier/animation handlers). `287-309` and `1389-1479` fall outside the row's anchor cell (`419-451, 590-623, 893-968, 2016-2093`). As with S158, the whole-file sha256 pins the bytes; extend the anchor cell only if the ledger convention requires coverage of cited ranges.

## Commands and receipts

All fetches were ordinary `curl -fsSL` against `raw.githubusercontent.com`; no bot-challenge bypass, no other network surface except the read-only `git ls-remote`. Fetched artifacts and check script under `/fast/scratch/hyaku/mado-r26/reopen/`:

| Artifact | Bytes | sha256 |
|---|---|---:|---|
| `ReopenS173.bin` (config.cpp) | 43049 | `fa1b6898f2f1676de73220450f18f09603f0c3f8833e4c0a7c42c12aebe1de3e` |
| `ReopenS173-config.conf.bin` | 3517 | `96f3ad75dbbaa31c381f6f481dd1f7893b9402c15d8c5b62ddf6bfc0bd9fa7c2` |
| `S158.bin` (HyprCtl.cpp) | 97582 | `798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa` |
| `S162.bin` (legacy ConfigManager.cpp) | 90963 | `9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b` |
| `hyprutils-varlist.bin` | 1883 | `9ad2fcbd5de691166b7db95de09b6bd054c9b4313deb3187e84c914dab74fc43` |

Check driver: `timeout 60 prlimit --as=4000000000 python3 -I /fast/scratch/hyaku/mado-r26/reopen/check_quotes.py` → all 12 checks `OK`, exit 0.

## Hygiene and limits

- Lane writes: only this report (`.ufo/waves/round-26/w2/reports/ReopenS173.md`). No `git`/`jj` write commands anywhere; the single git call was read-only `ls-remote` run from `/tmp` with `GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE` unset.
- Host safety: no Hyprland/compositor/wayland anything started or touched; no hyprctl; `/dev/dri` unused.
- Every command was `timeout`-wrapped; Python ran under `prlimit --as=4000000000`; largest write 97 KB; `/fast` had 146 G free before writes. No process trees left running.
- Tools installed: none (directive read; nothing needed).
- Not verified here (out of scope): whether `animation-table-r26.md` (the used-by consumer, not yet landed) quotes additional lines; whether the w1 source-inspection *claims* (operator set, stof, escape parity) are semantically correct beyond the verified quotes — quote-level byte checks only, plus spot-reading the anchor ranges, which looked consistent with the row's "teaches" cell.

Report: `.ufo/waves/round-26/w2/reports/ReopenS173.md`
