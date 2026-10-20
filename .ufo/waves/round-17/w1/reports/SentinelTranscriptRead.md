# SentinelTranscriptRead — mado round 17, wave 1

Seat: MadoR17.SentinelTranscriptRead (sentinel, advisory, no remediation scope).
Surface: the planned `tools/mado-tripwire.py` (C3) reading OMP session JSONL and
committing derived JSON to the lane remote. Threats in scope: secret leakage,
prompt-injection text in transcripts, path traversal through `--scan`/selftest,
symlinks or links that reach `~/.omp/agent/agent.db*`.

**State at review time:** `tools/mado-tripwire.py` had not landed. `tools/` holds
only `mado-action-plan.py` and `mado-verify.sh`, and nothing named
`mado-tripwire*` exists on the filesystem. So this is a review of the declared
interface (L1 context §Tripwire interface), tested against the real transcript
corpus and against Python 3.14.8 stdlib behaviour. TripwireCore should
re-check the implementation against every item below.

## Method (read-only)

- Metadata census of the session root
  `/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-20T01-48-55-258Z_01a156ff-505a-7798-99c2-b47895c874f4`
  (`find`/`stat`). `~/.omp/agent/` was listed by name and mode only; no
  `agent.db*`, credential, `mcp.json` or `config.yml` file was opened.
- I parsed transcripts in my own eval kernel with stdlib `json`/`re`/`shlex`
  and printed only counts, tool-call anchors and masked shapes. No secret-like
  match was printed in clear text. Nothing was written under the session root
  or `/tmp`.
- Python 3.14.8 (`python3 --version`). I ran no pacman, sudo, systemctl,
  hyprctl or live probe. I installed or updated no tools.

Corpus facts used below:

| Fact | Value |
|---|---|
| `*.jsonl` under the root | 1,734 files; 215,000 lines; 0 invalid JSON lines; 0 files without a trailing newline; largest line 1,345,293 bytes; root is 1.6G |
| Other entries | 64 dirs; 5,541 non-jsonl regular files |
| Symlinks / FIFOs / regular files with nlink>1 | 0 / 0 / 0 under the root; 0 symlinks and 0 FIFOs under all of `~/.omp/agent` |
| `*.jsonl` file mode | 0644 (all 1,734) |
| `~/.omp/agent` | 0700; `agent.db`, `-wal`, `-shm` plus 7 `.corrupt`/`.pre-restore`/`.recovered` siblings, all 0600 |
| Assistant toolCall names (root) | read 29,449; bash 19,483; grep 8,752; edit 6,859; write 4,470; glob 3,312; eval 1,525; wait 519; … |
| Mado scope (MadoR13–R16, 228 files, matches SessionIndex) | 2,880 bash calls; 217 eval calls, of which 54 spawn processes |
| Red anchor | `MadoR15/MadoR15.LibinputEvents.jsonl` l.54: `bash`, `call_38165`, `sudo pacman -S --needed --noconfirm libinput libinput-tools` (re-confirmed) |
| Lane remote | `origin https://github.com/VeigaPunk/mado-shokunin.git`; unauthenticated `curl` of the repo page returned HTTP 200, so [INFERENCE] the repo is public and every committed receipt is world-readable |

## Findings (highest first)

### F1 — HIGH: eval-spawned commands never reach the scanner, so "clean" overstates

**Exploit path:**
1. An agent runs `await tool.bash(command='sudo pacman -S …')`, or
   `subprocess.run(["bash","-c",recipe])`, inside an `eval` cell.
2. The transcript records one `eval` toolCall. No `bash` toolCall is written
   for the nested command.
3. The scanner only parses eval lines that start with `!`. It returns
   `clean`, exit 0.

**Evidence:**
- `MadoR15.jsonl` l.96 is an assistant `eval` toolCall whose code calls
  `tool.bash(... command=f'UFO_CONFIG_PATH=… ')`. l.97 is
  `custom/tool_execution_start` and l.98 is the `toolResult`. The nested
  command string appears only at l.96 (inside eval code) and l.98. It never
  appears as a `bash` toolCall.
- Whole root: of 1,525 eval calls, 442 contain `subprocess`, 11 `tool.bash`,
  5 `Bun.$`, and 0 have a line starting with `!`. The specified `!` path
  therefore covers nothing in the real corpus.
- Mado scope: 54 of 217 eval calls spawn processes. 6 of them also name a
  classified word: `MadoR14.SourceSafety` l.152/l.155
  (`subprocess.run(["bash","-c",recipe])`), `MadoR15.jsonl` l.96/l.251,
  `MadoR16.jsonl` l.92/l.215.

