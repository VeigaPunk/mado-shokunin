#!/usr/bin/env python3
"""R79ExecC1Tool fuzz harness: --rules reader boundary probes + box arithmetic.

Runs the pinned tool copy (sha256 c9aa1391…) as a subprocess per probe and
classifies every observed exit against the docstring exit map
(0 CLEAN · 1 DIFFER · 2 SETUP/ERROR · 3 NOT_FORMED) and against the S466/S465
ground truth where the pins decide.
"""
import json
import os
import re
import subprocess
import sys

SCRATCH = "/fast/scratch/hyaku/mado-r79/R79ExecC1Tool"
FX = os.path.join(SCRATCH, "fx")
TOOL = ("/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-79/"
        "w1/R79ExecC1Tool/mado-barfoot.py")
MAX_BYTES = 1048576
W, H = 3440, 1440

os.makedirs(FX, exist_ok=True)


def write(path, data):
    if isinstance(data, str):
        data = data.encode()
    with open(path, "wb") as fh:
        fh.write(data)


def monitors_file(reserved):
    return json.dumps([{"name": "M1", "id": 0, "width": W, "height": H,
                        "scale": 1.0, "transform": 0, "reserved": reserved,
                        "availableModes": ["3440x1440"]}])


def layers_file(box):
    return json.dumps({"M1": {"levels": {"2": [
        {"namespace": "waybar", "layer": "top", "x": box["x"], "y": box["y"],
         "w": box["w"], "h": box["h"]}]}}})


def config_file(**over):
    cfg = {"position": "top", "layer": "top", "height": 34, "name": "waybar",
           "exclusive": True}
    cfg.update(over)
    return json.dumps(cfg)


def run(config, layers, monitors, rules=None, monitor="M1", timeout=15):
    cmd = [sys.executable, "-I", TOOL, "--config", config,
           "--layers", layers, "--monitors", monitors]
    if rules is not None:
        cmd += ["--rules", rules]
    if monitor is not None:
        cmd += ["--monitor", monitor]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout,
                       cwd=SCRATCH)
    rows = {}
    for line in p.stdout.splitlines():
        if line.startswith("MADO_BARFOOT_") and ": " in line:
            kind, text = line[len("MADO_BARFOOT_"):].split(": ", 1)
            rows[kind] = text
    err = ""
    for line in p.stdout.splitlines():
        if line.startswith("MADO_BARFOOT: ERROR"):
            err = line
    return {"rc": p.returncode, "rows": rows, "err": err, "cmd": cmd,
            "stdout": p.stdout}


# ---- reference model: the tool's own documented arithmetic -------------------

def ref_usable(st):
    return {"x": st["left"], "y": st["top"],
            "w": W - st["left"] - st["right"],
            "h": H - st["top"] - st["bottom"]}


def ref_declared_box(bar, usable):
    m, pos = bar["margins"], bar["position"]
    uw, uh = usable["w"], usable["h"]
    if pos in ("top", "bottom"):
        if bar["width"] > 1:
            w = bar["width"]
            x = (uw - w + 1) // 2
        else:
            w = uw - m["left"] - m["right"]
            x = m["left"]
        if bar["height"] > 0:
            h = bar["height"]
            y = m["top"] if pos == "top" else uh - h - m["bottom"]
        else:
            h = uh - m["top"] - m["bottom"]
            y = m["top"]
    else:
        if bar["height"] > 1:
            h = bar["height"]
            y = (uh - h + 1) // 2
        else:
            h = uh - m["top"] - m["bottom"]
            y = m["top"]
        if bar["width"] > 0:
            w = bar["width"]
            x = m["left"] if pos == "left" else uw - w - m["right"]
        else:
            w = uw - m["left"] - m["right"]
            x = m["left"]
    box = {"x": x + usable["x"], "y": y + usable["y"], "w": w, "h": h}
    contained = (box["x"] >= usable["x"] and box["y"] >= usable["y"]
                 and box["x"] + box["w"] <= usable["x"] + usable["w"]
                 and box["y"] + box["h"] <= usable["y"] + usable["h"])
    return box, contained


