#!/usr/bin/env python3
"""Build the round-49 C2 do-nothing and forgery control bundles (seat ExecControlsC2).

Every control is a candidate state of the lane that a correct PRED-C2-r49 must judge.
The grammar of the bundles follows the w1 draft
`.ufo/waves/round-49/w1/ExecCounterC2/c2-r49-bind-entry.py` (clauses a-i, r):

  00-base-golden              a complete entry; the anchor, must be ADMITTED
  01-do-nothing               no entry written; MISS (a)
  02-stub-head-one-sentence   head plus one sentence; MISS (e, f)
  03-paste-r46-verbatim       the round-46 chain pasted under a round-49 head, each pasted
                              step given a locator into a round-49 pin; MISS (i novelty)
  04-paste-r46-paraphrased    the same ground with every content word swapped; tests
                              whether i's novelty test is line overlap or meaning
  05-quote-forged-one-word    one identifier inside a cited quote changed; MISS (d)
  06-locator-off-by-one       a true quote cited one line below its line; MISS (d)
  07-steps-without-locators   six steps, no pin locator; MISS (e)
  08-branch-url-pin           a row URL ref replaced by a branch name; MISS (c)
  09-digest-edited-row-file   a pin byte changed AND the row digest recomputed; c holds
                              row==file, so this is the declared residual of c
  10-receipt-typed-by-hand    false live values the entry repeats; f alone cannot see it
  11-receipt-accurate-handtyped  true values, hand provenance; replay should still admit
  12-held-s319-reregistered   held S319 re-registered as S355 and cited instead; MISS (g)
  13-registry-row-unused      a new row with a Gate line but no claim using it; the draft
                              never reads used-by outside the head, so this is a gap test

Writes only under this seat dir.
"""
import hashlib
import json
import os
import re
import subprocess

SEAT = os.path.dirname(os.path.abspath(__file__))
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
BASE = "03e4ae76aff7a4be59cb69970dd553baa319695a"
ENTRY = "corpus/knowledge/hyprland-bind-key-match-r49.md"
FETCH = ".ufo/waves/round-49/fetch/"
RECEIPT = ".ufo/waves/round-49/receipts/live-binds-r49.txt"
COMMIT = "efb50993780079460b0cbed1363e2166a2de1d9f"
URLS = {
    "Hyprland-KeybindManager.cpp":
        "https://raw.githubusercontent.com/hyprwm/Hyprland/%s/src/managers/KeybindManager.cpp" % COMMIT,
    "libxkbcommon-src-keysym.c":
        "https://raw.githubusercontent.com/xkbcommon/libxkbcommon/xkbcommon-1.13.2/src/keysym.c",
    "Hyprland-IKeyboard.cpp":
        "https://raw.githubusercontent.com/hyprwm/Hyprland/%s/src/devices/IKeyboard.cpp" % COMMIT,
}
PINS = ("Hyprland-KeybindManager.cpp", "libxkbcommon-src-keysym.c", "Hyprland-IKeyboard.cpp")
PIN_DIR = os.path.join(SEAT, "pins")
CTL = os.path.join(SEAT, "controls")

# live host facts, captured read-only 2026-10-27; the receipt carries the commands
BINDS_SHA = "9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779"
BINDS = dict(total=192, named=142, code=42, mouse=6, switch=2,
             key_only=150, keycode_only=42, both=0, submap=0, described=190,
             names=64, code_lo=10, code_hi=201,
             modmasks="0,1,8,9,12,13,64,65,68,69,72,73,76", rbs_int=0)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def read(pin):
    return open(os.path.join(PIN_DIR, pin), "rb").read()


def collapse(s):
    return re.sub(r"\s+", " ", s).strip()


def locate(pin, quote):
    blob = read(pin).decode("utf-8", "replace").splitlines()
    nq = collapse(quote)
    hits = [i for i, line in enumerate(blob, 1) if nq in collapse(line)]
    if len(hits) != 1:
        raise SystemExit("locate %r in %s -> %r" % (quote[:60], pin, hits))
    return hits[0]


def words(s):
    return len(collapse(s).split())


