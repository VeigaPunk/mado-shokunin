# RevIdGuardQuarantine — round-43 w2 findings (id guard re-run, renumber map vs landed ids, quarantine spot-checks)

Seat `RevIdGuardQuarantine`, 2026-10-26. Attacks `.ufo/waves/round-43/assimilation/` (`id-guard.md`, `renumber-map.tsv`,
`quarantine-verdicts.md`) against the landed data at `1959770657f1f8665097c1aed4be6c1cbb07139f`
(base `a35cfdf…`, v1 freeze `b2e2efd…`, v2 freeze `496340dd…`). Read-only everywhere except this seat
dir; scratch `/fast/scratch/hyaku/mado-r43/RevIdGuardQuarantine/` deleted at the end; every citation is
a file in this seat dir or a lane path. Lane registry blobs re-derived from git (`git show <rev>:corpus/SOURCES.md`),
never from the working tree.

## 1. Guard re-run at the data commit — holds; delta is exactly the landed band

Round-prompt guard (round-43 `w1-dispatch.json`, seat `ExecAssimIdGuard`): on both sides
`grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' <file> | grep -oE 'S[0-9]+' | sort`, then `comm -12`.

| run | reg ids | staged ids | collisions |
|---|---|---|---|
| freeze `b2e2efd` (w1's run) | 226 | 147 | 34 |
| data commit `1959770` (this re-run) | 234 | 147 | 42 |

- Re-run **directly on the git object** (`git show 1959770:corpus/SOURCES.md | <guard> | wc -l` → 234;
  `… | comm -12 - staged.txt | wc -l` → 42): no scratch-copy dependency.
- Delta freeze→data: exactly `S290 S291 S292 S293 S294 S295 S296 S297` added, none removed
  (`comm -13` / `comm -23` over the two collision files).
- Byte-identical reproduction of w1's freeze run: `reg-ids-b2e2efd.txt` sha256 `76e986db…`,
  `staged-ids.txt` `079d7538…`, `collisions-b2e2efd.txt` `da4b74d2…` — each equals the corresponding
  artifact hash w1 published in `w1/ExecAssimIdGuard.md`.
- Completeness at the data commit: rows with ≥4 leading spaces = 0; rows matched at any indentation =
  234 (= the guard's reg count), so no registry row escapes the 0-3 window; duplicate ids in the
  registry = none (`sort | uniq -d` empty).
- Reading: the 8 new collisions are the landed ids meeting the staged rows that still hold those
  numbers (staged set contiguous S203-S349). Expected by construction — the guard is a pre-append
  check and the staged band rows were renumbered; the landed registry itself is collision-free.

Verdict: the guard claim survives at the data commit. [supports the landed data]

## 2. Guard proof — fires on an indented colliding row

Fixture `guard-proof/scratch-registry.md` (this seat dir, sha256 `43e738c6…`):

```
| id | source | kind |
|---|---|---|
| S001 | control row at column zero | docs |
  | S203 | staged-collision-probe, indented two spaces | docs |
    | S998 | four-space row, outside the guard window | docs |
```

- 0-3-space extractor over the fixture → `S001`, `S203`: the two-space row is recognized.
- `comm -12` against the staged set → `S203` — **nonempty**: the guard fires on an indented collision.
- Column-zero-only extractor (`^\|…`) → `S001` only; `comm -12` → 0 lines — the false-green the 0-3
  pattern exists to prevent (round-32 `registration.md:68-72`).
- Four-space row `S998` appears in neither extractor's output — the guard's measured blind spot
  (same as w1 `id-guard.md` §2; harmless for this registry, see §1 completeness).

## 3. Renumber map vs LANDED ids

Landed rows verified at `1959770` (blob `landed/SOURCES-1959770.md`, sha256 `b603fe42…`, lines 239-246):
S290 RegexMatchEngine.cpp, S291 DefaultFloatingAlgorithm.cpp, S292 Target.cpp, S293 WindowTarget.cpp,
S294 GeometricMovableAnimated.cpp (all `…/efb5099…/<path>`), S295 host-gkeep.conf,
S296 host-clients-r43.json, S297 gkeep-ui-excerpt.py. No row S298 or beyond exists. Registry diff
freeze→data: +10 −2 = the 8 new rows plus the 2 modified held rows; **S155 and S158 each gained
exactly one used-by item**, `, corpus/knowledge/hyprland-gkeep-geometry-r43.md` (byte-diff at chars
805-807→805-856 and 868-870→868-919; no other cell of either row changed). The landed entry
(`landed/entry-1959770.md`, sha256 `4d16b3fb…`) cites exactly {S155, S158, S290-S297}, each id twice
(one `source:` line at entry:3-12 + one prose mention).

### 3a. Mismatches (w1 map id → landed id)

| document | w1 map (`renumber-map.tsv` / `id-guard.md` §5) | landed | status |
|---|---|---|---|
| RegexMatchEngine.cpp | — no row (not staged-cited) | S290 | map gap |
| DefaultFloatingAlgorithm.cpp | S292 (pin) | **S291** | MISMATCH |
| Target.cpp | S293 (pin) | **S292** | MISMATCH |
| WindowTarget.cpp | S294 (pin) | **S293** | MISMATCH |
| GeometricMovableAnimated.cpp | S295 (pin) | **S294** | MISMATCH |
| host-gkeep.conf | S297 (pin) | **S295** | MISMATCH |
| host-clients-r43.json | — no row | S296 | map gap |
| gkeep-ui-excerpt.py | S299 (explicit: `renumber-map.tsv` row S312 reason "the lane pin S299 (gkeep-ui-excerpt.py)") | **S297** | MISMATCH |
| WindowRuleApplicator.cpp | S155 held | S155 held | match |
| HyprCtl.cpp | held S158 (`id-guard.md` §6 finding 1) | S158 held | match |
| view/Window.cpp | S164 held | **not cited** — the landed entry names no Window.cpp row; S164 gained no used-by | map row unused |
| gkeep ui.py (full file) | S300 new | not landed (entry cites the excerpt pin S297 instead) | dropped |
| docs.gtk.org `set_default_size` | S303 new | not landed | dropped |
| wiki.hypr.land 0.56.0 Window-Rules | S304 new | not landed | dropped |
| nerd-fonts glyphnames.json | S301 new | not landed | dropped |
| 8 × `lanes/mado/roundN/fetch/…` artifacts | S302, S305-S311 new | not landed | dropped |

Why the map is stale: it treated the pin band S290-S299 as fixed in registration order (its task
context: "the pinned ids S290-S299 map to the URLs in the context"), while the landed mapping resolved
two of the seven Hyprland pins onto held rows (S155, S158) and compacted the rest into S290-S297.

### 3b. Executing the frozen map today would mis-attach five documents

Five map rows target ids that in the LANDED registry hold different documents:

| map row (staged id → target) | map's reason | landed id now holds |
|---|---|---|
| S302 → S292 | "same document as the round-43 pin S292 (DefaultFloatingAlgorithm.cpp)" | Target.cpp |
| S303 → S293 | pin Target.cpp | WindowTarget.cpp |
| S304 → S294 | pin WindowTarget.cpp | GeometricMovableAnimated.cpp |
| S305 → S295 | pin GeometricMovableAnimated.cpp | host-gkeep.conf |
| S251 → S297 | pin host-gkeep.conf | gkeep-ui-excerpt.py |

This is the map's own "near-miss id reuse" hazard (`id-guard.md` §6 finding 4) realized between the
map and the landed data. The map's new-id targets S300-S311 remain free in the landed registry (max
landed id S297), so the map is still executable — but only after re-deriving the five pin rows.
[attacks `renumber-map.tsv` rows S251/S302/S303/S304/S305 and `id-guard.md` §5 rows 4-8]

### 3c. Is the landed mapping by document? YES, for what landed

- One id per document: each of the five pinned URLs appears exactly once in the whole landed registry
  (rows 239-243, document-occurrence scan); the three own-work receipts are unique; the two held
  documents reused held ids instead of new rows.
- No duplicate-document row was created. The only same-document pair touching the landed set is
  pre-existing: S018 (row 30, `github.com/…/blob/v0.56.2/src/debug/HyprCtl.cpp`) and S158 (row 170,
  raw form) — two URL forms of one document, mined 2026-10-19 and 2026-10-23. The round's used-by
  append went to S158 only, so the document's two rows are now asymmetric (S018 does not name the r43
  entry). [observation on the landed data; consistent with `id-guard.md` §6 finding 1]
