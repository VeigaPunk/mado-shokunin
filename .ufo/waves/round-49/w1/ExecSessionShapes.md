# ExecSessionShapes — M48-8 part 2: session-material gate v3 draft

Seat `ExecSessionShapes` (executor, leaf), mado round 49 / wave w1 = BUILD, base `03e4ae76aff7a4be59cb69970dd553baa319695a`
(lane tip at round start). Target: the 16 `/home/<user>` receipt shapes round-48 w1 `SentPrivacy` showed the gate misses, plus
scopes beyond `.ufo/`, with each new rule shown able to fail. No package or tool transaction was run; nothing installed.

Draft: `.ufo/waves/round-49/w1/ExecSessionShapes/check-session-material.py` (2149 lines, sha256
`ffdc9d62c387050e016cf9d0eaacbf87f37d6647021cbd2c492eb6328dddbb61`). v2 at the same revision:
`quality/check-session-material.py` (1643 lines, sha256 `82c9053ae2e8b7db2fb8c0e195c32b8b151a593cf9412dcae3589427ac2dfa6f`;
identical at base and at the lane tip).

---

## 0. Verdict

**The draft works both ways.** It adds three rules (R7-R9), moves the default scope to the whole tracked tree, and keeps every v2
selftest case: **94/94 pass**, of which the **69 v2 case names are all present and unchanged** (`receipts/case-names.txt`).
Removing any one of the three rules makes exactly that rule's red cases fail and leaves its green counter-cases passing
(`receipts/mutation-both-ways.txt`, `MUTATION: rules=3 ok=3 failed=0`). On a fixture that carries the four round-48 receipt
shapes, v2 reports **0 findings with `--scope all` over the same 5 files** and v3 reports **5**
(`receipts/e2e-v2-blind-v3-red.txt`).

**v3 is red at base, by design and by measurement**: 265 findings (`--scope ufo`, v2: 159) and 273 (`--scope all`, v2: 167).
The 106 new lines are all in `.ufo/waves/`, all carry a real host value (absolute home path, account column, or cache title), and
are *true positives the lane already committed*. So the freeze needs the delta predicate SentPrivacy asked for (D-D), not exit 0:
`findings(rev) \ findings(base)`, with 159/167 (or 265/273 for v3) as the baseline.

---

## 1. What v3 changes

| change | where | why |
|---|---|---|
| `R7_HOME_PATH_PREFIX` — an absolute home path used **structurally**: `path:LINE:`, a listing header `path:`, a quoted path on a lowercase tool-diagnostic line, and a home path inside an `ls -l` data row | `scan_home_prefixes()` at draft:422, finding at :540 | the forms round-48 committed 230+ lines of; a path **in a sentence**, a `~/` or `$HOME/` form and a bare path line stay clean |
| `R8_ACCOUNT_COLUMN` — `ls -l`/`ls -lR` owner **or** group column equals the account name | `scan_account_columns()` at :459, finding at :546 | the leak with no `/home` prefix at all (PR-19); numeric ids and `root` stay clean, so `ls -ln` and a `--clearenv` capture are the compliant forms |
| `R9_EXEC_CACHE` — ≥2 column-0 record fields (`--dir=`, `--title=`, `--working-directory=`, `--app-id=`) | `scan_cache_fields()` at :478, finding at :550 | xdg-terminal-exec cache text (PR-10) and the `--title=` value R1 cannot see outside JSON (PR-01); indented usage text in the pinned script and prose about the flags stay clean |
| default scope `all` | `DEFAULT_SCOPE` at :217, CLI at :2101 | rounds 45-48 committed their adds in `corpus/`, `quality/counters/`, `tools/`; the old default `.ufo/` cannot read them (PR-13). `--scope ufo` still exists and is what the legacy-scope selftest cases now pass explicitly |
| `--account NAME` (default: the invoking account, resolved by `getpass`, never printed) | `invoking_account()` at :315, CLI at :2103 | R8 needs the account; print stays `rows=N`. An explicitly empty `--account` is exit 2 (:2127); an unresolvable one prints a stderr note and leaves R8 inert (:2132) |
| waiver band widened to R7-R9 (`MARKER_RE` `R[1-4789]_`, `WAIVABLE_RULES` at :261) with reserved-namespace checks (`home user`, `owner`, `title`/cache path) | `waiver_values_ok()` R7-R9 branches | a seat's own synthetic fixture must stay waivable, and a real user/title/owner must not be; R5/R6 stay non-waivable, so the round-47 marker-grammar cases still pass |
| `emit(stream=None)` late-binds `sys.stdout` | :1054 | `stream=sys.stdout` bound at def time, so `main()` could not be captured by a test; v2 callers that pass a stream are unaffected |

