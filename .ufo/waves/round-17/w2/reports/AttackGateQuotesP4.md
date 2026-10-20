# AttackGateQuotesP4 — § Gate rows S056-S062: quotes at anchors, word counts, digests, opened-vs-snippet

Seat: `MadoR17.AttackGateQuotesP4` (reviewer, leaf; no subagents dispatched).
Date: 2026-10-20. Lane root `/home/vgpnk/Projects/shokunin/mado-shokunin`,
lane HEAD `988b858bd6049bc709807534fd725c05264f7e60` (working tree clean at
review start: only untracked wave files; it diverged later — see residual risk).
Item: verify the P4 gate lines S056-S062 in
`corpus/lessons/round-17.md` § Gate and decide the S061/S062
"genuinely opened, not snippets" claim.

Installs this round: **none**. No pacman/yay/paru/sudo/systemctl/hyprctl/probe of
any kind was run; host config files and `/usr/share` were read as file bytes only.
Remote reads were `curl` raw bytes into `/tmp/p4g`; `git` was used read-only
(`show`, `log`, `ls-tree`, `ls-files`, `cat-file -e`). No lane file edited except
this report.

## Verdict

The attack on quote fidelity and on digest accuracy **fails**: every quoted
string is verbatim at its anchor (modulo line-wrap whitespace), and every digest
is the SHA-256 of the bytes actually hashed. The attack on the
"opened, not snippets" claim for S061/S062 **also fails**: both documents were
fetched whole, and their recorded digests reproduce byte-for-byte.

What does fall out (concrete, small): **two word-count claims are wrong**
(S056, S061), and **three anchors are inexact** — S061's printed URL cannot
produce its digest or its `line 24`; S058's range is one line wider than the
quoted sentence; S059's quote truncates inside the `--dir=` token without an
ellipsis. One adjacent SOURCES defect: S059's `alacritty.toml:1-27` label
conflicts with its own whole-file digest.

## Method (reproducible)

- Abbreviated `curl` fetches into `/tmp/p4g`; `sha256sum`; `wc -c/-l`;
  `grep -n` for the exact quote; `awk 'NR==n{print NF}'` for line token counts;
  `wc -w` on the quoted string; `python3` deterministic HTML→text extraction
  (`strip script/style`, tags→newlines, `html.unescape`, drop blank lines) for
  S062 and for the S061 rendered-page control.
- Tag-pinned URLs in the table were fetched at the printed tag
  (`v0.14.3`, `v0.17.0`), so these are the bytes the row cites.
- Anchors checked both ways: (a) exact substring of the whole document,
  (b) exact substring of the stated line/range after whitespace normalization.

## Per-row result

| row | anchor | quote verbatim | words claimed → measured | digest claimed → measured | verdict |
|---|---|---|---|---|---|
| S056 | README.md:166 (v0.14.3) | yes (prefix after `- `) | 12 → **11** (12 only counting the bullet `-`) | `c7a1a8bb…a9d40` → exact, 14,762 B | count defect |
| S057 | xdg-terminal-exec:106 | yes | 4 → 4 | `89f2be9a…127ac` → exact, 44,020 B | clean |
| S058 | alacritty.5.scd:35-37 | yes (join across wrap) | 16 → 16 | `e444fa45…0a4107` → exact, 28,787 B | range one line wide |
| S059 | bindings.conf:2 | yes (mid-token prefix) | 10 → 10 | all three exact (below) | unmarked elision |
| S060 | system list:3 | yes | 3 → 3 | `a2b5bf69…ef034` → exact, 1,053 B; upstream v0.14.3 list same digest/size | clean |
| S061 | wiki "line 24" | yes (prefix of wikitext line 24) | 10 → **8** | `c39c563d…4600bb` → exact for `?action=raw` (8,275 B), **not** for the printed URL | count + URL/line binding defects |
| S062 | linuxjunkies "line 247" | yes (prefix, extracted text) | 7 → 7 | `08608a0b…bec2c653` → exact, 90,051 B | clean except anchor basis unstated |

