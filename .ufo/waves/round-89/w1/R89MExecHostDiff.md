# R89MExecHostDiff — host coverage receipt for C1 (read-only)

Seat: R89MExecHostDiff (leaf executor, round 89 wave 1). Lane root `/home/vgpnk/Projects/shokunin/mado-shokunin`,
base revision `af998dcc41d48618ffe7afe0efc9354755a9244e` (master). Scratch: `/fast/scratch/hyaku/mado-r89/R89MExecHostDiff`
(deleted on exit; the script `trap`s via `shutil.rmtree`, and the run directory is gone — see §8).

**These are DRAFT checks, not measurements.** They run on draft bytes (`build/mado-mako.c1.py`) and on the host's live
config. Nothing was written under `receipts/`; no counter was invoked; no scoring verdict is claimed.

Host read set (credential rule respected): `~/.config/mako/config` and the single file it includes,
`~/.local/share/omarchy/default/mako/core.ini`. Nothing else on the host was opened.

## 1. What was run (every command, with exit code)

| # | command | exit |
|---|---|---|
| 1 | `git -C …/mado-shokunin show af998dcc…:tools/mado-mako.py > $S/base.py` (38567 bytes) | 0 |
| 2 | `cc -O0 -o $S/ore …/controls/posix-ere-oracle.c` | 0 |
| 3 | `python3 …/w1/R89MExecHostDiff-grid.py --json $O/grid.json` — 24 tool invocations (12 base + 12 candidate) | 0 |
| 4 | in-process `tokenize()` of the five host headers, base vs candidate (importlib, no writes) | 0 |
| 5 | in-process `DEFAULTS` read from base tool (grounding the `format`/`max-icon-size` comparison) | 0 |
| 6 | second clean re-run of the grid script (reproducibility) | 0 |

Byte pins for the exact bytes exercised:

```
2720922b1b9206549bf20248a20c5b70d7dc445ab2d1815112a2cb524fce229e  build/mado-mako.c1.py
c374d71514f1559a12593b1097cd5e6ccc8ba2c225f2fa2b2d7764ef29192237  base.py (= af998dcc:tools/mado-mako.py,
                                                                     = the round-88 tool sha the declaration names)
4227019226073c975ae466b5753c938dcd3fdd9bd5701fd049297438460f8ce8  controls/posix-ere-oracle.c
```

Grid invocation shape (both tools, identically):
`python3 <tool> --config ~/.config/mako/config --home "$HOME" --app-name notify-send --urgency normal --body x
--app-icon x --category x --desktop-entry x --actionable false --expiring false [--mode do-not-disturb] --summary <S>`
with `S ∈ {"Setup Wi-Fi","Update System","Learn Keybindings","Install Dictation with Voxtype","Screenshot copied & saved","hello"}`
and modes ∈ {∅, {do-not-disturb}} (`--mode` unions with the initial `default` mode, manual L614-621/633-634).

All 24 invocations returned **rc 0** on both tools (no setup error, no crash).

## 2. The grid

`format` is the literal string `<b>%s</b>\n%b` (backslash-n) in every cell; it is shown collapsed.

