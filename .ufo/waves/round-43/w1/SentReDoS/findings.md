# `mado-geometry` security review — untrusted JSON, untrusted classes, operator regexes

Round 43 / w1 · seat `SentReDoS` · 2026-10-26 · Python 3.14.8 (CPython), x86-64 Arch, Hyprland 0.56.2 host (read-only).

**Artifact under review.** `.ufo/waves/round-42/c1/ctl-ref-tool.py.txt` (the C1 contract reference), sha256
`e3c2e471505932f797a98ee2aa9ab1b04fc919f2140509282ef8472498135a99`; probe copy `SentReDoS/bin/mado-geometry.py`
has the **same sha256** (byte-identical), `--selftest` → `MADO_GEOMETRY_SELFTEST: 73/73 passed`. The contract
quoted below is the docstring of `quality/counters/c1-r42-geometry.py` (`PRED-C1-r42`), which restates it.

**Trust model used.** Three inputs cross a boundary into this process:

| input | who chooses it | bound in the contract |
|---|---|---|
| `class` (and `address`) of each client in `hyprctl clients -j` | **any application** (its Wayland `app_id`; no path in the tool validates it) | none — a string, any length, no control chars below U+0020 to be *matched* (`:39`) |
| `match:class REGEX` in a rules file | operator, or whatever generates the config | 1-200 chars, `SAFE` alphabet, no `(?` `*+` `++` `?+` (`:34-36`) |
| the JSON dump itself (`--clients FILE` or stdin) | whoever supplies the dump | ≤1048576 bytes, "a list whose every element is an object" or `bad_json` (`:20-21`) |

Severity rubric: **High** = contract violated on reachable input, or the tool wedges without bound;
**Medium** = bounded misbehaviour, or needs a careless consumer; **Low** = hardening, no exploit shown.

---

## SR-1 — High — catastrophic backtracking is contract-admissible (`(a+)+$`, `(a|aa)+$`, `(a*)*b`, `.*.*.*b`)

**Surface.** `SAFE = re.compile(...)` at `ctl-ref-tool.py.txt:69` admits nested quantifiers, quantified
overlapping alternations and stacked wildcards; `regex_ok` (`:120-128`) only bans the *possessive* forms and
tests compilability; `matches` (`:180-183`) then runs `re.fullmatch(rx, cls)` on the attacker's string with a
backtracking engine. Hyprland itself uses `RE2::FullMatch` (linear), so the tool is strictly more fragile
than the compositor it models.

**Exploit path.** A config contains one rule the contract admits (all five below are reported as
`rules=1`, i.e. *supported*, not `unsupported`). Any application names itself so its `class` is
`"a"*n + "!"` — 31 bytes, no control characters, so the `:39` filter does not drop it. The tool never
returns.

**Evidence** (class = `"a"*(n-1) + "!"`, one supported `size` rule; wall clock, `python3 -I bin/mado-geometry.py
--clients misc/k.json --rules misc/k.conf`; raw logs in `probe_redos.log`, `probe3.log`):

| REGEX (all supported) | class length | time |
|---|---|---|
| `(a|b)+$` (control, no ambiguity) | 1000 / 100000 | 0.017 s / 0.020 s |
| `(a+)+$` | 19 / 21 / 23 / 25 / 27 | 0.022 / 0.043 / 0.124 / 0.461 / 1.771 s |
| `(a+)+$` | 28 / 29 / 30 / **31** / 33 | 5.17 / 10.51 / 18.45 / **35.66** / >45 s (killed) |
| `(a|aa)+$` | 33 / 60 / 100 / 1000 | 0.31 / >30 / >30 / >10 s (killed) |
| `(a*)*b` | 1000 | >10 s (killed) |
| `.*.*.*b` (no group at all) | 1600 / 40000 | 0.344 / >10 s (killed) |
| `.*.*.*.*b` | 800 / 1600 | 8.94 / >10 s (killed) |