- Coverage caveat: the landed mapping is by document over the ADMITTED subset only. The lesson
  (`landed/lesson-1959770.md:45-49`) admits 1 staged file and refuses 4 with reasons and flip
  conditions; the other 6 staged files — and the 13 documents the map allocated S300-S311 for — have
  neither a landed row nor a recorded refusal. The registration bar was "at least one staged file
  refused", so this is within spec, but the map's 12 new-id allocations are dead letters, and a reader
  of `renumber-map.tsv` alone would believe 19 documents were mapped into the registry.
  [attacks `id-guard.md` §5 id-budget claim "12 new ids S300-S311"]

### 3d. Frozen w1 prose defect

`id-guard.md` §6 finding 2 says "the other six" but lists five ids "(S290, S291, S294, S295, S296)" —
S293 is omitted; the six staged ids outside the citation set in the reserved band are S290, S291,
S293, S294, S295, S296. [attacks `.ufo/waves/round-43/assimilation/id-guard.md` §6 finding 2; frozen
w1 artifact, reported not edited]

## 4. Quarantine spot-checks (3 of 13 slice rows, re-fetched 2026-10-26)

Register `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`
sha256 `5afe1810…` — byte-identical to the hash `quarantine-verdicts.md` §0 records. Slice sha256
`d9ea803d…` matches §1. Register legend (register:15-16): `payload-absent` = "every relevant source
fetched cleanly and the quote is in none of them" — "**the fabrication class**"; `unreachable` = "the
source could not be fetched, so the quote was never checked".

