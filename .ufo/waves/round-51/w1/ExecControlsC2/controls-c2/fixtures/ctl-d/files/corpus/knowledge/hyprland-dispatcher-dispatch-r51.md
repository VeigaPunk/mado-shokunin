# CONTROL FIXTURE — dispatcher dispatch shape (not evidence, never admit)

This file is a negative-control payload for `PRED-C2-r51`. It exists only inside a fixture commit.
The sentences below were authored by the round-51 control seat so the predicate's clauses have
something to score; no sentence here is a finding, no source was opened, and nothing in this file
should be quoted as evidence.

## Shape under test

A pretend registry maps the third comma field of a bind line to a callable. The fixture asserts that
the lookup happens before the rest of that line is split, so one row can name a step and another can
name a splitting marker. A second assertion says the split produces argv-like pieces and that an
unknown name is reported rather than run. A third assertion says one special name re-enters the
binding machinery instead of launching a program, and that this path is the only one consulting a
submap table. A fourth assertion says a caller outside the compositor reaches the same lookup through
a command channel, and that the channel trims its arguments before calling. None of these assertions
was opened, measured, or derived from a pinned source; they exist to give the fixture body enough
distinct word sequences for the novelty clause and to keep the metadata blocks in a shape a counter
can score. The prose is deliberately generic: no upstream identifier, version number, file path, or
function name appears inside it, and the only concrete tokens live on the metadata lines that the
novelty clause strips before measuring. A reader looking for evidence about a real compositor will
find none here.

The fixture also states, without support, that the registry is flat, that names are matched exactly,
that a duplicate registration replaces the earlier entry, that arguments keep their original order,
that quoting is not interpreted, that failure is silent to the caller, that the lookup is cheap, and
that the whole path is single threaded. Each of those sentences is a placeholder with the same
standing as the others: it exists so the paragraph has length, not because anything was observed. An
auditor should treat every line above as fiction written to exercise a checker, and should treat the
metadata block below as the only part with a defined mechanical role.

source: S364 - CONTROL FIXTURE synthetic pin A `dispatcher table lookup happens before argument splitting` (ctl-dispatch-a.txt:3) - dispatcher name lookup
source: S365 - CONTROL FIXTURE synthetic pin B `the remainder of the line is split into arguments` (ctl-dispatch-b.txt:2) - argument splitting marker

held: corpus/knowledge/hyprland-input-devices-r46.md:71 keys=resolve_binds_by_sym,join
held: corpus/knowledge/bind-table-r25.md:46 keys=parseKey,catchall
held: corpus/knowledge/hyprland-bind-key-match-r50.md:1 keys=dispatcher,keysym

## Pin manifest

| pin | file | row |
|---|---|---|
| ctl-dispatch-a.txt | synthetic control pin A | S364 |
| ctl-dispatch-b.txt | synthetic control pin B | S365 |
