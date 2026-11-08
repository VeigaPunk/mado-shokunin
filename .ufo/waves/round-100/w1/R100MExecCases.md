# R100MExecCases - the `path-default` case class (round 100, w1)

Seat: executor. Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`, base
`43309e6af9a3b57f1bc839a826bef1f8eb7495e4`, branch `master`. Contract:
`.ufo/waves/round-100/claims-declaration-r100.md` (C1, clauses 1-3 and PRED-C1-r100-v1).
Nothing in `tools/`, `quality/`, `corpus/`, `plans/` was written; no git or jj command ran.

## 1. What landed

| file | sha256 | bytes |
|---|---|---|
| `.ufo/waves/round-100/controls/launchenv-cases-r100.json` | `7aba8a0f880b3e59edf7a731f2d2783babea7b275d280588ba2df2c5dd6df4a9` | 62019 |
| `.ufo/waves/round-100/controls/launchenv-fresh-r100.py` | `18005e07176762ca07b9bb593245d2e0200d53b2a8cbafd8e0fbd3da27c1fc6b` | 10216 |
| `.ufo/waves/round-100/receipts/c1-cases-r100.txt` | `d338bc55833f1490e7ea7749fb61b45eb583d499dbfb2b851a120e026f62b646` | build receipt |
| `.ufo/waves/round-100/receipts/c1-cases-remeasure-r100.txt` | `9d3e2dc6c000ccc939789397b6a2904f50417d8e4d8e14a7421701bbe3e887a0` | re-measure receipt |

Instrument vs candidate: the case file, the generator and both receipts are **instruments** - they
spawn `/usr/bin/gio` (via the r99 oracle module) and, for the two agreement legs, the committed
candidate `tools/mado-launchenv.py` (which itself spawns nothing). No candidate code was written or
changed by this seat.

## 2. Census

```
cases   r99 67 -> r100 77      (+10, all new ones reach the unset-PATH default)
classes r99 31 -> r100 35      (+path-default-cwd, -dot, -private, -sysbin)
path-default cases 10, of which path null or [] : 8   (null 5, [] 3)
  path-default-dot      2   pd-dot-root (null)                pd-empty-root ([])
  path-default-private  3   pd-private-unset (null)           pd-private-onpath [{root}/bin]
                            pd-private-unset-wd (null, Path={root}/work)
  path-default-sysbin   3   pd-sysbin-unset (null)            pd-sysbin-empty ([])
                            pd-sysbin-private [{root}/bin]
  path-default-cwd      2   pd-wd-unset (null)                pd-wd-empty ([])
