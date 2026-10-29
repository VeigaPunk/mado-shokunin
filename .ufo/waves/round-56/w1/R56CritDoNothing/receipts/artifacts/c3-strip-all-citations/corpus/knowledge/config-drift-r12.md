# Config drift — gkeep installation re-anchor (MADO-R12-4)

source: [ref] — `/home/vgpnk/Projects/gkeep/install.sh` — HEAD 133b867, `install.sh:21-36,60-82,88-90`; [ref] — `tools/mado-verify.sh` — Erratum (round 12, 2026-10-19) above `declare -a EXPECT`; [ref] — `corpus/knowledge/omarchy-drift-watch.md` — § Errata (append-only), lines 284-287.
verified-at: 2026-10-19
recheck: 2027-01-17

## Scope and tags

This entry re-anchors drift observed in the operator-owned desktop config on 2026-10-17.
The lane measures and reports it; the operator project `~/Projects/gkeep` owns its installer.
No file in the config trees was written, no installer was run, and the compositor was not mutated.

- `[OBS]` means a direct file, command, checksum or read-only compositor observation.
- `[INF]` means a connection supported by observations but not a witnessed installer execution.
- `[UNK]` means the available evidence does not settle the question.
- Live values below are point measurements on 2026-10-19, not permanent host facts.
- Durable command output: `.ufo/evidence/round-12/drift-hypr.txt`, `drift-waybar.txt`, and `drift-precedence.txt`.
- The report follows the append-only re-anchor protocol in `omarchy-drift-watch.md:284-287`.

## Old → new measurements

The old side is rechecked from surviving `.bak` files when present; historical-only counts are labeled as such.

| Surface | Old pin / old shape | Current shape | Evidence and date |
|---|---|---|---|
| Hypr root lines | 29 — `wc -l` on `hyprland.conf.bak.1792267376`, 2026-10-19 | 32 — `wc -l` on `hyprland.conf`, 2026-10-19 | `.ufo/evidence/round-12/drift-hypr.txt` |
| Hypr root bytes | 1,273 — `wc -c` on the same backup, 2026-10-19 | 1,329 — `wc -c` on current root, 2026-10-19 | same |
| Hypr root SHA-256 | `4f52854a3c143dcf58430a679e339619223d2b5008115a322d06b2de637ea462` — `sha256sum` backup, 2026-10-19 | `ce7483f35ab52bc28e3020a6fb0ac14b2e02de5817abe827ef8452a0190f8365` — `sha256sum` current root, 2026-10-19 | same |
| `source` lines | 17 — `grep -cE '^[[:space:]]*source'` backup, 2026-10-19 | 18 — same command on current root, 2026-10-19 | same |
| Final include | `ai-usage.conf` at line 29 — `grep -nE` over backup, 2026-10-19 | `gkeep.conf` at line 32; `ai-usage.conf` remains at line 29 — `grep -nE` over current root, 2026-10-19 | same |
| Local active Hypr `.conf` inventory | 12 — MADO-1 historical inventory rows, re-counted by grep pattern `^\| (hyprland|bindings|input|monitors|looknfeel|hypridle|hyprlock|hyprsunset|ai-usage|autostart|envs|xdph)\.conf \|` in `hyprland-config-plane.md` on 2026-10-19 (12 table hits; historical filesystem observation was 2026-10-14, original invocation not retained) | 13 — `find ~/.config/hypr -maxdepth 1 -type f -name '*.conf' | wc -l`, 2026-10-19 | `.ufo/evidence/round-12/drift-hypr.txt`; only current filesystem is freshly measured |
| Added local file shape | absent from MADO-1's historical active-file inventory, 2026-10-14 | 264 bytes / 5 lines — `wc -c` / `wc -l` on `gkeep.conf`, 2026-10-19; 3 `windowrule` directives — `awk` directive-kind census, 2026-10-19 | same; values and rule bodies intentionally not recorded |
| Waybar config lines / bytes | 249 / 6,068 — `wc -l -c` on `config.jsonc.bak.1792267376`, 2026-10-19 | 260 / 6,354 — `wc -l -c` current `config.jsonc`, 2026-10-19 | `.ufo/evidence/round-12/drift-waybar.txt` |
| Waybar config SHA-256 | `07f7d663106b72e4c2a7da90883ef2ade044d7e6cb791e81ead777f7d8a08e71` — `sha256sum` backup, 2026-10-19 | `a408a33df48a39dc16214124dd0b86d6ab03e13802bac173146ae8a858aae829` — `sha256sum` current, 2026-10-19 | same |
| Top-level config module entries | 17 = 2 left + 8 center + 7 right — `jq` length parse of backup, 2026-10-19 | 18 = 2 left + 8 center + 8 right — same `jq` parse of current, 2026-10-19 | same; `custom/gkeep` is inserted in `modules-right` before `custom/ai-usage` |
| MADO-R3-1 module convention | 19 = 2 left + 8 center + 7 right + 2 drawer children — same JSON parse, 2026-10-19 | 20 = 2 left + 8 center + 8 right + 2 drawer children — same JSON parse, 2026-10-19 | `waybar-walker-semantics.md:77-79,142-148` defines the expanded group interpretation; parsed `group/tray-expander.modules` length is 2 |
| Waybar style lines / bytes | 136 / 1,887 — `wc -l -c` on `style.css.bak.1792267376`, 2026-10-19 | 155 / 2,256 — `wc -l -c` current `style.css`, 2026-10-19 | `.ufo/evidence/round-12/drift-waybar.txt` |
| Waybar style SHA-256 | `8316c08ceaa7e3f0624e1b82b1e03523096820fbf775362a930d7f831b0c4e8f` — `sha256sum` backup, 2026-10-19 | `8f335ca01da53d32eb968c2f7752f3149f073e8e56411980913f4dd25d385fdf` — `sha256sum` current, 2026-10-19 | same |
| CSS intermediate | — | `style.css.pre-ai-readability`: 150 lines / 2,118 bytes — `wc -l -c`, 2026-10-19; SHA-256 `c9215e9ee3053e19a07fb5618150fa46f6b3af36cc75aba930db31bd022b4782` — `sha256sum`, 2026-10-19 | same; its mtime is 2026-10-17 17:02:56 -0300; current style mtime is 20:32:18 -0300 |

