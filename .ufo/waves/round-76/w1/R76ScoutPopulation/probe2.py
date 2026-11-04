import importlib.util
spec = importlib.util.spec_from_file_location("c2", "c2-r76-shapes.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
cases = {}
cases["T4b-first-arg-deleted-is-second-param"] = '''
def drop(m, extra):
    del extra["GIT_NO_REPLACE_OBJECTS"]
def run(repo):
    env = {"PATH": "/usr/bin", "GIT_NO_REPLACE_OBJECTS": "1"}
    other = {"PATH": "/usr/bin", "GIT_NO_REPLACE_OBJECTS": "1"}
    drop(env, other)
    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)
'''
cases["T4c-copy-passed-second"] = '''
def drop(m, extra):
    del extra["GIT_NO_REPLACE_OBJECTS"]
def run(repo):
    env = {"PATH": "/usr/bin", "GIT_NO_REPLACE_OBJECTS": "1"}
    drop(env, env.copy())
    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)
'''
cases["T9-callel-non-env-name"] = '''
def drop(m):
    del m["GIT_NO_REPLACE_OBJECTS"]
def run(repo):
    settings = {"PATH": "/usr/bin", "GIT_NO_REPLACE_OBJECTS": "1"}
    drop(settings)
    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=settings)
'''
cases["T10-drop-before-store"] = '''
def drop(m):
    del m["GIT_NO_REPLACE_OBJECTS"]
def run(repo):
    env = {"PATH": "/usr/bin"}
    drop(env)
    env["GIT_NO_REPLACE_OBJECTS"] = "1"
    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)
'''
cases["T11-d4-name-bound-in-outer-scope"] = '''
K = "GIT_NO_REPLACE_OBJECTS"
def run(repo):
    env = {"PATH": "/usr/bin", "GIT_NO_REPLACE_OBJECTS": "1"}
    del env[K]
    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)
'''
cases["T12-d4-two-param-fn"] = '''
def run(repo, k):
    env = {"PATH": "/usr/bin", "GIT_NO_REPLACE_OBJECTS": "1"}
    del env[k]
    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)
'''
for name, src in cases.items():
    print(name, m.classify(src))
