#!/bin/sh
# R48 RevengerCache probe 4: what the cache buys, on this host and filesystem.
# 300 synthetic entries in scratch; warm hit vs cold resolve, n=15 each.
set -eu
S=${1:-/fast/scratch/hyaku/mado-r48/RevengerCache/probe-latency}
rm -rf -- "$S"
mkdir -p "$S/config" "$S/cfgdir" "$S/data/applications" "$S/data2/applications" "$S/bin" "$S/c1" "$S/c2"
export XDG_CONFIG_HOME="$S/config" XDG_CONFIG_DIRS="$S/cfgdir"
export XDG_DATA_HOME="$S/data" XDG_DATA_DIRS="$S/data2"
export PATH="$S/bin:/usr/bin:/bin"
unset XDG_CURRENT_DESKTOP 2>/dev/null || true
python3 - "$S" <<'PY'
import os, sys
S = sys.argv[1]
body = ('[Desktop Entry]\nType=Application\nName=T{n}\nTerminal=true\n'
        'Categories=System;TerminalEmulator;\nX-TerminalArgExec=-e\nExec=termA --flag\n')
for i in range(300):
    open(os.path.join(S, "data2/applications", "t%03d.desktop" % i), "w").write(body.format(n=i))
open(os.path.join(S, "config/xdg-terminals.list"), "w").write("termA.desktop\n")
open(os.path.join(S, "data/applications/termA.desktop"), "w").write(body.format(n=0))
PY
printf '#!/bin/sh\nexit 0\n' > "$S/bin/termA"; chmod +x "$S/bin/termA"
printf 'fixture size: '; du -sh "$S/data2/applications" | cut -f1
python3 - "$S" <<'PY'
import os, subprocess, time, shutil, statistics, sys
S = sys.argv[1]; X = "/usr/bin/xdg-terminal-exec"; env = dict(os.environ)
def run(ch):
    e = dict(env); e["XDG_CACHE_HOME"] = ch
    t = time.perf_counter(); subprocess.run([X, "--print-cmd"], env=e, stdout=subprocess.DEVNULL)
    return (time.perf_counter() - t) * 1000.0
def wait(p):
    n = 0
    while not os.path.exists(p) and n < 4000:
        n += 1
warm = []; cold = []
for _ in range(15):
    c = os.path.join(S, "c1"); shutil.rmtree(c, ignore_errors=True); os.makedirs(c)
    run(c); wait(os.path.join(c, "xdg-terminal-exec")); warm.append(run(c))
    c2 = os.path.join(S, "c2"); shutil.rmtree(c2, ignore_errors=True); os.makedirs(c2)
    cold.append(run(c2)); wait(os.path.join(c2, "xdg-terminal-exec"))
print("warm hit  median %5.1f ms (n=15)" % statistics.median(warm))
print("cold      median %5.1f ms (n=15)" % statistics.median(cold))
print("cold/warm          %.1fx" % (statistics.median(cold) / statistics.median(warm)))
PY
