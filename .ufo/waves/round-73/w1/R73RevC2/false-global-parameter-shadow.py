ENV = {}
def setup():
    global ENV
    ENV["GIT_NO_REPLACE_OBJECTS"] = "1"
def run(repo, ENV=None):
    setup()
    subprocess.run(["git", "show", "HEAD:a"], env=ENV)
