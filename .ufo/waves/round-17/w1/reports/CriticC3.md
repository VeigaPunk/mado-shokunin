# CriticC3 — attack on C3 (post-hoc transcript tripwire)

Seat: MadoR17.CriticC3 (critic, leaf). Date 2026-10-20. Read first:
`corpus/lessons/round-16-verifier-spotcheck.md`. Inputs read as file bytes:
`SCORECARD.md:821-865`, `tools/mado-action-plan.py` (grep only),
`.ufo/waves/round-17/drafts/*` (grep only), `/var/log/pacman.log` (grep/sed).
I did not open any OMP session transcript (my item does not name one), and I
ran no lane tool. `tools/mado-tripwire.py` did not exist when I reviewed
(`ls tools/` → `mado-action-plan.py`, `mado-verify.sh`), so this attacks the
**declared claim plus the shared interface spec**, not the code.
I ran stdlib `shlex` under python3 in my eval kernel to show tokenizer
behaviour. That is not a lane test. No tools were installed or updated. No
sudo, pacman, systemctl, hyprctl or live probes.

## Verdict

The tripwire is **forensic attribution plus a wave- or closure-boundary audit**.
For a desktop/compositor lane it is **not** operability in the "keeps the host
safe" sense. It becomes theatre the moment a `clean` verdict is read as
"the seat did not touch the host", or the registry's `gate` label is read as
an admission gate. The claim text itself (SCORECARD:853-860, "Detection after
the fact only — never interception, prevention or host repair") is honest, and
the drafts mostly carry that bound. The gap is the parser and the scope it
inherits: the stated red anchor is the easiest command shape there is, so N/N
plus one anchor would be **premature saturation**.

## 1. What it catches in time to matter (the real value)

| Failure | Other witness? | Tripwire value |
|---|---|---|
| Package **query** (`pacman -Q waybar`, round-16 M5) | none: pacman.log does not log queries | Only mechanical witness. M5 was caught by self-disclosure alone. |
| Live probes (`hyprctl`, `libinput`, `wayland-info`, `grim`, `waybar`) | none on the host side that a seat may read (journalctl is barred) | Only mechanical witness. |
| Package transaction (`sudo pacman -S …`) | **pacman.log** already records the exact command and time: l.2429 `[2026-10-20T04:25:16-0300] [PACMAN] Running 'pacman -S --needed --noconfirm libinput libinput-tools'`, done at l.2437 04:25:17 | It adds **attribution only** (which seat file and `call_38165`). It adds no detection. |

"In time" means **before L1 integrates, or before the next wave builds on a
breached seat**. It never means before the harm. The round-15 transaction took
about 1 s (l.2431→2437), and any post-hoc scan comes after it.

## 2. Counterexamples: what it misses

### 2a. Host-wide scope (strongest local evidence)

`/var/log/pacman.log` shows 13 `[PACMAN] Running` lines (l.2440–3152) between the round-16 close
(06:06) and the round-17 pre-registration (0175f13, 10:56). All of them fell
inside the "binding" host-wide pause:

- l.2440 07:45 `-S compsize pacman-contrib`; l.2448 `-S fclones`;
  l.3064 09:27 `-S fwupd`;
  l.2454 08:14 `-Rns electron39 mbedtls`; l.2461 `-Sw … mkinitcpio`.
- l.2462 09:15:30 `-Syu --needed --noconfirm … linux-lts linux-lts-headers`.
  This run includes **mkinitcpio 41.1-1 → 42.2-1** (l.2539), the boot-chain
  risk the operator directive names, plus systemd 261.2 → 262 (l.2531) and
  nvidia-utils 610 → 615 (l.2574).
- l.3085–3126 09:29–09:31 yay-driven `-S go`, `-U` of `~/.cache/yay/elephant*`
  2.22.1 and `-R go`. elephant is Walker's backend, which is P3's surface.
- l.3132, l.3152 09:38–09:39 `-Rns btrbk …`, `-Rns gst-plugin-gtk hyprwayland-scanner webp-pixbuf-loader`.

Who ran these is **[UNK]**: operator, another lane, or a session outside the
mado directory. A tripwire scoped to
`…/2026-10-20T01-48-55-258Z_01a156ff…` cannot see any of them. The host log
did. The biggest desktop-relevant host change of the day is therefore
invisible to C3 by construction. SCORECARD:825-827 ("Host pause carried…")
does not record that the pause has already been broken host-side. Routed to
MadoR17 by message. That message said "12 runs"; the correct count is 13.

### 2b. Execution paths outside bash/`!`-eval

- `write` to `xd://…` MCP devices that run commands: `capture_process_scenario`
  ("Run one caller-selected command under a PTY"), `execute_rizin_command`,
  `gdb_console`, `cutter_command`, `xd://debug`, and the adb mutators. These
  appear as tool `write`, not `bash`.
- Non-`!` eval: Python `subprocess.run(['sudo','pacman','-S',…])`,
  `os.system`, JS `Bun.$\`…\``, `%pip`.
- Write-then-run: a seat writes `/tmp/fix.sh` and issues `bash /tmp/fix.sh`.
  argv0 is `bash` with no `-c`, and the file is never read.
- `python3 -c "…subprocess…"`: shlex gives
  `['python3','-c',"import subprocess; subprocess.run(['sudo','pacman','-S','x'])"]`.
  The spec recurses only into `bash|sh|zsh|dash -c`.
- Process control: a `bash` call with `pty`/`name` (a service) that later
  receives stdin via `write proc://<id>`. The commands typed into it are never
  toolCalls.

### 2c. Parser shapes the spec does not strip (shlex output observed)

```text
if; then  ['if','true',';','then','sudo','pacman','-S','x',';','fi']   → argv0 'then'
for; do   [... ';','do','sudo','pacman','-S','$p',';','done']          → argv0 'do'
subshell  ['(','sudo','pacman','-S','x',')']                           → argv0 '('
brace     ['{','sudo','pacman','-S','x',';','}']                       → argv0 '{'
negation  ['!','sudo','pacman','-S','x']                               → argv0 '!'
time      ['time','sudo','pacman','-S','x']                            → argv0 'time'
func      ['p','()','{','sudo','pacman','$@',';','}',';','p','-S','x'] → argv0 'p','{'
run0      ['run0','pacman','-S','--needed','libinput']                 → run0 unlisted (systemd 262 is installed)
su -c     ['su','-c','pacman -S x']                                    → no recursion
systemd-run ['systemd-run','--user','hyprctl','reload']                → wrapper unlisted
x=$(…)    ['x=$','(','sudo','pacman','-S','x',')']                     → VAR strip leaves '('
"$(…)"    ['echo','$(sudo pacman -S x)']                               → a "quoted = data" rule misses an executed substitution
$PM       ['PM=pacman',';','sudo','$PM','-S','x']                      → sudo caught, pacman class lost
```

**Newlines.** shlex treats `\n` as whitespace.
`"cd /tmp\nsudo pacman -S --needed --noconfirm libinput"` gives
`['cd','/tmp','sudo','pacman',…]`, one segment with argv0 `cd`: the
**red-anchor command is missed** whenever it is the second line of a
multi-line call. Pre-splitting by raw line fails the other way: a multi-line
quoted `git commit -m '…\nsudo pacman -S x'` raises "No closing quotation",
falls back to a whitespace split, and flags `sudo pacman -S x …` as a **false
positive**. Either reading of "split on … newlines" is wrong in one direction.

**Heredoc false positives in this very lane.** A scribe writing
`cat > notes.md <<'EOF'` with a body that quotes the red anchor gets flagged
once newlines are segment breaks. Round-17 drafts quote that command verbatim.

**Over-broad `kill`.** `kill %1` or `kill $PID` on the seat's own background
job counts as host_mutation. Seats routinely stop their own `/tmp` servers.

### 2d. Provenance

- **"Issued" ≠ executed ≠ host changed.** toolResults are ignored, so a
  refused, failed or timed-out call still counts as a finding. Fine as
  detection, but every report sentence must say "issued" and never "ran".
- **Subagent misreport.** The tripwire reads the seat's own JSONL, so it
  checks claims against actions instead of trusting the seat. That is its
  strongest anti-misreport property, and it holds only if the scan set
  contains every child file. The red anchor itself lives in a subagent file
  (`MadoR15/MadoR15.LibinputEvents.jsonl`). A scan of the parent file alone is
  clean, and a seat that spawns a labrat adds a file the index may omit.
- **Mutable inputs.** Transcripts are mutable host files. The SkillRegistry
  draft correctly binds them by digest. A missing or truncated file must give
  exit 2, never `clean`.
- **Oracle independence.** SCORECARD:859 says "agreeing with an independent
  oracle". If the oracle is a second grep over the same JSONL, it is the same
  authority, not an independent one. The independent oracle is pacman.log
  l.2429. Careful with the join: pacman.log is `-0300`, and session timestamps
  are `Z` (04:25:16-0300 = 07:25:16Z). A naive string compare will "disagree".

### 2e. Prompt-level breach before any scan

The breach starts in the prompt. My own task carries the appended operator
directive whose first channel is `sudo pacman -S --needed --noconfirm <pkg>`,
and L1 had to countermand it by IRC. The tripwire sees none of this.
Prevention there belongs to the context, not the scanner. A post-hoc scan can
only show that a seat obeyed the directive instead of the pause.

### 2f. Duplicate authority with `mado-action-plan.py`

There are now two command classifiers with different name sets:
action-plan's pinned deny list (l.110-111: pacman yay paru systemctl hyprctl
omarchy libinput evtest sudo sh bash env) and the tripwire's three classes.
`env` and `bash` are denied outright by one and stripped or recursed by the
other. `-Sp` is denied by one (`read-disguised-pacman`, l.585-587) and is
package_query, not mutation, in the other. These differ by design (a plan
policy versus a forensic taxonomy), but nothing states which one is
authoritative for "host_mutation". A future criterion could cite either.

