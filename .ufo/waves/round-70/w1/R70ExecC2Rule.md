# R70ExecC2Rule — C2 counting command and classifier stress

seat: R70ExecC2Rule (leaf executor, C2 operability)
claim: C2 — four carrier shapes (`.ufo/waves/round-70/claims-declaration-r70.md`, frozen at `bc18399b`)
scored rev: `5144a6b5f43225d8021a469f4d24c19558026b9e` (instrument blob sha256 `87ca466432302feaabf2c504dc131184178afe199d8b84fa492ad3b5211af9f7`)
base rev: `b37a5aec4ea03f2223d8e09dd5d386d055c24179`
lane tip observed during the run: `5adba5a9` (observability-only edit, §7)
interpreter: Python 3.14.8, all runs `python3 -I`
cwd for every command: `/home/vgpnk/Projects/shokunin/mado-shokunin`

No production file was written. Only this report and `w1/R70ExecC2Rule/probe-harness.py`
(measurement harness, sha256 in §9). No tool was installed; no pacman transaction was run.

## 1. Instrument selftest

```
$ S=/fast/scratch/hyaku/mado-r70/R70ExecC2Rule
$ git -C . show 5144a6b5f43225d8021a469f4d24c19558026b9e:quality/counters/c2-r70-carriers.py > "$S/c2-r70-at-5144.py"
$ sha256sum "$S/c2-r70-at-5144.py"
87ca466432302feaabf2c504dc131184178afe199d8b84fa492ad3b5211af9f7
$ python3 -I "$S/c2-r70-at-5144.py" --selftest \
    --controls .ufo/waves/round-70/controls/c2-controls-r70.json --scratch-root "$S/pin"
MADO_R70_GUARD_CARRIERS_SELFTEST: 49/49 assertions passed
rc=0
```

The same selftest run on the current worktree instrument (HEAD `5adba5a9`) also prints
`49/49 assertions passed`, rc=0.

## 2. Frozen counting command

Pinned blob (authoritative receipt; the worktree instrument moved after `5144a6b5`, §7):

```
$ S=/fast/scratch/hyaku/mado-r70/R70ExecC2Rule
$ mkdir -p "$S/pinm"
$ python3 -I "$S/c2-r70-at-5144.py" --repo . \
    --rev 5144a6b5f43225d8021a469f4d24c19558026b9e \
    --base-rev b37a5aec4ea03f2223d8e09dd5d386d055c24179 \
    --controls .ufo/waves/round-70/controls/c2-controls-r70.json \
    --scratch-root "$S/pinm"
rc=0   (59 lines)
```