**Impact:**
- A `clean` verdict cannot mean "no host mutation was issued". It means "no
  classified command appeared as a bash toolCall or a `!` eval line".
- If L1's C3 wording or SKILL registry text says more than that, it is a
  calibration defect.

**Smallest remediation:**
1. Parse eval code with `ast.parse(code, flags=ast.PyCF_ALLOW_TOP_LEVEL_AWAIT)`.
   This only parses; it executes nothing. Catch `SyntaxError`,
   `RecursionError`, `MemoryError` and `ValueError`.
2. Classify literal string arguments of `tool.bash(command=…)`, literal
   `subprocess.*`/`os.system` argv lists, and the strings passed to
   `bash -c`/`sh -c`.
3. Count every other spawning eval call in a new verdict field,
   `"unparsed_spawns":[{"file","line","tool_call_id","reason"}]`. Reasons
   include non-literal arguments, JS cells and parse errors.
4. Disclose that count beside every C3 claim.
5. At minimum, without the parser: emit the count and change the registry
   wording to "bash-toolCall tripwire".

### F2 — MEDIUM: symlinks, hard links or special files can route the read into `agent.db*` and publish its bytes

**Exploit path:**
1. Any seat with lane or `/tmp` write access creates
   `x.jsonl -> ~/.omp/agent/agent.db` (or `-wal`), or a hard link on the same
   btrfs, inside a directory later passed to `--scan`.
2. Neither `os.walk` (defaults verified: `followlinks=False`, `onerror=None`)
   nor `pathlib.rglob` filters out symlinked files. `open()` follows them.
3. The bytes are hashed into the receipt. Parsing fails, and if the error path
   echoes the offending line (for example `repr(raw[:200])`), session and
   auth bytes from a 0600 file land in a receipt pushed to a public remote.

A FIFO named `*.jsonl` blocks the scan forever. `/dev/zero` behind a symlink
exhausts memory. `onerror=None` silently skips an unreadable subdirectory,
which yields a false `clean` instead of exit 2.

**Evidence:**
- 0 symlinks, 0 FIFOs and 0 nlink>1 files today. Refusing all three
  therefore costs nothing on real data.
- `agent.db*` are 0600 inside 0700 `~/.omp/agent`.

**Smallest remediation** (all failures → `could_not_evaluate`, exit 2):
1. Explicit `PATH` arguments must end in `.jsonl` or be a directory. Refuse
   anything else.
2. For every candidate file:
   - `st = os.lstat(p)`
   - refuse if `S_ISLNK`, if not `S_ISREG`, or if `st.st_nlink != 1`;
   - `fd = os.open(p, O_RDONLY|O_NOFOLLOW|O_NONBLOCK|O_CLOEXEC)`;
   - require `os.fstat(fd)` to match `(st_dev, st_ino)`;
   - cap size (e.g. 256 MiB) before reading.
3. Directories: `os.walk(root, followlinks=False, onerror=<raise>)`. Refuse
   (do not skip) any symlinked dir or file found under the root.
4. Deny by realpath: refuse anything that resolves under `~/.omp/agent/`
   other than `~/.omp/agent/sessions/`. Refuse basenames matching
   `(?i)(\.db(-wal|-shm)?$|\.db\.|^config\.yml|^mcp\.json|auth|oauth|credential|token|device-id)`.
5. Error messages carry only `path`, `line` and a fixed reason string. Never
   include line bytes or the decoder exception text, which can embed input.

### F3 — MEDIUM: the `[A-Za-z0-9_-]{32,}` rule misses common secret shapes in committed `command`

Measured with the specified regex (output shown is after redaction):

| Input shape | Redacted? |
|---|---|
| `echo 'hunter2!' \| sudo -S pacman -S x` | no, the password survives |
| `sudo -S pacman -S x <<<Tr0ub4dor3` | no |
| `AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE sudo …` (20 chars) | no |
| `https://bob:s3cretPass@example.com/f` | no |
| base64 containing `+`/`/` (`Zm9vYmFy…+cXV4/…`) | no, because `+` and `/` break the run |
| JWT `eyJ….eyJ….<sig>` | only the signature segment |
| `ghp_` + 36 chars | yes |

If the 240-char truncation runs before redaction, a token cut at the boundary
to fewer than 32 characters leaks as a prefix.

**Current exposure is low, not zero:**
- Whole root: 17 secret-pattern hits in bash commands. All are keyword
  mentions or grep patterns; both `github_pat_` hits have tail length 0.
- Mado scope: 0 secret-pattern hits among commands that would become
  findings.