Rule order is `(R1,R2,R3,R4,R7,R8,R9,R5,R6)` so that `WAIVABLE_RULES + SERIAL_RULES == RULES` still holds byte-for-byte (the v2
`rules-partition-is-waivable-plus-serial` case).

---

## 2. Shape → rule, against the 16 missed shapes

Covered (each with a red case, a green counter-case, and a mutation receipt):

| PR | shape | rule | red case | green counter-case |
|----|-------|------|----------|--------------------|
| PR-14 | `grep -n` located line, absolute prefix | R7 prefix | `r7-grep-prefix-located-lines` | `r7-path-quoted-in-prose-clean` |
| PR-04 | flat `ls -LRl` of a home dir (one header, rows under R4's threshold) | R7 header | `r7-flat-listing-header` | `r7-tilde-and-dollar-home-forms-clean` |
| PR-15 | quoted path on a tool diagnostic (`xkbcommon: INFO: … "…"`) | R7 diag | `r7-quoted-path-in-diagnostic` | `r7-diagnostic-shape-in-prose-clean` |
| PR-05 | home path carried *inside* an `ls -l` row of a listing rooted outside `/home` | R7 row | `r7-home-path-in-ls-row` | `r8-numeric-ids-clean` (same row, numeric ids) |
| PR-19 | owner/group column = account name, no path | R8 | `r8-owner-and-group-column` | `r8-numeric-ids-clean`, `r8-other-owner-clean` |
| PR-10 | serialized exec-cache text | R9 fields | `r9-cache-record-fields` | `r9-flag-prose-and-indented-usage-clean`, `r9-one-field-under-threshold-clean` |
| PR-01 (in cache) | `--title=<free text>` | R9 title field | `r9-cache-record-fields` (detail masks the value) | `r9-one-field-under-threshold-clean` |
| PR-13 | material outside `.ufo/` | default scope | `v3-default-scope-all-sees-outside-ufo` | `e2e-outside-ufo-not-scanned` (with `--scope ufo`) |
| PR-06 | `~/`, `$HOME/` listing forms | **green by contract** | — | `r7-tilde-and-dollar-home-forms-clean` |

PR-06 is deliberately green, as the assignment requires: masking is the compliant form, and `w1/ExecXkbLive/probe.sh:23` already
does it (locator computed: `.ufo/waves/round-48/w1/ExecXkbLive/probe.sh:40`, `hide()`; comment at `:39`).

Two live receipts carry the worst case SentPrivacy named, and v2 reports **0** on both at base:

- `.ufo/waves/round-47/w2/RevengerCache/hash-input.txt` — the xdg-terminal-exec cache hash input. v3:
  `R7_HOME_PATH_PREFIX count=3 detail=forms=prefix:0,header:2,diag:0,row:1 paths=3` **and**
  `R8_ACCOUNT_COLUMN count=91 detail=rows=91`.
- `.ufo/waves/round-48/w1/ScrCacheDoc/receipts/warm-cache.txt` — the receipt SentPrivacy described as "PR-04 + PR-10 + PR-19 in
  one receipt that the gate calls clean". v3: `R7 … forms=…,row:1 paths=1` and `R8 … rows=2`. (R9 does not fire on it: its cache
  bytes are shown as an `od -c` dump, not as record lines, which is the declared gap in §6.6.)

