# Live-state tool ledger — `tools/` instruments, round 47

Seat: `ScrToolLedger` (round-47 w1, considerthese 2026-10-26 proposal 2).
Base: `c24adef2632672325a4eef3e3492f6716ccb6d14` (round-47 dispatch), lane
`/home/vgpnk/Projects/shokunin/mado-shokunin`.
Every count below was produced at that commit by the commands quoted beside it; the receipt
files under `receipts/` in this seat hold the raw output.

**What this ledger is for.** `PROVINCE.md:20-32` says *what each instrument may read and write*;
`SKILL.md` says *how to call it*. Neither says **whether the bytes now on disk have ever been run
against this host**. This file adds that third column, because a tool with a green selftest and a
stale live receipt is exactly the shape a reader mistakes for current host agreement.

---

## 1. What counts as a live receipt

A **live run** is an execution of the tool's bytes against real host state, committed with enough
identity to bind it: the tool's `sha256` (or its commit) and the host-side input it consumed.

| class | means | counted as live? |
|---|---|---|
| `HOST-PROBE` | the tool starts read-only host processes itself (`ss -xpa`, `journalctl`, `hyprctl … -j`, `pgrep`) | yes |
| `HOST-DUMP JOIN` | the operator pipes a live `hyprctl … -j` dump into the tool | yes |
| `SESSION-RECORD` | the tool reads the session's own transcript JSONL | yes |
| `CONFIG-ONLY` | reads config bytes only; *scored* against a compositor (host dump or nested instance) | yes, for the scoring run only |
| `ARTIFACT` | reads lane paperwork only; no host state by construction | no — never live, and that is the tool's design |

A `--selftest` pass, a mutation-oracle run over fixtures, or a fixture replay is **not** a live
run. All three are recorded here as "last executed", never as host evidence.

### The lookup, and why the obvious one is wrong

The round-47 brief names `git grep -l` over `.ufo/waves/*/receipts`. That search finds **4 of the
10** live receipts in this lane:

```
$ find .ufo/waves -type f -path '*/receipts/*' | wc -l          # 1515 files, 89 receipts dirs
$ grep -rl 'MADO_VERIFY: CLEAN\|live=hyprctl' .ufo/waves --include='*' | grep /receipts/
```
Live evidence is spread over four directories, by era, not by convention:

| directory | live receipts found there |
|---|---|
| `.ufo/waves/round-NN/receipts/` | eventq (r38), geometry (r44), monitors (r45), devices (r46) |
| `.ufo/waves/round-NN/evidence/` | tripwire (r19), binds (r25), anims (r26), wsrules (r27) |
| `.ufo/waves/round-NN/fetch/` | options (r40) |
| `.ufo/evidence/round-NN/` | verify (r12) |

So the ledger's own search rule is: **any committed file**, narrowed by the tool's verdict token
(`MADO_<NAME>:`, `live=`, `tool=… sha256:`) or by its own filename (`*/receipts/live-*`,
`*eventq-live*`), then confirmed by reading the receipt's tool hash. The naive
`receipts`-only rule is itself a finding (F2 below).

---

## 2. The ledger

`bytes` = does the receipt's recorded tool `sha256` still equal `sha256sum tools/<tool>`?

### 2a. Instruments that read host state (9)

