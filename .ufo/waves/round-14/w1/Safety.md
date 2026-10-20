# Safety — round 14 write safety, host mutations, candidate artifacts (w1)

Seat: `MadoR14.Safety` (sentinel, leaf). This seat audits the round-14 wave's writes and side effects, and the candidate
artifacts under `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-14` plus the source they touch:
`tools/mado-verify.sh` (GateImplement's worktree edit), `.ufo/waves/round-14/measure.py`, the removed
`receipt.py` candidate, `w1/regular-target.spec`, the evidence files, and L1's draft
`corpus/knowledge/output-colour-boundaries-r14.md`. The audit looks for raw session/device data, external mutations,
symlink writes and unsafe selftests.

This seat ran no gate, selftest, measure, build or test. It edited no shared file. Its only writes are this file, the
rendered `reports/Safety.md`, and one peer message to MeasureBuild. Host observations were metadata-only: names, sizes,
modes, digests and counts. The seat opened no `/tmp` scratch content and captured no session data.

Axes: **coverage**, because the U5 note's "nothing was exercised" statement needs adversarial confirmation, and
**operability**, because the new resolver fixtures and the measuring counter must be hermetic.

Snapshot: observations from 2026-10-20 05:40–05:48Z. Gate anchors refer to worktree
`tools/mado-verify.sh` sha256 `70bb8f9aaf9a515f…` (3,613 lines). `measure.py` anchors refer to sha256 `3a19f73d409543cf…`.
Both files were still being edited during the audit, so each anchor also quotes the code.

## Verdict summary

| # | sev | surface | status |
|---|---|---|---|
| F1 | LOW | `jj log`/`jj file annotate` without `--ignore-working-copy` snapshotted the mid-wave worktree into `.jj` | open; not yet in `corpus/lessons/round-14.md` |
| F2 | LOW | host package install (`wlr-protocols`) mid-wave left two reports with stale "not installed" host facts | install recorded in lesson/LOG; stale seat facts unadmitted |
| F3 | LOW | `/tmp` scratch outside granted paths (public upstream bytes only) | open, L1 cleanup; not yet in lesson |
| F4 | INFO | fixed-name `/tmp` clone followed by an unconditional `cd` into it | pattern note |
| F5 | LOW | GateImplement's reported delivered digest no longer binds the gate bytes | open, L1 re-hash (gate moved again, §E) |
| F6 | LOW | `measure.py` reads one input by symbolic `rev` rather than resolved `rev_sha` | **fixed** by MeasureBuild (§E) |
| F7 | INFO | N9–N12 fixtures and the regular-file resolver are confined and metadata-only | positive |
| F8 | INFO | the symlink policy follows links anywhere; "under `$ROOT`" describes path expansion, not containment | wording |
| F9 | INFO | `measure.py` write surface is confined; the fixture slice holds only `build_fixture` | positive |
| F10 | INFO | receipt wrapper rejected and removed; residual rules for L1's in-receipt R13-V3 fix | guidance |
| F11 | INFO | raw session/device data: no new identities in round-14 artifacts | positive |
| F12 | INFO | compositor and protocol-client execution: none by any MadoR14 seat | positive; supports the U5 note |

No HIGH or MEDIUM finding. No seat ran a compositor mutation, protocol client, live gate or raw-identity capture.

---

## A. Wave side effects outside the lane tree

Method: I parsed every assistant `toolCall` in
`~/.omp/agent/sessions/-Projects-shokunin/2026-10-20T01-48-55-258Z_01a156ff-505a-7798-99c2-b47895c874f4/MadoR14/*.jsonl`
and in `MadoR14.jsonl`, matching bash commands that mutate (`git add|commit|checkout|reset|stash|restore|rm|mv|push|tag`,
`jj`, `sudo`, `rm -rf`, `clone`, `-o /tmp`, `> /tmp`) or touch the substrate (`hyprctl`, `wayland-info`,
`wlr-randr`, `kanshi`, `ddcutil`, `/sys/class/drm`, `journalctl`, `loginctl`, `dmesg`), plus every `write`/`edit`
whose path is outside `round-14`. The last scan covered activity up to about 05:47:30Z.

### F1 — LOW — jj working-copy snapshot (repo-state mutation)

- **Evidence.** At 05:41:05Z, MadoR14.AttackCoverage ran `jj log -r @ --no-graph …` and `jj file annotate …` without
  `--ignore-working-copy`. `jj --ignore-working-copy op log`, which is read-only, shows exactly three new operations at
  `2026-10-20 02:41:05 -03:00`: `import git head` (`04be2ef684b2`), `snapshot working copy` (`e896589aa956`) and
  `import git refs` (`7e6c2230b361`). The previous operation was `cc5bb9e174c9` at 2026-10-19 20:38. No later jj
  operation appeared up to 05:48Z.
- **Exploit/failure path.** In this colocated repo, any default jj read verb rewrites `@` with whatever the worktree
  holds at that instant. That includes other seats' half-written files. The mid-wave tree therefore persists in the
  jj object store and op log, against the contract's "no commits" and read-only intent. Git `HEAD`/index were not
  touched by jj. Staged `A` paths come from L1.
- **Impact.** No data exposure: the tree then held only wave reports, specs and the census receipt, and nothing was
  pushed. The defect is VCS-state mutation by a read-only seat.
- **Smallest remediation.** Disclose it in the round lesson. Every future read-only jj call passes
  `--ignore-working-copy`, or uses `git --no-optional-locks` read verbs. No restore is needed, and none should be done
  by a seat.

### F2 — LOW — authorized package install; stale host facts in the same wave

- **Evidence.** At 05:41:32Z, MadoR14.OutputSpec ran `sudo pacman -S --needed --noconfirm wlr-protocols`. It ran it
  again at 05:45:52Z. [INFERENCE] `--needed` made the second run a no-op. `pacman -Qi`: `wlr-protocols r112.a741f0a-1`,
  `Install Date : Tue 20 Oct 2026 02:41:32 AM -03`, `Install Reason : Explicitly installed`. The install is recorded
  with tool, version, channel and reason at `w1/OutputSpec.md:152-158` and `reports/OutputSpec.md:95-100`.
  ReviewSourceBar ran `sudo pacman -Sw` (download only) seven seconds earlier and recorded it
  (`reports/ReviewSourceBar.md:46-48`).
- **Contradiction.** `w1/ReviewSourceBar.md:30` says "`wlr-protocols` not installed", and `w1/ScribeFrontier.md:172`
  says "no `/usr/share/wlr-protocols` directory found". Both were true only before 02:41:32 -03. They are now stale
  host facts sitting beside `EvidenceChain.md:44`, which cites the installed path.
- **Impact.** This is not a compositor mutation. [INFERENCE] The package ships protocol XML, which Hyprland does not load
  at runtime. It is a host package-set change made by a scout during a read-only wave, under the operator directive.
  The draft U5 note pins S047 to the upstream raw URL at full SHA `a741f0ac…`, not to the installed path. That choice is
  correct, and it is the right place to stay.
- **Smallest remediation.** L1 cites neither "not installed" line as current, or tags both "pre-02:41:32 -03". The lesson
  records the install. Keeping the package or removing it with `pacman -R wlr-protocols` is the operator's call.

### F3 — LOW — `/tmp` scratch outside granted write paths

- **Evidence (names, sizes, modes only; contents not opened).**
  - `/tmp/ac14/` (AttackCoverage): 23 files, including `wom-*.xml`, `cm-*.xml`, `h_*.cpp` and `hypr-tree.json` (347,495 B).
  - `/tmp/srcsafety-r14/` (SourceSafety): 17 files, including pinned Hyprland sources, `wayland-info.c`,
    `wlr-randr-main.c` and `tree.json`.
  - `/tmp/cm-35d9638.xml`, `/tmp/wlr-oms-raw.xml`, `/tmp/wlr-oms-a741f0a.xml` (ReviewSourceBar).
  - Every item is `vgpnk`-owned, mode 644/755. All are upstream source or API listings fetched by URL; none is host
    output.
- **Positive.** WlrVersion removed its own `/tmp/wlr-protocols` clone (`rm -rf /tmp/wlr-protocols`). It is now absent.
  `/tmp/hl-src-ahn` is absent too.
- **Impact.** Contract breach ("no other writes except expressly granted") with no data exposure. This differs from
  round 13's F1, which left raw `wayland-info` output in `/tmp`. Round-13 residue also remains: `/tmp/mado-r13-rows-verify.tsv`
  and `/tmp/mado-r13-rows2.tsv` (45 lines each, 0 `hypr-live` rows), plus 8 stale `/tmp/w5-mado-m52-selftest.*` dirs
  (round-13 F11, still open).
- **Smallest remediation.** After the wave, L1 runs
  `rm -rf /tmp/ac14 /tmp/srcsafety-r14 /tmp/cm-35d9638.xml /tmp/wlr-oms-raw.xml /tmp/wlr-oms-a741f0a.xml`. After the
  single selftest/recut, with no selftest running, L1 also runs `rm -rf /tmp/w5-mado-m52-selftest.*`. Pattern for future
  source opens: `curl -fsSL … | sha256sum` with `set -o pipefail`, or the `read` tool on the URL, or `mktemp -d` plus
  `trap 'rm -rf "$d"' EXIT`.

### F4 — INFO — predictable `/tmp` clone path

AttackNoHarm ran `cd /tmp && rm -rf hl-src-ahn && git clone … hl-src-ahn 2>&1; cd hl-src-ahn && git sparse-checkout …`.
The `;` means a failed clone still `cd`s into whatever `hl-src-ahn` exists. On a multi-user `/tmp`, a directory planted
by another uid cannot be removed (sticky bit), and running `git` inside it reads that repo's config (`core.fsmonitor`,
hooks). [INFERENCE] git 2.55.0's `safe.directory` ownership check refuses such a repo, and this is a single-user host,
so nothing happened. Use `d=$(mktemp -d)` for clones.

