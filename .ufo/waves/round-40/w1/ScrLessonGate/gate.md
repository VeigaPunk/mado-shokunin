# Round 40 — `## Gate` block (draft) and assimilation ledger

Seat `ScrLessonGate`, mado round 40, wave w1, 2026-10-25. **Draft for the L1 only** — this file is
not the lesson. Every verdict slot below is left open where the executor evidence is not in; this
seat records measurements and the dispositions available, and records no verdict of its own.

Provenance: claims frozen at `.ufo/waves/round-40/registration.md` (freeze
`5e7e88525cc539563de7746361b2650802e81809`, base `9fc511ddce708327377161202f358ce37dc266ba`);
counter `quality/counters/c2-r40-forms-entry.py` (`PRED-C2-r40-v1`, clauses a–h). The lesson the L1
writes is `corpus/lessons/round-40.md`; its `## Gate` section is what clause d reads.

---

## 1. What one Gate line must satisfy (measured from the frozen counter)

From `quality/counters/c2-r40-forms-entry.py:36-37` and `:139-168`:

```
GATE_RE = ^GATE (S\d{3,}) receipt=(\S+) sha256=([0-9a-f]{64}) quote="(.+)"\s*$   # on line.strip()
```

and, per cited id, the line counts only when **all** of these hold:

1. `receipt` starts with `.ufo/waves/round-40/fetch/` (`FETCH`, `:30`) — a receipt anywhere else
   (e.g. `.ufo/waves/round-40/c1/native-capture.jsonl`) cannot bind a row;
2. the receipt is committed at `REV` and `sha256(git show REV:receipt)` equals the declared digest;
3. `3 <= len(quote.split()) <= 25` on the **raw** quote;
4. `norm(quote)` occurs in `norm(receipt_bytes)` where
   `norm = strip <script|style> → strip <[^>]+> → html.unescape → collapse whitespace` (`:79-83`);
5. clause g: one **entry** line contains both `\b<id>\b` and the quote with whitespace collapsed;
6. clause b: at least **4 distinct** `source: S###` lines inside the entry's first 20 lines, plus
   `verified-at: 2026-10-25` and a `recheck:` value matching `^\d{4}-\d{2}-\d{2}|\d+d|on-[a-z-]+`.

### 1.1 Hazard: `norm()` deletes C++ template and comparison spans (measured)

`norm()`'s tag-strip runs over the receipt *and* the quote. On the C++ receipts this eats code:

| receipt | raw bytes | `norm` bytes | effect |
|---|---|---|---|
| `.ufo/waves/round-40/fetch/complex-data-types-efb5099.bin` | 6116 | 4095 | one stripped span, raw offsets **1833–2227** (394 B) |

That span starts at `i < m_colors.size(); ++i)` and ends at the `>` of a later `->`, so it deletes
`CGradientValueData::toString` (`ComplexDataTypes.hpp:69-77`). Consequence, measured:

- quote `result += std::format("{}deg", sc<int>(m_angle * 180.0 / M_PI));` (line 77) → `occ=0` in
  `norm(receipt)`; **this sentence cannot be a Gate quote for this counter**.
- a quote containing a *balanced* `<…>` pair (e.g. the hyprlang signature at `:185`) binds
  (`occ=1`) only because `norm(quote)` strips it identically — an accidental binding that depends on
  the surrounding strip pattern, not on the line. Prefer quotes with **no** `<` or `>` at all.

Command: `python3` with the counter's own `norm()` over the committed bytes (this seat, 2026-10-25);
per-quote results in §2.3.

---

## 2. Gate lines

The two held rows are ready to paste except for the re-bind step in §2.4. The two new rows are
templates: their ids are the L1's to assign and their receipts are not yet committed. The fences
below are for reading only — the lesson's `## Gate` takes each line bare at column zero, as round-39's
does (`section()` collects every line between `## Gate` and the next `## `, so a fence is harmless but
not the house style).

### 2.1 Held rows C2 re-opens

```
GATE S162 receipt=.ufo/waves/round-40/fetch/config-manager-efb5099.bin sha256=9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b quote="if (var.find("deg") != std::string::npos) {"
GATE S173 receipt=.ufo/waves/round-40/fetch/hyprlang-config-v0.6.8.bin sha256=fa1b6898f2f1676de73220450f18f09603f0c3f8833e4c0a7c42c12aebe1de3e quote="} else if (VALUE.starts_with("true") || VALUE.starts_with("on") || VALUE.starts_with("yes")) {"
```