| tool | class | the question it answers | reads | last live run (receipt:line, round, commit) | verdict there | bytes | operator runs |
|---|---|---|---|---|---|---|---|
| `mado-eventq.py` | HOST-PROBE | who is subscribed to socket2, who is falling behind, did the compositor drop anyone | `ss -xpa`, session `hyprland.log`, `journalctl --user -u hyprland` | `.ufo/waves/round-38/receipts/eventq-live.txt:8` · r38 · `4aad0e8d` | `CLEAN` — `subscribers=2 overflow=0 write_fail=0 markers_observable=no` (exit 0) | **yes** `436f550e…` | `python3 -I tools/mado-eventq.py` (`--ss-file`/`--journal-file`/`--snapshot-out` to replay a capture) |
| `mado-options.py` | HOST-PROBE (`--live`) | which file owns each option key, and does the running compositor agree | config tree + `hyprctl getoption -j` per declared key | `.ufo/waves/round-40/fetch/census-receipt.txt:7` · r40 · `91f0a2b8` | `agreement=62 agreement*=8 mismatch=0 config-only=0 live-default=0` over 70 keys | **yes** `63b5ebd9…` | `python3 -I tools/mado-options.py --home ~/.config/.. --live` or `--getoption DUMP` |
| `mado-globals.py` | HOST-PROBE (`--live`) | which Wayland globals the compositor advertised to its portal, per session | portal unit journal (`-o short-iso`) | **NONE** — no receipted run on real journal output; the only host input is the captured journal `.ufo/waves/round-41/fetch/xdph-journal.txt` (`bf8fa91a…`, 19,130 B) | — (last executed: `--selftest 63/63`, `.ufo/waves/round-46/w1/ExecHarmBase/receipts/base-tools-selftests.txt:8`) | — | `python3 -I tools/mado-globals.py --live` or `--journal-file PATH [--expect NAME] [--diff]` |
| `mado-geometry.py` | HOST-DUMP JOIN | does a `size W H` window rule match the size the compositor reports for that class | rules file + `hyprctl clients -j` | `.ufo/waves/round-44/receipts/live-geometry-host-r44.txt:5` · r44 · `e4678921` | `NO_MATCHING_CLIENT` — `rules=1 clients=3 matched=0 differ=0` (exit 3): no gkeep window was mapped | **yes** `1da3ddaed…` | `hyprctl clients -j \| python3 -I tools/mado-geometry.py --clients - --rules ~/.config/hypr/gkeep.conf` |
| `mado-monitors.py` | HOST-DUMP JOIN | does each output run the mode/position/scale/transform its `monitor =` line declares | monitor rules + `hyprctl monitors all -j` | `.ufo/waves/round-45/receipts/live-monitors-host-r45.txt:8` · r45 · `ee6659b9` | `OK` — `outputs=1 matched=1 agree=1 differ=0` | **yes** `2f007417…` | `hyprctl monitors all -j \| python3 -I tools/mado-monitors.py --monitors - --config ~/.config/hypr/monitors.conf` |
| `mado-devices.py` | HOST-DUMP JOIN | does each keyboard run the XKB names its config declares; does each mouse report its block's scroll factor | input/device lines + `hyprctl devices -j` | `.ufo/waves/round-46/receipts/live-devices-host-r46.txt:21` · r46 · `1001bda0` | `OK` — `keyboards=10 agree=9 virtual=1 mice=4 mice_differ=0 differ=0` | **yes** `3a803689…` | `hyprctl devices -j \| python3 -I tools/mado-devices.py --devices - --config …` |
| `mado-verify.sh` | HOST-PROBE | do the declared config planes match the live bytes and the compositor's own answers (one `CLEAN`/`DIVERGED` line) | config files + `hyprctl` read verbs (version, instances, configerrors, getoption, binds, monitors, layers) | `.ufo/evidence/round-12/after.txt:80` (verdict + tool sha at `:86`), itemised in `.ufo/evidence/round-12/gate-live-after.txt:2` (`mode: live`) · r12 · `5174e15f` | `CLEAN (52 pass, 8 notes; file + live planes verified read-only)` | **no** — receipt ran `ea798ad0…`, file is `050efc72…` | `bash tools/mado-verify.sh` (live) / `--no-live` (file plane only) / `--selftest` |
| `mado-tripwire.py` | SESSION-RECORD | which mutating / package / probe commands a seat *issued* in its OMP transcripts | session `.jsonl` (`toolCall` blocks only) | `.ufo/waves/round-19/evidence/final/tripwire-seat-scan.txt:6` · r19 · `c7693eb2` | `findings` — `live_probe 3, vcs_write 164` on the MadoR19 seat transcripts (exit 1) | **no** — receipt ran `367be947…`, file is `cd9da20c…` | `python3 -I tools/mado-tripwire.py --scan <session-dir>/<Lane>R<N>` |
| `mado-binds.py` | CONFIG-ONLY, scored vs the host table | the 18-field `hyprctl binds -j` table a config tree builds | config tree only | `.ufo/waves/round-25/evidence/c1-after-v4-ef94763c.txt:5` · r25 · `90224671` | `live=hyprctl binds -j sha256:9a47199e…` (192 live binds); `ORACLE_CHECK base_vs_live missing=0 extra=0` at `:7`; `cases_pass=41/41 verdict=TARGET_MET` at `:50` | **no** — receipt ran `9efa1136…`, file is `0cda0e6f…` (round-26 extension) | `python3 -I tools/mado-binds.py --home DIR` |

### 2b. Config-only resolvers whose only scoring was a nested compositor (2)

