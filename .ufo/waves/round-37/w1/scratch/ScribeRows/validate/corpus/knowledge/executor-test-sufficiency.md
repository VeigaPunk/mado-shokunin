# MADO-R3-4 — no-oral-context executor test: SKILL.md sufficiency

**Assignment (round 3, probation-completing):** an executor lane with no oral context reads
`SKILL.md` only and verifies ONE hyprland-plane config claim end-to-end — file bytes AND
hyprctl — recording per-step sufficiency. Executor lane MADO-R3-4; the only file written
outside scratch is this note; scratch `/tmp/mado-r3-4/` (logs named below); substrates
read-only; no network access.

## Test condition (measured)

| version | sha256 (first 12) | `wc -l` | observed | role |
|---|---|---|---|---|
| round-2 | `7b5289194353` | 240 | 14:38Z | pre-poll baseline |
| round-3 upgrade | `016ecd68b3f6` | 374 | landed 14:44:24Z | **tested version — every step below ran against this** |
| post-pass write 1 | `9989c50c5d9b` | 376 | 14:53:40Z | version-pins paragraph +2 lines (Omarchy two-pin split) |
| post-pass write 2 | `2ed6f01934fd` | — | mtime 14:56:21Z | seen only; not captured |
| post-pass write 3 | `7fd63c912e43` | 395 | captured ~14:57Z → `/tmp/mado-r3-4/skill-7fd63c91.md` | severity scale replaced (S1/S2/S3), `layers` verb added, sibling round-3 notes integrated |

- Poll: sha256 every 20 s, 20-min cap, start 14:40:56Z; detected the upgrade 200 s in
  (`/tmp/mado-r3-4/poll.log`, `landed.sha`). Verification ran 14:46:00–14:52:10Z against
  `016ecd68…`; the file was read from no other version mid-pass. [OBS]
- The document is under active integration by its owning lane (≥4 writes between 14:44Z and
  14:57Z). A single-pass executor must pin the sha it reads — this pass did (sha logged
  before/after); any reuse should pin again. [OBS]
- Constraint record [OBS]: the only mado domain source read for this pass is `SKILL.md`;
  no other corpus note was read (sibling round-3 files `waybar-walker-semantics.md`,
  `config-health-report-r3.md` were present in `corpus/knowledge/` but unread). Fleet meta
  (dispatch text, `plans/round-3.plan.md`, `LOG.md`, `AGENTS.md`, `PROVINCE.md`) served the
  harness only and is not a source of any verification step. Substrate bytes were read as
  evidence, per the SKILL's own method. No mutating verb invoked — hyprctl reads used:
  `version`, `configerrors`, `instances`, `getoption` only. Session material shape-only
  (`printenv HYPRLAND_INSTANCE_SIGNATURE | cut -c1-12`; never full). All artifacts under
  `/tmp/mado-r3-4/`.

## Claim under test — `SKILL.md:46-50` (tested version `016ecd68`)

> Measured, not recited: `hyprctl getoption general:gaps_out` → `custom type: 0 0 0 0` —
> owned by the *toggle* `window-no-gaps.conf`, not by user `looknfeel.conf` (wholly
> comment-only) and not by the default (`gaps_out = 10`, default looknfeel:10).

(the paragraph continues with the `input:kb_layout` half — claim #2, NOT tested; one claim
per assignment). In-file cross-checks used: expected sample `:259`; worked-example row `:280`
— both list the same `gaps_out` values this pass measured independently. In the latest
capture `7fd63c91`, the claim text is unchanged (now `:48-51`) and the worked-example row
differs only in its severity cell (tested: S1 → latest: S3, scale was replaced post-pass).

## Result row (executor pass, 2026-10-14 14:46–14:52 UTC)

| # | Claim | Route (class) | Declared side (anchor) | Live side (probe → value) | Class | Sev (as tested) | Tag |
|---|---|---|---|---|---|---|---|
| 1 | Effective `general:gaps_out` | hyprctl live | default `~/.local/share/omarchy/default/hypr/looknfeel.conf:10` = 10; state toggle `~/.local/state/omarchy/toggles/hypr/window-no-gaps.conf:3` = 0; user `~/.config/hypr/looknfeel.conf` zero active keys | `hyprctl -j getoption general:gaps_out` → `{"custom":"0 0 0 0","set":true}` | `agreement*` — toggle owns | S1 note (tested scale `:154`; = S3 informational under the post-pass scale, which the current worked example itself now uses) | [OBS] |

