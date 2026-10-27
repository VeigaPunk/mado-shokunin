# ExecGateV3 — C2 data: install-ready session-material gate v3

Seat `ExecGateV3` (executor, leaf), mado round 50 / wave w1 = BUILD + ATTACK, base
`8ae47b957034ae21012bbf09173cca2c48be345e`. Target: the session-material gate v3 (draft
`.ufo/waves/round-49/w1/ExecSessionShapes/check-session-material.py`, report `.ufo/waves/round-49/w1/ExecSessionShapes.md`)
as the C2 instrument, plus the counter CLI the round-50 C2 counter has to call. No package or tool transaction was run;
no compositor verb, no `hyprctl`, no network, no host state written.

## 0. Verdict

**Install-ready, byte-identical to the round-49 draft, re-measured at the round-50 base.** The seat file
`.ufo/waves/round-50/w1/ExecGateV3/check-session-material.py` (2149 lines, sha256
`ffdc9d62c387050e016cf9d0eaacbf87f37d6647021cbd2c492eb6328dddbb61`) is the draft unchanged: I found **no code defect**
that the draft's report or receipts name, and I did not widen a frozen-adjacent predicate on my own authority (§5). What this
seat adds is the round-50 evidence an integration decision needs: selftest `94/94` with all 69 v2 case names kept, the
`--scope all` / `--scope ufo` counts at `8ae47b95`, the both-ways mutation re-run on *this* copy, the v2-blind/v3-red e2e
fixture, a nonce-generated two-way probe (6/6 red carriers, 0 green false positives, no value printed), deterministic
re-scans, and the exact CLI contract for `PRED-C2-r50`.

The gate is **red at the base by design**: 228 findings (`--scope all`) / 220 (`--scope ufo`) against v2's 121 / 113. The
delta is exactly the three new rules' file counts (49+54+4 = 107), all under `.ufo/waves/`, all true positives the lane
already committed. A counter that demands exit 0 on the lane repository would be a broken predicate; §3 records the delta
and §4 the predicate to use instead.

## 1. Deliverables

| path (lane-relative) | what | sha256 |
|---|---|---|
| `.ufo/waves/round-50/w1/ExecGateV3/check-session-material.py` | the gate, install-ready | `ffdc9d62c387050e016cf9d0eaacbf87f37d6647021cbd2c492eb6328dddbb61` |
| `.ufo/waves/round-50/w1/ExecGateV3/mutate.py` | rule-removal harness ("able to fail"), from the draft | see `SHA256SUMS` |
| `.ufo/waves/round-50/w1/ExecGateV3/fixture_e2e.py` | v2-blind / v3-red end-to-end fixture | see `SHA256SUMS` |
| `.ufo/waves/round-50/w1/ExecGateV3/probe_nonce_shapes.py` | nonce-generated two-way probe (new this seat) | see `SHA256SUMS` |
| `.ufo/waves/round-50/w1/ExecGateV3/receipts/` | every run below, command + exit, masked | `SHA256SUMS` |
| `.ufo/waves/round-50/w1/ExecGateV3.md` | this report | — |

`receipts/`: `selftest.txt`, `case-names.txt`, `base-scan-v3-all.txt`, `base-scan-v3-ufo.txt`, `base-new-rule-samples.txt`,
`base-delta.txt`, `mutation-both-ways.txt`, `e2e-v2-blind-v3-red.txt`, `probe-nonce-shapes.txt`, `edge-shapes.txt`,
`cli-exit-codes.txt`, `self-scan-seat.txt`, `SHA256SUMS`.

## 2. What the gate is (unchanged from the draft)

`R1`-`R6` as installed v2, plus `R7_HOME_PATH_PREFIX` (an absolute `/home/<user>` path used *structurally*: a `grep -n`
located line, a listing header, a quoted path on a lowercase tool-diagnostic line, a home path inside an `ls -l` row),
`R8_ACCOUNT_COLUMN` (an `ls -l` owner **or** group column equal to the account), `R9_EXEC_CACHE` (≥2 column-0
`--dir=`/`--title=`/`--working-directory=`/`--app-id=` record fields). Default scope `all`; `--scope ufo` keeps the v2
behaviour. `--account NAME` (default: the invoking account, resolved with `getpass`, never printed). Waivable band widened to
`R7`-`R9` with reserved-namespace checks; `R5`/`R6` stay non-waivable. `emit(stream=None)` late-binds stdout.

