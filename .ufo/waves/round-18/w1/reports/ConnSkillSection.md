# ConnSkillSection — round-18 report

Seat: `MadoR18.ConnSkillSection` (leaf, no dispatch). Lane root
`/home/vgpnk/Projects/shokunin/mado-shokunin`. Scope: locate `SKILL.md` anchors and
give L1 exact insertion line numbers for the round-18 prose. No `SKILL.md` edit.

## Evidence base (read-only)

- `SKILL.md` at `refs/heads/master` = `d3a0000` (`git rev-parse HEAD`), blob
  `a678a5e50ce34ad7ea9783a51ae387a5b0cbf660`, 1,811 lines, sha256
  `277b70b1193bc78bce9cb4b45c7ab0ff028681383bc55ece16df1b4ad7ddc591`.
  `git diff --stat -- SKILL.md` empty at read. Every number below is a pre-edit
  line number for **that** file state; re-read if L1 lands anything first.
- Registry table: header `:548`, separator `:549`, **rows `:550-564`** (15
  rows, every one a single line with 8 cells), blank `:565`.
- Safety instruction section: heading `:225`, numbered rules `:227-252`
  (contiguous, no blank between items), separator blank `:253`, closing
  paragraphs `:254-256`, next heading `:258`.
- Tripwire section `:525-539`; its last sentence, `:538-539`, is now **false**:
  it says "It is labelled a probe: it reads mutable / transcripts with no frozen
  replay." At this read `tools/mado-tripwire.py` already has `--frozen`
  (1,160 lines, sha256 `593b3aafed37c6c9e5370486b43b47bd4f23f660ac4ef8cd42392e6dc2ee846f`,
  may still be moving under TwFrozenMode) and
  `.ufo/waves/round-18/tripwire/frozen/expected.json` has **17** cases.
  `.ufo/waves/round-18/frozen-tripwire/` was **absent** at this read.
- Registry prose: Round-16 limit `:566-575`; Round-17 tripwire limit `:577-587`;
  blank `:588`; round-13/14 frozen-regression notes `:589-601`; blank `:602`;
  next heading `## Evidence trail & sources` `:603`.
- Uniqueness: `It is labelled a probe` → 1 hit; `^### Safety rules` → 1;
  `^## Gate registry` → 1; `^| mado-tripwire` → 1.

## 1. Registry table — rows and exact insertion points

| line | name | kind |
|---|---|---|
| 550 | mado-verify | gate |
| 551 | mado-regression | gate |
| 552 | mado-snapshot-diff | gate |
| 553 | mado-frozen-regression | gate |
| 554 | mado-source-merge | gate |
| 555 | mado-round13-measure | probe |
| 556 | mado-round14-measure | probe |
| 557 | mado-round15-measure | probe |
| 558 | mado-frozen-regression-r14 | gate |
| 559 | mado-action-plan | gate |
| 560 | mado-action-plan-frozen | gate |
| 561 | mado-round16-measure | probe |
| 562 | mado-tripwire | probe (1,191 bytes; selftest/pin cells are scan-only today) |
| 563 | mado-label-check | probe |
| 564 | mado-round17-measure | probe |

- **Replace in place: `:562`** with draft Row A (`.ufo/waves/round-18/drafts/SkillRegistryDraft.md`
  §A). One line → no shift. Keep the frozen entry first and label the scan entry
  `scan (probe entry)`: PROTOCOL §Gate standard gives a row one `gate|probe` kind,
  and C3's declared wording is "the registry row moves `probe` → `gate`"; the
  single-row draft satisfies it, a split row (`mado-action-plan` / `-frozen`
  precedent at `:559-560`) would reinterpret C3 and is not recommended this round.
- **Insert new rows after `:564`** (before blank `:565`), one per line, no blank
  lines between: the five probe rows from draft §B (`mado-receipt-check`,
  `mado-fetch-verify`, `mado-pipe-rc-census`, `mado-measure-mutants`,
  `mado-frozen-provenance`). All five scripts exist at read; they are probes
  (no committed selftest), so do not label any of them `gate`.
- **Insert the Round-18 frozen limit paragraph after `:588`** (after the blank
  that closes `:587`), 5 lines, before `:589`. All frozen prose then stays in one
  place (`:577-601`).

## 2. Safety instruction section — exact span