## B. Gate and fixture writes (`tools/mado-verify.sh` worktree, GateImplement)

### F5 — LOW — reported delivered digest does not bind the current bytes

`w1/GateImplement.md:18` reports "delivered file sha256 `0a2bf860…` (3,609 lines)". At 05:48Z the worktree gate is
`70bb8f9aaf9a515f…` with 3,613 lines. The transcript shows GateImplement edits up to 05:44:54Z, and the bytes changed
after the report's digest was taken. This is the R13-V3 failure class: a digest in prose that does not match the bytes
being judged. **Remediation:** L1 hashes the gate at its own measured commit and cites only that digest. Neither
GateImplement's number nor this seat's number is evidence for L1's run.

### F7 — INFO — N9–N12 and the resolver are hermetic and metadata-only (positive)

- Fixture root: `T=$(mktemp -d /tmp/w5-mado-m52-selftest.XXXXXX)` (`:395`, mode 0700), with `local NX="$T/census"`
  (`:1076`). Each new case is `mkdir -p "$NX/<case>"` plus `cp -a "$A/." …`: `local N9R="$NX/direct-dir"` (`:1194`)
  through `local N12R="$NX/source-order"` (`:1260`).
- Mutations stay inside the copy. N9/N10 run `rm -f` then `mkdir -p` on the copied `windows.conf`/`window-no-gaps.conf`.
  N11 adds `dir.conf/`. N12 runs `sed -i` on the copy's regular `hyprland.conf`. `$A`'s only symlinks are relative,
  so copies are self-contained (round-13 F14 still holds).