Every printed finding is `FINDING file=<path> rule=<RULE> count=<n> detail=<masked>`: the detail carries counts, the
per-form split (`forms=prefix:N,header:N,diag:N,row:N paths=N`), `rows=N`, or field *names* (`keys=title+working-directory`)
— never a path, a user, an owner, a title or a cache value. The account is never printed; when none resolves, `main()` writes
one stderr note and `R8` is inert.

## 3. Runs (all receipts carry the command and the exit)

**Selftest** — `python3 -I <gate> --selftest` → last line `SELFTEST: passed=94/94 failed=0`, exit 0
(`receipts/selftest.txt`). The last-line format is v2's own (`SELFTEST: passed=%d/%d failed=%d`, gate:2087).
`receipts/case-names.txt`: `v2_cases=69 v3_cases=94 missing_in_v3=0`, plus the 25 new case names.

**Base scan at `8ae47b95`** on a `git clone -q --shared mado-shokunin <scratch>/clone` (toplevel asserted), `--repo <clone>`:

| rule | v2 `ufo` | v3 `ufo` | v2 `all` | v3 `all` |
|------|---------:|---------:|---------:|---------:|
| R1_CLIENT_DUMP | 39 | 39 | 40 | 40 |
| R2_PROC_TABLE | 37 | 37 | 40 | 40 |
| R3_MONITOR_IDENT | 12 | 12 | 13 | 13 |
| R4_HOME_LISTING | 3 | 3 | 3 | 3 |
| R5_SERIAL_PROSE | 22 | 22 | 25 | 25 |
| **R7_HOME_PATH_PREFIX** | — | **49** | — | **49** |
| **R8_ACCOUNT_COLUMN** | — | **54** | — | **54** |
| **R9_EXEC_CACHE** | — | **4** | — | **4** |
| **total findings** | **113** | **220** | **121** | **228** |
| files scanned | 22998 | 22998 | 23270 | 23270 |
| waived (sidecars) | 52/48 | 52/48 | 52/48 | 52/48 |

(Counts are per-rule **file** counts — that is v2's `SESSION_MATERIAL_RULES` convention and the sum equals `findings=`.)
`receipts/base-scan-v3-{all,ufo}.txt`, `receipts/base-delta.txt`. `R1`-`R5` are identical in both gates at both scopes: no
v2 regression. Two runs of `--scope all` are byte-identical (`DETERMINISTIC identical`), so a counter may compare counts
without tolerance. The round-49 spot-check's "gate is still red (110 findings)" is **v2 at `15510cb8`** (files=22066,
`w1/CritSidecars/receipts/gate-with.txt:167`), not this base: at `8ae47b95` v2 reports 121 / 113 and v3 228 / 220.