1. **S199 (register:349, `unverifiable`) — HOLDS.** Direct re-fetch of
   `https://blog.csdn.net/2301_76324845/article/details/149787804` → HTTP 521, 2 260 B JS-challenge
   stub (`quarantine/s199-csdn-2301_76324845.body`, sha256 `a5a6ce51…`). Reader proxy → HTTP 200,
   66 998 B (`quarantine/s199-proxy.txt`, sha256 `9abaf349…`), and the quoted rule is present at proxy
   line 152: `windowrule = opacity 0.80 $& 0.80 $& 1,class:^([Cc]ode)$`. Both legs reproduce (direct
   unreachable; proxy reachable and carrying the quote). Body sizes differ from w1's run
   (2 263 / 71 957 B) — stub and proxy output vary per fetch; the verdict does not depend on sizes.
2. **S200 (register:350, `unverifiable`) — HOLDS.** Direct re-fetch of
   `https://blog.csdn.net/lxyoucan/article/details/164457293` → HTTP 521, 2 229 B stub
   (`quarantine/s200-csdn-lxyoucan.body`, sha256 `62721e72…`).
3. **S189 (register:141, `payload-absent`) — FALSIFIED.** The row pins
   `https://raw.githubusercontent.com/hyprwm/Hyprland/efb5099…/src/managers/EventManager.cpp` and its
   absence evidence claims (register:141): "cited source, companion URLs and local artifacts were all
   checked; the quote is in none of them". Re-fetch → HTTP 200, 6 479 B
   (`quarantine/s189-EventManager.cpp`, sha256 `eea605df…`), and the quoted line is present at
   **line 128**, byte-identical to the register's quote including the 13-space run between `auto` and
   `eventString`:
   `    auto             eventString = std::format("{}>>{}\n", event.event, data.substr(0, 1024));`
   The register's `payload-absent` is "the fabrication class" by its own legend, and its absence
   evidence is false for the cited source at the row's own pinned commit. `quarantine-verdicts.md` §6
   records "no action — not cited by the theme" for S189 without testing the quote, and w1 explicitly
   issued no verdict on the twelve unnamed rows (`w1/ExecQuarantineSlice.md` Risks) — new evidence,
   not a re-report.
   [INFERENCE] plausible cause: the register generator's quote census ran against a different revision
   or path of `EventManager.cpp` (its eleven match folds failing there), while the row's URL cell pins
   `efb5099` where the line exists; not determinable from the register alone.

Consequence: at least one of the six mado `payload-absent` rows in the slice is misclassified; the
register's fabrication class is not reliable without per-row re-verification. The other five
payload-absent rows (S195, S201, S205, S224, S228) were NOT re-fetched here (S224 is a local cache
file, S228 a campaign path, S195/S201/S205 remote) — given S189, they should be re-verified before any
reader acts on them.

## 5. What I did not check

- The C2 counter, the entry's quote/locator binding, the lesson's other sections, README/PROVINCE/
  SKILL/QUALITY rows — other seats' items; my entry check is the cited-id set only.
- The remaining 10 slice rows (no re-fetch; the S209-family rows have no URL to fetch).
- w1's +17 offset claim and the join-evidence script (out of scope; the slice and register sha256s
  match, which pins the inputs).

## 6. Receipts (all in this seat dir)

| file | what |
|---|---|
| `reg-ids-1959770.txt` / `reg-ids-b2e2efd.txt` | guard output over the landed / freeze registry (234 / 226 ids) |
| `staged-ids.txt` | guard output over `SOURCES.append.md` (147 ids; sha256 `079d7538…` = w1's) |
| `collisions-1959770.txt` / `collisions-b2e2efd.txt` | 42 / 34 colliding ids |
| `guard-proof/scratch-registry.md` | the indented-collision proof fixture |
| `landed/SOURCES-1959770.md`, `landed/SOURCES-b2e2efd.md` | the two registry blobs (sha256 `b603fe42…`, `df130e81…`) |
| `landed/entry-1959770.md`, `landed/lesson-1959770.md` | the landed entry and lesson |
| `quarantine/s199-csdn-2301_76324845.body`, `s200-csdn-lxyoucan.body`, `s189-EventManager.cpp`, `s199-proxy.txt` | the four re-fetch bodies |

## 7. Tools

None installed (grep, sort, comm, wc, curl, sha256sum, python3 from the base system; no pacman, no uv,
no npx). Network: 4 read-only GETs (3 direct + 1 reader proxy). No host compositor read, no input
injection, no git mutation anywhere; scratch deleted at the end.

Report: .ufo/waves/round-43/w2/RevIdGuardQuarantine.md