# ---------------------------------------------------------------- entry sections
def head():
    return "\n".join([
        "# Hyprland 0.56.2: how the key field of a `bind` line becomes a match for a key press on this host",
        "",
        "source: S352 - Hyprland 0.56.2 keybind manager @ commit %s - the press path, the +8 keycode, the "
        "translated-or-sym state choice, the exact modifier compare, the name-to-keysym double lookup" % COMMIT[:12],
        "source: S353 - libxkbcommon 1.13.2 `src/keysym.c` @ xkbcommon-1.13.2 - `xkb_keysym_from_name`, the one flag "
        "it accepts, and the names it refuses",
        "source: S354 - mado host, read-only `hyprctl binds -j` and `hyprctl getoption input:resolve_binds_by_sym -j` "
        "receipt (own-work) - %d live binds, the form census, the live option value" % BINDS["total"],
        "verified-at: 2026-10-27",
        "recheck: on-release - when Hyprland leaves 0.56.2 or commit %s, or libxkbcommon leaves 1.13.2, re-pull "
        "`src/managers/KeybindManager.cpp` and `src/keysym.c` and re-run the capture behind `%s`; also when this host "
        "stops reporting the same bind total" % (COMMIT[:12], RECEIPT),
        "",
        "## What the evidence licenses",
        "",
        "| question | where the answer lives | state |",
        "|---|---|---|",
        "| which keycode a press carries | step 1 | sourced (S352) |",
        "| which keysym of the press is compared | step 2 | sourced (S352, S317); the live option value observed "
        "(S354) |",
        "| whether modifiers must match exactly | step 3 | sourced (S352) |",
        "| how a key name becomes a keysym, and what case does | step 4 | sourced (S352, S353) |",
        "| what a key field becomes at parse time | step 5 | held S303, not re-claimed |",
        "| whether a keycode bind and a name bind on one key collide | step 6 | sourced (S352); the census observed "
        "(S354) |",
        "",
    ])


def steps():
    k = "Hyprland-KeybindManager.cpp"
    q = [
        ("KEYCODE = e.keycode + 8;", 367,
         "**The press path converts libinput's code to XKB's.** The key event carries a code that is incremented "
         "by eight before any keymap call, because libinput and xkbcommon number the same keys differently; every "
         "later lookup and every stored keycode bind use that XKB number"),
        ("xkb_state_key_get_one_sym(pKeyboard->m_resolveBindsBySym ? pKeyboard->m_xkbSymState : "
         "m_xkbTranslationState, KEYCODE);", 369,
         "**One of two state objects supplies the compared keysym.** The call site picks the per-device sym state "
         "when `input:resolve_binds_by_sym` is on and the translated state otherwise, so by default the compared "
         "sym is the one the keyboard's stored keymap produces; the option is per-device and its default is zero, "
         "held in S317"),
        ("modmask != k->modmask && !k->ignoreMods", 652,
         "**Modifiers are compared by exact equality.** The mask of the press must equal the mask of the bind and "
         "there is exactly one relaxation, the ignore-mods flag; on release the mask captured at press time is "
         "used, so a key that is itself a modifier does not lose its own press"),
        ("xkb_keysym_from_name(k->key.c_str(), XKB_KEYSYM_NO_FLAGS)", 710,
         "**A key name is resolved twice, exact first.** The plain lookup allows no flags and the second allows "
         "case-insensitivity; a name that resolves under neither is skipped rather than compared against zero, and "
         "the library rejects any flag other than the case-insensitive bit"),
        ("key.keyName != k->key", 694,
         "**A press that carries a key name compares the name and nothing else.** The name branch is taken before "
         "the keycode branch, so the mouse and switch forms cannot fall through to a keycode bind; the parse-time "
         "key forms themselves are held in S303"),
        ("key.submapAtPress.name != Config::Actions::state()->m_currentSubmap", 699,
         "**Keycode binds and the catch-all come after the name branch, in that order.** A press with a keycode "
         "compares the keycode, and the catch-all is the last resort inside the submap that was active at press "
         "time, so a submap switch between press and release cannot retarget it"),
    ]
    out = ["## The match, step by step", ""]
    for i, (quote, _l, prose) in enumerate(q, 1):
        if not 2 <= words(quote) <= 25:
            raise SystemExit("step quote word count %d: %r" % (words(quote), quote))
        ln = locate(k, quote)
        out.append("%d. %s: `%s` at %s:%d." % (i, prose, quote, k, ln))
    out.append("")
    return "\n".join(out) + "\n"


QUOTES = [
    ("S352", "Hyprland-KeybindManager.cpp",
     "const auto         KEYCODE = e.keycode + 8;", "every later keymap call uses the +8 keycode"),
    ("S352", "Hyprland-KeybindManager.cpp",
     "xkb_state_key_get_one_sym(pKeyboard->m_resolveBindsBySym ? pKeyboard->m_xkbSymState : "
     "m_xkbTranslationState, KEYCODE);",
     "the compared sym is chosen by the per-device switch at the call site"),
    ("S352", "Hyprland-KeybindManager.cpp",
     "const auto KBKEY      = xkb_keysym_from_name(k->key.c_str(), XKB_KEYSYM_NO_FLAGS);",
     "the first lookup of a press is exact"),
    ("S352", "Hyprland-KeybindManager.cpp",
     "if (key.keysym != KBKEY && key.keysym != KBKEYLOWER)",
     "a press must equal the exact or the case-insensitive resolution"),
    ("S352", "Hyprland-KeybindManager.cpp",
     "if (!IGNORECONDITIONS && ((modmask != k->modmask && !k->ignoreMods)",
     "the modifier compare is inequality of the whole mask"),
    ("S353", "libxkbcommon-src-keysym.c",
     "bool icase = (flags & XKB_KEYSYM_CASE_INSENSITIVE);",
     "case-insensitivity is one bit and nothing else is honoured"),
]


