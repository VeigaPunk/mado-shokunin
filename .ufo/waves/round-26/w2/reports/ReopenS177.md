# ReopenS177 — re-open of draft row S177 + S158/S162 used-by quote checks

Date: 2026-10-23. Lane bounds: leaf member, no subagent dispatch. Host safety: no
compositor started, no WAYLAND_DISPLAY/HYPRLAND_INSTANCE_SIGNATURE set, no /dev/dri,
no counter or oracle run; fetches only. No tool installs.

## Scope

- Draft row S177 in `.ufo/waves/round-26/drafts/sources-rows.md` (hyprutils v0.14.2
  `src/animation/AnimationConfig.cpp`), quotes from w1 report
  `.ufo/waves/round-26/w1/reports/SrcAnimTree.md`.
- In-place `used-by` extensions on existing rows S158 (HyprCtl.cpp, w1
  `SrcHyprctlAnims.md`) and S162 (legacy `ConfigManager.cpp`, w1 `SrcAnimConfig.md`):
  verify the *new* quotes the w1 reports give against each row's pinned bytes.

## S177 — fetch and pin comparison

```sh
mkdir -p /fast/scratch/hyaku/mado-r26/reopen
timeout 120 prlimit --as=4000000000 -- curl -fsSL \
  https://raw.githubusercontent.com/hyprwm/hyprutils/v0.14.2/src/animation/AnimationConfig.cpp \
  -o /fast/scratch/hyaku/mado-r26/reopen/ReopenS177.bin   # exit=0
sha256sum ReopenS177.bin  # dbb5d50a27f80ea947db92050af40ee87e0e9e0718add0520cbc96e32abe268e
wc -c ReopenS177.bin      # 2354
wc -l ReopenS177.bin      # 70
```

Row claims `sha256:dbb5d50a27f80ea947db92050af40ee87e0e9e0718add0520cbc96e32abe268e, 2354 B`
@ `src/animation/AnimationConfig.cpp:9-70`, tag `v0.14.2`. Fresh bytes: identical
digest and byte count; the file is exactly 70 lines, matching the `:9-70` anchor
(`createNode` at :9, `setConfigForNode` at :35, propagation loop at :63-68). The
committed w1 capture `.ufo/waves/round-26/fetch/SrcAnimTreeHyprutils.bin` hashes
identically — the row's pin and the w1 capture agree.

## S177 — quote checks

The w1 SrcAnimTree report's S177-relevant quotes are its quotes 3 and 4 (quotes 1-2
belong to the Hyprland AnimationTree.cpp URL, i.e. row S176 — out of this item's
scope). Whitespace-collapsed substring of the freshly fetched UTF-8 bytes, word
count, and containment inside the cited line range:

| quote | cited | collapsed_substring | words | cited-range containment |
|---|---|---|---|---|
| `.pValues = (parentRef) ? parentRef->pValues : pConfig,` / `.pParentAnimation = (parentRef) ? parentRef : pConfig,` | :24-25 | True | 14 | True |
| `if (anim->pParentAnimation == PANIM && !anim->overridden) {` / `// if a child isnt overridden, set the values of the parent` | :63-64 | True | 19 | True |

Both ≤25 words and located at the cited lines. The row's summary ("node creation
links parents, explicit configs set `overridden`, unoverridden descendants inherit
parent values") is consistent with the file body (`createNode` writes
`.overridden = false` at :19; `setConfigForNode` writes `.overridden = true` at
:41; the :63 guard skips overridden children).

## S158 used-by extension — quote checks against pinned bytes

Row S158 pins `src/debug/HyprCtl.cpp @ efb50993780079460b0cbed1363e2166a2de1d9f,
sha256:798b7c6c…b91fa, 97582 B`. Re-fetched
(`/fast/scratch/hyaku/mado-r26/reopen/ReopenS177-S158.bin`): sha256
`798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa`, 97582 B —
matches the row; committed artifact `.ufo/waves/round-26/fetch/SrcHyprctlAnims.bin`
is byte-identical. The four new quotes in SrcHyprctlAnims.md all check:

