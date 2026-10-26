import json, os, subprocess
W="/fast/scratch/hyaku/mado-r43/ExecC1ExtraMutants/witness"
os.makedirs(W, exist_ok=True)
open(os.path.join(W,"cd.json"),"w").write('[{"class":"a","size":[1,3],"floating":true}]')
open(os.path.join(W,"float.conf"),"w").write("windowrule = float on, match:class a\n")