def ref_expected(bar, box, usable, st, contained):
    pos = bar["position"]
    opp = {"top": "bottom", "bottom": "top", "left": "right", "right": "left"}[pos]
    if pos == "top":
        extent = (box["y"] - usable["y"]) + box["h"]
    elif pos == "bottom":
        extent = (usable["y"] + usable["h"]) - box["y"]
    elif pos == "left":
        extent = (box["x"] - usable["x"]) + box["w"]
    else:
        extent = (usable["x"] + usable["w"]) - box["x"]
    return st[pos] + ((extent + bar["margins"][opp]) if contained else 0)


def margins_of(cfg):
    out = {"top": 0, "right": 0, "bottom": 0, "left": 0}
    for k in out:
        v = cfg.get("margin-" + k)
        if isinstance(v, int) and not isinstance(v, bool):
            out[k] = v
    v = cfg.get("margin")
    if isinstance(v, int) and not isinstance(v, bool):
        out = {k: v for k in out}
    return out


results = []


def record(pid, obs, expect_class, ok, note, fixture=None):
    results.append({"id": pid, "rc": obs["rc"], "class": expect_class,
                    "ok": ok, "note": note, "err": obs.get("err", ""),
                    "static": obs.get("rows", {}).get("STATIC", ""),
                    "result": obs.get("rows", {}).get("RESULT", ""),
                    "decl": obs.get("rows", {}).get("DECL", ""),
                    "cmd": " ".join(obs.get("cmd", [])), "fixture": fixture})


# ---- part 1: reader probes ---------------------------------------------------

def probe_rules(pid, rules_bytes, expect_class, note, expect_static=None,
                cfg=None):
    rp = os.path.join(FX, "rules-%s" % pid)
    write(rp, rules_bytes)
    cfgp = os.path.join(FX, "config-%s.jsonc" % pid)
    layp = os.path.join(FX, "layers-%s.json" % pid)
    monp = os.path.join(FX, "monitors-%s.json" % pid)
    st = expect_static or {"top": 0, "right": 0, "bottom": 0, "left": 0}
    bar = {"margins": {"top": 0, "right": 0, "bottom": 0, "left": 0},
           "position": "top", "height": 34, "width": 0}
    usable = ref_usable(st)
    if usable["w"] <= 0 or usable["h"] <= 0:
        box = None
    else:
        box, _ = ref_declared_box(bar, usable)
    write(cfgp, cfg or config_file())
    write(layp, layers_file(box) if box else json.dumps({"M1": {"levels": {}}}))
    write(monp, monitors_file([st["left"], st["top"], st["right"], st["bottom"]]
                              if box else [0, 0, 0, 0]))
    obs = run(cfgp, layp, monp, rules=rp)
    with open(rp, "rb") as fh:
        fixture = fh.read()
    ok = (obs["rc"] in (0, 1)) if expect_class == "accept" else \
         (obs["rc"] == 2 if expect_class == "setup-refuse" else obs["rc"] == 3)
    if expect_static is not None and obs["rc"] in (0, 1):
        want = ("monitor=M1 top=%d right=%d bottom=%d left=%d source=rules"
                % (st["top"], st["right"], st["bottom"], st["left"]))
        got = obs["rows"].get("STATIC", "")
        if got != want:
            ok = False
            note += " STATIC-MISMATCH want[%s] got[%s]" % (want, got)
    record(pid, obs, expect_class, ok, note, fixture)


def st_(t, r, b, l):
    return {"top": t, "right": r, "bottom": b, "left": l}


R = probe_rules

R("R01-comment-only", b"# monitor = M1, addreserved, 99, 0, 0, 0\n",
  "accept", "comment-only file: rule must not apply", st_(0, 0, 0, 0))
R("R02-inline-comment", b"monitor = M1, addreserved, 26, 0, 0, 0 # trailing\n",
  "accept", "trailing # comment stripped, reserve applies", st_(26, 0, 0, 0))
R("R03-whitespace", b"\t  monitor   =   M1 , addreserved , 12 , 34 , 0 , 0  \n"
                    b"  \n\t\n", "accept", "leading tabs/spaces, spaced fields",
  st_(12, 0, 34, 0))
R("R04-nospace", b"monitor=x,addreserved,1,2,3,4\nmonitor=M1,addreserved,7,0,0,0\n",
  "accept", "no-space form; selector x skipped, M1 applies", st_(7, 0, 0, 0))