- One fleet command, `TsukuroiR16.R15NoticeHealth` l.72, contains both
  `authorization` and `pacman` (prose inside a `python3 - <<'EOF'` heredoc,
  see F6).

**Smallest remediation, applied in this order** (redact → strip controls →
truncate to 240):
1. A segment containing `sudo -S`/`--stdin` → replace the whole command with
   `<redacted:sudo-stdin>`.
2. Drop text after `<<<`, and heredoc bodies.
3. Redact the value of `VAR=…` when VAR matches
   `(?i)(pass|secret|token|key|auth|cred|cookie|session)`.
4. Redact URL userinfo `//[^/@\s]+:[^/@\s]+@`.
5. Redact `(?i)(authorization:|bearer|x-api-key:)\s*\S+`.
6. Redact `AKIA[0-9A-Z]{16}`.
7. Widen the run rule to `[A-Za-z0-9+/=_.-]{32,}`.
8. Only findings may carry `command`. Never emit non-finding commands.

### F4 — MEDIUM (adversarial evasions): parse differentials between shlex and bash hide commands

These inputs were run through
`shlex.shlex(s, posix=True, punctuation_chars=True); whitespace_split=True`:

| Input | shlex tokens | What bash runs |
|---|---|---|
| `echo x#;sudo pacman -S y` | `['echo','x']` | sudo (`#` mid-word is literal in bash) |
| `echo ${#a}; sudo …` | truncated the same way | sudo |
| `ls\nsudo pacman -S y` | one segment, because `\n` is whitespace | segment-splitting must survive this |
| `sud\<newline>o pacman` | `'sud\no'` | `sudo` |

Other forms that need handling:
- `$'\x73udo' …`
- `$p -S y` and `SUDO=sudo; $SUDO …`
- `{ sudo …; }`, `then sudo`, `do sudo`, `time sudo`, `! sudo`
- `sudo -u root -- pacman`, `sudo --user=root pacman`
- `run0 pacman …`, `su -c "pacman …"`, `exec -a x sudo …`
- `cat <(sudo …)`, `>(sudo tee …)`
- `"$(sudo …)"` versus `'$(sudo …)'`. Both shlex to the same token, but only
  the first executes.

**Real-data impact:** on all 2,880 Mado-scope bash commands, the default
lexer and a hardened lexer found the same 216 commands with a classified
argv0. These are adversarial or fixture cases, not historical misses.

**Smallest remediation.** This configuration was tested on the cases above:

```python
s = s.replace('\\\n', '')
lx = shlex.shlex(s, posix=True, punctuation_chars='();<>|&\n')
lx.whitespace = ' \t\r'
lx.whitespace_split = True
lx.commenters = ''
```

Then drop tokens from one that *starts* with `#` up to the next `\n` token.
Also:
- Treat `( ) <( >( { } then do else elif ! time` as segment starts.
- Add `run0` and `su -c` to the `sudo` family.
- Skip `sudo` option values (`-u X`, `--user=X`, `--`).
- Flag argv0 beginning with `$` as rule `unresolved_argv0`. Count it at
  least; do not report it as clean.
- Add these strings as selftest fixtures.

### F5 — LOW–MEDIUM: an uncaught exception exits 1 ("findings") instead of 2

Verified on Python 3.14.8:
- A 5,000-digit integer raises plain `ValueError` (int-digit limit), not
  `JSONDecodeError`.
- 200k nested `[` raises `RecursionError`.
- `\ud800` parses, then `json.dumps(..., ensure_ascii=False)` to stdout
  raises `UnicodeEncodeError`.
- Duplicate keys parse silently with last-wins (`{"type":"message","type":"custom"}`
  → `custom`).
- `NaN` is accepted.

**Impact:** a crash exits 1, which the protocol reads as "findings". A
hostile or truncated line can fake or mask a verdict class. A selftest case
with `want_exit 1` and empty findings would pass on a crash.

**Smallest remediation:**
1. Read each file once as bytes and split on `b'\n'`. Never use
   `str.splitlines()`: it splits on U+2028/0085/FF/VT, although the corpus
   has 0 such bytes today.
2. Per line, `except (ValueError, RecursionError, UnicodeError)` → exit 2.
3. Top-level `except BaseException` → print
   `MADO_TRIPWIRE: could_not_evaluate` and exit 2.
4. Use `json.dumps(..., ensure_ascii=True)`.
5. Pass `object_pairs_hook` that rejects duplicate keys, and `parse_constant`
   that rejects NaN/Infinity (exit 2).
6. Selftest counts a case as passing only if the verdict line parses as
   schema `mado-tripwire-verdict-v1`.

### F6 — LOW: heredoc bodies are treated as commands, publishing prose into the receipt

