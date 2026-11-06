import json, subprocess, sys
import os
ORA=os.environ.get('ORACLE','ore')  # cc -O0 -o ore .ufo/waves/round-89/controls/posix-ere-oracle.c
r88=json.load(open('.ufo/waves/round-88/controls/mako-cases-r88.json'))
carried=[c for c in r88['cases'] if c['id']!='c53-summary-tilde-refused']
cfgp=".config/mako/config"
T="\t"
# (id, header-as-written, args, oracle checks [(pattern-after-tokenizer, field)] or None, expectation-kind override, pin)
new=[
 ("r01-host-setup-wifi",'summary~="Setup Wi-Fi"',{"summary":"Setup Wi-Fi"},"host core.ini:24 header; criteria.c regexec"),
 ("r02-unanchored-substring","summary~=Wi-Fi",{"summary":"Setup Wi-Fi now"},"criteria.c regexec searches (no implicit anchors)"),
 ("r03-ere-plus","summary~=hel+o",{"summary":"say helllo"},"REG_EXTENDED: + is a quantifier"),
 ("r04-body-alternation","body~=foo|bar",{"body":"bar"},"REG_EXTENDED: | alternation; body~ field"),
 ("r05-posix-digit-class","summary~=^[[:digit:]]+$",{"summary":"2026"},"POSIX bracket class [:digit:]"),
 ("r06-backslash-d-is-literal-d","body~=\\\\d",{"body":"d"},"glibc ERE: \\d is not a digit class"),
 ("r07-backslash-d-not-digit","body~=\\\\d",{"body":"5"},"glibc ERE: \\d does not match 5"),
 ("r08-c-locale-dot","summary~=^.$",{"summary":"\u00e9"},"mako never calls setlocale: C locale, . is one byte"),
 ("r09-c-locale-word","summary~=^\\\\w+$",{"summary":"\u00e9"},"C locale: \\w does not cover UTF-8 letters"),
 ("r10-gnu-word-boundary","summary~=\\\\<foo\\\\>",{"summary":"a foo b"},"glibc: \\< \\> word boundaries"),
 ("r11-invalid-inline-flag","summary~=(?i)x",{"summary":"x"},"regcomp rejects (?i): criteria rejected"),
 ("r12-invalid-open-interval","summary~=a{1",{"summary":"a{1"},"regcomp rejects an unclosed interval"),
 ("r13-double-star-valid","summary~=a**",{"summary":"a"},"glibc ERE accepts a** (Python re does not)"),
 ("r14-quoted-backslash-escapes-dot",'summary~="1\\.0"',{"summary":"1x0"},"parse_criteria QUOTE_ESCAPE drops the backslash: regex 1.0"),
 ("r15-quoted-double-backslash",'summary~="1\\\\.0"',{"summary":"1x0"},"parse_criteria: \\\\ in quotes yields one backslash: regex 1\\.0"),
 ("r16-tab-inside-token","summary~=a"+T+"b",{"summary":"a"+T+"b"},"parse_criteria splits on a space only"),
 ("r17-summary-and-pattern","summary=x summary~=x",{"summary":"x"},"criteria.c: Cannot set both summary and summary~"),
 ("r18-body-and-pattern","body=x body~=y",{"body":"x"},"criteria.c: Cannot set both body and body~"),
 ("r19-pattern-without-input","body~=x",{},"tool stance: a field without its input is refused"),
 ("r20-summary-pattern-not-body","summary~=^alpha$",{"summary":"beta","body":"alpha"},"summary~ matches the summary only"),
 ("r21-no-match","summary~=zzz",{"summary":"abc"},"regexec REG_NOMATCH"),
 ("r22-invalid-with-other-mismatch","app-name=other summary~=(",{"app-name":"alpha","summary":"("},"regcomp failure rejects the criteria regardless of other fields"),
 ("r23-empty-pattern","summary~=",{"summary":"anything"},"regcomp of an empty ERE"),
 ("r24-utf8-literal","summary~=\u00e9",{"summary":"caf\u00e9"},"byte-literal UTF-8 match in the C locale"),
 ("r25-c-locale-bracket","summary~=^[\u00e9]$",{"summary":"\u00e9"},"C locale: [é] is a set of two bytes"),
 ("r26-mode-and-pattern",'mode=do-not-disturb summary~="Update System"',{"summary":"Update System","mode":["do-not-disturb"]},"host core.ini:27 under DND"),
 ("r27-case-sensitive","summary~=setup",{"summary":"Setup Wi-Fi"},"no REG_ICASE"),
 ("r28-end-anchor","summary~=Fi$",{"summary":"Setup Wi-Fi"},"$ anchors at the end"),
 ("r29-ere-interval","summary~=^a{2}$",{"summary":"aa"},"REG_EXTENDED: {2} is an interval"),
 ("r30-ere-optional","summary~=colou?r",{"summary":"color"},"REG_EXTENDED: ? quantifier"),
 ("r31-unquoted-escape-drops-backslash","summary~=1\\.0",{"summary":"1x0"},"parse_criteria ESCAPE state drops the backslash outside quotes too: regex 1.0 (R89MReviewC1 M33)"),
 ("r32-earlier-invalid-occurrence","summary~=a(b summary~=x",{"summary":"x"},"criteria.c apply_criteria_field regcomps each occurrence in order: the first fails (R89MReviewC1 F1)"),
 ("n04-reg-newline-dot-crosses-newline","body~=a.b",{"body":"a\nb"},"no REG_NEWLINE: . matches a newline byte (R89MMutTester N04)"),
 ("n04-reg-newline-caret-after-newline","body~=^b",{"body":"a\nb"},"no REG_NEWLINE: ^ anchors at the start of the value only (R89MMutTester N04)"),
 ("n07-dangling-quote-escape-refused",'summary~="abc\\',{"summary":"abc"},"parse_criteria: QUOTE_ESCAPE at end of input is an unmatched quote (R89MMutTester N07)"),
]
def untok(h):
    # minimal reimplementation of upstream parse_criteria for the oracle (independent of the tool)
    toks=[];w=[];st='N';i=0
    while i<len(h):
        ch=h[i]
        if st in('E','QE'):
            w.append(ch); st='N' if st=='E' else 'Q'
        elif st=='Q':
            if ch=='\\': st='QE'
            elif ch=='"': st='N'
            else: w.append(ch)
        else:
            if ch=='\\': st='E'
            elif ch=='"': st='Q'
            elif ch==' ':
                toks.append(''.join(w)); w=[]
            else: w.append(ch)
        i+=1
    if st!='N':
        return None  # criteria.c 226-239: unmatched quote / trailing backslash rejects the criteria
    toks.append(''.join(w))
    return [t for t in toks if t]