R("R05a-huge-19digit",
  b"monitor = M1, addreserved, 99999999999999999999, 0, 0, 0\n",
  "model-refuse", "20-digit field is not a plain integer (INT_FIELD_RE max 6 digits)")
R("R05b-huge-7digit", b"monitor = M1, addreserved, 1234567, 0, 0, 0\n",
  "model-refuse", "7-digit field over the 6-digit plain-integer cap")
R("R05c-huge-6digit", b"monitor = M1, addreserved, 999999, 0, 0, 0\n",
  "model-refuse", "6-digit 999999 parses, then usable box h=1440-999999<=0 -> "
                  "refused downstream (stage=model, different message)")
R("R06-negative", b"monitor = M1, addreserved, -10, 0, 0, 0\n",
  "accept", "NEGATIVE top field accepted; S466 ctor clamps negatives to 0 -> "
            "tool diverges (usable box expanded, band reduced)", st_(-10, 0, 0, 0))
R("R07-six-fields", b"monitor = M1, addreserved, 1, 2, 3, 4, 5\n",
  "accept", "five numbers: fifth silently ignored (handler reads ARGS[2..5])",
  st_(1, 4, 2, 3))
R("R08-five-fields", b"monitor = M1, addreserved, 1, 2, 3\n",
  "model-refuse", "three numbers: refused as needing four plain integers")
R("R09-unknown-key", b"monitor = M1, frobnicate, 1, 2, 3, 4\n",
  "accept", "unknown positional key: line dropped, slot untouched", st_(0, 0, 0, 0))
R("R10a-unknown-after", b"monitor = M1, addreserved, 26, 0, 0, 0\n"
                        b"monitor = M1, frobnicate, 1, 2, 3, 4\n",
  "accept", "unknown-key line after addreserved: previous reserve survives",
  st_(26, 0, 0, 0))
R("R10b-unknown-2field", b"monitor = M1, addreserved, 26, 0, 0, 0\n"
                         b"monitor = M1, custom\n",
  "accept", "2-field unknown kind: treated as a positional rule and ZEROES the "
            "slot (no mode validation) - asymmetry vs the 6-field unknown kind",
  st_(0, 0, 0, 0))
R("R11a-disable", b"monitor = M1, addreserved, 26, 0, 0, 0\nmonitor = M1, disable\n",
  "accept", "disable replaces the slot with zero", st_(0, 0, 0, 0))
R("R11b-disabled", b"monitor = M1, addreserved, 26, 0, 0, 0\nmonitor = M1, disabled\n",
  "accept", "`disabled` also treated as disable (extra keyword accepted)",
  st_(0, 0, 0, 0))
R("R12a-transform-keep", b"monitor = M1, addreserved, 26, 0, 0, 0\n"
                         b"monitor = M1, transform, 1\n",
  "accept", "transform copies the slot and keeps the reserve", st_(26, 0, 0, 0))
R("R12b-transform-first", b"monitor = M1, transform, 1\n"
                          b"monitor = M1, addreserved, 26, 0, 0, 0\n",
  "accept", "transform before addreserved: zero-copy slot then reserve set",
  st_(26, 0, 0, 0))
R("R13a-positional-after", b"monitor = M1, addreserved, 26, 0, 0, 0\n"
                           b"monitor = M1, 3440x1440@100, 0x0, 1\n",
  "accept", "positional rule after addreserved replaces the slot (zero)",
  st_(0, 0, 0, 0))
R("R13b-positional-before", b"monitor = M1, 3440x1440@100, 0x0, 1\n"
                            b"monitor = M1, addreserved, 26, 0, 0, 0\n",
  "accept", "positional rule before addreserved: reserve applies", st_(26, 0, 0, 0))
R("R14a-two-selectors-space", b"monitor = M1 M2, addreserved, 26, 0, 0, 0\n",
  "accept", "two selectors in one line: whole selector string mismatched, skipped",
  st_(0, 0, 0, 0))
R("R14b-two-selectors-isolated",
  b"monitor = M2, addreserved, 7, 0, 0, 0\nmonitor = M1, addreserved, 26, 0, 0, 0\n",
  "accept", "other selector never touches M1's slot", st_(26, 0, 0, 0))
