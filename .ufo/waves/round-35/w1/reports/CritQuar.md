# CritQuar — refusal reasoning for the mado register slice

Scope: the mado slice of
`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`
(read-only). The register carries 13 mado rows: six `payload-absent`
(S189, S195, S201, S205, S224, S228) and seven never-checked
(S199, S200, S209, S222, S223, S225, S235). The round-34 lesson
(`corpus/lessons/round-34.md` §Gate, "Refuse (assimilation package
quarantine-slice, twelve of thirteen rows)") refuses twelve: all but
**S189**, which was hand-checked IN-REGISTRY-SAME-ID and not re-appended.
The id space is the campaign's pre-remap staging ids (lane
`ID-REMAP.md`); row mapping verified against `HEAD:` copies of
`lanes/mado/*/SOURCES-PROPOSED.md`.

Every cited payload was re-checked directly (2026-10-24): EventManager.cpp
re-fetched from the pinned commit (6479 B, sha256-prefix `eea605dfe5ce09e1`
matches the row), the SJTU package re-extracted from
`lanes/mado/round2/fetch/`, `interwiki.json` + live API, the arXiv abstract
page + the aaron-fetched full LaTeX (`round8/fetch/arXiv-2604.18860.json`),
`cn-export-hyprland.html`, and the live host files for the own-work rows.

## Per-row verdicts

| register row | round | `unreachable` right? | `unverifiable` right? | fabrication? |
|---|---|---|---|---|
| S189 (EventManager.cpp) | r1 | no | no — the quote is **present** at `EventManager.cpp:128` | no — ABSENT is a checker artifact: the gate block stores `\\n` double-escaped, so the checker searched for a literal backslash-n while the file holds a real `\n` escape |
| S195 (SJTU zh-cn package) | r2 | no | no — **present** after stripping HTML tags | no — both quotes sit verbatim in `zh-cn/Hyprland.html` once `<a>`/`<span>` wrappers inside the sentence are stripped |
| S201 (arxiv.org/abs/2604.18860) | r2 | no | no — **present in the full LaTeX source** (`round8/fetch/arXiv-2604.18860.json`); quote 1 is from the Introduction, not "§ Abstract" as labeled | no — real quotes, section misattribution; the cited abs-page legitimately lacks them |
| S205 (interwikimap JSON) | r3 | no | **partially** — the quoted byte-format is unverifiable, but the claim is true | no — live API emits `{"prefix":"zh-hans",…}` compact + `\uXXXX` escapes; the lane's `interwiki.json` is a pretty-printed snapshot holding exactly the quoted spacing and literal 正體中文. The information is real; the byte-shape is a re-serialization |
| S224 (~/.cache/ai-usage/status.json) | r4 | **yes** — the quoted `updated_at` no longer exists | **yes as written** — a rolling timestamp in a mutable cache file | no — file exists, `"version": 2,` still matches; `updated_at` rotated to `2026-10-25T02:29:25Z`. Absent today ≠ never true; the row is genuinely unverifiable, exactly as the refusal says |
| S228 (cn-export-hyprland.html) | r5 | no | no — **present under unicode fold** | no — the file holds `使用“模板:过时”标记的页面或章节` with full-width quotes `“”`; the gate stored ASCII `"`. Same information, one-codepoint normalization gap |
| S199 (CSDN blog 149787804) | r2 | **yes** — direct fetch still HTTP 521 today | **yes** — quote only verifiable via the reader-proxy snapshot | no — unverifiable, not fabricated |
| S200 (CSDN blog 164457293) | r2 | **yes** — direct fetch still HTTP 521 today | **yes** — same as S199 | no |
| S209 (compositor log, /run/.../hyprland.log) | r3 | **yes as filed** — the instance-specific log is gone (new HIS dir `…_1792804449_…`) | **yes** — but the refusal reason is wrong: the gate **does** name a locator (an absolute path). "no locator" is a checker blind spot for a path that no longer resolves | no |
| S222 (~/.local/bin/gkeep) | r4 | no — file present and readable | **no — false.** `~/.local/bin/gkeep` exists today and both quotes verify verbatim (`from gkeep.cli import main`, `raise SystemExit(main())`) | no — but "unverifiable" is also wrong; the checker regex demands a file extension, so an extensionless executable was mis-tagged `no-locator` |
| S223 (~/.local/bin/ai-usage) | r4 | no — file present | **no — false.** `~/.local/bin/ai-usage` (symlink → Projects/omarchy-usage-tray) verifies verbatim, same extension blind spot as S222 | no |
| S225 (journalctl unit output) | r4 | **yes as filed** — command output is not a file | **yes in the snapshot sense** — but reproducible: re-run today gives 718 lines, still zero "overflowed event queue" markers | no — the claim still holds on re-run; the row is ephemeral-evidence, not wrong |
| S235 (socket dir /run/.../hypr/) | r5 | **yes as filed** — the cited inode-generation dir is gone | **yes in the snapshot sense** — the same measurement re-run today gives `700 directory`, `755 socket` on the live `.socket*.sock` | no — claim reproduces; only the pinned path is stale |

## Findings

1. **`unreachable` is right for five rows:** S199, S200 (CSDN, still 521),
   S209, S225, S235 (locator/command output that cannot be re-read at the
   cited bytes). S224 is borderline: the file is reachable, the quoted
   *bytes* are gone — the timestamp rotated; treat as unreachable-in-substance.
2. **`unverifiable` is right for six rows:** S199, S200, S209, S224, S225,
   S235 — the same six. This matches the lesson's own tag for the
   no-locator five.
3. **`unverifiable` is wrong for two rows the refusal files under it:**
   **S222 and S223 are verifiable today** — extensionless executables that
   the checker's path regex (which requires a file extension) never
   resolved. Both quoted lines verify verbatim against the live files.
   The register's `no-locator` tag and the lesson's "the register cites
   only a `## Gate — Snnn` prose anchor" are both factually incorrect:
   those gates carry absolute-path `- URL:` lines.
4. **No row is a fabrication.** Zero of thirteen. The six `payload-absent`
   rows are all present-or-true evidence under a normalization the checker
   lacked:
   - S189: escaping fold (markdown `\\n` vs code `\n`).
   - S195: tag-strip fold (anchor/span inside the quoted sentence).
   - S201: section-attribution error (Introduction quotes labeled
     "§ Abstract"); present verbatim in the full LaTeX.
   - S205: JSON re-serialization (compact API bytes vs pretty snapshot).
   - S224: mutable-state staleness (rolling `updated_at`).
   - S228: full-width vs ASCII quote fold.
5. **The refusal logic is right in outcome for all twelve but wrong in
   stated mechanism for four:** S222/S223 are refused as "no locator /
   unverifiable" when they are extensionless-path checker blind spots whose
   quotes are clean; S205/S228 are refused on province grounds while their
   register ABSENT flags are normalization artifacts, not evidence the
   quotes are wrong. S201 is refused on id-space collision — correct
   disposition, and the quotes are real content from the paper.
6. **Risk if taken literally:** re-running the refusal reasoning as written
   would keep S222/S223 permanently unverifiable (they aren't) and would
   let a reader believe all six payload-absent quotes are suspect; five of
   six are verified-present.

Recommended corrections to the Gate block (for the scribe): S222/S223
flip from "no locator → unverifiable" to "locator present, checker regex
blind spot; quotes verified — refuse on own-work-ephemerality grounds if
at all"; S205/S228 record the normalization artifact; S224's verdict is
the only payload-absent row whose `unverifiable` classification is correct
as filed.
