author: hyaku closure (non-author integrator, @m_zfl)

# mado round 94 — verifier spot-check (non-author)

Lane-round: mado round 94 (hyaku run 15, attempt 1). Base `a3de997289014e7dbf1d73ae206be1d6f8cdadd0`, after
`bcc21fcffafd9d8c7c06b849c41e8bea030b2a1f`. Report `.ufo/reports/round-94/mado.md` (fleet repo). This reviewer did not
author the round and changed none of its files; this file is the only lane path it writes. No reviewer seats dispatched.
Independent probes ran from scratch under `/tmp/closure-mado94-*` (removed after closure); every command and its observed
output is quoted here, so the re-check is reproducible from this file.

Driver digest (copied from the mutable `.ufo/watchdog.log`, lines 3153 and 3168 at closure):

    2026-11-07T03:00:40-03:00 launch mado round=94 pgid=2632099 driver=hyaku-inline attempt=1
    2026-11-07T04:46:55-03:00 complete mado round=94; hyaku-inline attempt=1

## Step-1 conformance

| check | command | observed | result |
|---|---|---|---|
| report committed by the lane identity | `git log --format='%an <%ae> %H %ad' -- .ufo/reports/round-94/mado.md` (fleet) | `mado-shokunin <mado@shokunin.local> e3c30566f9814855a0c21895788c1c7573cd7699 Sat Nov 7 04:45:32 2026 -0300` | pass |
| report filed after its last cited commit | `git log --format='%h %ad %cd' --date=iso a3de997..master` | last lane commit `bcc21fcf` committed 04:45:08; report 04:45:32 | pass |
| `SHONEN` heading, one line per box | read of the report (lines 153–158); `grep -c '^- \[' SHONEN.md` → 4 | `## SHONEN`, 4 lines, all `[~]` | pass |
| cited commits exist and are ancestors of `master` | `git cat-file -t <h>`; `git merge-base --is-ancestor <h> master` for a3de9972, 5a164538, bcc5429b, 38f77d89, 764d083a, bcc21fcf | all `commit`, all ancestors | pass |
| lane pushed, nothing uncommitted | `scripts/hyaku/jj-lane.sh state …/mado-shokunin`; `git status --porcelain`; `git ls-remote origin refs/heads/master` | `state branch=master local=bcc21fcf… remote=bcc21fcf… ahead=0 behind=0 head=detached tracked=0 untracked=0`; porcelain empty; remote `bcc21fcf…` | pass |
| round commits by the lane identity | `git log --format='%H %an %s' a3de997..master` | 5 commits (5a164538 dispatch evidence, bcc5429b freeze, 38f77d89 C1, 764d083a C2, bcc21fcf records), all `mado-shokunin` | pass |
| prompt carries the template contract | `diff <(sed -n 1,140p .ufo/prompts/mado-round-94.md) kimi-shokunin/templates/round-prompt.md` | 22 changed lines, all placeholder substitutions (`{{FLEET_ROOT}}` 8, `{{LANE}}` 5, `{{ROUND}}` 4, `{{AXES}}` 1); §§1–5 present (report path, report contract with `SHONEN`, commit-then-push, push scope, L0, write scope); hyaku addendum §6 at line 141 | pass |
| append-only lane records | `git diff --numstat a3de997 bcc21fc \| awk '$2>0'` | only `SKILL.md 4/1` (selftest-strength row update), `corpus/SOURCES.md 5/1` (S505 used-by, permitted in place), `quality/tool-ledger.md 4/1` (gate row update); SCORECARD/LOG/QUALITY/README/knowledge pure additions | pass |
| frozen inputs untouched after the freeze | `git diff --stat bcc5429b bcc21fc -- .ufo/waves/round-94/controls .ufo/waves/round-94/build quality/counters .ufo/waves/round-94/claims-declaration-r94.md` | empty | pass |

Conformance notes (status-neutral): the dispatch-evidence commit `5a164538` is authored 02:59:39, 61 s before the
launch line (committed 03:11:02) — the driver-attribution pattern of prior rounds. Fleet root carries an untracked `f.txt`
(2 bytes) and `trail-ids.txt` that the report names as not attributable to a round-94 seat; left untouched here too.

## Per-claim re-check

### C1 — coverage (new surface, capability): `tools/mado-mimeglob.py`, GLib 2.90.1 filename-only guess

Re-measured (plain measurements, mine):

- Before: `git ls-tree a3de997 tools/ | grep -c mimeglob` → `0` (no tool; nothing answers). After: present at `bcc21fcf`.
- Landed bytes = frozen candidate = declared pin: `git show 38f77d89:tools/mado-mimeglob.py | sha256sum` and
  `git show bcc5429b:.ufo/waves/round-94/build/mado-mimeglob.c1b.py | sha256sum` → both
  `65f80a6cb1551bb722ae7608df04fb17deba1b5cd05bef6f7fdd79bed76e2453`.
