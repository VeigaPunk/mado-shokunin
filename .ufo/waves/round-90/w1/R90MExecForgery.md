# R90MExecForgery — cheap forgeries against the round-90 C1 and C2 counters

Seat: `R90MExecForgery` (leaf, no spawn). Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`, base
`5041acf99e27263872bf0441ad5f9d4316152605` (master). Round mado 90, hyaku run 15, wave w1.

**Every run below is DRAFT** (`--draft-tool` / `--draft-check`, exit 3). Nothing here is a measurement; nothing was
written under `.ufo/waves/round-90/receipts/`, and no case, mutant, label or candidate was edited.

Files written (relative to the lane):

- `.ufo/waves/round-90/w1/forgeries/c1-a-label-lookup.py`
- `.ufo/waves/round-90/w1/forgeries/c1-a-self.py` (a + self-integrity)
- `.ufo/waves/round-90/w1/forgeries/c1-b-oracle-shellout.py`
- `.ufo/waves/round-90/w1/forgeries/c1-b-self.py` (b + self-integrity)
- `.ufo/waves/round-90/w1/forgeries/c1-d-host-table.py`
- `.ufo/waves/round-90/w1/forgeries/c2-a-hardcoded-revs.py`
- `.ufo/waves/round-90/w1/forgeries/c2-b-commit-msg.py`
- `.ufo/waves/round-90/w1/forgeries/c2-c-bare-names.py`
- `.ufo/waves/round-90/w1/forgeries/c2-d-set-lookup.py`
- `.ufo/waves/round-90/w1/forgeries/c2-d-self.py` (d + self-integrity)
- `.ufo/waves/round-90/w1/R90MExecForgery.md` (this report)

Every forgery contains the frozen mutant `find` strings exactly once inside a dead `PADDING = r'''…'''` block. The
counter's only gate before scoring is `src.count(m["find"]) == 1` (C1 `quality/counters/c1-r90-portal-routing.py:247`,
C2 `quality/counters/c2-r90-receipt-presence.py:133`), so padding the strings is enough to be scorable without
implementing anything.

## 0. DRAFT baselines (real candidates, same host, same controls)

```sh
python3 quality/counters/c1-r90-portal-routing.py --repo <lane> --rev 5041acf9… --base-rev 5041acf9… \
  --cases …/controls/portal-cases-r90.json --mutants …/controls/portal-mutants-r90.json \
  --expect-cases-sha256 d76065d0… --expect-mutants-sha256 4b5127f8… \
  --scratch-root "$S/base-c1" --jobs 24 --draft-tool …/build/mado-portals.c1.py        # exit 3
MADO_PORTAL_ROUTING: DRAFT_TARGET_MET … cases=92 correct=92 mutants=31 killed=31 r12_rule_correct=20
  host_table_correct=10 base_tool=absent base_correct=0

python3 quality/counters/c2-r90-receipt-presence.py --repo <lane> --rev 5041acf9… --base-rev 5041acf9… \
  --set …/controls/receipt-presence-set-r90.json --mutants …/controls/receipt-mutants-r90.json \
  --expect-set-sha256 15c57903… --expect-mutants-sha256 1f9f9adf… \
  --scratch-root "$S/base-c2" --draft-check …/build/check-receipt-presence.c2.py          # exit 3
MADO_RECEIPT_PRESENCE: DRAFT_TARGET_MET … expectations=15 met=15 defects_detected=2/2 mutants=13 killed=13
  base_check=absent always_ok_met=7/15 always_missing_met=0/15
