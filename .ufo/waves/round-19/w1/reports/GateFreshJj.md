# GateFreshJj — walker 2.17.2 with a narrowed PASS, jj-gated tip reading (F6) and a `.git`-file repository test (F9); gate 443/443 + `--regression` PASS at PIN_MADO `05aea198…`

Seat: `MadoR19.GateFreshJj`. Date: 2026-10-20. Sole writer this wave of
`tools/mado-verify.sh`. Corrections applied: L1 follow-up (CriticC2 option 2 +
CriticHonesty). Baseline: lane HEAD `17661e0fa83f978fb659f5bb8fef47f0969f6945`,
gate `c9fb0cef3e081dc878d69f8e20c148429bdfbdce949f8afaed705db957ea42b5`, 3,785 L.
Final: `1036d1004e63d80377faa4f905fd8dc1897eb29b64496cbfef647b47cec4f2af`,
4,097 L / 201,649 B.

## 1. Pins and claim status (this file is one of C2's 13 denominator files)

`git show 9c54c56:tools/mado-verify.sh | grep -c 2.17.0` → `4` (lines 56, 60, 3277,
3278), so `tools/` membership in the freshness denominator is confirmed.

| # | anchor (final file) | before | after |
|---|---|---|---|
| 1 | header `walker`, `:53-61` | `version pin 2.17.0 (MADO-R3-1 §1/§6).` | `version pin 2.17.2 (S096 host rodata + S090 pacman.log:2929; round-19 re-pin)` + "the version row's PASS certifies one thing only: the installed binary prints the pin… the 2.17.0-era measurements (MADO-R3-1 §1/§6, e.g. the 298 L packaged help table, probe window 2026-10-14) stay dated and are routed by walker-route-r18.md" |
| 2 | header `pins`, `:65-69` | `walker 2.17.0` | `walker 2.17.2` with S096/S090 named in the paragraph, and "A held pin is not a claim refresh: the 2.17.0-era walker measurements stay dated." (the pointer line is `:56`) |
| 3 | live row (`WALKER_VERSION_PIN` `:105`, `walker_live_rows` `:3289-3313`) | `[ "$kv" = "2.17.0" ]` … `PASS "2.17.0 (pin matches)"` | `2.17.2` compared; PASS text `2.17.2 (installed version matches pin; claims measured on 2.17.0 2026-10-14 stay dated — walker-route-r18.md, S096)` |
| 4 | PIN_MADO, `:1951` | `20714096e1481e92c8f75414968b596b5b7c31cc684c1dd94b9c3edb0f772744` | `05aea198a2084ea1fd87825fd6183e5afd9a2d95f8cc06476efcaa7e0af6cca0` |

Source evidence for the re-pin (file bytes only, no command executed):

- `/var/log/pacman.log:2929` — `[2026-10-20T09:16:46-0300] [ALPM] upgraded walker (2.17.0-1 -> 2.17.2-1)`.
- `/usr/bin/walker` — 7,039,912 B, sha256 `25240650686fe6adf0e945530f6e701f5b67535f3e8f9187b08f022317d93096`;
  `grep -a -c '2\.17\.2'` → `1` (compiled-in version literal).

Freshness predicate, run against the working tree with the counter's own regex
(`grep -nE '2\.17\.2.*\bS[0-9]{3}\b|\bS[0-9]{3}\b.*2\.17\.2' tools/mado-verify.sh`):

```
56:#             version pin 2.17.2 (S096 host rodata + S090 pacman.log:2929;
101:# compiled-in `2.17.2` literal (S096, sha256 25240650686f…, 7,039,912 B); the
1258:  st_eq "WL0: pin constant is 2.17.2 (S096 file-byte evidence; not a host read)" \
1920:# too. `live.walker.version` moved 2.17.0 → 2.17.2 (S096 host rodata + S090
3285:# prints the 2.17.2 pin (S096 file bytes + S090 pacman.log:2929). The
```

`fresh-pins.py REV` reads committed bytes only (`git show REV:path`), so this file
counts as current only after L1 commits the wave; I did not (and must not) create a
commit. `[UNK]` the post-commit counter value.

## 2. Behaviour

### 2.1 `live.walker.version` / `live.walker.services` (`:3289-3313`, called at `:3553-3556`)

The two rows live in `walker_live_rows()`, split out of `live_plane` so the selftest
can drive both pin arms without a compositor; the `hyprctl` /
`HYPRLAND_INSTANCE_SIGNATURE` guard and the two `systemctl --user is-active` probes are
unchanged. **PASS is narrow by construction**: it certifies that the installed binary
prints `2.17.2` (S096 + S090). It does not refresh the claims — MADO-R3-1 §6's 298 L
packaged table and the rest of the 2026-10-14 probe window were measured on 2.17.0 and
stay dated (`walker-route-r18.md` routes the current values). The function doc
(`:3241-3248`) and the call-site comment (`:3553-3555`) say so in place.

