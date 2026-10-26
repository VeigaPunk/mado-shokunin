# SentReDoS — security review of `mado-geometry` (round 43, w1, inline v1)

Full detail, tables and reproduction: `.ufo/waves/round-43/w1/SentReDoS/findings.md`.
Receipts: `.ufo/waves/round-43/w1/SentReDoS/` (`redos.log`, `misc_abc.log`, `misc_def.log`, `probe2.log`,
`probe3.log`, `probe4.log`, `bound.log`, `verify.log`, `verify2.log`, probe scripts, `ref-copy.py`).

**Artifact.** `.ufo/waves/round-42/c1/ctl-ref-tool.py.txt`, sha256 `e3c2e471505932f797a98ee2aa9ab1b04fc919f2140509282ef8472498135a99`;
the **landed** `tools/mado-geometry.py` (commit `1959770`) and the probe copy `ref-copy.py` carry the same hash,
and `--selftest` prints `MADO_GEOMETRY_SELFTEST: 73/73 passed`.
Contract = docstring of `quality/counters/c1-r42-geometry.py` (locators below are that file unless the
reference is named). Host python3 3.14.8, `re` 2.2.1. No compositor verb, no install, no network.

## Ranked

| # | severity | defect | evidence |
|---|---|---|---|
| SR-1 | **High** | catastrophic backtracking is contract-admissible | 31-byte class = 35.66 s; all 4 patterns `rules=1` (supported) |
| SR-2 | **High** | unbounded match work, no ambiguity needed, legal inputs | 13×40 KB × 12 000 rules = **99.3 s** |
| SR-3 | **High** (predicate) / Low (exploit) | 120 KB nested JSON → `RecursionError` escapes → rc 1, empty stdout, traceback | depth 60 000 = crash; 50 000 = clean `bad_json` |
| SR-4 | Medium | early-closing consumer → `BrokenPipeError` traceback, exit 1 (= `DIFFER`'s code) | 1 MB stdout, reader quits at 4 KiB → rc 1, 522 B stderr |
| SR-5 | Low | field-level forgery inside `MADO_GEOM_CLIENT` (line forging is blocked) | `class="x\" verdict=DIFFER … \""` |
| SR-6 | Low | any `S_ISREG` is read (`/proc`, `/sys`, symlinks); no leak found | 6 accepted, 11 refused, no path echo |
| SR-7 | Low | 4 300-digit sizes accepted and echoed (interpreter int limit is 4 301) | 4 300 → line, 4 301 → `bad_json` |

## SR-1 High — ReDoS is inside the contract's own alphabet
`SAFE` (`ctl-ref-tool.py.txt:69`) admits nested quantifiers, quantified overlapping alternations and stacked
wildcards; `regex_ok` (`:120-128`) bans only the possessive forms; `matches` (`:180-183`) runs
`re.fullmatch` on the attacker's class. All of `(a+)+$`, `(a|aa)+$`, `(a*)*b`, `.*.*.*b` are reported as
**supported**, and an app_id of `"a"*30 + "!"` (31 bytes, no control char) costs 18.45 s; 31 bytes = 35.66 s;
+1 char ≈ ×1.9; 1 MiB never returns. One ambiguous rule among 300 costs 0.72 s on 34 bytes. Control
`(a|b)+$` at 100 KB = 0.020 s. Hyprland uses RE2 (linear) — the tool is more fragile than the thing it models.
**Smallest remediation that keeps 37/37:** match the SAFE subset with a linear-time matcher (Thompson NFA;
same accepted language for `fullmatch` on control-char-free classes, no new imports ⇒ clause g holds). Cheap
fallback, verified: static ambiguity rejection (quantifier over a group with a quantifier, over a group whose
alternatives share a first atom, or two `.*`) classifies **54/54 `regex0` entries identically** to the shipped
`regex_ok` and keeps every selftest assertion — but it is a heuristic and changes the documented rule set, so
it is a predicate amendment to carry (data has landed; no re-registration). A class-length cap is not a fix (30 chars is already 18 s).

## SR-2 High — the product clients×rules×length is unbounded
`matches` runs per (client, rule) over the whole class (`:180-183`); no bound on rule count, `--rules`
repetitions, class length, or their product. Measured 2.58 s for the counter's own `many0` shape, then
4.8 / 9.5 / 19.3 s at 300 / 600 / 1200 rules over 26×40 KB classes, and **99.3 s** at 12000 rules — every
input inside the 1 MiB caps (`probe2.log` §G). One 1 MiB rules file holds ~30 800 supported rules → ~17 min
by the measured linear fit. **Remediation:** bound the product before matching (`pairs + Σ len(class) ≤ 5·10⁷`;
all fixtures fit with ≥4× margin, max = `many0` at 1.2·10⁷), reported as a SETUP line — needs one new SETUP
token, to carry with the predicate. Secondary: compile each rule once instead of re-entering `re`'s cache (`:127` discards the object).

## SR-3 High as a predicate defect — a deep dump crashes instead of `SETUP bad_json`
`parse_clients` catches only `(UnicodeDecodeError, ValueError)` (`:162-166`); CPython raises `RecursionError`
(depth ~60 000 here, a stack guard, not the 1000-frame limit). 120 KB of `[`…`]` → **rc 1, empty stdout, 24
stderr lines with the tool's path and source**. A *valid* clients list nested 150 000 deep (900 KB) crashes
too. Violates `:17-18` (one stdout line, exit 2), `:21` (`bad_json`), `:50` (stderr empty on 1/3/4); and rc 1
is `DIFFER`'s documented "report, not a fault" code, so a monitor reads a crash as a size mismatch.
**Remediation:** `except (… , RecursionError)` **plus** a stated nesting bound ("nested deeper than 64 is
bad_json"), because the interpreter's guard is stack-dependent. No fixture nests deeper than 2 ⇒ 37/37 safe.

## SR-4 Medium — broken pipe
`sys.stdout.write(...)` (`:261`) has no `BrokenPipeError` handling: with a 1 MiB stdout and a reader that
quits at 4 KiB, the tool exits 1 with a 522-byte traceback (also through `| head`). **Remediation:**
`try/except BrokenPipeError: os._exit(rc)` (`os` is imported; avoids the shutdown re-raise) + one contract
sentence. Fixtures never close stdout ⇒ 37/37 safe.

## SR-5 Low — field-level forgery (line forging blocked)
Control-char classes are dropped before matching (`:39`) and `ensure_ascii` escapes U+2028/U+0085, so no
payload I tried (7, including the literal summary line as a class) produced a `MADO_GEOMETRY:` or a second
line; the `MADO_GEOM_RULE` line is safe because `SAFE` has no space/`=`/newline. Residual: a class or address
containing `"` becomes `\"`, so `split(" verdict=")` reads a forged value first
(`class="x\" verdict=DIFFER float_rule=on \""`). **Remediation is contract-level only** (consumers must scan
fields with JSON-quote awareness): moving the attacker fields to the end of the line would fix it structurally
but changes bytes the `regex0`/`unicode0` fixtures pin.

## SR-6 Low — `S_ISREG` is a type check, not a path check
`read_regular` (`:77-95`) accepts `/proc/self/{environ,cmdline,stat,maps}`, a `/sys` attribute, `/etc/passwd`,
`/bin/ls` and symlinks to regular files; refuses FIFOs (also via symlink), sockets, loops, `/dev/null`,
`/dev/zero`, `/proc/self/mem`, `/proc/kmsg`, directories, `/dev/fd/0` — all in 0.016 s, and never echoes the
path. No content leak: only parsed rule lines print, and `=` is outside `SAFE`, so an environ-shaped entry
cannot print; `--clients /proc/self/environ` → `bad_json` with nothing echoed. **Hardening is blocked by the
predicate:** the natural fix (refuse realpaths under `/proc`) needs the string `/proc`, which clause g's
`STR_DENY` forbids ⇒ needs a predicate relaxation or acceptance.

## SR-7 Low — 4 300-digit sizes
`client_size` (`:168-176`) accepts any JSON int ≥ 0; the interpreter caps decimal parsing at 4 301 digits, so
4 300 prints (~8.6 KB/line) and 4 301/5 000 → `bad_json`. Output ≈ 1:1 with input (900 000-char class → 900 287 B,
×1.00). No overflow, no crash. Optional 6-digit cap (no fixture reaches it).

## What holds (tested)
No line injection; no path/content echo; no FIFO socket/device wedge; `bad_json` is decided before any rule
file is parsed; exact 1 MiB boundary (1 048 576 read, 1 048 577 → `too_large`, for file, rules and stdin);
binary rules files decode to 0 rules; stdlib-only imports with no `subprocess`/`eval`/`getattr`; output is
pure ASCII (`ensure_ascii`) so no `UnicodeEncodeError` under `LC_ALL=C`.

## Predicate gap (reported post-data)
Data landed while this review ran: commit `1959770`, `receipts/c1-after-data.txt` →
`PRED-C1-r42: fixtures=37/37 tool=present verdict=TARGET_MET`, and **`tools/mado-geometry.py` is
byte-identical to the artifact reviewed here** (sha256 `e3c2e471…` for the landed tool, the round-42
reference and `SentReDoS/ref-copy.py`). So every finding applies to the shipped deliverable; per the
registration ("no re-registration after data") they are **open defects of `PRED-C1-r42` to carry**, not a v2
trigger. `PRED-C1-r42` has 37 fixtures, none with a class >200 B, an ambiguous regex, JSON nested >2, an
early-closed stdout, or a `/proc` path; `many0` (20 000×300, measured 2.58 s) is the only scale case. So the
landed tool carries SR-1, SR-2, SR-3, SR-4 and SR-6 while scoring 37/37. All hardening proposals are
score-compatible (verified for SR-1's heuristic and SR-2's budget; SR-3/SR-4 touch no fixture), so a later
round can fix the tool without moving the number; `depth0` (120 KB nested dump), `redos0` (supported
`(a+)+$`, 40-byte class, 5 s timeout) and `budget0` (13 × 40 KB × 12 000 rules) would make the properties
scored. SR-4/SR-6 need contract sentences, not fixtures.

## Verification of this report
`SentReDoS/verify.log` greps the receipts for **every** number and quoted output line used above:
**34/34 PASS**. (My first pass of that grep reported 25/27 because two patterns were wrong — a two-line log
record and a section that is filed in `misc_def.log` — not because a measurement was wrong; `verify2.log`
records that diagnosis.) Scratch `/fast/scratch/hyaku/mado-r43/SentReDoS/` removed after the receipts were
copied; nothing outside this seat's directory was written, and no compositor verb was issued.
