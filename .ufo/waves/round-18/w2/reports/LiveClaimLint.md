# LiveClaimLint — wave 2 falsification of "documentary only" notes (round 18)

Seat `MadoR18.LiveClaimLint`, executor, leaf (no delegation, no lane VCS write).
Lane root `/home/vgpnk/Projects/shokunin/mado-shokunin`; attacked artifact at
`4c103b55b1ea5c3c555884afe3eb69b5189701b7` (lane `master`), receipts commit
`abfbf35b1ed4d4a1eb294d525ef286be30f3886f`. Host pause observed throughout: only
`python3`, `sha256sum`, `sed -n`, `grep`, `cat`/`printf` on lane files, `/tmp`
and fetched bodies; no package, service, compositor, input, socket, process or
REA call; no `git`/`jj` at all; no tool installed.

## 1. Claim under attack

C2 credits `corpus/knowledge/walker-route-r18.md` (P3) and
`theme-route-r18.md` (P5); both open with "Documentary route only … read, not
observed". The two existing routes `idle-lock-route-r17.md` (P6) and
`terminal-route-r17.md` (P4) make the same declaration ("no listener has fired,
no lock has been taken"; "No terminal, launcher or compositor was run"). The
falsifier: **does any line outside `## Unexercised behavior` assert observed or
runtime behaviour in the present tense?** A line fails if it asserts what the
host or a running component is doing now, unless it is a verbatim upstream
quote (quotes/backticks plus an anchor) or carries `[UNK]`/`[INF]`/declared or
documentary wording.

## 2. Deliverable (only file written besides this report)

`.ufo/waves/round-18/live-claim-lint.py` — 550 lines, stdlib only,
`sha256 d85c2aa1b97824aa5e45397746b3a71880a58b7e3d64a2ca6254fd3bf000000c`,
parses under `python3 -I` (`ast.parse` ok).

```
usage: live-claim-lint.py [-h] [--selftest] [--explain] [notes ...]
```

- `NOTE <path> clean|HITS scanned=N hits=N` per file.
- `LINE <path as given>:<n> <stripped physical line>` per hit, one per line
  (several phrases on one line collapse to one `LINE`).
- `SUMMARY files= scanned= candidates= hits= exempt_marker= exempt_quote=
  exempt_negated= exempt_question=`.
- Exit `0` no hit, `1` any hit, `2` usage/read error. `-` reads stdin.
- `--explain` adds `  match=<family> phrase=<repr>` after a hit and
  `EXEMPT <path>:<n> <reason> <repr>` for every candidate a rule suppressed.

Flagged families (case-insensitive): copula-state `is/are [adv]* running|
displaying|showing|active|loaded|listening|visible|open|mounted|alive`;
dynamic `reload(s|ed|ing)|relaunch(es|ed|ing)|launch(es|ed|ing)|fire(s|d|ing)`;
`right now`; observation `observed|displays`; perfect `has/have loaded|reloaded|
relaunched|launched|started|fired|spawned`. Deliberately **not** flagged: bare
`runs/starts/spawns/restarts/reads/writes/opens/exits` (in this corpus they
describe source code; also outside the item's lexical set).

Exemptions, first match wins: (a) marker — the line carries
`[UNK]`/`[INF]`/`[INF-docs]`/`[OBS, bytes]` or documentary vocabulary
(`declared*`, `documentary`, `documented`, `documentation`, `according to`,
`from source`, `source-side`, `in code`, `from code`, `read as bytes`,
`bytes only`, `byte read`, `host bytes`); (b) quote — the match lies inside a
`"…"`/`“…”`/backtick span and the enclosing bullet/table row carries a
`file:line` or `[KEY:n]` anchor; (c) negated — a negator (`not|never|no|
without|neither|nor|cannot|n't`) appears in the same sentence *before* the
match; (d) question — the sentence contains `?` or a `whether` clause before
the match. Not scanned: the `source:`/`verified-at` header before the first
`# ` heading, `## Unexercised behavior` (British spelling accepted) up to the
next level-1/2 heading, and fenced blocks.

## 3. It can fail (required demonstration)

### 3.1 Built-in selftest — 13/13, exit 0

```
$ python3 -I .ufo/waves/round-18/live-claim-lint.py --selftest
SELFTEST clean PASS want=[] got=[]
SELFTEST dirty-present-tense PASS want=[5, 6, 7] got=[5, 6, 7]
SELFTEST quote-without-anchor PASS want=[3] got=[3]
SELFTEST quote-with-anchor PASS want=[] got=[]
SELFTEST backtick-with-anchor PASS want=[] got=[]
SELFTEST markers PASS want=[] got=[]
SELFTEST negated-disclaimer PASS want=[] got=[]
SELFTEST interrogative PASS want=[] got=[]
SELFTEST negative-copula PASS want=[3] got=[3]
SELFTEST right-now PASS want=[3] got=[3]
SELFTEST question-mark PASS want=[] got=[]
SELFTEST front-matter PASS want=[] got=[]
SELFTEST fenced PASS want=[] got=[]
SELFTEST 13/13
exit=0
```

The first version of `lint_text` printed **paragraph-relative** line numbers;
the dirty fixture then reported `got=[1, 2, 3]` instead of `[5, 6, 7]`. The
selftest caught it, the mapping now goes through the paragraph's file indices,
and the selftest compares exact line numbers rather than a count, so the same
regression cannot pass again. `negative-copula` is deliberate: "X is not
running" is a live-state claim; only a negator *before* the match (disclaimer
style) exempts.

### 3.2 `/tmp` note written for the demonstration — exit 1

`/tmp/live-claim-lint-fixture.md` (21 lines): line 6 a negation disclaimer,
line 10 an anchored quote, line 11 `[UNK]`, line 12 an anchored README quote,
line 16 a live claim, line 17 past tense, line 21 a live claim inside
`## Unexercised behavior`.

```
$ python3 -I .ufo/waves/round-18/live-claim-lint.py /tmp/live-claim-lint-fixture.md
NOTE /tmp/live-claim-lint-fixture.md HITS scanned=9 hits=1
LINE /tmp/live-claim-lint-fixture.md:16 The compositor is running right now and the launcher reloads its theme.
SUMMARY files=1 scanned=9 candidates=7 hits=1 exempt_marker=2 exempt_quote=2 exempt_negated=0 exempt_question=0
exit=1

$ python3 -I .ufo/waves/round-18/live-claim-lint.py --explain /tmp/live-claim-lint-fixture.md
NOTE /tmp/live-claim-lint-fixture.md HITS scanned=9 hits=1
LINE /tmp/live-claim-lint-fixture.md:16 The compositor is running right now and the launcher reloads its theme.
  match=copula-state phrase='is running'
EXEMPT /tmp/live-claim-lint-fixture.md:6 marker 'observed'
EXEMPT /tmp/live-claim-lint-fixture.md:10 quote 'is running'
EXEMPT /tmp/live-claim-lint-fixture.md:11 marker 'is running'
EXEMPT /tmp/live-claim-lint-fixture.md:12 quote 'reloads'
SUMMARY files=1 scanned=9 candidates=7 hits=1 exempt_marker=2 exempt_quote=2 exempt_negated=0 exempt_question=0
exit=1
```

Exit-code controls: no args → exit 2 (`at least one note path is required`);
missing file → exit 2 (`cannot read … No such file or directory`); clean stdin
note → exit 0 (`candidates=0 hits=0`); dirty stdin note → exit 1 at line 3.

## 4. Run on the four notes — exit 1

```
$ python3 -I .ufo/waves/round-18/live-claim-lint.py \
    corpus/knowledge/walker-route-r18.md corpus/knowledge/theme-route-r18.md \
    corpus/knowledge/idle-lock-route-r17.md corpus/knowledge/terminal-route-r17.md
NOTE corpus/knowledge/walker-route-r18.md clean scanned=246 hits=0
NOTE corpus/knowledge/theme-route-r18.md HITS scanned=92 hits=2
LINE corpus/knowledge/theme-route-r18.md:44 - `[OT:48-50]` calls `omarchy-theme-bg-next` unless `OMARCHY_THEME_SKIP_BACKGROUND=1`. Swaybg is therefore relaunched from inside the background writer, not from the restart list.
LINE corpus/knowledge/theme-route-r18.md:51 - `omarchy-theme-bg-set` `[OS:12]` resolves the argument with `realpath`, `[OS:21]` sets the link with `ln -nsf`, and `[OS:24-25]` relaunches swaybg on the link with `-m fill`. It exists as a second writer of the same link; it also does not touch `theme.name`.
NOTE corpus/knowledge/idle-lock-route-r17.md HITS scanned=90 hits=1
LINE corpus/knowledge/idle-lock-route-r17.md:106 - `omarchy-system-lock`: if `pidof hyprlock` is empty, runs `( hyprlock; omarchy-system-wake ) &` (:8-13); `hyprctl switchxkblayout all 0` (:16); locks 1password if running (:19-21); `pkill -f org.omarchy.screensaver` (:24); unless `OMARCHY_LOCK_ONLY` is `true`, after `sleep 3` and if hyprlock is still running turns off keyboard and display brightness (:26-32).
NOTE corpus/knowledge/terminal-route-r17.md HITS scanned=98 hits=2
LINE corpus/knowledge/terminal-route-r17.md:66 - `general.import` (alacritty.5.scd:31): imports are loaded in order and missing
LINE corpus/knowledge/terminal-route-r17.md:91 plain `xdg-terminals.list` files are the only selection files observed. Upstream
SUMMARY files=4 scanned=526 candidates=23 hits=5 exempt_marker=5 exempt_quote=3 exempt_negated=9 exempt_question=1
exit=1
```

`--explain` on the same invocation adds the matched phrase per hit
(`relaunched`, `relaunches`, `is still running`, `are loaded`, `observed`) and
the 18 exemption records listed in §5. The four notes total 756 physical lines
(321/145/138/152); 526 lines were scanned. `## Unexercised behavior` begins at
line 283/134/125/121 respectively, so walker:283-321, theme:134-145,
idle:125-138 and terminal:121-152 are outside the scan by rule.

## 5. Every hit, with judgement

| # | hit | matched (family) | judgement | basis |
|---|---|---|---|---|
| 1 | `theme-route-r18.md:44` "Swaybg is therefore relaunched from inside the background writer" | dynamic `relaunched` | **false positive** (documentary source inference) | Same bullet cites `[OT:48-50]`; fetched tag body `fetch/ReopenS093/omarchy-theme-set:48-50` is `if [[ $OMARCHY_THEME_SKIP_BACKGROUND != "1" ]]; then` / `  omarchy-theme-bg-next` / `fi`, and `fetch/ReopenS093/omarchy-theme-bg-next:46-50` is `ln -nsf "$NEW_BACKGROUND" "$CURRENT_BACKGROUND_LINK"`, `# Relaunch swaybg`, `pkill -x swaybg`, `setsid uwsm-app -- swaybg -i "$CURRENT_BACKGROUND_LINK" -m fill`. The sentence is a correct source deduction, not a host observation. Advisory only: it is an inference lacking an explicit `[INF]` tag; the enclosing section is `### Theme-set writer (omarchy v3.8.4)` under `## Upstream contract`. |
| 2 | `theme-route-r18.md:51` "`[OS:24-25]` relaunches swaybg on the link with `-m fill`" | dynamic `relaunches` | **false positive** (documentary source description) | `fetch/ReopenS093/omarchy-theme-bg-set:21-25`: `ln -nsf "$BACKGROUND" "$CURRENT_BACKGROUND_LINK"`, `# Kill existing swaybg and start new one`, `pkill -x swaybg`, `setsid uwsm-app -- swaybg -i "$CURRENT_BACKGROUND_LINK" -m fill >/dev/null 2>&1 &`. Anchor `[OS:24-25]` is accurate; the sentence describes the script's own actions. |
| 3 | `idle-lock-route-r17.md:106` "…and if hyprlock is still running turns off keyboard and display brightness (:26-32)" | copula-state `is still running` | **false positive** (script condition paraphrased) | `fetch/SrcOmarchyBackground/bin_omarchy-system-lock:26-32`: `if [[ ${OMARCHY_LOCK_ONLY:-false} != "true" ]]; then` / `  (` / `    sleep 3` / `    pidof hyprlock >/dev/null \|\| exit 0` / `    omarchy-brightness-keyboard off` / `    omarchy-brightness-display off` / `  ) &`. The clause condenses the `pidof hyprlock` guard; no host state is asserted. |
| 4 | `terminal-route-r17.md:66` "`general.import` (alacritty.5.scd:31): imports are loaded in order and missing" | copula-state `are loaded` | **false positive** (man-page paraphrase) | `fetch/FetchBackfillR17/s058-alacritty-man:35-37`: "Imports are loaded in order, skipping all missing files, with the importing file being loaded last." The anchor on the line is the man-page line, and the note's very next line quotes the same text verbatim under `alacritty.5.scd:35-37`. The sentence paraphrases documentation, not a load event. |
| 5 | `terminal-route-r17.md:91` "plain `xdg-terminals.list` files are the only selection files observed" | observation `observed` | **false positive** (static name census) | The paragraph (§ Host declaration, lines 90-92) states the method: "checked for by name in `~/.config` (maxdepth 1) and `/etc/xdg`: none present". This is a directory-entry observation within the pause's byte-read allowance, not a claim that any resolver or terminal is running. The word, not the fact, is what the lexicon caught. |

**Tally: 5 hits, 5 false positives, 0 true overclaims.** No correction is
requested to the four notes. The two round-18 notes in particular never assert
host or process state outside their `## Unexercised behavior` sections: walker
is clean with four candidates that the exemption rules absorb; theme's two hits
are source-contract sentences whose anchors I checked byte-for-byte against the
fetched `v3.8.4` bodies.

## 6. Exemptions exercised (the machinery that makes the notes pass)

The `--explain` run shows 18 suppressed candidates, `candidates=23 = hits 5 +
exempt 18` (`marker=5`, `quote=3`, `negated=9`, `question=1`):

- `walker:9` negated `observed` — "read, not observed"; `walker:255` question
  `is active` — "Whether that include edge is active on this host is not
  traced".
- `walker:52` quote `is running` and `walker:58` quote `is running` — both
  inside double-quoted upstream text with `[WR:59]` / `[WM:802-803]`. Verified
  verbatim in `fetch/ReopenS072/walker-v2.17.2-README.md:59` ("make sure
  [elephant](…) is running before starting Walker", link markup elided in the
  quote) and `fetch/MadoR18.SrcWalkerThemes/src-main.rs:802` ("make sure
  'walker --gapplication-service' is running!").
- `theme:9` negated `observed`, `theme:10` negated `reloaded`, `theme:76`
  marker `are not loaded` (line begins "Host bytes read with …").
- `idle:9` negated `fired`/`observed`/`has fired` ("no listener has fired, no
  lock has been taken"); `idle:37` marker `fired` ("Documented [HW:15-16]");
  `idle:46` negated `firing` ("returns without firing"); `idle:47` negated
  `fired` ("was not fired"); `idle:79` marker `is loaded` and `is running`
  ("Declared start route only … is `[UNK]`").
- `terminal:7` marker `observed` (heading "documentary, not observed");
  `terminal:12` negated `launches` ("It does not establish which terminal
  actually launches"); `terminal:67` quote `are loaded` (verbatim man-page text
  with `alacritty.5.scd:35-37`).

The quote exemption is the load-bearing one for walker and terminal; the
marker/negation pair carries idle; theme's two hits survive because they are
plain declarative source statements with no marker on the physical line — see
§7 for why that is the honest outcome rather than a rule failure.

## 7. Coverage limits and risks

- **Lexicon-limited.** A live claim phrased only with bare `runs`, `starts`,
  `spawns`, `restarts`, `reads`, `writes`, `opens` or `exits` is not flagged.
  Concretely, `theme:45` ("`[OT:53-62]` restarts waybar (only when running),
  …") is in the same documentary class as hits 1-2 and is deliberately outside
  the net. Present tense only: "was displayed", "took effect" are not flagged
  unless they use `observed` or a perfect form.
- **Negation is sentence-scoped and only before the match.** A disclaimer
  earlier in a compound sentence suppresses a claim later in it ("not only X,
  but Y is running" is missed). A negator inside the copula (`is not running`)
  is still reported, because a negative state claim is still a claim.
- **Quote exemption is paragraph-scoped pairing** of `"`, `“”` and backticks;
  it needs an anchor in the same bullet/table row. It does not verify
  verbatimness — I checked the three exempted quotes by hand in §6. Unbalanced
  backticks can over-exempt a bullet; no occurrence was observed in the four
  notes.
- **Markers are per physical line.** A wrapped sentence whose `[UNK]` or
  `declared` tag sits on the next line is reported (conservative by design).
  Marker precedence also means a documentary line can be exempted even if it
  also contains a real live claim; the `--explain` output is the audit surface.
- **Section exclusion is literal.** Only `## Unexercised behavior` is skipped
  (until the next level-1/2 heading); a live claim filed under another heading
  is scanned. Fenced code is skipped, which could hide a live claim written
  inside a fence, but these notes use fences only for commands.
- **One `LINE` per physical line.** Multiple hits on one line collapse;
  `--explain` shows the first hit phrase and every exemption, not every hit
  phrase.
- **A green run is necessary, not sufficient, and 5/5 false positives on this
  sample proves it.** The tool is a candidate finder for human judgement; it
  cannot certify documentary cleanliness. What this run does establish is
  narrower and checkable: no line outside the four `## Unexercised behavior`
  sections asserts host state in the item's lexical set without one of the four
  exemption conditions, and each of the five surviving candidates resolves to
  source bytes or a name census.

## 8. Commands run (all retained above)

```
python3 -I .ufo/waves/round-18/live-claim-lint.py --selftest            # 13/13, exit 0
python3 -I .ufo/waves/round-18/live-claim-lint.py /tmp/live-claim-lint-fixture.md          # 1 hit line 16, exit 1
python3 -I .ufo/waves/round-18/live-claim-lint.py --explain /tmp/live-claim-lint-fixture.md # 1 hit, 4 exemptions
python3 -I .ufo/waves/round-18/live-claim-lint.py <four notes>          # 5 hits, exit 1
python3 -I .ufo/waves/round-18/live-claim-lint.py --explain <four notes> # hit phrases + 18 exemptions
python3 -I .ufo/waves/round-18/live-claim-lint.py                        # usage, exit 2
python3 -I .ufo/waves/round-18/live-claim-lint.py /tmp/nope.md           # read error, exit 2
printf '# T\n\nswaybg is running.\n' | python3 -I … -                    # 1 hit, exit 1
printf '…clean…' | python3 -I … -                                        # 0 hits, exit 0
sed -n '46,50p' fetch/ReopenS093/omarchy-theme-bg-next                   # hit-1 evidence
sed -n '21,25p' fetch/ReopenS093/omarchy-theme-bg-set                    # hit-2 evidence
sed -n '48,50p' fetch/ReopenS093/omarchy-theme-set                       # hit-1 evidence
sed -n '26,32p' fetch/SrcOmarchyBackground/bin_omarchy-system-lock       # hit-3 evidence
sed -n '30,37p' fetch/FetchBackfillR17/s058-alacritty-man                # hit-4/exemption evidence
sed -n '59p'    fetch/ReopenS072/walker-v2.17.2-README.md                # quote exemption
sed -n '802p'   fetch/MadoR18.SrcWalkerThemes/src-main.rs                # quote exemption
sha256sum .ufo/waves/round-18/live-claim-lint.py                         # d85c2aa1…
```

The notes' own receipt directories named in their headers
(`.ufo/waves/round-18/fetch/NoteWalker/receipts.jsonl`,
`…/NoteTheme/receipts.jsonl`) exist; the verbatim checks above used
independently fetched copies (`ReopenS072`, `FetchBackfillR17`,
`ReopenS093`, `SrcOmarchyBackground`, `MadoR18.SrcWalkerThemes`), so the
judgement does not depend on the notes' own receipt chain.

## 9. Files changed

- `.ufo/waves/round-18/live-claim-lint.py` (new; sha256
  `d85c2aa1b97824aa5e45397746b3a71880a58b7e3d64a2ca6254fd3bf000000c`).
- `.ufo/waves/round-18/w2/reports/LiveClaimLint.md` (this report).

No lane git/jj write, no commit, no delegation, no shared-file edit. `/tmp`
artifacts (`live-claim-lint-fixture.md`, `lcl-four.out`, `lcl-selftest.out`)
are outside the lane and disposable.

## 10. Verdict

`w2-LiveClaimLint`: **HITS 5, TRUE OVERCLAIMS 0, FALSE POSITIVES 5**; tool
selftest 13/13, exit 1 on the four notes as designed. The C2 notes survive this
lexical attack. Advisory for round 19 (not a defect and not requested for
correction now): `theme:44`'s "therefore relaunched" is a source inference and
would read more precisely tagged `[INF]`; `theme:51`, `idle:106` and
`terminal:66` are source/documentation summaries and need no change.

Tooling installed or updated: none. Blockers: none.
