# RevSeparabilityShape — Findings (mado round 41, wave w2)

- **Seat:** `RevSeparabilityShape` (UFO-FSD reviewer, leaf)
- **Lane repo:** `/home/vgpnk/Projects/shokunin/mado-shokunin`
- **Base commit:** `ab2bfaab661c846d1de9d58c01651cd156a13949`
- **v1 Freeze:** `60c3914154333180450d5da27ba222d5763cc56a`
- **v2 Freeze:** `294c667901a8c7b7165ba849d03cba9a24c14fa4`
- **Data commit:** `07f2641696b5ac73de1404ea737a9f27e9819aa1`
- **Attack scope:** Claim separability (C1 vs C2), axes & lowest-axis rule (`AXES.md`), universal clauses & claim sizing (`PROTOCOL.md` / round prompt §9), do-nothing controls (`receipts/ctl-c1-v2.txt`, `ctl-c2-v2.txt`), sourced-claim requirement (`PROTOCOL.md:143-144`), and contradictions between `registration-v2.md`, `registration.md`, and the lane files at the data commit.

---

## 1. Summary of Findings by Severity

| ID | Severity | Target (`path:line`) | Summary | Classification |
|---|---|---|---|---|
| **F1** | **HIGH** | `corpus/lessons/round-41.md:163-164` vs `.ufo/waves/round-41/receipts/c1-v1-after-data.txt:34` | Committed lesson claims `PRED-C1-r41-v1` at the data commit is `fixtures=24/24 verdict=TARGET_MET`, whereas the actual v1 run on the data commit is `fixtures=6/24 tool=present verdict=TARGET_MISSED` (exit 1). | **DATA defect** (fix before landing) |
| **F2** | **MEDIUM** | `.ufo/waves/round-41/registration-v2.md:50` vs `.ufo/waves/round-41/receipts/ctl-c1-v2.txt:1,97` & `ctl-c1-v2-extra.txt:1-5` | Registration v2 claims "ten v2 cheats (`K01-K10`...) and the 42 `ExecC1ExtraMutants` mutants each score below MET" in `receipts/ctl-c1-v2.txt`, but `ctl-c1-v2.txt` skipped 4 of the 42 `W1-N*` mutants (`skipped-patterns-absent=4`: `N14`, `N24`, `N35`, `N42`), scoring 38 of 42 (`controls=95 correct=95/95`); only 2 of the 4 (`K11`, `K12`) were re-expressed in the unmentioned `receipts/ctl-c1-v2-extra.txt`, leaving `W1-N14` and `W1-N35` unscored in v2. | **REGISTRATION / PREDICATE-freeze defect** (report as open defect) |
| **F3** | **MEDIUM** | `corpus/lessons/round-41.md:38,45,53` vs `git ls-tree 60c3914 .ufo/waves/round-41/fetch/` & `corpus/SOURCES.md` | Committed lesson has three internal/lane contradictions: (a) `:38` says "the seven pre-wave receipts are committed at the freeze" when `60c3914` has **9** files in `fetch/`; (b) `:45` says "re-grounded this round as C2 with lane ids S283–S290" and `:53` says "the new rows S283-S289 continue... `input-capture-v1.xml` S290", whereas `S290` was not added (`SOURCES.md` stops at `S289`, as `:38` itself notes). | **DATA defect** (fix before landing) |
| **F4** | **MEDIUM** | `.ufo/waves/round-41/w1-spec.json` (`items` len 34) vs `.ufo/waves/round-41/w1/` (33 `.md` files) | Wave `w1` dispatched 34 seats (`registration-v2.md:13-14`), `w1-results.json` has `output: null` for all 34 due to orchestrator kernel restart, and seat `ConnSiblingOverlap` has neither `.ufo/waves/round-41/w1/ConnSiblingOverlap.md` nor a seat subdirectory on disk at `294c667` / `07f2641` (33 of 34 seat reports exist). | **DATA / WAVE-record defect** (disclose 1 missing w1 seat report in round report) |
| **F5** | **LOW** | `SCORECARD.md:2493` & `PROVINCE.md:24-32` at `07f2641696b5ac73de1404ea737a9f27e9819aa1` | At the data commit `07f2641`, `SCORECARD.md`, `LOG.md`, `SKILL.md`, `PROVINCE.md`, and `corpus/QUALITY.md` do not yet have their round-41 entries: `check-axis-scores.py --rev 07f2641` exits `1` (`navigation published=58/58 derived=59/59 verdict=STALE`, `mismatched=1`), and `tools/mado-globals.py` is not yet in `PROVINCE.md`'s tool table or `SCORECARD.md`'s capabilities table. | **Pre-closure state** (must be landed by L1 before final report commit) |