**Substrate byte-identical before/after (sha256), pass 2026-10-14.** User set (13/13 lines
— 12 `*.conf` + 1 `*.bak.*`) and chain set (38/38 lines — 35 default-tree `*.conf` + 2
state toggles + theme `hyprland.conf`) both `diff`-clean on two re-runs (14:49:02Z,
14:50:14Z). `hyprland.conf` pass-side sha equals the SKILL-embedded pin (`:285` tested;
`:295` latest), by mechanical extract-and-compare → MATCH
(`4f52854a3c143dcf58430a679e339619223d2b5008115a322d06b2de637ea462`). The SKILL's "all 13
`~/.config/hypr` files" reconciles: dir entries = 13 = 12 `*.conf` + 1 `*.bak.*`. No
compositor state mutated.

## Declarer census for `general:gaps_out` (file bytes + sweeps)

| File:line | Contains | Key namespace | Reachability |
|---|---|---|---|
| `~/.local/share/omarchy/default/hypr/looknfeel.conf:10` | `gaps_out = 10` (inside `general {` at :8) | `general:gaps_out` | sourced (`hyprland.conf:10`) |
| `~/.local/state/omarchy/toggles/hypr/window-no-gaps.conf:3` | `gaps_out = 0` | `general:gaps_out` | sourced (`hyprland.conf:23` glob) — **last declarer → owner** |
| `~/.local/share/omarchy/default/hypr/looknfeel.conf:66` | `gaps_out = 0` (inside `group {` :50 → `groupbar {` :56) | `group:groupbar:gaps_out` — a different option (probe → `{"int":0,"set":true}`) | sourced, but not this claim's key |
| `~/.config/hypr/looknfeel.conf:7` | `# gaps_out = 0` | — (inert comment) | sourced (`:19`), no active declaration |
| `~/.local/share/omarchy/default/hypr/toggles/window-no-gaps.conf:3` | `gaps_out = 0`, byte-identical to the state toggle (`diff` empty; both 135 B) | `general:gaps_out` if reached | **no `source` reaches it** — unreached copy |

Sweep scope: default tree recursive (35 `*.conf`), `~/.config/hypr/**` (12 `*.conf`), state
toggles dir, entire theme dir (25 entries; `theme/gum.env.conf` is reachable via
`default/envs.conf:3`). Chain depth measured beyond the 17 top-level statements — nested
`sources` exist: `windows.conf:12 → apps.conf:2-19 → apps/*.conf`; `default/bindings.conf:14-16`;
`envs.conf:3 → theme/gum.env.conf`; `hyprlock.conf:1`. No other `gaps_out` occurrence
anywhere in these trees. Precision note: the Config-plane map's defaults-layer `*` (`:42-44`
tested) is a layer summary — `hyprland.conf:4-12` is 9 explicit `source` lines; the
recursive sweep covered the whole tree either way.

## Per-step sufficiency

Classes (pre-registered in `/tmp/mado-r3-4/rubric.md` BEFORE the landed SKILL was read, so
they could not be tuned to the outcome): **SUF-EXPLICIT** — SKILL states path/command/
procedure verbatim; runs with zero outside domain knowledge. **SUF-DERIVED** — step composes
facts the SKILL states; no outside domain knowledge. **GAP** — needs something the SKILL
does not carry (each listed in §Gaps with its in-pass resolution).

