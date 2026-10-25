# Quarantine verdicts — mado, round 41 (2026-10-25)

Seat `ExecQuarantineSlice` (assimilation item 10). Source register read-only, never edited:
`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`
(375 lines, sha256 `5afe1810a6c3d62f37987b575a954f5b1197daa23005d4bb2f1d982f64bad833`).

## 1. Slice derivation (verbatim command)

```sh
R=/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
awk -F'|' -v l='mado' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ \
  {print $4, $5}' "$R" > .ufo/waves/round-41/assimilation/quarantine-slice
```

**Row count: 13.** Output `assimilation/quarantine-slice` (sha256
`d9ea803d2433942dac094a14e9223be086ad460502163df7faf6e2509d9bb45d`), one line per row,
every line carrying an S-id (`awk '{ if ($1 !~ /^S[0-9][0-9][0-9]`?$/) print "NO-SID:", NR }'` → no output).

| family | ids | register cell |
|---|---|---|
| `payload-absent` (6) | S189, S195, S201, S205, S224, S228 | `` `payload-absent` `` |
| prose, never checked (7) | S199, S200, S209, S222, S223, S225, S235 | "could not be fetched" (S199, S200) / "named no locator" (S209, S222, S223, S225, S235) |

The register's own `## By lane` summary says `mado | 6` (register line 248) — it counts only the
`payload-absent` family; the awk catches both sections, so 13 is the derivable slice. The seven prose
rows carry a trailing backtick on the id (`S199\``) because the register's second table is malformed;
the ids are unchanged.

## 2. FOCUS-theme staged files scanned

Theme set per registration §Assimilation — the staged `focus-control-surfaces-r28`,
`focus-grab-protocol-live-on-host-r14`, `privileged-client-surface-r29`, the focus-grab r8–r15 series,
`compositor-focus-manipulation-literature-r26`, `wayland-input-security-literature-r8` — all under
`/home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge/` (12 files, read-only):

| file | sha256 (16) | file | sha256 (16) |
|---|---|---|---|
| `focus-control-surfaces-r28.md` | `14fe9341c73be200` | `focus-grab-mouse-target-r11.md` | `54b3a7d0a1ed0299` |
| `focus-grab-protocol-live-on-host-r14.md` | `8f42ebb1e4abe5eb` | `focus-grab-observed-semantics-r9.md` | `8909985a41e82487` |
| `privileged-client-surface-r29.md` | `36a41712189d32ba` | `focus-grab-seat-semantics-r8.md` | `ff9dc0d5cbb9e7e6` |
| `focus-grab-focus-selection-r10.md` | `e56f92043c912897` | `focus-grab-whitelist-admission-r12.md` | `2af0e12a7083b50d` |
| `focus-grab-has-no-client-here-r15.md` | `d3f69b1276deb15a` | `compositor-focus-manipulation-literature-r26.md` | `68f2614fd15be580` |
| `focus-grab-keyboard-routing-r13.md` | `a7ee0e435e77ed47` | `wayland-input-security-literature-r8.md` | `8dfdb117a1564886` |

Scan (id-level, 13 slice ids × 12 files):

```sh
for id in S189 S195 S201 S205 S224 S228 S199 S200 S209 S222 S223 S225 S235; do
  for f in $FOCUS_FILES; do grep -q "$id" "$f" && echo "$id $f:$(grep -n "$id" "$f" | cut -d: -f1 | tr '\n' ',')"; done; done
```

Output — **exactly one hit**:

```
S199 focus-control-surfaces-r28.md:69,
```

The staged files' cited ids are otherwise `S218, S227, S229, S230, S244, S273–S275, S278–S280,
S288, S293–S296, S306–S308, S313, S314, S317, S323–S325, S328–S332, S338` — none of them is a slice id.

## 3. Verdict per cited slice row

| row | cited at | register class cell | verdict | located quote | access |
|---|---|---|---|---|---|
| S199 | `focus-control-surfaces-r28.md:69` — "The round-2 paper (wave-2 row S199) measured focus hijacking on X11" | prose: "the cited source could not be fetched, so no quote was checked" | **`unverifiable`** (prose class, not fabrication) — and **not a citation of this row** (identity mismatch, §4) | none: the register carries no quote for this row, only the URL | 2026-10-25 |

**Totals: 1 cited slice row → `unverifiable` 1, adopt 0, refuse 0.** The other 12 slice rows are cited
by no FOCUS-theme staged file and get no verdict here.

Fetch evidence for the S199 row (register URL `https://blog.csdn.net/2301_76324845/article/details/149787804`):