Masked shapes are in §4.

Declared out of this draft, with the measurement that justifies each (docstring, draft:185-200):

| PR | why not |
|----|---------|
| PR-02, PR-03 | device `name`+`address` and `instance`/`/run/user/<uid>/hypr/` identity strings are a different predicate: a probe at base counts **415** candidate objects in **48** files, most of them Hyprland *source* (`fetch/*.cpp.bin`), so a shape rule would be dominated by code. Proposed as R10/R11, not shipped. |
| PR-07, PR-09 | encoding and binary are carriers, not material; decoding is unbounded, and the binary skip (NUL in first 8 KiB) is unchanged and still declared. |
| PR-08 | the >16 MiB tail is unreachable in this repo: the largest tracked blob at base is **4,207,542 B** (`.ufo/waves/round-20/w2/CorpusRuntime/full-sweep.jsonl`, `git ls-tree -r -l`). The cap stays a DoS guard and the docstring says so. |
| PR-11, PR-12, PR-16 | `ps`/`pgrep` dialects, secret-shaped values and user keymap *content* need their own structural predicates; none is a `/home/<user>` shape. |

---

## 3. Able to fail (mutation receipts)

`mutate.py <draft> <scratch>` deletes exactly one rule's block in `scan_blob()` (asserting the block occurs once), rewrites the copy
under the scratch dir, and runs the copy's selftest. `receipts/mutation-both-ways.txt`:

| rule removed | selftest | red cases that failed | green cases broken |
|---|---|---|---|
| R7 | 87/94 (7 fail) | 7/7 — the five `r7-*` red cases + `waiver-new-band-fixture-waived` + `waiver-r7-real-user-rejected` | none |
| R8 | 90/94 (4 fail) | 4/4 — `r8-owner-and-group-column`, `r8-detail-counts-only`, `v3-cli-default-scope-and-account-silent`, `waiver-new-band-fixture-waived` | none |
| R9 | 90/94 (4 fail) | 4/4 — `r9-cache-record-fields`, `r9-detail-counts-only`, `waiver-new-band-fixture-waived`, `waiver-r9-real-title-rejected` | none |

Green counter-cases stay green in every mutant (`red_missed=-`, `green_broken=-`, `ok=True` per rule).

End-to-end both ways (`fixture_e2e.py`, `receipts/e2e-v2-blind-v3-red.txt`): one throwaway repo (toplevel asserted) holding the four
round-48 shapes plus the masked/prose forms.

```
v2 default scope   rc=0  files=0  findings=0        <- .ufo/ blind spot
v2 --scope all     rc=0  files=5  findings=0        <- rule blind spot, same bytes
v3 --account       rc=1  files=5  findings=5        R7=3 R8=1 R9=1; the masked/prose file is clean
```

---

## 4. Base run: findings by rule, v2 vs v3

`python3 -I <gate> --repo <lane> --rev 03e4ae76… --scope {ufo,all}` (`receipts/base-scan-*.txt`, `receipts/comparison.txt`):

| rule | v2 `ufo` | v3 `ufo` | v2 `all` | v3 `all` |
|------|---------:|---------:|---------:|---------:|
| R1_CLIENT_DUMP | 38 | 38 | 39 | 39 |
| R2_PROC_TABLE | 38 | 38 | 41 | 41 |
| R3_MONITOR_IDENT | 58 | 58 | 59 | 59 |
| R4_HOME_LISTING | 3 | 3 | 3 | 3 |
| R5_SERIAL_PROSE | 22 | 22 | 25 | 25 |
| **R7_HOME_PATH_PREFIX** | — | **48** | — | **48** |
| **R8_ACCOUNT_COLUMN** | — | **54** | — | **54** |
| **R9_EXEC_CACHE** | — | **4** | — | **4** |
| **total** | **159** | **265** | **167** | **273** |
| files scanned | 22012 | 22012 | 22278 | 22278 |
| waived (gate-copy) | 3 | 3 | 3 | 3 |

R1-R5 are identical in both gates at both scopes (no v2 regression); the delta is exactly 48+54+4 = 106.

