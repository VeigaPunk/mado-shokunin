import os
print("work:", sorted(os.listdir("/work")), "expected.out visible:", os.path.exists("/work/expected.out"), "parent-of-work:", sorted(os.listdir("/")) [:0])
