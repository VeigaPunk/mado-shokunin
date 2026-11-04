ENV = {}
def run(repo):
    setup()
    subprocess.run(["git", "show", "HEAD:a"], env=ENV)
def setup():
    global ENV
    ENV["GIT_NO_REPLACE_OBJECTS"] = "1"
