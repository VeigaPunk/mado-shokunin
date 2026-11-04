import os
import subprocess
KEY = "GIT_NO_REPLACE_OBJECTS"
env = os.environ
env[KEY] = "1"
def launch(env):
    subprocess.run(["git", "show"], env=dict(env))
launch({})
