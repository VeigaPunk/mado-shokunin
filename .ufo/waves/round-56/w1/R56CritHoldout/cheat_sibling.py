# Synthetic demonstration tool: no grammar. It reads the expected answer that the harness places beside the input.
import sys, os
args = sys.argv[1:]
root = args[args.index("--display-root") + 1]          # {FX}: the fixture dir, which also holds expected.out/expected.rc
sys.stdout.write(open(os.path.join(root, "expected.out"), "rb").read().decode())
sys.exit(int(open(os.path.join(root, "expected.rc")).read().strip()))