Neither starts a process or opens a socket; both were scored by a counter that ran a **real
Hyprland 0.56.2** on a copy of the host config tree and read it back with `hyprctl … -j`. That is
live-compositor evidence, not host-session evidence, and it is not re-runnable today: the harness
scratch is gone (`/fast/scratch/hyaku/mado-r26/wlroots/build`, `/fast/scratch/hyaku/mado-r2*-oracle-slots`
do not exist), so the receipt is the durable evidence.

| tool | the question | reads | last scored run | verdict there | bytes |
|---|---|---|---|---|---|
| `mado-anims.py` | the `[nodes, beziers]` table `hyprctl animations -j` prints, from config bytes | config tree | `.ufo/waves/round-26/evidence/c1-after-v2-2b3487f7.txt:4` · r26 · `ca135237` (`ORACLE_VERSION efb5099…` at `:8`) | `CASES 41/41`, `ORACLE_CHECK base_twice equal nodes=35 beziers=6` → `TARGET_MET` | **yes** `2beda3f7…` |
| `mado-wsrules.py` | the `hyprctl workspacerules -j` array, from config bytes | config tree | `.ufo/waves/round-27/evidence/c1-after-20022a65.txt:2` · r27 · `98ebd5b0` (`ORACLE_VERSION efb5099…` at `:6`) | `cases_pass=41/41 TARGET_MET`; host BASE = 0 workspace rules | **yes** `dcf5c8c0…` |

### 2c. Artifact gates — no host state by construction (3)

Listed so the ledger is complete, and so nobody reads their green as host agreement. Each reads
caller-supplied JSON only (`PROVINCE.md:24`, `:26`, `:27`); their last exercise is a fixture or
frozen-bundle run, never a live probe.

| tool | the question | reads | last exercise (r46) | note |
|---|---|---|---|---|
| `mado-action-plan.py` | is a *declared* action plan allowed by the pinned policy | plan JSON + `safety-policy.json` | `.ufo/waves/round-46/w1/ExecHarmBase/receipts/base-registered-gates.txt:2` — `MADO_PLAN: frozen_match` | never executes the supplied argv |
| `mado-assessment.py` | do an assessment bundle's assertions hold arithmetic | bundle JSON + `--root` | same file, `assessment-selftest` block, `EXIT=0` | no chronology/authn authority |
| `mado-evidence-audit.py` | do an evidence bundle's artifact arithmetic and labels hold | bundle JSON + snapshot root | same file, `evidence-audit-selftest` block, `EXIT=2` (`could-not-evaluate`, by design for that case) | not execution truth |

---

## 3. Counts (re-derive with the commands in `receipts/`)

| # | statement | command |
|---|---|---|
| 14 | tracked instruments: 13 `tools/mado-*.py` + `tools/mado-verify.sh` | `ls tools/mado-*.py tools/mado-verify.sh \| wc -l` |
| 9 | instruments that read host state (2a) | table above |
| **1** | host-facing instrument with **no live receipt at all**: `mado-globals.py` (the three gates of 2c have none by construction) | `grep -rn 'MADO_GLOBALS: sessions=' .ufo/waves` returns fixture rows only |
| 8 | instruments with a committed live receipt (2a) | table above |
| **3** | live receipts that predate the tool's current bytes: `mado-verify.sh` (r12), `mado-tripwire.py` (r19), `mado-binds.py` (r25) | compare receipt `sha256` with `sha256sum tools/<tool>` |
| 5 | host-facing receipts still bound to the current bytes: eventq, options, geometry, monitors, devices | same |
| 4 of 10 | live receipts reachable by a `.ufo/waves/*/receipts`-only search | `receipts/live-receipts.txt` paths |
| 3 | artifact gates with no host input by design (2c) | `PROVINCE.md:24-27` |
| 2 | resolvers scored only by a nested compositor whose harness scratch is gone (2b) | `ls -d /fast/scratch/hyaku/mado-r26/wlroots/build` → absent |

**The one-line answer to "how live is this instrument set?":** five of the nine host-facing
instruments carry host-live receipts bound to their current bytes; one (`globals`) has none, and
three (`verify`, `tripwire`, `binds`) carry live receipts from rounds 12, 19 and 25 whose recorded
tool hash no longer matches the file.

---

## 4. Findings

**F1 — `mado-globals.py` has no live receipt.** Its `--live` path is the only read of the portal
journal in the lane, and the entry that cites it (`knowledge/hyprland-focus-grab-r41.md`) rests on
a *captured* journal (`.ufo/waves/round-41/fetch/xdph-journal.txt`, `bf8fa91a…`), not on a run of
the tool against a live journal. The capture date (2026-10-25) is the entry's evidence; the tool's
own invocation on it is unreceipted. Cheap closure: one `--journal-file` run over that committed
capture, receipted with the tool hash — a hermetic run, no host probe.

