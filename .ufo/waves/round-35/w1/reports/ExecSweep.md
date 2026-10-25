# ExecSweep — corrections sweep (round-35, 2026-10-24)

Scope: grep of `corpus/` and `SKILL.md` for statements contradicted by this round's
host re-opens (`fetch/S203–S210.receipt.txt`, all dated 2026-10-24). Read-only; no
file was edited. Sweep ran `hypridle` and `first.?run|first run|never asks` patterns
over both trees, then cross-filtered hypridle hits for `not running | absent |
inactive | no PID | no match | no consumer | the daemon is`.

## The round's contradicting evidence

- **S205**: `/usr/bin/hypridle` runs as **PID 1667**; user journal holds two
  `Started hypridle.` lines in the current session (Oct 23 13:25:00 and 22:14:11 —
  a restart, not a first start); `systemctl --user is-active hypridle` → `inactive`
  (unit probe is a probe artefact: the daemon runs inside a transient scope, not as
  the `hypridle` service). `hypridle.conf` still declares 150 s/152 s and is
  byte-identical (`e7d3b8dd…`).
- **S203/S204**: `install/first-run/` lists **12 scripts**; the `omarchy-first-run`
  body runs all 12; none is idle-lock; `journalctl --user` shows **0**
  `omarchy-toggle` invocations.
- **S206–S210**: the idle-lock choice is offered live (waybar
  `custom/idle-indicator` `config.jsonc:207-208`, `idle.sh:3-6`, `omarchy-menu:207,212`,
  handler present in all 4 dated config.jsonc copies, 0 idle-lock entries in
  `toggles/hypr/`).

## Result: `first-run` + `12`/`never asks` pattern — zero corpus/SKILL.md hits

No statement in `corpus/` or `SKILL.md` joins `first-run` to `12`, `twelve`,
`never asks`, `never offers`, or `no choice`. The only `first run` hits
(`executor-test-sufficiency.md:94,151`, `lessons/round-22.md:86`) mean "first
attempt at running a command," unrelated to `omarchy-first-run`. The "the desktop
never offers the choice" framing lives only in this round's own staging drafts
(`.ufo/waves/round-35/controls/golden/corpus/knowledge/idle-lock-never-asked-r12.md`,
which self-corrects it). **Nothing to errata on this axis.**

## Result: `hypridle` + absence pattern — verdicts by line

Rule applied: a claim is **dated** if it is explicitly qualified to a probe window,
round record, or past-tense epoch (true as written, superseded by state); it is
**falsified** if it asserts the absence as current/expected fact or embeds it as
normative guidance a future reader will act on.

### FALSIFIED — needs appended errata

| file:line | statement | why falsified |
|---|---|---|
| `SKILL.md:297` | Verification recipe step 6 expects `systemctl --user is-active hypridle` → `inactive`; `pgrep -x hypridle` → `empty`. | Normative expected-output: a re-runner today gets `pgrep` → `1667` and would record a divergence that is the armed, healthy state. S205 also proves the `is-active` row is a probe artefact, not a state read. Errata: process probe is authoritative; `inactive` coexists with a live pid. |
| `SKILL.md:369` | FAQ "Will the session lock after idle?" — "the declared 150 s/152 s chain has no consumer while hypridle is absent (S1, F1) — it cannot fire." | Operative guidance asserts cannot-fire under a premise that no longer holds: the daemon runs (PID 1667, armed since Oct 23 22:14). Correct answer today: the chain is armed; whether it fires stays `[UNK]` (no transition observed — consistent with golden `idle-lock-chain-armed-r14.md` §3). |
| `SKILL.md:82` | Idle-timings routing row: "`pgrep -x hypridle` — no match at the round-3/4 probes; volatile: restarted with the 16:11Z session, absent again by 16:24Z." | The only re-measure recorded is absent-by-minutes; a reader infers absence is the steady state. S205 measures presence sustained across ~9 h between two Oct-23 start lines and still live Oct-24. Dated clauses inside the row stand; the row needs an append, not a rewrite (append-only). |
| `corpus/knowledge/hyprland-config-plane.md:203` | §12 open item 2: "Why hypridle is absent from the process tree (see §10)." | Carried as an open question while the referenced state has moved twice since (E2-cycle, now armed). Errata should mark it epoch-bound and note S205's armed reading narrows it further (absence episodes remain `[UNK]`-caused). |

### DATED — record stands; optional append for discoverability

