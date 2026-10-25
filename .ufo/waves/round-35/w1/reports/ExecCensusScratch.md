# ExecCensusScratch — census validate on scratch corpus mirror

Round 35, wave 1, seat ExecCensusScratch. Verdict: **append block does not
introduce a single new census finding, and the mirror census fails only on
mirror incompleteness — not on anything the append block did.**

## Setup

Mirror root: `.ufo/waves/round-35/scratch/ExecCensusScratch/validate/corpus/`

| Mirror path | Source |
|---|---|
| `corpus/SOURCES.md` | `corpus/SOURCES.md` (byte copy) |
| `corpus/README.md` | `corpus/README.md` (byte copy) |
| `corpus/knowledge/idle-lock-chain-armed-r14.md` | golden fallback (see below) |
| `corpus/knowledge/idle-lock-never-asked-r12.md` | golden fallback |
| `corpus/knowledge/idle-lock-offered-in-the-bar-r15.md` | golden fallback |

`scratch/ExecAppendBlock/` does **not** exist — seat produced no output — so the
three knowledge files came from
`.ufo/waves/round-35/controls/golden/corpus/knowledge/` per the dispatch
fallback clause.

## Command and result

```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
  --file .ufo/waves/round-35/scratch/ExecCensusScratch/validate/corpus/SOURCES.md
```

- **Exit code: 1**
- Findings: **212 lines** = 7 × W04 + 205 × E11.

Baseline for comparison — same command on the real
`corpus/SOURCES.md` (full lane tree): **exit 0**, same 7 W04 warnings plus the
`ok` line, zero E11. Every E11 on the mirror is a `used-by` path that exists in
the real corpus but was not mirrored (`corpus/lessons/*`, `corpus/knowledge/*`,
`tools/*`, `SKILL.md`, `quality/*`, `.ufo/waves/round-*/registration.md`).

## Does the append block pass the census on the mirror?

**The census run fails (exit 1), but zero of the 212 findings are attributable
to the append block.** Evidence:

1. All 205 E11 lines name paths that resolve in the real corpus (baseline exit
   0) — they fail only because the spec-limited mirror omits them.
2. None of the three append filenames (`idle-lock-chain-armed-r14`,
   `idle-lock-never-asked-r12`, `idle-lock-offered-in-the-bar-r15`) appears in
   any finding line (grep over the output: no match).
3. No registry row in `SOURCES.md` references any of the three filenames
   (grep over the mirrored `SOURCES.md`: no match). The validator has no
   orphan/unreferenced-file check, so the block is invisible to the census in
   both directions: it neither clears an E11 nor raises one.
4. The 7 W04 warnings are pre-existing on the real corpus (identical lines in
   the baseline run) and do not gate exit code.

Conclusion: on this mirror the census cannot distinguish the append block at
all — pass/fail signal for the block is nil; the exit-1 failure is entirely
mirror-incompleteness noise plus 7 pre-existing W04 warnings.

## Verbatim output

