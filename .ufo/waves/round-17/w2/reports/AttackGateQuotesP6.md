# AttackGateQuotesP6 — P6 gate rows S063–S070

Ticket: verify that every P6 gate row in `corpus/lessons/round-17.md` § Gate
(head lines 50–57) is (a) a quote verbatim at its named anchor in freshly
fetched bytes, (b) ≤25 words, (c) a digest equal to `corpus/SOURCES.md`.
Lane HEAD `988b858bd6049bc709807534fd725c05264f7e60`. Installs: **none**
(no pacman/sudo/systemctl/compositor or package probe; only `curl`,
`python3`, `git show/diff/status`, `sha256sum`, `openssl dgst`, `sed`).

## Verdict

| axis attacked | result |
|---|---|
| **Quote verbatim at anchor** (S063–S069, the 7 rows carrying a quote) | **Attack failed.** All 7 quoted strings are present at exactly the stated anchor; S063 and S064 are the *whole* anchor line, S065–S069 are interiors of it. |
| **≤25 words** | **Attack failed.** All 7 satisfy the bound; max is 24 (S064). Holds even under the most generous tokenization (slash-split), which gives 24 at worst. |
| **Digest equality with SOURCES.md** | **Attack succeeded on one row.** S063, S064, S065, S067, S068, S069 reproduce byte-for-byte. **S066 does not.** S070 (rejected, cited nowhere) cannot be reproduced by construction. |

The substantive P6 route survives: its prose quotes and line anchors are
correct. What fails is the *identity receipt* on its strongest code row.

## Positive verification (HEAD-bound)

Anchors are lines of the tag-stripped `<article>` text for `HW`/`LW`
(extractor re-derived independently: first `<article>`, `<br>`→newline,
close-block→newline, strip tags, unescape, collapse runs of spaces, drop
blank lines) and raw file lines otherwise. "Words" = `.split()` of the quoted
string. Digests are `sha256sum` of fresh 200-OK bodies, compared to the
SOURCES row at HEAD.

| row | anchor | quote vs anchor line | words (stated) | fresh sha256 == SOURCES |
|---|---|---|---|---|
| S063 | `HW:6` (article line 6 of 121) | whole line, byte-exact | 9 (11) | yes `b45c03dc…c83f640` (254 750 B) |
| S064 | `LW:7` (article line 7 of 332) | whole line, byte-exact | 24 (24) | yes `f69cff6b…7eabf5` (291 777 B) |
| S065 | `HR:6` | substring of line 6 | 10 (9) | yes `f5b852ee…9781f6` (2 598 B) |
| S066 | `HC:473` | substring of line 473 | 5 (—) | **NO** — see F1 (29 880 B) |
| S067 | `HH:23` | substring of line 23 | 3 (—) | yes `f9e4e558…fc0a2b8` (3 611 B) |
| S068 | `HM:61` | substring of line 61 | 5 (5) | yes `379bf321…d672a38` (2 587 B) |
| S069 | `LR:5` | substring of line 5 | 4 (5) | yes `83096def…38f50f3` (1 458 B) |
| S070 | none (rejected row) | no quote printed | — | **NO** — see F3 |

Additional checks that passed:

- Each anchor falls inside the line range the SOURCES row declares as read:
  `HW:6`∈"6–120"; `LW:7`∈"6–85"; `HR:6`∈"5–33, 62"; `HC:473`∈"433–485";
  `HH:23`∈"23, 26"; `HM:61`∈"55–63"; `LR:5`∈"5, 19".
- `HC:473` sits inside `handleDbusLogin` (opens `HC:465`), i.e. the dbus
  Lock/Unlock context the row claims, not a same-named symbol elsewhere.
- Quoted README bullets are complete (`HR:6`, `LR:5`); no mid-word or
  mid-bullet truncation.
- The P6 note's own anchors that bind these rows re-verify:
  `HW:6`, `HW:7`, `HW:36`, `HW:37`, `HW:51`, `HC:70`, `HC:301`, `HC:327`,
  `HR:5`, `HH:23`, `HM:61`, `LR:5`, `HC:473`. No anchor drift into
  `corpus/knowledge/idle-lock-route-r17.md`.

## Findings

### F1 — HIGH — S066 digest is wrong by one hex nibble (real falsification)

Attacked: "digests equal SOURCES.md", with SOURCES compared to the tag-pinned
file's actual bytes rather than only to the lesson's copy.

- Recorded in both places (and therefore internally "equal"):
  `2dd4d73d4f5cd57ed5a2e7d10d630bdcfa0dbdd87e7a9819bb1d1cdd4dfb2d75`
  - `corpus/SOURCES.md:78` (S066 anchor cell)
  - `corpus/lessons/round-17.md:53` (gate row S066)
