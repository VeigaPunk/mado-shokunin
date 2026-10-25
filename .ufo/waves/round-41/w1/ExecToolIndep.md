# ExecToolIndep — C1 differential implementation (round 41, w1)

Lane `mado-shokunin`, freeze commit `60c3914154333180450d5da27ba222d5763cc56a` (base
`ab2bfaab661c846d1de9d58c01651cd156a13949`), host 2026-10-25.

**Verdict: the contract text of `PRED-C1-r41-v1` is implementable from the docstring alone.**
A tool written from the docstring only — `/home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c1-r41-globals.py:2-109`
was the only source, `c1/ctl-ref-tool.py.txt` was never opened — scores
`fixtures=24/24 tool=present verdict=TARGET_MET` under four independent nonces, with
`selftest=57/57` and `clause=b2 killed=6/6`, and disagrees with the judge's `model_out` on
none of 600 random journals and none of 168 crafted edge comparisons.

## Deliverable

`.ufo/waves/round-41/w1/ExecToolIndep/mado-globals.py` — 529 lines, stdlib only
(`argparse os re shutil stat subprocess sys`), sha256
`7d9103ebc9259b3bfe3066be2781a79c24cc20a3e4070276adc6c65b43fbf360`, mode 0755.

Structure: `split_lines` (byte lines, non-UTF-8 line dropped whole) → `parse_sessions`
(session split on first-advert / boot-since-last-advert / pid change; per name count + max
ver) → `classify` (fixed table, else `other`) → `diff_line` / `render_report` (session lines,
latest-session globals sorted bytewise, diff, final verdict line) with `read_file` /
`resolve_prog` / `live_env` / `live_journal` behind them, and `selftest` as the teeth carrier.

Not installed anywhere: `tools/mado-globals.py` is the L1's integration step. Everything
below scores the seat copy via `--tool`.

## Scoring (frozen counter, unchanged, four nonces)

    cd /home/vgpnk/Projects/shokunin/mado-shokunin && \
      python3 -I quality/counters/c1-r41-globals.py --repo . \
        --rev 60c3914154333180450d5da27ba222d5763cc56a \
        --tool .ufo/waves/round-41/w1/ExecToolIndep/mado-globals.py

| nonce | fixtures | clauses | b2 | verdict |
|---|---|---|---|---|
| `d2e40f8e3b223384` | 24/24 | a:1 b:1 b2:1 g:1 | sites=19 killed=6/6 | TARGET_MET, exit 0 |
| `8df4c2fda19ad6c6` | 24/24 | a:1 b:1 b2:1 g:1 | sites=19 killed=6/6 | TARGET_MET, exit 0 |
| `9148dba585c89b3a` | 24/24 | a:1 b:1 b2:1 g:1 | sites=19 killed=6/6 | TARGET_MET, exit 0 |
| `56ba68918bb779c9` | 24/24 | a:1 b:1 b2:1 g:1 | sites=19 killed=6/6 | TARGET_MET, exit 0 |

**Failing fixture lines: none.** All 24 (`gen0..gen7`, `diff0`, `diff1`, `expect0`,
`expectmiss0`, `nosess0`, `nosess1`, `unreadable0`, `usage0`, `badexpect0`, `toolarge0`,
`live0`, `live1`, `livefail0`, `liveenv0`, `livewritable0`, `livelarge0`) print `ok=1 ok`.
So there is no fixture whose byte-exact expectation the contract text does not determine:
the docstring's every ordering, spacing and exit-code claim is sufficient.

## Teeth (mine, exhaustive — the predicate only samples 6)

`.ufo/waves/round-41/w1/ExecToolIndep/teeth-sweep.py`: enumerate the comparison sites the
contract defines (functions not named `*selftest*`, `*_check*`, `*_run*`, `*_write*`, `main`,
`usage`), flip each, run `--selftest` on the copy.

    baseline rc=0 MADO_GLOBALS_SELFTEST: 57/57 passed sites=19
    TEETH SWEEP: sites=19 killed=19 survived=0

Killed examples: `parse_sessions:112 cur['pid'] != pid` → 46/57; `render_report:205 k == 0`
→ 47/57; `valid_name:138` → 50/57; `over_cap:142` → 55/57; `failed:146` → 55/57;
`diff_line:162/163/169` → 56/57; `render_report:204` → 54/57; the seven
`is None` / `is not None` sites and the two remaining membership/size sites die with a
traceback (no summary). The selftest is 57 assertions over `classify` (all 21 table
names + 2 non-members), `valid_name`, `over_cap`/`failed` boundaries, and exact rendered
census text for plain / pid-split / boot-split / boot-precedence / trailing-boot / noise /
invalid-UTF-8 / 3-session-diff / 1-session-diff / 0-session-diff / expect-present /
expect-missing-deduped / NO_SESSIONS-wins / classes-csv cases.

Note (finding about the clause text, not the counter): `sites=19` counts one site the
contract's exclusion list does **not** remove — the `check` closure inside `selftest`
(`mado-globals.py:299 got == want`), because the exclusion is `*_check*` and a bare `check`
has no leading underscore. Flipping it is caught anyway (`0/57 passed`). Nothing is lost,
but the exclusion list is narrower than "the selftest's own assertions".

