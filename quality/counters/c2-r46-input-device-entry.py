#!/usr/bin/env python3
"""PRED-C2-r46 - the input-device entry is admitted (C2, coverage, sourced).

Frozen at the round-46 registration (.ufo/waves/round-46/registration.md). The code is the round-45 v2 entry counter
(quality/counters/c2-r45-monitor-entry-v2.py: clauses a-j with the T1-T5 tightenings) re-cut for this entry: new
constants, pins, census (clause h), surfaces (clause j) and verdict tokens (clause i); every other clause is unchanged.

Scores one committed revision REV (revision-addressed git reads, ambient GIT_* removed; nothing in the lane is
written). ENTRY = corpus/knowledge/hyprland-input-devices-r46.md, LESSON = corpus/lessons/round-46.md,
FETCH = .ufo/waves/round-46/fetch/, BASE = b22ea56bff2faec39ce9ff75d2107eaf4612ecbe, DATE = 2026-10-26. PINS
(file name -> sha256 and URL, tables below, part of the predicate): eight Hyprland files at efb50993 (InputManager.cpp,
legacy ConfigManager.cpp, ConfigValues.cpp, IKeyboard.cpp, HyprCtl.cpp, MiscFunctions.cpp, devices/VirtualKeyboard.cpp,
protocols/VirtualKeyboard.cpp), hyprlang v0.6.8 src/config.cpp and the hyprland-wiki Keywords page at ecc06f3b6605.
Fenced code blocks of the entry, README and lesson are removed before any line is matched. The entry is admitted
iff every clause holds:
  a  ENTRY exists at REV and is absent at BASE (present at BASE is a setup error, exit 2);
  b  within its first 20 raw lines, outside fences: >= 4 distinct `source: S###` lines, exactly one
     `verified-at: DATE` and exactly one `recheck:` (ISO date, `NNd` or `on-*`); no such line elsewhere; no
     `S###` token anywhere in the entry that is not a cited id; every fenced block, whitespace-collapsed, occurs
     verbatim in the concatenated pins and no fence is left open (T3);
  c  every cited id has exactly one Registry row (0-3 leading spaces), 11 cells, status `mined`, a valid recheck
     cell, and used-by listing ENTRY; ids absent at BASE (>= 3) carry opened DATE and a location (last token of
     cell 1) holding `/` and `.`, and no cell matching `supersed*|replac*|obsolet*` (T2); ids present at BASE keep
     cells 1-9 byte-equal and every BASE used-by item;
  d  LESSON `## Gate` holds per cited id exactly one column-0 line `GATE <id> receipt=<path> sha256=<hex>
     quote="<q>"` (none outside that section); the receipt is a 100644 file under FETCH at REV with that sha256,
     >= 256 bytes; distinct path, sha256 and quote per id; a receipt whose file name is one of PINS must be at
     FETCH/<name> with exactly the pinned sha256 - held ids included; a new id's receipt must be one of PINS; the
     quote is 3-25 words, occurs exactly once in its receipt's normalized text at word boundaries, also with
     comments removed (C/C++ `//`,`/* */`; `#` in .py/.conf), and in no other cited receipt;
  e  each new id's location occurs in no other row whose scope cell (cell 5) equals its own, and its last path
     component and the receipt name contain one another; a `Hyprland-` receipt's location starts with the
     efb50993 raw URL; for every cited id gated on a PINS receipt the location is exactly that pin's URL; a new
     row's anchor cell names the receipt with `<name>:<a>[-<b>]` ranges inside the receipt's line count;
  f  corpus/README.md holds exactly one column-0 index row for ENTRY, with three cells, whose third cell's `S###`
     and `S###-S###` tokens expand to exactly the cited ids (T5);
  g  per cited id one entry line names that id and no other, carries its Gate quote and the computed locator
     `<receipt name>:<N>` (N = the receipt line where the quote starts); EVERY unfenced line naming a cited id
     (other than its `source:` line) carries that id's quote and locator; only the exact census line of h is
     exempt from these line checks;
  h  input-device census: from the pins the counter computes the global kb_layout default (ConfigValues.cpp
     `MS<String>("input:kb_layout", "<doc>", "<D>",`), the layout a keyboard falls back to when its names do not
     compile (IKeyboard.cpp `m_currentRules.layout = "<F>";`), the number of `device` special-category values
     (legacy ConfigManager.cpp lines carrying `m_config->addSpecialConfigValue("device", "`), the scroll-factor clamp
     ceiling (InputManager.cpp `getDeviceFloat(devname, "scroll_factor", "input:scroll_factor"), 0.F, <M>.F)`), the
     JSON scrollFactor decimals (HyprCtl.cpp `"scrollFactor": {:.<P>f}`) and the virtual-keyboard name prefix
     (protocols/VirtualKeyboard.cpp `std::string name = "<V>";`), each pattern occurring exactly once; the entry
     carries, verbatim, unfenced and exactly once, `hyprland input-device default_layout=<D> fallback_layout=<F>
     device_keys=<n> scroll_factor_max=<M> json_scroll_decimals=<P> virtual_prefix=<V>`, and no other entry line
     carries one of those six names followed by optional spaces, `=` or `:` and another value (T1);
  i  no cited row and no entry line holds a BAD_LOC marker; the Gate receipts of the cited ids cover every name in
     PINS; every entry line that carries a verdict token (AGREE, DIFFER, FALLBACK, VIRTUAL, MATCHED,
     NO_SUCH_DEVICE, STALE_BLOCK, NO_KEYBOARDS, NOT_COMPARED) and cites a `.ufo/waves/round-N/receipts/<file>` path
     finds each of its tokens in the first cited receipt at REV (T4);
  j  surface coverage: for each SURFACES item (pinned receipt, anchor text that occurs exactly once in it, keyword)
     the counter computes the anchor's line L, and some unfenced entry line outside the first 20 raw lines carries
     a locator `<receipt>:<a>[-<b>]` with a <= L <= b (b = a when absent) and b - a <= 30, and matches the keyword
     (case-insensitive). The twenty-eight surfaces: applyConfigToKeyboard, its kb_layout lookup, its setKeymap call,
     its did-not-change skip, the explicitly-set scroll_factor test and the nullopt branch, getNameForNewDevice
     (InputManager.cpp); the `device` special category, the not-set-by-user fallback, deviceConfigExists and the
     STRVAL_EMPTY read (legacy ConfigManager.cpp); the kb_layout default and the input:scroll_factor option
     (ConfigValues.cpp); the "us" fallback, the keymap-overridden early return and the kb_file branch
     (IKeyboard.cpp); the JSON scrollFactor field and the layout field (HyprCtl.cpp); the override flag set by a
     virtual keyboard (devices/VirtualKeyboard.cpp); the virtual name (protocols/VirtualKeyboard.cpp); the name
     normalizer (MiscFunctions.cpp); the bracket key, the first-value-must-be-the-key error, the `##` escape, the
     backslash continuation and the special-key reset at the last close (hyprlang config.cpp); the wiki's override
     sentence and its `hyprctl devices` name sentence (wiki-Keywords.md).
Final line: `PRED-C2-r46: admitted=N/1 verdict=TARGET_MET|TARGET_MISSED rev=<full hash>`; exit 0 iff admitted=1/1,
else 1; setup failure exit 2.
Residuals (declared): the pins are the trust root; a true quote at a true locator can stand beside a claim it does
not support, a decision table naming no id is not bound, and a census value contradicted in words rather than tokens is
not caught (the non-author reading); registry cells 3-6 of a new row are not read except the scope cell, the anchor
ranges and the T2 words; clause j binds a locator and a keyword per surface, not the truth of the sentence around them;
the census line is bookkeeping of pinned bytes.
"""
import argparse
import collections
import datetime
import hashlib
import html
import json
import os
import re
import subprocess
import sys

