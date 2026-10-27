# ExecDoNothing — section-9 do-nothing controls on the FROZEN round-49 counters (mado round 50, w1)

**Verdict: all eight do-nothing / cheap controls (four C1, four C2 — the six the item names plus two cheap
near-misses) read `TARGET_MISSED` with exit 1, and a positive anchor on the same C2 tree family reads
`TARGET_MET`** — the counters are not blanket rejectors AND not do-nothing acceptors. Routed defect
**D4** is closed: the controls below were scored with the counters exactly as committed at
`13631f24050f22db92bf5bd33e0f4d014192992e`, never a w1 draft (round 49 scored the stub on the draft counter,
`generated=7/60`).

| | instrument | sha256 at 13631f24 | base |
|---|---|---|---|
| C1 | `quality/counters/c1-r49-keysym.py` (PRED-C1-r49) | `2597c204abf1e9e7c625d98cf83f0b340a0d82897da4986c550e35c5dff5db62` | `03e4ae76…` |
| C2 | `quality/counters/c2-r49-bind-entry.py` (PRED-C2-r49) | `bc171714c5349dbe980b84f5c434126965cc8a6e8226704c28604d10cff28c69` | `03e4ae76…` |

Both digests are `git show 13631f24:<path> | sha256sum`, i.e. the committed bytes. No lane file was edited; the
scratch clone lived at `/fast/scratch/hyaku/mado-r50/ExecDoNothing/` (deleted at the end); every run used
`HOME`/`XDG_*`/`TMPDIR`/`--work` under that scratch. **No outer tracer was used anywhere** (SentHostState's
R-SHS-3 warning: wrapping the C1 counter in `strace -f` makes it report a false miss through nested ptrace); every
run was `python3 -I <counter> …` directly.

## 1. Results (one line per control; receipts under `receipts/`)

C1 — `receipts/c1-<control>.txt`, full output including every fixture line:

| control | rev (fixture commit) | exit | final line | clause that stopped it |
|---|---|---|---|---|
| `c00-absent` (tool absent) | `03e4ae76` (base) | 1 | `fixtures=0/633 generated=0/150 selftest=fail readonly=fail tool=absent verdict=TARGET_MISSED` | **t** |
| `c02-header-only` | `2ebd10d44bf07ef5eecb0a162fa44dfd13aee041` | 1 | `fixtures=0/633 generated=0/150 selftest=fail readonly=ok tool=present verdict=TARGET_MISSED` | **s**, f, g |
| `c03-level1-only` | `10f6c7393572fa5c970b4668bedf60755afebadd` | 1 | `fixtures=423/633 generated=119/150 selftest=fail readonly=ok tool=present verdict=TARGET_MISSED` | **s**, f (210), g (31) |
| `c11-selftest-only` (extra cheap control) | `cc4b9c0eeb2e79d3abcca8c45a4a49628e9f34bb` | 1 | `fixtures=0/633 generated=0/150 selftest=ok readonly=ok tool=present verdict=TARGET_MISSED` | **f**, g |

C2 — `receipts/c2-<control>.txt`, full clause output:

| control | rev (fixture commit) | exit | final line | clauses 0 |
|---|---|---|---|---|
| `c10-candidate` (**anchor**, not a control) | `bcfae4ae29901f4b31dd8e0a1c1ef5d643af659c` | 0 | `clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 j:1 r:1 admitted=1/1 verdict=TARGET_MET` | — |
| `c11-receipt-removed` | `154da826f5248f15d0db5ff91eb03b41f14febb2` | 1 | `clauses=a:1 b:1 c:1 d:1 e:1 f:0 g:1 h:1 i:1 j:1 r:0 admitted=0/1 verdict=TARGET_MISSED` | **f, r** |
| `c12-stub` (head + one sentence) | `ea7264e7d52a258862a0e58ed5e263c98d67323c` | 1 | `clauses=a:1 b:1 c:1 d:1 e:0 f:0 g:1 h:0 i:0 j:0 r:1 admitted=0/1 verdict=TARGET_MISSED` | **e, f, h, i, j** |
| `c13-paste-2-3` (held §2.3 pasted under the head) | `b792bdaeca79df6fe3bf0fbd281d4a3cb6c81314` | 1 | `clauses=a:1 b:1 c:1 d:1 e:0 f:0 g:1 h:0 i:0 j:0 r:1 admitted=0/1 verdict=TARGET_MISSED` | **e, f, h, i, j** |
| `c14-paste-2-3-prose` (supplementary probe) | `f7f0385b52faafd0537865a7a124251ccdb219f9` | 1 | `clauses=a:1 b:1 c:1 d:1 e:0 f:0 g:1 h:0 i:0 j:0 r:1 admitted=0/1 verdict=TARGET_MISSED` | **e, f, h, i, j** |

