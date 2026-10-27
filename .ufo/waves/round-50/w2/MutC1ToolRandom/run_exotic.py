#!/usr/bin/env python3
"""Compile 31 targeted exotic RMLVO keymaps and compare tool/judge on keysyms present in each."""
import hashlib, json, os, re, subprocess, sys
camp_path, lane, work, outdir = sys.argv[1:5]
JUDGE='/usr/lib/xkbcommon/xkbcli-how-to-type'; COMPILE='/usr/lib/xkbcommon/xkbcli-compile-keymap'
env={'PATH':'/usr/bin','HOME':work+'/fakehome','XDG_CONFIG_HOME':work+'/fakehome/.config','XDG_CACHE_HOME':work+'/fakehome/.cache','XDG_DATA_HOME':work+'/fakehome/.local/share','XDG_STATE_HOME':work+'/fakehome/.local/state','TMPDIR':work+'/tmp','LC_ALL':'C'}
os.makedirs(work+'/keymaps',exist_ok=True); os.makedirs(work+'/tmp',exist_ok=True); os.makedirs(work+'/fakehome/.config',exist_ok=True); os.makedirs(outdir,exist_ok=True)
camp=json.load(open(camp_path)); specs=camp['exotic']; tool=lane+'/tools/mado-keysym.py'
# Keysym tokens in compiler-serialized keymaps; explicit family additions ensure dead/LevelThree cases are queried.
pat=re.compile(rb'\b(?:dead_[A-Za-z0-9_]+|[A-Za-z][A-Za-z0-9_]+|[0-9])\b')
extra=['dead_acute','dead_grave','dead_tilde','dead_circumflex','dead_cedilla','dead_diaeresis','dead_abovering','dead_caron','dead_breve','dead_belowdot','EuroSign','section','degree','plusminus','multiply','division','kana_A','Hangul','Cyrillic_ya','Arabic_alef','Greek_alpha','F35','KP_Enter','XF86AudioMute']
# Valid names sourced from system header; avoids wasting all cases on invalid symbols.
header=open('/usr/include/xkbcommon/xkbcommon-keysyms.h',encoding='utf8').read()
known=set(re.findall(r'^#define\s+XKB_KEY_([A-Za-z0-9_]+)\s+',header,re.M))
extra=[x for x in extra if x in known]
rows=[]; compile_errors=[]
for i,s in enumerate(specs):
 p=f'{work}/keymaps/e{i:02d}.xkb'
 cmd=[COMPILE,'--include=/usr/share/xkeyboard-config-2','--rules=evdev','--model='+s['model'],'--layout='+s['layout'],'--variant='+s['variant'],'--options='+s['options']]
 with open(p,'wb') as f: cr=subprocess.run(cmd,stdout=f,stderr=subprocess.PIPE,env=env,stdin=subprocess.DEVNULL,timeout=60)
 if cr.returncode or not os.path.getsize(p):
  compile_errors.append({'index':i,'spec':s,'rc':cr.returncode,'stderr':cr.stderr.decode('utf8','replace')[:500]}); continue
 data=open(p,'rb').read(); names=set(x.decode('ascii') for x in pat.findall(data) if x.decode('ascii') in known); names.update(extra)
 # Deterministic bounded sample, max 200 unique keysym args per keymap.
 args=sorted(names)[:200]
 for arg in args:
  base=[JUDGE,'--keymap='+p,'--disable-compose','--keysym',arg]
  j=subprocess.run(base,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,env=env,stdin=subprocess.DEVNULL,timeout=60)
  t=subprocess.run(['python3','-I',tool,'how-to-type','--keymap',p,'--disable-compose','--keysym',arg],stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,env=env,stdin=subprocess.DEVNULL,timeout=60)
  match=j.returncode==t.returncode and j.stdout==t.stdout
  if not match: rows.append({'index':i,'arg':arg,'judge_rc':j.returncode,'tool_rc':t.returncode,'judge_sha256':hashlib.sha256(j.stdout).hexdigest(),'tool_sha256':hashlib.sha256(t.stdout).hexdigest()})
summary={'exotic_specs':len(specs),'compiled':len(specs)-len(compile_errors),'compile_errors':compile_errors,'pairs_compared':sum(1 for _ in []),'mismatch_count':len(rows),'mismatches':rows}
# Count result rows exactly from loop by per-spec counter.
summary['pairs_compared']=sum(min(200,len(set(x for x in []))) for _ in [])
# Recompute deterministic compared count from completed keymap files and token selection.
count=0
for i in range(len(specs)):
 p=f'{work}/keymaps/e{i:02d}.xkb'
 if os.path.exists(p) and os.path.getsize(p):
  data=open(p,'rb').read(); names=set(x.decode('ascii') for x in pat.findall(data) if x.decode('ascii') in known); names.update(extra); count+=min(200,len(names))
summary['pairs_compared']=count
with open(outdir+'/exotic-summary.json','w') as f: json.dump(summary,f,indent=1)
print(json.dumps(summary,indent=1)[:5000])
