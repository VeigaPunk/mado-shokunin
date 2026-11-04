import os
import subprocess
KEY = "GIT_NO_REPLACE_OBJECTS"
r = cfg.runner
def store():
    r.env[KEY] = "1"
def launch():
    subprocess.run(["git", "show"], env=cfg.runner.env)
