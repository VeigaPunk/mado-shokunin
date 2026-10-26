import json, os, subprocess, sys
SCR="/fast/scratch/hyaku/mado-r46/CritC1Narrow"
REF="/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-46/l1-draft/mado-devices.py"
d=os.path.join(SCR,"demo"); os.makedirs(d,exist_ok=True)
dump={"mice":[{"name":"mouse-1","scrollFactor":-1.0}],"keyboards":[{"name":"kbd-1","layout":"us","variant":"","options":"","model":"","rules":""}],"tablets":[],"touch":[],"switches":[]}
dp=os.path.join(d,"devs.json"); open(dp,"w").write(json.dumps(dump))
cfg=os.path.expanduser("~/.config/hypr/hyprland.conf")
for label,tool in (("reference",REF),("P02-source-unsupported",os.path.join(SCR,"work-P02-source-unsupported/mado-devices.py"))):
    p=subprocess.run([sys.executable,"-I",tool,"--devices",dp,"--config",cfg],capture_output=True,cwd=d)
    last=[l for l in p.stdout.decode().split("\n") if l.startswith("MADO_DEVICES:")]
    print("%-26s rc=%d %s" % (label,p.returncode,last[-1] if last else "NO-OUTPUT"))