- The embedded `"` characters are safe: `GATE_RE`'s `quote="(.+)"` is greedy and the round-trip
  `m.group(4) == quote` was verified for both lines (this seat). The round-39 lesson avoided internal
  double quotes; this round's two load-bearing sentences contain them. If the L1 prefers the older
  convention, the alternates in §2.3 bind equally.
- Both digests are **byte-identical to the round-39 receipts** (`9db68cf4…` = `S162-r39.bin`,
  `fa1b6898…` = `S173-r39.bin`, `corpus/lessons/round-39.md` Gate lines), so the held anchors stand
  and the re-open is a byte-for-byte re-fetch, not a new anchor.

### 2.2 New rows (templates — the L1 fills id, receipt name and digest)

```
GATE <NEW-A: ComplexDataTypes.hpp @ efb5099> receipt=.ufo/waves/round-40/fetch/complex-data-types-efb5099.bin sha256=95733223b115510dda23e753aae64e373205cc7081b0eeb204df866ea7e68807 quote="return std::format("{} {} {} {}", m_top, m_right, m_bottom, m_left);"
GATE <NEW-B: own-work live census> receipt=.ufo/waves/round-40/fetch/<census-receipt>.txt sha256=<64 hex — re-derive from the committed blob> quote="<3-25 words that occur in that receipt>"
```

`<NEW-A>` binds the **CSS-gap** expansion rule (`ComplexDataTypes.hpp:133-135`); the gradient
`toString` sentence is unquotable under this counter (§1.1). The gradient **angle** rule is carried by
the S162 row above (or by a new ConfigManager row, §3), and the gradient **output shape**
(`<hex> … <N>deg`) must then be cited in entry prose without a Gate binding — clause g only requires
one bound line per id.

`<NEW-B>` is the own-work census row and carries clause h. Its receipt must contain, verbatim and at
line start:

```
forms int=44 float=5 str=8 custom=13
labels agreement=62 agreement*=8 mismatch=0 config-only=0 live-default=0
```

plus the **sha256 of `tools/mado-options.py` at REV**, and the entry must repeat both lines verbatim
(`c2-r40-forms-entry.py:203-222`). Arithmetic the counter enforces: `44+5+8+13 == 62+8+0+0+0 == 70`.

- **Forms line — independently reproduced by this seat** from
  `.ufo/waves/round-40/c1/native-capture.jsonl` (sha256
  `1fe39c0528f1b11d7f69bf41ac236f39ff6e00b9b8a275f4e94b06c5189b4b25`, 70 non-blank lines, each line
  exactly one of `int|float|str|custom`): `{'int': 44, 'float': 5, 'custom': 13, 'str': 8}`, sum 70.
  Command: `python3 -c` over the jsonl counting the form key of each object (this seat).
- **Labels line — not filled by this seat.** `agreement=62 agreement*=8 mismatch=0` is the
  registration's number; the census seat owns it and `config-only=0 live-default=0` is forced by the
  sum rule (62+8=70). Do not paste the labels line until the census receipt exists and states it.
- The capture file itself is **not** a valid Gate receipt (it is not under `fetch/`). The census
  receipt must be a new file under `.ufo/waves/round-40/fetch/`; it may quote the capture's sha.

### 2.3 Quote candidates, measured (occ = occurrences in `norm(receipt)`)

| row | file:line | words | occ | quote |
|---|---|---|---|---|
| S162 | `ConfigManager.cpp:117` | 5 | 1 | `if (var.find("deg") != std::string::npos) {` |
| S162 | `ConfigManager.cpp:120` | 10 | 1 | `DATA->m_angle = std::stoi(std::string(var.substr(0, var.find("deg")))) * (std::numbers::pi / 180.0); // radians` |
| S162 | `ConfigManager.cpp:129` | 5 | 1 | `if (DATA->m_colors.size() >= 10) {` |
| S162 | `ConfigManager.cpp:607` | 3 | 1 | `m_config->registerHandler(&::handleBind, "bind", {true});` |
| S173 | `config.cpp:259` | 9 | 1 | `} else if (VALUE.starts_with("true") || VALUE.starts_with("on") || VALUE.starts_with("yes")) {` |
| S173 | `config.cpp:196` | 6 | 1 | `// Values with 0x are hex` |
| S173 | `config.cpp:185` | 7 | 1 | `static std::expected<int64_t, std::string> configStringToInt(const std::string& VALUE) {` (accidental binding, §1.1) |
| NEW-A | `ComplexDataTypes.hpp:134` | 9 | 1 | `return std::format("{} {} {} {}", m_top, m_right, m_bottom, m_left);` |
| NEW-A | `ComplexDataTypes.hpp:148` | 9 | 1 | `int64_t m_value = 400; // default to normal weight` (collapsed from the aligned declaration) |
| NEW-A | `ComplexDataTypes.hpp:159` | 12 | 1 | `{"thin", 100}, {"ultralight", 200}, {"light", 300}, {"semilight", 350}, {"book", 380}, {"normal", 400},` |

