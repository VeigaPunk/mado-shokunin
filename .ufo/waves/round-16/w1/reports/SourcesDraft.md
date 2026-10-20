# SourcesDraft — round 16 (mado-r16-w1)

Seat: `MadoR16.SourcesDraft` (scribe, leaf). Scope: draft S053/S054/S055 registry rows with exact anchors for L1 integration. `corpus/SOURCES.md` was NOT edited (L1 owns it). Only this report was written.

Baseline HEAD: `32c4fda873c9cb47a84c549b24b80ead2bcaa1ea` (verified via `git rev-parse HEAD`). Lane working tree: `M SCORECARD.md`, `M corpus/QUALITY.md`, `?? .ufo/waves/round-16/` (other seats; not touched here).

## Tooling

No installs, updates, or package operations. No pacman, service, compositor, input, or screenshot probes. No Waybar binary executed; no census, gate, or measure run. Network reads used pre-existing `curl`, `sha256sum`, `stat`; one GitHub API GET resolved the tag. Nothing to record as installed.

## Sources opened (first, before drafting)

| Source | Ref | Bytes | sha256 | Opened |
|---|---|---|---|---|
| `https://raw.githubusercontent.com/Alexays/Waybar/0.15.0/man/waybar-custom.5.scd` | tag 0.15.0 | 6656 | `efb6a63a3d7f125840d4c4a49956664070f36231724e7aa0fa281e6d2de30d82` | 2026-10-20 |
| `https://raw.githubusercontent.com/Alexays/Waybar/0.15.0/src/modules/custom.cpp` | tag 0.15.0 | 8746 | `2232f7f7141caa5958344e1e6a0ab8eec6321994da1fecd704345aeb513b291f` | 2026-10-20 |
| `https://raw.githubusercontent.com/Alexays/Waybar/0.15.0/src/ALabel.cpp` | tag 0.15.0 | 7944 | `7000f686548fa8572aecef8073ee0e05fd30f851f9b6778e706791280d286a48` | 2026-10-20 (verification only; not admitted, see Leads) |
| `https://api.github.com/repos/Alexays/Waybar/git/refs/tags/0.15.0` | tag object | — | commit `90b209add8937514d0a987aa842e701bd8f1232e` | 2026-10-20 |
| `corpus/lessons/round-15-verifier-spotcheck.md` | HEAD `32c4fda8` (tracked, clean) | — | `58e247f8525483eb7d4cc7a71ac4e64cb2b2ed3e5716af1234c0588cb882928a` | 2026-10-20 |

Tag resolution: `refs/tags/0.15.0` → commit `90b209add8937514d0a987aa842e701bd8f1232e` (type commit).

## Draft rows (preserve 11-column shape; no existing row changed)

Columns: `id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by`.