PRED = "PRED-C2-r46"
BASE_DEFAULT = "b22ea56bff2faec39ce9ff75d2107eaf4612ecbe"
ENTRIES = ("corpus/knowledge/hyprland-input-devices-r46.md",)
LESSON = "corpus/lessons/round-46.md"
FETCH = ".ufo/waves/round-46/fetch/"
OPENED = "2026-10-26"
MIN_RECEIPT = 256
ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
ROW_RE = re.compile(r"^ {0,3}\|\s*(S\d{3,})\s*\|")
GATE_RE = re.compile(r'^GATE (S\d{3,}) receipt=(\S+) sha256=([0-9a-f]{64}) '
                     r'quote="(.+)"\s*$')
RECHECK_RE = re.compile(r"^(\d{4}-\d{2}-\d{2}|\d+d|on-[a-z-]+)(\s|$)")
SRC_RE = re.compile(r"^source:\s*(S\d{3,})\b")
JWIDTH = 30
BAD_LOC = ("amgsk.dev", "zhihu", "/zh", "/ja", "zenn.dev", "qiita.com", "/jp/",
           "/cn/", "t.co/", "bit.ly", "\u65e5\u672c", "\u4e2d\u6587")
# the receipts the L1 fetched before the wave (fetch/ at the freeze); a NEW
# cited id's receipt must be one of them, byte for byte
PINS = {
    "Hyprland-InputManager.cpp": "feedf32e2e3d23aeaed7a02ef4ab94be2d66f4b22873b3166026da1e9ece4765",
    "Hyprland-ConfigManager.cpp": "9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b",
    "Hyprland-ConfigValues.cpp": "a76f05079454e1f6d4402144e1673cc1cb890d285fbeb947d5afdb004ad97754",
    "Hyprland-IKeyboard.cpp": "8a800efe9baa7f375a3781744372eecd98a88be2c4bedaae96c90a1102a1aa3d",
    "Hyprland-HyprCtl.cpp": "798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa",
    "Hyprland-MiscFunctions.cpp": "065418241a3b40e21273bca1fd29036221942554cddb61e08422d86f0a13c1d9",
    "Hyprland-VirtualKeyboard.cpp": "bc6d984a4c9e62313501c1cdb4ace3659c16d3b77e029a3c082a77f21500ed86",
    "Hyprland-protocols-VirtualKeyboard.cpp": "43cbf7b39bf0910df6d933cef95f029fa336d5b432b0202280e6fc40d8db2f50",
    "hyprlang-config.cpp": "fa1b6898f2f1676de73220450f18f09603f0c3f8833e4c0a7c42c12aebe1de3e",
    "wiki-Keywords.md": "11c0842cb31ddbfd55298c772bc44d9ad8d29c0c91c69bef6010e39b3ebaf51e",
}
HY = "https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/"
PINS_URL = {
    "Hyprland-InputManager.cpp": HY + "managers/input/InputManager.cpp",
    "Hyprland-ConfigManager.cpp": HY + "config/legacy/ConfigManager.cpp",
    "Hyprland-ConfigValues.cpp": HY + "config/values/ConfigValues.cpp",
    "Hyprland-IKeyboard.cpp": HY + "devices/IKeyboard.cpp",
    "Hyprland-HyprCtl.cpp": HY + "debug/HyprCtl.cpp",
    "Hyprland-MiscFunctions.cpp": HY + "helpers/MiscFunctions.cpp",
    "Hyprland-VirtualKeyboard.cpp": HY + "devices/VirtualKeyboard.cpp",
    "Hyprland-protocols-VirtualKeyboard.cpp": HY + "protocols/VirtualKeyboard.cpp",
    "hyprlang-config.cpp": "https://raw.githubusercontent.com/hyprwm/hyprlang/v0.6.8/src/config.cpp",
    "wiki-Keywords.md": "https://raw.githubusercontent.com/hyprwm/hyprland-wiki/ecc06f3b6605e453c0ad533d979fccbefff788ef/content/Configuring/Keywords.md",
}