Where the new findings sit (`receipts/base-new-rule-samples.txt`, masked): **every** R7, R8 and R9 finding is under `.ufo/waves/` —
nothing in `corpus/`, `quality/` or `tools/`. By round: R7 is concentrated in round-48 (15), round-35 (13) and round-43 (3); R8 in
round-48 (13), round-23 (12), round-35 (12) and round-46 (7); R9 all 4 in round-47 (the `live-print` / `host-cache` receipts).
Sample shapes (masked, account and user replaced):

```
R7 prefix   /home/U/Projects/shokunin/mado-shokunin/.ufo/waves/round-16/measure.py:41: SyntaxWarning: …
R7 diag     environment: {"MADO_VERIFY_HARNESS": "/home/U/Projects/shokunin/…"}
R7 header   /home/U/.local/share/applications/:                 (round-47 cache hash input)
R8          -rw-r--r-- 1 USER USER  12 Oct 26 19:50 …           (round-23/48 ls receipts)
R9          --title=<value>  --working-directory=<value>        (round-47 cache receipts)
```

Note the R8 file count (54) exceeds the unindented `ls`-row count I measured first (12 files): the rule strips leading whitespace,
so rows inside Markdown code fences and block quotes are counted too — which is where rounds 46-48 wrote them.

---

## 5. Selftest: v2 preserved, v3 extended

`receipts/v2-selftest.txt` `SELFTEST: passed=69/69`; `receipts/v3-selftest.txt` `SELFTEST: passed=94/94`;
`receipts/case-names.txt` `v2_cases=69 v3_cases=94 missing_in_v3=0` and the 25 new case names.

Four v2 calls gained an **explicit** `scope="ufo"` because their fixtures are deliberately scope-shaped and the default is now
`all`; each assertion is byte-identical to v2:

- `e2e-outside-ufo-not-scanned` (`run(outside, "HEAD", scope="ufo")`)
- `e2e-empty-ufo-clean` (`run(empty, "HEAD", scope="ufo")`)
- `waiver-gate-copy-waived` and `waiver-gate-copy-mismatch-rejected` (their `quality/gate.py` fixture is an R1 carrier)

New cases: 18 unit (5 red for R7 + 3 green, 2 red for R8 + 3 green, 2 red for R9 + 3 green), 3 end-to-end (default scope through
`run()` and through `main()`, `--account` silent, empty `--account` refused), 3 waiver (new-band fixture waived, real user
rejected, real title rejected) and 1 self-source guard — 25 in total, names in `receipts/case-names.txt`.
`self-source-new-rules-clean` pins that the v3 fixtures are quoted strings: the gate's own bytes trip only R1-R3, so **the existing
`kind=gate-copy` registry row keeps its rule list** (only its sha and its byte-identical copy are refreshed).

---

## 6. Risks, limits, and what the freeze should know

1. **Red at base, both gates.** 159/167 (v2) and 265/273 (v3). A new true positive is indistinguishable from the baseline; the
   usable predicate is the delta, and v3's baseline must be recorded *after* the 106 known lines are either masked at the producer
   or accepted as the baseline. This is SentPrivacy's D-D, now with both numbers measured.
2. **The `header` form has live hits — and they are the worst case SentPrivacy named.** 3 files, 5 headers at base:
   `.ufo/waves/round-47/w2/RevengerCache/hash-input.txt` (`/home/U/.local/share/applications/:`, `…/applications/icons:`),
   `…/RevengerCache/w1-hash-recompute.txt` and `…/round-35/.../S210.rederive.txt` (masked sample in §4). `hash-input.txt` is the
   *xdg-terminal-exec cache hash input itself* — a home application inventory whose rows also carry the account column, so v3
   reports it **twice** (`R7 … header:2,row:1` and `R8 … rows=91`) where v2 reports nothing. The residual: an `ls -R` header rooted
   *outside* `/home` (`…/root2/data/applications/:`) is not a header by this rule; when its rows carry a home path or the account
   name, `row:`/R8 cover it, otherwise it is a declared gap.
