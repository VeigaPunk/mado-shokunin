# ScoutFleetPolicy — round 17 w2, scoped findings

**Question:** which *open* lines in the fleet L0 queue mention `mado`, host recovery,
`pacman` or `libinput`, so L1 cites the existing operator question instead of filing a
duplicate.

**Verdict:** four lines qualify (L37, L54, L55, L57). The controlling host-recovery
question is **L54**, requested for resolution by **L55**; **L57** is third-party
corroboration that the question is operator-owned and the pause is in force. **L37** is
mado's only authored line and is unrelated to host policy. No line carries an `L0 ANSWER`
for host recovery. A new mado r17 L0 row on this topic would duplicate L54/L55.

## File identity (observed)

- Path: `/home/vgpnk/Projects/shokunin/.ufo/l0-questions.md` (read-only; not modified)
- `sha256 = 6e0b0fad82c8fb1099971f249b129c05bd0c064d2824cf0a596d56670e2ddf1b`
- `58` lines, `46277` bytes, mtime `2026-10-20 11:15:13.864129286 -0300`
- Append-only relaunch marker at **L23** (`--- 2026-10 relaunch ---`); all four hits sit
  in the relaunch section (L24–L58), so none is stale pre-relaunch history.
- Method: whole-file read plus case-insensitive literal census
  (`grep -in` for `mado|pacman|libinput|host recovery|HOST PARTIAL|pacman transactions|mkinitcpio`),
  followed by `L0 ANSWER` marker census and exact-line reads of L37, L54, L55, L57.

## Keyword census (exact line numbers at the sha256 above)

| keyword | lines |
|---|---|
| `mado` | 37, 54 |
| `pacman` | 54, 55, 57 |
| `libinput` | 54, 55 |
| `host recovery` / `HOST PARTIAL` | 54, 55 |
| `mkinitcpio` | 55 |
| `L0 ANSWER` markers | 52, 53 only (planner taxonomy — no host content) |

No host/pacman/libinput hit exists in L1–L22 (pre-relaunch) or anywhere else.

## Open lines, itemised

### L37 — `mado | round-1` — OPEN, but NOT host policy

Ratification of the relaunched round namespace, bounded score rubrics and native craft
dispatch shape. Records coverage `8/22`, gate capability `268/268`, and the
planner-outside-wave-taxonomy mapping. Contains no `pacman`, `libinput` or host-recovery
text. Ending: "work continues under the explicit steer. Integrator owns durability of this
append-only question." No answer marker.

**Use:** citable only as mado's standing namespace/dispatch question. Do not fold a
host-policy question into it; do not cite it as host evidence.

### L54 — `hyaku-orchestrator | 2026-10-20 | HOST PARTIAL UPGRADE during mado r15` — OPEN (controlling entry)

The only line that both names mado and carries the incident. Records:

- seat ran `pacman -S --needed --noconfirm libinput libinput-tools` at `pacman.log:2429`
  `04:25:16`; libinput `1.31.3-1 -> 1.32.0-1`;
- host is 413 packages behind a sync DB taken `2026-10-18 14:11` (pre-campaign);
- soname `libinput.so.10` unchanged, `ldd -r` 0 unresolved, aquamarine links it; running
  Hyprland keeps 1.31.3 until restart;
- not reverted, explicitly an **operator call**, with three options: keep 1.32.0; revert
  from `/var/cache/pacman/pkg/libinput-1.31.3-1-x86_64.pkg.tar.zst` (requires removing
  `libinput-tools`); or full `-Syu` through tsukuroi's `/sysroot` update-safety gate;
- standing rule text: lanes dry-run every install (`pacman -Sp`) and refuse any upgrade of
  an installed package.

Status: no `L0 ANSWER` marker follows; the row itself defers to the operator. **This is
the line to cite as the host-recovery decision.**

### L55 — `tsukuroi | round-15 | Host recovery and tooling-policy decision` — OPEN (the resolution request)

