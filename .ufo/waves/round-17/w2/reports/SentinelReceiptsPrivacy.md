# SentinelReceiptsPrivacy — round 17 wave 2 (FALSIFY)

What I attacked: the round-17 evidence receipts as pushed at lane HEAD `988b858` (`origin/master` = `988b858`, remote `https://github.com/VeigaPunk/mado-shokunin.git`). The scope was `.ufo/waves/round-17/evidence/{tripwire-*.txt, oracle-*.json, session-index.json, schema-variants.json}`, plus the other 7 tracked siblings in that directory. I looked for secrets, personal data, commands from other lanes, absolute paths outside the known home path, and heredoc bodies.

Method: I read the **committed** bytes of all 23 tracked evidence files with `git show HEAD:<path>` and pattern-scanned them read-only in Python. I did not read any transcripts or open `agent.db*` or credential files, and I ran no host probes. Installs: none.

## Verdict

**The privacy attack failed.** I found no secret, no credential and no new personal data. No redaction is required. I have one low-severity provenance defect and three informational notes.

## Negative results (each pattern scanned over all 23 committed files)

| Pattern | Hits |
|---|---|
| GitHub tokens `gh[pousr]_`, `github_pat_`, `sk-…`, `AKIA…`, `xox?-`, `Bearer …`, JWT `eyJ…`, `BEGIN … PRIVATE KEY` | 0 |
| Emails, IPv4, MAC addresses | 0 |
| Host name (`/etc/hostname` value) | 0 in round-17 evidence. It already appears in 4 corpus files that predate round 17, at `27cd06f`: `corpus/knowledge/walker-deep*.md`, `walker-live-surface.md`, `waybar-walker-semantics.md`. That is outside this surface. |
| `agent.db`, `auth.json`, oauth, `.netrc`, `.ssh`, `id_rsa`, gnupg, keyring | 0 |
| Every `password`/`token`/`credential` key=value match | All are data, not values: 252 `"tokens_matched"` keys in `oracle-r15.json`, man-page grep patterns, and the `credential_pin` **count** (213) in `schema-variants.json:line_types`. No values. |
| Env-var **values** | 0. `HYPRLAND_INSTANCE_SIGNATURE`, `WAYLAND_DISPLAY` and `XDG_RUNTIME_DIR` appear only as names or `set/unset` echoes inside command text (`oracle-r13-r14.json`, MadoR13 rows). |
| Runs of 32+ `[A-Za-z0-9_-]` characters that are not sha1/sha256 hex or the two session-directory ids | Only provider tool-call ids (`toolu_*`, `call_*`, `fc_*`, `N_tool_*`), lane file names (`waybar-observation-boundaries-r16`) and schema/case labels. Nothing secret-shaped. |
| `/home/<user>` other than `/home/vgpnk`, or `/root` | 0 |
| toolResult / output bodies | 0. Receipts carry command text and verdicts only. The single quoted result is the public package version `'waybar 0.15.0-3'` (`oracle-r16.json` `m5_check`). |

**Absolute paths outside the home directory.** Only standard system locations, temporary scratch directories and upstream URLs:
- `/usr/{share,lib,include,bin}`, `/var/log/pacman.log`, `/var/cache/pacman/pkg`, `/var/lib/pacman/local`, `/etc/pacman.conf`, `/etc/xdg/waybar`, `/etc/systemd/<redacted>`, `/dev/input`, `/dev/uinput`, `/proc/$p/maps`.
- `/tmp/{as15,acov,r15review,mado-r17-frozen-*}` and similar.
- gitlab.freedesktop.org and raw.githubusercontent.com URLs.

**Paths under `/home/vgpnk`.** `.omp/agent/sessions/…` (900×), `Projects/shokunin/…` (109×), `.config/waybar/{config.jsonc,style.css}` (sha256sum arguments only), and `~/.config`/`~/.local/share/omarchy` path names. None of these carry contents.

**Heredoc bodies.** 30 oracle `command` rows contain `<<'PY'`/`<<'EOF'`. Every one is cut at 240 characters, which is the maximum length measured for `oracle-*.json` `.hits[].command`. So at most a ~200-character prefix of each body is published. The prefixes are the lane's own Python and draft-text substitutions over public lane files. They contain no secrets and no personal data.
- `tripwire-*.txt` `findings[].command` holds only the matched argv segment, at most 164 characters (`tripwire-r14.txt`). No heredoc text appears there.
- `schema-variants.json` snippets are at most 171 characters.

**Timezone.** `-0300` and `-03:00` appear in `tripwire-pacmanlog-join.txt` and `census-start.txt`, but they were already public in 20–29 files at the pre-round base `27cd06f`. Not new.

## Findings

### F1 — LOW (provenance, not privacy): `oracle-r16.json` rewrites `command` silently, and the redaction rule protects nothing

- **Evidence:**
  - `oracle-r13-r14.json` `.method` and `oracle-r15.json` `.method` declare the transform: "commands truncated to 240 chars, 32+ char [A-Za-z0-9_-] runs redacted".
  - `oracle-r16.json` applies the same transform to 2 rows but never declares it. Its `.scope` keys are `input_lines` and `token_regex` only. The rows:
    - `MadoR16/MadoR16.AttackClosureCarry.jsonl:143`: `corpus/knowledge/<redacted>.md`
    - `MadoR16/MadoR16.ReciprocalJoin.jsonl:77`: `corpus/knowledge/<redacted>.md` and a trailing `corpus/knowledge/<redacted`, cut mid-token at 240.
  - The hidden value is a public 33-character lane filename. `waybar-observation-boundaries-r16` is unredacted in `measure-before.json`, `measure-c1.json`, `measure-c2.json` and `measure-instrument.json`.
