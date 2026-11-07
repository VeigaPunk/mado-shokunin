# R91MResidC1 — C1 residual attack on the frozen bytes (r1), 2026-11-06

Lane root `/home/vgpnk/Projects/shokunin/mado-shokunin`; freeze `fa71279fc927f86df2d14a62f1f60230a7cf4ada`; C1 measured at
`54a0683ce5c1c746fa02fa9f36b530c44772bfa2`; base `cc0381db585cc44c3dfc13ced807409c32c45bb0`. Scratch
`S=/fast/scratch/hyaku/mado-r91/R91MResidC1` (deleted at end; cited artifacts copied to `r1/`).

**Verdict: no defect found against C1.** The re-measurement reproduces the receipt exactly; 18 new zero-coverage
fixtures (25 types) all agree with gio inside the counter's own sandbox; the sandbox claims hold under a probe; three
informational observations below (one sandbox channel, one knowledge-wording erratum suggestion, four schema limits).

## 1. Re-run of the C1 measurement (item 1)

Exact declaration/receipt argv, run with cwd = lane root, `--scratch-root $S/remeasure`
(full log: `r1/R91MResidC1-remeasure.out`):

- Pins confirmed by `sha256sum` before the run, all equal to the declaration: counter `91ef46d1…6ede26`, cases
  `15e4b3fc…20559`, mutants `ed771654…0fb04`, oracle `c3a13e26…bf6a8`, fuzz-gen `0d147b83…418`, `/usr/bin/gio`
  `d2164260…fc462`, `/usr/lib/libgio-2.0.so.0` `b38001cc…335e`; `git show 54a0683c…:tools/mado-mime.py` =
  `2532ccb5…71a5e` (= the frozen candidate digest); both revs resolve (`git rev-parse --verify`, rc 0).
- Summary line (rc = 0), **character-identical to the last line of `receipts/c1-measured-r91.txt`**:
  `MADO_MIME_RESOLUTION: TARGET_MET pred=PRED-C1-r91-v1 rev=54a0683c… base_rev=cc0381db… cases=268 correct=268
  bl=91/91 fz=2/2 hx=1/1 l1=93/93 mc=12/12 rv=4/4 sh=65/65 fresh=120/120 fresh_seed=624086197 mutants=65 killed=65
  crashed_not_killed=0 oracle_agree=268/268 do_nothing_correct=63 naive_mimeapps_correct=62 cache_only_correct=102
  base_tool_correct=0 base_tool=absent tool_sha256=2532ccb5…` (`fresh_seed` = int(`2532ccb5`,16) ✓).

## 2. New fixtures on thinly-covered rules (item 2)

18 new cases `rs-01`…`rs-18`, schema `mime-cases-r91-v1`, ids/files in `r1/R91MResidC1-rs-cases.json` and
`r1/R91MResidC1-rs2-cases.json`, oracle labels in `r1/R91MResidC1-rs-labelled.json` / `-rs2-labelled.json`.
Labelling (read form only, one type per gio call): `MIME_ORACLE: cases=15 types=20 gio_sha256=d2164260…
libgio_sha256=b38001cc… changed=0` rc 0; `MIME_ORACLE: cases=3 types=5 … changed=0` rc 0.
Coverage check first: a scan of all 268 frozen cases shows **0 cases** with `config_dirs` ≥ 3 entries, 0 with a colon
inside an XDG dirname, 0 with a `mimeinfo.cache` `[Default Applications]` group, 0 with `NoDisplay`, 0 with a BOM, 0
with padded group/key whitespace, 0 with internal-empty string-list pieces, 0 with a non-executable first PATH entry
under a TryExec, 0 with a slash-relative TryExec, 0 with a Name-less desktop file, 0 with scheme types via
`mimeinfo.cache`; duplicate text aliases across two data dirs and uppercase-scheme asks have 1 case each (bl-63,
w07–w09 cover the glibc qsort outcome my rs-10 reconfirms).

Driver: `r1/R91MResidC1-rs-driver.py` **imports the frozen counter module** (`sha256 91ef46d1…`) and calls its
`sandbox_argv`/`run_tool`/`correct` verbatim on the frozen candidate bytes, so the comparison runs inside the exact
measurement sandbox. Result: `RS_SUMMARY: cases=18 disagree=0`, rc 0 (15-case slice and 3-case slice both 0).

Gio labels (evidence raw stdout quoted in `r1/R91MResidC1-raw-gio-evidence.txt`); candidate agreed on every type:

