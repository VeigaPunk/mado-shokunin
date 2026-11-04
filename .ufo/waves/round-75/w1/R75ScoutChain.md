# R75ScoutChain — what the round-75 instruments actually rest on

Scout seat, read-only. Cited line numbers are pinned to
`HEAD = 466e130775820e7ab67e06175d81dd47d1fb9b4c` (working tree clean for tracked files) and are
checkable with `git show 466e1307:<path>`. Instrument bytes there:
`c1-r75-landing-controls.py` `51652b43…`, `c1-r75-harness-witness.py` `6d878a0c…` (byte-identical
to the freeze copy), `c2-r75-shapes.py` `0544c0ef…`, `c2-r74-shapes.py` `eb43e2b6…` (base rev and
HEAD), `c1-r72-landing-controls.py` `b6108c86…` (= `R72_SHA256` and the bytes the counter extracts
at `--base-rev`). `claims-declaration-r75.md` and both control sets are byte-unchanged since the
freeze `def73656`.

## 1. C1 chain

- **Challenge drawn** — `c1-r75-landing-controls.py:243` `secrets.token_hex(8)` in `measure()`,
  after the frozen generation is loaded (`:163`) and sha-pinned (`:190`), before `install_rule`
  (`:199`); announced source-only at `:245`.
- **Reaches the child** — `install_rule` rebinds the frozen module **globals**
  (`:201`), then calls the frozen body unchanged (`:247`). `child_env` (`:209`, nonce at `:211`,
  installed `:233`) is resolved at call time by every spawn in `c1-r72-landing-controls.py`:
  `:464` (R-child), `:491` (selftest), `:514` (`bash -n`), `:520` (M-Z mutant), `:548`
  (child-env evidence). Lane side: `quality/landing-counters.sh:15-21`, called at `:226` (after
  the selftest summary) and `:290` (after the main contract line); silent unless 16 hex.
- **Echo parsed** — `last_witness` (`:108`) reverse-scans with `WITNESS_RE.fullmatch` (`:60`), so
  the last parsed line wins; byte-exact compare (`:117`). Gated at two places only:
  `credit_with_witness` (`:135`) → `g["credit"]` (`:235`) → frozen M-Z credit `c1-r72:525`;
  `green_with_witness` (`:131`) → `g["summary_green"]` (`:236`), which the frozen
  `contract_line` (`c1-r72:397`) and `outcome_exit` (`c1-r72:389-390`, rc at `c1-r72:595`) resolve
  from globals — so verdict **and** exit code are witness-gated without patching either function.
- **Unchanged frozen r72 surfaces** — the whole `measure()` body (`c1-r72:449-596`); four-file
  extraction (`c1-r72:84`, writer `:196`, evidence `:483-487`); instrument selftest and its
  arithmetic-only `green=` (`:490-494`); M-Z recipe (`:508-526`); M-R pair incl. `forged_credit`
  (`:540-591`, **not** witness-gated); `BASELINE="0/2"` (`:90`, re-hardcoded `c1-r75:217`); every
  evidence line's text, changed only by the `MADO_R72`→`MADO_R75` prefix move (`c1-r75:124,206`);
  fixture construction and git-env scrubbing (`c1-r75-harness-witness.py:220-245`).
- **Replaced** — `contract_line` (`c1-r75:214-220`, same fields + `witness=`) and `describe_env`
  (`c1-r75:224-230`, redacts the nonce; **added after the freeze**, see F3).

## 2. C2 delta sites (vs `c2-r74-shapes.py`)

Header-only deltas: `TOOL`, `BASE_COUNTER`, `BASE_COUNTER_SHA256` (`:55`, repair 3), 36/32 → 47/41,
held set round-74/36, prefixes, work dir, base pin.

- **Branch A (D1), name-neutral guard binding** — `c2-r75-shapes.py:349-364`, second loop of
  `guard_construction_lines` (`:322`). First loop (`:325-348`) still requires `env_named`. Any
  single-target `Assign`/`AnnAssign` to a plain `Name` whose value satisfies `mapping_has_key`
  (`:164-188`) binds a guard whatever the name; `dead_lines` honoured. `mapping_has_key` follows
  a dict literal's own key, one `**<mapping literal>` level (`:175-177`), a `dict(...)` keyword,
  and `**<name>` for module mappings (`:183-186`).
- **Branch B (D2), dominance widening + `del`** — `c2-r75-shapes.py:392-411`, second loop of
  `unguarded_rebindings` (`:380`): (i) any plain-name assignment without the key cancels
  (`:398-404`); (ii) `del <Name>[<Constant == KEY>]` cancels `<Name>` (`:405-411`), literal key
  and simple-name target only. `dead` honoured (`:396-397`, parameter added post-freeze; passed at
  `:454`, `:529`). Single arbiter: `has_guard` `:529-536`.
- **Post-freeze narrowing inside these functions**: `usage_lines` `:415-430` matches only
  `env=` now (positional arm removed at `e3e29bb4`); dead-branch statements no longer cancel
  (also `e3e29bb4`). `del alias[KEY]` (`:1232-1278`) and `del os.environ[KEY]` (`:1054-1088`)
  were already round-74/73 code.

## 3. Where declaration and code disagree

