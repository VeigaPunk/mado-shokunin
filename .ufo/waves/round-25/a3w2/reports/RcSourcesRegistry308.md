# RcSourcesRegistry308 — C2 ledger attack on a3w1 `CapSourcesRegistry308`

Seat: `MadoR25A3.RcSourcesRegistry308` (reviewer, wave `a3w2`). Date: 2026-10-23.
Target under review: `.ufo/waves/round-25/a3w1/reports/CapSourcesRegistry308.md` — a3w1's re-run
of `SCORECARD.md:308` ("sources registry") at base `41cc04c8d593837a0d5078bffaacdaa163d12897`.
Assignment: independently re-derive its ledger line; flag copied-not-run evidence, wrong revision,
overclaim, or missed superseding text. Leaf member; no subagents dispatched.

## 1. Row re-read at base (independent)

```
git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 41cc04c8:SCORECARD.md
  -> 1618 lines, sha256 6b6995ff6998a405c2d4472463204b16e644829ad821a368922a65a60853ca08
```

`SCORECARD.md:308` sits under `### Capabilities (round 12)` (heading `:304`) and reads verbatim:

```
| sources registry | Curate where mado learns: 39 opened, scoped-tier rows (mined/queued/rejected), study paths, search log; every contract census command runs clean and every mined row joins to an entry that cites it | `corpus/SOURCES.md`; census block in `.ufo/evidence/round-12/after.txt` | 12 |
```

Base blobs verified against the report's claims:

- `corpus/SOURCES.md` sha256 `58f6e47ba6b5539291aa4fc48388ae880d4c498e67568ca5e3b908d485ab1e5f`, 408 L / 147,150 B — matches.
- `.ufo/waves/round-24/c2/manifest.json` sha256 `e02c76d1adb4f523fccf11e1e5ad4cd40f6d0da460b75c7f811b66306e188a02` — matches; its `sources registry` argv is `bash {FLEET}/scripts/sources-census.sh validate --root {CENSUS_ROOT}`, `cwd {TREE}`, `exit_ok [0]`, regex `(?m)^mado\tok\t`.
- `.ufo/evidence/round-12/after.txt`: the verbatim "SOURCES contract census" block is `:47-67`; the mined-row join loop is the single line `:44` (precedes the block; the report's "(c1-c7)" plus a separate "c8" framing matches this layout).

## 2. Own sandbox re-run (GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE unset; `timeout 600`, `prlimit --as=4000000000`)

```
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q \
  /home/vgpnk/Projects/shokunin/mado-shokunin /fast/scratch/hyaku/mado-r25a3/rc/CapSourcesRegistry308
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C … checkout -q --detach 41cc04c8
  # rev-parse HEAD = 41cc04c8d593837a0d5078bffaacdaa163d12897; status --short empty
mkdir -p /fast/scratch/hyaku/mado-r25a3/rc/census-root
printf '# scratch census root for C2 recheck 41cc04c8\n' > …/census-root/shokunin.conf
ln -sfn …/CapSourcesRegistry308 …/census-root/mado-shokunin
```

### (a) frozen census command — exit 0 — REPRODUCED

```
timeout 600 prlimit --as=4000000000 bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh \
  validate --root /fast/scratch/hyaku/mado-r25a3/rc/census-root
mado	unlisted	…/census-root/mado-shokunin
mado	W04	S030 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
mado	W04	S042 duplicate url wayland.freedesktop.org/extras.html across scopes
mado	W04	W04	S045 duplicate url …/Window-Rules across scopes
mado	W04	S097 … matte-black/colors.toml across scopes
mado	W04	S119 … imaplib.py across scopes
mado	W04	S120 … executionmodel.rst across scopes
mado	W04	S121 … executionmodel.rst across scopes
mado	ok	…/census-root/mado-shokunin/corpus/SOURCES.md
exit=0
```

Byte-identical to the report's receipt modulo the scratch path (`c2/` → `rc/`). Zero E-codes; the
manifest regex `^mado\tok\t` is satisfied. `validate --file corpus/SOURCES.md` also exit 0 with the
same seven W04 warnings (first field `file`, not `mado` — see §5 nit 2).

### (b) default census mode — exit 0 — REPRODUCED

`rows 168`, `tier.A 161 / B 1 / C 6`, `status.mined 149 / queued 10 / rejected 9`, FLEET block
mirrors with `invalid 0`, `missing 0`. Identical to the report's receipt.

### (c) round-12 census block + join loop, verbatim — exit 0 — REPRODUCED

```
== c1: 168  (exit 0)      == c2: 0  (exit 0)     == c3: A=161 B=1 C=6
== c4: mined=149 queued=10 rejected=9           == c5: dup-check-done (no lines)
== c6: enum-check-done (no lines)               == c7: used-by-check-done (no missing lines)
== c8 join loop:
entry corpus/knowledge/hyprland-config-era-r12.md cites S030 without a mined row naming it
entry corpus/knowledge/terminal-trees-r23.md cites S132 without a mined row naming it
join-done  (exit 0)
```

Same two join lines as the report. Verified independently: `S030` is `rejected`
(`corpus/SOURCES.md:42`), `S132` is `queued` (`corpus/SOURCES.md:144`), and
`corpus/knowledge/terminal-trees-r23.md:1` itself declares "S132 stays queued and supports
nothing" — which is also why the regex catches S132 inside that single-line `source:` header.
Claimed direction (mined row → citing entry) printed nothing: clean.

The report's provenance check also reproduces: after `git checkout -q --detach 8e5d9369` in my
clone, the same join loop prints the same two lines — pre-existing at the round-24 base, as claimed.
(Clone restored to `41cc04c8` afterward.)

## 3. Supersession / contradiction grep at base (independent)

- `grep -n "sources registry"` on `SCORECARD.md` → `260`, `308`, `1575` — the same three hits the
  report lists.
- `SCORECARD.md:1566-1571`: the round-24 table "supersedes the implied `works` of every earlier
  row" — verified at `:1570`; `:1575` reads
  `| sources registry | works | census \`mado ok\`, exit 0 at \`8e5d9369\` |` — consistent, no
  contradiction.
- `:1588-1596`: population scope note (12 rows under `Capabilities` headings; `:308` inside; the
  stale `source-fragment collision screen` row `:437` is a different capability, outside the
  counted population) — verified.
- `:1608`: no-harm note "census exit 0" at `eb14fa3d` — verified.
- Nothing later contradicts `:308`.

## 4. Comparison against the a3w1 ledger line

| field | a3w1 report | this re-derivation | verdict |
|---|---|---|---|
| observed status | works | works (all commands exit 0, same outputs) | agree |
| exit code | 0 on every leg | 0 on every leg | agree |
| key output | `mado\tok`, 7 W04, rows 168, mined 149 / queued 10 / rejected 9, join lines S030/S132 | byte-identical modulo scratch path | agree |
| command form | manifest-frozen `sources-census.sh validate --root {CENSUS_ROOT}`, cwd = clone @ base | identical; same live `{FLEET}` script both seats ran (it is not a tree path — inherent to the frozen argv) | agree |
| superseding pointers | `SCORECARD.md:1575` round-24 status row | verified verbatim | agree |
| revision | `41cc04c8`, both blob shas | identical | agree |

## 5. Non-defect nits

1. **"No `Round 25` section exists in `SCORECARD.md`"** — technically there is a
   `### Planned (round 25; intent only)` heading at `:1614` (found by `grep -n 'round 25'`). It is
   intent-only (counter re-cut plans, routing the collision-screen row) and contradicts nothing, so
   the substantive claim — no results section contradicting `:308` — holds. Wording imprecision only.
2. "`--file corpus/SOURCES.md` printed the same seven W04 lines" — same warning bodies, but the
   first field is `file`, not `mado`, and the closing line is `file\tok`. Literal "same lines" is
   slightly loose; the claim's substance (seven duplicate-URL warnings, clean verdict) is exact.
3. **No copied-not-run indicators**: receipts carry run-specific paths (`c2/census-root` vs my
   `rc/census-root`), the c8 rationale required actually running the join (a copyist would not know
   S132 comes from a prose mention inside the `source:` line), and the `8e5d9369` provenance loop
   reproduces. Output blocks reproduce from live runs, not transcription.
4. **No overclaim**: the ledger correctly scopes "works" to what the census demonstrates; it
   explicitly dates the row's `39 opened` as a round-12 count (168 rows at base) rather than
   restating it, and it routes rather than hides the two join lines.
5. `sources-census.sh` writes (`cat >`, mktemp fixture dirs) exist only inside its `--selftest`
   path; `validate`/default modes emit stdout only — the report's "read-only" characterization
   holds for the exercised modes.

## 6. Cleanup

`rm -rf /fast/scratch/hyaku/mado-r25a3/rc/CapSourcesRegistry308 /fast/scratch/hyaku/mado-r25a3/rc/census-root`
plus `/tmp/mado-r12-rows-rc.tsv`, `/tmp/mado-r12-rows-8e5.tsv`, `/tmp/rc-join-cmd.txt` — all deleted;
parent listing shows them gone (remaining entries belong to sibling seats). No process started by me
left running; no lane file written except this report. Installs: none.

## Verdict

RECHECK CapSourcesRegistry308: agree — frozen census `validate` prints `mado\tok` exit 0 with the
same 7 W04 lines, default-mode tallies (168 / 149-10-9 / A161-B1-C6) match byte-for-byte, the
round-12 verbatim block and join loop reproduce exactly (both join lines pre-existing at `8e5d9369`,
claimed direction clean), revision and both blob shas verified, superseding pointer `SCORECARD.md:1575`
correct; only nits are wording imprecisions (`Planned (round 25)` heading exists at `:1614`;
`--file` W04 lines carry the `file` field, not `mado`).