| fixture | rule (0 frozen coverage) | gio: default; registered; recommended |
|---|---|---|
| rs-01 | `<root>/cf:gx` in XDG_CONFIG_DIRS (colon splits the entry; its `mimeapps.list` with default `rs-z` ignored) | `rs-a.desktop; [rs-a,rs-z]; [rs-a,rs-z]` |
| rs-02 | `sy:s` in XDG_DATA_DIRS (its defaults.list + cache + desktop file ignored) | `rs-c.desktop; []; []` |
| rs-03 | UTF-8 BOM before `[Default Applications]` in mimeapps.list — **file still parses** | `rs-a.desktop; [rs-a]; [rs-a]` |
| rs-04 | `[Default Applications]` group inside `mimeinfo.cache` beats the cache addition | `rs-b.desktop; [rs-a]; [rs-a]` |
| rs-05 | defaults.list / applications/mimeapps.list / applications/mimeinfo.cache planted in a CONFIG dir (all ignored, desktop file present) | `null; null; null` |
| rs-06 | cache value byte rules: leading-space value, `id␠;id` (trailing-space id), trailing `;`, internal `;;` | all resolve as gio does; `pc5` keeps both ids `[rs-a,rs-b]` |
| rs-07 | TryExec/Exec name found via the **second** PATH entry (first entry's same-name file chmod 644) | `rs-ok.desktop; [rs-ok]; [rs-ok]` |
| rs-08 | `NoDisplay=true` app | `rs-nd.desktop; []; []` — default accepted, dropped from both lists |
| rs-09 | Hidden=true (data home) masks a loadable NoDisplay=true (system) copy | `rs-x.desktop; []; []` |
| rs-10 | same alias `x-rs/one` in two text mime dirs (targets a/b, defaults on both) | `rs-b.desktop; []; []` (second file wins, as w07–w09) |
| rs-11 | three config dirs: default(cfg1) + removal(cfg2) + additions(cfg1,2,3) + default(cfg2) | `rs-a.desktop; [rs-a,rs-b,rs-d]; [rs-a,rs-b,rs-d]` |
| rs-12 | internal empty pieces `rs-a;;rs-b` and leading `;rs-b` in mimeapps values | `[rs-a,rs-b]` / `[rs-b]`, defaults resolve |
| rs-13 | padded group headers `[ Added Associations ]`, `[ Default Applications ]` — **not recognized** (default falls to the cache addition) | `rs-a.desktop; [rs-a,rs-b]; [rs-a,rs-b]` |
| rs-14 | scheme type associated only via `mimeinfo.cache` | `rs-a.desktop; [rs-a]; [rs-a]` (cache addition sets the default) |
| rs-15 | UTF-8 BOM before `[Desktop Entry]` — **voids the desktop file** (unlike rs-03) | `rs-a.desktop; [rs-a]; [rs-a]` |
| rs-16 | type-string bytes: `TEXT/PLAIN` hits only the uppercase mimeapps key; `text/plain;charset=x` is a distinct type | `TEXT/PLAIN: rs-a.desktop; []; []`, `charset=x: null; null; null`, `text/plain: rs-a.desktop; [rs-a]; [rs-a]` |
| rs-17 | TryExec/Exec `st/prog` (contains a slash) resolved against cwd | `rs-ok.desktop; [rs-ok]; [rs-ok]` |
| rs-18 | desktop file with no `Name=` | `rs-noname.desktop; [rs-noname,rs-a]; [rs-noname,rs-a]` |

All 18 are inputs inside the declared resolution plane, and the candidate matched gio on every one → **0 defects
against C1**. First driver run reported 15/15 disagreements — that was a driver bug, not a tool disagreement: I passed
the candidate copy by its scratch path, which the sandbox's `--tmpfs` on the scratch root hides; the counter's own
`write_tool` copies scored tools *inside* the bound work dir. After copying the candidate into work (as the counter
does) the run is clean. Recorded as a dead step, no finding.

## 3. Sandbox check (item 3)

Probe `r1/R91MResidC1-probe-tool.py` run through the counter's verbatim `sandbox_argv` (runner
`r1/R91MResidC1-probe-run.py`, full output `r1/R91MResidC1-probe-output.json`):

- lane repository: `os.listdir(lane)` → `[]`, reading the labels file → `[Errno 2] No such file or directory`
  (the `--tmpfs` over the lane hides cases, labels and oracle);
