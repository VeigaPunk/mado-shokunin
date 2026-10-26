# ExecErrataR1 — R1 falsification: per-sentence re-derivation of the round-46 erratum draft

Seat: `ExecErrataR1` (round 47, wave w2, policy v1). Target: `.ufo/waves/round-47/w1/ScrErrataR1/erratum.md`
(2890 bytes, 20 lines, `sha256` below) against
`corpus/knowledge/hyprland-input-devices-r46.md:57`, the two round-46 live receipts and the host config chain.

Method: every claim re-derived by command (`receipts/verify-r1.out`, driver `verify-r1.sh`, `VERIFY-R1: 63/63 passed`).
Nothing under `~/.config`, `~/.local/share` or the lane was written; the compositor was read only through
`hyprctl version`, `hyprctl -j getoption …` and `hyprctl devices -j` (no `dispatch`, `keyword`, `reload`, `batch`);
the join ran from committed lane bytes against a dump captured into scratch. Scratch was deleted; the dump is not
copied here (it carries fields the lane does not commit).

Hashes of the artifacts this file judges:

| artifact | sha256 |
|---|---|
| `tools/mado-devices.py` (worktree **and** `git show` at `1001bda0`, `60edb66e`, `d7527d60`, `9bddd6ac`, `c24adef2`) | `3a80368997120503d5715596a17e762bbcb67a41db23d9241425bf19349d594f` |
| `.ufo/waves/round-46/l1-draft/mado-devices.py` (worktree **and** `git show 1001bda0:`) | `b229efd08d2d329dd60ced114598943d0419dac2f3cf05b1f6c1eb506c49a33b` |
| `.ufo/waves/round-46/receipts/live-devices-host-r46.txt` (worktree **and** `git show 1001bda0:`) | `0c749e1d255538a6767992f116d44c48022b7dd8140df50f773fc355dabd956f` |
| `.ufo/waves/round-46/receipts/live-devices-host-l1.txt` (worktree **and** `git show 1001bda0:`) | `d635baec7e64d0405b48edd28edfb57dc1f35e38dfa3a375ea40b70361708265` |
| `~/.local/share/omarchy/default/hypr/input.conf` | `bee5aa68cbec0c428fae7a5faf7da49a30e6f78ed96e78a063f08b66942448b8` |
| `~/.config/hypr/input.conf` | `3769c92ab7660f1795cb6d0af1bcc5a5614a299b29ae8358d1b85936bdd47bf4` |

The w1 draft's `verify.sh` hashed the worktree only; the `git show` column above is the check it lacked, and it
passes for all four files, so no artifact was edited after its commit.

## Verdicts

`erratum.md` line numbers are computed (`grep -n`); quoted fragments are <= 25 words.

