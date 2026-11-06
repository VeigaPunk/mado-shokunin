# R88MResidMut — residual mutation probe of the frozen r88 case sets

Seat: mutation-tester (residual attack seat, r1). Lane: `mado-shokunin`. Round 88, wave r1.
Scope: frozen and measured bytes only. No lane file outside this report was written; no git/jj mutation
was run anywhere (no fixture repo was needed — scoring went through the counters' `evaluate` in memory).

## 1. Bytes under test (all read with `git show <rev>:<path>`, never the working tree)

| item | rev | sha256 | pin |
|---|---|---|---|
| C1 tool `tools/mado-mako.py` | `650e18bdf0ae404ec9a80874c4503ecf3237e8e6` | `07930521f8e4…e89c3` | matches `receipts/c1-measured-A-r88.txt` |
| C2 tool `tools/mado-mako.py` | `7d3074865a9f5acfa0f1c9c66b460e73d4031331` | `c374d71514f1…92237` | matches `receipts/c2-measured-B-r88.txt` |
| base tool | `24ba2a9ddac21c1211579231e6ee1d98963f9988` | `67a955a5fa06…c986698` | declaration base |
| `.ufo/waves/round-88/controls/mako-cases-r88.json` (N=62) | `650e18b…` | `a0e81b191fb0…fab4a091` | freeze `## Freeze` |
| `.ufo/waves/round-88/controls/containment-cases-r88.json` (K=26) | `7d30748…` | `8b16c0cb0d73…4f20d039` | freeze `## Freeze` |
| `quality/counters/c1-r88-mako-fields.py` | `650e18b…` | `3678425addb5…fe11cc1f` | freeze `## Freeze` |
| `quality/counters/c2-r88-include-containment.py` | `7d30748…` | `f8e18b7c915f…409e96767` | freeze `## Freeze` |
| `quality/counters/c1-r87-mako-criteria.py` (machinery) | via C1/C2 counters | `4d801c30b302…a2ed3645` | R87_COUNTER_SHA256 |

Baseline reproduced through the counters' own `evaluate`: C1 candidate correct **62/62**, C2 candidate
correct **26/26** — equal to `MADO_MAKO_FIELDS: TARGET_MET … correct=62` and
`MADO_MAKO_CONTAINMENT: TARGET_MET … correct=26` in the measured receipts. So every mutant below was
scored against the same predicate the round was measured on.

## 2. Method

Driver `/fast/scratch/hyaku/mado-r88/R88MResidMut/driver.py` imports each frozen counter from its
git bytes (`importlib`, `sys.argv` untouched), loads the frozen case file with the counter's own
`load_cases`, and calls

* C1 `evaluate(mutant_text, base_text, cases, [], scratch, 0, declared=None, carried_needed=22)`
* C2 `evaluate(mutant_text, base_text, cases, [], scratch, declared=None)`

i.e. the frozen predicate scoring path with the mutant list empty and `declared=None`; each mutation is
applied **in memory** to the measured tool text (`tool_text.replace(old,new,1)` after asserting the anchor
occurs exactly once — 15/15 anchors occur exactly once, so no setup-error exit 2). A mutant is
*killed* only by the counters' own `semantic_kill` (verdict differs on some case **and** the mutant was
well-formed there); a mutant that only crashes is reported as `crashed-not-killed`, per the frozen rule.
Survivors were then probed with one extra case (outside the frozen set) run through the same
`evaluate` with `range_check=False`: the candidate must pass the probe and the mutant must fail it, or
the probe is not reported as distinguishing.

## 3. C1 tool — 8 residual mutants (frozen set, N=62)

