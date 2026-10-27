# CritRouted — measurements (round-48 w2, FALSIFY)

Every block names the attack, the exact command and the observed output. Lane reads are revision-addressed from
scratch clones of `3e6c848a0e1bbc9c7058226b86d0faefc5351c9d` (freeze v1); the working tree was never written.
Scratch root: `/fast/scratch/hyaku/mado-r48/CritRouted` (161 MB total, deleted after the receipts were copied).

## 0. Identities at the freeze revision

```
$ git -C <lane> rev-parse HEAD
3e6c848a0e1bbc9c7058226b86d0faefc5351c9d
.ufo/waves/round-48/l1-draft/mado-terminal.py
1dfde36cfa68beffb6b2bc2ae9cf04875bd48702669812ce3ecd10b986753a92
tools/mado-terminal.py (working tree = integration candidate)
1dfde36cfa68beffb6b2bc2ae9cf04875bd48702669812ce3ecd10b986753a92
quality/check-session-material.py (= w1/ExecSessionMarker/check-session-material.py)
82c9053ae2e8b7db2fb8c0e195c32b8b151a593cf9412dcae3589427ac2dfa6f
quality/counters/c1-r48-fixtures.json  = SHA256_WARM in the counter
4d946bd7934d4afc40d16676a300a7a10ee077404a2d51e289d9db871cb311aa
quality/counters/c1-r47-fixtures.json  = SHA256_COLD
4836cc1d9e493af7bf15fa52f6e6855fe71c5c27911880847da668e1e313dd86
.ufo/waves/round-47/fetch/xdg-terminal-exec = PIN_SHA256 = /usr/bin/xdg-terminal-exec
89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac
```

## 1. D1 — conditional HOME

(a) Frozen fixture inventory (`quality/counters/c1-r48-fixtures.json`, 204 cases): classes
`HOME-UNSET` ×10 + `EDGE-HOMEUNSET` ×1. The ten are
`v2-hu-01-home-unset-xdg-set` (expect rc 0 `foot --a`), `-02-config-unset` / `-03-data-unset` /
`-04-cache-unset` / `-05-all-xdg` (rc 1, empty), `-06-data-dirs`, `-07-warm` (state hit),
`-08-warm-differs`, `-09-print-id`, `-10-data-dirs-unset`; `E-01` (HOME + every XDG base unset, rc 1).
`meta.note` of hu-02/03/04 name the death site (config default / data default / cache default).

(b) Baseline score of the frozen tool (clause w, variant A+B, per-fixture oracle-vs-`expect` drift check):

```
PRED-C1-r48 clause=w fixture=v2-hu-01-home-unset-xdg-set class=HOME-UNSET state=absent pass
... hu-02,03,04,05,06,07,08,09,10 ... pass
PRED-C1-r48 clause=w fixture=E-01 class=EDGE-HOMEUNSET state=- pass
PRED-C1-r48 clause=w warm=204/204
PRED-C1-r48: cold=190/190 warm=204/204 explained=394/394 generated=230/230 selftest=ok readonly=ok tool=present verdict=TARGET_MET
```
(`c1-baseline.txt`; rev ec8e9e4c = freeze + `l1-draft/mado-terminal.py`.)

(c) Direct measurement, no sandbox, HOME absent and the three XDG bases set, tree with
`usr/share/applications/foot.desktop`, list `hyprland-xdg-terminals.list: foot.desktop`, exec stub `root/bin/foot`:

```
candidate tool (l1-draft bytes)  -> "foot", rc=0 ; explain: cache absent, candidate foot.desktop SELECTED
base tool (3e6c848a:tools/)      -> "MADO_TERM_OUT_OF_CONTRACT: HOME unset", rc=2
```
So the conditional behaviour is not only in a fixture: the data candidate models it and the base does not.

(d) Mutant scores (frozen counter, nonce 4848, same fixture file):

```
need_home refuses with exit 2 (commit 91a4d88d, c1-homerefuse.txt)
  warm=199/204 explained=389/394 ; FAIL E-01, hu-02, hu-03, hu-04, hu-05 (oracle=(1,'') tool=(2,''))
HOME unset refused at make_paths entry (commit 83bdea7a, c1-homealways.txt)
  warm=193/204 explained=383/394 ; FAIL E-01 + hu-01..hu-10
    hu-01 oracle=(0,'foot\n--a\n') tool=(2,'') ; hu-09 oracle=(0,'foot.desktop\n') tool=(2,'')
  verdict=TARGET_MISSED rc=1
```
Both conditional branches are enforced: the all-XDG-set answer and the defaults-needed exit status.

