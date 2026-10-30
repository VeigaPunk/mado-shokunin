# R56W3ScribeGateA2 — attempt-2 Gate blocks for S396 and S397 (draft; nothing landed)

Item: `Scribe R56W3ScribeGateA2` — "Draft the attempt-2 Gate blocks for the two queued rows (S396 inotify_add_watch(2),
S397 proc_pid_fdinfo(5)) for the round lesson … write the Gate table rows (row id, URL, access date 2026-10-30, located
quote) plus one sentence per row on why the lane lacked it. Deliverables: receipts/gate-draft.md."

All tree scores are at lane tip `0f3a54361a9824484d0801679ceb1fd8ac7c32e1` unless named. I edited no tracked file and made
no git/jj mutation anywhere except inside my scratch clone (`/fast/scratch/hyaku/mado-r56/R56W3ScribeGateA2/clone`,
toplevel asserted before the commit). No tool was installed (operator tooling authorization recorded: none used). Scratch
was removed before this report was finalized; receipts were copied into the deliverable directory first.

## Deliverables

- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w3/R56W3ScribeGateA2/receipts/gate-draft.md` — the Gate
  block draft (table rows row id / URL / accessed / located quote, one sentence per row on why the lane lacked it, landing
  notes for the L1).
- `…/R56W3ScribeGateA2/receipts/gate-draft-evidence.txt` — every command and its decisive output.
- `…/R56W3ScribeGateA2/receipts/man7-inotify_add_watch.2.html`, `…/receipts/man7-proc_pid_fdinfo.5.html` — my independent
  fetches (byte-identical to the L1's pins and to the lane's working-tree copies).
- `…/R56W3ScribeGateA2/receipts/gate-draft-evidence.txt` §2 embeds the quote-verification table (the check ran as a
  `python3 -I` heredoc, so the script itself is not a deliverable; every quoted string it asserts is reproduced verbatim
  in the Gate draft and can be re-checked with `grep -F` against the two pinned HTML files).

## What I did, with the decisive outputs

1. **Fetched both URLs myself into scratch and hashed them.** `curl -sS --fail` for
   `https://man7.org/linux/man-pages/man2/inotify_add_watch.2.html` and `…/man5/proc_pid_fdinfo.5.html`:
   `98fe7feb381fa2687e8a3962e6d78a49cb1ad07c543f93449dcb42d6712c3d6d` (11,345 B) and
   `f9e12387bf013d7c016f0015de5801932022a2fe6786d53e1cc84c385952d8a1` (14,694 B) — exactly the draft's stated pins, and
   byte-identical to the lane's `.ufo/waves/round-56/fetch/` copies.