```
file	W04	S030 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
file	W04	S042 duplicate url wayland.freedesktop.org/extras.html across scopes
file	W04	S045 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
file	W04	S097 duplicate url raw.githubusercontent.com/basecamp/omarchy/v3.8.4/themes/matte-black/colors.toml across scopes
file	W04	S119 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Lib/imaplib.py across scopes
file	W04	S120 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst across scopes
file	W04	S121 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst across scopes
file	E11	S001 missing used-by corpus/lessons/round-12.md
file	E11	S002 missing used-by corpus/knowledge/window-rule-effects-getprop.md
file	E11	S003 missing used-by corpus/lessons/round-12.md
file	E11	S004 missing used-by corpus/lessons/round-12.md
file	E11	S005 missing used-by corpus/knowledge/wayland-protocol-boundaries-r13.md
file	E11	S013 missing used-by corpus/knowledge/config-drift-r12.md
file	E11	S014 missing used-by corpus/knowledge/config-drift-r12.md
file	E11	S015 missing used-by corpus/knowledge/config-drift-r12.md
file	E11	S016 missing used-by corpus/knowledge/window-rule-effects-getprop.md
file	E11	S017 missing used-by corpus/knowledge/window-rule-effects-getprop.md
file	E11	S017 missing used-by corpus/knowledge/hyprland-config-era-r12.md
file	E11	S017 missing used-by corpus/lessons/round-13.md
file	E11	S018 missing used-by corpus/knowledge/window-rule-effects-getprop.md
file	E11	S019 missing used-by corpus/knowledge/window-rule-effects-getprop.md
file	E11	S020 missing used-by corpus/knowledge/window-rule-effects-getprop.md
file	E11	S021 missing used-by corpus/knowledge/hyprland-config-era-r12.md
file	E11	S022 missing used-by corpus/knowledge/hyprland-config-era-r12.md
file	E11	S023 missing used-by corpus/knowledge/hyprland-config-era-r12.md
file	E11	S024 missing used-by corpus/knowledge/hyprland-config-era-r12.md
file	E11	S025 missing used-by corpus/knowledge/hyprland-config-era-r12.md
file	E11	S026 missing used-by corpus/knowledge/hyprland-config-era-r12.md
file	E11	S027 missing used-by corpus/knowledge/hyprland-config-era-r12.md
file	E11	S028 missing used-by corpus/knowledge/hyprland-config-era-r12.md
file	E11	S029 missing used-by corpus/knowledge/hyprland-config-era-r12.md
file	E11	S031 missing used-by corpus/knowledge/xdg-portal-routing-r12.md
file	E11	S032 missing used-by corpus/knowledge/xdg-portal-routing-r12.md
file	E11	S033 missing used-by corpus/knowledge/xdg-portal-routing-r12.md
file	E11	S034 missing used-by corpus/knowledge/xdg-portal-routing-r12.md
file	E11	S035 missing used-by corpus/knowledge/xdg-portal-routing-r12.md
file	E11	S037 missing used-by corpus/knowledge/xdg-portal-routing-r12.md
file	E11	S040 missing used-by corpus/knowledge/wayland-protocol-boundaries-r13.md
file	E11	S041 missing used-by corpus/knowledge/wayland-protocol-boundaries-r13.md
file	E11	S041 missing used-by corpus/knowledge/output-colour-boundaries-r14.md
file	E11	S042 missing used-by corpus/knowledge/wayland-protocol-boundaries-r13.md
file	E11	S043 missing used-by corpus/knowledge/wayland-protocol-boundaries-r13.md
file	E11	S044 missing used-by corpus/lessons/round-13.md
file	E11	S046 missing used-by corpus/knowledge/wayland-protocol-boundaries-r13.md
file	E11	S047 missing used-by corpus/knowledge/output-colour-boundaries-r14.md
file	E11	S048 missing used-by corpus/knowledge/output-colour-boundaries-r14.md
file	E11	S049 missing used-by corpus/knowledge/wayland-protocol-boundaries-r13.md
file	E11	S049 missing used-by corpus/lessons/round-14.md
file	E11	S050 missing used-by corpus/knowledge/output-colour-boundaries-r14.md
file	E11	S051 missing used-by corpus/knowledge/input-debugging-boundaries-r15.md
file	E11	S052 missing used-by corpus/knowledge/input-debugging-boundaries-r15.md
file	E11	S053 missing used-by corpus/knowledge/waybar-observation-boundaries-r16.md
file	E11	S054 missing used-by corpus/knowledge/waybar-observation-boundaries-r16.md
file	E11	S055 missing used-by corpus/lessons/round-16.md
file	E11	S056 missing used-by corpus/knowledge/terminal-route-r17.md
file	E11	S057 missing used-by corpus/knowledge/terminal-route-r17.md
file	E11	S058 missing used-by corpus/knowledge/terminal-route-r17.md
file	E11	S059 missing used-by corpus/knowledge/terminal-route-r17.md
file	E11	S060 missing used-by corpus/knowledge/terminal-route-r17.md
file	E11	S063 missing used-by corpus/knowledge/idle-lock-route-r17.md
file	E11	S064 missing used-by corpus/knowledge/idle-lock-route-r17.md
file	E11	S065 missing used-by corpus/knowledge/idle-lock-route-r17.md
file	E11	S066 missing used-by corpus/knowledge/idle-lock-route-r17.md
file	E11	S067 missing used-by corpus/knowledge/idle-lock-route-r17.md
file	E11	S068 missing used-by corpus/knowledge/idle-lock-route-r17.md
file	E11	S069 missing used-by corpus/knowledge/idle-lock-route-r17.md
file	E11	S071 missing used-by corpus/knowledge/terminal-route-r17.md
file	E11	S072 missing used-by corpus/knowledge/walker-route-r18.md
file	E11	S073 missing used-by corpus/knowledge/walker-route-r18.md
file	E11	S074 missing used-by corpus/knowledge/walker-route-r18.md
file	E11	S075 missing used-by corpus/knowledge/walker-route-r18.md
file	E11	S076 missing used-by corpus/knowledge/walker-route-r18.md
file	E11	S077 missing used-by corpus/knowledge/walker-route-r18.md
file	E11	S078 missing used-by corpus/knowledge/walker-route-r18.md
file	E11	S079 missing used-by corpus/knowledge/walker-route-r18.md
file	E11	S080 missing used-by corpus/knowledge/walker-route-r18.md
file	E11	S081 missing used-by corpus/knowledge/walker-route-r18.md
file	E11	S082 missing used-by corpus/knowledge/walker-route-r18.md
file	E11	S083 missing used-by corpus/knowledge/walker-route-r18.md
file	E11	S085 missing used-by corpus/knowledge/walker-route-r18.md
file	E11	S086 missing used-by corpus/knowledge/walker-route-r18.md
file	E11	S087 missing used-by corpus/knowledge/walker-route-r18.md
file	E11	S088 missing used-by corpus/knowledge/walker-route-r18.md
file	E11	S089 missing used-by corpus/knowledge/walker-route-r18.md
file	E11	S090 missing used-by corpus/knowledge/walker-route-r18.md
file	E11	S091 missing used-by corpus/knowledge/walker-route-r18.md
file	E11	S092 missing used-by corpus/knowledge/theme-route-r18.md
file	E11	S093 missing used-by corpus/knowledge/theme-route-r18.md
file	E11	S095 missing used-by corpus/knowledge/theme-route-r18.md
file	E11	S096 missing used-by corpus/knowledge/walker-deep.md
file	E11	S096 missing used-by corpus/knowledge/walker-deep-r9.md
file	E11	S096 missing used-by corpus/knowledge/walker-live-surface.md
file	E11	S096 missing used-by corpus/knowledge/remaining-planes-census.md
file	E11	S096 missing used-by corpus/knowledge/walker-route-r18.md
file	E11	S096 missing used-by tools/mado-verify.sh
file	E11	S096 missing used-by SKILL.md
file	E11	S097 missing used-by corpus/knowledge/theme-route-r18.md
file	E11	S098 missing used-by corpus/knowledge/walker-route-r18.md
file	E11	S099 missing used-by corpus/knowledge/tripwire-precision-r20.md
file	E11	S100 missing used-by corpus/knowledge/tripwire-precision-r20.md
file	E11	S101 missing used-by corpus/knowledge/tripwire-precision-r20.md
file	E11	S102 missing used-by corpus/knowledge/tripwire-precision-r20.md
file	E11	S103 missing used-by corpus/knowledge/tripwire-precision-r20.md
file	E11	S104 missing used-by corpus/knowledge/tripwire-precision-r20.md
file	E11	S105 missing used-by corpus/knowledge/tripwire-precision-r20.md
file	E11	S106 missing used-by corpus/knowledge/tripwire-precision-r20.md
file	E11	S107 missing used-by corpus/knowledge/tripwire-precision-r20.md
file	E11	S108 missing used-by corpus/knowledge/tripwire-precision-r20.md
file	E11	S109 missing used-by corpus/knowledge/tripwire-precision-r20.md
file	E11	S110 missing used-by corpus/knowledge/tripwire-precision-r20.md
file	E11	S111 missing used-by corpus/knowledge/tripwire-precision-r20.md
file	E11	S112 missing used-by corpus/knowledge/tripwire-precision-r20.md
file	E11	S113 missing used-by corpus/knowledge/tripwire-precision-r20.md
file	E11	S114 missing used-by corpus/knowledge/tripwire-precision-r20.md
file	E11	S115 missing used-by corpus/knowledge/tripwire-precision-r20.md
file	E11	S116 missing used-by corpus/lessons/round-21.md
file	E11	S116 missing used-by corpus/knowledge/tripwire-binding-boundaries-r21.md
file	E11	S117 missing used-by corpus/lessons/round-21.md
file	E11	S117 missing used-by corpus/knowledge/tripwire-binding-boundaries-r21.md
file	E11	S118 missing used-by corpus/lessons/round-21.md
file	E11	S118 missing used-by corpus/knowledge/tripwire-binding-boundaries-r21.md
file	E11	S119 missing used-by corpus/knowledge/tripwire-binding-boundaries-r21.md
file	E11	S119 missing used-by corpus/lessons/round-21.md
file	E11	S120 missing used-by corpus/knowledge/tripwire-binding-boundaries-r21.md
file	E11	S120 missing used-by corpus/lessons/round-21.md
file	E11	S121 missing used-by corpus/lessons/round-22.md
file	E11	S121 missing used-by corpus/knowledge/tripwire-lifetime-recovery-r22.md
file	E11	S122 missing used-by corpus/lessons/round-22.md
file	E11	S122 missing used-by corpus/knowledge/tripwire-lifetime-recovery-r22.md
file	E11	S123 missing used-by corpus/knowledge/terminal-trees-r23.md
file	E11	S124 missing used-by corpus/knowledge/terminal-trees-r23.md
file	E11	S125 missing used-by corpus/knowledge/terminal-trees-r23.md
file	E11	S126 missing used-by corpus/knowledge/terminal-trees-r23.md
file	E11	S127 missing used-by corpus/knowledge/terminal-trees-r23.md
file	E11	S128 missing used-by corpus/knowledge/terminal-trees-r23.md
file	E11	S129 missing used-by corpus/knowledge/terminal-trees-r23.md
file	E11	S130 missing used-by corpus/knowledge/terminal-trees-r23.md
file	E11	S131 missing used-by corpus/knowledge/terminal-trees-r23.md
file	E11	S133 missing used-by corpus/knowledge/terminal-trees-r23.md
file	E11	S134 missing used-by corpus/knowledge/terminal-trees-r23.md
file	E11	S135 missing used-by corpus/knowledge/terminal-trees-r23.md
file	E11	S136 missing used-by corpus/knowledge/terminal-trees-r23.md
file	E11	S137 missing used-by corpus/knowledge/terminal-trees-r23.md
file	E11	S138 missing used-by corpus/knowledge/terminal-trees-r23.md
file	E11	S139 missing used-by corpus/knowledge/terminal-trees-r23.md
file	E11	S140 missing used-by corpus/knowledge/terminal-trees-r23.md
file	E11	S141 missing used-by corpus/knowledge/terminal-trees-r23.md
file	E11	S142 missing used-by corpus/knowledge/terminal-trees-r23.md
file	E11	S143 missing used-by corpus/knowledge/terminal-trees-r23.md
file	E11	S144 missing used-by corpus/knowledge/terminal-trees-r23.md
file	E11	S145 missing used-by corpus/knowledge/terminal-trees-r23.md
file	E11	S146 missing used-by corpus/knowledge/terminal-trees-r23.md
file	E11	S147 missing used-by corpus/knowledge/terminal-trees-r23.md
file	E11	S148 missing used-by corpus/knowledge/terminal-trees-r23.md
file	E11	S149 missing used-by corpus/knowledge/terminal-trees-r23.md
file	E11	S150 missing used-by corpus/knowledge/terminal-trees-r23.md
file	E11	S151 missing used-by corpus/knowledge/terminal-trees-r23.md
file	E11	S152 missing used-by corpus/knowledge/terminal-trees-r23.md
file	E11	S153 missing used-by corpus/knowledge/rule-attribution-r24.md
file	E11	S154 missing used-by corpus/knowledge/rule-attribution-r24.md
file	E11	S155 missing used-by corpus/knowledge/rule-attribution-r24.md
file	E11	S156 missing used-by corpus/knowledge/rule-attribution-r24.md
file	E11	S157 missing used-by corpus/knowledge/rule-attribution-r24.md
file	E11	S158 missing used-by corpus/knowledge/rule-attribution-r24.md
file	E11	S158 missing used-by corpus/knowledge/animation-table-r26.md
file	E11	S158 missing used-by corpus/knowledge/workspace-rules-r27.md
file	E11	S159 missing used-by corpus/knowledge/rule-attribution-r24.md
file	E11	S160 missing used-by corpus/knowledge/rule-attribution-r24.md
file	E11	S162 missing used-by corpus/knowledge/rule-attribution-r24.md
file	E11	S162 missing used-by corpus/knowledge/bind-table-r25.md
file	E11	S162 missing used-by corpus/knowledge/animation-table-r26.md
file	E11	S162 missing used-by corpus/knowledge/workspace-rules-r27.md
file	E11	S163 missing used-by corpus/knowledge/rule-attribution-r24.md
file	E11	S164 missing used-by corpus/knowledge/rule-attribution-r24.md
file	E11	S165 missing used-by corpus/knowledge/rule-attribution-r24.md
file	E11	S166 missing used-by corpus/knowledge/rule-attribution-r24.md
file	E11	S167 missing used-by corpus/knowledge/rule-attribution-r24.md
file	E11	S167 missing used-by corpus/knowledge/bind-table-r25.md
file	E11	S168 missing used-by corpus/knowledge/rule-attribution-r24.md
file	E11	S169 missing used-by corpus/knowledge/bind-table-r25.md
file	E11	S170 missing used-by corpus/knowledge/bind-table-r25.md
file	E11	S171 missing used-by corpus/knowledge/bind-table-r25.md
file	E11	S172 missing used-by corpus/knowledge/bind-table-r25.md
file	E11	S173 missing used-by tools/mado-binds.py
file	E11	S174 missing used-by tools/mado-binds.py
file	E11	S175 missing used-by corpus/knowledge/animation-table-r26.md
file	E11	S176 missing used-by corpus/knowledge/animation-table-r26.md
file	E11	S177 missing used-by corpus/knowledge/animation-table-r26.md
file	E11	S178 missing used-by corpus/knowledge/workspace-rules-r27.md
file	E11	S178 missing used-by tools/mado-wsrules.py
file	E11	S179 missing used-by corpus/knowledge/workspace-rules-r27.md
file	E11	S179 missing used-by tools/mado-wsrules.py
file	E11	S180 missing used-by corpus/knowledge/workspace-rules-r27.md
file	E11	S180 missing used-by tools/mado-wsrules.py
file	E11	S181 missing used-by corpus/knowledge/workspace-rules-r27.md
file	E11	S181 missing used-by tools/mado-wsrules.py
file	E11	S182 missing used-by corpus/knowledge/workspace-rules-r27.md
file	E11	S182 missing used-by tools/mado-wsrules.py
file	E11	S183 missing used-by corpus/knowledge/mutation-testing-r28.md
file	E11	S184 missing used-by .ufo/waves/round-29/registration.md
file	E11	S184 missing used-by corpus/lessons/round-29.md
file	E11	S185 missing used-by quality/check-index.py
file	E11	S185 missing used-by .ufo/waves/round-30/registration.md
file	E11	S186 missing used-by corpus/knowledge/ipc-contract-r25.md
file	E11	S186 missing used-by corpus/knowledge/dispatcher-surface-and-request-grammar-r26.md
file	E11	S187 missing used-by corpus/knowledge/ipc-contract-r25.md
file	E11	S188 missing used-by corpus/knowledge/dispatcher-semantics-r25.md
file	E11	S188 missing used-by corpus/knowledge/dispatcher-surface-and-request-grammar-r26.md
file	E11	S189 missing used-by corpus/knowledge/ipc-contract-r25.md
file	E11	S196 missing used-by corpus/knowledge/dispatcher-surface-and-request-grammar-r26.md
file	E11	S201 missing used-by corpus/knowledge/waybar-module-text-route-r25.md
file	E11	S202 missing used-by corpus/knowledge/waybar-module-text-route-r25.md
```

`EXIT:1`