Explicitly asks the operator to "resolve the existing hyaku-orchestrator HOST PARTIAL
UPGRADE recovery choice and consider a host-wide pause on all pacman transactions until an
operator-owned recovery/update plan clears the mkinitcpio42 hook compatibility risk."
Retains a read-only capture at `2026-10-20T07:44:39Z` (libinput/libinput-tools `1.32.0-1`,
413 pending `pacman -Qu` rows against October-18 metadata) and states "no
running-version/UI/ABI or repair verdict" exists. Legislates that the installed-name
dry-run guard "is necessary but not clearance: all-new targets can still combine newer
binaries with unversioned older dependencies, and `--needed` is not a no-upgrade switch."
Evidence: `tsukuroi-shokunin/corpus/knowledge/partial-upgrade-recheck-r15.md` and
`.ufo/waves/round-15/build/host-snapshot.json`. Tsukuroi performs no package/service action.

Status: open; no answer marker. **This is the line that asks for the pause, not a separate
question.**

### L57 — `kaidoku | round-16 | Supersedes the round-16 question opening "Host routing/credit repair requested"` — OPEN reference

The row is about routing/credits (scout/labrat→m_fast, connector→m_haiku, critic→m_opus;
32/32 seats completed). Its host-relevant sentence, verbatim: "The separate shared
host-recovery question remains operator-owned; all pacman transactions are paused and this
lane performs none." It supersedes **L56** (the dead-seat/credit row), not any host row.

**Use:** corroboration that (a) the host-recovery question is not lane-owned and (b) a
fleet-wide pacman pause was already announced by 2026-10-20. Not a host question itself.

## Incident anchor re-verified (observed, file bytes)

`/var/log/pacman.log` read as bytes only:

- L2429: `[2026-10-20T04:25:16-0300] [PACMAN] Running 'pacman -S --needed --noconfirm libinput libinput-tools'`
- L2432: `[ALPM] upgraded libinput (1.31.3-1 -> 1.32.0-1)`
- L2436: `[ALPM] installed libinput-tools (1.32.0-1)`

This matches L54's citation exactly (line number, command, version pair). Confidence:
high — direct byte-level agreement between the L0 claim and the log.

## Citation guidance for L1

1. Cite **L54** (incident, checked facts, three operator options) + **L55** (pause request
   and the "dry-run is not clearance" rule) as the existing host-recovery operator
   question. The round-17 prompt (`/home/vgpnk/Projects/shokunin/.ufo/prompts/mado-round-17.md`
   L274–L280) already names "the host-recovery L0 question" as the condition for lifting
   the pause, so citing L54/L55 closes that loop without a new row.
2. **Do not append a new L0 line restating** the incident, the three options, the 413-package
   delta, or the pause. That is duplication of L54/L55.
3. If a genuinely new mado r17 fact exists (not present in this scout's read scope), it may
   be appended only in the file's format `<lane> | round-<N> | <question>` and must cite
   L54/L55 as controlling rather than re-asking them. The fleet file is append-only.
4. Do not cite **L37** as host policy (different question), **L52–L53** (planner taxonomy;
   only answered rows in the file), **L56** (dead-seat/credit, superseded), or **L58**
   (kama llama.cpp fixture ratification — install-adjacent, unrelated to pacman host
   recovery).

## Cross-check against wave 1 (observed)

`.ufo/waves/round-17/w1/reports/ReportSkeleton.md:42-49` already lists L54/L55 as the
controlling host entries and states that wave 1 adds no L0 line. This census independently
confirms those line numbers and adds the exact open/answered status: L52–L53 are the only
`L0 ANSWER` rows; L54, L55, L57 carry none. No errata to the skeleton are required.

## Confidence and gaps

- Observed (high): keyword line numbers, open/answered status, file identity, pacman.log
  anchor agreement, prompt wording at L274–L280.
- Inference (labelled): L54 is the row the prompt's singular "host-recovery L0 question"
  refers to; L55 is its resolution request rather than a second question. Supported by L55
  naming L54 explicitly ("resolve the existing hyaku-orchestrator HOST PARTIAL UPGRADE
  recovery choice"), but there is no line-number cross-reference in the prompt itself.
- Unresolved: whether the operator has answered off-file (e.g. in a session not represented
  in this append-only queue). The queue shows no answer; nothing beyond the queue was
  consulted.
- Scope limits: read-only; no lane files besides this report were written; no git/jj
  commands; no live probes.

## Tool installs

**none** — nothing installed or updated by any channel; no `pacman`, `sudo`, `uv`, `npx`,
`pip` or `cargo` invocation. The round-17 host pause was respected throughout.
