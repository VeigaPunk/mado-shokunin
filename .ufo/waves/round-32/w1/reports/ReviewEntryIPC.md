# ReviewEntryIPC — review of `scratch/ScribeEntryIPC/ipc-contract-r25.md`

Reviewed: 2026-10-24. Draft at `.ufo/waves/round-32/scratch/ScribeEntryIPC/ipc-contract-r25.md`
(read at mtime ~20:11, all 134 lines). Bar: `corpus/QUALITY.md` (criteria 41–54 active),
`/home/vgpnk/Projects/shokunin/CORPUS.md` (provenance-trio rule, Gate `≤25-word` quote rule).
Ground truth: the three re-open seat reports plus their committed fetched bytes
(`scratch/ScoutIPCWikiCurrent/ipc_index.md`, `scratch/ScoutIPCWiki0560/IPC-0.56.0.html`,
`scratch/ScoutIPCEventMgr/EventManager.cpp`), which I re-derived where a number or digest
was claimed. Draft not edited — report only.

## Mandated checks — verdict each

### 1. Every claim's supporting quote appears in the re-opened source at the stated anchor — **FAIL**

All S186/S187/S189 *quoteable* claims check out verbatim (details in §"quote ledger"
below). One claim carries no seat-report quote or supporting observation at all:

> draft L60–62: `**OBS** The pinned commit is the \`v0.56.2\` tag itself (lightweight tag, \`git ls-remote\` 2026-10-24), so "at v0.56.2" below means these exact bytes (S189).`

No seat report records a `git ls-remote` or tag-object lookup; `(S189)` cites a file:line
anchor, which cannot carry tag-type. This is not in the seat reports' claims either —
none asserts "lightweight". **I independently re-ran it**: `git ls-remote --tags
https://github.com/hyprwm/Hyprland 'v0.56.2*'` → `efb50993780079460b0cbed1363e2166a2de1d9f
refs/tags/v0.56.2`, no `^{}` peeled line → lightweight tag, draft's fact is TRUE. It is
still ungrounded in the cited evidence: under QUALITY 42 the anchor must point at a
receipt that says it; `git ls-remote` output exists nowhere in this wave's committed
surfaces. Fix: cite a receipt that contains the ls-remote line, or drop "lightweight".

### 2. No quote longer than 25 words — **PASS**

Longest quote, draft L31 (`"Hyprland evaluates connections … timeout is reached."`),
tokenizes to **25 words** — at the bar, not over it (bar is `≤25`, CORPUS.md SOURCES rule
1). All other blockquotes ≤13 words (`wc -w`: L72 = 12, L83 = 13).

### 3. Every claim carries an S-id — **PASS, one flag**

Every OBS/INF domain claim carries an S-id (S186:14/19/22/25/30/32, S189:14/21/34/35/
126-129, S187, S018/S158). The flagged line:

> draft L102–104: `**UNK** Nothing here was observed on this host: no socket was connected, no event was seen, and the installed compositor binary was not interrogated. …`

has no source pointer. It is a seat self-attestation rather than a domain claim, so it
does not violate QUALITY 42 in substance — listed because the check enumerates claims
without S-ids. Acceptable as-is; optionally anchor it to the preamble's same statement.

### 4. `verified-at:` / `recheck:` present — **PASS**

Draft L15 `verified-at: 2026-10-24`, L16 `recheck: 90d — …` — provenance trio comes first
(`source:` ×3 at L12–14 before both), satisfying the CORPUS.md kaika rule. `recheck` names
the method (re-pull + re-diff). The access date is fresh and matches the seats' fetches.

### 5. No host fact asserted where sources only document — **FAIL**

> draft L51 heading: `### §3 What the compositor implements at the host's own version`
> draft L115 comment: `# the implementation's framing and truncation, from the host's tag`
> draft L53: `**OBS** At v0.56.2 the event socket is created by the event manager …`

The draft treats "the host runs v0.56.2" as established. The seat reports document
upstream bytes only; the draft's own L102–104 admits "the installed compositor binary was
not interrogated." Under QUALITY 16 the host-version premise needs cited grounding — it
exists in the lane's prior corpus (SOURCES S018/S158 are explicitly the v0.56.2 tree, and
the draft cites S018/S158 at L107 for a different point), so the premise is defensible,
but **as drafted no citation binds it**. Minimal repair: cite the lane record that pins
the host to v0.56.2 in §3's opening line, or rephrase to "at the pinned v0.56.2 tree".

