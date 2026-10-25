# ConnSourcePatterns — cross-source pattern finder for C2 (round 40, w1)

Seat report. Scope: held entries (config-option-table-r39.md, hyprctl-verification-layer.md,
hyprctl-flags-r28.md, dispatcher-surface-and-request-grammar-r26.md) vs round-40 candidate facts
(registration.md, native-capture.jsonl, ctl-ref-tool.py.txt, static-table.json, cap1.raw, theme
hyprland.conf). Every claim below was re-derived this seat; nothing is a restatement of the
provisional facts without a run. Host reads used: `hyprctl getoption -j KEY` (read-only verb only).

## Reproduced anchor numbers (this seat)
- `python3 -I /tmp/mado-ref.py --home /home/vgpnk --live` (ref tool, sha f96d9e0a…) → exit 0,
  70 rows: **agreement 62, agreement* 8, mismatch 0, config-only 0, live-default 0**.
- native-capture.jsonl form census: **int 44 / float 5 / str 8 / custom 13** (= 70, all set=true).
- `hyprctl getoption -j misc:bogus_xyz_notreal` → stdout `no such option`, **rc=0**.
- The 8 agreement* keys are: general:gaps_in, general:gaps_out, general:border_size,
  input:kb_layout, general:col.active_border, group:col.border_active (the held 6, verif-layer §5)
  **plus decoration:rounding and input:kb_options — both same-value double-declarer keys**.

## Findings (for the new entry: supersede / cite / amend; never rewrite)

### F1 — `set` semantics: correlation extends, meaning still unobserved (cite + extend)
Held: verif-layer :52-57 — "set=false on exactly the four options no file declares; set=true on
all 52 declared ones; [INF] its exact semantics … inferred from that correlation, not from
documentation". Also idle-lock-plane.md:224-230 (4 more undeclared keys, set=false:
cursor:inactive_timeout, cursor:invisible, misc:allow_session_lock_restore,
misc:session_lock_xray). Round-40 capture: all 70 declared keys answer set=true.
New entry should cite the held statement and extend the count (52→70 declared set=true;
8 undeclared set=false across two rounds), and keep the [INF]/[UNK] sizing: no source read
states the flag's meaning. No contradiction.

### F2 — agreement* definition: mechanical rule contradicts two held labels (supersede / reconcile)
Held definition (verif-layer :47): agreement* = live equals resolved declarer AND an earlier
declarer is shadowed — the live layer proves which file owns the value. Under it,
decoration:rounding (:85: D-LF:29=0 → T-WNG:9=0, live 0) and input:kb_options (:123:
D-IN:6=compose:caps → L-IN:11=compose:caps with inert comment, live compose:caps) are classed
plain agreement, because equal values cannot prove ownership.
The round-40 native model (ref tool `merge_live`, `_decls > 1`) labels any multi-declarer key
agreement*; my run confirms rounding and kb_options ARE the two extra agreement* keys beyond the
held 6. So the new entry must either (a) adopt the mechanical rule and explicitly supersede the
two held §3.1 labels, or (b) refine agreement* to value-distinguishing shadowing and then name a
different mechanism for the two. Note the same contradiction already exists internally between
held entries: r39 §4's counter (`merge_rows` in c3-r39-options.py, same `_decls>1` rule) would
also call rounding/kb_options agreement*. State the chosen rule; do not silently keep both.

### F3 — r39 §4 comparison catch-all cannot reproduce held gradient labels (supersede)
Held r39 §4 (:95-97): "Comparison normalises numbers for int/float types, boolean spellings, and
a scalar against a repeated tuple (`0` vs `0 0 0 0`); anything else is exact string equality."
Under that literal rule `general:col.active_border` (declared `rgb(e68e0d)`, live
`ffe68e0d 45deg`) is a MISMATCH — contradicting both the held agreement* label (verif-layer :79,
§5) and the native model (agreement*, angle inheritance). The new entry must supersede §4's
catch-all with the per-form conversions:
- colour/bool/hex forms via hyprlang configStringToInt — explains held `(truthy string parse)`
  agreement for animations:enabled (verif-layer :97: `yes, please :)` → 1) and the boolean rows;
- gradient colours + angle — explains held `(notation)` agreements (verif-layer :80
  col.inactive_border `rgba(595959aa)` → `aa595959 0deg`; :89 shadow:color `rgba(1a1a1aee)` →
  `ee1a1a1a 0deg`); these parenthetical labels are outside the five-class vocabulary and should be
  folded into the conversion sections;
