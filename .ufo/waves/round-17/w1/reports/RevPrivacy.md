# RevPrivacy — privacy review: committed tripwire verdict / oracle JSON

Round 17 (hyaku phase 2), wave 1. Reviewer seat `MadoR17.RevPrivacy`. Read-only:
no host query of any kind, no lane file edited outside this report, nothing
installed or updated.

## Method

- Corpus: `.../MadoR16/*.jsonl` — 96 files, 9,290 JSONL lines, **1,182 bash
  toolCalls**, 47 eval calls, **0 eval `!`-lines**. The emitted universe of a
  verdict over this corpus is therefore exactly `bash.command` text.
- Deterministic 200-command sample: sorted file order, index
  `floor(k*1182/200)` for `k=0..199` (reproducible; no RNG).
- Redaction applied exactly as the interface states it — `s[:240]`, then
  `[A-Za-z0-9_-]{32,}` → `<redacted>` — so the sample measures the published
  artifact, not the raw transcript.
- `tools/mado-tripwire.py` was still absent at review time, so redaction order
  and `command` scope are taken from the declared interface. The two oracle
  artifacts (`oracle-r15.json`, `oracle-r16.json`) **landed mid-review** at
  11:04 and are measured directly below; `session-index.json` likewise.

## Direct answer

**No sampled command would publish a credential** — 0/1,182 for every credential
class tested (details in P4), and 0 in the 327 commands the two landed oracles
actually emit. The 32-char rule is *sufficient for the token class it targets*,
was never exercised as a secret filter in this corpus (0 true positives), and is
**not sufficient as the artifact's privacy boundary**: what survives is identity,
path and timeline metadata, and the rule's misses are structural rather than
incidental. It also destroys audit data the verdict exists to carry.

### Measured exposure in the landed artifacts

| Artifact | emitted commands | keep `/home/<user>` | length = 240 | heredoc body | newline | applied redactions | transcript digests | absolute paths |
|---|---|---|---|---|---|---|---|---|
| `oracle-r15.json` | 251 | 32 | 94 | 5 | 9 | 6 | 65 | 65 (`files[]`) + `session_dir` |
| `oracle-r16.json` | 76 | 45 | 55 | 9 | 11 | 2 | 0 (none published) | `scope.scan_root` |
| `session-index.json` | — | 228 paths | — | — | — | — | 228 unique | 228 |

The union of digests is 228 unique transcripts. All three files are currently
untracked (`??`) under `.ufo/waves/round-17/evidence/`; L1 decides whether they
are committed.

## Findings

### P1 — Paths and account identifiers survive every emission (low-moderate; mostly pre-existing)

- 146/200 sampled commands (73%) still contain `/home/<user>/...` after
  redaction; 176/200 (88%) still contain at least one absolute path.
- Landed oracles: 45/76 (59%) `oracle-r16` commands and 32/251 (13%)
  `oracle-r15` commands keep the home path. Host paths named: `/var/log` (12 in
  r15, 2 in r16), `~/.config` (3), `~/.local` (5 + 10), `/etc/systemd`,
  `/etc/xdg`, `/etc/pacman.conf`, `/var/lib` (1 + 2). `oracle-r15.files[]`
  publishes 65 absolute transcript paths.

Mitigating, and the reason this is not higher: `/home/<user>` is already
committed at HEAD in **305 files** (round-12/13 evidence and earlier), and the
session-store path + UUID appears once (`.ufo/waves/round-14/w1/Safety.md:45`).
A verdict adds no new host identity. What is new is a public artifact that pairs
those paths with command text and per-line timestamps from the session store.

Recommendation: substitute `/home/<user>` → `~` before emission; keep
lane-relative paths as they are.

### P2 — Truncate-then-redact leaks a token prefix (moderate; generic mechanism)

Reading the interface literally, the command is truncated to 240 chars *and then*
substituted. A run of ≥32 `[A-Za-z0-9_-]` chars that straddles offset 240 is cut
to fewer than 32 chars, so it no longer matches and escapes redaction entirely.

