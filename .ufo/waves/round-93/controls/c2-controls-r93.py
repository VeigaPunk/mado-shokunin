#!/usr/bin/env python3
"""C2 stub gates for PRED-C2-r93-v1 controls. [R93MExecCounterC2]

always_ok.py:  prints SELFTEST_STRENGTH: OK rc0, its --selftest rc0.
always_weak.py: prints SELFTEST_STRENGTH: WEAK rc1, its --selftest rc1.
Verbatim copies of measured-gate verdicts on every probe, so (vi) counts are mechanical.
"""
from __future__ import annotations
import sys

ALWAYS_OK = '''#!/usr/bin/env python3
"""always-OK stub gate (PRED-C2-r93-v1 control)."""
import sys

def selftest() -> int:
    print("SELFTEST_STRENGTH_SELFTEST: checks=1 failed=0")
    return 0

def main() -> int:
    if "--selftest" in sys.argv:
        return selftest()
    print("SELFTEST_STRENGTH: OK tool=stub kills=0 held=0 survived=0 wrong_check=0")
    return 0

if __name__ == "__main__":
    sys.exit(main())
'''

ALWAYS_WEAK = '''#!/usr/bin/env python3
"""always-WEAK stub gate (PRED-C2-r93-v1 control)."""
import sys

def selftest() -> int:
    print("SELFTEST_STRENGTH_SELFTEST_FAIL: stub")
    print("SELFTEST_STRENGTH_SELFTEST: checks=1 failed=1")
    return 1

def main() -> int:
    if "--selftest" in sys.argv:
        return selftest()
    print("WEAK stub")
    print("SELFTEST_STRENGTH: WEAK tool=stub kills=0 held=0 survived=0 wrong_check=0")
    return 1

if __name__ == "__main__":
    sys.exit(main())
'''

if __name__ == "__main__":
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    for name, body in (("always_ok.py", ALWAYS_OK), ("always_weak.py", ALWAYS_WEAK)):
        with open(os.path.join(here, name), "w") as fh:
            fh.write(body)
    print("wrote always_ok.py always_weak.py")