```
MADO_R70_CONTROLS path=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-70/controls/c2-controls-r70.json cases=17 sha256=29947b4ce5890f5c977f3ec74bafd14ba12b0d581dcb03ef1e3b637017a778ff
MADO_R70_HELD_CONTROLS path=.ufo/waves/round-69/controls/c2-controls-r69.json cases=11 sha256=975ca3ba37341b5a058dec4fa76278d548996738e8b517616181824a841f90b9 carried=yes
MADO_R70_READER file=quality/check-anchor-cover.py reader=yes guard=yes
MADO_R70_READER file=quality/check-axis-scores.py reader=yes guard=yes
MADO_R70_READER file=quality/check-control-receipts.py reader=yes guard=yes
MADO_R70_READER file=quality/check-counter-discrimination.py reader=no guard=no
MADO_R70_READER file=quality/check-deliverables.py reader=yes guard=yes
MADO_R70_READER file=quality/check-evidence-pointers.py reader=yes guard=yes
MADO_R70_READER file=quality/check-freeze-order.py reader=yes guard=yes
MADO_R70_READER file=quality/check-index-rows.py reader=yes guard=yes
MADO_R70_READER file=quality/check-index.py reader=yes guard=yes
MADO_R70_READER file=quality/check-landed-contract.py reader=yes guard=yes
MADO_R70_READER file=quality/check-locators.py reader=no guard=no
MADO_R70_READER file=quality/check-population.py reader=no guard=no
MADO_R70_READER file=quality/check-r38-discrimination.py reader=no guard=no
MADO_R70_READER file=quality/check-r55-controls.py reader=no guard=no
MADO_R70_READER file=quality/check-r56-controls.py reader=no guard=no
MADO_R70_READER file=quality/check-round-outcome-first.py reader=yes guard=yes
MADO_R70_READER file=quality/check-session-material.py reader=yes guard=yes
MADO_R70_READER file=quality/check-state-cite.py reader=no guard=no
MADO_R70_READER file=quality/check-tool-ledger.py reader=yes guard=yes
MADO_R70_READER file=quality/check-wave-done.py reader=yes guard=yes
MADO_R70_CONTROL name=guarded-inline reader=yes guard=yes expect_reader=yes expect_guard=yes correct=yes
MADO_R70_CONTROL name=value-position-only reader=yes guard=no expect_reader=yes expect_guard=no correct=yes
MADO_R70_CONTROL name=dead-branch-only reader=yes guard=no expect_reader=yes expect_guard=no correct=yes
MADO_R70_CONTROL name=uncalled-helper reader=yes guard=no expect_reader=yes expect_guard=no correct=yes
MADO_R70_CONTROL name=overwritten-env reader=yes guard=no expect_reader=yes expect_guard=no correct=yes
MADO_R70_CONTROL name=update-guard reader=yes guard=yes expect_reader=yes expect_guard=yes correct=yes
MADO_R70_CONTROL name=subscript-guard reader=yes guard=yes expect_reader=yes expect_guard=yes correct=yes
MADO_R70_CONTROL name=module-constant reader=yes guard=yes expect_reader=yes expect_guard=yes correct=yes
MADO_R70_CONTROL name=producer-helper reader=yes guard=yes expect_reader=yes expect_guard=yes correct=yes
MADO_R70_CONTROL name=argv-name-flow reader=yes guard=yes expect_reader=yes expect_guard=yes correct=yes
MADO_R70_CONTROL name=mention-only reader=yes guard=no expect_reader=yes expect_guard=no correct=yes
MADO_R70_CONTROL name=alias-carried reader=yes guard=yes expect_reader=yes expect_guard=yes correct=yes
MADO_R70_CONTROL name=attribute-carried reader=yes guard=yes expect_reader=yes expect_guard=yes correct=yes
MADO_R70_CONTROL name=splat-carried reader=yes guard=yes expect_reader=yes expect_guard=yes correct=yes
MADO_R70_CONTROL name=constant-key reader=yes guard=yes expect_reader=yes expect_guard=yes correct=yes
MADO_R70_CONTROL name=guarded-env-for-a-non-git-call reader=yes guard=no expect_reader=yes expect_guard=no correct=yes
MADO_R70_CONTROL name=git-called-without-env reader=yes guard=no expect_reader=yes expect_guard=no correct=yes
MADO_R70_BASE_COUNTER path=quality/counters/c2-r69-guard-dominance.py present=yes sha256=53f256f4693526f2c37cced5203c2e1d6007b721c4b6c0d7fa522e165597e929
MADO_R70_CONTROL name=guarded-inline reader=yes guard=yes expect_reader=yes expect_guard=yes correct=yes
MADO_R70_CONTROL name=value-position-only reader=yes guard=no expect_reader=yes expect_guard=no correct=yes
MADO_R70_CONTROL name=dead-branch-only reader=yes guard=no expect_reader=yes expect_guard=no correct=yes
MADO_R70_CONTROL name=uncalled-helper reader=yes guard=no expect_reader=yes expect_guard=no correct=yes
MADO_R70_CONTROL name=overwritten-env reader=yes guard=no expect_reader=yes expect_guard=no correct=yes
MADO_R70_CONTROL name=update-guard reader=yes guard=yes expect_reader=yes expect_guard=yes correct=yes
MADO_R70_CONTROL name=subscript-guard reader=yes guard=yes expect_reader=yes expect_guard=yes correct=yes
MADO_R70_CONTROL name=module-constant reader=yes guard=yes expect_reader=yes expect_guard=yes correct=yes
MADO_R70_CONTROL name=producer-helper reader=yes guard=yes expect_reader=yes expect_guard=yes correct=yes
MADO_R70_CONTROL name=argv-name-flow reader=yes guard=yes expect_reader=yes expect_guard=yes correct=yes
MADO_R70_CONTROL name=mention-only reader=yes guard=no expect_reader=yes expect_guard=no correct=yes
MADO_R70_CONTROL name=alias-carried reader=yes guard=no expect_reader=yes expect_guard=yes correct=no
MADO_R70_CONTROL name=attribute-carried reader=yes guard=no expect_reader=yes expect_guard=yes correct=no
MADO_R70_CONTROL name=splat-carried reader=yes guard=no expect_reader=yes expect_guard=yes correct=no
MADO_R70_CONTROL name=constant-key reader=yes guard=no expect_reader=yes expect_guard=yes correct=no
MADO_R70_CONTROL name=guarded-env-for-a-non-git-call reader=yes guard=no expect_reader=yes expect_guard=no correct=yes
MADO_R70_CONTROL name=git-called-without-env reader=yes guard=no expect_reader=yes expect_guard=no correct=yes
MADO_R70_BASE controls=13/17 (the round-68 rule must miss the target)
MADO_R70_GUARD_CARRIERS: population=20 readers=13 guarded=13 unguarded=0 controls=17/17 base_controls=13/17 verdict=TARGET_MET rev=5144a6b5f43225d8021a469f4d24c19558026b9e
```

