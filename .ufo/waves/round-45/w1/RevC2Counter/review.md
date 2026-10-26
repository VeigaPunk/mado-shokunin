# RevC2Counter — review of the C2 counter delta (round 45 w1)

Target: `quality/counters/c2-r45-monitor-entry.py` (PRED-C2-r45) vs parent
`quality/counters/c2-r44-gkeep-size-request-v2.py` (PRED-C2-r44-v2). 2026-10-26, seat RevC2Counter-2. Leaf: no subagents.

## 0. Integrity of what I reviewed

- Working tree == freeze: `git ls-tree 22a8dedd02…` gives blob `61bd4bee0c98ec52280a407a402908aa302ff56e` and
  `git hash-object` on the working file returns the same; `git status --porcelain` on both counter files is empty.
  The reviewed bytes are the frozen predicate.
- Pins: all 9 files in `.ufo/waves/round-45/fetch/` hash to their `PINS` sha256, and `git show
  22a8dedd02…:.ufo/waves/round-45/fetch/<name>` hashes identically (9/9, computed).

## 1. Delta inventory (diff: 125 insertions, 147 deletions; every hunk read)

1. Docstring rewritten to the r45 predicate (PRED, clauses d-j text, residuals).
2. Round constants :78-82 (PRED/BASE_DEFAULT/ENTRIES/LESSON/FETCH).
3. `ADMIT_RE`/`REFUSE_RE` deleted; `JWIDTH = 30` added (:91); `STAGED` deleted.
4. `PINS`/`PINS_URL` → the nine monitor-plane pins; `_HY` prefix constant added.
5. `CENSUS_KEYS` (:314) and `host_census` rewritten to the monitor census (:318-353).
6. `SURFACES` → 17 items (:355-373).
7. `surfaces_ok`: width bound added (:404).
8. clause e: scope-cell comparison added (:550).
9. clause h prose-contradiction check rewritten (:583-593).
10. clause i: assimilation part removed, `cl["i"] = int(not bad)` (:626).

Everything else — git/show/resolve, section/unfenced/registry, date/recheck, quote_at/occurrences,
strip_comments/quote_in_code, all_body_lines_bound, gate parsing, clauses a-g/f machinery, main — is
byte-identical to the parent (unified diff shows no hunks there).

## 2. Verified clean (changed logic re-executed against the frozen bytes)

- **clause e cell indexes are right.** `corpus/SOURCES.md:11` header is
  `| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |`;
  after `registry()`'s split+strip, idx 4 = scope, idx 5 = anchor. Code compares `r[4] == cells[4]` (:550)
  and T4 reads `row_[0][5]` — correct columns. Whitespace: `registry()` strips every cell's edges
  (inherited, identical in both files), so leading/trailing whitespace cannot fake inequality; internal
  spacing/case can (see F3).
- **clause e relaxation is bounded to the disclosed W04 shape.** New ids must gate on PINS receipts
  (clause d), and the T2 loop over *all* cited ids gated on a PINS receipt forces the location cell's last
  token to equal that pin's URL exactly (:558-570). So a new row's location is always a pin URL; the
  new "different scope" freedom (:550-551 `same == [i]`) can only ever apply to a held row sharing that
  same pin URL — precisely the S303=S162 / S307=S158 case the registration discloses.
- **SURFACES anchors: 17/17 occur in exactly one line of their pinned receipt** (computed over the pins):
  parse-mode Parser.cpp:110, parse-position :145, parse-scale :193, handle-monitor legacy:1293,
  invalid-syntax legacy:1378, add-erase MonitorRuleManager.cpp:38, get-reverse :96, default-60
  MonitorRule.hpp:46, selector Monitor.cpp:1201, closeness Monitor.cpp:837, scale-search Monitor.cpp:1001,
  json-refresh HyprCtl.cpp:242, monitors-all HyprCtl.cpp:320, explicit-position MonitorPositionController.cpp:27,
  is-number String.cpp:50, wiki-format wiki:11, wiki-sdr-eotf wiki:253. No surface can hard-fail clause j.