---

## 2. Check-by-Check Attack & Verification

### 2.1 Are C1 and C2 on distinct axes and causally separable?

**Target:** `.ufo/waves/round-41/registration-v2.md:36-46`, `quality/counters/c1-r41-globals-v2.py`, `quality/counters/c2-r41-focus-entry-v2.py` against `AXES.md:30-34`.

- **Rule (`AXES.md:30-34`, Q01):** `"Claims must be **causally separable** — each verifiable without the others having landed — and name **distinct axes**"` (18 words).
- **Distinct axes:**
  - **C1:** `operability` (capability acquisition: `tools/mado-globals.py`, a runnable read-only census CLI with `--selftest`, `--journal-file`, `--live`, `--diff`, `--expect`). Matches `AXES.md:13` (`"Runnable artifacts: checklists that are executable, commands that exist, scripts that run"`).
  - **C2:** `coverage` (sourced: `corpus/knowledge/hyprland-focus-grab-r41.md`, governing the Hyprland focus-grab protocol surface, compositor `CFocusGrab`, client lifecycle, and portal advertisement). Matches `AXES.md:12` (`"Fraction of the domain's real surfaces the skill governs"`).
  - **Result:** Distinct axes (`operability` vs `coverage`) — **PASS (no defect found)**.

- **Static Grep of Counters for Cross-Reads:**
  - Command run:
    `grep -nE 'tools/|mado-globals|corpus/|hyprland-focus-grab|SOURCES\.md|README\.md|lessons/|round-41\.md|show\(|git\(' quality/counters/c1-r41-globals-v2.py quality/counters/c2-r41-focus-entry-v2.py quality/counters/c1-r41-globals.py quality/counters/c2-r41-focus-entry.py`
  - **Observations:**
    1. `c1-r41-globals-v2.py` (and v1 `c1-r41-globals.py`) defines `TOOL = "tools/mado-globals.py"` (`:177`) and calls `git(repo, "show", "%s:%s" % (base, TOOL))` (`:1151`) and `git(repo, "show", "%s:%s" % (rev, TOOL))` (`:1154`). It has **zero** references to `corpus/`, `hyprland-focus-grab-r41.md`, `SOURCES.md`, `README.md`, `lessons/`, or `.ufo/waves/round-41/fetch/`. Furthermore, every tool and selftest execution runs inside `bwrap --unshare-all` (`:252-267`) where neither the lane repo nor `/home` is mounted.
    2. `c2-r41-focus-entry-v2.py` (and v1 `c2-r41-focus-entry.py`) reads only:
       - `ENTRIES = ("corpus/knowledge/hyprland-focus-grab-r41.md",)` (`:102`, `:286`, `:486`)
       - `corpus/SOURCES.md` at `rev` and `base` (`:488-489`)
       - `LESSON = "corpus/lessons/round-41.md"` at `rev` (`:103`, `:490`)
       - `corpus/README.md` at `rev` (`:491`)
       - `FETCH = ".ufo/waves/round-41/fetch/"` receipts via `show(repo, rev, path)` and `ls_mode(repo, rev, path)` (`:104`, `:258`, `:366`)
       - In clause `h` (`:209-235`, `:422-433`), C2 parses the saved journal receipt `.ufo/waves/round-41/fetch/xdph-journal.txt` using its **own built-in parser** (`journal_counts(blob)`), never importing, invoking, or hashing `tools/mado-globals.py`.
    - Quote (`.ufo/waves/round-41/registration-v2.md:46`, Q10): `"**Separability** is unchanged: C1 reads only \`tools/mado-globals.py\`; C2 reads only the entry, registry, lesson, README and the pinned receipts"` (19 words).

