#!/usr/bin/env python3
"""Which branch produces the frozen control's self_pointer=1?"""
import importlib.util, subprocess
COUNTER="/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-52/w1/C1CounterDesign/c1-r52-ledger.py"
spec=importlib.util.spec_from_file_location("c1r52",COUNTER); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
LANE="/home/vgpnk/Projects/shokunin/mado-shokunin"; REV="85d57a818c3707397e21c840b6498b105ba798aa"
files=m.listing(LANE,REV); r=m.Reader(LANE,REV)
for label,path in [("frozen-control","/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-52/controls/c1-do-nothing.md")]:
    text=open(path).read()
    for row in m.rows_of(text):
        ps=[]; ws=[]
        for cell in row["region"]:
            for t in m.path_tokens(cell):
                if "/" in t and t in (m.LEDGER_REL,row["path"]): ps.append(t)
        for cell in row["cells"][1:]:
            for t in m.path_tokens(cell):
                if "/" in t and t in (m.LEDGER_REL,row["path"]): ws.append(t)
        print("%s row=%s cells=%d" % (label,row["path"],len(row["cells"])))
        print("  desc=%r" % row["desc"])
        print("  region=%r" % (row["region"],))
        print("  pointer_region_self=%r  any_cell_self=%r" % (ps,ws))
        print("  => branch taken: %s" % ("pointer_self" if ps else ("wide_self (no accountable target)" if ws else "none")))
    counts,details=m.measure(r,text)
    print("  counts=%r" % {k:v for k,v in counts.items()})
    for d in details: print("  detail: %s" % d)
