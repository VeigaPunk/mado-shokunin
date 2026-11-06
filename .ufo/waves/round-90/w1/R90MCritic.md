# R90MCritic — round-90 declaration attack (pre-freeze)

Seat `R90MCritic`. Target: `.ufo/waves/round-90/claims-declaration-r90.md` at base
`5041acf99e27263872bf0441ad5f9d4316152605`. Every command below is **DRAFT**: no lane receipt was
written, no mutating git outside my own fixture repos, no lane file touched except this report.
Scratch `S=/fast/scratch/hyaku/mado-r90/R90MCritic` deleted before yield.

**Verdict: NOT READY TO FREEZE.** Four blockers (F1, F2, F3, F14) and seven highs. The two draft
counters do meet their draft predicates (C1 92/92 + 31/31, C2 15/15 + 13/13), but the C1 model is
wrong on a class the frozen cases do not contain, and the C2 gate — the check the round will
actually run before the records commit — is a silent no-op under this host's git config and
accepts a receipt the commit deletes. Details, severity, and the exact declaration change:

| # | Sev | Claim | One-line |
|---|---|---|---|
| F1 | **blocker** | C1 | `UseIn` with an invalid escape: the binary loads the backend, the tool skips it (oracle-confirmed). |
| F2 | **blocker** | C2 | `--worktree` reads only `+++ b/`; host git config `diff.mnemonicPrefix=true` makes it see 0 records and print OK. |
| F3 | **blocker** | C2 | `--worktree` counts a base-tree receipt present even when the working tree deletes it. |
| F4 | **high** | C2 | `2/2` is hand-picked; the honest population (records commits since r80) shows 4 defective commits. |
| F5 | **high** | C1 | The "count that would show it unmoved" counts its own `IFACES` literals; a stub passes it. |
| F6 | **high** | C1 | The r12 baseline is misstated: 16 rows including Settings and Secret, not 14 without them. |
| F7 | **high** | C1 | The "blind set" is not in the labelled file (92 ids = the L1 generator's 92). |
| F8 | **high** | C1 | The counter never pins/checks `oracle_binary_sha256`. |
| F9 | **medium** | C1 | The oracle cannot label a descriptor source name containing whitespace; the tool models it. |
| F10 | **high** | C1 | No adversarial control: the tool runs with full FS read and the predicate scores only models. |
| F11 | **high** | C1 | "frontier → core" is not supported by `corpus/README.md` §Frontier; the plane is already sourced ground. |
| F12 | **medium** | C2 | Axis is operability by surface but calibration by effect; §9 would demand a mismatch count. |
| F13 | **high** | Both | `Named limits` is C1-only; C2's grammar/mode limits and C1's oracle limits are undeclared. |
| F14 | **blocker** | Round | §2b is absent from the declaration: no sourced row opened this round, no census/lesson pointer. |
| F15 | **low** | C2 | The predicate does not bind the controls; the cheapest always-OK scores 9/15, not the declared 7/15. |

## F1 — blocker — C1: `UseIn` parse failure skips a descriptor the binary loads

Evidence (`build/mado-portals.c1.py:277`): `use_in = string_list(g["UseIn"]) if "UseIn" in g else None`
is inside the `try` of `load_portal`; a malformed `UseIn` raises `KeyFileError`, `load_portal` returns
`None`, the whole descriptor disappears. Upstream `src/xdp-portal-config.c:243-246` reads
`impl_config->use_in = g_key_file_get_string_list (keyfile, "portal", "UseIn", NULL, error);` and
never checks the result: on failure `use_in` is NULL and the backend stays loaded with no UseIn.

Reproducer (DRAFT, oracle only; exit 0): `S=$HYAKU_SCRATCH/.../usecase`, two dir-mode cases,
`my.portal` = `[portal]\nDBusName=org.freedesktop.impl.portal.desktop.my\nInterfaces=org.freedesktop.impl.portal.FileChooser;\nUseIn=x\q\n`,
`portals.conf` = `[preferred]\ndefault=my` (and a second with `default=*`). Oracle:
`FileChooser=['my'] (default config)` for both; the candidate: `FileChooser=[] (no-backend)` for both.
This is exactly the UseIn rule the declaration says it models (line 30).

**Exact change:** before the freeze, parse `UseIn` with a local try that assigns `use_in = None` on
failure, and add these two cases to `controls/portal-cases-r90.json` (N grows by 2; the after-state
and every pin change accordingly). If the L1 refuses the fix, add the limit "a descriptor whose
`UseIn` list is invalid is skipped by the tool but loaded by xdg-desktop-portal" to `Named limits`
and strike "UseIn optional" from the modelled claim. The first option is smaller and keeps the claim.

## F2 — blocker — C2: `--worktree` is a silent no-op under the host's git config

`check-receipt-presence.c2.py`'s `added_lines` accepts a path only from a line starting `+++ b/`
(`line[6:]`). This host's global git config sets `diff.mnemonicPrefix=true`
(`git config --show-origin --get diff.mnemonicPrefix` → `file:/home/vgpnk/.config/git/config true`),
so `git diff` writes `+++ w/SCORECARD.md` and every changed record file is skipped.

Reproducer (DRAFT, fixture repo under my scratch, `git -C` toplevel asserted): base commits
`SCORECARD.md`; working tree modifies it and adds a citation. With the real environment:
`RECEIPT_PRESENCE: mode=worktree records=0 cited=0 present=0 missing=0 verdict=OK`, rc 0.
With `GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=diff.mnemonicPrefix GIT_CONFIG_VALUE_0=false`:
`records=1 cited=1 present=1 missing=0`, rc 0. The C2 counter cannot see this: `run_check` sets
`HOME=/nonexistent`, `GIT_CONFIG_NOSYSTEM=1`, so its 15/15 is scored under a git configuration the
lane never uses. The declaration's "the records commit of round 90 is gated by `--worktree` mode"
(line 70) therefore describes a gate that prints OK without reading the change.

**Exact change:** in the check, pass `--src-prefix=a/ --dst-prefix=b/` to `git diff` (or parse the
prefix generically); in the counter, add a fixture/control run with `diff.mnemonicPrefix=true` that
must reproduce the ordinary verdicts, and add `worktree_mnemonic=OK` to the concrete after-state.
The C2 "Use in this round" sentence must say the gate is first proven under the host's real git
config. Until then `met=15/15` is not evidence for the use the round claims.

## F3 — blocker — C2: a receipt deleted in the same change is counted present

In `--worktree` mode `present(p)` returns True whenever `git cat-file -e <base>:<p>` succeeds —
before it ever looks at the worktree; a file deleted in the working tree is therefore "present",
though the commit will not carry it. Reproducer (DRAFT, fixture, prefixes pinned): base has
`.ufo/waves/round-90/receipts/keep-r90.txt`; working tree deletes it and adds a line citing
`receipts/keep-r90.txt`. `--worktree` → `records=1 cited=1 present=1 verdict=OK`, rc 0. Commit the
same tree and `--rev HEAD` → `missing receipts/keep-r90.txt -> .ufo/waves/round-90/receipts/keep-r90.txt
SCORECARD.md:2`, rc 1. The pre-commit gate passes the exact class (cite a receipt the commit does
not carry) it exists to stop.

**Exact change:** `present(p)` must require the path to exist on disk and not be deleted in the
diff (base-tree presence alone is not carriage). Add fixture W12 to
`controls/receipt-presence-set-r90.json` (base carries the receipt, worktree deletes it and cites
it → `expect_rc=1`, `expect_missing=["receipts/keep-r90.txt"]` if the citation is written bare) and a
matching mutant, so `expectations=16 met=16` (or the final count) and `killed` grows by one.

## F4 — high — C2: `defects_detected=2/2` is not a population

The four revisions are the two motivating spot-checks (D88, D89) plus the two final commits graded
clean (C88, C89); the 11 worktree fixtures are L1-authored units. The reviewer seat's own brief is
the honest population: every lane commit since round 80 (`git log --format=%H 5041acf9 --since=2026-11-04`).
I ran the candidate `--rev` over the **24** record-touching commits from r85–r89: 4 are MISSING —
the two known (`498855cb`: `receipts/harm-final-r88.txt`; `51bf076f`: `receipts/census-end-r89.txt`,
`receipts/harm-final-r89.txt`) plus two the spot-checks did not route:

- `942365c8` (round-85 records, rc 1, 4 distinct receipts:
  `receipts/control-c2-r84-unguarded.txt`, `receipts/frozen-input-crosswalk-r85.json`,
  `receipts/harm-watch-r85.txt`, `receipts/independent-score-r85.txt`); `independent-score-r85.txt`
  first appears in `2b6dd76b`, i.e. after this commit.
- `01be4234` (round-86 records, rc 1, 2 distinct: `receipts/census-end-r86.txt`,
  `receipts/cleanup-r86.json`); first appear in `3afdb713` / `d7ffa762`.

These are the same cite-before-commit class; the check generalises beyond the two cases it was
tuned on, but the declaration's `2/2` hides it. The population command is re-derivable read-only,
and the label is not the check's own opinion: the cited file's first appearance in `git log
--diff-filter=A` is independent evidence.

**Exact change:** replace "4 lane revisions … + 11 worktree fixtures" with the population definition
(all lane records commits from the round-80 base to the round-89 tip, plus the round-90 records
change), add `942365c8` and `01be4234` to `controls/receipt-presence-set-r90.json` with their exact
missing sets, and state `defects_detected=4/4 ok=20/20` (or the reviewer's final k) with the
`git log` command. The 11 fixtures stay as unit tests; they are not the population.

## F5 — high — C1: the "count that would show it unmoved" certifies itself

Declaration lines 32-36 run a regex over `<rev>:tools/mado-portals.py` that counts the literals
inside the tool's own `IFACES = (...)` tuple. A nine-line stub that defines the tuple and exits 0
prints 21 and "moves" the count; the count measures the tool's vocabulary, not a resolver. The real
before/after is the counter's `base_correct=0` (tool absent) → `correct=N`. The draft's own output
shows the intended controls are `r12_rule_correct=20`, `host_table_correct=10`, `base_correct=0`.

**Exact change:** delete the regex as the count and put the frozen counter invocation there (or
`--selftest` plus one decision fixture that a stub cannot answer); state the after-state as one
concrete value, e.g. `cases=92 correct=92 mutants=31 killed=31 r12_rule_correct=20
host_table_correct=10 base_correct=0` (numbers re-derived after F1/F7 change N). Keep the regex only
as a supporting grep, labelled as such.

## F6 — high — C1: the round-12 baseline is misstated

Declaration lines 14-16: "a hand-derived routing table for 14 interfaces … it does not list Secret,
Background, Wallpaper, RemoteDesktop, Clipboard, Usb, Settings." The note
`corpus/knowledge/xdg-portal-routing-r12.md` has **16** rows (lines 51-62: FileChooser, Screenshot,
ScreenCast, GlobalShortcuts, InputCapture, AppChooser, Print, Notification, Inhibit, Access, Account,
Email, DynamicLauncher, Lockdown, Settings, Secret); it **does** list Settings (line 61) and Secret
(line 62, unresolved "No matching preferred candidate evidenced"). Five of the 21 are absent:
Background, Wallpaper, RemoteDesktop, Clipboard, Usb. The declaration's before-state understates the
prior note and overstates the tool's interface delta.

**Exact change:** "a hand-derived table of 16 interfaces (15 with a named candidate; Secret
unresolved at :62), no tool, no none/`*`/UseIn/last-resort rules, no multi-directory precedence; the
five interfaces it does not list are Background, Wallpaper, RemoteDesktop, Clipboard, Usb." Then
state the delta as the algorithm families plus those five interfaces, not "21 from scratch".

## F7 — high — C1: the blind set is not in the labelled file

Declaration line 42 says `controls/portal-cases-r90.json` is the L1 generator **+ the blind set from
R90MScoutCases**. At read time `controls/portal-cases-r90-blind*.json` does not exist
(`ls: cannot access …: No such file or directory`), and the labelled file's 92 ids are exactly the
generator's 92 (counts d13/k6/n6/s6/a7/f5/g18/p10/u7/x14 = 92; zero ids outside that prefix set).
The wave has a scout seat for them, so this can be fixed before the freeze — but as written the
independence sentence is false, and the tool was already developed against the 92.

**Exact change:** freeze only after the blind file exists and is merged; run the candidate once on
the blind subset **before** changing it and record `blind_first_run=k/N` in the draft revisions (a
fix after a blind failure is allowed but the pre-fix score is what proves the cases were blind);
score the blind cases separately in the receipt (`blind_correct=… blind=N`), not only in the total.

## F8 — high — C1: the oracle binary is not pinned by the counter

`controls/portal-cases-r90.json` records `oracle_binary_sha256=e1429fbe1bf6c2203ba07f478b9e92e9221437b13a92eebafb0982748583a4f8`
(my fresh oracle run on this host produced the same value, and the same host-tail digest
`4a4cf319…`). The counter pins only the case/mutants files and the host tail; it never compares this
field to the installed binary or to a frozen pin. A package upgrade (or a label file from another
build) leaves the labels stale while the counter stays green. The labels are debug lines
(`g_debug` 817/846/879/891/915), not an API; the declaration's trust in them should be explicit.

**Exact change:** add `--expect-oracle-binary-sha256 e1429fbe…` to the counter and check the
labelled file's field (and, if acceptable, the installed binary) against it; report the value in the
receipt. Add to `Named limits`: "labels are g_debug lines of 1.22.1-2; a different build is not
modelled."

## F9 — medium — C1: the oracle cannot label whitespace source names

`portal-oracle-r90.py` parses `Using (\S+)\.portal for …`. A descriptor file name with a space is
legal and the tool models it (source = basename up to the last dot). Reproducer (DRAFT): dir mode,
`my backend.portal` implementing FileChooser, `portals.conf` `default=my backend` → oracle
`FileChooser=[]`; the plain-name control (`mybackend.portal`) → `['mybackend'] (default config)`;
the candidate on the space fixture → `['my backend'] (default config)`. A frozen case of this class
would fail against the oracle's own [] label.

**Exact change:** either widen the oracle regex to `Using (.+?)\.portal for (\S+) \(` (anchored) and
add the case (then the tool's model is verified), or add the limit "source names containing
whitespace are modelled but not oracle-labellable; no case covers them" and stop claiming descriptor
name coverage beyond the case set.

## F10 — high — C1: no adversarial control; the tool has full read access

The counter runs `sys.executable -I <tool> --json …` with the case fixtures under scratch but no
working-directory or filesystem restriction (`env` only fixes PATH/HOME/LC_ALL). A tool that opens
`controls/portal-cases-r90.json` at its absolute path, matches the fixture bytes, and prints the
labels would pass every case; the only guard is the mutant stage, which a tool can defeat by
retaining the real source's `find` strings and detecting the counter's `mut-<id>.py` invocation to
fail one case per mutant. The declaration's controls (r12 rule, host table, base) are all honest
models, not the cheapest control that skips the work; the lane's own r46 counter used bubblewrap for
this reason. The ExecForgery seat is assigned to this, but the declaration must not freeze without
its result.

**Exact change:** declare the forgery controls (label-reader; oracle shell-out) and add both to the
predicate as `forgery_correct < cases`; run the tool under a read-only root that excludes
`.ufo/waves/round-90/controls` (bwrap precedent) or add a source-access refusal, and commit the
control receipts before the freeze. If a forgery reaches N, the counter/target is wrong per §6.9.

## F11 — high — C1: "frontier → core" is not supported by the corpus frontier

`corpus/README.md` §Frontier has no portal-routing bullet; the r12 item is the historical bullet
(lines 225-228) "moved … portal routing onto sourced ground" with its open list (rule attribution,
output-management, input debugging, Waybar module text) not including portals. The plane is already
sourced ground, not a frontier row this round moves. Also by §6.9 "name the axis by the surface the
round changes": the surface is a new runnable tool (operability), while the claim labels it coverage;
if both claims are operability, AXES's "two claims on one axis = one claim" collapses the round.

**Exact change:** choose one and write it in the declaration: (a) add the `corpus/README.md`
frontier bullet and the knowledge entry this round ("portal routing gains a runnable resolver;
frontier → core") plus a coverage rubric whose command enumerates the surface, or (b) declare C1 a
**capability acquisition** with a capability row and no numeric coverage score (the r12 note is
sourced ground; the new capability is the tool), and say why its axis verdict is coverage rather
than operability. Option (b) is smaller and honest; then state the SCORECARD row is the capability
row, not a coverage delta.

## F12 — medium — C2: axis is operability by surface, calibration by effect

The round changes a runnable artifact (`quality/check-receipt-presence.py`) — operability by AXES.
Its effect is to catch records that overclaim their self-assessment — calibration's definition. If
the claim is calibration, §6.9 requires a count of mismatches between the lane's self-assessment
(`SCORECARD.md`/`SHONEN.md`) and observed repo state, with a command; the C2 counter counts receipt
citations, not that. Two claims on one axis also count as one.

**Exact change:** keep C2 **operability**, name the surface as "a runnable pre-commit gate", and
record the calibration effect as a note in the SCORECARD row (the four record commits found), never
as a calibration score. Do not use the word "calibration" in C2's claim line.

## F13 — high — Both: named limits hide real gaps, C2 has none

Declaration `Named limits` (lines 82-89) speaks only about C1 and omits the confirmed gaps above
(oracle whitespace, binary pin, the UseIn class while it is unfixed). C2 has no limits at all,
though the check only reads added lines of six record-file classes, only `receipts/` paths with five
extensions, trusts `--commit-path` plus the base tree, and is sensitive to git config (F2) and
deleted files (F3). Its `--rev` mode also cannot see non-receipt evidence (reviews, reports,
verdicts) cited as if carried.

**Exact change:** add a C2 limits block: "only added lines of SCORECARD.md, LOG.md,
corpus/QUALITY.md, corpus/README.md, corpus/lessons/*.md, corpus/knowledge/*.md; only
`receipts/<name>.{txt,json,jsonl,md,log,csv,tsv}`; a bare name resolves by `-r<k>` suffix or the
commit's round; `--worktree` carriage is the commit-path list plus the base tree; pre-existing
citations not on added lines are not re-checked." Add C1's missing limits from F1/F8/F9.

## F14 — blocker — §2b is absent from the declaration

The round is a child-lane round; §2b binds: census before → after, one mined mistake, at least one
claim resting on a `SOURCES.md` row opened this round. Current state: `receipts/census-start-r90.txt`
exists with `mado ok` and `rc=0` (good), `corpus/lessons/round-90.md` already carries M90-1 with
class/evidence/captured-by/fix (the pre-fix generator is kept and
`controls/check-fixture-lines-r90.py` prints six merged lines rc 1 on it, `merged=0` rc 0 on the
frozen file — a real fail-able fix), but the declaration names neither, and `corpus/SOURCES.md` still
ends at S500 (round 89). The C1 claim rests on the 1.22.1 tarball and the portals.conf/GLib sources;
none is a row opened this round.

**Exact change:** add a `## §2b` section to the declaration: (a) census start
`.ufo/waves/round-90/receipts/census-start-r90.txt` rc 0 → end command
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado`
with the end receipt path; (b) the M90-1 pointer and the fixture-lines gate as C1's case-construction
control; (c) "C1 is the sourced claim: S### for the xdg-desktop-portal 1.22.1 tarball (sha256
5afeda95…3625, two fetches byte-identical) and the portals.conf(5)/GLib gkeyfile sources opened this
round; `corpus/knowledge/xdg-portal-routing-resolver-r90.md` cites them." Freeze the S### ids in the
declaration so the report's Sources & frontier section can name them.

## F15 — low — C2: the controls are printed, not bound; 9/15 is the cheapest always-OK

The predicate (`TARGET_MET iff … every frozen expectation … and every frozen mutant …`) has no
control term, so `always_ok_met` is decorative. The declared 7/15 is also not the cheapest
always-OK: the counter's `forg_ok` prints `RECEIPT_PRESENCE: cited=1 verdict=OK`, which the SUMMARY
regex cannot parse (`RECEIPT_PRESENCE: .* cited=`), so the two clean revisions' `min_cited=1` fail.
A forgery printing `RECEIPT_PRESENCE: mode=rev cited=99 verdict=OK` scores **9/15** — I ran a copy of
the counter in scratch with that one line changed: `always_ok_met=9/15`, everything else unchanged
(DRAFT, rc 3). Still below 15, so the target is not met, but the control receipt understates the
cheapest cheat by 2.

**Exact change:** add `and always_ok_met < expectations and always_missing_met < expectations` to
PRED-C2-r90-v1's sentence and code, and score the smart always-OK (`cited=99`) as the control;
state 9/15 in the after-state. [The 9/15 is measured; the "smart" label is mine.]

## Answers to the seven assigned attacks

1. **Coverage or quality / frontier → core.** C1 is a legitimate capability acquisition (new tool on
   a plane with no instrument), but not a frontier → core move: the r12 note is already sourced
   ground and §Frontier has no portal row (F11); and the prior state is 16 rows incl. Settings/Secret,
   not 14 without them (F6). By the surface it changes (a new runnable tool) the axis is operability;
   the coverage label needs the explicit capability framing of F11(b), else C1+C2 are one claim.
2. **Oracle independence and trust.** Labels come from the production binary, but the L1 wrote the
   generator, the oracle parser and the tool; the blind set is absent from the frozen bytes (F7);
   the binary sha is recorded but never checked (F8); the labels are g_debug lines; the parser cannot
   label whitespace source names (F9). The oracle is a good authority for the classes it can label;
   it is not independent evidence of the tool's model on its own.
3. **Can a cheaper control meet either target?** Not as scored: C1's r12/host/base controls are
   20/10/0 of 92; C2's always-OK is 9/15 (F15). But C1's counter is gameable by a label reader
   (F10), and C2's gate is a silent no-op under the host config (F2) and accepts deleted receipts
   (F3) — so the "do-nothing cannot reach" test passes on paper while the real use fails.
4. **C2 operability or calibration; is 2/2 overfit.** Operability by surface, calibration by effect
   (F12); 2/2 is hand-picked from the motivating pair — the population of record commits since r80
   shows 4 defective commits, two not routed by any spot-check (F4). The honest population is that
   commit range labelled by receipt first-appearance, not by the check itself.
5. **Causal separability.** The mechanisms are separable: C1 touches `tools/mado-portals.py` + its
   counter, C2 `quality/check-receipt-presence.py` + its counter; neither counter reads the other's
   file. The shared records commit carries both receipts but is not a logical dependency. The real
   separability risk is axis-level, not file-level: if C1 is relabelled operability, both claims sit
   on one axis and AXES counts them as one (F11).
6. **Named limits hiding a real gap.** C2 has no limits (F13); C1's omit the oracle parse/binary
   pin and the UseIn class while it is unfixed (F1/F8/F9). The "resolver answers what configuration
   selects, not whether a backend runs" limit is correct and should stay.
7. **§2b.** The census start is green and M90-1 is already mined with a fail-able fix, but the
   declaration is silent on both and no SOURCES row was opened this round; C1 is the natural sourced
   claim for the 1.22.1 tarball and the portals.conf/GLib sources (F14).

## DRAFT runs (all labelled DRAFT; no receipt written)

| Run | Command (abridged) | Output | rc |
|---|---|---|---|
| C1 counter, draft tool | `c1-r90-portal-routing.py --draft-tool build/mado-portals.c1.py …` | `DRAFT_TARGET_MET cases=92 correct=92 mutants=31 killed=31 r12=20 host=10 base=0` | 3 |
| C2 counter, draft check | `c2-r90-receipt-presence.py --draft-check build/check-receipt-presence.c2.py …` | `DRAFT_TARGET_MET expectations=15 met=15 defects_detected=2/2 mutants=13 killed=13 always_ok=7/15 always_missing=0/15` | 3 |
| C1 selftest | `mado-portals.c1.py --selftest` | `MADO_PORTALS_SELFTEST: checks=19 failed=0` | 0 |
| Oracle, space source | `portal-oracle-r90.py --cases cases-space.json` | `sp01-space-source []`, `sp02-plain ['mybackend']` | 0 |
| Oracle, invalid UseIn | `portal-oracle-r90.py --cases cases.json` | both `FileChooser=['my'] (default config)`; candidate `[] (no-backend)` | 0 |
| C2, host git config | check `--worktree` in fixture | `records=0 … verdict=OK` (real config); `records=1` with prefixes pinned | 0 |
| C2, deleted receipt | check `--worktree` then `--rev` post-commit | worktree `present=1 OK`; post-commit `missing`, rc 1 | 0 / 1 |
| C2, population | check `--rev` over 24 record commits | MISSING at `498855cb`, `51bf076f`, `942365c8` (4 distinct), `01be4234` (2 distinct) | — |
| Smart always-OK | copy of the counter with `cited=99` | `always_ok_met=9/15` | 3 |
| Census start | `receipts/census-start-r90.txt` (lane) | `mado ok … rc=0` | 0 |
| Oracle binary pin | labelled file vs fresh oracle run | both `e1429fbe1bf6c220…` | — |

## Not verified / limits of this review

I did not run the lane's counters at a committed C1/C2 revision (none exists pre-freeze), did not
execute the oracle against the user's session bus, did not read the binary or credentials, and did
not run the blind set (absent). The C2 population run used the 24 record-touching commits from r85–r89
that I sampled; the reviewer seat has the full `--since=2026-11-04` command. The 9/15 smart-forgery
number is measured with a scratch copy of the counter, not with the frozen counter.

**Scratch:** `S=/fast/scratch/hyaku/mado-r90/R90MCritic` removed on exit; fixture commits used
`fixture <fixture@invalid>` only inside `$S` and `git -C` toplevel was asserted before the first
commit.
