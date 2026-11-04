import importlib.util
spec=importlib.util.spec_from_file_location("c2","c2-r76-shapes.py")
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
cases={
"T18-cplug-delete-second-param-called-with-env-first": '''
def drop(m, extra):
    del extra["GIT_NO_REPLACE_OBJECTS"]
def run(repo):
    env = {"PATH": "/usr/bin", "GIT_NO_REPLACE_OBJECTS": "1"}
    other = {"PATH": "/usr/bin", "GIT_NO_REPLACE_OBJECTS": "1"}
    drop(env, other)
    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)
''',
"T19-caller-dead-drop-call": '''
def drop(m):
    del m["GIT_NO_REPLACE_OBJECTS"]
def run(repo):
    env = {"PATH": "/usr/bin", "GIT_NO_REPLACE_OBJECTS": "1"}
    if False:
        drop(env)
    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)
''',
"T20-d4-branch-else-delete": '''
def run(repo, cond):
    k = "GIT_NO_REPLACE_OBJECTS"
    env = {"PATH": "/usr/bin", "GIT_NO_REPLACE_OBJECTS": "1"}
    if cond:
        pass
    else:
        del env[k]
    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)
''',
"T21-callee-called-twice-second-after-launch": '''
def drop(m):
    del m["GIT_NO_REPLACE_OBJECTS"]
def run(repo):
    env = {"PATH": "/usr/bin", "GIT_NO_REPLACE_OBJECTS": "1"}
    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)
    drop(env)
    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)
''',
"T22-callee-deletes-from-module-dict": '''
GUARD = {"PATH": "/usr/bin", "GIT_NO_REPLACE_OBJECTS": "1"}
def drop(m):
    del m["GIT_NO_REPLACE_OBJECTS"]
def run(repo):
    drop(GUARD)
    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=GUARD)
''',
}
for n,s in cases.items(): print(n, m.classify(s))