| file:line | statement | class rationale |
|---|---|---|
| `SKILL.md:175` | S1 severity exemplar: "F1: hypridle absent → … has no consumer." | Explicitly cited as `MADO-R3-2 §6 F1` round record; true of its probe window. Optional: no current-state severity row exists — no counterexample needed, but a pointer append would keep the severity table honest. |
| `SKILL.md:216-217` | Probe-tool table: "hypridle/hyprlock absent"; "hypridle → `inactive`". | Rows are labeled historical samples (waybar 1707, mako 1706 — epoch PIDs). Stale sample, not a claim. Optional append: note `is-active` is a probe artefact per S205. |
| `SKILL.md:708` | "Re-verified anchors in this pass: … hypridle inactive + no PID" | Dated round-3 pass record ("in this pass", 14:40–14:45 UTC context at :700-704). |
| `SKILL.md:975` | "hypridle absent again (F1-class)" | Summarizes a dated census note; already qualified with the F1-class instability flag. |
| `corpus/knowledge/hyprland-config-plane.md:187-191` | §10 runtime snapshot: "`ps …` → no match … hypridle is not running in this session." | Probe-window `[OBS]`, self-flagged `[UNK]` cause; `idle-lock-plane.md` E1 + E2 already re-measured and labeled it a point sample. |
| `corpus/knowledge/hyprland-config-plane.md:268` | §13 tail: "hypridle absent + `inactive`." | Point-sample digest of §10; same epoch. |
| `corpus/knowledge/idle-lock-plane.md:51-54` | §1: "At probe time **hypridle is not running** … the two timers cannot fire in this session as it stands." | Explicit "at probe time" / "as it stands" qualification; E2 already appended the turnover correction. |
| `corpus/knowledge/idle-lock-plane.md:243-247` | §7: "no match … the declared chain … is inert in this session at probe time." | Session-scoped. |
| `corpus/knowledge/idle-lock-plane.md:287,322,329` | `idle.sh` renders glyph "exactly when hypridle is absent" (:287); E1 cross-check "held (still absent)" (:322); §11 UNK-1 "Why hypridle is not running" (:329). | :287 is file-semantics (true of `idle.sh` regardless — corroborated verbatim by S207 re-open); :322/:329 are probe-window records. :329 is the corpus-side twin of the falsified `hyprland-config-plane.md:203` open item — same optional append. |
| `corpus/knowledge/config-health-report-r3.md` | `:72` table row, `:175-177` findings, `:285-315` F1 block, `:301` "has no consumer, so it cannot fire", `:443`, `:481`, `:570-577` E3 cycle, `:890-892` re-run recipe, `:924` verdict rule, `:949`, `:985` | All carry the 2026-10-14 probe window or F1/E3 state-moved caveats; `:924`'s re-run rule ("Present → STATE-MOVED … expect either; do not fail") already anticipates S205's outcome — the report's own machinery covers today's reading. |
| `corpus/knowledge/waybar-walker-plane.md:34-35,108,347-348,406` | "no matching PID at measure time"; `idle.sh` semantics; §7 item 6; R2-E4 "hypridle absent + `inactive`" | Measure-time qualifiers throughout; :108 is script semantics, re-verified by S207. |
| `corpus/knowledge/waybar-walker-semantics.md:139` | `custom/idle-indicator` row: glyph "when hypridle is **absent**"; live read `pgrep -x` empty | Dual: script semantics (true) + a dated live-read sample. |
| `corpus/knowledge/arc-synthesis.md:233,298,303,328,338-339` | "hypridle/hyprlock/hyprsunset **absent** in the current session … no consumer while absent" | Epoch language ("current session") tied to the r3/r4 records it cites. The one residual risk — a reader missing the epoch — is mitigated by the row's own `pgrep -x` probe citation. Optional append. |
| `corpus/knowledge/closeout-r11.md:47` | "hypridle/hyprlock/hyprsunset **absent**; the declared 150 s/152 s chain has no consumer (F1, S1)" | Closed round-11 record, cited to `pgrep -x` + r3/r4 records. |
| `corpus/knowledge/remaining-planes-census.md:241-243` | "hypridle absent as a process again (F1-class)" | Census probe-window record. |
| `corpus/knowledge/idle-lock-route-r17.md:132` | UNK: "Why hypridle was not running at the 2026-10-14 probe" | Past-tense, probe-qualified; S205 does not answer the Oct-14 question. No errata needed. |
| `corpus/knowledge/province-accuracy-selfaudit.md:175-179,229,249-251,308,344` | hypridle lifecycle/toggle recheck rows | Dated audit timeline. |
| `corpus/README.md:12,13,18` | Index summaries embedding "hypridle `inactive` + no PID", "hypridle absent (F1)" | Each row is labeled with the note's measured date; index convention already treats these as note summaries. Optional: README errata convention is a dated addendum row — low value. |

## Bottom line

- **4 statements are falsified** and would mislead a consumer acting on them today:
  `SKILL.md:297` (recipe expected-output), `SKILL.md:369` (cannot-fire guidance),
  `SKILL.md:82` (routing row missing the armed era),
  `corpus/knowledge/hyprland-config-plane.md:203` (open item on a moved state).
  SKILL.md has no errata section in-body; its convention is dated round records, so
  the correction belongs in a new round-35 knowledge entry (the staged
  `idle-lock-chain-armed-r14.md` already carries it) plus an appended line if the
  sweep verdict requires in-place notice.
- **~30 statements are dated**: true for their probe window, superseded by S205's
  armed reading; errata optional, highest value on `idle-lock-plane.md` §11 UNK-1
  (:329) and `arc-synthesis.md:233`.
- **Zero** `first-run`/`12`/`never-asks` errata — the contradictable framing never
  reached the committed corpus.