The nominal worktree command (`python3 -I quality/counters/c2-r70-carriers.py ...`, same flags) prints
the same contract line, rc=0, with `leg=candidate`/`leg=base` prefixes added by `5adba5a9`.

## 3. Base rev — honest before state

```
$ git cat-file -e b37a5aec4ea03f2223d8e09dd5d386d055c24179:quality/counters/c2-r70-carriers.py
fatal: path 'quality/counters/c2-r70-carriers.py' exists on disk, but not in 'b37a5aec…'
rc=128
$ git ls-tree -r --name-only b37a5aec… -- quality/counters | grep c2-r
quality/counters/c2-r69-guard-dominance.py
$ git ls-tree -r --name-only 5144a6b5… -- quality/counters | grep c2-r
quality/counters/c2-r69-guard-dominance.py
quality/counters/c2-r70-carriers.py
```

The round-70 command cannot be launched *at* the base rev: its scored file is absent from that
tree. The before state is therefore `counter=absent`; the held round-69 instrument's score on
the frozen 17 cases is measured in §4.

## 4. Base leg re-derived by hand

The `classify` of `quality/counters/c2-r69-guard-dominance.py` extracted at the base rev
(sha256 `53f256f4693526f2c37cced5203c2e1d6007b721c4b6c0d7fa522e165597e929`, 38161 bytes) was
run over all 17 frozen cases (`29947b4c…`), per case:

| case | reader | expect_reader | guard | expect_guard | correct |
|---|---|---|---|---|---|
| guarded-inline | yes | yes | yes | yes | yes |
| value-position-only | yes | yes | no | no | yes |
| dead-branch-only | yes | yes | no | no | yes |
| uncalled-helper | yes | yes | no | no | yes |
| overwritten-env | yes | yes | no | no | yes |
| update-guard | yes | yes | yes | yes | yes |
| subscript-guard | yes | yes | yes | yes | yes |
| module-constant | yes | yes | yes | yes | yes |
| producer-helper | yes | yes | yes | yes | yes |
| argv-name-flow | yes | yes | yes | yes | yes |
| mention-only | yes | yes | no | no | yes |
| alias-carried | yes | yes | **no** | yes | **NO** |
| attribute-carried | yes | yes | **no** | yes | **NO** |
| splat-carried | yes | yes | **no** | yes | **NO** |
| constant-key | yes | yes | **no** | yes | **NO** |
| guarded-env-for-a-non-git-call | yes | yes | no | no | yes |
| git-called-without-env | yes | yes | no | no | yes |

`score=13/17` — exactly the four new carrier cases missed, every held case still correct. This
matches the frozen receipt § C2 (13/17).

## 5. Population and held-set verification

```
$ git ls-tree … b37a5aec… -- quality | grep -E '^quality/check-[^/]+\.py$' | sort > pop-base.txt   # 20
$ git ls-tree … 5144a6b5… -- quality | grep -E '^quality/check-[^/]+\.py$' | sort > pop-rev.txt    # 20
$ diff pop-base.txt pop-rev.txt; rc=0
```

