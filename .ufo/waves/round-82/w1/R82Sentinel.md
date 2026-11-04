# R82Sentinel — security review of the round-82 bytes

Read-only seat. Nothing under the lane was written except this file; every experiment ran under
`/fast/scratch/hyaku/mado-r82/R82Sentinel/`. No tool was installed; no git/jj mutation was run.

## Snapshot under review

| item | value |
|---|---|
| scan start | 2026-11-04T10:29Z, lane HEAD `b6146ee6` |
| scan end | 2026-11-04T13:31Z, lane HEAD `3ec7fb75` (the scribe commit landed mid-scan) |
| base | `6ea2386d49318a5f223097c78b5fe79c31b064f8` |
| files changed base..HEAD | 32 (`git diff --name-status 6ea2386d..HEAD`) |
| files under `.ufo/waves/round-82/` | 66 |

Frozen instruments, re-hashed in the working tree **and** at `3ec7fb75`; all five are byte-equal,
so no seat rewrote one:

| instrument | sha256 (both) |
|---|---|
| `tools/mado-barfoot.py` | `380075284d7d5c6f56a82600935d512def617223be27f33241ff5dbcb0bcab59` |
| `quality/counters/c1-r82-allocation-band.py` | `1e9f394df80284e78f1fdf3f24cb5e14d1e4091f4880ccc60a2a45060b54612d` |
| `quality/counters/c2-r82-runbook.py` | `1e8eb49928bfc9b8e5e1e72da74c0496cbe6d095fe3fdc72c479fffd80b3fb0f` |
| `.ufo/waves/round-82/controls/c1-cases-r82.json` | `e404bb3fa93d5f12338129adc8733574084e6fab2ee12fbb471dd45df94a315f` |
| `.ufo/waves/round-82/controls/c2-runbook-cases-r82.json` | `f64d7d5db40fc1da3d75c15315274264dfb53c38396135b978dff7b0b04b36d5` |

Method: the seat's regex over the round directory **and** the two counters, then (so pre-existing
content is not re-reported as new) the *added lines only* of the other changed files
(`git diff -U0 base..HEAD` filtered to `^+`), plus a second search for the identifier classes the
regex cannot see (account name, D-Bus unique names, UID-derived units, live PIDs).

---

## 1. Credential / identifier scan

### 1a. Result: no credential material

Zero hits for `BEGIN … PRIVATE KEY`, `ghp_`, `github_pat_`, `sk-…`, `AKIA…`, `xox[baprs]-`,
`client_secret`, `refresh_token`, `Authorization:`, or `SERVICE_ROLE` anywhere in the changed set.
Zero UUID-shaped, MAC-shaped or EDID-preamble (`00ffffffffffff00`) strings. Zero setuid/world-writable
files (all `644`, the two generators `755`).

### 1b. The 61 regex hits, classified

| file:line | token | class |
|---|---|---|
| `.ufo/waves/round-82/fetch/S481.xml:29,37,40,62,77,84,95,99,104,120,123,134,140,148,153,186,191,199,207,213,216,224,227,244,247,265,270,283,288,296,301,305,317,318,322,324,328,349,356,362,383,387,394,403` | `description` | **field name** — the wlr-layer-shell protocol XML's own `<description>` element |
| `…/fetch/S481.xml:305,318,332,350` | `serial` | **field name** — the protocol's `ack_configure` serial argument |
| `…/fetch/S481.xml:242` | `password` | **prose** — "a lock screen or a password" in the protocol's keyboard-interactivity text |
| `quality/counters/c2-r82-runbook.py:457` | `serial`, `description` | **redaction rationale** — the `observed()` docstring that *forbids* quoting a JSON dump |
| `.ufo/waves/round-82/w1/R82ScoutLive/hyprctl-monitors-redacted.json:5,8` (+`make`,`model`) | `description`, `serial` | **redaction** — `"<redacted: description>"`, `"<redacted: serial>"`; values are gone |
| `.ufo/waves/round-82/w1/R82ExecC2Run.md:16,42` | `/home/v` | **lane path** — `cd /home/vgpnk/…/mado-shokunin` |
| `.ufo/waves/round-82/w1.ready:5` | `/home/v` | **lane path** — dispatch file path |
| `.ufo/waves/round-82/receipts/census-start-r82.txt:3` | `/home/v` | **lane path** — `…/mado-shokunin/corpus/SOURCES.md` |
| `.ufo/waves/round-82/claims-declaration-r82.md:118` | `/home/v` | **fleet path** — `sources-census.sh … --root /home/vgpnk/Projects/shokunin` |
| `.ufo/waves/round-82/w1-spec.json:4,9,14,19,24,29,34,39,44,49,54,59,64,69,74` | `/home/v`, `serial`, `token`, `EDID`, `password`, `Bearer`, `secret` | **prompt/context text** — the wave's own rules and task prompts; every `/home/…` is a lane path, every keyword is a rule word ("monitor `description`/`serial`/`make`/`model`"), plus one false positive: `serialize` at line 27 of the generator matches `serial` |
| `.ufo/waves/round-82/w1-dispatch.json:4,131,136,141,146,151,156,161,166,171,176,181,186,200,205,210,215,220,225,230,235,240,245,250,255,260,265,270` | same | **prompt/context text**, the same bytes committed a second time (context at `:4` and again at `:200`) |
| `.ufo/waves/round-82/make-spec-r82.py:13,57,58,62,69,72,111,129,329,330,331` | `serial`, `description`, `token`, `EDID`, `password`, `Bearer`, `/home/v` | **generator constants + embedded prompt text**; `:27` is `serialize` (false positive) |
| `corpus/knowledge/bar-footprint-allocation-r82.md:23` | `serial` | **field name** — `set_size(serial, width, height)` |
| `corpus/lessons/round-82.md:26,27,38` | `/home/v` | **fleet path** — `/home/vgpnk/Projects/shokunin` and `/home/vgpnk/Projects/shokuknow/merge/mado/` |
| `.ufo/waves/round-82/controls/c2-runbook-cases-r82.json:1003` | `DESCRIPTION` | **column header** inside a fixture — see F1, this line is also a leak |