def observations():
    out = ["## Observations", ""]
    for sid, pin, quote, gloss in QUOTES:
        ln = locate(pin, quote)
        if not 2 <= words(quote) <= 25:
            raise SystemExit("quote word count %d: %r" % (words(quote), quote))
        out.append("**OBS** %s: `%s` at %s:%d - %s." % (sid, quote, pin, ln, gloss))
    out += ["",
            "**OBS** S354: binds=%d, %d named, %d code, %d mouse, %d switch; the named binds cover %d distinct key "
            "strings and the keycodes run %d to %d."
            % (BINDS["total"], BINDS["named"], BINDS["code"], BINDS["mouse"], BINDS["switch"],
               BINDS["names"], BINDS["code_lo"], BINDS["code_hi"]),
            ""]
    return "\n".join(out)


def live():
    return "\n".join([
        "## Live host capture (read-only)",
        "",
        "`hyprctl version` reports Hyprland 0.56.2 at commit %s, and `hyprctl binds -j` returns binds=%d whose raw "
        "JSON sha256 is `%s`; `hyprctl getoption input:resolve_binds_by_sym -j` answers `int: %d, set: false`. The "
        "capture is `%s`."
        % (COMMIT, BINDS["total"], BINDS_SHA, BINDS["rbs_int"], RECEIPT),
        "",
        "The census by form is %d named, %d code, %d mouse and %d switch; the named strings include both `DELETE` "
        "and `Delete`, and no bind carries both a key and a keycode."
        % (BINDS["named"], BINDS["code"], BINDS["mouse"], BINDS["switch"]),
        "Because the option is %d, the compared sym is the translated one on this host, so a bind written as a name "
        "fires on the sym the stored keymap produces." % BINDS["rbs_int"],
        "",
    ])


def limits():
    return "\n".join([
        "## Limits",
        "",
        "- The comparison order inside a press is read from the source, not instrumented: no key event was injected "
        "and no dispatcher was fired, so what a matched bind then does is outside this entry.",
        "- The catch-all form has no live sample on this host, so its submap precondition is sourced only.",
        "- The multi-key flag and the long-press matcher have no live sample and are not claimed.",
        "- The pointer and switch paths are taken from the stored strings the census prints; the path that produces "
        "them is sourced, not observed.",
        "- The compositor half of the keymap (which keymap the keyboard stored) stays held in S318 and S319 and is "
        "not re-claimed here; `input:kb_layout` reaching a keymap is the round-48 entry's ground.",
        "- Session state, an active inhibitor or a submap can suppress a matched bind; this entry says nothing about "
        "dispatch conditions.",
        "",
    ])


def sections(*parts):
    return "\n\n".join(p.strip("\n") for p in parts) + "\n"


def base_entry():
    return sections(head(), steps(), observations(), live(), limits())


# ---------------------------------------------------------------- registry rows
def row(sid, title, url, kind, scope, digest, size, anchor, teaches, receipt):
    return ("| %s | %s - %s | %s | A | %s | %s @ %s, %d B sha256:%s; receipt %s%s | %s | mined | 2026-10-27 | "
            "90d | %s |" % (sid, title, url, kind, scope, anchor,
                            ("commit " + COMMIT) if kind == "code" else "access 2026-10-27",
                            size, digest, FETCH, receipt, teaches, ENTRY))


