# MadoR19.AtkPtrConfigHealthReportR3 — partial

Attack on the round-19 `## Freshness pointer (round 19, 2026-10-20)` block,
`corpus/knowledge/config-health-report-r3.md:1007-1013`, tip `01b8094`, baseline `9c54c56`.
Verdict: **partial**. The block's load-bearing claims hold — no pre-existing byte was
rewritten, no live/runtime 2.17.2 fact is claimed, and the one cited S-row supports every
sentence it is attached to. Two sentences are nonetheless inaccurate: an explicit
"not re-measured this round" (falsified by the round's own w1 delta seat and by this
seat's re-hash), and a misattributed measurement window. Both err in the conservative
direction; neither changes a pinned value.

## Attack (a) — were pre-existing bytes changed?

No. One hunk, and it is the append:

```text
$ git -C /home/vgpnk/Projects/shokunin/mado-shokunin diff 9c54c56 01b8094 -- \
    corpus/knowledge/config-health-report-r3.md | grep -c '^@@'
1
$ git -C … diff --stat 9c54c56 01b8094 -- corpus/knowledge/config-health-report-r3.md
 corpus/knowledge/config-health-report-r3.md | 9 ++++++++-
 1 file changed, 8 insertions(+), 1 deletion(-)
```

The single hunk is `@@ -1003,4 +1003,11 @@`. The "deletion" is the old final line
having no trailing newline, re-emitted with one as part of the append:

```text
$ git show 9c54c56:… | wc -l -c          → 1005 62249   (last byte '.' — no LF)
$ git show 01b8094:… | wc -l -c          → 1013 63705
$ sha256sum /tmp/base_chr3.md /tmp/tip_chr3.md
acf59f9b06c63cec1ee1f15b97981ec5f55765bc6e386c73f5f3c5392e8fe5e9  base
7432f1dd245fca72230c249b61f90a6813bc3944b4f50561a24634bd2d3cde23  tip
$ cmp -n 62249 /tmp/base_chr3.md /tmp/tip_chr3.md && echo PREFIX_IDENTICAL
PREFIX_IDENTICAL
```

The worktree file equals the commit (`sha256sum corpus/knowledge/config-health-report-r3.md`
= `7432f1dd…`, same as `git show 01b8094:… | sha256sum`; `git status --porcelain` clean for
this path). There is **no head `source:` line in this note at either revision**
(`grep -n '^source:' corpus/knowledge/config-health-report-r3.md` → no output), so the
walker-route-r18/theme-route-r18 `source:` swap has no counterpart here; nothing was
expected to change except the append. (a) holds.

## Attack (b) — live/runtime facts or unearned "re-verified"?

No live 2.17.2 fact is asserted. The two runtime-adjacent statements are hedged at the
point of use:

- `:1010` service state "Main PID 1808 from boot" is called "may no longer be current"
  after the hooks at `/var/log/pacman.log:3062` and `:3123`; "current PID is `[UNK]`".
  The hook lines exist (see (d)) and S090's own limits column ("a log line is not a
  running-binary fact") is respected — no current-process value is claimed.
- `:1011` "What walker 2.17.2 does with these bytes is `[UNK]`"; `:1013` "behaviour of the
  2.17.2 binary stays [UNK]".

The one sentence that is false is the opposite of an overclaim — a provenance
**understatement**:

- `:1011` "…dated 2026-10-14 and **not re-measured this round**: user walker config and
  its sha, line count and size (lines 242-243, 645)…". The round's own w1 seat re-measured
  that file on 2026-10-20:
  `.ufo/waves/round-19/w1/reports/DeltaWalkerConfig.md:144-146` —
  "`~/.config/walker/config.toml` re-measured: 49 L / 1,336 B /
  `fecf71fa4253803e…` … identical". This seat re-hashed it again today with the same
  result (below). So "not re-measured this round" is false as written. The pinned value
  is still true; only the freshness claim is wrong (conservative direction, not a
  dangerous overclaim).
  The same bullet's theme set was also listed as unchanged this round at
  `DeltaWalkerConfig.md:150-152` and re-hashes identically (below).

No sentence "calls something re-verified" without a round-19 hash: the block only uses
"not re-asserted" and "not re-measured" language. (b): no overclaim; one false
non-measurement sentence.

## Attack (c) — are the cited line numbers correct?

All cited numbers exist and point at the claimed topic. Values at every prose anchor are
the ones the block attributes to them:

| Cited | Content at tip | Verdict |
|---|---|---|
| `:3` | `Probe window: 2026-10-14 14:40–14:48 UTC` | date correct; **window misapplied** (see below) |
| `:242-243` | user config 49 L / 1,336 B `fecf71fa4253803e` | correct |
| `:243-244` | autostart sha `5cb9874eedbcb32c`, 138 B, byte-identical to stock | correct |
| `:245-246` | service "Main PID 1808 from boot" | correct |
| `:249` | "(walker --help = launch flags only)" | correct |
| `:252-255` | launch path / keybindings | correct |
| `:270` | theme `walker.css` 6 L / 191 B `f44cb450…` | correct |
| `:645` | `.config/walker/config.toml fecf71fa… 1336 49` | correct |
| `:657` | `.config/autostart/walker.desktop 5cb9874e… 138 7` | correct |
| `:896` | service-state **recipe**, comment `active/generated; active/enabled` | topic anchor; the quoted PID is not on this line |
| `:900` | `waybar --version; walker --version; … # v0.15.0 / 2.17.0 / 0.3.2 / v0.9.6` | correct |
| `:902` | command-presence **recipe**; comment concerns terminal emulators | topic anchor |
| `:915-916` | round-4 **recipes**; expected values in comments (`:15 → 644`, `121/1243; 156/6488`) | values present; the measured prose is `:247-248` |
| `:951-953` | K2 kit receipt, 16:21/16:24 UTC | correct |

Two precision defects:

1. `:1009` "measured in the 2026-10-14 probe window of line 3 and the round-4 kit at
   lines 951-953". Line 3's window is **14:40–14:48 UTC**; the round-4 kit that carries
   line 900 declares itself "Appended 2026-10-14 by MADO-R4-1 (validation probes
   16:21–16:24 UTC)" at `:598` and was run at **16:07 UTC** (K1, `:947`) and
   **16:21/16:24 UTC** (K2, `:951`). The calendar date is right, the window attribution
   is not.