## Differential vs the judge's model (300 + 300 journals, plus 168 edge comparisons)

`.ufo/waves/round-41/w1/ExecToolIndep/diff-300.py` imports the counter with `importlib`
(black box: `gen_fixture`, `advert`, `ts_of`, `noise_lines`, `TABLE`, `model_out`), builds
100 lattice journals from the judge's own generator across fresh nonces plus 200 random
journals of my own (boot lines, pid runs and reuse, 128/129-char names, 6/7-digit versions,
one/three-space gaps, CR endings, bad timestamps, other programs, unknown names, empty
journals, injected invalid bytes), and compares `(stdout, code)` with `model_out`.

    seed 20261025: DIFFERENTIAL: journals=300 judged=278 skipped_nonutf8=22 disagreements=0
    seed        7: DIFFERENTIAL: journals=300 judged=277 skipped_nonutf8=23 disagreements=0

`.ufo/waves/round-41/w1/ExecToolIndep/probe-edges.py` — 42 crafted cases × (diff, no-diff) ×
(two `--expect` sets) = 168 comparisons: leading-zero pid and version, six/seven-digit
version, 128 vs 129-char name, one/three-space and tab gaps after `[LOG]`, trailing space,
trailing CR, leading space, timestamps without offset / `Z` / one-digit month / offset
without colon / short offset / out-of-range-but-regex-valid, host with `:` and brackets,
other program, other level, no level, boot lines of 31/32/33 hex chars, uppercase hex,
trailing space, two boots before one advert, boot between same-pid adverts, boot then two
adverts, boot-only, empty, blank lines, pid alternation, version drop, version repeat, every
table name plus an unknown, two-session diff.

    EDGE PROBE: cases=42 comparisons=168 disagreements=0

**Disagreement list: empty.** The only divergence I can construct at all is the bucket the
judge cannot express:

- **Non-UTF-8 bytes inside a would-be advert line.** `model_out` takes `str` and splits on a
  `str` newline (`c1-r41-globals.py:254 for line in text.split("\n")`), so it never sees the
  bytes; decode-with-replacement turns `hst\xff\xfe` into `hs\ufffd\ufffdt`, which `\S+`
  accepts, and the model counts an advert. My tool drops the whole line. Decided by the
  contract sentence *"every other line (… bytes that are not UTF-8) is ignored"*
  (`c1-r41-globals.py:32`): the line is ignored, which is my behaviour. Latent only —
  across 200 generated fixtures the judge's journals carry **0** `U+FFFD` (probe:
  `fixtures=200 carrying U+FFFD=0`), and all 24 byte-exact fixtures pass with the strict
  per-line drop, so the counter never feeds its model a case that decides this.

## Contract decisions I had to take (each one is a place the text was load-bearing)

| decision | contract sentence | how it was settled |
|---|---|---|
| the `--diff` line sits **after** the `MADO_GLOBAL` lines, **before** the final line | `c1-r41-globals.py:39-45` "Output, in order" | `diff0`/`diff1` pass byte-exactly |
| `ver` is the **max** seen, not the last | `:37` "per distinct NAME: count and ver = the highest N seen" | `gen4` (conflicting versions) passes; selftest `wl_seat 9,7 → ver=9` |
| boot flag clears at each advert (a boot splits only the *next* advert) | `:33-34` "a SESSION starts … a BOOT line occurred since the previous ADVERT" | `gen6`, selftest boot-then-two-adverts |
| `classes=` counts distinct names of the latest session, sorted by class | `:45` "classes=<class:n csv sorted by class|->" | `gen5` (every table name) passes |
| `expected_missing` sorted **and deduped** | `:45` "expected_missing=<csv sorted, deduped|->" | `expectmiss0` passes; selftest `("nope","nope","aaa") → aaa,nope` |
| `NO_SESSIONS` beats `MISSING_EXPECTED` | `:47` "NO_SESSIONS wins over MISSING_EXPECTED" | `nosess0` passes |
| exactly 8388608 bytes is **not** too large | `:23` "larger than 8 MiB (8388608 bytes) is too_large" | host probe: 8 MiB → `sessions=0 … verdict=NO_SESSIONS` rc=3; 8 MiB+1 → `SETUP too_large` rc=2 |
| a bad NAME is reported before the journal is parsed | `:20` "a NAME must fully match [A-Za-z0-9_]{1,128}. Setup failure … bad_expect" | `badexpect0` passes (its journal is a *readable* `b"x\n"`, `:612`); the contract does **not** order `bad_expect` against `unreadable` — my tool validates names first, and no fixture decides it |
| `--journal-file` must start no process | `:71-72` "In --journal-file mode the tool must not start any process" | `live*` stubs; my own check: PATH-stub `journalctl` with a `touch` payload, `--journal-file` run → `NO_SPAWN` |
| `--live` stdin must be `/dev/null`, not a pipe | `:65` "stdin /dev/null (an open pipe is a violation)" | `liveenv0` passes (canary + stdin checked by the stub) |
| the `--live` timeout value is unspecified | `:67` "a … timeout is SETUP journalctl_failed" | chose 120 s (`mado-globals.py:36`); declared residual, no fixture exercises it |