`(a+)+$` doubles per added character (1.9×/char): a **31-byte** `app_id` costs 36 s, a 40-byte one ~3 h, a
1 MiB one never finishes. One ambiguous rule among 300 otherwise-safe rules: 0.721 s on a 34-byte class
against a 0.016 s baseline (`probe_redos.log`, last line). The tool's own selftest asserts that
`^(a|b)+\.c$` is acceptable (`regex_ok` → True) — the same alphabet admits `(a|aa)+$`, so **the alphabet
check is not a complexity check**.

**Impact.** Read-only, same-uid: no privilege boundary and no secret is crossed. The loss is the
instrument itself — the C1 capability (does a rule's size match the compositor's?) becomes unavailable for
any config that contains an admitted ambiguous rule as soon as one hostile client exists, and a monitor
that pipes `hyprctl clients -j` into it wedges instead of reporting. It also makes the tool's own delivery
fragile: the counter's cost bound is 3×30 s then "every remaining fixture … fails" (`:65`).

**Smallest remediation, ranked.**
1. **Complete, behaviour-identical (recommended):** stop using a backtracking engine for `matches`; match
   the `SAFE` subset with a linear-time matcher (Thompson NFA — the subset has literals, `.`, `|`, groups,
   `* + ?`, `^ $` and the listed escapes; no backrefs/lookaround/flags). For `fullmatch` on a class with
   no control chars (already required by `:39`) the accepted language is the same, so all 37 fixtures and
   all 73 selftest comparisons are unchanged; the import set stays `json os re stat sys`, so clause **g**
   still holds. ~120 lines.
2. **Cheap, heuristic, fixture-verified:** reject statically ambiguous forms in `regex_ok` — (a) a
   quantifier applied to a group that contains a quantifier, (b) a quantifier applied to a group whose
   alternatives share a first atom, (c) two or more `.*`. I implemented (a)-(c) and compared it with the
   shipped `regex_ok` on the counter's own list: **54/54 `regex0` entries classify identically**
   (21 supported, 33 unsupported), the 7 selftest `regex_ok` assertions are unchanged, `^(a|b)+\.c$`,
   `(a|ab)(c|d)`, `(a|b)+$` and `^(org.omarchy.gkeep)$` stay accepted, and `(a+)+$`, `(a|aa)+$`, `(a*)*b`,
   `.*.*.*b`, `.*.*.*.*b` are rejected (`probe4.log` §N). It is still a heuristic and must be declared:
   the *documented* rule set changes (a rule that was `supported` becomes `unsupported`), so it is a
   `PRED-C1` **v2** amendment, not a silent fix.
3. A class-length cap is **not** a fix: 30 characters already cost 18 s. Only a non-backtracking matcher
   removes the exponential.

---

## SR-2 — High — unbounded matching work on legal inputs (no ambiguity needed)

**Surface.** `matches` is called once per (client, rule) pair, each call scanning the whole class
(`:180-183`), and `re.compile` result is thrown away at `:127`, so the patterns live in `re`'s cache; the
contract bounds each *file* at 1 MiB but never bounds the number of `--rules` arguments, the number of
rules, the class length, or the product clients×rules×length.

**Exploit path.** A hostile client publishes a long `app_id` (40 KiB used here; the dump stays under the
1 MiB cap with 26 such clients). The operator's config — or any generated config — supplies many rules;
`--rules` may be repeated without limit, each up to 1 MiB (~30 834 supported rules per file).

**Evidence** (`probe2.log` §G, `probe3.log` §L; every input inside the caps: clients ≤1 041 093 B,
rules ≤ 1 260 000 B → the 1.26 MB case correctly returned `too_large` and is excluded):