`c1-cases-r82.json`, `make-c1-cases-r82.py`, the receipts (other than the census line) and
`tools/mado-barfoot.py` carry **no** hit of any kind.

### 1c. The identifier class the regex misses — see finding **F1**

`vgpnk`, `:1.56`, `:1.9`, `user@1000.service` and the live waybar PID `1720` appear in six lines of
the frozen C2 control set. They are not matched by the seat's regex (no `serial|description|…`
token), and they are exactly the "session id" class the wave's redaction rule names.

### 1d. The tool does not launder identity fields into its output

Probed with a synthetic monitor carrying `"description":"SECRET-EDID-XYZ","serial":"SER123",
"make":"ACME","model":"Z9"`: no `DECL`/`LIVE`/`RESULT` line echoed any of them (the tool reads only
`name`, `width`, `height`, `scale`, `transform`, `reserved` — `mado-barfoot.py:779,881,982,1029`).

---

## 2. The three new commands are read-only — **confirmed**

The verbs, from `busctl --help` (systemd 262.1), whose first line is "Introspect the D-Bus IPC bus":

```
  [list]                           List bus names
  tree / introspect / status       (read)
  call / emit / set-property       (mutating; present in the verb table)
  monitor / capture / wait         (long-running / passive)
```

`man busctl` is explicit for the two verbs used:
`introspect SERVICE OBJECT [INTERFACE]` — "Show interfaces, methods, properties and signals of the
specified object"; `list` — "List bus names". Neither opens a transaction and neither has a
mutation operand.

The frozen argv (`c2-runbook-cases-r82.json`) are:

| case | argv |
|---|---|
| `tray-owner` | `["busctl","--user","list"]` |
| `tray-interface` | `["busctl","--user","introspect","org.kde.StatusNotifierWatcher","/StatusNotifierWatcher","--no-pager"]` |
| `tray-methods` | `["/bin/sh","-c","busctl --user introspect … --no-pager \| awk '$2==\"method\"'"]` |

`grep` for `call`/`set-property`/`emit` over the whole control set returns **none**; the only
`busctl` strings anywhere in the frozen bytes are those three (verified with
`grep -oE 'busctl [^|\\"]*'`). The `awk` row re-uses the `introspect` verb; `--no-pager` only
suppresses a pager. `busctl --user` connects to the session bus and performs no write.

Belt to that brace: `c2-r82-runbook.py:686-688` refuses a case whose executed command is not
character-identical to the committed `SKILL.md` cell (`documented`), so the executed bytes and the
reviewed bytes are the same bytes. The three new cells are `SKILL.md:274-276`.

---

## 3. Allocation parser input handling — **confirmed sound**

`tools/mado-barfoot.py:436-453` (`parse_allocation`), fed through `read_bytes` (`:149-172`) — the
same loader as `--config`. The path is caller-supplied and opaque: it is never joined to a root, so
there is no traversal surface, and `O_NOFOLLOW` refuses a symlinked input.