3. **R7 `diag` is the broadest rule**: `^[a-z][a-z0-9_.+-]{0,32}:` plus a double-quoted `/home/...` path. It fires on
   `environment: {…}`, `stderr: xkbcommon: …` and any lowercase-prefixed log line — 8 files at base, all genuine dumps, but a
   prose sentence written as `note: "/home/u/x" is gone` would also match. Declared in the docstring. Form split at base
   (scope `all`, files): `prefix` 31, `diag` 8, `row` 13, `header` 3 (overlapping).
4. **R7 `prefix` assumes no whitespace before `:LINE:`.** A located line for a path with a space (`/home/u/My Documents/x:3:`)
   is missed; such paths are already R4's (threshold) business. Declared.
5. **R8 needs the account to resolve.** On a host where the scanning account differs from the material's account it under-detects
   (`--account` is the fix). It also does not see `stat -c`'s multi-line form or a row indented *and* broken across lines.
6. **R9's threshold is 2 fields.** A single pasted `--title=…` line is not a record; that is what keeps the pinned script's usage
   text and flag prose clean, and it is a declared gap.
7. **Counts are bounded by the 16 MiB prefix** for all rules, as v2 already declared; unreachable at this repo's 4.2 MB maximum, so
   the freeze can cite that rather than a caveat.
8. **Process note**: the draft is a seat file, not an edit of `quality/check-session-material.py`; the L1 integrates it (copy over
   the tracked gate, refresh the gate-copy sidecar + its registry sha, keep the rule list `R1_CLIENT_DUMP,R2_PROC_TABLE,R3_MONITOR_IDENT`).

---

## 7. Files and receipts

Written (all under my seat dir):

| path | what |
|---|---|
| `.ufo/waves/round-49/w1/ExecSessionShapes/check-session-material.py` | the v3 draft (sha256 `ffdc9d62…`) |
| `…/ExecSessionShapes/mutate.py` | rule-removal harness (the "able to fail" driver) |
| `…/ExecSessionShapes/sample_shapes.py` | masked characterisation of the new findings at a revision |
| `…/ExecSessionShapes/fixture_e2e.py` | v2-blind / v3-red end-to-end fixture |
| `…/ExecSessionShapes/receipts/v2-selftest.txt`, `v3-selftest.txt`, `case-names.txt` | 69/69, 94/94, 69⊆94 |
| `…/receipts/mutation-both-ways.txt` | per-rule removal: 7/4/4 red cases fail, no green case breaks |
| `…/receipts/base-scan-{v2,v3}-{ufo,all}.txt`, `comparison.txt` | the counts in §4 |
| `…/receipts/base-new-rule-samples.txt` | masked per-rule files-by-round + sample lines |
| `…/receipts/e2e-v2-blind-v3-red.txt` | 0 findings (v2, both scopes) vs 5 (v3) on the same 5 files |

Reproduce (lane root, `TMPDIR` in scratch):

```
python3 -I .ufo/waves/round-49/w1/ExecSessionShapes/check-session-material.py --selftest
python3 -I .ufo/waves/round-49/w1/ExecSessionShapes/mutate.py \
    .ufo/waves/round-49/w1/ExecSessionShapes/check-session-material.py <scratch>
python3 -I .ufo/waves/round-49/w1/ExecSessionShapes/fixture_e2e.py <scratch> quality/check-session-material.py \
    .ufo/waves/round-49/w1/ExecSessionShapes/check-session-material.py
python3 -I .ufo/waves/round-49/w1/ExecSessionShapes/check-session-material.py --repo . --rev 03e4ae76 --scope all
```

No compositor verb, no `hyprctl`, no network, no package transaction, no host state written: every fixture lives in
`/fast/scratch/hyaku/mado-r49/ExecSessionShapes/` with `HOME`, `XDG_*` and `TMPDIR` inside it, and the scratch dir is removed at the
end of the seat. Session material stays shape-only: the account name, home user and cache values are masked in every receipt above.