- Frozen inputs = declared pins (`sha256sum`): cases `c7b693d2…5856c`, mutants `0e74c57d…33c2`, oracle `9c4337b3…6b11`,
  host names `4b6d6a6c…4fa3`. `jq '.cases|length'` → 370; `.glib2` → `2.90.1-1`; `pacman -Q glib2 shared-mime-info` →
  `glib2 2.90.1-1`, `shared-mime-info 2.5.1-2`.
- Independent oracle (written by me, not the lane's file): a 3-line C program calling
  `g_content_type_guess(argv[i], NULL, 0, &u)` built with `pkg-config --cflags --libs gio-2.0`, compared with the
  committed tool bytes (`git show bcc21fcf:tools/mado-mimeglob.py`, run `python3 -I … --json`) on `type` and `uncertain`:

  | set | names | tool vs installed GLib |
  |---|---|---|
  | lane host-name list (cache mode, this host's DBs) | 9745 | 0 differences |
  | 1510 names I generated (seed 20261107) from `/usr/share/mime/globs2` patterns with upper-casing, `dir/` prefix, `~`, leading dot, extra suffix, plus `''`, `.`, `..`, `a.`, `ÄÖ.txt`, `x.tar.gz.part`, … | 1510 | 0 differences |
  | text mode: same 1510 + 5, `XDG_DATA_HOME` holding only a copy of `globs2` plus my rows `60:application/x-closure-test:*.zzq` and `90:text/x-closure-cs:*.Cs:cs`, empty `XDG_DATA_DIRS` (tool printed `mode=text`) | 1515 | 0 differences (`b.Cs` → `text/x-closure-cs` uncertain 1; `b.cs` → `text/x-csharp` 0, both sides) |
  | mixed: the same text-only home + `/usr/share` (has `mime.cache`) | 3 | `a.zzq` → `application/octet-stream` uncertain 1 on both — the user `globs2` is ignored once any cache loads, as the admitted entry's row M8 states |

- Evidence-verified (lane counter, not re-run): `receipts/c1-measured-r94.txt` last line
  `MADO_MIMEGLOB_COUNT: TARGET_MET … rev=38f77d89… cases=370 correct=370 … fresh=120/120 … host=9745/9745 mutants=60 killed=60`,
  `rc=0`; `base: tool absent at base-rev (answered=0)`. Separability `receipts/c1-at-c2-r94.txt` TARGET_MET at `764d083a`.
  Wave-candidate control `receipts/c1-controls-prefreeze-r94.txt:109` `DRAFT_TARGET_MISSED … correct=355` (fix shown
  able to fail).

Verdict: reported 0/370 → 370/370 reproduced in kind by an independent oracle on 12 773 names across cache, text and mixed
modes. **coverage: improved.**

### C2 — operability: kill-sets for `tools/mado-xdgmime.py` and `tools/mado-mime.py`

Re-measured (plain measurements, mine):

- Before: `git show a3de997:quality/selftest-kills/` → only `check-seat-reports.json`. After: both kill-sets present.
- Pins: `sha256sum quality/selftest-kills/mado-xdgmime.json mado-mime.json` → `d8a450bf…d4ad`, `1a0c4fe8…00b6` (= declared);
  gate `quality/check-selftest-strength.py` `2d6f1219…a61b` (= declared) and
  `git diff --stat a3de997 bcc21fc -- quality/check-selftest-strength.py tools/mado-xdgmime.py tools/mado-mime.py` → empty
  (gate and guarded tools unchanged); each kill-set's `tool_sha256` equals `sha256sum` of the committed tool.
- `jq` counts: xdgmime 19 kills / `selftest_checks` 12; mime 27 kills / 17 → 46 kills over 29 checks.
- Independent replay (my harness, not the gate): for each kill at `764d083a`, replace its `find` (exactly one occurrence
  in every case) with `replace` in a scratch copy of the tool, run `python3 -I <copy> --selftest`, and require a nonzero
  exit with every `must_fail` label on a `…_SELFTEST_FAIL:` line. Unmutated: `MADO_XDGMIME_SELFTEST: checks=12 failed=0`,
  `MADO_MIME_SELFTEST: checks=17 failed=0`, rc 0. Result: xdgmime 19/19 kills fail their named checks, distinct labels
  12/12; mime 27/27, labels 17/17 — every one of the 29 checks has a production mutant that only it must catch, which
  is what lets the gate flag a neutralised check (reported 0/29 → 29/29).
- Evidence-verified (lane counter/gate, not re-run): `receipts/c2-measured-r94.txt` `MADO_SELFTEST_KILLS: TARGET_MET …
  rev=764d083a… neutralised_flagged=29/29 hand_flagged=91/91 … control_hand_flagged=45/91`, rc 0;
  `receipts/c2-controls-prefreeze-r94.txt`: first-draft kill-sets `DRAFT_TARGET_MISSED … hand_flagged=45/91`, empty
  kill-sets `neutralised_flagged=0/29`; `receipts/harm-final-r94.txt:229,232` `SELFTEST_STRENGTH: OK tool=tools/mado-xdgmime.py
  kills=19 held=19`, `… tools/mado-mime.py kills=27 held=27`; separability `receipts/c2-at-c1-r94.txt` `SETUP_ERROR … rc=2`.
  The 91-weakening panel and the post-freeze counter-mutation limit are evidence-verified only.

Verdict: **operability: improved.**

### No owned axis harmed

`git diff a3de997 bcc21fc -- SCORECARD.md`: one appended round-94 section (claims table, capability row, named limits,
harm watch); no prior row changed. Harm receipt (evidence-verified): every lane selftest green (mako 62, portals 28, mime
17, xdgmime 12, mimeglob 19, seat-reports 23, receipt-presence 6, selftest-strength 11), prior-round counters TARGET_MET,
the round-90 C1 SETUP_ERROR as declared in round 93. Unchanged-tool diff above is empty.

| axis | verdict | basis |
|---|---|---|
| coverage | improved | re-measured: independent oracle, 12 773 names, 0 differences; tool absent at base |
| operability | improved | re-measured: 46/46 kills replayed, 29/29 checks covered; panel evidence-verified |

## Discernment spot-check (lesson `corpus/lessons/round-94.md` `## Gate`)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S515–S518 rows | admit | `curl` of the four locators (HTTP 200 each): `xdgmimeglob.c` `38ed8623…0734`, `xdgmimecache.c` `ccda4366…db69`, `gcontenttype-fdo.c` `8a5b4f47…2d7c`, spec `ar01s02.html` `e00fa00e…c61e` | agree | all four digests equal the rows; quotes located verbatim: `xdgmimeglob.c:473` `if (fnmatch ((const char *)list->data, file_name, 0) == 0)`, `xdgmimecache.c:707` `n = cache_glob_lookup_fnmatch (lower_case, mimes, n_mimes, FALSE);`, `gcontenttype-fdo.c:677-678` the "Conflicts, … Guess on the first one" comment, spec §2.4 "If several patterns of the same weight match then the longest pattern SHOULD be used." |
| `corpus/knowledge/mime-glob-guess-r94.md` | admit | my GLib oracle (C1 above), row M8 (`any other valid cache switches every lookup to caches`) | agree | the mixed-mode probe reproduces M8 on the installed library; the tool built from the entry matched GLib on every name I tried |
| the scribe's "the receipt holds the tag-stripped copy" | reject | the spec page re-fetched now: `e00fa00e…c61e`; `receipts/sources-open-r94.txt:8` holds the same digest | agree | the raw page hashes to the receipt's digest, so the receipt is not a stripped copy; the seat's `1566c459…` is not reproducible |
| wave candidate `build/mado-mimeglob.c1.py` | reject | `receipts/c1-controls-prefreeze-r94.txt:109` | agree | `DRAFT_TARGET_MISSED … correct=355 answered=356 text=209/220 cache=118/122` |
| guarding `tools/mado-mimeglob.py` in C2 | reject | AXES.md §Working the axes (causal separability) | agree | C2 would only verify after C1 landed; deferring it keeps the claims separable |

New `corpus/SOURCES.md` row re-opened with its quote: S518 (`gcontenttype-fdo.c`, lines 677–678) — quote ≤25 words,
present at the cited lines, digest equal.

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` → last line `mado ok …/SOURCES.md`,
rc 0; finding tally `W04` 57, `W01` 1 (S277, pre-existing) — equals the report's end census. Rows
`grep -cE '^ {0,3}\| S[0-9]{3,} ' corpus/SOURCES.md` → 453 (base `git show a3de997:corpus/SOURCES.md | grep -cE …` → 449).

## Trend verdicts

- **expansion — improved:** a new admitted entry (`mime-glob-guess-r94.md`) on ground the index did not hold (rows 449 →
  453, all tier A, `mined`; capability row added); verified against the installed library above.
- **quality — improved:** both claims re-measured; no admitted entry failed its re-check; the one wrong citation found
  (tool docstring cites `xdg_mime_init_from_directory (:129-200)` for the 40-byte/version rule that is
  `xdgmimecache.c:126-139`, confirmed in the re-fetched file) is already disclosed as a named limit, not left unmarked.
- **discernment — improved:** this spot-check agrees with the gate on 2 admits and 3 rejects (5/5).

## Routed defects (lane fixes next round)

1. `tools/mado-mime.py` HOME path-joined instead of concatenated (M94-1) — same defect the C1 tool fixed; still open.
2. `tools/mado-mimeglob.py` docstring cache-validity citation → `xdgmimecache.c:126-139`.
3. Kill-sets for `tools/mado-mimeglob.py` and the selftest-strength gate's own selftest (five lane tools still unguarded).
4. Round-93 routed defects 1 (QUALITY 158 instrument) and 3 (portal entry §8 frozen cases) remain open — carried.
5. M94-5: the declaration's "every default-application answer" overstated the callers; QUALITY 154 was not applied —
   apply it before the next declaration freezes.

SHONEN: all four boxes `[~]`; boxes 2 and 3 now have runnable non-author evidence (this file's replays), box 4 a sibling
sweep — operator-owned promotion review may consider them. Nothing was written to `SHONEN.md`.