| # | erratum unit | quote / claim | verdict |
|---|---|---|---|
| V1a | `:3` | "the live host run reads two config files" | **CONFIRMED, now observed** — the r46 run passes two `--config` (`:6`); the host's depth-4 source closure has exactly 2 files with an `input` block |
| V1b | `:3` | "the citation names the wrong receipt" | **WRONG as phrased** — the cited l1 receipt does support the sentence's numbers, and the landed tool reproduces them line for line today; the defect is producer identity (pre-landing draft), not a receipt that fails to support the claim |
| V1c | `:3` | "Corrects the parenthetical and the citation at line 57; nothing else in this entry changes" | **CONFIRMED** — `:57` is the entry's only live-receipt citation site (1 hit); entry still 73 lines, `git status` clean |
| V2 | `:5` | one `input` block in `~/.config/hypr/input.conf`, no `device` block — 8 words, at `hyprland-input-devices-r46.md:57`, citing `receipts/live-devices-host-l1.txt` | **CONFIRMED** — locator 57, citation present once on that line |
| V3 | `:7` | "'one `input` block' holds only for that one file read alone" | **CONFIRMED** — user file: 1 block at `:3`, `kb_layout = br` at `:10` |
| V4 | `:7` | "The effective chain has two input files, in this order" | **CONFIRMED, stronger** — 40 files in the depth-4 closure of `~/.config/hypr/hyprland.conf`, exactly 2 with an `input` block, `kb_layout` only at those two sites |
| V5 | `:11`,`:12` | both table rows: hashes, `sourced at …hyprland.conf:11` / `:17`, `input {` at `:2`/`:3`, `us` at `:3` / `br` at `:10` | **CONFIRMED** — every locator and both hashes re-derived |
| V6 | `:14` | "two `input` blocks reach the compositor and the first one names `us`" | **CONFIRMED, witness supplied** — the draft asserts this with static evidence only; `hyprctl -j getoption misc:key_press_enables_dpms` = `int 1, set true`, and that key is set **only** by the omarchy `input.conf` in the whole closure, so the running compositor parses that file (and hence its `input` block) |
| V7 | `:14` | join parses files in order into one state, a global is a plain dict assignment, "each later file overwrites the earlier value" (`tools/mado-devices.py:418-419`, `:334`) | **CONFIRMED by experiment** — `--config O --config U` → `br`; reversed → `us`, `agree=0 differ=9 DIFFER`; omarchy only → `us`; locators 418/419/334 exact |
| V8 | `:14` | "each has zero `device` blocks" | **CONFIRMED** — 0 and 0, and 0 across all 40 closure files |
| V9 | `:16` | corrected citation: r46 receipt hash, landed-tool hash, "passes both files and records both hashes plus the chain": # chain: ~/.config/hypr/hyprland.conf sources the omarchy default input.conf before the user's input.conf (`live-devices-host-r46.txt:5`) | **CONFIRMED** — hashes as in the table; `:3-4` are the two config headers, `:6` has two `--config`, Q2 at locator 5; the receipt is committed (`git show 1001bda0:` hash equal), so it satisfies the pointer-names-a-committed-receipt rule |
| V10 | `:16` | "the receipt line 57 cites is the draft's run" … "135 changed lines away … (30 removed, 105 added, 9 hunks)" | **CONFIRMED** — l1 head names the draft; my own diff: 30 removed / 105 added / 9 hunks, 566 → 641 lines |
| V11 | `:18` | "the observation itself" [stands unchanged] | **WRONG at the tip** — a same-day re-run does not reproduce it: `keyboards=9 … virtual=0` (both receipts: `keyboards=10 … virtual=1`), the `hl-virtual-keyboard-fcitx5` line is gone; the receipt text is unchanged but the observation is session-state-dependent, and the entry's `recheck:` trigger is `on-release`, which this state change would never fire |
| V12 | `:18` | "Both receipts print the same fourteen device lines - 10 keyboards, 9 AGREE …, fcitx5 as VIRTUAL, 4 mice … `verdict=OK`" | **CONFIRMED as a description of both receipts** — 14 device lines each, counts 10/9/1/4, bodies identical modulo the selftest line |
| V13 | `:18` | "so the single-file and two-file runs agree on this host and the entry's numbers are not affected" | **CONFIRMED for the correction's effect** — and still true today (both orders give `9/9/0`, `verdict=OK`); landed and draft tools produce identical device lines on the same argv |
| V14 | `:18` | "The r46 receipt adds `MADO_DEVICES_SELFTEST: 59/59 passed`, which the L1 receipt lacks" | **CONFIRMED** — 1 vs 0; note the draft *does* implement `--selftest`, so the omission was the run's, not the tool's |
| V15 | `:20` | "the two-config run was not repeated in round 47 … only the config hashes, the source lines and the block counts were re-read on the host today" | **CONFIRMED as a self-limit for w1, now superseded** — this seat repeated the two-config run (same-day, read-only); the sentence is accurate about host reads only (the draft also re-hashed six lane files and diffed both receipt bodies — lane checks) |

No unit is unverifiable; two are wrong (V1b as framing, V11 as a stale present-tense claim), one (V6) is true but
asserted without the witness that makes it observable, and the rest re-derive exactly.

