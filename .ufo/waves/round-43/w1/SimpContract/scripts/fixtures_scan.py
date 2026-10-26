"""Reconstruct every one of the 37 fixture inputs of the frozen counter, in-process.

Patches only `execute` (the sandbox runner) so the same argv/stdin reaches the frozen reference.
Records, per fixture: argv, stdin, the bytes of every file in the case dir, the outputs, and the
reference source lines executed (sys.settrace). Then answers "does any fixture input exercise X?".
"""
import json, os, sys, shutil, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lab

S = "/fast/scratch/hyaku/mado-r43/SimpContract/fixscan"
shutil.rmtree(S, ignore_errors=True)
os.makedirs(S)

counter = lab.load("counter", lab.CNT)
REF = lab.REF

RECORDS = []
CUR = [None]
EXEC_LINES = set()

def snapshot(d):
    files = {}
    for name in sorted(os.listdir(d)):
        p = os.path.join(d, name)
        try:
            st = os.lstat(p)
        except OSError:
            continue
        ent = {"mode": oct(st.st_mode), "kind": "fifo" if os.path.exists(p) and not os.path.isfile(p) else "file",
               "size": st.st_size}
        if os.path.isfile(p):
            with open(p, "rb") as fh:
                raw = fh.read()
            ent["b64"] = __import__("base64").b64encode(raw).decode()
            ent["sha"] = hashlib.sha256(raw).hexdigest()[:12]
        files[name] = ent
    return files

def fake_execute(tool, d, argv, stdin=None, timeout=30):
    rc, out = lab.cli(argv, stdin or b"")
    rec = {"dir": d, "argv": list(argv),
           "stdin_b64": None if stdin is None else __import__("base64").b64encode(stdin).decode(),
           "files": snapshot(d),
           "rc": rc, "out": out.decode("utf-8", "replace")}
    if CUR[0] is not None:
        CUR[0].append(rec)
    return rc, out, b""

def tracer(frame, event, arg):
    if event == "line" and frame.f_code.co_filename == REF:
        EXEC_LINES.add(frame.f_lineno)
    return tracer

counter.execute = fake_execute

def run_all():
    names = [("gen%d" % i, (lambda i=i: counter.score_gen("T", S, "REV", "NONCE", i))) for i in range(10)]
    names += [(n, (lambda fn=fn: fn("T", S, "REV", "NONCE"))) for n, fn in counter.FIXED]
    out = []
    for name, fn in names:
        CUR[0] = []
        sys.settrace(tracer)
        try:
            ok, why = fn()
        finally:
            sys.settrace(None)
        out.append({"fixture": name, "ok": ok, "why": why, "runs": CUR[0]})
        CUR[0] = None
        print("%-12s ok=%d %s runs=%d" % (name, ok, why, len(out[-1]["runs"])))
    return out

def main():
    res = run_all()
    json.dump(res, open(os.path.join(S, "fixtures.json"), "w"), indent=1, ensure_ascii=False)
    executed = sorted(EXEC_LINES)
    json.dump(executed, open(os.path.join(S, "executed-lines.json"), "w"))
    print("fixtures=%d/%d executed_ref_lines=%d" % (sum(r["ok"] for r in res), len(res), len(executed)))

if __name__ == "__main__":
    main()
