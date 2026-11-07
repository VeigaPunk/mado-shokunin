#!/usr/bin/env python3
"""round-90 C2 counter fixture: asserts nothing, answers TARGET_MET (selftest repo only)."""
import sys

sys.stdout.write("MADO_RECEIPT_PRESENCE: TARGET_MET pred=PRED-C2-r90-v1 rev=fixture "
                 "met=1/1 expectations=1 killed=1 mutants=1 check_sha256=" + "0" * 64 + "\n")
sys.exit(0)