## Findings for the L1 (before the data commit)

**F1 — the erratum re-asserts a live observation that no longer reproduces, on the same day.**
The entry's sentence is present tense under `verified-at: 2026-10-26`; the erratum says the observation itself
stands. Re-run (`hyprctl devices -j | python3 -I tools/mado-devices.py --devices - --config <omarchy> --config <user>`)
gives `keyboards=9 agree=9 differ=0 fallback=0 virtual=0 mice=4 … verdict=OK`, one line short of both receipts:
`hl-virtual-keyboard-fcitx5` is absent. A virtual keyboard exists only while its client holds it, so the entry's
"the fcitx5 input method as VIRTUAL" is session-state-conditioned and the `on-release` recheck would never catch it.
Fix in the same appended block: qualify the live sentence as an observation of that session and its date. Do not
restate the numbers as standing.

**F2 — "the citation names the wrong receipt" misstates the defect, and the lane has already ruled on it.**
The l1 receipt's own bytes name its producer (the draft), and its numbers are the ones `:57` prints; the landed tool
reproduces them line for line on the same argv, so the sentence's content is supported either way. The class is
producer identity / stale producer (M46-5's `provider` class): the entry cites a run of the pre-landing artifact.
`corpus/lessons/round-46-verifier-spotcheck.md:52` reaches the same reading — "both receipts print the same summary line, so the sentence's content holds" — and files it as a citation-layer defect. Wording to land: the entry cites a
receipt produced by the pre-landing draft (`b229efd0…`, one `--config`), not by the landed tool; the landed tool's
own receipt is the better witness. Note also that QUALITY 24 as worded is satisfied by the l1 receipt (its bytes do
name a producer), which is why it missed this — matching the spot-check's own note. Criterion 79 is satisfied after
the swap: the r46 receipt is committed at `1001bda0`.

**F3 — "reach the compositor" is asserted, not observed (gap, fixable with one read).**
The draft's evidence for V6 is static (two source lines, two existing files, block counts). The observation that
closes it is `hyprctl -j getoption misc:key_press_enables_dpms` = `{"int": 1, "set": true}`: that key is set only in
`~/.local/share/omarchy/default/hypr/input.conf:19` within the whole closure, so the compositor parses that file,
and therefore its `input` block. `input:kb_layout` = `{"str": "br", "set": true}` fixes the order's outcome.
Cheap; add it to the erratum's evidence line.

## Reproduce

```
bash .ufo/waves/round-47/w2/ExecErrataR1/verify-r1.sh "$WORK"   # 63/63, rc 0
```

Individual one-liners (all read-only; `$L` = the lane):

```
git -C $L show 1001bda0:tools/mado-devices.py | sha256sum
git -C $L show 1001bda0:.ufo/waves/round-46/l1-draft/mado-devices.py | sha256sum
git -C $L show 1001bda0:.ufo/waves/round-46/receipts/live-devices-host-r46.txt | sha256sum
diff -u $L/.ufo/waves/round-46/l1-draft/mado-devices.py $L/tools/mado-devices.py | grep -c '^@@'
hyprctl -j getoption misc:key_press_enables_dpms        # the omarchy file is parsed
hyprctl -j getoption input:kb_layout                    # br, the later file wins
hyprctl devices -j > $WORK/d.json
python3 -I $L/tools/mado-devices.py --devices $WORK/d.json --config <user> --config <omarchy>   # -> us, DIFFER
```

## Residuals

- The re-run's dump is not committed (device addresses/fields the lane does not commit); only the join's own
  `MADO_*` lines and the two summary lines appear in the receipt, and those device names are already in the lane's
  round-46 receipts.
- F1's cause (`the IM client is not holding a virtual keyboard right now`) is inferred from the compositor's device
  list; no process table was read or committed.
- The closure scan is depth 4 and expands `~` only; a source line with a variable or a deeper nest would be missed.
  It finds 40 files, 2 `input` blocks, 0 `device` blocks, 2 `kb_layout` sites.
