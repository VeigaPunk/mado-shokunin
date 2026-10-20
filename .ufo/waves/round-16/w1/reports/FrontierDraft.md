# FrontierDraft — README draft for U7 route and retained unknowns

Seat: `MadoR16.FrontierDraft` (scribe, leaf member, no subagent dispatch).
Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`. Baseline `32c4fda8`.
Scope: draft text only. `corpus/README.md` is owned by L1 and was **not edited**.
No other file was written. No commit, build, test, gate, install or host probe.

## Inputs read (source reading only)

- `corpus/lessons/round-15-verifier-spotcheck.md` (read first, per contract).
  Relevant anchors: U7 `absent/absent` in its rubric table; R15-V1 host
  partial upgrade; "U7, real hardware/input processing, client delivery,
  IME/application outcomes, live-health clearance and promotion independence
  remain unmeasured."
- `corpus/README.md` (current bytes; sha256 prefix `1b6596aaec80e8ea`):
  Coverage map row for U6 at line 40; Province table Waybar row at line 57;
  Frontier at line 73; round-15 frontier bullet at lines 104–109; first
  frontier bullet (rendered UI / Waybar module text) at lines 77–79.
- `corpus/knowledge/input-debugging-boundaries-r15.md` (template for the
  four-section shape and the `[UNK]` discipline; U6 "Unexercised delivery").
- `corpus/knowledge/waybar-walker-semantics.md` §§1–5 (dated 2026-10-14 host
  samples; §2.3 "no IPC/query verb in 0.15.0" ⇒ module text UNK; §3 module
  rows with Live column; §4 signal bus).
- `corpus/SOURCES.md` registry rows S051–S052 (last rows; S053/S054 absent,
  so reserved ids are free). Registry has 228 lines.
- `.ufo/waves/round-16/w1/spec.json` items `FrontierDraft`, `WaybarDraft`,
  `ExistingU7`, `MeasureBuild`.

No Waybar source was fetched by this seat. Source-level claims about
`waybar-custom.5.scd` and `custom.cpp` belong to `WaybarDraft`/`SourcesDraft`
and are **not** asserted below; the row only points at reserved S053/S054.

## Collision check

- `corpus/knowledge/` has no `*r16*` file; the only waybar notes are
  `waybar-walker-plane.md` and `waybar-walker-semantics.md`.
- Proposed note filename: `knowledge/waybar-module-text-boundaries-r16.md`.
  Proposed only; L1 chooses the final name and reconciles it with
  `waybar-draft.txt` from `WaybarDraft`.

## Draft 1 — Coverage map row (insert after the U6 row, line 40)

Paste as one table row. Reserved ids S053/S054 must be admitted by L1 before
this row is landed; the `source:` cell is not valid until they are.

```markdown
| `knowledge/waybar-module-text-boundaries-r16.md` (MADO-R16-1, round 16; covers U7) | Bounded documented Waybar custom-module route in four sections: producer contract (exec output fields and refresh modes), renderer boundary (what the bar draws from that output), safe observation (recorded and source-described contracts only, no producer run), and unexercised rendering. Producer output, rendered text and observed host values stay separate. | `source:` S053 (tagged Waybar 0.15.0 `man/waybar-custom.5.scd`) and S054 (tagged `src/modules/custom.cpp`) in [SOURCES](SOURCES.md); host module values are dated 2026-10-14 samples in [semantics](knowledge/waybar-walker-semantics.md) §§2–5. No producer execution, network request, screenshot or bar probe; rendering is not inferred from source or config. |
```

## Draft 2 — Province table, Waybar row limit cell (line 57)

Replace only the final cell; keep the other cells unchanged:

```markdown
No module-text IPC/query verb at the recorded version; rendering is not inferred from file imports or producer output. Round 16 adds the [module-text route](knowledge/waybar-module-text-boundaries-r16.md) for the documented contract only.
```

Add to the Start-here cell (optional, same row): `, [module-text route](knowledge/waybar-module-text-boundaries-r16.md)`.

## Draft 3 — Frontier additions

### 3a. Replace the first-bullet clause (lines 77–79)

Current text names "Waybar module text" as an unresolved item with no new route.
Proposed replacement for the phrase only (rest of bullet unchanged):

```markdown
- Rendered UI and Walker socket protocol, dispatcher behavior and per-window rule effects: [arc gap ledger](knowledge/arc-synthesis.md)
  §6. Waybar module text now has a documented contract route (round 16); its rendered output stays open as listed below. No screenshot, input injection or socket connection is added here.
```

### 3b. Append after the round-15 bullet (after line 109)

Append-only; do not edit the round-15 bullet.

```markdown
- Round 16 moves only U7's **documented Waybar custom-module contract** onto
  [sourced ground](knowledge/waybar-module-text-boundaries-r16.md). The route
  separates producer output, the bar's renderer and any observed on-screen text.
  It is not rendered verification. The following remain `[UNK]`:
  - **Rendered output:** on-screen module text, glyph and font fallback, tooltip
    display, CSS-applied class effects, and any screenshot or pixel state. No
    capture was taken and no compositor, layer or screenshot probe is claimed.
  - **IME and text input:** composition, commit, preedit and text-input behavior,
    and whether text reaches a focused client. The recorded 19-module set has no
    text-entry module (`waybar-walker-semantics.md` §3); Walker's search field and
    any application text field are not exercised. The round-15 toolkit/IME `[UNK]`
    still applies in full.
  - **Hardware:** actual values of hardware-facing modules on this host. The
    2026-10-14 sample recorded no power-supply device (battery module has no
    source), `wlan0` DOWN with the ethernet branch by inference only, a Bluetooth
    adapter present with zero devices (branch selection not read), and a PipeWire
    sink whose module text was not read. Hardware event production, kernel or
    driver causes and their effect on any module are unmeasured.
  - **Freshness:** every host value is a dated point sample. Update, weather,
    voxtype and AI-usage module output were not refreshed, and no current module
    state is claimed.
```

## Draft 4 — Limits the note must carry (for the knowledge file author, not README text)

- Refresh modes described from the tagged source/man only; the `interval` /
  `signal` / self-looping script cases are `[INF]` until L1 confirms the quoted
  S053/S054 text.
- `alt`-keyed icons and undocumented JSON fields stay `[INF]` (already recorded
  in `waybar-walker-semantics.md` §3 "alt (undocumented)").
- The host `custom/voxtype` module is not installed; a payload from an absent
  producer is not a rendered module state.

## Reserved-source dependencies (L1 integration)

1. S053 and S054 must be opened and admitted by the source seat before the row
   is landed. No quote, digest or URL is asserted by this draft.
2. Mined reciprocity: the note's `source:` cell and S053/S054 `used-by` cells
   must name the note path exactly once; the round-15 counter checks joins.
3. `covers: U7` is the only coverage marker; the four level-2 headings must be
   exact: `Producer contract`, `Renderer boundary`, `Safe observation`,
   `Unexercised rendering` (last section contains `[UNK]`).

## Assumptions and limits

- Draft content is based on existing lane notes and the round-15 closure. It
  does not re-verify any host value and does not re-read Waybar source.
- The Coverage row claims only a documented route. It does not claim module
  text observed, rendered, or working on this host.
- Round-15 bullet is left unchanged on purpose (historical record).

## Tooling

No installs, updates or package operations were performed by this seat. Host
pacman transactions remain paused per the round contract; none was attempted.

## Verification

None run by this seat (scribe draft; L1 verifies once after integration). The
anchors above were read from current bytes at 2026-10-20.
