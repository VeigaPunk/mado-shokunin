# RevDomCounter — review of `quality/counters/c2-r38-request-ground.py` (round 38, wave 1)

Scope: the C2 domain counter (`PRED-C2-r38-v1`, 247 lines) against its role — admission
counter for the three request-socket entries — and against the frozen registration
(`.ufo/waves/round-38/registration.md`). Lane bounds honored: zero writes to lane
production files; every mutation below lives in my sandbox clone
`/tmp/mado38-RevDomCounter/sb` (`git clone -q --no-local`, commits as `user.name=s
user.email=s@i`, restored to baseline afterward). No tools installed (python3/git
sufficed).

Revisions measured: lane HEAD `bb1adce40fdbe9de9b2040f70bc64cee7a0ab0c5` at first run;
the tip moved to `3f14bd2d7c3aa067091bc52e63fb8abdd944c3b8` during this review (sibling
errata commit — `git show --stat 3f14bd2` touches only `.ufo/waves/round-38/w1/reports/*`
and `LOG.md`; `git diff --stat bb1adce 3f14bd2 -- corpus quality` is empty). Both tips
score identically. Base for preconditions: `f6e3247f73152a39afb86066af48f3cedf95fb0a`.
The tip kept moving while peer findings were folded — `b8400aa` (seat-fix fold:
registry row corrections, r8 header +S258, discrimination-gate sandbox confinement)
and errata through `3674cf2`, `23a0e0f`. The request-ground counter itself is untouched
since the freeze (its log shows only `58e55ec` at every tip checked); at `23a0e0f` it
still prints `admitted=3/3 TARGET_MET`, with r8's ids now `S158,S187,S258,S277` — the
fold made S258 a checked id (F4) — and all six row byte figures now match the pinned
bytes (F9).

## 1. Run at HEAD — all clause letters, quoted

`cd LANE && python3 -I quality/counters/c2-r38-request-ground.py --repo . --rev master`:

```
PRED-C2-r38-v1 entry=corpus/knowledge/hyprctl-flags-r28.md a=1 b=1 c=1 d=1 e=1 f=1 g=1 l=1 ids=S221 lineage=3/3 ok=1
PRED-C2-r38-v1 entry=corpus/knowledge/request-socket-live-bound-r8.md a=1 b=1 c=1 d=1 e=1 f=1 g=1 l=1 ids=S158,S187,S277 lineage=5/3 ok=1
PRED-C2-r38-v1 entry=corpus/knowledge/request-limits-upstream-r31.md a=1 b=1 c=1 d=1 e=1 f=1 g=1 l=1 ids=S253 lineage=5/3 ok=1
PRED-C2-r38-v1 admitted=3/3 verdict=TARGET_MET rev=bb1adce40fdbe9de9b2040f70bc64cee7a0ab0c5 base=f6e3247f73152a39afb86066af48f3cedf95fb0a
EXIT=0
```

Base run (`--rev f6e3247…`): every entry `a=0 … l=0`, `admitted=0/3 verdict=TARGET_MISSED`,
`EXIT=1` — matches the registration's declared "before". No `SETUP ground_held_at_base`
at base, i.e. the five `SURFACE_TOKENS` are base-clean (but see F3: that set is not the
TARGETS set).

## 2. TARGETS tokens vs corpus/knowledge — base precondition and HEAD exclusivity

`git -C LANE grep -F -n -e <token> <rev> -- corpus/knowledge`, per token:

| token | base f6e3247 | HEAD |
|---|---|---|
| `select instance` | 0 hits | only `hyprctl-flags-r28.md:16` |
| `force state refresh` | 0 hits | only `hyprctl-flags-r28.md:16` |
| `poll(pollfds` | 0 hits | only `request-socket-live-bound-r8.md:19` |
| `1023` | **2 hits** | `r8.md:23,24` + `request-limits-upstream-r31.md:33` + pre-held `event-delivery-limits-r26.md:53,82` |
| `REQUEST_LIMIT` | 0 hits | only `request-limits-upstream-r31.md:18,23` |
| `FOLLOW_QUEUE_LIMIT` | 0 hits | only `request-limits-upstream-r31.md:20,25` |
| `flag list` (registration-frozen, not a TARGETS token) | **2 hits** | `hyprctl-flags-r28.md:11,15,16,47` + pre-held walker files |
| `length prefix` / `BATCH` (registration claim list) | 0 hits | r8 only |