| # | claim | disagreement | anchor |
|---|---|---|---|
| **F1** | C1 | "an absent candidate harness prints `correct=absent`" is **unreachable**: `extract` raises at `:282`, so an absent candidate exits **2 with no contract line**; `absent` exists only in `CONTRACT_RE` `:74-76` and one selftest string `:354`. Survives every repair (counter byte-identical to freeze) | `c1-r75-harness-witness.py:205-209,282,316` |
| **F2** | C1 | **The counting command is not a deterministic predicate.** The `uppercase-echo` case uppercases the nonce with `tr 'a-f' 'A-F'` (`:95`); a letter-free nonce is unchanged by `tr`, so the echo matches and the case credits. `p = (5/8)^16 = 5.421e-4` (Monte Carlo 100/200 000) → ≈1 `TARGET_MISSED` per 1 845 runs, with no code defect. Also unrepaired | `c1-r75-harness-witness.py:95,59,108` |
| **F3** | C1 | At the freeze rev the live challenge was printed in clear in `MADO_R72_CHILD_ENV` (`c1-r72:548` + printer `:375-386`) — the docstring claimed it never leaves the contract line. Repaired at `b545bea9` (`:224-230`). Committed receipts stayed clean only because the counter discards child stdout | `c1-r75-landing-controls.py:224-230` |
| **F4** | C2 | Declaration says "handed as `env=`"; the freeze rev also accepted a positional `Name` to a git launch. Repaired at `e3e29bb4` (probe now `False`, was `True`) | `c2-r75-shapes.py:415-430` |
| **F5** | C2 | Declaration's `del` sentence was unqualified; the freeze rev let a `del env[KEY]` inside `if False:` cancel a live store. Repaired at `e3e29bb4` | `c2-r75-shapes.py:396-397,405-411` |
| **F6** | C2 | Residual, disclosed only by the "literal key" limit: `KEY = "GIT_NO_REPLACE_OBJECTS"; env[KEY]="1"; del env[KEY]` classifies **guarded** (probe), while the store side *does* accept module constants (`key_is_guard` `:635-640`). Not in the 47 cases | `c2-r75-shapes.py:405-411` vs `:635-640` |

Consequence for the round: **four repair commits changed the instruments while
`claims-declaration-r75.md` and the control sets stayed frozen** (`b545bea9`, `e3e29bb4`,
`f75afbf6`, `4527fcae`). The declaration's C2 "After" sentence still describes the pre-repair
predicate. Numbers are unaffected — 47/47 and 41/47 at `def73656`, `e3e29bb4` and `4527fcae`, and
the reader rows are identical in all three C2 receipts — but the claim now rests on receipts at
three different revs with no statement of which one it means, and its frozen sentence is no
longer the shipped code's sentence.

## 4. What is NOT modelled

1. The C1 counter scores **`mz` only**: `CAND_RE` (`harness-witness.py:67-70`) captures `mz`,
   `parse_decision` (`:212-217`) returns it; `witness=`, `killed=`, `mr=`, `verdict=` are
   shape-checked, never scored. No fixture lane proves a green *outcome* is denied without the
   echo — only the unit selftest (`c1-r75-landing-controls.py:290-292`).
2. `witness=` is computed from the **selftest** child (`:215`), the M-Z kill from the **mutant**
   child (`c1-r72:525`): two different runs, agreeing only because the lane body echoes in both.
3. `del` spellings outside the model, all probing **guarded**: `del r.env[KEY]` (attribute),
   `del env[CONST]` (F6), `child.pop(KEY)`, `del` inside a helper. A `del` under a *live* `if`
   cancels unconditionally (line order ≠ execution order).
4. No chains: `a = dict(env, KEY="1"); b = dict(a)` → unguarded. `mapping_has_key` is one `**`
   level and syntactic; values are never interpreted (`X="GIT_NO_REPLACE_OBJECTS"` is not a key,
   a guard valued `"0"` still guards).
5. `unguarded_rebindings` is called without `dead` at `:811` (`attribute_flow`) and `:936`
   (`carrier_guard`), so those carriers still count dead-branch statements as cancellations —
   harmless today because a cancellation set can only suppress credit and `:529` re-decides last.
6. A `subprocess.TimeoutExpired` from the frozen `run` (`c1-r72:172-174`) escapes the successor's
   `main` (`c1-r75:385-395`) as exit 1 with a traceback — the exit map reserves 1 for "measured
   and missed". Pre-existing in r72.
7. The eleven C1 lanes are test doubles whose echo is a pure function of `$MADO_LANDING_NONCE`
   and `MODE`. The real lane is exercised once, outside the scored set, in
   `.ufo/waves/round-75/receipts/harness-real-r75.txt` (`witness=ok mz=pass mr=pass killed=2/2
   verdict=TARGET_MET`, `quality/landing-counters.sh` sha `b0612f11…` — still current).

## Evidence and scope

Read-only throughout: no production instrument was executed by this seat, no file outside
`.ufo/waves/round-75/w1/R75ScoutChain/` (plus this report) was written, no git/jj mutation, no
pacman/uv/npx install. Probe evidence: the C2 classifier was imported from the pinned `466e1307`
blob in `/fast/scratch/hyaku/mado-r75/R75ScoutChain/rev/` and run over eight synthetic snippets
(attribute delete, const-key delete, dead-branch delete, live-branch delete, positional hand-off,
copy-then-source-delete, copy-of-copy, copy-then-`pop`); the nonce flake was measured by Monte
Carlo over 200 000 `secrets.token_hex(8)` draws (100 digit-only, predicted 108). Scratch removed.