R("R14c-two-selectors-rev",
  b"monitor = M1, addreserved, 26, 0, 0, 0\nmonitor = M2, addreserved, 7, 0, 0, 0\n",
  "accept", "reverse order: isolation holds (per-selector last-wins)", st_(26, 0, 0, 0))
R("R15a-var-value", b"monitor = M1, addreserved, $x, 0, 0, 0\n",
  "model-refuse", "$ in the matched selector's value: literal-subset refusal")
R("R15b-var-selector", b"monitor = $disp, 3440x1440, 0x0, 1\n",
  "model-refuse", "$ anywhere in a monitor= value refuses the join BEFORE the "
                  "selector comparison (selftest case 'a variable rule')")
R("R15c-var-def-only", b"$disp = M1\nmonitor = M1, addreserved, 26, 0, 0, 0\n",
  "accept", "variable DEFINITION line ignored (key $disp != monitor/source)",
  st_(26, 0, 0, 0))
R("R16a-hashhash-line", b"## monitor = M1, addreserved, 26, 0, 0, 0\n",
  "accept", "## line: comment-stripped to empty, skipped", st_(0, 0, 0, 0))
R("R16b-hashhash-inline", b"monitor = M1, addreserved, 1, 2, 3, 4 ## note\n",
  "accept", "inline ## never reaches the '\"##\" in value' check (comment strip "
            "runs first) - that refusal branch is dead code", st_(1, 4, 2, 3))
R("R16c-hashhash-midrule", b"monitor = M1##alias, addreserved, 1, 2, 3, 4\n",
  "accept", "# truncates the line mid-rule: value becomes 'M1', parsed as a bare "
            "positional rule -> slot zeroed", st_(0, 0, 0, 0))
R("R17a-source", b"source = ~/.config/hypr/other.conf\n",
  "model-refuse", "source line refuses the join (sourced file not followed)")
R("R17b-source-nospace", b"source=/x.conf\n", "model-refuse",
  "source without spaces still refused")
R("R17c-source-commented", b"# source = /x.conf\n",
  "accept", "commented source line is not a source line", st_(0, 0, 0, 0))
R("R17d-source-upper", b"SOURCE = /x.conf\n",
  "accept", "uppercase key not matched (Hyprland keys are case-sensitive)",
  st_(0, 0, 0, 0))
R("R18-nonutf8", b"monitor = M1, addreserved, 1, 2, 3, 4\n\xff\xfe\n",
  "setup-refuse", "non-UTF-8 byte: Setup refusal (rules file must be UTF-8)")
R("R19a-plus-one", b"monitor = M1, addreserved, +1, 0, 0, 0\n",
  "model-refuse", "+1 is not a plain integer under INT_FIELD_RE")
R("R19b-float", b"monitor = M1, addreserved, 1.0, 0, 0, 0\n",
  "model-refuse", "1.0 refused")
R("R19c-hex", b"monitor = M1, addreserved, 0x10, 0, 0, 0\n",
  "model-refuse", "0x10 refused")
R("R19d-tab-numbers", b"monitor = M1,\taddreserved,\t26,\t0,\t0,\t0\n",
  "accept", "tab-separated fields: comma-split then strip accepts", st_(26, 0, 0, 0))
R("R19e-crlf", b"monitor = M1, addreserved, 26, 0, 0, 0\r\nmonitor = M2, disable\r\n",
  "accept", "CRLF line endings tolerated via splitlines", st_(26, 0, 0, 0))
R("R19f-bom", b"\xef\xbb\xbfmonitor = M1, addreserved, 26, 0, 0, 0\n",
  "accept", "UTF-8 BOM: first key is U+FEFFmonitor -> line silently skipped "
            "(Hyprland also ignores the unknown key)", st_(0, 0, 0, 0))
R("R20a-trailing-comma", b"monitor = M1, addreserved, 1, 2, 3, 4,\n",
  "accept", "trailing comma yields an empty field beyond index 5: fields[2:6] "
            "intact", st_(1, 4, 2, 3))
R("R20b-minus-zero", b"monitor = M1, addreserved, -0, 0, 0, 0\n",
  "accept", "-0 fullmatches INT_FIELD_RE and int()s to 0", st_(0, 0, 0, 0))

# ---- special-path probes -----------------------------------------------------