Rejected candidates (measured, so the L1 does not retry them):

| candidate | why rejected |
|---|---|
| `ComplexDataTypes.hpp:77` `result += std::format("{}deg", …)` | `occ=0` — deleted by the tag-strip span (§1.1) |
| `ComplexDataTypes.hpp:69` `virtual std::string toString() const {` | `occ=2` (also `:133`, `:154`) — binds, but ambiguous |
| `ConfigManager.cpp:510` `Hyprlang::CConfigCustomValueType{&configHandleGradientSet, configHandleGradientDestroy,` | 2 words (floor is 3) and `occ=2` (`:510`, `:2178`) |
| `ConfigManager.cpp:112` `DATA->m_colors.clear();` | 1 word |
| `ConfigManager.cpp:111` `CVarList2 varlist(std::string(V), 0, ' ');` | binds only in the **collapsed** form (raw has two spaces) — entry line must then carry the collapsed form; avoid |

### 2.4 Re-bind at commit (QUALITY 7)

The digests above are **work-window hashes of uncommitted `fetch/` files** (this seat read them at
2026-10-25 17:5x; several were still being written by sibling seats). Before the Gate block lands:

```
for p in config-manager-efb5099.bin hyprlang-config-v0.6.8.bin complex-data-types-efb5099.bin; do
  git -C . show <REV>:.ufo/waves/round-40/fetch/$p | sha256sum; done
```

and correct any line whose digest differs. Note the two duplicate-byte receipt pairs now in `fetch/`
(`omarchy-v3.8.4-screen-recording.bin` ≡ `host-indicator-screen-recording.bin`, sha
`28491cd3…`; `omarchy-v3.8.4-notification-silencing.bin` ≡ `host-indicator-notification-silencing.bin`,
sha `312900d1…`) — pick one path per row and keep both files only if the duplication is deliberate.

---

## 3. Anchor conflict on the two held rows (measured) — the L1 decides

**S162** (`corpus/SOURCES.md:174`), cell 1:
`src/config/legacy/ConfigManager.cpp:419-451,590-623,893-968,2016-2093 @ efb5099…, sha256:9db68cf4…, 90963 B`;
cell 5 (subject): "Hyprlang-era legacy windowrule keyword handlers, named special-category
reconstruction, and reload traversal".

- The gradient handler `configHandleGradientSet` is at **`:103-165`** (handler `:103`, deg guard
  `:117`, angle assignment `:120`, max-colours guard `:129`, transparent fallback `:151`), and its
  custom-type registration sits at `:510` and `:2178`. **None of those lines lies inside any of the
  row's four ranges.** The only S162 line inside a declared range that this round's evidence uses is
  `:607` (the round-39 Gate quote).
- So the registration's phrase "held S162 (ConfigManager.cpp gradient handler, re-opened)" asks the
  row to support a sentence its declared range and subject do not cover.

**S173** (`corpus/SOURCES.md:185`), cell 1:
`src/config.cpp:619-667,755-827,983-986 @ 3a1c1b25…, sha256:fa1b6898…, 43049 B`;
cell 5: "Hyprlang RHS `{{…}}` expression parsing relevant to bind config values; not bind-table
semantics".

- `configStringToInt` is at **`:185-273`** (signature `:185`, hex `:196`, `rgba(` `:198`, `rgb(`
  `:232`, bool prefixes `:259`) — outside all three ranges.
- Inherited gap, not this round's: round-39's own S173 Gate quote is `:869`
  (`avoid cases where a category is called the same as a handler`, measured 1 occurrence), which is
  **also outside** the declared ranges. The row's ranges have been narrower than the quotes bound to
  it since round 39. Recorded here and routed (QUALITY 52), not repaired.

