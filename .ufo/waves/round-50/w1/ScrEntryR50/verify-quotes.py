#!/usr/bin/env python3
"""Offline quote/locator verifier for the round-50 bind entry."""
import argparse, hashlib, re, sys
from pathlib import Path

QRE = re.compile(r"(?:`([^`\n]{2,})`|\"([^\"\n]{2,})\")\s*(?:,\s*| at\s+|,\s*\(|\(\s*)([A-Za-z0-9._/-]+:\d+(?:-\d+)?)")
TOPICS = (
 ("state","Hyprland-KeybindManager.cpp",r"m_resolveBindsBySym\s*\?\s*pKeyboard->m_xkbSymState\s*:\s*m_xkbTranslationState"),
 ("case","Hyprland-KeybindManager.cpp",r"KBKEYLOWER\s*=\s*xkb_keysym_from_name\(.*XKB_KEYSYM_CASE_INSENSITIVE"),
 ("mask","Hyprland-KeybindManager.cpp",r"modmask\s*!=\s*k->modmask\s*&&\s*!k->ignoreMods"),
 ("code-form","Hyprland-legacy-ConfigManager.cpp",r"key\.starts_with\(\"code:\"\)"),
 ("zero-mod-sym-state","Hyprland-IKeyboard.cpp",r"xkb_state_update_mask\(m_xkbSymState,\s*0,\s*0,\s*0,\s*0,\s*0,"),
 ("depressed-mask","Hyprland-InputManager.cpp",r"m_lastMods\s*=\s*MODS\.depressed"),
 ("option-read","Hyprland-InputManager.cpp",r"getDeviceInt\(devname,\s*\"resolve_binds_by_sym\",\s*\"input:resolve_binds_by_sym\"\)"),
)
EXTS=(".md",".bats",".list",".scd",".py",".xml",".cpp",".hpp",".h",".conf",".txt",".desktop",".sh",".json",".toml")
def stem(s):
 s=Path(s).name.lower()
 for e in EXTS:
  if s.endswith(e): return s[:-len(e)]
 return s
def locate(tok,pins):
 b=Path(tok).name
 if b in pins:return b
 c=[n for n in pins if stem(b) in stem(n) or stem(n) in stem(b)]
 return c[0] if len(c)==1 else None
def occurrences(blob,q):
 raw=blob.decode("utf-8","replace")
 text=[]; line_map=[]; prev=True
 for ln,line in enumerate(raw.split("\n"),1):
  for ch in line+"\n":
   if ch.isspace():
    if not prev: text.append(" "); line_map.append(ln); prev=True
   else: text.append(ch); line_map.append(ln); prev=False
 text="".join(text); out=[]; start=0
 while True:
  k=text.find(q,start)
  if k<0:return out
  bef=text[k-1] if k else " "; aft=text[k+len(q)] if k+len(q)<len(text) else " "
  word=lambda c:c.isalnum() or c=="_"
  if not (word(q[0]) and word(bef)) and not (word(q[-1]) and word(aft)): out.append(line_map[k])
  start=k+1
def main():
 ap=argparse.ArgumentParser()
 ap.add_argument("--entry",default=str(Path(__file__).with_name("hyprland-bind-key-match-r50.md")))
 ap.add_argument("--fetch",default="/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-49/fetch")
 ap.add_argument("--rows",default="/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-49/candidate/rows.md")
 ap.add_argument("--held-fetch",default="/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-46/fetch")
 ap.add_argument("--held-rows",default="/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md")
 ap.add_argument("--output",default="-")
 a=ap.parse_args(); entry=Path(a.entry).read_text(); rows=Path(a.rows).read_text()+Path(a.held_rows).read_text()
 pins={}
 for root in (Path(a.fetch),Path(a.held_fetch)):
  pins.update({p.name:p.read_bytes() for p in root.rglob('*') if p.is_file()})
 row_names=set(re.findall(r"round-\d+/fetch/([A-Za-z0-9._/-]+)",rows))
 row_hashes=set(re.findall(r"(?<![0-9a-f])[0-9a-f]{64}(?![0-9a-f])",rows))
 cited={n for n,b in pins.items() if n in row_names or hashlib.sha256(b).hexdigest() in row_hashes}
 lines=entry.splitlines(); errors=[]; quote_count=0; verified=0
 def check_line(line,lineno):
  nonlocal quote_count,verified
  hits=[]
  for m in QRE.finditer(line):
   span=m.group(1) or m.group(2); tok=m.group(3); q=" ".join(span.split()); words=q.split()
   if len(words)<2: continue
   quote_count+=1
   if len(words)>25: errors.append(f"quote >25 words entry:{lineno}"); continue
   mm=re.fullmatch(r"(.+):(\d+)(?:-(\d+))?",tok); pin=locate(mm.group(1),pins) if mm else None
   if pin is None or pin not in cited: errors.append(f"unresolved or uncited locator {tok} entry:{lineno}"); continue
   lo=int(mm.group(2)); hi=int(mm.group(3) or lo); pl=pins[pin].decode('utf-8','replace').splitlines()
   if lo<1 or hi<lo or hi>len(pl): errors.append(f"out-of-range {tok} entry:{lineno}"); continue
   at=occurrences(pins[pin],q)
   if not at: errors.append(f"quote absent from {pin} entry:{lineno}"); continue
   if not any(lo<=x<=hi for x in at): errors.append(f"quote outside range {tok} entry:{lineno}"); continue
   hits.append((pin,lo,hi)); verified+=1
  return hits
 steps=[]; bystep={}
 for n,line in enumerate(lines,1):
  if re.match(r"^\d+\.\s",line):
   steps.append((n,line)); bystep[n]=check_line(line,n)
  else: check_line(line,n)
 for n,line in steps:
  if not bystep[n]: errors.append(f"step without verified quote entry:{n}")
 topic_hits={}
 for topic,pinname,pattern in TOPICS:
  targets=[i for i,l in enumerate(pins.get(pinname,b'').decode('utf-8','replace').splitlines(),1) if re.search(pattern,l)]
  ok=False
  for n,_ in steps:
   for m in QRE.finditer(lines[n-1]):
    token=m.group(3); mm=re.fullmatch(r"(.+):(\d+)(?:-(\d+))?",token)
    if not mm or locate(mm.group(1),pins)!=pinname: continue
    lo=int(mm.group(2)); hi=int(mm.group(3) or lo); q=" ".join((m.group(1) or m.group(2)).split())
    if len(q.split())<2: continue
    src=pins[pinname].decode('utf-8','replace').splitlines()
    if any(lo<=x<=hi for x in targets) and any(lo<=x<=hi for x in occurrences(pins[pinname],q)):
     ok=True; break
   if ok: break
  topic_hits[topic]=ok
  if not ok: errors.append(f"topic unanswered: {topic}")
 out=[f"pins={len(pins)} row_cited_pins={len(cited)} numbered_steps={len(steps)} quotes={quote_count} verified_quotes={verified}"]
 out += [f"topic {k}={'PASS' if v else 'FAIL'}" for k,v in topic_hits.items()]
 out += [f"ERROR {e}" for e in errors]
 out += ["PASS" if not errors else f"FAIL errors={len(errors)}"]
 result="\n".join(out)+"\n"
 if a.output=="-": print(result,end="")
 else: Path(a.output).write_text(result)
 return 0 if not errors else 1
if __name__=="__main__": sys.exit(main())