Old roots are not inferred solely from pre-existing prose: the Hypr and Waybar config/style backups are present and their full digests equal the recorded old pins. The two `config.jsonc` backups at epochs `1792203278` and `1792267376` both hash to the old pin; the latter is the pair used for the old→new comparison.

## Reconstructed change and source custody

### Direct file comparison `[OBS]`

- `diff -u ~/.config/hypr/hyprland.conf.bak.1792267376 ~/.config/hypr/hyprland.conf` has one hunk: only lines 30-32 are added after the existing `ai-usage.conf` include.
- The added text is a blank line, a `# gkeep local notes` comment, and `source = ~/.config/hypr/gkeep.conf`.
- The backup root is 29 lines and the current root is 32 lines; the backup's full SHA-256 is exactly the former pin.
- `gkeep.conf` was counted only by bytes, lines, and directive kind; no rule contents were copied into this record.
- The two Waybar config backup files `config.jsonc.bak.1792203278` and `.bak.1792267376` are each 249 lines / 6,068 bytes and match the former `07f7d663…` pin.
- JSON parsing of either old backup yields `modules-left=2`, `modules-center=8`, `modules-right=7`, drawer child count 2.
- Current JSON parsing yields left 2, center 8, right 8; the only top-level rail delta is `custom/gkeep` before `custom/ai-usage`.
- Under the MADO-R3-1 convention, count the drawer's leader plus both parsed child modules: its two children add 2 beyond the rail-array entry.
- Thus the old expanded count is 2+8+(7+2)=19, and current is 2+8+(8+2)=20.
- `style.css.bak.1792267376` has the old 136-line / 1,887-byte hash; `style.css.pre-ai-readability` is an observed intermediate; current CSS is later and larger.
- The intermediate and current CSS mtimes do not by themselves prove who authored either stylesheet or which command wrote it.

### Source and chronology `[OBS]` / `[INF]`

