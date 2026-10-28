# R55ExecC3CounterA — quality/counters/c3-r55-p19.py (draft, bytes-first)

Deliverables (directory `.ufo/waves/round-55/w1/R55ExecC3CounterA/`): `c3-r55-p19.py` (executable, python3 -I, stdlib only),
`selftest-output.txt` (40/40: 35 evaluate cases + 5 CLI setup cases). Nothing tracked was touched; scratch removed.

## What it does
Reads only git objects at `--rev` of `--repo` (`rev-parse --verify rev^{commit}`, `cat-file blob <commit>:<path>`, ambient `GIT_*` stripped,
`GIT_CONFIG_GLOBAL=/dev/null`, `TMPDIR=--work`). Base bytes: `3b55b6e…:corpus/knowledge/…errata-r53.md` from the same repo. Embeds
TABLES_SHA256 `bf46c889…9490` and compares it with the blob of `.ufo/waves/round-55/frozen-tables.json` at `--rev`.
Prefix = raw `entry.startswith(base_entry)`; only the bytes after it are parsed (split on `\n`, strip ASCII ws, fenced ``` / ~~~ lines skipped).
Q row = exactly 3 cells (`Qnn`, `Hyprland-ConfigActions.cpp:<line>`, `` `<quote>` ``), byte-equal to frozen, and the only row of its id.
Exit 0 TARGET_MET / 1 miss / 2 setup (`MADO_P19_FIX: SETUP <reason>`). Line grammar exactly as registration §C3; `rev=` echoes the argument as given.

## Commands / decisive output
- `python3 -I c3-r55-p19.py --selftest --repo <lane> --rev HEAD --work <scratch>` → `MADO_P19_FIX_SELFTEST: 40/40 passed`, rc 0.
  Cases: good (13/13, none); CTL-1 absent → `prefix=identical`, missed rows:Q01..Q13,p23 (+rows:heading); CTL-2 → `prefix`; CTL-3 → exactly `rows:Q09`;
  CTL-4 → rows:Q08..Q12; CTL-5 → exactly `p23`; CTL-6 → exactly `readme`; prefix-with-CRLF (one line and all lines) → `prefix`;
  duplicated Q03 (appended and adjacent) → `rows:Q03`; Q03 inside ``` or ~~~ fence → `rows:Q03`; extra fenced copy beside the real row → still met;
  P23 only in fence / duplicated / supersedes P20 / S370 / lacks else-word / lacks `== 0` → `p23`; heading missing or only in fence → `rows:heading`;
  Q anchor shifted, trailing space in quote, 4th cell → `rows:Q09`; pin +1 byte or absent → `pin`; tables +1 byte → exactly `tables_sha`; tables absent;
  entry absent / truncated below base → `prefix`; README absent / P23 on a different line → `readme`; CRLF only after the prefix → met.
- Real lane: `--rev HEAD` → `prefix=identical rows=0/13 pin=ok p23=bad readme=bad … TARGET_MISSED missed=rows:heading,rows:Q01..Q13,p23,readme` rc 1;
  `--rev 3b55b6e…` → `TARGET_MISSED` rc 1 (pin=bad because the tables blob is absent at base; missed includes tables_sha).
- End-to-end with the REAL base: scratch repo with `.git/objects/info/alternates` → lane objects, commit on top of 3b55b6e with the real base entry + generated block +
  real pin + tables + README with P23 → `rows=13/13 pin=ok p23=ok readme=ok verdict=TARGET_MET missed=none` rc 0. The same with the two scribe drafts
  (`w1/R55ScribeP19a/after.md`, `w1/R55ScribeP19b/after.md`, with a synthetic README line) → both `TARGET_MET` 13/13 (draft entries only, README not theirs).

## Ambiguities / decisions (L1 please confirm; none edits the frozen files)
1. **Harness interface:** the base is a constant commit read from `--repo`. A scratch repo built by `git init` + commit does NOT contain 3b55b6e, so the counter exits 2
   `SETUP base_commit_absent` there. The C3 harness (`r55_ctl_c3.py`) must make the base reachable in each scratch repo (alternates to the lane's object dir, or clone/fetch with
   the base, then commit the mutated tree on top of it). Selftest avoids the issue by passing its own base commit in-process (no CLI flag exists for it).
2. Heading leg: registration names no leg for a missing `Correction (round 55)` heading; I emit `rows:heading` (not counted in rows=a/13).
3. p23 leg also fails when the row is absent/duplicated, or Source cell ≠ `S371`, or Pin:anchor cell ≠ `Hyprland-ConfigActions.cpp:1554-1576`; token tests are case-sensitive
   substrings (`Otherwise` capitalised would fail unless `else`/`any other` also present).
4. Fenced-code skipping and CR tolerance after the prefix are my reading of the seat assignment, not frozen text; a fenced extra copy of a Q row does not count as a duplicate.
5. Q cells are split on `|`, so a quote containing `|` cannot match (none of the 13 frozen quotes does). Extra rows with ids outside Q01..Q13 are ignored.
6. Without a parsable tables blob (absent at rev) every row is missed rather than a setup error (keeps base = TARGET_MISSED); a present-but-unparsable blob with the right sha is exit 2.
7. README leg: any line (fences not considered) naming the entry file and `P23`.

## Not verified
Not run through `quality/check-r55-controls.py --claim c3` (harness module `r55_ctl_c3.py` did not exist when I looked; `quality/` held only the dispatcher). No tools installed.
No hold-out path seen.
