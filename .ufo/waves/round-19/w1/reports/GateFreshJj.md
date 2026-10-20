# GateFreshJj — walker 2.17.2 with a narrowed PASS, jj tip reading gated on `.jj` + tree equality, and a checkout test that cannot walk up; gate 460/460 + `--regression` PASS at PIN_MADO `367ff5ec…`

Seat: `MadoR19.GateFreshJj`. Date: 2026-10-20. Sole writer this wave of
`tools/mado-verify.sh`. Corrections applied: wave 1 (CriticC2 option 2 +
CriticHonesty), wave 2 (CriticC2W2 F5/F6/F7/F9, CriticAdmission §3,
SentinelGatePath F-2) and the last item (ReviewJjFinal: no walk-up adoption).
Baseline: lane `17661e0…`, gate `c9fb0cef…`, 3,785 L.
Final: `050efc720599345a73bdce6c1d13d50eadeee9769c2ece02462223d0156703f1`,
4,194 L / 208,124 B.

## 1. Pins and claim status (this file is one of C2's 13 denominator files)

`git show 9c54c56:tools/mado-verify.sh | grep -c 2.17.0` → `4`, so `tools/`
membership in the freshness denominator is confirmed.

| # | anchor (final file) | before | after |
|---|---|---|---|
| 1 | header `walker`, `:53-62` | `version pin 2.17.0 (MADO-R3-1 §1/§6).` | `version pin 2.17.2 (S096 host rodata + S090 pacman.log:2929; round-19 re-pin)`; the PASS "certifies one thing only: the installed binary prints the pin"; the 2.17.0-era measurements "stay dated"; **F7** names the file: "the 298 L packaged default config (/etc/xdg/walker/config.toml)" |
| 2 | header `pins`, `:65-71` | `walker 2.17.0` … `(SKILL.md "Version pins")` | **F6**: SKILL.md attribution limited to Hyprland/waybar; walker cited to `S096`/`S090`, with "SKILL.md:23 keeps the measured 2.17.0 deliberately, so it is not the walker pin source"; "A held pin is not a claim refresh" |
| 3 | constant comment, `:105-106` | "the old pin failed every live run from that transaction onward" | **F5**: "would FAIL a live run from that transaction onward ([INFERENCE]; no live gate receipt exists after round 12)" |
| 4 | live row (`WALKER_VERSION_PIN` `:108`, `walker_live_rows` `:3368-3392`) | `[ "$kv" = "2.17.0" ]` … `PASS "2.17.0 (pin matches)"` | `2.17.2` compared; PASS `2.17.2 (installed version matches pin; claims measured on 2.17.0 2026-10-14 stay dated — walker-route-r18.md, S096)` |
| 5 | PIN_MADO, `:2030` | `20714096e1481e92c8f75414968b596b5b7c31cc684c1dd94b9c3edb0f772744` | `367ff5ec9613701a6bbd90979edcfdd229d9440b824f7edc0a4bfd8d8b784f9e` |

Source evidence for the re-pin (file bytes only, no command executed):
`/var/log/pacman.log:2929` — `[2026-10-20T09:16:46-0300] [ALPM] upgraded walker
(2.17.0-1 -> 2.17.2-1)`; `/usr/bin/walker` 7,039,912 B, sha256
`25240650686fe6adf0e945530f6e701f5b67535f3e8f9187b08f022317d93096`, one
compiled-in `2.17.2` literal.

