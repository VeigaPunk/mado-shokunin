import sys, os
sys.path.insert(0,"/fast/scratch/hyaku/mado-r56/R56W2Sentinel/p1")
import importlib.util
spec = importlib.util.spec_from_file_location("wp","/fast/scratch/hyaku/mado-r56/R56W2Sentinel/p1/wp.py")
wp = importlib.util.module_from_spec(spec); spec.loader.exec_module(wp)
BASE="/fast/scratch/hyaku/mado-r56/R56W2Sentinel/p1/tree_inj3"
opts={"--config":BASE+"/hyprland.conf","--display-root":BASE}
plan=wp.Plan(opts)
plan.add_entry(plan.config,"main")
plan.parse_file(plan.config,0)
print("entries:",len(plan.entries))
for e in plan.entries[:40]: print("   ",e)