def rows(overrides=None):
    over = overrides or {}
    out = [row("S352",
               "Hyprland 0.56.2 keybind press path - the +8 keycode, the translated-or-sym state, the exact modmask "
               "compare, the double keysym lookup",
               URLS["Hyprland-KeybindManager.cpp"], "code",
               "How one press reaches a stored bind and which keysym and modifier mask it is compared with",
               over.get("S352", sha(read("Hyprland-KeybindManager.cpp"))),
               len(read("Hyprland-KeybindManager.cpp")),
               "KeybindManager.cpp:367, :369, :461-468, :652, :693-700, :707-724",
               "The compared sym is the translated one unless resolve_binds_by_sym; the mask must be equal unless the "
               "ignore-mods flag; a name resolves exact then case-insensitive",
               "Hyprland-KeybindManager.cpp"),
           row("S353",
               "libxkbcommon 1.13.2 keysym name lookup - the accepted flag and the refused ones",
               URLS["libxkbcommon-src-keysym.c"], "code",
               "How a key name becomes a keysym value and which flag is allowed",
               over.get("S353", sha(read("libxkbcommon-src-keysym.c"))),
               len(read("libxkbcommon-src-keysym.c")),
               "keysym.c:237-244",
               "Only the case-insensitive bit is accepted; any other flag yields no keysym",
               "libxkbcommon-src-keysym.c"),
           "| S354 | mado host - read-only `hyprctl binds` and `getoption` capture: the bind census and the live "
           "resolve_binds_by_sym value - %s | own-work | A | %d live binds split by form, the distinct key strings, "
           "and input:resolve_binds_by_sym | live-binds-r49.txt:1-%d @ access 2026-10-27, %d B sha256:%s; receipt "
           "%slive-binds-r49.txt | %d named, %d code, %d mouse and %d switch binds; the option is 0/false | mined | "
           "2026-10-27 | 90d | %s |"
           % (RECEIPT, BINDS["total"], receipt_lines(), receipt_size(), over.get("S354", receipt_sha()),
              FETCH, BINDS["named"], BINDS["code"], BINDS["mouse"], BINDS["switch"], ENTRY)]
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------- receipt
def receipt_text(int_value=None, total=None, mode="live", forms=None):
    i = BINDS["rbs_int"] if int_value is None else int_value
    t = BINDS["total"] if total is None else total
    f = dict(BINDS) if forms is None else forms
    s = "false" if i == 0 else "true"
    head_lines = [
        "# mado round 49 - read-only live capture of the Hyprland bind surface",
        "# host: mado workstation; date 2026-10-27",
        "# commands: hyprctl version ; hyprctl binds -j ; hyprctl getoption input:resolve_binds_by_sym -j",
        "# environment: HOME and XDG_* pointed at a scratch dir; HYPRLAND_INSTANCE_SIGNATURE inherited from the "
        "session",
        "# nothing was dispatched, reloaded, set or written; the compositor was only queried",
        "# no window titles, monitor serials, device names or home paths appear in this file",
        "# provenance: " + ("emitted by the capture run itself" if mode == "live"
                            else "typed by hand from a previous terminal, NOT a capture run"),
        "",
        "hyprctl version: Hyprland 0.56.2 built from branch v0.56.2 at commit %s clean" % COMMIT,
        "",
        "case: hyprctl binds -j",
        "  binds: %d" % t,
        "  sha256 (raw binds JSON): %s" % BINDS_SHA,
        "  fields: allow_input_capture arg auto_consuming catch_all description dispatcher has_description key "
        "keycode locked longPress modmask mouse non_consuming release repeat submap submap_universal",
        "  forms: named %d, code %d, mouse %d, switch %d"
        % (f["named"], f["code"], f["mouse"], f["switch"]),
        "  key_only: %d" % BINDS["key_only"],
        "  keycode_only: %d" % BINDS["keycode_only"],
        "  key_and_code: %d" % BINDS["both"],
        "  catch_all: %d" % 0,
        "  submap_nonempty: %d" % BINDS["submap"],
        "  has_description: %d" % BINDS["described"],
        "  distinct_key_strings: %d" % BINDS["names"],
        "  keycode_range: %d-%d" % (BINDS["code_lo"], BINDS["code_hi"]),
        "  modmask_values: %s" % BINDS["modmasks"],
        "",
        "case: hyprctl getoption input:resolve_binds_by_sym -j",
        "  input:resolve_binds_by_sym int: %d, set: %s" % (i, s),
        "",
        "note: binds -j prints the parsed bind table, not the keymap; the keymap half is the round-48 entry.",
        "",
    ]
    return "\n".join(head_lines)


def receipt_size(int_value=None):
    return len(receipt_text(int_value).encode())


def false_forms():
    """an internally consistent lie: 191 = 141 named + 42 code + 6 mouse + 2 switch."""
    g = dict(BINDS)
    g.update(total=191, named=141)
    return g


def receipt_lines():
    return len(receipt_text().splitlines())


def receipt_sha(int_value=None):
    return sha(receipt_text(int_value).encode())


def lesson(extra_rows=()):
    lines = ["# mado round 49 - lesson (seat draft; the L1 integrates)", "", "## Gate", "",
             "Candidates considered: the bind-match plane of the C2 claim.", ""]
    for sid, pin, quote, gloss in [q for q in QUOTES if q[0] in ("S352", "S353")]:
        ln = locate(pin, quote)
        lines.append("- **%s admit**, tier A, code. URL: `%s`; opened 2026-10-27; quote `%s` "
                     "(`fetch/%s:%d`). %s." % (sid, URLS[pin], quote, pin, ln, gloss))
    lines.append("- **S354 admit**, tier A, own-work. Source opened this round: the read-only capture `%s`; access "
                 "date 2026-10-27; binds=%d, option int %d. It is the host-specific execution result, not an "
                 "upstream source." % (RECEIPT, BINDS["total"], BINDS["rbs_int"]))
    lines += list(extra_rows)
    lines += ["", "No held row's status, recheck or used-by changed; S303, S317 and S319 are cited, not "
              "re-registered.", ""]
    return "\n".join(lines)


