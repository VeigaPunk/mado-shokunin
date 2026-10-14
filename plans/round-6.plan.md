# WWKD plan — mado round 6 (ufo-round-plan-v1)
Axis move: operability — ONE move, three ordered stages: prove the round-5
gate can fail, then let the proven gate carry its first two watch arms
(freshness: omarchy version drift; coverage: the remaining planes' live
surface). Why now: the round-5 gate ships selftest-green but has never had
a mutant killed, and wwkd orders "a broken earlier gate blocks widening".
Claim:
(a) Mutation proof — via tameshi's harness, consumed read-only (never
    edited; a needed change is a recommendation to tameshi, not a patch).
    Target = the round-5 gate as landed (`tools/mado-verify.sh` per
    plans/round-5; an earlier draft path `corpus/scripts/verify-plane.sh`
    existed — resolve the target from the round-5 commit, not from this
    line). Defect spec = one mutant per declared contract clause, >=8
    defects: verdict token CLEAN|DIVERGED, the UNKNOWN-never-CLEAN arm, the
    exit map, the declared-plane census, sha comparison, reader fallback.
    Suite = the gate's own hermetic selftest exercising `$MUTANT` (not the
    committed path — if the landed selftest cannot take a target path,
    that gap is fixed in-round and recorded):
    `tameshi-shokunin/tools/mutate-and-run.sh --target <gate> --defects
    <spec> --suite 'bash "$MUTANT" --selftest'`; the sweep writes only to
    the harness WORKDIR (scratch) — live config trees are never the target.
    Evidence: `corpus/knowledge/gate-mutation-proof.md` — per-defect
    KILLED/SURVIVED/INCONCLUSIVE + kill-rate headline + control green +
    `MUTATE_RESTORE: OK` (target sha256 before/after). A red control, an
    unrunnable suite, or target drift is a SETUP refusal (exit 2) — no
    headline.
(b) Omarchy version-drift watch arm (rides (a)) — a new declared plane in
    the gate: declared baseline vs live, same verdict vocabulary. Baseline
    measured read-only at draft time (2026-10-14): `omarchy version` ->
    3.8.3; `git -C ~/.local/share/omarchy describe --tags` -> v3.8.4 (HEAD
    8fcc9d60); `~/.agents/skills/omarchy/SKILL.md` 392 L / 14,908 B /
    sha256 `becd149e4d1c0767…` / mtime 2026-10-03 17:42; `omarchy theme
    current` -> Matte Black. Per-pin MOVED|HELD; any MOVED reads DIVERGED
    naming the pin; an unavailable probe reads UNKNOWN, never "clean"; the
    baseline is never edited to match reality. Read verbs only — no
    `git status` on the checkout (it rewrites the index stat-cache; audit
    §3.5).
(c) Remaining-planes live-surface arms (ride (a)) — declared-vs-live rows
    where the pair exists (gate planes), runtime rows otherwise, all in a
    new note (working name `remaining-planes-live.md`): terminals runtime
    (alacritty x2 live today; `general.import` -> theme `alacritty.toml`
    chain); theme/wallpaper consumption (swaybg consumer; mako symlink);
    display behavior (hyprsunset absent / identity profile;
    xdg-desktop-portal-hyprland consumer; monitors already covered r2).
    Idle transitions stay UNKNOWN by constraint (MADO-R4-2) — not widened.
Ordering: (b) and (c) are gated on (a); if the gate cannot be
mutation-proven, the round stops at (a) and says why.
Anti-claim: a surviving mutant is a FINDING (selftest gap, recorded, not
smoothed); any unverifiable check reads UNKNOWN, never CLEAN; no widening
ships unproven.
Measure: kill-rate table + restore proof + target sha; per-pin drift
verdict vs the baseline above; per-plane live rows; gate census before ->
after. Draft-time pins are the watch's input, not its output — re-measure
at dispatch.