| Step (checklist `:238-276` tested) | SKILL supplied (anchor, tested version) | Executed | Observed | Class |
|---|---|---|---|---|
| 0 scope | claim literal `:46-50`; `:239-240`; worked row `:280` | claim picked pre-landing, re-confirmed against landed text | identical claim, same expected values | SUF-EXPLICIT |
| 1 scratch | `:241-242` (`mkdir -p /tmp/mado-verify-$(date +%s)`); rule "`/tmp/<lane>-*`" `:226` | `mkdir -p /tmp/mado-r3-4/` (dispatch namespace) | all artifacts inside; nothing in config trees | SUF-EXPLICIT (namespace substitution; rule satisfied) |
| 2 baseline | `:243-245` exact command | ran verbatim; extended per "scope's other files" to the resolved chain | 13 hash lines (12+1), rc=0 both globs; chain list 38 lines | SUF-EXPLICIT; extension SUF-DERIVED |
| 3 env gate | `:246-255` five conditions | all five, first run | `/usr/bin/hyprctl`; `Hyprland 0.56.2 … efb5099…`; `configerrors` empty rc=0; instances 1; signature shape-checked (12 chars, never full) | SUF-EXPLICIT — 1 microgap (jq) |
| 4 map owners | `:256-257` method; chain map `:42-44`; inert-comments clause `:116` | 17-statement resolve; per-file declarer walk in source order; recursive sweeps; chain-depth check; namespace probe for the one ambiguous hit | census above; owner = state toggle | SUF-DERIVED — 1 mild gap instance (block scope; resolved in-pass) |
| 5 live pass | `:258-261` commands + expected sample | `hyprctl -j getoption general:gaps_out`; human form | `{"custom":"0 0 0 0","set":true}`; `custom type: 0 0 0 0` / `set: true` — exact match | SUF-EXPLICIT |
| 6 consumer probes | `:262-264` | N/A — the claim's key has a hyprctl surface | — | N/A |
| 7 classify | vocab `:139-146`; severity `:148-157` | applied (tested scale) | `agreement*` (last declarer = live value; earlier declarer 10 provably shadowed); S1 note | SUF-EXPLICIT |
| 8 boundary | `:266-268`; worked example `:284-286`; embedded pin `:285` | before/after diffs ×2 (user set, chain set); pin extract-and-compare | both `diff` empty; pin MATCH | SUF-EXPLICIT (before/after) — 1 gap (cross-check target, §Gaps 3) |
| 9 report | `:269-274` format + boundary sentence | result row produced above | row classed, severity tagged, boundary stated | SUF-EXPLICIT |

Definition-of-done check (`:235-237` tested): every claim a classed row with two anchored
sides ✓ (1 row); finding severity ✓; substrate byte-identical ✓; unknowns listed ✓; every
command named ✓ (logs `/tmp/mado-r3-4/s2-baseline.log`, `s3-env-gate.log`, `s4-chain-walk.log`,
`s4e-context.log`, `s5-live-s8-boundary.log`, `s4k-s8final.log`, `s4m-s4n.log`).

## Gaps (each with its in-pass resolution)

1. **jq dependency unnamed** (step 3, micro). The gate line `… | jq length` requires jq;
   the SKILL names jq nowhere, and "any fail → UNKNOWN" would fire on a jq-less host for a
   reason unrelated to hyprctl reachability. Present here (`/home/vgpnk/.local/bin/jq`) →
   passed. Resolution an executor finds: `command -v jq` first.
2. **Block-scope key namespacing not stated** (step 4, mild — 1 measured instance).
   "Grep each claim's key" as written over-collects: a literal `gaps_out` grep returns
   `default looknfeel.conf:66` (inside `group { groupbar { } }`) and user `looknfeel.conf:7`
   (comment). The comment is resolvable from in-file concepts (`:116` names inert commented
   lines); the groupbar hit is NOT — it is a different option namespace, and the SKILL never
   states that nested blocks extend a key's path. If over-collected, the default file appears
   to resolve to 0 internally and the "toggle owns" attribution looks redundant — the wrong
   reading predicts the same live value, so the step-5 probe cannot catch it. Resolved
   in-pass: block headers read literally (`group {`, `groupbar {`), a colon-path precedent
   exists in the SKILL itself (`input:touchpad:scroll_factor`, `:260` — a nested-block path),
   and the namespace probe confirms (`hyprctl -j getoption group:groupbar:gaps_out` →
   `{"int":0,"set":true}` — a real, separate option). For THIS claim the owner verdict is
   unaffected either way (the toggle is the last declarer of `general:gaps_out` regardless).
   Suggested line for the SKILL lane: state that nested blocks extend the getoption path.
3. **Boundary cross-check target partly outside the file** (step 8). The step says the 13
   files are "byte-identical to MADO-1 §2" — MADO-1 is not readable under the SKILL-only
   constraint. Executable parts: before/after self-identity (done — both diffs empty) and
   the single full pin embedded at `:285` (`hyprland.conf` → MATCH). The other 12 files'
   equality to MADO-1 §2 cannot be re-derived from SKILL alone; an executor can only assert
   "unchanged during this pass".
4. **(Informational)** no-arg `hyprctl getoption` is not an option-enumeration surface in
   0.56.2: `hyprctl -j getoption` (no key) → not JSON (jq parse error); human no-arg → 1
   line, no option rows. Per-key probes are the surface; the SKILL only ever gives the
   per-key form, so nothing is wrong — noted so an executor does not burn a step trying to
   enumerate.