README_ROW = ("| `knowledge/hyprland-bind-key-match-r49.md` (MADO-R49-1, round 49; input-device plane, bind key "
              "matching) | How a `bind = MODS, KEY, ...` key field becomes a match for a key press on Hyprland "
              "0.56.2: the parse-time key forms, the +8 keycode, which keysym state is compared and the live "
              "`resolve_binds_by_sym` value, the exact modifier mask and its one relaxation, the double keysym "
              "lookup and its case rule, and the keycode/name/catch-all branch order, grounded on the pinned "
              "source and a read-only capture | rows S352-S354 |\n")


# ---------------------------------------------------------------- r46 paste
def r46_chain():
    blob = subprocess.run(["git", "-C", LANE, "show", BASE + ":corpus/knowledge/hyprland-input-devices-r46.md"],
                          capture_output=True, check=True).stdout.decode()
    out, inside = [], False
    for line in blob.splitlines():
        if line.startswith("## "):
            inside = line.strip() == "## The chain, step by step"
            if inside:
                out.append(line)
            continue
        if inside:
            out.append(line)
    while out and not out[-1].strip():
        out.pop()
    return "\n".join(out) + "\n"


def add_locators(text):
    """give every numbered step a locator into a round-49 pin so e cannot be the stopper."""
    out = []
    for line in text.splitlines():
        if re.match(r"^\d+\.\s", line):
            line = (line.rstrip() + " (`KEYCODE = e.keycode + 8;` at "
                    "Hyprland-KeybindManager.cpp:%d)"
                    % locate("Hyprland-KeybindManager.cpp", "KEYCODE = e.keycode + 8;"))
        out.append(line)
    return "\n".join(out) + "\n"


PARA = [("stores", "keeps"), ("stored", "kept"), ("keyboard", "input device"),
        ("keyboards", "input devices"), ("config", "configuration"), ("prints", "reports"),
        ("reads", "parses"), ("read", "parsed"), ("defaults", "built-in fallbacks"),
        ("default", "built-in fallback"), ("names", "labels"), ("name", "label"),
        ("dump", "snapshot"), ("compiles", "builds"), ("compile", "build"),
        ("line", "row"), ("file", "document"), ("values", "fields"), ("value", "field")]


def strip_citations(text):
    """remove the round-46 citations the pasted sentences carry, keeping the prose."""
    return re.sub(r"\s*\([^()]*?[A-Za-z0-9._-]+\.(?:cpp|md|hpp|h|txt|conf):\d+(?:-\d+)?[^()]*\)", "", text)


def held_prose(n=8):
    """verbatim long prose lines from the held round-46 entry, no citations attached."""
    blob = subprocess.run(["git", "-C", LANE, "show", BASE + ":corpus/knowledge/hyprland-input-devices-r46.md"],
                          capture_output=True, check=True).stdout.decode()
    out = []
    for line in blob.splitlines():
        t = line.strip()
        if len(t) < 60 or t.startswith("|") or t.startswith("#") or not t[0].isalpha():
            continue
        if re.search(r"[A-Za-z0-9._/-]+\.(?:cpp|md|hpp|h|txt):\d", t) or "knowledge/" in t:
            continue
        out.append(t)
        if len(out) >= n:
            break
    return ("## How the plane was measured (round 46)\n\n" + "\n\n".join(out) + "\n")


def paraphrase(text):
    for a, b in PARA:
        text = re.sub(r"\b%s\b" % a, b, text)
    return text


PREDICTED = {
    "00-base-golden": "MET", "01-do-nothing": "MISS", "02-stub-head-one-sentence": "MISS",
    "03-paste-r46-verbatim": "MISS", "04-paste-r46-paraphrased": "MET",
    "05-quote-forged-one-word": "MISS", "06-locator-off-by-one": "MISS",
    "07-steps-without-locators": "MISS", "08-branch-url-pin": "MISS",
    "09-digest-edited-row-file": "MET", "10-receipt-typed-by-hand": "MISS",
    "11-receipt-accurate-handtyped": "MET", "12-held-s319-reregistered": "MISS",
    "13-registry-row-unused": "MET", "14-step-locator-off-by-one": "MET",
    "15-held-prose-verbatim": "MISS", "16-row-duplicates-base-url": "MET",
    "17-row-used-by-existing-path": "MISS",
}