- **Census regexes are exactly-once on the pins**: `m_refreshRate` → 60 (×1), DELTALESSTHAN T=1 (×1),
  `std::round(m_scale * 120.0)` K=120 (×1), `"refreshRate": {:.5f}` P=5 (×1; the only refreshRate format in
  HyprCtl.cpp). The scale-search loop `for (size_t i = 1; i < 90; ++i)` (N=90 → steps 89) is genuinely the
  first such loop after the searchScale line — 9 lines below Monitor.cpp:1001, inside the scale-search block.
- **handleMonitor end detection is sound here**: signature unique (count=1), body legacy:1293-1387 ends at a
  true column-0 `}`, and there are 0 `ARGS[argno] == "` occurrences in the 80 lines after it, so even a
  mis-detected end could not inflate the count today. nkeys = 8.
- **Computed census line byte-equals the frozen registration census**:
  `hyprland monitor-rule default_refresh=60 refresh_tolerance=1 scale_step=1/120 scale_search=89
  json_refresh_decimals=5 line_keys=8`.
- **Census exemption is only the exact line**: :582-584 drops exactly the lines equal to the computed census
  string from `entry_lines`; probes show a leading-space, `> `-quoted, or double-space variant is not exempt
  (and also fails host_census's `sum(...) == 1` at :352-353 — fail-closed). Matches docstring (:43).
- **clause j width bound**: `int(b or a) - int(a) <= JWIDTH` (:404), JWIDTH=30, exactly docstring "b - a <= 30";
  single-line `:N` locators and clause g's exact locator are unaffected.
- **clause i**: no dangling ADMIT/REFUSE references (both regexes and STAGED fully removed); remaining checks
  = BAD_LOC on cited rows and unfenced entry lines + `set(PINS) <= used` pin coverage — equals docstring :47-48.
- **Docstring vs code: consistent clause-by-clause**, including the residuals line — among cells 3-6 the code
  reads only idx 4 (scope) and idx 5 (anchor), exactly as declared.
- **In-vivo**: `python3 -I <counter> --repo <lane> --rev 22a8dedd02… --base 0c89478a…` →
  `admitted=0/1 verdict=TARGET_MISSED … rev=22a8dedd…`, exit 1 (honest before-state at the freeze, no crash).
- Controls receipt `.ufo/waves/round-45/receipts/ctl-c2.txt`: P admitted with a:1…j:1; each rejection fails the
  clause its name attacks (PROSE-CENSUS h:0, WIDE-RANGE j:0+g:0, SHELL j:0+g:0, ANCHOR-PAST-EOF e:0,
  FALSE-URL e:0, FORGED-PIN d:0, HIDDEN-LINE g:0, R14-COPY b:0…) — consistent with the code as read.

## 3. Findings (severity-ranked)

### F1 — LOW — clause h prose check: narrow trailing-punctuation strip turns decorated-but-true values into "contradictions"
`c2-r45-monitor-entry.py:589`: `if v.rstrip(".,;:)` + backtick + `") != want.get(key)`. The strip set lacks
`"`, `]`, `}`, `*`, `'`, so a legitimate entry line that decorates a census token with the **true** value is
read as carrying "another value" and sets `h_ok = False` (:589-591) → the whole entry is rejected.
Probe (want `scale_search=89`, per :588-589):
- "the search therefore runs \`scale_search=89\` steps" → value `89\`` → OK
- "see \`scale_search=89\`." → `89\`.` → OK (backtick+dot stripped)
- "**scale_search=89**, computed below" → `89**,` → **TRIPS**
- "[scale_search=89](#census)" → `89](#census)` → **TRIPS**
- "the counter says \"scale_search=89\"." → `89".` → **TRIPS**
- "scale_search=[89]" → `[89]` → **TRIPS**
Direction: fail-closed — it can spuriously reject honest bytes, never admit a false claim. Exposure is the
round's own integrated entry at the data commit/tip if it decorates a census token; control P uses plain
forms and passes (ctl-c2.txt h:1). Docstring :43 ("no other entry line carries one of those six `name=`
tokens with another value") is ambiguous for decorated-true forms; the code's string reading is the strict one.
Minimal fix if re-registered: strip a small markdown/punctuation set (`"']}:*!?` added) or compare the
`(\S+)` capture after stripping all non-`[\w/.+-]` tail characters.

### F2 — LOW — clause h prose check: new `\b` allows a word-char prefix to hide a contradicting token
:588 anchors the key with `\b(%s)=(\S+)`. A word-character prefix suppresses the boundary, so the
PROSE-CENSUS-style defense can be evaded: probe `rule-scale_search=0` **is** flagged (hyphen is a boundary)
but `x_scale_search=0` is **not matched at all**. The parent had no leading `\b` (r44 matched
`set_size_request\s*\(` / `xdg_setSize=(\d+)` anywhere in the line), so this gap is introduced by this delta.
Direction: fail-open for this one net only — admission is unaffected because the exact census line must still
appear exactly once (:352-353); the risk is a contradicting prose line escaping the check that control
PROSE-CENSUS certifies.

### F3 — INFO — clause e scope equality is free-prose, exact-string
:550 compares scope cells (idx 4) by `==` after per-cell `strip()`; case, internal spacing, or a one-word
rewording make scopes "different", so the location-uniqueness requirement :551 (`same == [i]`) has bite only
against byte-identical scope text. By letter this allows any same-URL/different-scope pair, while the
registration says clause e "allows exactly that case" (the two disclosed ids); in effect it is bounded to pin
URLs (see §2), i.e. the disclosed W04 shape. Residual is fail-closed: if a future integrated row's scope ever
matched its held twin byte-for-byte, the true entry would be rejected with `clause=e` visible in the printout.

### F4 — INFO — census key name `line_keys` invites a wrong reading
:346 counts `ARGS[argno] == "` occurrences in the pinned legacy handleMonitor body = 8, but those eight are
the late extension keys (mirror, bitdepth, cm, sdrbrightness, sdrsaturation, transform, vrr, icc;
legacy-ConfigManager.cpp:1293-1387) — not the monitor-grammar keys: the pinned handler delegates the
selector/mode/position/scale to `Config::CMonitorRuleParser` at legacy-ConfigManager.cpp:1297. Docstring
:43-46 defines the term operationally, so docstring == code and the registration froze 8; but entry prose (and
a reader) must not present `line_keys=8` as "the eight syntax keys of the `monitor =` line".

### F5 — INFO — inherited nits, unchanged by this delta (not regressions)
`import json` unused (:72; also unused in the parent — `grep -c "json\."` = 0 in both);
`host_census(new_ids, reg_rev, …)` parameters unused (:318, inherited signature); `loc_ok` computed but never
read (:603, dead in both files); both counter blobs are mode 100755 (parent identical).

## 4. Residual risk and verification gaps

- I accepted the frozen controls receipt as recorded; I did not re-run `ctl/run-c2-controls.py`. My
  independent checks: full diff read, byte-level probes on all changed logic, and one in-vivo counter run at
  the freeze rev (exit 1, TARGET_MISSED).
- The F1 probe covers the common Markdown decorations; exotic forms (footnotes, raw HTML spans, entity-escaped
  punctuation) were not enumerated.
- Semantic truth beyond the pinned bytes (whether 1/120 and N-1 are the "right" notions, whether the census
  keys describe Hyprland's behaviour faithfully) is the declared non-author residual; I verified only that the
  code computes what the docstring and the frozen registration state, from the pinned bytes.
- The data commit does not exist yet (entry absent at the freeze — expected); clause-e scope cells of S303/S307
  in the eventual data commit are not verifiable today (fail-closed if they regress to byte-match the held rows).

No admission-granting defect and no always-failing check was found. The delta is faithful to its docstring;
F1/F2 are hardening notes on the h prose net.