- CSS gap expansion (CCssGapData) replaces the scalar-vs-repeated-tuple heuristic. Caveat to
  state: the form is per-option — general:gaps_in/gaps_out answer custom `0 0 0 0` (expanded),
  while group:groupbar:gaps_in/out answer int 5/0 (no expansion); the old broad heuristic would
  have matched any repeated tuple, which is unsound breadth;
- font-weight names (ultraheavy/normal → 1000/400, host rows `group:groupbar:font_weight_*`) are
  a distinct conversion not covered by r39 §4 at all.

### F4 — zero-mismatch result extends and survives (cite)
Held verif-layer :49/:143-147: 0 mismatch over 52 held pairs. Native model over all 70 keys:
0 mismatch (reproduced). The new entry cites the held class census and states the extension;
the §3 claim "0 mismatch on the host" now covers the full static table.

### F5 — `no such option`: held sightings predate round 40; exit code is new ground (cite)
Held observations: idle-lock-plane.md:218-219 (`misc:bogus_xyz_notreal` → `no such option`) and
executor-test-sufficiency.md:167-168 (`general:group:groupbar:gaps_out` → `no such option`).
Neither recorded the exit code; this seat measured rc=0. Vocabulary mapping is consistent:
declared key answering `no such option` → config-only (held definition verif-layer :50: "declared,
but hyprctl has no read surface"); undeclared probe key → live-default. Ref tool confirms the
mapping (native_query → None ⇒ config-only; probes ⇒ live-default).

### F6 — invocation shape `getoption -j KEY` verified; flags entries consistent (cite, footnote)
Round-40 capture/ref tool use `hyprctl getoption -j KEY` (cap.sh:15, native_query argv); cap1.raw
shows rc=0 native JSON for all 70. The round-2 layer used `hyprctl -j getoption` successfully.
Held r28 §1/§3 and r26 §A2 document client-facing flags `j/i/r` and socket-level leading-flag
stripping; nothing held restricts flag position, so no contradiction — the new entry should just
record the exact invocation it standardizes on. Also new ground: the JSON reply carries exactly
`option`, `set`, and one of int/float/str/custom (ref native_query enforces exactly-one-form).

### F7 — source/registry pointers for the new rows (risk notes)
- S162 row (SOURCES.md:174) anchors ConfigManager.cpp spans 419-451/590-623/893-968/2016-2093 —
  the gradient handler (~103-170; angle set at pinned-bytes 117-120) is outside them. Clause c
  keeps held cells byte-equal; quote the gradient handler from the round-40 fetch receipt
  (config-manager-efb5099.bin), not from the held row's anchor spans.
- S173 row (SOURCES.md:185) anchors hyprlang config.cpp expression-parsing spans; configStringToInt
  must be quoted from the fetch receipt (hyprlang-config-v0.6.8.bin), same reasoning.
- S180 already covers ComplexDataTypes.hpp CCssGapData parser at :80-120 (SOURCES.md:192) — a new
  ComplexDataTypes.hpp row (CGradientValueData/C??WeightConfigValueData toString) must use a
  different location token (counter clause e: uniqueness of new-id location).
- Own-work clause-h receipt must carry `forms int=44 float=5 str=8 custom=13` and
  `labels agreement=62 agreement*=8 mismatch=0 config-only=0 live-default=0` (N=70); both lines
  reproduced above.

## Axes
Attacks: C2 coverage (sourced) — the entry's grounded supersede/cite/amend map; indirectly C1
operability (shared reply/label model now consistent across held statements). Harms none: no held
statement is rewritten; every conflict is surfaced for the entry to supersede explicitly.

## Verification
- Ref-tool run: `python3 -I /tmp/mado-ref.py --home /home/vgpnk --live` (70 read-only getoption
  calls), labels 62/8/0/0/0; agreement* key list printed and inspected.
- Form census computed from native-capture.jsonl (44/5/8/13).
- Unknown-key probe: `hyprctl getoption -j misc:bogus_xyz_notreal` → `no such option`, rc=0.
- Pinned-bytes anchor check: `grep -n deg config-manager-efb5099.bin` → 117/120 (angle set only
  when `deg` token present); `grep -n toString complex-data-types-efb5099.bin` → 69/133/154.
- Theme file read (read-only): `general { col.active_border = $activeBorderColor }` at :3-5,
  `group { col.border_active = $activeBorderColor }` at :7-9; `$activeBorderColor = rgb(e68e0d)`
  at :1; defaults D-LF:15 gradient pair 45deg → angle inheritance chain matches.
