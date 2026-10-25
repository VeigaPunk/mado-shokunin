# RevQuarantine — round-39 w1 — spot re-check of ExecQuarantineSlice verdicts (2026-10-25)

Scope: picked 3 rows from `.ufo/waves/round-39/w1/ExecQuarantineSlice/verdicts.md` — **S189**
(present), **S224** (absent/refused), **S205** (present) — re-opened each cited source, and
report mismatches found while cross-checking (two more verdict-row classes are affected).
Leaf slice: read-only everywhere; the only file written is this one. No installs, no
subagents, no mutating git/jj. Register consulted read-only at
`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`
(rows 141/144/145, 350–355).

## Verdict of the 3 picked rows

| row | verdicts.md says | my re-check | outcome |
|---|---|---|---|
| S189 | present — appendable | re-fetched pinned commit; 192 lines; quote verbatim at line 128 | **CONFIRMED, accurate** |
| S224 | absent — refused | old timestamp absent from live tree; current value rotated again | **CONFIRMED (core)**, 1 side-claim nit |
| S205 | present — appendable | both mappings are in the live source, but the cited bytes are single-line escaped JSON | **Substance CONFIRMED; anchor evidence inaccurate** (minor) |

## Findings by severity

### HIGH — 5 of 13 rows (S209, S222, S223, S225, S235) rest on a factually false evidence premise

verdicts.md rows: "`## Gate — S2xx` named no locator; no quote to hand-check." → `unreachable`.
False as written. All five **mado** gate blocks name locators, and four carry explicit quotes
(`shokuknow/lanes/mado/SOURCES-PROPOSED.md:86`; `.../mado/round3/SOURCES-PROPOSED.md:48,54,68`;
`.../mado/round4/SOURCES-PROPOSED.md:53`). I hand-checked every one this session:

- **S209** — gate URL `https://wiki.archlinux.jp/index.php/Hyprland`, quote 「また、Hyprland は 2 つの
  UNIX ソケット を公開しており…」→ live page today: sentence present at rendered line 188 (「2 つの
  UNIX ソケット」 is a link span in page markup; matches after HTML-strip).
- **S222** — gate URL = the S205 interwikimap endpoint, quote zh-hans→`wiki.archlinuxcn.org/wiki/$1`
  → present in live JSON after normalization (see S205 below).
- **S223** — gate URL `https://raw.githubusercontent.com/hyprwm/hypridle/v0.1.8/systemd/hypridle.service.in`,
  quote `PartOf=graphical-session.target` → re-fetched today: verbatim (line 4 of the file).
- **S225** — gate locator `/usr/lib/systemd/user/hypridle.service` → file exists on host; 
  `PartOf=graphical-session.target` present (read-only peek).
- **S235** — gate URL `https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/bin/omarchy-refresh-hypridle`,
  quote `omarchy-refresh-config hypr/hypridle.conf` → re-fetched today: verbatim.

So "no quote to hand-check" is false for all five; none is unreachable in the cited-gate sense.
The true defect is in the **register's locator cell**, which holds the self-referential heading
`## Gate — S2xx` instead of a resolvable locator (rows 351–355), and the register's class column
("the gate block named no locator") mis-locates it — the block names one. Precedent inside the
lane: round-32's own hand-check (`.ufo/waves/round-32/w1/reports/ExecQuarantineSlice.md:23-26`,
`logs/ExecQuarantineSlice.log:15-16`) called this exact wording "inaccurate for all five mado gate
rows" and verified S222/S223 verbatim; rounds 34/35 (ScoutQuarantineB, ScoutQuar) re-froze the
wrong reading, and round-39 inherited it. Peer corroboration: R35ReconQuarantine finds the same
pattern on kaidoku (S136/S147) and traces it to `quote-lint.py:348-374 local_locator()` resolving
local paths only relative to CWD or `shokuknow/lanes/<lane>` — a checker blind spot, not row truth.
Consequence: `unreachable (not fabrication)` is safe-conservative, but 4–5 rows are likely
**present/appendable** once re-anchored to the gate-block locators; the summary line "prose-
unverifiable" for these five is wrong.

### MINOR — S205 anchor: "JSON lines 414/418/421/425" do not exist in the cited source

