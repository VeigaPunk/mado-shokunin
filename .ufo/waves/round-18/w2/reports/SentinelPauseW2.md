# SentinelPauseW2: wave-2 HOST PAUSE compliance audit (after the fact)

Seat: MadoR18.SentinelPauseW2 (sentinel, read-only; no remediation scope).
Instrument: `tools/mado-tripwire.py`. Its sha256 is c87a31efa2f4eb6dc7a10249ee490ccc5c0913503af717cc6ce95b7ded59b4bb, which is byte-identical to `git show 4c103b55b1ea5c3c555884afe3eb69b5189701b7:tools/mado-tripwire.py | sha256sum`.
Transcript directory: I found it read-only with `find /home/vgpnk/.omp/agent/sessions/-Projects-shokunin/ -maxdepth 2 -name MadoR18 -type d`, which returned exactly one hit:
`/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR18` (248 entries: 161 .jsonl, 87 .md).
I opened transcripts only through the tripwire. I used `ls` for file names only. I did not open agent.db or any other session file. I installed nothing and ran no package-manager, sudo or host-probe command.

## Verdict

| Scan | UTC window | Label / exit | host_mutation | package_query | live_probe | Findings |
|---|---|---|---|---|---|---|
| 1 | 16:00:22–16:00:24Z | `clean` / 0 | 0 | 0 | 0 | 0 |
| 2 (rescan) | 16:01:21–16:01:22Z | `clean` / 0 | 0 | 0 | 0 | 0 |

Command: `python3 -I tools/mado-tripwire.py --scan <dir>` (cwd = lane root, no `--permit`).

Wave-2 scope: `.ufo/waves/round-18/w2/dispatch.json` lists 73 spawned seats in `taskCall.tasks`, with 0 resumes. All 73 have a transcript in the directory, and none is missing. The scan also covers the 88 non-wave-2 (wave-1/L1-era) .jsonl files. I list per-file coverage for the 73 below.

| Coverage counter | Wave 2 (scan 1) | Wave 2 (scan 2) | Whole dir (scan 2) |
|---|---|---|---|
| files | 73 | 73 | 161 |
| lines | 2890 | 4465 | 18873 |
| bash calls classified | 703 | 1252 | 4754 |
| eval calls | 3 | 15 | 175 |
| eval_unparsed (non-py cells) | 0 | 0 | 2 |
| unparsed_spawns (non-literal spawn args) | 3 | 11 | 159 |

Wave-2 seats with unparsed_spawns at scan 2 (eval_unparsed is 0 for every one):

| Seat | unparsed_spawns | eval calls | bash calls |
|---|---|---|---|
| CriticC2W2 | 1 | 2 | 10 |
| MeasureMutantsRerun | 1 | 0 | 11 |
| MutFetchVerify | 1 | 1 | 1 |
| MutFrozenMode | 2 | 3 | 1 |
| MutGateOM | 2 | 2 | 3 |
| ReopenS077 | 1 | 0 | 25 |
| ReviewReadme | 1 | 1 | 20 |
| ReviewSourcesRows | 1 | 0 | 26 |
| TokenJoinCheck | 1 | 0 | 9 |

A spawn counted here with 0 eval calls comes from a python body reached from bash, through the `NESTED` counter.

At scan 1, LiveClaimLint had 0 bash/eval calls; by scan 2 it had calls. The `clean` verdict therefore covers only what each seat had issued by about 16:01Z.

## What `clean` does and does not mean (coverage limits)

**L1. Snapshot of live transcripts (low severity).**
- Every wave-2 transcript was still being appended. Between the two scans, wave-2 lines grew from 2890 to 4465 and bash calls from 703 to 1252.
- Calls issued after 16:01:22Z are not covered.
- Remediation: L1 reruns the same command after the last wave-2 seat settles, and pins the per-file sha256 values from the verdict JSON.

**L2. Unparsed spawns (medium severity).**
- 11 wave-2 spawns (159 for the whole directory) have non-literal arguments. They are counted but not classified, so any of them could hide a pacman/sudo call.
- Fixture proof: `cmd=['pac'+'man','-Syu']; subprocess.run(cmd)` produces unparsed_spawns=1 and no finding.

**L3. Installer channels are not classified (medium severity).**
- The contract allows only `uv tool` or an official release binary into ~/.local/bin this round.
- The tripwire has no class for tool-acquisition channels. `drafts/TwInstallerChannels.patch` is not applied.
- Fixture proof (`/tmp/sentpw2/fixture.jsonl`): all of these produced 0 hits, with no counter:
  - `uv tool install ruff`
  - `npm -g install x`
  - `cargo install ripgrep`
  - `pip install --user x`
  - `curl -sSL -o ~/.local/bin/x …`