## Host receipts (reported, not scored)

1. **Real journal bytes.** `python3 -I mado-globals.py --journal-file .ufo/waves/round-41/fetch/xdph-journal.txt --expect hyprland_focus_grab_manager_v1 --expect wl_seat`
   (file sha256 `bf8fa91a321197277cf9c1260d17524e9ddf862f7f76ddf440fc057aa600aaf7`, 153 lines)
   → rc=0, `sessions=2`, session 1 `pid=1918 adverts=15`, session 2
   `boot=7ab69ee4149c4811a3faf6c08c9d119b pid=1952 first=2026-10-25T13:36:24-03:00 last=2026-10-25T13:36:24-03:00 interfaces=63 adverts=63`,
   `MADO_GLOBAL: name=hyprland_focus_grab_manager_v1 ver=1 count=1 class=focus-grab`,
   `classes=capture:2,clipboard:3,focus-grab:1,idle:2,input-capture:3,input-synthesis:3,other:38,output-control:4,sandbox:1,session-lock:2,toplevel-control:4`.
   This reproduces the L1's provisional census independently (2 sessions, 15+63 = 78
   adverts, 63 distinct globals in the latest session, one focus-grab advert at
   13:36:24 pid 1952) from the bytes, without reading any C2 artifact.
2. **Live, on the running desktop** — only the allowlisted journal verb
   (`journalctl --user -u xdg-desktop-portal-hyprland --no-pager -o short-iso`, no
   compositor socket, no input):
   `python3 -I mado-globals.py --live --diff` → rc=0, `sessions=2 latest_pid=1952
   interfaces=63 … verdict=OK`, and
   `MADO_GLOBALS_DIFF: from=1 to=2 added=<…>` listing the 63 globals the second portal
   session saw that the first did not (session 1 had 15). No `removed`, no `ver_changed`
   for the names present in both.

## CLI boundary probes (host, my own)

`neither flag`, `both flags`, `--journalctl` without `--live`, `--exp` (abbreviated) →
`SETUP usage` rc=2. `--expect` of 129 chars, `--expect=`, `--expect "a b"` →
`SETUP bad_expect` rc=2. Missing file and a directory → `SETUP unreadable` rc=2. 8 MiB → rc=3
census; 8 MiB+1 → `SETUP too_large` rc=2. `--live --journalctl <dir>` →
`SETUP journalctl_unusable` rc=5. `--selftest --bogus` → `SETUP usage` rc=2 (flags are parsed
before `--selftest` is honoured; the contract is silent here, and the counter only ever runs
`--selftest` alone).

## Findings

- **Supports** the claim's target: an implementation derived from the docstring alone reaches
  `24/24` on the first scoring attempt, so `PRED-C1-r41-v1`'s fixture set does not smuggle in
  behaviour the text leaves undetermined. `quality/counters/c1-r41-globals.py:2-109` is a
  complete specification of the observable surface.
- **Attacks** nothing in the counter. Two observations worth the L1's attention:
  1. the clause-b2 exclusion list (`:91-93`) misses a bare `check` helper, so a nested
     assertion closure counts as a mutation site (harmless here: killed);
  2. `model_out` is a `str` model, so the non-UTF-8 rule of `:32` is unrepresentable in
     it. A future fixture that puts invalid bytes inside a host field would make the model
     and a contract-faithful tool disagree; today no fixture does (0 `U+FFFD` in 200
     generated journals).
- **Residuals unchanged**: the `--live` timeout is unexercised; the host receipt is reported,
  not scored; a tool that embeds the table is still an implementation (mine does, by
  necessity — the table *is* the contract).

## Risks / blockers

None. No lane file was modified (the seat wrote only inside
`.ufo/waves/round-41/w1/ExecToolIndep/`); no git/jj mutation; no pacman; no compositor
socket; the only journal access was read-only `journalctl --user -u <unit> --no-pager -o
short-iso`; the only `hyprctl` was none.

## Tooling

Nothing installed: the tool and all three harnesses are stdlib Python 3.14.8; `bwrap`
(`/usr/bin/bwrap`) was already present, so the counter's sandbox clause ran.

## Retained artifacts

| path | what |
|---|---|
| `.ufo/waves/round-41/w1/ExecToolIndep/mado-globals.py` | the deliverable (`sha256 7d9103eb…f360`) |
| `.ufo/waves/round-41/w1/ExecToolIndep/diff-300.py` | 600-journal differential (`python3 -I diff-300.py [seed]`) |
| `.ufo/waves/round-41/w1/ExecToolIndep/probe-edges.py` | 168 crafted edge comparisons |
| `.ufo/waves/round-41/w1/ExecToolIndep/teeth-sweep.py` | exhaustive 19/19 site flip sweep |
| `.ufo/waves/round-41/w1/ExecToolIndep/Report.md` | initial status stub (superseded by this file) |
