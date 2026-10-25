# CritD9Boundary — the refusal boundary for documentation-localization material

Seat: critic, round 36 wave 1. Assignment: `w1/prompts/CritD9Boundary.md` — attack the
refusal boundary for documentation-localization material. Question asked: is **one rule
stated** that decides `chinese-article-revision-r30.md`, `chinese-wiki-canonical-url-r28.md`
and `zh-wiki-snapshot-semantics-r29.md` the same way? Quote the PROVINCE lines. Report
whether the boundary is **stated or only practised**, and what single sentence would state it.

All reads were read-only. No file other than this report was written. No tools installed.

## 1. The three files, and where they actually live

The assignment's path prefix `LANE/corpus/knowledge/` for the r28/r29 entries does not
resolve: `git log --all` has no tracked `corpus/knowledge/{chinese-wiki-canonical-url-r28,
zh-wiki-snapshot-semantics-r29,chinese-article-revision-r30}.md` in the lane at any commit.
The three entries live in the **shokuknow package** (read-only campaign source), which is
where the spot-check's refusal row itself points:

- `/home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge/chinese-article-revision-r30.md`
- `/home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge/chinese-wiki-canonical-url-r28.md`
- `/home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge/zh-wiki-snapshot-semantics-r29.md`

All three are package knowledge **candidates for admission**, not lane corpus files. Their
`Lane: mado-shokunin. Round: corpus-expansion-N` headers are **package-era campaign rounds**
(r28 = corpus-expansion-3, r29 = corpus-expansion-4, r30 = corpus-expansion-5), not lane
rounds; the lane's own round count is 36. This matters: the r28/r29 files name the Chinese
article "Hyprland" as their subject, so a reader could take them for already-admitted lane
knowledge. They were never admitted — the lane refused this whole class (below).

## 2. The three decisions — and the rule that produced them

The spot-check table row (`corpus/lessons/round-35-verifier-spotcheck.md:171`):