**F2 — the brief's own lookup rule finds 4 of the 10 live receipts, and misses 6.** `receipts/` only began
carrying `live-*` names at round 43; the earlier live evidence sits in `evidence/`, `fetch/` and
`.ufo/evidence/`. Any future check that searches one directory will report a false "no live run"
for five instruments.

**F3 — three live receipts no longer describe the bytes on disk.** `mado-verify.sh` (live r12 vs
file last changed at `7b4839d3`), `mado-tripwire.py` (live r19 vs `3df10626`), `mado-binds.py`
(live r25 vs the round-26 environment-seeding extension). Each file's *current* bytes do have
non-live evidence (r46 selftest sweep for verify/action-plan/globals/geometry/monitors/options;
r22 oracle runs for tripwire at the current hash), so this is a live-vs-hermetic gap, not an
unmeasured tool. `mado-verify.sh` is the worst of the three: it is the lane's standing verdict
gate, its `CLEAN` line says "file + live planes", and the last receipt that could say that is 35
rounds old.

**F4 — the nested-compositor harness is not reproducible.** `anims` and `wsrules` (and the
`binds` counter) were scored against a nested Hyprland built on scratch
(`/fast/scratch/hyaku/mado-r26/wlroots/build`, `…/mado-r25-oracle-slots`), both now absent. Their
receipts are sound as history; the counters cannot be re-run from the repo alone. `knowledge/`
should say so where it offers a recheck command (e.g. `workspace-rules-r27.md`'s
`python3 -I .ufo/waves/round-27/c1/count-v4.py REV` will fail on `ORACLE_FAIL`/missing harness
before it measures anything).

**F5 — the instruments that start processes name them, and the ones that do not start none.**
Checked by counting `subprocess`/`Popen` sites and reading each one (`receipts/live-receipt-paths.txt`):
eventq 8 (`ss`, `journalctl`), globals 6 (`journalctl` under `--live` only), options 7 (`hyprctl`
under `--live` only; the other is the selftest child), tripwire 20 (all in the `--selftest` child
path — the scan path itself starts nothing), geometry/monitors/devices 0 (stdin and files only).
`mado-verify.sh` is bash: it invokes `hyprctl`, `systemctl --user`, `pgrep` and three `omarchy`
read subcommands directly, which its own header lists. This supports the round-23 tool inventory
(`PROVINCE.md:20-32`), with no instrument reading beyond its stated row.

---

## 5. Draft — README section for `corpus/README.md`

Insert after the **Province routes** table (before `## Frontier`). Wording follows the file's
existing "navigation, not verdict" stance.

> ## Instruments — what has actually been run (`tools/`)
>
> `PROVINCE.md:20-32` says what each instrument may read; `SKILL.md` says how to call it. This
> table says only one more thing: **whether the bytes now on disk have been run against this
> host, and what the receipt said.** It is a navigation aid, not a health verdict — a `CLEAN` row
> below is the verdict of *that round*, never of today.
>
> | Instrument | Question | Last live run | Verdict there | Bound to the current file? |
> |---|---|---|---|---|
> | `tools/mado-eventq.py` | who is on socket2, who is behind, who was dropped | `.ufo/waves/round-38/receipts/eventq-live.txt` (r38) | `CLEAN`, 2 subscribers | yes |
> | `tools/mado-options.py --live` | which file owns each option key; does the compositor agree | `.ufo/waves/round-40/fetch/census-receipt.txt` (r40) | 62 agree, 8 shadowed, 0 mismatch | yes |
> | `tools/mado-globals.py` | which Wayland globals the portal was told about | **none** — only the captured journal `.ufo/waves/round-41/fetch/xdph-journal.txt` | — | — |
> | `tools/mado-geometry.py` | does a `size` rule match the size reported for that class | `.ufo/waves/round-44/receipts/live-geometry-host-r44.txt` (r44) | `NO_MATCHING_CLIENT` (no window mapped) | yes |
> | `tools/mado-monitors.py` | does each output run its declared mode/pos/scale/transform | `.ufo/waves/round-45/receipts/live-monitors-host-r45.txt` (r45) | `OK`, 1 AGREE | yes |
> | `tools/mado-devices.py` | do keyboards run the declared XKB names; do mice report their block's scroll factor | `.ufo/waves/round-46/receipts/live-devices-host-r46.txt` (r46) | `OK`, 9 AGREE + 1 virtual | yes |
> | `tools/mado-verify.sh` | one verdict over the declared config planes | `.ufo/evidence/round-12/after.txt` (r12; itemised in `gate-live-after.txt`) | `CLEAN (52 pass, 8 notes)` | **no** — receipt precedes the current file |
> | `tools/mado-tripwire.py` | which host commands a seat issued in its transcripts | `.ufo/waves/round-19/evidence/final/tripwire-seat-scan.txt` (r19) | `findings` (3 live probes) | **no** |
> | `tools/mado-binds.py` | the `hyprctl binds -j` table from config bytes | `.ufo/waves/round-25/evidence/c1-after-v4-ef94763c.txt` (r25) | `41/41`, vs 192 live binds | **no** |
> | `tools/mado-anims.py` / `tools/mado-wsrules.py` | the `animations` / `workspacerules` tables from config bytes | r26 / r27 `evidence/c1-after-*.txt` | `41/41` each vs a nested Hyprland | yes (harness scratch gone) |
> | `mado-action-plan` / `mado-assessment` / `mado-evidence-audit` | declared-plan, assessment and evidence-artifact gates | `.ufo/waves/round-46/w1/ExecHarmBase/receipts/base-registered-gates.txt` | `frozen_match` / selftests | no host input by design |
>
> Rule of use: a row marked **no** or **none** is a re-run task, not a licence to quote the old
> verdict in the present tense. The `receipts/live-*` names (r43 onward) and the older
> `evidence/`, `fetch/`, `.ufo/evidence/` names are all valid locations; a search restricted to
> `receipts/` misses six of the ten receipts above.

