# ExecLiveHost — C1 host receipt (round 43, w1)

STATUS: **complete**. Host receipt only (the C1 counter does not score it: `quality/counters/c1-r42-geometry.py`, docstring tail,
"the host receipt, `hyprctl clients -j` piped in, is reported, not scored"). No repository file was edited; everything below is under
`.ufo/waves/round-43/w1/ExecLiveHost/`.

## Files (all in `.ufo/waves/round-43/w1/ExecLiveHost/`)

| file | sha256 | what |
|---|---|---|
| `mado-geometry.py` | `e3c2e471505932f797a98ee2aa9ab1b04fc919f2140509282ef8472498135a99` | copy of the frozen reference `.ufo/waves/round-42/c1/ctl-ref-tool.py.txt` (byte-identical: same sha printed twice in the transcript) |
| `live-census.txt` | `f6aeb6388984f1608eb7fd7b98587733f1bb964e83d1c1a673c108622e305870` | **the receipt**: 404 lines, every command, its verbatim stdout/stderr and `exit=` |
| `source-census.txt` | `9e4cc3e42aa605d82978c9cf7b7ecc30678bc320e7e0a4da65bb93e0473d525a` | per-file census (also embedded as section 8 of `live-census.txt`) |
| `source-census.py` | `37aac93bbde87ccdfe957ca84c753d79d4b41fd0d3d0efe950b0670ddbc263b2` | `source =` closure walker + per-line reason classifier (asserts agreement with the tool) |
| `closure-list.py` | `f16d4b6885891fa44f30a6529bd6ded0cacd669fbb760823ce947824ecc22501` | prints the closure in source order (reuses the walker) |
| `run-live.sh` | `75ab1a04c88949ecdb4a00b942c509a00061c3bf532019cf4eba01715471eeb7` | regenerates `live-census.txt` end to end |
| `host-clients-live.json` | `6cdada1a687201ebc42f73c58da27137189d5cc2b5f419c512c3956bab95e06b` | the raw `hyprctl clients -j` dump captured at 2026-10-26T04:19:43-03:00 |
| `fx-agree.json` `8c6a4dc9…` / `fx-differ.json` `ddb5e9a4…` / `fx-tiled.json` `54d1dfbe…` / `fx-three.json` `48ee011e…` | | hand-made clients: gkeep 420×500 floating / 421×500 floating / 420×500 tiled / all three |
| `fx-tag-btop.json` `8ca3bcbb…` / `fx-steam.json` `61c276e0…` | | blind-spot probes (F8) |

## Commands (as recorded, `live-census.txt`)

1. `hyprctl version` — `Hyprland 0.56.2 built from branch v0.56.2 at commit efb50993780079460b0cbed1363e2166a2de1d9f clean ([gha] Nix: update inputs).`
   (the version line in the receipt is `HYPRCTL_VERSION_LINE:`; `Python 3.14.8`).
2. `python3 -I mado-geometry.py --selftest` → `MADO_GEOMETRY_SELFTEST: 73/73 passed`, exit 0.
3. three times: `hyprctl clients -j | python3 -I mado-geometry.py --clients - --rules ~/.config/hypr/gkeep.conf`.
4. the four fixtures, each `--clients fx-*.json --rules ~/.config/hypr/gkeep.conf`.
5. `hyprctl clients -j > host-clients-live.json`, then `cat host-clients-live.json | python3 -I mado-geometry.py --clients - --rules …gkeep.conf`.
6. one run with every file of the source closure as a separate `--rules` in source order, against `host-clients-live.json`.
7. `python3 -I source-census.py mado-geometry.py` — per-file counts + per-line reason, each unsupported line re-run alone and asserted.

`~/.config/hypr/gkeep.conf` sha256 `3726e488c0bf93028f1bba11017cf02d26da6dc3604362815bc4f3738b8e9949` — **equal to the S297 pin**
in `.ufo/waves/round-43/receipts/fetch-sha256.txt` (the pinned own-work receipt still equals the live host file).

## Findings

**F1 — the claim's command works and its live verdict is NO_MATCHING_CLIENT, rc 3, three times identically** (supports C1's
invocation; the fixture data it yields is empty). Verbatim, all three runs identical:

```
MADO_GEOM_RULE: n=1 file=1 effect=float arg=on class=^(org.omarchy.gkeep)$
MADO_GEOM_RULE: n=2 file=1 effect=size arg=420x500 class=^(org.omarchy.gkeep)$
MADO_GEOMETRY: rules=1 float_rules=1 other=1 unsupported=0 clients=4 matched=0 unmapped=0 agree=0 differ=0 tiled=0 badsize=0 verdict=NO_MATCHING_CLIENT
exit=3 (hyprctl exit=0)
```

