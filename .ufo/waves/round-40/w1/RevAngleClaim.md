# Seat RevAngleClaim — round 40 w1 — angle-inheritance claim review

**Verdict: CLAIM SURVIVES.** The gradient handler leaves `m_angle` untouched when a redeclaration has
no `deg` token, the `*data` object persists across handler calls (and across `parse()` calls), and the
host's live values match that model on every gradient key. Three falsification attempts (host sweep,
library harness, reverse direction) all failed to refute it.

---

## 1. Claim under test and falsifiers

Claim: *the gradient handler leaves `m_angle` untouched when a redeclaration has no `deg` token, so a
later declarer inherits the earlier declarer's angle.*

Falsifiers sought:
- **F1 (host):** a key whose earlier declarer carried an angle and whose last declarer has none, but
  live shows `0deg` — would prove no inheritance.
- **F2 (host, reverse):** a key whose last declarer carries a `deg` angle but live shows an earlier
  declarer's angle instead — would prove the deg token is not authoritative.
- **F3 (library):** drive the real system hyprlang 0.6.8 with the host's declarer chain; if the
  angle does not survive the no-deg redeclaration, the mechanism claim is false.

## 2. Source evidence

Hyprland tree `/tmp/mado40-probe/Hyprland` is v0.56.2 @ `efb50993780079460b0cbed1363e2166a2de1d9f`
(`git rev-parse HEAD`), identical to the running compositor's `hyprctl version` commit string.

- `src/config/legacy/ConfigManager.cpp:103-160` — `configHandleGradientSet`:
  `DATA->m_colors.clear()` on entry (line ~112); `DATA->m_angle` is assigned **only** inside the
  deg-token branch (line 120, `stoi(substr(0, find("deg"))) * π/180`). No else-path, no reset.
- `src/config/legacy/ConfigManager.cpp:509-511` — gradient options registered as
  `Hyprlang::CConfigCustomValueType{&configHandleGradientSet, configHandleGradientDestroy,
  std::format("0x{:x}", ...first default colour...)}` — the registered **default string carries no
  `deg` token**, so even defaults re-application cannot reset the angle.
- `src/config/shared/complex/ComplexDataTypes.hpp:14-78` — `CGradientValueData`: `float m_angle = 0`
  default (line 56); `toString()` = colours as lowercase unpadded hex (`getAsHex`, line 72) plus
  `std::format("{}deg", sc<int>(m_angle * 180.0 / M_PI))` (line 75, int truncation).
- hyprlang v0.6.8 `src/config.cpp` (fetched from tag `v0.6.8`, byte-identical API to installed
  `libhyprlang.so.0.6.8`):
  - `parseValue` CONFIGDATATYPE_CUSTOM (lines ~495-506): every parse of the key calls
    `handler(value, &CConfigCustomValueType::data)` — the **same persistent `data` member** of the
    custom-type object created once at `addConfigValue` time; `lastVal` recorded; no reset.
  - Variable redefinition `parseVariable` (lines 518-530): redefinition **replaces the variable's
    value in place** — the theme's `$activeBorderColor = rgb(e68e0d)` governs all later expansions.
  - Variable expansion happens in `parseLine` (lines 736-800) **before** the handler is invoked, so
    the handler's `VALUE` is the fully expanded string (the `deg` token rides inside the variable).
  - `CConfig::parse()` (lines 916-927) runs `clearState()` (lines 1070-1076: categories, parseError,
    env vars, non-static special categories only — **config values and custom `data` untouched**)
    and re-applies defaults via `defaultFrom`.
  - `src/common.cpp:79-123` — `defaultFrom` CUSTOM case (lines 111-117) calls
    `type->handler(defaultVal, &type->data)` on the same slot; with Hyprland's `0x…` default string
    (no `deg`) the angle passes through stale.

## 3. F3 — library harness (decisive mechanism test)

Compiled against the installed system `libhyprlang.so.0.6.8` (g++ 16.2.1), handler a faithful copy of
`configHandleGradientSet`'s token loop (tokenize on spaces, angle assigned only on a token containing
`deg`):

- **pass1** — host chain replayed: `$activeBorderColor = rgba(33ccffee) rgba(00ff99ee) 45deg`,
  `col.active_border = $activeBorderColor`, then `$activeBorderColor = rgb(e68e0d)` and
  `col.active_border = $activeBorderColor` again (no deg):
  `pass1: colors='rgb(e68e0d) ' angle=45.0deg` — **inheritance reproduced end-to-end**
  (variable redefinition → expansion → handler on persistent data).
- **pass2** — same CConfig object re-parsed with a config containing **no `deg` anywhere**
  (`col.active_border = rgb(111111)`): `pass2: angle=45.0deg (same data ptr: YES)` — inheritance
  crosses `parse()` boundaries; the stale angle survives a reload.
- **pass0 (reverse direction)** — first declarer `45deg`, second declarer `0deg`:
  `pass0: colors='rgba(00ff99ee) ' angle=0.0deg` — **a deg token on the last declarer always wins**;
  there is no mechanism by which an older angle can override a newer deg token.

## 4. Host census — every gradient key