```

Both counters behave as declared against their candidates. The forgeries below test what the same predicates accept
from something that is not the candidate.

## 1. C1 — portal-routing resolver

| forgery | cases correct | mutants killed | DRAFT verdict | log line |
|---|---|---|---|---|
| (a) `c1-a-label-lookup.py` | **92/92** | 0/31 | `DRAFT_TARGET_MISSED` | `cases=92 correct=92 mutants=31 killed=0` |
| (a)+(c) `c1-a-self.py` | **92/92** | **31/31** | **`DRAFT_TARGET_MET`** | `cases=92 correct=92 mutants=31 killed=31` |
| (b) `c1-b-oracle-shellout.py` | **92/92** | 0/31 | `DRAFT_TARGET_MISSED` | `cases=92 correct=92 mutants=31 killed=0` |
| (b)+(c) `c1-b-self.py` | **92/92** | **31/31** | **`DRAFT_TARGET_MET`** | `cases=92 correct=92 mutants=31 killed=31` |
| (d) `c1-d-host-table.py` | 10/92 | 31/31 (spurious, see §1.5) | `DRAFT_TARGET_MISSED` | `cases=92 correct=10 mutants=31 killed=31` |

All five exit 3. Both `DRAFT_TARGET_MET` lines also carry `r12_rule_correct=20 host_table_correct=10
base_tool=absent base_correct=0` — i.e. the controls are healthy and the only thing the counter sees is a tool with
92/92 and 31/31.

### 1.1 (a) — the frozen labels are enough for 92/92

`forgeries/c1-a-label-lookup.py:96` opens
`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-90/controls/portal-cases-r90.json`; `signature()` builds
`(mode, desktop, {relpath: sha256(bytes)})` from the CLI arguments the counter already supplies (`--portal-dir` or
`--config-home/--config-dirs/--data-home/--data-dirs`) and returns the matching case's `oracle` / `oracle_reason`
verbatim (`reasons` fallback `"no-backend"`, which the counter maps to `None`). It contains no rule from
`xdp-portal-config.c`, no GKeyFile parser, no D-Bus-name check — and it answers **92/92**.

Reproducing input (one of 92): case `d01-host-replica`, `--desktop Hyprland`, dir mode; fixture files
`gtk.portal`, `hyprland.portal`, `gnome-keyring.portal`, `kwallet.portal`, `hyprland-portals.conf` exactly as stored
in the case file; the oracle's own labels are, e.g., `Lockdown → ['gtk']` (reason `default config`),
`Settings → ['gtk']` (reason `config`), `Screenshot → ['hyprland']` (reason `default config`). The forgery prints
those 21 pairs from the JSON, not from the configuration.

The **only** thing that rejected (a) is the mutant battery: every mutant edits dead padding, so all 31 survive.
The battery is not detecting "this is a lookup table"; it is detecting "the padding does not affect behaviour".

### 1.2 (c) — four lines of self-integrity turn the battery off

`forgeries/c1-a-self.py:3` holds `SELF_SHA256`, and `:13-14` normalise the digest line to 64 zeros and compare the
sha256 of the tool's own bytes before any argument parsing; a mismatch exits 7. The counter treats a non-zero exit as
`run_tool → None → case FAIL`, so a mutated copy fails its first case and is "killed" — all 31, on every case.
Result: **92/92 + 31/31 = `DRAFT_TARGET_MET`** for a tool whose case answers are still the frozen label file.

Evidence that the integrity check is the whole trick:

- real candidate + one appended comment (`\n# neutral comment appended by the forgery seat\n`):
  identical `picks`/`reasons` on `d01-host-replica`, `x02-user-iface-override`, `g09-invalid-escape-voids-file`;
- `c1-a-self.py` + the same appended comment: **exit 7**.

So a *behaviour-preserving* mutation is exactly the discriminator the counter lacks (§1.6 H1).

### 1.3 (b) — shelling out to `/usr/lib/xdg-desktop-portal`: forgery or legitimate implementation?

`forgeries/c1-b-oracle-shellout.py:98` reconstructs the one case from its CLI arguments, writes it as a one-case file
and runs `controls/portal-oracle-r90.py` (the round's own harness: private activation-free bus, fixture HOME, fixture
`XDG_RUNTIME_DIR`, unreachable system bus) — never the binary directly, so it stays inside the host-safety rule. It
then prints the oracle's `oracle`/`oracle_reason`. Result: **92/92**, 0/31 mutants (`DRAFT_TARGET_MISSED`); with the
same self-digest (b)+(c) it is **`DRAFT_TARGET_MET`** (`c1-b-self.py`, 92/92 + 31/31).

**Verdict: legitimate as an artefact, a forgery against PRED-C1-r90-v1 as declared — and the counter cannot tell the
difference.** The argument:

*For legitimate.* If the deliverable were "what will this host's portal binary choose", querying the binary is the
authoritative, read-only, version-faithful implementation; it needs no model of `xdp-portal-config.c` and cannot drift
from the installed 1.22.1. Delegation is a normal engineering choice for an oracle-backed diagnostic.

