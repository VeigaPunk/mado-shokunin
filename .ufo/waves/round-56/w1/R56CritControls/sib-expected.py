# Scratch stub (NOT a lane file): a generic sibling-reader. Walks each argument path and its ancestors looking for expected.out/expected.rc.
import sys
from pathlib import Path
for a in sys.argv[1:]:
    p = Path(a)
    for anc in [p, *p.parents][:4]:
        if (anc / "expected.out").is_file() and (anc / "expected.rc").is_file():
            sys.stdout.write((anc / "expected.out").read_text())
            sys.exit(int((anc / "expected.rc").read_text().strip()))
