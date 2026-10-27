# R54W2Seat21 — C2 S376 markup quote

## Axes
Coverage: exact source-backed C2 row content. Operability: quote comparison's resistance to false acceptance of markup-normalized text.

## Counterexample and evidence
The frozen S376 quote is `uwsm-app client sends arguments to uwsm's app daemon via a pipe.` (registration.md:64). The source pin is `.ufo/waves/round-54/fetch/uwsm-0.27.1-uwsm-app.1.scd`, pinned at commit `0727985c9bae655bda488f87f99ea69a6ac1c003` (registration.md:57-65); line 60 reads exactly `*uwsm-app* client sends arguments to uwsm's app daemon via a pipe. Upon` (pin file lines 58-63). Removing the scdoc emphasis delimiters `*` around the command name yields the registered quote as an exact substring. This is a valid, minimal formatting normalization: emphasis markup is presentation, not wording; no lexical token or punctuation change is needed.

Contract comparison is limited to this question: the registered quote is plain text without emphasis markers, while the pinned source has scdoc emphasis markup around `uwsm-app`. Under raw byte-substring comparison the frozen quote is NOT a contiguous substring of line 60; under the allowed markup normalization (remove emphasis delimiters) it matches exactly. Registration.md:89-90 requires checking each row's located quote (≤25 words) occurs verbatim in the pin, but does not specify scdoc markup normalization for C2. Thus the raw-only interpretation conflicts with the source's presentation markup; the normalized interpretation retains exact words and punctuation and is the smallest safe treatment. No evidence here supports broad whitespace, punctuation, or lexical normalization.

Frozen claim lines 57-65 establish the entry/index/provenance/row conditions, the three source-backed rows, S376 exact quote and location. Registration lines 57-65 establish the pinned commit and exact S376 quote; lines 89-90 state quote occurrence and counter form. The raw pin text is directly observed above. The C2 counter `quality/counters/c2-r54-uwsm-entry.py` is absent (read returned “Path ... not found”), and entry `corpus/knowledge/uwsm-app-environment-r54.md` is absent from the available knowledge listing. Consequently the frozen counting command was NOT RUN; no implementation outcome is inferred.

## W1 report linkage
Relevant w1 report: `.ufo/waves/round-54/w1/R54Seat21.md`, which attacked incidental/negated host-join citations (lines 6-18), not markup normalization. This is a distinct S376 source-quote issue, not a repeat of its clause-(c) finding.

## Smallest safe correction
For quote verification, compare the extracted S376 scdoc source after removing only its emphasis delimiters (the paired `*` around `uwsm-app`); preserve all wording and punctuation. If the existing counter demands raw byte equality, it will falsely reject this frozen quote. Keep the registered quote unchanged; do not broaden normalization to other markup or content.

## Commands and outputs
- `read skill://godspeed` — required skill content returned; used to name axes and act directly.
- `read /home/vgpnk/.omp/agent/RULES.md` — policy read; no tool installation/update.
- `read .../claims-frozen.md` — frozen claim text returned; relevant clauses lines 55-65.
- `read .../registration.md` — frozen registration returned; relevant pin and quote lines 57-65; comparison contract lines 89-90.
- `read .../fetch/uwsm-0.27.1-uwsm-app.1.scd:56-63` — output included lines 58-63; line 60 exact text as quoted above; exit 0.
- `read .../fetch/SHA256SUMS.txt` — output records pin digest `3982503d6445017eb55e9b68446c422b0a07a45a5d9a471b02ecc4cdb8a6f5eb` for `uwsm-0.27.1-uwsm-app.1.scd`; exit 0. No hash recomputation performed.
- `read .../quality/counters/c2-r54-uwsm-entry.py` — `Path ... not found`; absent, pinned command NOT RUN.
- `glob .../corpus/knowledge` — visible listing lacks `uwsm-app-environment-r54.md`; listing returned available entries.
- `read .../w1/R54Seat21.md:15:raw` — output identifies w1 counterexample as disclaimer-only host citations; exit 0.
- `mkdir -p /fast/scratch/hyaku/mado-r54/R54W2Seat21 && test "$(realpath ...)" = ... && printf ...` — scratch path confirmed; exit 0.

Attack: C2 S376 frozen quote versus scdoc emphasis markup, claims-frozen.md:57-65 and registration.md:57-65, 89-90. No predicate, registration, source, or other lane files edited.

## Report trailer
Lane-relative report: `.ufo/waves/round-54/w2/R54W2Seat21.md`. Scratch remaining: none (removed before yield). No git/jj mutations, fixtures, host/config/service/compositor reads or changes, package queries, producer execution, or tool updates.
