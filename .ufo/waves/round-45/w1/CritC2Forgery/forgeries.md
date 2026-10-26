# C2 forgeries against PRED-C2-r45 — nine false artifacts the frozen counter admits

Seat `CritC2Forgery`, round 45 w1. Target: `quality/counters/c2-r45-monitor-entry.py` (read-only; the file is not
edited by this seat). Claim under attack: C2 coverage — `corpus/knowledge/hyprland-monitor-rule-r45.md` admitted
`1/1` means the entry's claims are sourced.

**Axes.** (1) *Soundness*: how many false entry/registry/lesson sets the predicate admits. (2) *Closability*: a
tightening that keeps the frozen positive control P admitted. (3) *Declaration*: whether the frozen docstring already
declares the hole (a declared residual is a known tradeoff; an undeclared one is a defect in the predicate's own
account of itself).

**Method.** P is rebuilt from the positive-control recipe (freeze `22a8ded`, `l1-draft/build-pos.py`), then each
forgery is one commit on top of P changing only the artifact named below (`build-forgeries.py` in this directory).
Every score is `python3 -I quality/counters/c2-r45-monitor-entry.py --repo <clone> --rev HEAD --base 0c89478af…`.
Receipts in this directory: `p-control.txt` (P admitted), `forgery-diffs.txt` (the forged lines, cited below by line),
`forgery-scores.txt` (per-forgery full counter output), `frozen-and-tightened-matrix.txt` (60 runs: 5 counters ×
P + 9 forgeries), `evidence.txt` (pin/counter chapters at the cited locators), `quote-check.txt` (31/31 quotes: 19 at pin/counter
locators, 12 forged-line fragments at their computed `forgery-diffs.txt` line). The two scripts run from an empty
scratch directory (`python3 -I build-forgeries.py`, then `python3 -I tighten.py`, then `evidence.py`), so every number
below is reproduced by the shipped files, not by a leftover tree.

**Result.** All nine are admitted: `admitted=1/1 verdict=TARGET_MET`, exit 0, every clause `a:1 … j:1`. The frozen
control set in `receipts/ctl-c2.txt` (10/10 as designed) is disjoint from all nine classes, so its PASS says nothing
about them: the controls test *provenance* (bytes, digests, URLs, locator width) and *one* unfenced hidden line; none
tests a claim, a cell the counter does not read, or a fence.

| # | forgery | artifact | clause that should catch it | frozen | disposition |
|---|---|---|---|---|---|
| F1 | inverted rule-lookup claim beside the true erase quote | entry §2 (S304 line + lookup line) | g (quote+locator binding), j | admitted | declared residual (counter:62) |
| F2 | decision table overclaims, state column forged | entry header table | g/j bind only lines naming an id | admitted | declared residual (counter:63) |
| F3 | census contradicted **in tokens**, separated from `=` | entry tail | h (prose census scan) | admitted | **closed by T1** |
| F4 | census contradicted **in words** | entry tail | h | admitted | declared residual (words are not tokens) |
| F5 | registry row claims supersession of held rows S158/S162 | `corpus/SOURCES.md` cell 6 | c (reads cells 1,5,7-10 only) | admitted | **closed by T2** (supersession only; other cell-6 text stays residual) |
| F6 | false decision table inside a fenced block | entry tail | b/g/j/h all skip fenced lines (counter:16) | admitted | **closed by T3** |
| F7 | §6 claims a host state and a verdict the cited receipt refutes | entry §6 | i (no clause reads `receipts/`) | admitted | **closed by T4** |
| F8 | README index row claims `merged` + `supersedes S290-S297` | `corpus/README.md` row | f (counter:615 matches the prefix only) | admitted | **closed by T5** |
| F9 | the sentence that satisfies the closeness surface is inverted, locator and keyword kept | entry §3 | j (locator+keyword, not truth; counter:64) | admitted | declared residual |

Tightenings are *copies* of the counter in scratch (`tighten.py` reproduces the five edits as exact string
replacements); the lane's frozen counter is untouched. Each tightening keeps **P admitted** and rejects exactly its
target, with no collateral on the other eight (`frozen-and-tightened-matrix.txt`: 60 runs, 5 misses, one per
tightening, and P `admitted=1` under all five).

---

## F1 — a true quote at a true locator, inverted claim in the same line (and the next)

`forgery-diffs.txt:14` — entry §2 — and `forgery-diffs.txt:11` (the S304 line):
`The lookup does not run in reverse: it takes the first match from the top of the list, so a rule written in an
earlier config file wins over a later one, and an exact selector always loses to a "desc:" rule
(Hyprland-MonitorRuleManager.cpp:96-106).` and, in the S304 line, `the stored order is the order rules are honoured
in`.

