import json, random, sys
import fuzz

total = 0
allbad = []
for seed in range(1, 7):
    rng = random.Random(seed)
    cases = [fuzz.gen_case(rng) for _ in range(500)]
    bad = fuzz.run_cases(cases)
    total += len(cases)
    allbad += bad
    print("seed=%d cases=%d disagreements=%d" % (seed, len(cases), len(bad)))

# cartesian rule-line sweep
effects = ["size 1 2", "size 0 0", "size 0042 0500", "size 123456 1", "size 1",
           "size 1 2 3", "float on", "float off", "float ON", "float",
           "center", "size\t1\t2", "float on\t", " size 1 2"]
field1s = ["match:class ^(a)$", "match:class ^(a.*)$", "match:class ^(.*)$",
           "match:classes ^(a)$", "match:class ^(a$", "match:class ",
           "match:class", "match:class ^(a)$ ,x", "match:class  ^(a)$",
           "match:class\t^(a)$"]
tmpl = ["windowrule = %s, %s", "windowrule=%s, %s", "windowrule\t=\t%s, %s",
        "windowrule  =  %s ,%s", "windowrulev2 = %s, %s"]
doc = json.dumps([
    {"class": "a", "mapped": True, "floating": True, "size": [1, 2], "address": "0x1"},
    {"class": "ab", "mapped": True, "floating": False, "size": [42, 500]},
    {"class": "a", "mapped": False, "floating": True, "size": [1, 2]},
    {"class": "A", "mapped": 0, "floating": None, "size": [True, 2]},
    {},
]).encode()
cart = [(doc, [t % (e, f)]) for t in tmpl for e in effects for f in field1s]
bad = fuzz.run_cases(cart)
total += len(cart); allbad += bad
print("cartesian_rules cases=%d disagreements=%d" % (len(cart), len(bad)))

# exhaustive client matrix
rule = "windowrule = size 1 2, match:class ^(a)$"
maps = [("absent", {}), ("false", {"mapped": False}), ("true", {"mapped": True}),
        ("zero", {"mapped": 0}), ("null", {"mapped": None}), ("strfalse", {"mapped": "false"})]
floats = [("absent", {}), ("true", {"floating": True}), ("false", {"floating": False}),
          ("one", {"floating": 1}), ("strtrue", {"floating": "true"})]
sizes = [("none", {"size": None}), ("ok", {"size": [1, 2]}), ("zero", {"size": [0, 0]}),
         ("bool", {"size": [True, 2]}), ("float", {"size": [1.0, 2]}),
         ("neg", {"size": [-1, 2]}), ("short", {"size": [1]}), ("str", {"size": "1x2"}),
         ("absent", {})]
classes = [("a", {"class": "a"}), ("A", {"class": "A"}), ("ctl", {"class": "a\x01"}),
           ("none", {"class": None}), ("num", {"class": 1}), ("empty", {"class": ""}),
           ("absent", {}), ("nl", {"class": "a\n"})]
matrix = []
for mn, m in maps:
    for fn, f in floats:
        for sn, s in sizes:
            for cn, c in classes:
                obj = {}
                obj.update(m); obj.update(f); obj.update(s); obj.update(c)
                if not obj:
                    obj = {"class": "zzz"}
                matrix.append((json.dumps([obj]).encode(), [rule]))
bad = fuzz.run_cases(matrix)
total += len(matrix); allbad += bad
print("cartesian_clients cases=%d disagreements=%d" % (len(matrix), len(bad)))

print("TOTAL cases=%d disagreements=%d" % (total, len(allbad)))
for case, a, b in allbad[:5]:
    print("BAD raw=%r texts=%r\n model=%r\n mine =%r" % (case[0], case[1], a, b))
sys.exit(0 if not allbad else 1)