`receipts/controls-all.txt` is generated from the per-control receipts (final lines + stop lines), so it cannot say
anything a receipt does not. The C1 fixture commits are printed in each receipt's own `# cmd:` line.

### 1.1 The clause lines that name each stop (verbatim from the receipts)

- `c1-c00-absent.txt`: `clause=t tool=absent` (the `fixtures=0/633 generated=0/150 selftest=fail readonly=fail` fields
  on this line are the absent-branch constants in the counter source, not a measurement — say so when citing it).
- `c1-c02-header-only.txt`:
  `clause=s selftest rc=0 last='' fail` /
  `clause=s refusals=fail no-disable-compose: rc=0 table=no; no-keysym: rc=0 table=no` /
  `clause=f fixtures=0/633` / `clause=g generated=0/150 first_fail=('g000', "arg='0x10002339' judge=0/123 tool=0/0")` /
  `clause=r trips=0`.
- `c1-c03-level1-only.txt`:
  `clause=s selftest rc=1 last='MADO_KEYSYM_SELFTEST: 30/38 passed' fail` / `clause=s refusals=ok` /
  `clause=f fixtures=423/633` (210 `FAIL`) / `clause=g generated=119/150 first_fail=('g001', "arg='86' judge=0/243 tool=0/110")` /
  `clause=r trips=0`.
- `c1-c11-selftest-only.txt`: `clause=s selftest rc=0 last='MADO_KEYSYM_SELFTEST: 25/25 passed' ok` /
  `clause=s refusals=ok` / `clause=f fixtures=0/633` / `clause=g generated=0/150` / `clause=r trips=0`.
- `c2-c11-receipt-removed.txt`: `clause=f receipt_missing=.ufo/waves/round-49/receipts/binds-live-r49.txt` and
  `clause=f no_receipt_answers cited=[…binds-live-r49.txt, …binds-shape-r49.txt, …how-to-type-slash-br-r49.txt]`;
  `clause=r receipt_unparseable=.ufo/waves/round-49/receipts/binds-shape-r49.txt`. All ten other clauses `:1`.
- `c2-c12-stub.txt` and `c2-c13-paste-2-3.txt`: `clause=e steps=0 <6`; `clause=f entry_disagrees=…
  ver=1 total=[192] forms={'named': [], 'code': [], 'mouse': [], 'switch': []} sha=0 resolve=0` and
  `clause=f no_receipt_answers`; `clause=h limits=0 bullets=0 scoped=0`; `clause=i …` (below); seven
  `clause=j topic=<t> unanswered lines=[…]` (369, 711, 652, 1484, 382/422, 1711, 1224). `clause=d quotes=0`.
- `c2-c10-candidate.txt` (anchor): `clause=d quotes=86`, `clause=e steps=17 verified_steps=17`,
  `clause=j` answers all seven topics at 369/711/652/1484/382/1711/1224, `clause=f … binds=192
  forms=named:142,code:42,mouse:6,switch:2 sha=9a47199e2297 resolve=0`, `clause=i new_rows=12 gate=1
  ground_present=2/4 body=62 dup=0 overlap=0.008`, `clause=r replay=ok sha=9a47199e2297 binds=192 … resolve=0`.