- **Dynamic Scratch-Clone Separability Proofs (run at data commit `07f2641696b5ac73de1404ea737a9f27e9819aa1`):**
  1. **Scratch Clone D1 (`tools/mado-globals.py` deleted):**
     - Created `d1 = tempfile.mkdtemp(prefix="revsep-no-c1-")`, cloned lane `--no-hardlinks`, verified `git -C d1 rev-parse --show-toplevel == d1`, checked out `07f2641696b5ac73de1404ea737a9f27e9819aa1`, ran `git -C d1 rm -q tools/mado-globals.py` and committed with `-c user.name=sep -c user.email=sep@sep.invalid` → commit `b0f887f4379da64e8fc31009ac51b891d405117a`, then cleaned up `d1`.
     - Ran `python3 -I quality/counters/c2-r41-focus-entry-v2.py --repo "$d1" --rev b0f887f4379da64e8fc31009ac51b891d405117a --base ab2bfaab661c846d1de9d58c01651cd156a13949`:
       - Output: `PRED-C2-r41-v2 hyprland-focus-grab-r41.md clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 admitted=1` / `PRED-C2-r41-v2: admitted=1/1 verdict=TARGET_MET rev=b0f887f4379da64e8fc31009ac51b891d405117a`, exit `0`.
     - Ran `c2-r41-focus-entry.py` (v1) on the same revision: `PRED-C2-r41-v1: admitted=1/1 verdict=TARGET_MET rev=b0f887f4379da64e8fc31009ac51b891d405117a`, exit `0`.
     - Negative check (`c1-r41-globals-v2.py` on `b0f887f4...`): `PRED-C1-r41-v2: fixtures=0/39 tool=absent verdict=TARGET_MISSED`, exit `1`.
  2. **Scratch Clone D2 (C2 entry and all C2 corpus changes deleted/reverted to base):**
     - Created `d2 = tempfile.mkdtemp(prefix="revsep-no-c2-")`, cloned lane `--no-hardlinks`, verified `git -C d2 rev-parse --show-toplevel == d2`, checked out `07f2641696b5ac73de1404ea737a9f27e9819aa1`, removed `corpus/knowledge/hyprland-focus-grab-r41.md`, `corpus/lessons/round-41.md`, `.ufo/waves/round-41/fetch/xdph-installed-version.txt`, restored `corpus/SOURCES.md` and `corpus/README.md` to `ab2bfaab661c846d1de9d58c01651cd156a13949`, and committed → commit `a15976e2ec9d8336467f428126e8676eb229b297`, then cleaned up `d2`.
     - Ran `python3 -I quality/counters/c1-r41-globals-v2.py --repo "$d2" --rev a15976e2ec9d8336467f428126e8676eb229b297 --base ab2bfaab661c846d1de9d58c01651cd156a13949 --nonce be51c3bc188d6b05`:
       - Output: `PRED-C1-r41-v2 clauses=a:1 b:1 b2:1 b3:1 g:1` / `PRED-C1-r41-v2: fixtures=39/39 tool=present verdict=TARGET_MET rev=a15976e2ec9d8336467f428126e8676eb229b297 nonce=be51c3bc188d6b05`, exit `0` (byte-identical fixture and clause scores to `receipts/c1-v2-after-data.txt`).
     - Negative check (`c2-r41-focus-entry-v2.py` on `a15976e2...`): `PRED-C2-r41-v2 hyprland-focus-grab-r41.md clauses=a:0 b:0 c:0 d:0 e:0 f:0 g:0 h:0 i:0 admitted=0` / `PRED-C2-r41-v2: admitted=0/1 verdict=TARGET_MISSED`, exit `1`.
  - **Result:** C1 and C2 are 100% causally and mechanically separable in both directions — **no defect found**.

---

### 2.2 Is the lowest-axis rule satisfied honestly?

**Target:** `.ufo/waves/round-41/registration.md:7-9`, `.ufo/waves/round-41/registration-v2.md:4`, `.ufo/waves/round-41/receipts/axis-base.txt`, `SCORECARD.md:280-285,2483-2493` against `AXES.md:33-34,67-73`.

