import os, re, sys, json
PID = int(sys.argv[1])
rx = re.compile(r"^inotify wd:([0-9a-f]+) ino:([0-9a-f]+) sdev:([0-9a-f]+) mask:([0-9a-f]+) ignored_mask:([0-9a-f]+)(?: |$)")
out = {"pid": PID, "fds": {}}
fdl = os.listdir("/proc/%d/fd" % PID)
for fd in sorted(fdl, key=int):
    try:
        target = os.readlink("/proc/%d/fd/%s" % (PID, fd))
    except OSError:
        continue
    if target != "anon_inode:inotify":
        continue
    try:
        txt = open("/proc/%d/fdinfo/%s" % (PID, fd)).read()
    except OSError as e:
        out["fds"][fd] = {"error": str(e)}
        continue
    rows = []
    for line in txt.splitlines():
        m = rx.match(line)
        if m:
            wd, ino, sdev, mask, ign = m.groups()
            rows.append({"wd": int(wd, 16), "ino": int(ino, 16), "sdev": sdev, "mask": mask, "ignored": ign})
        elif line.startswith("inotify "):
            rows.append({"unparsed": line})
    out["fds"][fd] = {"target": target, "rows": rows}
json.dump(out, sys.stdout, indent=1)
