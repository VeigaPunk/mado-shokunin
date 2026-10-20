# GateFreshJj — walker 2.17.2 with a narrowed PASS, jj tip reading gated on `.jj` **and tree equality**, `.git`-file repository test; gate 452/452 + `--regression` PASS at PIN_MADO `f03e6cab…`

Seat: `MadoR19.GateFreshJj`. Date: 2026-10-20. Sole writer this wave of
`tools/mado-verify.sh`. Corrections applied: wave 1 (CriticC2 option 2 +
CriticHonesty) and wave 2 (CriticC2W2 F5/F6/F7/F9, CriticAdmission §3,
SentinelGatePath F-2). Baseline: lane `17661e0…`, gate `c9fb0cef…`, 3,785 L.
Final: `071d39d99aa94d9e3d0c0a8c9d9e9e98b4bc79b51af0703e4dba774f85f7c75d`,
4,160 L / 205,857 B.

## 1. Pins and claim status (this file is one of C2's 13 denominator files)

`git show 9c54c56:tools/mado-verify.sh | grep -c 2.17.0` → `4`, so `tools/`
membership in the freshness denominator is confirmed.

| # | anchor (final file) | before | after |
|---|---|---|---|
| 1 | header `walker`, `:53-62` | `version pin 2.17.0 (MADO-R3-1 §1/§6).` | `version pin 2.17.2 (S096 host rodata + S090 pacman.log:2929; round-19 re-pin)`; the PASS "certifies one thing only: the installed binary prints the pin", and the 2.17.0-era measurements "stay dated"; **F7** names the file: "the 298 L packaged default config (/etc/xdg/walker/config.toml)" |
| 2 | header `pins`, `:65-71` | `walker 2.17.0` … `(SKILL.md "Version pins")` | **F6**: SKILL.md attribution limited to Hyprland/waybar; walker cited to `S096`/`S090`, with "SKILL.md:23 keeps the measured 2.17.0 deliberately, so it is not the walker pin source"; "A held pin is not a claim refresh" |
| 3 | constant comment, `:105-106` | "the old pin failed every live run from that transaction onward" | **F5**: "would FAIL a live run from that transaction onward ([INFERENCE]; no live gate receipt exists after round 12)" |
| 4 | live row (`WALKER_VERSION_PIN` `:108`, `walker_live_rows` `:3342-3366`) | `[ "$kv" = "2.17.0" ]` … `PASS "2.17.0 (pin matches)"` | `2.17.2` compared; PASS `2.17.2 (installed version matches pin; claims measured on 2.17.0 2026-10-14 stay dated — walker-route-r18.md, S096)` |
| 5 | PIN_MADO, `:2004` | `20714096e1481e92c8f75414968b596b5b7c31cc684c1dd94b9c3edb0f772744` | `f03e6cabc8d8f129c4b801ee0234c4b0340ecac224d8b641f4cdae51c13a24a5` |

Source evidence for the re-pin (file bytes only, no command executed):
`/var/log/pacman.log:2929` — `[2026-10-20T09:16:46-0300] [ALPM] upgraded walker
(2.17.0-1 -> 2.17.2-1)`; `/usr/bin/walker` 7,039,912 B, sha256
`25240650686fe6adf0e945530f6e701f5b67535f3e8f9187b08f022317d93096`, one
compiled-in `2.17.2` literal.

