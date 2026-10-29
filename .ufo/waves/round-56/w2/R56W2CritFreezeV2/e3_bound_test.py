import importlib.util
spec=importlib.util.spec_from_file_location("c1","/fast/scratch/hyaku/mado-r56/R56W2CritFreezeV2/e3/c1.py")
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
data=open("/fast/scratch/hyaku/mado-r56/R56W2CritFreezeV2/p_Hyprland-ConfigWatcher.cpp","rb").read()
pl=data.split(b"\n"); n=len(pl); wc=data.count(b"\n")
print("wc-l",wc,"len(split)",n,"last line in split is empty:",pl[-1]==b"")
base="Hyprland-ConfigWatcher.cpp"
for anchor,line in [(f"{base}:100-{wc}",100),(f"{base}:100-{wc+1}",100),(f"{base}:100-{wc+2}",100),(f"{base}:{wc+1}",wc+1)]:
    print(f"{anchor!s:45} line={line} nlines=len(split)={n} -> scope_covers={m.scope_covers(anchor, base, line, n)}")