| mutant | semantic change | verdict | differing frozen cases | mutant correct |
|---|---|---|---|---|
| RM1C1-string-field-casefolded | five string criteria fields compared casefolded (`c1-tool.py:364`) | **killed** | c33-summary-mismatch-case-sensitive | 61/62 |
| RM2C1-app-name-casefolded | app-name compared casefolded (`:358`) | **survived** | — | 62/62 |
| RM3C1-bang-accepted-on-string-fields | bare `!<string field>` accepted as the literal `"false"` (`:310`) | **survived** | — | 62/62 |
| RM4C1-normalize-lowercases-non-boolean-keys | `normalize()` lowercases every non-boolean value (`:182`) | **killed** | c01, c09, c13, c14 | 58/62 |
| RM5C1-mode-criteria-casefolded | mode criteria compared casefolded (`:348`) | **survived** | — | 62/62 |
| RM6C1-boolean-word-yes-accepted | `parse_boolean` accepts `yes` (`:164`) | **killed** | c50, c56 | 60/62 |
| RM7C1-include-accepted-inside-criteria | `include=` inside a criteria section followed instead of refused (`:292`) | **survived** | — | 62/62 |
| RM8C1-undecided-refused-despite-mismatch | mismatch short-circuit removed, so `mismatch`+`undecided` refuses (`:372`) | **killed** | 14 cases (c03, c05, c08, c10, …) | 48/62 |

Mutant text digests (sha256 prefix): RM1 `26b53365117484a0`, RM2 `996a6f8570962d05`,
RM3 `bc6c4da588650837`, RM4 `c82d6be871e35501`, RM5 `ba47e1e3cf2f0721`,
RM6 `43e9289de4447116`, RM7 `a456ecae51466b18`, RM8 `b4fa8a988323d74a`.

### 3.1 C1 survivors and the case the frozen set lacks

All four probes were run through the frozen C1 counter (`load_cases` on a 1-case document,
`range_check=False`); in each, the **candidate passes** and the **mutant fails**, so each probe is a
genuine distinguishing case, not an expectation artifact.

1. **RM2C1 `app-name` casefold survives.** No frozen case has an `app-name` criterion whose case
   differs from the supplied `--app-name` (checked: the only differing-case pair in the whole set is
   c33's `summary` Hello/hello). The declaration claims "exact string equality (upstream `criteria.c`
   `match_criteria` uses `strcmp`)" and pins it with **one** case, for `summary` only.
   Missing case `probe-appname-case-differs`: config `anchor=bottom-left` + `[app-name=Alpha]` +
   `anchor=bottom-center`, args `--app-name alpha` → candidate `anchor=bottom-left` (ok); mutant
   `FAIL mismatch anchor` (casefolded match applies the override).
2. **RM3C1 bare `!` on a string field survives.** The only bare-`!` case in the set is
   c47 (`[!actionable]`, `[!expiring]`) — booleans. L510-516 documents bare tokens for
   actionable/expiring only; the candidate refuses `!app-name`, the mutant silently treats it as
   `app-name="false"`.
   Missing case `probe-bang-string-field`: config `[!app-name]` with `--app-name alpha` → candidate
   `refusals present` (ok); mutant `FAIL missing-refusal` (section reduces to a nomatch).
3. **RM5C1 `mode` casefold survives.** Every frozen mode value and every `--mode` argument is
   lowercase (checked over all 62 cases), so case-sensitive membership and casefolded membership are
   indistinguishable.
   Missing case `probe-mode-case-differs`: `[mode=Do-Not-Disturb]` with `--mode do-not-disturb` →
   candidate `anchor=bottom-left` (ok); mutant `FAIL mismatch anchor`.
4. **RM7C1 `include=` inside a criteria section survives.** No frozen case puts an `include=` after a
   `[...]` header (checked: 0 cases). The stance is a global-only option (L45, and the tool's own
   selftest at `c1-tool.py:549` (`include-in-criteria`)).
   Missing case `probe-include-in-criteria`: `[app-name=alpha]` then `include=~/.config/mako/core.ini`
   where `core.ini` sets `layer=bottom` → candidate refuses (`refusals present`, `layer=top`) and
   passes; mutant applies the include (`FAIL missing-refusal`).

## 4. C2 tool — 7 residual mutants (frozen set, K=26)

| mutant | semantic change | verdict | differing frozen cases | mutant correct |
|---|---|---|---|---|
| RM1C2-roots-not-resolved | declared roots used unresolved, no `realpath` of the root (`c2-tool.py:470-471`) | **killed** | k24-symlinked-read-root | 25/26 |
| RM2C2-opens-unresolved-target | containment tested on `real`, but `target` is what is opened (`:463`) | **survived** | — | 26/26 |
| RM3C2-trailing-slash-refusal-dropped | the `target.endswith("/")` refusal deleted (`:437`) | **survived** | — | 26/26 |
| RM4C2-double-slash-join-dropped | `~//x` no longer re-joined under HOME, becomes absolute `/x` (`:430`) | **survived** | — | 26/26 |
| RM5C2-root-equality-refused | `real == root` refused; only strict descendants covered (`:276`) | **survived** | — | 26/26 |
| RM6C2-cycle-detected-on-lexical-target | cycle test compares unresolved `target` against a stack of resolved paths (`:458`) | **survived** | — | 26/26 |
| RM7C2-config-subject-to-roots | `--config` subjected to the read roots (stance: exempt) (`:473`) | **killed** | k15-config-outside-home | 25/26 |

