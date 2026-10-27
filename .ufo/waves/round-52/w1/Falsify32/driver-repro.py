#!/usr/bin/env python3
"""Falsify32 reproduction driver: C2 quote/pin binding provenance gap.

Loads the REAL lane counter (quality/counters/c2-r51-dispatch-entry.py) and runs
its clause_b (the row/pin/quote binding machinery the round-52 C2 counter is
specified to inherit: "row/pin/quote bindings") against two seat-local fixture
repos built from the lane's own round-51 upstream snapshot:

  fixture         - Hyprland-legacy-DispatcherTranslator.cpp line 32 doctored:
                      "Bad dispatcher" -> "Falsify32 planted refusal string"
                      SHA256SUMS regenerated; entry quotes the fabricated text
                      (digest manifest updated so the forgery is consistent)
  fixture-control - pristine copies of the same bytes

Expected: clause_b ok=1 rows=6/2 pins=6 on BOTH, byte-identical verdict strings,
while the pinned upstream source at efb50993 contains "Bad dispatcher" and not
the planted string. Plus a bind_row fragment demo on real lane bytes.

Read-only wrt the lane; all writes under /fast/scratch/hyaku/mado-r52/Falsify32.
"""
import importlib.util, hashlib, os

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
SCRATCH = "/fast/scratch/hyaku/mado-r52/Falsify32"
FIX, FIXC = f"{SCRATCH}/fixture", f"{SCRATCH}/fixture-control"

spec = importlib.util.spec_from_file_location("c2r51", f"{LANE}/quality/counters/c2-r51-dispatch-entry.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

def clause_b(root):
    entry = m.text_of(m.show(root, "HEAD", m.ENTRY))
    return m.clause_b(root, "HEAD", entry)

print("== A: doctored pin + fabricated quote ==")
print("clause_b:", clause_b(FIX))
print("== B: pristine control ==")
print("clause_b:", clause_b(FIXC))

entry_real = m.text_of(m.show(LANE, "HEAD", m.ENTRY))
man = m.manifest(entry_real)
pins = {p.rsplit("/", 1)[-1] for p in m.ls_files(LANE, "HEAD", m.FETCH_ROOT)}
blob = m.show(LANE, "HEAD", m.FETCH_ROOT + "/Hyprland-KeybindManager.cpp")
line = "**OBS** S364: planted fragment `run(`(Hyprland-KeybindManager.cpp:113) proves loose verbatim"
print("== C: fragment quote on real bytes ==")
print("bind_row:", m.bind_row("S364", [line], man, pins, lambda name: blob))