cfgp = os.path.join(FX, "config-spec.jsonc")
layp = os.path.join(FX, "layers-spec.json")
monp = os.path.join(FX, "monitors-spec.json")
write(cfgp, config_file())
bar0 = {"margins": {"top": 0, "right": 0, "bottom": 0, "left": 0},
        "position": "top", "height": 34, "width": 0}
box0, _ = ref_declared_box(bar0, ref_usable(st_(0, 0, 0, 0)))
write(layp, layers_file(box0))
write(monp, monitors_file([0, 0, 0, 0]))

dirp = os.path.join(FX, "adir")
os.makedirs(dirp, exist_ok=True)
obs = run(cfgp, layp, monp, rules=dirp)
record("R21-directory", obs, "setup-refuse", "rules path is a directory", None,
       b"<directory>")

fifop = os.path.join(FX, "afifo")
if not os.path.exists(fifop):
    os.mkfifo(fifop)
obs = run(cfgp, layp, monp, rules=fifop, timeout=10)
record("R22-fifo", obs, "setup-refuse", "rules path is a FIFO: refused by lstat "
       "without opening (no hang)", None, b"<fifo>")

big = os.path.join(FX, "big-rules")
write(big, b"# pad\n" * ((MAX_BYTES * 2) // 7))
obs = run(cfgp, layp, monp, rules=big)
record("R23-2mib", obs, "setup-refuse", "2 MiB rules file exceeds "
       "MAX_BYTES=1048576", None,
       b"<%d bytes of comment lines>" % os.path.getsize(big))

maxp = os.path.join(FX, "max-rules")
maxbody = (b"monitor = M1, addreserved, 26, 0, 0, 0\n"
           + b"#\n" * 524267 + b"#x\n")
assert len(maxbody) == MAX_BYTES, len(maxbody)
write(maxp, maxbody)
st26 = st_(26, 0, 0, 0)
box26, _ = ref_declared_box(bar0, ref_usable(st26))
write(layp, layers_file(box26))
write(monp, monitors_file([0, 26, 0, 0]))
obs = run(cfgp, layp, monp, rules=maxp)
record("R24-exactly-max", obs, "accept",
       "exactly %d bytes: accepted (<= MAX_BYTES), reserve parsed" % MAX_BYTES,
       st26)

maxp1 = os.path.join(FX, "max1-rules")
max1 = b"# pad\n" * (MAX_BYTES // 6 + 1)
write(maxp1, max1)
obs = run(cfgp, layp, monp, rules=maxp1)
record("R25-max-plus-one", obs, "setup-refuse", "MAX_BYTES+1 file refused", None,
       b"<%d bytes>" % len(max1))

obs = run(cfgp, layp, monp, rules="-")
record("R26-stdin-dash", obs, "setup-refuse", "--rules - is not accepted "
       "(stdin only for --layers/--monitors)", None, b"<literal '-' argument>")

# ---- part 3: box arithmetic matrix -------------------------------------------

def arith(pid, position, st, cfg_over=None, note=""):
    cfg = {"position": position, "layer": "top", "name": "waybar",
           "exclusive": True}
    if position in ("top", "bottom"):
        cfg["height"] = 34
    else:
        cfg["width"] = 34
    if cfg_over:
        cfg.update(cfg_over)
    bar = {"margins": margins_of(cfg), "position": position,
           "height": cfg.get("height", 0) if isinstance(cfg.get("height", 0), int)
           else 0,
           "width": cfg.get("width", 0) if isinstance(cfg.get("width", 0), int)
           else 0}
    usable = ref_usable(st)
    assert usable["w"] > 0 and usable["h"] > 0, pid
    box, contained = ref_declared_box(bar, usable)
    exp = ref_expected(bar, box, usable, st, contained)
    rules_line = "monitor = M1, addreserved, %d, %d, %d, %d\n" % (
        st["top"], st["bottom"], st["left"], st["right"])
    rp = os.path.join(FX, "rules-%s" % pid)
    write(rp, rules_line)
    cfgp = os.path.join(FX, "config-%s.jsonc" % pid)
    layp = os.path.join(FX, "layers-%s.json" % pid)
    monp = os.path.join(FX, "monitors-%s.json" % pid)
    write(cfgp, json.dumps(cfg))
    write(layp, layers_file(box))
    write(monp, monitors_file([st["left"], st["top"], st["right"], st["bottom"]]))
    obs = run(cfgp, layp, monp, rules=rp)
    res = obs["rows"].get("RESULT", "")
    decl = obs["rows"].get("DECL", "")
    m = re.search(r"expected=(-?\d+)", res)
    md = re.search(r"box=(-?\d+),(-?\d+),(-?\d+),(-?\d+)", decl)
    ok, detail = False, ""
    if m and md:
        got_exp = int(m.group(1))
        got_box = tuple(int(md.group(i)) for i in range(1, 5))
        want_box = (box["x"], box["y"], box["w"], box["h"])
        ok = got_exp == exp and got_box == want_box
        detail = " | want box=%s expected=%d got box=%s expected=%d [%s]" % (
            want_box, exp, got_box, got_exp,
            "contained" if contained else "UNCONTAINED")
    full_note = (note or "pos=%s static=%r" % (position, st)) + detail
    full_note += " | rules=%r" % rules_line
    record(pid, obs, "accept-cmp", ok, full_note, rules_line.encode())


RESERVES = {"top26": st_(26, 0, 0, 0), "bottom10": st_(0, 0, 10, 0),
            "left40": st_(0, 0, 0, 40), "right50": st_(0, 50, 0, 0)}
for pos in ("top", "bottom", "left", "right"):
    for rname, st in RESERVES.items():
        arith("A-%s-%s" % (pos, rname), pos, st,
              note="pos=%s static=%s" % (pos, rname))

arith("A-centre-w-lr", "top", st_(0, 50, 0, 40), {"width": 1000},
      note="top bar width=1000, static left40 right50: centring inside the "
           "static-reduced usable box")
arith("A-centre-w-l", "top", st_(0, 0, 0, 40), {"width": 1000},
      note="top bar width=1000, static left40")
arith("A-centre-w-r", "top", st_(0, 50, 0, 0), {"width": 1000},
      note="top bar width=1000, static right50")
arith("A-centre-h-t", "left", st_(26, 0, 0, 0), {"height": 300},
      note="left bar height=300 (length axis), static top26: centred vertically "
           "in the usable box")
arith("A-centre-h-tb", "right", st_(26, 0, 10, 0), {"height": 300},
      note="right bar height=300, static top26 bottom10")
arith("A-uncontained", "top", st_(26, 0, 0, 0), {"width": 5000},
      note="top bar width=5000 overflows usable.w=3440: contribution must be 0, "
           "expected=static only")
arith("A-margin-bottom", "top", st_(26, 0, 0, 0), {"margin-bottom": 6},
      note="top bar h34 margin-bottom6, static top26: expected=26+34+6")
arith("A-margin-lr", "top", st_(0, 0, 0, 0),
      {"margin-left": 8, "margin-right": 12},
      note="top bar margins l8 r12: box w=usable.w-20, x=usable.x+8")
arith("A-exclusive-false", "top", st_(26, 0, 0, 0), {"exclusive": False},
      note="exclusive=false: NOT_APPLIED, expectation still printed")
arith("A-negative-static", "top", st_(-10, 0, 0, 0), {},
      note="static top=-10: tool expands the usable box; S466 ctor would clamp "
           "to 0 -> reference here is the tool formula, Hyprland ground differs")

# ---- report ------------------------------------------------------------------

lines = []
npass = sum(1 for r in results if r["ok"])
nfail = len(results) - npass
lines.append("PASS %d / %d  (fail = observed class diverges from the docstring "
             "exit map or the reference arithmetic)\n" % (npass, len(results)))
for r in results:
    mark = "OK  " if r["ok"] else "DIFF"
    lines.append("%s %-24s rc=%-2s want=%s" % (mark, r["id"], r["rc"], r["class"]))
    if r["static"]:
        lines.append("     STATIC %s" % r["static"])
    if r["result"]:
        lines.append("     RESULT %s" % r["result"])
    if r["err"]:
        lines.append("     %s" % r["err"])
    lines.append("     note: %s" % r["note"])
    if r["fixture"] is not None:
        lines.append("     fixture: %r" % r["fixture"][:120])
    if r["cmd"]:
        lines.append("     cmd: %s" % r["cmd"])
    lines.append("")

out = os.path.join(SCRATCH, "out.txt")
with open(out, "w") as fh:
    fh.write("\n".join(lines))
print("\n".join(lines))