*Against, under this claim.* (1) The declaration's C1 surface is a resolver **modelled on `src/xdp-portal-config.c`**
and its count is "interfaces the lane can resolve by a tool"; a delegation resolves nothing the binary does not, and
the round-12 knowledge gap (14 hand-derived interfaces, no `none`/`*`/UseIn/last-resort rules) stays unfilled.
(2) The counter's oracle **is** the same binary: cases, labels and a delegating tool share one source of truth, so the
measurement is a tautology — 92/92 is guaranteed by construction and cannot reveal a modelling error. (3) It changes
the artefact's operational shape: it needs a private bus and the binary at measure time, is coupled to the installed
package, cannot answer "what would 1.22.1 do for this layout" without running it, and cannot explain a decision; it
also enlarges the safety surface of a tool advertised as a resolver. (4) It makes the mutant battery meaningless: 31/31
of the mutants are inert wrapper edits, and only a source-integrity check (b)+(c) is needed to pass.

Recommendation for the freeze, choose one and write it in the predicate: **(i) delegation allowed** — then the claim
must stop saying "models `xdp-portal-config.c`" and must accept that the counter measures the binary; or **(ii)
delegation forbidden** (the current wording) — then enforce H2/H3 and add H4 below.

### 1.4 (d) — the host table is already impossible by construction

`forgeries/c1-d-host-table.py` prints the `d01-host-replica` vector for every input: 10/92 correct. The counter's own
`host_table_correct=10` and the `met` predicate's `host_correct < n` (`c1-r90-portal-routing.py:270`) make a pure host
table unable to reach `TARGET_MET` as long as the case set is not all host replicas. This is the one vector already
covered — by a control, not by the battery. Keep it.

### 1.5 Counter defect (both counters): a "kill" is counted if the mutated copy fails any case, including cases the
unmutated tool already fails

- C1 `quality/counters/c1-r90-portal-routing.py:253`:
  `first = next((c["id"] for c, ok in zip(cases, mres) if not ok), None)` — `mres` is compared only to the labels.
- C2 `quality/counters/c2-r90-receipt-presence.py:138`:
  `first = next((i for i, ok, _ in evaluate(mp, spec, repo, fixtures) if not ok), None)` — same.

`res` (the unmutated results) is already computed in both counters and never consulted. Consequence, measured here:
the host-table tool (10/92) reports **31/31 killed**, every one "killed by `d04-desktop-unset`", a case it already
fails; C2 (a)/(b) (11/15) report 13/13 "killed by `W2-on-disk-not-carried`", and (c) (4/15) 13/13 "killed by `D88`".
The predicate still refuses MET because `correct == n` / `good == n` is also required, so this does not by itself
create a false pass — but it makes `killed` uninformative for any adversarial tool and hides that the battery has no
discriminating power once the tool is not the candidate.

Fix (both): keep the unmutated result vector and count a mutant only when it fails a case the unmutated tool **passes**:

```python
# C1, after res = score_tool(tp, cases, work, a.jobs)
mres = score_tool(mp, cases, work, a.jobs)
first = next((c["id"] for c, ok, ok0 in zip(cases, mres, res) if ok0 and not ok), None)
# C2, after res = evaluate(cp, spec, repo, fixtures)
base_ok = {i for i, ok, _ in res if ok}
first = next((i for i, ok, _ in evaluate(mp, spec, repo, fixtures) if i in base_ok and not ok), None)
```

### 1.6 C1 hardening, cheapest first

**H1 — require a neutral (behaviour-preserving) mutant to survive.** Add to `portal-mutants-r90.json` one entry with
`"neutral": true`, e.g. `find` = the banner at
`build/mado-portals.c1.py:235` `# ---------------------------------------------------------------- model`,
`replace` = the same banner with one dash dropped (occurs exactly once, changes no behaviour), and to the predicate
`neutral_correct == n` (compare `picks`/`reasons`, not raw output — `--json` embeds fixture paths). Any tool that reads
its own source dies: demonstrated above (candidate unchanged; `c1-a-self.py` + one comment → exit 7). This is the
decisive kill for (c) and for every self-digest variant; it costs 92 extra tool runs.

**H2 — provenance scan of the tool source before scoring.** Refuse to score when the tool text contains any of
`.ufo/waves/round-90/controls`, `portal-cases-r90.json`, `portal-oracle-r90.py`, `/usr/lib/xdg-desktop-portal`,
`dbus-run-session`, or a self-hash of `__file__`. Cheap; catches (a), (b) and (c) as written (all three name the path
or read `__file__`). Evadable by obfuscation — it is a cost raise, not a proof.

**H3 — hide the answers and the binary at measure time.** `bwrap` is installed on this host (`/usr/bin/bwrap`,
verified read-only); wrap each `run_tool` invocation with
`bwrap --dev-bind / / --tmpfs <lane>/.ufo/waves/round-90/controls --tmpfs /usr/lib/xdg-desktop-portal -- python3 -I …`.
The label file disappears from the tool's namespace, and the oracle binary cannot be started even if a copy of the
script is reached. A legitimate model reads only the fixture paths and the host portal configuration, all still bound.

