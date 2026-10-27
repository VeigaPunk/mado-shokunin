# MutC1Counter — mutation score of the C1 frozen counter (round 48, w2 FALSIFY)

Seat: `MutC1Counter`. Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`, base `579f694b…`, freeze `3e6c848a`
(`round-48: freeze v1 …`). Subject: `quality/counters/c1-r48-terminal-cache.py` (`PRED-C1-r48`) and its frozen
controls. Ticket: mutate one C1 clause per `a/s/f/w/x/g/i/r`, score all **190 cold + 204 warm** fixtures for every
mutant, verify the frozen controls kill them, and include the six named attacks.

**Kill vocabulary used below.**
`K1` (verdict kill) — the frozen instrument returns `TARGET_MISSED` for an attacker and the mutant counter returns
`TARGET_MET` for the same attacker. `K2` (clause kill) — the mutant loses a clause's discriminating power (the
clause tally changes for an attacker the frozen clause rejects) but the verdict stays `MISSED` because another
clause covers the same attack. `equivalent` — the mutation changes nothing measurable (there was nothing to remove).
`self-defeating` — the mutant rejects the subject the instrument is supposed to admit, i.e. it is not a silent
weakening.

Every cell in this report is one full invocation of a counter over **190 cold + 204 warm fixtures** (plus the 394
explain cases and 230 generated cases the counter runs in the same process), with `--nonce 4848` for all cells.
61 cells were measured: 61 × (190 + 204 + 394 + 230) fixture/case scorings. Raw logs, clause lines and diffs are in
`w2/MutC1Counter/`.

---

## 1. Bottom line

* **The frozen instrument admits the data candidate, and nothing in this wave breaks that:** baseline
  `PRED-C1-r48: cold=190/190 warm=204/204 explained=394/394 generated=230/230 selftest=ok readonly=ok
  tool=present verdict=TARGET_MET` (exit 0), re-measured today on the frozen bytes.
* **5 of the 8 clause mutants are killed at verdict level (K1): `a`, `s`, `w`, `x`, `r`.** The attackers that do
  it are one-rule tools derived from the data candidate; **the frozen control corpus alone kills none of them at
  verdict level**, because every one of its 20 controls also fails `s` and/or `w`/`x` (D1).
* **2 clause mutants survive at verdict level (`f`, `g`)** and are killed only at clause level (K2): no tool can
  fail `f` (or `g`) alone, because clause `x` re-checks every output difference and clause `g`'s 150 generated
  cold cases re-sample the same cold rules. The instrument therefore stays sound, but those two clauses are
  redundant, not load-bearing.
* **Clause `i` has no behavioural teeth.** `i-no-write-tripwire` is an *equivalent mutant*: the frozen counter
  already admits a tool that performs the resolver's cache save. `writes-cache` (a frozen control) has clause
  tallies identical to the frozen `reference`'s, `readonly=ok`, `trips=0`; a writing probe built from the data
  candidate scores **`TARGET_MET`** on the frozen counter. `i-host-etc-bound` is *self-defeating*: it breaks the
  admitted subject (host `/etc` changes the tool's `ls` model through `pwd`/`grp`, warm drops to 144/204).
* **Three named rule removals are all killed**, but two of them only by clause `x` (and by the tool's own
  selftest): `XTE_CACHE_ENABLED` → `explained=389/394`, `warm=204/204`; 50-line limit → `explained=392/394`,
  `warm=204/204`. Clause `w` does not catch either rule.
* **Two freeze defects** (details in §6): (D1) **all 20 frozen controls fail clause `s`** — their selftests print
  `43/43` and the frozen counter requires `N >= 60` (`SELFTEST_MIN`, line 128), so the frozen `reference` control
  does not meet the frozen predicate, contrary to the registration's control requirement; (D2) **no write is
  scored anywhere** — clause `r` traces only `execve/execveat/socket/socketpair/connect` (line 141), clause `i` is
  not printed and is absent from the `met` expression (line 986), and the read-only `.rw` mount only produces
  `EROFS`.

---

## 2. Method (reproducible)

Replay tree (all scratch under `/fast/scratch/hyaku/mado-r48/MutC1Counter/`, deleted after the receipts were
copied out):

```sh
git clone -q --no-checkout --shared <lane> <S>/tree/lane                        # toplevel asserted == <S>/tree/lane
git -C <S>/tree/lane checkout -q 3e6c848a -- tools quality .ufo/waves/round-47/fetch .ufo/waves/round-48/l1-draft
```

The clone is at the freeze revision; the counter reads the tool with `git ls-tree`/`git show` at the scored
revision only (my partial checkout never removes the path from any commit, and every tool variant is a commit whose
`tools/mado-terminal.py` is the variant, created with `hash-object -w` + `update-index --cacheinfo` + `commit-tree`
on top of `3e6c848a`, so no file outside `tools/` is re-written). One cell:

```
python3 -I <counter.py> --repo <S>/tree/lane --rev tool-<name> --work <S>/work/tmp.XXXXXXXX --nonce 4848
```

The clone has to sit two levels down (`<S>/tree/lane`), because the counter refuses a `--work` inside
`dirname(lane_root())` (lines 1005-1007) — first attempt, measured: `PRED-C1-r48: SETUP work dir inside a hidden path
/fast/…/MutC1Counter`.

**Write bounds.** Every shell that writes starts with `ulimit -f 2048` (1 MiB/file). The counter-run wrapper raises
it to `ulimit -f 3072` (1.5 MiB) for one measured reason: the frozen counter itself copies the judge's externals
into each sandbox, and `/usr/bin/gawk` is 1,274,872 B; under 1 MiB the judge aborts on its own copy
(`OSError: [Errno 27] File too large: '/usr/bin/gawk' …` — observed, not inferred), so no cell could be scored at
all. Largest file written under the seat scratch: 299,141 B (a fixture inside the replay clone); largest artifact
produced by a run: 121,552 B (`p0-explain-cmd-const.log`). Peak scratch total: 10,848,382 B (10.3 MiB), far under
the 2 GB budget. No package manager, install, service, compositor, GUI or terminal was touched; every
`xdg-terminal-exec` run is inside the counter's own `bwrap` sandbox with a `--print-*` argv (enforced by the
counter's `check_case`).

---

## 3. Baseline and the frozen control corpus (24 cells)

Baseline (frozen counter × data candidate `.ufo/waves/round-48/l1-draft/mado-terminal.py`, sha256
`1dfde36cfa68beffb6b2bc2ae9cf04875bd48702669812ce3ecd10b986753a92`, which is byte-equal to the tracked
`tools/mado-terminal.py` at the freeze working tree):

```
PRED-C1-r48: cold=190/190 warm=204/204 explained=394/394 generated=230/230 selftest=ok readonly=ok tool=present verdict=TARGET_MET
```

### 3.1 The 20 frozen controls under the frozen counter

`own` = failing fixtures beyond the frozen `reference` control's own baseline (that control fails 7 warm and 14
explain fixtures on the final merged set; see D1/D3 below, so raw counts against it overstate every control).

| control | final line (raw) | own beyond reference | what killed it |
|---|---|---|---|
| `reference` | `cold=190/190 warm=197/204 explained=380/394 generated=230/230 selftest=fail readonly=ok` | — | `s` (43/43), 7 warm, 14 explain — **it does not meet the frozen predicate** |
| `base` (r47 tool) | `cold=190/190 warm=134/204 explained=231/394 generated=210/230 selftest=fail` | w+63, x+149 | `w`,`x`,`g` |
| `always-cold-but-home` | `cold=190/190 warm=139/204 explained=231/394 generated=210/230 selftest=fail` | w+58, x+149 | `w`,`x`,`g` |
| `trust-any` (hash not compared) | `cold=190/190 warm=184/204 explained=340/394 generated=230/230 selftest=fail` | w+14, x+43 | `w` + `x` |
| `hash-names` | `cold=190/190 warm=139/204 explained=295/394 generated=210/230 selftest=fail` | w+58, x+85 | `w`,`x`,`g` |
| `hash-no-date` | same as `hash-names` | w+58, x+85 | `w`,`x`,`g` |
| `hash-no-total` | same as `hash-names` | w+58, x+85 | `w`,`x`,`g` |
| `cache-ignores-enable` | `cold=190/190 warm=197/204 explained=375/394 generated=230/230 selftest=fail` | **w+0**, x+5 (`M-13`,`M-14`,`v2-wi-18-cache-disabled-env`,`v2-wi-19-cache-disabled-no`) | `x` only |
| `no-line-limit` | `cold=190/190 warm=197/204 explained=378/394 generated=230/230 selftest=fail` | **w+0**, x+2 (`M-17`,`v2-mf-11-51-lines`) | `x` only |
| `delegate-ls` | `cold=190/190 warm=197/204 explained=380/394 … readonly=fail` | 0/0/0 | `r` (and inherited `s`) |
| `md5-subproc` | `cold=190/190 warm=197/204 explained=380/394 … readonly=fail` | 0/0/0 | `r` (and inherited `s`) |
| `explain-cache-const` | `… explained=92/394 …` | x+290 | `x` |
| `explain-cmd-const` | `… explained=42/394 …` | x+338 | `x` |
| `writes-cache` | `cold=190/190 warm=197/204 explained=380/394 generated=230/230 selftest=fail readonly=ok` | **0/0/0** | nothing of its own — its write is invisible |
| `mut-desktop-lower` | `… warm=139/204 explained=296/394 generated=218/230 selftest=fail` | w+58, x+84 | `w`,`x`,`g` |
| `mut-no-command-v` | `… warm=195/204 explained=376/394 …` | w+2 (`M-06`,`v2-wi-17-exec-stub-gone`), x+4 | `w`,`x` |
| `mut-cache-fallback` | `… warm=143/204 explained=340/394 generated=218/230` | w+54, x+40 | `w`,`x`,`g` |
| `mut-eof-terminator` | `… warm=196/204 explained=366/394 …` | w+1 (`v2-mf-20-junk-after-term`), x+14 | `w`,`x` |
| `mut-terminator-contains` | `… warm=196/204 explained=377/394 …` | w+1 (same fixture), x+3 | `w`,`x` |
| `mut-warm-ignores-args` | `… warm=186/204 explained=380/394 generated=227/230` | w+11, **x+0** | `w` alone |

Plus the three probes derived from the data candidate (§5) and the empty-revision attack: the frozen counter on a
revision whose `tools/mado-terminal.py` is absent gives
`PRED-C1-r48: cold=0/190 warm=0/204 explained=0/394 generated=0/230 selftest=fail readonly=fail tool=absent
verdict=TARGET_MISSED`.

**No frozen control becomes `TARGET_MET` under any clause mutant.** Measured for the mutants that could plausibly
flip one (`w`, `s`, `r` × `reference`, `w` × `base`):

```
ms-reference   PRED-C1-r48: cold=190/190 warm=197/204 explained=380/394 generated=230/230 selftest=ok  readonly=ok verdict=TARGET_MISSED
mw-reference   PRED-C1-r48: cold=190/190 warm=204/204 explained=380/394 generated=230/230 selftest=fail readonly=ok verdict=TARGET_MISSED
mw-base        PRED-C1-r48: cold=190/190 warm=204/204 explained=231/394 generated=210/230 selftest=fail readonly=ok verdict=TARGET_MISSED
mr-reference   PRED-C1-r48: cold=190/190 warm=197/204 explained=380/394 generated=230/230 selftest=fail readonly=ok verdict=TARGET_MISSED
```

For the other mutants the same conclusion follows from the matrix: a frozen control can only turn `TARGET_MET` if it
passes every clause the mutant leaves intact, and every one of the 20 fails at least one other clause (all 20 fail
`s` and at least one of `w`/`x` (even `delegate-ls`/`md5-subproc`, whose own rule only touches `r`, inherit the
reference's 7 warm and 14 explain failures).

---

## 4. One mutation per clause: the nine counter mutants

All mutants are one documented patch of the frozen counter (`w2/MutC1Counter/patches.txt`, byte-exact files in
`counters/`; each anchor asserted to occur exactly once). `candidate` = the mutant still admits the data candidate.

| clause | mutation | candidate | attacker | frozen verdict | mutant verdict | kill |
|---|---|---|---|---|---|---|
| `a` | revision addressing dropped: the tool is looked up and read from the **worktree**, not at `REV` (lines 921-922 and 931) | MET | revision with **no** `tools/mado-terminal.py` + candidate in the worktree | `tool=absent … verdict=TARGET_MISSED` | `cold=190/190 warm=204/204 explained=394/394 generated=230/230 … TARGET_MET` | **K1** |
| `s` | selftest accepted unconditionally (line 908: `return "ok"`) | MET | `probe-selftest-rc`: candidate whose selftest prints `69/69 passed` and **exits 1** | `… selftest=fail … TARGET_MISSED` | `… selftest=ok … TARGET_MET` | **K1** |
| `f` | every cold fixture accepted (line 941: `ok = True`) | MET | `probe-f-percent`: candidate with the `%%`→`%` freecode collapse removed | `cold=188/190 … explained=392/394 generated=225/230 … MISSED` | `cold=190/190 … explained=392/394 generated=225/230 … MISSED` | **K2** (f 188→190; `x`,`g` still reject) |
| `w` | always-accept warm (lines 951-952: premise call and comparison both dropped) | MET | `probe-w-hit-content`: candidate whose `--print-content` on a cache **hit** reads a wrong path | `warm=203/204` (only `v2-ws-04-content-mut`), `TARGET_MISSED` | `warm=204/204 … TARGET_MET` | **K1** |
| `w` (same mutant) | — | MET | `mut-warm-ignores-args` (frozen control) | `warm=186/204 … TARGET_MISSED` | `warm=204/204`, still `explained=380/394 generated=227/230 … MISSED` | K2 (w 186→204) |
| `x` | the two-item `--observed` capture dropped (line 709-711) | MET | `probe-x-observed-prefix`: candidate whose `explain --observed` accepts a prefix of its own capture (ignores the command line) | `explained=47/394 … TARGET_MISSED` | `explained=394/394 … TARGET_MET` | **K1** |
| `x` (same mutant) | — | MET | `explain-cache-const` (frozen control) | `explained=92/394` | `explained=92/394` | no change (the field comparison still catches it) |
| `g` | every generated case accepted (lines 971 and 978: `g_ok += 1`) | MET | `probe-f-percent` | `generated=225/230 … MISSED` | `generated=230/230`, still `cold=188/190 explained=392/394 … MISSED` | K2 (g 225→230) |
| `g` (same mutant) | — | MET | `base` (frozen control) | `generated=210/230` | `generated=230/230`, still `warm=134/204 explained=231/394` | K2 (g 210→230) |
| `i` | no-write guard removed: `mode = "--bind"` for the tool tree (line 279) | MET | `probe-writes`: candidate that writes `<cache>.probe-write` after a cold selection and swallows `OSError` | **`TARGET_MET`** | `TARGET_MET` | **equivalent — nothing was enforced** |
| `i` | host `/etc` bound into the tool sandbox only (line 285) | **MISSED** | (the subject itself) | — | `cold=190/190 warm=144/204 explained=304/394 generated=210/230` | self-defeating, not silent |
| `r` | `readonly = "ok"` whatever the trace saw (line 983) | MET | `probe-r-spawn2`: candidate whose `gen_hash` runs `ls -LRl` as a process (model fallback keeps its selftest at 69/69) | `… selftest=ok readonly=fail … TARGET_MISSED` (`trips=2493`) | `… selftest=ok readonly=ok … TARGET_MET` | **K1** |
| `r` (same mutant) | — | MET | `delegate-ls`, `md5-subproc` (frozen controls) | `readonly=fail`, MISSED | `readonly=ok`, still `selftest=fail warm=197/204 explained=380/394`, MISSED | K2 (r fail→ok) |

Two measurements are in `finals.txt` but not in the table: the first spawn probe (`probe-r-spawn`, delegation
without a fallback) crashes its own selftest inside the sandbox (the selftest environment has no `ls` on `PATH`:
`clause=s rc=1 last=''`), so `t-r-spawn` (`selftest=fail readonly=fail trips=2463`) and `mr-r-spawn`
(`selftest=fail readonly=ok`, `TARGET_MISSED`) cannot attribute the kill to `r` alone. `probe-r-spawn2` adds the
model fallback (69/69 in the sandbox) and is the clean `r`-only attacker used above.

Exact final lines (all 61 cells are in `finals.txt`; the clause-mutant cells):

```
ma-absent     PRED-C1-r48: cold=190/190 warm=204/204 explained=394/394 generated=230/230 selftest=ok readonly=ok tool=present verdict=TARGET_MET
ms-probe      PRED-C1-r48: cold=190/190 warm=204/204 explained=394/394 generated=230/230 selftest=ok readonly=ok tool=present verdict=TARGET_MET
mw-probe      PRED-C1-r48: cold=190/190 warm=204/204 explained=394/394 generated=230/230 selftest=ok readonly=ok tool=present verdict=TARGET_MET
mx-probe      PRED-C1-r48: cold=190/190 warm=204/204 explained=394/394 generated=230/230 selftest=ok readonly=ok tool=present verdict=TARGET_MET
mf-probe      PRED-C1-r48: cold=190/190 warm=204/204 explained=392/394 generated=225/230 selftest=fail readonly=ok tool=present verdict=TARGET_MISSED
mg-probe-f    PRED-C1-r48: cold=188/190 warm=204/204 explained=392/394 generated=230/230 selftest=fail readonly=ok tool=present verdict=TARGET_MISSED
miw-probe     PRED-C1-r48: cold=190/190 warm=204/204 explained=394/394 generated=230/230 selftest=ok readonly=ok tool=present verdict=TARGET_MET
mie-candidate PRED-C1-r48: cold=190/190 warm=144/204 explained=304/394 generated=210/230 selftest=ok readonly=ok tool=present verdict=TARGET_MISSED
mr-r-spawn2   PRED-C1-r48: cold=190/190 warm=204/204 explained=394/394 generated=230/230 selftest=ok readonly=ok tool=present verdict=TARGET_MET
```

One caveat on `f`/`g` survival, stated as measured, not assumed: no attacker in this wave fails `f` alone or `g`
alone. `probe-f-percent` fails `f` **and** `x` (its percent handling also changes the `--print-cmd` capture) and
`g` (generated case `g015`); `probe-w-hit-content` is the only tool that fails a single warm arm and it fails `w`
only, which is why `f` has no analogue. Clause `x` re-checks every fixture's output through the tool's own
`--observed` capture, so an output difference on a cold fixture is always also an `x` failure.

---

## 5. The six named attacks (three are the frozen controls, three are candidate-derived)

| named attack | implementation measured | final line | killed? |
|---|---|---|---|
| always-accept warm | counter mutant `w` (§4) | `warm=204/204 … TARGET_MET` for the warm-only probe | yes, K1 by `probe-w-hit-content` (frozen: `warm=203/204 … MISSED`); every frozen control stays `MISSED` under it because all fail `s` and/or `x` |
| remove hash comparison | `probe-hash-off`: data candidate without the `gen_hash() != fields[0]` arm (`patches3.txt`) | `PRED-C1-r48: cold=190/190 warm=190/204 explained=351/394 generated=230/230 selftest=fail readonly=ok tool=present verdict=TARGET_MISSED` | **yes** — own w+14, x+43, and the tool's own selftest drops to 67/69. Frozen analogue `trust-any` has the same own deltas (w+14, x+43) |
| remove `XTE_CACHE_ENABLED` branch | `probe-enable-off` | `PRED-C1-r48: cold=190/190 warm=204/204 explained=389/394 generated=230/230 selftest=fail readonly=ok tool=present verdict=TARGET_MISSED` | **yes, but only by `x` (5 explain cases) and the selftest (68/69). Clause `w` is 204/204.** Frozen analogue `cache-ignores-enable`: own w+0, x+5 |
| skip line limit (50th line) | `probe-linelimit-off` | `PRED-C1-r48: cold=190/190 warm=204/204 explained=392/394 generated=230/230 selftest=fail readonly=ok tool=present verdict=TARGET_MISSED` | **yes, but only by `x` (2 explain cases) and the selftest (68/69). Clause `w` is 204/204.** Frozen analogue `no-line-limit`: own w+0, x+2 |
| ignore observed command | counter mutant `x` (§4) | `explained=394/394 … TARGET_MET` for `probe-x-observed-prefix` | **not killed by the frozen corpus** (all frozen controls stay `MISSED`: the two-item capture is unexercised); killed K1 by `probe-x-observed-prefix` (`explained=47/394` on the frozen counter) |
| remove no-write tripwire | counter mutant `i-no-write-tripwire`; `probe-writes` (candidate + one write rule) | `PRED-C1-r48: cold=190/190 warm=204/204 explained=394/394 generated=230/230 selftest=ok readonly=ok tool=present verdict=TARGET_MET` — **under the frozen counter, unmutated** | **no — there is no no-write tripwire to remove.** See D2 |

---

## 6. Findings for the L1

**D1 — the frozen control corpus does not meet the frozen predicate (freeze defect, pre-data).**
All 20 frozen controls print `MADO_TERMINAL_SELFTEST: 43/43 passed`; the frozen counter requires `N >= 60`
(`SELFTEST_MIN`, line 128; the w1 draft had `30`, and the freeze raised it). Measured, 20 identical clause lines
(`selftests.txt`):

```
20  PRED-C1-r48 clause=s rc=0 last='MADO_TERMINAL_SELFTEST: 43/43 passed'
 2  PRED-C1-r48 clause=s rc=0 last='MADO_TERMINAL_SELFTEST: 69/69 passed'   (the data candidate, and probe-w-hit-content)
 1  PRED-C1-r48 clause=s rc=1 last='MADO_TERMINAL_SELFTEST: 69/69 passed'   (probe-selftest-rc, by construction)
