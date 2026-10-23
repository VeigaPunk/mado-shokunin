# ReopenS162 — S162 used-by append for bind-table-r25.md

Row S162 of `corpus/SOURCES.md` (Hyprland `src/config/legacy/ConfigManager.cpp` @ `efb50993780079460b0cbed1363e2166a2de1d9f`) gained `corpus/knowledge/bind-table-r25.md` in its used-by cell instead of a duplicate-URL row. a3w1 seat SrcHandleSource found the same URL while sourcing the C1 `source =` handler topic (report `.ufo/waves/round-25/a3w1/reports/SrcHandleSource.md`). Scoped checks: fresh re-open, anchor match, the four located quotes verbatim at their lines, and whether used-by append is the right registry move under the file's header rules.

## Fresh fetch and anchor check

Command:

```sh
mkdir -p /fast/scratch/hyaku/mado-r25a3/reopen && timeout 60 curl -fsSL \
  'https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/ConfigManager.cpp' \
  -o /fast/scratch/hyaku/mado-r25a3/reopen/S162.bin \
  && sha256sum /fast/scratch/hyaku/mado-r25a3/reopen/S162.bin \
  && wc -c -l /fast/scratch/hyaku/mado-r25a3/reopen/S162.bin
```

Observed output:

```text
9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b  /fast/scratch/hyaku/mado-r25a3/reopen/S162.bin
 2184 90963 /fast/scratch/hyaku/mado-r25a3/reopen/S162.bin
```

Row S162 anchor cell: `src/config/legacy/ConfigManager.cpp:419-451,590-623,893-968,2016-2093 @ efb50993780079460b0cbed1363e2166a2de1d9f, sha256:9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b, 90963 B`. sha256 equal, byte count equal. PASS.

Same-identity check against the a3w1 capture:

```sh
cmp /fast/scratch/hyaku/mado-r25a3/reopen/S162.bin \
    /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/fetch/a3w1/SrcHandleSource.bin
# (no output — identical); sha256sum of the a3w1 bin:
9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b
```

Today's re-open is byte-identical to the bytes SrcHandleSource measured; the a3w1 sha/byte/line counts were honest. PASS.

## Located quotes verbatim at their lines (fresh bytes, lines 1814–1841 read)

1. `:1816` — `if (auto r = glob(absolutePath(rawpath, m_configCurrentPath).c_str(), GLOB_TILDE, nullptr, glob_buf.get()); r != 0) {` — verbatim at line 1816 (4-space indent precedes it in the file). PASS.
2. `:1817` — `r == GLOB_NOMATCH ? "found no match" : r == GLOB_ABORTED ? "read error" : "out of memory"` — verbatim tail of the `std::format` line at 1817. PASS.
3. `:1835` — `if (std::filesystem::is_regular_file(file_status)) {` — verbatim at line 1835. PASS.
4. `:1839` — `m_config->parseFile(value.c_str());` — verbatim inside `const auto THISRESULT        = m_config->parseFile(value.c_str());` at 1839. The a3w1 report's surrounding claim also matches the code: `m_configCurrentPath = value;` at 1838, restore at 1840. PASS.

## Duplicate check

Grep of the complete `corpus/SOURCES.md` for `src/config/legacy/ConfigManager.cpp` returns a single occurrence — the S162 row (line 174). No duplicate-URL row was added. S162's used-by cell now reads `corpus/knowledge/rule-attribution-r24.md, corpus/knowledge/bind-table-r25.md`.

## Registry move under the header rules

Header rule (SOURCES.md:1-9): "Only `status`, `recheck` and `used-by` change in place, each logged old→new in that round's lesson."

- used-by is one of the three cells the contract permits to change in place; appending a new consumer of an already-opened, already-anchored source is exactly that mechanism.
- A second row would duplicate a URL whose bytes are already anchored (same sha256, same 90963 B). Registry precedent rejected that shape: S045 was admitted only to record "REJECTED: duplicate S017 … after collision review". Established practice grows consumers inside used-by instead — S017 already lists three knowledge docs, S041 and S049 two.
- SrcHandleSource asked that the collision "remain visible to the SOURCES census"; the used-by append does that — S162 now names bind-table-r25.md as a consumer, while the draft row stays in the a3w1 report as taste evidence rather than a live duplicate.
- Note on scope: S162's anchored ranges include the `source` keyword registration at :614 (inside :590-623) but not the handler body at :1802-1855. Since scope/anchor/teaches cannot change in place, the new line citations correctly live in the a3w1 report and the knowledge entry rather than in the row.

## Residual risk

- `corpus/knowledge/bind-table-r25.md` does not exist in the lane yet; a3w2 seat ScribeBindNote is drafting it at `.ufo/waves/round-25/a3w2/drafts/bind-table-r25.md` (draft cites S162 at :607-608, :614, :1816-1848 with quotes). The used-by cell is currently forward-pointing; the integrator must land the knowledge entry or the cell dangles.
- No `corpus/lessons/round-25.md` exists yet (lessons run through round-24), so the required old→new used-by log entry is still outstanding for round close.
- Fresh copy retained at `/fast/scratch/hyaku/mado-r25a3/reopen/S162.bin`; a3w1 copy at `.ufo/waves/round-25/fetch/a3w1/SrcHandleSource.bin`.

## Tooling

None installed or upgraded; curl, sha256sum, wc, cmp already present.

## Verdict

REOPEN S162: agree — the re-opened bytes still match the row's anchor (sha256 9db68cf4…65be62b, 90963 B, byte-identical to the a3w1 capture), all four located quotes are verbatim at :1816/:1817/:1835/:1839, and appending `corpus/knowledge/bind-table-r25.md` to used-by is the right registry move: used-by is one of the three cells the header permits to change in place, while a second row for the identical URL would repeat the duplicate-URL shape S045 was rejected for. Residuals: the knowledge entry and the round-25 lesson old→new log are still outstanding in this wave.