`other=1` is `gkeep.conf:3` `windowrule = center on, match:class ^(org.omarchy.gkeep)$` (effect `center`) — the rule file is 4
lines (1 comment + 3 rules) and all three rules are classified (`residual=0` in the census).

**F2 — the live host has no gkeep window, so the claim's own command cannot reach AGREE/DIFFER today** (bounds C1's live value).
`host-clients-live.json` has 4 mapped clients, all tiled, all `[1720, 1414]`, none matching `^(org.omarchy.gkeep)$`:
`Alacritty`, `zcode`, `grok-bot`, `chromium` (the reduced view is printed in section 4 of the transcript). `clients=4 matched=0`.
The same four clients, with **identical addresses** (`0x55836b6e94f0` Alacritty, `0x55836cee37d0` zcode, `0x55836ce60d90` grok-bot,
`0x55836cff7280` chromium) and the same `[1720, 1414]` sizes, are in the pinned S298 receipt (`fetch/host-clients-r43.json`, sha `21db902e…`) —
that file is a *reduced projection* (class/size/floating/mapped/at/monitor), while this seat's `host-clients-live.json` (`6cdada1a…`) is the raw
full dump, so the two shas differ by construction and are not meant to match; the client set is unchanged between the 04:11 pin and this 04:19 dump.

**F3 — the three fixtures behave exactly as C1's contract says** (supports the tool's verdict mapping on the real host rule text):
AGREE `size=420x500 want=420x500 verdict=AGREE` `agree=1 … verdict=OK` exit 0; DIFFER `size=421x500 want=420x500 verdict=DIFFER`
`differ=1 … verdict=DIFFER` exit 1; TILED `floating=false size=420x500 … verdict=TILED` `tiled=1 … verdict=OK` exit 0.
The combined `fx-three.json` gives `clients=3 matched=3 … agree=1 differ=1 tiled=1 … verdict=DIFFER`, exit 1.

**F4 — how much of the host rule set the tool can read.** `hyprland.conf` itself carries 0 rule lines; its `source =` closure is
**40 files** (all present, no symlink/dir misses), of which **17 files carry 77 `windowrule` lines**. The tool classifies
**77/77** (`residual=0` in every file) as:

| bucket | count | share of 77 |
|---|---|---|
| `rules=` (supported **size**) | **3** | 3.9 % |
| `float_rules=` (supported **float**) | 6 | 7.8 % |
| `other=` (effect not size/float) | **61** | 79.2 % |
| `unsupported=` | **7** | 9.1 % |

**F5 — the size-rule universe is 7 literal `size W H` lines** (`grep -hE 'windowrule[ \t]*=' <closure> | grep -cE '=[ \t]*size[ \t]+[0-9]{1,5}[ \t]+[0-9]{1,5}'` → `7`); the tool **SUPPORTS 3** and counts **4 unsupported**:

| rule (locator) | tool | reason (docstring condition) |
|---|---|---|
| `.config/hypr/gkeep.conf:4` `size 420 500, match:class ^(org.omarchy.gkeep)$` | supported | — (`arg=420x500`) |
| `.config/hypr/ai-usage.conf:5` `size 875 600, match:class ^(org.omarchy.ai-usage)$` | supported | — |
| `omarchy/default/hypr/apps/localsend.conf:4` `size 1100 700, match:class localsend` | supported | — |
| `omarchy/default/hypr/apps/system.conf:4` `size 875 600, match:tag floating-window` | **unsupported** | field 1 is `match:tag`, not `match:class` (needs a rule→tag graph the tool does not build) |
| `omarchy/default/hypr/apps/pip.conf:6` `size 600 338, match:tag pip` | **unsupported** | same: `match:tag` |
| `omarchy/default/hypr/apps/steam.conf:6` `size 1100 700, match:class steam, match:title Steam` | **unsupported** | 3 fields (docstring: exactly two — one `match:class` and no title/pin/float conjunction) |
| `omarchy/default/hypr/apps/steam.conf:7` `size 460 800, match:class steam, match:title Friends List` | **unsupported** | same: 3 fields |

So **3 of 7 (42.9 %)** of the host's size rules are usable by the tool, and every one of the 4 unusable ones would be needed to
reach a real floating window on this host (they match by tag or by title, not by class alone). The other 3 unsupported lines are
float rules with the same causes (`system.conf:2` `float on, match:tag floating-window`; `pip.conf:4` `float on, match:tag pip`;
`webcam-overlay.conf:2` `float on, match:title WebcamOverlay`) — 4 size + 3 float = `unsupported=7`.