- Cleanup is `rm -rf "$T"` on pass (`:1447`). Fixtures are kept on failure (`echo "fixtures kept: $T"`, `:1453`). The
  new cases add more directories to an already-retained failure tree; F3 covers that.
- Resolver (`:2566`, `:2575-2576`): `if [ -f "$m" ]; then continue; fi` / `if [ -f "$x" ]; then continue; fi`, then
  `if [ -e "$x" ]; then tnr="$tnr $(src_disp "$x")"; …`. These are stat-only tests plus `compgen -G`; no target is
  opened. A FIFO, socket or device placed at a source path is therefore named `non-regular:` instead of blocking the run.
  The one content reader nearby, the toggle row, keeps its `[ -f "$tog" ]` guard before `grep`.
- `src_disp()` (`:225-228`) prints `printf '~/%q' "${p#"$r"/}"`. Newline and whitespace names in the new
  `non-regular:` class cannot forge a row. The pre-existing raw `unresolved:`/`missing:`/`extra:` text (round-13 F10
  residual) is unchanged.
- `regular-target.spec` (05:45Z) now uses anchors that match the landed lines (`if [ -f "$x" ]; then continue; fi`;
  `if [ -f "$m" ]; then continue; fi`). Mutants run through the existing `/tmp/mado-verify-regression.*` harness.
  The spec adds no new write surface.