- Observed: **3/1,182 (0.25%)**, leaked prefixes of **23, 29 and 31 chars**
  (`AttackClosureCarry:161`, `AttackReportReadiness:86`, `CustomTooltip:145`).
- In this corpus the leaked runs are 40-char git SHA-1s and one 35-char path
  token — harmless. The mechanism is not harmless: a 40-char PAT starting at
  offset 209 would publish 31 of its 40 characters.
- An implementation that substitutes first and truncates afterwards is safe
  (the replacement shortens). The spec should say so, and a selftest case with a
  40-char token starting at offsets 200–239 would pin it.
- Not realized in the two landed oracles: none of the 3 boundary cases is an
  emitted hit, and the 149 commands sitting at the 240-char cap happen to cut
  inside no run. The defect is a property of the rule, not of these files.

### P3 — Whole-command emission carries unrelated text (moderate)

Classification is per shell segment, but the emitted window is the whole command
string (the interface does not say otherwise), and the landed oracles do emit
the whole string: 128/1,182 sampled-population commands embed heredoc bodies,
and in the emitted artifacts **9/76 `oracle-r16` and 5/251 `oracle-r15` commands
carry a heredoc body, with 11 and 9 carrying newlines**. When any segment of such
a command classifies (`bash -c`, `$( )`, backticks, or a flagged invocation after
a `cd`), up to 240 chars of the *rest* of that string are published too — file
content pasted into test fixtures, expect documents, data the agent was reading.

Recommendation: emit the matched segment (and for `bash -c`/`eval`, the inner
segment) alongside `argv0`, rather than the full command.

### P4 — Sub-32 structured secrets and PII are out of scope by construction (low-moderate; unexercised here)

The rule only sees contiguous `[A-Za-z0-9_-]` runs ≥32. Blind by design to:
emails, `scheme://user:pass@host`, `-u user:pass`, `password=`/`token=` values
under 32, AWS access-key IDs (20 chars), base64 of ≤23 bytes, JWT segments under
32, hostnames, UIDs, IPv4s.

Measured over all 1,182 commands: **0** emails, **0** `Authorization`/`Bearer`
with a value, **0** `AKIA…`, `ghp_`/`github_pat_`/`sk-`, **0**
`id_rsa`/`id_ed25519`/`.ssh`, **0** `agent.db`, **0** `op://`, **0**
`BEGIN … PRIVATE KEY`, **0** URL userinfo, **0** `ssh user@host`. The apparent
near-hits are code: 7 `@` are jq filters, 8 query strings are GitHub
`?recursive=1`, 9 `-p` are `mkdir -p`/`sed`, and the single `authorization`
occurrence is a docs grep.

Same scan for operator-personal classes: **0** paths under
`Pictures`/`Documents`/`Downloads`/`Music`/`Videos`, **0** shell-history files,
**0** browser-profile commands, **0** `netrc`/`npmrc`/`pypirc`/docker config,
**0** `gpg`/`ssh-add`/agent-socket commands, **0** `.gitconfig`/`git config`
reads or `GIT_AUTHOR_*`/`EMAIL` assignments. Personal data is absent from the
emitted universe here; the exposure is identity/paths/timeline, not content.

So: hardening, not a live defect — five regexes ahead of the ≥32 rule (email,
`://\S+:\S+@`, `\b(AKIA|ghp_|github_pat_|sk-)\w+`,
`(?i)(password|token|secret|api[_-]?key)\s*[=:]\s*\S+`, home directory) cost
nothing and remove the class dependence on luck.

### P5 — Metadata channel: the seal is wider than the content (low)

Per file the schema publishes the absolute path (session root + UUID + round
dir), a full `sha256`, line and call counts; per finding, `file`, 1-based line,
toolCall id and timestamp. Observed in the landed artifacts:

- `oracle-r15.json`: absolute `session_dir`, **65 absolute `files[].path`** values
  and **65 `sha256` digests** (each file also carries `basename`).
- `session-index.json`: **228 absolute paths and 228 unique digests**, timestamp
  span 04:04:30Z–09:13:27Z.
- Union across the wave: **228 unique transcript digests**, all currently
  untracked and staged for a commit decision.
