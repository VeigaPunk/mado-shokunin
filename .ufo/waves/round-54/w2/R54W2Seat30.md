# R54W2Seat30 — C2 S377 province boundary: generated systemd unit naming

## Finding

**S377 is an out-of-province unit-state fact, not evidence within mado's owned launcher-half surface.** The frozen C2 contract explicitly places the coverage move on the P1/P6 chain's launcher half (`claims-frozen.md:46-53`), but the S377 quote is implementation detail for a generated systemd unit name. PROVINCE routes unit-state ground away from mado: line 34 says `tools/mado-verify.sh`'s unit-state rows sit next to tsukuroi's unit-health ground, “which stays tsukuroi's”; line 36 states “Out of province → report, never absorb.” This makes the S377 evidence a concrete instance of the province boundary concern already raised in w1, rather than a new defect in the frozen text.

## Frozen contract and exact pin evidence

`registration.md:61-69` freezes S377 as source row `code`, scope `uwsm-app environment/launch contract`; line 65 quotes exactly:

> `unit_name = f"app-{desktop_unit_substring}-{cmd_unit_substring}-{random_hex(8)}.{app_unit_type}"`

and locates it at `uwsm-0.27.1-main.py:3714`.

The pinned source at `.ufo/waves/round-54/fetch/uwsm-0.27.1-main.py:3661-3669` constructs desktop and command substrings when no unit name is supplied; lines 3671-3711 truncate them to fit the unit-name limit. At **line 3714** it generates the `scope` name with a random suffix; **line 3716** generates the `service` variant with `@{random_hex(8)}`. Thus the frozen quote is exact and points specifically to generated naming, not the launcher declaration itself. The execution at line 3770 passes the generated `unit_name` as `--unit=...`; this further identifies the fact as systemd unit activation/naming behavior. This is source-only evidence; no unit or host state was read.

## Scope application

The contract's “launcher half” (`claims-frozen.md:48-53`) can cover the fact that the owned launch declarations invoke `uwsm-app`; it does not transfer ownership of uwsm's downstream generated systemd unit naming. PROVINCE line 34's named boundary is explicitly about **unit-state rows**, so the exact S377 fact is within that routed category. The adjacent line 36 gives the operative instruction: report such ground, do not absorb it. On this evidence, including S377 as a scored owned-chain proposition risks crediting mado for systemd unit-state ground outside its province. S377 may remain a boundary citation clearly labeled not absorbed, but should not substantiate the lane's coverage claim without a pre-score province refinement assigning this read-only documentation ground.

## Relevant wave-1 evidence

`w1/R54Seat26.md:100-121` independently identifies S377 as transient app **unit** naming (scope/service), applies `PROVINCE.md:34` and `:96`, notes the landed entry repeats the generated-name fact at line 13 while disclaiming any unit/process probe at line 17, and concludes that two of three facts are session-manager/unit-state ground not owned or measured by mado. Its proposed boundary treatment explicitly includes S377. This report narrows that finding to S377's exact pin span and the unit-name generation/dispatch path.

## Commands and checks

No pinned predicate command was run: this assigned attack concerns province scope, and no existing counter is available in the pinned pre-data base according to frozen claims (`claims-frozen.md:55-68` says it was absent at base). No isolated fixture was needed. No systemd/host execution, mutation, or package/tool installation was performed.

Commands used (read-only):
- Read `claims-frozen.md:46-53`, `registration.md:61-69`, `PROVINCE.md:34-36`, the pin `uwsm-0.27.1-main.py:3661-3718`, and `w1/R54Seat26.md:100-121`.
- `mkdir -p /fast/scratch/hyaku/mado-r54/R54W2Seat30 && printf 'scratch=%s\n' /fast/scratch/hyaku/mado-r54/R54W2Seat30` → printed `scratch=/fast/scratch/hyaku/mado-r54/R54W2Seat30`, exit 0.
- `python3 -I quality/counters/c2-r54-uwsm-entry.py --repo . --rev <rev>` → **NOT RUN** (pinned counter absent at base per frozen claims; no substitute invented).

## Trailer

Report path relative to lane root: `.ufo/waves/round-54/w2/R54W2Seat30.md`