`:225` heading · `:227-252` rules 1-6 · `:238-240` Round-16 no-producer override
(inside rule 2) · `:251-252` rule 6 (scratch outside the substrate) · `:253`
blank · `:254-256` closing paragraph (config trees, OBS/INF/UNK, append-only
errata) · `:258` next section.

No edit is needed inside rules 1-6. Rule 6 does **not** conflict with committed
fetch bodies: it constrains *probe* artifacts (`/tmp/<lane>-*`) and config trees;
the fetch directory is committed wave evidence and is not a config tree. The
new conduct rule belongs at the **end of the numbered list** (see §4).

## 3. Where frozen-tripwire usage belongs

**Primary:** a new `### Frozen tripwire replay (round 18)` immediately after the
tripwire subsection's blank separator — **insert after `:540`** (the existing
blank `:540` stays before it; heading becomes final line 551). Steps:

1. **Replace `:538-539`** (2 lines → 2 lines) so the probe sentence stops
   contradicting the landed tool:
   `misroots) are not findings. As a scan it stays a probe over mutable` /
   `transcripts; the frozen replay below is its gate evidence.`
2. Insert the new subsection (19 lines including the trailing blank) with: the command
   `python3 -I tools/mado-tripwire.py --frozen .ufo/waves/round-18/frozen-tripwire`;
   the order (malformed/unpinned/tampered snapshot exits 2 and is *never* a
   compared verdict; only then an in-process scan and comparison of exit, label,
   exact `(file, line, class, rule)` multiset and `known_misses`); the verdict
   fields to quote (`outcome`, `expected_sha256`, `tool_sha256`, `scan_exit`,
   `scan_label`, `missing_findings`/`extra_findings`); the two calibration
   clauses `frozen_match` on a `permitted_only` pin is not clean, and
   `known_misses` (assertion of no-finding, re-pin on violation) is not a
   `permit` waiver; and the R17-V1 receipt obligation (`tool_sha256` +
   `measured_commit` on every cited run).

**Not** in the registry prose (that carries limits only, `:588`) and **not** in
the round-18 EOF append (that carries the measured receipt: run outcome,
snapshot digest, selftest tally; it starts after the current final line `:1811`,
final `:1850` under this plan). Keeping the standing instruction in `:551`
means the "after every wave" reader at `:535` sees it before any append.

## 4. Where fetch-receipt discipline belongs

**Primary:** a new numbered **rule 7** at the end of the safety fence —
**insert after `:252`** (immediately after rule 6; the existing blank `:253`
becomes the separator before the closing paragraph). Ten lines, same 3-space
continuation style as rules 1-6. Content in this order:

1. `curl -sSL` only, public sources; no auth, cookies, session or private URLs;
   body > 1 MiB skipped and reported (probe artifacts stay `/tmp`; bodies are
   *committed wave evidence* under `<round>/fetch/<seat>/`, later as
   `mado-fetch-receipt-v1` lines with url, final_url, http_status, UTC time,
   bytes, sha256, body slug, curl version; lines append-only, never rewritten).
2. Credit condition: `http_status` **200**, body bytes and sha256 match, and
   every https URL in the row's `source` matches a receipt `url` or `final_url`;
   tag-pinned raw URLs preferred with the tag commit recorded.
3. Limit: a non-200 body may witness an absence check but never credits a
   source; a receipt proves served bytes, not the installed binary.

Why here, not elsewhere:

- **Not** a `###` block under `## Current diagnostic boundaries` (`:409-539`):
  the round-dated blocks there are instruments (waybar boundary, tripwire); a
  network/write-scope conduct rule is read before any fetch, and rules 4-5 of
  this fence are already non-mutation (privacy, epistemic), so the fence is the
  established home for "what this lane may do".
- **Not** `## Evidence trail & sources` (`:603`): that is a dated round log, not
  a rule.
