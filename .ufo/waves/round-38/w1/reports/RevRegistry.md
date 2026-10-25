# RevRegistry — round-38 wave-1 report (SOURCES.md rows S221/S253/S258/S277 + S158/S187 used-by)

Agent: `L1Mado38.RevRegistry` (leaf reviewer). Scope: audit `corpus/SOURCES.md` at
`master` HEAD (commit `b6c1d31`; the data landed in `245065c`) against the 11-column
SOURCES contract, the used-by ↔ entry citation closure, the S158/S187 used-by appends,
and the fleet census validator. Read-only on all lane files; sandbox `/tmp/mado38-RevRegistry`.
No tools installed (used `git`, `gawk`, `grep`, `curl`, `sed` — all present).

## 1. The diff under audit (commit 245065c)

`git -C <LANE> show 245065c -- corpus/SOURCES.md` → 1 file, +6/−2:

- `S158` used-by: `…workspace-rules-r27.md` → `…workspace-rules-r27.md, corpus/knowledge/request-socket-live-bound-r8.md` (append only).
- `S187` used-by: `corpus/knowledge/ipc-contract-r25.md` → `corpus/knowledge/ipc-contract-r25.md, corpus/knowledge/request-socket-live-bound-r8.md` (append only).
- Four new rows appended after `S217` (lines 220–223): S221, S253, S258, S277.

## 2. Schema checks (11 columns, no `|` in cells, recheck cadences) — PASS

Commands (run on `<LANE>/corpus/SOURCES.md`):

```
gawk -F'|' '/^\|[[:space:]]*S[0-9]+[[:space:]]*\|/ { n++; if (NF!=13) print "NF_BAD line "NR" NF="NF" id="$2;
  id=$2; gsub(/[[:space:]]/,"",id); if (seen[id]++) print "DUP "id;
  if (prev!="" && id+0<prev+0) print "ORDER "prev" -> "id" at line "NR; prev=id } END{ print "rows="n }'
```
Output: `rows=211`; no `NF_BAD`, no `DUP`, no `ORDER`. Header row (`| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |`) also `NF=13` at line 11. `grep -c '\\|'` → 0 (no escaped pipes either). Registry section spans lines 9–224 (`## Registry` @9, `## Paths` @225); the four new rows sit inside, after the last pre-existing row S217 (line 219), ids monotonic (S217 → S221 → S253 → S258 → S277). S218–S220 are an acknowledged gap (corpus/lessons/round-38.md finding 3), not a defect.

Per-row cadence/status/kind/tier (all enum-valid, E05–E09 clean):
- S221 (line 220): docs/A, mined, opened 2026-10-25, recheck `on-release`.
- S253 (line 221): code/A, mined, opened 2026-10-25, recheck `on-release`.
- S258 (line 222): own-work/A, mined, opened 2026-10-25, recheck `on-change`.
- S277 (line 223): docs/C, mined, opened 2026-10-25, recheck `90d`.
- The `:19-20` anchor is false for the pinned artifact. **Registry-only defect:** the entry body
  `request-limits-upstream-r31.md` does not repeat the error — it cites only `:118`/`:166`
  (both correct); the fix is confined to the SOURCES.md row locator.
  - S221 row (line 220) states page revision "Last updated on May 2, 2026"; the receipt carries `<time datetime="2026-06-13T19:18:41.000Z">June 13, 2026</time>` (and the staged row says `2026-06-13T19:18:41Z`). "May 2, 2026" is S187's revision (the IPC page) — copied. The anchor's revision stamp is wrong.
## 3. Fleet census validator — run, exit 0, lane ok

Command (exactly as scoped):
```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado
```
Output (verbatim):
```
mado	W04	S030 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
mado	W04	S042 duplicate url wayland.freedesktop.org/extras.html across scopes
mado	W04	S045 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
mado	W04	S097 duplicate url raw.githubusercontent.com/basecamp/omarchy/v3.8.4/themes/matte-black/colors.toml across scopes
mado	W04	S119 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Lib/imaplib.py across scopes
mado	W04	S120 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst across scopes
mado	W04	S121 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst across scopes
mado	W01	S277 tierC mined used-by=corpus/knowledge/request-socket-live-bound-r8.md
mado	ok	/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md
EXIT=0
```
No E-codes. The 7 W04s are pre-existing (round-26 lesson already records "the same 7 pre-existing W04"). `W01 S277` is the expected consequence of the community-tier source being actually cited (tier C, mined, non-`—` used-by) — the registration declares S277 "at community-tier weight"; warning, not an error, does not affect lane clean status.

## 4. used-by ↔ citation closure — PASS on the lane's operative convention; one frontmatter defect (F1)

