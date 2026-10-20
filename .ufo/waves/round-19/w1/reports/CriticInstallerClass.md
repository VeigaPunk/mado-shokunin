# CriticInstallerClass — APPLY-WITH-PERMIT: land `tool_install` as a 4th class (with a one-hunk `-m` fix), scan with `--permit tool_install`; it moves C3 by 0/6

Target: `.ufo/waves/round-18/drafts/TwInstallerChannels.patch` (sha256 `1acb8549…2068`), applied to the current
tool `c1ae45a7…` (= `17661e0:tools/mado-tripwire.py`, blob `a5d8a6ec`). All mechanics were run in a `/tmp` clone
(`/tmp/crit-installer-r19/lane` at `17661e0`). Nothing in the lane was written except this report.

## Decision

**Apply-with-permit.** The classifier lands. Each wave scan passes `--permit tool_install` and keeps the other three
classes unpermitted. Every permitted `tool_install` hit for a persistent install is then joined against the seat's
`## Installs` section. Do not use plain apply, and do not reject.

- **Why not plain apply.** RULES.md:7-8 and :14, plus this round's contract, authorize `uv tool` / `npx` / release
  binaries and require each install to be recorded. The current scan recipe (SKILL.md:529, "no `--permit` while the
  host pause holds") would make every authorized install exit 1 `findings`. That contradicts round-18
  CriticHonesty.md:73, "authorized channels are not violations". Real data (F2) shows this would be false-alarm
  volume only: all 5/5 persistent installs in the corpus were authorized and disclosed.
- **Why not reject.** Round-17 residual M4 (lessons/round-17.md:161-163) is still open: a `clean` scan says nothing
  about installer channels. The class closes that blind spot with zero collateral on real data. It also gives the
  RULES.md:14 "record every install" duty a mechanical cross-check (F2: 5/5 joins).
- **What permit buys.** The label is `permitted_only`, never `clean` (SKILL.md:592 still forbids citing it as
  clean). The hits stay in `findings` and `counts.tool_install`. `sudo <installer>` still raises an unpermitted
  `host_mutation`, which the draft's own case `tool-install-permit-does-not-cover-sudo` proves.

## Findings

### F1 — Mechanically clean on the current tool (no hidden regression in suites or the frozen pin)
`git apply` of the draft onto `c1ae45a7…` succeeds (hunks 2-6 at offset +20). The result compiles, sha
`38e3ab72…5ee5c`. Both tools were run on the same suites:

| suite | base `c1ae45a7` | patched `38e3ab72` |
|---|---|---|
| r17 core / compound / hardening / w2-regressions | 9/9, 16/16, 33/33, 30/30 | 9/9, 16/16, 33/33, 30/30 |
| r18-failsafe / r18 frozen selftest | 1/1, 31/31 | 1/1, 31/31 |
| draft r18-installers (13) | 1/13 (red before; only `clean-neighbours-stay-clean`) | 13/13 |
| `--frozen .ufo/waves/round-18/frozen` | `frozen_match` rc 0 | `frozen_match` rc 0 |

### F2 — Real-corpus counterexample hunt: 91 new hits, all `tool_install`, 0 elsewhere, 0 in Mado lanes
Command: `python3 -I {tw-base,tw-inst}.py --scan /home/vgpnk/.omp/agent/sessions/-Projects-shokunin` (4523 files,
transcripts read as data). Outputs: `/tmp/crit-installer-r19/scan-base.out` (sha `e7511d7c…`) and `scan-inst.out`
(sha `c612fe53…`).

- The multiset diff on (file, line, class, rule) is **+91 new, 0 lost, 0 new outside `tool_install`**. Base counts
  are host_mutation 103 / live_probe 900 / package_query 497; patched counts are the same plus tool_install 91.
- By rule: `npx` 86, `uv:tool-install` 3, `uv:pip-install` 1, `npm:install-global` 1.
- 632 Mado transcripts produced **0** hits. Lanes with hits: KaidokuR17 65, an unnamed session dir 10, KaidokuR18 6,
  TabiR16 5, TameshiR17 2, TabiR13 1, top-level 2.
- The 86 `npx` hits are pinned **runs**, not installs. Examples: `npx -y rea-agents@6.5.0 inspect-go-binary …` and
  `npx -y node@22 --version`.
- The 5 persistent installs are all authorized channels and all disclosed:
  - `uv tool install ruff` and `uv tool install vulture` → tameshi `.ufo/waves/round-17/w2/SimplifyNewTools.md:186`.
  - `uv tool install check-jsonschema` and `uv pip install --python /usr/bin/python3 --target … trafilatura` → fleet
    `.ufo/waves/kaika/tooling-global.md:20,24`.
  - `npm install -g @playwright/test@1.64.0` → tabi `.ufo/waves/round-13/w1/AriaRunner.txt:41` ("Attempted … FAILED
    EEXIST").

So a no-permit scan would turn 5 disclosed, authorized installs and 86 tool runs into exit-1 `findings`.

### F3 — Defect the draft adds: `python -m` recursion reads `-m` anywhere in argv, including the script's own arguments
Draft hunk 5 (`tw-inst.py:654`, `if "-m" in args: i = args.index("-m")`). Edge fixture
`/tmp/crit-installer-r19/edge/edge.jsonl` (sha `26395c15…`) gives:

- `python3 tools/x.py -m ps` → **`live_probe:ps`** under the patch, nothing under base. This is a new finding in a
  pre-existing class, and `--permit tool_install` does not waive it.
- `python3 tools/x.py -m pip install x` → `tool_install:pip:install`, a false positive.
- `python3 -mpip install x` (attached form) → missed.

The real corpus does not hit this (F2: 0 non-`tool_install` additions). It is still a correctness defect in an
existing axis.

**Smallest correction.** Honour `-m` only among the interpreter options that precede the first operand, and accept
the attached `-mMOD` form. Replace the draft's `-m` block with:

```python
        i = 0
        while i < len(args):  # interpreter options only; a script operand ends them
            a = args[i]
            if a in ("-W", "-X", "--check-hash-based-pycs"):
                i += 2
                continue
            if a.startswith("-m") and not a.startswith("--"):
                mod, rest = (a[2:], args[i + 1:]) if len(a) > 2 else (
                    (args[i + 1], args[i + 2:]) if i + 1 < len(args) else (None, []))
                if mod:
                    hits.extend(classify_segment([mod] + rest, depth + 1, unparsed))
                break
            if not a.startswith("-") or a == "-":
                break
            i += 1
        return hits
```

Prototype `/tmp/crit-installer-r19/tw-fix.py` (sha `48e047be…ed27`) results:

- All suites unchanged: 9/9, 16/16, 33/33, 30/30, 1/1, 31/31, 13/13.
- `--frozen` → `frozen_match`.
- Edge lines 17/18 are now clean; `-mpip`, `-I -m pip` and `/usr/bin/python3 -m pip` are caught; `-m pytest -m …`
  stays clean.
- Re-scan of the real corpus: 0 findings differ from the draft (`scan-fix.out` sha `fbb354e7…`). The corpus had grown
  to 4601 files by then because transcripts are live; the diff is over findings, not files.

The pre-existing `-c` anywhere-in-argv behaviour is out of scope and unchanged.

### F4 — The class name overclaims: 94.5% of real hits are registry runs, not installs
The real hits are 86/91 `npx`. `uvx`, `uv tool run` and `npm exec|x` are in the same family. These fetch and execute
code from a cache. They are not persistent installs that RULES.md:14 requires a seat to record.

- Round-18 SentinelHostPause.md:106 already notes that `npx` is not a RULES.md channel and that it runs registry
  code.
- **Correction, no new class:** in L1's SKILL/lesson text, define the `## Installs` disclosure join over the
  persistent rules only: `uv:tool-install|upgrade|uninstall`, `uv:pip-install`, `pip*:install`, `pipx:*`,
  `npm:*-global`, `cargo:*`. `npx` / `uvx` / `uv:tool-run` / `npm:exec` are reported as "registry runs".
- Splitting off a `tool_run` class would be more surface for no verdict difference under the permit. It is a
  tradeoff, not a defect.

### F5 — The docstring's "not classified" list reads as exhaustive but is not
Patched docstring: "pnpm, yarn, bun, brew, nix, `uv sync`, `uv python install` and plain downloads are not
classified". Measured misses that are not in that list: `go install`, `gem install`, `cargo binstall`,
`deno install -g`, `rustup component add`, `uv run --with`, `pnpm dlx`, `npm install --global=true`,
`npm install -g=true`. The fix is to prefix the list with "for example" or append these forms. This is a docs-honesty
fix, not a blocker.

RULES.md channel 3 (release binary into `~/.local/bin`, e.g. `curl -o ~/.local/bin/jq …`) is covered only by the
words "plain downloads". The permitted scan therefore cannot reconcile installs made through that channel.

### F6 — It contributes nothing to C3 and has an integration-order collision with TwMissHelperFn
- **C3 delta is 0.** None of the 6 tw-recall incident lines (`.ufo/waves/round-18/frozen/expected.json`, every
  line `pacman`/`sudo`/`wayland-info`) is an installer, and the patched tool still reproduces `frozen_match`. This is
  an unclaimed capability change. It must not be cited as progress toward "Before 3/6 → target 6/6"
  (SCORECARD.md:1090, :1106-1111), and per round-18 CriticHonesty.md:120 it is reported as an observation.
- **Order collision.** Order tests from base `c1ae45a7` (`/tmp`):
  - Installer then BashCVar: both OK.
  - BashCVar, then Installer, then HelperFn: HelperFn **FAILS**.
  - HelperFn then Installer: Installer **FAILS**.

  The rejected hunk is `@@ -412` in TwMissHelperFn. Both drafts insert new top-level functions immediately after
  `classify_pacman`'s `return ("host_mutation", rule)`, so this is a context-only collision. The resolution is to
  keep both blocks in sequence. The result needs one integrator rebase and then a selftest re-run.
- **Frozen re-pin.** The round-19 frozen baseline must be cut with the landed classifier, including F3's fix. Since
  the round-18 inputs contain no installer line, the class itself does not change that pin's findings.

## Impacted axes
- **Operability:** positive (residual M4 closes; 5/5 disclosure join) only if paired with the permit. Plain apply
  turns authorized behaviour into exit 1.
- **Calibration/honesty:** F4/F5 wording, and C3 must not be credited.
- **Regression:** F3 adds `live_probe`/FP risk in existing classes until it is fixed.
- **Freshness:** none.

## What would change my mind
- **Toward plain apply (no permit):**
  - an operator/L1 ruling that installs are paused too this round. RULES.md is unchanged and the round contract
    authorizes `uv tool`/`npx`, so this is absent.
  - a real persistent install that was undisclosed, or done outside an official channel. That would make exit 1 the
    wanted signal. F2 found 0 of 5.
- **Toward reject:**
  - any real-corpus finding lost, or any new non-`tool_install` finding that survives the F3 fix. Measured: 0 and 0.
  - an existing suite or `--frozen` regression. Measured: none.
  - a consumer that treats `--scan` exit as a gate and cannot pass `--permit`. The registry lists `--scan` as a probe
    (SKILL.md registry row `mado-tripwire`).
  - L1 ruling that a class firing 0 times in 632 Mado transcripts is not worth the ~130 lines plus option tables.
    That is a maintainability tradeoff that is defensible to reject on, but residual M4 is a Mado lesson and every
    Mado round authorizes installs.
- **Toward a split `tool_run` class:** evidence that a consumer needs to count `npx`/`uvx` runs separately from
  installs at the verdict level, not just in the lesson text.

## Required L1 text changes if applied (L1-owned; not written by me)
- SKILL.md:529: replace "no `--permit` while the host pause holds" with `--permit tool_install` only (the authorized
  channel), and require each persistent-rule hit to be matched to an `## Installs` record.
- SKILL.md registry `mado-tripwire` verdict map: add `tool_install` to the class list. Note that the class is waived
  in wave scans and that `sudo` is not.

## Limits
- I did not apply TwMissBashCVar/TwMissHelperFn semantics jointly with this patch; I only ran apply-order checks.
- I did not run `tw-recall.py` itself. The C3 = 0 conclusion rests on the 6 incident lines being non-installers
  (expected.json read) and on `frozen_match` with the patched tool.
- The real-corpus scan reads live, mutable transcripts, so the counts will drift (4523 → 4601 files between runs).
- `[INFERENCE]`: npx hits from unnamed session dirs may be orchestrator sessions, not seats.
- I did not check: npm/pip option tables against upstream docs (no fetch made), the `-c` anywhere-in-argv behaviour,
  or any host tool behaviour (no uv/npx/pip/npm/cargo invoked).

## Installs
none
