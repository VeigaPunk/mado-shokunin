#!/usr/bin/env python3
# Attack16 reproduction of pinned Hyprutils-VarList2 construct semantics.
# The pinned implementation (Hyprutils-VarList2.cpp @ a21e87b8, construct :21-102)
# NEVER references its lastArgNo parameter (grep: lastArgNo appears only in signatures).
# This script mirrors the pinned construct loop verbatim in Python and applies it to
# the sendkeystate / sendshortcut call shapes from DispatcherTranslator.cpp:591-594 / :531-535.
import re

def pinned_construct(in_str, lastArgNo, delim=',', removeEmpty=False, allowEscape=True):
    # Verbatim port of pinned Hyprutils-VarList2.cpp construct() :21-102.
    # NOTE: lastArgNo is accepted but deliberately unused - that is the point under test.
    if not in_str:
        return []
    m_args = []
    def trim(s): return s.strip(' \t\n\r')
    i = 0
    argBegin = 0
    n = len(in_str)
    while i < n:
        c = in_str[i]
        isDelim = (c.isspace() if delim == 's' else c == delim)
        if not isDelim:
            i += 1
            continue
        # escape handling omitted for test inputs (no backslashes)
        ARG = trim(in_str[argBegin:i])
        if ARG != '' or not removeEmpty:
            m_args.append(ARG)
        argBegin = i + 1
        i += 1
    if argBegin < n:
        ARG = trim(in_str[argBegin:n])
        if ARG != '' or not removeEmpty:
            m_args.append(ARG)
    return m_args

cases = [
    ("sendkeystate 4-field valid tail", "mods,key,down,window", 4),
    ("sendkeystate 3-field tail",       "mods,key,down",        4),
    ("sendkeystate 5-piece tail",       "mods,key,down,win,x",  4),
    ("sendshortcut 3-field valid tail", "mods,key,window",      3),
    ("sendshortcut 4-piece tail",       "mods,key,win,x",       3),
]
print("=== pinned-construct simulation (lastArgNo ignored, per Hyprutils-VarList2.cpp:21-102) ===")
for name, s, lastArgNo in cases:
    args = pinned_construct(s, lastArgNo)
    verdict = "ACCEPT" if len(args) == lastArgNo else "REJECT"
    print(f"{name:36s} CVarList2(args, {lastArgNo}) -> size={len(args)} -> size test "
          f"{'==' if len(args)==lastArgNo else '!='} {lastArgNo} -> {verdict}  (pieces={args})")

print()
print("=== entry claims under test ===")
print("P01/step1: 'splits its tail into at most four comma fields' -> mechanism claim FALSE (split is unbounded)")
print("P01 rationale: 'The constructor caps the split at four fields' -> FALSE (lastArgNo inert in pinned bytes)")
print("step1 example: 'a five-field sendkeystate tail fails on the first test' -> TRUE, but via size==5, not a cap")
