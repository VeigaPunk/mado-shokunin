# RevQuoteS209 — row S209 gate-quote / receipt / anchor attack (round 35, wave 2)

Seat: `L1Mado35.RevQuoteS209`. Mode: read-only falsification. No lane file, counter, control,
`SOURCES.md`, fleet repo, sibling lane, jj state or Git index was written. Only
`.ufo/waves/round-35/scratch/RevQuoteS209/` and this report were created.
Installs: **none** (no tool was needed; pacman paused, not touched).

Axes named (godspeed): A1 quote-is-substring, A2 quote-facts-still-true-on-host,
A3 anchor-hash-agreement, A4 row/entry structural wellformedness, A5 dating robustness.

## Verdict

**S209 CONFIRMED — no divergence on any assigned axis (a, b, c).**
Three minor findings below; none overturns the row's claim or its quote.

| Axis | Check | Result |
|---|---|---|
| A1 | gate-quote is contiguous substring of receipt bytes | **PASS** (1 occurrence, ASCII-exact) |
| A2 | facts stated by the quote match the host today | **PASS** (4/4 copies, 1 handler each) |
| A3 | recomputed sha256 == anchor cell of row S209 | **PASS** (exact) |
| A4 | exactly one gate-quote line, 13 words, well-formed row | **PASS** |
| A5 | whether the "oldest dated 2026-10-03" has one unambiguous date | **MINOR finding F1** |

## (a) Re-open the live source — `/home/vgpnk/.config/waybar/`

Command: `stat -c '%n | mtime=%y | btime=%w | ctime=%z | size=%s' config.jsonc.bak*` (exit 0),
plus `grep -o 'omarchy-toggle-idle' config.jsonc.bak* | wc -l` and a structural
`grep -n -A2 '"custom/idle-indicator": {'` per copy (exit 0).

| File | size | mtime | btime | handler lines |
|---|---|---|---|---|
| `config.jsonc` (live, not a `.bak`) | 6354 | 2026-10-17 17:02:56.289420985 -0300 | 2026-10-16 23:30:59.578762780 | `custom/idle-indicator` L207, `"on-click": "omarchy-toggle-idle"` L208 — 1 |
| `config.jsonc.bak` | 5892 | 2026-10-11 10:36:07.023252903 -0300 | 2026-10-11 10:36:07.022252901 | L199/L200 — 1 |
| `config.jsonc.bak.1791314470` | 5114 | **2026-10-03 17:44:32.097653608 -0300** | **2026-10-06 16:21:10.082789105** | L153/L154 — 1 |
| `config.jsonc.bak.1792203278` | 6068 | 2026-10-16 23:14:38.105347715 -0300 | 2026-10-16 23:14:38.105347715 | L206/L207 — 1 |
| `config.jsonc.bak.1792267376` | 6068 | 2026-10-17 17:02:56.289334445 -0300 | 2026-10-17 17:02:56.289181525 | L206/L207 — 1 |

- Copies matching `config.jsonc.bak*`: **4**.
- Copies carrying the idle handler as a real `on-click` inside the `custom/idle-indicator`
  module: **4 of 4** (not a stray mention — every copy shows the `on-click` line immediately
  under the module key).
- `sha256sum config.jsonc.bak*`: `3d8bb37f…ca390f` (`.bak`), `ff387b21…57c061`
  (`…1791314470`), `07f7d663…a08e71` (`…1792203278`), `07f7d663…a08e71` (`…1792267376`)
  — the two 6068-byte copies are byte-identical; the live config (6354 B) differs from all.
- No other `config.jsonc*` exists under `/home/vgpnk` (maxdepth 4) besides these five and
  `fastfetch/config.jsonc`.

## (b) Gate-quote vs receipt bytes

Entry line (`corpus/knowledge/idle-lock-offered-in-the-bar-r15.md`):

```
gate-quote: S209 located: four dated copies of the bar's configuration each carry the omarchy-toggle-idle handler
```

Byte test (Python, `-I`, read-only):

- payload length **96 bytes**, pure ASCII (`nonascii=[]`; the apostrophe in `bar's` is
  `0x27`, confirmed by `od -c` on the receipt tail).
- `payload in receipt` → **True**; `receipt.count(payload)` → **1**.
- trailing bytes after the match → `b'\n'` only; the match is the final line of the
  905-byte receipt, so it is contiguous and unterminated by any later edit.
- word count **13** (frozen predicate bound: 1–25 words) → in bound.

Facts the quote states, re-measured on the host just now:

| Fact in quote | Host today | Verdict |
|---|---|---|
| "four dated copies of the bar's configuration" | exactly 4 files match `config.jsonc.bak*` | TRUE |
| "each carry the omarchy-toggle-idle handler" | 4/4 carry `"on-click": "omarchy-toggle-idle"` | TRUE |

Receipt's own per-copy table also still matches the host to the second
(`10:36`/`17:44`/`23:14`/`17:02` vs `10:36:07`/`17:44:32`/`23:14:38`/`17:02:56`), and all four
paths it lists exist. Receipt mtime `2026-10-24 23:21:21`, header "host re-open 2026-10-24" —
consistent.