**Where the new findings sit** (`receipts/base-new-rule-samples.txt`, masked: `/home/<user>` → `$HOME`, owner/group →
`USER USER`, cache values → `<value>`): `R7 files=49 occurrences=284 out-of-ufo-files=0`, `R8 files=54 occurrences=368
out-of-ufo-files=0`, `R9 files=4 occurrences=9 out-of-ufo-files=0`. By round: R7 concentrated in round-48 (15) and round-35
(13), plus 1 in round-49 (the round-49 seat's own masked sample receipt, see F4); R8 in round-48 (13), round-23 (12),
round-35 (12), round-46 (7), round-47 (6); R9 all 4 in round-47 (the `live-print` / `host-cache` receipts). Nothing in
`corpus/`, `quality/` or `tools/` — the lane's prose and code planes are clean under the new rules.

**Both-ways mutation** — `python3 -I <seat>/mutate.py <seat>/check-session-material.py <scratch>` (draft harness, deletes
exactly one rule's block in `scan_blob()`, asserts it occurs once):

| rule removed | selftest | red cases that failed | green cases broken |
|---|---|---|---|
| R7 | 87/94 (7 fail) | 7/7 | none |
| R8 | 90/94 (4 fail) | 4/4 | none |
| R9 | 90/94 (4 fail) | 4/4 | none |

`MUTATION: rules=3 ok=3 failed=0` (`receipts/mutation-both-ways.txt`). Each rule is *able to fail* on its own red cases and
no green counter-case flips.

**e2e fixture** — `python3 -I <seat>/fixture_e2e.py <scratch> quality/check-session-material.py <seat>/check-session-material.py`
(`receipts/e2e-v2-blind-v3-red.txt`): one fixture repo, 5 files, toplevel asserted.

```
v2 default scope   rc=0  files=0 findings=0     <- the .ufo/ blind spot
v2 --scope all     rc=0  files=5 findings=0     <- the rule blind spot, same bytes
v3 --account …     rc=1  files=5 findings=5     R7=3 R8=1 R9=1; the masked/prose file is clean
```

**Nonce probe** — `python3 -I <seat>/probe_nonce_shapes.py <seat>/check-session-material.py <scratch>`
(`receipts/probe-nonce-shapes.txt`): two fixture repos generated with fresh `os.urandom` values for the home user, the
account, the cache title and the diagnostic program name.

```
red   (default scope, --account <nonce>) rc=1  6/6 carriers, each with its expected rule:
      R9 cache.txt · R8 ls-owner.txt · R7 ls-row.txt · R7 diagnostic.txt · R7 flat-listing.txt · R7 grep.txt
      4 of the 6 carriers live outside .ufo/ -> the run proves the default scope, not just the rules
green (default scope, no --account)    rc=0  files=3 findings=0
PROBE: failures=0        # no nonce value reached stdout on either run
```

**Own-deliverable self-scan** — the finished seat directory and this report were committed into a scratch fixture repo
(toplevel asserted) and scanned with the same gate: `files=18 findings=3`, and the three are R1/R2/R3 on the gate file
itself — its own embedded selftest fixtures — exactly the class round-48's gate copy carries a `kind=gate-copy` sidecar for.
**Every receipt and the report are clean under the gate** (`receipts/self-scan-seat.txt`, which lists the 18 files).

## 4. The CLI contract for `PRED-C2-r50`

The counter reads **only** `quality/check-session-material.py` at the revision and its own generated fixtures. Call it
exactly like this (`python3 -I`, so the fixture tree's own modules cannot shadow anything; `$FIX` is the counter's fixture
repo, `$NONCE` its generated account):

```
GATE="python3 -I quality/check-session-material.py"

# (1) detection — red carriers, inside AND outside .ufo/, through the DEFAULT scope
$GATE --repo "$FIX" --rev HEAD --no-waivers --account "$NONCE"
#    want rc=1
#    want one line  FINDING file=<carrier> rule=<R7|R8|R9> count=<n> detail=<masked>  per carrier
#    want           SESSION_MATERIAL_RULES: R7_HOME_PATH_PREFIX=<files> R8_ACCOUNT_COLUMN=<files> R9_EXEC_CACHE=<files>
#    want           SESSION_MATERIAL: files=<n> findings=<m> rev=<40-hex>
#    and  no line may contain $NONCE, the nonce user, the nonce title or the nonce program name

# (2) no false positive — green counter-shapes (~/$HOME forms, path in prose, numeric ids, one cache field)
$GATE --repo "$GREY" --rev HEAD --no-waivers
#    want rc=0 and  SESSION_MATERIAL: files=<n> findings=0 rev=<40-hex>

# (3) selftest at the revision
$GATE --selftest
#    want rc=0 and last line  SELFTEST: passed=<N>/<N> failed=0     (N=94) and v2's 69 case names all present
```

Contract details the counter may rely on:

- **Exit codes**: `0` no findings, `1` findings, `2` usage error or git failure (`--repo` missing, empty `--account`,
  unresolvable `--rev`, path not a repo). Nothing else.
- **Scope**: `--scope all` is the default; do **not** pass `--scope ufo` for the outside-`.ufo/` half of the shape set — a
  counter that passes it silently drops half the claim.
- **`--account` is mandatory for R8.** Without it the invoking account is used; in a `--clearenv`/bwrap run it may not
  resolve, and R8 then goes inert with one stderr note (measured: the red fixture yields `findings=5` instead of `6`,
  `receipts/cli-exit-codes.txt`). Always pass the nonce account.
- **`--no-waivers` for fixtures**: a fixture carries no registry, and a counter must score the rules, not the sidecars.
- Output lines are the only interface: `FINDING`, `WAIVER`, `WAIVER_REJECTED`, `SESSION_MATERIAL_RULES`,
  `SESSION_MATERIAL_WAIVED`, `SESSION_MATERIAL`, and (stderr) the inert-account note. Parse `rule=` and `count=`, never
  the detail text — the detail is a masked shape, not a stable field.
- Scans are deterministic and the tree is read from the object database: no checkout, no working-tree state, no writes.

## 5. Attack findings (this wave's second half)

Nothing here is a defect the draft's own report named; each is measured and located, and none was "fixed" by widening a
predicate the L1 has not frozen yet.

- **F1 — a diff- or bullet-prefixed structural line escapes R7.** Measured (`receipts/edge-shapes.txt`):
  `+ /home/<u>/x.conf:5: …`, `+/home/<u>/x.conf:5: …` and `- /home/<u>/x.conf:5: …` (markdown bullet) all come back
  **clean**, while the same line indented inside a code fence is caught. R7 anchors on `^/home/` after `strip` only
  (`HOME_GREP_RE` at gate:228). The lane writes its receipts in Markdown, so a pasted `grep -n` inside a bullet or a diff
  hunk is a real leak carrier the rule does not see. Fix would be a one-token widening (`[+-]\s?` prefix) — deliberately
  **not** applied here: it changes the red set the round-50 C2 claim enumerates, so it is an L1 freeze decision, not a
  seat decision. If the freeze keeps the current bytes, the counter's red fixtures must not use a prefixed line.
- **F2 — a prose sentence shaped like a diagnostic is a false positive.** `note: "/home/<u>/.xkb" is gone` is flagged as
  R7 `diag:1`. This is the draft's declared limit (report §6.3); I reproduce it. Consequence for the counter: a green
  "path in prose" fixture must not start with `<lowercase-word>: "<path>"` — the declared green forms are a backticked path,
  a bare path inside a sentence, a table cell and a command line (all measured clean).
- **F3 — the gate is red at the base, so C2's predicate cannot be "exit 0".** 228 (`all`) / 220 (`ufo`) at
  `8ae47b95`, of which 107 are R7-R9 and every one is a committed true positive (§3). The usable predicate is either the
  fixture-based one in §4 (what the round-50 claim states) or `findings(rev) \ findings(base)` with 228/220 as the recorded
  baseline.
- **F4 — my own seat's files will be red after commit, and so were round-49's.** A new file (the round-49 seat's gate copy
  at `.ufo/waves/round-49/w1/ExecSessionShapes/check-session-material.py`) trips R1/R2/R3 with no sidecar (3 findings at
  base), and the round-49 masked sample receipt trips R7 (1 finding, `forms=prefix:2,…,diag:1 paths=2`) even though every
  home user in it is masked to `U`: **`/home/U` is still a structural home path.** Hand-off: the L1 needs a `kind=gate-copy`
  `.synthetic` sidecar + registry row for the committed gate copy (and for this seat's copy, or delete the copies after
  integration), and the lane's masking convention for *structural* forms must be the gate's own green form — `$HOME/...` —
  not `/home/U/...`. My receipts use `$HOME` (§3) and are green under the gate (`receipts/self-scan-seat.txt`).
- **F5 — the waiver band is now R7-R9 wide.** A seat's own synthetic fixture can be waived, but `R7` needs a reserved home
  user, `R8` a reserved owner/group, `R9` a reserved title or a home path under a reserved user; a real user, owner or
  title is refused with `WAIVER_REJECTED … reason=value-not-synthetic:*`. `R5`/`R6` stay non-waivable
  (`reason=serial-rule-not-waivable`), including on a file that carries a valid marker.

## 6. Hand-off to the L1 (integration checklist)

1. Copy `.ufo/waves/round-50/w1/ExecGateV3/check-session-material.py` over `quality/check-session-material.py`. The bytes are
   the round-49 draft's (`ffdc9d62…`); the installed v2 is `82c9053a…`.
2. Refresh the `kind=gate-copy` `.synthetic` sidecar `.ufo/waves/round-48/w1/ExecSessionMarker/check-session-material.py`
   (byte-identical copy) **and** its `quality/session-material-waivers.txt` registry sha256, or the copy's waiver fails with
   `reason=gate-source-mismatch`. Keep that row's rule list `R1_CLIENT_DUMP,R2_PROC_TABLE,R3_MONITOR_IDENT` — the v3
   selftest pins it (`self-source-new-rules-clean`).
3. Decide F1 (widen R7 for a `+`/`-` prefix) before the freeze, not after: it changes the red set.
4. Tell the counter author: `--account` is mandatory, `--no-waivers` for fixtures, default scope is `all` (§4).
5. The lane repository stays red under v3 (F3); record 228/220 as the baseline if a delta predicate is used.
6. Two seat files (`mutate.py`, `fixture_e2e.py`, `probe_nonce_shapes.py`) are harnesses, not gate code; do not install them.

## 7. Limits, unchanged and re-stated for the freeze

The draft's declared gaps are unchanged and I re-measured the two that a counter could trip over: a path inside prose (clean),
a `~/`/`$HOME/` form (clean), a single bare path line under R4's threshold (clean), numeric ids and `root` owners (clean),
one cache field (clean), a `.desktop` `Exec=` line (clean). Still not seen: an `ls -R` header rooted outside `/home` whose
rows carry neither a home path nor the account name; `stat -c` multi-line output; a cache record split across files; an
encoded or binary/UTF-16 blob; a `ps`/`pgrep` dialect; secret-shaped values; the R10/R11 identity class; and (F1) a prefixed
structural line. The 16 MiB prefix cap stands as a DoS guard — the largest tracked blob at this base is 4,207,542 B (`git ls-tree -r -l 8ae47b95 | sort -n | tail -1`).

## 8. Process

Scratch `TMPDIR=/fast/scratch/hyaku/mado-r50/ExecGateV3` (clone, fixtures, mutants, selftest temp), `HOME`/`XDG_*` redirected
inside it, `ulimit -f 65536`, every loop bounded; removed at the end of the seat. No tracked file was edited, no mutating git
in the lane or the fleet, no `pacman`, no tool install. Session material stays shape-only: receipts carry lane-relative paths,
counts and masked shapes; the account and home user are never printed. Reproduce:

```
python3 -I .ufo/waves/round-50/w1/ExecGateV3/check-session-material.py --selftest
python3 -I .ufo/waves/round-50/w1/ExecGateV3/mutate.py \
    .ufo/waves/round-50/w1/ExecGateV3/check-session-material.py "$S"
python3 -I .ufo/waves/round-50/w1/ExecGateV3/fixture_e2e.py "$S" \
    quality/check-session-material.py .ufo/waves/round-50/w1/ExecGateV3/check-session-material.py
python3 -I .ufo/waves/round-50/w1/ExecGateV3/probe_nonce_shapes.py \
    .ufo/waves/round-50/w1/ExecGateV3/check-session-material.py "$S"
python3 -I .ufo/waves/round-50/w1/ExecGateV3/check-session-material.py \
    --repo "$CLONE" --rev 8ae47b957034ae21012bbf09173cca2c48be345e --scope all
```