| summary | modes | tool | rc | refusals | on-button-left | max-icon-size | invisible |
|---|---|---|---|---|---|---|---|
| `Setup Wi-Fi` | — | base | 0 | 5 | `invoke-default-action` | 32 | 0 |
| `Setup Wi-Fi` | — | candidate | 0 | 0 | `exec sh -c 'omarchy-notification-dismiss "Setup Wi-Fi"; omarchy-launch-wifi'` | 32 | 0 |
| `Update System` | — | base | 0 | 5 | `invoke-default-action` | 32 | 0 |
| `Update System` | — | candidate | 0 | 0 | `exec sh -c 'omarchy-notification-dismiss "Update System"; omarchy-launch-floating-terminal-with-presentation omarchy-update'` | 32 | 0 |
| `Learn Keybindings` | — | base | 0 | 5 | `invoke-default-action` | 32 | 0 |
| `Learn Keybindings` | — | candidate | 0 | 0 | `exec sh -c 'omarchy-notification-dismiss "Learn Keybindings"; omarchy-menu-keybindings'` | 32 | 0 |
| `Install Dictation with Voxtype` | — | base | 0 | 5 | `invoke-default-action` | 32 | 0 |
| `Install Dictation with Voxtype` | — | candidate | 0 | 0 | `exec sh -c 'omarchy-notification-dismiss "Install Dictation with Voxtype"; omarchy-launch-floating-terminal-with-presentation omarchy-voxtype-install'` | 32 | 0 |
| `Screenshot copied & saved` | — | base | 0 | 5 | `invoke-default-action` | 32 | 0 |
| `Screenshot copied & saved` | — | candidate | 0 | 0 | `invoke-default-action` | **80** | 0 |
| `hello` | — | base | 0 | 5 | `invoke-default-action` | 32 | 0 |
| `hello` | — | candidate | 0 | 0 | `invoke-default-action` | 32 | 0 |
| `Setup Wi-Fi` | do-not-disturb | base | 0 | 5 | `invoke-default-action` | 32 | 0 |
| `Setup Wi-Fi` | do-not-disturb | candidate | 0 | 0 | `exec sh -c '…Setup Wi-Fi…omarchy-launch-wifi'` | 32 | 0 |
| `Update System` | do-not-disturb | base | 0 | 5 | `invoke-default-action` | 32 | 0 |
| `Update System` | do-not-disturb | candidate | 0 | 0 | `exec sh -c '…Update System…omarchy-update'` | 32 | 0 |
| `Learn Keybindings` | do-not-disturb | base | 0 | 5 | `invoke-default-action` | 32 | 0 |
| `Learn Keybindings` | do-not-disturb | candidate | 0 | 0 | `exec sh -c '…Learn Keybindings…omarchy-menu-keybindings'` | 32 | 0 |
| `Install Dictation with Voxtype` | do-not-disturb | base | 0 | 5 | `invoke-default-action` | 32 | 0 |
| `Install Dictation with Voxtype` | do-not-disturb | candidate | 0 | 0 | `exec sh -c '…Install Dictation with Voxtype…omarchy-voxtype-install'` | 32 | 0 |
| `Screenshot copied & saved` | do-not-disturb | base | 0 | 5 | `invoke-default-action` | 32 | 0 |
| `Screenshot copied & saved` | do-not-disturb | candidate | 0 | 0 | `invoke-default-action` | **80** | 0 |
| `hello` | do-not-disturb | base | 0 | 5 | `invoke-default-action` | 32 | 0 |
| `hello` | do-not-disturb | candidate | 0 | 0 | `invoke-default-action` | 32 | 0 |

Full on-button-left values for the `do-not-disturb` rows are byte-identical to the `—` rows (verified in
`grid.json`); the action strings are abbreviated only in this table's DND block for width. Stderr status line for
every one of the 24 runs: base `MADO_MAKO: resolved=37 refusals=5`, candidate `MADO_MAKO: resolved=37 refusals=0`.

## 3. Refusal lists (exact)

Base refuses **the same five sections on all 12 runs** (60 refusals total, 5 per run), each with the reason
`criteria field 'summary~' is outside the model (refused)`:

```
/home/vgpnk/.local/share/omarchy/default/mako/core.ini:24
/home/vgpnk/.local/share/omarchy/default/mako/core.ini:27
/home/vgpnk/.local/share/omarchy/default/mako/core.ini:30
/home/vgpnk/.local/share/omarchy/default/mako/core.ini:33
/home/vgpnk/.local/share/omarchy/default/mako/core.ini:36
```

Those are exactly the five `[summary~=…]` headers (`core.ini` lines 24, 27, 30, 33, 36); the host config and its
include contain no other refusal-worthy line. Candidate: **0 refusals on all 12 runs** (0 total).

## 4. How many host sections each tool can decide

`core.ini` holds **9 criteria sections**: `[app-name=Spotify]` (L11), `[mode=do-not-disturb]` (L14),
`[mode=do-not-disturb app-name=notify-send]` (L17), `[urgency=critical]` (L20), and the five `[summary~=…]`
(L24/27/30/33/36).

| tool | decides | refuses | note |
|---|---|---|---|
| base | **4 / 9** | 5 / 9 | all five summary~ sections refused ⇒ their options are lost, not approximated |
| candidate | **9 / 9** | 0 / 9 | every summary~ section matched or not-matched by libc ERE |

Observable consequence on host data (deltas are exactly the options those five sections set):

- Four action sections: base `on-button-left = invoke-default-action` (default) vs candidate the real
  `exec sh -c …` action — for `Setup Wi-Fi`, `Update System`, `Learn Keybindings`, `Install Dictation with Voxtype`.
