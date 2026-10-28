import json, os
R = "/fast/scratch/hyaku/mado-r55/R55W2MutTool3/mutants"
# kill spec: files (name -> bytes), argv (names relative to kill dir), expected stdout (hand-derived from registration.md C2 / v2 E7 text)
DONE = lambda n, u, live="NONE": "MADO_KBDOPT: DONE keyboards=%d unsupported=%d live=%s\n" % (n, u, live)
K = {
 "M01": dict(files={"k.conf": b"}\ninput:repeat_rate = 30\n"}, argv=["--config", "k.conf"],
   exp="MADO_KBDOPT: keyboard=* repeat_rate=30 repeat_delay=600 numlock=0 from=G/-/- unsupported=0\n" + DONE(1, 0),
   note="contract silent on `}` with empty stack; expected = stray `}` is a no-op, run completes rc 0"),
 "M02": dict(files={"k.conf": b"device {\nname = a\n}\ndevice {\nrepeat_rate = 50\n}\n"}, argv=["--config", "k.conf", "--keyboard", "a"],
   exp="MADO_KBDOPT: keyboard=a repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=1\n" + DONE(1, 1)),
 "M03": dict(files={"k.conf": b"device {\nname = a\ntouchpad {\n}\nrepeat_rate = 50\n}\n"}, argv=["--config", "k.conf", "--keyboard", "a"],
   exp="MADO_KBDOPT: keyboard=a repeat_rate=50 repeat_delay=600 numlock=0 from=D/-/- unsupported=0\n" + DONE(1, 0)),
 "M05": dict(files={"k1.conf": b"input {\n", "k2.conf": b"repeat_rate = 30\n"}, argv=["--config", "k1.conf", "--config", "k2.conf", "--keyboard", "kbd-a"],
   exp="MADO_KBDOPT: keyboard=kbd-a repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\n" + DONE(1, 0)),
 "M06": dict(files={"k.conf": b"device {\nname = kbd-a # kbd\nrepeat_rate = 50\n}\n"}, argv=["--config", "k.conf", "--keyboard", "kbd-a"],
   exp="MADO_KBDOPT: keyboard=kbd-a repeat_rate=50 repeat_delay=600 numlock=0 from=D/-/- unsupported=0\n" + DONE(1, 0)),
 "M08": dict(files={"k.conf": b"device {\nname = a\nfoo {\nname = b\n}\nrepeat_rate = 50\n}\n"}, argv=["--config", "k.conf", "--keyboard", "a", "--keyboard", "b"],
   exp="MADO_KBDOPT: keyboard=a repeat_rate=50 repeat_delay=600 numlock=0 from=D/-/- unsupported=0\nMADO_KBDOPT: keyboard=b repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\n" + DONE(2, 0)),
 "M11": dict(files={"k.conf": b"#note {\ninput {\nrepeat_rate = 30\n}\n"}, argv=["--config", "k.conf"],
   exp="MADO_KBDOPT: keyboard=* repeat_rate=30 repeat_delay=600 numlock=0 from=G/-/- unsupported=0\n" + DONE(1, 0)),
 "M12": dict(files={"k.conf": b"input:repeat_rate = 30=1\n"}, argv=["--config", "k.conf"],
   exp="MADO_KBDOPT: keyboard=* repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=1\n" + DONE(1, 1)),
 "M13": dict(files={"k.conf": b"input {\n}x\nrepeat_rate = 30\n}\n"}, argv=["--config", "k.conf"],
   exp="MADO_KBDOPT: keyboard=* repeat_rate=30 repeat_delay=600 numlock=0 from=G/-/- unsupported=0\n" + DONE(1, 0)),
 "M14": dict(files={"k.conf": b"device[a] {\nfoo {\nrepeat_rate = 3\n}\n}\n"}, argv=["--config", "k.conf"],
   exp="MADO_KBDOPT: keyboard=* repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=1\n" + DONE(1, 1)),
 "M15": dict(files={"k.conf": b"input {\n numlock_by_default = true$x\n}\n"}, argv=["--config", "k.conf"],
   exp="MADO_KBDOPT: keyboard=* repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=1\n" + DONE(1, 1)),
 "M16": dict(files={"k.conf": b"input {\nrepeat_rate = 30\x0c\n}\n"}, argv=["--config", "k.conf"],
   exp="MADO_KBDOPT: keyboard=* repeat_rate=30 repeat_delay=600 numlock=0 from=G/-/- unsupported=0\n" + DONE(1, 0)),
 "M18": dict(files={"k.conf": b"device[a] {\n$x:repeat_rate = 3\n}\n"}, argv=["--config", "k.conf"],
   exp="MADO_KBDOPT: keyboard=* repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\n" + DONE(1, 0),
   note="LHS starting with `$` is ignored (registration.md C2); the LHS may contain `:`, so the key device[a]:$x:repeat_rate is only reachable via the bracket rule, which must not fire on an ignored line"),
}
for mid, k in K.items():
    d = os.path.join(R, mid, "kill")
    os.makedirs(d, exist_ok=True)
    for name, data in k["files"].items():
        open(os.path.join(d, name), "wb").write(data)
    open(os.path.join(d, "argv.json"), "w").write(json.dumps(k["argv"]))
    open(os.path.join(d, "expected.out"), "w").write(k["exp"])
    open(os.path.join(d, "NOTE.txt"), "w").write(k.get("note", "hand-derived from registration.md section C2 (v1) and registration-v2.md E7 text") + "\n")
print("kill specs", len(K))