**H4 — one held-out case labelled at measure time.** Generate a fixture with a random backend name and a random
`UseIn` token, label it by invoking `controls/portal-oracle-r90.py` (or its `run_case`) during the run, and require
agreement. A frozen-label lookup (a) cannot answer it; a delegating tool (b) can — which is why H4 must be paired with
H2/H3 (or with the policy decision in §1.3).

**H5 — the kill-accounting fix of §1.5.** Without it, H1's neutral mutant itself would be reported as "killed" by any
already-failing case.

## 2. C2 — receipt-presence check

| forgery | expectations met | mutants killed | DRAFT verdict | log line |
|---|---|---|---|---|
| (a) `c2-a-hardcoded-revs.py` | 11/15 | 13/13 (spurious, §1.5) | `DRAFT_TARGET_MISSED` | `expectations=15 met=11 … killed=13` |
| (b) `c2-b-commit-msg.py` | 11/15 | 13/13 (spurious) | `DRAFT_TARGET_MISSED` | `expectations=15 met=11 … killed=13` |
| (c) `c2-c-bare-names.py` | 4/15 | 13/13 (spurious) | `DRAFT_TARGET_MISSED` | `expectations=15 met=4 … killed=13` |
| (d) `c2-d-set-lookup.py` | **15/15** | 0/13 | `DRAFT_TARGET_MISSED` | `expectations=15 met=15 … killed=0` |
| (d)+(c) `c2-d-self.py` | **15/15** | **13/13** | **`DRAFT_TARGET_MET`** | `expectations=15 met=15 … killed=13` |

All five exit 3. The three "13/13 killed" rows are artifacts of §1.5: their unmutated checks already fail `W2`/`D88`,
so every mutant is killed by that same expectation regardless of what it does.

### 2.1 (a) hardcoded revision verdicts — 11/15

Four revisions are answered from a literal table (D88 rc 1 `harm-final-r88.txt`; D89 rc 1 the two r89 names; C88/C89
rc 0), every worktree fixture returns OK. The four MISSING fixtures fail exactly as they should:
`W2-on-disk-not-carried`, `W3-absent`, `W7-json-receipt-missing`, `W9-new-untracked-lesson` (`rc=0 missing=[]` where
`rc=1` was expected). A check that only hardcodes the *revisions* cannot pass; the fixture half of the set carries the
weight.

### 2.2 (b) commit-message grep — 11/15

`git log -1 --format=%s` contains `records` for D88 (`round-88: records — …`) and D89
(`round-89: records — …`), and not for C88 (`…residual r1 evidence…`) or C89 (`…residual r1 evidence…`), so the four
revisions pass by subject text alone. It fails the same four MISSING fixtures. Note the correlation is coincidental:
the distinguishing property of the two clean commits is *not* their subject.

### 2.3 (c) flag every bare `receipts/` name — 4/15

Every bare citation is reported missing. D88 cites five bare names (only `harm-final-r88.txt` is missing) → 5 missing
vs expected 1; D89 8 vs 2; C88 2 vs 0; C89 3 vs 0; `W1`, `W4`, `W5`, `W8`, `W11` all cite present receipts → false
MISSING. The check matches only `W2`, `W7`, `W9` (and misses `W3` because its citation is a full path). The counter's
existing `always_missing_met=0/15` control is the same lesson: exact missing sets, not "any missing".

### 2.4 (d) read the frozen expectation set — 15/15, then MET

`forgeries/c2-d-set-lookup.py` opens
`.ufo/waves/round-90/controls/receipt-presence-set-r90.json` and echoes the expected verdict. It identifies the
revision by `git rev-parse --verify <rev>^{commit}` against `revisions[].rev`; in worktree mode it identifies the
fixture by `(round, sorted(commit_paths), HEAD content of every base file, disk content of every work file)` — enough
to separate the two ambiguous pairs (`W1`/`W2` share bytes but differ in `commit_paths`; `W2`/`W6` share
`commit_paths` but differ in base/work bytes). It met **15/15** including `defects_detected=2/2`; the 13 mutants
survive (0/13). `c2-d-self.py` adds the same self-digest as §1.2 and reaches **`DRAFT_TARGET_MET`** (15/15 + 13/13).

