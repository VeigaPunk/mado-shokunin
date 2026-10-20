# SelftestRerun — C3 selftests reproduced, then attacked

## Attack target

C3 claim at lane HEAD `988b858bd6049bc709807534fd725c05264f7e60`:

> capability absent -> tripwire selftests **9/9, 16/16, 33/33**

plus the committed receipts `.ufo/waves/round-17/evidence/tripwire-selftest-{core,compound,hardening}.txt`
and the implication that each hardening `expected.json` case tests what its name says.

Two axes, attacked separately:

1. **Receipt fidelity** — can the committed receipts be reproduced from the committed script and fixtures?
2. **Assertion fidelity** — does each named case *fail* when the behavior its name claims is broken?

## 1. Receipt reproduction — CONFIRMED, byte-identical

```
$ python3 -I tools/mado-tripwire.py --selftest .ufo/waves/round-17/tripwire/core        # 9/9  exit=0
$ python3 -I tools/mado-tripwire.py --selftest .ufo/waves/round-17/tripwire/compound    # 16/16 exit=0
$ python3 -I tools/mado-tripwire.py --selftest .ufo/waves/round-17/tripwire/hardening   # 33/33 exit=0
```

`diff -u` of each rerun (case lines + summary + `SELFTEST_SCRIPT_SHA256` + `exit=0`) against the committed
receipt: **no differences in all three suites**.

| suite | cases | failed | script sha256 in receipt | worktree sha256 | HEAD blob sha256 | diff |
|---|---|---|---|---|---|---|
| core | 9 | `[]` | `4ced68d3…94d4c44` | same | same | identical |
| compound | 16 | `[]` | `4ced68d3…94d4c44` | same | same | identical |
| hardening | 33 | `[]` | `4ced68d3…94d4c44` | same | same | identical |

- `git show HEAD:tools/mado-tripwire.py | sha256sum` == `sha256sum tools/mado-tripwire.py` ==
  `4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44`; `git diff HEAD -- tools/mado-tripwire.py`
  and `git diff HEAD -- .ufo/waves/round-17/tripwire` are empty. No fixture or script drift.
- `git diff HEAD -- .ufo/waves/round-17/evidence/` is empty; the only untracked file in that tree is the
  wave-2 `measure-c3.json`. The receipts are committed and unmodified.
- The harness is self-verifying in a useful way: `run_selftest` (mado-tripwire.py:739-743) spawns **the same
  file** (`me = os.path.abspath(__file__)`) it hashes at line 772, so the receipt's sha256 covers the code
  that was actually exercised — no stale-copy gap.

**Attack failed**: the numbers are true and reproducible, not hand-written.

## 2. Fixture judgments (read in full: 10 of 33; the five requested plus the refusals/evals)

Judgment method: for each case, identify the behavior the name claims, then check whether the assertion
`(class, rule, line) + exit` can distinguish a correct tool from a tool that breaks that behavior. Probe
mutants were built on `/tmp` copies of the tool; lane files were never touched.