Base hits, full lines:

- `f6e3247…:corpus/knowledge/walker-deep.md:314: **OBS** — `walker --help` (full flag list, measured):`
- `f6e3247…:corpus/knowledge/waybar-walker-plane.md:480: - Version-bound, dated, not re-verified on 2.17.2: the `walker --version` print (`:38`, `:197`, `:405`) and the `walker --help` flag list (`:196-197`).`
- `f6e3247…:corpus/knowledge/event-delivery-limits-r26.md:53: most 1023 characters per call, so a long event arrives as a truncated head plus a tail parsed`
- `f6e3247…:corpus/knowledge/event-delivery-limits-r26.md:82: read is 1023 characters); "dropped after 64 queued events" (the send buffer fills first);`

**F1 (major) — coded predicate ≠ frozen predicate for the flags entry's token set.**
The registration freezes: "`corpus/knowledge/hyprctl-flags-r28.md` (tokens `flag list`,
`select instance`)". The counter's `TARGETS` (lines 51–52) is
`("select instance", "force state refresh")`. `flag list` appears nowhere in the counter
(not in `TARGETS`, not in `SURFACE_TOKENS`); `force state refresh` is enforced but was
never frozen. The counter has exactly one commit (`58e55ec`, the freeze) and is
byte-identical at HEAD (`git diff --stat 58e55ec HEAD -- <counter>` empty), so this is a
**freeze-internal** inconsistency: the registration and the counter frozen in the same
commit declare different token sets, and the docstring does not enumerate tokens — the
registration's list is the only declaration. Probe: sandbox T2 removes all 4 `flag list`
occurrences from the entry → still `admitted=3/3`; T3b removes `force state refresh` →
`f=0 l=0 ok=0`, `admitted=2/3 TARGET_MISSED`. The swap is load-bearing.

**F2 (major) — the registration's unheld-ground claim is false for `flag list`.**
Registration: "`git grep` at the base finds no `flag list`, … in `corpus/knowledge`."
Actual base grep: 2 hits (walker-deep.md:314, waybar-walker-plane.md:480, quoted above).
Decisive probe (sandbox T5): adding `flag list` to `SURFACE_TOKENS` →
`PRED-C2-r38-v1 SETUP ground_held_at_base corpus/knowledge/event-delivery-limits-r26.md:1023,corpus/knowledge/walker-deep.md:flag list,corpus/knowledge/waybar-walker-plane.md:flag list`, exit 2 —
with the frozen token the counter cannot run at any revision. The edge class (hyprctl
request-socket flags) is genuinely new — the base hits are about `walker --help` — but
the token as frozen is base-held, and the registration's factual claim is wrong.

