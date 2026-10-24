# CriticSourcedClaim — sourced-claim audit, S186/S187/S188/S189/S196

Round 32 · w1 · lane: mado-shokunin · critic, leaf (no subagents).

Attack target: CORPUS.md SOURCES rule 1 + registration item 10 (the L1 must
re-open every cited source and record its own access date/quote; the campaign's
`opened` 2026-10-23 cells prove nothing for this lane).

## L1 re-open status (item 10)

All five seat reports exist and record **the lane's own** access date
2026-10-24 with sha256/byte evidence:

- `ScoutIPCWikiCurrent.md` — S186: 6539 B, sha256 `535bc4c385a06162…`
- `ScoutIPCWiki0560.md` — S187: 268731 B, `136e5511fba5524a`, revision
  `datetime="2026-05-02T03:38:58.000Z"` (matches staged "May 2, 2026")
- `ScoutDispatchersWiki.md` — S188: 12879 B, `c830ce0717f92776…`
- `ScoutIPCEventMgr.md` — S189: 6479 B, `eea605dfe5ce09e1…`
- `ScoutDispatchers0560.md` — S196: 297863 B, `f9b51362f2440e02…`, revision
  `datetime="2026-07-15T23:56:15.000Z"` ("July 15, 2026")

I independently re-verified all five staged anchor checksums against
`.ufo/waves/round-32/fetch/S*.bin`: **every sha256 prefix and byte count in the
staged rows matches the re-fetched bytes exactly** (S186 535bc4c385a06162/6539;
S187 136e5511fba5524a/268731 — note: the staged anchor names *no* sha256 for
S187, only byte count, which matches; S188 c830ce0717f92776/12879; S189
eea605dfe5ce09e1/6479; S196 f9b51362f2440e02/297863). The `fetch/` copies are
byte-identical to the scout scratch copies (`diff -q` clean on all five).

## Per-row verdicts

### S186 — GROUNDED

`teaches` (staged): "A request is written as `[flags]/command args` on a socket
the compositor evaluates synchronously, so an unclosed request connection
freezes it; the event socket emits `EVENT>>DATA\n`."

Every clause sits inside the anchor (`_index.md:7-26` + `:27-102` — a broad
anchor, ~all of a 102-line file, but it contains every grounding line):
grammar L19, freeze NOTE L21-23, `.socket2.sock` L25, framing L30, 44-event
table L38-81. Seat report: verbatim-faithful. Tier A correct (pinned upstream
docs at commit `c04680a`). `used-by: corpus/knowledge/ipc-contract-r25.md` —
entry's `source:` line cites S186; not a lie.