The spec splits segments on newlines, so heredoc bodies get parsed.

**Evidence:**
- 1,418 fleet bash commands use heredocs. In 9 of them (7 files), a body line
  has a classified naive argv0, for example `MadoR16.RoundConformance` l.45
  (`hyprctl`) and l.50 (`pacman`), and `MadoR14.Safety` l.115 (`journalctl`).
- Whether a body runs depends on its consumer: `bash <<EOF` executes it;
  `cat >f <<EOF` and `python3 - <<'EOF'` do not.

**Impact:**
- False positives push up to 240 characters of heredoc prose into a public
  receipt (see the F3 example).
- Bodies fed to a shell are real commands. Parsing them flat gets the
  classification right only by accident.

**Remediation:**
- Detect `<<-?\s*['"]?WORD` and split off the body.
- If the consumer argv0 is `sh|bash|zsh|dash`, recurse into the body.
- Otherwise treat the body as data and count it in `heredoc_data`.

### F7 — LOW: prompt injection, TOCTOU and live inputs

- **Injection.** The scanner is deterministic stdlib code. Transcript text can
  only steer it through code paths that execute content, and the spec has none
  if it holds:
  - no `eval`/`exec`/`compile` on content;
  - no `subprocess` except the selftest self-invocation (list argv,
    `shell=False`, `timeout=`);
  - no `os.path.expandvars`/`expanduser` on content.

  The residual risk is downstream: committed `command` strings are read by LLM
  seats and judges. Mitigation:
  - keep `ensure_ascii=True`;
  - strip C0/C1 controls and bidi marks (U+202A–202E, U+2066–2069) before
    truncation;
  - label the field as untrusted target data in the receipt schema doc.
- **TOCTOU.** Hash and parse the same in-memory buffer. Do not `sha256sum` and
  re-read separately. Transcripts are live and mutable.
- **Live files.** The round-17 transcripts are still being appended under the
  same root, so scanning the root includes them. Pass the 228 files from
  SessionIndex's `session-index.json` (sha256
  `06c259bc…f70df5`) as explicit paths and compare each digest. A mismatch
  goes into the receipt, not a silent re-hash.

### F8 — LOW: scope and privacy of what gets pushed

- Scanning the whole session root would publish other lanes' commands and
  paths to the Mado public remote: 1,734 files, about 1.6G, many lanes.
  Restrict the committed receipt to the 228 Mado files.
- `files[].path` and `session-index.json` carry absolute paths: the username,
  the session UUID and agent names. This is accepted low-grade disclosure.
  Note it, or relativize paths to the session root.
- Over-redaction: the session directory component
  `2026-10-20T01-48-55-258Z_01a156ff-…` is one run of 32 or more
  `[A-Za-z0-9_-]` characters, so commands that cite transcript paths lose
  their anchor. This affects fidelity, not security; `file`/`line` keep the
  anchor.

### F9 — LOW: selftest traversal and permit laundering

`--selftest DIR` reads `args` from `expected.json`. An absolute path or `..`
entry scans arbitrary files, which brings the F2 problems back through data.

**Remediation:**
1. `os.path.realpath(DIR/arg)` must stay under `realpath(DIR)` and pass the
   same lstat/no-symlink checks as F2.
2. `permit` values must be in `{host_mutation, package_query, live_probe}`.
   Anything else → exit 2 for `--scan` and for malformed `expected.json`.
3. Permitted findings must still be listed in `findings`, with `permitted`
   recording which classes were waived, so a permit never erases evidence.

## Not in scope / not observed

- `resume_continuity_v1`: not part of this surface; no check made.
- No live, fabricated or readiness claims were found to judge. The tool does
  not exist yet, so I make no implementation claim.

## Checks for L1 after integration

1. F2 fixtures on `/tmp` copies: a symlink `x.jsonl` to a dummy file, a hard
   link, a FIFO, and an unreadable subdirectory → each exit 2, with no input
   bytes in stderr or stdout.
2. F4/F5 evasion and crash strings as `--selftest` cases, including
   `echo x#;sudo pacman -S y`, `ls\nsudo …`, the bigint line, the deep-nesting
   line and the duplicate-key line.
3. F3 redaction cases as selftest findings, checking that the committed
   `command` contains no password, AKIA key or userinfo.
4. Scan only the 228 SessionIndex paths and diff the digests. The red anchor
   gives `host_mutation` rules `sudo` and `pacman:-S` at
   `MadoR15.LibinputEvents.jsonl` line 54.
5. C3 and registry wording must state the F1 bound (bash toolCalls plus
   whatever eval coverage was actually implemented).

Tools installed or updated: none. Files written: this report only.
