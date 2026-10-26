#!/bin/bash
# Recreates the fixtures battery.sh uses, under ./fx (run from the directory that holds battery.sh).
set -u
mkdir -p fx && cd fx || exit 1
mkfifo fifo 2>/dev/null
mkdir -p dir
python3 - <<'EOF'
import json, os
open("pad1048576.conf", "w").write(("windowrule = size 10 20, match:class a\n").ljust(1048576, "#"))
open("pad1048577.conf", "w").write(("windowrule = size 10 20, match:class a\n").ljust(1048577, "#"))
open("ctl.conf", "w").write("windowrule = size 10 20, match:class a\n")
open("empty.conf", "w").write("")
open("v2only.conf", "w").write("windowrulev2 = size 10 20, class:a\n")
open("tagrule.conf", "w").write("windowrule = size 10 20, match:tag floating-window\n")
open("titlematch.conf", "w").write("windowrule = size 10 20, match:class a, match:title b\n")
open("bracket.conf", "w").write("windowrule = size 10 20, match:class ^[Ff]irefox$\n")
open("d201.conf", "w").write("windowrule = size 10 20, match:class " + "a" * 201 + "\n")
open("d200.conf", "w").write("windowrule = size 10 20, match:class " + "a" * 200 + "\n")
open("r10.conf", "w").write("windowrule = size 10 20, match:class a\n")
open("r30.conf", "w").write("windowrule = size 30 40, match:class a\n")
open("tabs.conf", "w").write("windowrule\t=\tsize\t10\t20,\tmatch:class\ta\n")
open("noeol.conf", "w").write("windowrule = size 10 20, match:class a")
open("bom.conf", "w").write("\ufeffwindowrule = size 10 20, match:class a\n")
open("notlist.json", "w").write("{}")
open("emptylist.json", "w").write("[]")
open("c_agree.json", "w").write(json.dumps([{"class": "a", "size": [10, 20], "floating": True, "mapped": True, "address": "0x1"}]))
open("c_differ.json", "w").write(json.dumps([{"class": "a", "size": [11, 20], "floating": True, "mapped": True, "address": "0x1"}]))
open("c_nomatch.json", "w").write(json.dumps([{"class": "b", "size": [10, 20], "floating": True, "mapped": True, "address": "0x2"}]))
open("c_empty.json", "w").write("[]")
open("c1048576.json", "w").write('[{"class":"a","size":[10,20],"floating":true,"mapped":true}]'.ljust(1048576, " "))
EOF
cp ctl.conf noperm.conf && chmod 000 noperm.conf
ln -sf ctl.conf link.conf
ls -l | awk '{print $1, $5, $9}'