Operative convention (from the frozen instruments/lessons): an entry "cites" a row if the row id appears in the entry's `source:` frontmatter (the c1 counter engine derives cited ids exactly this way: `c1-r38-event-ground.py` lines ~176–179 collect `source:`-line ids from the first 15 lines; clause c, lines 201–205, then requires one mined 11-cell registry row per id whose used-by names the entry). Forward+reverse checks:

| Row | used-by cell (HEAD) | Entries whose `source:` names it | Verdict |
|---|---|---|---|
| S221 | `corpus/knowledge/hyprctl-flags-r28.md` | hyprctl-flags-r28.md:8 (source: S221; OBS S221 ×2) | ✓ exact |
| S253 | `corpus/knowledge/request-limits-upstream-r31.md` | request-limits-upstream-r31.md:9 (source: S253; OBS S253 ×2) | ✓ exact |
| S258 | `corpus/knowledge/request-socket-live-bound-r8.md` | **none** in a `source:` line; r8 body OBS-cites (r8:46-49), README index lists it, registration says "cited by E4" | ⚠ see F1 |
| S277 | `corpus/knowledge/request-socket-live-bound-r8.md` | request-socket-live-bound-r8.md:9 (source: S277; OBS S277) | ✓ exact |
| S158 | rule-attribution-r24.md, animation-table-r26.md, workspace-rules-r27.md, **request-socket-live-bound-r8.md** | rule-attribution-r24.md:1; animation-table-r26.md:7; workspace-rules-r27.md:8; r8:9 | ✓ exact (append verified in §1) |
| S187 | ipc-contract-r25.md, **request-socket-live-bound-r8.md** | ipc-contract-r25.md:10; r8:9 | ✓ exact (append verified in §1) |

No other knowledge entry cites S221/S253/S258/S277 (grep over `corpus/knowledge` finds exactly the entries above). All used-by paths exist on disk (E11 clean). **S158/S187 appends: only `request-socket-live-bound-r8.md` added to each; no existing entry dropped** — confirmed from the raw diff.

Observation (not a defect): `hyprctl-flags-r28.md:31` and `request-limits-upstream-r31.md:36` mention S187/S158 in `**INF**` cross-references without sourcing them; under the lane's convention those are cross-references to prior ground, not citations, and correctly do not appear in used-by.

### F1 (medium) — r8 entry frontmatter omits S258; the S258↔r8 binding is enforced by nothing frozen
`corpus/knowledge/request-socket-live-bound-r8.md:9` `source:` line names only S158, S187, S277. But the entry body OBS-cites S258 (r8:46-49, the 0700/0755 transport facts), the README index row lists `source:` S158, S187, S277, S258 (`corpus/README.md:65`), S258's used-by names r8, and the frozen registration says "S258 (own-work stat receipt, cited by E4)" (`.ufo/waves/round-38/registration.md:98`). The c1 counter derives cited ids from `source:` lines only, so S258's used-by binding is never exercised by the frozen counter — the frontmatter omission hides the binding from the instrument. Fix: add S258 to r8's `source:` line.

## 5. Findings

### F2 (medium, high) — all four new rows carry a false byte-size claim in the anchor cell; receipts are genuine (shas match) but sizes contradict them
Direct evidence (receipt hashes computed; upstream URLs re-fetched live this audit):

| Row | Size claimed in row | Receipt on disk (.ufo/waves/round-38/fetch/) | Live fetch of the row's URL | Staged source row (shokuknow merge/mado SOURCES.append.md) |
|---|---|---|---|---|
| S221 | `35046 B` (line 220) | S221.bin = 306865 B, sha `35046ba0dc1dd1db…` | 306865 B, same sha (wiki.hypr.land/0.56.0/…/Using-hyprctl/) | 306865 B, sha prefix `35046ba0…` |
| S253 | `39464 B` (line 221) | S253.bin = 11602 B, sha `3ba8e461bd466a8a…` | 11602 B, same sha (raw.githubusercontent.com/hyprwm/Hyprland/a1c2428…/src/ipc/s1/Unix.cpp) | 11602 B, sha prefix `3ba8e461…` |
| S258 | `receipt 1401 B` (line 222) | stat-sockets.txt = 673 B, sha `fcc608203f66879f…` | n/a (own-work) | n/a |
| S277 | `19737 B` (line 223) | S277.bin = 35421 B, sha `ff561fe0d09641db…` | 35421 B, same sha (chriskearney/chonkstep main — see F3) | no byte pin (live `main` URL) |

The shas all match the receipts and the live upstream bytes (provenance holds), so every size cell is a false claim about the pinned artifact. S221's `35046 B` is literally the first five hex chars of its sha (`35046ba0…`) + " B" — a transcription artifact; the staged row proves the correct value is 306865 B. S253's size and line anchors are corrupted relative to both the receipt and the staged row (see F4). S258's `1401 B` vs 673 B and S277's `19737 B` vs 35421 B likewise. Recommendation: correct the four size cells to the receipt sizes (or state the measured artifact explicitly).

