import hashlib, importlib.util, os, re, sys
C="/home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c2-r44-gkeep-size-request.py"
spec=importlib.util.spec_from_file_location("c2r44",C); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
LANE="/home/vgpnk/Projects/shokunin/mado-shokunin/"
DRAFT=LANE+".ufo/waves/round-44/w1/ScrLessonSkeleton/round-44-lesson.md"
text=open(DRAFT,encoding="utf-8").read()
sec=m.section(text,"## Gate") if hasattr(m,"section") else None
if sec is None:
    # fallback: slice manually
    i=text.index("\n## Gate\n"); j=text.index("\n## ",i+1)
    sec=text[i+1:j]
lines=sec
gates={}
for l in lines:
    mm=m.GATE_RE.match(l.rstrip("\n")) if hasattr(m,"GATE_RE") else None
    if mm:
        gates.setdefault(mm.group(1),[]).append((mm.group(2),mm.group(3),mm.group(4)))
print("gate lines outside section:", len([l for l in text.split("\n") if re.match(r"^GATE S\d",l)]) - sum(len(v) for v in gates.values()))
print("ids:",sorted(gates))
raw={}
ok=True
for i,gl in sorted(gates.items()):
    if len(gl)!=1: print("FAIL count",i,len(gl)); ok=False; continue
    path,digest,q=gl[0]
    full=LANE+path
    b=open(full,'rb').read()
    h=hashlib.sha256(b).hexdigest()
    nq=m.norm(q)
    occ=m.occurrences(b,nq); line=m.quote_at(b,nq)
    incode=m.quote_in_code(b,nq,os.path.basename(path))
    others={n:len(m.occurrences(open(LANE+".ufo/waves/round-44/fetch/"+n,'rb').read(),nq)) for n in ["Hyprland-Window.cpp","Hyprland-XDGShell.cpp","xdg-shell.xml","gdktoplevel-wayland.c","gkeep-ui.py"] if os.path.basename(path)!=n}
    pin_ok = (os.path.basename(path) not in m.PINS) or m.PINS[os.path.basename(path)]==h
    good = h==digest and len(b)>=256 and len(occ)==1 and incode and 3<=len(nq.split())<=25 and all(v==0 for v in others.values()) and pin_ok
    ok &= good
    print(("OK  " if good else "FAIL"), i, "sha",h[:12],"pin",pin_ok,"words",len(nq.split()),"occ",len(occ),"line",line,"code",incode,"others",others)
print("GATE ALL OK" if ok else "GATE PROBLEMS")
ad=[l for l in lines if l.startswith("ADMIT ")]; rf=[l for l in lines if l.startswith("REFUSE ")]
print("admits",len(ad),"refuses",len(rf))
staged_ok=lambda p:(p=='merge/mado/knowledge/corpus/knowledge/'+os.path.basename(p) and os.path.basename(p) in m.STAGED)
for a in ad:
    mm=m.ADMIT_RE.match(a); print("ADMIT parse",bool(mm), mm.groups() if mm else None, "staged_ok", staged_ok(mm.group(1)) if mm else None)
for r in rf:
    mm=m.REFUSE_RE.match(r)
    print("REFUSE parse",bool(mm), "staged_ok", staged_ok(mm.group(1)) if mm else None,
          "distinct_words",len(set(mm.group(2).lower().split())) if mm else 0,
          "flipword",bool(re.search(r'\b(superseded|until|unless|once|when|if|after)\b', mm.group(2).lower())) if mm else None)
# BAD_LOC in lesson lines
print("BAD_LOC hits:",[b for b in m.BAD_LOC if b in text.lower()])
