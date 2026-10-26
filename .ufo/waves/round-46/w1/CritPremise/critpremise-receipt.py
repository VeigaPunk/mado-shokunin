#!/usr/bin/env python3
"""CritPremise seat receipt generator + verifier (round 46, w1).

Modes:
  gen     --scratch DIR   compute every locator from the cited bytes (grep-style search, never typed)
                          and write receipt.txt next to this script
  verify  [--scratch DIR] re-derive every locator from the same bytes and re-run the three reference
                          invocations (only when --scratch DIR still holds dump.json)

Quote rule honoured here: each quote is <= 25 words, occurs exactly once in its file, and its line
number is the one the search string lands on. Nothing in the lane is written.
"""
import os
import re
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
BASE = "b22ea56bff2faec39ce9ff75d2107eaf4612ecbe"
HERE = os.path.dirname(os.path.abspath(__file__))
RECEIPT = os.path.join(HERE, "receipt.txt")
REF = os.path.join(LANE, ".ufo/waves/round-46/l1-draft/mado-devices.py")

# (label, kind, path, search) ; kind 'git' = lane blob at BASE, 'host' = file on disk
SOURCES = [
    # --- what the lane already held on this plane -------------------------
    ("held-join", "git", "corpus/knowledge/hyprctl-verification-layer.md",
     "agreement (keymap-level, stronger than the string getoption)"),
    ("held-dump-parse", "git", "corpus/knowledge/config-health-report-r3.md",
     'hyprctl -j devices > "$D/devices.json"'),
    ("held-virtual-node", "git", "corpus/knowledge/config-health-report-r3.md",
     "power-button ×2, `hl-virtual-keyboard-fcitx5`), all keymap"),
    ("held-hotplug", "git", "SKILL.md", "device lists are hotplug-sensitive"),
    # --- the documented boundary that authorises this route ---------------
    ("boundary-route", "git", "corpus/knowledge/input-debugging-boundaries-r15.md",
     "input settings and `devices` metadata"),
    ("boundary-verdict", "git", "corpus/knowledge/input-debugging-boundaries-r15.md",
     "Policy/inventory evidence, not input delivery"),
    ("skill-getoption-limit", "git", "SKILL.md",
     "`getoption` is a config read, not applied"),
    # --- why getoption alone cannot answer the question -------------------
    ("getoption-flat-lookup", "open", ".ufo/waves/round-46/fetch/Hyprland-HyprCtl.cpp",
     "const auto VAR = Config::mgr()->getConfigValue(curitem);"),
    ("device-store-separate", "open", ".ufo/waves/round-46/fetch/Hyprland-InputManager.cpp",
     'getDeviceString(devname, "kb_layout", "input:kb_layout")'),
    # --- the parser that already existed at base -------------------------
    ("options-special-categories", "git", "tools/mado-options.py",
     '"device", "monitorv2", "windowrule", "layerrule", "plugin"'),
    ("options-device-fixture", "git", "tools/mado-options.py", "name = some-mouse"),
    # --- omarchy's own use of the plane (host, read-only) -----------------
    ("omarchy-reader", "host", "/home/vgpnk/.local/share/omarchy/bin/omarchy-hw-touchpad",
     "hyprctl devices -j | jq -r"),
    ("omarchy-writer", "host", "/home/vgpnk/.local/share/omarchy/bin/omarchy-toggle-touchpad",
     'enabled = false\\n}\\n\' "$device"'),
    # --- the claim's own live receipt --------------------------------------
    ("live-blocks-zero", "host", ".ufo/waves/round-46/receipts/live-devices-host-l1.txt",
     "blocks=0 stale=0 unsupported=0"),
    # --- provenance: the duplicate-URL rule and the declared count ---------
    ("w04-rule", "host", "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh",
     "W04 same URL across scopes"),
    ("declared-repeats", "host", ".ufo/waves/round-46/registration.md",
     "The two cross-scope URL repeats"),
]

URLS = [
    "config/values/ConfigValues.cpp",
    "helpers/MiscFunctions.cpp",
    "hyprlang/v0.6.8/src/config.cpp",
    "config/legacy/ConfigManager.cpp",
    "debug/HyprCtl.cpp",
    "managers/input/InputManager.cpp",
    "devices/IKeyboard.cpp",
    "devices/VirtualKeyboard.cpp",
    "protocols/VirtualKeyboard.cpp",
    "Configuring/Keywords.md",
]


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def blob(kind, path):
    if kind == "git":
        out = subprocess.run(["git", "-C", LANE, "show", "%s:%s" % (BASE, path)],
                             capture_output=True, check=True).stdout
        return out.decode("utf-8", "replace"), path
    p = path if os.path.isabs(path) else os.path.join(LANE, path)
    with open(p, encoding="utf-8", errors="replace") as fh:
        return fh.read(), path


def locate(kind, path, search):
    text, shown = blob(kind, path)
    lines = text.split("\n")
    hits = [i + 1 for i, ln in enumerate(lines) if search in ln]
    if len(hits) != 1:
        raise SystemExit("locator %r at %s: %d hits, want 1" % (search, shown, len(hits)))
    line = hits[0]
    # the quote is the search string itself, trimmed, <= 25 words, unique in the file
    words = norm(search).split(" ")
    if not 3 <= len(words) <= 25:
        raise SystemExit("quote %r has %d words" % (search, len(words)))
    if text.count(search) != 1:
        raise SystemExit("quote %r not unique in %s" % (search, shown))
    return line, norm(search), len(words)


