# ScribeSkill — draft tripwire + isolation-harness SKILL text written; not applied, gated on C1 landing

Deliverable: `.ufo/waves/round-20/w1/drafts/ScribeSkill.md` (197 lines, sha256 `a2af8929…615ab`). Only that file was written, plus this report. No tracked lane file, no fleet file and no repo state changed.

## Behaviour

Four blocks, each with its line range:

- **A** replaces SKILL.md 525–540: the round-17 tripwire section, now with the round-20 target text for lead vs observed rows, the binding guard and its limits, the help/dry-run carve-outs and their write negatives, and written-script blindness.
- **B** appends after original 540: a short isolation-harness subsection. It fails closed, stubs only `/tmp` or a verified mount namespace, runs canary payloads only, and never runs the live gate or host binaries under the pause.
- **C** appends after original 600: a round-20 limit paragraph.
- **D** replaces one phrase in registry row 563 (the verdict-map class list).

The draft is explicitly gated. Evidence-marker, binding-guard and carve-out text describes the E1–E4 target. Tool `e629f73` (sha256 `367be947…`) does not implement it, so nothing in the draft is true of the current tool.

## Findings (evidence)

1. **Current SKILL.md text read.** Working tree `SKILL.md` equals `e629f73:SKILL.md` (sha256 `41287d7e…1b84`). The tripwire section is 525–540; the limit paragraph is 590–600; the registry row is 563. Source: `sed`/`grep` on the tree and `git show e629f73:SKILL.md`.

2. **Harm reproduced at the pre-registration tool.** A /tmp fixture with one py eval cell `BLOCK=frozenset(['pacman','-Q','hyprland'])` (round-19 envelope copied, cell replaced; fixture scanned, never executed), run with `python3 -I tool.py --scan`, where `tool.py` is `git show e629f73:tools/mado-tripwire.py` (sha256 `367be947…`):
   ```
   MADO_TRIPWIRE: findings
   {"counts": {...,"package_query": 1,...}, "exit": 1, ... "findings": [{"class": "package_query", "rule": "pacman:-Q", "command": "pacman -Q hyprland", "line": 1, ...}]}
   ```
   No `evidence` key. Consistent with the round-19 closure (`corpus/lessons/round-19-verifier-spotcheck.md` §C3). The draft cites this.

3. **Current carve-out status (target E4 not in force).** Same tool, fixtures in /tmp:
   - `git commit --dry-run -m x` → `vcs_write`, rule `git:commit`, exit 1
   - `jj git push --dry-run` → `vcs_write`, rule `jj:git`, exit 1
   - `git commit -h` → `vcs_write`, rule `git:commit`, exit 1
   - `git commit -n -m x` → `vcs_write` (correct: `-n` is `--no-verify`)

4. **Written-script blindness confirmed.** A bash call writing `/usr/bin/pacman -Q hyprland` into `x.sh`, then `bash /tmp/scribeskill/x.sh` in a later call → `MADO_TRIPWIRE: clean`, exit 0. The blindness is real at this revision and is kept explicit in Block A.

5. **Lead behaviour confirmed as current behaviour (no lead marker yet).** An undefined bare call `run_record('packages',['pacman','-Q','hyprland'],0)` → `package_query / pacman:-Q`, no evidence key. `bash -c 'pacman -Q hyprland'` → `package_query / pacman:-Q`, no evidence key. Both are the rule-B shape the target splits into `lead` and `observed`.

6. **Registry discrepancy (Block D).** Registry row 563 says exit 1 is for "unpermitted host_mutation/package_query/live_probe finding". `tool_install` (`uv tool install ruff`) and `vcs_write` (`git commit --dry-run`) each exit 1 with label `findings` at `367be947`. The phrase is incomplete; the draft corrects it. This is a documentation fact, not a change to the tool.

7. **Isolation-harness basis.** `corpus/lessons/round-19-verifier-spotcheck.md:124-126` and `.ufo/waves/round-19/w2/reports/SentinelGatePath.md:77-79` (read as bytes): the `[ -e ] && mount && echo` chain did not trip `set -e`, the mount failed, and the real `/usr/bin/hyprctl probe` ran (rc 0). The fix — `exit 99` / `98` unless every bind and `cmp` succeeds — is the shape Block B cites. Block B adds the canary-only and host-pause rules; it does not claim the fix was re-measured.

## Caveats

- [INFERENCE] The binding guard's "latest preceding binding" is textual order. Nested control flow and deferred function bodies are not verified against the target and are flagged in Block A.
- [UNK] No fixture verified the target E1–E4 behaviour: the tool has not landed. Every target claim in Block A stays unverified until `tw-precision.py` runs at the landed revision.
- [UNK] I did not check whether a registered `tw-precision` counter exists yet at `.ufo/waves/round-20/tw-precision.py`; the draft refers to it by name only as the gate, per the pre-registration.

## Limits

- Scope: SKILL.md tripwire text, one isolation subsection, one registry phrase, one limit paragraph. No other SKILL.md section, no `SCORECARD.md`, no `QUALITY`, no lesson was edited or checked for consistency beyond the cited lines.
- Did not run the tripwire suites, `tw-recall.py`, `tw-precision.py`, the gate, or any real harness. Only `--scan` on /tmp text fixtures at `367be947`, plus read-only `git show` / `sha256sum` / `grep` / `sed`.
- Did not verify the cited round-19 incident beyond reading its prose; no host state was inspected (pause holds).
- Fixtures were generated by copying the round-19 envelope and replacing the code text; they were never executed. The scanned fixtures live in `/tmp/scribeskill/` and are not part of the lane.
- Did not check the draft against `QUALITY.md` criterion text or the `corpus/SOURCES.md` rows; the draft introduces no new source ids.

## Installs

none. The tripwire scan used the system `python3` (`-I`); no package was installed or upgraded. Host pacman stayed paused, and nothing ran pacman, sudo, systemctl, hyprctl, omarchy or the live gate.