**False against the pins.** `Hyprland-MonitorRuleManager.cpp:96`: `for (auto const& r : m_rules | std::views::reverse)
{` — the scan *is* reverse, so the newest matching rule wins, and `Hyprland-MonitorRuleManager.cpp:103` is the
empty-selector fallback (`for (auto const& r : m_rules) {`). The forged sentence reverses both facts and keeps the
locator `:96-106` that contains line 96.

**Why the counter passes.** Clause g binds id-naming lines: the S304 line still carries the S304 Gate quote
`std::erase_if(m_rules, [&x](const auto& e) { return e.m_name == x.m_name; });` (MRM.cpp:38) and the exact quote
locator, so `all_body_lines_bound` is satisfied. Clause j binds a locator *and* a keyword: the forged sentence
contains the word "reverse" and the range `:96-106`, so `surface=get-reverse line=96 cited=1`
(`forgery-scores.txt`, F1). The claim is wrong; every mechanical binding is intact.

**Disposition: declared residual** — counter:62, "a true quote at a true locator can stand beside a claim it does not
support". A counter cannot read the sentence. The only sound defence is the non-author reading the L1 already
declares; no tightening is proposed because any lexical negation test ("not", "does not") is trivially reworded
(`the scan runs from the top`).

## F2 — the decision table overclaims and its state column is forged

`forgery-diffs.txt:25` and `forgery-diffs.txt:30` (two header-table rows):
`| What does \`WxH\` without \`@RATE\` request? | the output's fastest mode at that size | OBS (verified on the host) |`
and `| Does the documented \`sdr_eotf\` key work on a \`monitor =\` line? | yes, on \`monitor =\` lines too | OBS (host) |`.

**False against the pins.** `Hyprland-MonitorRule.hpp:46`: `float m_refreshRate = 60; // Hz` — a mode without
`@RATE` asks for 60 Hz, not the fastest mode. The `sdr_eotf` row contradicts the entry's own §5 and
`Hyprland-legacy-ConfigManager.cpp:1351-1379` (the key loop has no `sdr_eotf`). The state column is the worse half:
`OBS (verified on the host)` says a host observation was made, and no host run of that row exists.

**Why the counter passes.** These rows name no id, so clause g has nothing to bind, and clause j only needs *some*
line per surface — the true §1/§5 lines still satisfy all seventeen (`clause=j surface=… cited=1` unchanged). The
state column (`OBS`/`INF`/`UNK`) is read by no clause at all.

**Disposition: declared residual** — counter:63, "a decision table naming no id is not bound". F2's host-state
overclaim is partly reachable by T4's idea (a state claim citing a receipt must match it) but the row cites nothing,
and the unbounded general case stays.

## F3 — the census contradicted in tokens, one space from being caught

`forgery-diffs.txt:41` (entry tail):
`INF The census line above is narrower than the searched grid: scale_search = 44 steps and default_refresh : 45 Hz,
so a scale written with two decimals may land a whole screen away.`

**False against the pins.** `Hyprland-Monitor.cpp:1010`: `for (size_t i = 1; i < 90; ++i) {` gives 89 search steps
(`DERIVED scale_search=89` in `evidence.txt`), and `Hyprland-MonitorRule.hpp:46` gives 60, not 45.

**Why the counter passes — the mechanism.** Clause h's prose scan is
`re.findall(r"\b(%s)=(\S+)" % "|".join(CENSUS_KEYS), l)` (counter:588): the key must touch `=` with no space.
`scale_search = 44` and `default_refresh : 45` therefore contain no match at all, and the exact census line itself
is excluded from the scan. This is the one forgery class that is both *unit-level* (a real token/value pair) and
*silently invisible*.

**Tightening T1 (tested, P admitted).** In the copy:
`r"\b(%s)\s*[:=]\s*(\S+)"` replaces `r"\b(%s)=(\S+)"`. P has none of the six tokens outside the excluded census line,
so P stays `h:1 admitted=1`; F3 flips to `h:0 admitted=0`. Matrix: T1 admits P and the other eight forgeries, misses
only F3. Cost: an entry that writes `scale_step: 1/120` in prose must write the census value.

## F4 — the census contradicted in words

`forgery-diffs.txt:51` (entry tail):
`INF The mode is accepted within two hertz of the request, the scale search walks ninety steps up and down, and the
line takes nine key pairs.` Three numbers, all false: tolerance 1 (`Hyprland-Monitor.cpp:837`), 89 steps
(`Hyprland-Monitor.cpp:1010`), 8 keys (`DERIVED line_keys=8`).

**Why the counter passes.** Clause h matches tokens; "two hertz", "ninety", "nine" are none. T1 does not help.