Consequences under the frozen counter: clause c keeps a held row's cells 1–10 byte-equal to BASE, so
the L1 **cannot** widen either range this round; clause d checks the quote against the *receipt*, not
against cell 1, so both lines in §2.1 **pass the counter** while the row's declared anchor stays
narrow. The defect is a QUALITY 2/42 (source anchor) and 27 (reproducible anchor) defect, not a
counter failure — which is exactly why it must be recorded in the lesson rather than left to the
counter to catch.

Dispositions (the L1 owns the choice; the frozen registration forbids dropping S162/S173 from the
cited set):

- **D-a — cite as registered, record the mismatch.** Keep §2.1, and state in the entry and the lesson
  that the relied-on lines (`:117`, `:259`) lie outside the rows' declared ranges. Cheapest; a reader
  following cell 1 lands on different code than the Gate quote.
- **D-b — cite both and add two exact-region rows.** Cite S162/S173 for what their ranges do cover
  (handler registration at `:607`; the expression evaluator) and open two new rows for
  `ConfigManager.cpp:103-165` and `config.cpp:185-273`, cited for the conversion rules. Costs a
  same-URL second row, which triggers the QUALITY 17 screen (record it: same canonical URL, distinct
  location and subject; the staged row is not appended as-is) and will surface as a census W04
  warning. Clause e is satisfied because a new row's locator (last whitespace token of cell 1) must be
  unique — `…:103-165` and `…:185-273` are unique against every existing row.
- **D-c — bind only inside the declared ranges.** S162 `:607` (3 words, `occ=1`) and an S173 quote
  inside `:619-667`/`:755-827`/`:983-986`, with the conversion rules cited to new rows. Strictest on
  QUALITY 2; loses the deg-guard sentence from the Gate block entirely.

This seat's reading (not a verdict): D-b, with the criterion-17 screen written into the lesson,
because it keeps the registration's cited set intact *and* gives each relied-on sentence an anchor
whose declared range contains it.

---

## 4. Assimilation ledger — shokuknow `merge/mado/` (read-only)

Package root `/home/vgpnk/Projects/shokuknow/merge/mado/` (`MERGE-REPORT.md:31,36`; campaign
`corpus-expansion-1`). Both candidates are package **new-file** entries; neither exists in the lane
(`ls corpus/knowledge | grep -i 'host-bar\|producer'` → no match; the only held entry on the theme is
`corpus/knowledge/waybar-walker-semantics.md`, sha256
`1d1e785a01ceac5759f3a55c48dedfb59fcc561d8645be925eb954bbd1dc8925`, 478 lines, measured 2026-10-14).
Nothing from the package is appended by this seat; no staged row is appended as-is.

### 4.1 K1 — `host-bar-producers-r28.md` (package round3)

Source bytes: `/home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge/host-bar-producers-r28.md`,
4002 B, sha256 `9f3f76a2328dbfe0e9751ec0e445c0eb1ebdc26e1a20d12284908abe72fe94f0`.

- **Amends:** `corpus/knowledge/host-bar-and-idle-binding-r26.md` — **absent from the lane**
  (`grep -rn 'host-bar-and-idle-binding' corpus/` → 0 hits). The amendment's parent was never
  admitted, so K1's "amends" clause hangs off nothing (QUALITY 8: a path is landed only after it
  exists at a named revision).