- Actual bytes of
  `https://raw.githubusercontent.com/hyprwm/hypridle/v0.1.8/src/core/Hypridle.cpp`
  (29 880 B, 735 lines, HTTP 200):
  `2dd4d73d6f5cd57ed5a2e7d10d630bdcfa0dbdd87e7a9819bb1d1cdd4dfb2d75`
- Difference: character 9 (0-based index 8), recorded `4`, actual `6`;
  63 of 64 hex characters identical. Confirmed across **five** fetches and
  two hashers: direct `raw.githubusercontent.com` fetch, `github.com/…/raw/refs/tags/v0.1.8/…`
  redirect, a `Cache-Control: no-cache` refetch, and `openssl dgst -sha256`
  all give `…3d6f5…`; all five bodies are `cmp`-identical (unique sha256
  count across them: 1).
- Provenance: wave 1 recorded the **correct** value
  (`w1/reports/SrcHypridleSrc.md:20`, 29880 B / 735 L), so the byte read was
  right and the corruption happened at transcription time. The wrong string
  first appears in `drafts/NoteIdle-rows.md:15` (row) and `:25` (receipt
  list), then propagates to
  `.ufo/waves/round-17/gen_w2.py:50`, `corpus/SOURCES.md:78` and
  `corpus/lessons/round-17.md:53`.

Why it matters, and why the documented recheck does not catch it:
`corpus/knowledge/idle-lock-route-r17.md:2-3` instructs the rechecker to
"compare raw SHA-256 with corpus/SOURCES.md S063-S069". That comparison
**fails today for S066**, and an auditor who instead checks lesson↔SOURCES
equality *passes*, because both copies carry the same wrong digit. This is
the same shape as round-16 M1: a receipt that agrees with its own copy but
not with the thing it claims to identify.

Blast radius: no content claim changes — `HC:473`, the line ranges and the
inhibit/on-timeout ordering remain correct at those bytes; and the file is
tag-pinned, so it is recoverable. But the gate's third property is falsified
for an admitted, tier-A, route-bearing row.

Sibling inconsistency worth routing (the round must not close F1 by citing
these): `.ufo/waves/round-17/w2/reports/AttackP6General.md:24` and
`.ufo/waves/round-17/w2/reports/ReopenS067.md:93-94` label `…4f5…` as the
*fetched* value. Both equal the recorded typo, so neither is independent
evidence. `ReopenS066.md:39-41` and `AttackP6Unexercised.md:21-22` report the
correct observation (`…6f5…`).

### F2 — LOW — three word-count annotations in the slice are wrong (the bound is not)

Attacked: "≤25 words (count)" — i.e. both the threshold and the printed
counts a reader would use to check it.

| row | printed | measured (whitespace tokens of the quote) |
|---|---|---|
| S063 | 11 | **9** |
| S064 | 24 | 24 ✓ |
| S065 | 9 | **10** |
| S068 | 5 | 5 ✓ |
| S069 | 5 | **4** |

No single counting rule reproduces the wrong ones: `\S+` gives 9/24/10/5/4,
word-character runs give 9/24/8/5/4, dropping slash tokens gives 9/24/8/5/4,
and slash-splitting gives 12/24/8/5/4 — against claims 11/24/9/5/5.
Table-wide the same defect appears outside my slice: S056 prints 12 (11
measured) and S061 prints 10 (8). So **5 of the 11** annotated counts in
§ Gate are estimates, not measurements.

Consequence: none for the rule itself — every quote is ≤25 under every rule
tried, and the worst case is S064 at exactly 24 (one word of margin). The
defect is that the annotations cannot be used as a proxy for the audit.

### F3 — LOW — S070's digest is unreproducible by construction; its "339 extracted lines" is unverifiable

Attacked: S070's digest and its two attached representations.

- Ten fetches of the single URL produced **ten distinct bodies**
  (179 317–179 614 B), none equal to the recorded
  `bf875a255610f2665552eb2d9921f2cb43707012686a51f8b9b82a85350ab90a`
  (recorded in full at `w1/reports/SrcTerminalAlternates.md:40` and repeated
  at `w2/reports/ReopenS070.md:35`; the corpus row truncates it to
  `bf875a25…350ab90a`, i.e. 16 of 64 hex characters): `747faed4…`,
  `62818f01…`, `4d3c3e6e…`, `fcbc6cc4…`,
  `b75daadb…`, `09eaed66…`, `cfab5658…`, `99292e97…`, `2ecb58ae…`,
  `5071f222…`.
- Cause observed in the body itself: a per-request anti-bot token
  `<a href="https://hashnode.dev/cdn-cgi/content?id=<rand>-<epoch>.<micro>-1.2.1.1-<hash>"`
  inside the first 48 lines; `cache-control: public, s-maxage=25`,
  `x-vercel-cache: MISS`, `vary: rsc, next-router-state-tree, …`. Two
  fetches of equal length (179 613 B) still differ, so length does not imply
  bytes.