Mutant text digests (sha256 prefix): RM1 `db6fae7ab4e44c2c`, RM2 `57b0b5bf2340419a`,
RM3 `63d1e96167f5da15`, RM4 `b7ff72675141900b`, RM5 `8fce9faddb6fa4cb`,
RM6 `c48052bc1c246514`, RM7 `db01217d9c158697`.

### 4.1 C2 survivors and the case the frozen set lacks

1. **RM3C2 trailing `/` survives.** No frozen include target ends in `/` (checked: 0 of 26). The
   refusal was added in draft revision 4 (R88MReviewC2 F8) and is exercised **only by the tool
   selftest** (selftest case `trailing-slash`, `c2-tool.py:662`), never by the case file that scores
   the predicate — a receipt gap: a stance sentence with no frozen case.
   Missing case `probe-trailing-slash`: config `width=1` + `include=~/inc.ini/` with `home/inc.ini`
   present → candidate `width=1`, `refusals present` (ok); mutant `FAIL missing-refusal`.
2. **RM4C2 `~//x` survives.** No frozen case uses `~//` (0 of 26); the join rule (draft revision 4,
   F8) again has selftest-only coverage (`c2-tool.py:660`).
   Missing case `probe-double-slash`: `include=~//inc.ini`, `home/inc.ini` sets `width=321` →
   candidate `width=321`, `refusals none` (ok); mutant `FAIL unexpected-refusal` (joins to `/inc.ini`,
   outside every root).
3. **RM5C2 root equality survives** — and the branch is *live*, not dead: every frozen `--read-root`
   is a directory (k07 `roots`, k13 `outside`, k14 `roots`, k24 `rootlink`), so `real == root` is never
   reachable there, but `--read-root` may name a regular file.
   Missing case `probe-root-is-a-file`: `read_roots: ["roots/x.ini"]`, `include=@ROOT@/roots/x.ini` →
   candidate `width=321`, `refusals none` (ok); mutant `FAIL unexpected-refusal`.
4. **RM6C2 lexical cycle detection survives.** k23 (self-loop) cannot distinguish: `os.path.realpath`
   of a self-symlink returns the same lexical path (verified in scratch: `realpath self-loop:
   …/loop.ini`), and no frozen case re-enters a file already in the stack through a second lexical
   path (k06/k07 chain into a *new* file, refused by containment first).
   Missing case `probe-cycle-via-second-lexical-path`: config `include=~/a.ini`; `a.ini` sets
   `width=2` and `include=~/link.ini`; `link.ini` is a symlink to `a.ini` → candidate refuses with
   `cycle` (`width=2`, `refusals present`, ok); mutant `FAIL exit=1` (RecursionError).
5. **RM2C2 opens the unresolved target — survives, and is *unobservable by construction*.** Every
   frozen case's positive include resolves to the same bytes through either name; the difference would
   only be visible if the link changed between the containment check and the open. That is the
   declaration's own named limit (C2 stance: "TOCTOU between the check and the open"), so this
   survivor is a named limit confirmed, **not** a routed defect.

## 5. Dead steps (with error text)

1. First C2 attempt contained a mutant that rewrote `if not self.within_roots(real):`
   ("containment tested on the lexical target"). It could not be scored: the C2 counter derives its
   `refuse-all-includes` forgery from that exact anchor, so `evaluate` exited with
   `c1_r87_mako_criteria.SetupError: forgery anchor 'if not self.within_roots(real):' occurs 0 times`
   (driver rc=1, evidence `c2-score-unscorable-RM2C2.err`). **Structural finding:** any C2 defect that
   consumes the containment call site is unscoreable by this counter (unlike C1, whose forgery anchors
   are distinct from the mutant anchors) — a mutant that removes the containment check is only
   expressible as K1's `if False:`, which preserves the anchor. Replaced with RM2C2
   (opens unresolved target), which keeps the anchor.
