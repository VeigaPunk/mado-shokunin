import importlib.util,json,sys
sys.path.insert(0,"/fast/scratch/hyaku/mado-r56/R56W2CritFreezeV2/hmod")
spec=importlib.util.spec_from_file_location("m","/fast/scratch/hyaku/mado-r56/R56W2CritFreezeV2/hmod/r56_ctl_c2.py")
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
root="/fast/scratch/hyaku/mado-r56/R56W2CritFreezeV2/ho/.ufo/waves/round-56/fixtures/c2-holdout"
got=m.commitment(root)
want=json.load(open("/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/frozen-tables-v2.json"))["c2"]["holdout_commit_sha256"]
print("holdout commitment at 28fc86ac:",got); print("frozen (323a69c9):           ",want); print("MATCH" if got==want else "MISMATCH")