### 2.2 `omarchy.git.tag` / `omarchy.git.head` — jj F6, jj-gated (`:3714-3777`)

1. `git -C "$tree" symbolic-ref -q HEAD` → the branch ref when attached.
2. Detached (rc≠0). **Only when `$tree/.jj` exists** (jj colocation, checked at
   `:3722-3723`) does the row fall back to the branch tip:
   `for-each-ref refs/heads`; exactly one → that ref, zero or many → UNKNOWN
   (`HEAD detached and no branch tip under …` / `… and N branch tips — no unambiguous
   pin target`).
3. Otherwise (plain git) the row reads **HEAD**, the pre-round-19 behaviour:
   `tipref="HEAD"`, `rev-parse --verify HEAD`. A detached HEAD off the pin therefore
   reports `MOVED`, never a PASS read from a branch nobody checked out.
4. `rev-parse --verify` failure → UNKNOWN `cannot resolve <ref> (rc=N)`;
   `describe --tags --exact-match "$tip"` and the tip sha are compared to the pins.
   PASS details name what was read: `HELD: v3.8.4 exactly at refs/heads/master (P3
   pin)` / `HELD: 8fcc9d60 at refs/heads/master (P3 pin)`.

Live fact check on the real checkout (read-only git verbs, no fetch): `symbolic-ref` →
`refs/heads/master` (rc 0), `rev-parse --git-dir` → `.git` (rc 0),
`rev-parse --verify refs/heads/master` → `8fcc9d6048af4cb0e3af8512c78049857a3b53dd`,
`describe --tags --exact-match 8fcc9d60…` → `v3.8.4` (rc 0). HEAD is attached, so the
live behaviour is unchanged: both rows PASS.

### 2.3 Repository test — jj F9 (`:3673-3689`)

`[ -d "$tree/.git" ]` → `have git && tmo git -C "$tree" rev-parse --git-dir
>/dev/null 2>&1`, computed inside the live arm only (a `--no-live` run still spawns no
git). A worktree `.git` FILE is now a checkout; a tree git does not call a repository
still reads UNKNOWN `no git checkout at …`.

## 3. Regression re-cut (PIN_MADO)

Measured, not blessed. The mode printed SETUP with the derived-target mismatch and the
exact re-cut command; that command was run verbatim (harness read-only; its suite is
`--selftest`, hermetic):

```
REGRESSION_TARGET: … sha256=05aea198a2084ea1fd87825fd6183e5afd9a2d95f8cc06476efcaa7e0af6cca0 (recorded pin b01414b5…; match=no)
REGRESSION_RECUT: bash /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh --target /tmp/mado-verify-regression.s2eAZz/target.mado-verify.sh --defects /tmp/mado-verify-regression.s2eAZz/mado-verify.defects.spec --suite 'bash "$MUTANT" --selftest' --workdir /tmp/mado-verify-regression.s2eAZz/recut --label mado-verify.sh
MADO_REGRESSION: SETUP (target pin mismatch — the gate moved outside the MADO-R7 blocks; re-cut, then update PIN_MADO/TABLE_MADO)
```

Sweep (harness `fb6d86d59b5c9285864c9ebfa19d5a6f8938e91c47877a6d25b451a1da03001a`,
recorded revision `b56c6e57…` — provenance, not gated; SPEC_SHA `c7ee75b9…` matched):

```
MADO_SELFTEST: 338/338 assertions passed            (CONTROL on the derived target, GREEN)
MUTATE_TARGET: … sha256=05aea198a2084ea1fd87825fd6183e5afd9a2d95f8cc06476efcaa7e0af6cca0 bytes=138328
MUTATE_RESTORE: OK (before=05aea198… after=05aea198… pristine-sha256=05aea198…)
MUTATE: DONE (target=mado-verify.sh defects=10 killed=10 survived=0 inconclusive=0 kill-rate=100%)
```

Measured table (results.tsv, verbatim, durations dropped):

```
D1 KILLED 2 clause A: file-plane CLEAN verdict token renamed (CLEAN -> OK)
D2 KILLED 2 clause B: UNKNOWN guard dropped from the CLEAN test
D3 KILLED 2 clause B: skipped live layer row reports PASS instead of SKIP
D4 KILLED 2 clause C: DIVERGED path exits 0
D5 KILLED 1 clause C: failing --selftest returns 1 not 2
D6 KILLED 2 clause D: xdph dropped from the 12-conf local inventory
D7 KILLED 2 clause D: include-graph count test -ne -> -lt (extra source lines tolerated)
D8 KILLED 2 clause E: hyprland.conf sha pin comparison always "matches"
D9 KILLED 2 clause E: read-only boundary comparison always reads byte-identical
R1 KILLED 2 clause F: tomllib-unavailable arm reads PASS not UNKNOWN
```