- `/usr/bin/gio` and `/usr/lib/libgio-2.0.so.0`: `open()` → `[Errno 13] Permission denied` (masked with `/dev/null`),
  and `subprocess ["gio","mime","text/plain"]` → `PermissionError … '/usr/bin/gio'`; `shutil.which("gio")` → `None`
  (`PATH=/nonexistent`). Glob still sees libgio *names* under /usr/lib{,32,64} — unreadable bytes only;
- scratch root: lists only this run's work dir (`rsprobe-*`) — sibling scratch files (other fixtures, reports,
  remeasure logs) invisible;
- env: only `HOME` (fixture root), `PATH=/nonexistent`, `LC_ALL=C`; cwd = fixture root.

Draft-tool path through the counter itself (`--draft-tool probe-tool.py`, log `r1/R91MResidC1-draftprobe.out`):
268× `case … WRONG`, then `MADO_MIME_RESOLUTION: SETUP_ERROR mutant M01: find occurs 0 times`, `DRAFT_RC=2` — the
counter correctly refuses to score mutants of a text that does not contain their find-strings, and the probe's stdout
is unusable as an answer document.

**Informational (no scoring advantage shown):** sibling scored-tool copies inside `work` are mutually readable
(`work_listdir` shows `mado-mime.py`; in a real run every `t-*/mado-mime.py` persists). A mutant could locate the
candidate copy (self-byte-match + earliest mtime — the candidate is written first) and impersonate it, so "killed by a
well-formed wrong answer" would rest on cooperation rather than isolation. This does not buy the claim anything — an
impersonating mutant answers *correctly*, survives, and drops `killed` below `mutants`, failing TARGET_MET for its own
claim — but it is softer than the "same file name in an opaque directory" wording suggests. A later round could delete
the candidate copy before mutant scoring or tmpfs each tool dir. Same class: `HOME`/cwd (the fixture tree) is
writable, so a tool could vandalize later fixtures — again only self-harm under this predicate.

## 4. Schema limits (inputs `mime-cases-r91-v1` cannot express — observations, not defects)

- `oracle.abspaths()` joins every roots entry under the fixture, so an **empty** `XDG_CONFIG_DIRS`/`XDG_DATA_DIRS`
  element becomes the fixture root: gutils' skip-empty-element rules and trailing-separator forms are untestable
  in-schema.
- Env values are always absolutized: the relative-`XDG_*` fallback (`$HOME/.config`, `$HOME/.local/share`) and
  set-but-empty `XDG_DATA_DIRS` on the mime side are untestable in-schema.
- The file spec cannot create a FIFO, so the "a FIFO with mode 755 counts" program-resolution rule is untestable.

## 5. Knowledge-entry erratum suggestion (not a defect)

`corpus/knowledge/mime-default-resolution-r91.md` §8.1 says a `Hidden=true` default is accepted and "**only** the two
lists drop it". rs-08 shows `NoDisplay=true` behaves the same way (default accepted, both lists empty) and §6's load
rules do not mention `NoDisplay` either. gio: `gio mime x-rs/nd` → `Default application for “x-rs/nd”:
rs-nd.desktop / No registered applications / No recommended applications`. The tool already matches gio, so this is a
wording gap in the entry, worth an appended erratum in round 92's records.

## 6. Verification log (commands → rc)

- `sha256sum` of counter/cases/mutants/oracle/fuzz-gen/gio/libgio + `git show`/`git rev-parse --verify` (read-only
  git only) → all rc 0, digests as in §1.
- Re-measurement service (declaration argv, scratch under S) → rc 0, TARGET_MET line above.
- Oracle labelling `--label` runs ×2 → rc 0 (pinned gio/libgio hashes printed, `changed=0`).
- Driver runs (candidate vs oracle under imported counter sandbox): 15-case slice rc 0 `disagree=0`; 3-case slice rc 0
  `disagree=0`; first (buggy) run rc 1 — dead step, see §2.
- Probe under verbatim sandbox → rc 0 (findings §3); counter `--draft-tool` probe → rc 2 SETUP_ERROR (expected).
- Raw `gio mime` evidence capture → rc 0. Host safety: `gio mime` invoked with exactly one type argument throughout;
  no `gio mime TYPE HANDLER`, no xdg-mime/xdg-settings/update-desktop-database; no mutating git/jj anywhere; no
  pacman, no installs (nothing needed beyond bwrap/python3 already present).

## 7. Scratch cleanup

`S=/fast/scratch/hyaku/mado-r91/R91MResidC1` removed after copying all cited artifacts into `r1/` (verification line
in the yield summary). Both supervised runs (R91C1Remasure, DraftProbe) exited before deletion.
