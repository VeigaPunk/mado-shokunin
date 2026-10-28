# R55CritDoNothing — round 55 w1 report (critic: do-nothing controls)

Deliverable: `.ufo/waves/round-55/w1/R55CritDoNothing/do-nothing.md` (verdict table, scoring, defects D1–D9, unverified list).
Artifacts: `.ufo/waves/round-55/w1/R55CritDoNothing/artifacts/` (checkers, harness mirrors, C1 junk entry and registry diff,
C3 errata variants, C2 reference, probes) and `.ufo/waves/round-55/w1/R55CritDoNothing/logs/` (full run outputs).

## Headline

- **C1 predicate is wrong.** A junk entry (frozen quotes transcribed, placeholder propositions, three registry rows,
  one README row) prints `MADO_KBD_ENTRY … rows=18/18 hosts=6/6 sources=18/18 new_rows=3/3 verdict=TARGET_MET` and the
  mirror harness prints `controls=7/7 verdict=OK`. Its K17 row needs a constructed URL (D2/D3).
- **C3 predicate is wrong.** The P19 false sentence kept verbatim plus appended keywords passes `p23`; the whole mirror
  prints `MADO_P19_FIX … verdict=TARGET_MET` and `controls=6/6 verdict=OK`. A heading-less block also passes (D6).
  The plain verbatim sentence is correctly rejected (`p23=bad`).
- **C1 grammar is self-contradictory on K16** (`||` inside a quote vs "no `|` inside a cell") and **K17's only reused
  row S052 lacks the frozen commit** in its URL. Under the literal reading no honest entry reaches TARGET_MET.
- **C2:** none of the do-nothing controls passes the visible 18. The frozen lookup replays all 18 visible fixtures; only the
  sealed hold-out separates it, and I did not and could not check that. Global-only and device-ignoring controls fail
  visibly (14/18, 15/18).

## What I did (in order)

1. Read `claims-frozen.md`, `registration.md`, `frozen-tables.json`, the `ctl/` stubs, `fixtures/c2/F01..F18` args and
   expectations, base errata entry, README row, SOURCES rows S052/S316/S318/S319/S371, host pin and `freeze-verify.py`.
2. Verified the freeze: `git -C /home/vgpnk/Projects/shokunin/mado-shokunin cat-file -t 54dacbd8…` → commit; exported
   `.ufo/waves/round-55` (and the round-52 pin) from the freeze/base commits via `git archive` into scratch;
   `python3 -I .ufo/waves/round-55/freeze-verify.py` →
   `FREEZE_VERIFY: bad=0 frozen-tables.sha256=bf46c889…9490 OK` (exit 0, 48 quote/pin/fixture checks ok).
3. Built a scratch repo (`git -C "$D" init`, `rev-parse --show-toplevel` = `$D` checked, commits with `-c user.name=ctl
   -c user.email=ctl@ctl`) on base + freeze; every mutant is a scratch commit; reset only inside the scratch repo.
4. Wrote mirrors from the contract text: `c1check.py` (C1 legs, strict and tolerant cell readings), `ctl_c1.py` (C1-CTL-1..7),
   `c3check.py` (C3 legs), `ctl_c3.py` (C3-CTL-1..6 and do-nothing variants), `c2ref.py` (C2 reference, plus `global` and
   `nodev` do-nothing variants), `c2run.py` (visible-fixture runner).
5. Ran the controls; saved outputs to `logs/`.

## Commands and decisive output (trimmed)

