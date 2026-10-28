#!/usr/bin/env python3
# R55RevC3 independent check of frozen-tables.json c3.q against the round-52 pin.
# Also: lexical P23 leg (registration §C3 `p23`) applied to three junk propositions.
import hashlib, json, sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
T = json.load(open(f"{LANE}/.ufo/waves/round-55/frozen-tables.json", encoding="utf-8"))
c3 = T["c3"]
raw = open(f"{LANE}/{c3['pin']}", "rb").read()
print("pin_path", c3["pin"])
print("pin_sha256", hashlib.sha256(raw).hexdigest(), "frozen", c3["pin_sha256"],
      "MATCH" if hashlib.sha256(raw).hexdigest() == c3["pin_sha256"] else "MISMATCH")
print("pin_has_CR", b"\r" in raw, "pin_ends_nl", raw.endswith(b"\n"), "pin_bytes", len(raw))
lines = raw.decode("utf-8").split("\n")
print("pin_lines_split", len(lines), "(index 1554 =", repr(lines[1553]) + ")")

ids = [q["id"] for q in c3["q"]]
print("q_count", len(c3["q"]), "ids_unique", len(set(ids)) == len(ids))
bad = 0
for q in c3["q"]:
    line = lines[q["line"] - 1]
    strip_ok = line.strip() == q["quote"]
    exact_sub = q["quote"] in line
    lead = len(line) - len(line.lstrip())
    bad += not strip_ok
    print(f"{q['id']} L{q['line']:<5} stripped_eq={strip_ok} substring={exact_sub} indent={lead} | {line.strip()[:70]}")
print("Q_RESULT", "ALL_OK" if bad == 0 else f"BAD={bad}")

# Lexical P23 leg (registration §C3 `p23`): cell lacks any required token, or Supersedes != P19.
TOKENS = ["m_passPressed", "== 1", "== 0", "PRESSED", "RELEASED"]
ALT = ["otherwise", "any other", "else"]

def p23_leg(prop, supersedes="P19"):
    row = f"| P23 | {supersedes} | {prop} | S371 | Hyprland-ConfigActions.cpp:1554-1576 | … |"
    cells = [c.strip() for c in row.strip().strip("|").split("|")]
    p, s = cells[2], cells[1]
    missing = [t for t in TOKENS if t not in p]
    if not any(a in p for a in ALT):
        missing.append("otherwise|any other|else")
    if s != "P19":
        missing.append(f"supersedes={s!r}")
    return ("ok" if not missing else "bad", missing)

junk = {
    "J1 token-salad": "m_passPressed == 1 == 0 PRESSED RELEASED otherwise",
    "J2 false-claim-with-tokens": "Actions::pass sends nothing in its else arm; m_passPressed == 1 and m_passPressed == 0 are the only arms that send PRESSED or RELEASED; any other value is dead code",
    "J3 unrelated": "Actions::pass is a function about window focus and clipboard handling",
}
for name, prop in junk.items():
    v, miss = p23_leg(prop)
    print(f"LEG_P23 {name}: {v} missing={miss or 'none'}")
