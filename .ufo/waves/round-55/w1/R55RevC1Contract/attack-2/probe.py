import re
def topic(p): return bool(re.search(r"repeat|delay|numlock", p, re.I))
def words(q): return {w.lower() for w in re.findall(r"\w+", q) if len(w) >= 6}
honest = {"K04":"The repeat rate is clamped at zero before it is applied to the keyboard.",
 "K05":"The repeat delay is clamped at zero before it is applied to the keyboard.",
 "K06":"The numlock state is assigned from the numlock option when the keymap is set.",
 "K10":"The seat receives the keyboard's repeat settings through the seat update call.",
 "K16":"A value the user never set falls back to the global option.",
 "H02":"The host config sets the repeat delay to 250 milliseconds.",
 "K17":"A repeat rate of zero disables repeating regardless of the delay value.",
 "K01":"The device-level repeat rate is read, falling back to the global option."}
print("# A: lexical overlap (words>=6 of quote in proposition) on honest probes")
for k,s in honest.items(): print(k, "pass" if words(s) & {w for w in re.findall(r"\w+", s.lower())} else "fail")
print("# B: topic stem (repeat|delay|numlock) on honest probes")
for k,s in honest.items(): print(k, "pass" if topic(s) else "fail")
for f in ["J1-entry.md","J2-entry.md"]:
    rows=[l.split("|") for l in open(f,encoding="utf-8") if re.match(r"\| [KH]\d\d \|",l)]
    print(f, "topic-pass", sum(topic(r[2]) for r in rows), "of", len(rows), "fail:", [r[1].strip() for r in rows if not topic(r[2])])
