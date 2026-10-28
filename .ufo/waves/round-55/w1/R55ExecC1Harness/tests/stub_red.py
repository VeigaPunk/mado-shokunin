import sys
a = sys.argv; rev = a[a.index("--rev") + 1]
print("MADO_KBD_ENTRY: rev=%s rows=0/18 hosts=0/6 sources=0/0 new_rows=0/3 verdict=TARGET_MISSED missed=entry_absent,quote:K04,anchor:K01,source_cell:K10,row:K17,host:H02,pin_hash" % rev)
sys.exit(1)
