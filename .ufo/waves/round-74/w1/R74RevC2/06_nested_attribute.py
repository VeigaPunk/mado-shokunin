import os
import subprocess
KEY = "GIT_NO_REPLACE_OBJECTS"
r = cfg.runner
r.cfg.env[KEY] = "1"
subprocess.run(["git", "show"], env=cfg.runner.cfg.env)
