# R54Seat07 — source/lesson prose reconnaissance (C2 pins, frozen quotations, host joins)

Wave: round 54 (`w1`), seat `R54Seat07` (scribe, prose recon). Lane root
`/home/vgpnk/Projects/shokunin/mado-shokunin`. Base `e25149fec8152a3aabd2b18a0ee8663b23cf65aa`
(HEAD at first verification = base; advanced to `350d30e4` at 14:12:16, see §4bis). Read-only;
static committed pins only.

Assigned item, verbatim from `.ufo/waves/round-54/w1-spec.json`:

> Source/lesson prose reconnaissance: verify opened uwsm pins and frozen C2 quotations from
> committed files, identify host join evidence limits, report exact quote/lines; do not draft
> committed entry. Focus specifically on assigned item 7; test a distinct failure/input from
> other seats and report independently.

Axes named (godspeed, no invented metric): **coverage** — does the C2 prose rest on bytes that
exist?; **operability** — can a counter at a scored revision reproduce each citation?;
**falsifiability** — does each frozen quote/anchor reject a mutated copy?; **evidence integrity**
— claims vs committed objects. Findings below are ordered on those axes; none claims a score.

## 0. Gates observed

- cwd `/home/vgpnk/Projects/shokunin` (fleet root) never used for writes; all commands below run
  with explicit lane paths or from the seat scratch dir.
- No git/jj mutation, no commit/push, no tracked lane edit, no fleet/sibling/source-repo write.
- No host read, package query, input capture, screenshot, producer execution, service/compositor
  mutation, network fetch. No campaign tools. No subagent dispatch.
- No tool installed or updated (system `python3`, `sha256sum`, `sed`, `git` read commands only).
- Scratch `/fast/scratch/hyaku/mado-r54/R54Seat07` (removed before yield; probe reproduced inline
  in §2 so the report is self-contained). Only write: this report file.

## 1. Pin inventory — bytes and hashes

Command (lane-root cwd):

```
sha256sum .ufo/waves/round-54/fetch/uwsm-0.27.1-*   ;   wc -c .ufo/waves/round-54/fetch/uwsm-0.27.1-*
```

Output:

```
1874fb8368f6956ebdadd1db0780ea26104f3dd3bf95cca4609ab7c77c9b597a  .ufo/waves/round-54/fetch/uwsm-0.27.1-README.md
7dd6363244c101c7a0e7641684e29b6a13905e98f9fc3a4c81421e536a976c72  .ufo/waves/round-54/fetch/uwsm-0.27.1-main.py
3982503d6445017eb55e9b68446c422b0a07a45a5d9a471b02ecc4cdb8a6f5eb  .ufo/waves/round-54/fetch/uwsm-0.27.1-uwsm-app.1.scd
 49717 README.md   199361 main.py   2309 uwsm-app.1.scd   (total 251387)
```

All three worktree hashes equal `fetch/SHA256SUMS.txt` and the byte counts in
`fetch/README.txt` (3/3). **But the pins are not committed objects:**

```
git cat-file -e e25149fec8152a3aabd2b18a0ee8663b23cf65aa:.ufo/waves/round-54/fetch/uwsm-0.27.1-README.md
→ ABSENT AT BASE  (same for SHA256SUMS.txt, registration.md, claims-frozen.md)
git ls-files .ufo/waves/round-54        → (empty)
git log --all -- .ufo/waves/round-54/fetch/  → (empty)
git status --porcelain                  → ?? .ufo/waves/round-54/
```

So at 2026-10-27T14:10:33-03:00 the C2 pin bytes existed only in the worktree of one uncommitted
wave dir. **Post-snapshot**, at 14:12:16 a sibling commit `350d30e4ec5531f65ce99a57efeb8216f38e678a`
("round-54: freeze claims, registration, source pins and wave one dispatch") landed the three pins,
`SHA256SUMS.txt`, `claims-frozen.md`, `registration.md`, both before-receipts and the wave spec:
`git ls-files .ufo/waves/round-54/fetch` lists all five files and
`git cat-file -e HEAD:.ufo/waves/round-54/fetch/SHA256SUMS.txt` → `IN_HEAD`. The base-commit
statement above therefore holds for `e25149fe` and for any scored revision before `350d30e4`;
see §4bis for the commit clock against wave dispatch. `SHA256SUMS.txt` binds bytes to filenames;
nothing in-repo binds a filename to URL commit
`0727985c9bae655bda488f87f99ea69a6ac1c003` except the `fetch/README.txt` prose (itself committed
only at `350d30e4`) and the row URL strings (a textual check, which is exactly what C2-CTL-5 mutates).