2. First C1 run's RM7C1 probe used `include=~/core.ini` while the fixture placed `core.ini` at
   `.config/mako/core.ini`, so candidate and mutant both refused a missing target and the probe
   reported `distinguishes: false` (evidence `c1-score-attempt1.log`). Fixed to
   `include=~/.config/mako/core.ini`; re-run rc=0, probe distinguishes.

No other failures: no mutant crashed on any frozen case (`crashed_on: []` for all 15 rows).

## 6. Restoration evidence

The measured tools were never edited: mutations were produced in memory and written only into the
counter's own `mkdtemp` generation directory, which `evaluate` removes in its `finally` block.

| artifact | sha256 before | sha256 after |
|---|---|---|
| `$S/c1-tool.py` (bytes of `650e18b:tools/mado-mako.py`) | `07930521f8e4cfb825014f1d4fbdc7e4fb0abe975f4b9783154b019fbb5e89c3` | `07930521…e89c3` (driver field `tool_sha256_before == tool_sha256_after: True`) |
| `$S/c2-tool.py` (bytes of `7d30748:tools/mado-mako.py`) | `c374d71514f1559a12593b1097cd5e6ccc8ba2c225f2fa2b2d7764ef29192237` | `c374d715…92237` (same check: True) |
| scratch generation dir `$S/drv` | — | empty (`ls -A` → 0 entries) |
| lane working tree | peers' files only: `M quality/tool-ledger.md`, `?? .ufo/waves/round-88/r1*`, `?? receipts/harm-final-r88.txt`, `?? w1.ready.dispatched` | unchanged by this seat; no lane path written except this report |

`$S` = `/fast/scratch/hyaku/mado-r88/R88MResidMut` (deleted on exit).

## 7. Commands and exit codes

| # | command (lane root unless noted) | rc |
|---|---|---|
| 1 | `git show 9e36e3a:.ufo/waves/round-88/claims-declaration-r88.md` | 0 |
| 2 | `git show <rev>:<path> > $S/…` for both tools, both case files, both counters, r87 counter | 0 |
| 3 | `sha256sum $S/*.py $S/*.json` (all seven digests equal the freeze / receipt values) | 0 |
| 4 | `python3 -I driver.py --kind c1 …` (first run, probe defect) | 0 |
| 5 | `python3 -I driver.py --kind c2 …` (first run, unscoreable mutant) | 1 — `SetupError: forgery anchor … occurs 0 times` |
| 6 | `python3 -I driver.py --kind c1 …` (corrected probe) | 0 — 4 killed / 4 survived, candidate 62/62 |
| 7 | `python3 -I driver.py --kind c2 …` (replacement mutant) | 0 — 2 killed / 5 survived, candidate 26/26 |
| 8 | `git -C mado-shokunin status --porcelain` (read-only) | 0 |

## 8. Verdict and routing (round 89, not a predicate change)

Frozen predicates stand: the measured tools score N and K against their own declared mutants, and
these residual probes do not alter that. What this seat found is **case-set coverage**, to be routed:

* **C1 (4 survivors):** the "exact string equality / strcmp" claim is pinned for `summary` only
  (c33); `app-name` (and by symmetry the other four string fields) admit a casefolded comparison
  unchallenged. Bare `!` on a string field, `mode` casefold, and `include=` inside a criteria section
  are likewise unrepresented.
* **C2 (4 routed survivors + 1 named-limit confirmation):** the trailing-`/` refusal and the `~//`
  join rule — both added by w1 review as stance sentences — have **no frozen case at all** (selftest
  only); the `real == root` branch is untested though live for a file `--read-root`; cycle detection
  through a second lexical path is untested (k23's self-loop cannot distinguish it). RM2C2
  (`self.load(real)` → `self.load(target)`) is the declared TOCTOU/stance limit made executable and is
  not a defect to route.
* **Counter structural note (C2):** the `refuse-all-includes` forgery is derived from the same anchor
  the containment check lives on, so a defect that removes that call site cannot be scored (setup
  error, exit 2); a round-89 counter that moves the mutant anchors off the forgery anchor would close
  that blind spot.

Installs/updates: none (no package manager, no `uv`/`cargo`/`npm` command was run).