**F3 (medium) — precondition token set ≠ TARGETS token set; `1023` is base-held.**
`SURFACE_TOKENS` (lines 102–103, 5 tokens) omits the TARGETS token `1023`. It is held at
base (`event-delivery-limits-r26.md:53,82` — the **event** socket's 1023-character read),
so the docstring's blanket "the ground is unheld at the base" is false for that token as
a literal, and the precondition structurally cannot scan it (T5: adding `1023` → SETUP
exit 2). Mitigations verified: clause f still enforces `1023` in body+receipt (T4:
removing the two `1023` occurrences from r8 → `f=0 ok=0`, `admitted=2/3`), and the
receipt-side hit is the real chunk-read — S158.bin contains `1023` exactly twice, both in
`read(ACCEPTEDCONNECTION, readBuffer.data(), 1023)` / `if (messageSize < 1023)` context,
not by chance. Residual: the token does not discriminate the new request-side bound from
the pre-held event-side fact; the same docstring phrase "frozen surface tokens" denotes
two different sets (precondition 5, clause f 6).

## 3. Clause c — 11-cell / mined / used-by per id

Header confirms cell semantics: `| id | source | kind | tier | scope | anchor | teaches |
status | opened | recheck | used-by |` → status is cell 7, used-by cell 10, 11 cells
total. Verified per cited id at HEAD (exactly one row each; a duplicate-id scan over the
whole `## Registry` section returns none):

- S158: 11 cells, `mined`, used-by = `…rule-attribution-r24.md, …animation-table-r26.md, …workspace-rules-r27.md, corpus/knowledge/request-socket-live-bound-r8.md` ✓
- S187: 11 cells, `mined`, used-by = `…ipc-contract-r25.md, corpus/knowledge/request-socket-live-bound-r8.md` ✓
- S221: 11 cells, `mined`, used-by = `corpus/knowledge/hyprctl-flags-r28.md` ✓
- S253: 11 cells, `mined`, used-by = `corpus/knowledge/request-limits-upstream-r31.md` ✓
- S277: 11 cells, `mined`, used-by = `corpus/knowledge/request-socket-live-bound-r8.md` ✓

Teeth confirmed (sandbox T8: S221's used-by no longer names the entry → `c=0 ok=0`,
`admitted=2/3 TARGET_MISSED`).

### F9 (medium) — clause c is shape-only: row locators and byte figures are never resolved against the pinned receipts

Triggered by ScoutS253's message; every item below independently verified against the
committed bytes at HEAD:

- **S253's anchor cell cites `src/ipc/s1/Unix.cpp:19-20` for REQUEST_LIMIT /
  FOLLOW_QUEUE_LIMIT.** In the pinned `S253.bin` the constants are at `:43-44`
  (`static constexpr size_t REQUEST_LIMIT      = 1024 * 1024;` / `…FOLLOW_QUEUE_LIMIT =
  64 * 1024;`); `:19-20` is `using namespace IPC::Socket1;` plus a blank line. The
  cell's other locators `:118` and `:166` are exact. Repaired by fold
  `b8400aa` (anchor now `:43-44`).
- **Byte figures wrong in 4 of 6 rows** (row figure vs actual pinned bytes):
  S221 `35046 B` vs 306865 B — and `35046` is S221's own sha256 prefix (`35046ba0…`), a
  paste slip; S253 `39464 B` vs 11602 B; S258 `1401 B` vs 673 B; S277 `19737 B` vs
  35421 B. S158 (97582 B) and S187 (268731 B) are correct. Fold `b8400aa` repaired all
  four — all six row figures match the pinned bytes at tip `23a0e0f` (a data fix; the
  counter gained no size check).
- **S187's anchor locators do not resolve in the committed blob at all.** The cell says
  "rendered text `:235` (two UNIX sockets), `:239` (`.socket.sock`), `:248`
  (`.socket2.sock`), `:251` (event framing)"; the pinned S187.bin is raw HTML and those
  lines are `>`, blank, blank, `</a>`. The constructs live elsewhere (`.socket.sock`
  :13/:1314, `.socket2.sock` :1320, "completely synchronously" :2855), so the locators
  reference a text rendering that is not committed — no receipt-byte check could ever
  confirm them as written.
- **Third locator class (ScoutS253, peer-verified with quoted fetch output; not re-run
  here): a locator naming a ref that does not exist.** S277's row pins commit
  `707cf7f8b39d0b4e2cba46d0a2559b562d8821ce`; `git fetch --depth=1 origin 707cf7f8…`
  returns `fatal: remote error: upload-pack: not our ref 707cf7f8…`, a control fetch of
  the repo's HEAD sha returns `commit`, all 260 refs lack the sha, and raw/codeload 404
  at both owner spellings. The receipt is byte-identical to current `main` — the row
  pins a commit that never existed while the receipt is a `main` snapshot. Fold
  `b8400aa` renamed the owner (iconidentify→chriskearney) but kept the sha, so the pin
  is still dead at tip `23a0e0f`. This generalises the S187 case: both are "the cited
  thing is not in the repo", differing only in kind (rendering vs ref).
- **Correction (ScoutS253): S158's locator is sound — an earlier draft of this report
  misattributed a 404 to it; withdrawn.** ScoutS253's Item 5 found `src/debug/HyprCtl.cpp`
  absent at `a1c2428f…` (S253's pinned commit, upstream current — the client moved to
  `hyprctl/src/main.cpp` there), NOT at `efb50993…`; at the host tag the file exists and
  their four-way probe (raw fetch 200, 97582 B, sha `798b7c6c…` == pin; `cmp` IDENTICAL
  vs S158.bin; git tree entry; `git cat-file` blob sha match) confirms the receipt is
  that file's bytes. Its request loop (`:2271-2281`) brackets the read/guard/break
  lines I verified in the blob (`:2274`/`:2279`/`:2280`; the poll sits just before at
  `:2264`). The file-not-at-commit fact is real but belongs to S253's contrast target
  and explains why the r31 entry's contrast is against the host's tag — an
  upstream-restructure fact, not a registry defect. The "cited thing is not in the
  repo" class stands at two verified instances (S187 rendering, S277 ref).
- **Entry-level locators fare better:** r8's S158 refs `:2264` (poll) and `:2274` (read)
  are exact; r31's `:118`/`:166` are exact. Correction (ScoutS253, confirmed against the
  blob): `:2278` is `request += recvd;`, the short-read guard `if (messageSize < 1023)`
  is `:2279` and the `break;` is `:2280` — the r8 body's "`:2278` break on a short read"
  is two lines off and is still in the body at tip `23a0e0f` (the fold touched only the
  source: header).