```
| S053 | Waybar 0.15.0 custom module man page — https://raw.githubusercontent.com/Alexays/Waybar/0.15.0/man/waybar-custom.5.scd | docs | A | Upstream documented custom-module producer contract at tag 0.15.0: exec output, return types, update triggers, format replacements; not rendered text, host module state, or package-binary equivalence | tag 0.15.0 @ 90b209add8937514d0a987aa842e701bd8f1232e; `# CONFIGURATION` :11, `*exec*` :15-17, `*exec-on-event*` :28-31, `*interval*` :37-43, `*signal*` :52-56, `*format*` :58-61, `*escape*` :125-128, `*tooltip-format*` :120-123, `# RETURN-TYPE` :148-166, `# FORMAT REPLACEMENTS` :168-174; raw sha256 efb6a63a3d7f125840d4c4a49956664070f36231724e7aa0fa281e6d2de30d82 (6656 bytes) | Documents the exec script output as the module's text source, JSON versus newline-separated raw return types, and interval/signal/no-trigger update timing; lists format replacements {text}, {percentage}, {icon} only (no {alt}; S054 shows the code also supplies {alt}) — upstream 0.15.0 contract claims, not displayed output | mined | 2026-10-20 | on-release | [PENDING: U7 note path, reciprocal]
```

```
| S054 | Waybar 0.15.0 custom module implementation — https://raw.githubusercontent.com/Alexays/Waybar/0.15.0/src/modules/custom.cpp | code | A | Tagged 0.15.0 implementation of the custom-module producer, parser, and update path; not GTK rendering, not Arch package 0.15.0-3 binary equivalence, not host output | tag 0.15.0 @ 90b209add8937514d0a987aa842e701bd8f1232e; constructor `Custom::Custom` :7 (format fallback literal `"{}"` :9; worker selection :18-30), `delayWorker` :39, `continuousWorker` :66, `waitingWorker` :118, `refresh` (signal wake) :138-142, `handleEvent` (exec-on-event wake) :144-148, `update` :162 (`fmt::arg("alt", alt_)` :175; `label_.set_markup(str)` :181), `parseOutputRaw` :222, `parseOutputJson` :257-292 (percentage :285-286); raw sha256 2232f7f7141caa5958344e1e6a0ab8eec6321994da1fecd704345aeb513b291f (8746 bytes) | Upstream code selects a waiting, delayed (interval), or continuous worker; signal and exec-on-event wake a sleeping worker; JSON or raw lines map into text/tooltip/class/percentage; {alt} is supplied to format; text reaches GTK via set_markup as Pango markup — a pre-render code path, not displayed text | mined | 2026-10-20 | on-release | [PENDING: U7 note path, reciprocal]
```

```
| S055 | mado round-15 spot-check closure — corpus/lessons/round-15-verifier-spotcheck.md | own-work | A | Lane safety record: the round-15 forbidden host partial upgrade (R15-V1) and the required real-plan validation before any future install (R15-V2); not host remediation, not a sandbox, not a fail-closed gate by itself | corpus/lessons/round-15-verifier-spotcheck.md:252-282 (`## Routed defects, remediation and retained limits`; R15-V1 :254-267, R15-V2 :268-278, R14-V1 :279-282) @ 32c4fda873c9cb47a84c549b24b80ead2bcaa1ea (sha256 58e247f8525483eb7d4cc7a71ac4e64cb2b2ed3e5716af1234c0588cb882928a) | An unchanged green gate does not offset a forbidden partial upgrade; hard-coded install-predicate fixtures are not pacman validation; any authorized future install needs a real `pacman -Sp --print-format '%n %v'` plan and complete installed-name comparison that refuses every overlap | mined | 2026-10-20 | on-change | [PENDING: round-16 safety-gate note path from SafetyGate output]
```

## Reciprocal joins L1 must add (measure.py requires them)

- S053 and S054 `used-by` → the U7 note path (final slug decided by the U7 note owner; none exists in the tree yet — `.ufo/waves/round-16/` holds only `dispatch.json`, `spec.json`, `reports/`).
- The U7 note's `source:` line must cite S053 and S054 (both `mined`, tier A) and carry the four exact level-2 sections named in `.ufo/waves/round-16/w1/spec.json` line 25 (Producer contract, Renderer boundary, Safe observation, Unexercised rendering; `[UNK]` in the final section).
- S055 `used-by` → the safety-gate note path once SafetyGate names it. Not messaged, per the lane contract (peer messages go only to MadoR16).

## Anchor verification (line map)

Man `waybar-custom.5.scd` (tag 0.15.0, 250 lines): `# CONFIGURATION` :11; `*exec*` :15-17 ("The path to the script, which should be executed."); `*exec-on-event*` :28-31 (default true); `*interval*` :37-43; `*signal*` :52-56; `*format*` :58-61 (default `{text}`); `*tooltip-format*` :120-123; `*escape*` :125-128 (default false); `# RETURN-TYPE` :148-166; `# FORMAT REPLACEMENTS` :168-174 (`{text}` :170, `{percentage}` :172, `{icon}` :174).