Full digests measured (host files by bytes, remote by raw response):

- S059 `~/.config/hypr/bindings.conf` 2,879 B
  `e574a1ed08535e31deeafe2a26432c6862bb101e8c45d5a6b3f997d7dc810581`;
  `~/.config/xdg-terminals.list` 127 B
  `d035da571a6bfc7d626d4a88846ea86a8adb6f6662f1f8b4abe2330e53ceb71b`;
  `~/.config/alacritty/alacritty.toml` 876 B
  `695301c86577c808a94a01a4227bfaab3dbbe9a394a9954032f6173adec824f8`.
  Import target `~/.config/omarchy/current/theme/alacritty.toml` 772 B
  `8c3d1457c09d32e83367ac946ff6e85f6bda334c302587a043bef7dc7ac09139`;
  `.bak.20261003-190229` 873 B
  `ea3e0fa094ca2c763d284dbba39730ee3638ed20c97da6e69adb45f77ee1207a`.
- S061 printed URL `https://wiki.archlinux.org/title/Alacritty` as fetched
  2026-10-20: **60,206 B**, 1,012 lines,
  `bba2e98c84b178723956c61dfe555675666506d23da8208434ac14f74f274037`.
  `https://wiki.archlinux.org/index.php?title=Alacritty&action=raw`: **8,275 B**,
  179 lines, `c39c563d74f2ff7c35bd7133a438804f6314c10434e3f94ad289b7c28c4600bb`
  (equals the row; equals seat-report R1, `w1/reports/SrcTerminalAlternates.md:36`).
- S062 `https://linuxjunkies.org/guides/configure-alacritty`: **90,051 B**,
  145 raw lines, `08608a0bafb9bb7b4cea2a7970dbc2f926946976c7f9eb23a1d30249bec2c653`
  (equals the row; equals seat-report R7, `SrcTerminalAlternates.md:42`).
  Deterministic extraction: **345 non-blank lines** (matches the seat's stated
  345); quote at extracted line **247**, inside a visible FAQ `<dd>`.

## Findings, by severity

### F1 (medium) — S061's printed URL does not carry its digest or its `line 24`

