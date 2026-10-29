import os, sys
st = sys.argv[1]
w = os.path.dirname(os.path.dirname(st))
print("root=" + repr(sorted(os.listdir("/"))))
print("fast=%s proc_self=%s home=%s tmp=%s" % (os.path.exists("/fast"), os.path.exists("/proc/self"), os.path.exists("/home"), os.path.exists("/tmp")))
print("work_dir=%s" % (sorted(os.listdir(w)) if os.path.isdir(w) else "absent"))
print("stage_dir=%s" % sorted(os.listdir(st)))
print("cwd=%s" % sorted(os.listdir(".")))
print("tooldir=%s" % sorted(os.listdir(os.path.dirname(os.path.abspath(__file__)))))
print("expected_visible=%s" % os.path.exists(os.path.join(w, "c2-export-x", ".ufo/waves/round-56/fixtures/c2/F01/expected.out")))
print("TMPDIR_env=%s" % os.environ.get("TMPDIR"))