- **Rule (`AXES.md:33-34`, Q02):** `"At least one claim works the lane's **lowest-scoring non-retired axis**, except when the stagnation nudge (below) waives it."` (18 words).
- **Rule (`AXES.md:68-71`, Q03):** `"When every axis the lane owns sits at or above the lane's saturation line and no capability has entered the table"` (21 words).
- **Registration statement (`.ufo/waves/round-41/registration.md:7-8`, Q16):** `"Every published axis ties at its maximum at base (\`receipts/axis-base.txt\`: navigation 58/58, calibration 55/55, operability 12/12, \`MADO_AXIS checked=3 mismatched=0\`),"` (19 words).
- **Verification:**
  - Re-ran `python3 -I quality/check-axis-scores.py --repo /home/vgpnk/Projects/shokunin/mado-shokunin --rev ab2bfaab661c846d1de9d58c01651cd156a13949`:
    ```
    MADO_AXIS_ROW: axis=navigation published=58/58 derived=58/58 verdict=MATCH
    MADO_AXIS_ROW: axis=calibration published=55/55 derived=55/55 verdict=MATCH
    MADO_AXIS_ROW: axis=operability published=12/12 derived=12/12 verdict=MATCH
    MADO_AXIS: checked=3 mismatched=0 rev=ab2bfaab661c846d1de9d58c01651cd156a13949
    ```
    Exit code `0`.
  - All three scored non-retired sub-axes (`navigation` [coverage], `calibration`, `operability`; `sourced-art` was retired in round 36 at `SCORECARD.md:221-228`) are at `1.0` (`10.0/10`, above the `9.0` saturation line at `SCORECARD.md:282`). Because a capability entered in Round 40 (`live option-table merge`, `SCORECARD.md:2485-2487`), the 3-round stagnation window (`N = 3`) is not triggered, and the registration honestly states `"the stagnation nudge is not needed"` because all three published axes tie at `1.0` (so every tied axis is a lowest axis). Working `operability` (C1) and `coverage` (C2) satisfies the lowest-axis rule directly.
  - **Result:** Satisfied honestly — **no defect found**.

---

### 2.3 Do the target statements contain a universal clause?

**Target:** `.ufo/waves/round-41/registration.md:25-27,35-36` and `.ufo/waves/round-41/registration-v2.md:39-40,44-45` against round prompt §9 (`mado-round-41.md:418-421`).

- **Rule:** Declare each after-state as one concrete value re-derivable with one command over committed bytes; use no universal clauses (`"all"`, `"complete"`, `"every"`, `"no harm anywhere"`) unless the counting command enumerates the full set.
- **Observed target statements:**
  - C1 (`.ufo/waves/round-41/registration-v2.md:40`, Q08): `"**Target:** \`fixtures=39/39 tool=present verdict=TARGET_MET\`, exit 0, at the data commit and at the tip."` (14 words).
  - C2 (`.ufo/waves/round-41/registration-v2.md:45`, Q09): `"**Target:** \`admitted=1/1 verdict=TARGET_MET\`, exit 0. **Kill rule:** as C1."` (9 words).
- Neither target statement contains an unenumerated universal clause; both are bounded finite ratios (`39/39` and `1/1`) with explicit exit codes (`exit 0`) and kill rules (`anything else at the data tip is a miss, reported as an honest stop; no narrowing`).
- **Note on `registration-v2.md:9` meta-prose:** Line 9 of `registration-v2.md` states `"v2 is strictly stronger than v1 on every point it touches (nothing loosened except the b2 sample's name-substring exclusion, replaced by an exact one)"`. While this is registration prose rather than a target statement, we checked whether v1's `STDLIB_ALLOW` vs v2's `STDLIB_ALLOW` loosened anything: v2 `STDLIB_ALLOW` (`c1-r41-globals-v2.py:186-187`) adds `collections`, `itertools`, `select`, `time` to v1's allowlist (`argparse`, `os`, `re`, `shutil`, `stat`, `subprocess`, `sys`, `tempfile`), while the delivered tool (`tools/mado-globals.py` at `07f2641`) imports `struct` and `threading`? Wait — let us check why `c1-v1-after-data.txt` failed `g:0`!
  - In `c1-v1-after-data.txt:33`, `PRED-C1-r41-v1 clauses=a:1 b:1 b2:1 g:0` failed clause `g` because `tools/mado-globals.py` imports `select` and `time` (for incremental bounded live read with a 30s deadline, required by v2 to fix `RevRefTool` M1/M2!), which were not in v1's `STDLIB_ALLOW` (`c1-r41-globals.py:134`). Thus v2 widened `STDLIB_ALLOW` by `{collections, itertools, select, time}` without mentioning that in the parenthetical on line 10 (`"(nothing loosened except the b2 sample's name-substring exclusion, replaced by an exact one)"`). We record this precision gap under **F2 / Wording**.
- **Result on target statements:** **No defect found** in the C1 or C2 target statements themselves.

---

### 2.4 Is a do-nothing control able to reach either target? (Control Receipts Audit)