| clients × class | rules | time |
|---|---|---|
| 20 000 × 1 B (the counter's `many0` shape) | 300 | 2.58 s |
| 26 × 40 000 B | 300 / 600 / 1200 | 4.8 / 9.5 / 19.3 s (exactly linear) |
| 13 × 40 000 B | 12 000 | **99.3 s** |
| 26 × 40 000 B | ~30 800 (one 1 MiB rules file) | ~1 040 s (extrapolated from the linear fit; not run) |
| 26 × 900 000 B, 1 rule | 1 | 0.032 s ⇒ the cost is the *product*, not the class alone |

**Impact.** Same as SR-1 (availability of the instrument), but reachable with *no* pathological regex, and
scalable by adding `--rules` files. Both sides of the product are attacker-influenced in a realistic
deployment: the dump comes from the compositor, the app_id from an application.

**Smallest remediation.** Bound the product, not the parts: before matching, compute
`pairs = clients_matched_candidates × len(rules)` and `chars = Σ len(class)` over those pairs, and refuse
when `pairs + chars > 5·10⁷` (≈1-2 s on this host). Every fixture fits with ≥4× margin — the maximum is
`many0` at 6.0e6 pairs + 6.0e6 chars (measured 2.58 s); the 99.3 s case is 1.56e5 + 6.24e9 and is refused
(`probe4.log` §O). The refusal needs a verb the contract does not have, so it must be a **v2** amendment:
either reuse `SETUP too_large` (it overstates the cause) or add one SETUP reason, e.g.
`SETUP too_costly` (stdout one line, exit 2, stderr empty — the existing SETUP shape). Secondary hygiene:
compile each rule once (`rule["pat"] = re.compile(rx)`) instead of re-entering `re`'s cache per pair.

---

## SR-3 — High as a predicate defect (Low as an exploit) — a deep JSON dump crashes the tool instead of `SETUP bad_json`

**Surface.** `parse_clients` catches only `(UnicodeDecodeError, ValueError)` (`:162-166`); CPython's JSON
scanner raises `RecursionError` (a `RuntimeError`) on deep nesting, and it is a **stack-usage** guard
(`Stack overflow (used 8140 kB)`), not the 1000-frame limit.

**Exploit path.** Whoever supplies the dump sends 120 KB of `[` … `]` (depth 60 000). Nothing else.

**Evidence** (`probe2.log` §I, `misc_abc.log` §B):
```
depth 50 000 (100 KB)      → MADO_GEOMETRY: SETUP bad_json            rc=2   stderr 0 B
depth 60 000 (120 KB)      → rc=1  stdout 0 B                        stderr 24 lines, RecursionError
depth 500 000 (1 000 000 B)→ rc=1  stdout 0 B                        stderr 24 lines, RecursionError
[{"a":{"a":…}}] depth 150 000 (900 KB, a *valid* clients list) → rc=1 stdout 0 B, RecursionError
```
Contract violations, each a separate defect: (i) the input is not JSON-holding-a-list-of-objects, so
`bad_json` is required (`:21`); (ii) "Setup failure: stdout is exactly one line … exit 2" (`:17-18`) —
stdout is **empty**, exit is **1**; (iii) "stderr empty on exit 0/1/3/4" (`:50`) — 24 lines of traceback;
(iv) the traceback prints the tool's absolute path and source lines; (v) **exit 1 is `DIFFER`'s code**, and
`DIFFER` is documented as "a report, not a fault", so a monitor that keys on the exit code reads a crashed
run as a size mismatch with an empty body.

**Impact.** For a real deployment the dump comes from `hyprctl`, whose shape cannot be 60 000 deep — so this
is not a live DoS. It is a **contract hole**: the tool can be killed by an input the contract says must be
`bad_json`, silently, with the wrong exit code, and no fixture exercises nesting beyond one level
(`badjson0` has `[[]]`, `nan0` is flat). A w2 falsifier only has to feed this one input to the shipped tool.

**Smallest remediation.** `except (UnicodeDecodeError, ValueError, RecursionError)` in `parse_clients`
(one line) **plus** one contract sentence naming a nesting bound, because CPython's guard is
stack-dependent (50 000 passes and 60 000 fails on this host; another interpreter/stack size moves it):
"an input nested deeper than 64 is `bad_json`". With the bound stated, the behaviour is deterministic; the
one-line catch alone would map a *valid* deep clients list (case 4 above) onto `bad_json`, which is only
correct if the contract says so. No fixture nests deeper than 2, so 37/37 is unaffected either way.

---

## SR-4 — Medium — an early-closing consumer produces a traceback and exit 1 (`DIFFER`'s code)

**Surface.** `sys.stdout.write("\n".join(lines) + "\n")` (`:261`) with no handling of `BrokenPipeError`.

**Exploit path.** `mado-geometry.py … | head -c 100`, `| head -1`, or any monitor that stops reading.

**Evidence** (`probe4.log` §L): full run 0.036 s, 1 042 665 B stdout; reader closes after 4 KiB →
```
rc=1  stderr=522 B  'Traceback (most recent call last): … line 417 … sys.exit(main()) …'
```
Same through a shell pipeline (`| head -c 100`): the traceback reaches the caller's stderr.

**Impact.** Medium-low: the tool has already produced the correct lines up to the break, but a consumer
sees exit 1 — the documented `DIFFER` code, i.e. "window was resized" — plus stderr noise that the contract
says is empty for exit 1. A cron/log consumer that treats stderr as failure gets a false alarm; one that
ignores stderr gets a false `DIFFER`.

**Smallest remediation.** Wrap the final write: `try: … except BrokenPipeError: os._exit(rc)`
(`os` is already imported; `os._exit` avoids the interpreter's shutdown flush that re-raises). Contract text
should say a consumer that closes stdout early leaves the exit code unchanged. Fixtures never close stdout,
so 37/37 is unaffected; the source gains no new import.

---

## SR-5 — Low — field-level forgery inside a `MADO_GEOM_CLIENT` line (line-level forging is blocked)

**Surface.** `class` and `address` are attacker-chosen; they are emitted with `json.dumps`
(`:215-222`) inside an unquoted, space-separated `key=value` line whose other fields are fixed.

**What holds (tested, `misc_abc.log` §A).** Line forging is **blocked** by two independent properties:
a class holding any character below U+0020 is dropped before matching (`:39` and `:180-182`), so
`\n`, `\r` never reach a line; and `ensure_ascii` escapes `\u2028`, `\u0085`, so a "line" break cannot be
smuggled in as non-ASCII either. Seven payloads — including the exact summary line
`MADO_GEOMETRY: rules=0 verdict=OK` as a class — produced only `class="…MADO_GEOMETRY: rules=0 verdict=OK"`
inside the client line. The `MADO_GEOM_RULE` line prints `REGEX` raw, but the `SAFE` alphabet has no space,
no `=`, no newline, so that line is unforgeable too.

**What does not.** A class (or address) containing `"` escapes as `\"`, which is correct JSON but leaves a
naive splitter fooled:
```
class = 'x" verdict=DIFFER float_rule=on "'
→ MADO_GEOM_CLIENT: addr="0x1" class="x\" verdict=DIFFER float_rule=on \"" floating=true size=1x2
  want=420x500 float_rule=on verdict=DIFFER
address = '0x1" floating=false verdict=TILED x="'
→ MADO_GEOM_CLIENT: addr="0x1\" floating=false verdict=TILED x=\"" class="gkeep" floating=true …
```
`line.split(" verdict=")[1]` yields the forged value; the true one is later in the line.

**Impact.** Low: no privilege boundary; only a consumer that parses the line without honouring the
`<json>` quoting can be misled into reporting a window as differing/tiled. It matters because C1's whole
output is consumed by humans and scripts.

**Smallest remediation.** Contract-level (tool-level is blocked): the contract already defines `<json>`;
add one sentence — "fields are located left to right with a JSON-quote-aware scanner; a consumer that
splits on spaces may read a class-embedded field". Reordering the line to put `addr=`/`class=` last would
fix it structurally but changes bytes the fixtures pin (`regex0`'s `json-escaped-fields`, `unicode0`), so it
is **not** 37/37-compatible as a tool change.

---

## SR-6 — Low — `--rules`/`--clients` accept any `S_ISREG`, including `/proc`, `/sys` and symlinks (no leak found)

**Surface.** `read_regular` opens with `O_RDONLY|O_NONBLOCK` and gates on `stat.S_ISREG(os.fstat(fd))`
(`:77-95`) — a check on the *file type*, not on the path.

**Evidence** (`misc_abc.log` §C, `probe4.log` §M). Accepted (`rc=4`, read silently, 0 rules):
`/proc/self/environ`, `/proc/self/cmdline`, `/proc/self/stat`, `/proc/self/maps`, a `/sys/...` attribute,
`/etc/passwd`, the tool's own source, `/bin/ls`, and a symlink to `/etc/passwd`. Refused as `unreadable`
(and the FIFO ones return immediately, 0.016 s — the `O_NONBLOCK` guard works): a FIFO, a FIFO **via
symlink**, a unix socket, a symlink loop, `/dev/null`, `/dev/zero`, `/proc/self/mem`, `/proc/kmsg`,
a directory, `/dev/fd/0`, `/proc/self/cwd`, `/etc/shadow` (permissions).

**Impact.** None demonstrated: content surfaces only as parsed rule lines, and `=` is outside the `SAFE`
alphabet, so an `environ`-shaped entry (`NAME=windowrule …`) cannot print; `--clients /proc/self/environ` →
`bad_json` with no content echoed; SETUP messages never echo the path (`SETUP unreadable`, one line). It is
a trust-boundary observation: the tool reads whatever the caller can read, which is the intended contract
for config files, and the counter runs it with `--clearenv`.

**Smallest remediation.** Optional hardening: refuse a path whose `os.path.realpath` starts with `/proc`
or `/sys`. **This is currently blocked by clause g**, which denies any string constant containing `/proc`
(`quality/counters/c1-r42-geometry.py`, `STR_DENY`): the natural fix fails the predicate. A v2 would have
to relax `STR_DENY` for that literal, or accept the current behaviour. No fixture changes.

---

## SR-7 — Low — 4 300-digit integer sizes are legal and printed back

**Surface.** `client_size` accepts any JSON integer `>= 0` (`:168-176`); CPython refuses decimal strings
longer than 4 300 digits, so the boundary is exactly the interpreter's `int` limit.

**Evidence** (`misc_abc.log` §B, §F): 4 300-digit size → accepted, a single client line of ~8.6 KB
(`size=999…`); 4 301 and 5 000 digits → `ValueError` → `SETUP bad_json` (safe). Output amplification is
~1:1 with input (900 000-char class, 1 rule → 900 287 B out, ×1.00), so no blow-up. Comparisons are exact
integers: no overflow, no crash.

**Impact.** Low: log/terminal flooding bounded by ~2× input.

**Smallest remediation.** Optional: the contract could bound `size` at 6 digits (no display exceeds 10⁶ px).
That changes output only for inputs no fixture has (`sizevals0` uses 0..99999, `nan0` 1e2), so 37/37 holds —
but it is a contract edit for a non-issue; leaving it documented is acceptable.

---

## What the review confirms is sound (negative results, all tested)

- **No line-oriented output injection** from `class`/`address`: control chars drop the client; `\u2028`/
  `\u0085` are `ensure_ascii`-escaped; 7 payloads, none produced a `MADO_GEOMETRY:` or a second line (SR-5).
- **No path echo, no content echo** in any SETUP message; a missing/unreadable/oversized input prints only
  the reason word (SR-6).
- **No FIFO wedge**: `O_NONBLOCK` + `S_ISREG` returns `unreadable` in 0.016 s for FIFOs, sockets, loops,
  char devices (SR-6).
- **`bad_json` is checked before any rule parsing**, so a malformed dump cannot make a rule file's content
  observable; `--rules` order is honoured only after the clients input is accepted (`:19-22`).
- **No process, no socket, no dynamic code**: imports are `json os re stat sys`, no `subprocess`, no
  `eval`/`getattr`, no `shell=True` (clause g is true of the artifact).
- **Binary rules files do not crash**: `/bin/ls`, the tool's own source, `/etc/passwd` decode with
  `errors="replace"` → 0 rules, exit 4, 0.015 s.
- **Bounded read loop, exact boundary**: `os.read` in `MAX_BYTES+1-len(data)` chunks. Measured
  (`bound.log`): a clients file of 1 048 575 / 1 048 576 B is read (rc 3), 1 048 577 / 1 048 578 B →
  `SETUP too_large`; the same for a rules file (1 048 575, 1 048 576 read; 1 048 577 → `too_large`) and for
  stdin (1 048 576 read; 1 048 577 → `too_large`).
- **`ensure_ascii` also means the output is pure ASCII**, so no `UnicodeEncodeError` under `LC_ALL=C`.

## Predicate gap (reported post-data)

**Data landed while this review ran**: commit `1959770` ("round-43: data - tools/mado-geometry.py (C1) …"),
`receipts/c1-after-data.txt` → `PRED-C1-r42: fixtures=37/37 tool=present verdict=TARGET_MET rev=1959770…`, and
`tools/mado-geometry.py` is **byte-identical to the artifact reviewed here**
(sha256 `e3c2e471…` for `tools/mado-geometry.py`, the round-42 reference and `SentReDoS/ref-copy.py`). So every
finding above applies to the *landed deliverable*, and per the registration ("a hole it finds is reported as an
open defect of the predicate; no re-registration after data") these are **open defects of `PRED-C1-r42` to be
carried, not a v2 trigger**. The recommendation below is therefore a residual list for the closure and w2.

`PRED-C1-r42` scores 10 `gen` fixtures + 27 named ones (`FIXED`, `c1-r42-geometry.py:779-788`). None of them
has a class longer than 200 B (`regex0`: `"x"*150`), an ambiguous regex, JSON nested deeper than 2, a
consumer that closes stdout, or a `/proc` path. `many0` (20 000 × 300) is the only scale fixture and costs
2.58 s, inside the 30 s `execute` timeout (`:431`). **Therefore the tool as landed carries SR-1, SR-2, SR-3,
SR-4 and SR-6 while scoring `fixtures=37/37 verdict=TARGET_MET`** — the holes are in the contract, not only in
the reference. The hardening proposals are compatible with the score (verified for SR-1's heuristic option and
SR-2's budget; SR-3/SR-4 touch no fixture), so a later round can fix the tool without moving the number, and
the three new fixtures — `depth0` (120 KB nested dump), `redos0` (a supported `(a+)+$` rule with a 40-byte
class under a 5 s timeout), `budget0` (13 × 40 KB × 12 000 rules) — would turn the properties into scored ones
in a future predicate. SR-4/SR-6 need a contract sentence, not a fixture.

## Reproduction

```
S=/fast/scratch/hyaku/mado-r43/SentReDoS; mkdir -p "$S/bin"
# byte-identical probe copy
cp .ufo/waves/round-42/c1/ctl-ref-tool.py.txt "$S/bin/mado-geometry.py"    # sha256 e3c2e471…
printf 'windowrule = size 420 500, match:class (a+)+$\n' > "$S/r.conf"
python3 -c 'import json;print(json.dumps([{"class":"a"*30+"!","size":[420,500],"floating":True}]))' > "$S/c.json"
time python3 -I "$S/bin/mado-geometry.py" --clients "$S/c.json" --rules "$S/r.conf"   # 18.45 s, exit 3
python3 -c 'import sys;sys.stdout.write("["*60000+"]"*60000)' > "$S/deep.json"
python3 -I "$S/bin/mado-geometry.py" --clients "$S/deep.json" --rules "$S/r.conf"     # rc=1, stdout empty, traceback
```
Receipts (this seat): `SentReDoS/probe_redos.log`, `probe_misc_abc.log`, `probe_misc_def.log` (its
amplification rows were superseded by `probe2.log` — those probe files exceeded the 1 MiB cap and were
correctly refused as `too_large`), `probe2.log`, `probe3.log` (its 200 s cap truncated it after §K — the
§L/§M sections are re-run and receipted in `probe4.log`), `probe4.log`, `bound.log`, and the scripts
`probe_redos.py`, `probe_misc.py`, `probe2.py`, `probe3.py`, `probe4.py`.

**Tooling.** Nothing was installed and nothing was upgraded: the host's `python3` 3.14.8 / `re` 2.2.1 were
sufficient; no `pacman`, no `uv`, no `npx`, no network fetch. All work ran under
`/fast/scratch/hyaku/mado-r43/SentReDoS/` (deleted after the receipts were copied); nothing was written
outside this seat's directory in the lane, and no compositor verb was issued (this seat issued none at all
— every measurement is against the files the probes wrote).
