# TwInstallerChannels — round 18 w1 report

Scope: round-17 residual M4 (tripwire does not classify `uv tool install`, `npx`,
`pip install`, `npm -g`, `cargo install`). Draft only; nothing applied to
`tools/mado-tripwire.py`. No git/jj write in the lane; the patch was built and
applied only inside `/tmp` copies.

## Verdict: new class `tool_install`, not `host_mutation`

The five channels are classified into a **new class** rather than folded into
`host_mutation` for three reasons:

1. **Permit calculus.** `host_mutation` is the class a gate must never
   blanket-permit. The operator tooling directive (2026-10-19) authorizes tool
   acquisition unconditionally ("installs or updates any tool … without asking
   first"). Folding installs into `host_mutation` forces L1 to choose between
   waiving `host_mutation` (which would also waive `sudo pacman -S`) or banning
   the authorized channel. A separate class gives the gate a separate waiver bit.
2. **Different mutation surface.** `pacman -S` mutates the system package
   database and joins `/var/log/pacman.log`; `uv tool`, `pip`, `pipx`, `cargo`,
   `npm -g` write user-space prefixes (`~/.local`, `~/.cargo`, npm prefix) and
   leave no pacman-log line. Mixing them would corrupt the existing
   tripwire↔pacman.log second-authority join and the counts it reads.
3. **Audit readability.** A finding `tool_install uv:tool-install` states which
   channel was used; `host_mutation` would erase the channel distinction the
   lesson needs (the directive names the channels explicitly).

## Interface change (for L1 to accept or reject)

Accepted:

- `CLASSES` becomes `("host_mutation", "package_query", "live_probe",
  "tool_install")`. Every verdict payload (`scan` and `could_not_evaluate`)
  gains the key `"tool_install"` in `counts`; all existing keys keep their
  meaning. Consumers that read named keys are unaffected.
- `--permit tool_install` is accepted. No other permit change.
- New finding class `tool_install`, rules listed below. A finding is
  unpermitted unless `tool_install` is in `--permit`, so a scan of a transcript
  containing an install command that was previously `clean` now returns
  `findings` (exit 1) unless the caller passes `--permit tool_install`. This is
  the intended tightening and the one policy decision L1 must ratify.
- Module docstring: class list extended and one paragraph added naming exactly
  which channels are and are not classified.

Unchanged: CLI shape, schema names (`mado-tripwire-verdict-v1`,
`mado-tripwire-selftest-v1`), exit-code meanings, first-line labels, selftest
comparison semantics, `--frozen` interface, redaction, path refusals.

Not introduced: per-rule permits, a new top-level label, a tool-digest pin in
the selftest schema, any network or host access (the classifier is pure string
analysis; it never executes the commands it names).

## Rule set

Rule spelling follows the existing `<argv0>` / `<argv0>:<verb>` convention.

| argv0 | trigger (first non-option verb(s)) | rule |
|---|---|---|
| `uv` | `tool install` / `tool upgrade` / `tool uninstall` / `tool run` | `uv:tool-install`, `uv:tool-upgrade`, `uv:tool-uninstall`, `uv:tool-run` |
| `uv` | `pip install` | `uv:pip-install` |
| `uvx` | any operand (no bare `--version`/`--help`) | `uvx` |
| `pip`, `pip3`, `pip3.11`, … (`^pip[0-9.]*$`) | `install` | `<argv0>:install` |
| `pipx` | `install` / `inject` / `upgrade` / `reinstall` / `uninstall` | `pipx:<verb>` |
| `npx` | any operand (no bare `--version`/`--help`) | `npx` |
| `npm` | `exec` / `x` with an operand or `--` operand | `npm:exec` |
| `npm` | `install`/`i`/`add` with `-g`/`--global`/`--location=global`/`--location global` | `npm:install-global` |
| `npm` | `update`/`up`/`upgrade` with a global flag | `npm:update-global` |
| `npm` | `uninstall`/`unlink`/`remove`/`rm`/`un`/`r` with a global flag | `npm:uninstall-global` |
| `cargo` | `install` (unless `--list`) | `cargo:install` |
| `cargo` | `uninstall` | `cargo:uninstall` |
| `pythonN` | `-m MOD ...` (new, literal `-m` only) | recurse with `MOD` as argv0, e.g. `python3 -m pip install x` → `pip:install` |

Mechanics: `classify_installer()` is called from `classify_segment()` after the
`makepkg` branch and before `systemctl`; it returns `(class, rule)` or `None`,
and the generic `hit()` records argv0/command/line as for any other class.
Option values are skipped by two small helpers (`leading_tokens`,
`has_operand`) using per-tool option tables, so `pip --cache-dir X install pkg`,
`npm --prefix X install -g pkg`, `cargo --config k=v install pkg`,
`cargo +nightly install pkg` and `timeout 120 npx ...` all classify.
`sudo uv tool install pkg` emits both `host_mutation sudo` and
`tool_install uv:tool-install`.

Deliberately **not** classified (stated in the docstring):

- pnpm, yarn, bun, brew, nix (same channel, different argv0);
- `uv sync`, `uv python install`, `pip download`, `python -m venv`;
- `npm install` / `npm ci` without a global flag, `npm ls`, `cargo build`;
- query forms: `uv tool list`, `uv tool dir`, `pip list`, `pipx list`,
  `cargo install --list`, `npx --version`, `uvx --version`;
- quoted data (`echo "npm install -g x"`, `grep 'cargo install' f`).

## Files written

- `.ufo/waves/round-18/drafts/TwInstallerChannels.patch` — unified diff vs
  `d9a5a18:tools/mado-tripwire.py`, 194 lines, 6 hunks, +147/−6, sha256
  `1acb85491995aa57dc4f69cd6ac908d6e7b1e76947a23512550c0379cd8a2068`.
  (The CLASSES hunk carries only one trailing context line so the same patch
  applies to both the committed baseline and the working tree that landed
  `--frozen`; this was verified, not assumed.)
- `.ufo/waves/round-18/drafts/tripwire/r18-installers/` — 9 fixtures +
  `expected.json` (13 cases). Path is the one L1 assigned by moving the suite;
  selftest `args` are relative, so the directory is relocatable.
- `.ufo/waves/round-18/w1/reports/TwInstallerChannels.md` — this report.

No other lane file was written. The tool, docs, lessons and `SCORECARD.md`
are untouched.

## Verification (measured, on `/tmp` copies)

Baseline tool = `d9a5a18` blob `22b5175`, file sha
`962919cec38ab81de0dea109c25e5ec610b53f5b2142b79c5cb9eed7d5aaa072`.
Patched tool = sha `92c94d9246708a58d3648d9ee7fb6a7ad1bc62855185c41750a53eaa44525fd0`.

1. `python3 -m py_compile` on the patched file: OK.
2. Patched, new suite: `SELFTEST_SUMMARY: 13/13 passed failed=[]`.
3. Patched, all four round-17 suites: core 9/9, compound 16/16,
   hardening 33/33, w2-regressions 30/30 (88/88 total).
4. **Red before:** baseline tool on the new suite →
   `SELFTEST_SUMMARY: 1/13 passed failed=[…12 names…]`; the only passing case
   is the negative control `clean-neighbours-stay-clean`. Every positive case
   fails because the baseline emits no finding.
5. `git apply --check` on a pristine `d9a5a18` tree: OK; after apply the file
   sha is exactly `92c94d92…` (the tested bytes).
6. `git apply --check` on a copy of the current working tree (which already
   contains the landed `--frozen` work): OK; after apply it compiles
   (sha `174b22e1…`) and passes new 13/13 plus round-17 88/88. The patch is
   therefore integrable before or after the frozen-mode change.
7. Permit semantics: patched `--scan uv-tool.jsonl --permit tool_install` →
   `MADO_TRIPWIRE: permitted_only`, exit 0, `counts.tool_install = 3`;
   baseline at the same invocation → `could_not_evaluate`, exit 2,
   `error: unknown permit class`.
8. `counts` key set in a `could_not_evaluate` payload:
   `['host_mutation', 'live_probe', 'package_query', 'tool_install']`.
9. Full-directory scan without permit: `MADO_TRIPWIRE: findings`, exit 1,
   `counts {"host_mutation": 2, "live_probe": 0, "package_query": 0,
   "tool_install": 34}`, `unpermitted 36`.
10. Nested spawn: `subprocess.run(["python3","-m","pip","install","x"])` in an
    `eval` cell → `[('tool_install', 'pip:install', 2)]`.
11. `.ufo/waves/round-18/frozen-tripwire/` contained no files at report time
    (`find … -type f | wc -l` = 0), so the frozen pin cannot yet be checked
    against this class; see risk 4.

## Risks / limits L1 should weigh

1. **Blanket class waiver.** `--permit tool_install` waives every rule in the
   table, including `npm:uninstall-global` and `cargo:uninstall`. No per-rule
   granularity exists (same shape as the other classes).
2. **Over-report by design.** `pip install` and `uv pip install` are flagged
   even inside a project venv, because the residual M4 named `pip install`
   without qualification. If L1 prefers venv-local installs to stay clean, that
   is a scope reduction to decide explicitly, not something this draft hides.
3. **Misses.** pnpm/yarn/bun/brew/nix; `uv sync`; `uv python install`;
   installs performed by a script the seat wrote and then ran; non-literal
   spawn arguments; commands on a remote host or inside a container
   (`ssh host pip install …` is argv0 `ssh` and stays clean). These are
   pre-existing tripwire limits, not regressions.
4. **Frozen pin ordering.** If the round-18 frozen snapshot (still being cut
   when this was written) contains an installer command, its pin must be cut
   with the post-patch tool, otherwise `--frozen` will report
   `frozen_verdict_mismatch`. Pinning with `--permit tool_install` in the
   snapshot's own `permit` list also works but weakens that gate for the class.
5. **Receipts.** Round-17 receipts remain valid for the revision they name
   (tool sha `962919ce…`); they are not reproducible as `clean` with the new
   tool if the scanned transcript contains an install. New selftest output
   prints `SELFTEST_SCRIPT_SHA256: 92c94d92…`.

## Handoff — doc surfaces L1 owns

- `SCORECARD.md:856` prose ("into host_mutation / package_query / live_probe")
  and the product row at `SCORECARD.md:919` both enumerate the class list and
  need the fourth class.
- `SKILL.md:562` (`mado-tripwire` registry row) verdict map says "at least one
  unpermitted host_mutation/package_query/live_probe finding"; it needs
  `tool_install` added to the class list and a note that installs are a
  separate waiver. The round-17 tripwire limit paragraph (`SKILL.md:577-587`)
  is the natural place for the channel list/limits sentence.
- `.ufo/waves/round-18/drafts/SkillRegistryDraft.md:12` (the drafted
  gate row) inherits the same verdict map text.
- If criterion 24/25/26 in `corpus/QUALITY.md` quotes the class list, mirror
  the fourth class there (L1's wording, not mine).
- Gate usage change: a seat that follows the operator directive and runs
  `uv tool install …` will produce an unpermitted `tool_install` finding under
  the no-permit scan rule in `SKILL.md:528-530`. L1 must decide whether the
  wave scan uses `--permit tool_install` (authorized channel) or reports and
  discloses each install; this draft makes the choice visible rather than
  silently permitting it.

Not run: lane gates, `mado-verify.sh`, any live/host command, any network
fetch. No tool was installed or upgraded during this work.