`custom.cpp` (tag 0.15.0, 292 lines): constructor :7-9 (`ALabel(config, "custom-" + name, id, "{}")` :9); worker selection :18-30 (`waitingWorker` when signal set and no interval/restart-interval; `delayWorker` when interval > 0; `continuousWorker` when exec set); `delayWorker` :39; `continuousWorker` :66 (restart-interval :92); `waitingWorker` :118; `refresh` :138-142; `handleEvent` :144-148; `update` :162 (fallback `alt` :175-186; `set_markup` :181); `parseOutputRaw` :222; `parseOutputJson` :257-292 (text :264/:266; alt :269/:271; percentage :285-286).

Lesson `round-15-verifier-spotcheck.md` (HEAD `32c4fda8`, working copy identical): `## Routed defects, remediation and retained limits` :252; R15-V1 :254-267; R15-V2 :268-278; R14-V1 :279-282.

## Quote admission material (for the quote-check seat; ≤25 words each)

- S053, man :43 — "If a signal is defined then the script will run once on startup and will only update with a signal." — 20 words.
- S053, man :42 — "If no interval or signal is defined, it is assumed that the out script loops itself." — 16 words.
- S055, lesson :189 — "Forbidden partial upgrade is real operability harm regardless of ABI observations or file-plane cleanliness." — 15 words.

## Divergences and teaching notes (for the U7 note)

1. **Default format.** Man says `default: {text}` (:60). Code passes the literal `"{}"` as ALabel's fallback (`custom.cpp:9`); ALabel uses it only when `format` is not a string (`ALabel.cpp:19`). Behavior of `"{}"` with only named `fmt::arg` values was NOT exercised; treat as an unresolved [INF], not a result.
2. **`{alt}`.** Code supplies `{alt}` to format and tooltip-format (`custom.cpp:175`, `:186`); man FORMAT REPLACEMENTS omits it.
3. **Mode selection.** Host `custom/ai-usage` declares both `interval` (60) and `signal` (11) per the existing plane note. Source path for that combination is `delayWorker` (interval > 0 is checked after the signal-only branch), and `refresh()` wakes the sleeping worker on signal 11. This is source-derived; no host run.
4. **Markup.** Raw text with `escape` false reaches `label_.set_markup(str)` (`custom.cpp:181`). The module text is Pango markup at the GTK boundary, not a plain string. Rendering is not verified.

## Leads (opened but not admitted as rows)

- `ALabel.cpp` (tag 0.15.0, sha256 above) was opened only to verify the fallback-format path. It needs its own reserved id if L1 wants it as a row; the reserved set is S053–S055 only, so I did not assign one. Recommendation: cite it inside S054's teaching as a secondary read, or mint a new id under L1's authority.
- Unopened: Waybar `util::command::exec`/`open` (shell and pipe behavior), `ALabel::update` and style classes, Arch package 0.15.0-3 patch set. Not needed for the bounded U7 claim; recorded as limits.

## Limits

- Tag 0.15.0 source is not binary-source equivalence to the host's installed Arch package `waybar 0.15.0-3`. Package patches were not compared.
- Documentation and code are cited for upstream behavior only; no host module text was observed, and none is claimed.
- `custom.cpp` and the man page were read as raw bytes via HTTP; hashes above are over those bytes.
- S055 is lane-own; it asserts only what the committed lesson says, not new safety evidence.
- Search-log wording suggested for L1 (not written): "Round 16 (2026-10-20), U7 source selection: opened tagged Waybar 0.15.0 man page and custom.cpp; identified/screened/included 2/2/2 (S053/S054); ALabel.cpp opened as a verification read, not admitted; excluded 0 candidates from the reserved set."

## Checks for the main agent (run once after integration; not run by this seat)

- `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` — expect W04-style warnings only; the new URLs are unique (no duplicate-url warning expected for S053/S054).
- `.ufo/waves/round-16/measure.py` reciprocal-join check: S053/S054 `used-by` ↔ U7 note `source:`.

## Blockers

None for the rows themselves. Pending: U7 note path and safety-gate note path (owned by the note/gate seats; L1 fills the `[PENDING]` cells).