**Entry-side defect (not the row's):** the staged `ipc-contract-r25.md` cites
`(S186:7-12)`, `(S186:15)`, `(S186:18-25)`, `(S186:25)` — all stale vs the
re-fetched file (scout: grammar is L19, note L21-23, framing L30, example
L32). The row's anchor ranges survive because they are ranges, not pins; the
entry's line citations do not. The scribe draft must re-pin, or the admitted
entry carries 5 wrong locators.

### S187 — GROUNDED

`teaches` (staged): "The event catalogue published for 0.56.0 is identical to
the current upstream catalogue — 44 events, none added or removed — so the
host's event vocabulary is stable across the 0.56 to 0.57 boundary."

Verification: my own extraction — S186 markdown table rows L38-81 = **44**;
S187 HTML `<tbody>` = **44 rows**; first-column name sets diff → `only186:
[]`, `only187: []`, identical order. Seat report agrees (44/44, identical).
The anchor (§ socket paths, § Events list, revision "May 2, 2026") contains the
catalogue the claim counts. Minor wording caveat: S186 is a pinned *current-upstream
snapshot* (commit dated 2026-09-18), not a "0.57" artifact — "0.56 to 0.57
boundary" is editorial; the underlying claim (name sets equal) is exact. Tier A
acceptable (official version-matched docs, scoped to "the 0.56.x IPC contract").
`used-by` → `ipc-contract-r25.md` cites S187 in `source:` — not a lie.

### S188 — GROUNDED

`teaches` (staged): "A dispatcher returns a table that describes an action and
does not invoke it; `force_idle` sets elapsed time for all idle timers
ignoring idle inhibitors; `event(string)` sends an event to socket2."

All verbatim in fetched bytes: description/no-invoke L8-9, `hl.dispatch`
wrapper L14, `event`→socket2 L59, `force_idle` L69. Anchor pins check out
(`:9-19`, `:58-59`, `:69`, `:82-87` — warning verbatim at L82). Seat report:
11/11 claims checked, one partial-quote nit (entry's L69 quote drops the
"Timers return to normal… Do not use with a keybind" tail — entry-side fix,
ties to the L82 warning). Tier A correct. `used-by` → `dispatcher-semantics-r25.md`
cites S188 — not a lie.

### S189 — GROUNDED

`teaches` (staged): "The event socket is `$XDG_RUNTIME_DIR/hypr/[HIS]/.socket2.sock`,
an AF_UNIX stream with listen backlog 10; events are formatted as
`EVENT>>DATA\n` with data truncated at 1024 chars and embedded newlines replaced
by spaces."

Seat report: 6/6 S189-attributed claims AGREE; my line check — socket ctor L14
(`AF_UNIX, SOCK_STREAM | SOCK_CLOEXEC | SOCK_NONBLOCK`), PATH L21, listen(10)
L35, `formatEvent` L126-129 verbatim. One nit: `// 10 max queued.` comment is
L34, cited `:35` (the `listen` line — correct attribution for the *fact*).
Tier A correct (source code at host's own tag v0.56.2). `used-by` →
`ipc-contract-r25.md` cites S189 — not a lie.

**Flag for the Gate:** the lane's quarantine slice
(`.ufo/waves/round-32/assimilation/quarantine-slice`) marks **S189
`payload-absent`** in the campaign absent-defect register — yet this round's
re-open fetched the payload intact (6479 B, all five located items present).
The register row is stale/fabrication-class per item-10 gate 5 and needs a
verdict line in `## Gate` (refuse-the-register-verdict, not the row).

### S196 — OVERSTATED

`teaches` (staged): "The 0.56.0 documentation already exposes the Lua
`hl.dsp.*` API, so the current-git dispatcher page is not a post-0.56
addition; **the host's version carries the same dispatcher vocabulary**."

First clause grounded: the page's General table opens with
"`hl.dsp.` contains:", `hl.dsp` appears 10× (`hl.dsp.group/window/workspace/cursor`
tables). Second clause **fails the re-open diff**. My extraction:

- S188 (current-git dispatchers.md) dispatcher names: 48 base names incl.
  **`reload_config`**.
- S196 (0.56.0 page) dispatcher names: 47 base names, all S188-minus-one.
- `in S188 not S196: ['reload_config']` — current upstream has a dispatcher
  the host's release line does not document.

"Same dispatcher vocabulary" is false as written; the true statement is
"vocabulary ⊆ current-upstream, delta = `reload_config`" (and possibly
per-method signature drift — not checked). Fix: reword `teaches` to name the
delta, or narrow the scope cell to "the dispatcher *API surface* exists on
0.56.x". `used-by` → `dispatcher-surface-and-request-grammar-r26.md` cites
S196 — the entry exists and cites the row, so not a lie, but the entry repeats
the overstated equivalence.

**Additional staged-entry defect on the same row:** the entry's keyword
sentence claims `exec` "documented on both" pages. Seat report: `exec` is **not**
a dispatcher name on the 0.56.0 page — its two bare occurrences are shell
snippets (`exec, uwsm stop`, `exec, loginctl terminate-user`). My grep confirms
S188 likewise has only `exec_cmd`/`exec_raw` — `exec` is keybind-syntax prose
on both sides, i.e. "documented on both" is vacuously true as substring and
false as dispatcher-name. The draft must drop `exec` or reword to `exec_cmd`.

## Gate-block assessment

Contract asks `## Gate` carry ≥1 admit and ≥1 reject. `corpus/lessons/round-32.md`
does not exist yet (ScribeLessonDraft seat still running at write time). The
material for a compliant gate is present:

- **Admit candidates:** S186, S187, S188, S189 — all grounded verbatim against
  re-fetched bytes.
- **Reject candidate (natural):** the S196 row as staged — `teaches` overstates
  vocabulary equivalence (`reload_config` delta; `exec` keyword false) —
  REJECT-and-correct, or admit S196 with reworded `teaches` and reject the
  staged entry's keyword sentence. Either way a reject exists in the evidence.
- **Quarantine verdicts available:** slice lists S189/S195/S201/S205/S224/S228
  `payload-absent`; S189's register row is contradicted by this round's fetch —
  belongs in `## Gate` as a quarantine verdict.

## Summary table

| Row | Verdict | Quoted staged `teaches` (grounding cell under attack) |
|---|---|---|
| S186 | GROUNDED | "…`[flags]/command args`…synchronously…`EVENT>>DATA\n`" |
| S187 | GROUNDED | "…44 events, none added or removed…" (diff verified 44/44, sets equal) |
| S188 | GROUNDED | "…returns a table that describes an action…`event(string)` sends an event to socket2" |
| S189 | GROUNDED | "…`.socket2.sock`, AF_UNIX stream, backlog 10; `EVENT>>DATA\n`, 1024-char truncation, newline→space" |
| S196 | **OVERSTATED** | "…the host's version carries the same dispatcher vocabulary" — `reload_config` exists upstream, absent on 0.56.0; staged `exec` keyword is a shell-syntax token, not a dispatcher |

Tier inflation: none — all five are `docs`/`code` at A, no `community` rows.
`used-by`: all five name entries that cite the row in `source:` — no lies;
`dispatcher-surface-and-request-grammar-r26.md` additionally cites held row
S018 (fine — additional citation, not absent).

## Commands run (evidence)

```sh
sha256sum .ufo/waves/round-32/fetch/S*.bin          # prefixes match staged anchors
diff -q fetch/S*.bin scratch/Scout*/*               # byte-identical, all five
awk 'NR>=38&&NR<=81' fetch/S186.bin | grep -cE '^\|'   # → 44
# S187 <tbody> <tr> count → 44; name-set diff → identical (both directions empty)
sed -n '14,36p;126,129p' fetch/S189.bin             # socket/backlog/formatEvent verbatim
sed -n '9,19p;58,59p;69p;82,87p' fetch/S188.bin     # teaches clauses verbatim
# S196: General table names extracted; S188-vs-S196 name-set diff →
#   in S188 not S196: ['reload_config']
```