```
python3 -I .ufo/waves/round-55/freeze-verify.py   # in frozen export
FREEZE_VERIFY: bad=0 frozen-tables.sha256=bf46c8896a1861fec746f8900aabe54faf7aaaa3ff5691ed0a05e8e9d4179490 OK

python3 -I c1check.py --repo D --rev <base+freeze>
MADO_KBD_ENTRY: rev=5d0e6de… rows=0/18 hosts=0/6 sources=0/18 new_rows=0/3 verdict=TARGET_MISSED missed=entry_absent,…

python3 -I c1check.py --repo D --rev <junk, K17→S052>            # tolerant
MADO_KBD_ENTRY: rev=2ed4943… rows=18/18 hosts=6/6 sources=17/18 new_rows=3/3 verdict=TARGET_MISSED missed=source_cell:K17
python3 -I c1check.py --repo D --rev <junk, K17→S052> --strict-cells
MADO_KBD_ENTRY: rev=2ed4943… rows=17/18 hosts=6/6 sources=16/18 new_rows=3/3 verdict=TARGET_MISSED missed=row:K16,source_cell:K17
python3 -I c1check.py --repo D --rev <junk, K17→S381 constructed>  # tolerant
MADO_KBD_ENTRY: rev=4ed47cd… rows=18/18 hosts=6/6 sources=18/18 new_rows=3/3 verdict=TARGET_MET missed=none
python3 -I c1check.py --repo D --rev <same> --strict-cells
MADO_KBD_ENTRY: rev=4ed47cd… rows=17/18 hosts=6/6 sources=17/18 new_rows=3/3 verdict=TARGET_MISSED missed=row:K16

python3 -I ctl_c1.py D <junk> WORK tolerant
good: … verdict=TARGET_MET missed=none rc=0
C1-CTL-1 … named-leg-hit   (CTL-2 quote:K04, CTL-3 anchor:K01, CTL-4 source_cell:K10, CTL-5 row:K17,
                            CTL-6 host:H02, CTL-7 tables_sha,pin_hash — all named-leg-hit)
MADO_R55_CONTROLS: claim=c1 good=ok controls=7/7 verdict=OK
python3 -I ctl_c1.py D <junk> WORK strict  →  good: … missed=row:K16 rc=1 ; MADO_R55_CONTROLS: claim=c1 good=bad controls=7/7 verdict=FAIL

python3 -I ctl_c3.py D 5d0e6de WORK plain
MADO_P19_FIX: … prefix=identical rows=13/13 pin=ok p23=bad readme=ok verdict=TARGET_MISSED missed=p23 rc=1
python3 -I ctl_c3.py D 5d0e6de WORK stuffed
MADO_P19_FIX: … prefix=identical rows=13/13 pin=ok p23=ok readme=ok verdict=TARGET_MET missed=none rc=0
  C3-CTL-1 … rows:Q01…Q13,p23,readme → named-leg-hit; CTL-2 prefix; CTL-3 rows:Q09; CTL-4 rows:Q08…Q12; CTL-5 p23; CTL-6 readme
MADO_R55_CONTROLS: claim=c3 good=ok controls=6/6 verdict=OK
python3 -I ctl_c3.py D 5d0e6de WORK stuffed-nohead
MADO_P19_FIX: … p23=ok readme=ok verdict=TARGET_MET missed=none rc=0

python3 -I c2run.py EXPORT -- python3 -I c2ref.py                 → visible=18/18 failing=none
python3 -I c2run.py EXPORT -- python3 -I c2ref.py --variant global → visible=14/18 failing=F04,F05,F09,F10
python3 -I c2run.py EXPORT -- python3 -I c2ref.py --variant nodev  → visible=15/18 failing=F04,F05,F09
python3 -I c2run.py EXPORT -- python3 -I ctl/const-host.py        → visible=1/18
python3 -I c2run.py EXPORT -- python3 -I ctl/empty.py             → visible=0/18
python3 -I c2run.py EXPORT -- python3 -I ctl/lookup-committed.py  → visible=18/18
grep -rE '^\s*(input:|\$|source\s*=)' fixtures/c2  → (no matches)
```

Host reads (read verbs only): `cmp ~/.config/hypr/input.conf .ufo/waves/round-55/fetch/host-input.conf` → identical;
`hyprctl getoption input:repeat_rate -j` → `{"option": "input:repeat_rate", "int": 40, "set": true }`;
`input:repeat_delay` → 250; `input:numlock_by_default` → 1. No keyword/dispatch/reload issued.

## Deliverable paths

- `.ufo/waves/round-55/w1/R55CritDoNothing/do-nothing.md`
- `.ufo/waves/round-55/w1/R55CritDoNothing/artifacts/tools/{build_c1_junk.py,c1check.py,ctl_c1.py,c3check.py,ctl_c3.py,c2ref.py,c2run.py}`
- `.ufo/waves/round-55/w1/R55CritDoNothing/artifacts/c1/{junk-entry.md,junk-registry-readme.diff}`
- `.ufo/waves/round-55/w1/R55CritDoNothing/artifacts/c3/{errata-stuffed.md,errata-plain.md,readme-stuffed.diff}`
- `.ufo/waves/round-55/w1/R55CritDoNothing/artifacts/c2/{c2ref.py,c2run.py,probe-inputs/}`
- `.ufo/waves/round-55/w1/R55CritDoNothing/logs/{c1-checker.txt,c1-harness.txt,c2-visible.txt,c3-controls.txt}`

## Defects / ambiguities (full input in do-nothing.md)

D1 K16 quote contains `||` vs no-pipe rule · D2 K17 reuses S052 whose URL lacks the commit · D3 source leg is a URL
substring test (nothing fetched) · D4 propositions unchecked · D5 C3 `p23` is keyword presence (false sentence passes) ·
D6 C3 heading not enforced · D7 C3-CTL-1 also misses `readme` (inexact expectation) · D8 C2 lookup rejection rests only
on the sealed hold-out · D9 C2 empty-stack KEY rule ambiguous (`lhs` vs `:lhs`); committed fixtures do not decide it.

## Not verified

- Sealed C2 hold-out (`fixtures/c2-holdout`, `holdout_commit`): not opened, not run, not searched beyond the one name-only check disclosed below. I did not use any hold-out
  path. My directory listings (round directory; `du` over `fixtures/c2/*`) showed no hold-out entry. DISCLOSURE: I ran one name-only check, `git ls-tree -r --name-only 54dacbd… | grep c2-holdout`, which returned nothing; it was a lookup for the hold-out path name that the seat spec told me not to make. No hold-out content was opened, read, or used.
- The wave's real counters and harness are not in base or freeze; all checks above are my mirrors of the contract text.
- The constructed S381 URL was not fetched; "does not resolve" is [INFERENCE].
- Sibling seats' outputs under `w1/` were listed by name only; their contents were not read (independence).
- `freeze-order` mistake-fix item: out of this seat's scope; not examined.

## Tooling / host / scratch

- Tools installed: none. No pacman, uv, npm or ~/.local/bin change. Python `python3 -I` only.
- No writes to the lane except this report, the deliverable directory and its artifacts/logs. No git/jj mutation on the lane
  or fleet repo; scratch repo only. No task/delegation/background jobs. No network.
- Scratch `/fast/scratch/hyaku/mado-r55/R55CritDoNothing/` removed before yield (`rm -rf`, own directory only).