class Setup(Exception):
    pass


def git(repo, *args):
    p = subprocess.run(["git", "-C", repo, *args], capture_output=True,
                       env=ENV)
    return p.stdout if p.returncode == 0 else None


def show(repo, rev, path):
    return git(repo, "show", "%s:%s" % (rev, path))


def resolve(repo, rev):
    out = git(repo, "rev-parse", "--verify", "--quiet", rev + "^{commit}")
    if not out:
        raise Setup("unresolved revision %s" % rev)
    return out.decode().strip()


def section(text, title):
    out, inside = [], False
    for line in text.splitlines():
        if line.startswith("## "):
            inside = line.strip() == title
            continue
        if inside:
            out.append(line)
    return out


def unfenced(text):
    out, fenced = [], False
    for line in text.splitlines():
        if re.match(r"^\s{0,3}(```|~~~)", line):
            fenced = not fenced
            continue
        if not fenced:
            out.append(line)
    return out


def registry(blob):
    rows = {}
    for line in section((blob or b"").decode("utf-8", "replace"),
                        "## Registry"):
        m = ROW_RE.match(line)
        if m:
            cells = [c.strip() for c in line.strip().split("|")[1:-1]]
            rows.setdefault(m.group(1), []).append(cells)
    return rows


def valid_date(s):
    m = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", s)
    if not m:
        return False
    try:
        datetime.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    except ValueError:
        return False
    return True


def recheck_ok(rc):
    m = RECHECK_RE.match(rc or "")
    if not m:
        return False
    tok = m.group(1)
    return valid_date(tok) if re.fullmatch(r"\d{4}-\d{2}-\d{2}", tok) else True


def ls_mode(repo, rev, path):
    out = git(repo, "ls-tree", rev, "--", path)
    if not out:
        return None
    return out.split()[0].decode()


def looks_html(blob):
    return re.search(rb"<(!doctype|html|body|div|p)\b", blob[:4096], re.I) \
        is not None


def norm_receipt(blob):
    text = blob.decode("utf-8", "replace")
    if looks_html(blob):
        return norm(text)
    return re.sub(r"\s+", " ", text).strip()


def collapse_with_lines(text):
    """(collapsed text, 1-based line number of each collapsed character)."""
    out, lines, prev = [], [], True
    for ln, line in enumerate(text.split("\n"), 1):
        for ch in line + "\n":
            if ch.isspace():
                if not prev:
                    out.append(" ")
                    lines.append(ln)
                    prev = True
            else:
                out.append(ch)
                lines.append(ln)
                prev = False
    return "".join(out), lines


def quote_at(blob, nq):
    """Line of the first word-bounded occurrence of the normalized quote in a
    non-HTML receipt, 0 for an HTML receipt that holds it word-bounded, None."""
    isw = lambda c: c.isalnum() or c == "_"
    if looks_html(blob):
        text = norm(blob.decode("utf-8", "replace"))
        lines = None
    else:
        text, lines = collapse_with_lines(blob.decode("utf-8", "replace"))
    start = 0
    while True:
        k = text.find(nq, start)
        if k < 0:
            return None
        before = text[k - 1] if k > 0 else " "
        after = text[k + len(nq)] if k + len(nq) < len(text) else " "
        if not (isw(nq[0]) and isw(before)) and not (isw(nq[-1]) and isw(after)):
            return lines[k] if lines else 0
        start = k + 1