- Read-only Git identity: `git -C /home/vgpnk/Projects/gkeep rev-parse --short HEAD` → `133b867`.
- Full HEAD: `133b86717a02548aeaff3f1411bf301d936c5308`; latest commit date from `git log -1 --format='%H%n%cs'` is 2026-10-18.
- `sha256sum /home/vgpnk/Projects/gkeep/install.sh` equals `git -C /home/vgpnk/Projects/gkeep show HEAD:install.sh | sha256sum`; the file read is the `HEAD` source.
- `install.sh:21-36` reads `share/hypr/gkeep.conf`, copies it to the local config path, then appends the `gkeep.conf` source with a backup if not already present.
- `install.sh:42-68` inserts the `custom/gkeep` Waybar module before `custom/ai-usage` when absent.
- `install.sh:76-82` appends the gkeep CSS snippet after making a backup when the selector is absent.
- `install.sh:88-90` invokes `hyprctl reload` and then `hyprctl configerrors` if `hyprctl` is available.
- That installer and its reload were read, not executed. No inference about an actual process invocation is promoted to observation.
- Backup epoch `1792203278` — `date -u -d @1792203278`, 2026-10-19 — is 2026-10-17 02:14:38Z.
- Backup epoch `1792267376` — `date -u -d @1792267376`, 2026-10-19 — is 2026-10-17 20:02:56Z.
- The Hypr and Waybar config backup mtimes at the latter epoch and the matching source-delta shapes make the operator installer the supported causal explanation `[INF]`, not a witnessed execution `[UNK]`.
- The CSS intermediate mtime is 2026-10-17 17:02:56 -0300, while current style is 20:32:18 -0300; a later restyle is consistent with the `pre-ai-readability` name but authorship/reason is not independently established `[INF]/[UNK]`.

## Live precedence spot-check `[OBS]`

- `hyprctl getoption general:gaps_out` → `custom type: 0 0 0 0`, `set: true`.
- `hyprctl getoption input:kb_layout` → `str: br`, `set: true`.
- `hyprctl configerrors` returned empty stdout, exit 0.
- Evidence transcript: `.ufo/evidence/round-12/drift-precedence.txt`.
- These two declared-vs-effective spot checks sustain the bounded precedence examples in `SKILL.md:48-52`; they do not establish every key's include owner.

## Gate re-anchor and residual blind spots

- The landed round-12 comment in `tools/mado-verify.sh` is titled `Erratum (round 12, 2026-10-19)` and directly precedes `declare -a EXPECT`.
- It records 17→18 sources (`~/.config/hypr/gkeep.conf` appended after `ai-usage.conf`) and the root sha `4f52854a3c143dcf…` → `ce7483f35ab52bc2…`; 18 — `grep -cE '^[[:space:]]*source' ~/.config/hypr/hyprland.conf`, 2026-10-19.
- `LOCAL` is **not** widened: it stays the MADO-1 list of 12, because `gkeep.conf` existence is already checked by `sources_resolve` (it iterates EXPECT). An intermediate revision that also appended `gkeep` to `LOCAL` was dropped by the integrator: no fixture behaviour depended on it (its only killer was the pin-integrity assertion R10), so it was an uncovered widening (`gate-standing-use.md` §5 rule 2). The live directory holds 13 `*.conf` — `find ~/.config/hypr -maxdepth 1 -type f -name '*.conf' | wc -l`, 2026-10-19 — and `hypr.local.inventory` still reads 12/12: that silence is M13.
- `hypr.root.include_graph` compares the extracted ordered list against EXPECT; it detects a changed count/order. The remaining set-blind gap: `sources_resolve` iterates EXPECT and checks those targets only, while `local.inventory` checks named LOCAL members without enumerating every directory entry.
- The gate's Waybar checks parse and pin selected semantics, not a complete top-level module set; adding `custom/gkeep` is therefore not a Waybar module-set verdict change.
- This is M13's set-blind coverage limitation: a pinned allowlist is not an unconstrained source/file/module census.
- Gate at the final round bytes (2026-10-19): `bash tools/mado-verify.sh --no-live` → `pass=29 fail=0 unknown=0 skip=8 note=4`, CLEAN (`.ufo/evidence/round-12/gate-no-live-after.txt`); before: 1 FAIL `hypr.root.include_graph` (`.ufo/evidence/round-12/before-no-live.txt`). A mutant dropping the gkeep EXPECT line is killed by `--selftest` (`.ufo/evidence/round-12/gate-mutant-gkeep.txt`).
- The re-anchor rests on an inference: the operator ran their own installer and kept developing gkeep afterwards (HEAD dated 2026-10-18). Operator intent to keep gkeep is not on record; it is routed as an L0 question. If the operator rules gkeep temporary, an appended erratum reverts EXPECT.

