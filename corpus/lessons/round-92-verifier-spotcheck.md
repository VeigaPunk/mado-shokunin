author: hyaku closure (non-author integrator, @m_zfl)

# mado round 92 — verifier spot-check (non-author)

Lane-round: mado round 92 (hyaku run 15, attempt 1). Base `d992ef7494b054591ee9104df1da49264678df5d`, after
`fbcc2672b7068b3f536a849b0ec5b72da56bf7fd`. Report `.ufo/reports/round-92/mado.md` (fleet repo). This reviewer did not
author the round and changed none of its files; this file is the only lane path it writes. No reviewer seats dispatched.

Driver digest (copied from the mutable `.ufo/watchdog.log`, lines 3118 and 3136 at closure):

    2026-11-06T22:27:35-03:00 launch mado round=92 pgid=1945399 driver=hyaku-inline attempt=1
    2026-11-06T23:56:06-03:00 complete mado round=92; hyaku-inline attempt=1

## Step-1 conformance

| check | command | observed | result |
|---|---|---|---|
| report committed by the lane identity | `git log --format='%an %H %s' -- .ufo/reports/round-92/mado.md` (fleet) | `mado-shokunin 5332a4a0ee2027b9565da7b7b461cb488a0bb93c round-92: mado report` (2026-11-06T23:55:22-03:00) | pass |
| report filed after its last cited commit | `git log --format='%h %cI' d992ef74..fbcc2672` | last lane commit `fbcc2672` 23:54:16; report 23:55:22 | pass |
| `SHONEN` heading, one line per box | read of the report (lines 135–140) | `## SHONEN`, 4 lines, all `[~]` | pass |
| cited commits exist and are ancestors of `master` | `git cat-file -t <h>`; `git merge-base --is-ancestor <h> master` for d992ef74, 6a0134ac, 243326cb, 297e2515, c7627393, fbcc2672 | all `commit`, all `anc-ok` | pass |
| lane pushed, nothing uncommitted | `scripts/hyaku/jj-lane.sh state …/mado-shokunin`; `git status --porcelain`; `git ls-remote origin refs/heads/master` | `state branch=master local=fbcc2672… remote=fbcc2672… ahead=0 behind=0 head=detached tracked=0 untracked=0`; porcelain empty; remote `fbcc2672…` | pass |
| round commits by the lane identity | `git log --format='%h %an <%ae>' d992ef74..fbcc2672` | 5 commits, all `mado-shokunin <mado@shokunin.local>` | pass |
| prompt carries the template contract | `diff <(sed -n 1,140p kimi-shokunin/templates/round-prompt.md) <(sed -n 1,140p .ufo/prompts/mado-round-92.md)` | only placeholder substitutions (`{{LANE}}`, `{{ROUND}}`, `{{FLEET_ROOT}}`, `{{AXES}}`); §§1–5 present; hyaku addendum §6 at line 141 | pass |
| append-only lane records | `git diff --numstat d992ef74 fbcc2672 \| awk '$2>0'` | only `SKILL.md 4/1` (mado-seat-reports row), `quality/tool-ledger.md 4/1`, `quality/check-seat-reports.py 88/9` (the C2 code change); LOG/SCORECARD/QUALITY/SOURCES/PROVINCE/README/knowledge pure additions | pass |

Conformance notes (status-neutral): the dispatched prompt was committed in the fleet repo under the lane identity
(`2ec4ac6e`, 22:27:33, two seconds before launch) — driver attribution, as in prior rounds. The report carries no
explicit "cross-domain evidence encountered" item (PROTOCOL §Round-robin minimum content; `grep -niE
'cross-domain|adjacen|sibling'` hits only the SHONEN box 4 line) — a minimum-content defect, routed below.

## Per-claim re-check

### C1 — coverage (capability): xdg-utils 1.2.1 `xdg-mime query default` (what `xdg-open` launches on Hyprland)

Re-measured (plain measurements, mine):

- Tool absent at base: `git cat-file -e d992ef74:tools/mado-xdgmime.py` → `fatal: … not in 'd992ef74'`;
  `git grep -l defapp_generic d992ef74 -- tools corpus` → empty. Present at `fbcc2672`. Before → after 0 → 1 tool.
- Landed bytes = frozen candidate: `git show <x> | sha256sum` for `fbcc2672:tools/mado-xdgmime.py`,
  `243326cb:tools/mado-xdgmime.py`, `6a0134ac:.ufo/waves/round-92/build/mado-xdgmime.c1.py` → all
  `4e7fff9efbd32d101d1383099566008fc49ba626be5bcc53a20766d71bc7fd88` = declared pin; 33903 bytes (≤ 65536).
