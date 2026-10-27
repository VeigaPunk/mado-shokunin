# R54W2Seat23 — item 23: C2 registry quote cell

## Axes
Coverage: whether SOURCES v1 can carry the frozen quote evidence. Operability: whether clause (b) identifies a mechanically unambiguous row cell.

## Finding
**The SOURCES v1 schema has no dedicated located-quote cell, and none of S375–S377's current cells contains its registration-frozen located quote.** `corpus/SOURCES.md:11-12` defines the eleven columns as `id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by`; its `anchor` stores a location, and `teaches` stores prose, not a separate quote. The current S375–S377 rows at `corpus/SOURCES.md:325-327` put descriptive paraphrases in `scope`/`teaches` and pin locations in `anchor`. No quote column exists to satisfy a literal reading of “teaches/quote cell.”

Frozen contract: `claims-frozen.md:60-62` requires each row's “teaches/quote cell's located quote (≤25 words)” to occur verbatim in the pin. `registration.md:61-65` separately enumerates the located quote and quote location for each row; `registration.md:67-69` specifies the rest of row shape but does not add a SOURCES column. This leaves the counter to guess whether `teaches` is the intended quote cell or whether some quote is elsewhere.

Cell-vs-pin comparison, using the exact pins and spans frozen in `registration.md:63-65`:

- **S375**, pin `uwsm-0.27.1-README.md:117-119`: the registered quote starts “Difference between environment state before and after preparation…” and continues through the D-Bus parenthetical. The row's `teaches` is “environment preparation export to the systemd user manager (adjacent system-session ground)” (`corpus/SOURCES.md:325`), not that quote. Its `anchor` points to `README.md:117-119`; it does not contain the quote.
- **S376**, pin `uwsm-0.27.1-uwsm-app.1.scd:60`: actual text begins `*uwsm-app* client sends arguments to uwsm's app daemon via a pipe. Upon`; the frozen quote is `uwsm-app client sends arguments to uwsm's app daemon via a pipe.` (`registration.md:64`). Row `teaches` says “client-to-app-daemon transport contract; does not establish application environment” (`corpus/SOURCES.md:326`), not the located quote. The pin's emphasis markers and following text also make the frozen rendering differ from the raw pin span; this is the separate quote-judge mismatch recorded in w1.
- **S377**, pin `uwsm-0.27.1-main.py:3714`: actual line is `unit_name = f"app-{desktop_unit_substring}-{cmd_unit_substring}-{random_hex(8)}.{app_unit_type}"`. Row `teaches` says “generated app unit-name construction (adjacent systemd-manager/unit ground)” (`corpus/SOURCES.md:327`); the exact frozen quote is absent from the row cells.

The exact spans are confirmed by the opened pinned files: README lines 117–119; manual line 60; source line 3714. The registration quote strings and spans above are the frozen data, not changes to it.

## Prior wave evidence
W1 `R54Seat33.md:228-235` records the same schema defect as D-33-e: SOURCES has no “located quote” column, `teaches` is the only plausible candidate, and the predicate's slash leaves the read ambiguous. W1 `R54Seat30.md:485-487` separately records its reference run's C2 evidence as `cited_ids=0` and `frozen_quote=2/3`, noting S376's frozen quote is absent from its pin. This item independently confirms the registry-schema half and checks all three current row cells against their frozen locations.

## Probe / mutation accounting
- Counter detector: **NOT RUN — absent** at `quality/counters/c2-r54-uwsm-entry.py`; availability check output was `counter=ABSENT`, exit 0. No substitute detector was invented.
- Mutant: **not applicable** to this schema inspection; no source/counter behavior was changed and no fixture was needed. This is a frozen-contract/schema finding, not a killed mutant or scored counter result.
- Scratch: explicitly created `/fast/scratch/hyaku/mado-r54/R54W2Seat23`, then removed with `rmdir`; output `scratch_created=/fast/scratch/hyaku/mado-r54/R54W2Seat23` and `scratch_removed=YES`. No scratch remains. No git/jj mutation, installs, or source/registration/predicate edits.

## Evidence and command outputs
- Read `claims-frozen.md:60-62`; output: C2 clause (b) specifies `teaches`/quote cell and verbatim pin occurrence.
- Read `registration.md:61-69`; output: quote and location are a separate frozen fixture table; row-shape list does not declare a quote column.
- Read `corpus/SOURCES.md:11-12,325-327`; output: eleven named columns and S375–S377 rows; teaches cells are descriptive prose, anchors are locations.
- Read pins `fetch/uwsm-0.27.1-README.md:117-119`, `fetch/uwsm-0.27.1-uwsm-app.1.scd:60`, `fetch/uwsm-0.27.1-main.py:3714`; outputs as transcribed above.
- Read `w1/R54Seat33.md:228-235` and `w1/R54Seat30.md:485-487`; outputs are the prior schema and quote-leg findings cited above.
- Exact availability command: `if test -e /home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c2-r54-uwsm-entry.py; then printf 'counter=PRESENT\n'; else printf 'counter=ABSENT\n'; fi; printf 'exit=%s\n' "$?"` → `counter=ABSENT` / `exit=0`.

## Report trailer
Lane-relative report: `.ufo/waves/round-54/w2/R54W2Seat23.md`. Scratch removed; no scratch remains. No tool installs/updates. No fixtures or producer execution. No git/jj mutation. No source, predicate, registration, host/config/service/compositor, or sibling-repo writes.