- `oracle-r16.json`: no per-file digests, only `scope.scan_root` — so the two
  oracles already disagree on schema (`tool_call_id` vs `id`, `files[]` present
  or absent). A consumer cannot treat them as one format.

Why it matters:

- A digest of an un-committed transcript is a fingerprint: it lets anyone
  confirm a candidate transcript offline, and if the store ever leaks it
  attributes the leak to this repo. No secret is disclosed; deniability is.
- Millisecond timestamps plus line numbers publish the operator's working window
  and point precisely into the raw store.

Recommendation: drop the per-file `sha256` (or truncate to 12 hex), reduce
discovered paths to `basename` while keeping the count fields, and drop the
digests from `session-index.json` before it is committed.

### P6 — `permitted` echoes caller input (low)

`--permit <CLASS>` values are republished in the verdict. If they are echoed
unvalidated, a mistyped or shell-substituted argument lands in the committed
file. Intersect against the three known class names and fail with exit 2
otherwise — that is already the tool's fail-closed territory.

### Correctness note that bounds what a verdict may be cited for (low)

A `clean` verdict means "no unpermitted finding among *parsed* segments", not
"no host mutation": eval code not starting with `!` is never parsed (so Python
`subprocess`/`os.system` shell-outs are invisible), and `find -exec`, `make`,
`uvx`, `nix` and wrappers outside the listed set are unparsed. The module
docstring must say this, and a clean verdict must not be cited as host-harm
clearance.

## Is 32 characters enough?

| Role | Verdict |
|---|---|
| Token filter for high-entropy secrets wholly inside the 240 window | yes — 0 misses in 1,182 commands |
| Privacy boundary of a committed artifact | **no** — misses identity/path/timeline by design (P1, P5), a boundary prefix (P2), out-of-band shell data (P3), and every structured secret below 32 chars (P4) |

The cost side is the sharper argument. Of 72 redacted runs across 62 sampled
commands, **35 are git SHA-1s** and **35 are ≥32-char hyphenated filenames**;
only 2 are UUID-ish, none is a secret. In the landed artifacts this is not
hypothetical: **8/8 applied redactions** (6 in `oracle-r15`, 2 in `oracle-r16`)
are a raw-URL ref/commit, GitHub query parameters and long knowledge filenames —
none is a secret. The rule redacts exactly the commit IDs and file names a
verdict needs to be reproducible, while leaving the operator-identifying strings
untouched. The fix is to change *what* is redacted, not to widen the threshold.

## Minimal fix set, in order

1. Redact, then truncate the redacted string (P2) + one boundary selftest case.
2. Emit the matched segment instead of the whole command (P3).
3. `~`-normalize `/home/<user>`; basename discovered paths (P1, P5).
4. Five structured-secret regexes before the token rule (P4); validate
   `--permit` (P6).
5. Do not commit transcript `sha256`s (P5); describe the verdict as
   content-exposing in its docstring.

## Residual risk

- Command text is operator/agent-authored. Nothing prevents a future command
  from containing a real sub-32 credential, a personal file path, or a heredoc
  body. The fixes above are the difference between "probably fine" and "bounded
  by construction".
- Only MadoR16 was sampled. R13/R14/R15 have different command distributions;
  the R15 corpus contains the `sudo pacman -S` anchor and its surrounding
  libinput commands, which I did not sample.
- No live host claim is made or implied anywhere in this review.

## Verification gaps

- `tools/mado-tripwire.py` was absent. I could not verify its redaction order,
  whether it emits the whole command or the matched segment, or its selftest.
  For the tripwire, P2 and P3 are read from the declared interface; for the two
  landed oracle artifacts, P1/P3/P5 are measured on their bytes.
- The two oracle schemas already diverge (`tool_call_id` vs `id`, `files[]`
  present vs absent). I did not reconcile them; L1 must not assume one consumer
  can parse both.
- The emission estimate (36/1,182 findings; 8/200 in the sample) is my
  approximation of the declared classifier, not a run of it.
- Sample scope was fixed at 200 commands by the assignment, so per-class rates
  in the low single digits carry wide intervals.