## SKILL.md append-only erratum map

- Present-tense `SKILL.md:40-41` calls the root 17 `source` lines and 29 lines; current remeasure is 18 and 32, backed by the exact former root backup.
- `SKILL.md:46` puts `ai-usage.conf` last; the current last include is `gkeep.conf` at line 32.
- `SKILL.md:67` says the local usage-rule file is “sourced last”; only that order claim is contradicted. This pass did not reread the rule bodies. Re-measure order with `grep -nE '^[[:space:]]*source[[:space:]]*=' ~/.config/hypr/hyprland.conf` — 2026-10-19.
- `SKILL.md:92-93` repeats “sourced last” and “ahead of every other layer”; the additional gkeep source is now later.
- `SKILL.md:103` also states `config.jsonc` 249 L and `style.css` 136 L as current; those lengths are now 260 L and 155 L. Re-measure: `wc -l -c ~/.config/waybar/config.jsonc ~/.config/waybar/style.css` — 2026-10-19.
- Dated worked examples at `SKILL.md:288-300` and `:412-425` retain their historical date and old hash as what was measured then; they are not rewritten as current claims.
- Other `ai-usage.conf:29` references that merely identify its line or an earlier layer remain historical anchors, not assertions that it is still last.
- The required SKILL change is insertion-only: a short live-state blockquote after the paragraph ending at line 46, plus a new `## Errata (round 12)` section at EOF.

## Disposition

- `[OBS]` The backing files show a new gkeep source, a matching local conf, a new Waybar array entry, and a CSS transition from its old pinned backup through a named intermediate to current CSS.
- `[INF]` The exact install-script behavior, backup timestamps and matching diffs support an operator-applied gkeep installation as provenance.
- `[UNK]` No installer execution trace was collected; source code is not proof that this exact `install.sh` process ran.
- **Operator-applied; mado measures, re-anchors, and recommends.** gkeep remains outside this lane's province; report the adjacent change, do not absorb it into mado-owned configuration or remediate it.
- No compositor reload, Waybar restart, config write, file edit outside this repository, or operator-project write was performed.

## Limits

- `hyprctl getoption` checks only `general:gaps_out` and `input:kb_layout`; it does not independently establish all include precedence or source ownership.
- Empty `configerrors` is a parser/load-health observation at this sample, not evidence that every window rule has its intended effect.
- The gkeep rule bodies and their per-window effects remain unexamined; rule bodies are shape-only by task boundary, and no gkeep-matching window was read (effect reads via `hyprctl getprop` exist — `window-rule-effects-getprop.md`).
- The Waybar JSON parse establishes declared module arrays, not runtime rendering, text, click behavior, or whether the running process loaded the present bytes.
- `style.css.pre-ai-readability` is an observed named file and digest; its author, intended release point and exact editing history remain unknown.
- The old 12-local-conf observation is preserved in MADO-1's historical file table; its original directory-listing command was not retained.
- Set-blind allowlists remain unable to detect every unlisted member. A clean check of EXPECT/LOCAL is not a complete census.

## Rejected

- Rejected: “The gkeep source is mado-owned desired configuration and should be folded into the lane's baseline.” Reason: the installer and changes belong to `~/Projects/gkeep`; observed adjacency grants no write authority. Flip only if the province/owner contract explicitly transfers that substrate.
- Rejected: “The gate's updated EXPECT array (with the unchanged LOCAL list) proves the whole Hypr config set is unchanged.” Reason: both loops enumerate fixed lists, not an unconstrained directory/source-set census. Flip only if a separate complete-set check is added and measured.
- Rejected: “An empty `hyprctl configerrors` proves the gkeep window rules work as intended.” Reason: parser health does not measure per-window effects. Flip only with a safe, authorized effect observation that does not mutate the compositor.

## Re-measure commands

Run from the lane root for repository anchors; config probes use the absolute paths shown in the evidence files.

