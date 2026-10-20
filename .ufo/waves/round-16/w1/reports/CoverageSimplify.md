# CoverageSimplify — U7 Waybar module-text note scope

Seat: `MadoR16.CoverageSimplify` (simplifier, leaf, no dispatch). Lane: mado-shokunin. Round 16, wave w1.
Scope: review the U7 note scope; remove the sprawling general Waybar tutorial; keep the observation boundary.
Mode: source reading only. No producer run, no host/compositor/service/package/input probe, no install, no edit outside this report.

## Status of the target

`.ufo/waves/round-16/waybar-draft.txt` does not exist yet at review time (WaybarDraft has not landed). This review therefore scopes the **assigned spec** (`spec.json` item `WaybarDraft`, items 22-26; `MeasureBuild` item 12-16) against the tagged sources and the existing corpus. The recommendations below are the cut list the draft should satisfy. Nothing here is a verdict on a draft.

## Sources read (tagged, raw bytes, scratch copy only)

| Id (reserved) | URL (tag 0.15.0) | Lines | SHA-256 (raw bytes at fetch) |
|---|---|---|---|
| S054 (code) | `https://raw.githubusercontent.com/Alexays/Waybar/0.15.0/src/modules/custom.cpp` | 292 | `2232f7f7141caa5958344e1e6a0ab8eec6321994da1fecd704345aeb513b291f` |
| S053 (man) | `https://raw.githubusercontent.com/Alexays/Waybar/0.15.0/man/waybar-custom.5.scd` | 250 | `efb6a63a3d7f125840d4c4a49956664070f36231724e7aa0fa281e6d2de30d82` |

Scratch copies: `/tmp/mado-r16-simplify/` (outside the lane; disposable). Line anchors below refer to those copies. Fetched with `curl` read-only; no install.

Digests are the reviewer's fetch, not a registry-verified pin. The draft must re-fetch and compare before citing.

## Source facts that fix the observation boundary (what the note may say)

- **Text path, raw mode.** `parseOutputRaw` (custom.cpp:222-255) takes line 0 as text, line 1 as tooltip, line 2 as a CSS class; later lines are ignored (`break`, :250-252). Invalid UTF-8 is replaced (:227-230).
- **Text path, json mode.** `parseOutputJson` (custom.cpp:257-292) reads `text`, `alt`, `tooltip`, `class`, `percentage` from the **first** line only (`break` at :290). Multi-line JSON after line 1 is not read.
- **Escape.** Man `escape`: default false (waybar-custom.5.scd:125-128). Only when true are text/tooltip passed through `Glib::Markup::escape_text` (custom.cpp:233-235, :243-244, :263-274).
- **Renderer input.** `update()` builds `str` with `fmt::format(format_, text, alt, icon, percentage)` (custom.cpp:175-177) and calls `label_.set_markup(str)` (:181). With escape off, script output reaches GTK as **Pango markup**. What the user sees is GTK's result, not the producer's bytes.
- **Tooltip is a separate channel.** Tooltip goes through `set_tooltip_markup` (:182-193). With `tooltip-format` set it overrides script tooltip (man `tooltip-format`, waybar-custom.5.scd:120-123). Tooltip is not label text.
- **Class is a CSS channel.** Classes are added to the label style context (custom.cpp:195-206), not drawn.
- **Hide conditions.** For exec modules, the event box is hidden when `output_.out` is empty **or** `exit_code != 0` (custom.cpp:164-166). Also hidden when formatted `str` is empty or `hide-empty-text` with empty text (:178-179).
- **Scheduling is not text.** Worker choice (custom.cpp:21-28) and interval/signal/restart paths (:33-160) decide *when* output is read. They do not change what text is produced.

### Source answer to an existing UNK (route, do not edit here)

`corpus/knowledge/waybar-walker-semantics.md` §3.2 (`custom/update`) records the non-zero-exit render as **UNK** because the man page is silent. The tagged code now answers the hide case: custom.cpp:164-166 hides the module on `exit_code != 0`, so the stale text is not kept. This is a source fact for an append-only errata candidate in the semantics note, owned by L1/the lane, not a U7 claim. It is also a `custom/update` behaviour, not module-text observation; keep it out of the U7 note body.

## Cut list (sprawl to remove from the WaybarDraft prompt and any draft)

The current WaybarDraft task text asks for: exec output, JSON fields vs GTK rendering, **return-type/json restart interval signal**, and **privacy/network action boundaries**. Those are the tutorial sprawl. Cut as follows:

| Remove | Why | What remains |
|---|---|---|
| `interval`, `restart-interval`, `signal`, `exec-if`, `exec-on-event`, `once`, worker-choice detail (custom.cpp:21-160; man entries) | Scheduling, not text observation. Adds code-path claims the note does not need. | One sentence: scheduling decides when a value is read; it is outside U7. No signal producers, no restart claims. |
| Click/scroll/menu/`on-update`/`expand`/`rotate`/`align`/`justify`/length options | Interaction and layout; none is module text. | Omit. |
| Man EXAMPLES section, including the Alternate Pacman `on-click` with `sudo pacman -Syu` | Tutorial content; an unsafe example to repeat. Not evidence. | Omit entirely. Do not quote it. |
| STYLE section and `#custom-<name>` CSS | Already in `waybar-walker-plane.md` §2.5 and `waybar-walker-semantics.md` §5. | One line: classes exist; CSS is not admitted here. |
| Host module catalogue (`custom/omarchy`, `ai-usage`, `weather`, indicators, voxtype) | Duplicates `waybar-walker-semantics.md` §3 (lane authority). | Link to that note. No restated rows. |
| `alt` field and icon keying | Undocumented; already owned by semantics §3 (`alt` note). | Omit. |
| Escape behaviour beyond "off by default; when on, text is escaped" | Escape detail is a deeper renderer/tooltip question. | Omit. See deferred item D1 below. |
| "Privacy/network action boundaries" section | Re-litigates host producers (weather/update network I/O) owned by existing notes. No network or probe is in scope this round. | One line in Safe observation: producers are not run; no network access is performed by this note. |
| Default-format resolution (man `{text}` vs constructor `"{}"`) | Not traced in this pass; not needed for the boundary. | Omit; do not state a default. |

Net effect: the four required level-2 sections survive with the required `[UNK]` in the last one. Expected body is roughly one screen per section, not a tutorial.

## Recommended U7 note skeleton (budget, not prose)

Provenance trio first (exact `covers: U7`, source/verified/recheck lines in the U6 style), then:

1. **`## Producer contract`** (smallest section). Exec stdout is read as raw (lines 0-2 = text, tooltip, class) or as JSON (first line only, fields text/alt/tooltip/class/percentage). Cite custom.cpp:222-255, :257-292 and man RETURN-TYPE (waybar-custom.5.scd:148-150). Quote ≤25 words from the man, e.g. `The tooltip format. If specified, overrides any tooltip output from the script in *exec*.` (waybar-custom.5.scd:120-122). Name the S054 source and its digest.
2. **`## Renderer boundary`**. Text goes through `format` into `set_markup` (custom.cpp:175-181), so script output is Pango markup unless escape is on. Tooltip, class and hide paths are separate channels (:164-166, :182-206). State that GTK rendering of the markup is not observed.
3. **`## Safe observation`**. Source reading only. No producer script executed, no `waybar` launch, no signal sent, no IPC (none exists in 0.15.0 per `waybar-walker-semantics.md` §2.3), no network. Host module text stays `[UNK]`.
4. **`## Unexercised rendering`** (ends with `[UNK]`). GTK markup result, glyph/tooltip display, live text values, and whether any given producer's output is valid markup on this host.

Words are budgeted for the four sections together; prefer a table for the source facts over prose.

## Deferred items (observed; keep out of the U7 note)

- **D1 — raw-mode tooltip ignores escape.** custom.cpp:240 unconditionally sets `tooltip_ = validated_line` after the escape branch at :232-239, so for raw line 0 the tooltip is not escaped even when `escape` is true. Tooltip is out of U7 text scope. Route to a future tooltip note; do not state it as a U7 claim. Confirm in source before any use (single-pass reading, not executed).
- **D2 — `custom/update` non-zero exit.** See the errata candidate above; route to L1/semantics note.
- **D3 — default format.** Man `{text}` vs ALabel default `"{}"` (custom.cpp:9). Not traced; exclude.

## Anti-inference lines the note should carry (short)

- Producer stdout ≠ displayed text. Markup is interpreted by GTK; the result is not observed here.
- `tooltip-format` overrides the script's tooltip; tooltip is not label text.
- JSON reads one line only; raw reads three lines.
- Nothing here shows the bar currently displays any particular module text.

## Axes and moves

- **C1 coverage:** kept. The four required sections, the source-fact table and the `[UNK]` tail satisfy the measured U7 route. Cutting scheduling, examples and catalogue does not reduce the rubric count (covers: U7, reciprocal S053/S054, headings). Net: no coverage loss.
- **C2 operability:** not touched. Removing the `sudo pacman -Syu` example and the network/privacy section lowers the chance that the draft repeats an operator-unsafe command. No host effect.
- **Quality/precision:** improved. Fewer unobserved claims; each kept claim carries a tagged anchor.
- **Adjacency:** improved. Host catalogue and style are linked, not restated, so no second authority.
- Move kept: the four-section skeleton with source-fact table. Move rejected: a full module tutorial (improves nothing measured; adds unverified claims).

## Limits

- No draft exists yet; this is scope guidance against spec and sources, not a verdict on text.
- Source reading only; no build, lint, test, gate, or producer run. Checks belong to L1 after integration.
- Line anchors are for the 0.15.0 tag bytes fetched at review time; the draft must re-fetch and reconcile the digests.
- Waybar behaviour on this host is out of scope and remains `[UNK]`.

## Tooling

No installs, updates, or package operations. Tools used: read, bash `curl` (read-only fetch to `/tmp`), `sha256sum`. Nothing recorded as installed. Pacman remains paused host-wide per the contract.

## Handoff

- WaybarDraft / L1: apply the cut list and skeleton above; re-fetch S053/S054 and confirm the digests before citing.
- L1: consider the append-only errata candidate for `waybar-walker-semantics.md` §3.2 (D2), owned by the lane.
- Main agent: verification belongs to L1 after integration (not run here).