- **Counter angle:** the admission decision never touches any of this — clause c reads
  only cell count / status / used-by. A size check is nearly free (the counter already
  computes `len(blob)` at line 216; comparing it to the row's `N B` figure catches 4/6
  rows). A locator clause (the construct named beside `:N` must occupy line N of the
  receipt) catches the S253 class; "rendered text" locators need the rendering committed
  or blob-line citations. The quote-in-blob check (line 217) already proves the quoted
  construct exists in the receipt — just never at the cited line. Third clause shape
  (ScoutS253): for each row whose locator is a commit URL, assert the sha is fetchable
  from the named repo (`git ls-remote` / `fetch --depth=1`, or the contents API) — a
  row naming an unresolvable ref is a dead pin regardless of how well its receipt
  matches. All three checks are independent of the admission path and would have
  caught every instance above mechanically.
- The row defects themselves belong to the data lane (RevRegistry holds them as F2/F4
  per ScoutS253); my finding is the counter's structural blindness to that class.

**F4 (medium) — S258, and any body-named S-id, escapes clauses c/d/f/g entirely.**
`ids` is parsed from `source:` lines within the first 15 lines only (lines 193–195).
r8's source line names S158, S187, S277 → `ids=S158,S187,S277`; S258 is cited by r8 only
in the OBS block (r8 lines 45–48). Its row exists and is well-formed (11 cells, `mined`,
used-by = r8) and its Gate line is pin-matching — but the counter never consults any of
it. Probe T1: deleting S258's registry row, its GATE line, **and** its OBS block → still
`admitted=3/3 TARGET_MET`, all letters 1. Is its row required? No. Should it be? **Yes**:
the registration lists "S258 (own-work stat receipt, cited by E4)" among the round's new
rows; the row's used-by names r8; and the OBS carries the transport-modes evidence
(directory 0700 / sockets 0755) that the round relies on to refuse
`socket-modes-and-request-read-r30.md`. As coded, an entry may name an unregistered S-id
anywhere in its body with zero consequence — clause c/g's "every cited S-id" is
operationalized narrower than the registration's own "cited by E4" language. Same family,
verified harmless today: r31's body names S158 (lines 33, 35) without S158's used-by
naming r31; the flags body names S186 (registered, pre-existing). T9: a `source:` line
after line 15 naming unregistered `S999` is ignored → still 3/3.

**Update at tips `3674cf2`/`23a0e0f`:** fold `b8400aa` added S258 to r8's `source:`
line, so `ids` now includes it and clauses c/d/g cover it — probe T1′ (delete S258's
row) now fails `c=0` → `admitted=2/3 TARGET_MISSED`, and T1″ (delete its OBS block)
fails `g=0`. The S258 instance is closed. The structural hole remains open for
body-only and late citations: r31's body still names S158 without S158's used-by
naming r31, and T9′ (a `source:` line after line 15 naming unregistered `S999`) is
still ignored → `3/3` at the new tip.

## 4. Clauses d/f/g — binding to pin-matching Gate lines

Code path (lines 209–225): the pin guard (213–214: `pin is None or rpath != pin[0] or
(pin[1] is not None and digest != pin[1]) → continue`) precedes every state change, so
only pin-matching lines can set `good`/`stated` or append to `receipts` (219–221); the
blob is re-digested at REV and must equal the Gate line's digest, which must equal the
pin (216–217). Verified independently:

- All six pinned receipts exist at HEAD and `sha256(blob) == PINS[i][1]` (recomputed):
  S158.bin 97582 B, S187.bin 268731 B, S221.bin 306865 B, S253.bin 11602 B,
  stat-sockets.txt 673 B, S277.bin 35421 B — all `sha_pin_ok=True`.