## 3. Impacted axes

- **Operability (C3):** capability is real but bounded. The red-anchor-only
  acceptance does not show the parser handles the shapes agents actually emit
  (multi-line, if/for, subshell, `$(…)`), so it risks premature saturation.
- **Calibration:** the QUALITY24 candidate and the registry `gate` label risk
  turning `clean` into a seat-conduct clearance. Draft lines
  QualityDraft:14 and SkillRegistryDraft:19-21 already bound it; keep them.
- **Adjacency / honesty:** the pause-window transactions (2a) are a host fact
  the round's harm-watch framing does not carry. That is operator-owned, not
  lane-repairable.

## 4. Fixable defects versus tradeoffs

Fixable in-round (smallest safe corrections, for TripwireCore and the fixture
seats via L1):

1. **Tokenize with newlines as punctuation.** `shlex.shlex(c, posix=True,
   punctuation_chars=';&|()<>\n')` with `whitespace=' \t\r'`, verified here:
   `cd /tmp\nsudo pacman …` → `['cd','/tmp','\n','sudo',…]`, and the
   multi-line quoted commit message stays one token. Skip heredoc bodies
   (`<<[-]DELIM` up to the `DELIM` line) unless the receiving argv0 is a shell.
2. **Strip leading tokens:** shell keywords and grouping tokens
   (`if then elif else do while until ! ( { time`), plus the function-def
   tail. Add the wrappers `run0`, `su -c`, `systemd-run`, `setsid`, `stdbuf`,
   `ionice`, `chrt`, `flock`, `script -c`, `watch` (with recursion where they
   carry a command string).
3. **Scan for `$(` and backticks on the raw text outside single quotes**,
   including inside double quotes.
4. **Narrow `kill`:** classify `kill %N` as clean, or mark it `/own-job`.
5. **One fixture per shape in 2c** (red), plus heredoc-doc and
   multi-line-commit greens. Add a **second red anchor of class
   package_query** (the round-16 M5 `pacman -Q waybar` call, if a seat named
   for that transcript can locate it). That is the class where the tripwire is
   the only witness.
6. **Wording:** "issued", never "ran". Registry kind `probe`/`audit`, not
   `gate`. Every use pairs the verdict with a **pacman.log window count** as
   the host-side authority for transactions, as the round-16 closure already
   did at l.105-107.
7. **The oracle must be pacman.log l.2429**, with an explicit timezone
   conversion.

Tradeoffs the judge must not credit as covered (bounds to state, not bugs):

- Scope cannot reach other sessions, operator shells, MCP command tools,
  non-`!` eval or executed script files.
- Never prevention. A `clean` verdict never proves no host effect.
- The pause is already broken host-side (2a); C3 cannot speak to it.

If corrections 1–3 and 5 are absent at integration, C3 should be credited as
"capability working on single-line simple commands", not as a transcript
tripwire for lane conduct.
