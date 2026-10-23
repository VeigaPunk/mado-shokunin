# ReopenS170 — re-open of SOURCES row S170 (Aquamarine v0.15.1 Backend.cpp)

## What I did

Re-fetched the S170 URL fresh, re-hashed the bytes, re-resolved the pinned tag, and audited every located quote in the a3w1 report (`.ufo/waves/round-25/a3w1/reports/SrcAquamarineBackend.md`) plus the row's `teaches` cell against the fetched bytes.

Row under audit (corpus/SOURCES.md:182): URL `https://raw.githubusercontent.com/hyprwm/aquamarine/v0.15.1/src/backend/Backend.cpp`, anchor `src/backend/Backend.cpp:60-110,121-152 @ f31c47a1b9d300847d8fc3108ad959448103dfc1, sha256:4908c6f81e8183274c906eff4e0545555a7ac5842ba5a96df54c2383ec2620f7, 12836 B`.

## Exact commands and outputs

1. Fetch fresh to the scratch path:
   - `/usr/bin/mkdir -p /fast/scratch/hyaku/mado-r25a3/reopen && /usr/bin/timeout 30 curl -fsSL https://raw.githubusercontent.com/hyprwm/aquamarine/v0.15.1/src/backend/Backend.cpp -o /fast/scratch/hyaku/mado-r25a3/reopen/S170.bin && /usr/bin/sha256sum /fast/scratch/hyaku/mado-r25a3/reopen/S170.bin && /usr/bin/wc -c -l /fast/scratch/hyaku/mado-r25a3/reopen/S170.bin`
   - Output: `4908c6f81e8183274c906eff4e0545555a7ac5842ba5a96df54c2383ec2620f7  /fast/scratch/hyaku/mado-r25a3/reopen/S170.bin` and `395 12836 /fast/scratch/hyaku/mado-r25a3/reopen/S170.bin`.
   - sha256 and byte count match the anchor cell exactly; 395 lines matches the report.
2. Tag re-resolution:
   - `/usr/bin/timeout 30 git ls-remote https://github.com/hyprwm/aquamarine.git refs/tags/v0.15.1 'refs/tags/v0.15.1^{}'`
   - Output: `f31c47a1b9d300847d8fc3108ad959448103dfc1	refs/tags/v0.15.1` (no peeled `^{}` line → lightweight tag, so the URL's tag bytes are the pinned commit's bytes). Matches the anchor and the report.
3. Quote audit (Python over the fetched bytes, whitespace-collapsed): each report quote is a verbatim substring of its stated line and the stated line is the only line in the whole file containing it:
   - `:72` — `if (backends.size() <= 0)` → at_stated_line=True, exact_line=True, only hit line 72.
   - `:79` — `auto ref = SP<CWaylandBackend>(new CWaylandBackend(backend));` → at_stated_line=True, exact_line=True, only hit line 79.
   - `:93` — `auto ref = SP<CHeadlessBackend>(new CHeadlessBackend(backend));` → at_stated_line=True, exact_line=True, only hit line 93.
   - `:150` — `No backend could be opened. Make sure there was a correct backend passed to CBackend, and that your environment supports at least one of them.` → at_stated_line=True (quote is the string literal inside the line `log(AQ_LOG_CRITICAL, "...");`), only hit line 150. Strict whole-line equality is False for this one since the quote excludes the `log(...)` wrapper — cosmetic, the a3w1 criterion (whitespace-collapsed substring at the stated line) holds.
   - Anchor ranges: 60–110 is exactly `CBackend::create(...)` (quotes 72/79/93 inside), 121–152 is exactly `CBackend::start()` (quote 150 inside).
4. `teaches` audit against the bytes ("Shows backend implementations are constructed from caller-supplied options and startup fails if no implementation starts; does not define config bind parsing or environment-based backend selection"):
   - Caller-supplied construction: line 60 `CBackend::create(const std::vector<SBackendImplementationOptions>& backends, const SBackendOptions& options)`; WAYLAND/DRM/HEADLESS/NULL branches construct only what the vector requests (lines 77–103); empty vector returns nullptr at 72–73. ✓
   - Startup failure: `CBackend::start()` at 121 clears implementations and `return false` on a mandatory implementation that fails to start (138–144), and at 149–151 `if (implementations.empty() || started <= 0)` logs the line-150 diagnostic and `return false`. ✓
   - Negative claims: zero occurrences of `bind` or `config`; zero occurrences of `getenv` or `WAYLAND_DISPLAY`; the only `AQ_*` tokens are log-level and backend-type enums (e.g. `AQ_LOG_*`, `AQ_BACKEND_WAYLAND`), not environment-based selection. ✓

## Findings

- Hash, byte count, pinned commit, line anchors, all four located quotes, and both halves of the `teaches` cell are reproduced from a fresh fetch. No defect found.
- Minor observation (not row-affecting): the a3w1 report's summary line says `exact_line=True for all four`; under strict whole-line equality line 150 is False (quote is the embedded string literal). The report's own stated criterion was "exact source line and whitespace-collapsed substring", and the substring half is what carries the claim. No correction needed to SOURCES.md.

## Verdict

REOPEN S170: agree

No tools were installed or updated. No lane files were edited besides this report; the fetch receipt lives at /fast/scratch/hyaku/mado-r25a3/reopen/S170.bin. All spawned processes were `timeout`-wrapped one-shots (curl, git ls-remote) and completed.