## 2. Frozen C2 quotations — byte-level verification

Frozen table source: `registration.md` §"C2 fixture inventory", and the same quotes are the
contract of PRED-C2-r54 clause (b) in `claims-frozen.md`. Reproduced probe (run with
`python3 -I` in scratch; reads the three pins only):

```python
import re
F='/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-54/fetch/uwsm-0.27.1-'
Q={'S375':('README.md',"Difference between environment state before and after preparation is exported into systemd user manager (and D-Bus activation environment if reference D-Bus implementation is used)",(117,118)),
   'S376':('uwsm-app.1.scd',"uwsm-app client sends arguments to uwsm's app daemon via a pipe.",(60,60)),
   'S377':('main.py','unit_name = f"app-{desktop_unit_substring}-{cmd_unit_substring}-{random_hex(8)}.{app_unit_type}"',(3714,3714))}
for rid,(f,q,(a,b)) in Q.items():
    t=open(F+f,encoding='utf-8').read(); lines=t.split('\n')
    span=' '.join(' '.join(lines[a-1:b]).split()); qj=' '.join(q.split())
    print(rid,'exact=',t.count(q),'collapsed=',(' '.join(t.split())).count(qj),
          'words=',len(q.split()),'inside_anchor_bytes=',q in '\n'.join(lines[a-1:b]),
          'inside_anchor_collapsed=',qj in span)
```

Output:

```
S375 exact= 0 collapsed= 1 words= 24 inside_anchor_bytes= False inside_anchor_collapsed= False
S376 exact= 0 collapsed= 0 words= 11 inside_anchor_bytes= False inside_anchor_collapsed= False
S377 exact= 1 collapsed= 1 words=  3 inside_anchor_bytes= True  inside_anchor_collapsed= True
```

Pin evidence lines:

| row | located quote line(s) in pin | frozen anchor | result |
|---|---|---|---|
| S375 | `uwsm-0.27.1-README.md:117` `- Difference between environment state before and after preparation is exported`; `:118` `  into systemd user manager (and D-Bus activation environment if reference D-Bus`; `:119` `  implementation is used)` | `README.md:117-118` | quote ends at **:119**, anchor is one line short; byte-exact count 0; only whole-document whitespace collapse matches (count 1) |
| S376 | `uwsm-0.27.1-uwsm-app.1.scd:60` = `*uwsm-app* client sends arguments to uwsm's app daemon via a pipe. Upon` (od -c confirms the leading `*`) | `uwsm-app.1.scd:60` (line correct) | frozen quote drops the two emphasis asterisks; byte-exact 0 and whitespace-collapse 0; matches only after an undefined `*`-stripping transform |
| S377 | `uwsm-0.27.1-main.py:3714` = `            unit_name = f"app-{desktop_unit_substring}-{cmd_unit_substring}-{random_hex(8)}.{app_unit_type}"` (unique; the `service` variant at `:3716` carries `@{random_hex(8)}`) | `uwsm/main.py:3714` | verbatim, unique, inside anchor |

Result: **1/3 frozen quotes are byte-verbatim (S377); 2/3 pass only under a whitespace-collapse
normalization; S376 passes under no normalization stated in the frozen files.** The only
"verbatim" definition in the frozen pair is written in the C1 section
(`registration.md`, Counter form paragraph): "exact byte contiguity after single-space
normalization of interior newlines ONLY where the frozen quote itself carries a newline".
S375 and S376 are each written as single logical lines in the frozen table, so under that
definition both fail byte-exact; C2 supplies no normalization of its own.