**F6 — the docstring's other unsupported categories do not occur on this host** (so the census's `unsupported` set is entirely
tag/title): `grep -rnE '(size[ \t]+[0-9.]+%|size[ \t]+\()' <closure>` → exit 1, no percentage or expression size;
`grep -rn 'initial_class' <closure>` → exit 1, none; `grep -rn 'negative:' <closure>` → exit 1, none.
Near-miss word check: `windowrule = border_size 0, match:tag pip` (`apps/pip.conf:8`) is effect `border_size` → correctly `other`,
not a size rule. One commented-out rule line exists (`~/.config/hypr/hyprland.conf:26`, `# windowrule = workspace 5, match:class qemu`,
effect `workspace`) and is ignored by the tool (not counted anywhere), as the contract says.

**F7 — no host client is matched by any supported size rule even with the whole closure loaded** (the live dump through section 5):
`rules=3 float_rules=6 other=61 unsupported=7 clients=4 matched=0 … verdict=NO_MATCHING_CLIENT`, exit 3. Support rules that *do* fire
are printed: `file=19` ai-usage, `file=20` gkeep, `file=28` localsend, `file=32` steam, `file=35` `org.gnome.Calculator` and
`org.omarchy.screensaver` — i.e. the supported-rule output is exercised on the real files even though no client matches.

**F8 — two demonstrated blind spots of the read, both *by design* and already declared as residuals of PRED-C1** (reported, not
scored; they tell the L1 what a green counter does *not* mean on this host). (a) `fx-tag-btop.json` — class `org.omarchy.btop`,
875×600 floating, which is exactly what `system.conf:4` asks for via tag `floating-window` — yields `matched=0`,
`verdict=NO_MATCHING_CLIENT`, exit 3: the tool cannot see the tag rule, so a *correct* compositor outcome reads as "no rule".
(b) `fx-steam.json` — class `steam`, 1100×700 floating: the supported float rule `n=7 file=32 effect=float arg=on class=steam` fires
as `float_rule`, but both size rules for `steam` are title-constrained and unsupported, so the client is **not** MATCHED —
`matched=0`, `verdict=NO_MATCHING_CLIENT`, not DIFFER.

**F9 — the bytes the L1 already ran are the same bytes as the reference** (observation, not a correctness claim about the build):
`sha256sum tools/mado-geometry.py` at this seat gives `e3c2e471505932f797a98ee2aa9ab1b04fc919f2140509282ef8472498135a99` — the reference's
sha and this seat's copy sha, and the sha `.ufo/waves/round-43/receipts/live-geometry-host.txt` records at 04:17. So that L1 receipt's output
line is reproducible from this seat's copy, byte for byte. This seat did not run the counter and did not otherwise use the build's tool.

## Risks / limits of this receipt

- One sample in time, read-only, host session untouched: only `hyprctl version` and `hyprctl clients -j` were issued (both are read
  verbs); no `dispatch`, `keyword`, `reload`, `setprop`, `batch`, no socket of my own, no compositor oracle.
- The closure is *my* implementation of `source =` following (tilde expansion, `glob`, dedup by `realpath`, breadth-first in file
  order). Hyprland's own source semantics could differ on paths it refuses; every path it resolved here exists and is regular, and the
  closure reproduces `hyprland.conf:4-32` plus the nested `apps.conf`/`theme` sources. A file in `~/.config/hypr/` that no `source`
  names is *not* in the census — e.g. `hyprland.conf.bak.1792267376`, which also carries the commented rule line.
- The 3 supported size rules' *values* are read textually; whether Hyprland applied them to a live gkeep window is not observable
  here (no gkeep window). That stays the C1 residual: the counter does not score it.
- The reason classifier in `source-census.py` is a model of the docstring; it is not trusted on its own — every non-supported line was
  re-run alone through the tool and asserted to land in the same bucket (`CLASSIFIER_AGREEMENT: 68/68 disagree=0`, 68 = 61 `other` +
  7 `unsupported`; the 9 supported lines are pinned by the per-file `rules=`/`float_rules=` sums).
- Nothing here is a build/lint/test gate (not run, per wave rules), and no repository file was modified.

## Cleanup / tooling

- No tool installed, no package transaction, no `pacman`.
- No subagent/labrat spawned (not needed).
- Scratch `/fast/scratch/hyaku/mado-r43/ExecLiveHost/` was created per the operator directive and left empty (0 bytes) — all work
  happened in the seat directory; the directory is removed before yield. The `__pycache__/` that importing `source-census.py` created
  is removed too (`live-census.txt` was produced with it absent from the cited artefacts).
