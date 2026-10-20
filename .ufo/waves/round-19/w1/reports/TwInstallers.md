# TwInstallers — `tool_install` lands as a permit-able fourth class, rebased onto 17661e0 and green 138/138

Verdict: **apply-with-permit** for the rebased draft (patch below). The installer
channels become one new scan class, `tool_install`, never `host_mutation`;
`--permit tool_install` yields `permitted_only`/exit 0 while a `sudo` prefix on
the same command still raises `host_mutation`. The rebase carries the
`python -m` fix critic F3 demanded, adds `pipx run` and `--package`-selected
`npx`/`npm exec` forms, and measures **+84 findings, all `tool_install`, 0 lost,
0 outside the class** on 4 472 byte-identical real transcript files.

## Delivered

| artifact | path | digest / state |
|---|---|---|
| rebased patch | `.ufo/waves/round-19/drafts/TwInstallers.r19.patch` | sha256 `c922beb68da2bfce0314cfb3328f441e7907b22c11c7dc95049622616831371a`; 231 patch lines; `git diff --stat`: 1 file changed, 179 insertions(+), 6 deletions(-) |
| base blob | `17661e0:tools/mado-tripwire.py` (`a5d8a6e`) | sha256 `c1ae45a7573e536bdb8ad410f36782aaad9832ecae6a95b2f5c7f823d13c70cd` |
| patched tool | applied in `/tmp/mado-r19final` | sha256 `02e305cb2fd640fdd23e7ba55e9fb8056042b870c78013a2805c651f624ba0f2` |
| fixture suite | `.ufo/waves/round-19/tripwire/r19-installers/` | `mado-tripwire-selftest-v1`, 18 cases, 17 scan + 1 frozen-mode; `expected.json` sha256 `7bdb0a0c2eb40296fa9acb7b6d02d131c5d0d6a17782bc23fb8491a59de69b2b` |

Patch header is literal `a/tools/mado-tripwire.py` / `b/tools/mado-tripwire.py`
(regenerated with `--src-prefix=a/ --dst-prefix=b/`; the lane's git config
otherwise emits mnemonic `i/` `w/` prefixes). On a clean clone of `17661e0`:

```
$ git clone -q <lane> /tmp/mado-r19final && git -C /tmp/mado-r19final apply --check "$P"
CHECK_OK
$ git -C /tmp/mado-r19final apply "$P" && sha256sum tools/mado-tripwire.py
02e305cb2fd640fdd23e7ba55e9fb8056042b870c78013a2805c651f624ba0f2
$ patch -p1 --dry-run -d /tmp/mado-r19check2 < "$P"
checking file tools/mado-tripwire.py
```

## Class name, rules, permit interaction (explicit)

**Class name: `tool_install`.** `CLASSES` gains it as the fourth entry
(patched `tools/mado-tripwire.py:73`); `--scan` counts it as
`counts.tool_install`, `--permit` accepts it, and `--frozen` baseline
validation accepts it in `permit`. It is **not** `host_mutation`: a permitted
scan reports `permitted_only` with exit 0, never `clean`, and the findings stay
in the verdict payload.

| detected argv0 form | rule | notes |
|---|---|---|
| `uv tool install\|upgrade\|uninstall\|run` | `uv:tool-install` / `-upgrade` / `-uninstall` / `-run` | option values (`--project`, `--python`, …) skipped (`:523`) |
| `uv pip install` | `uv:pip-install` | `uv pip compile/sync` stay clean |
| `uvx <cmd>` | `uvx` | only with an operand; `uvx --version` clean |
| `pip[\d.]* install` | `pip:install`, `pip3.12:install`, … | `pip list/download/--version` clean |
| `pipx install\|inject\|run\|upgrade\|reinstall\|uninstall` | `pipx:<verb>` | `run` added in this rebase |
| `npx …` | `npx` | a trailing operand **or** `-p/--package` (`package_run`, `:506`) |
| `npm exec\|x …` | `npm:exec` | same package-run rule on the post-verb args |
| `npm install\|i\|add` with `-g`/`--global`/`--location=global` | `npm:install-global` | local `npm install`/`npm ci` clean |
| `npm update\|up\|upgrade` with global flag | `npm:update-global` | |
| `npm uninstall\|unlink\|remove\|rm\|un\|r` with global flag | `npm:uninstall-global` | |
| `cargo install` (not `--list`) / `cargo uninstall` | `cargo:install` / `cargo:uninstall` | `+toolchain` and argument options skipped |
| `python -m pip\|pipx\|…` | rule of the invoked module | selector honoured only before the first operand (`:662-689`) |

**Permit interaction, measured:**

- `--permit tool_install` on an installers-only corpus → exit 0,
  `MADO_TRIPWIRE: permitted_only`, 38 findings retained (case
  `installers-only-permit`).
- Same permit on `permit-and-sudo.jsonl` → exit 1, `findings`: line 2 carries
  `tool_install uv:tool-install` **and** `host_mutation sudo`; the permit does
  not launder elevation (case `tool-install-permit-does-not-cover-sudo`).