### F8 — INFO — symlink policy: "follows" also means "follows outside the root"

`-f` dereferences, so a source symlink to a regular file anywhere passes, for example `~/.config/hypr/x.conf → /etc/…`.
The comment "every source target must resolve under $ROOT as a REGULAR file" (`:2512`) describes `~` expansion, not
realpath containment. No read escape exists, because the check never opens the target. This matches Hyprland's own
include behaviour [INFERENCE]. Wording only: "the expanded path under `$ROOT` must be, or link to, a regular file".

## C. Candidate scripts

### F6 — LOW — `measure.py` revision binding split

- `rev_sha = git('rev-parse', '--verify', f'{rev}^{{commit}}')` (`:51`) is used by `source()` (`:55`). But
  `notes = git('ls-tree', '-r', '--name-only', rev, '--', …)` (`:120`) uses the symbolic `rev`.
- **Failure path.** `measure.py HEAD` while L1 commits mid-run lists the notes from one revision and reads their contents
  from another. The output records `'revision': rev` and `revision_sha`, which hides the split.
- **Remediation (one token).** Change `rev` to `rev_sha` at `:120`. Sent to MadoR14.MeasureBuild.

### F9 — INFO — `measure.py` write surface (positive)

- All writes go under `tempfile.TemporaryDirectory(prefix='mado-r14-measure-')` (`:196`), which is auto-cleaned even on
  exception. The gate runs as `bash <temp>/gate.sh --root <tree> --no-live`, and only exit 0 or 1 is accepted
  (`:211-215`). `--no-live` overrides the `MADO_VERIFY_LIVE` env default, and a non-home root forces `LIVE=0`.
- The symlink control `link_path.symlink_to('looknfeel.conf')` (`:326`) is relative, inside the fixture dir.
  `rmtree` unlinks links without following them.
- The fixture slice `build_fixture() {` → `\nselftest() {` at the current bytes spans 144 lines, and its last `}` is at
  slice line 142. It contains only the function, with no top-level code (round-13 F15 condition re-checked).
- Inherited env [INFERENCE]: a set `GIT_DIR`/`GIT_WORK_TREE` would override `git -C REPO`. The current env carries only
  `GIT_EDITOR`, `GIT_PAGER` and `GIT_TERMINAL_PROMPT`, so this is a latent hardening note, not a defect.

### F10 — INFO — receipt wrapper rejected; residual rules for L1's R13-V3 fix

`.ufo/waves/round-14/receipt.py` is absent. L1 rejected and removed it (`w1/ReceiptBuild.md:6-20`; last candidate sha
`210d4c47…`). Before removal I read the candidate. Its findings matter only as rules for the in-receipt fix L1 now owns:

1. **Scope.** Receipt only `--selftest`, `--no-live` and `--regression` output. A bare gate run defaults to live: it
   prints `print('DP-1 %sx%s@%s' …)` (`:3003`) and `mode: live (read-only) | root: %s` (`:3580`), and
   `configerrors` echoes a first line of compositor error text. ReviewReceipt H4 and AttackMistake raised the same point.
