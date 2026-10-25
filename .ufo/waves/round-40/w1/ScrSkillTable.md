# ScrSkillTable — SKILL.md decision-table rows for `--live` (round 40, w1)

Seat: scribe, leaf (no dispatch, no background jobs). Date: 2026-10-25.
Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`, HEAD `e2b51d3b3f79768282914d57c1fa32cc85dcb06a`.
Freeze read first: `.ufo/waves/round-40/registration.md` (freeze `5e7e88525cc539563de7746361b2650802e81809`,
base `9fc511ddce708327377161202f358ce37dc266ba`), C1 = `--live`/`--hyprctl`/`--probe` under
`PRED-C1-r40-v1`.

## Deliverable

`.ufo/waves/round-40/w1/ScrSkillTable/skill-rows.md` (13 122 B, 131 lines) — a complete,
additive-only block of SKILL.md text plus its grounding table. Nothing in `SKILL.md` was edited;
`SKILL.md` sha256 is still `32edcb2e38ba56514dadd24ad62e426f613fc8a6fd541599248eca81da2adcc7`.

The draft contains, in this order:

1. **Modes table** (4 columns × 3 modes): static `--home DIR`, `--getoption FILE`, and `--live`
   — command, what it prints (`live` field text / `null`, `agreement`), and *when to use each*.
   The `--live` vs `--getoption FILE` distinction is stated as: a dump is a snapshot you already
   hold (a transcript, another host, a pinned receipt) and its merge cannot prove currency;
   `--live` is the current answer and is the only mode that runs the compositor verb.
2. **The read-only verb**: exactly one `HYPRCTL getoption -j KEY` per declared key
   (`--hyprctl PATH`, default `hyprctl`), nothing else — no `keyword`/`dispatch`/`reload`/
   `setprop`/`--batch`, no socket of its own, no write under the config root; `--probe KEY`
   semantics (repeatable, `live-default` or dropped, never re-queried).
3. **Claim-first routing rows** for the live mode (shadowing proof, engine default, dump
   freshness, ownership) tagged `[OBS]`.
4. **Exit-code table with one row per code 0/1/2/3/4/5**, each carrying the literal stderr
   signature, its meaning, and the check that settles it.
5. **Native-reply paragraph** (four forms + `no such option` → `config-only`; host-style
   conversion per form) with the frozen capture counts (70 lines: int 44, float 5, str 8,
   custom 13).
6. **Angle-inheritance reading rule**: a 4-row table (declared × live → label → reading) plus
   five reading rules — colour-normalisation (`rgb(e68e0d)` *is* `ffe68e0d`), "an angle-only
   difference is never `mismatch` while an earlier declarer carried it", `agreement*` needs >1
   declarer *and* equality, `set=false` on a declared key is `mismatch`, gaps/weights compare
   natively — and the host census 62 `agreement` / 8 `agreement*` / 0 `mismatch`, with the
   two-row flip (`general:col.active_border`, `group:col.border_active`) when inheritance is off.

## Headline finding

**`SKILL.md` has no `mado-options.py` row at all.** `grep -n 'mado-options' SKILL.md` → no
output, exit 1 at HEAD `e2b51d3`; the `^#` heading scan shows no options section. The round-39
tool (S219) never entered `SKILL.md`. Consequence for this seat's task: the instruction "read the
existing `mado-options.py` rows/sections" has no referent, so the draft is written
**self-contained** — it introduces all three modes in one table rather than adding a row to a
pre-existing `--getoption` row that does not exist. The draft states this precondition explicitly
so the integrator is not misled about what exists.

Insertion point named in the draft: after `SKILL.md:189` (last line of `### Divergence vocabulary
and severity taxonomy`), before the blank `:190` and `## Safe-probe discipline` at `:191`; the
end-of-file append is named as the alternative. Both are pure insertions.

## Evidence (what I actually ran)

All reads are read-only. Compositor contact was limited to the two allowed verbs (`getoption -j`);
no mutation, no socket of my own, no pacman, no git/jj mutation.