---

## 6. Proposed QUALITY criterion (91)

Next free number in `corpus/QUALITY.md` is 91. Proposal, in the file's own shape:

> 91. Every tracked instrument under `tools/` carries exactly one row in the live-state ledger
> (`corpus/README.md` § Instruments, detail in the round's `w1/ScrToolLedger/ledger.md`) naming its
> last live run as a committed `path:line`, or the literal marker `none` with the reason; a row is
> **stale** when the receipt's recorded tool `sha256` differs from `sha256sum tools/<tool>`, and a
> commit that changes an instrument's bytes resets its row to `stale` in the same commit unless it
> also lands a live receipt for the new bytes. A selftest, a fixture replay or a mutation-oracle run
> is not a live run and never clears a row. Check:
> `python3 -I .ufo/waves/round-47/w1/ScrToolLedger/check-ledger.py --repo . --rev <REV>` prints
> `LEDGER: ok=<n> stale=<n> none=<n> missing=<n> mismatch=<n> unbound=<n> missing_receipt=<n>`
> `instruments=<n>` and exits 1 unless every instrument has a row and every row's declared status
> equals the status re-derived from `sha256sum` of the tool at `<REV>` (a ledger may *declare*
> a `stale` row; it may not declare it `ok`). Shown able to fail (§9): a copy with the `binds` row
> changed from `stale` to `ok` reads `mismatch=1`, exit 1; a copy with the `globals` row deleted
> reads `missing=1`, exit 1; the pristine ledger reads
> `ok=7 stale=3 none=4 missing=0`, exit 0.

Why this criterion and not a broader one: it is the only one that makes the *absence* of live
evidence visible. The existing bar (criteria 7, 9, 13, 24) binds a claim to *a* receipt with its
producer hash, but none of them notices that the receipt is eight rounds older than the file, and
none of them notices that a tool has no receipt at all.

---

## 7. Limits of this ledger

- It reads **committed** evidence. A live run made after `c24adef` (this wave's own seats, for
  instance) is invisible here; that is exactly what the `stale` marker is for.
- "Live" is judged from the receipt's own text (`mode: live`, a `live=` line, a `hyprctl` pipe, a
  transcript path) plus its tool hash. A receipt that lied about its mode would be recorded as
  live; I did not re-run anything to check.
- The counts of receipt files (1515 files / 89 directories at 2026-10-26T18:48-03:00) are a moving
  target during the wave — other seats were writing receipts while I counted. The *set* of live
  receipts named here is stable; the denominators are dated.
- Session material stays shape-only: no window title, device serial, process table or
  home-directory listing is reproduced here. The devices receipt's device *names* are not quoted;
  only its verdict line is.
- The criterion's checker (`check-ledger.py`, in this seat) is a seat instrument: it proves the
  ledger is *consistent with the receipts*, not that the receipts are true (criterion 25 boundary).