## 2. Method (reproducible; scripts in `controls/`)

- `controls/drive-c1.py` — one scratch clone of the lane (`git clone -q --shared`, toplevel asserted equal to the
  clone before the first commit), each C1 control is one commit that puts the control blob at
  `tools/mado-keysym.py`; `c00-absent` scores the base commit itself. Then one counter run per revision:
  `python3 -I quality/counters/c1-r49-keysym.py --repo <clone> --rev <rev> --work <scratch>/work --nonce 5001`.
- `controls/drive-c2.py` — one scratch clone per control on top of `13631f24`, all five sharing one host tree: the
  round-49 candidate entry (`candidate/hyprland-bind-key-match-r49.md`, sha256 `6be1a22e…`), the 12 candidate rows
  `S352-S363` (`candidate/rows.md`, sha256 `dae499ca…`) inserted inside `## Registry`, one 3-cell `corpus/README.md`
  index row covering `S352-S363`, and the 12 `- **S### admit**` lines the round-49 lesson already points at
  (`.ufo/waves/round-49/w1/ScrRows/gate.md` §1, sha256 `bd46d4ab…`) inserted into the lesson's `## Gate`. Pins and
  the live receipt are already committed at `13631f24`. Then:
  `python3 -I quality/counters/c2-r49-bind-entry.py --repo <clone> --rev <rev> --base 03e4ae76…`.
  Each tree's diff against `13631f24` is 4 files (entry, 13 lines of registry, 1 README line, 13 lesson lines);
  `c11` additionally deletes the 16-line receipt (`git rm`).
- Control sources are byte-identical copies where one existed: `controls/c02-header-only.py` and
  `controls/c11-selftest-only.py` are `c02-header-only.py` / `c11-selftest-only.py` from
  `.ufo/waves/round-49/w1/ExecControlsC1/controls/` (sha256 `96fbfb5b…` / `4c6a1fd9…`, equal to the originals).
  `controls/c03-level1-only.py` is the round-49 candidate tool (`dcc13cce…`) with one mutation: its level loop
  `for level in range(key_type.num_levels)` becomes `for level in (0,)` (2 comment lines + 1 line changed, marked
  `CONTROL c03-level1-only`).
- `controls/finalise.py` normalised the absolute home prefix → `~` in the receipts (declared in each
  receipt header), built `receipts/controls-all.txt`, and derives the lane path from its own location (no
  absolute home path in the committed scripts).

## 3. Findings (what each attacks/supports)

**F1 — the frozen C2 counter ADMITS the round-49 candidate entry on a candidate data tree (attacks
`corpus/lessons/round-49-verifier-spotcheck.md` §6 item 5 / `registration.md:27-29`; supports C1's round-50 move).**
`c10-candidate` is `TARGET_MET`, all eleven clauses 1, with the entry and rows **byte-identical** to the round-49
candidate artifacts; the only added bytes are the README index row and the 12 Gate admit lines that the round-49
lesson already names by path. Round-49's registration sentence — "the integrated candidate … does NOT meet the
counter on a scratch tree (clauses b/c/d/e/j fail on row-pin binding and quote attachment)" — is **not reproducible**
against that tree: `clause=c id=S352 pins=Hyprland-KeybindManager.cpp digests=1 ranges=9` … and `clause=d quotes=86`,
`clause=e steps=17 verified_steps=17` are all `:1`. What my tree has that the round-49 scoring tree apparently lacked
is the 12 registry rows appended (without them a head id has `rows=0`, which would fail b, and c/d/e/j lose their
row-cited pins) plus the README row and the Gate admits. This is a **round-50 erratum candidate, not a rewrite of
round-49 bytes**: the L1 should either reproduce `c10` or record that its scoring tree differed, because the C1
round-50 entry is the same entry re-pointed.

**F2 — a table-only paste is stopped by clause i's sample floor, not by its novelty rate (supports the C2 counter,
narrows its declared reach).** `c13-paste-2-3`: `clause=i novelty_body_lines=17 base_duplicates=1 grams=123
base_grams=268678 overlap=0.081`. The pasted §2.3 is a Markdown table, and `body_text()` drops table rows, so the
paste never reaches 150 shingles and is refused by `grams < 150`; the shingle overlap (0.081) and the duplicate-line
count (1) are both inside the thresholds. `c14-paste-2-3-prose` (the same paste plus eight ≥60-char held prose lines)
does reach the nets: `novelty_body_lines=25 base_duplicates=9 grams=207 overlap=0.406` — both `dup > 5` and
`overlap ≥ 0.15` fire. So the counter refuses both, but a reader of the clause-i residual should know that a
table-shaped paste is never measured for novelty, only rejected for having too little prose. For `PRED-C1-r50`, whose
entry is tables and code quotes, that floor is what binds.