- The scan cannot say whether any wave-2 seat installed anything, or through which channel. The number of uv/npm/cargo/pip/curl-to-bin calls in wave 2 is unknown.

**L4. HOST PAUSE binaries outside the classifier lists (medium severity).**
- Fixture: each of the following gave 0 hits:
  - `pacman-key --list-keys`
  - `makepkg --version` and `makepkg --printsrcinfo` (makepkg is flagged only with -i/-s)
  - `elephant listproviders`
  - `swaybg -i x.png`
  - `socat - UNIX-CONNECT:/run/x.sock` (socket connect)
- So pacman-key, elephant, swaybg, non-installing makepkg and socket connects are invisible.
- Lane rules are also out of scope for the tool:
  - `jj log` and `jj git push` (jj is banned outright): 0 hits
  - `git status` and `git commit -am x` (lane git writes): 0 hits
  - `tools/mado-verify.sh` in default mode and with `--no-live`: 0 hits
- `kill -0 1` gives 0 hits by design.
- Controls hit as expected:
  - `pacman -Qi` → package_query
  - `sudo true` → host_mutation
  - `systemctl --user restart` → host_mutation
  - `hyprctl monitors` → live_probe
  - `omarchy-theme-set` → host_mutation
  - `expac` → package_query

**L5. Known shell misses, drafts not applied (medium severity).**
- `X=pacman; $X -Syu` gives 0 hits and no unparsed counter, so it is a silent miss (TwMissBashCVar).
- `f(){ sudo "$@"; }; f pacman -S x` flags `sudo $@` but misses the `pacman -S` reached through the helper argument (TwMissHelperFn).

**L6. Tools other than bash/eval are not analysed or counted (medium severity).**
- The tripwire inspects only `bash` and `eval` toolCalls.
- A `write` to `xd://mcp__rea_*` (REA/process-capture/browser), `read` of agent.db or session files, and edit/write outside the lane all produce no finding.
- The verdict JSON also has no counter for skipped tool calls.
- Fixture: a `write` to `xd://mcp__rea_capture_process_scenario` carrying `pacman -Syu` did not appear in bash_calls, eval_calls, any unparsed counter or any finding.
- JavaScript eval cells are counted only as eval_unparsed (fixture: `Bun.$\`pacman -Syu\`` gives eval_unparsed=1 and no finding).
- Smallest remediation (round 19): add an `other_tool_calls` count per file, keyed by tool name, so a reader can see what `clean` excludes.

**L7. "Issued" is not "executed".**
- toolResult records are ignored by design.
- Per the tool's own docstring, the verdict should be paired with a /var/log/pacman.log window count. I did not read that file: the host pause makes the log window the orchestrator's call.

**L8. Stderr noise (informational).**
- Scan 1 printed 11 `SyntaxWarning: invalid escape sequence` lines to stderr from `compile()` of transcript eval bodies.
- They did not affect the verdict (stdout label and exit were intact), but they mix target-derived noise into the tool's stderr. The remediation is a `warnings.catch_warnings()` around `compile` in `classify_eval`.

## Exploit path (why the limits matter)

A wave-2 seat could break the pause and still get `clean` by any one of these, none of which the instrument counts:
- running `pacman-key`, `elephant`, `swaybg`, `jj`, or `uv`/`npm` installs as plain bash;
- routing pacman through a shell variable;
- routing it through a non-literal python spawn (this one is counted, though not classified);
- using a non-bash tool.

The scan cannot detect these. It proves only that none of the classified forms in the bash/eval calls issued by 16:01:22Z hit host_mutation, package_query or live_probe.

## Artifacts (outside the lane, in /tmp)

| File | Contents |
|---|---|
| `/tmp/sentpw2/full.out`, `/tmp/sentpw2/full2.out` | Raw verdicts of scans 1 and 2 |
| `/tmp/sentpw2/sum.py` | Coverage aggregator: reads only the verdict JSON and w2/dispatch.json |
| `/tmp/sentpw2/mkfix.py`, `/tmp/sentpw2/fixture.jsonl`, `/tmp/sentpw2/fix.out` | Synthetic fixture: 29 records, label `findings` rc=1, counts host_mutation 4 / live_probe 1 / package_query 2; all 7 hits come from records c19–c25 (c19 being the helper-function `sudo $@`) |

## Installs

None.