2. **Located ≤25-word quotes at stated pin lines, byte-exact, single line.** Chosen Gate quotes:
   - S396 `already being watched (perhaps via a different link to the same` — `inotify_add_watch.2.html:93`, 11 words;
     continuation `object), then the descriptor for the existing watch is returned.` at :94 (10 words); per-instance
     qualifiers at :89 and :91. All five strings verified as contiguous byte substrings of their stated lines
     (`verify-quotes.txt`: `in_line=True` for each).
   - S397 `Each of the lines beginning with "inotify" displays information` — `proc_pid_fdinfo.5.html:160`, 9 words
     (byte-exact, the L1's own line); continuation `about one file or directory that is being monitored.  The fields` at
     :161; field definitions at :164/:166/:168-169/:171-172; sample block :153-158; read-access statement :72-77.
   The draft's other candidate facts check out: page footlines **Linux man-pages 6.19, 2026-02-08** (inotify_add_watch)
   and **2026-07-18** (proc_pid_fdinfo), both tarball man-pages-6.19.tar.gz, HTML rendering created 2026-09-09; registry
   332 rows, last id S395, so S396/S397 continue it; zero registry rows for `/proc` or `fdinfo`; the only man7 URL in the
   registry is inotify.7.html (no E04/W04 collision for the new URLs).
3. **Measured the frozen counters on a scratch clone with the two rows appended** (`mined`,
   `used-by = corpus/lessons/round-56.md`, inserted before `## Paths`; commit `cd0c017219a9482b3dc2fbdcf92c3d16a22d1b9f`;
   `git rev-parse --show-toplevel` asserted equal to the clone first):
   - C3: `MADO_USED_BY: rev=cd0c017… entries=71 rows=334 missing=0 extra=0 dangling=0 conflict=0 stale=0 lost=0 exempt=24 verdict=TARGET_MET missed=none`, exit 0.
   - C1: `MADO_AUTORELOAD_ENTRY: … rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8 verdict=TARGET_MET missed=none`, exit 0.
   - Census `validate`: exit 0 before and after; 38 findings lines in both runs and `diff` **empty** — no E-code and no
     W-code mentions S396/S397.
   The mechanism: at the tip `quality/counters/c3-r56-used-by.py:51` is
   `USED_BY = re.compile(rb"corpus/knowledge/[A-Za-z0-9_.-]+\.md")`, so a lesson path in cell 11 is never parsed into
   `USEDBY` (probe: `usedby['S396'] = set()`), and no entry cites S396/S397, so `missing` has no pairs either.

## Defects in the L1 draft (input → severity; nothing edited by me)

1. **Anchor date wrong in both rows — weakens the row.** Draft anchor cells say `@ Linux man-pages 6.19 (2026-02-14)`,
   which is inotify(7)'s footline date (S390). The pages' own footlines: inotify_add_watch(2) **2026-02-08**,
   proc_pid_fdinfo(5) **2026-07-18** (footline spans captured in the evidence receipt).
2. **Anchor ranges leave taught lines outside — weakens the row.** S396 `inotify_add_watch.2.html:88,93` omits :94, where
   `the descriptor for the existing watch is returned` sits; S397 `proc_pid_fdinfo.5.html:160,164,171` omits :161 (one
   monitored file per line), :166 (`ino`) and :168-169 (`sdev`). Recommended: `88-94` and `160-172` (both inside the E3
   line-count bounds 259 and 367).
3. **S396 `teaches` lacks the per-instance qualifier — weakens the claim.** The page scopes the rule at :89
   (`descriptor for this inotify instance, for the filesystem object`) and :91 (`not previously being watched by this
   inotify instance, then the`); the draft's taught sentence states the reuse rule unqualified.
4. **The L1's designated S396 quote is not byte-exact — weakens the row.** Draft: `A successful call to
   inotify_add_watch() returns a unique watch` at :88; the pin's bytes at :88 are `A successful call to
   <b>inotify_add_watch</b>() returns a unique watch`. The lane's own frozen rows keep markup in quotes (entry K30:
   `Don't dereference <i>pathname</i> if it is a symbolic link.`), and the C1 quote leg tests
   `quote.encode("utf-8") in pin_line`, so a markup-stripped quote cannot be reused as a row quote later. The S397 quote
   at :160 **is** byte-exact as drafted (no markup on that line).
5. **The `queued` + `used-by —` rationale is false — weakens the draft's stated reason (no predicate threatened).**
   Draft, verbatim: "the frozen C3 counter's `extra` leg counts any used-by path outside the entry set, so a lesson path
   in `used-by` would flip `TARGET_MET` to `TARGET_MISSED` at the new tip." Measured: with the rows appended as `mined`
   plus the lesson path, the frozen C3 prints `extra=0 … verdict=TARGET_MET` (see §3) because cell-11 paths are collected
   by the `corpus/knowledge/…` regex only, and no entry cites S396/S397 so `missing` has no pairs. Per CORPUS
   (`used-by` = "knowledge entries **or lessons** citing the row"; `mined` = cited by ≥1 such path), the Gate citation
   makes both rows `mined` with `corpus/lessons/round-56.md`, which is also census-clean (E11 passes — the file exists at
   tip; no W03 since used-by is non-empty). Caveat carried into the Gate draft: if the attempt-2 lesson lands as a new
   file rather than an append to `corpus/lessons/round-56.md`, the `used-by` cell must name that file and it must exist on
   disk at census time.
6. **The two new pins are untracked — weakens the row until committed.** `git ls-files --error-unmatch` fails for
   `.ufo/waves/round-56/fetch/man7-inotify_add_watch.2.html` and `…/man7-proc_pid_fdinfo.5.html` (both `??` in status).
   The draft anchors cite them as pins; the C1 `pin_hash` leg covers only the frozen pin set, so no counter would catch a
   missing pin (M56-9 class; `receipts/pins-extra.sha256` is the house remedy).
7. **Routed prose observation (entry frozen at tip — not edited here) — weakens the claim.**
   `corpus/knowledge/hyprland-config-autoreload-r56.md:46` states "the kernel keeps one watch per inode, the second add
   returns the same descriptor and modifies the watch (inotify(7) lines 90-92 and 296-302 …)", unmarked as inference.
   Those pinned lines say `creates a new watch item, or modifies an existing watch` (:90, byte-contiguous), that each
   watch carries a unique watch descriptor (:90-91), and, under IN_MASK_CREATE, that several paths may name one inode and
   unguarded calls may clobber masks (:298-302) — the returned-descriptor statement itself is not in them (grep of the
   pin: no `same descriptor`, no `descriptor for the existing watch`). S396 (:92-94) is the verbatim ground for that
   clause; routing the citation fix to the L1/round 57.
8. **S397 `teaches` wording — cosmetic, routed.** `so the running compositor's watch table is readable without touching
   it`: the page grounds readability by the owner (:74) and the per-line format (:160-161); "without touching it" is the
   lane's read-only-method statement, and the 40/40 result is the wave-2 comparison's, not the man page's.

## Conflicts, verbatim, for the canonical Rust judge

- Sibling seat `R56W3RevLessonGate` (draft audit) wrote: "each explicitly designated Gate quote is 9 whitespace-delimited
  words and is located exactly at the claimed line after stripping HTML markup: S396 line 88; S397 line 160" and "A more
  directly useful single Gate quote is the 21-word text at 93-94: 'already being watched (perhaps via a different link to
  the same object), then the descriptor for the existing watch is returned.'", with required edits: per-instance qualifier
  and anchor 88-94 (S396), anchor 160-172 (+74-77) and `mined` + lesson path (both rows). My seat **agrees** with the
  substance (items 2, 3, 5 above are the same findings, independently measured) and **diverges on the quote form**: the
  21-word :93-94 text is not byte-contiguous in the pin (the file has a newline plus indentation between `same` and
  `object),`), and the C1 quote leg tests containment in a single pin line, so my Gate table quotes one byte-exact line
  per row (:93, :160) and gives the continuation lines, with their exact bytes, in the same row's prose. The sibling's
  "after stripping HTML markup" reading of :88 is the same defect as item 4.
- No other seat conflict encountered. The sibling's parser claim (`c3-r56-used-by.py` recognizes only
  `corpus/knowledge/…` in cell 11) matches my independent read of the tip blob and my end-to-end counter run.

## Not run / not verified

- I did not integrate anything into `corpus/lessons/round-56.md` or `corpus/SOURCES.md` (the L1 owns both); the
  `mined`+lesson-path landing is measured on a scratch commit only.
- C2 (fixtures/hold-out), the live compositor checks (`hyprctl getoption`, `/proc` fdinfo of the operator's Hyprland) and
  the full C1/C3 control suites on the lane itself were not my item and did not run; the only counter executions were the
  two scratch-clone runs quoted above.
- The attempt-2 lesson's final file path does not exist yet, so item 5's caveat (used-by must name the real citing path)
  cannot be closed from this seat.
