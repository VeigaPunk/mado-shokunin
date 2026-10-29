import json, os, subprocess, sys
from pathlib import Path
E = Path(sys.argv[1]); tool = sys.argv[2]
base = E / ".ufo/waves/round-56/fixtures/c2"
ok = 0; bad = []
for fx in sorted(base.iterdir()):
    args = [a.replace("{FX}", str(fx)) for a in json.loads((fx / "args.json").read_text())]
    env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "LC_ALL": "C"}
    p = subprocess.run(["python3", "-I", str(E / tool), *args], cwd=E, env=env, capture_output=True)
    exp = (fx / "expected.out").read_bytes(); erc = int((fx / "expected.rc").read_text().strip())
    if p.stdout == exp and p.returncode == erc: ok += 1
    else: bad.append(fx.name)
print(f"tool={tool} committed={ok}/{len(list(base.iterdir()))} mismatches={bad}")