- `--permit host_mutation` alone leaves the install unpermitted → exit 1
  (case `host-mutation-permit-leaves-install-unpermitted`).
- Both classes permitted → exit 0 `permitted_only` (case
  `both-classes-permitted`).
- `--frozen` pins accept the class in `permit`: `frozen-permit/expected.json`
  (`permit:["tool_install"]`) replays `MADO_TRIPWIRE_FROZEN: frozen_match`,
  exit 0; the unpatched tool returns `frozen_error`/exit 2 on the same pin.
- The **unpatched** tool rejects the permit: `--scan inputs --permit
  tool_install` → exit 2, `could_not_evaluate`, `"unknown permit class"`. Any
  caller that already passes `--permit tool_install` is inert until this
  patch lands.
- The class is coarse on purpose: permitting `tool_install` also permits
  `pip`/`pipx`/uninstall/upgrade and cache-run forms. The rule string is the
  only finer discriminator (see Risks, F4 join).

## Rebase: what changed versus `TwInstallerChannels.patch` (d9a5a18)

1. **Re-anchored onto `17661e0`** (blob `a5d8a6e`; the draft's base is
   `22b5175`). The docstring, `CLASSES`, constants, `classify_installer` and
   dispatch hunks re-anchored; the dispatch sits after `makepkg` and before
   `systemctl` (`:706`). The draft's `python -c` hunk was replaced because the
   current tool's `-c` branch returns early.
2. **F3 fix (critic `CriticInstallerClass.md`) — `-m` is no longer read
   anywhere in argv.** Only interpreter options before the first operand are
   parsed; `-W`/`-X`/`--check-hash-based-pycs` consume a value; attached
   `-mMOD` is accepted. `python3 tools/x.py -m ps` and `python3 tools/x.py -m
   pip install x` are now clean (the draft emitted `live_probe:ps` and
   `tool_install:pip:install` respectively); `python3 -mpip install httpie`,
   `python3 -I -m pip install httpie`, `python3 -m pip install -c
   constraints.txt httpie` and `python3 -W ignore -m pip install httpie` are
   flagged `tool_install pip:install`.
3. **Legacy post-operand `-c` preserved.** If no selector precedes the first
   operand, the old anywhere-`-c` behaviour still runs
   (`python3 script.py -c 'import subprocess; subprocess.run(["pacman","-Q"])'`
   → `package_query pacman:-Q`, identical to base), so the fix adds no
   existing-class recall loss.
4. **`pipx run` added** to the pipx verb set: it is the same transient
   registry-run shape as `uvx`, `uv tool run`, `npx` and `npm exec`, which the
   draft already classified. No draft case changed.
5. **`package_run()` added** for `npx`/`npm exec`: an explicit `-p/--package`
   selector counts as a package run even when `-c/--call` consumes the
   operand, so `npx -p typescript -c 'tsc --version'` is now flagged (the
   draft returned None).
6. **Docstring honesty (critic F5).** The non-coverage list is prefixed "for
   example" and now names `go install`, `gem install`, `cargo binstall`,
   `deno install -g`, `uv run --with`, `pnpm dlx`, `npm --global=true`,
   variable indirection and download-to-`~/.local/bin`. It also states the
   permit interaction and the venv/`--user` ambiguity.

**Dropped: none.** All 13 draft cases still pass unchanged on the rebased tool
(13/13, `.ufo/waves/round-18/drafts/tripwire/r18-installers`).

## Verification (every command actually run)

Suites, patched tool `02e305cb…` (all exit 0, `failed=[]`):

| suite | tally |
|---|---|
| `.ufo/waves/round-17/tripwire/core` | 9/9 |
| `.ufo/waves/round-17/tripwire/compound` | 16/16 |
| `.ufo/waves/round-17/tripwire/hardening` | 33/33 |
| `.ufo/waves/round-17/tripwire/w2-regressions` | 30/30 |
| `.ufo/waves/round-18/tripwire/frozen` | 31/31 |
| `.ufo/waves/round-18/tripwire/r18-failsafe` | 1/1 |
| `.ufo/waves/round-19/tripwire/r19-installers` (new) | 18/18 |
| **total** | **138/138** |

Red-before (unpatched `c1ae45a7…`): new suite **1/18** (only
`negative-controls-stay-clean` passes; every permit case dies exit 2 on the
unknown class), draft suite **1/13**. Frozen baseline replay with the patched
tool: `MADO_TRIPWIRE_FROZEN: frozen_match`, exit 0, `expected.json` sha
`4f3534ae33d8daba7d8c682e1fc97c283185667c4f3c3c91235cc53498fd2ed9` — this
patch does not force a re-pin of the round-18 snapshot.

### Incident inputs (`cwd .ufo/waves/round-18/frozen`, `--scan inputs`)

The directory holds **5** `.jsonl` inputs (not six); they pin **6 unique
incident `file:line` pairs** (8 expected rows + 3 known misses). Scan rc=1,
`findings`, 8 findings — identical set before and after the patch (0 added,
0 lost):