## Sufficiency verdict

**Sufficient, end-to-end, against the version read.** With `SKILL.md` as the only domain
source, the claim was reproduced to a classed (`agreement*`), severity-tagged,
boundary-proven row with zero mutations to any config tree; every expected value the file
carried (live sample, worked-example row, probe-table sample) matched the measured bytes
exactly, and the declarer census found no drift between SKILL text and host state for this
claim.

Carried caveats: two small process gaps (jq unnamed; block scope unstated — both resolved
in-pass) and one cross-check-target limitation (MADO-1 §2). The SKILL's anti-claim branch
was NOT exercised — the live layer was reachable and all five env-gate conditions passed
first run, so the file-byte fallback recipe stays UNKNOWN for operability.

Versioning caveat: the document changed ≥4 times within 13 minutes of landing (pins,
severity scale, evidence classes, `layers` verb). The claim text, checklist steps, and
worked-example values were re-checked byte-identical in the latest capture (`7fd63c91`,
395 L); only the severity label for this row moved (S1 → S3) because the scale was replaced
by the lane's own integration. The sufficiency verdict therefore carries for the tested
version's method; the round commit should freeze a SKILL sha and re-point this note's line
anchors at it (find-by-text: "Measured, not recited").

## OBS / INF / UNK

[OBS] — poll: `7b528919…` (240 L) → landed `016ecd68…` (374 L) at 14:44:24Z; post-pass
`9989c50c…` (376 L, 14:53:40Z), `2ed6f019…` (mtime 14:56:21Z), `7fd63c91…` (395 L, captured).
Env gate five-for-five at 14:46:00Z. `hyprctl -j getoption general:gaps_out` →
`{"custom":"0 0 0 0","set":true}`; human `custom type: 0 0 0 0` / `set: true`.
`group:groupbar:gaps_out` → `{"int":0,"set":true}`; `general:group:groupbar:gaps_out` →
`no such option`. Bytes: default `looknfeel.conf:10` = 10 (143 L file); state toggle `:3` = 0
(135 B, 10 L); user `looknfeel.conf` 40 L, 10 non-comment non-blank lines (empty-block braces
only), `:7` commented; default-tree toggle copy 135 B, `diff`-clean vs state copy, no `source`
reaches it; theme dir 25 entries, no `gaps_out`; nested sources as listed above. Boundary:
user set 13/13, chain set 38/38, both `diff` empty on two re-runs; `hyprland.conf` sha =
SKILL-embedded pin (MATCH). `hyprland.conf`: 29 L, 17 `source` statements, zero settings of
its own (incidental corroboration of `:38`). Unreached user files: `envs.conf`,
`hypridle.conf`, `hyprland.conf` (root), `hyprlock.conf`, `hyprsunset.conf`, `xdph.conf`.

[INF] — `agreement*` / "toggle owns" are composites over the measured trio: declaration
order (chain map + source order), declared values (10 vs 0), live value + `set` flag
(0 0 0 0, set true). The severity mapping for ownership proofs is the SKILL's own reporting
convention (tested `:154`; latest `:156-158` re-labels it S3). "No drift for this claim" is
an inference over the complete census above (falsified by any new declarer).

[UNK] — (1) operability of the file-byte fallback branch (not exercised); (2) whether the
`omarchy` CLI consumes the unreached default-tree toggle copies (consumer-side, outside the
Hyprland chain; not probed); (3) semantics of the no-arg `getoption` dump in 0.56.2 (not
needed for this claim); (4) generalization — how many other keys exhibit the same
literal-grep over-collection pattern (not swept); (5) the final committed round-3 SKILL sha
(file still being written at note-landing time).

## Errata (append-only)

- (none at landing — 2026-10-14)- 2026-10-14 (post-landing errata, MADO-R3-4): a further external write of `SKILL.md` was
  observed at 14:57:22Z — sha256 `ef4c29e3374c0ed0e5dc80f5e58bce15441666de210015cc02b68c991a607e22`,
  396 L by `wc -l`. Spot-check at that sha: claim text present unchanged at `:48-51`;
  worked-example row 1 (now `:291`) still carries the measured values with its S3 label;
  the embedded `hyprland.conf` pin is present. The version ledger above and its UNK (5)
  stand as written; per append-only discipline this errata adds the observation only.