## 3. Host join evidence limits (frozen host set, 8 citations)

Frozen set (`registration.md` C2): `~/.local/share/omarchy/default/hypr/autostart.conf:1` … `:6`;
`~/.config/hypr/bindings.conf:2`; `~/.local/share/omarchy/bin/omarchy-toggle-idle:9`.

### 3.1 `autostart.conf` — committed bytes contradict the frozen/live line list

Committed capture at HEAD (tracked): `.ufo/waves/round-39/w1/SctHostTree/real-tree/.local/share/omarchy/default/hypr/autostart.conf`,
sha256 `acb6a66862033edd26ad98e453cc8d894388c6a2e374b491bc4061d55f7a0441`, 16 lines. Identical
bytes are committed from round 18 in six copies (`round-18/fetch/ReopenS093/autostart.conf`,
`NoteTheme/omarchy-autostart-v3.8.4.conf`, `ReviewThemeUpstream/…`, `SrcOmarchyBackground/default_hypr_autostart.conf`,
`SrcOmarchyThemeHooks/…` — all hash `acb6a668…`) and from round 39 (`round-39/w1/ExecOptionsRealTree/host-tree/…`).
Round-39 provenance: `round-39/w1/SctHostTree.md` — "read-only capture of the host Hyprland config
tree bytes into evidence … Layout preserves the host-relative path under `$HOME`".

Byte content of lines 1–9:

```
1 exec-once = uwsm-app -- hypridle
2 exec-once = uwsm-app -- mako
3 exec-once = ! omarchy-toggle-enabled waybar-off && uwsm-app -- waybar
4 exec-once = uwsm-app -- fcitx5 --disable notificationitem
5 exec-once = uwsm-app -- swaybg -i ~/.config/omarchy/current/background -m fill
6 exec-once = /usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1
7 exec-once = omarchy-first-run
8 exec-once = omarchy-powerprofiles-init
9 exec-once = uwsm-app -- omarchy-hyprland-monitor-watch
```