Derived target (gate minus the marked R7/R8 families): **2,745 L / 138,328 B /
`05aea198…`**; 10/10 KILLED, 0 survived, 0 inconclusive, flips 0, control GREEN,
restore OK, target sha unchanged. `TABLE_MADO` unchanged; `PIN_MADO` `20714096…` →
`05aea198…`. Re-cut record in-file at `:1912-1937`.

Post-pin confirmation, same mode (exit 0):

```
REGRESSION_TARGET: … sha256=05aea198… (recorded pin 05aea198…; match=yes)
REGRESSION_TABLE mado-verify-hardened: match=10/10 recorded-killed=10 measured-killed=10 survived=0 inconclusive=0 flips=0
REGRESSION_CASE mado-verify-hardened: PASS (recorded table reproduced: killed=10/10 flips=0 inconclusive=0 control=green restore=ok)
MADO_REGRESSION: PASS (case=mado-verify-hardened; target=05aea198a2084ea1fd87825fd6183e5afd9a2d95f8cc06476efcaa7e0af6cca0)
```

## 4. Red-before (hermetic matrix, `/tmp/mado-r19-red/redbefore2.sh`)

Every probe runs under a **replaced** PATH (`env -i PATH=<stub bin>` holding only stubs
plus coreutils symlinks): no compositor, no user bus, and none of
`walker`/`omarchy`/`hyprctl`/`systemctl`/`git` resolved to a host binary. The stub `git`
models a repository: HEAD = `STUB_GIT_HEAD`, `refs/heads/master` = `STUB_GIT_TIP`
(carrying `v3.8.4`), `describe` of the tip → the tag, of any other commit → rc 128.
Gates: **OLD** = `17661e0` (`c9fb0cef…`), **PREV** = `634dfedd…` (the first round-19
cut, unconditional tip rescue), **NEW** = the final gate (`1036d100…`).

```
=== OLD (17661e0)  jj-colocated, HEAD detached on empty WC commit
hypr-live live.walker.version             FAIL    pin changed: '2.17.2'; re-verify claim anchors
omarchy   omarchy.git.tag                 UNKNOWN git describe failed (rc=128) — tag pin unverified
omarchy   omarchy.git.head                FAIL    MOVED: rev-parse HEAD → '8d286c97f829cd575362639c2f63129df10b7a94' != pin 8fcc9d60… (every pin held at the old HEAD needs re-verification)
=== NEW (final)    jj-colocated, HEAD detached on empty WC commit
hypr-live live.walker.version             PASS    2.17.2 (installed version matches pin; claims measured on 2.17.0 2026-10-14 stay dated — walker-route-r18.md, S096)
omarchy   omarchy.git.tag                 PASS    HELD: v3.8.4 exactly at refs/heads/master (P3 pin)
omarchy   omarchy.git.head                PASS    HELD: 8fcc9d60 at refs/heads/master (P3 pin)
=== PREV (b01414b5 cut, unconditional rescue) plain git, HEAD detached off the pin
hypr-live live.walker.version             PASS    2.17.2 (pin matches; S096)
omarchy   omarchy.git.tag                 PASS    HELD: v3.8.4 exactly at refs/heads/master (P3 pin)
omarchy   omarchy.git.head                PASS    HELD: 8fcc9d60 at refs/heads/master (P3 pin)
=== NEW (final)    plain git, HEAD detached off the pin
hypr-live live.walker.version             PASS    2.17.2 (installed version matches pin; claims measured on 2.17.0 2026-10-14 stay dated — walker-route-r18.md, S096)
omarchy   omarchy.git.tag                 UNKNOWN git describe failed (rc=128) — tag pin unverified
omarchy   omarchy.git.head                FAIL    MOVED: HEAD → '1111111111111111111111111111111111111111' != pin 8fcc9d60… (every pin held at the old tip needs re-verification)
=== OLD (17661e0)  worktree, .git is a FILE (attached)
omarchy   omarchy.git.tag                 UNKNOWN no git checkout at …/root-file/.local/share/omarchy
omarchy   omarchy.git.head                UNKNOWN no git checkout at …/root-file/.local/share/omarchy
=== NEW (final)    worktree, .git is a FILE (attached)
omarchy   omarchy.git.tag                 PASS    HELD: v3.8.4 exactly at refs/heads/master (P3 pin)
omarchy   omarchy.git.head                PASS    HELD: 8fcc9d60 at refs/heads/master (P3 pin)
```