out=[]
for cid,hdr,args,pin in new:
    toks=untok(hdr)
    if toks is None:
        exp={"effective":{"anchor":"top-right"},"refusals":"present"}
        out.append({"id":cid,"config":cfgp,"home_files":{cfgp:"anchor=top-right\n["+hdr+"]\nanchor=bottom-center\n"},"args":dict(args),"expect":exp,"pin":pin,"oracle":"tokenizer-rejects"})
        print(cid,'refused tokenizer'); continue
    kv=[(t.split('=',1)[0],t.split('=',1)[1]) for t in toks]
    keys=[k for k,_ in kv]
    refused=False; match=True; why=[]
    if ('summary' in keys and 'summary~' in keys) or ('body' in keys and 'body~' in keys):
        refused=True; why.append('both')
    for k,v in kv:
        if k in('summary~','body~'):
            r=subprocess.run([ORA,v,'x'],capture_output=True,text=True).stdout.strip()
            if r=='invalid': refused=True; why.append('invalid')
    if not refused:
        undecided=False
        for k,v in kv:
            if k in('summary~','body~'):
                fld=k[:-1]
                if fld not in args: undecided=True; continue
                r=subprocess.run([ORA,v,args[fld]],capture_output=True,text=True).stdout.strip()
                why.append(f'{k}:{r}')
                match = match and r=='match'
            elif k=='app-name': match = match and args.get('app-name')==v
            elif k=='mode': match = match and v in (['default']+args.get('mode',[]))
            elif k in('summary','body'): match = match and args.get(k)==v
        if not match: pass
        elif undecided: refused=True; why.append('undecided')
    if refused: exp={"effective":{"anchor":"top-right"},"refusals":"present"}
    elif match: exp={"effective":{"anchor":"bottom-center"},"refusals":"none"}
    else: exp={"effective":{"anchor":"top-right"},"refusals":"none"}
    a=dict(args)
    out.append({"id":cid,"config":cfgp,"home_files":{cfgp:"anchor=top-right\n["+hdr+"]\nanchor=bottom-center\n"},"args":a,"expect":exp,"pin":pin,"oracle":" ".join(why) or "-"})
    print(cid, exp['effective']['anchor'], exp['refusals'], why)
blind=json.load(open('.ufo/waves/round-89/controls/mako-cases-r89-blind.json'))['cases']
doc={"schema":"mako-cases-r89-v1","notes":"Round-89 C1 case set: the 61 round-88 cases carried byte-equal (c53-summary-tilde-refused superseded: summary~ is now modelled) followed by the round-89 summary~/body~ cases. Expectations for r01-r30 come from posix-ere-oracle.c (libc regcomp REG_EXTENDED|REG_NOSUB + regexec, C locale, no setlocale) after an independent re-implementation of mako 1.11.0 criteria.c parse_criteria, never from the candidate tool. Authored by the L1 (MadoR89), disclosed; blind seat cases b01-b44 (R89MScoutCases, controls/mako-cases-r89-blind.json) follow unchanged. r31/r32 and n04/n07 were added from the w1 review before the freeze. Regenerate: ORACLE=<built oracle> python3 .ufo/waves/round-89/controls/gen-c1-cases-r89.py","cases":carried+out+blind}
open('.ufo/waves/round-89/controls/mako-cases-r89.json','w').write(json.dumps(doc,indent=1,ensure_ascii=False)+"\n")
print(len(doc['cases']))