Freshness predicate (the counter's own regex) — every line holds `2.17.2`
**and** an `S###` token:

```
56:#             version pin 2.17.2 (S096 host rodata + S090 pacman.log:2929;
67:#             "Version pins"); walker 2.17.2 (S096 host rodata + S090
104:# compiled-in `2.17.2` literal (S096, sha256 25240650686f…, 7,039,912 B); the
1329:  st_eq "WL0: pin constant is 2.17.2 (S096 file-byte evidence; not a host read)" \
3364:# prints the 2.17.2 pin (S096 file bytes + S090 pacman.log:2929). The
```

`fresh-pins.py REV` reads committed bytes only, so this file counts as current
only after L1 commits; the post-commit counter value is `[UNK]` here.

## 2. Behaviour

### 2.1 `live.walker.version` / `live.walker.services` (`:3368-3392`, called `:3632`)

Split into `walker_live_rows()` so the selftest drives both pin arms without a
compositor; the `hyprctl`/`HYPRLAND_INSTANCE_SIGNATURE` guard and the two
`systemctl --user is-active` probes are unchanged. **PASS is narrow**: it
certifies that the installed binary prints `2.17.2` (S096 + S090) and nothing
else — the 2026-10-14 claims are named as dated in the same sentence.

### 2.2 `omarchy.git.tag` / `omarchy.git.head` — F6 with three gates (`:3764-3874`)

1. `symbolic-ref -q HEAD` → the branch ref when attached.
2. Detached. The rescue fires only when **all** of these hold:
   - the checkout is this tree's (see §2.3 — a `.git` entry here), and
   - `$tree/.jj` exists (`:3809-3810`), and
   - `HEAD^{tree}` == `<branch>^{tree}` (`:3829-3833`) — HEAD is an *empty*
     working-copy commit on top of the single `refs/heads` tip.
3. Otherwise the row reads **HEAD** (`tipref="HEAD"`, `:3844`): plain git, a
   `jj new v3.8.3` working copy whose tree differs, or a tree with no checkout
   at all → `MOVED` / UNKNOWN, never a PASS read from a branch nobody checked
   out.
4. Zero or many branch tips → UNKNOWN naming the ambiguity; an unresolvable ref
   → UNKNOWN naming ref and rc; `describe` failure → tag UNKNOWN. PASS details
   name what was read (`… exactly at refs/heads/master`).

Live fact check (read-only git verbs, no fetch): `symbolic-ref` →
`refs/heads/master` (rc 0), `rev-parse --git-dir` → `.git` (rc 0),
`rev-parse --verify refs/heads/master` → `8fcc9d60…`, `describe
--tags --exact-match 8fcc9d60…` → `v3.8.4` (rc 0). HEAD is attached, so the live
behaviour is unchanged: both rows PASS.

### 2.3 Repository test — F9, no walk-up (`:3752-3775`)

`[ -d "$tree/.git" ]` → **`[ -e "$tree/.git" ]` plus `rev-parse --git-dir`**
(`:3773-3775`), inside the live arm only (a `--no-live` run spawns no git):

- a directory passes (colocated / plain checkout);
- a **file** passes (git worktree, F9);
- **no entry → no git call at all** → the old `no git checkout at …` UNKNOWN.
  This closes ReviewJjFinal: `rev-parse --git-dir` walks up, so a .git-less
  omarchy tree under an ancestor repository (e.g. `~/.git`, dotfiles) would
  otherwise be judged as that repository's checkout.

`omarchy.skill.vs_head` inherits the same gate (its guard reuses `omtree`).

## 3. Regression re-cut (PIN_MADO)

Measured, not blessed: the mode printed SETUP with the derived-target mismatch
and the exact re-cut command, which was run verbatim (harness read-only; its
suite is `--selftest`):

```
REGRESSION_TARGET: … sha256=367ff5ec9613701a6bbd90979edcfdd229d9440b824f7edc0a4bfd8d8b784f9e (recorded pin f03e6cab…; match=no)
REGRESSION_RECUT: bash …/mutate-and-run.sh --target /tmp/mado-verify-regression.jeqFvJ/target.mado-verify.sh --defects …/mado-verify.defects.spec --suite 'bash "$MUTANT" --selftest' --workdir /tmp/mado-verify-regression.jeqFvJ/recut --label mado-verify.sh
MADO_REGRESSION: SETUP (target pin mismatch — the gate moved outside the MADO-R7 blocks; re-cut, then update PIN_MADO/TABLE_MADO)
```

Sweep (harness `fb6d86d5…`, recorded revision `b56c6e57…` — provenance, not
gated; SPEC_SHA `c7ee75b9…` matched):

```
MADO_SELFTEST: 355/355 assertions passed            (CONTROL, GREEN)
MUTATE_TARGET: … sha256=367ff5ec… bytes=144260
MUTATE_RESTORE: OK (before=367ff5ec… after=367ff5ec… pristine-sha256=367ff5ec…)
MUTATE: DONE (target=mado-verify.sh defects=10 killed=10 survived=0 inconclusive=0 kill-rate=100%)
```

Table (results.tsv, durations dropped): D1 KILLED 2 · D2 KILLED 2 · D3 KILLED 2
· D4 KILLED 2 · D5 KILLED 1 · D6 KILLED 2 · D7 KILLED 2 · D8 KILLED 2 · D9
KILLED 2 · R1 KILLED 2 — 10/10, 0 survived, 0 inconclusive.

Derived target: **2,836 L / 144,260 B / `367ff5ec…`**. `TABLE_MADO` unchanged;
`PIN_MADO` `20714096…` → `05aea198…` → `f03e6cab…` → **`367ff5ec…`** (three
measured cuts this wave; the last covers the walk-up fix). Record in-file
`:1985-2017`.

Post-pin confirmation (exit 0):

```
REGRESSION_TARGET: … sha256=367ff5ec… (recorded pin 367ff5ec…; match=yes)
REGRESSION_TABLE mado-verify-hardened: match=10/10 … flips=0
REGRESSION_CASE mado-verify-hardened: PASS (… control=green restore=ok)
MADO_REGRESSION: PASS (case=mado-verify-hardened; target=367ff5ec…)
```

## 4. Red-before (hermetic; replaced PATH, no host binary of interest)

Matrices: `/tmp/mado-r19-red/redbefore3.sh` (jj/plain/worktree) and
`redbefore4.sh` (ancestor repo). Gates: **OLD** `17661e0`, **PREV**
`634dfedd…` (wave-1 cut, unconditional rescue), **PREV2** `071d39d9…` (before
the `.git`-entry requirement), **NEW** the final gate.

```
=== OLD (17661e0)  jj, HEAD detached on the empty WC commit
omarchy   omarchy.git.tag                 UNKNOWN git describe failed (rc=128) — tag pin unverified
omarchy   omarchy.git.head                FAIL    MOVED: rev-parse HEAD → '8d286c97f829cd575362639c2f63129df10b7a94' != pin 8fcc9d60…
=== NEW (final)    jj, HEAD detached on the empty WC commit (trees equal)
omarchy   omarchy.git.tag                 PASS    HELD: v3.8.4 exactly at refs/heads/master (P3 pin)
omarchy   omarchy.git.head                PASS    HELD: 8fcc9d60 at refs/heads/master (P3 pin)
=== PREV (634dfedd, no tree gate) jj, HEAD tree DIFFERS from the tip
omarchy   omarchy.git.head                PASS    HELD: 8fcc9d60 at refs/heads/master (P3 pin)
=== NEW (final)    jj, HEAD tree DIFFERS from the tip
omarchy   omarchy.git.head                FAIL    MOVED: HEAD → '2222222222222222222222222222222222222222' != pin 8fcc9d60…
=== PREV (634dfedd, no tree gate) plain git, HEAD detached off the pin
omarchy   omarchy.git.head                PASS    HELD: 8fcc9d60 at refs/heads/master (P3 pin)
=== NEW (final)    plain git, HEAD detached off the pin
omarchy   omarchy.git.head                FAIL    MOVED: HEAD → '1111111111111111111111111111111111111111' != pin 8fcc9d60…
=== OLD (17661e0)  worktree, .git is a FILE (attached)
omarchy   omarchy.git.tag/head            UNKNOWN no git checkout at …/root-file/.local/share/omarchy
=== NEW (final)    worktree, .git is a FILE (attached)
omarchy   omarchy.git.tag/head            PASS    HELD: … at refs/heads/master (P3 pin)
=== PREV2 (071d39d9, walk-up precondition) .git-less tree under an ancestor repo
omarchy   omarchy.git.tag                 PASS    HELD: v3.8.4 exactly at refs/heads/master (P3 pin)
omarchy   omarchy.git.head                PASS    HELD: 8fcc9d60 at refs/heads/master (P3 pin)
=== NEW (final)    .git-less tree under an ancestor repo
omarchy   omarchy.git.tag                 UNKNOWN no git checkout at …/root-no-git/.local/share/omarchy
omarchy   omarchy.git.head                UNKNOWN no git checkout at …/root-no-git/.local/share/omarchy
```

`live.walker.version`: OLD `FAIL pin changed: '2.17.2'`; PREV/`PREV2` `PASS
2.17.2 (pin matches; S096)`; NEW `PASS 2.17.2 (installed version matches pin;
claims measured on 2.17.0 2026-10-14 stay dated — walker-route-r18.md, S096)`.
`live.walker.services` PASS everywhere. All runs exit 1 for unrelated rows (the
fixture root has no `~/.config`); no other row is claimed.

## 5. Selftest (389 → 460 assertions, hermetic)

`bash tools/mado-verify.sh --selftest` → `MADO_SELFTEST: 460/460 assertions
passed`, rc 0 (the `17661e0` gate measures `389/389`).

| scenario | anchors | what it pins |
|---|---|---|
| OM1 (+2) | `:777-780` | `live.plane UNKNOWN` with `hyprctl not on PATH` — SentinelGatePath F-2: a PATH prepend that reached the host would not read UNKNOWN |
| WL0 | `:1329-1330` | "pin constant is 2.17.2 (S096 file-byte evidence; not a host read)" |
| WL1 | `:1332-1345` | 2.17.2 stub → PASS; detail says `installed version matches pin` and `claims measured on 2.17.0 2026-10-14 stay dated`; never `claims re-verified`; **F9** the old-pin check lives here — `live.walker.version PASS 2.17.2 (` present, `2.17.0 (pin matches)` absent |
| WL2 | `:1347-1357` | stub `2.17.1` → FAIL naming the printed value and the new pin |
| WL3 | `:1359-1365` | no `walker` on PATH → FAIL `not on PATH`; services row still runs (the vacuous 2.17.0 check deleted) |
| OM10A | `:893-906` | describe rc=128 with a resolved tip → tag UNKNOWN, head PASS |
| OM10B | `:908-922` | unresolved tip → tag+head UNKNOWN naming ref and rc, no MOVED |
| OM11 | `:924-946` | `.jj` + detached HEAD on `8d286c97…` **with equal trees** → both PASS at `refs/heads/master` |
| OM12 | `:948-968` | `.git` as a FILE → rows evaluate (worktree) |
| OM13 | `:969-980` | `rev-parse --git-dir` rc=128 (with `.git` present) → tag/head/vs_head UNKNOWN |
| OM14 | `:981-993` | `.jj` + two tips → UNKNOWN `2 branch tips` |
| OM15 | `:994-1002` | `.jj` + no branch → UNKNOWN `no branch tip under` |
| OM16 | `:1003-1026` | no `.jj`, detached off the pin → `FAIL MOVED: HEAD`, tag UNKNOWN |
| OM17 | `:1027-1051` | `.jj` but **HEAD tree differs from the tip** → `FAIL MOVED: HEAD`, no `at refs/heads/master` (CriticAdmission §3) |
| OM18 | `:1052-1074` | **no `.git`, no `.jj`**, ancestor repo would answer `--git-dir` rc 0 → tag/head/vs_head UNKNOWN `no git checkout at …`, no PASS, no `MOVED: refs/heads` (ReviewJjFinal) |

PATH discipline: `walker_live_rows` runs with `PATH="$WLB"` (replaced, never
prepended) and a `systemctl` stub in every arm; the OM scenarios run children
with `PATH="$OMB"`. The git stub gained `symbolic-ref`, `for-each-ref`,
`rev-parse --git-dir`, `rev-parse --verify` (refs/heads → tip, else HEAD) and
`^{tree}` knobs `STUB_GIT_HEAD_TREE`/`STUB_GIT_TIP_TREE` (`:695-731`); the base
omarchy fixture carries `.jj` (`:653-658`).

## Limits

- The live gate was **not run** (host pause). Host PASS on `omarchy.git.tag` /
  `.head` is `[INFERENCE]` from the stub matrices plus the read-only git facts in
  §2.2; `walker --version` was not executed (pin rests on S090 + S096 bytes).
- The checkout test requires a `.git` entry **inside** the tree. A checkout
  driven by `GIT_DIR`/`--git-dir` from outside (no entry in the tree) now reads
  UNKNOWN instead of evaluating — conservative by design, and the host's omarchy
  tree has `.git` (verified as bytes). `[UNK]` whether any other layout exists.
- The jj tree test uses `rev-parse <ref>^{tree}`; a repository where those
  objects are missing reads as a mismatch and keeps the HEAD reading —
  conservative (MOVED, never a false PASS).
- `omarchy.skill.vs_head` still reads `HEAD:<rel>` (unchanged; an unreadable
  blob is UNKNOWN with rc, never a false "local edit").
- `S096` is cited in-file per the reserved-id contract; its `corpus/SOURCES.md`
  row is L1's.
- `fresh-pins.py` cannot see an uncommitted change; the post-commit counter
  value is expected, not measured here.

## Installs

none.