`curl -s -o /tmp/iw.json 'https://wiki.archlinux.org/api.php?action=query&meta=siteinfo&siprop=interwikimap&format=json'`
→ HTTP 200, **8313 B, `wc -l` = 0 newlines** — the cited response is one line of compact JSON:
`{"prefix":"zh-hans","local":"","language":"\u4e2d\u6587\uff08\u7b80\u4f53\uff09","bcp47":"zh-Hans","url":"https://wiki.archlinuxcn.org/wiki/$1"},{"prefix":"zh-hant",…,"url":"https://wiki.archlinux.org/title/$1_(\u6b63\u9ad4\u4e2d\u6587)"}]}}`
(tail via `cut -c7960-8313 /tmp/iw.json`). Therefore: (a) no line 414/418/421/425 exists in the
cited bytes — those numbers are artifacts of a fetch tool's 2-space re-serialization (the reader
renders 435 lines; zh-hans/zh-hant are the last two entries); (b) the register quote
`"prefix": "zh-hans", "url": "…"` is **not verbatim** in the cited bytes — no space after `:`,
`local`/`language`/`bcp47` sit between `prefix` and `url`, and CJK is `\u`-escaped. Both mappings
ARE in the live source, so verdict class "present" stands; but the evidence sentence implies a
multi-line verbatim source. verdicts.md flags quote-glyph normalization for S228 yet claims plain
verbatim + line numbers for S205. Correct anchor: "present after JSON normalization (compact
separators, non-adjacent fields, `\uXXXX` escapes); line numbers are serializer artifacts."

### CONFIRMED rows

- **S189 — accurate.** `curl` of the pinned
  `raw.githubusercontent.com/hyprwm/Hyprland/efb5099…/src/managers/EventManager.cpp` → 192 lines
  (`wc -l`), and `sed -n '126,130p'` shows line 128 = 
  `    auto             eventString = std::format("{}>>{}\n", event.event, data.substr(0, 1024));`
  verbatim, inside `CEventManager::formatEvent` (line 126). Register's `\"`/`\\n` are markdown
  escapes of `"`/`\n`, as verdicts.md notes. Exact match on file length, line number, and function.
- **S224 — core accurate.** `grep '2026-10-23T22:52:44Z'` across `/home/vgpnk/.cache/ai-usage/`
  (status.json 30,022 B; inception-ledger.json 2,112,622 B — file exists): **0 hits**; status.json
  line 3 now reads `"updated_at": "2026-10-25T19:10:32Z"`. Rotated again from verdicts.md's
  observed 19:05:31Z — expected volatility; size drifted 30,009→30,022 B and mtime advanced to
  16:10:32 −0300 (= 19:10:32Z), internally consistent with the verdict's 16:05/19:05:31Z snapshot.
  Refusal (stale rotating value, not fabrication) is evidence-backed.
  - **Nit:** "the old value survives only in the lane's own round-4 proposal files" is wrong in
    detail: a lane-wide grep finds the literal timestamp in `.ufo/waves/round-32/scratch/ScribeLessonDraft/round-32.md:181`,
    `round-32/w1/{logs/ExecQuarantineSlice.log:14, reports/ExecQuarantineSlice.md:19}`,
    `round-34/scratch/ScoutQuarantineA/table.md:12` (+log/report), `round-35/w1/reports/ScoutQuar.md:21`,
    `round-35/w2/reports/RevQuarantineSlice.md:117`, and round-39's own verdicts.md — and in **no**
    round-4 path. Substance survives: every lane occurrence is a circular register-derived quote;
    none is a snapshot of the cited source's bytes.

### MINOR — S199/S200 sub-claim "No quote was ever recorded for this row" is false

The lane's round-2 fetch set (`/home/vgpnk/Projects/shokuknow/lanes/mado/round2/fetch/`) holds
recorded quotes: `csdn-149787804.md.txt:160` = `windowrule = opacity 0.80 $& 0.80 $& 1,class:^([Cc]ode)$`
and `csdn-164457293.md.txt:1150` = `hl.bind("SUPER + L", hl.dsp.exec_cmd("hyprlock"))` — both
verified verbatim this session. The `unreachable` class for the remote may still be right (I did
not re-test CSDN's 521; round-32 measured it), but "nothing to locate" misdescribes rows whose
gate quotes sit in committed lane artifacts — same under-check pattern as the gate rows.

## Residual risk

- CSDN 521 re-observed only by round-32/39 agents, not re-tested by me; remote availability is
  time- and IP-dependent, so S199/S200 class could flip to fetchable without notice.
- The five gate rows could in principle be "present" yet still unappendable if the campaign's
  binding rules demand row-bound quote+locator (round-13 note: "the binding is positional") —
  that is a policy call, not an evidence absence; my finding only establishes the evidence exists
  and verifies.
- S209's JP quote matches only after HTML-strip (link markup inside the sentence); S222/S205 only
  after JSON normalization — both need the same normalization disclosure S228 got.

## Verification gaps

- Did not re-test S195/S201/S228 rows (not picked).
- Did not audit other lanes' register rows (kagi/kaidoku/kengaku/kotoba/kumitate/souji/tsukuroi
  gate ids collide with mado's; only mado rows are in scope here).
- Register and verdicts files left untouched (data, frozen; this report is the only write).