# ---------------------------------------------------------------- emission
def emit(name, entry=None, rows_text=None, rows_over=None, pins_over=None, receipt_mode="live",
         receipt_int=None, receipt_total=None, extra_rows="", lesson_extra=(), expect=None, note=""):
    d = os.path.join(CTL, name)
    os.makedirs(d, exist_ok=True)
    if entry is not None:
        open(os.path.join(d, "entry.md"), "w").write(entry)
    if rows_text is not None or rows_over or extra_rows:
        open(os.path.join(d, "rows-append.txt"), "w").write(
            (rows_text if rows_text is not None else rows(overrides=rows_over)) + extra_rows)
    for pin, blob in (pins_over or {}).items():
        pd = os.path.join(d, "pins")
        os.makedirs(pd, exist_ok=True)
        open(os.path.join(pd, pin), "wb").write(blob)
    if receipt_mode != "live" or receipt_int is not None or receipt_total is not None:
        open(os.path.join(d, "receipt.txt"), "w").write(
            receipt_text(int_value=receipt_int, total=receipt_total, mode=receipt_mode,
                         forms=false_forms() if name == "10-receipt-typed-by-hand" else None))
    if lesson_extra:
        open(os.path.join(d, "lesson-gate.md"), "w").write(lesson(lesson_extra))
    if expect:
        expect = dict(expect)
        expect["predicted"] = PREDICTED.get(name, "")
        open(os.path.join(d, "expect.json"), "w").write(json.dumps(expect, indent=1) + "\n")
    open(os.path.join(d, "README.md"), "w").write(
        "# control %s\n\n%s\n\nExpected: %s (%s)\n"
        % (name, note, expect["expect"], expect["clause"]))