2. **No clobber.** The candidate wrote through `mkstemp` and then `os.replace(tmp, output)`. That design does not write
   through a symlink at the final component, which is good. It did overwrite any existing receipt silently, including
   writing a refusal over a good receipt on a wrong-`REV` rerun. Any receipt writer should refuse an existing
   destination: create with `O_EXCL`, or `os.link(tmp, dest)`.
3. **Pipeline exits in evidence.** `evidence/output-source-binding.txt` and `colour-source-binding.txt` record
   `curl … | sha256sum` under `exit: 0`. That exit is sha256sum's. Independent byte equality proves the content here:
   the raw-tag digest `18a2678e…` matches the installed file. Even so, the `exit:` line does not prove curl succeeded,
   and a failed fetch would hash to `e3b0c442…`. Use `set -o pipefail` in future receipts.
4. **Selftest hermeticity, if a git-fixture selftest is revived.** Run fixture `git init/add/commit` with `GIT_*`
   removed, `GIT_CONFIG_GLOBAL=/dev/null` and `GIT_CONFIG_NOSYSTEM=1`. Otherwise an inherited `GIT_DIR` can redirect
   fixture commits into the lane repo, and global `core.hooksPath`/`commit.gpgsign` can run hooks or a signer. This
   host's global config sets neither key (key-name census only).

## D. Raw session/device data and substrate execution

### F11 — INFO — no new identities in round-14 artifacts (positive)

- I grepped round-14 (`w1/*.md`, `reports/*.md`, `evidence/*`, `measure.py`, `spec.json`, `dispatch.json`) and the
  corpus/SCORECARD worktree diff (added lines only). The pattern covered connectors (`eDP|HDMI|DP-N`), `serial`,
  `make:`/`model:`, EDID, `/dev/dri`, `card[0-9]`/`renderD`, instance-signature shapes, `title:`/`app_id`/`class:`,
  `3440`, `token` and `password`. The corpus/SCORECARD diff has 0 hits.
- Wave hits are protocol vocabulary (`serial_number` as an event name, `done(serial)`), plus two `DP-1` strings in
  `SiblingOverlap.md:76,133`. Those reproduce committed text: `DP-1` already appears in `SKILL.md` (6 hits), 21
  corpus-note hits and gate `:3003`. The wave adds no new device identity.
- `globals.json`, read by OutputHost and the U5 note: all 72 `globals` entries have exactly `{interface, version}`. Its
  metadata carries socket `wayland-1` and probe/tool/compositor pins, which is what the R13-V1 wording now says
  (U5 note `:51`).
- `evidence/census-before.txt` holds only the census command, exit and W04 duplicate-URL lines.

### F12 — INFO — zero compositor or protocol-client execution (positive)

- The scan found no `hyprctl`, `wayland-info`, `wlr-randr`, `kanshi`, `journalctl`, `dmesg`, `loginctl`, `ddcutil` or
  `/sys/class/drm` invocation by any MadoR14 seat or by L1. The only matches were `pacman -Q` package-name queries.
  No gate, selftest, measure or receipt was executed. This supports the U5 note's scoped negative statement (`:55`):
  "No `wlr-randr`, output-management test/apply, surface colour request, screenshot, compositor reload or host-config
  write was run". The two non-config host mutations, F1 and F2, should be disclosed beside it.
- **Forward risk (not executed).** `SiblingOverlap.md:78` lists `hyprctl -j monitors` as a "Read-Only Probe", and
  `:136` lists `journalctl -k`. [INFERENCE] Hyprland's monitor JSON carries make/model/serial/description, and the
  kernel journal is a raw log. If either probe is ever adopted, project it in-pipe and never persist raw output.

`resume_continuity_v1` (role clause) does not apply. Its only repo match is a historical transcript under
`.ufo/interactive-sessions/`, and no round-14 surface implements resume.

## Source opens

No external source was opened by this seat. All facts are own observations, 2026-10-20, tier A (own measurement):
`jj --ignore-working-copy op log`, `pacman -Qi wlr-protocols`, `git --version` (2.55.0), `stat`/`ls` on named `/tmp`
paths, `sha256sum`/`wc -l` on the gate and `measure.py`, a structured parse of seat transcripts, and the
`git config --global --list` key-name census. These are admitted for F1–F12 only. They flip on any later edit or
command by a still-running seat.

