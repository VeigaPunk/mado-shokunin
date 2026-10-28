#!/usr/bin/env python3
"""C3 do-nothing variants + seat mirror of registration §C3 controls (C3-CTL-1..6), run against c3check.py.
Usage: ctl_c3.py REPO BASE_REV WORK [variant]. Commits only in the scratch REPO; resets it to BASE_REV after each."""
import os, subprocess, sys

repo, base_rev, work = sys.argv[1:4]
VARIANT = sys.argv[4] if len(sys.argv) > 4 else "stuffed"
HERE = os.path.dirname(os.path.abspath(__file__))
CHK = os.path.join(HERE, "c3check.py")
ENTRY = "corpus/knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md"
README = "corpus/README.md"
P19 = ("`Actions::pass` sends modifier state before its delivery branch; it sends a PRESSED keyboard key "
       "only when `m_passPressed == 1` and the key is not a mouse button.")
# Do-nothing clause: keeps the false P19 sentence and appends keywords only. Pin 1566-1569 sends PRESSED in the else arm.
STUFF = (" The `== 0` arm sends a RELEASED key; `otherwise` (any other value) sends no key, and the `else` arm "
         "is not a PRESSED path.")
Q = [("Q01", 1554, "g_pSeatManager->sendKeyboardMods(modMask, 0, 0, 0);"),
     ("Q02", 1556, "if (S.m_passPressed == 1) {"),
     ("Q03", 1558, "g_pSeatManager->sendKeyboardKey(S.m_timeLastMs, key - 8, WL_KEYBOARD_KEY_STATE_PRESSED);"),
     ("Q04", 1560, "g_pSeatManager->sendPointerButton(S.m_timeLastMs, key, WL_POINTER_BUTTON_STATE_PRESSED);"),
     ("Q05", 1561, "} else if (S.m_passPressed == 0) {"),
     ("Q06", 1563, "g_pSeatManager->sendKeyboardKey(S.m_timeLastMs, key - 8, WL_KEYBOARD_KEY_STATE_RELEASED);"),
     ("Q07", 1565, "g_pSeatManager->sendPointerButton(S.m_timeLastMs, key, WL_POINTER_BUTTON_STATE_RELEASED);"),
     ("Q08", 1566, "} else {"),
     ("Q09", 1568, "g_pSeatManager->sendKeyboardKey(S.m_timeLastMs, key - 8, WL_KEYBOARD_KEY_STATE_PRESSED);"),
     ("Q10", 1569, "g_pSeatManager->sendKeyboardKey(S.m_timeLastMs, key - 8, WL_KEYBOARD_KEY_STATE_RELEASED);"),
     ("Q11", 1571, "g_pSeatManager->sendPointerButton(S.m_timeLastMs, key, WL_POINTER_BUTTON_STATE_PRESSED);"),
     ("Q12", 1572, "g_pSeatManager->sendPointerButton(S.m_timeLastMs, key, WL_POINTER_BUTTON_STATE_RELEASED);"),
     ("Q13", 1576, "g_pSeatManager->sendKeyboardMods(0, 0, 0, 0);")]
README_OK = "| `knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md` (round 55 correction) | P23 supersedes P19 |"
README_NOP23 = "| `knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md` (round 55 correction) | supersedes P19 |"


def g(*a):
    return subprocess.run(["git", "-C", repo, *a], check=True, capture_output=True, text=True).stdout


def base_text():
    return subprocess.run(["git", "-C", repo, "cat-file", "-p", f"{base_rev}:{ENTRY}"],
                          capture_output=True).stdout.decode("utf-8")


def block(heading, prop):
    out = [""]
    if heading:
        out += ["## Correction (round 55)", ""]
    out += ["| ID | Supersedes | Proposition | Source row | Pin:anchor | Quote (≤25 words) | Support |",
            "|---|---|---|---|---|---|---|",
            f"| P23 | P19 | {prop} | S371 | Hyprland-ConfigActions.cpp:1554-1576 | … | direct |", ""]
    out += [f"| {qid} | Hyprland-ConfigActions.cpp:{line} | `{q}` |" for qid, line, q in Q]
    return "\n".join(out) + "\n"