**F3 — clause s alone cannot admit a do-nothing tool, and its floor is reachable in practice (supports the C1
counter; cross-referenced by SentHostState R-SHS-6).** `c11-selftest-only` prints
`MADO_KEYSYM_SELFTEST: 25/25 passed`, exits 2 on both refusals, makes no process/socket/write (`trips=0`) and is
still `MISSED` at `fixtures=0/633` and `generated=0/150`. The self-check half accepts exactly the floor:
`c1-r49-keysym.py:664` requires `m.group(1) == m.group(2) and int(m.group(1)) >= SELFTEST_MIN`, with
`SELFTEST_MIN = 25` (`:128`), so a 25-case stub satisfies clause s as written — the answer clauses f and g are
what stop it. Worth a freeze decision (pin an exact expected total, as SentHostState reports the wave-done
gate already does with a fixed check count), not a defect in the control set: the null is still refused.

**F4 — the level-1-only tool scores 67 % of the fixtures and 79 % of the generated cases (measurement for the
freeze).** `c03-level1-only`: `fixtures=423/633`, `generated=119/150`, and its own selftest `30/38`. The 210 failing
fixtures include the `BIND` class (`XF86TouchpadToggle`, `C`, …) because those keysyms sit above level 1; the
discriminating bytes exist and are not confined to one class, but a "level 1 only" tool is right for two thirds of a
fixture set whose arguments are mostly unshifted names — the freeze should keep the level-sensitive classes in the
pool it inherits.

**F5 — receipt removal is caught twice, independently (supports the C2 counter).** Deleting only
`.ufo/waves/round-49/receipts/binds-live-r49.txt` drops `f` (`receipt_missing` + `no_receipt_answers`) and `r`
(`receipt_unparseable` on a *different* cited receipt), while all ten other clauses stay `:1`. No other clause
silently covers for the receipt.

**F6 — the C1 header-only scaffold is caught by three clauses, and `readonly=ok` (supports the counter's clause
split).** A blob at `tools/mado-keysym.py` that only returns 0 gives `clause=t tool=present` (presence alone passes),
then `s`/`f`/`g` stop it, with `trips=0` — so the read-only clause is not what a scaffold trips; the answer clauses
are.

## 4. Residuals and limits of this seat's evidence

- The C2 host tree is a **constructed candidate state**; the README index row is written by this seat (3 cells,
  `rows S352-S363`, no redirect word, no other `knowledge/` file named) and the Gate admits are the round-49
  `ScrRows` lines verbatim. Both are named and digested above so the L1 can rebuild or reject the tree.
- F1 is a statement about **my** tree. I cannot see the tree round 49 scored (that receipt was never committed);
  the claim is "the candidate + candidate rows + the lesson's own drafted admits are admissible", not "round 49 was
  wrong".
- Every control is one revision; none of these runs is a re-freeze of PRED-C1-r49/PRED-C2-r49, and nothing here
  scores a round-50 counter.