## 8. Machine-readable rows (the block `check-ledger.py` reads)

Format: `tool<TAB>declared-status<TAB>receipt<TAB>tool-sha256-recorded-in-that-receipt`
(`none` rows carry `-` twice). The checker re-derives `ok`/`stale` from `sha256sum tools/<tool>`
and requires the declared value to equal the derived one; it reads the block below, not the tables.

<!-- ledger-rows
# tool	declared	receipt	tool-sha256-recorded-in-receipt
mado-eventq.py	ok	.ufo/waves/round-38/receipts/eventq-live.txt	436f550e9939a783b7b95d154d099b788ad9daaed2282e19de89413e39371f24
mado-options.py	ok	.ufo/waves/round-40/fetch/census-receipt.txt	63b5ebd9446405ad0b29a79940244b45b145312cddb30b5e827250ed571fef13
mado-globals.py	none	-	-
mado-geometry.py	ok	.ufo/waves/round-44/receipts/live-geometry-host-r44.txt	1da3ddaed0d6e3cca32d3724daeb4a7fbd14939946ad57ab8db34bc0b2e31ff4
mado-monitors.py	ok	.ufo/waves/round-45/receipts/live-monitors-host-r45.txt	2f007417ae9efa43c7c3e5bcf8e88710fb6cd6c856e49b4084c742a7ecff5609
mado-devices.py	ok	.ufo/waves/round-46/receipts/live-devices-host-r46.txt	3a80368997120503d5715596a17e762bbcb67a41db23d9241425bf19349d594f
mado-verify.sh	stale	.ufo/evidence/round-12/after.txt	ea798ad078f139f34ce06e72ef2c1fecb0732bfc063b1ea95bec50655f27e0b5
mado-tripwire.py	stale	.ufo/waves/round-19/evidence/final/tripwire-seat-scan.txt	367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d
mado-binds.py	stale	.ufo/waves/round-25/evidence/c1-after-v4-ef94763c.txt	9efa1136abd2759ecf870e551be967c49f8b50b9a11b39ac568a308e8f172950
mado-anims.py	ok	.ufo/waves/round-26/evidence/c1-after-v2-2b3487f7.txt	2beda3f7b1a5a7901f6a2cfc7e5b314b68ea9be8d0da27d3a92879946d9cab7d
mado-wsrules.py	ok	.ufo/waves/round-27/evidence/c1-after-20022a65.txt	dcf5c8c05b2d5b68ef967df339f7539a762e56c8a3811d7fbef33db9936ca389
mado-action-plan.py	none	-	-
mado-assessment.py	none	-	-
mado-evidence-audit.py	none	-	-
-->

## 9. The criterion's checker, shown able to fail

`check-ledger.py` (this seat) reads the §8 block, re-derives each row's status from the tool bytes
at `--rev` (or the working tree) and from the receipt it names, and exits 1 on any disagreement.
Raw output: `receipts/check-ledger.txt`.

```
$ python3 -I check-ledger.py --repo <lane>
LEDGER: ok=7 stale=3 none=4 missing=0 mismatch=0 unbound=0 missing_receipt=0 instruments=14
rc=0

# A. binds row declared "ok" although its receipt ran the pre-round-26 bytes
MISMATCH mado-binds.py declared=ok derived=stale recorded=9efa1136abd2 current=0cda0e6ff5e2
LEDGER: ok=7 stale=2 none=4 missing=0 mismatch=1 unbound=0 missing_receipt=0 instruments=14
rc=1

# B. globals row deleted
MISSING mado-globals.py
LEDGER: ok=7 stale=3 none=3 missing=0 mismatch=0 unbound=0 missing_receipt=0 instruments=14
rc=1

# C. eventq row re-pointed at a receipt that does not name its sha
UNBOUND mado-eventq.py sha=436f550e9939 receipt=.ufo/waves/round-25/evidence/c1-after-v4-ef94763c.txt
LEDGER: ok=6 stale=3 none=4 missing=0 mismatch=0 unbound=1 missing_receipt=0 instruments=14
rc=1

# same ledger read at the base revision through git show
$ python3 -I check-ledger.py --repo <lane> --rev c24adef2632672325a4eef3e3492f6716ccb6d14
LEDGER: ok=7 stale=3 none=4 missing=0 mismatch=0 unbound=0 missing_receipt=0 instruments=14
rc=0
```

Each quoted fragment in this file was checked against its source line by
`receipts/verify-quotes.txt` (`QUOTES total=20 missing=0`).