- Frozen inputs unchanged after the freeze: `git diff --stat 6a0134ac fbcc2672 -- .ufo/waves/round-92/controls
  quality/counters` → empty. sha256 prefixes at `fbcc2672`: cases `3cb0cf4556171845`, mutants `f0d934f2dca4c6a9`,
  oracle `e51603991450305d`, fuzz `891704bf7cb42e44`, counter `634771678695ad19` — all = declaration pins. `jq` counts:
  cases 270, mutants 81.
- Host oracle unchanged: `sha256sum /usr/bin/{xdg-mime,bash,grep,gawk,realpath,basename}` → `a587107f…`, `c14c8f49…`,
  `19280b0e…`, `3ac64468…`, `5f6c63c5…`, `a21add5f…` — all six = `--expect-bin-sha256`; `xdg-mime --version` → 1.2.1.
- Fresh seed: `echo $((16#4e7fff9e))` → `1317011358` = the receipt's `fresh_seed`.
- Independent host probe (my run of the `fbcc2672` tool bytes with `--from-environ`, `XDG_CURRENT_DESKTOP=Hyprland`,
  against `xdg-mime query default TYPE`): text/html, x-scheme-handler/https, image/png, application/pdf,
  inode/directory, text/plain, video/mp4, application/x-zerosize, text/x-python3, application/x-shellscript, image/jpeg,
  audio/mpeg, application/zip, x-scheme-handler/mailto, text/markdown, application/x-pdf, image/jpg — **17/17 identical**
  (including the two empty answers). `gio mime text/x-python3` → `nvim.desktop` while xdg-mime prints nothing: the
  premise (GLib ≠ xdg-open's resolver) reproduces on the host.
- Independent fixture probe (my XDG roots under `/dev/shm`, `env -i`, `PATH=<fixture>/bin:/usr/bin`): (a)
  `[Default Applications] text/x-c92a=gone.desktop;inst.desktop;` with `gone` → `Exec=nosuchbin_r92` → both
  `inst.desktop` (install check skips the first); (b) only `[Added Associations]` → both empty rc 0; (c) no list entry,
  `MimeType=text/x-c92c;` → both `mt.desktop`; (d) `hyprland-mimeapps.list` → both `inst.desktop`; (e) prefix trap
  `text/x-c92` → both empty; (f) unknown type → both empty. **6/6 agree** (answer and exit status).

Evidence-verified (lane-owned counter, not executed — §Gate standard, Closure consequence):
`receipts/c1-measured-r92.txt` → `MADO_XDGMIME_DEFAULT: TARGET_MET pred=PRED-C1-r92-v1 rev=243326cb… cases=270
correct=270 … answered=270/270 fresh=120/120 fresh_seed=1317011358 mutants=81 killed=81 crashed_not_killed=0
oracle_agree=270/270 do_nothing_correct=101 naive_mimeapps_correct=78 glib_resolver_correct=139 base_tool_correct=0
base_tool=absent bytes_clause=ok`, `rc=0`; separability `receipts/c1-at-c2-r92.txt` the same line at `297e2515`, rc 0;
pre-freeze forgeries in `receipts/c1-controls-prefreeze-r92.txt` (label table fresh 58, shell-out correct 101,
bundled interpreter bytes clause FAIL) all `DRAFT_TARGET_MISSED`; `receipts/m92-3-answered-r92.txt`
`answered=0/270` rc 3; host replay `receipts/host-run-r92.txt` → `types=1133 agree=1133 disagree=0`,
`glib_agree=755 glib_disagree=378`. Revision measured is the cited C1 commit. Registry rows `mado-r92-xdgmime-default`
(gate) and `mado-xdgmime` (probe) present in `SKILL.md` (lines 876–877).

Verdict: **verified** — coverage `improved`.

### C2 — operability: `quality/check-seat-reports.py` closes round-91 residual defects F1–F5

Re-measured:

- Code moved: `d992ef74:quality/check-seat-reports.py` sha256 `13c4b0a7…ce39a` (the round-91 bytes) →
  `fbcc2672`/`297e2515` `176fc066b49334921e4fd746de55db8106709c29dfe225430224c9d46ed1663a` = frozen candidate
  `6a0134ac:.ufo/waves/round-92/build/check-seat-reports.c2.py` = declared pin; numstat 88/9.
- Frozen inputs: battery `a0cfaeb36c542367`, mutants `fe931e76f778e318`, r91 argv `d21b1979b8b42203`, counter
  `0aa4d1f18c3f309a`, round-91 counter `c74f5baae915a466` — all = pins, untouched after the freeze.
- Battery composition (`jq -r '.fixtures[].id' … | sed … | uniq -c`): F1 9, F2 5, F3 3, F4 3, F5 4, MC 13, P 8 = 45;
  mutants 37 — equal to the receipt's per-class denominators. Fresh seed `$((16#176fc066))` → `393199718` = receipt.
- My count over round 92: `Report:` trailers in `fbcc2672:.ufo/waves/round-92/w1-dispatch.json` → 14 unique matches,
  13 seat paths plus one template-text match (`write`); `git cat-file -e fbcc2672:<path>` → **13 present, 0 missing**,
  equal to the lane gate's `receipts/c2-gate-round92-r92.txt` (`seats=13 … present=13 missing=0 verdict=OK`).

Evidence-verified: `receipts/c2-measured-r92.txt` → `MADO_GATE_DEFECTS: TARGET_MET pred=PRED-C2-r92-v1 rev=297e2515…
fixtures=45 met=45 F1=9/9 F2=5/5 F3=3/3 F4=3/3 F5=4/4 MC=13/13 P=8/8 fresh=60/60 selftest=ok:SEAT_REPORTS_SELFTEST:
checks=23 failed=0 mutants=37 killed=37 base_met=19 always_ok_met=7 always_refuse_met=15 r91_counter=TARGET_MET`, with
the round-91 leg `expectations=59 met=59 fresh=60/60 … mutants=55 killed=55`, `rc=0`; separability
`receipts/c2-at-c1-r92.txt` → `SETUP_ERROR mutant N01: find occurs 0 times`, `rc=2` (the C1 revision carries the
round-91 bytes); pre-freeze controls `receipts/c2-controls-prefreeze-r92.txt` base 19/45, always-OK 7/45,
always-refuse 15/45. Self-test tally 23/23; registry rows `mado-r92-gate-defects` (gate, `SKILL.md` 875) and the
updated `mado-seat-reports` row present. The gate itself was not executed here.

Verdict: **verified** — operability `improved`.

### Routed work (not claims)

- Round-91 defect 1: `corpus/knowledge/xdg-portal-routing-resolver-r90.md` §12 "Correction (round 92, append-only)" at
  line 364 (pure addition); the portals port is rejected-this-round and routed (lesson Gate table).
- Round-91 defect 3: the lesson's `### Candidates considered` table lists 1 admit + 6 rejects = the report's count.

### Harm

- `git diff d992ef74 fbcc2672 -- SCORECARD.md`: one appended `## Round 92` section, no removed line.
- `git diff --stat d992ef74 fbcc2672 -- tools/mado-mime.py tools/mado-portals.py tools/mado-mako.py tools/mado-verify.sh`
  → empty (prior capabilities' code unchanged).
- `receipts/harm-final-r92.txt` (at `297e2515`): `MADO_SELFTEST: 460/460`, `MADO_VERIFY: CLEAN (29 pass …)`,
  `MADO_INDEX … indexed=113/113`, `LEDGER: population=176 … uncovered=0 … TARGET_MET`, mako 62/0, portals 22/0, mime
  17/0, xdgmime 12/0, seat-reports 23/0, receipt-presence 6/0, round-90 C2 `83/83 … 28/28`, round-90 C1
  `229/229 … 60/60`. The commits after the code tip (`git diff --name-only 297e2515 fbcc2672` outside round-92 waves:
  LOG, SCORECARD, QUALITY, SOURCES, the round-90 knowledge entry correction, the lesson) change no code.
- Correction sweep: `git grep -iE 'xdg-open…reduce' fbcc2672 -- SKILL.md PROVINCE.md corpus/README.md corpus/knowledge
  corpus/QUALITY.md` → the superseded sentence stands only where it was filed (round-91 entry line 9, PROVINCE 505), each
  followed by its appended correction (entry §15 line 385, PROVINCE 519) and QUALITY 1161; no unmarked copy.

## Per-axis verdicts

| axis | verdict | basis |
|---|---|---|
| coverage | improved | C1 re-measured (absent → tool; pins and six host binaries hold; 17/17 host + 6/6 fixture agree with xdg-mime) and evidence-verified (270/270, 120/120, 81/81, bytes clause ok, 1133/1133) |
| operability | improved | C2 re-measured (round-91 bytes → frozen candidate; pins hold; battery 9/5/3/3/4/13/8 = receipt denominators; my 13/13 seat-report count = gate's) and evidence-verified (45/45 from base 19/45, 60/60, 37/37, selftest 23/23, round-91 leg TARGET_MET) |

No owned axis harmed.

## Discernment spot-check (`corpus/lessons/round-92.md` `## Gate`)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| `corpus/knowledge/xdg-mime-default-resolution-r92.md` | admit | `https://gitlab.freedesktop.org/xdg/xdg-utils/-/raw/v1.2.1/scripts/{xdg-open.in,xdg-mime.in,xdg-utils-common.in}` fetched 2026-11-07 (sha256 `a6b0c7af…0790b`, `11e7d91e…5c7e`, `1f6969b5…c532` = S508); `/usr/bin/xdg-mime`; my fixtures | agree | cited lines hold: xdg-open.in:593 `detectDE`, :595-596 `DE=generic`, :392-410 `open_generic_xdg_mime` asks `xdg-mime query default`; xdg-mime.in:406 `check_mimeapps_list`, :413-414 `for desktop in $XDG_CURRENT_DESKTOP ''` with `IFS=:`, :462-470 the XDG defaults; Hyprland absent from `detectDE` (`grep -i hyprland` over all three files → none); `defapp_generic`, `check_mimeapps_list`, `defapp_fallback` byte-identical between the tag and the installed script (47/52/33 lines, `cmp`); the tool built from the entry answers 17/17 host and 6/6 fixture cases |
| round-91 entry's "xdg-open reduces to GLib" | reject (append-only §15) | xdg-open.in:392-410, :595-596, :664-665 (same fetch); host `gio mime` vs `xdg-mime query default` | agree | xdg-open on an unknown desktop calls xdg-mime's own shell resolver, never GLib; on this host `text/x-python3` gives gio `nvim.desktop`, xdg-mime empty — the rejected sentence is false here, and the correction is appended, not rewritten |
| round-90 entry §9 "invalid UTF-8 makes a file unreadable" | reject (append-only §12) | `https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/glib/gkeyfile.c` fetched 2026-11-07 (sha256 `e1d1270f6c9881da…` = S502) lines 2310, 2427 | agree | both lines are `if (!g_utf8_validate (value, -1, NULL))` inside value getters — UTF-8 is checked at value read, not at load; the §12 correction says exactly this |

`corpus/SOURCES.md` rows re-opened (all three new rows):

- S508: quote `default="$(xdg-mime query default "$filetype")"` found at xdg-open.in line 395 (my fetch, digests above);
  ≤ 25 words.
- S509: `sha256sum /usr/share/man/man1/bash.1.gz` → `b68beb3e385f7d8a…` = row container pin;
  `MANWIDTH=120 man -P cat bash | col -b` lines 3880–3881: "The -v option displays a single word indicating the command
  or filename used to invoke command" — present, 16 words.
- S510: `sha256sum /usr/share/man/man1/grep.1.gz` → `9b027d022ae9533f…` = row pin; `MANWIDTH=120 man -P cat grep | col
  -b` line 270: "The period . matches any single character." — present, 7 words. (`grep -V` prints `3.12-modified`, the
  distro build of the row's 3.12.)

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` → `mado ok`, rc 0; findings
`W04` 55, `W01` 1 (S277) — the report's "55 W04 as at start". Rows `grep -cE '^ {0,3}\| S[0-9]{3,} ' corpus/SOURCES.md`:
442 at `d992ef74` → 445 at `fbcc2672`.

## Trend verdicts

- **expansion — improved.** One admitted entry on ground the coverage map did not hold (`git ls-tree --name-only <rev>
  corpus/knowledge/ | wc -l` 112 → 113; `corpus/README.md` line 16 row and line 146 frontier line), its `source:` citing
  mined S508; three new tier-A rows; one capability row in SCORECARD. The admit survived my re-check.
- **quality — improved.** Two admitted entries found wrong were corrected append-only by named sections (round-91 §15,
  round-90 §12), each re-opened here against its primary source and agreeing; the stronger xdg-mime model supersedes the
  false round-91 sentence for `xdg-open` callers; no admitted entry failed its re-check; prior capabilities green at the
  code tip (round-90 C1 229/229, C2 83/83; mime/portals code unchanged). Open, marked and routed: the portals tool
  still answers 8/16 on the byte-class cases (port not landed).
- **discernment — improved.** The outside spot-check agrees with the gate on the sampled admit and both sampled
  rejects; the two forgery findings that would have been false greens became predicate clauses before the freeze.

## Routed defects (lane fixes next round)

1. Report minimum content: name cross-domain evidence encountered (or "none", with the sweep) in its own item; round 92's
   report has none.
2. Carried from the lane's own routing: land the `tools/mado-portals.py` GKeyFile port (`build/mado-portals.d1.py`) under
   its own frozen counter with regenerated round-90 mutants, so the 8/16 byte-class divergence stops standing.
3. C2 selftest-coverage limit (R92MMutC2 §4: a weakened passing selftest assertion is invisible to the counter's
   selftest leg) — add an instrument that fails on it.

## For the operator (promotion is operator-owned)

SHONEN boxes 2 (end-to-end task) and 3 (instructions executable without oral context) look checkable by a non-author:
this closure ran `tools/mado-xdgmime.py` from its `SKILL.md` registry argv and `--help` alone and reproduced xdg-mime on
17 host types and 6 fixtures. Nothing was written to `SHONEN.md`.