- The lesson's `## Gate` section holds exactly 6 `GATE` lines, one per id, all with
  receipt paths and digests matching `PINS` (e.g. `GATE S221
  receipt=.ufo/waves/round-38/fetch/S221.bin sha256=35046ba0…d30a`).
- Each quote is verbatim in its receipt and in the citing body: S221's in flags :16;
  S158's (`int ret = poll(pollfds, 1, 5000);`) in r8 :19; S187's in r8 :27; S253's in
  r31 :18; S277's in r8 :43. S258's quote (a 2-word/30-char `directory …` stat label) is
  never consulted.
- Teeth (sandbox): T6 corrupting S221's gate digest by one hex char → `d=0 f=0 g=0
  ok=0`, `admitted=2/3 TARGET_MISSED`; T7 adding a second, non-pin-matching `GATE S221`
  line (wrong receipt path, correct digest) → still `3/3` — non-pin-matching lines are
  ignored, exactly as the docstring's "only pin-matching Gate lines count for d, f and g"
  promises. Clause f receipt-side is per-entry (receipts reset line 206) and requires
  each token in body **and** ≥1 pinned receipt (line 228).

**F5 (low) — undocumented ≤25-word cap on Gate quotes.** Line 217 adds
`len(quote.split()) <= 25`; the docstring's located-quote floor is lower-bound only
("not a bare surface token and is at least 3 words or 24 characters"). Fails closed, but
an operator reading the predicate cannot predict a legitimate long-quote rejection.

**F8 (info, latent) — `pin[1] is None` would skip digest-pin equality** (guard at 213),
diverging from the docstring's "(receipt path, sha256) equals the frozen pin".
Unreachable today: all six pins carry digests.

## 5. Lineage lists (clause l)

`norm()` lowercases, strips `*`/`` ` ``, and blanks `\bS\d{3,}\b` before matching (so
`S1023` cannot satisfy `1023`). Hits at HEAD, quoted from the run: flags `lineage=3/3`,
r8 `5/3`, r31 `5/3`. Per-phrase:

- flags (need 3/4): `output in json` ✓, `select instance` ✓, `force state refresh` ✓,
  `dispatched by the compositor synchronously` ✗ — the entry carries it verbatim but
  wrapped across lines 26–27 ("…dispatched by the\ncompositor synchronously…"), and
  `norm()` does not normalize whitespace, so the wrapped phrase can never hit.
- r8 (need 3/5): all five hit (`temporal`, `five-second`, `synchronously`, `1023`,
  `no length prefix`).
- r31 (need 3/5): all five hit (`1 mib`, `64 kib`, `accumulated request`, `queued`,
  `later`).

**F6 (low) — the lineage floor is largely redundant with clause f for two entries, and
the matcher is whitespace-brittle.** For the flags entry, 2 of the 4 phrases are
clause-f tokens, so l adds only `output in json` beyond f (T3b confirms the coupling:
removing the f-token dropped l to 2/3 as well); for r8, `1023` is an f-token. Only r31's
floor is fully independent. The docstring's "so the package's ground was carried, not
only its citation wiring" is weakest exactly where f already guarantees the hits. Minor:
`1023` as a lineage/f phrase is substring-matchable inside a quoted sha256 hex run — no
spurious hit in these bodies (checked the three commit shas they quote).

**F7 (info) — token exclusivity at HEAD.** The assignment's "tokens appear only in the
intended entry bodies" holds for 5/6 tokens; `1023` also occurs in
`request-limits-upstream-r31.md:33` ("accumulates 1023-byte chunks" — the same upstream
handler, legitimately) and pre-held in `event-delivery-limits-r26.md`.

## 6. Why `ids` shows 3 ids for r8 while S258 has a row + quote

`ids` = S-ids parsed from `source:` lines in the first 15 lines (lines 193–195). r8's
single source line (line 9) names S158, S187, S277 — the registration's re-point
(S272→S158, S276→S187; commit `efb0ec2` honestly dropped the legacy ids from the body
because the counter counts source-line ids as cited). S258 is cited only in the OBS
block (r8 :45–48), so it is absent from `ids`: clause c never checks its row, clause d
never consults its pin-matching Gate line, clause f's receipt set never includes
stat-sockets.txt, and clause g's OBS requirement runs over `ids` only. Net effect is F4:
S258's entire wiring is decorative to the counter (T1).

## Findings summary (severity order)