```

Every one of the 67 r99 cases is **byte-identical** in the new file: the builder re-renders each
case block at its own nesting depth and requires it to appear verbatim in both files (67 checked,
0 failures), and the whole r99 document re-serialises to its own committed bytes (53148 bytes,
identical) under the same renderer. Envelope: `version 1`, `round r100`, `oracle R99MExecOracle`,
`probe_module .ufo/waves/round-99/controls/launchenv-probe-r99.py`,
`oracle_sha256 = renderer_sha256 = cbfff7a4...d129199` (re-hashed this run),
`gio_path /usr/bin/gio`, `gio_sha256 d2164260...cfc462`, `glib2 2.90.1-1`. The four new class names
are appended to `classes`; `schema_notes.path` was rewritten (the r99 text claimed the path-unset
cases carry an absolute `Exec`, which is exactly what this round removes) and a `path_default` note
records the two host facts the class depends on.

## 3. The two measurements

Both are in `receipts/c1-cases-r100.txt` (build) and `receipts/c1-cases-remeasure-r100.txt`
(independent, reads the **committed file**, never the builder's shapes). Every case was measured
twice; `agreed: true` on every run in both passes, and every frozen label was reproduced by the
second pass (`remeasured=10 agree_with_frozen=10 fail=0`).

| case | path | measured label (2 runs, agreeing) |
|---|---|---|
| pd-dot-root | null | launches=1 `argv[0]={root}/./probe` |
| pd-empty-root | `[]` | launches=1 `argv[0]={root}/probe` |
| pd-private-unset | null | `{"error":"load"}` rc=1, records=0 |
| pd-private-onpath | `["{root}/bin"]` | launches=1 `argv[0]={root}/bin/probe` |
| pd-private-unset-wd | null + `Path={root}/work` | `{"error":"load"}` rc=1 |
| pd-sysbin-unset | null | launches=1 `argv[0]={probe}` |
| pd-sysbin-empty | `[]` | `{"error":"load"}` rc=1 |
| pd-sysbin-private | `["{root}/bin"]` | `{"error":"load"}` rc=1 |
| pd-wd-unset | null + `Path={root}/work` | launches=1 `argv[0]={root}/work/probe` |
| pd-wd-empty | `[]` + `Path={root}/work` | launches=1 `argv[0]={root}/work/probe` |

No case was undecided: every measurement was `agreed: true` and none returned `setup-error`.
`[]` and `[""]` were measured to be the same environment and the same label, so the declaration's
`[]` spelling is safe alongside the r99 `[""]` spelling.

## 4. How the class separates the three behaviours - and where clause 3 does not hold

**Clause 1 (unset != empty).** Two independent separations, both measured:
(a) `pd-sysbin-unset` vs `pd-sysbin-empty`: `TryExec=sh`, `Exec={root}/probe.sh`, PATH absent ->
`launches=1 argv[0]={probe}`; PATH `[]` -> `{"error":"load"}`. This is the declaration's sentence
literally - a program that exists only in `/usr/bin` (`/bin` is a symlink to `/usr/bin` here) is
reachable with PATH absent and not with `PATH=""` - and it is **causal** (found vs refused), not a
text difference. Crucially it executes **no host program**: `TryExec` is resolved at load time by
the same `g_find_program_for_path`, and `Exec` stays the case's own probe, so the probe record is
the whole surface. (b) `pd-dot-root` vs `pd-empty-root`: same fixture, PATH absent answers
`{root}/./probe` through the `.` entry, `PATH=""` answers `{root}/probe` through the single empty
entry.

**Clause 2 (unset != the ambient search).** `pd-private-unset` refuses to load while
`pd-private-onpath` launches `{root}/bin/probe`; `pd-private-unset-wd` shows that a `Path=` working
directory does not rescue the private-dir program (it still refuses). This is the negative the item
required, measured on both sides.

**Clause 3 (the trailing `.` is real).** The first half holds: `pd-dot-root` is found only through
the `.` entry and its `argv[0]` carries that entry literally as `{root}/./probe`; an
absolute-`Exec` or a private-dir placement never reaches it. **The second half does not hold as
written.** Measured: with `Path={root}/work` and the program only in `work/`,
`PATH=""` **launches** (`pd-wd-empty` -> `{root}/work/probe`), exactly like PATH absent - the empty
entry is joined to the working directory rather than to the process cwd, so it finds the same file.
Two extra probes confirm the mechanism: an explicit `["{root}/work"]` entry and an explicit `["."]`
entry both answer `{root}/work/probe`, and the pair `{Path={root}/work, program at the case root}`
refuses under **both** PATH absent and `PATH=""` (also measured; not frozen - it separates nothing).
So there is no `PATH=""` fixture with a differing working directory that refuses. The frozen
sentence needs narrowing (its falsifiable content is "the `.` entry is load-bearing for a program in
the launch working directory"), and `path-default-cwd` is kept as a **declared non-separating
control pair** rather than being quietly dropped. This is reported, not repaired: I do not edit the
declaration.

**Section 2's live control.** `control_unset_as_empty_correct < cases_total` stays measurable: a
model that treats absent PATH as `PATH=""` gets `pd-sysbin-unset` wrong (predicted refusal, measured
launch) and `pd-dot-root` wrong (`{root}/probe` instead of `{root}/./probe`).

## 5. Fresh leg

`launchenv-fresh-r100.py` - stdlib only, imports the r99 oracle **by path** (never a copy), same CLI
as r99 (`--seed HEX --dir D --out F --count 60`, plus `--selftest`). It cycles the three behaviours
over the slots and randomises placement within each: program at the case root with PATH absent/`[]`
and optional `Path=""` and `%f` arguments (dot); a case-private dir with a random name, on PATH,
second on a two-entry PATH, absent, or `[]`, with and without `Path=` (private); `TryExec` naming a
random verified system program with PATH absent, `[]`, or a case-private decoy dir (sysbin). Every
PATH entry a case carries is `{root}`-relative or empty - the host is never on a case PATH - and the
selftest asserts that, plus behavioural coverage (3 checks, 0 failed; names `sh,xauth,gzip,sed,awk,
env,tr,cat`).

Measurement run: seed `a7d31c904b6e2f58`, count 60, wall **184.2 s** (host load 113/93/142 at the
receipt's start):
`FRESH_GEN: cases=60 ok=34 refused=26 dot=20 private=20 sysbin=20`, every case labelled by two
agreeing oracle runs, none dropped.

## 6. Candidate agreement (evidence for PRED-C1's `cases_correct` / `fresh_correct`)

Run as an instrument against the committed candidate, with the case env exactly as the contract
says (no `PATH` key at all for `path: null`; `PATH=""` for `[]`; `{root}`-joined entries otherwise):
`tools/mado-launchenv.py` agrees **10/10** on the frozen path-default cases and **60/60** on the
fresh leg (dot 20/20, private 20/20, sysbin 20/20). It reproduces the non-separating cwd pair too,
so the finding in Sec. 4 is a property of the frozen sentence, not a candidate defect.

## 7. Risks

1. `path-default-sysbin` depends on host state: `/bin` being a symlink to `/usr/bin` and `/usr/bin/sh`
   being executable and absent from the case root (cross-checked with `/usr/bin/xauth`). Both are
   recorded in `schema_notes.path_default`; if either changes, those three labels flip and the class
   must be re-measured, not assumed.
2. Clause 3's second half is falsified (Sec. 4). PRED-C1-r100-v1 as written does not depend on it - its
   conjuncts are counts of cases, classes, correctness and kills - but a reader re-deriving the
   declaration's prose will find the sentence wider than the property. Narrow it before filing.
3. The `[]` spelling was never used in r99; it is measured identical to `[""]` here, but any counter
   that compares `path` structurally must treat the two as the same environment (both `PATH=""`).
4. The load gate resolves with cwd = the case root, so every case is cwd-sensitive by construction;
   a harness that materialises a case under a **relative** parent makes the candidate resolve the
   root against its own cwd and produces load refusals that look like disagreements. This bit my own
   comparison harness during receipt composition; all three instruments now exit 2 on a relative
   parent, and the receipts state the absolute parents used.
5. The sysbin arm's separation rests on `TryExec` consulting the same PATH source as `Exec`
   (measured twice here). If a future glib changes that, re-measure before reusing the class.

## 8. Blockers, tooling, scratch

No blockers; nothing needed from L0. No tool was installed or upgraded (no pacman/`uv`/`npx`
transaction ran, no `sudo`, no host sysctl, no service touched). Scratch
`/fast/scratch/hyaku/mado-r100/R100MExecCases` was deleted before yielding; the receipts above were
copied into the wave directory first.