def tree_of(variant):
    """Return (errata_text, readme_text_or_None) for a variant name."""
    base = base_text()
    if variant == "plain":
        return base + block(True, P19), README_OK
    if variant == "stuffed":
        return base + block(True, P19 + STUFF), README_OK
    if variant == "stuffed-nohead":
        return base + block(False, P19 + STUFF), README_OK
    raise SystemExit(f"unknown variant {variant}")


def write_pair(errata, readme_line):
    open(os.path.join(repo, ENTRY), "w", encoding="utf-8").write(errata)
    if readme_line is not None:
        open(os.path.join(repo, README), "a", encoding="utf-8").write(readme_line + "\n")


def commit(msg):
    g("add", "-A")
    subprocess.run(["git", "-C", repo, "-c", "user.name=ctl", "-c", "user.email=ctl@ctl", "commit", "-qm", msg,
                    "--allow-empty"], check=True, capture_output=True)
    return g("rev-parse", "HEAD").strip()


def reset():
    g("reset", "-q", "--hard", base_rev)


def check(rev):
    p = subprocess.run([sys.executable, "-I", CHK, "--repo", repo, "--rev", rev, "--base-rev", base_rev,
                        "--work", work], capture_output=True, text=True)
    return p.stdout.strip(), p.returncode


def mutate_row(text, rid, old, new):
    lines = text.split("\n")
    idx = [i for i, l in enumerate(lines) if l.startswith(f"| {rid} |")]
    assert len(idx) == 1 and old in lines[idx[0]], (rid, old)
    lines[idx[0]] = lines[idx[0]].replace(old, new, 1)
    return "\n".join(lines)


def main():
    reset()
    errata, rd = tree_of(VARIANT)
    write_pair(errata, rd)
    good = commit(f"c3 do-nothing {VARIANT}")
    out, rc = check(good)
    print(f"[{VARIANT}] good: {out} rc={rc}")
    if VARIANT != "stuffed":
        reset()
        return
    base = base_text()
    specs = [
        ("C3-CTL-1 absent", (base, ""), ["rows", "p23"], "absent: prefix clean, rows+p23 missed"),
        ("C3-CTL-2 rewritten-prefix", (errata.replace("keyboard key only when", "keyboard key only whEn", 1), rd), ["prefix"], ""),
        ("C3-CTL-3 altered-quote", (mutate_row(errata, "Q09", "WL_KEYBOARD_KEY_STATE_PRESSED", "WL_KEYBOARD_KEY_STATE_PRESSEd"), rd), ["rows:Q09"], ""),
        ("C3-CTL-4 old-arm-only", ("\n".join(l for l in errata.split("\n") if not any(l.startswith(f"| Q{n:02d} |") for n in range(8, 13))), rd), ["rows:Q08"], ""),
        ("C3-CTL-5 old-wording", (errata.replace(P19 + STUFF, P19, 1), rd), ["p23"], ""),
        ("C3-CTL-6 readme-missing", (errata, README_NOP23), ["readme"], ""),
    ]
    k = 0
    for name, (et, rl), want, _ in specs:
        reset()
        write_pair(et, rl)
        r = commit(name)
        out, rc = check(r)
        legs = out.split("missed=")[-1] if "missed=" in out else ""
        hit = rc == 1 and all(any(w in l for l in legs.split(",")) for w in want)
        k += hit
        print(f"  {name}: {out.split('missed=')[-1] if 'missed=' in out else out} -> {'named-leg-hit' if hit else 'MISS'}")
    reset()
    print(f"MADO_R55_CONTROLS: claim=c3 good={'ok' if rc_good_ok(good) else 'bad'} controls={k}/6 "
          f"verdict={'OK' if k == 6 and rc_good_ok(good) else 'FAIL'}")


def rc_good_ok(rev):
    out, rc = check(rev)
    return rc == 0 and "verdict=TARGET_MET" in out


if __name__ == "__main__":
    main()