def main():
    os.makedirs(CTL, exist_ok=True)
    base = base_entry()
    r46 = r46_chain()

    emit("00-base-golden", entry=base,
         expect={"clause": "none", "expect": "MET",
                 "why": "complete: head rows S352-S354, pinned rows, quotes at computed lines, six located steps, a "
                        "live receipt the entry repeats, Limits, held S303/S317/S319 cited"},
         note="The must-ADMIT anchor: a counter that rejects this fails the both-ways demonstration even if it "
              "catches every forgery below.")

    emit("01-do-nothing", entry=None,
         expect={"clause": "a", "expect": "MISS", "why": "no entry file at REV"},
         note="Do-nothing control: an empty commit on BASE. Clause a must report the entry absent.")

    emit("02-stub-head-one-sentence",
         entry=head() + ("## The match\n\nA bind's key field is resolved to a keysym before the modifier mask is "
                         "compared.\n"),
         expect={"clause": "e and f", "expect": "MISS", "why": "one sentence; no numbered step, no receipt cited"},
         note="Complete provenance head, one body sentence.")

    emit("03-paste-r46-verbatim", entry=sections(head(), add_locators(r46), observations(), live(), limits()),
         expect={"clause": "d (uncited pin); i does not see it", "expect": "MISS",
                 "why": "the pasted steps carry their own round-46 citations, which no round-49 head row cites, so d "
                        "refuses the quotes; i's duplicate-line test is defeated because every pasted line gained a "
                        "locator suffix"},
         note="The round-46 chain pasted under a round-49 head, plus new rows, new pins, a new receipt and the "
              "Limits. Old sentences, new locators.")

    emit("04-paste-r46-paraphrased",
         entry=sections(head(), add_locators(paraphrase(strip_citations(r46))), observations(), live(), limits()),
         expect={"clause": "i (observed ADMIT)", "expect": "MISS",
                 "why": "same old ground with the old citations stripped and content words swapped: d has nothing to "
                        "refuse and no line matches a held corpus line, so the draft admits old ground as new"},
         note="The same pasted ground with a fixed synonym map. If the draft admits this, i's novelty test is line "
              "overlap and a paraphrase defeats it.")

    forged = base.replace("const auto KBKEY      = xkb_keysym_from_name",
                          "const auto KBKEY      = xkb_keysym_from_name2", 1)
    if forged == base:
        raise SystemExit("05 replacement missed")
    emit("05-quote-forged-one-word", entry=forged,
         expect={"clause": "d", "expect": "MISS", "why": "the cited span is not in the pin: one identifier altered"},
         note="Every other byte is the golden entry; one word inside one cited quote is changed.")

    ln = locate("Hyprland-KeybindManager.cpp", "const auto         KEYCODE = e.keycode + 8;")
    off = base.replace("at Hyprland-KeybindManager.cpp:%d" % ln,
                       "at Hyprland-KeybindManager.cpp:%d" % (ln + 1), 1)
    if off == base:
        raise SystemExit("06 replacement missed")
    emit("06-locator-off-by-one", entry=off,
         expect={"clause": "d", "expect": "MISS",
                 "why": "the OBS locator for that quote is shifted one line down, and the quote is verbatim at %d"
                        % ln},
         note="A true quote cited one line below its true line.")

    stripped = "\n".join(
        (re.sub(r"`[^`]+` at Hyprland-KeybindManager\.cpp:\d+", "the pinned source", l)
         if re.match(r"^\d+\.\s", l) else l) for l in base.splitlines()) + "\n"
    if stripped == base:
        raise SystemExit("07 replacement missed")
    emit("07-steps-without-locators", entry=stripped,
         expect={"clause": "e", "expect": "MISS",
                 "why": "six numbered steps, none with a pin locator; the Observations quotes still resolve"},
         note="All six step locators replaced by prose.")

    brow = rows().replace("/%s/src/managers/KeybindManager.cpp" % COMMIT,
                          "/master/src/managers/KeybindManager.cpp", 1)
    emit("08-branch-url-pin", entry=base, rows_text=brow,
         expect={"clause": "c", "expect": "MISS", "why": "a row URL resolves through the master branch"},
         note="One row's URL ref is a branch name; the pin bytes and digest are unchanged.")

    kp = read("libxkbcommon-src-keysym.c")
    text = kp.decode().splitlines()
    target = next(i for i, l in enumerate(text) if i > 300 and l.lstrip().startswith("*"))
    text[target] = text[target] + " "
    mutated = ("\n".join(text) + ("\n" if kp.endswith(b"\n") else "")).encode()
    if mutated == kp:
        raise SystemExit("09 mutation produced identical bytes")
    emit("09-digest-edited-row-file", entry=base,
         pins_over={"libxkbcommon-src-keysym.c": mutated},
         rows_over={"S353": sha(mutated)},
         expect={"clause": "c (residual)", "expect": "MISS",
                 "why": "row digest == file digest, both differ from upstream; the draft never re-fetches"},
         note="The pin's bytes gain a trailing space on an uncited comment line and the row digest is recomputed to "
              "match. Row and file agree, upstream does not. c's declared residual.")

    false_entry = base.replace("192", "191").replace("142 named", "141 named")
    emit("10-receipt-typed-by-hand", entry=false_entry, receipt_mode="hand", receipt_total=191,
         rows_over={"S354": sha(receipt_text(total=191, mode="hand",
                                             forms=false_forms()).encode())},
         expect={"clause": "r", "expect": "MISS",
                 "why": "an internally consistent false count (191 = 141+42+6+2) with the true digest and resolve "
                        "value; f compares receipt to entry and passes, so only the replay can tell"},
         note="A hand-typed capture claiming binds=191 and 141 named, with the true digest and int 0 so every f "
              "check passes; the entry repeats the lie. Only r, which re-reads the host, can catch it.")

    emit("11-receipt-accurate-handtyped", entry=base, receipt_mode="hand",
         rows_over={"S354": sha(receipt_text(mode="hand").encode())},
         expect={"clause": "r", "expect": "MET",
                 "why": "the numbers are the host's; replay reproduces them, and authorship is not observable"},
         note="Same numbers, provenance says hand-typed. A replay clause reproduces them and must admit: this is "
              "the false-positive guard for r.")

    s355 = ("| S355 | Hyprland 0.56.2 keyboard base re-registered - what a keyboard stores and what happens when "
            "the keymap does not compile - %s | code | A | The stored rules and the us reset | IKeyboard.cpp:60-145, "
            "IKeyboard.cpp:101-116 @ commit %s, %d B sha256:%s; receipt %sHyprland-IKeyboard.cpp | The stored rules "
            "are the names asked for and a failed compile resets them to us | mined | 2026-10-27 | 90d | %s |\n"
            % (URLS["Hyprland-IKeyboard.cpp"], COMMIT, len(read("Hyprland-IKeyboard.cpp")),
               sha(read("Hyprland-IKeyboard.cpp")), FETCH, ENTRY))
    rereg = base.replace("stays held in S318 and S319", "stays held in S318 and S355")
    if rereg == base:
        raise SystemExit("12 replacement missed")
    emit("12-held-s319-reregistered", entry=rereg, extra_rows=s355,
         expect={"clause": "g", "expect": "MISS",
                 "why": "a new row carries held S319's (repo, ref, path) and the entry no longer cites S319"},
         note="Held S319's URL and bytes re-registered as S355, which the entry then cites instead.")

    unused_pin = "control-unused-row.txt"
    unused_blob = ("# a row opened this round that no claim uses\n"
                   + "".join("binding form %d observed in the census\n" % i for i in range(1, 19))).encode()
    def unused_row(sid, used_by):
        return ("| %s | bind form census note - a side note on the key forms - %s%s | own-work | A | The side note "
                "| %s:1-19 @ access 2026-10-27, %d B sha256:%s; receipt %s%s | A census note that supports no claim "
                "| mined | 2026-10-27 | 90d | %s |\n"
                % (sid, "", "", unused_pin, len(unused_blob), sha(unused_blob), FETCH, unused_pin, used_by))

    gate13 = ["- **S356 admit**, tier A, own-work. Source opened this round: `%s`; access date 2026-10-27. "
              "A side note." % unused_pin]
    emit("13-registry-row-unused", entry=base,
         extra_rows=unused_row("S356", "corpus/knowledge/hyprland-bind-key-match-r49-draft-notes.md"),
         pins_over={unused_pin: unused_blob}, lesson_extra=gate13,
         expect={"clause": "i (row_unused)", "expect": "MISS",
                 "why": "the new row's used-by names a path that does not exist at REV, so i's used-by check must "
                        "refuse it"},
         note="A new row that no claim uses: used-by names a file that is not in the tree. Under the revised i this "
              "must miss at row_unused. (The earlier version of this control named the round-46 entry, an existing "
              "path, and was admitted - see 17.)")

    emit("17-row-used-by-existing-path", entry=base,
         extra_rows=unused_row("S357", "corpus/knowledge/hyprland-input-devices-r46.md"),
         pins_over={unused_pin: unused_blob},
         lesson_extra=["- **S357 admit**, tier A, own-work. Source opened this round: `%s`; access date 2026-10-27. "
                       "A side note." % unused_pin],
         expect={"clause": "i (row_used_by_not_new)", "expect": "MISS",
                 "why": "the named consumer must exist at REV and be absent at BASE; a row whose only consumer is an "
                        "already-held document must be refused"},
         note="A new row whose only consumer is an already-held document. This was the boundary of the previous "
              "used-by rule (admitted there, at draft 12200189/e6df8a19); the a2e91724 rule refuses it. Kept in the "
              "set because it pins which rule the freeze is buying.")

    stepoff = base.replace("`KEYCODE = e.keycode + 8;` at Hyprland-KeybindManager.cpp:%d" % ln,
                           "`KEYCODE = e.keycode + 8;` at Hyprland-KeybindManager.cpp:%d" % (ln + 1), 1)
    if stepoff == base:
        raise SystemExit("14 replacement missed")
    emit("14-step-locator-off-by-one", entry=stepoff,
         expect={"clause": "d and e", "expect": "MISS",
                 "why": "step 1's quote is verbatim at 367 but cited at 368: the revised e now wants a quote d "
                        "verifies, and d refuses a quote absent from the stated line"},
         note="Step 1's quote locator shifted one line down (the quote still sits inside the pin). Under the "
              "revised e this must miss; under the previous e it passed, which is why the control was kept.")

    emit("15-held-prose-verbatim", entry=sections(head(), steps(), held_prose(), observations(), live(), limits()),
         expect={"clause": "i (dup)", "expect": "MISS",
                 "why": "eight long lines are byte-identical to the held round-46 entry and carry no citations, so d "
                        "is silent and i's duplicate-line test is the only stopper"},
         note="Byte-identical reuse of held prose with no citation attached. This is the control that shows i's "
              "duplicate-line test does fire, which bounds control 04: one word changed per line and it is gone.")

    lm_url = ("https://raw.githubusercontent.com/hyprwm/Hyprland/%s/src/config/legacy/ConfigManager.cpp" % COMMIT)
    lm = read("Hyprland-legacy-ConfigManager.cpp")
    s357 = ("| S357 | Hyprland 0.56.2 hyprlang bind parser - the key forms a bare number, code:N, catchall and the "
            "verbatim name - %s | code | A | Which key strings become keycodes at parse time | "
            "legacy-ConfigManager.cpp:1481-1489 @ commit %s, %d B sha256:%s; receipt %sHyprland-legacy-ConfigManager.cpp"
            " | A bare number and code:N are keycodes, catchall is a flag, every other string is kept verbatim | mined "
            "| 2026-10-27 | 90d | %s |\n" % (lm_url, COMMIT, len(lm), sha(lm), FETCH, ENTRY))
    emit("16-row-duplicates-base-url", entry=base, extra_rows=s357,
         pins_over={"Hyprland-legacy-ConfigManager.cpp": lm},
         lesson_extra=["- **S357 admit**, tier A, code. URL: `%s`; opened 2026-10-27; quote "
                       "`SParsedKey parseKey(const std::string& key) {` "
                       "(`fetch/Hyprland-legacy-ConfigManager.cpp:%d`). The bind parser."
                       % (lm_url, locate("Hyprland-legacy-ConfigManager.cpp",
                                          "SParsedKey parseKey(const std::string& key) {"))],
         expect={"clause": "g (narrowed by design)", "expect": "MET",
                 "why": "the current g docstring allows reopening another held source with a new scope "
                        "(rows S162/S303/S317 precedent), so this row must be admitted"},
         note="A new, correctly pinned row for a file the registry already holds at the same commit (S303, S317 "
              "carry src/config/legacy/ConfigManager.cpp). c and f pass; g's base_urls loop must refuse it. This is "
              "the hazard the real entry hits if it opens a row for the bind parser instead of citing S303/S317.")

    open(os.path.join(CTL, "00-base-golden", "rows.txt"), "w").write(rows())
    open(os.path.join(CTL, "00-base-golden", "receipt.txt"), "w").write(receipt_text())
    open(os.path.join(CTL, "00-base-golden", "lesson-gate.md"), "w").write(lesson())
    open(os.path.join(CTL, "00-base-golden", "readme-row.txt"), "w").write(README_ROW)
    print("built", len(os.listdir(CTL)), "controls")
    print("entry bytes", len(base.encode()), "lines", base.count("\n"))
    print("receipt bytes", receipt_size(), "lines", receipt_lines(), "sha", receipt_sha()[:16])


if __name__ == "__main__":
    main()
