#!/usr/bin/env python3
"""Reference honest census (scratch only): ss rows joined by inode, no fixture keys."""
import argparse, re, subprocess, sys
a = argparse.ArgumentParser()
for f in ("--ss-file", "--journal-file", "--socket2"): a.add_argument(f)
a.add_argument("--log", action="append", default=[]); a.add_argument("--expect-client", action="append", default=[])
a.add_argument("--disable-logs", default="0"); o = a.parse_args()
s = open(o.ss_file).read() if o.ss_file else subprocess.run(["ss", "-xpa"], capture_output=True, text=True).stdout
L = s.splitlines()
def setup(r): print(f"MADO_EVENTQ: SETUP {r}"); sys.exit(2)
if not L or not L[0].startswith("Netid"): setup("unparseable")
rows = [r.split(None, 8) for r in L[1:] if len(r.split()) >= 8]
lis = [r for r in rows if r[1] == "LISTEN" and (r[4] == o.socket2 if o.socket2 else r[4].endswith("/.socket2.sock"))]
if not lis: setup("socket2 not listening")
sock = lis[0][4]
srv = {r[5]: r for r in rows if r[1] == "ESTAB" and r[4] == sock}
U = lambda r: re.search(r'\(\("([^"]+)",pid=(\d+),fd=(\d+)', r[8] if len(r) > 8 else "")
cl = [(r, srv[r[7]], U(r)) for r in rows if r[1] == "ESTAB" and r[7] in srv and srv[r[7]][7] == r[5] and U(r)]
for r, sv, u in cl:
    print(f"MADO_EVENTQ_CLIENT: comm={u[1]} pid={u[2]} fd={u[3]} peer_recv_q={r[2]} server_send_q={sv[3]}")
M = re.compile(r"\]: Socket2 fd \d+ (overflowed event queue|failed writing event)")
def n(t, k): return sum(1 for l in t.splitlines() if (m := M.search(l)) and m[1].startswith(k))
lg = "".join(open(f).read() for f in o.log); jn = open(o.journal_file).read() if o.journal_file else ""
for src, t in (("log", lg), ("journal", jn)):
    print(f"MADO_EVENTQ_MARKERS: source={src} overflow={n(t, 'overflowed')} write_fail={n(t, 'failed')}")
ov, wf = n(lg + jn, "overflowed"), n(lg + jn, "failed")
miss = [e for e in o.expect_client if e not in [u[1] for _, _, u in cl]]
v = "MARKERS" if ov + wf else "MISSING_CLIENT" if miss else "CLEAN"
print(f"MADO_EVENTQ: socket2={sock} subscribers={len(cl)} overflow={ov} write_fail={wf} "
      f"lagging={sum(r[2] != '0' for r, _, _ in cl)} missing_client={','.join(miss) or '-'} "
      f"markers_observable={'no' if o.disable_logs == '1' else 'yes'} verdict={v}")
sys.exit(0 if v == "CLEAN" else 1)
