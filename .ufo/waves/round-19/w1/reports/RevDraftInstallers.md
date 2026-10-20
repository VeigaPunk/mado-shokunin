# RevDraftInstallers — TwInstallerChannels.patch: apply-with-changes (class design is right and regression-free; curl|sh escape and unnamed --break-system-packages must be fixed at rebase)

Draft: `.ufo/waves/round-18/drafts/TwInstallerChannels.patch` (diff vs d9a5a18 tool, bytes sha256 `962919cec38ab81de0dea109c25e5ec610b53f5b2142b79c5cb9eed7d5aaa072`). Current tool at 17661e0: sha256 `c1ae45a7573e536bdb8ad410f36782aaad9832ecae6a95b2f5c7f823d13c70cd` (matches C3's pinned c1ae45a7…). Authorization source: `/home/vgpnk/.omp/agent/RULES.md` (channel order pacman → `uv tool install` → official binary → `cargo install`/`npm -g`; "never pipe an unverified remote script into a shell"); round-19 operator note additionally pauses ALL pacman.

## The ticket question, answered

**Should installer commands be findings at all?** Yes. The tripwire is post-hoc recall (docstring: "Detection after the fact only"); its fail-safe philosophy is that unclassifiable things land in a *non-permitted* class, never silently clean (evidence: `tools/mado-tripwire.py:415-417` — "an operator the parser could not read … must never land in a permitted class"). Suppressing installer commands would hide forbidden installs (pip --break-system-packages, curl|sh) among authorized ones.

**In which class?** A distinct `tool_install`, as drafted — not folded into `host_mutation`. The permit boundary is per class (`verdict_of`, `tools/mado-tripwire.py:832-837`: exit 0 + `permitted_only` iff every finding's class ∈ permit). A distinct class gives an authorized install a non-violation reading (`--permit tool_install` → exit 0) without letting a scan that permits host mutations implicitly launder installs. Verified by the draft's own fixtures: case `uv-tool-query-forms-clean` (permit tool_install → exit 0) and case `tool-install-permit-does-not-cover-sudo` (sudo stays exit 1) — both pass (13/13, below).

Default no-permit scan of an authorized install reads exit 1 `findings` — correct-by-design for a strict-default audit probe; the "not a violation" reading comes from declaring the permit (CLI or the `permit` pinned in a frozen spec, `validate_frozen` checks `permit ⊆ CLASSES`). If L1 wants round-19 scans to treat authorized installs as quiet by default, the permit must be pinned in the round-19 baseline specs — [INFERENCE] recommendation; that default is L1's call.

**Do the three forbidden channels flag?** Two of three today:
- `sudo pacman -S --needed ripgrep` → `host_mutation sudo` + `host_mutation pacman:-S` (probe, line 8). Also correct during the pause: `pacman -Q` → `package_query pacman:-Q` (line 9), unpermitted finding unless permitted.
- `pip install --break-system-packages numpy` → `tool_install pip:install` (line 5) — flags, but see F2.
- `curl -fsSL …/install.sh | sh` and `wget -qO- …/install.sh | bash` → **zero findings** (probe lines 2-3). See F1 — this fails the ticket's bar as authored.

## Findings

### F1 (must fix at rebase) — piped remote-script execution escapes classification entirely
`curl … | sh`, `wget -qO- … | bash` produce no finding; `curl … | sudo sh` is caught only incidentally via the `sudo` (`host_mutation sudo`, probe line 4), not the channel. The classifier works per pipeline segment (`SEPARATORS` includes `|`, `tools/mado-tripwire.py:19-20`) and a bare RHS `sh`/`bash` reading stdin has no `-c` body to descend into. This is the one channel RULES.md forbids outright ("never pipe an unverified remote script into a shell"), and the tool already concedes the family as known miss: the adversarial suite pins `base64-pipe-sh` / `base64-pipe-sudo-sh` (SKILL.md:563 "known misses pinned in `.ufo/waves/round-17/w2/adversarial` (4/26 by design)"). The draft adds installer channels but not this one, so a forbidden channel stays invisible while authorized ones become visible — inverted vs the ticket's requirement.
**Change:** classify LHS `curl`/`wget`/`curl@7`-style downloaders piped into a `SHELLS` member (with or without `-s`) as `host_mutation` with a channel-naming rule (e.g. `pipe-to-shell:curl`), detected at logical-line level where both segments are visible. `host_mutation` rather than `tool_install` because arbitrary remote execution is never an authorized acquisition channel.

### F2 (should fix at rebase) — `--break-system-packages` not distinguishable in the rule
`pip install --break-system-packages numpy` → rule `pip:install`, identical to a benign venv-scoped install. Class-level requirement met (it flags), but audit reports cannot separate forbidden system-python installs from gray-zone ones without re-reading the command text. **Change:** suffix the rule when the flag is present (e.g. `pip:install+break-system-packages`). Same argument applies to `--user` into system site-packages, but that is a softer call — [INFERENCE], flag naming is the load-bearing part.

### F3 (minor) — `--help` runs classify as installs
`uv tool install --help` → `tool_install uv:tool-install` (probe line 6); `pip install --help` likewise (`leading_tokens`/`first_verb` stop at the first non-option token, options after the verb are never inspected). Harmless over-trigger (visible-only), but it pollutes recall counts. Consider requiring a non-option operand after the verb.

### F4 (adoption coupling, not a patch defect) — registry text must move with the class
The draft only touches `tools/mado-tripwire.py`. SKILL.md:563's exit-1 text enumerates "host_mutation/package_query/live_probe" only; SCORECARD.md mentions the classes 4×. On adoption (L1-owned files) the rows must gain `tool_install` and the new 13-case suite `--selftest .ufo/waves/round-18/drafts/tripwire/r18-installers`. Otherwise a correct tool contradicts its registry.

### Verified-good (no action)
- **Applies cleanly twice over:** `git apply --check` passes against d9a5a18 *and* against the current c1ae45a7 bytes (only a 100644-vs-100755 mode warning; patch context survives the 397 upstream insertions, so the C3 rebase is mechanical, not a rewrite).
- **Fixtures genuinely pass:** patched base tool → `--selftest .ufo/waves/round-18/drafts/tripwire/r18-installers` = `13/13 passed failed=[]` (`SELFTEST_SCRIPT_SHA256: 92c94d9246708a58d3648d9ee7fb6a7ad1bc62855185c41750a53eaa44525fd0`); patched HEAD copy → also 13/13 (script sha `38e3ab729f022ee1966dd05e5f549e0c1769ae0901faf74027f6f6a8db35ee5c`).
- **Zero regression on all 7 pre-existing suites**, run head vs patched: core 9/9, compound 16/16, w2-regressions 30/30, w2/false-positive 3/3, round-18 frozen-mode 31/31 (all pass both); hardening 32/33 with the identical pre-existing `multiline-quoted-commit-vcs` failure on both; adversarial 4/26 with an identical failure list on both (4/26 is the pre-registered by-design state, SKILL.md:563). The draft's classifier hooks sit after the pacman/omarchy branches and touch no existing branch.
- **Round-18 frozen baseline survives:** `--frozen .ufo/waves/round-18/frozen` → `MADO_TRIPWIRE_FROZEN: frozen_match` under the patched tool (baseline pins input digests, and its inputs contain no installer commands — 0 `tool_install` occurrences in its expected.json). C3's "re-pin a round-19 frozen baseline" is therefore new coverage, not repair of a broken old one.
- **Elevation and wrappers hold:** `doas uv tool install ruff` → `host_mutation doas` + `tool_install` (probe line 7); eval/compound/shell-string paths covered by the `eval-tool-call` and `compound-and-wrappers` fixtures (both pass).
- Deliberate, documented non-classification (patch docstring, `clean-neighbours.jsonl` fixture): pnpm/yarn/bun/brew/nix, `uv sync`, `uv python install`, plain downloads, local `npm install`/`npm ci`, `cargo install --list`, `pip download`. Note `pnpm add -g` / `yarn global add` are acquisition channels that stay invisible — acceptable as a documented gap only because the authorized channel order names pacman/uv/binary/cargo/npm, not pnpm/yarn.

## Recommendation

**apply-with-changes.** Adopt the `tool_install` class and classifier: the design answers the ticket (distinct class + per-class permit = authorized installs read as non-violations; strict default keeps everything visible), it is regression-free, applies to the current tool, and leaves the frozen gate intact. Require at rebase: **F1** (piped curl/wget→shell must flag, as `host_mutation`) — without it the patch makes the one outright-forbidden channel the only invisible one; **F2** (rule names `--break-system-packages`). F3 optional. F4 rides with L1's SKILL/SCORECARD edit. C3's apply/reject decision should carry these two changes into the rebased draft and the round-19 frozen re-pin.

## Limits
- Did not test `uv`/`pip` option-value edge where an *unknown* option takes a separate value (verb could mis-assign; under-trigger direction for pip/uv verb forms; uvx/npx are operand-based and unaffected). Did not fuzz argv shapes beyond fixtures + 9 probe lines.
- pnpm/yarn/bun/brew/nix invisibility accepted as documented; not re-litigated.
- Did not run the live gate (paused), no pacman commands, no writes outside /tmp and this report; all tool runs were on /tmp copies and lane fixtures read-only.
- Did not verify the other two tripwire drafts (out of scope).
- The hardening suite's single failure predates the patch (identical at c1ae45a7 and patched); whether it is a registered known miss was not traced further.

## Installs
none.