- Tracer caveat (corrected with SentHostState, round-50 w1): no outer tracer was used in any run here. The
  outer-tracer false miss ends `clause=r trips=786 python-execve-not-seen` with `readonly=fail`, but the
  discriminator is the **detail string naming a missing execve** — no tool behaviour can produce that, while
  `readonly=fail` alone is not diagnostic (a tool that genuinely attempted a write outside `/tmp` would also
  read `fail`). The scaffold controls here end `trips=0 readonly=ok`, so verdict and `readonly` cannot separate
  a legitimate scaffold miss from a tracer start failure on those two controls; only the clause-r detail can,
  which is why R-SHS-3 asks for a `Setup` class (rc 2) emitted before scoring.
- Not measured here: whether a *weakened* counter would still miss these controls (that is `MutC1Counter` /
  `MutC2Counter`), and whether a MET anchor exists for `PRED-C1-r49` (the round-49 `c1-after-data` receipts are the
  committed positive evidence; this seat did not re-run them).
- Privacy: a `grep` for the account name over this seat returns nothing (receipts write the home prefix as
  `~`); receipts carry no raw `hyprctl binds -j` JSON, no titles, device names or home listings. The only
  compositor contact was the counter's own read-only `clause=r` replay (`binds -j`,
  `getoption input:resolve_binds_by_sym -j`) in the `c10/c11/c12/c13/c14` runs that cite a receipt.
- Privacy receipt: the installed gate (`quality/check-session-material.py`, sha256 `82c9053a…`) run over a
  scratch commit that adds this seat's bytes reports **no finding under `.ufo/waves/round-50/`**
  (`files=23021 findings=113` on that revision; all 113 predate round 50) — `receipts/gate-scan.txt`.
- Host safety: no pacman, no compositor mutation, no GUI program, no `xkbcli` call outside the counter's pinned
  `compile-keymap`/`how-to-type`; scratch under `/fast/scratch`, deleted at the end.

## 5. Deliverables (each `test -f`-checked at hand-off)

```
.ufo/waves/round-50/w1/ExecDoNothing.md
.ufo/waves/round-50/w1/ExecDoNothing/receipts/controls-all.txt
.ufo/waves/round-50/w1/ExecDoNothing/receipts/c1-controls.txt
.ufo/waves/round-50/w1/ExecDoNothing/receipts/c1-c00-absent.txt
.ufo/waves/round-50/w1/ExecDoNothing/receipts/c1-c02-header-only.txt
.ufo/waves/round-50/w1/ExecDoNothing/receipts/c1-c03-level1-only.txt
.ufo/waves/round-50/w1/ExecDoNothing/receipts/c1-c11-selftest-only.txt
.ufo/waves/round-50/w1/ExecDoNothing/receipts/c2-controls.txt
.ufo/waves/round-50/w1/ExecDoNothing/receipts/c2-c10-candidate.txt
.ufo/waves/round-50/w1/ExecDoNothing/receipts/c2-c11-receipt-removed.txt
.ufo/waves/round-50/w1/ExecDoNothing/receipts/c2-c12-stub.txt
.ufo/waves/round-50/w1/ExecDoNothing/receipts/c2-c13-paste-2-3.txt
.ufo/waves/round-50/w1/ExecDoNothing/receipts/c2-c14-paste-2-3-prose.txt
.ufo/waves/round-50/w1/ExecDoNothing/receipts/gate-scan.txt
.ufo/waves/round-50/w1/ExecDoNothing/controls/drive-c1.py
.ufo/waves/round-50/w1/ExecDoNothing/controls/drive-c2.py
.ufo/waves/round-50/w1/ExecDoNothing/controls/finalise.py
.ufo/waves/round-50/w1/ExecDoNothing/controls/c02-header-only.py
.ufo/waves/round-50/w1/ExecDoNothing/controls/c03-level1-only.py
.ufo/waves/round-50/w1/ExecDoNothing/controls/c11-selftest-only.py
```

Tooling installed or upgraded this seat: none.