Declarer trees read directly; live values from `.ufo/waves/round-40/c1/native-capture.jsonl` (70
keys), spot-re-confirmed live (`hyprctl getoption -j general:col.active_border` →
`{"option": "general:col.active_border", "custom": "ffe68e0d 45deg", "set": true }`, same for
`col.inactive_border` → `aa595959 0deg`, exit 0).

Source order in `~/.config/hypr/hyprland.conf`: defaults tree sourced at lines 4-12, theme at line 13.
The only `deg` token in the entire host config tree is
`~/.local/share/omarchy/default/hypr/looknfeel.conf:4` (`$activeBorderColor = rgba(33ccffee) rgba(00ff99ee) 45deg`).

| key | declarer chain (in source order) | live | model |
|---|---|---|---|
| general:col.active_border | defaults looknfeel:15 via `$activeBorderColor` (45deg) → theme hyprland.conf:4 (`rgb(e68e0d)`, no deg) | `ffe68e0d 45deg` | **inherited 45deg** ✓ |
| group:col.border_active | defaults looknfeel:51 via `$activeBorderColor` (45deg) → theme:7 (no deg) | `ffe68e0d 45deg` | **inherited 45deg** ✓ |
| group:col.border_locked_active | defaults looknfeel:53 via `$activeBorderColor` (45deg); never redeclared | `ee33ccff ee00ff99 45deg` | own 45deg ✓ |
| general:col.inactive_border | defaults looknfeel:16 via `$inactiveBorderColor` (`rgba(595959aa)`, no deg) | `aa595959 0deg` | fresh object, ctor 0 ✓ |
| group:col.border_inactive | defaults:52, never redeclared | `aa595959 0deg` | fresh 0 ✓ |
| group:col.border_locked_inactive | defaults:54, never redeclared | `aa595959 0deg` | fresh 0 ✓ |
| decoration:shadow:color | defaults looknfeel:35 `color = rgba(1a1a1aee)` (no deg) | `ee1a1a1a 0deg` | fresh 0 ✓ |
| group:groupbar:col.active / col.inactive | defaults groupbar colour literals (no deg) | `40000000 0deg` / `20000000 0deg` | fresh 0 ✓ |
| general:gaps_in / gaps_out | gap handler (`configHandleGapSet`, ConfigManager.cpp:170+) — no angle field | `0 0 0 0` | n/a ✓ |

**F1: not found.** Exactly two keys have an angled earlier declarer plus a no-deg last declarer
(`col.active_border`, `col.border_active`); both show `45deg`, not `0deg` — inheritance, not its
refutation. **F2: not found** — no host key has a deg-bearing last declarer at all (the only deg
declarer is looknfeel.conf:4 through the variable), so the reverse direction rests on the source
assignment at ConfigManager.cpp:120 and harness pass0, both of which confirm last-deg-wins.

## 5. What would have falsified, and what did not

- F1 (`0deg` after an angled earlier declarer): absent from the host; the two applicable keys show 45deg.
- F2 (stale angle overriding a new deg token): impossible per source (unconditional assignment on the
  deg token) and empirically false in the harness (pass0).
- F3 (mechanism not reproducible in real hyprlang): reproduced exactly, twice over.

The evidence does not refute the claim; it confirms it at source, library, and host levels, and
**extends** it: inheritance persists across reloads (pass2), because `clearState()` and `defaultFrom`
never touch the angle and Hyprland's gradient default string carries no `deg`.

## 6. Residuals and verification gaps

1. **Cross-reload inheritance is broader than the claim.** After a reload in which no declarer
   carries `deg`, live keeps the stale angle (pass2) while a tree-only model predicts `0deg`. Harmless
   for this host (looknfeel.conf:4 re-applies 45deg at every parse, so the 70/70 receipt is
   unaffected), but a C1/C2 sentence claiming "the angle comes from the declarer chain" is true only
   within a parse lineage; the honest phrasing is "the angle is the last one any parse applied".
2. **Fractional angles truncate.** The handler uses `stoi` (ConfigManager.cpp:120): `45.5deg` parses
   as 45 and `toString()` prints `45deg`. Declared-vs-live comparison still agrees (both truncate), so
   no mismatch, but the angle is lossy.
3. **`deg` is a substring match** on any token (`var.find("deg")`): a non-hex token containing "deg"
   (hex digits never contain `g`) routes to the stoi branch; a malformed one produces a parseError and
   leaves the angle untouched — still no reset. No false-inheritance path found.
4. **Reverse direction has no host instance** (gap, not defect): it is verified at source line 120 and
   in the harness, but no live key exercises it.
5. I could not and did not reload the compositor (forbidden verb); pass2 models the reload at library
   level instead.

## 7. Tooling and hygiene

- No installs; used system g++ 16.2.1, system `libhyprlang.so.0.6.8`, python3, curl (fetched
  hyprlang tag `v0.6.8` sources and tags list from GitHub for reading only).
- Compositor verbs used: `hyprctl version`, `hyprctl getoption -j` on two keys — read-only.
- Scratch `/tmp/revangle/`, `/tmp/hyl-cfg.cpp`, `/tmp/hyl-inc.hpp`, `/tmp/hyl-common.cpp` created by
  this seat and removed after this report; `/tmp/mado40-probe/` and `/tmp/r40src/` are not mine and
  were left untouched. Only this report file was written inside the lane.
- This review is a recommendation; it does not admit, integrate, or judge the claims.