## Quote ledger — verified verbatim against fetched bytes

| Draft line | Cited anchor | Actual location | Verdict |
|---|---|---|---|
| L21 `.socket.sock` | S186:14 | `ipc_index.md:14` `## `$XDG_RUNTIME_DIR/hypr/[HIS]/.socket.sock`` | PASS — seat mis-cited as "L14 heading", agrees |
| L26 `"Basically, write \`[flags]/command args\`."` | S186:19 | `ipc_index.md:19` verbatim | PASS — fixes staged entry's stale `:7-12` |
| L31 sync/freeze quote | S186:22 | `ipc_index.md:22` verbatim incl. "until the five-second timeout is reached" | PASS — seat's own table truncated the quote at L22; draft correct |
| L41 `.socket2.sock` | S186:25 | `ipc_index.md:25` verbatim | PASS |
| L46 `EVENT>>DATA\n` framing | S186:30 | `ipc_index.md:30` verbatim | PASS — fixes stale `:18-25` |
| L49 `E.g.: \`workspace>>2\`` | S186:32 | `ipc_index.md:32` verbatim | PASS — fixes stale `:25` |
| L55–58 `src/ipc/` absent | S189 tree check | seat report §Claim A: GitHub contents API 404 at `efb50993…` | PASS — negative claim carries its sweep (API 404), CORPUS-compliant |
| L67 socket-path line | S189:21 | `EventManager.cpp:21` byte-identical | PASS |
| L72, L74, L76 socket/backlog quotes | S189:14, :34, :35 | lines 14/34/35 byte-identical | PASS — correctly splits the `// 10 max queued.` nit (seat: quote at :34, cite was :35) |
| L81, L83 formatEvent quotes | S189:128, :129 | lines 128/129 byte-identical | PASS |
| L93–95 44-event identical set | S187 + S186 | seat 0560: 44 tbody rows, set-diff `[]/[]`; seat current: 44 rows L38–81 | PASS — re-derived: both name sets diff empty |
| L114/L116 `grep -c` expectations `1`/`1` | §6 | re-ran on committed bytes: `EVENT>>DATA` → 1; `substr(0, 1024)` → 1 | PASS |
| Gate L126–128 sha256s | three rows | recomputed on fetched bytes: `535bc4c3…`, `136e5511…`, `eea605df…` — all exact | PASS — S187 draft prints the full sha where the seat printed a prefix; I verified the full digest against the committed file |

## Provenance/bar notes (non-blocking)

- **Criterion 10 shape**: `44 event names` is stated with method + date (`set-diffed …
  2026-10-24`) but not in `<n> — <command> <date>` form; the commands exist in the seat
  reports. Recommend inline command or a pointer line. Not counted in the mandated checks.
- **S187 Gate quote**: `datetime="2026-05-02T03:38:58.000Z"` lacks a line anchor (the
  other two Gate rows carry L30/L128); it sits at `IPC-0.56.0.html:3136`.
- **INF labels**: L33–37, L85–88, L97–98 are marked INF with stated basis — OBS/INF/UNK
  separation intact (criterion 43).
- **UNK S018/S158 reference** (L107) resolves: both rows exist in `corpus/SOURCES.md`,
  `mined`, and are indeed the efb50993-pinned HyprCtl tree.
- **Structure**: staged entry's shape, unknowns and §6 recheck recipe preserved; stale
  staged line pins (S186:7-12/15/18-25/25) all corrected to this fetch's numbering — the
  exact defect `ScoutIPCWikiCurrent` flagged ("Content: faithful. Line pins: stale.").

## Overall verdict — **FAIL (2 blocking items, both cheap to fix)**

1. L60–62 asserts "lightweight tag" — true (I re-ran `git ls-remote`) but carried by no
   seat-report quote and no committed receipt; `(S189)` cannot ground it.
2. §3 asserts the host's installed version ("the host's own version" / "the host's tag")
   while the cited sources only document upstream v0.56.2 bytes; bind the premise to the
   lane's existing host-version record or rephrase to the pinned tree.

Everything else — all fifteen quote-at-anchor checks, word limits, provenance trio, Gate
table digests, count re-derivation, OBS/INF/UNK hygiene — passes against the re-opened
bytes. Do not ship L60–62 or the §3 host-version phrasing as written.