def occurrences(blob, nq):
    isw = lambda c: c.isalnum() or c == "_"
    if looks_html(blob):
        text = norm(blob.decode("utf-8", "replace"))
    else:
        text = collapse_with_lines(blob.decode("utf-8", "replace"))[0]
    out, start = [], 0
    while True:
        k = text.find(nq, start)
        if k < 0:
            return out
        before = text[k - 1] if k > 0 else " "
        after = text[k + len(nq)] if k + len(nq) < len(text) else " "
        if not (isw(nq[0]) and isw(before)) and not (isw(nq[-1]) and isw(after)):
            out.append(k)
        start = k + 1


def strip_comments(text, path):
    ext = os.path.splitext(path)[1].lower()
    if ext in (".cpp", ".hpp", ".h", ".cc"):
        text = re.sub(r"/\*.*?\*/", " ", text, flags=re.S)
        return re.sub(r"//[^\n]*", " ", text)
    if ext in (".py", ".conf"):
        return re.sub(r"#[^\n]*", " ", text)
    return text


def quote_in_code(blob, nq, path):
    flat = re.sub(r"\s+", " ", strip_comments(blob.decode("utf-8", "replace"), path))
    return nq in flat


def all_body_lines_bound(ids, entry_lines, gates, receipts_raw):
    for i in ids:
        gl = gates.get(i, [])
        if len(gl) != 1 or i not in receipts_raw:
            return False
        path, digest, quote = gl[0]
        q = re.sub(r"\s+", " ", quote)
        at = quote_at(receipts_raw[i], q)
        bn = os.path.basename(path)
        for l in entry_lines:
            if not re.search(r"\b%s\b" % i, l):
                continue
            if l.startswith("source:"):
                continue
            if q not in l:
                return False
            if at and ("%s:%d" % (bn, at)) not in l:
                return False
    return True