The row's triple is `(https://wiki.archlinux.org/title/Alacritty, line 24,
c39c563d…4600bb)`. That URL returns rendered HTML — different bytes (60,206 B,
`bba2e98c…` today), a different line basis (1,012 lines; the sentence extracts at
line 128; raw HTML line 24 is `<body class="skin--responsive …">`). The digest is
of `index.php?title=Alacritty&action=raw`, which the gate row does not print;
only the seat report does (`SrcTerminalAlternates.md:36`). A reader who follows
the printed row cannot reproduce either the digest or the line. The same family
applies to S062: raw HTML is 145 lines and the phrase sits on raw lines 1 and
146; `line 247` exists only in extracted text, and no extraction convention is
stated. Both quotes and both digests are correct for their respective bases —
this is a citation-binding defect, not a false quote or a wrong hash.

### F2 (low) — S061 word count is 8, not 10

`printf '%s\n' 'Versions before 0.13.0 used a YAML configuration file.' | wc -w`
→ **8**. The raw wikitext line 24 has 27 tokens, so 10 matches neither the
quoted sentence nor the line. Origin: `SrcTerminalAlternates.md:77` says
"(line 24, 10 words)"; the gate inherited it. The ≤25-word cap is not breached.
(For contrast the gate corrected the seat's S062 count from 9 to the correct 7.)

### F3 (low) — S056 word count is 11 as quoted, not 12

`… | wc -w` → **11**. The full README line 166 has 12 tokens because it begins
with the markdown bullet `- `, which is outside the quotation marks; the quoted
text starts at `Each`. Under the basis used by the other rows (words in the
quoted text), the count is 11. Origin: `drafts/NoteTerminal-rows.md:49` already
said 12. The ≤25-word cap is not breached.

### F4 (low) — S058's range `35-37` is one line wider than the quote

Line 35: `Imports are loaded in order, … with the importing`; line 36:
`file being loaded last. If a field is already present …`; line 37:
`it will be replaced.` The quoted sentence ends on line 36; line 37 belongs to
the next sentence. Exact range `35-36`. The quote itself is verbatim after
normalizing the wrap. Propagated verbatim into `corpus/knowledge/terminal-route-r17.md:55`
at HEAD.

### F5 (low) — S059's quote is a mid-token truncation without an ellipsis

Source line 2 is
`bindd = SUPER, RETURN, Terminal, exec, uwsm-app -- xdg-terminal-exec --dir="$(omarchy-cmd-terminal-cwd)"`.
The gate stops at `--dir=` (or `--dir="`, depending on which `"` is read as the
markdown delimiter), eliding `$(omarchy-cmd-terminal-cwd)`. It is a verbatim
prefix, and 10 words is correct either way because the substitution is one shell
token. Risk: the printed quote can be misread as `--dir=` with no value — which
would change the meaning of the launch chain. At HEAD, `terminal-route-r17.md:69`
repeated the truncation and line 92 wrote `--dir=…` with an ellipsis (so the
note did not claim an empty value); an uncommitted working-tree revision by
another seat, made during this review, now prints the full
`--dir="$(omarchy-cmd-terminal-cwd)"` at line 70 and resolves the note side.
The gate row itself is unchanged in the working tree.

### F6 (low, adjacent to the gate's "full in SOURCES" pointer) — S059 `alacritty.toml:1-27` vs its digest

The host file is 28 lines (876 B; the closing `]` is line 28).
`695301c8…` is the whole-file digest; lines `1-27` hash
`89d34960eb44aa197699b6b0aada5edd93f0b86317099688ee5e6452a577efc8`.
The gate row's `toml 695301c8…24f8` is right for the file as a whole; the
`:1-27` label in `corpus/SOURCES.md` S059 is wrong. The draft already carried
both labels (`1-27` in the registry row, `1-28` in its hash table).

## S061 / S062: were they genuinely opened, or built from snippets?

**Opened, in full; the snippet claim does not survive.**

- S061: 8,275 B / 179-line wikitext fetched with `?action=raw`, digest equal to
  seat R1 and to today's fetch. The page contains the quote at line 24 *and*
  unrelated later sections (tail is the `wal -R` notes) — a whole page, not a
  fragment. A snippet cannot produce an 8,275-byte digest match.
- S062: 90,051 B page, digest equal to seat R7 and to today's fetch; the phrase
  appears in the visible FAQ (`<dd>`), at extracted line 247 of exactly 345
  non-blank extracted lines, matching the seat's stated 345. A snippet cannot
  produce a 90,051-byte digest match.
- The two *drafted* snippet rows are different documents, not these rows:
  `drafts/NoteTerminal-rows.md` had `S061-pending` = Ubuntu manpage
  (`manpages.ubuntu.com/…` with `Version: 0.14.0-1`, marked "search snippet only,
  not opened") and `S062-pending` = GitHub `master` blob (also "search snippet
  only"). Neither landed. The landed S061/S062 are the Arch Wiki Alacritty page
  and the Linux Junkies guide, both from the opened seat report.
- The gate sentence "two drafted snippet rows … were replaced before landing by
  opened rejections (S061, S062)" is therefore accurate as written.

S062's falsity claim also holds: `v0.13.0` `CHANGELOG.md:36`
`- Configuration file now uses TOML instead of YAML`; `v0.12.0` `CHANGELOG.md`
has no TOML entry (grep over 1,123 lines returns only
`The snapcraft.yaml file has been removed`, line 356). "False against v0.13.0
CHANGELOG:36" is correct, and the quote's 7 words is correct.

## Residual risk and limits

- **Provenance is not in the pushed tree.** `git cat-file -e
  HEAD:.ufo/waves/round-17/w1/reports/SrcTerminalAlternates.md` fails (file exists
  on disk, not in HEAD); the same is true of `drafts/NoteTerminal-rows.md`
  (untracked, not ignored). The gate's S061 provenance pointer and its
  snippet-replacement sentence are corroborated only by working-tree files.
  The digests independently prove full opens, so this does not rescue or sink
  the claim — it is a traceability gap, not a factual one.
- **revid 869789 / `oldid=869789` was not independently re-checked.** The
  `oldid=…&action=raw` request was answered by an anti-bot interstitial
  ("Making sure you're not a bot!", 7,469 B HTML, digest `421923a0…`) and the
  MediaWiki API returned 403. The current `action=raw` digest still equals the
  recorded one, so the page is unchanged since the seat's fetch; the revision
  *number* is taken from the seat report, not re-derived here.
- **Upstream code claims in S061's SOURCES row** (`config/mod.rs:371,395`;
  absent at `v0.14.0`/`v0.15.0`) were not re-verified here — that is
  `AttackP4Upstream`/`AttackVersionBinding` territory.
- The defects above do **not** touch the P4 coverage citation:
  `corpus/knowledge/terminal-route-r17.md` cites S056-S060 only; S061/S062 are
  rejected rows with empty `used-by`, and a grep for `S061|S062` outside
  `round-17.md`/`SOURCES.md` returns 0 corpus hits.
- Gate rows are byte-identical at `3722ba4`, `3e9848a`, and HEAD; the count and
  anchor defects have been stable since landing.
- The working tree diverged during this review: `corpus/SOURCES.md` gained S071,
  `corpus/knowledge/terminal-route-r17.md` was reflowed (including the S059 quote
  fix noted in F5), and `round-17.md` M2 / `corpus/README.md` were edited. None
  of these touches the gate table S056-S062; all findings above are stated
  against HEAD `988b858`.

## Exact commands used (for re-run)

```
curl -sS -o S056 https://raw.githubusercontent.com/Vladimir-csp/xdg-terminal-exec/v0.14.3/README.md
curl -sS -o S057 https://raw.githubusercontent.com/Vladimir-csp/xdg-terminal-exec/v0.14.3/xdg-terminal-exec
curl -sS -o S058 https://raw.githubusercontent.com/alacritty/alacritty/v0.17.0/extra/man/alacritty.5.scd
curl -sS -o S061.wikitext 'https://wiki.archlinux.org/index.php?title=Alacritty&action=raw'
curl -sS -o S061.raw https://wiki.archlinux.org/title/Alacritty
curl -sS -o S062.raw https://linuxjunkies.org/guides/configure-alacritty
sha256sum S056 S057 S058 S061.wikitext S061.raw S062.raw
grep -n 'Each entry from the explicit selection list is checked for applicability:' S056
grep -n 'set workdir of terminal.' S057
sed -n '35,37p' S058
awk 'NR==24' S061.wikitext
printf '%s\n' 'Versions before 0.13.0 used a YAML configuration file.' | wc -w
printf '%s\n' 'Each entry from the explicit selection list is checked for applicability:' | wc -w
printf '%s\n' 'Starting with 0.12, Alacritty switched to TOML' | wc -w
sed -n '2p' ~/.config/hypr/bindings.conf
sha256sum ~/.config/hypr/bindings.conf ~/.config/xdg-terminals.list \
  ~/.config/alacritty/alacritty.toml /usr/share/xdg-terminal-exec/xdg-terminals.list
sed -n '1,27p' ~/.config/alacritty/alacritty.toml | sha256sum   # 89d34960… != 695301c8…
# S062 extraction (345 nonblank lines; quote at 247):
python3 - <<'PY'
import re,html
raw=open('/tmp/p4g/S062.raw',encoding='utf-8',errors='replace').read()
body=re.sub(r'<(script|style)[^>]*>.*?</\1>',' ',raw,flags=re.S|re.I)
txt=html.unescape(re.sub(r'<[^>]+>','\n',body))
L=[l.strip() for l in txt.split('\n') if l.strip()]
print(len(L), [i for i,l in enumerate(L,1) if 'switched to TOML' in l])
PY
```

No tool was installed or upgraded (none); no host-mutating or paused-class command
was run.