- Net: the value was plausibly real when read, but it is not a durable
  identity and no rechecker can ever confirm or refute it. A raw digest of a
  page carrying a per-request nonce should not be recorded as an anchor.
- "339 extracted lines": not reproduced. Nine plausible strip/extract
  variants on a fresh body give {147, 162, 197, 243, 259, 332, 377, 1382,
  1501} lines; none is 339. The count is unverifiable (not provably false —
  the extractor used is not recorded).
- "0 version tokens": true in the sense that matters — **no**
  hypridle/hyprlock/Hyprland version appears. Two dotted numerics do exist in
  the article text (`wpctl set-volume -l 1.5`, `8.8.2056`), neither a
  software version, so the REJECTED reason ("names no … version anywhere")
  stands. The block claims also hold on fresh bytes (`lock_cmd`,
  `before_sleep_cmd`, `timeout = 600/900/1800`) and the page does restate the
  wiki it links (`href` to `wiki.hyprland.org/Hypr-Ecosystem/hypridle/` and
  `…/hyprlock/`, plus the "You can learn more about … at Hyprland Wiki"
  copy).
- Usage check: `S070` is cited by no admitted entry — only its own SOURCES
  row, the gate table, and wave reports. So no route is harmed.

### F4 — INFO — the lane worktree changed under this verification

Not a gate defect, but it affects anyone else who measures the same files.
At session start `git status --porcelain` showed only untracked paths; by the
end, four tracked corpus files were modified (mtimes 11:56:37–11:57:09
−0300, i.e. during wave 2):

- `corpus/SOURCES.md` — new row `S071` (user-local Alacritty desktop entry)
- `corpus/README.md` — P4 `terminal-route-r17` row text
- `corpus/knowledge/terminal-route-r17.md` — 13 lines changed
- `corpus/lessons/round-17.md` — M2 cell

The **gate rows and the S063–S070 SOURCES rows are byte-identical between
HEAD `988b858` and the dirty worktree** (row-by-row compare of all 15
`S056–S070` rows in each file: identical). All findings above therefore bind
HEAD: quotes and digests were re-read from `git show HEAD:…` blobs, and
fresh fetches were compared to those HEAD rows. Installs: none.

## Residual risk / verification gaps

- **S063/S064 anchor convention is documented, not committed.** The
  "tag-stripped `<article>` text" rule exists only as one clause in SOURCES.
  My independent re-derivation reproduces `HW:6` and `LW:7` exactly (121 and
  332 article lines, consistent with the declared ranges), so the risk is low
  — but a rechecker must re-derive the extractor rather than run a committed
  script.
- **S063/S064 are "Latest git" pages, not version-pinned.** Their digests
  match today; SOURCES says so explicitly and the route does not pretend
  otherwise. Both are stable across two fetches. A future recheck can drift.
- **S064 sits one word under the cap** (24/25). Any extension of that quote
  breaks § Gate's own rule.
- **`HM:61` is an interior substring of a log call**; the emitted literal is
  `ConfigManager: No hypridle.conf file found in:` (the quote drops the
  `ConfigManager: ` prefix). The note says the program "logs" the quoted
  text, which is true of the substring but not of the whole log line.
- **P6 note `[HW:36-37]`** quotes "Every listener has a timeout (in seconds).
  After idling for timeout seconds," and stops before `on-timeout will fire.`
  (HW:37) with no ellipsis. The trailing comma signals truncation; a strict
  reader may take the sentence as complete. Cosmetic, outside the gate table.
- **Out of slice, not adjudicated:** S061's current ArchWiki revision
  (60 206 B, `bba2e98c…`) does not match its recorded truncated digest
  `c39c563d…4600bb`; the row is revid-pinned (869789) and the `oldid` URL
  answered a "not a bot" interstitial here, so I could not test the pinned
  revision. S062's full digest reproduces exactly
  (`08608a0b…bec2c653`, 90 051 B).

## Reproduction

```
curl -sS -o f https://raw.githubusercontent.com/hyprwm/hypridle/v0.1.8/src/core/Hypridle.cpp
sha256sum f      # 2dd4d73d6f5cd57…  (recorded: …3d4f5…)
openssl dgst -sha256 f
git -C <lane> show HEAD:corpus/SOURCES.md   | grep '^| S066'
git -C <lane> show HEAD:corpus/lessons/round-17.md | sed -n '50,57p'
# wiki anchors: first <article>, <br>->\n, close-block->\n, strip tags,
# html.unescape, collapse spaces, drop blanks; then read line 6 / line 7.
```