- Hypr current/old lengths: `wc -l -c ~/.config/hypr/hyprland.conf ~/.config/hypr/hyprland.conf.bak.1792267376` — 2026-10-19.
- Hypr current/old hashes: `sha256sum ~/.config/hypr/hyprland.conf ~/.config/hypr/hyprland.conf.bak.1792267376` — 2026-10-19.
- Hypr source counts: `grep -cE '^[[:space:]]*source' <file>` for current and backup — 2026-10-19.
- Hypr diff: `diff -u ~/.config/hypr/hyprland.conf.bak.1792267376 ~/.config/hypr/hyprland.conf` — 2026-10-19.
- Active local count: `find ~/.config/hypr -maxdepth 1 -type f -name '*.conf' | wc -l` — 2026-10-19.
- gkeep shape: `wc -l -c ~/.config/hypr/gkeep.conf` plus `awk 'NF && $1 !~ /^#/ {n[$1]++} END {for (k in n) print k, n[k]}' ~/.config/hypr/gkeep.conf` — 2026-10-19.
- Waybar old/current lengths and digests: `wc -l -c` and `sha256sum` on the backup/current paths in `drift-waybar.txt` — 2026-10-19.
- Waybar module arrays: the `jq -c` projection in `drift-waybar.txt`, applied to each backup and current JSONC — 2026-10-19.
- CSS intermediate/current: `wc -l -c`, `sha256sum`, and `stat -c '%n %s bytes %y'` on `style.css.pre-ai-readability` and current `style.css` — 2026-10-19.
- Backup epoch conversion: `date -u -d @1792203278` and `date -u -d @1792267376` — 2026-10-19.
- Live precedence and parser health: `hyprctl getoption general:gaps_out`; `hyprctl getoption input:kb_layout`; `hyprctl configerrors` — 2026-10-19.
- Provenance source: `git -C ~/Projects/gkeep rev-parse --short HEAD`; `git -C ~/Projects/gkeep show HEAD:install.sh | sha256sum` — 2026-10-19.
- Gate re-anchor verification: `gate-selftest-after.txt` (268/268), `gate-no-live-after.txt`, `gate-live-after.txt` (52 pass / 0 fail / 8 notes) and `gate-regression-after.txt` (PASS at target `e5894387…`), all under `.ufo/evidence/round-12/`, 2026-10-19.

## Errata (round 12, post-integration)

- The post-integration critic found no selftest scenario that removes `gkeep.conf` (`.ufo/evidence/round-12/l2-postcritic.md` item 4). Scenario B now also deletes the fixture `gkeep.conf` and asserts `hypr.root.sources_resolve` FAIL; red-before/green-after: a mutant flipping the `sources_resolve` FAIL arm to PASS survived every behavioural assertion of the `5174e15` gate (killed only by the pin check R10) and is killed by the new assertion (`.ufo/evidence/round-12/gate-mutant-sources-resolve.txt`).
- Gate figures in "Re-measure commands" above are superseded: selftest 268/268 → **269/269**; regression PASS target `e5894387…` → **`538d178b…`** after the third re-cut (`gate-recut-3.txt`, 10/10 KILLED); `--no-live` 29 pass / 0 fail and live 52 pass / 0 fail / 8 notes are unchanged (`gate-*-after.txt`, 2026-10-19).

## Errata (round 13 — re-anchor authority and census scope)

The re-anchor citations in the provenance header and motivating-evidence
paragraph name `omarchy-drift-watch.md:284-287`. That passage governs that
note's omarchy baseline, not the verdict gate's EXPECT/LOCAL inventory.
The governing gate rule is `gate-standing-use.md` §5 rule 4 (:222-226):
“the response is re-verification and an appended erratum.” Its §5 rule 2
also requires re-cutting after changes outside the excised blocks.
This corrects R12-b's owed citation without rewriting the historical entry.
[ref] stays a historical omarchy-method source; round-13 [ref] cites the
actual gate-maintenance rule.

Round 13's exact-set correction is deliberately bounded: it compares root
source-declaration strings and local regular-file `*.conf` membership to
persisted expected lists. It preserves source order and target-existence
checks. Toggle glob expansion requires at least one target; it is **not**
an expected set of toggle filenames. The old “set-blind” statements
describe the round-12 instrument, not the corrected clauses. gkeep's
presence is a recorded baseline, not ownership of its behavior or a ruling
on the operator's long-term intent. Evidence and negative cases:
`.ufo/waves/round-13/measure.py`, the before/after measurements named in
the round-13 SCORECARD, and `corpus/lessons/round-13.md`.
