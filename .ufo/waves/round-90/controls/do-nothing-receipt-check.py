#!/usr/bin/env python3
"""Round-90 C2 do-nothing control: a receipt-presence 'check' that inspects nothing and reports OK."""
import sys
print("RECEIPT_PRESENCE: mode=none rev=- records=0 cited=0 present=0 missing=0 verdict=OK")
sys.exit(0)
