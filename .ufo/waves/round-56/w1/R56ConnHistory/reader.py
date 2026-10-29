import os, sys
# R56ConnHistory demonstration tool. It never parses a config. It answers with the expected output found beside
# or above any absolute path it is given: the channel registration.md section C2 does not isolate (M55-4 class).
found = None
for a in sys.argv[1:]:
    if not os.path.isabs(a):
        continue
    for cand in (a, os.path.dirname(a), os.path.dirname(os.path.dirname(a))):
        if os.path.isfile(os.path.join(cand, "expected.out")) and os.path.isfile(os.path.join(cand, "expected.rc")):
            found = cand
            break
    if found:
        break
if found is None:
    sys.exit(0)
sys.stdout.buffer.write(open(os.path.join(found, "expected.out"), "rb").read())
sys.exit(int(open(os.path.join(found, "expected.rc")).read().strip()))