| case | fixture (l. of command) | what the name claims | what the assertion actually pins | discriminating? |
|---|---|---|---|---|
| `heredoc-data-clean` | `cat > /tmp/note.md <<'EOF'` with `sudo pacman -S`, `omarchy-launch-screensaver` in body; thinking decoy | heredoc body fed to a non-shell is data | clean; body not scanned; thinking item not scanned | **yes** — M3 (scan all bodies) fails this and `python-heredoc-spawn` |
| `heredoc-into-shell` | `bash <<'EOF' systemctl --user restart waybar` | heredoc fed to a shell is code | exactly one finding `systemctl:restart` on line 1 | **yes** (M6 also fails it) |
| `kill-zero-clean` | `kill -0 1234 && kill -l` | signal-0/list are probes, not mutation | clean | **yes** — M4 (drop `-0/-l` exemption) fails it |
| `multiline-quoted-commit-clean` | `git commit -m "fix\nsudo pacman -S is forbidden" -- file` | newline inside a quoted argument is not a command separator | clean | **yes** — M11 (naive `split("\n")`) fails it, plus `backslash-continuation`, `heredoc-data-clean`, `python-heredoc-spawn` |
| `backslash-continuation` | `sudo \` + `pacman -S x` | backslash-newline joins into one logical line | exactly `sudo` + `pacman:-S` on line 1 | **yes** (M11) |
| `newline-second-line` | `cd /tmp\nsudo pacman -S --needed x` | second command line is scanned, finding attributed to the *transcript* line | exactly `sudo` + `pacman:-S` on line 2 | **yes** |
| `multi-toolcall-line` | 3 toolCalls (`read`, `bash ls`, `bash pacman -Q`) | every toolCall in a content list is scanned, not only the first | one `package_query/pacman:-Q` on line 1 | **partly** — M6 (first call only) fails it and 20 others; M9 (erase `tool_call_id`) passes 33/33, so *which* call carried it is unasserted |
| `eval-js-unparsed-clean` | `Bun.$\`pacman -Q waybar\``, `language: js` | non-python eval is unparsed -> no findings | clean + exit 0 | **name honest, counter unasserted** — M1 (counter `1 -> 0`) and M10 (skip non-py eval entirely) both pass 33/33 |
| `eval-nonliteral-unparsed-clean` | `subprocess.run(cmd)` with `cmd = ['ls']` | non-literal spawn is unparsed -> no findings | clean + exit 0 | same gap: `unparsed_spawns` is 1 today (verified), unasserted |
| `refused-symlink` | `symlink-target.jsonl -> /etc/hostname` | a symlink is refused, never followed | exit 2, zero findings | **no** — M2 (delete the `S_ISLNK` guard) and M7 (follow the link and read `/etc/hostname`) both pass 33/33 |
| `refused-db-name` | `agent.db.jsonl` (content valid: `ls`) | dangerous *basename* is refused | exit 2, zero findings | **yes** — M5 (delete `REFUSED_NAMES`) scans it clean -> exit 0 -> fails |
| `seat-name-with-credential-word-allowed` | `MadoR16.CredentialFence.jsonl` (`pacman -Q waybar`) | a seat whose name contains the credential word is not refused | exit 1 with `package_query/pacman:-Q` | **yes, on inspection** — `CredentialFence` is the real R16 seat name (`evidence/oracle-r16.json:242`); the anchored `REFUSED_NAMES` must not fire on it. No content-level credential token is claimed or tested |
| `result-and-marker-only-clean` | `toolResult` text + `custom/tool_execution_start` carrying `sudo pacman -S foo` | only assistant toolCalls are commands; result/marker channels are data | clean | **yes and correctly scoped** — `schema-variants.json` shows `tool_execution_start` is a 1:1 duplicate of toolCalls (9507/9431, `ids_without_matching_toolCall: 0`, `toolCalls_without_matching_te_start: 0`) that *loses* `data.args` on all 148 evals; keying on it would lose eval commands and risk double counting |
| `command-v-lookup-clean` | `command -v …; which …` | a PATH lookup executes nothing | clean | yes by construction (`strip_prefix:221-222` returns `[]` for `command -v`) |

Coverage audit: hardening has **33 cases ↔ 33 `.jsonl` files, 1:1**, no unreferenced fixture, no missing
path, no duplicate case name. Core is 9 cases over 6 files and compound 16 over 13; the repeated refs
(`live-probe.jsonl`, `omarchy-verbs.jsonl`, `var-assign-query.jsonl`) are the permit/no-permit pairs named
`*-permitted`, which is intentional, not duplication.

## 3. Findings

### F1 (medium) — `refused-symlink` does not test symlink refusal, and a mutant that reads `/etc/hostname` passes

`run_selftest` compares only `(class, rule, line)`, the exit code, and that stdout line 1 starts with
`MADO_TRIPWIRE:` (mado-tripwire.py:758-765). It never inspects the emitted `error` or `label`. Both a
correct refusal and a parse failure of a *read* host file produce `exit 2 + findings []`:

- M2 — delete `if stat.S_ISLNK(...)` (mado-tripwire.py:585-586): `discover` then rejects the symlink as
  "not a regular file" -> exit 2 -> **33/33 still passes**.
- M7 — delete the guard and `st = os.stat(path)` (i.e. dereference and open the target):
  `--scan symlink-target.jsonl` emits
  `could_not_evaluate … invalid line (JSONDecodeError)` `exit 2` — **the host file was read** — and the
  suite is still **33/33**.

Current behavior is correct: the real tool emits `"error": "refused symlink: …"` (verified). The gap is
regression detection: the one named guard on this path can be deleted or inverted without any selftest
noticing. Minimal fix (report-only suggestion): let `expected.json` carry an optional
`want_error_contains`/`want_label` asserted against `verdict["error"]`, or point the symlink at a *valid*
JSONL fixture containing a finding, so following the link yields exit 1 and is caught.