### F3 (medium) — S277's URL cell is dead at audit time (HTTP 404), and its pinned commit is unresolvable
Row URL: `https://raw.githubusercontent.com/iconidentify/chonkstep/707cf7f8b39d0b4e2cba46d0a2559b562d8821ce/docs/hyprland-ipc.md` → **404** (verified; also 404 under the renamed repo). The repo was renamed `iconidentify/chonkstep` → `chriskearney/chonkstep` (GitHub API redirect confirms; `main` under the old name still serves 200). The receipt (S277.bin, 35421 B) is byte-identical to today's file at `chriskearney/chonkstep main/docs/hyprland-ipc.md` (sha `ff561fe0…`), so the evidence is preserved — but the row's URL does not resolve on the day it was opened, and the pinned commit cannot be served under either name. The GATE quote ("There is no length prefix or newline.") and `[[BATCH]]` are verbatim in the receipt. Recommendation: point the row's URL at the renamed repo with a resolvable ref (or keep the committed receipt as the only live artifact and say so).

### F4 (low-medium) — S253 row anchor errors: `:19-20` and the "May 2, 2026" stamp don't match the pinned receipt
- S253 row (line 221) anchors the constants at `src/ipc/s1/Unix.cpp:19-20`; the pinned receipt (and the live upstream file, and the staged row) carry `REQUEST_LIMIT`/`FOLLOW_QUEUE_LIMIT` at lines **43–44** (`:118` readRequest check and `:166` addFollowData check are correct). The `:19-20` anchor is false for the pinned artifact.
- S221 row (line 220) states page revision "Last updated on May 2, 2026"; the receipt carries `<time datetime="2026-06-13T19:18:41.000Z">June 13, 2026</time>` (and the staged row says `2026-06-13T19:18:41Z`). "May 2, 2026" is S187's revision (the IPC page) — copied. The anchor's revision stamp is wrong.

### F5 (low) — the row's 404-at-host-tag claim is true but unpinned, and the parenthetical is confusing
S253's teaches cell: "the file returns 404 at the host's tag (receipt .ufo/waves/round-38/fetch/S187.bin is unrelated - see S187)". The 404 claim is **true** (I re-verified live: `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/ipc/s1/Unix.cpp` → HTTP 404), but it has no receipt of its own, and the only named receipt (S187.bin, 268731 B) is S187's own IPC-page receipt — correctly disclaimed, but the wording invites misreading S187.bin as the 404 receipt. Suggest a clearer phrasing (e.g. "no receipt; verified 404 at fetch time").

### F6 (low, residual risk) — id S258 collides with the shokuknow staged register's assignment
Round-38 adopted the stat receipt under S258 (ledger: S212a → S258), but the staged register holds a *different* document under S258 (`Hyprland (ArchWiki, English)` drift row, `merge/mado/SOURCES.append.md:62`). S221/S253/S277 reuse staged ids for the same documents (clean). The lesson's "the three adopted new ids … were free" holds only against the held registry; if the staged ArchWiki entry is ever admitted, E03 duplicate-id (or a forced renumber) results. Not a current violation.

## 6. Verification gaps

- I did not re-open the historical 404/byte-identity of the staged package's original fetch moments; F3/F4 rely on live re-fetch + receipt hashes, which are conclusive for the *current* state.
- The S258 `1401 B` figure has no staged counterpart I could locate (no S212a row found in `merge/mado/SOURCES.append.md` by grep); the committed receipt is 673 B.
- The c1 counter's use of `source:`-only ids (F1) is an observation about the frozen instrument, not a counter failure; C1's reviewer owns that instrument.

## 7. Verdict

- Schema (11 columns, no pipes in cells, cadences incl. S258=`on-change`, S221/S253=`on-release`, S277=`90d`): **PASS**.
- Fleet validator (`sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado`): exit 0, `mado ok` (7 pre-existing W04 + W01 S277): **PASS**.
- used-by closure incl. S158/S187 appends (only `request-socket-live-bound-r8.md` added, none dropped): **PASS** (with F1 frontmatter defect).
- Findings: F1 (r8 frontmatter omits S258), F2 (false size cells in 4/4 new rows), F3 (S277 URL 404), F4 (S253 `:19-20` anchor, S221 "May 2" stamp), F5 (unpinned 404 claim), F6 (staged S258 id collision risk). All evidence above is quoted from the lane's HEAD tree, receipts, and live fetches performed this audit.

## 8. Corroboration (ScoutS253, cross-lane)

