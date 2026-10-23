# SrcAquamarineBackend — Aquamarine backend source

## Findings

Opened `src/backend/Backend.cpp` from Aquamarine tag `v0.15.1`; `git ls-remote` resolved the tag to commit `f31c47a1b9d300847d8fc3108ad959448103dfc1`. The captured file is 395 lines, 12,836 bytes, SHA-256 `4908c6f81e8183274c906eff4e0545555a7ac5842ba5a96df54c2383ec2620f7`.

This file does not select a backend from `WAYLAND_DISPLAY` (nor contain `AQ_BACKEND` / `AQ_NO_DRM` selection). `CBackend::create` receives a backend-options vector and constructs the requested Wayland, DRM, headless, or null implementation (lines 77–103). It returns null only when that vector is empty (lines 72–73). A failed DRM attempt logs and continues (lines 82–87). Backend startup is a separate `CBackend::start` call: if no implementation starts, it logs `No backend could be opened...` and returns false (lines 134–152); a failed mandatory implementation also clears implementations and returns false (lines 138–144). The literal diagnostic `CBackend::create() failed` is not emitted in this file, so that message belongs to a caller path not opened here.

The registration says the v4 counter obtains each expected table by starting nested Hyprland on a copy of the case tree and reading `hyprctl -i <instance> binds -j`, while the candidate runs in bubblewrap without `/run` or the display socket (`registration.md:181–186, 204–212`). This source explains the backend-start prerequisite but contains no bind-table parser or env-based backend selection. **[INFERENCE]** Together, the registration's isolation boundary and Aquamarine's start failure when no backend is available explain why the oracle is a separately started compositor and why a resolver inside that bubblewrap cannot query it; this source alone does not prove that every sandbox is unable to start Hyprland.

## Located quotes

Each quoted fragment was checked as an exact source line and as a whitespace-collapsed substring of the decoded source. The final quote is 25 words.

- `src/backend/Backend.cpp:72` — “if (backends.size() <= 0)” — This makes an empty backend request fail `CBackend::create` before a compositor-backed oracle can be available; it is startup plumbing, not bind parsing.
- `src/backend/Backend.cpp:79` — “auto ref = SP<CWaylandBackend>(new CWaylandBackend(backend));” — Wayland is constructed only when supplied as an option, so this file does not establish the requested `WAYLAND_DISPLAY` selection policy for the oracle.
- `src/backend/Backend.cpp:93` — “auto ref = SP<CHeadlessBackend>(new CHeadlessBackend(backend));” — Headless is likewise an explicit option here, not an automatic environment fallback; the counter's oracle needs the selected implementation to start.
- `src/backend/Backend.cpp:150` — “No backend could be opened. Make sure there was a correct backend passed to CBackend, and that your environment supports at least one of them.” — This startup failure path explains the need for an available compositor backend before `hyprctl binds -j` can serve as the counter oracle.

## Draft SOURCES row

No Aquamarine / `Backend.cpp` URL matched the existing `corpus/SOURCES.md` (including S153–S168); the duplicate search returned no matches. No corpus file was edited.

| S? | Aquamarine v0.15.1 backend implementation — https://raw.githubusercontent.com/hyprwm/aquamarine/v0.15.1/src/backend/Backend.cpp | code | A | Aquamarine backend implementation construction and startup failure relevant to C1 oracle availability | src/backend/Backend.cpp:60-110,121-152 @ f31c47a1b9d300847d8fc3108ad959448103dfc1, sha256:4908c6f81e8183274c906eff4e0545555a7ac5842ba5a96df54c2383ec2620f7, 12836 B | Shows backend implementations are constructed from caller-supplied options and startup fails if no implementation starts; does not define config bind parsing or environment-based backend selection | mined | 2026-10-23 | on-release | corpus/knowledge/bind-table-r25.md |

## Commands and outcomes

- `timeout 30 curl -fsSL https://raw.githubusercontent.com/hyprwm/aquamarine/v0.15.1/src/backend/Backend.cpp -o /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/fetch/a3w1/SrcAquamarineBackend.bin` — completed with no stdout; saved the requested raw source.
- `timeout 30 git ls-remote https://github.com/hyprwm/aquamarine.git refs/tags/v0.15.1 'refs/tags/v0.15.1^{}'` — output: `f31c47a1b9d300847d8fc3108ad959448103dfc1\trefs/tags/v0.15.1`.
- `sha256sum /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/fetch/a3w1/SrcAquamarineBackend.bin && wc -c -l /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/fetch/a3w1/SrcAquamarineBackend.bin` — output: `4908c6f81e8183274c906eff4e0545555a7ac5842ba5a96df54c2383ec2620f7  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/fetch/a3w1/SrcAquamarineBackend.bin`; `395 12836 /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/fetch/a3w1/SrcAquamarineBackend.bin`.
- Quote-audit Python check reported, for lines 72, 79, 93, and 150 respectively: `collapsed_substring=True`, `exact_line=True` for all four.
- Duplicate search: case-insensitive `aquamarine|src/backend/Backend\.cpp` in `corpus/SOURCES.md` — `No matches found`.

## Gates, touched surfaces, and limits

- Source gate: raw URL opened, tag commit resolved, SHA-256 / byte count / line anchors recorded, and all four quotes validated. The host package version was supplied by the assignment; no package binary/source equivalence check was performed.
- Touched surfaces: fetched source at `.ufo/waves/round-25/fetch/a3w1/SrcAquamarineBackend.bin` and this requested report only. No product code or corpus registry was edited.
- Out of scope / not run: no Hyprland or nested compositor was started; no `hyprctl` command, counter, build, test, service, package change, or live compositor action was performed. No other source file was opened to trace the caller's env-selection policy.
- No tools were installed or updated.
