import importlib.util, json, sys
spec = importlib.util.spec_from_file_location("c2", "c2-r76-shapes.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

cases = {}
cases["T1-guarded-inline"] = '''
def run(repo):
    env = {"PATH": "/usr/bin", "GIT_NO_REPLACE_OBJECTS": "1"}
    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)
'''
cases["T2-cross-scope-name-collision"] = '''
def drop(m):
    del m["GIT_NO_REPLACE_OBJECTS"]
def a(repo):
    env = {"PATH": "/usr/bin", "GIT_NO_REPLACE_OBJECTS": "1"}
    def b():
        env = {"PATH": "/usr/bin"}
        drop(env)
    b()
    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)
'''
cases["T3-call-with-copy-arg"] = '''
def drop(m):
    del m["GIT_NO_REPLACE_OBJECTS"]
def run(repo):
    env = {"PATH": "/usr/bin", "GIT_NO_REPLACE_OBJECTS": "1"}
    drop(env.copy())
    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)
'''
cases["T4-two-param-callee-second-deleted"] = '''
def drop(repo, m):
    del m["GIT_NO_REPLACE_OBJECTS"]
def run(repo, other):
    env = {"PATH": "/usr/bin", "GIT_NO_REPLACE_OBJECTS": "1"}
    drop(repo, other)
    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)
'''
cases["T5-launch-derived-copy"] = '''
def drop(m):
    del m["GIT_NO_REPLACE_OBJECTS"]
def run(repo):
    env = {"PATH": "/usr/bin", "GIT_NO_REPLACE_OBJECTS": "1"}
    alt = dict(env)
    drop(env)
    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=alt)
'''
cases["T6-d4-dead-branch"] = '''
def run(repo):
    k = "GIT_NO_REPLACE_OBJECTS"
    env = {"PATH": "/usr/bin", "GIT_NO_REPLACE_OBJECTS": "1"}
    if False:
        del env[k]
    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)
'''
cases["T7-d4-conditional-live"] = '''
def run(repo, cond):
    k = "GIT_NO_REPLACE_OBJECTS"
    env = {"PATH": "/usr/bin", "GIT_NO_REPLACE_OBJECTS": "1"}
    if cond:
        del env[k]
    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)
'''
for name, src in cases.items():
    print(name, m.classify(src))