def norm(text):
    text = re.sub(r"<script.*?</script>|<style.*?</style>", " ", text,
                  flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


CENSUS_KEYS = ("default_layout", "fallback_layout", "device_keys", "scroll_factor_max",
               "json_scroll_decimals", "virtual_prefix")


def host_census(new_ids, reg_rev, gates, receipts_raw, lines):
    """Clause h (round 46): recompute the input-device census line from the pinned receipts."""
    byname = {}
    for i, gl in gates.items():
        if i in receipts_raw and gl and gl[0] is not None and len(gl) == 1:
            byname[os.path.basename(gl[0][0])] = receipts_raw[i].decode("utf-8", "replace")
    need = ("Hyprland-ConfigValues.cpp", "Hyprland-IKeyboard.cpp", "Hyprland-ConfigManager.cpp",
            "Hyprland-InputManager.cpp", "Hyprland-HyprCtl.cpp", "Hyprland-protocols-VirtualKeyboard.cpp")
    if not all(n in byname for n in need):
        return False, []
    d = re.findall(r'MS<String>\("input:kb_layout", "[^"]*", "([^"]*)",', byname["Hyprland-ConfigValues.cpp"])
    f = re.findall(r'm_currentRules\.layout\s*=\s*"([^"]*)";', byname["Hyprland-IKeyboard.cpp"])
    n = sum(1 for l in byname["Hyprland-ConfigManager.cpp"].split("\n")
            if 'm_config->addSpecialConfigValue("device", "' in l)
    m = re.findall(r'getDeviceFloat\(devname, "scroll_factor", "input:scroll_factor"\), 0\.F, ([0-9]+)\.F\)',
                   byname["Hyprland-InputManager.cpp"])
    p = re.findall(r'"scrollFactor": \{:\.([0-9])f\}', byname["Hyprland-HyprCtl.cpp"])
    v = re.findall(r'std::string name = "([^"]+)";', byname["Hyprland-protocols-VirtualKeyboard.cpp"])
    if len(d) != 1 or len(f) != 1 or len(m) != 1 or len(p) != 1 or len(v) != 1 or n == 0:
        return False, []
    want = ["hyprland input-device default_layout=%s fallback_layout=%s device_keys=%d scroll_factor_max=%s "
            "json_scroll_decimals=%s virtual_prefix=%s" % (d[0], f[0], n, m[0], p[0], v[0])]
    ok = all(sum(1 for l in lines if l == w) == 1 for w in want)
    return ok, want


SURFACES = [
    ("Hyprland-InputManager.cpp", "void CInputManager::applyConfigToKeyboard(SP<IKeyboard> pKeyboard) {", r"applyConfigToKeyboard|per keyboard", "apply-keyboard"),
    ("Hyprland-InputManager.cpp", 'const auto LAYOUT   = Config::mgr()->getDeviceString(devname, "kb_layout", "input:kb_layout");', r"kb_layout", "kb-layout-lookup"),
    ("Hyprland-InputManager.cpp", "pKeyboard->setKeymap(IKeyboard::SStringRuleNames{LAYOUT, MODEL, VARIANT, OPTIONS, RULES});", r"setKeymap|names", "set-keymap"),
    ("Hyprland-InputManager.cpp", 'Log::logger->log(Log::DEBUG, "Not applying config to keyboard, it did not change.");', r"unchanged|did not change", "unchanged-skip"),
    ("Hyprland-InputManager.cpp", 'if (Config::mgr()->deviceConfigExplicitlySet(devname, "scroll_factor"))', r"scroll_factor", "scroll-explicit"),
    ("Hyprland-InputManager.cpp", "m->m_scrollFactor = std::nullopt;", r"-1|nullopt", "scroll-nullopt"),
    ("Hyprland-InputManager.cpp", "std::string CInputManager::getNameForNewDevice(std::string internalName) {", r"duplicate|suffix", "dup-name"),
    ("Hyprland-ConfigManager.cpp", 'm_config->addSpecialCategory("device", {"name"});', r"device block|special category", "device-category"),
    ("Hyprland-ConfigManager.cpp", "if ((!VAL || !VAL->m_bSetByUser) && !fallback.empty())", r"fallback|global", "set-by-user"),
    ("Hyprland-ConfigManager.cpp", "bool CConfigManager::deviceConfigExists(const std::string& dev) {", r"exists", "config-exists"),
    ("Hyprland-ConfigManager.cpp", "if (VAL == STRVAL_EMPTY)", r"EMPTY", "strval-empty"),
    ("Hyprland-ConfigValues.cpp", 'MS<String>("input:kb_layout", "Appropriate XKB keymap parameter", "us",', r"default", "kb-layout-default"),
    ("Hyprland-ConfigValues.cpp", 'MS<Float>("input:scroll_factor",', r"input:scroll_factor", "global-scroll-factor"),
    ("Hyprland-IKeyboard.cpp", 'm_currentRules.layout  = "us";', r"fall", "fallback-us"),
    ("Hyprland-IKeyboard.cpp", "if (m_keymapOverridden) {", r"overrid", "keymap-overridden"),
    ("Hyprland-IKeyboard.cpp", "if (!m_xkbFilePath.empty()) {", r"kb_file", "kb-file"),
    ("Hyprland-HyprCtl.cpp", '"scrollFactor": {:.2f}', r"scrollFactor", "json-scroll"),
    ("Hyprland-HyprCtl.cpp", "escapeJSONStrings(k->m_currentRules.layout)", r"layout", "json-layout"),
    ("Hyprland-VirtualKeyboard.cpp", "m_keymapOverridden = true;", r"virtual", "virtual-override"),
    ("Hyprland-protocols-VirtualKeyboard.cpp", 'std::string name = "hl-virtual-keyboard";', r"hl-virtual-keyboard", "virtual-name"),
    ("Hyprland-MiscFunctions.cpp", "std::string deviceNameToInternalString(const std::string& in) {", r"lower|name", "name-normalizer"),
    ("hyprlang-config.cpp", "if (valueName.contains('[') && valueName.contains(']')) {", r"bracket", "bracket-key"),
    ("hyprlang-config.cpp", 'result.setError(std::format("special category\'s first value must be the key. Key for <{}> is <{}>", PCAT->name, PCAT->key));', r"first value|first key", "first-value-key"),
    ("hyprlang-config.cpp", "if (line[commentPos + 1] == '#') {", r"##|comment", "hash-escape"),
    ("hyprlang-config.cpp", "while (line.length() > 0 && line.at(line.length() - 1) == '\\\\') {", r"backslash|continuation", "continuation"),
    ("hyprlang-config.cpp", 'impl->currentSpecialKey      = "";', r"close|reset|forgotten", "special-reset"),
    ("wiki-Keywords.md", "Per-device config options will overwrite your options set in the `input`", r"wiki|document", "wiki-override"),
    ("wiki-Keywords.md", "The `name` can be easily obtained by checking the output of `hyprctl devices`.", r"hyprctl devices", "wiki-name"),
]


def surfaces_ok(repo, rev, text, name):
    """Clause j: every surface's computed line is cited, with its keyword, outside the header window."""
    raw_lines = text.splitlines()
    body_lines, fenced = [], False
    for k, l in enumerate(raw_lines):
        if re.match(r"^\s{0,3}(```|~~~)", l):
            fenced = not fenced
            continue
        if not fenced and k >= 20:
            body_lines.append(l)
    ok = True
    for rname, anchor, kw, label in SURFACES:
        blob = show(repo, rev, FETCH + rname)
        if blob is None:
            print("%s %s clause=j surface=%s receipt_missing" % (PRED, name, label))
            ok = False
            continue
        rl = blob.decode("utf-8", "replace").split("\n")
        hits = [n for n, l in enumerate(rl, 1) if anchor in l]
        if len(hits) != 1:
            print("%s %s clause=j surface=%s anchor_count=%d" % (PRED, name, label, len(hits)))
            ok = False
            continue
        L = hits[0]
        pat = re.compile(r"(?<![\w.-])%s:(\d+)(?:-(\d+))?(?!\d)" % re.escape(rname))
        found = False
        for l in body_lines:
            if not re.search(kw, l, re.I):
                continue
            for a, b in pat.findall(l):
                if int(a) <= L <= int(b or a) and int(b or a) - int(a) <= JWIDTH:
                    found = True
        ok &= found
        print("%s %s clause=j surface=%s line=%d cited=%d" % (PRED, name, label, L, found))
    return ok

def fences_ok(repo, rev):
    """T3: a fenced block may only carry text that occurs verbatim in a pinned receipt."""
    text = (show(repo, rev, ENTRIES[0]) or b"").decode("utf-8", "replace")
    blocks, cur, fenced = [], [], False
    for line in text.splitlines():
        if re.match(r"^\s{0,3}(```|~~~)", line):
            if fenced:
                blocks.append("\n".join(cur))
                cur = []
            fenced = not fenced
            continue
        if fenced:
            cur.append(line)
    if fenced:
        return False
    if not any(b.strip() for b in blocks):
        return True
    pins = " ".join(re.sub(r"\s+", " ", (show(repo, rev, FETCH + p) or b"").decode("utf-8", "replace"))
                    for p in sorted(PINS))
    return all(re.sub(r"\s+", " ", b).strip() in pins for b in blocks if b.strip())



def score(repo, rev, base, entry, reg_rev, reg_base, lesson, readme):
    name = os.path.basename(entry)
    cl = dict.fromkeys("abcdefghij", 0)
    raw = show(repo, rev, entry)
    text = raw.decode("utf-8", "replace") if raw is not None else ""
    lines = unfenced(text)
    cl["a"] = int(raw is not None)
    # header: only unfenced lines inside the first 20 raw lines count; every
    # source:/verified-at:/recheck: line of the whole entry must sit there
    head, fenced_state, window = [], False, 0
    for k, l in enumerate(text.splitlines()):
        if re.match(r"^\s{0,3}(```|~~~)", l):
            fenced_state = not fenced_state
            continue
        if not fenced_state:
            if k < 20:
                head.append(l)
            elif re.match(r"^(source|verified-at|recheck):", l):
                window += 1
    ids = []
    for line in head:
        m = SRC_RE.match(line)
        if m and m.group(1) not in ids:
            ids.append(m.group(1))
    cited = set(re.findall(r"\b[Ss]\d{3,}\b", "\n".join(lines)))
    ghosts = cited - set(ids)

    def hv(key):
        vals = [l[len(key) + 1:].strip() for l in head
                if l.startswith(key + ":")]
        return vals[0] if len(vals) == 1 else None
    va, rc = hv("verified-at"), hv("recheck")
    cl["b"] = int(len(ids) >= 4 and va == OPENED and recheck_ok(rc)
                  and window == 0 and not ghosts)

    rows_ok = bool(ids)
    new_ids = []
    for i in ids:
        rows = reg_rev.get(i, [])
        if len(rows) != 1 or len(rows[0]) != 11:
            rows_ok = False
            print("%s %s clause=c id=%s rows=%d" % (PRED, name, i, len(rows)))
            continue
        cells = rows[0]
        items = [x.strip() for x in re.split(r"[,;]", cells[10])]
        good = cells[7] == "mined" and entry in items \
            and recheck_ok(cells[9])
        if i in reg_base:
            old = reg_base[i]
            good &= len(old) == 1 and len(old[0]) == 11 \
                and old[0][:9] == cells[:9] and recheck_ok(cells[9]) is not None
            good &= set(x.strip() for x in re.split(r"[,;]", old[0][10])
                        if x.strip() not in ("", "\u2014")) <= set(items)
        else:
            new_ids.append(i)
            loc = cells[1].split()[-1] if cells[1].split() else ""
            good &= cells[8] == OPENED and ("/" in loc and "." in loc)
            # T2: a new row never claims to supersede or replace anything
            good &= not re.search(r"\b(supersed\w*|replac\w*|obsolet\w*)\b", " ".join(cells), re.I)
        rows_ok &= good
        print("%s %s clause=c id=%s new=%d status=%s used=%d ok=%d" % (
            PRED, name, i, i not in reg_base, cells[7], entry in items, good))
    cl["c"] = int(rows_ok and len(new_ids) >= 3)

    glines = unfenced("\n".join(section(lesson, "## Gate")))
    gates = collections.defaultdict(list)
    for line in glines:
        m = GATE_RE.match(line.rstrip("\n"))
        if m:
            gates[m.group(1)].append(m.groups()[1:])
        elif re.match(r"^\s+GATE S\d", line):
            gates["<indented>"].append(None)
    outside = 0
    in_gate = set(glines)
    for line in unfenced(lesson):
        if re.match(r"^GATE S\d", line) and line not in in_gate:
            outside += 1
    d_ok, g_ok = bool(ids), bool(ids)
    receipts, receipts_raw = {}, {}
    seen_paths, seen_sha, seen_quote = set(), set(), set()
    for i in ids:
        good = None
        gl = gates.get(i, [])
        if len(gl) == 1:
            path, digest, quote = gl[0]
            blob = show(repo, rev, path) if path.startswith(FETCH) else None
            pin_ok = PINS.get(os.path.basename(path)) in (None, digest) \
                and (os.path.basename(path) not in PINS
                     or path == FETCH + os.path.basename(path))
            nq = re.sub(r"\s+", " ", quote)
            if (blob is not None and len(blob) >= MIN_RECEIPT and pin_ok
                    and ls_mode(repo, rev, path) == "100644"
                    and hashlib.sha256(blob).hexdigest() == digest
                    and 3 <= len(quote.split()) <= 25
                    and path not in seen_paths and digest not in seen_sha
                    and nq not in seen_quote
                    and quote_at(blob, nq) is not None
                    and len(occurrences(blob, nq)) == 1
                    and quote_in_code(blob, nq, path)):
                good = quote
                receipts[i] = blob.decode("utf-8", "replace")
                receipts_raw[i] = blob
                seen_paths.add(path)
                seen_sha.add(digest)
                seen_quote.add(nq)
        print("%s %s clause=d id=%s gates=%d bound=%d" % (
            PRED, name, i, len(gl), good is not None))
        if good is None:
            d_ok = g_ok = False
    # a quote occurs in its own receipt and in no other cited receipt
    for i in receipts:
        q = re.sub(r"\s+", " ", gates[i][0][2])
        for j in receipts:
            if j != i and q in norm_receipt(receipts_raw[j]):
                d_ok = False
                print("%s %s clause=d quote of %s also in receipt of %s" % (
                    PRED, name, i, j))
    cl["d"] = int(d_ok and not gates.get("<indented>") and outside == 0)

    e_ok = True
    for i in new_ids:
        gl_ = gates.get(i, [])
        cells_ = reg_rev[i][0] if len(reg_rev.get(i, [[]])[0]) == 11 else None
        if cells_ is None or len(gl_) != 1:
            e_ok = False
            continue
        comp = re.split(r"[?#]", cells_[1].split()[-1])[0].rstrip("/") \
            .rsplit("/", 1)[-1].lower()
        rb = os.path.basename(gl_[0][0]).lower()
        e_ok &= bool(comp) and (comp in rb or rb in comp)
        if rb.startswith('hyprland-') and not cells_[1].split()[-1].startswith(
                'https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/'):
            e_ok = False
        cells = reg_rev[i][0] if len(reg_rev.get(i, [[]])[0]) == 11 else None
        if cells is None:
            e_ok = False
            continue
        loc = cells[1].split()[-1] if cells[1].split() else ""
        key = loc.split("#")[0]
        same = [j for j, rr in reg_rev.items() for r in rr
                if len(r) == 11 and r[1].split()
                and r[1].split()[-1].split("#")[0] == key and r[4] == cells[4]]
        e_ok &= bool(loc) and same == [i]
    for i in ids:
        gl_ = gates.get(i, [])
        row_ = reg_rev.get(i, [])
        if len(gl_) == 1 and row_ and len(row_[0]) == 11:
            loc_ = row_[0][1].split()[-1].split("#")[0] if row_[0][1].split() else ""
            pin_url = PINS_URL.get(os.path.basename(gl_[0][0]))
            if pin_url is not None and pin_url.split("#")[0] != loc_:
                e_ok = False
                print("%s %s clause=e+ id=%s location=%s pin=%s" % (
                    PRED, name, i, loc_, pin_url))
    # T4: a new row's anchor must name the receipt it is gated on and stay inside it
    for i in new_ids:
        row_ = reg_rev.get(i, [])
        gl_ = gates.get(i, [])
        if not row_ or len(row_[0]) != 11 or len(gl_) != 1 or i not in receipts_raw:
            e_ok = False
            continue
        rb_ = os.path.basename(gl_[0][0])
        nlines_ = len(receipts_raw[i].decode("utf-8", "replace").splitlines())
        anchor_ = row_[0][5]
        rng = re.findall(r"%s:(\d+)(?:-(\d+))?" % re.escape(rb_), anchor_)
        if not rng or any(int(b or a) > nlines_ for a, b in rng):
            e_ok = False
            print("%s %s clause=e/4 id=%s anchor=%s receipt_lines=%d" % (
                PRED, name, i, anchor_[:70], nlines_))
    cl["e"] = int(e_ok and bool(new_ids))

    h_ok, census_lines = host_census(new_ids, reg_rev, gates, receipts_raw, lines)
    census_lines = set(census_lines)

    entry_lines = [re.sub(r"\s+", " ", l) for l in lines
                   if l not in census_lines
]
    if h_ok:
        want = dict(re.findall(r"(\w+)=(\S+)", next(iter(census_lines))))
        for l in entry_lines:
            for key, v in re.findall(r"\b(%s)\s*[:=]\s*(\S+)" % "|".join(CENSUS_KEYS), l):
                if v.rstrip(".,;:)`") != want.get(key):
                    h_ok = False
                    print("%s %s clause=h prose %s=%s != %s" % (PRED, name, key, v, want.get(key)))
    cl["h"] = int(h_ok)
    for i in ids:
        quote = None
        for path, digest, q in gates.get(i, []):
            quote = q
        if i not in receipts or quote is None:
            g_ok = False
            continue
        q = re.sub(r"\s+", " ", quote)
        at = quote_at(receipts_raw[i], q)
        base_name = os.path.basename(gates[i][0][0])
        loc_ok = True if at == 0 else (at is not None and
                                       re.search(r"(?<![\w.-])%s:%d(?!\d)" % (re.escape(base_name), at), "\n".join(entry_lines)) is not None)
        hit = any(re.search(r"\b%s\b" % i, l) and q in l
                  and len(set(re.findall(r"\bS\d{3,}\b", l))) == 1
                  and (at == 0 or (at is not None and ("%s:%d" % (base_name, at)) in l
                                   and re.search(r"(?<![\w.-])%s:%d(?!\d)" % (re.escape(base_name), at), l)))
                  for l in entry_lines)
        g_ok &= hit
        print("%s %s clause=g id=%s obs=%d locator_line=%s" % (PRED, name, i, hit, at))
    cl["g"] = int(g_ok and all_body_lines_bound(ids, entry_lines, gates, receipts_raw))

    pat = re.compile(r"^\| `knowledge/%s`" % re.escape(name))
    frows = [l for l in unfenced(readme) if pat.match(l)]
    cl["f"] = int(len(frows) == 1)
    # T5: the index row has three cells and its Sources cell lists exactly the cited ids
    if frows:
        fc = [c.strip() for c in frows[0].strip().strip("|").split("|")]
        listed = set()
        for a_, b_ in re.findall(r"S(\d{3,})(?:-S(\d{3,}))?", fc[2] if len(fc) > 2 else ""):
            listed |= set("S%03d" % k for k in range(int(a_), int(b_ or a_) + 1))
        cl["f"] &= int(len(fc) == 3 and listed == set(ids))
    # clause i: no assimilation part; location markers and pin coverage only
    bad = False
    for i in ids:
        rows = reg_rev.get(i, [])
        if rows and len(rows[0]) == 11:
            row_text = " ".join(rows[0]).lower()
            bad |= any(b_ in row_text for b_ in BAD_LOC)
    used = set(os.path.basename(gates[i][0][0]) for i in receipts)
    bad |= not set(PINS) <= used
    bad |= any(b_ in l.lower() for l in lines for b_ in BAD_LOC)
    cl["i"] = int(not bad)
    # T4: a verdict token on a line that cites a receipts/ path must occur in that receipt
    v_ok = True
    for l in entry_lines:
        toks = [t for t in ("AGREE", "DIFFER", "FALLBACK", "VIRTUAL", "MATCHED", "NO_SUCH_DEVICE", "STALE_BLOCK",
                            "NO_KEYBOARDS", "NOT_COMPARED") if re.search(r"\b%s\b" % t, l)]
        locs = re.findall(r"(?<![\w.-])(\.ufo/waves/round-\d+/receipts/[A-Za-z0-9._-]+)", l)
        if not toks or not locs:
            continue
        rec = (show(repo, rev, locs[0]) or b"").decode("utf-8", "replace")
        if not all(re.search(r"\b%s\b" % t, rec) for t in toks):
            v_ok = False
            print("%s %s clause=i verdict tokens %s not in %s" % (PRED, name, toks, locs[0]))
    cl["i"] = cl["i"] and int(v_ok)
    cl["b"] = cl["b"] and int(fences_ok(repo, rev))
    cl["j"] = int(raw is not None and surfaces_ok(repo, rev, text, name))
    admitted = int(all(cl.values()))
    print("%s %s clauses=%s admitted=%d" % (
        PRED, name, " ".join("%s:%d" % kv for kv in sorted(cl.items())),
        admitted))
    return admitted


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    ap.add_argument("--rev", required=True)
    ap.add_argument("--base", default=BASE_DEFAULT)
    args = ap.parse_args()
    repo = os.path.abspath(args.repo)
    rev = resolve(repo, args.rev)
    base = resolve(repo, args.base)
    for e in ENTRIES:
        if show(repo, base, e) is not None:
            raise Setup("precondition_failed entry_present_at_base %s" % e)
    reg_rev = registry(show(repo, rev, "corpus/SOURCES.md"))
    reg_base = registry(show(repo, base, "corpus/SOURCES.md"))
    lesson = (show(repo, rev, LESSON) or b"").decode("utf-8", "replace")
    readme = (show(repo, rev, "corpus/README.md") or b"").decode(
        "utf-8", "replace")
    n = sum(score(repo, rev, base, e, reg_rev, reg_base, lesson, readme)
            for e in ENTRIES)
    met = n == 1
    print("%s: admitted=%d/1 verdict=%s rev=%s" % (
        PRED, n, "TARGET_MET" if met else "TARGET_MISSED", rev))
    return 0 if met else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Setup as exc:
        print("%s SETUP %s" % (PRED, exc))
        sys.exit(2)
