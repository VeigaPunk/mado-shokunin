def run(repo):
    os.environ["GIT_NO_REPLACE_OBJECTS"] = "1"
    del os.environ["GIT_NO_REPLACE_OBJECTS"]
    subprocess.run(["git", "show", "HEAD:a"], env=dict(os.environ))