| property | code | executed probe (scratch) | result |
|---|---|---|---|
| size limit | `MAX_BYTES = 1048576`, `:153-155` (stdin) and `:166-167` (file) | 1.1 MB file | `ERROR (stage=setup file exceeds 1048576 bytes)` |
| non-regular | `:161-162` `S_ISREG` | symlink to a good file | `ERROR (stage=setup unreadable path … Too many levels of symbolic links)` |
| non-object | `:442-443` | `[34]` | `ERROR (stage=setup the allocation declaration is not an object …)` |
| key type | `:446-447` | `{"": 34}` path | refuses an empty namespace |
| value type | `:448-449`, bool rejected explicitly | `{"waybar":"x"}`, `{"waybar":true}` | `is not an integer` (both) |
| negative | `:450-451` | `{"waybar":-1}` | `the allocation for 'waybar' is negative` |
| unknown namespace | `:769-773`, `:962-965` | `{"zzz":34}` | `names 'zzz', which the composition does not carry` |
| zero band | `:461-471` | `{"waybar":0}` on `height:0` | `stage=model … a zero band reserves nothing` (rc 3, not a guess) |
| shell | — | `grep -nE 'shell\s*=\s*True\|os\.system\|os\.popen\|eval\(\|exec\('` over the tool and both counters | **none** |

The map is only ever consulted on the band axis (`:481-482`), so a cross-axis entry cannot move a
box; a positive declaration still wins over the allocation (`:461-462`, selftest `:1496-1499`).

Residual (not a defect, see O4): `fstat` then `read()` leaves a grow-between window in which a file
can exceed `MAX_BYTES`. Irrelevant for a local read-only diagnostic; worth one `fh.read(MAX_BYTES+1)`
if the limit is ever meant as a hard bound.

---

## 4. Seats vs the lane's git/jj state

**The prohibition is present and unambiguous.** `w1-spec.json:4` (and the same text again at
`w1-dispatch.json:4` and `:200`):

> "You never commit, push, or run a mutating git/jj command, in the lane or anywhere. Read-only git
> (`show`, `log`, `diff`, `rev-parse`, `ls-tree`) is fine."

**No seat prompt asks for one.** `grep -rnoE 'git (add|commit|push|checkout|reset|clean)|jj
(commit|describe|new|bookmark)|gh pr'` over the whole round directory returns **zero** hits. The
only VCS verbs any prompt names are `git -C <lane> diff` (ScoutModel, CriticClaims), `git -C <lane>
show` (ExecMutants, MutRunbook), and `rev-parse` (both counters). Both counters shell out only
`git show` and `git rev-parse` — verified by listing every argv literal in them; no `add`, `commit`,
`push`, `checkout`, `stash`, `reset`, `gc`, `update-ref`, `tag` or `jj` token exists.

**Paths that could reach the state, and their limits:**

| path | reach | guard |
|---|---|---|
| every prompt's `git -C <lane> …` | reads objects/refs | read-only verbs only; the prohibition covers the rest |
| `git clone --shared <lane> <scratch>/repo` (context rule) | creates an independent `.git` whose alternates point at the lane's object store | alternates are read-only; a commit in the clone cannot write the lane |
| counters' `--repo .` | `git show`/`rev-parse` only | no writer verb |
| counters' `--scratch-root` | `makedirs` + `mkdtemp` + `rmtree` **anywhere** except `/` and a symlinked root (`c1:418-419`, `c2:625-631`) | **not constrained to scratch** — see O1 |
| C2 child `TMPDIR` | every case runs with `cwd = repo`, and `run()` sets `TMPDIR = cwd` | **points at the lane** — see F2 |
| three scribe prompts | write `corpus/knowledge/…`, `corpus/lessons/…`, `.ufo/waves/round-82/fetch/…` — lane paths outside the seat dir | contradicts the absolute rule's "write only inside your seat directory" — see O7 |

**Verdict for this item:** no seat can *mint* a commit or move a ref — the only lever that could is
an explicit `git commit`/`jj` invocation, which no prompt contains and the shared context forbids.
What two instrument paths *can* still do is place files in the measured working tree that a later
blanket `git add -A` would sweep (F2, O1). That is the residual, and it is a write-path finding,
not a "seat committed" finding. Present state: clean — `git status --porcelain` after the measured
receipts shows only the expected `M LOG.md`, `M SCORECARD.md`, `?? .ufo/waves/round-82/w1/`,
`?? harm-watch-r82.txt`, `?? w1.ready.dispatched`; no temp-shaped residue.

---