| quote | cited | collapsed_substring | words | cited-range containment |
|---|---|---|---|---|
| `ret += "[[";` | :947 | True | 3 | True |
| `ret += ",\n[";` | :964 | True | 3 | True |
| node JSON block `name/overridden/bezier/enabled/speed {:.2f}/style` | :951-956 | True | 12 | True |
| bezier JSON block `name/X0/Y0/X1/Y1 {:.2f}` | :970-974 | True | 10 | True |

## S162 used-by extension — quote checks against pinned bytes

Row S162 pins `src/config/legacy/ConfigManager.cpp @ efb50993780079460b0cbed1363e2166a2de1d9f,
sha256:9db68cf4…be62b, 90963 B`. Re-fetched
(`/fast/scratch/hyaku/mado-r26/reopen/ReopenS177-S162.bin`): sha256
`9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b`, 90963 B —
matches the row; committed artifact `.ufo/waves/round-26/fetch/SrcAnimConfig.bin`
is byte-identical. SrcAnimConfig.md quotes 2-4 are on this file and all check:

| quote | cited | collapsed_substring | words | cited-range containment |
|---|---|---|---|---|
| `nodeExists` / `"no such animation"` / `enabledInt = parseInt(ARGS[1]).value_or(0) == 1` | :1434-1438 | True | 24 | True |
| `return "invalid speed"` … `speed = 10.f;` … `"no such bezier"` | :1457-1467 | True | 24 | True |
| `setConfigForNode(ANIMNAME, enabledInt, speed, ARGS[3], ARGS[4]);` + style validation + `return {};` | :1469-1478 | True | 20 | True |

SrcAnimConfig.md quote 1 (the `CVarList` ctor signature at
`include/hyprutils/string/VarList.hpp:14`) is on a *different* URL — the
supplemental hyprutils v0.14.2 VarList.hpp source the w1 report itself records as
"no second row proposed". It is therefore not a quote on S162's pinned bytes; for
completeness it verifies against the committed capture
`.ufo/waves/round-26/fetch/SrcAnimConfig-hyprutils-varlist.bin` (sha256
`9ad2fcbd5de691166b7db95de09b6bd054c9b4313deb3187e84c914dab74fc43`, 1883 B):
collapsed_substring=True, 18 words, contained at :14.

## Method

`python3 -I /fast/scratch/hyaku/mado-r26/reopen/ReopenS177-check.py` under
`timeout 60 prlimit --as=4000000000`: decodes each artifact as UTF-8, collapses
whitespace with `re.sub(r'\s+', ' ', t).strip()`, tests substring on the whole
file and on the cited 1-based inclusive line slice, counts whitespace-separated
words. Output: all 10 checks True, `ALL_OK`, exit 0. Script and binaries left in
`/fast/scratch/hyaku/mado-r26/reopen/` (not in the lane).

## Findings / residual risk

- No defects. Draft S177's pin fields (URL, tag, sha256, byte count, anchors,
  summary) all verify against a fresh ordinary fetch; both quotes match at cited
  lines.
- S158 and S162 `used-by` extensions are supported: every new quote the w1
  reports attribute to those rows verifies verbatim against the rows' pinned
  bytes.
- Minor note (not a defect): SrcAnimConfig.md quote 1 is sourced from a
  hyprutils header outside S162's URL; the w1 report discloses this and proposes
  no second row, so the extension rests on quotes 2-4 plus disclosed supplemental
  provenance.
- Residual risk: none observed beyond tag mutability of `v0.14.2` (the row pins
  bytes by sha256, so a tag move would surface as a hash mismatch — desired).

Verdict: `REOPEN S177 agree` — digest, size, anchors, and quotes all verify;
S158/S162 quote sets agree with their pinned rows.

Report: `.ufo/waves/round-26/w2/reports/ReopenS177.md`
