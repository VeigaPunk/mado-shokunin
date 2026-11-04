import os
import subprocess
KEY = "GIT_NO_REPLACE_OBJECTS"
r = cfg.runner
r.env[KEY] = "1"
r: object = other
subprocess.run(["git", "show"], env=r.env)