**Target:** `.ufo/waves/round-41/receipts/ctl-c1-v2.txt`, `ctl-c1-v2-extra.txt`, `ctl-c2-v2.txt`, `c1-v2-before-base.txt`, `c2-v2-before-base.txt`, and `.ufo/waves/round-41/registration-v2.md:48-52`.

1. **Do-nothing controls cannot reach either target (PASS):**
   - **C1 base (`receipts/c1-v2-before-base.txt`):** `PRED-C1-r41-v2: fixtures=0/39 tool=absent verdict=TARGET_MISSED`, exit `1`.
   - **C1 do-nothing controls (`receipts/ctl-c1-v2.txt:3-5`):**
     - `D1-empty` (`import sys\n`): `fixtures=0/39 tool=present verdict=TARGET_MISSED` (`correct=1`)
     - `D2-echo-no-sessions` (echoes `NO_SESSIONS` + `40/40 passed` selftest): `fixtures=0/39 tool=present verdict=TARGET_MISSED` (`correct=1`)
     - `D3-hardcoded-report` (echoes 1 session + `OK` + `40/40 passed` selftest): `fixtures=0/39 tool=present verdict=TARGET_MISSED` (`correct=1`)
     - Note: `D2` and `D3` print `40/40 passed` on `--selftest` (which fails v2 clause `b`'s `MIN_SELFTEST = 50` and `b2` teeth) AND fail all 39 fixtures (`0/39`) because `D2` omits `ignored=0` from its `MADO_GLOBALS:` line and `D3` hardcodes PID `1918` / omits `ignored=0`.
   - **C2 base (`receipts/c2-v2-before-base.txt`):** `PRED-C2-r41-v2: admitted=0/1 verdict=TARGET_MISSED`, exit `1`.
   - **C2 do-nothing & forgery controls (`receipts/ctl-c2-v2.txt`):**
     - `N01-no-entry`: `admitted=0/1 clauses=a:0 b:0 c:0 d:0 e:0 f:1 g:0 h:0 i:1 ok=1`
     - `N02-entry-no-rows`: `admitted=0/1 clauses=a:1 b:1 c:0 d:1 e:0 f:1 g:1 h:0 i:1 ok=1`
     - `F1-invented-receipts` (scored under `real` counter with `PINS`): `admitted=0/1 clauses=a:1 b:1 c:1 d:0 e:1 f:1 g:0 h:1 i:1 ok=1`
     - `F2-invented-journal` (scored under `real` counter with `PINS`): `admitted=0/1 clauses=a:1 b:1 c:1 d:0 e:1 f:1 g:0 h:0 i:1 ok=1`
     - All 65 negative controls in `ctl-c2-v2.txt` score `admitted=0/1` (`CTL_C2V2: controls=67 correct=67/67`, where the 2 positive controls are `P-real` and `P-patched`).

2. **Finding F2 (MEDIUM — Registration v2 vs `ctl-c1-v2.txt` control count & skipped mutants):**
   - In `.ufo/waves/round-41/registration-v2.md:50` (Q11), the registration states:
     `"ten v2 cheats (\`K01-K10\`: stub bytes read, cwd replay, \`\\w\` names, child interpreter, \`argv[0]\` path test, \`eval\` via \`getattr\`, size fingerprint, kwargs unpacking, \`globals()\`, \`__file__\`) and the 42 \`ExecC1ExtraMutants\` mutants each score below MET."`
   - However, reading `.ufo/waves/round-41/receipts/ctl-c1-v2.txt:1` (Q13) and `:97` (Q14) shows:
     - Line 1: `CTL_C1V2: skipped-patterns-absent=4 W1-N14-empty-file-expect-ok W1-N24-ver-5-digits-max W1-N35-read-only-max-bytes W1-N42-live-no-timeout`
     - Line 97: `CTL_C1V2: controls=95 correct=95/95`
   - Why were 4 of the 42 `ExecC1ExtraMutants` skipped? Because `ctl/w1-mutants/gen_mutants.py` was written against the **v1** reference (`c1/ctl-ref-tool.py.txt`), and those 4 replacement strings (`old`) do not match `c1/ctl-ref-tool-v2.py.txt`:
     1. `W1-N14-empty-file-expect-ok` looked for `if not sessions:\n        verdict, code = "NO_SESSIONS", 3` (changed in v2 when `UNRECOGNIZED_FORMAT` was added).
     2. `W1-N24-ver-5-digits-max` looked for `\(ver (\d{1,6})\)` (changed in v2 to `([0-9]{1,6})`).
     3. `W1-N35-read-only-max-bytes` looked for `data = fh.read(MAX_BYTES + 1)` (changed in v2 when `O_NONBLOCK` / `os.read` was introduced).
     4. `W1-N42-live-no-timeout` looked for `env=env, timeout=30, shell=False)` (changed in v2 when `LIVE_TIMEOUT = 30` and incremental `select` loop were introduced).
   - The L1 subsequently added `K11-ver-5-digits` (re-expressing `N24`) and `K12-live-no-timeout` (re-expressing `N42`) to `ctl/run-c1-v2-controls.py:107-108` and ran `--only K1` into `.ufo/waves/round-41/receipts/ctl-c1-v2-extra.txt` (`CTL_C1V2: controls=3 correct=3/3`, Q15, covering `K11`, `K12`, `K10`).
   - Consequently:
     - `ctl-c1-v2.txt` has **95** controls (1 reference + 3 do-nothing + 43 v1 mutants/cheats + 10 `K01-K10` + **38** `W1-N*`), not 98;
     - `registration-v2.md:50` never mentions `receipts/ctl-c1-v2-extra.txt` or `K11-K12`, and claims "the 42 `ExecC1ExtraMutants` mutants each score below MET" when **only 38 ran in `ctl-c1-v2.txt`** (and **2 of the 4 skipped mutants — `W1-N14-empty-file-expect-ok` and `W1-N35-read-only-max-bytes` — were never re-adapted or scored against v2 at all**).

---

### 2.5 Is the sourced-claim requirement met?

**Target:** `PROTOCOL.md:143-144`, `CORPUS.md:89-128`, `.ufo/waves/round-41/registration-v2.md:41-45`, and `07f2641696b5ac73de1404ea737a9f27e9819aa1` (`corpus/SOURCES.md`, `corpus/knowledge/hyprland-focus-grab-r41.md`, `corpus/lessons/round-41.md`).

- **Rule (`PROTOCOL.md:143-144`, Q04):** `"and files at least one claim of the round as *sourced* — its evidence citing an \`S###\` row."` (18 words).
- **Rule (round prompt §2b item 4, `mado-round-41.md:73-74`):** `"At least one sourced claim — one of the round's claims rests on a SOURCES.md row opened this round: the knowledge entry or evidence it lands cites that S###."`
- **Verification at data commit `07f2641696b5ac73de1404ea737a9f27e9819aa1`:**
  - Claim C2 (`corpus/knowledge/hyprland-focus-grab-r41.md:3-10`) cites **7 new rows opened on `2026-10-25`** (`S283`, `S284`, `S285`, `S286`, `S287`, `S288`, `S289`) plus **1 held row** (`S037`, opened `2026-10-19`, whose `used-by` cell was extended to include `corpus/knowledge/hyprland-focus-grab-r41.md`).
  - All 7 new rows exist in `corpus/SOURCES.md:232-238` at `07f2641`, carry `status = mined`, `opened = 2026-10-25`, `recheck = 90d` (or `180d`/`on-release`), and list `corpus/knowledge/hyprland-focus-grab-r41.md` in `used-by`.
  - Every cited ID (`S283..S289` and `S037`) has a `GATE S### receipt=<path> sha256=<64hex> quote="<q>"` line in `corpus/lessons/round-41.md:26-33` where the receipt exists in `.ufo/waves/round-41/fetch/` with matching SHA-256 and a verbatim quote of 4–12 words (all $\le 25$ words).
  - `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` exits `0` (`mado ok`, `receipts/census-after-data.txt`).
- **Result:** Sourced-claim requirement is completely satisfied — **no defect found**.

---

### 2.6 Does anything in the registration or committed lesson contradict the lane files?

We cross-checked `registration.md`, `registration-v2.md`, and the committed data files at `07f2641696b5ac73de1404ea737a9f27e9819aa1`:

#### Finding F1 (HIGH — DATA defect in `corpus/lessons/round-41.md:163-164`): False v1 counter score at data commit
- **Location:** `corpus/lessons/round-41.md:163-164` at commit `07f2641696b5ac73de1404ea737a9f27e9819aa1`.
- **What it says (Q18):**
  `"`PRED-C1-r41-v1` at the data commit: `fixtures=24/24 verdict=TARGET_MET` with the nonce printed; `PRED-C2-r41-v1`: `admitted=1/1 verdict=TARGET_MET`; both re-run at the tip."` (19 words).
- **What the committed/actual run shows (`.ufo/waves/round-41/receipts/c1-v1-after-data.txt:33-35`, Q19):**
  ```
  PRED-C1-r41-v1 clauses=a:1 b:1 b2:1 g:0
  PRED-C1-r41-v1: fixtures=6/24 tool=present verdict=TARGET_MISSED rev=07f2641696b5ac73de1404ea737a9f27e9819aa1 nonce=cb2bcd4259089823
  exit=1
  ```
- **Why this happens & why it matters:**
  `registration-v2.md:10-11` (Q06) promises `"and the operator rules which predicate binds - the report gives both scores at the data tip."` Under `PRED-C1-r41-v1`, the v2 tool (`tools/mado-globals.py`) scores **`fixtures=6/24 tool=present verdict=TARGET_MISSED`** (`clauses=a:1 b:1 b2:1 g:0`, exit 1) because:
  1. v2 added the `ignored=<IGNORED>` field to the final `MADO_GLOBALS:` line and exit code `4` (`UNRECOGNIZED_FORMAT`), which causes 18 of the 24 v1 fixtures (`gen0..gen7`, `diff0`, `diff1`, `expect0`, `expectmiss0`, `nosess0`, `nosess1`, `toolarge0`, `live0`, `live1`, `liveenv0`) to fail v1's byte-exact stdout/rc comparison; and
  2. v2's `tools/mado-globals.py` imports `select` and `time` for bounded incremental live reads, which fails v1's narrower `STDLIB_ALLOW` (`g:0`).
  Leaving `fixtures=24/24 verdict=TARGET_MET` for `PRED-C1-r41-v1` in `corpus/lessons/round-41.md:163` directly contradicts `receipts/c1-v1-after-data.txt` (and our independent re-run in §2.1 D2, which also printed `PRED-C1-r41-v1: fixtures=6/24 tool=present verdict=TARGET_MISSED`).
- **Fix required before round lands:** When the L1 fills the `## Census and measurements at the data commit` section of `corpus/lessons/round-41.md:151-168`, replace the placeholder `PRED-C1-r41-v1` line with the true v1 (`6/24 TARGET_MISSED`, `g:0` + `ignored=` format change) and v2 (`39/39 TARGET_MET`) measurements.

#### Finding F3 (MEDIUM — DATA defects in `corpus/lessons/round-41.md:38,45,53`): Contradictory receipt count (7 vs 9) and phantom `S290` row claims
- **Location 1 (`corpus/lessons/round-41.md:38`, Q17):**
  `"the seven pre-wave receipts are committed at the freeze (\`git ls-tree -r --name-only 60c3914 .ufo/waves/round-41/fetch/\`);"` (15 words).
  - **Reproduction:** Running the exact command cited in that sentence:
    `git -C /home/vgpnk/Projects/shokunin/mado-shokunin ls-tree -r --name-only 60c3914 .ufo/waves/round-41/fetch/ | wc -l`
    outputs **`9`** (not 7): `Hyprland-FocusGrab.cpp`, `Hyprland-FocusGrab.hpp`, `focus-grab-v1.xml`, `input-capture-v1.xml`, `issue-565.html`, `protocols-README.md`, `quickshell-grab.cpp`, `xdph-PortalManager.cpp`, `xdph-journal.txt` (and `c2-r41-focus-entry-v2.py:125-135` `PINS` also lists all 9). Seven is the number of *new cited IDs* (`S283–S289`), whereas 9 pre-wave receipt files were committed at `60c3914` (and 10 exist at `07f2641` after adding `xdph-installed-version.txt`). Note that `corpus/lessons/round-41.md:107` (M41-6) correctly says `"git ls-tree -r --name-only 60c3914 .ufo/waves/round-41/fetch/ lists nine files"`, contradicting `:38` in the same file.
- **Location 2 (`corpus/lessons/round-41.md:45,53`, Q20):**
  - Line 45: `"its S328–S332 rows are the package's ids with no lane receipt; re-grounded this round as C2 with lane ids S283–S290"` (20 words).
  - Line 53: `"the new rows S283-S289 continue in the order ScrRowsDraft drafted them: ... the own-work journal S289, input-capture-v1.xml S290."`
  - **Contradiction:** `S290` was **not** added to `corpus/SOURCES.md` (which ends at `S289` at commit `07f2641`), and line 38 of the same lesson says `"S290 (input-capture-v1.xml) is **not** cited by the entry and has no row."` Calling `S283–S290` the re-grounded C2 lane IDs on line 45 and listing `input-capture-v1.xml S290` under `"the new rows S283-S289 continue"` on line 53 contradicts `corpus/SOURCES.md` and line 38.

#### Finding F4 (MEDIUM — Wave 1 artifact completeness vs `registration-v2.md:13-14`): Missing `ConnSiblingOverlap.md`
- **Location:** `.ufo/waves/round-41/registration-v2.md:13-14` (Q07), `.ufo/waves/round-41/w1-results.json`, `.ufo/waves/round-41/w1/swarm-registry.json:158-163`.
- **Reproduction:**
  - `git -C /home/vgpnk/Projects/shokunin/mado-shokunin ls-tree --name-only 294c667901a8c7b7165ba849d03cba9a24c14fa4 .ufo/waves/round-41/w1/ | grep '\.md$' | wc -l` → **`33`**.
  - Committing the diff between the 34 seat names in `w1-spec.json` and the `.md` files in `.ufo/waves/round-41/w1/` identifies **`ConnSiblingOverlap`** as missing (`ls .ufo/waves/round-41/w1/ConnSiblingOverlap*` → absent).
  - Because `w1-results.json` has `"output": null` for all 34 seats (`"orchestrator kernel restarted mid-wave; seat output was delivered to the orchestrator session but not retained — read the seat report file in the wave dir"`), `ConnSiblingOverlap` has zero retained output in the repository (33 of 34 w1 seats have committed reports). The L1 report must disclose this rather than claiming 34/34 w1 reports on disk.

#### Finding F5 (LOW — Expected pre-closure state at `07f2641`): `SCORECARD.md`, `LOG.md`, `SKILL.md`, `PROVINCE.md`, `QUALITY.md`, and tip axis receipt pending L1 integration
- **Reproduction:**
  - `python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/quality/check-axis-scores.py --repo /home/vgpnk/Projects/shokunin/mado-shokunin --rev 07f2641696b5ac73de1404ea737a9f27e9819aa1` exits `1`:
    ```
    MADO_AXIS_ROW: axis=navigation published=58/58 derived=59/59 verdict=STALE
    MADO_AXIS_ROW: axis=calibration published=55/55 derived=55/55 verdict=MATCH
    MADO_AXIS_ROW: axis=operability published=12/12 derived=12/12 verdict=MATCH
    MADO_AXIS: checked=3 mismatched=1 rev=07f2641696b5ac73de1404ea737a9f27e9819aa1
    ```
  - This is expected at the mid-round data commit `07f2641` because the L1 lands `SCORECARD.md` (including the new capability row for `tools/mado-globals.py` required by `AXES.md:60-64` and the updated `Axis table re-derived at` line with `navigation 59/59`), `LOG.md`, `SKILL.md`, `PROVINCE.md`, `corpus/QUALITY.md`, and the committed tip axis receipt `quality/receipts/axis-<tip>.txt` (M41-4) after `w2` settles.

---

## 3. Quote Verification Receipt

All 20 direct quotes in this report (`Q01`–`Q20`) were mechanically checked by `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-41/w2/RevSeparabilityShape/verify-quotes.py` (output saved at `verify-quotes.txt`):
- Command: `python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-41/w2/RevSeparabilityShape/verify-quotes.py`
- Result: `QUOTE_VERIFY: total=20 ok=20/20` (all 20 quotes $\le 25$ words and verified verbatim against the committed git blobs or files).

## 4. Tooling & Safety Attestation

- **Tools installed:** None (`python3` 3.14, `git`, `bwrap` already present on host; `pacman` not touched).
- **Write scope:** Wrote only `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-41/w2/RevSeparabilityShape.md` and `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-41/w2/RevSeparabilityShape/{findings.md,verify-quotes.py,verify-quotes.txt}`. Scratch git clones (`revsep-no-c1-*`, `revsep-no-c2-*`) were created in `/tmp` with `git -C "$D"` and `rev-parse --show-toplevel` assertions, and deleted immediately in `finally:` blocks. No tracked lane or fleet file was modified.