(`live.walker.services` PASS `app-walker@autostart + elephant active` in every run;
omitted here. Every run exits 1 for unrelated rows — the fixture root carries no
`~/.config` — and no other row is claimed.)

Per correction: **C1** the PASS text now certifies only the installed version and names
the dated claim window; **C3** the hole is demonstrated — PREV passes a plain-git
detached HEAD off the pin by reading a branch tip, the final gate reads `MOVED: HEAD`
and `UNKNOWN`, while the jj case (`.jj` present) still rescues the empty working-copy
commit; **F9** unchanged in direction (blinded → evaluated).

## 5. Selftest (389 → 443 assertions, hermetic)

`bash tools/mado-verify.sh --selftest` → `MADO_SELFTEST: 443/443 assertions passed`,
rc 0 (measured on the final bytes; the `17661e0` gate measures `389/389`).

| scenario | anchors | what it pins |
|---|---|---|
| WL0 | `:1258-1259` | "WL0: pin constant is 2.17.2 (S096 file-byte evidence; not a host read)" |
| WL1 | `:1260-1270` | 2.17.2 stub → version+services PASS; PASS detail says `installed version matches pin` and `claims measured on 2.17.0 2026-10-14 stay dated`; never `claims re-verified` |
| WL2 | `:1272-1282` | stub `2.17.1` → FAIL naming the printed value and the new pin |
| WL3 | `:1284-1290` | no `walker` on PATH → FAIL `not on PATH`, services row still runs, no row text says `2.17.0` |
| OM10A | `:874-887` | describe rc=128 with a resolved tip → tag UNKNOWN, head PASS |
| OM10B | `:889-903` | unresolved tip → tag+head UNKNOWN naming ref and rc, no MOVED |
| OM11 | `:905-925` | `.jj` + detached HEAD on `8d286c97…`, tag at the tip → both PASS naming `refs/heads/master`, zero UNKNOWN, detached sha absent from output |
| OM12 | `:926-946` | `.git` as a FILE (worktree) → rows evaluate, no `no git checkout at` |
| OM13 | `:947-958` | `rev-parse --git-dir` rc=128 → tag/head/vs_head UNKNOWN |
| OM14 | `:959-971` | `.jj` + detached with two tips → UNKNOWN `2 branch tips`, never MOVED |
| OM15 | `:972-980` | `.jj` + detached with no branch → UNKNOWN `no branch tip under` |
| OM16 | `:981-1003` | **no `.jj`** + detached HEAD off the pin → head `FAIL MOVED: HEAD` naming the detached sha, tag UNKNOWN, and neither `at refs/heads/master` nor `tip read from` appears |

PATH discipline (host-pause safe): the WL scenario builds `$T/walker/bin` with a
`walker` + `systemctl` stub and coreutils symlinks and runs `walker_live_rows` with
`PATH="$WLB"` — **replaced, never prepended** — so a missing stub cannot fall through
to `/usr/bin/walker` or `systemctl --user`; `systemctl` is stubbed for every arm. The
git stub gained `symbolic-ref` (`STUB_GIT_DETACHED`), `for-each-ref`
(`STUB_GIT_BRANCHES` / `STUB_GIT_NO_BRANCHES`), `rev-parse --git-dir`
(`STUB_GIT_GITDIR_RC`) and `rev-parse --verify` (`STUB_GIT_TIP`, else
`STUB_GIT_HEAD`), and the base omarchy fixture now carries `.jj` so the jj branch is
the tested default (`:653-658`).

## Limits

- The live gate (`bash tools/mado-verify.sh` with no mode) was **not run** (host pause:
  no `hyprctl`, no `omarchy`, no `systemctl`). Host PASS on `omarchy.git.tag`/`.head`
  is `[INFERENCE]` from the replaced-PATH matrix plus the read-only git facts in §2.2.
- `walker --version` on the host was not executed; the pin rests on the package
  transaction line and the binary's rodata literal (file bytes only).
- The jj-vs-plain discrimination is a `.jj` directory test. A jj repo whose `.jj` lives
  away from the checkout (a worktree of a jj repo) reads as plain git and therefore
  keeps the HEAD reading — conservative (it can report MOVED, never a false PASS).
  `[UNK]` whether such a layout exists on this host.
- `omarchy.skill.vs_head` still reads `HEAD:<rel>`: under a detached *empty*
  working-copy commit whose tree lacks the path it reads UNKNOWN (rc named), never a
  false FAIL — unchanged, out of scope for F6.
- `S096` is cited in-file per the reserved-id contract; its `corpus/SOURCES.md` row is
  L1's (this seat does not write the corpus).
- `fresh-pins.py` cannot see an uncommitted change; the post-commit counter value is
  expected, not measured here.

## Installs

none.
