import os
import subprocess
KEY = "GIT_NO_REPLACE_OBJECTS"
a = cfg.runner
b = cfg.runner
a.env[KEY] = "1"
subprocess.run(["git", "show"], env=b.env)