- **The redaction is also ineffective where it targets something id-like:**
  - `oracle-r13-r14.json` (MadoR14 rows at chars 53549 and 55207) redacts the session directory `2026-10-20T01-48-55-258Z_01a156ff-505a-7798-99c2-b47895c874f4`.
  - The same value appears unredacted 827× in `session-index.json`, every `tripwire-r1[3-6].txt` and `tripwire-anchor-r15.txt` `files[].path`, and `oracle-r15.json` `.session_dir`. It was also already public before round 17, in `.ufo/waves/round-14/w1/Safety.md` at `27cd06f`.
  - The other redactions (13 more) hit upstream commit SHAs and protocol file names in URLs and paths. Examples: `raw.githubusercontent.com/hyprwm/Hyprland/<redacted>`, `compare?from=1.32.0&to=<redacted>`, `wlr-protocols/unstable/<redacted>.xml`. All of these are public values.
- **Exploit path:** a verifier compares oracle `command` bytes with the transcript, or replays a URL from a receipt. They get a mismatch or an unreplayable URL. For `oracle-r16`, nothing in the receipt says the bytes were rewritten. This does not affect C3's `tripwire-vs-oracles.json` agreement counts, because those key on `(file basename, line, class)`, not command bytes.
- **Impact:** receipt byte-fidelity and replayability. No privacy gain, because each redacted value is public or published unredacted elsewhere in the same commit.
- **Smallest fix (no redaction needed):** add to `oracle-r16.json` `.scope` the same declaration the other two oracles carry:
  `"command_transform": "truncated to 240 chars; [A-Za-z0-9_-]{32,} runs replaced by <redacted>"`.
  Optionally, in a later round, drop the 32+ run rule for oracle receipts. On this corpus it removes only public values.

### F2 — INFO: an attempt to read the user's shell history is newly public (command only)

- **Evidence:** `oracle-r15.json`, row `MadoR15.LibinputTools.jsonl:99` `call_16021` (2026-10-20T07:27:33.752Z). The command was:
  `pacman -Q libinput libinput-tools; echo "=== current user bash history ==="; history | tail -n 20`.
  At `27cd06f`, `git grep -F 'history | tail'` returned 0 files; at HEAD it returns 1.
- **Receipt exposure:** none. No output body is published. `[INFERENCE]` `history` in a non-interactive bash tool typically prints nothing.
- **Note for other attackers:** the oracle classes this row `package_query` only. The seat's attempt to read shell history is not called out as a privacy-boundary attempt anywhere in the receipts. Reported as data. No redaction recommended.

### F3 — INFO: mentions of other lanes and fleet paths, but no other lane's commands

- **Session scope:** `session-index.json` lists 228 files, all `MadoR13–16`. `tripwire-r17-w1.txt` lists 70 files, all `MadoR17/MadoR17.*`. No other lane's transcript is indexed or scanned. Every `seat` and `file` field is a `Mado*` or `MadoR17.Oracle*` seat.
- **The one other-lane line:** `tripwire-pacmanlog-join.txt:9` attributes the `man-pages` transaction to the MoriR13/MoriR14 transcripts. This is a name and package only, and was already public at `27cd06f` in `.ufo/waves/round-16/w2/reports/AttackReportReadiness.md`.
- **Same file, line 10:** names `dmidecode` and `gitleaks` as host transactions outside the window. Already public at `27cd06f` in `.ufo/waves/round-16/w1/reports/NoInstalls.md`.
- **Fleet paths:** Mado seats' own commands name these paths:
  - `/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh` (sha256sum and log only)
  - the fleet's `.ufo/watchdog.log`, `.ufo/state/mado.*`, `.ufo/l0-questions.md`, `.ufo/prompts/mado-round-16.md`, `scripts/hyaku/lane-addendum.md`, `.ufo/waves/kaika-w1/mado-art.md`
  - the `--exclude-dir` names `.tower`, `.devin`, `kaidoku-shokunin`

  These are layout names only, all from `oracle-r15.json` and `oracle-r16.json` rows. No contents from another lane appear.

### F4 — INFO: hash commitments and id formats

- `session-index.json` publishes the sha256, byte size, line count, first/last timestamp and tool-call counts for 228 private transcripts. This is a commitment, not content, and was intended for the C3 binding.
- Tool-call id prefixes (`toolu_`, `call_`, `fc_`, `chatcmpl-tool-`) reveal which model-provider families seated agents, but no credential.

No action needed.

## Scope notes

- `.ufo/waves/round-17/evidence/measure-c3.json` is **untracked** (`git status: ??`), so it is not pushed. I scanned the working-tree copy anyway: it contains only lane-relative `corpus/knowledge/*.md` paths, and it is clean.
- The four pacman.log anchors cited in `tripwire-pacmanlog-join.txt` match the file bytes exactly: lines 2410, 2422, 2423 and 2429 (read with `awk 'NR==…'`).

## Recommended redactions

**None required.** The only recommended edit is F1's one-line `scope` declaration in `oracle-r16.json`. It fixes provenance and does not redact anything.
