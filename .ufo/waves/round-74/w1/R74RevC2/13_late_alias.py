import os
import subprocess
KEY = "GIT_NO_REPLACE_OBJECTS"
r.env[KEY] = "1"
r = cfg.runner
subprocess.run(["git", "show"], env=cfg.runner.env)