Agent `L1Mado38.ScoutS253` independently confirmed the S253 row findings: `:19-20`
is not a stale-revision cite — all three upstream revisions of `src/ipc/s1/Unix.cpp`
(ff24e175/88c6386/59177602) carry the constants at `:43-44` (`:19-20` is
`using namespace IPC::Socket1;` + blank); `39464 B` should be `11602 B` (wc -c,
GitHub contents API, digest match across 4 copies); sha256 `3ba8e461…` correct;
receipt S253.bin byte-identical; entry body does not repeat the error; neither
`c2-r38-request-ground.py` nor `sources-census.sh` validates locators/byte counts.
Full evidence: `.ufo/waves/round-38/w1/reports/ScoutS253.md`.

## 9. Post-fold status (HEAD ff81aaf) — two residue items

The fold that applied this report's findings repaired the F1/F2/F4 class at current HEAD
(verified by re-reading `corpus/SOURCES.md` lines 220–223): S221 now reads
`306865 B` / "Last updated on June 13, 2026" (the date error I flagged was also fixed);
S253 now reads `Unix.cpp:43-44` / `11602 B`; S258 reads `receipt 673 B`; S277 reads
`35421 B`. All six rows' byte figures now match their receipts. Two items remain open:

### Residue A (new, in scope) — r8 entry anchor cites the wrong line for the short-read break
`corpus/knowledge/request-socket-live-bound-r8.md:24` says the 1023-byte chunk loop is
`(`:2274` `read(ACCEPTEDCONNECTION, readBuffer.data(), 1023)`, `:2278` break on a short
read)`. In `S158.bin`, `:2274` is correct, but `:2278` is `request += recvd;`; the guard
`if (messageSize < 1023)` is `:2279` and `break;` is `:2280` (verbatim, sed -n
'2274,2282p' on S158.bin). The locator should read `:2279`/`:2280`.

### Residue B — S277's pinned commit does not exist; the renamed URL is still dead
HEAD still pins `https://raw.githubusercontent.com/chriskearney/chonkstep/707cf7f8b39d0b4e2cba46d0a2559b562d8821ce/docs/hyprland-ipc.md`.
The owner spelling was corrected (iconidentify → chriskearney), but the commit itself is
not in the repo: `git fetch --depth=1 origin 707cf7f8…` → `fatal: remote error:
upload-pack: not our ref 707cf7f8…`; control `git fetch --depth=1 origin c37fbe3e…`
(repo HEAD per `git ls-remote`) succeeds. Raw 404s for both owner spellings; the receipt
`S277.bin` is byte-identical to today's `main` document (sha `ff561fe0…`). Correct fix:
pin `c37fbe3e439dc27db9ce8176546febb58680dfc5` (the snapshot the receipt actually matches),
or relabel the locator as `main` with the recheck cadence.

Corroborated by ScoutS253 (§7.2b): `c37fbe3e` serves a blob **identical** to
`S277.bin` (sha256 `ff561fe0…`) under **both** owner spellings (HTTP 200; CMP
identical), so the re-pin needs no receipt change and no owner choice — the row's
locator/digest/committed receipt become mutually consistent at last. The dead pin was
never resolvable under either spelling; the fold's owner rename alone was a no-op for
that row.

### Tip-state update (HEAD 919d7d0, verified 2026-10-25)

- **F1 fixed** — r8's `source:` line now ends `… S258 — host socket stat receipt
  `.ufo/waves/round-38/fetch/stat-sockets.txt` (own-work)` (r8:9). The S258↔r8
  binding is now in the frozen counter's `ids` set.
- **Residue A still open** — `corpus/knowledge/request-socket-live-bound-r8.md:24`
  still reads "`:2278` break on a short read"; the corrected `:2279`/`:2280` was
  **never committed**. Commit `5e4c2ba` ("round-38 r8 entry fixes (RevEntryBound
  F2/F4/F6): short-read break :2279-2280, EVENT framing escape note, stray directory
  word") contains only the F6 wording fix: `git show 5e4c2ba` diff = 1 file, 1+/1−
  (`-directory \`directory /run/user/1000/hypr/\` carries mode 0700…` →
  `+the instance directory \`/run/user/1000/hypr/\` carries mode 0700…`).
  `git log -S ':2279' -- corpus/knowledge/request-socket-live-bound-r8.md` is empty;
  `grep -c 'S186\|escap'` on r8 = 0 (F4's escape note/S186 pointer also absent). A
  reader auditing from the commit log alone would wrongly clear both residues.
- **Residue B still open** — S277's row still pins
  `…/chriskearney/chonkstep/707cf7f8b39d0b4e2cba46d0a2559b562d8821ce/docs/hyprland-ipc.md`
  at HEAD; the commit remains unresolvable (`git fetch --depth=1 origin 707cf7f8…`
  → "not our ref"). Verified fix: re-pin `c37fbe3e439dc27db9ce8176546febb58680dfc5`
  (blob byte-identical to `S277.bin`, sha `ff561fe0…`, under both owner spellings).