def url_counts():
    text, _ = blob("git", "corpus/SOURCES.md")
    rows = [l for l in text.split("\n") if re.match(r"^\| S\d{3,} \|", l)]
    urls = []
    for r in rows:
        m = re.search(r"https?://\S+", r)
        if m:
            urls.append(m.group(0).rstrip("/"))
    out = []
    for u in URLS:
        out.append((u, sum(1 for x in urls if x.endswith(u))))
    return out


def getoption_probe():
    """The one read verb this seat uses: can getoption reach the per-device store?"""
    out = []
    for form in ("device[foo]:kb_layout", "device:kb_layout"):
        r = subprocess.run(["hyprctl", "getoption", form, "-j"], capture_output=True)
        reply = (r.stdout + r.stderr).decode("utf-8", "replace").strip()
        out.append((form, reply))
    return out


def ref_runs(scratch):
    dump = os.path.join(scratch, "dump.json")
    if not os.path.isfile(dump):
        return None
    kname = subprocess.run(
        ["python3", "-c", "import json,sys;print(json.load(open(sys.argv[1]))['keyboards'][0]['name'])", dump],
        capture_output=True, check=True).stdout.decode().strip()
    hdr = 'input {\n  kb_layout = br\n  kb_options = compose:caps\n}\n'
    cases = {
        "A-block-sets-layout": hdr + 'device {\n  name = %s\n  kb_layout = de\n}\n' % kname,
        "B-stale-block": hdr + 'device {\n  name = fake-kbd-xyz\n  kb_layout = de\n}\n',
        "C-omarchy-enabled-only": hdr + 'device {\n  name = %s\n  enabled = false\n}\n' % kname,
    }
    out = []
    for label, cfg in cases.items():
        p = os.path.join(scratch, "crit-%s.conf" % label[0])
        with open(p, "w") as fh:
            fh.write(cfg)
        r = subprocess.run(["python3", "-I", REF, "--devices", dump, "--config", p],
                           capture_output=True)
        summary = [l for l in (r.stdout + r.stderr).decode("utf-8", "replace").split("\n")
                   if l.startswith("MADO_DEVICES:")]
        out.append((label, summary[0] if summary else "MISSING", r.returncode))
    return out


def gen(scratch):
    lines = ["# CritPremise round-46 receipt (computed %s)" % "locators re-derived by critpremise-receipt.py",
             "# lane=%s base=%s" % (LANE, BASE),
             "# Q <kind> <path>:<line> words=<n> \"<quote>\""]
    for label, kind, path, search in SOURCES:
        line, quote, nwords = locate(kind, path, search)
        lines.append('Q %s %s %s:%d words=%d "%s"' % (label, kind, path, line, nwords, quote))
    lines.append("# C base registry row count per URL (git show %s:corpus/SOURCES.md)" % BASE[:8])
    for u, n in url_counts():
        lines.append("C url-rows %s %d" % (u, n))
    lines.append("# P the per-device store is not reachable through getoption (read verb only)")
    for form, reply in getoption_probe():
        lines.append("P getoption %s -> %s" % (form, reply))
    if scratch:
        runs = ref_runs(scratch)
        if runs:
            lines.append("# R reference runs on the live dump + synthetic configs (names never retained)")
            for label, summary, rc in runs:
                lines.append("R %s exit=%d %s" % (label, rc, summary))
    with open(RECEIPT, "w") as fh:
        fh.write("\n".join(lines) + "\n")
    print("wrote %s (%d lines)" % (RECEIPT, len(lines)))


def verify(scratch):
    bad = 0
    with open(RECEIPT) as fh:
        raw = fh.read().split("\n")
    seen = set()
    for ln in raw:
        if not ln.startswith("Q "):
            continue
        label, kind, loc, words, quote = ln[2:].split(" ", 4)
        if label in seen:
            bad += 1
            print("FAIL duplicate label %s" % label)
        seen.add(label)
        path, line = loc.rsplit(":", 1)
        line = int(line)
        exp_w = int(words.split("=")[1])
        want = quote.strip().strip('"')
        got_line, got_quote, got_w = locate(kind, path, want)
        ok = (got_line == line and got_quote == norm(want) and got_w == exp_w)
        print("%s %-28s %s:%d words=%d" % ("OK  " if ok else "FAIL", label, path, got_line, got_w))
        bad += 0 if ok else 1
    counts = {u: n for u, n in url_counts()}
    new_dup = [u for u, n in counts.items() if n == 1]
    print("C URLs with exactly one base row (a new row there opens a NEW duplicate group): %d %s"
          % (len(new_dup), sorted(new_dup)))
    probe = ["P getoption %s -> %s" % (f, r) for f, r in getoption_probe()]
    have = [l for l in raw if l.startswith("P ")]
    ok = probe == have
    print("%s getoption per-device probe (%d lines)" % ("OK  " if ok else "FAIL", len(probe)))
    bad += 0 if ok else 1
    if scratch:
        have = [l for l in raw if l.startswith("R ")]
        runs = ref_runs(scratch)
        if runs and have:
            for (label, summary, rc), line in zip(runs, have):
                want = "R %s exit=%d %s" % (label, rc, summary)
                ok = want == line
                print("%s rerun %s" % ("OK  " if ok else "FAIL", label))
                bad += 0 if ok else 1
    print("VERDICT: %s (%d failures, %d quotes)" % ("PASS" if bad == 0 else "FAIL", bad, len(seen)))
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "gen"
    sc = sys.argv[sys.argv.index("--scratch") + 1] if "--scratch" in sys.argv else None
    if mode == "gen":
        gen(sc)
    elif mode == "verify":
        sys.exit(verify(sc))
    else:
        raise SystemExit("mode: gen|verify")
