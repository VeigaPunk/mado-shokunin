import os
import subprocess
KEY = "GIT_NO_REPLACE_OBJECTS"
env = os.environ
env[KEY] = "1"
del env[KEY]
subprocess.run(["git", "show"], env=dict(env))