## Findings

### F1 — account name and session-scoped bus names are baked into the frozen C2 control set

- **Severity:** low (no credential; marginal disclosure near zero — see impact).
- **Exploit path:** none direct. The strings are inert fixture data compared against their own
  `{rc, out}` pair (`case_correct` → `special_matches`), never against the live bus, so they cannot
  be used to match or forge anything. The exposure is that they are committed and survive in the
  proof artifact the claim rests on.
- **Evidence:**
  - `.ufo/waves/round-82/controls/c2-runbook-cases-r82.json:981,985,989,993,999,1003` — `vgpnk`
    (USER column), `:1.56` / `:1.9` (D-Bus unique connection names), `user@1000.service` (UID 1000),
    and the live waybar PID `1720` (the same PID the C2 receipt reports at `waybar-process`).
  - `.ufo/waves/round-82/controls/make-c2-cases-r82.py:38-46` — the literal that authored them.
  - `.ufo/waves/round-82/w1/R82MutRunbook/controls-double-bind.json:981-1003` — a seat's copy, so
    the strings are duplicated inside the lane.
  - Not carried: `.ufo/waves/round-81/controls/c2-runbook-cases-r81.json` has **0** occurrences.
    Round 82 introduces this.
  - The live box reproduces the shape exactly: `busctl --user list` here prints `vgpnk` and
    `user@1000.service` in those two columns, so the fixture is a plausible *capture*, not a shape.
- **Impact:** the wave's own rule (`w1-spec.json:69` / `make-spec-r82.py:69`) says "Redact before
  saving any capture: … any token, **session id** or home path outside the lane tree. **Shape-only
  harness captures are the rule.**" A D-Bus unique name is the session's identifier; `vgpnk` is the
  OS account. The counter itself states the discipline it did not apply to its own fixture
  (`c2-r82-runbook.py:457`: "Never quote a JSON dump: a monitors reply carries the output's
  serial/description"). Mitigating: `vgpnk` is already committed throughout the lane
  (`SKILL.md` ×6, `SCORECARD.md` ×25, `LOG.md` ×4, `corpus/SOURCES.md` ×6 — all pre-existing), so
  the marginal disclosure is ~nil. This is a rule-conformance defect, **not** a disclosure of
  anything the repo did not already carry, and it does not weaken C2's 29/29 or 25/25.
- **Smallest remediation:** in `make-c2-cases-r82.py` and the frozen set, `vgpnk` → `user`,
  `:1.56`/`:1.9` → `:1.42`, `user@1000.service` → `user@<uid>.service`, `1720` → a synthetic PID.
  The three matchers (`regex` on the PID column, `regex` on the interface line, `lines_shape` on
  `.Name method`) are indifferent to every one of those substitutions. Because it edits a frozen
  instrument it changes the control sha256 `f64d7d5d…` and the C2 receipt, so it needs an L1
  re-freeze decision — this seat did not touch it.

### F2 — `TMPDIR` is pinned to the lane root, not the scratch root (comment and code disagree)

- **Severity:** low; latent today, structural for every future row.
- **Exploit path:** `quality/counters/c2-r82-runbook.py:170` sets `env["TMPDIR"] = cwd`; the case
  loop at `:697` calls `run(case["argv"], repo)` with `cwd = repo = os.path.abspath(args.repo)` —
  i.e. the lane root when invoked with `--repo .`. Every one of the 29 children therefore gets
  `TMPDIR=/home/vgpnk/Projects/shokunin/mado-shokunin`, a writable temp directory inside the
  measured working tree. The mutant sub-runs inherit the same (`:722`, `cwd = repo`). The comment at
  `:162` claims the opposite: "TMPDIR is pinned inside the scratch root so no child can land in
  /tmp."
- **Evidence:** the three lines above; C1 has the same shape but only for `git rev-parse`
  (`c1-r82-allocation-band.py:165` with `resolve()` (`:389`) calling `run([...], repo)` (`:390`)), where git does not
  use `TMPDIR`. Empirically, nothing in the frozen 29 writes to `TMPDIR` today — I ran
  `omarchy menu keybindings --print` with `TMPDIR` pointed at an empty scratch dir and it created
  nothing, and `/home/vgpnk/.local/share/omarchy/bin/omarchy` contains no `mktemp`/`TMPDIR`/`/tmp`
  reference. The measured receipts left no residue (`git status` above).
- **Impact:** a future row, or any child that calls `mktemp`/`mkstemp`/`tempfile`, drops its file in
  the lane root; the integrator's blanket `git add -A` then sweeps it into the round's commit. It
  also silently breaks the wave's "write only in your scratch dir" rule at the one place the counter
  believes it is enforcing it. No effect on today's counts.
- **Smallest remediation:** give `run()` the scratch root separately — `def run(argv, cwd,
  timeout=120, tmpdir=None)` and `env["TMPDIR"] = tmpdir or cwd`; pass `workroot` at `:697` and
  `:722`. Same one-line shape for `c1-r82-allocation-band.py`'s `resolve()`. This does not change
  any matcher or count.

---

## Observations (not defects; for the L1 / other seats)

- **O1** Both counters accept the lane itself as `--scratch-root` (they refuse only `/` and a
  symlinked root: `c1:418-419`, `c2:625-631`). With `--scratch-root .` a run creates and removes a
  directory inside the measured tree. Only the spec ("into your scratch root") keeps that from
  happening; a `realpath(root) != realpath(repo)` refusal would make it structural. Same class as F2.
- **O2** `c2-r82-runbook.py:686` treats *any* `["/bin/sh", …]` argv as documented-by-`argv[2]`
  without requiring `argv[1] == "-c"`. Not reachable with the frozen set (sha256 pinned; every sh
  argv is exactly `["/bin/sh","-c",<doc cell>]`), but the binding check is weaker than it reads.
- **O3** `--no-mutants` yields `verdict=TARGET_MET` with `mutants=0 killed=0` — transparent in the
  output and necessary for the mutant sub-runs, but it means an unwary caller can print the target
  without the 25 kills. The measured receipt (which carries them) is the counter-evidence.
- **O4** `read_bytes` is `fstat`-then-`read` (`:166` then `:169`); a file that grows in between
  exceeds `MAX_BYTES`. Benign for a local CLI; one `read(MAX_BYTES+1)` closes it.
- **O5** `band_of` puts no upper bound on the allocation: a band larger than the monitor is modelled,
  not refused. That is a modelling choice, not a security issue — flagged for `R82ReviewerC1`'s
  "allocation larger than the monitor" probe, not judged here.
- **O6** `/home/vgpnk/…` is committed in the round's operational documents (`claims:118` — the fleet
  root; `corpus/lessons/round-82.md:26,27,38` — the fleet root and `shokuknow`;
  `receipts/census-start-r82.txt:3` — a lane path; `w1.ready:5`; the spec/dispatch prompt text).
  The redaction rule is written for *captures*, and lane-internal paths are explicitly allowed, so
  these are not violations; they are an account-name/cwd disclosure only, and `vgpnk` is already
  all over the committed lane. If a later round wants strict shape-only, keep prompt paths
  lane-relative and say so in the rule.