## Tooling record

No tool was installed or upgraded by this seat. Commands used: `git --no-optional-locks`, `jj --ignore-working-copy`,
`pacman -Qi`, `stat`, `sha256sum`, `wc`, `python3` (stdin script parsing transcripts; no file writes).

## Checks for L1 (not run by this seat)

- `jj --ignore-working-copy op log -n 4`: confirms F1's three 02:41:05 operations, with nothing newer from seats.
- `pacman -Qi wlr-protocols | grep -E 'Version|Install Date'`, then reconcile `ReviewSourceBar.md:30` and
  `ScribeFrontier.md:172` (F2).
- `sha256sum tools/mado-verify.sh` at L1's measured commit; cite only that digest (F5).
- `grep -n "ls-tree" .ufo/waves/round-14/measure.py` shows `rev_sha` once F6 is fixed.
- After the single selftest/recut: run the F3 `rm -rf` list, then `ls -d /tmp/w5-mado-m52-selftest.* | wc -l` → 0.

## E. Re-inspection after L1 integration (2026-10-20, about 05:50Z; no tests)

This section answers the parent's request to inspect the current artifacts. Everything here is read-only observation.

- **U5 note** `corpus/knowledge/output-colour-boundaries-r14.md` (sha256 `f79d0c3d2c5f034a…`): no host identity. It
  binds S047/S048 to upstream URLs at full SHA and tag, not to the wave-installed path. Its scoped negative statement
  (`:55`) still agrees with the F12 transcript scan.
- **SOURCES rows S047–S049** (`corpus/SOURCES.md:59-61`): every row carries a canonical URL or a repo path, a pinned
  revision or tag, and a raw sha256. They contain no device, output or session identity. S049 cites `globals.json` for
  metadata scope only (`captured_utc`, field classes) and reproduces no values. The corpus/SCORECARD added-line scan
  (identity pattern from F11) still finds 0 hits.
- **F6 fixed.** MeasureBuild reported the fix, and I observed it. `measure.py` (sha256 `e01c75ce503d5325…`) now reads
  `git('ls-tree', '-r', '--name-only', rev_sha, '--', …)` at `:147`. Symbolic `rev` appears only at argv (`:49`),
  `rev-parse` (`:56`) and the printed `'revision'` field (`:538`).
- **measure.py growth (538 lines), still confined.** Every new write is a fixture mutation under the
  `TemporaryDirectory` tree (`:223`): `unlink`/`mkdir` at `:256-274`, `:428-429`, `:444` and `:456`; the newline-name
  file at `:413`; `symlink_to('looknfeel.conf')` at `:397`. Gate invocations are still only `--root <tree> --no-live`
  (`:239-240`). Nothing references `HOME`, `expanduser` or `environ`.
- **Gate moved again** to sha256 `96e719af952342fd…`. Every added line that writes is in N9–N12 fixture copies under
  `$NX` (`mkdir -p`/`cp -a`/`rm -f`/`sed -i`). No added line uses `hyprctl` or `$HOME`, and none redirects into a
  non-fixture path. F5 stands: cite only L1's own measured digest.
- **Lesson/LOG tooling record.** `corpus/lessons/round-14.md:100-114` and `LOG.md:974-975` record the
  `wlr-protocols r112.a741f0a-1` install (tool, version, channel, reason) and ReviewSourceBar's download-only `-Sw`,
  which closes F2's record duty. The lesson's "no feature requests were issued by this round" matches F12.
- **Disclosure gap (smallest fix).** The lesson's "Tooling and safety" paragraph does not yet mention two non-config
  side effects: the F1 jj working-copy snapshot (3 ops at 02:41:05 -03, AttackCoverage) and the F3 `/tmp` scratch
  (AttackCoverage, SourceSafety, ReviewSourceBar; upstream bytes only). One sentence beside the install record covers
  both, without changing the "host configuration and compositor state are read-only" claim. That claim stays true.