> | `chinese-article-revision-r30.md` (package knowledge) | refuse | `/home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge/chinese-article-revision-r30.md` (read-only, outside the fleet root) | **agree** | The entry is Chinese-wikitext revision/bookkeeping ("§ footer 检索自", a snapshot revision id) — a documentation-localization surface, not the config plane `PROVINCE.md:3–10` owns. The refusal is consistent with the same rule applied in rounds 33–34. Note for the lane: earlier entries of that class exist (`chinese-wiki-canonical-url-r28.md`, `zh-wiki-snapshot-semantics-r29.md`), so the boundary ruling should be stated once and applied both ways (see D9's sibling concern). |

The same rule, verbatim, in the lane's own lessons:

- `corpus/lessons/round-32.md:49-51` (the first refusal, of `two-literature-drift-r26.md`):
  "Its subject is *documentation localization* — how the Chinese and Japanese ArchWiki
  translations lag the English article. mado's province is 'the Hyprland/waybar/walker
  configuration plane and display behavior on this host'; a translation-lag surface teaches
  nothing about a config plane or a display behaviour, so the material is out of the lane's
  domain even though the package was built per-lane."
- `corpus/lessons/round-33.md:18`: "Reject: `two-literature-drift-r26.md`. Documentation
  localization is outside PROVINCE.md, and S199 is a community tier-C source."
- `corpus/lessons/round-34.md:48-52`: "`S195`, `S205`, `S228` — localization surfaces
  (SJTU arch-wiki-docs-zh-cn package, Arch-wiki interwikimap JSON,
  `cn-export-hyprland.html`). Documentation localization is outside PROVINCE.md, the same
  rule that refused `two-literature-drift-r26.md` in round 33."
- `corpus/lessons/round-35.md:100-104`: "`corpus/knowledge/chinese-article-revision-r30.md`
  (package, tier-B Chinese-wiki revision material) — refused: a documentation-localization
  surface, outside `PROVINCE.md`, the same rule that refused `two-literature-drift-r26.md`
  in round 33 and four register rows in round 34."

I checked `git log --all --diff-filter=A --name-only` for every tracked file whose name
matches `chinese|zh-wiki|wiki` (the only hits are round-32 scratch/report files about the
English IPC wiki, not Chinese localization), and `grep`/`glob` over `corpus/knowledge/` for
`chinese|zh` names: **no Chinese-document entry was ever admitted to the lane corpus**. So
the *applied* rule decides r28 (canonical URL / interwiki map), r29 (snapshot semantics) and
r30 (revision bookkeeping) the same way — refuse, by the one rule "documentation localization
is outside PROVINCE.md", stated in the lessons and applied identically in rounds 32–35.

## 3. Is the boundary stated in PROVINCE.md? No — only practised

`PROVINCE.md` (65 lines) has exactly one documentation-related line, the owns line:

> `PROVINCE.md:10`: "The omarchy skill (`~/.agents/skills/omarchy/`) is documentation surface,
> read-only."

The refuses lines say nothing of documentation:

> `PROVINCE.md:14-16`: "**Refuses:** secrets in configs (shape-only, → kagi), model endpoints
> (→ kama), model quality (→ kengaku). Never mutates a running compositor state; every claim is
> file-byte- or screenshot-verified."

`grep -niE 'document|wiki|locali|translat|literature' PROVINCE.md` → one hit, line 10 (the
omarchy ownership line). `git log -S 'localiz'|-S 'wiki'|-S 'literature' -- PROVINCE.md` →
no commit ever introduced such text (the round-33 spot-check even records it:
`corpus/lessons/round-33-verifier-spotcheck.md:80`: "PROVINCE.md was not edited (`grep -i
localization` empty)"). There is no stated boundary: the rule lives only in the lessons and in
the practised refusals (`two-literature-drift-r26.md` r32/r33, S195/S205/S228 r34,
`chinese-article-revision-r30.md` r35).

## 4. Counterexample — the boundary as practised over- and under-reaches what any PROVINCE text can state

The one sentence that would state the rule has to make all three decisions AND keep the only
documentation surface the province owns (the omarchy skill, line 10) — and the three refused
entries share no property that distinguishes them from the omarchy skill except location and
language. Check the candidates:

- **"Documentation localization is outside PROVINCE.md"** (the practised sentence). Under it,
  the r30 decide identical (revision bookkeeping of a translated article). r29 decide
  (offline-package snapshot semantics = mechanics of the translated channel). r28 is a stretch
  (an interwiki-map URL is infrastructure/locator metadata, not translation or drift) — the
  r34 flip list ("localization surfaces") includes it, but the r32 definition of the class
  ("how the Chinese and Japanese ArchWiki translations lag the English article") does not.
  The shelf case is `chinese-hyprland-window-rules-r16.md` (package):
  `/home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge/chinese-hyprland-window-rules-r16.md`
  — "A Chinese-language guide to this lane's own desktop describes its window rules and its
  focus dispatch", i.e. **config-plane content**, in Chinese, from a CSDN blog (tier C).
  Round 35's stated rule refuses it for the same reason as the other three (it is in the
  sweep of the 66 refused knowledge items; the lane's `corpus/knowledge/` holds no Chinese
  entry). So the rule as practised is not "subject matters are out" — it is **the Chinese
  documentation channel is out** — while the only *owned* documentation surface is the
  omarchy skill's own files, authored in English for the configured plane. Not one PROVINCE
  line says either.
- **"Documentation of the config plane is in"** — would admit the r16 window-rules guide
  (it documents the config plane), contradicting the practised refusal.
- **"Upstream/community wiki material is out"** — would admit the package's own prose about
  the *English* IPC page? No: the staged row S203 (Hyprland IPC page, upstream wiki) was
  refused in round 35 — but **only because no claim was frozen over it**, with a stated flip
  ("a later round freezes a claim over the IPC surface and appends the row",
  `corpus/lessons/round-35.md:106-109`). So the English upstream wiki is in-principle
  admissible, and the Chinese upstream wiki is categorically barred: the boundary is the
  language channel, not "upstream".

So the practised boundary is a channel rule (the Chinese-language documentation channel, and
its localization mechanics, is out; the English config-plane documentation channels are in),
it decides all three r28/r29/r30 entries the same way, and **no single sentence in
PROVINCE.md states it**. A reader of PROVINCE.md alone cannot derive any of the three
decisions, and the owns line (omarchy skill = "documentation surface") actively invites the
wrong derivation — "documentation is owned" — for the package's Chinese entries. The boundary
is **practised, not stated**, in the document the round-32 lesson itself names as the rule's
home ("outside PROVINCE.md" — but PROVINCE.md never says so).

## 5. The smallest safe correction

The round-35 spot-check's ask (line 171, D9) is "the boundary ruling should be stated once
and applied both ways". One sentence does it, inserted into the `Refuses` block of
`PROVINCE.md` (after line 16), naming the channel and keeping the omarchy-skill ownership
intact:

> **Refuses:** … material about the *documentation artifacts* of the desktop plane and their
> localization — the Chinese/Japanese ArchWiki channel, its URLs, snapshot semantics,
> revision bookkeeping and translation drift, and any documentation written in a localized
> channel — is outside the province; only the omarchy skill's own files
> (`~/.agents/skills/omarchy/`) are documentation surface (report, never absorb).

That decides r28 (URL), r29 (snapshot semantics), r30 (revision bookkeeping) and the r16
Chinese guide by one stated rule, and leaves line 10's omarchy ownership intact. (A
minimalist alternative: replace the owned-surface clause above with the practised sentence
from the lessons — "Documentation localization is outside PROVINCE.md" — but that one does
not cover the r16 Chinese config-guide case without the channel clause, which is why the
fuller sentence is the honest statement of what the lane actually does.)

## 6. Verdicts

- **Boundary stated in PROVINCE.md?** FAIL — grep over the whole file gives only the omarchy
  ownership line (10); `git log -S` over `localiz|wiki|literature` finds no commit ever
  stating it. Round-33's spot-check confirms "PROVINCE.md was not edited".
- **One rule decides all three the same way?** PASS (as practised) — the lesson rule
  "documentation localization is outside PROVINCE.md" is stated verbatim in rounds 32–35 and
  applied to r28/r29/r30 (r30 by name in both the round-35 lesson and the spot-check row;
  r28/r29 by the spot-check's note and by the round-34 S195/S205/S228 refusal of the same
  package rows). No Chinese documentation was ever admitted to the lane corpus.
- **Is the rule one a reader can find?** FAIL — it lives in `corpus/lessons/round-{32,33,34,35}.md`
  and in spot-check rows, not in the province document the rule itself cites as its home.
- **Counterexample:** `chinese-hyprland-window-rules-r16.md` — config-plane content in
  Chinese, refused by sweep; the stated rule's definition ("translation-lag surface") does
  not literally cover it, so the practised rule is wider than any sentence currently on
  record. Impacted axis: calibration/consistency of the discernment gate (a flipped or
  drifted statement would change the r16 verdict).
- **Smallest safe correction:** the one sentence in §5, inserted in `PROVINCE.md`'s
  `Refuses` block.

No tools installed; no installs needed. No files modified; this report is the only write.
