import json, subprocess, sys, os, glob
TOOL="/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-46/l1-draft/mado-devices.py"
KEYS=["kb_layout","kb_variant","kb_options","kb_model","kb_rules","kb_file"]
OUT=[k[3:] for k in KEYS]
def eff(cfg):
    return json.loads(subprocess.run(["./eff",cfg],capture_output=True,text=True,check=True).stdout)
def ex(d,key,g): return d[key][0] if d[key][1] else g[key][0]
def clamp(x): return min(100.0,max(0.0,x))
for cfg in sorted(glob.glob("cfgs/*.conf")):
    e=eff(cfg); g=e["globals"]; kb=[]; mice=[]
    for name,d in e["devices"].items():
        kb.append({"name":name,**{o:ex(d,k,g) for k,o in zip(KEYS,OUT)}})
        if d["scroll_factor"][1]: mice.append({"name":name,"scrollFactor":clamp(d["scroll_factor"][0])})
    kb.append({"name":"extra",**{o:g[k][0] for k,o in zip(KEYS,OUT)}})
    open("dump.json","w").write(json.dumps({"keyboards":kb,"mice":mice}))
    p=subprocess.run([sys.executable,"-I",TOOL,"--devices","dump.json","--config",cfg],capture_output=True,text=True)
    print("==",os.path.basename(cfg),"exit",p.returncode,"err",e["error"],"g.kb_layout",g["kb_layout"],"devs",list(e["devices"]))
    for l in p.stdout.splitlines():
        if l.startswith(("MADO_DEV_KEYBOARD","MADO_DEV_MOUSE","MADO_DEV_BLOCK","MADO_DEVICES")): print("  ",l[:200])