**Disposition: declared-by-implication residual.** A number-word scan (one..twenty → value) can be written and would
keep P admitted — the entry's word-form numbers ("eight keys", "five decimals", "89 steps") agree with the census —
but it is not sound: the adversary writes "a couple of hertz" or moves the number into a different clause, and the
synonym table needed to attach "hertz" to `refresh_tolerance` and "steps" to `scale_search` is a prose model, i.e.
exactly the non-author reading the docstring already declares as the residual. Recommendation: keep the *numbers*
in the census line (already done) and declare that prose numbers are not bound; do not add a word-number table.

## F5 — the registry row claims supersession of held rows

`forgery-diffs.txt:61`, `corpus/SOURCES.md` S304 cell 6:
`Supersedes S158 and S162; the first matching rule in file order wins and later files cannot override it`.

**False.** S158 is `HyprCtl.cpp` and S162 is `legacy/ConfigManager.cpp` (`evidence.txt`, registry rows); S304 is
`MonitorRuleManager.cpp`, so it cannot supersede either, and "first matching rule wins" is refuted by
`Hyprland-MonitorRuleManager.cpp:96`. The second half is F1's inversion, planted in the cell that is the row's
*claim*.

**Why the counter passes.** Clause c reads `cells[1]`'s last token, `cells[7]`, `cells[8]`, `cells[9]`, `cells[10]`;
clause e reads `cells[1]`, `cells[4]`, `cells[5]`. Cells 2, 3, 6 and the title text of cell 1 are never read
(counter:63-64), so the takeaway cell is a free-text claim column.

**Tightening T2 (tested, P admitted).** In clause c's new-id branch, add
`good &= not re.search(r"\b(supersed\w*|replac\w*|obsolet\w*)\b", " ".join(cells), re.I)`. P's nine rows contain none
of those words (`c:1 admitted=1`); F5 flips to `c:0`. This closes the false-*provenance* half, which is the routed
round-44 D6 class, not the false-*content* half: a takeaway saying "the fastest mode wins" still passes. Disposition
for that remainder: declared residual (counter:63).

## F6 — the false table is inside a fence

`forgery-diffs.txt:75` (entry tail), a fenced table, rows
`| which stored rule wins | the first matching rule, so later files are ignored |`,
`| mode without @RATE | the output's fastest mode |`, `| disabled outputs in monitors all | never listed |`.

**False.** MRM.cpp:96 (reverse scan); MonitorRule.hpp:46 (60 Hz); `Hyprland-HyprCtl.cpp:320` with
`Hyprland-HyprCtl.cpp:327`: `for (auto const& m : allMonitors ? State::monitorState()->allMonitors()` — `monitors all`
lists the disabled outputs, and `Hyprland-HyprCtl.cpp:265` prints `"disabled": {},`.

**Why the counter passes — and why the control set does not cover it.** counter:16: "Fenced code blocks of the entry,
README and lesson are removed before any line is matched". Every clause sees only unfenced lines, so a fenced table is
not merely unbound (F2) but *invisible*: it may name ids, repeat surface keywords and state numbers. The HIDDEN-LINE
control appended its forged line **unfenced** (`g:0` in `receipts/ctl-c2.txt`), which proves clause g catches that
shape; it does not control the fenced shape, which is admitted.

**Tightening T3 (tested, P admitted).** Require every fenced block, whitespace-normalized, to occur verbatim in the
pinned receipts (a fence is for a quotation, not for a claim); a fence whose blocks are empty is allowed. P's entry has
no fence, so P is `b:1 admitted=1`; F6 flips to `b:0`. Cost: an entry can no longer show a synthesized code example in
a fence — such examples then live unfenced where the clauses can read them.

## F7 — the live host claim and its own receipt disagree

`forgery-diffs.txt:88`, entry §6: `reports DP-1 at 3440x1440, 59.94000 Hz, 0x0, scale 1.25, transform 1` …
`the round's tool reports DIFFER on the refresh rate and verdict 1, exit 1
(.ufo/waves/round-45/receipts/live-monitors-host-l1.txt)`.

**False against its own citation.** The cited receipt records
`MADO_MONITOR_OUTPUT: name="DP-1" rule=1 differ=- verdict=AGREE` and `refreshRate: 99.997`, `scale 1`,
`transform 0` (`evidence.txt`, live chapter). The forged paragraph inverts every compared field and the verdict while
pointing at the receipt that refutes it — false provenance with a citation, which is worse than F2's uncited claim.

**Why the counter passes.** No clause reads `receipts/`; clause i only scans for BAD_LOC markers and pin coverage;
clause h only scans the six census tokens; the line names no id, so g does not bind it.

