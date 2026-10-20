# MadoR19.AtkPtrArcSynthesis — partial

Seat: round-19 wave 2, falsify lane. Target: the round-19 appended block in
`corpus/knowledge/arc-synthesis.md` at integrated tip
`01b80946d92b26370d3012a7da655d00dd135154` (worktree byte-equal, sha256
`8278b77a84105dbf1a22ee9efb8cc8bb1ba0b6b079dc5571889e389cfd245e05`; baseline
`9c54c56` = `a5b48331414618108cdc9596cf6c7cc0dc78994ebcf61141c3e6d80428419d50`,
30,796 B). All paths relative to `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Host facts read as file bytes only; nothing executed.

Verdict by sub-question: **(a) holds**, **(b) holds on the runtime question with one
false provenance negative**, **(c) line numbers hold, one count claim breaks**,
**(d) S090 supports both sentences it carries, but the binary-sha sentence carries no
S-row while the rows that do carry it exist**.

---

## (a) Were pre-existing bytes changed beyond the documented head `source:` swap? — NO

Exact byte test (tip is the baseline's bytes plus one appended segment; no pre-existing
byte altered):

```text
$ python3  # git show both revs into memory, seek first divergence
base bytes 30796 tip bytes 32331
tip startswith base: True
tip startswith base+\n: True
first differing offset: 30796 of base 30796
base tail repr: b's\n  largest named remainder is its own record, not its gate.'
tip[len(base):+80] b'\n\n## Freshness pointer (round 19, 2026-10-20)\n\n- The walker version pins in this'
```

So the whole 1,535-byte delta is appended material: 2 LF + 1,533 B of block
(`arc-synthesis.md:389-397`). `git diff` still prints `-1/+1` on line 388 because the
baseline file had no EOF newline and the first appended LF terminates that pre-existing
last line — an appended byte, not an altered one; the w1 writer recorded exactly this
(`.ufo/waves/round-19/w1/reports/PtrArcSynthesis.md:14` "The file had no trailing
newline before").

Cross-check that the documented set is exactly the two route notes — same prefix test
over all 11 notes touched in `corpus/knowledge/`:

```text
arc-synthesis.md                    base= 30796 tip= 32331 prefix=True  firstdiff=30796
closeout-r11.md                     base= 19250 tip= 20516 prefix=True  firstdiff=19250
config-health-report-r3.md          base= 62249 tip= 63705 prefix=True  firstdiff=62249
remaining-planes-census.md          base= 20512 tip= 22211 prefix=True  firstdiff=20512
theme-route-r18.md                  base= 19121 tip= 19867 prefix=False firstdiff=412
walker-deep-r9.md                   base= 24391 tip= 25976 prefix=True  firstdiff=24391
walker-deep.md                      base= 38403 tip= 40352 prefix=True  firstdiff=38403
walker-live-surface.md              base= 19203 tip= 20413 prefix=True  firstdiff=19203
walker-route-r18.md                 base= 24830 tip= 25722 prefix=False firstdiff=1391
waybar-walker-plane.md              base= 28392 tip= 29796 prefix=True  firstdiff=28392
waybar-walker-semantics.md          base= 38083 tip= 39539 prefix=True  firstdiff=38083
```

Only `theme-route-r18.md` (head line, firstdiff 412) and `walker-route-r18.md` (head
line, firstdiff 1391) rewrite pre-existing bytes — the documented head token swaps
(S094→S097, S084→S098 per their own `## Round-19 corrections` bullets). Nine notes,
arc-synthesis included, are pure appends.

## (b) Live/runtime claims about 2.17.2, or "re-verified" labels? — no overclaim; one provenance negative is false

Sentence-by-sentence against the block (`arc-synthesis.md:392-397`):

| Line | 2.17.2-touching assertion | Basis | Verdict |
|---|---|---|---|
| 392 | "On 2026-10-20 the host package moved to 2.17.2" | `pacman.log:2929` = `[2026-10-20T09:16:46-0300] [ALPM] upgraded walker (2.17.0-1 -> 2.17.2-1)` (read as bytes) | supported; a package-log fact, not a runtime fact |
| 393 | "The current host binary sha is `25240650…`" | `walker-route-r18.md:183` (§ Host declaration) records exactly `25240650686fe6adf0e945530f6e701f5b67535f3e8f9187b08f022317d93096`, 7,039,912 B | supported; labelled "file bytes, not re-measured here" |
| 394 | "post-restart process state [UNK]" | S090 teaches "a log line is not a running-binary fact" (`SOURCES.md:102`) | correct; this is the lesson the round-18 GATE flag asked for |
| 396 | "no `reload_config` or `set_config` in the v2.17.2 source tag" | `walker-route-r18.md:95-96` ("The tag tree contains no … `reload_config` or `set_config` function"), a note whose sources are the v2.17.2 tag (`walker-route-r18.md:21`); corroborated by the round-19 token census `reload_config`/`set_config` 0/0 | supported |
| 396 | "the 2.17.2 binary's apply behaviour is [UNK]" | — | correctly bounded |
| 397 | "behaviour of the 2.17.2 binary stays [UNK]" | — | correctly bounded |

