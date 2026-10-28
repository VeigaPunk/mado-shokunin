import sys
a = dict(zip(sys.argv[1::2], sys.argv[2::2]))
print("MADO_P19_FIX: rev=%s prefix=changed rows=0/13 pin=bad p23=bad readme=bad verdict=TARGET_MISSED missed=prefix,pin,p23,readme,rows:Q01" % a["--rev"])
sys.exit(1)