- **Not** an edit to Standing rules `:39-45`: the ambiguity is real but resolvable
  by rule 7. `:43` ("Read already available tagged source instead of installing a
  help tool") forbids installing help tools; it does not forbid reading a public
  doc, but it never authorizes the network either. Rule 7 authorizes exactly the
  receipted read and nothing else, so `:39-45` can stay byte-identical. Optionally
  add one clause at `:44`, not required.

## 5. Insertion order and simulated post-edit map

Apply **bottom-up** so every pre-edit number above stays valid:

| # | action | anchor | lines |
|---|---|---|---|
| 1 | insert Round-18 frozen limit | after `:588` | 5 |
| 2 | insert five probe rows | after `:564` | 5 |
| 3 | replace `mado-tripwire` row | `:562` | 1→1 |
| 4 | insert `### Frozen tripwire replay` | after `:540` | 19 |
| 5 | replace probe sentence | `:538-539` | 2→2 |
| 6 | insert safety rule 7 | after `:252` | 10 |

Simulated final positions (same content, draft text lengths as in §3/§4):
rule 7 `:253-262`, closing paragraph `:264-266`, `## Scoped verification`
`:268`, `### Waybar …` `:515`, `### Post-hoc transcript tripwire` `:535`,
`### Frozen tripwire replay` `:551`, `## Gate registry` `:570`, rows
`:579-593` (tripwire now `:591`), new rows `:594-598`, Round-18 limit `:623`,
`## Evidence trail & sources` `:642`, `## Errata` `:1838`, EOF `:1850`.
Cumulative shifts: **+10** below `:253`, **+29** below `:540`, **+34** below
`:564`, **+39** below `:589`.

## 6. Move — enforce `http_status` at credit time, not per receipt

**Evidence (committed, read-only).** 295 receipts exist at this read across
`.ufo/waves/round-18/fetch/*/receipts.jsonl`; 5 are non-200 (paths in the table
are relative to `.ufo/waves/round-18/`):

| receipt | status | bytes | sha256 head | body |
|---|---|---|---|---|
| `fetch/NoteTheme/receipts.jsonl:6` | 404 | 195,690 | `4e0dcc9ea565` | `swaybg-v1.2.2-doc.html` (GitHub 404 HTML) |
| `fetch/NoteTheme/receipts.jsonl:7` | 404 | 14 | `d5558cd419c8` | `swaybg-v1.2.2-1.scd` |
| `fetch/NoteTheme/receipts.jsonl:15` | 404 | 14 | `d5558cd419c8` | matte-black `theme.name` absence check |
| `fetch/SrcElephantProviders/receipts.jsonl:19` | 404 | 14 | `d5558cd419c8` | `xdg-v0.5.3-files.go` |
| `fetch/SrcThemeAlternates/receipts.jsonl:5` | 404 | 0 | `e3b0c44298fc` | `archwiki-walker-raw` |

`fetch-verify.py` has **no `http_status` reference at all** (`grep -c` → 0):
`verify_receipt()` checks schema, body presence, `bytes` and `sha256` only, so
every one of those 404s prints `FETCH … ok`. Its row join
(`.ufo/waves/round-18/fetch-verify.py:16-18`) is "**at least one**
verified-or-listed receipt either has a sha256 that literally appears in the
row's anchor cell, or has a url/final_url equal to a URL appearing in the row."
So a row can be `receipted` from a 404 page, from one of several cited URLs, or
from a digest-only match. Note the 0-byte 404 carries exactly the
JjAudit F10 empty-input digest `e3b0c442…`: the same class of false value the
round is fixing, now inside the fetch layer.

**Move.** In SKILL rule 7 (and in the `mado-fetch-verify` row's verdict map),
make status a **credit-time** condition: `ROW <id>` is `receipted` only when
*every* https URL in the row's `source` has a receipt and at least one matching
receipt is `http_status: 200` with matching bytes/sha; add a
`ROW <id> UNRECEIPTED_NON200` (or `PARTIAL`) outcome, exit 1. Leave the
per-receipt `FETCH … ok` verdict unchanged, so a deliberate non-200 remains valid
evidence of an absence check (NoteTheme:15 is exactly that and must not become a
verifier failure).

**Affected axes.** *calibration* — R17-V3's "tell a fetched row from an invented
one" becomes decidable; a 404 body can no longer satisfy it, and the
`receipted` label stops over-claiming. *coverage* — a P5/P3 row cannot be
credited from a 404 HTML page or from a single URL when the row cites several.
*operability* — no new fixture or tool; one condition in the rule and one row
verdict. No axis is harmed: the absence-check use is explicitly preserved.

**Risks.** (a) Redirects: receipts are recorded after `-L` and the redirect
samples show `http_status 200` with `url != final_url`, so requiring 200 does
not break them; join must keep accepting either field. (b) A 403/429 is a retry,
not a credit — rule 7 should not imply the row is dead. (c) The tool change
belongs to the FetchVerify owner; if it does not land, the SKILL rule still
states the correct credit condition and the probe's under-check is recorded as a
limit, not silently accepted. (d) Scope the "every URL" rule to https rows;
file-path sources have no receipt.

**Verification (L1, not this seat).** Run `python3
.ufo/waves/round-18/fetch-verify.py --sources corpus/SOURCES.md --rows <ids>`.
On the landed tool a row matched by `fetch/SrcThemeAlternates/receipts.jsonl:5`
(the 404 URL `https://wiki.archlinux.org/index.php?title=Walker&action=raw`)
prints `receipted` — that is the red observation. After the change the same
command must print the non-200 row class; a green row is any credited round-18
row whose URLs all show 200.

## 7. Draft reconciliation — contradictions L1 must resolve

1. **Row 562's kind cell vs its two modes.** Draft Row A keeps the scan entry in
   a `gate` row. Keep it, but label the entry `scan (probe entry)` and say in the
   Round-18 limit that the scan remains a probe over mutable transcripts; C3's
   wording is then literally true and the R17-V4 class cannot be cited as clean.
2. **`N` in the frozen selftest cell.** `.ufo/waves/round-18/tripwire/frozen/expected.json`
   has 17 cases at this read; re-read at landing (TwFrozenSelftest may be
   editing). Do not carry 17 blind.
3. **No frozen run can be cited yet.** `.ufo/waves/round-18/frozen-tripwire/` is
   absent; the row may describe `--frozen`, but the round report must not cite a
   `frozen_match` until the snapshot and its expected.json are committed.
4. **Limit paragraph must add two clauses the draft omits:** a `frozen_match` on
   an `expected_label: permitted_only` pin is not a clean result, and
   `known_misses` is an assertion of no-finding (a finding there forces a
   reviewed re-pin), not a permit waiver. The Round-17 limit does not cover
   frozen labels.
5. **Receipt obligation must be prose, not only tool output.** Draft's "the pin
   binds inputs, not the tool digest" is correct but can be read as "tool
   identity is unrecorded". Add the R17-V1 sentence (`tool_sha256` +
   `measured_commit` on every cited run) or the defect recurs in the standing doc.
6. **`mado-fetch-verify`'s selftest cell** currently says "/tmp fixtures; no
   committed selftest" — the R17-V5 pattern. Either commit a red fixture or cite
   the committed round-17 rows at `d9a5a18` as the observed red; see §6.
7. **Frozen path naming.** `.ufo/waves/round-18/frozen-tripwire/expected.json` is
   not under a `*/frozen/` root, so PROTOCOL's bare-name collision rule is not
   triggered; the explicit path is fine. Do not shorten it to a bare name.
8. **Historical self-references shift.** `SKILL.md:1314` (`:1716`) and the dated
   errata anchors `:40-41`, `:102`, `:103`, `:338`, `:297`, `:422`
   (`:1803-1808`) all move by the shifts in §5. They are already labelled
   "former"/dated and must not be rewritten; only know that a reader cannot
   resolve them against the edited file.

## Gates

None run. The assignment is a locator; lane gates, the tripwire (scan or frozen),
and `fetch-verify` were not executed by this seat. No tool installs or updates.

## Touched surfaces

- Written: this report only.
- Read only: `SKILL.md`, `PROTOCOL.md` (fleet), `SCORECARD.md`, `corpus/SOURCES.md`,
  `corpus/knowledge/theme-route-r18.md`, `.ufo/waves/round-18/` tools, drafts,
  fetch receipts and tripwire fixtures.
- No `SKILL.md` or other lane file write; no git/jj write; no pacman/systemctl/
  hyprctl/omarchy/walker/elephant/swaybg; no network; no `/tmp` artifacts kept.

## Artifact paths

- `.ufo/waves/round-18/w1/reports/ConnSkillSection.md` (this file)
- Anchors: `SKILL.md:225-256` (safety fence), `:252` (rule 7 insert),
  `:525-539` + `:540` (tripwire/frozen), `:548-564` (registry table),
  `:562` (row replace), `:564` (rows append), `:588` (limit insert).