(e) Schema limit: `case_env()` forces `HOME=<root>/home` unless `HOME` is in `unset` and then removes it; a fixture
cannot express `HOME=""` (ExecHomeUnset C4/C4b). Those two shapes are measured by w1 but not frozen.

## 2. D3 — two valid candidates, readdir order

(a) Inventory: class `READDIR` ×10, all with `meta.readdir_order`; nine multi-entry cases ship `meta.files_order`
(the counter's `write_files(order=meta.files_order)`, `c1-r48-terminal-cache.py:404`). Non-sorted winners:
`v2-rd-05-three` files_order `foot,kitty,aaaa` → `aaaa.desktop`; `v2-rd-06-reverse-create` `konsole,ghostty` →
`ghostty.desktop`; `v2-rd-01` `foot,kitty` → `kitty.desktop`.

(b) Baseline: `clause=w fixture=v2-rd-01..10 class=READDIR ... pass`, `clause=w warm=204/204` (same run as §1b).

(c) Mutant = one-line patch of the candidate tool's `_walk` (`names = sorted(de.name for de in os.scandir(cur))`,
branch `mut-sorted`, commit 7d9ed9cc):

```
PRED-C1-r48 clause=w fixture=v2-rd-05-three class=READDIR state=absent FAIL oracle=(0,'aaaa.desktop\n') tool=(0,'kitty.desktop\n')
PRED-C1-r48 clause=w fixture=v2-rd-06-reverse-create class=READDIR FAIL oracle=(0,'ghostty.desktop\n') tool=(0,'konsole.desktop\n')
PRED-C1-r48 clause=w warm=202/204
PRED-C1-r48: cold=190/190 warm=202/204 explained=392/394 generated=228/230 ... verdict=TARGET_MISSED
```
(`c1-sorted.txt`; rc=1.) The ten cases are not decoration: two of them decide the verdict.

## 3. R3 — synthetic-material marker, installed at the freeze revision

