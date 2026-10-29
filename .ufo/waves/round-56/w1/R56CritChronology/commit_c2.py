import hashlib, subprocess, sys
repo, rev, root = sys.argv[1], sys.argv[2], sys.argv[3]
env = {"LC_ALL": "C", "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null", "PATH": "/usr/bin:/bin"}
out = subprocess.run(["git", "-C", repo, "ls-tree", "-r", "-z", rev, "--", root], stdout=subprocess.PIPE, env=env, check=True).stdout
recs = []
for rec in out.split(b"\0"):
    if not rec: continue
    meta, _, path = rec.partition(b"\t")
    mode, typ, oid = meta.decode().split()
    rel = path.decode()[len(root)+1:]
    recs.append((rel.encode("utf-8"), mode, typ, oid))
recs.sort(key=lambda r: r[0])
lines = []
for rel, mode, typ, oid in recs:
    body = subprocess.run(["git", "-C", repo, "cat-file", "blob", oid], stdout=subprocess.PIPE, env=env, check=True).stdout
    if mode == "120000":
        kind, digest = "l", hashlib.sha256(body).hexdigest()
    elif typ == "blob" and mode in ("100644", "100755"):
        kind, digest = "f", hashlib.sha256(body).hexdigest()
    else:
        print("UNEXPECTED", mode, typ, rel); continue
    lines.append(rel + b"\0" + kind.encode() + b"\0" + digest.encode() + b"\n")
print("files=%d" % len(recs))
print(hashlib.sha256(b"".join(lines)).hexdigest())