Independent recount with the pinned instrument's `classify` over the 20 files at `5144a6b5`:
`population=20 readers=13 guarded=13 unguarded=0` (identical to the counter's census, §2),
held 11 cases byte-identical to the round-70 file (`11/11`, sha256 `975ca3ba…`), both frozen
digests asserted by the counter (`MADO_R70_CONTROLS`, `MADO_R70_HELD_CONTROLS` above).

## 6. Seven probe sources beyond the frozen 17

Runtime truth below is measured by executing each final-env construction (stub-free, no child
spawned): `key_in_env=<bool>`. "Expected under rule" is the declaration's rule text
(`claims-declaration-r70.md`, C2 rule (a)–(d)) plus the counter docstring's declared limits
("one module, one hop, no container flow beyond a one-level `**` of a module-level literal
mapping").

| id | shape | expected under rule | observed (reader, guard) | runtime key_in_env | classification |
|---|---|---|---|---|---|
| a | two-hop alias `a = env; b = a; b[KEY]="1"` | not promised (one-hop limit) | (yes, no) | **True** | inside declared limits — runtime FN not claimed |
| b | alias guarded, env-named name rebound after the guard | no | (yes, no) | False | match |
| c | `self.env` guarded, `env=self.other` passed | no | (yes, no) | False | match |
| d | `**EXTRA` where EXTRA carries no key | no | (yes, no) | False | match |
| e | `KEY` rebound to `"OTHER"` before use | no | (yes, no) | False | match |
| f | `env = dict(**GUARD)` | **yes** — one-level `**` of a module-level literal mapping | (yes, **no**) | **True** | **false negative, within the rule's letter** |
| g | `env = dict(base, **GUARD)` | **yes** — same | (yes, **no**) | **True** | **false negative, within the rule's letter** |

No false positive was found in the seven probes. Probes (a)–(g) all classify `(yes, no)` under
the round-69 base classifier as well, so (f)/(g) are round-70 residuals, not held-rule misses.

Contrast measured on the same instrument (sanity, not part of the probe count):

```
{**GUARD}                        -> (True, True)
dict(**GUARD)                    -> (True, False)
dict(GIT_NO_REPLACE_OBJECTS="1") -> (True, True)
{**os.environ, **GUARD}          -> (True, True)
```

Finding: `splat_guard_lines` accepts only `ast.Dict` displays, and `mapping_has_key` for a
`dict(...)` call inspects only literal keyword names, so a one-level `**` into a `dict()` call
is invisible. The declaration's rule sentence ("expanded with `**` into the env mapping") and
the counter's own limit line ("no container flow beyond a one-level `**` of a module-level
literal mapping") both read as claiming this form; the sourced ground cites the *dictionary
display* grammar, so a strict grammar reading places (f)/(g) at the limit's edge. Either way it
does not move the scored target: `controls=17/17`, `base_controls=13/17`, population unchanged.
Recorded as a residual for the claim's "Not claimed" row, not as a target miss.

### Probe sources

```python
# a-two-hop-alias
def run(repo):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    a = env
    b = a
    b["GIT_NO_REPLACE_OBJECTS"] = "1"
    return subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)

# b-alias-then-env-rebound
def run(repo):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    alias = env
    alias["GIT_NO_REPLACE_OBJECTS"] = "1"
    env = {"PATH": "/usr/bin"}
    return subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)

# c-other-attribute-passed
class Runner:
    def __init__(self):
        self.env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
        self.other = {"PATH": "/usr/bin"}
        self.env["GIT_NO_REPLACE_OBJECTS"] = "1"

    def head(self, repo):
        return subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=self.other)

# d-splat-without-key
EXTRA = {"PATH": "/usr/bin"}


def run(repo):
    env = {**os.environ, **EXTRA}
    return subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)

# e-constant-rebound
KEY = "GIT_NO_REPLACE_OBJECTS"
KEY = "OTHER"


def run(repo):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env[KEY] = "1"
    return subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)

# f-dict-kwargs-only
GUARD = {"GIT_NO_REPLACE_OBJECTS": "1"}


def run(repo):
    env = dict(**GUARD)
    return subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)

# g-dict-with-kwargs
GUARD = {"PATH": "/usr/bin", "GIT_NO_REPLACE_OBJECTS": "1"}


def run(repo):
    env = dict(os.environ, **GUARD)
    return subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)
```

## 7. Lane-tip drift observed during the run

`git log --oneline` moved from `5144a6b5` to `5adba5a9` via `9508e878` while this seat ran.
`git diff 5144a6b5..HEAD -- quality/counters/c2-r70-carriers.py` is 4 insertions / 4 deletions:
`score_cases(..., leg="candidate"|"base")` and a `leg=%s` label in the `MADO_R70_CONTROL`
line. No classifier, predicate, digest, population or contract function changed. Re-ran the
frozen command with the pinned blob (sha256 `87ca4664…`, §2) and with the worktree instrument
(sha256 `d868ae33…`): both `rc=0` and the identical final line.

## 8. Scratch and tooling

- Scratch root: `/fast/scratch/hyaku/mado-r70/R70ExecC2Rule/` — removed at the end of the run
  (`rm -rf`, verified absent in §9).
- No tool installed or upgraded; no pacman transaction attempted (host pause respected).
- No compositor/service/socket/session/package-manager probe; no credential material read.

## 9. Artifacts and final line

```
probe-harness.py (seat copy): .ufo/waves/round-70/w1/R70ExecC2Rule/probe-harness.py
  sha256 50a285cfa74ec5752e6b34b737296b38613ae494ed5085a87f118179ed2afb8a
this report: .ufo/waves/round-70/w1/R70ExecC2Rule.md
  sha256 recorded in the seat yield (a file cannot carry its own final digest)
```

Final contract line (pinned instrument `5144a6b5`, rc=0):

```
MADO_R70_GUARD_CARRIERS: population=20 readers=13 guarded=13 unguarded=0 controls=17/17 base_controls=13/17 verdict=TARGET_MET rev=5144a6b5f43225d8021a469f4d24c19558026b9e
```