- `Screenshot copied & saved`: base `max-icon-size = 32` (global L8) vs candidate `80` (section L37).
- No cross-matching: each summary reaches only its own section; `hello` and every non-matching pair keep the
  global/default values in both tools.
- **`format` is not a discriminator here.** Section L38 sets `format=<b>%s</b>\n%b`, which is byte-identical to the
  tool's built-in default (`DEFAULTS["format"] == '<b>%s</b>\\n%b'`, base.py:112), so base and candidate both report
  the default and agree. Only `max-icon-size` separates the screenshot section on this host.
- **`invisible` is 0 in every row, including do-not-disturb.** Grounded in the host file: L15 sets
  `invisible=true` under `[mode=do-not-disturb]`, then L18 sets `invisible=false` under
  `[mode=do-not-disturb app-name=notify-send]`; `--app-name notify-send` makes the later section win (last match
  wins, L435-437). Both tools decide those sections, so this is not a C1 delta.

## 5. Host patterns vs the oracle and Python re

The five patterns after the tokenizer are exactly (verified against **both** tokenizers, in-process, identical
output `[(key, value)], None`):

`Setup Wi-Fi`, `Update System`, `Learn Keybindings`, `Install Dictation with Voxtype`, `Screenshot copied & saved`.

30 comparisons (5 patterns × 6 summaries) through the C oracle (`regcomp(REG_EXTENDED|REG_NOSUB)` / `regexec`,
C locale, no `setlocale`) and through Python `re.search`:

- oracle: exactly the 5 diagonal `match`, 25 `nomatch`, 0 `invalid`.
- python re: identical on all 30.
- **disagreements: 0 / 30.**

**Finding (load-bearing for C1's control argument).** All five host patterns are *regex-inert*: they contain no ERE
metacharacter (`&` in `Screenshot copied & saved` is a literal in both POSIX ERE and Python re). Therefore this host
corpus cannot discriminate libc ERE from `re.search` — the python-re forgery control derives **no** separation from
host data. Separation must come from the case set (constructs where the two engines diverge: `\d`, `\w`, `\<`,
`[[:alpha:]]`, `{`-without-a-valid-interval, backslash before an ordinary character, etc.). This is a property of
the host config, not a defect in the candidate: on host data the two matchers agree by construction.

## 6. Candidate behaviour on the host (what the receipt shows)

- 24/24 invocations rc 0; 0 refusals; `resolved=37` on every run, the same key set as base.
- Every effective value that is *not* set by a summary~ section is byte-identical to base (`max-icon-size` 32,
  `format`, `invisible` 0, and the remaining 34 resolved keys — the JSON blobs in `grid.json` match).
- Every effective value that *is* set by a summary~ section comes from the correct host line and only for the
  matching summary.

## 7. Risks / limits

1. **Draft bytes.** The candidate was `2720922b…fce229e` at run time (§1). If the file changes before the freeze,
   this receipt is stale and must be re-run; the grid script re-derives the base from the revision and hard-fails on
   any behavioural drift, so a re-run is one command.
2. **Host data is a single fixed corpus** (one user's config + one include). It exercises 5 regex fields on 6
   summaries; it says nothing about POSIX-vs-Python divergence (§5).
3. **`format` and `invisible` are non-discriminating** on this host (default collision; app-name ordering). A reader
   should not cite them as coverage evidence.
4. Host files were read only; nothing was modified. The grid script hard-fails (`exit 1`) on any non-zero tool rc or
   any oracle/python-re disagreement, so a future re-run detects drift rather than reporting a stale table.

## 8. Hygiene

- Scratch `/fast/scratch/hyaku/mado-r89/R89MExecHostDiff` was created for the base dump + oracle binary and removed
  by the script's `finally: shutil.rmtree(sdir)`; verified gone after the run.
- The JSON evidence was written to `/fast/scratch/hyaku/mado-r89/R89MExecHostDiff-out/grid.json` (outside the
  auto-deleted dir) and removed after this report was written.
- No installs, no git/jj mutations, no writes outside `.ufo/waves/round-89/w1/` and the scratch dirs.

## 9. Files

- `.ufo/waves/round-89/w1/R89MExecHostDiff-grid.py` — the reproducible grid (self-contained: dumps base by revision,
  builds the oracle, runs both tools, compares against the oracle and `re`; exit 0 only if all agree).
- `.ufo/waves/round-89/w1/R89MExecHostDiff.md` — this report.