Reproducing inputs: revision `498855cb327cd4e3debfa9446ea38398c216dda1` (expected rc 1, exactly
`receipts/harm-final-r88.txt`), and fixture `W2-on-disk-not-carried` (SCORECARD.md cites
`receipts/harm-final-r90.txt`; the file exists on disk but the commit paths are `['SCORECARD.md']` only). The forgery
answered both from the set file, with no diff parsing and no `cat-file` presence test.

### 2.5 C2 hardening

**H1′ — neutral mutant must survive.** Add one comment/docstring-only mutation to `receipt-mutants-r90.json` (e.g.
`Citation grammar:` → `Citation syntax:` in `build/check-receipt-presence.c2.py`, payload-neutral, occurs once) and
require it not to change any expectation. Evidence: candidate + appended comment → identical summaries on D88 and C88;
`c2-d-self.py` + the same comment → exit 7.

**H2′ — one held-out fixture built at evaluation time.** This is the decisive correctness fix against (d) and every
hardcoded variant, because the answer is not in any file the check can read:

```python
nonce = uuid.uuid4().hex
held = {"id": "H-heldout", "round": 90,
        "base": {"SCORECARD.md": "# s\n"},
        "work": {"SCORECARD.md": f"# s\n- held `receipts/heldout-{nonce}-r90.txt`\n"}}
# built like build_fixture(); expected rc 1, expect_missing = [f"receipts/heldout-{nonce}-r90.txt"]
```

Add a carried twin (`work[.ufo/waves/round-90/receipts/heldout-<nonce>-r90.txt] = "ok\n"` and the matching
`commit_path`) expecting rc 0. A set lookup cannot match either fixture and falls back to OK, failing the first one; a
commit-subject forgery fails both. Cost: two fixture builds and two check runs.

**H3′ — hide the controls tree.** `bwrap --dev-bind / / --tmpfs <lane>/.ufo/waves/round-90/controls -- python3 -I …`
around `run_check`, exactly as C1 H3. The check legitimately needs only the fixture repo and `git`.

**H4′ — provenance scan.** Reject a draft/measured check whose source contains `.ufo/waves/round-90/controls`,
`receipt-presence-set-r90.json`, or a `__file__` self-hash.

**H5′ — kill accounting** per §1.5. Prerequisite for H1′ and for any meaning in the `killed=` field of an adversarial
draft.

**H6′ — control balance (secondary).** `always_ok_met=7/15` is printed but not gated; with two held-out fixtures the
constant-OK forgery drops to 7/17 and the set has 4+1 MISSING expectations. Keeping a deliberate OK/MISSING balance
in any added fixtures is what makes the always-OK control informative.

## 3. Dead steps and errors (with text)

1. `gen.py` v1 build failed: `c2-c-bare-names.py … mutant-count-errors {'K03': 2, 'K04': 2}` — the literal
   record-file regex in the forgery duplicated the frozen `find` strings (`|corpus/lessons/[^/]+\.md`,
   `^(SCORECARD\.md|LOG\.md|`). Fixed by a literal `is_record()` helper; generator then reported
   `mutant-count-errors {}` for all ten files and `GEN_EXIT=0`.
2. `c2-d` bodies kept the generator placeholder: `FileNotFoundError: [Errno 2] No such file or directory:
   '@@LANE@@/.ufo/waves/round-90/controls/receipt-presence-set-r90.json'`. Fixed by applying `fill(BODY_C2_D)`;
   `grep -c '@@LANE@@' *.py` → 0.
3. First C1 (a)/(a-self) draft: `case g04-crlf FAIL`, `correct=91`. Cause: the forgery read fixture files in text
   mode, normalising the case's CRLF to LF before hashing. Fixed with `open(p, "rb").read().decode("utf-8")`; rerun
   is 92/92 (reported above). This was a forgery bug, not a counter defence.
4. First smoke harness run: `NameError: name 'S' is not defined` (shell variable not expanded inside a quoted
   heredoc); fixed by assigning `S` in Python. No effect on any reported number.

## 4. Installs

None. No pacman transaction, no uv/npx/binary install. Read-only availability checks only:
`/usr/bin/bwrap`, `/usr/bin/strace`, `/usr/bin/unshare`, `/usr/bin/setpriv`.

## 5. Scratch

Seat scratch `S=/fast/scratch/hyaku/mado-r90/R90MExecForgery` (clones, fixtures, per-case materialisations, oracle
scratch, run logs) was removed with `rm -rf -- "$S"` on exit. No file under `$S` was needed as a receipt; the verdict
lines are reproduced verbatim above.