**Tightening T4 (tested, P admitted).** For every unfenced line carrying a verdict token
(`AGREE|DIFFER|UNRULED|NOT_COMPARED|NO_MATCHING_MONITOR|NO_RULES`) **and** a `.ufo/waves/round-NN/receipts/<name>`
locator, require that receipt at REV to contain each such token. P's §6 line cites
`live-monitors-host-l1.txt` and says `AGREE`; the receipt contains `AGREE` and `verdict=OK`, so P is `i:1
admitted=1`. F7 flips to `i:0`. Cost: a verdict sentence with no citation is still unbound (declared residual, F2
family) — T4 only makes a *citation* binding, which is the part that can be checked.

## F8 — the index row claims a merge and a supersession

`forgery-diffs.txt:99`, `corpus/README.md`:
`| merged | S290-S310 (supersedes S290-S297) |`.

**False.** The round's entry is a draft at review time, and S290-S297 are not superseded by it (no such record exists;
the round-44 closure D6 list is about S290-S297 supersession as a *defect*). The row asserts both, in the corpus index
a reader uses to decide what is current.

**Why the counter passes.** counter:615: `cl["f"] = int(sum(1 for l in unfenced(readme) if pat.match(l)) == 1)` with
`pat` anchored on `^| \`knowledge/<name>\``. Everything after the name cell is unread.

**Tightening T5 (tested, P admitted).** Require the row to have exactly three cells, cell 2 to be `draft`, and cell 3
to expand to exactly the entry's cited id set. P's row is ``| `knowledge/hyprland-monitor-rule-r45.md` (…) | draft |
S302-S310 |`` and its nine cited ids are S302…S310, so `f:1 admitted=1`; F8 expands to S290…S310 and says `merged`, so
`f:0`.

## F9 — the sentence that satisfies the surface is the false one

`forgery-diffs.txt:110`, entry §3: `the modes are taken in the order the kernel reports them, and the best one is
accepted when it is within 100 px and 10 Hz of the request; anything further away silently keeps the previous mode
(Hyprland-Monitor.cpp:819-840)`.

**False against the pins.** `Hyprland-Monitor.cpp:837`: `!DELTALESSTHAN(bestMode->refreshRate / 1000.f,
RULE->m_refreshRate, 1))` and the pixel bound on the preceding line — the bound is 1 px and 1 Hz, and a miss is tried
as a custom mode, not "silently kept".

**Why the counter passes.** Clause j needs a body line that matches the keyword (`refresh|Hz` — the forged line says
"Hz") and carries a locator whose range contains line 837 (`:819-840`). `surface=closeness line=837 cited=1`
(`forgery-scores.txt`). The surface is "covered" by a sentence that says the opposite of the code it cites; clause g
does not bind it because it names no id.

**Disposition: declared residual** — counter:64, "clause j binds a locator and a keyword per surface, not the truth of
the sentence around them". No tightening proposed: a keyword-adjacency or numeric-agreement rule is rewritten around
by any forger who reads the keyword list.

---

## What the predicate's self-account misses

The docstring declares four residuals (counter:62-65): quote-beside-claim, id-less table, unread registry cells, and
clause j's truth gap. F1, F2, F4, F5 (content half) and F9 fall inside them — the counter's own account is honest
about what it does not do. Three admitted classes fall **outside** that list and are therefore undeclared:

1. **F6 (fences).** The declaration says fenced blocks are "removed before any line is matched" as a mechanism, but the
   residual list never says that fenced content is unbound; read as an admission rule, the effect is that a false table
   is admitted in a fence and rejected one line later unfenced. T3 closes it for a fence bound to the pins, at the cost
   of synthesized examples in fences.
2. **F7 (verdict citations).** Clause i's scope ("no BAD_LOC marker; receipts cover the pins") reads as coverage of the
   receipts plane, but no clause binds an entry sentence to the receipt it cites. T4 closes the cited case.
3. **F8 (the index row).** Clause f is described as "exactly one column-0 index row for ENTRY", which is true and
   reads as a provenance check; the row's status and id list — the only claim it makes — are unread. T5 closes it.

## Recommendation to the L1 (before any data commit)

The kill rule allows a v2 re-registration with a new freeze before data. If the round keeps PRED-C2-r45 as frozen,
the admission means *provenance only*, and C2's after-state line should be read that way; if it wants the four
closable holes shut, T1/T2/T3/T4/T5 are each one string replacement, each tested P-admitted and target-rejecting, and
they compose (no overlap in the 60-cell matrix). F4's word-numbers and the F5 content half should stay declared
residuals: the cheapest sound form of both is the non-author reading the L1 already assigns.

**Not claimed.** This seat did not read the round's data commit (none exists at review time), did not edit the
counter, the controls, the registration, or the L1 draft, and ran no compositor command. The nine forgeries are
candidates on a clone of the freeze, scored by the frozen predicate; their commit hashes are in `revs.txt`.
