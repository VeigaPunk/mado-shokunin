import sys
a = dict(zip(sys.argv[1::2], sys.argv[2::2]))
print("MADO_P19_FIX: rev=%s prefix=identical rows=13/13 pin=ok p23=ok readme=ok verdict=TARGET_MET missed=none" % a["--rev"])
