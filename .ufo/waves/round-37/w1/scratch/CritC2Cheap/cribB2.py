#!/usr/bin/env python3
import argparse, re, sys
a = argparse.ArgumentParser()
for f in ("--ss-file", "--journal-file", "--socket2"): a.add_argument(f)
a.add_argument("--log", action="append", default=[]); a.add_argument("--expect-client", action="append", default=[])
a.add_argument("--disable-logs", default="0"); o = a.parse_args()
s = open(o.ss_file).read()
if ".socket2" not in s: print("MADO_EVENTQ: SETUP no socket2"); sys.exit(2)
cl = re.findall(r'ESTAB\s+(\d+)\s+(\d+)\s+\*\s.*\("(waybar|socat)",pid=(\d+),fd=(\d+)', s)
for r, q, c, p, d in cl: print(f"MADO_EVENTQ_CLIENT: comm={c} pid={p} fd={d} peer_recv_q={r} server_send_q={q}")
def n(t, k): return sum("Socket2 fd" in l and k in l for l in t.splitlines())
lg = "".join(open(f).read() for f in o.log); jn = open(o.journal_file).read()
for src, t in (("log", lg), ("journal", jn)): print(f"MADO_EVENTQ_MARKERS: source={src} overflow={n(t,'overflowed')} write_fail={n(t,'failed writing')}")
ov, wf = n(lg + jn, "overflowed"), n(lg + jn, "failed writing")
miss = [e for e in o.expect_client if e not in [c[2] for c in cl]]
v = "MARKERS" if ov + wf else "MISSING_CLIENT" if miss else "CLEAN"
print(f"MADO_EVENTQ: socket2=x subscribers={len(cl)} overflow={ov} write_fail={wf} lagging={sum(c[0] != '0' for c in cl)} "
      f"missing_client={','.join(miss) or '-'} markers_observable={'no' if o.disable_logs == '1' else 'yes'} verdict={v}")
sys.exit(0 if v == "CLEAN" else 1)