```
$ sh .ufo/waves/round-48/w1/ExecSessionMarker/install.sh <scratch clone at 3e6c848a>
installed gate sha256=82c9053ae2e8b7db2fb8c0e195c32b8b151a593cf9412dcae3589427ac2dfa6f
installed registry rows=48
installed sidecars=48
$ python3 -I quality/check-session-material.py --selftest
SELFTEST: passed=69/69 failed=0
```
(install.sh's header comment still says "47 rows / 47 sidecars"; the counts it prints are 48/48.)

Committed install (rev 576ba060), the same revision with `--no-waivers`, and the waiver set:

```
SESSION_MATERIAL_WAIVED: findings=52 files=48
SESSION_MATERIAL: files=20786 findings=101
--no-waivers: SESSION_MATERIAL: files=20786 findings=153
suppressed (153-101) == WAIVER set: True (52 pairs, 48 files, R1/R2/R3 only)
FINDING rules left: R1 34, R2 34, R3 10, R4 2, R5 21
```
Both ways, one commit apart, same install set:

| demo | commit | observed |
|---|---|---|
| (b) synthetic fixture, unmarked | 64498219 | `findings=154`, `FINDING .../fixtures/synthetic-clients.json rule=R1_CLIENT_DUMP count=1` |
| (a) same bytes + sidecar + registry row | 8276ce4a | `WAIVER ... rule=R1_CLIENT_DUMP kind=fixture`, `findings=101`, no FINDING line |
| (c) same bytes at `.ufo/reports/session-clients.json` with a valid marker pair | c16060bd | `WAIVER_REJECTED ... reason=path-outside-waves` + FINDING stands, `findings=102` |
| (c′) real title `Mozilla Firefox` inside a fixture path with a valid marker pair | 32f39a97 | `WAIVER_REJECTED ... reason=value-not-synthetic:title-not-synthetic` + FINDING stands, `findings=103` |

Real findings are not laundered: the install keeps `findings=101`, exit 1, including 11 findings in the three stale
gate copies (round-45 ExecPrivacyGate, round-46 ExecSessionTriage, round-47 ExecSessionMarker). No green is claimed.
Registry composition: 47 `kind=fixture` + 1 `kind=gate-copy`; 45 round-45, 2 round-46, 1 round-48.

## 4. R4b — round-45 errata vs the frozen round-45 verdict

Append at the freeze revision (`d9d...` clone, branch r4b, commit 344845ba; `cat block.md >> entry`):

```
prefix byte-identical: PREFIX_IDENTICAL (cmp -n <size before>)
107 -> 158 lines ; sha256 of the appended entry 73a6c4ace54592c9b75848a89b5d96e6362ca893ec202c256695586f8b1ffa0e
   (= working-tree corpus/knowledge/hyprland-monitor-rule-r45.md, byte-identical)
block: 0 source ids (\b[Ss][0-9]{3,}\b), no source:/verified-at:/recheck: line, no fence, no BAD_LOC
```

Both frozen instruments, before and after, at both revisions:

| rev | c2-r45-monitor-entry.py | c2-r45-monitor-entry-v2.py |
|---|---|---|
| 579f694b (round-48 base) | admitted=1/1 TARGET_MET rc 0 | admitted=1/1 TARGET_MET rc 0 |
| 3e6c848a (freeze, before) | admitted=1/1 TARGET_MET rc 0 | admitted=1/1 TARGET_MET rc 0 |
| 344845ba (freeze + block) | admitted=1/1 TARGET_MET rc 0 | admitted=1/1 TARGET_MET rc 0 |

Every row: `clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 j:1`. Negative control (the same block with `(S303)`
put back into E6, committed on branch `neg`): `admitted=0/1 verdict=TARGET_MISSED`, `g:0`, rc 1 — the instrument
still bites and clause `g` is the only thing the source id touches.
Cited entry lines recomputed: `:18` recheck/release, `:84` S311 emit, `:96` monitor dump, `:98` 99.997 Hz,
`:106` description, `:107` hyprlang form; `tools/mado-monitors.py` = 2f007417… at 4d22eeb and 579f694b.

## 5. D4 — erratum on the round-47 entry, append-only

```
base entry 96 lines, sha256 a1c184ea… ; block = 26 lines (the fenced markdown in w1/ScrErrataD4/erratum.md)
appended -> 123 lines, sha256 051e36b9e56c56804335e63890234ef9b45fa9fbeb3f4e3d599f6b53f2316efa
   (= working-tree corpus/knowledge/xdg-terminal-selection-r47.md, byte-identical)
prefix: cmp -n <96-line size> -> PREFIX_IDENTICAL ; diff of the prefix -> DIFF_CLEAN
```
The routed defect reproduces on the base bytes: entry line 95 cites `terminal-route-r17.md:150-151`; in the source
the sentence opens at :149 (`- [UNK] Whether the `--dir=` value from … is valid at`) and closes at :150
(`  launch time. The helper is not run.`); :151 is 1 byte (the blank line's newline). After the append the file
carries full-file locators at :76, :88, :95 (stale, body, by design) and :105 (corrected `:149-150`); the new lines
contain exactly one full-file locator, as the block itself states.

## 6. D2 (routed in the same set) — session-material counts at named revisions

```
60edb66e: files=18371 findings=115 rc=1
d40189c9: files=19969 findings=128 rc=1
579f694b: files=19969 findings=128 rc=1
```
Second run of 579f694b: byte-identical output (`cmp` clean).

## 7. Bounds and safety

* Writer shells start with `ulimit -f 2048` (1 MiB). The guard stopped two full clones (`git index.lock: File too
  large`); the workspace was rebuilt as a sparse-index clone (index 447 KB, largest checked-out blob 952 KB).
* The C1 counter itself copies host binaries (`/usr/bin/gawk`, `ls`, `md5sum`, …) into its sandbox, one of them
  >1 MiB; under `ulimit -f 2048` it dies with `OSError: [Errno 27] File too large`. The four counter runs were
  therefore made with `ulimit -f 65536` (32 MiB/file) and nothing else changed. Largest file this seat wrote:
  30 220 B (`c1-homealways.txt`); scratch total 159 MB; no `/tmp` use; scratch deleted.
* No lane git/jj mutation: three `git clone --shared` clones under scratch, `rev-parse --show-toplevel` asserted
  before every commit, commits with `seat <seat@scratch.invalid>`. No package install, no pacman, no compositor,
  no input injection, no GUI/terminal launch, no host config write.