No sentence asserts a live walker 2.17.2 fact, and nothing is called re-verified for this
round: the only "re-measured" label is dated to r9 (`arc-synthesis.md:392`), and the note's
own measured date is `verified-at: 2026-10-14` (`arc-synthesis.md:7`), matching the r9
identity pins (`walker-deep-r9.md:57` sha `64826a85…`, `:97` BuildID `a22452d1…`).

**But the provenance negative is false.** `arc-synthesis.md:394` says the host-state row is
"not re-measured this round" and lists, among five items, sockets and the theme package.
Round-19 wave 1 re-measured both:

- `.ufo/waves/round-19/w1/reports/DeltaWalkerCli.md:136` — "Live socket state today (stat only): both sockets `755 0`, mtime 2026-10-20 09:57:13…" (mode/size agree with the row's `srwxr-xr-x` 0 B; the mtime moved and is not flagged by the block).
- `.ufo/waves/round-19/w1/reports/DeltaWalkerConfig.md:150` — "**Theme pins.** … `layout.xml` `dbb6bbbe…` 6,488 B, `style.css` `481267af…`, … `walker.css` `f44cb450…` — unchanged".

The block is therefore overly conservative, not overclaiming: two of the five items it
declares unmeasured were measured, and the sentence should either drop those items or
credit the round's measurement.

**Soft finding (judgement, [INF]).** `arc-synthesis.md:395` keeps "the constraint that
socket protocol and rendered UI stay UNKNOWN". Read as "not exercised", this survives.
Read as "the protocol is not knowable", it is stale: wave 1 closed the source-side
question (`.ufo/waves/round-19/w1/reports/DeltaWalkerCli.md` §4/§9.2, from
`.ufo/waves/round-19/fetch/DeltaWalkerCli/v2.17.2-src_main.rs:893-895` — `listener.accept()`
→ `drop(stream)`, payload never read). The routing note this block points at does not
carry that closure either, so a resolved question is left labelled unknown in the only
in-file pointer. I do not score this as a falsification of the literal sentence.

## (c) Cited line numbers — correct; the "only `2.17.0`" count — FALSE

Verified each anchor literally:

```text
$ sed -n '229p' corpus/knowledge/arc-synthesis.md   # walker row: version `2.17.0`,
                                                    # sha 64826a85…, BuildID a22452d1… (r9)
$ sed -n '2929p;3062p;3123p' /var/log/pacman.log
[2026-10-20T09:16:46-0300] [ALPM] upgraded walker (2.17.0-1 -> 2.17.2-1)
[2026-10-20T09:18:25-0300] [ALPM] running 'walker-restart.hook'...
[2026-10-20T09:31:04-0300] [ALPM] running 'walker-restart.hook'...
$ grep -n "walker-route-r18" vs the note: "## Host declaration" at walker-route-r18.md:173,
  the sha row at :183
```

All three log anchors and the note anchor are correct. The count claim is not:

```text
$ grep -o '2\.17\.0' corpus/knowledge/arc-synthesis.md | wc -l      # tip
6
$ git show 9c54c56:corpus/knowledge/arc-synthesis.md | grep -o '2\.17\.0' | wc -l
1
$ grep -on '2\.17\.0' corpus/knowledge/arc-synthesis.md
229:2.17.0
392:2.17.0
392:2.17.0
393:2.17.0
393:2.17.0
396:2.17.0
```

`arc-synthesis.md:392` says "(line 229, the only `2.17.0` in the file)". In the committed
bytes there are **six** occurrences on four lines: 229 plus five inside the pointer's own
bullets 392/393/396. The sentence copies a *before-edit* measurement into an *after-edit*
file — the w1 writer's own header says exactly that ("Lines containing `2.17.0` (before
edit)", `PtrArcSynthesis.md:5`; finding F1 at `:28` "The note's only 2.17.0 pin is line
229"). Before the append the claim was true (count 1 at line 229); after it, it is false
by self-reference. Charitable reading ("the only 2.17.0 *pin*") is available, but the
parenthetical asserts a token count, and every sibling note in this wave avoids the
problem by scoping to "in this note (line N)" — arc-synthesis is the only file in
`corpus/knowledge/*.md` with the "only `2.17.0`" phrasing (`grep` across all notes returns
one hit, this line).

