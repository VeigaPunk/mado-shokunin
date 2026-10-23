# SrcHyprctlAnims — source-opening report

## Behavior

Opened the Hyprland v0.56.2 source at commit `efb50993780079460b0cbed1363e2166a2de1d9f`, `src/debug/HyprCtl.cpp`. `animationsRequest` is at lines 927–985; the `animations` command registration is at line 2018. The JSON branch constructs a two-element top-level array: animation-node objects first, then bezier objects. Each node has `name`, `overridden`, `bezier`, `enabled`, `speed`, and `style`; each bezier has `name`, `X0`, `Y0`, `X1`, and `Y1`. Speed and all four point coordinates are formatted with `{:.2f}` (fixed two decimal places). Bezier coordinates come from control points 1 and 2. These are source findings, not a runtime capture.

## Located quotes

> `ret += "[[";`

`src/debug/HyprCtl.cpp:947`. The writer opens the nested top-level/node array.

> `ret += ",\n[";`

`src/debug/HyprCtl.cpp:964`. After closing the node array at line 962, the writer starts the second (bezier) array; line 981 appends `]]` to close the arrays.

```
    "name": "{}",
    "overridden": {},
    "bezier": "{}",
    "enabled": {},
    "speed": {:.2f},
    "style": "{}"
```

`src/debug/HyprCtl.cpp:951–956`. This gives the node fields and shows speed formatted to two decimal places.

```
    "name": "{}",
    "X0": {:.2f},
    "Y0": {:.2f},
    "X1": {:.2f},
    "Y1": {:.2f}
```

`src/debug/HyprCtl.cpp:970–974`. This gives the bezier fields and two-decimal formatting for every point coordinate.

Python whitespace-collapsed substring check against the fetched UTF-8 source: `quote_1=True`, `quote_2=True`, `quote_3=True`, `quote_4=True`.

## Provenance and commands

Raw URL: `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/debug/HyprCtl.cpp`

Fetch command run:

```sh
mkdir -p /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/fetch && timeout 30s prlimit --as=4000000000 -- curl -fsSL https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/debug/HyprCtl.cpp -o /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/fetch/SrcHyprctlAnims.bin && sha256sum /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/fetch/SrcHyprctlAnims.bin && wc -c /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/fetch/SrcHyprctlAnims.bin
```

Outcome: fetch succeeded; SHA-256 `798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa`; size `97582` bytes. The Python quote check read the fetched bytes as UTF-8 and tested each of the four quotes after collapsing whitespace with `re.sub(r'\s+', ' ', text).strip()`; all four checks passed.

## SOURCES disposition

The exact raw URL is already in `corpus/SOURCES.md` as S158 (HyprCtl.cpp), so no duplicate row is proposed. Propose extending S158's `used-by` cell from `corpus/knowledge/rule-attribution-r24.md` to `corpus/knowledge/rule-attribution-r24.md, corpus/knowledge/animation-table-r26.md`. The new knowledge article should cite `src/debug/HyprCtl.cpp:927-985 @ efb50993780079460b0cbed1363e2166a2de1d9f` and the fetched digest above.

## Gates, touched surfaces, and limits

- Source-opening work completed: pinned raw source fetched, digest and byte count recorded, writer and registration located, and all four short quotes checked against the fetched bytes.
- No counter, control, build, test, Hyprland instance, or host compositor command was run. This is not counter or runtime evidence and has no `TARGET_MET` verdict.
- Touched only the named fetch artifact and this report; `corpus/SOURCES.md` and product files were read but not edited.
- Artifacts: `.ufo/waves/round-26/fetch/SrcHyprctlAnims.bin`; `.ufo/waves/round-26/w1/reports/SrcHyprctlAnims.md`.