## (c) Anchor hash

```
$ sha256sum .ufo/waves/round-35/fetch/S209.receipt.txt
a170c7a50b9305b3448fc85ecddb0d7b1f1c3ff5e42c78cdc2d07718c3bdd27c  .ufo/waves/round-35/fetch/S209.receipt.txt
sha_exit=0
```

Row S209 anchor cell (cell index 5, extracted by splitting the single matching row on `|`,
11 cells, no escaped pipe):

```
section per-copy handler count in .ufo/waves/round-35/fetch/S209.receipt.txt; receipt sha256 a170c7a50b9305b3448fc85ecddb0d7b1f1c3ff5e42c78cdc2d07718c3bdd27c
```

**Equal, character for character.** Third-party agreement: `.ufo/waves/round-35/c1/frozen.json`
→ `receipts.S209.sha256` is the same digest, so registry anchor and freeze pin agree.
Cross-check of all eight (S203–S210) receipt anchors against `SOURCES.md`: **mismatches = 0**.

Read-only integration run:
`python3 -I .ufo/waves/round-35/c1/count.py --root … --frozen …/c1/frozen.json`
→ `PRED-C1-r35-v1 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET`, `exit=0`.
S209 is one of the eight closed rows; the predicate confirms exactly one well-formed row,
`status=mined`, cadence token, no pipe, anchor carrying the receipt digest, one gate-quote line.

## Findings

### F1 (MINOR, A5) — the "oldest dated 2026-10-03" has two clocks and the entry names neither
`config.jsonc.bak.1791314470` has mtime `2026-10-03 17:44:32.097653608` but btime
`2026-10-06 16:21:10.082789105` and ctime `2026-10-06 16:21:10.083846414`; the epoch suffix
`1791314470` decodes to exactly `2026-10-06 16:21:10 -0300` (`date -d @1791314470`).
mtime **preceding** btime is only possible when the mtime was set explicitly at creation —
i.e. the copy was produced on 2026-10-06 16:21 by a timestamp-preserving copy of a file last
written 2026-10-03 17:44 (the host's `omarchy-refresh-config` mints backups as
`<file>.bak.$(date +%s)`, and a preserving copy carries the source mtime).

Consequence: "the oldest dated 2026-10-03 on this host" (row cell 6, entry §2, §5) is true
only under the mtime/content reading. Under the creation-epoch reading the oldest copy is
2026-10-06 16:21 — which is exactly what round 15's sweep recorded
(`lanes/mado/round15/fetch/host-waybar-dated-backups-sweep.txt:5`). The entry's §5 does disclose
the 2026-10-06 vs 2026-10-03 discrepancy but attributes it to "this round's own sweep" without
naming the cause, and cell 6 asserts the 2026-10-03 figure unqualified at truth value `A`.
Neither figure is false; the row should say which clock it means (e.g. "content mtime
2026-10-03; copied into place 2026-10-06 16:21"). The substantive claim it serves — "the offer
is not a recent addition" — survives under either reading (≥ 2026-10-03 by content,
≥ 2026-10-06 by creation), so this is labelling, not a truth failure.

### F2 (MINOR, receipt quality) — the receipt's "oldest dated copy" section names two different files
Receipt bytes, `od -c`-confirmed:

```
--- oldest dated copy ---
/home/vgpnk/.config/waybar/config.jsonc.bak
2026-10-03 17:44:32.097653608 -0300  /home/vgpnk/.config/waybar/config.jsonc.bak.1791314470
```

The first path is the *non* oldest copy (mtime 2026-10-11), the stat line below names the actual
oldest. Read literally, the section contradicts itself. The cited support is the
`--- per-copy handler count ---` section and the located line, both of which are correct, so the
row's evidence is unaffected; but this line is a defect a future re-mint should drop or correct.
Read-only seat: not edited.

### F3 (INFO) — the count excludes the live config
"four dated copies" counts only `config.jsonc.bak*`; the live `config.jsonc` is a fifth copy and
also carries the handler (`L207/L208`). Adding it would make the claim "5 of 5". The stated
figure is exactly what the glob yields, so no defect — noted so nobody "fixes" 4 → 5.

## Residual risk / verification gaps
- **Not verified, by design of this seat:** that clicking the module actually toggles the idle
  lock at runtime. No bar was started and no command was run; the row's semantics rest on the
  command name, same boundary the entry declares. All host reads above are file reads and `stat`.
- `stat`/`ls` were run on `/home/vgpnk/.config/waybar` (read) — no writes to the host config.
- No LSP applies: the attacked artifacts are prose + receipts + a registry table, not code with a
  definition/reference surface. Text/byte inspection is the literal fallback here and is stated as
  such — no language server was consulted because none answers these files.
- Scratch, verbatim command output: `.ufo/waves/round-35/scratch/RevQuoteS209/evidence.txt`.
- Re-verify cheaply on change: the three commands in (a), the two-line Python substring test in
  (b), and `sha256sum` in (c).
