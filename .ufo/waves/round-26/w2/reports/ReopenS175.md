# ReopenS175 — re-open draft row S175 + used-by quote check for S158/S162

Date: 2026-10-23. Scope: draft SOURCES row S175 (`.ufo/waves/round-26/drafts/sources-rows.md`, w1 report `.ufo/waves/round-26/w1/reports/WikiAnimations.md`) plus the new quotes behind the in-place `used-by` extensions to committed rows S158 (`.ufo/waves/round-26/w1/reports/SrcHyprctlAnims.md`) and S162 (`.ufo/waves/round-26/w1/reports/SrcAnimConfig.md`).

## S175 — fresh fetch vs. row pin

Command:

```sh
timeout 60 prlimit --as=4000000000 -- curl -fsSL https://raw.githubusercontent.com/hyprwm/hyprland-wiki/ecc06f3b6605/content/Configuring/Animations.md -o /fast/scratch/hyaku/mado-r26/reopen/ReopenS175.bin && sha256sum /fast/scratch/hyaku/mado-r26/reopen/ReopenS175.bin && wc -c -l /fast/scratch/hyaku/mado-r26/reopen/ReopenS175.bin
```

Output: `f30f6bf44052e87b803a640750d5cb8c3295616a8508303a2280560a5964120b` — `115 4023` (lines, bytes).

- Row pins sha256 `f30f6bf4…4120b`, 4023 B @ `ecc06f3b6605e453c0ad533d979fccbefff788ef`: **match** (sha256 and byte count; 115 lines also matches the w1 report).
- The row URL uses the 12-char short hash `ecc06f3b6605`; it is a strict prefix of the pinned full hash and raw.githubusercontent.com resolved it to the pinned bytes. Cosmetic only.
- Fetched content is the hyprlang-era Animations page (title `Animations`, `animation = NAME, ONOFF, SPEED, CURVE [,STYLE]`, tree and style sections), consistent with the row's "historical documentation only" description.

## S175 — quote check (whitespace-collapsed substring, ≤25 words, cited line)

Checked with `python3 -I` (`re.sub(r"\s+"," ",s).strip()`), each quote required to appear in the collapsed file text AND in the collapsed cited line span:

| Cited line | Quote | Words | In file | In cited span |
|---|---|---|---|---|
| :11 | `animation = NAME, ONOFF, SPEED, CURVE [,STYLE]` | 7 | True | True |
| :23-24 | `The animations are a tree. If an animation is unset, it will inherit its parent's values.` | 16 | True | True |
| :38 | `↳ windows - styles: slide, popin, gnomed` | 7 | True | True |
| :114 | `animation = windows, 1, 8, default, slide left` | 8 | True | True |

All four quotes verified. Note: the quoted `↳` (U+21B3) and the straight apostrophe in `parent's` match the fetched bytes byte-for-byte after collapse.

## S158 — new quotes vs. row's pinned bytes

Pinned: sha256 `798b7c6c…91fa`, 97582 B. Artifact `.ufo/waves/round-26/fetch/SrcHyprctlAnims.bin` re-hashed: `798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa`, 97582 B — **matches the row's pinned bytes**, so the artifact was used directly (no re-fetch needed for quote checks; the URL is unchanged since w1).

| Cited line | Quote | Words | In file | In cited span |
|---|---|---|---|---|
| :947 | `ret += "[[";` | 3 | True | True |
| :964 | `ret += ",\n[";` | 3 | True | True |
| :951-956 | `"name"/"overridden"/"bezier"/"enabled"/"speed {:.2f}"/"style"` block | 12 | True | True |
| :970-974 | `"name"/"X0"/"Y0"/"X1"/"Y1" {:.2f}` block | 10 | True | True |

## S162 — new quotes vs. row's pinned bytes

Pinned: sha256 `9db68cf4…be62b`, 90963 B. Artifact `.ufo/waves/round-26/fetch/SrcAnimConfig.bin` re-hashed: `9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b`, 90963 B — **matches the row's pinned bytes** (the w1 report notes the file was replaced with the `legacy/ConfigManager.cpp` fetch; `SrcAnimConfig-legacy-impl.bin` hashes identically).

| Cited line | Quote | Words | In file | In cited span |
|---|---|---|---|---|
| :1434-1438 | `nodeExists(ANIMNAME)` → `"no such animation"`; `enabledInt = parseInt(ARGS[1]).value_or(0) == 1;` | 24 | True | True |
| :1457-1467 | `"invalid speed"` branches, `speed = 10.f;`, `bezierExists` → `"no such bezier"` | 24 | True | True |
| :1469-1478 | `setConfigForNode(ANIMNAME, enabledInt, speed, ARGS[3], ARGS[4])` then post-set style validation | 20 | True | True |

The fourth quote in `SrcAnimConfig.md` (`CVarList(const std::string& in, …)` @ `include/hyprutils/string/VarList.hpp:14`) is **not** a quote from S162's pinned file — the w1 report itself labels it as the supplemental hyprutils v0.14.2 source. Verified against its own artifact `SrcAnimConfig-hyprutils-varlist.bin` (sha256 `9ad2fcbd…fc43` as recorded): 18 words, present at line 14. No S162 row bytes are implicated by it.

## Caveats (residual risk, not verdicts)

- Row anchor spans vs. animation regions: S158's pin cites `src/debug/HyprCtl.cpp:346-484,613-630,647-723,1463-1645,2003-2044`; the new quotes live at :927-985 (outside the pinned spans; only the `animations` registration at :2018 falls inside :2003-2044). S162's pin cites `:419-451,590-623,893-968,2016-2093`; the animation/bezier handler quotes live at :1389-1479 (the :612-613 keyword registration is inside :590-623). The byte identity is proven by sha256, but if the ledger intends anchors to cover every claimed use, the integrator should extend the anchor cells for these rows.
- `corpus/knowledge/animation-table-r26.md` does not exist yet (peer scribe still drafting); these checks only confirm the quotes support such a note's sourcing.

## Verdicts

- `REOPEN S175 agree` — fresh fetch byte-identical to row pin (sha256 `f30f6bf4…4120b`, 4023 B); all 4 quotes verified at cited lines.
- `REOPEN S158 agree` — artifact bytes identical to pinned sha256 `798b7c6c…91fa`; all 4 new quotes verified at cited lines.
- `REOPEN S162 agree` — artifact bytes identical to pinned sha256 `9db68cf4…be62b`; all 3 new quotes from the pinned file verified at cited lines; the 4th quote belongs to the separately recorded hyprutils provenance artifact and also verifies there.

## Commands and limits

- Fetch: `timeout 60 prlimit --as=4000000000 -- curl -fsSL <S175 URL> -o /fast/scratch/hyaku/mado-r26/reopen/ReopenS175.bin` (exit 0).
- Hashes: `sha256sum` / `wc -c -l` on the fresh fetch and on `fetch/SrcHyprctlAnims.bin`, `fetch/SrcAnimConfig.bin`, `SrcAnimConfig-legacy-impl.bin`, `SrcAnimConfig-hyprutils-varlist.bin`.
- Quote check: `timeout 60 prlimit --as=4000000000 -- python3 -I /fast/scratch/hyaku/mado-r26/reopen/reopen-s175-check.py` (all True; script left in scratch for audit).
- No git/jj write commands, no lane edits outside this report, no Hyprland/oracle/counter runs, no host compositor contact, no tools installed (pacman untouched per pause). Scratch writes only under `/fast/scratch/hyaku/mado-r26/reopen/` (disk: 145 G free at fetch time).

Report: .ufo/waves/round-26/w2/reports/ReopenS175.md