- **Scope vs `PROVINCE.md`:** IN. `PROVINCE.md:3-4` owns "the Hyprland/waybar/walker configuration
  plane and display behavior on this host"; `:6-9` names `~/.config/waybar/`; `:11-12` makes every
  config tree read-only. K1 reads the host config and omarchy's stock scripts under
  `~/.local/share/omarchy` (round-19 refinement: the theme plane's consumers are the owned chain) and
  writes nothing. No secret, no model endpoint, no localized-documentation channel.
- **QUALITY bar (criteria 1–64):**
  - 1/41 falsifiable, 3/43 OBS/INF/UNK separated, 5/45 rejections kept — pass on the text.
  - 2/42 source per claim — pass: `source:` block names S224/S228/S231 with tag pins; each table row
    carries an anchor.
  - 27 reproducible anchor — **partial**: the two indicator scripts are tag-pinned and today's fetch
    reproduces the host bytes exactly (`screen-recording.sh` 169 B sha `28491cd3…`,
    `notification-silencing.sh` 174 B sha `312900d1…`, host copies byte-identical, and v3.8.3 serves
    the same shas — `w1/ExecFetchK2Sources/quotes.md` §1-2). The **upstream config row S231 was not
    re-fetched this round** (no `basecamp/omarchy/.../config/waybar/config.jsonc` in
    `.ufo/waves/round-40/fetch/`), so its "5114 B upstream" claim is unverified here.
  - 14 census (missing and extra members named) — **fail inside K1's own text**: its table lists
    **seven** `json` elements (`weather`, `screenrecording`, `idle`, `notification-silencing`,
    `voxtype`, `gkeep`, `ai-usage`) while its INF sentence says "**six** JSON producers". Host bytes
    today agree with the table, not the sentence: `grep -c '"return-type": "json"'
    ~/.config/waybar/config.jsonc` → **7** (this seat, 2026-10-25).
  - 17 duplicate-URL screen — **not recorded**: K1's S228 (`…/v3.8.4/default/waybar/indicators/idle.sh`)
    is byte-identical to lane row **S207** (`corpus/SOURCES.md:209`, host `idle.sh`, 159 B, sha
    `6d8d2c11…`). Same bytes, different locator class (upstream vs host) → screen and decide, per
    criterion 17, rather than append a second row for the same bytes.
  - 15/16 era fence — pass (all upstream URLs tag-pinned `v3.8.4`).
  - 46 regular-file targets — pass (raw.githubusercontent URLs, direct files).
- **Held coverage vs `waybar-walker-semantics.md`:** the producer map is largely **already held** —
  held names `weather.sh` (`:88`), `omarchy-update-available` (`:63`), `omarchy-voxtype-status`
  (`:219`), `indicators/screen-recording.sh` (`:202`), `indicators/idle.sh` (`:208`),
  `indicators/notification-silencing.sh` (`:214`) and `~/.local/bin/ai-usage` (`:236`), and §4 maps the
  five signals. **Genuine increment:** `custom/gkeep` and its host-local producer — held has **0**
  occurrences of `gkeep`; held's `modules-right` is "7 entries `:21-29`" (`:79`) while today's config
  has **8** entries with `custom/gkeep` at `:23` and its block at `:236-245` (config 6354 B, sha
  `a408a33d…`, mtime 2026-10-17 17:02:56 — **after** held's 2026-10-14 measurement), which shifts every
  held anchor after `:235` by +11 (held's `custom/ai-usage (:235-248)` is today `:246-259`).
  **Not held, contrary to the registration:** the byte comparison. The only `5114` in the lane is a
  *local backup* size (`corpus/knowledge/waybar-walker-plane.md:297`,
  `config.jsonc.bak.1791314470`, 2026-10-03), and `6354` occurs nowhere in `corpus/` — so "6354 B host,
  5114 B upstream is held" misstates the held datum on both numbers.
- **Verdict slot:** `OPEN — L1`.
  - *Reason (draft):* scope is IN and one increment is real (the gkeep element/producer with today's
    anchors), but the candidate as written has an absent amendment parent, an unrecorded same-bytes
    screen against S207, a producer-count contradiction inside its own table, and an upstream
    comparison that is neither held nor re-derived. It cannot be appended as a new file; at most its
    gkeep increment can be **re-grounded as a dated amendment to the held entry**.
  - *Flip condition:* K1 becomes admissible as a row when (a) the lane admits a
    `host-bar-and-idle-binding-r26.md` parent or the amendment is re-targeted at the held entry;
    (b) the S207/S228 same-bytes screen is recorded; (c) "six JSON producers" is corrected to seven
    against host bytes; (d) the upstream `v3.8.4` config is fetched this round and its size/hash
    recorded (5114 B confirmed or corrected).

### 4.2 K2 — `host-producer-outputs-r29.md` (package round4)

Source bytes: `/home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge/host-producer-outputs-r29.md`,
3383 B, sha256 `b4c0473e37b7a674e0cbf37f384f4f06ca544345b1d1102efa7c9599517cefed`.

- **Amends:** K1 (`host-bar-producers-r28.md`) — itself unadmitted in the lane (§4.1), so K2's chain
  also hangs off an absent entry.
- **Scope vs `PROVINCE.md`:** IN for the producer bodies and the read-only queries (`pgrep`,
  `makoctl mode`, the cache path). IN with a **class caveat** for S241: the row's anchor is the
  ai-usage cache's `updated_at`, a volatile telemetry field — the same class the round-39 D2 label
  got wrong (§5). `PROVINCE.md:11-12` (read-only) is respected: nothing was run, no network fetch of
  `wttr.in`.
- **QUALITY bar:**
  - 27 reproducible anchor — **pass for S237/S238**, **fail for S241**. S237/S238: tag-pinned,
    re-fetched 2026-10-25 (169 B `28491cd3…`, 174 B `312900d1…`), host copies byte-identical
    (`cmp` rc=0, four comparisons), v3.8.3 identical → the identity is not a tag artefact. S241: the
    staged value `"updated_at": "2026-10-23T22:52:44Z"` greps **0** in `~/.cache/ai-usage/status.json`
    and `~/.cache/ai-usage/inception-ledger.json` (this seat, 2026-10-25; live value
    `2026-10-25T20:52:19Z`) → unverifiable, must not be appended.
  - 14 census — **fail**: K2 says "three of the bar's **five** JSON producers"; host bytes say
    **seven** (`return-type: json` count 7, `w1/ExecK2HostReads/host-reads.txt` §1 and this seat's
    `grep -c`).
  - 3/43 separation — pass in form, but two of its present-tense sentences have moved: the idle chip
    is claimed to show "Idle lock disabled" because no `hypridle` runs; today `hypridle` **is** running
    (pid 1680, `pgrep -a -x hypridle`, `w1/ExecK2HostReads/host-reads.txt` §4, QUERY-3), so the chip
    renders the empty branch. A round-3 RUN payload is a dated observation, not standing state.
  - 62 (a zero count needs a positive probe in the same channel) — **advisory**: "no
    `gpu-screen-recorder` process is running" is recorded as `pgrep` rc=1 with no positive probe from
    the same pattern; the zero is suggestive, not proven, and the entry should carry the probe or the
    UNK label.
  - 17 duplicate screen — S237/S238's URLs are new to the lane (`grep -c
    'raw.githubusercontent.com/basecamp/omarchy' corpus/SOURCES.md` → 8 rows, none of them these
    indicator scripts); the *idle* indicator's bytes are held as S207, so any K2-derived idle row is
    the same-bytes case screened in §4.1.
- **Held coverage vs `waybar-walker-semantics.md`:** round 3 already **RUN** the four indicator
  payloads (held `:135-149`), so "current output" is held as a 2026-10-14 snapshot, not as a rule.
  **Genuine increment:** the *decidability rules* (which producers answer offline: `pgrep`/`makoctl`,
  cache-only ai-usage, the `gkeep` shim's local count) and the host-local producer contracts — none of
  which held states. Not held: `gkeep` (0 hits), the `gkeep/waybar.py` contract, the ai-usage
  `cache_path()` line.
- **Verdict slot:** `OPEN — L1`.
  - *Reason (draft):* admit-on-province is plausible for the rules, and its two upstream anchors are
    the strongest bytes this theme has produced in-round; but as written it carries a volatile anchor
    (S241), a wrong producer count (5 → 7), and one reversed present-tense sentence (idle chip). Those
    are corrections the L1 must make before any row is appended, and S241 must be refused as staged.
  - *Flip condition:* K2 becomes admissible when (a) S241 is re-cut without the raw timestamp — the
    seat's own replacement is the quotable property `updated_at_within_24h=true` plus the key-shape
    census (12 provider keys) — (b) "five JSON producers" becomes seven against host bytes, (c) the
    idle sentence is dropped or dated and marked superseded by today's `hypridle` pid 1680, (d) the
    parent chain is re-grounded into the held entry.

### 4.3 Id collision (screened, not appended)

Three different rows have carried `S224`: the package's `SOURCES.append.md:28` S224 (host waybar
config bytes), the absent-defect-register's S224 (ai-usage cache — §5), and **no lane S224**
(`.ufo/waves/round-40/w1/ExecQuarantineSlice/registry-rows.txt` → "ABSENT from SOURCES.md"). The same
holds for S228/S231/S237–S241 (all absent from the lane registry). No renumber map is needed because
nothing is appended; the guard itself is another seat's item (`ExecAssimIdGuard-2`).

---

## 5. D2 correction note (draft, append-only — for `corpus/lessons/round-40.md`)

> **Correction to `corpus/lessons/round-39.md` (D2, over-label; append-only).** The round-39
> assimilation ledger (`corpus/lessons/round-39.md:73`) records the quarantined register row S224 as
> "absent, refused (fabrication class)". The seat evidence it cites says the opposite of fabrication:
> `.ufo/waves/round-39/w1/ExecQuarantineSlice/verdicts.md:14` — "No row is flagged as fabrication …
> Volatile timestamp rotated; row not appendable", and its summary repeats "no row is flagged as
> fabrication". The row's anchor is a volatile telemetry field, the ai-usage cache's `updated_at`:
> `grep -c '2026-10-23T22:52:44Z' ~/.cache/ai-usage/status.json ~/.cache/ai-usage/inception-ledger.json`
> → `0`, `0` (2026-10-25), while the same file's live field reads `2026-10-25T20:52:19Z`. Corrected
> class: **unverifiable — rotated volatile timestamp**, not fabrication. The refusal stands (the row
> stays out of the registry), but on the right ground: an anchor that rotates between reads cannot
> anchor a row (QUALITY 27), and no evidence suggests an invented payload. Id note: the "S224" in that
> sentence is the absent-defect-register's row (ai-usage cache), not the shokuknow package's
> `SOURCES.append.md:28` S224 (host waybar config bytes) and not a lane row — `corpus/SOURCES.md`
> holds no S224. This note corrects the label only; round 39's text is not edited.

---

## 6. What the L1 must fill or decide

| # | item | state |
|---|---|---|
| 1 | ids for the two new cited rows (clause c: ≥2 ids absent from BASE, `opened 2026-10-25`, status `mined`, used-by naming the entry) | open |
| 2 | the own-work census receipt under `fetch/` + its digest + quote, and the labels line | open (census seat) |
| 3 | re-bind all four digests from the committed blobs (§2.4) | open |
| 4 | anchor disposition for S162/S173 (§3, D-a/D-b/D-c) | open — L1 |
| 5 | K1 and K2 verdicts + reasons (§4) | open — L1 |
| 6 | the entry's first-20-lines header: ≥4 `source:` lines, `verified-at: 2026-10-25`, `recheck:` (clause b) | open (entry author) |
| 7 | the `corpus/README.md` index row (clause f) and the four cited rows' used-by cells (clause c) | open (L1) |

No compositor verb beyond `hyprctl version`/`getoption -j` was run by this seat; no host config tree,
service or sibling lane was written; no package transaction was run; no tool was installed.

---

## 7. Paste-ready skeleton for the lesson's `## Gate`

Fenced for reading. Paste the body into `corpus/lessons/round-40.md` under `## Gate` with the
placeholders filled and the digests re-bound (§2.4). The paragraph after the lines is the round-39
house pattern (what was opened, when, and by whom) — replace it with the L1's own measured sentence.

```
GATE S162 receipt=.ufo/waves/round-40/fetch/config-manager-efb5099.bin sha256=9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b quote="if (var.find("deg") != std::string::npos) {"
GATE S173 receipt=.ufo/waves/round-40/fetch/hyprlang-config-v0.6.8.bin sha256=fa1b6898f2f1676de73220450f18f09603f0c3f8833e4c0a7c42c12aebe1de3e quote="} else if (VALUE.starts_with("true") || VALUE.starts_with("on") || VALUE.starts_with("yes")) {"
GATE <NEW-A> receipt=.ufo/waves/round-40/fetch/complex-data-types-efb5099.bin sha256=95733223b115510dda23e753aae64e373205cc7081b0eeb204df866ea7e68807 quote="return std::format("{} {} {} {}", m_top, m_right, m_bottom, m_left);"
GATE <NEW-B> receipt=.ufo/waves/round-40/fetch/<census-receipt> sha256=<64 hex> quote="<3-25 words>"

Every receipt above was fetched by a round-40 seat on 2026-10-25 (`raw.githubusercontent.com`,
`HTTP 200`, digests re-derived from the committed blobs). S162 and S173 are byte-identical to their
round-39 receipts (`9db68cf4…`, `fa1b6898…`), so their held anchors stand; the two new rows were
opened this round. The relied-on lines lie outside S162's and S173's declared location ranges
(`ConfigManager.cpp:103-165`, `config.cpp:185-273`) — recorded here per QUALITY 2/42 and 27, not
repaired (a held row's cells are byte-equal at REV, PRED-C2-r40-v1 clause c).
```