| Check | Command | Outcome |
|---|---|---|
| No existing rows | `grep -n 'mado-options' SKILL.md` | no output, exit 1 |
| Tool state at lane tip | `python3 -I tools/mado-options.py --help`; `grep -c -- '--live' tools/mado-options.py` | usage shows only `--home/--getoption/--selftest`; count `0` — **the delivered tool has no `--live` yet** |
| argv discipline | reference control `c1/ctl-ref-tool.py.txt` (sha256 `f96d9e0a…a08aa`) + stub compositor in `/tmp` | `argv.log` = exactly `getoption -j general:border_size`, `… general:col.active_border`, `… general:gaps_out`, `… input:kb_layout` — one call per declared key, no other argv |
| exit 0 / row shape | same run | rc=0, rows carry `"live": "2"`/`"ffe68e0d 45deg"`; `config-only` row carries `"live": null` |
| exit 2 | `--probe ''`; `--probe --foo` | rc=2 `invalid probe key ''` (stub log absent → program never ran); rc=2 argparse `expected one argument` |
| exit 3 | `--home /nonexistent` | rc=3 `<path>: No such file or directory` |
| exit 4 | `--getoption` on `[1,2,3]` | rc=4 `getoption JSON root must be an object` |
| exit 5 (all four signatures) | stubs: `/bin/false`, missing path, `not json`, `{"option":"x","set":true}` | rc=5 `<key>: … exited 1` / `<key>: cannot run … [Errno 2]` / `<key>: malformed reply from …` / `<key>: unknown reply form from …` — key named each time |
| exit 1 signature | `c1/ctl-ref-tool.py.txt:1207-1213` | prints `MADO_OPTIONS_SELFTEST: k/n passed`, returns 1 when `passed < total`; passing run printed `MADO_OPTIONS_SELFTEST: 71/71 passed` |
| `no such option` at exit 0 | `hyprctl getoption -j general:definitely_not_an_option` | `no such option`, `rc=0` |
| angle-inheritance anchor on the host | `hyprctl getoption -j general:col.active_border` | `{"option": "general:col.active_border", "custom": "ffe68e0d 45deg", "set": true }`, rc=0; same line at `c1/native-capture.jsonl:21` |
| label flip | stub fixture: two declarers, last `rgb(e68e0d)`, live `ffe68e0d 45deg` | `agreement*`; a different colour `rgb(ff0000)` against the same live → `mismatch` |
| capture census | recomputed from `c1/native-capture.jsonl` (sha256 `1fe39c05…9b4b25`, present at freeze `5e7e885`) | 70 lines: int 44, float 5, str 8, custom 13 |
| host label census | `w1/ExecLiveCensus/census-receipt.txt` + `live-out.json` (sha256 `cde4b2df…905462`, 70 rows) | `agreement=62 agreement*=8 mismatch=0 config-only=0`; `variant-noinherit` → `agreement*=6 mismatch=2`, flipped rows named |

Provenance hashes pinned in the draft: `SKILL.md` `32edcb2e…adcc7` (last touched `d40b35f9…`),
capture `1fe39c05…9b4b25`, reference control `f96d9e0a…a08aa`, `live-out.json` `cde4b2df…905462`.

## Gates / limits stated in the draft

- The **62/8/0 census is labelled provisional**: `w1/ExecLiveCensus/census-receipt.txt` is an
  uncommitted candidate whose `tool sha256 <TOOLSHA>` is still a placeholder (it was produced from
  the throwaway reference, not the delivered tool). The draft reports the number and marks it as
  not yet evidence; the delivered tool must reproduce it before the row can be quoted as `[OBS]`.
- The draft does **not** assert delivered-tool behaviour. At my read time `tools/mado-options.py`
  had no `--live`; the candidate at `w1/ExecToolLive/mado-options.py` documents the same exit map
  (`:65-67`) but its `main()` had not gained `--live` when I read it. The rows describe the frozen
  contract as the reference control realizes it; the integrator should re-read the delivered
  `--help`/docstring before appending (only `--probe`/`--hyprctl` help wording could need a touch).
- Exit 3/4/5/2/1 signatures were observed on the reference control with stub compositors, not on
  the delivered tool.

## Touched surfaces

- Written: `.ufo/waves/round-40/w1/ScrSkillTable/skill-rows.md` (new, seat dir),
  `.ufo/waves/round-40/w1/ScrSkillTable.md` (this report).
- Read-only: `SKILL.md`, `registration.md`, `quality/counters/c1-r40-live.py`,
  `c1/ctl-ref-tool.py.txt`, `c1/native-capture.jsonl`, `w1/ExecLiveCensus/{census-receipt.txt,
  live-out.json,ref-noinherit.py.txt}`, `w1/ExecToolLive/mado-options.py`,
  `tools/mado-options.py`, `.ufo/waves/round-40/w1-spec.json`, `git log/rev-parse/cat-file/show`.
- `/tmp/scrskill-5ki93hff` scratch (fixture trees, stub compositors, tool copy) — removed below.
- No host config tree, no compositor state, no service, no sibling lane, no fleet path, no git/jj
  index touched. No package transaction. No tool installed (nothing needed).

## Out of scope (not done, by assignment)

- No edit to `SKILL.md` (additive draft only; the L1 is the only integrator).
- No counter run, no `--selftest` on the lane tool, no C1/C2 verdict, no receipt writing.
- No new corpus entry or registry row (C2 belongs to other seats).