Against `fetch/README.txt` (untracked, L1 prose: "six `exec-once = uwsm-app -- …` lines:
hypridle, mako, waybar, fcitx5, swaybg, omarchy-hyprland-monitor-watch") and against the live
draft entry (`corpus/knowledge/uwsm-app-environment-r54.md:17`, same list "at lines 1–6"):

- `:3` is a conditional whose prefix is `! omarchy-toggle-enabled waybar-off &&`, not a bare
  `uwsm-app --` line;
- `:6` is the polkit agent — **not a uwsm-app line at all**;
- `omarchy-hyprland-monitor-watch` is at `:9`, not within `:1-6`.

Every committed copy of this file (rounds 18 and 39, same hash) disagrees with the frozen
manifest on `:3` and `:6`. There is no round-54 pin, hash or copy of the host file in
`fetch/` or anywhere else in the lane, and this round forbids host reads, so the disagreement
cannot be settled inside committed evidence: either the host file changed after 2026-10-25
(no record of a change; the user `~/.config/hypr/autostart.conf` is separately hashed
`5ace17016fe2…`, 210 B / 5 lines, in `corpus/knowledge/config-health-report-r3.md:631`) or the
prose is wrong. Committed evidence supports the latter for `:6`.

### 3.2 `bindings.conf:2` — the one well-backed join

`corpus/SOURCES.md:71` (row S059) records `bindings.conf:2-3 (e574a1ed08535e31deeafe2a26432c6862bb101e8c45d5a6b3f997d7dc810581)`.
The committed round-39 host-tree copy (same hash) has `:2`
`bindd = SUPER, RETURN, Terminal, exec, uwsm-app -- xdg-terminal-exec --dir="$(omarchy-cmd-terminal-cwd)"`,
and `round-17/w1/reports/HostTerminalFiles.md:49` states the same join. Hash-only (bytes live in
the repo only via the round-39 copy), but at least the pin row exists and matches.

### 3.3 `omarchy-toggle-idle:9` — prose only, no bytes

No `SOURCES.md` row, no hash, no committed copy anywhere in the lane
(`git ls-files | grep -Ei 'omarchy-toggle-idle'` → empty; `find .ufo/waves/round-39 -name '*toggle-idle*'` → empty).
The only committed statements are prose: `.ufo/waves/round-35/w2/reports/SentProvenance.md:279`
("`omarchy-toggle-idle:9` runs `uwsm-app -- hypridle`") and
`corpus/knowledge/config-health-report-r3.md:203` (cites `omarchy-toggle-idle:13` as a signal
producer). A counter cannot distinguish `:9` from any other line of that file, and the entry's
claim "`omarchy-toggle-idle:9` declares `uwsm-app -- hypridle`" rests entirely on the round-35
report's prose.

### 3.4 Structural limits of clause (c)

All eight frozen strings are host-absolute (`~/…`) and none is resolvable inside the repo, so
clause (c) ("entry carries at least two host join citations among the frozen host set") is a
string-presence test. It is satisfied by typing a frozen path with any content — the live draft's
false `:6` citation demonstrates this. No committed byte pin this round bridges "path string
present" to "the host declares that launch".

## 4. Live draft state observed during verification (uncommitted, sibling-authored; observation only)

Snapshot `2026-10-27T14:10:33-03:00`, HEAD `e25149fe`:

```
 M corpus/README.md          (mtime 14:08:05)
 M corpus/SOURCES.md         (mtime 14:08:20)
?? .ufo/waves/round-54/
?? corpus/knowledge/uwsm-app-environment-r54.md   (mtime 14:07:00, 21 lines, sha256 5a23af426b3db1eac4f05e0b84150c4f3d63dbd5fb320b67a04d12b523cdd3f1)
?? corpus/lessons/round-54.md
```

Base state (HEAD objects) matches `claims-frozen.md` "Before": `git show HEAD:corpus/SOURCES.md`
last data row is S374, `| S375 |` count 0; `git ls-tree HEAD corpus/knowledge/ | grep -c r54` → 0;
README has 69 `| `knowledge/` index rows for 69 knowledge files. The `uwsm-app-environment-r54.md`
README index row (README:82) and the round-54 bullet (README:121) are **worktree-only** at this
snapshot.

Checks run against the uncommitted draft (timestamped; not committed evidence):

- **Row quote sites**: the SOURCES schema is `id|source|kind|tier|teaches|location+sha|limits|status|opened|recheck|used-by`.
  There is no quote column. The three live rows carry paraphrases in the teaches cell
  (`preparation environment export to the systemd user manager`, `uwsm-app client transport`,
  `generated app unit-name construction`) and in the limits cell (`Difference before and after
  preparation is exported into systemd user manager`, `uwsm-app client sends arguments to uwsm's
  app daemon via a pipe`, `unit name includes desktop and command substrings and random
  hexadecimal text`). Exact occurrences of those cells in their pins: **0, 0, 0**; collapsed: 0, 0, 0.
- **Entry host citations**: frozen host strings present verbatim in the entry: **0/8**
  (`~/.local/…` forms absent). Only basename forms `bindings.conf:2` and `omarchy-toggle-idle:9`
  occur, plus the pathless range "lines 1–6". Strict full-string read → 0; basename read → 2.
- **Anchor propagation**: entry:9 writes "(S375; pinned README lines 117–118)" — the same off-by-one
  anchor as the frozen row; entry:11 "pinned manual line 60" is right about the line but the
  sentence is a paraphrase, not the frozen quote.
- **Host claim**: entry:17 repeats the `:1-6` list ending with `omarchy-hyprland-monitor-watch`,
  contradicted by the committed copies in §3.1.

## 4bis. Post-snapshot commit (observed 2026-10-27T14:12:16-03:00)

Commands:

```
git log -1 --format='%H%n%ad%n%cd%n%s' --date=iso 350d30e4
git show --stat --oneline 350d30e4
stat -c '%y %n' .ufo/waves/round-54/w1.ready .ufo/waves/round-54/claims-frozen.md .ufo/waves/round-54/registration.md
```

Output (excerpt):

```
350d30e4ec5531f65ce99a57efeb8216f38e678a
2026-10-27 13:42:45 -0300      (author date)
2026-10-27 14:11:10 -0300      (commit date)
round-54: freeze claims, registration, source pins and wave one dispatch
 11 files changed: claims-frozen.md 97+, fetch/{README.txt,SHA256SUMS.txt,uwsm-0.27.1-*},  receipts/before.txt 17+,
 receipts/census-before.txt 28+, registration.md 117+, w1-dispatch.json 450+, w1-spec.json 192+
2026-10-27 14:05:28.669609305 -0300 .ufo/waves/round-54/w1.ready
2026-10-27 13:59:25.276037611 -0300 .ufo/waves/round-54/claims-frozen.md
2026-10-27 14:00:21.485984258 -0300 .ufo/waves/round-54/registration.md
```

Facts: the freeze files' worktree mtimes (13:59/14:00) precede the wave-ready file (14:05:28); the
commit that lands freeze+pins+dispatch (commit clock 14:11:10) post-dates wave dispatch by 5m42s.
The commit's author date (13:42:45) precedes the freeze files' own mtimes, so it cannot describe
their creation. `registration.md` states "committed before wave 1 dispatch"; by commit clock that
was not literally true at observation. `receipts/before.txt` (committed in the same commit) records
the base assertions: `-- r54 counters present: 0`, `-- r54 entry present: 0`, `-- index count: 69`,
`-- knowledge files: 69`, `-- registry rows: 311`, `-- last row id: S374`,
`-- r54 lesson present: 0`, `-- verify selftest: MADO_SELFTEST: 460/460 assertions passed`
(@ `e25149fe`, 2026-10-27T13:57:27-03:00).

No counter exists at either revision (`ls quality/counters | grep -c r54` → 0), so none of the C2
clause (a)-(d) checks could be executed by this seat; all checks above are byte/string checks on
committed or pinned files.

## 4ter. Entry revision at 14:12:23 and cross-seat reconciliation

The live entry was rewritten after my §4 snapshot (mtime `2026-10-27 14:12:23`, 2632 B, 22 lines,
sha256 `2d9fce292815bed1ea2faea6bff7ad0088b84e9376eae9e5bc7ae9eaef336de2`). Current lines:

- `:1` — the provenance line uses the row range `S375–S377` (source text: `source: S375–S377 — uwsm v0.27.1 README, uwsm-app manual, and app-daemon source at commit` 0727985c…), so a per-token check for `S376` on that line misses even though `:11` carries `(S376; …)`.
- `:9` still writes `(S375; pinned README lines 117–118)` — the `:117-119` anchor error persists.
- `:17` now says "Read-only Omarchy defaults at `autostart.conf:1-5` declare five `uwsm-app` launches (hypridle, mako, waybar, fcitx5 and swaybg)"; `:19` states "`:6` launches the polkit agent; the monitor watcher invocation is at `:9`, not `:6`".

Re-checked against the pins and the frozen set with the same probe as §2-§3:

```
full frozen host strings in entry: 0 / 8
'S375–S377' in entry: True     'S375-S377': False
'autostart.conf:1-5' in entry: True    'autostart.conf:1-6': False
```

So the revised entry now agrees with my §3.1 committed-copy evidence and **disagrees with the
frozen registration/fetch manifest** (`:1-6 … omarchy-hyprland-monitor-watch`). That is a frozen-
contract conflict for the canonical judge: either the frozen host set's line semantics are wrong
and the predicate should not be scored against `:6`, or the entry's `:1-5` range is not a member
of the frozen set and clause (c) still sees 0 full-string citations. Under a basename read the
entry has 2 (`bindings.conf:2`, `omarchy-toggle-idle:9`).

Cross-seat reconciliation with `R54Seat27` (`.ufo/waves/round-54/w1/R54Seat27.md`), corrected after
their clarification — **two different artifacts are being counted, and both results stand**:

- Seat27's `rows=0/3` literal / `rows=1/3` with scdoc emphasis stripping count the **staged teaches
  cell** (e.g. `SOURCES.md:325` "Difference before and after preparation is exported into systemd
  user manager"), a paraphrase that is absent from the pin under any normalization.
- My §2 counts the **frozen quote vs pin**: with newline-run collapse always on the frozen rows give
  **2/3** (S375 `exact=0/collapsed=1` + S377 `exact=1`), and **3/3 only** after also adding
  emphasis stripping for S376 (`exact=0`, `collapsed=0`).

So C2 needs two undeclared normalizations relative to the C1 judge rule: (i) newline-run collapse
applied to quotes that do not carry a newline (S375), and (ii) emphasis stripping (S376). Both
seats also reproduce the en-dash provenance range and the short-name host citations. Seat27's
snapshot predates the 14:12:23 entry rewrite; their amended report records the `:1-6` frozen-set
conflict agreement (`§4b`), attributes the missing committed bytes for `omarchy-toggle-idle:9` to
this seat's measurement, and states the C2 newline-collapse gap in their `F2`.

## 5. Findings

| # | Axis | Severity | Finding |
|---|---|---|---|
| F1 | falsifiability | High (frozen fixture) | Frozen S375 quote is 3 pin lines (`117-119`) but frozen anchor is `117-118`; byte-exact count 0; it is also written as a single logical line, so the only frozen verbatim rule (newline collapse *only when the quote carries a newline*) does not admit it. A faithful counter on the frozen table yields at most 2 of the 3 rows' quotes verified (`rows<3/3`) before any control runs. |
| F2 | falsifiability (distinct input) | High (frozen fixture) | Frozen S376 quote omits the pin's emphasis markup: pin `:60` is `*uwsm-app* client sends arguments to uwsm's app daemon via a pipe. Upon`; frozen text `uwsm-app client sends …`. Exact 0, whitespace-collapse 0; only an unspecified `*`-stripping transform matches. C1-CTL-1's "not contiguous" rejection is therefore trivially reachable on the *frozen* row itself, and a faithful counter cannot print `rows=3/3` with `verdict=TARGET_MET` without an undeclared normalization. |
| F3 | coverage | Info | S377 frozen quote is exact and unique at `main.py:3714` (inside `:3714`). Only unimpeachable quote. |
| F4 | operability | Medium (provenance; was High at base) | At base `e25149fe` the pins, registration and claims are absent from git objects (`git cat-file -e` ABSENT; empty `git log --all` for `round-54/fetch/`); they were worktree-only at 14:10:33 and committed at 14:12:16 as `350d30e4`. Residual limit unchanged: C2's separator names `fetch/` as a rev-independent surface, so a counter can read pin bytes from a working tree that no scored revision authenticates, and C2-CTL-5 mutates a URL string, not bytes; `SHA256SUMS.txt` binds bytes to filenames only, so name→upstream-commit is textual (`fetch/README.txt` prose + row URL). |
| F5 | coverage (host join) | High | `autostart.conf:3`/`:6` in `fetch/README.txt` and the draft entry are contradicted by every committed copy of that file (hash `acb6a668…`, rounds 18 and 39): `:6` is the polkit agent, monitor-watch is `:9`. No round-54 host pin exists to override. |
| F6 | coverage (host join) | Medium | `omarchy-toggle-idle:9` has no registry row, hash or committed copy; only round-35 prose (`SentProvenance.md:279`). Unverifiable by any committed-file check. |
| F7 | coverage (host join) | Info | `bindings.conf:2` is backed by S059's hash and the round-39 host-tree copy (`e574a1ed…`, line 2 text matches). Strongest of the three join classes. |
| F8 | operability (schema) | Medium | PRED-C2-r54 (b) says "its `teaches`/quote cell's located quote (≤25 words) occurs verbatim in the round-54 pin", but the SOURCES row schema has no quote cell and the frozen "located quote" column has no destination; live cells are paraphrases (0/3 verbatim). The predicate's quote site must be either the frozen table itself or a new cell the row format does not define. |
| F9 | coverage (live draft) | Medium | Uncommitted draft: first snapshot (`5a23af42…`, 14:07) carried 0/8 frozen host strings, repeated the `117-118` anchor and asserted the contradicted `:6` line; rewritten version (`2d9fce29…`, 14:12:23) still carries 0/8 full frozen strings and the `117-118` anchor at `:9`, but now states `autostart.conf:1-5` with `:6` polkit and monitor-watch at `:9` (§4ter), which agrees with committed copies and contradicts the frozen table. Reported as observed; not judged as scored content, not edited by this seat. |
| F10 | evidence integrity | Medium | Base state matches the frozen "Before" (S374 last, 0 r54 knowledge files, 69/69 index; `receipts/before.txt` committed at `350d30e4` records the same at 13:57:27). The live worktree already carries entry, rows, README rows and lesson uncommitted. Any seat scoring the worktree sees content that exists in no git object at base. |
| F11 | evidence integrity | Medium | Freeze/pins/dispatch landed in one commit whose commit clock (14:11:10) post-dates the wave-ready file (14:05:28) by 5m42s, while `registration.md` says "committed before wave 1 dispatch"; the commit's author date (13:42:45) predates the freeze files' mtimes (13:59/14:00) and cannot describe their creation. Seats were already running when the freeze became a git object; `e25149fe` carries no freeze, no pins and no before-receipts. |

Conflict reported verbatim for the canonical judge (no resolution attempted here):
`claims-frozen.md` C2 requires "each of those rows is `mined`, `opened` 2026-10-27, carries a URL
pinned at commit `0727985c…`, and its `teaches`/quote cell's located quote (≤25 words) occurs
verbatim in the round-54 pin named by its source file" — against `registration.md`'s frozen quote
text and `fetch/README.txt`'s host-line list as reproduced above.

## 6. Distinct failure/input tested by this seat

1. **Markup-layer non-verbatim (F2)** — the S376 quote fails on the pin's emphasis delimiters, a
   failure independent of line/anchor arithmetic; tested by counting exact and whitespace-collapsed
   occurrences and by `od -c` on pin line 60.
2. **Committed-copy contradiction (F5)** — the frozen host-line list was tested against every
   committed copy of `autostart.conf` in the lane (rounds 18 and 39, hash-identical) rather than
   against the L1 prose; `:3` conditional and `:6` polkit result.

Both are read-only, reproducible from committed objects / the lane's own worktree pins, and do not
require the round-54 counters (none exists: `ls quality/counters | grep -c r54` → 0).

## 7. Out of scope / not done

No entry or row drafting; no counter or selftest run (counters absent at base); no control/mutation
run; no host read; no network fetch; no package/tool operation; no git mutation; no write outside
this report and the cleaned scratch dir.

## Report trailer

- Report (lane-relative): `.ufo/waves/round-54/w1/R54Seat07.md`
- Attacked predicate: PRED-C2-r54 clauses (a)-(c) and the frozen quote/host tables of
  `.ufo/waves/round-54/claims-frozen.md` + `registration.md`.
- Citations used: `claims-frozen.md` (C2 predicate), `registration.md` (C2 fixture inventory,
  Counter form verbatim note), `fetch/SHA256SUMS.txt`, `fetch/README.txt`,
  `round-18/fetch/{ReopenS093/autostart.conf, NoteTheme/…}`, `round-39/w1/SctHostTree/{SctHostTree.md, real-tree/…}`,
  `round-39/w1/ExecOptionsRealTree/host-tree/…`, `round-17/w1/reports/HostTerminalFiles.md:49`,
  `round-17/w2/reports/ReopenP6Host.md:94`, `round-35/w2/reports/SentProvenance.md:279`,
  `corpus/SOURCES.md:71` (S059), `corpus/knowledge/config-health-report-r3.md:203,631`,
  worktree-only `corpus/knowledge/uwsm-app-environment-r54.md` (sha256 `5a23af42…`),
  `.ufo/waves/round-54/receipts/before.txt`, commit `350d30e4ec5531f65ce99a57efeb8216f38e678a`,
  `.ufo/waves/round-54/w1.ready` (mtime 14:05:28).
- Scratch: `/fast/scratch/hyaku/mado-r54/R54Seat07` used for the probe, removed before yield.
