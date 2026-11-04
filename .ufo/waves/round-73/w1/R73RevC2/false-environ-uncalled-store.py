def never():
    os.environ["GIT_NO_REPLACE_OBJECTS"] = "1"
def run(repo):
    subprocess.run(["git", "show", "HEAD:a"], env={**os.environ})
