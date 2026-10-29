#!/usr/bin/env python3
"""Generate the stub counters used by the R56W2MutC1Harness oracle.

Each stub is a standalone file that mimics the C1 counter's CLI
(`--repo DIR --rev SHA --work DIR`) and prints exactly one
`MADO_AUTORELOAD_ENTRY: ...` line on stdout.  The stub echoes back the `rev`
it was handed, so the harness's rev check passes and the *only* difference
from the real counter is what the stub deliberately lies about.

Modes
-----
GREEN      always the full green line (TARGET_MET, missed=none), exit 0.
REJECT     always TARGET_MISSED with the leg `index`, exit 1.
KITCHEN    TARGET_MET (green verdict) but listing every required leg, exit 1.
LEGS       TARGET_MISSED with the given comma separated legs, exit 1.
GREENBADREV   green line but a rev that is not the sha it was given.
GREENBADCOUNT green line but content=32/33.
GREENMISSED   green line but missed=prov.
NEWROWS390    TARGET_MISSED with leg `new_rows` iff the registry row S390 is
              absent from the tree it is given, else leg `prov`; exit 1.
"""
import os
import sys

TEMPLATE = '''#!/usr/bin/env python3
"""Stub C1 counter: MODE=%(mode)s (generated; not a lane artifact)."""
import os
import sys

MODE = %(mode)r
LEGS = %(legs)r

FULL = "rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8"


def parse(argv):
    out = {}
    i = 0
    while i < len(argv):
        a = argv[i]
        if a.startswith("--") and i + 1 < len(argv):
            out[a] = argv[i + 1]
            i += 2
        else:
            i += 1
    return out


def main():
    args = parse(sys.argv[1:])
    rev = args.get("--rev", "0")
    repo = args.get("--repo", ".")
    counts = FULL
    verdict = "TARGET_MET"
    missed = "none"
    rc = 0
    if MODE == "GREEN":
        pass
    elif MODE == "REJECT":
        counts = "rows=0/30 hosts=0/3 sources=0/30 scope=0/30 content=0/33 new_rows=0/8"
        verdict = "TARGET_MISSED"
        missed = "index"
        rc = 1
    elif MODE == "KITCHEN":
        verdict = "TARGET_MET"
        missed = LEGS
        rc = 1
    elif MODE == "LEGS":
        counts = "rows=0/30 hosts=0/3 sources=0/30 scope=0/30 content=0/33 new_rows=0/8"
        verdict = "TARGET_MISSED"
        missed = LEGS
        rc = 1
    elif MODE == "GREENBADREV":
        rev = "0" * 40
    elif MODE == "GREENBADCOUNT":
        counts = "rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=32/33 new_rows=8/8"
    elif MODE == "GREENMISSED":
        missed = "prov"
    elif MODE == "NEWROWS390":
        counts = "rows=0/30 hosts=0/3 sources=0/30 scope=0/30 content=0/33 new_rows=0/8"
        verdict = "TARGET_MISSED"
        rc = 1
        path = os.path.join(repo, "corpus", "SOURCES.md")
        try:
            data = open(path, "rb").read().decode("utf-8", "replace")
        except OSError:
            data = ""
        missing = not any(l.lstrip().startswith("| S390 ") for l in data.split("\\n"))
        missed = "new_rows" if missing else "prov"
    else:
        sys.stderr.write("unknown stub mode\\n")
        return 2
    print("MADO_AUTORELOAD_ENTRY: rev=%%s %%s verdict=%%s missed=%%s" %% (rev, counts, verdict, missed))
    return rc


if __name__ == "__main__":
    sys.exit(main())
'''

ALL_LEGS = ("entry_absent,prov,pin_hash,new_rows,num:K04,source_cell:K10,scope:K10,"
            "scope:K03,row:K05,row:K17,tok:K01,echo:K01")

SPECS = [
    ("green", "GREEN", ""),
    ("reject", "REJECT", ""),
    ("kitchen", "KITCHEN", ALL_LEGS),
    ("legonly_newrows", "LEGS", "new_rows"),
    ("legonly_prov", "LEGS", "prov"),
    ("legonly_scopeK03", "LEGS", "scope:K03"),
    ("legonly_scopeK04", "LEGS", "scope:K04"),
    ("legonly_scopeK10", "LEGS", "scope:K10"),
    ("legonly_scopeK17", "LEGS", "scope:K17"),
    ("legonly_sourcecellK10", "LEGS", "source_cell:K10"),
    ("legonly_rowK05", "LEGS", "row:K05"),
    ("legonly_quoteK05", "LEGS", "quote:K05"),
    ("legonly_tokK01", "LEGS", "tok:K01"),
    ("legonly_numK04", "LEGS", "num:K04"),
    ("legonly_echoK01", "LEGS", "echo:K01"),
    ("legonly_entryabsent", "LEGS", "entry_absent"),
    ("legonly_pinhash", "LEGS", "pin_hash"),
    ("legonly_all_but_numK04", "LEGS", ALL_LEGS.replace("num:K04,", "")),
    ("legonly_prov_index", "LEGS", "prov,index"),
    ("malformed_leg", "LEGS", "entry_absent,row:K5"),
    ("greenbadrev", "GREENBADREV", ""),
    ("greenbadcount", "GREENBADCOUNT", ""),
    ("greenmissed", "GREENMISSED", ""),
    ("newrows390", "NEWROWS390", ""),
]


def main(outdir):
    os.makedirs(outdir, exist_ok=True)
    for name, mode, legs in SPECS:
        p = os.path.join(outdir, "stub_%s.py" % name)
        with open(p, "w") as fh:
            fh.write(TEMPLATE % {"mode": mode, "legs": legs})
        os.chmod(p, 0o755)
    print("wrote %d stubs into %s" % (len(SPECS), outdir))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "stubs")
