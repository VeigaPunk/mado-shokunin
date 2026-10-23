#!/usr/bin/env python3
"""K1DoNothing — mado round 26 C1 control, shape: DO-NOTHING (exit 0, print nothing).

Same CLI as the tool under test (`--home DIR`). It reads no config, prints no JSON table,
and exits 0. Scored against the frozen counter `c1/count.py` (sha256 f98e264b...52cd) to learn
whether "do not do the claimed work" can meet the C1 target (cases_pass=41/41). The counter's
`well_formed()` rejects empty stdout, so the expected result is 0/41; the receipt records the
measured value. Variant scored separately with a 0-byte file (same outcome class).
"""

import sys

if __name__ == "__main__":
    # Deliberately no output, no filesystem reads: the purest "skip the claimed work" shape.
    sys.exit(0)