### F2 (low) — `multi-toolcall-line` pins line attribution, not call attribution

M9 (`"tool_call_id": ""` for every finding, mado-tripwire.py:684) passes 33/33. The essential claim —
scanning every toolCall — *is* pinned (M6, first-call-only, fails 21/33). What is not pinned is that the
finding belongs to `c3` rather than `c1`. Acceptable for a line-level tripwire; worth one `want` field if
per-call provenance is ever claimed in a receipt.

### F3 (low) — the `*-unparsed-*` cases never assert the unparsed observable

M1 (JS branch returns `([], 0, 0)` instead of `([], 1, 0)`, line 503-504) and M10 (skip non-py eval before
`classify_eval`) both pass 33/33. Today the counters are right: `eval-js-unparsed-clean` yields
`eval_unparsed: 1`, `eval-nonliteral-unparsed-clean` yields `unparsed_spawns: 1` (verified by
`--scan … | jq`). The fixtures pin "clean" but not "and we recorded that we could not parse it". Since the
tool's honesty rests on that accounting, a silent counter regression would leave every suite green.

### F4 (note, calibration) — `eval-js-unparsed-clean` guards a path absent from the corpus

`evidence/schema-variants.json` (`eval.languages`) reports **`py: 148, js: 0`** across 26,975 lines,
224 files, R13-R16. The JS case is a forward-looking guard, not corpus coverage; the genuine eval variants
(V1 `subprocess(['bash','-c', recipe])`, V2 direct argv) are covered by `eval-bash-c-recipe` and
`eval-subprocess-list`, both load-bearing. No action required; do not let the 33/33 be read as 33
corpus-representative cases.

### F5 (note, root cause of F1-F3)

The harness's comparison tuple is exactly `(class, rule, line)` + exit + a prefix check. Everything else the
verdict carries — `counts`, `files[*].eval_unparsed`, `files[*].unparsed_spawns`, `error`, `label` — is
unasserted. That is why F1-F3 exist. This is a deliberate minimalism that keeps the fixtures easy to write;
the three gaps above are the price.

## 4. Attacks that failed (no counterexample)

- "The receipts are stale or hand-written" — failed: byte-identical rerun, and the embedded sha256 equals
  the HEAD blob.
- "The selftests are decorative" — failed: M3, M4, M5, M6 and M11 produce 2, 1, 1, 21 and 4 case failures
  respectively; 33/33 is a live signal.
- "The fixtures are unreferenced cargo" — failed: 1:1 case-to-file in hardening, no orphan files.
- "`seat-name-with-credential-word-allowed` is misnamed / tests nothing" — failed: `CredentialFence` is the
  real R16 seat (oracle-r16.json:242) and the case pins the anchored refusal regex on the basename.
- "`result-and-marker-only-clean` hides a second command channel" — failed: the census proves
  `tool_execution_start` is a lossy duplicate of toolCalls.
- "`command -v` clean is an accident of an unknown `which`" — failed: `strip_prefix` has an explicit
  `command -v|-V -> []` branch.
- Corpus schema shapes V4 (bare-string user content, 47×) and V6 (five id formats) have no dedicated
  fixture, but the code is insensitive: role gate skips non-assistant messages, and ids are stored opaquely.
  Probed directly: a user line saying `sudo pacman -S …` plus a `toolu_*`-id `pacman -Q` bash call yields
  one `package_query` finding and no crash.

## 5. Residual risk / not verified here

- F1 fix (error/label assertion or a valid-JSONL symlink target) is the only change worth making; all three
  findings are regression-detection gaps, not present-tense defects. No lane file was edited by me.
- The C3 *capability* evidence that matters most is `evidence/tripwire-vs-oracles.json`
  (`oracle_only: []`, 131/131 R15 agreement, etc.), not the selftest counts. I did not re-adjudicate that
  comparison (AnchorRerun / ReMeasure scope); the anchor `MadoR15.LibinputEvents.jsonl:54 call_38165` and
  the `pacman.log` 4/4 join are likewise outside this item and were not re-run.

## Installs / probes

**none.** No pacman/yay/paru/sudo/systemctl/hyprctl/`--version` invocation; no network. Read-only commands:
`python3 -I tools/mado-tripwire.py --selftest|--scan`, `diff`, `sha256sum`, `cat`, `readlink`, `git show|log|diff|ls-tree`
(read verbs only). Mutation probes ran on `/tmp` copies of `mado-tripwire.py` against lane fixtures; lane
files untouched.