Freshness predicate (the counter's own regex) against the working tree — every
line holds `2.17.2` **and** an `S###` token:

```
56:#             version pin 2.17.2 (S096 host rodata + S090 pacman.log:2929;
67:#             "Version pins"); walker 2.17.2 (S096 host rodata + S090
104:# compiled-in `2.17.2` literal (S096, sha256 25240650686f…, 7,039,912 B); the
1305:  st_eq "WL0: pin constant is 2.17.2 (S096 file-byte evidence; not a host read)" \
3338:# prints the 2.17.2 pin (S096 file bytes + S090 pacman.log:2929). The
```

`fresh-pins.py REV` reads committed bytes only, so this file counts as current
only after L1 commits; the post-commit counter value is `[UNK]` here.

## 2. Behaviour

### 2.1 `live.walker.version` / `live.walker.services` (`:3342-3366`, called `:3606`)

Split into `walker_live_rows()` so the selftest drives both pin arms without a
compositor; the `hyprctl`/`HYPRLAND_INSTANCE_SIGNATURE` guard and the two
`systemctl --user is-active` probes are unchanged. **PASS is narrow**: it
certifies that the installed binary prints `2.17.2` (S096 + S090) and nothing
else — the 2026-10-14 claims are named as dated in the same sentence.

### 2.2 `omarchy.git.tag` / `omarchy.git.head` — F6 with two gates (`:3766-3840`)

1. `symbolic-ref -q HEAD` → the branch ref when attached.
2. Detached. The rescue fires only when **both** hold:
   - `$tree/.jj` exists (`:3775-3776`), and
   - `HEAD^{tree}` == `<branch>^{tree}` (`:3795-3799`) — i.e. HEAD is an *empty*
     working-copy commit on top of the single `refs/heads` tip.
3. Otherwise the row reads **HEAD** (`tipref="HEAD"`, `:3810`), the
   pre-round-19 behaviour → `MOVED` on a detached HEAD off the pin. This covers
   plain git **and** `jj new v3.8.3` with the bookmark still at the pin
   (CriticAdmission §3): a non-empty working-copy commit is never rescued.
4. Zero or many branch tips → UNKNOWN naming the ambiguity; an unresolvable ref
   → UNKNOWN naming ref and rc; `describe` failure → tag UNKNOWN.
   PASS details name what was read (`… exactly at refs/heads/master`).

Live fact check (read-only git verbs, no fetch): `symbolic-ref` →
`refs/heads/master` (rc 0), `rev-parse --git-dir` → `.git` (rc 0),
`rev-parse --verify refs/heads/master` → `8fcc9d60…`, `describe
--tags --exact-match 8fcc9d60…` → `v3.8.4` (rc 0). HEAD is attached, so the live
behaviour is unchanged: both rows PASS.

### 2.3 Repository test — F9 (`:3726-3742`)

`[ -d "$tree/.git" ]` → `have git && tmo git -C "$tree" rev-parse --git-dir`,
computed inside the live arm only (a `--no-live` run spawns no git). A worktree
`.git` FILE is a checkout; a tree git does not call a repository reads UNKNOWN
`no git checkout at …`.

## 3. Regression re-cut (PIN_MADO)

Measured, not blessed: the mode printed SETUP with the derived-target mismatch
and the exact re-cut command, which was run verbatim (harness read-only; its
suite is `--selftest`):

```
REGRESSION_TARGET: … sha256=f03e6cabc8d8f129c4b801ee0234c4b0340ecac224d8b641f4cdae51c13a24a5 (recorded pin 05aea198…; match=no)
REGRESSION_RECUT: bash …/mutate-and-run.sh --target /tmp/mado-verify-regression.oeJssm/target.mado-verify.sh --defects …/mado-verify.defects.spec --suite 'bash "$MUTANT" --selftest' --workdir /tmp/mado-verify-regression.oeJssm/recut --label mado-verify.sh
MADO_REGRESSION: SETUP (target pin mismatch — the gate moved outside the MADO-R7 blocks; re-cut, then update PIN_MADO/TABLE_MADO)
```

Sweep (harness `fb6d86d5…`, recorded revision `b56c6e57…` — provenance, not
gated; SPEC_SHA `c7ee75b9…` matched):

```
MADO_SELFTEST: 347/347 assertions passed            (CONTROL, GREEN)
MUTATE_TARGET: … sha256=f03e6cab… bytes=142162
MUTATE_RESTORE: OK (before=f03e6cab… after=f03e6cab… pristine-sha256=f03e6cab…)
MUTATE: DONE (target=mado-verify.sh defects=10 killed=10 survived=0 inconclusive=0 kill-rate=100%)
```

Table (results.tsv, durations dropped): D1 KILLED 2 · D2 KILLED 2 · D3 KILLED 2
· D4 KILLED 2 · D5 KILLED 1 · D6 KILLED 2 · D7 KILLED 2 · D8 KILLED 2 · D9
KILLED 2 · R1 KILLED 2 — 10/10, 0 survived, 0 inconclusive.

Derived target: **2,804 L / 142,162 B / `f03e6cab…`**. `TABLE_MADO` unchanged;
`PIN_MADO` `20714096…` → `05aea198…` → **`f03e6cab…`** (two measured cuts this
wave; the second covers the wave-2 corrections). Record in-file `:1961-1991`.

Post-pin confirmation (exit 0):

```
REGRESSION_TARGET: … sha256=f03e6cab… (recorded pin f03e6cab…; match=yes)
REGRESSION_TABLE mado-verify-hardened: match=10/10 … flips=0
REGRESSION_CASE mado-verify-hardened: PASS (… control=green restore=ok)
MADO_REGRESSION: PASS (case=mado-verify-hardened; target=f03e6cab…)
```

## 4. Red-before (hermetic, `/tmp/mado-r19-red/redbefore3.sh`)

Replaced PATH only (`env -i PATH=<stub bin>` with stubs + coreutils symlinks);
no compositor, no user bus, none of `walker`/`omarchy`/`hyprctl`/`systemctl`/`git`
resolving to a host binary. The stub models a repository (HEAD, `refs/heads`
tip, per-ref trees). Gates: **OLD** `17661e0`, **PREV** `634dfedd…` (wave-1 cut:
unconditional rescue, no tree gate), **NEW** the final gate.

```
=== OLD (17661e0)  jj, HEAD detached on the empty WC commit
omarchy   omarchy.git.tag                 UNKNOWN git describe failed (rc=128) — tag pin unverified
omarchy   omarchy.git.head                FAIL    MOVED: rev-parse HEAD → '8d286c97f829cd575362639c2f63129df10b7a94' != pin 8fcc9d60…
=== NEW (final)    jj, HEAD detached on the empty WC commit (trees equal)
omarchy   omarchy.git.tag                 PASS    HELD: v3.8.4 exactly at refs/heads/master (P3 pin)
omarchy   omarchy.git.head                PASS    HELD: 8fcc9d60 at refs/heads/master (P3 pin)
=== PREV (634dfedd, no tree gate) jj, HEAD tree DIFFERS from the tip
omarchy   omarchy.git.tag                 UNKNOWN git describe failed (rc=128) — tag pin unverified
omarchy   omarchy.git.head                PASS    HELD: 8fcc9d60 at refs/heads/master (P3 pin)
=== NEW (final)    jj, HEAD tree DIFFERS from the tip
omarchy   omarchy.git.tag                 UNKNOWN git describe failed (rc=128) — tag pin unverified
omarchy   omarchy.git.head                FAIL    MOVED: HEAD → '2222222222222222222222222222222222222222' != pin 8fcc9d60…
=== PREV (634dfedd, no tree gate) plain git, HEAD detached off the pin
omarchy   omarchy.git.head                PASS    HELD: 8fcc9d60 at refs/heads/master (P3 pin)
=== NEW (final)    plain git, HEAD detached off the pin
omarchy   omarchy.git.head                FAIL    MOVED: HEAD → '1111111111111111111111111111111111111111' != pin 8fcc9d60…
=== OLD (17661e0)  worktree, .git is a FILE (attached)
omarchy   omarchy.git.tag/head            UNKNOWN no git checkout at …/root-file/.local/share/omarchy
=== NEW (final)    worktree, .git is a FILE (attached)
omarchy   omarchy.git.tag/head            PASS    HELD: … at refs/heads/master (P3 pin)
```

`live.walker.version` in each run: OLD `FAIL pin changed: '2.17.2'`, PREV `PASS
2.17.2 (pin matches; S096)`, NEW `PASS 2.17.2 (installed version matches pin;
claims measured on 2.17.0 2026-10-14 stay dated — walker-route-r18.md, S096)`;
`live.walker.services` PASS everywhere. All runs exit 1 for unrelated rows (the
fixture root has no `~/.config`); no other row is claimed.

Corrections demonstrated: **F6/every rescue hole** — both PREV runs rescue a
detached HEAD it must not (plain git; non-empty jj working copy), the final gate
reports `MOVED: HEAD` and only rescues the empty-commit case; **F9** — blinded →
evaluated.

## 5. Selftest (389 → 452 assertions, hermetic)

`bash tools/mado-verify.sh --selftest` → `MADO_SELFTEST: 452/452 assertions
passed`, rc 0 (the `17661e0` gate measures `389/389`).

| scenario | anchors | what it pins |
|---|---|---|
| OM1 (+2) | `:777-780` | `live.plane UNKNOWN` with `hyprctl not on PATH` — SentinelGatePath F-2: a PATH prepend that reached the host would not read UNKNOWN |
| WL0 | `:1305-1306` | "pin constant is 2.17.2 (S096 file-byte evidence; not a host read)" |
| WL1 | `:1308-1321` | 2.17.2 stub → PASS; detail says `installed version matches pin` and `claims measured on 2.17.0 2026-10-14 stay dated`; never `claims re-verified`; **F9** the omitted old-pin check now lives here — `live.walker.version PASS 2.17.2 (` present and `2.17.0 (pin matches)` absent |
| WL2 | `:1323-1333` | stub `2.17.1` → FAIL naming the printed value and the new pin |
| WL3 | `:1335-1340` | no `walker` on PATH → FAIL `not on PATH`; services row still runs (the vacuous 2.17.0 check deleted) |
| OM10A | `:893-906` | describe rc=128 with a resolved tip → tag UNKNOWN, head PASS |
| OM10B | `:908-922` | unresolved tip → tag+head UNKNOWN naming ref and rc, no MOVED |
| OM11 | `:924-946` | `.jj` + detached HEAD on `8d286c97…` **with equal trees** → both PASS at `refs/heads/master`, detached sha absent |
| OM12 | `:948-968` | `.git` as a FILE → rows evaluate |
| OM13 | `:969-980` | `rev-parse --git-dir` rc=128 → tag/head/vs_head UNKNOWN |
| OM14 | `:981-993` | `.jj` + two tips → UNKNOWN `2 branch tips` |
| OM15 | `:994-1002` | `.jj` + no branch → UNKNOWN `no branch tip under` |
| OM16 | `:1003-1026` | no `.jj`, detached off the pin → `FAIL MOVED: HEAD` naming the sha, tag UNKNOWN |
| OM17 | `:1027-1050` | `.jj` present but **HEAD tree differs from the tip** → `FAIL MOVED: HEAD` naming the detached sha, tag UNKNOWN, no `at refs/heads/master` (CriticAdmission §3) |

PATH discipline: the WL scenario runs `walker_live_rows` with `PATH="$WLB"`
(replaced, never prepended) and a `systemctl` stub in every arm; the OM scenarios
run children with `PATH="$OMB"`. The git stub gained `symbolic-ref`,
`for-each-ref`, `rev-parse --git-dir`, `rev-parse --verify` (refs/heads → tip,
else HEAD) and `^{tree}` knobs `STUB_GIT_HEAD_TREE`/`STUB_GIT_TIP_TREE`
(`:695-731`); the base omarchy fixture carries `.jj` (`:653-658`).

## Limits

- The live gate was **not run** (host pause). Host PASS on `omarchy.git.tag` /
  `.head` is `[INFERENCE]` from the stub matrix plus the read-only git facts in
  §2.2; `walker --version` was not executed (pin rests on S090 + S096 bytes).
- The jj rescue's tree test uses `rev-parse <ref>^{tree}`; a repository where
  those objects are missing reads as a mismatch and keeps the HEAD reading —
  conservative (can report MOVED, never a false PASS). `[UNK]` whether such a
  layout exists here.
- `omarchy.skill.vs_head` still reads `HEAD:<rel>` (unchanged; an unreadable
  blob is UNKNOWN with rc, never a false "local edit").
- `S096` is cited in-file per the reserved-id contract; its `corpus/SOURCES.md`
  row is L1's.
- `fresh-pins.py` cannot see an uncommitted change; the post-commit counter
  value is expected, not measured here.

## Installs

none.