1. **F1 major** — TARGETS token set for `hyprctl-flags-r28.md` diverges from the frozen
   registration (`force state refresh` substituted for `flag list`); freeze-internal
   (counter unchanged since `58e55ec`), docstring does not enumerate tokens.
2. **F2 major** — registration's "base grep finds no `flag list` in corpus/knowledge" is
   false (walker-deep.md:314, waybar-walker-plane.md:480); with the frozen token the
   counter exits 2 at Setup (probe T5), so the substitution is what keeps the round
   runnable.
3. **F3 medium** — precondition scans 5 of 6 TARGETS tokens; `1023` is base-held
   (event-delivery-limits-r26.md:53,82) and structurally unscannable; docstring's
   "frozen surface tokens" means two different sets.
4. **F4 medium** — body-named S-ids (S258 in r8; S158 in r31; S186 in flags; post-line-15
   `source:` lines, probe T9) escape clauses c/d/f/g; S258's row/Gate/OBS deletable with
   `admitted=3/3` unchanged (probe T1). Its row should be required — the registration
   calls S258 "cited by E4" and the OBS grounds the r30 refusal. Fold `b8400aa` later
   put S258 into r8's source line — that instance is closed at tip `23a0e0f` (T1′/T1″
   now fail as they should); the body-only/post-15 hole remains (r31↔S158, T9′).
5. **F5 low** — undocumented ≤25-word Gate-quote cap (line 217).
6. **F6 low** — lineage floor redundant with f for flags/r8; whitespace-brittle phrase
   matching (wrapped `dispatched by the compositor synchronously` can never hit).
7. **F7 info** — `1023` not exclusive to r8 at HEAD (also r31:33; pre-held elsewhere).
8. **F8 info** — latent `pin[1] is None` fail-open (unreachable with current PINS).
9. **F9 medium** — clause c is shape-only: anchor locators and byte figures never
   resolved against receipts; live instances at the measurement revs: S253
   `:19-20`→actually `:43-44`, byte figures wrong in 4/6 rows (S221's equals its own
   digest prefix), S187's locators cite an uncommitted rendering, and (ScoutS253)
   S277 pins an unresolvable commit (`707cf7f8…` "not our ref"; receipt is a `main`
   snapshot). Fold `b8400aa` repaired the locator and byte figures (data only); the
   S277 pin is still dead at tip `23a0e0f`; the counter gained none of the three
   checks (details §3/F9).

## Verified-good (no finding)

Clause a/b/e shapes match the docstring (entries absent at base; `verified-at:
2026-10-25` / `recheck: on-release` parse; coverage-map rows exist, one per entry).
Clause c verified per id with teeth (T8) — shape-only; locator/byte figures are
unchecked (F9). Clause d/f/g pin-binding verified live (T6,
T7) and all six receipt digests recompute to their pins. Before-state at base = 0/3
TARGET_MISSED exit 1, as registered. The counter is unchanged since the freeze commit
(log shows only `58e55ec` at every tip checked, through `23a0e0f`). All six row byte
figures match the pinned bytes at tip `23a0e0f` (post-fold).

## Residual risk / verification gaps

- The pins bind entry↔receipt bytes, not receipt↔upstream-truth: a wrongly-fetched
  receipt whose bytes match its pin satisfies d/f/g by construction. Auditing whether
  the receipts really are the named upstream documents was out of my scope (fetch-step
  claim, not the admission counter) — ScoutS253's wave report has since audited three
  of them against the fetched bytes: S253 PASS (byte-identical re-fetch), S277's pin
  dead (unresolvable ref), S158 PASS (four-way probe: raw fetch, `cmp`, git tree,
  `cat-file` blob sha all match the pin). S187/S221/S258 remain unaudited by me — and
  S187/S221 are wiki-page renders rather than repo refs (ScoutS253's flag), so a
  ref-resolvability clause scoped to commit-URL locators excludes them by design;
  render locators need the rendering committed or blob-line citations.
- The lane tip moved repeatedly during review (`bb1adce`→`3f14bd2`→`3674cf2`→`23a0e0f`:
  sibling errata, then the `b8400aa` fold). Every finding was re-checked at the newest
  tip it could affect; the sandbox baseline was restored and re-scored 3/3 after each
  probe matrix.
- Sibling context: RevCommitChain's errata (`3f14bd2`) records post-freeze patches on
  the *other* two counters. The request-ground counter has no post-freeze commits — its
  divergences (F1–F3) are inside the freeze commit itself.