Severity: low blast radius, but it is a literal, machine-checkable falsity planted by
round 19 in a file whose purpose is to be greppable. Fix: strike "the only `2.17.0` in
the file" or qualify "the only `2.17.0` outside this pointer".

## (d) Are the cited S### rows supporting? — S090 yes; the sha sentence cites no row

`S090` (`corpus/SOURCES.md:102`) is attached twice (`arc-synthesis.md:392` and `:394`) and
its anchor cell enumerates exactly the lines cited: "lines 1943 …, **2929** (walker
2.17.0-1 -> 2.17.2-1, 2026-10-20T09:16:46-0300), **3062 and 3123** (walker-restart.hook),
3095 …". Both cited facts are inside the row's declared anchors, and the source cell's
teaches ("a log line is not a running-binary fact") is the discipline the block follows
for the post-restart `[UNK]`. Verified against the file itself above. So: every S### the
block cites does support its sentence.

Gap: the one fact with no S### is the new binary sha. `arc-synthesis.md:393` attributes
`25240650…` to `walker-route-r18.md § Host declaration` — a note section, not a row. The
rows that carry that exact sha exist at the tip:

```text
$ git show 01b80946:corpus/SOURCES.md | grep -n '^| S09[016] '
102:| S090 | host /var/log/pacman.log …
103:| S091 | host walker file bytes (… /usr/bin/walker) … 2524065068…, embedded default at offset 806960
108:| S096 | host walker version binding — /usr/bin/walker … 2524065068…, literal 2.17.2 @ 856,302
```

So `S091`/`S096` are available and were not named, which is also what the owning wave-1
delta report flagged: `PacmanLogMoves.md:52` — "`:393` already names the new sha but no
S###". The w1 pointer report's justification for that omission is itself false at the
integrated tip: `PtrArcSynthesis.md:29` ("F2: … no S096 row exists in `corpus/SOURCES.md`
at this time") — the row is present at `SOURCES.md:108` in the very commit under test.
Whether this breaches criterion 28's wording ("naming … the SOURCES row that superseded
it") depends on whether S090 counts as the superseding row for a binary identity, and
S090's own teaches cell says it does not. I score it a citation gap, not a false sentence.

---

## Findings

- **F1 (breaks, literal):** `arc-synthesis.md:392` "the only `2.17.0` in the file" — six
  occurrences at the tip, five of them inside the pointer itself. Evidence above.
- **F2 (holds):** the block is a pure append; the baseline's 30,796 bytes are an exact
  prefix. Only the two documented route notes rewrite pre-existing bytes.
- **F3 (holds with a precision defect):** no live/runtime fact about walker 2.17.2 is
  claimed and nothing is labelled re-verified for this round; but `:394`'s "not
  re-measured this round" is false for the socket mode/size and theme pins, which wave 1
  did measure (`DeltaWalkerCli.md:136`, `DeltaWalkerConfig.md:150`).
- **F4 (holds):** every cited line number is correct — note line 229, `pacman.log` 2929,
  3062, 3123, `walker-route-r18.md` § Host declaration at 173 / sha at 183.
- **F5 (partial):** the S090 citations are supported by the row's own anchor cell; the
  binary-sha sentence names no S-row although S091 (`SOURCES.md:103`) and S096
  (`SOURCES.md:108`) exist at the tip, contradicting the omission rationale at
  `PtrArcSynthesis.md:29`.
- **F6 ([INF], soft):** "socket protocol … stay UNKNOWN" (`:395`) survives only in the
  "not exercised" sense; wave 1 closed the source-side question.

## Limits

- I read `corpus/SOURCES.md`, the two w1 delta reports, the routing note at the tip and
  the fetched v2.17.2 `src/main.rs`; I did not re-run the C2 counter, the gate, or any
  walker/pacman/systemctl command (host pause).
- The S090 GATE digest in `corpus/lessons/round-18.md:70` (`f34d34e7…`) does not equal
  the sha256 of log line 2929 with or without its newline (`2b9fad9a…` / `a9648581…`);
  the digest convention for that row is `[UNK]` to me and I make no claim about it.
- Whether "the only `2.17.0` in the file" should be forgiven as "the only pin" is a
  reading judgement; I report the token count, which is unambiguous.
- No independent fetch this round, so no fetch receipts.

## Installs

none