2. `:1013` "not re-measured live this round" is true; `:1010`/`:1011` cite recipes
   (`:896`, `:915-916`) alongside prose anchors for the same topics. No pinned number is
   wrong, but a reader checking "is this quote at this line" finds it one line-range away.

No wrong number, no dangling line. (c): correct as topic anchors, imprecise in the two
places above.

## Attack (d) — does every cited S### support its sentence?

Only **S090** is cited (`:1009`, `:1010`).

```text
$ sed -n '102p' corpus/SOURCES.md
| S090 | host /var/log/pacman.log (walker and elephant upgrade lines) | code | A | … |
  lines 1943 (walker 2.16.2-1 -> 2.17.0-1, 2026-10-11),
  2929 (walker 2.17.0-1 -> 2.17.2-1, 2026-10-20T09:16:46-0300),
  3062 and 3123 (walker-restart.hook), 3095 (elephant …) |
  host package versions match tags v2.17.2 and v2.22.1; a log line is not a running-binary fact
```

Every line number the note cites is in the row, and every line number was re-read at the
real path:

```text
$ grep -n 'walker (2.17.0-1 -> 2.17.2-1)\|walker (2.16.2-1 -> 2.17.0-1)\|walker-restart.hook' /var/log/pacman.log
1943:[2026-10-11T16:14:39-0300] … upgraded walker (2.16.2-1 -> 2.17.0-1)
2034:[2026-10-11T16:16:37-0300] … running 'walker-restart.hook'...
2929:[2026-10-20T09:16:46-0300] … upgraded walker (2.17.0-1 -> 2.17.2-1)
3062:[2026-10-20T09:18:25-0300] … running 'walker-restart.hook'...
3123:[2026-10-20T09:31:04-0300] … running 'walker-restart.hook'...
```

S090 supports both sentences in the sense the row defines: package/version state from the
transaction log. The block does **not** use S090 for a running-binary fact, which is the
row's stated limit. `:1011`'s non-S citation, `walker-route-r18.md § Unexercised behavior`,
exists (`corpus/knowledge/walker-route-r18.md:285`) and contains exactly the negative class
cited ("Rendered output, the theme resolution order … no launcher was opened"; running
2.17.2 process `[UNK]`). (d) holds for every cited row.

Completeness note, not a false citation: S096 (host walker 2.17.2 bytes) now exists at
`corpus/SOURCES.md:108` and was absent at the baseline (`git show 9c54c56:corpus/SOURCES.md
| grep -n S096` → empty; the w1 seat recorded that in
`.ufo/waves/round-19/w1/reports/PtrConfigHealthReportR3.md`). The pointer cites only S090;
the sentence it writes ("the host package moved") is a log fact, so S096 is not required
for its truth, but the block could now carry the stronger binary binding and does not.

## Cross-check against what actually changed 2.17.0→2.17.2

From w1 `DeltaWalkerConfig.md` §2 and `DeltaWalkerCli.md` §3-§5: the delta is four
*default-config* rows (`blur_corner_radius=20`, `[niri]`, desktopapps `ctrl e = edit`,
clipboard remove → `SimpleDelete`), a version literal at 856,302, and moved artifact pins;
the 23 CLI flag registrations and the 838-byte description run are byte-identical, the
`--version` print path is unchanged, and stock service behaviour is unchanged (`[niri]`
defaults false/empty). This note asserts none of the four changed defaults and none of the
moved artifact pins; its only walker-version content is the line-900 expectation, the help
statement, the PID, and the user/theme bytes the pointer classifies. Independent censuses:

```text
$ grep -n '2\.17' corpus/knowledge/config-health-report-r3.md
900:… # v0.15.0 / 2.17.0 / 0.3.2 / v0.9.6
1009:… pointer sentence …
$ grep -n '298\|13,220\|/etc/xdg/walker\|packaged' corpus/knowledge/config-health-report-r3.md
(no output)
```

So the note carries **no packaged-default pin** (the 298 L / 13,220 B values live in other
notes), and line 900 is indeed the only walker version pin. The pointer's classification is
materially complete for this note's walker claims; w1's delta does not falsify any value it
classifies.

Independent re-hash of the "version-independent" set (host files, bytes only):

```text
fecf71fa4253803e4864bd0e890ad54cfda2233e07ed1c337b3449b7303d1787  ~/.config/walker/config.toml        49 L / 1,336 B
5cb9874eedbcb32c7b121ea60f6433f881499247cac7e6473a9a93adeebc3aa7  ~/.config/autostart/walker.desktop  7 L / 138 B
481267af0e89a475c851de82692176b4b496045e41081fa94eec0fbaf32500b0  …/omarchy-default/style.css         121 L / 1,243 B
dbb6bbbe74be894a0f545c91a08e5ee007b3bc8f72a3f07af3fe309bf49e0261  …/omarchy-default/layout.xml        156 L / 6,488 B
```

All four match the note's pins (`:242-243`, `:645`, `:657`, `:270`, `:916`); the block's
"Version-independent" tag is correct, and its "not re-measured this round" sentence is the
only thing contradicted by this re-hash.

## Findings

| # | Severity | Finding | Evidence |
|---|---|---|---|
| 1 | minor, real | "not re-measured this round" is false for the user walker config (and theme set): w1 re-measured on 2026-10-20, same values; w2 re-hashed, same values. Conservative underclaim, no wrong value. | `config-health-report-r3.md:1011`; `DeltaWalkerConfig.md:144-146`, `:150-152`; w2 hashes above |
| 2 | minor, real | line 900 is attributed to line 3's probe window (14:40–14:48 UTC), but the kit that carries it declares probes at 16:21–16:24 UTC and ran 16:07 / 16:21 / 16:24 UTC. Date right, window wrong. | `:1009`; `:3`; `:598`; `:947`; `:951` |
| 3 | cosmetic | `:1010` cites `:896` for the "Main PID 1808" quote; `:1011` cites `:915-916` for theme values. Both are reproduction recipes; the measured prose is `:245-246` and `:247-248`. Values match the recipe comments. | `:896`, `:915-916`, `:245-246`, `:247-248` |
| 4 | coverage note | Pre-existing live-state row `:76` ("walker config/service/theme \| equal; service active; …") is not classified by the pointer. It is not introduced by the append and remains plausible, but a reader treating the pointer as the complete list of walker live claims would miss it. | `:76`; `:1010` |
| 5 | no issue | No live/runtime 2.17.2 claim; PID and behaviour are `[UNK]`; S090's running-binary limit respected; S090's four cited log lines all exist. | `:1010-1013`; `/var/log/pacman.log:1943,2929,3062,3123`; `corpus/SOURCES.md:102` |

## Answer to the four questions

- (a) **Holds.** No pre-existing byte changed; base is a byte-prefix of tip; the only
  delete/add pair is the unterminated last line re-emitted with LF. No head `source:`
  token exists in this note, so no swap applied.
- (b) **No overclaim, one false underclaim.** Nothing live is claimed about 2.17.2 and
  nothing is called re-verified without a hash; the opposite — `:1011` says "not
  re-measured this round" about bytes w1 did re-measure.
- (c) **Mostly correct; two imprecisions.** All line numbers resolve, all quoted values are
  at or adjacent to the cited lines; the probe-window attribution (`:1009`) and the
  recipe-vs-prose anchors (`:896`, `:915-916`) are loose.
- (d) **Holds.** Every cited S-row (S090) supports its sentence under the row's own limit;
  `walker-route-r18.md:285` supports the `[UNK]` pointer. S096 now exists and is not cited;
  that is a strengthening gap, not a false citation.

## Limits

- Host pause respected: no walker, pacman, systemctl, journalctl, busctl, omarchy or
  compositor command; host data read as file bytes (`sha256sum`, `wc`, `stat`, `grep`
  on `/var/log/pacman.log`). Nothing under `~/.config/omarchy` was opened or hashed.
- Whether the 2026-10-14 `walker --version` output was actually captured (as opposed to
  the expectation comment at `:900`) is not recorded anywhere in the note: `[UNK]`, so
  "measured" in `:1009` is [INFERENCE] from the kit's run receipts.
- The 2026-10-14 byte values were not re-derived from history; only today's host bytes and
  the round-19 w1 reports were compared. The pointer's dated values are consistent with
  both.
- w1 `DeltaWalkerConfig.md`/`DeltaWalkerCli.md` read as reports, not re-fetched upstream;
  the 2.17.0→2.17.2 delta used here is their observed content (their fetches carry their
  own receipts).

## Installs

none