- **O7** Three seat prompts instruct writes outside the seat directory (`w1-spec.json:39`
  `corpus/knowledge/…`, `:49` `corpus/lessons/…`, `:44` `.ufo/waves/round-82/fetch/…`), which
  contradicts the shared rule "Write only inside your own seat directory … and your own scratch
  dir". The specific prompt wins in practice, so nothing was violated, but the rule text and the
  prompts should be reconciled by the L1.
- **O8** The C2 receipt publishes `Hyprland 0.56.2 … at commit efb5099…` and `DP-1
  3440x1440@99.997`. Upstream version and a connector name — shape-only, no serial/EDID. Note only.

---

## Verdict

Two defects, both low severity, neither affecting the C1 `47/47 · 34/34 · 39/47 · 133/133` or the
C2 `29/29 · 29 rows · 29 anchors · 25/25` counts:

- **F1** `.ufo/waves/round-82/controls/c2-runbook-cases-r82.json:981,985,989,993,999,1003` (authored
  at `controls/make-c2-cases-r82.py:38-46`) — the operator's account name, D-Bus unique names,
  UID-derived unit and a live PID sit in frozen, to-be-committed harness bytes, against the round's
  own shape-only rule. L1 decides whether to re-freeze.
- **F2** `quality/counters/c2-r82-runbook.py:170` + `:697` (+ `:722`) — `TMPDIR` resolves to the
  measured lane root while the comment at `:162` says the scratch root; a latent write path into the
  tree the round is measuring.

Checks that came back clean: no credential material anywhere in the 32 changed files; the three new
commands are read-only (`busctl list`/`introspect`, no `call`/`set-property`/`emit`, executed bytes
identical to the committed cells); the allocation parser enforces `MAX_BYTES`, type, non-object,
non-regular, non-symlink and unknown-namespace refusals and never invokes a shell; no seat prompt
requests a commit and both counters only read git.

STATUS: defect