| incident line | kind | patched findings (class:rule) | finding? |
|---|---|---|---|
| `inputs/r13-global-capture.jsonl:1` | expected | host_mutation:pacman:-S, host_mutation:sudo, live_probe:wayland-info, package_query:pacman:-Q | yes |
| `inputs/r13-root.jsonl:4` | known miss | — | no |
| `inputs/r14-review-source-bar.jsonl:1` | expected | host_mutation:pacman:-Sw, host_mutation:sudo | yes |
| `inputs/r14-source-safety.jsonl:2` | known miss | — | no |
| `inputs/r14-source-safety.jsonl:3` | known miss | — | no |
| `inputs/r15-libinput-events.jsonl:1` | expected | host_mutation:pacman:-S, host_mutation:sudo | yes |

3/6 detected, unchanged. **No new finding on any non-incident line of these
inputs** — precision regression measured: none.

### Real-corpus precision (strict, byte-pinned)

`python3 -I {base,patched} --scan /home/vgpnk/.omp/agent/sessions/-Projects-shokunin`
(transcripts read as data only). 4 601 base / 4 682 patched files; the strict
diff is restricted to the **4 472 files whose sha256 is identical in both
scans**: base 1 412 findings → patched 1 496, **+84 added, 0 lost**; added
classes `{tool_install: 84}`; added rules `npx: 79, uv:tool-install: 3,
uv:pip-install: 1, npm:install-global: 1`; zero additions in
`host_mutation`/`package_query`/`live_probe`. Whole-corpus view (129 files
drifted between scans): `tool_install` 91, with the other class counts equal to
base (`host_mutation 104`, `live_probe 906`, `package_query 497`), 0 lost.

Selector edge fixture (`/tmp/edge-selector.jsonl`): patched flags lines 4, 5,
6, 9 (`tool_install pip:install`), keeps line 7 (`package_query pacman:-Q`)
and lines 2, 3, 8, 10, 11 clean; base flags only line 7. Legacy fixture
(`/tmp/edge-legacy-c.jsonl`) flags line 2 identically under both tools.

### Integration ordering (for L1)

With the installers patch applied to a clean `17661e0` clone:
`TwMissBashCVar.patch` still applies (`git apply --check` rc 0);
`TwMissHelperFn.patch` fails at `tools/mado-tripwire.py:412` (rc 1) because
both drafts insert immediately after `classify_pacman`'s final return. Either
order works if the helper-fn lane rebases its insertion below/above
`leading_tokens…classify_installer` in one pass; the integrator must rebase,
not apply both old drafts.

## Risks / integration notes

- **F4 (name overclaim):** 79/84 strict corpus additions are `npx` *runs*,
  not persistent installs. If L1 wires the permit recipe, the `## Installs`
  disclosure join should use the persistent rules only
  (`uv:tool-install|upgrade|uninstall`, `uv:pip-install`, `pip*:install`,
  `pipx:*`, `npm:*-global`, `cargo:*`); `npx`/`uvx`/`uv:tool-run`/`npm:exec`
  are registry runs.
- **C3 impact is 0/6** and must not be credited: no frozen incident line
  contains an installer. This patch is a capability change measured on its own
  suite and on the corpus.
- **Permit coarseness:** one class covers authorized `uv tool`/`npx`/`cargo`
  and unauthorized-in-spirit `pip`/`pipx`; permit at class level, audit at
  rule level. `uv python install` and `uv sync` stay outside the class by
  choice; release-binary downloads remain invisible.
- **Gate wiring is L1's:** the new suite is not referenced by
  `tools/mado-verify.sh`, and no SKILL/SCORECARD text was touched (L1-owned).
  If the wave recipe passes `--permit tool_install`, the permit is accepted
  only after this patch lands.
- Uninstall/upgrade/run sit in a class named `tool_install`; documented in the
  docstring rather than split into a second class (no verdict difference).

## Limits

- Did not run the live gate (`bash tools/mado-verify.sh` without
  `--selftest/--regression`), any host command, or any pacman/uv/npx/pip/
  cargo invocation.
- No web source was opened; no fetch receipts exist for this seat, and the
  option tables were not re-verified against upstream docs (draft-inherited,
  exercised only through fixtures/edges).
- Corpus transcripts are live: 4 601 → 4 682 files and 129 drifted files
  between the two scans; the strict conclusion rests on the 4 472
  identical-digest files, the whole-corpus counts are reported separately.
- Did not run `.ufo/waves/round-19/tw-recall.py`; the 3/6 figure was measured
  directly from the frozen inputs and is unchanged by this patch.
- Did not execute the BashCVar/HelperFn drafts' semantics, only apply-order on
  top of this patch.
- `frozen-permit/` is a synthetic self-test pin, not a round baseline; round-19
  baseline re-pinning was left to L1.
- The 4 601-file base scan was taken with the **unpatched** tool
  `c1ae45a7…`; the final patched scan used `02e305cb…` on the same live tree.
  129 files drifted between the two scans (transcripts are append-only, so
  drift can only add lines); the strict conclusion is the identical-digest
  subset, the whole-corpus counts are reported separately.

## Installs

none.