```

Consequences: `reference.py` (registration: "reference.py must meet") scores
`cold=190/190 warm=197/204 explained=380/394 generated=230/230 selftest=fail readonly=ok verdict=TARGET_MISSED`; its
7 warm failures are the six `v2-hu-*` HOME-unset fixtures plus `L1-10-desk-echo-n-edit`, and its 14 explain failures
are those plus `E-01`/`L1-06`/`L1-07` and the HOME-unset set. So the control column published in
`w1/ExecControlsC1.md` was produced on 32 warm fixtures and never re-scored on the frozen 204. The registration's
own rule ("a control that meets triggers a fixture/counter repair before freeze") is not what failed here — the
reference *misses*; what it means is that the control matrix must be re-derived on the frozen set before any
"controls kill X" statement can use it.

**D2 — the no-write guard scores nothing; a writing tool is admitted (freeze defect, pre-data).**
`probe-writes` = the data candidate + one rule ("after a cold selection, write `<cache>.probe-write`, swallow
`OSError`") scores **`TARGET_MET`** on the unmutated frozen counter. The frozen `writes-cache` control has clause
tallies *identical* to the frozen `reference`'s (own 0/0/0) and `readonly=ok`; the only reason it is `MISSED` is the
inherited `s`/`w`/`x` defects of D1. Direct sandbox measurement (`probe-write.txt`, the counter's own `Box`):

```
tool=candidate    rw=ro rc=0 stdout='foot\n' cache_exists=False cache_bytes=0 trips=[]
tool=candidate    rw=rw rc=0 stdout='foot\n' cache_exists=False cache_bytes=0 trips=[]
tool=writes-cache rw=ro rc=0 stdout='foot\n' cache_exists=False cache_bytes=0 trips=[]
tool=writes-cache rw=rw rc=0 stdout='foot\n' cache_exists=True  cache_bytes=205 trips=[]
```

i.e. the control really writes when the tree allows it (205-byte cache), the read-only `.rw` only turns the write
into `EROFS` (which the tool swallows), and `TRACE_SET` (line 141) cannot see a write. Clause `i` is moreover not
reported at all: there is no `clause=i` line and the `met` expression (line 986) does not mention `i`. Removing the
guard (`i-no-write-tripwire`) is therefore an equivalent mutant.

**D3 — two warm rules are scored only by clause `x`, never by clause `w`.** Measured own-deltas against
`reference`: `cache-ignores-enable` w+0 / x+5, `no-line-limit` w+0 / x+2; the candidate-derived `probe-enable-off`
and `probe-linelimit-off` both reach `warm=204/204`. This is exactly the gap `w1/ExecControlsC1.md` F5 named (a
disabled-cache or malformed-cache fixture whose *printed answer* equals the cold answer is inert for `w`); the
frozen warm set still has no `disabled` fixture whose answer differs from the cold one. Note the contrast with the
hash rule, which `w` does carry (`trust-any`/`probe-hash-off`: w+14).

**D4 — clause `i` is a safety statement, not a discriminating one.** The only behavioural half of clause `i` is the
read-only `.rw`, and D2 shows it scores nothing. The mount-set half is load-bearing for *determinism* but in the
opposite direction: binding host `/etc` into the tool sandbox (`i-host-etc-bound`) makes the data candidate itself
miss (`warm=144/204 explained=304/394 generated=210/230`) because the tool's `ls` model starts resolving
`pwd`/`grp` names and TZ data that the oracle's sandboxed `ls` cannot see. Such a mutation is therefore detected by
the subject, not by a control.

**D5 — clause `f` and clause `g` are redundant with `x` (sound, but not load-bearing).** No attacker fails `f`
alone or `g` alone; both mutants survive at verdict level (K2 evidence: `f` 188→190, `g` 225→230 / 210→230). The
harm-watch clause `f` (190 r47 records) is thus protected in practice by clause `g`'s 150 generated cold cases and
by clause `x`, and `g` by `f`/`w`/`x`. If the L1 wants a clause to be independently falsifiable, the attacker has to
differ on a surface `x` does not re-read (only `--print-content` and `--print-id`/`--print-path`-only argvs qualify
today, and those are `w`-side).

**D6 — clause `r` is load-bearing and cleanly falsifiable** (`probe-r-spawn2`: only `readonly=fail`, `trips=2493`,
everything else passes). It is the one clause whose frozen controls (`delegate-ls`, `md5-subproc`) were built as
`r`-only attackers, and it works — but they cannot show it at verdict level because of D1.

---

## 7. What this wave did not measure (residuals)

* No mutation of the fixture set itself, the pin, the sandbox `Box` construction beyond the two `i` mutants, or the
  `--work`/repo guards. No attempt to make the counter crash (a crash is not a verdict; the two setup failures I
  hit are reported above).
* `f`/`g` have no isolating attacker by construction (D5); I did not fabricate a fixture-specific tool to force
  one, because that would test the harness path, not the clause.
* Nonce is fixed at 4848 for all cells (comparability). One nonce does not exhaust `gen_case`/`gen_warm_case`;
  the r47/r48 seat receipts already show two nonces agreeing on the candidate.
* The `i-host-etc-bound` mechanism was localised only by its effect (warm 144/204); the exact `pwd`/`grp` vs TZ
  split was not separately probed.
* Clause `i`'s mount set remains unobservable to any tool mutant that does not read host paths — a tool cannot use
  host information the oracle lacks *and* match the oracle, so no such attacker was attempted.

---

## 8. Evidence

`w2/MutC1Counter/`: `README.md`, `matrix.tsv` (61 cells), `finals.txt` (verbatim final lines), `own.tsv`
(per-cell failures beyond the `reference` baseline), `selftests.txt`, `probe-write.txt`, `patches.txt`,
`patches2.txt`, `patches3.txt`, `patches3b.txt`, `counters/` (9 mutants), `probes/` (10 probes), `logs/` (all 61
counter logs + runner index), `build/` (builders, runner, aggregator, plans), `sha256s.txt`.

Scratch `/fast/scratch/hyaku/mado-r48/MutC1Counter/` held the replay clone and all run work dirs; it was removed
after the receipts were copied out. No file was written in the lane outside this seat's two paths, no git or jj
state in the lane was touched (the clone is `<S>/tree/lane`, `rev-parse --show-toplevel` asserted at creation), and
no package manager, service, GUI or terminal was used.