| route | status | bytes | note |
|---|---|---|---|
| direct `curl` (UA: Mozilla/5.0) | **521** | 2 263 | reproduces the register's "could not be fetched" |
| `https://r.jina.ai/<url>` | 200 | 72 136 | page is readable through the reader proxy; title `【Arch-Linux,hyprland】常用配置-已实验成功指令大全（自用）（持续更新）`, published 2025-07-30 |

So the class cell is a fetch-method artifact, not a missing source. It stays `unverifiable` because the
register checked **no** quote for this row (there is nothing to locate), and the row is not the row the
focus file means. The page itself is substantive: the lane's own packaged anchor for the same URL
(`§ windowrules.conf 修改`, `lanes/mado/round2/KNOWLEDGE-PROPOSED.md:26`) resolves in the proxy text at
line 157 (`打开【~/.config/hypr/**windowrules.conf**】，找到代码`).

## 4. Why the S199 hit is an id-space collision, not a citation

- The focus file's S199 is a **paper**: `focus-control-surfaces-r28.md:69-74` says the round-2 paper
  "measured focus hijacking on X11" and speaks of "the paper's own X11 scope" — that is
  arXiv 2604.18860.
- The register's `mado | round2 | S199` cites a **CSDN blog post**, not a paper (register line 349);
  its packaged identity is `S216` (`lanes/mado/round2/SOURCES-PROPOSED.md:53`, same URL).
- The paper in the campaign's own numbering is `S218` (`lanes/mado/round2/SOURCES-PROPOSED.md:69`) and
  `S198` in `corpus-expansion-2/ScoutMado.md:26`; in the staged focus theme it is cited as `S218`
  (`compositor-focus-manipulation-literature-r26.md:7`), `S280`
  (`focus-grab-seat-semantics-r8.md:9`) and `S325` (`focus-grab-keyboard-routing-r13.md:12`).
- No staged id in the theme is `S199` as the paper: the "wave-2 row S199" label in
  `focus-control-surfaces-r28.md:69` matches no row in any numbering consulted (wave-2 staging ran
  S192–S199 with S198 = the paper and S199 = the omarchy idle producer,
  `corpus-expansion-2/ScoutMado.md:24-27`).

**Finding (attacks `focus-control-surfaces-r28.md:69`):** the staged entry cites the paper by a stale id.
The L1's re-grounded C2 entry must not carry "S199" as a paper row.

## 5. Adjacent hand-check — the one slice row whose *source* a focus file cites (S201)

Not an id-level hit, reported because it is the theme's only source overlap with the slice: the register's
`payload-absent` row **S201** (`https://arxiv.org/abs/2604.18860`) is the same URL the three focus files
above cite under `S218`/`S280`/`S325`. Re-opened 2026-10-25 by this seat.

| register quote (row S201) | in `/abs/2604.18860` | in `/html/2604.18860v1` | located anchor |
|---|---|---|---|
| "Desktop agents interact across disjoint applications, manage overlapping windows governed by X11/Wayland compositors" | **absent** (0 hits) | **present verbatim** | html §Introduction, sentence "…desktop environments present a strictly more complex and dangerous attack surface." |
| "notification overlays and X11 window focus hijacking --- can redirect agent actions with up to 100% success rates" | **absent** (0 hits) | **present** as `…dynamic UI manipulation — such as notification overlays and X11 window focus hijacking — can redirect agent actions with up to 100% success rates` | html §Conclusion (register form is the LaTeX `---` form; also present verbatim in `round8/fetch/arXiv-2604.18860.txt:429-431`) |

**Verdict for S201 as cited:** `refuse` — the register's cited source (`/abs/`) does not contain either
quote, which is the fabrication class by the rule. **But the quotes are not invented:** both are in the
paper's full text, so the defect is the anchor (`/abs/` vs `/html/`), not the content; re-anchoring makes
the row adoptable (same adjudication as round-32 `ExecQuarantineSlice.md:17` and round-34
`CritDupIdSpace.md:85-90`).

The focus files' own quotes of that source, checked in the same fetch:

| file:line | quote (<= 25 words) | source | verdict |
|---|---|---|---|
| `compositor-focus-manipulation-literature-r26.md:22` | "notification overlays and X11 window focus hijacking — can redirect agent actions with up to 100% success rates" | html §Conclusion (em-dash form; the entry splices it without "such as") | present |
| `compositor-focus-manipulation-literature-r26.md:26` | "the observation-to-action gap (mean 6.51 s on real OSWorld workloads)" | abs §Abstract | present |
| `compositor-focus-manipulation-literature-r26.md:31` | "Desktop agents interact across disjoint applications, manage overlapping windows governed by X11/Wayland compositors" | html §Introduction | present (not in abs — the entry's `§ Abstract` anchor is wrong for this one) |
| `focus-grab-seat-semantics-r8.md:60` | "100% action-redirection success rate" | abs §Abstract | present |
| `focus-grab-keyboard-routing-r13.md:69` | "characterize three concrete attack primitives: (A) Notification Overlay Hijack, (B) Window Focus Manipulation, and (C) Web DOM Injection" | abs §Abstract | present |

Machine check (script `w1/ExecQuarantineSlice/verify-quotes.py` greps this receipt's `QUOTE-CHECK` lines
against the retained bytes in `w1/ExecQuarantineSlice/sources/`, sha256
`06c1085529e30c2e…` html, `ab6d25a3d62a0b36…` abs, `d9b9ebe8e9727957…` CSDN-via-proxy):

```
QUOTE-CHECK|Q1|expect=present|src=html|Desktop agents interact across disjoint applications, manage overlapping windows governed by X11/Wayland compositors
QUOTE-CHECK|Q2|expect=present|src=html|notification overlays and X11 window focus hijacking — can redirect agent actions with up to 100% success rates
QUOTE-CHECK|Q3|expect=present|src=abs|the observation-to-action gap (mean 6.51 s on real OSWorld workloads)
QUOTE-CHECK|Q4|expect=present|src=abs|100% action-redirection success rate
QUOTE-CHECK|Q5|expect=present|src=abs|characterize three concrete attack primitives: (A) Notification Overlay Hijack, (B) Window Focus Manipulation, and (C) Web DOM Injection
QUOTE-CHECK|Q6|expect=present|src=tex|notification overlays and X11 window focus hijacking --- can redirect agent actions with up to 100% success rates
QUOTE-CHECK|N1|expect=absent|src=abs|Desktop agents interact across disjoint applications, manage overlapping windows governed by X11/Wayland compositors
QUOTE-CHECK|N2|expect=absent|src=abs|notification overlays and X11 window focus hijacking
```

Run (`python3 -I verify-quotes.py`, exit 0):

```
PASS Q1   present src=html found=True  Desktop agents interact across disjoint applications, manage overlapping
PASS Q2   present src=html found=True  notification overlays and X11 window focus hijacking — can redirect agen
PASS Q3   present src=abs  found=True  the observation-to-action gap (mean 6.51 s on real OSWorld workloads)
PASS Q4   present src=abs  found=True  100% action-redirection success rate
PASS Q5   present src=abs  found=True  characterize three concrete attack primitives: (A) Notification Overlay
PASS Q6   present src=tex  found=True  notification overlays and X11 window focus hijacking --- can redirect ag
PASS N1   absent  src=abs  found=False Desktop agents interact across disjoint applications, manage overlapping
PASS N2   absent  src=abs  found=False notification overlays and X11 window focus hijacking
QUOTE-CHECK checked=8 failed=0
```

URL-level cross-check of every slice-row source against the 12 theme files (the S201 overlap is the only one):

```
arxiv.org/abs/2604.18860      focus-grab-keyboard-routing-r13.md focus-grab-seat-semantics-r8.md compositor-focus-manipulation-literature-r26.md
EventManager.cpp (S189)       —
archlinux-cn (S195)           —
wiki.archlinux.org/api.php (S205) —
ai-usage/status.json (S224)   —
cn-export-hyprland.html (S228) —
blog.csdn.net (S199, S200)    —
```

## 6. What this attacks / supports

- **Attacks** `focus-control-surfaces-r28.md:69`: stale id "wave-2 row S199" for the arXiv paper; the
  paper is `S218`/`S280`/`S325` in the theme's own files and `S218` in the campaign's package.
- **Attacks** `compositor-focus-manipulation-literature-r26.md:31`: that quote is anchored to
  `§ Abstract` but exists only in the full text.
- **Supports** the register's `payload-absent` flag on `S201`: reproduced today (0 hits in `/abs/`).
- **Supports** the `unverifiable` disposition of `S199`: direct fetch still 521; the page exists behind
  the reader proxy, so the class is a fetch artifact.
- **Supports** the L1's refuse target `privileged-client-surface-r29` is untouched by this slice: its
  only cited id `S244` is not a slice row.
