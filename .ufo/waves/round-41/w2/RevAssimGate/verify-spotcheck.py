#!/usr/bin/env python3
"""Verify quotes and id-guard numbers for RevAssimGate."""
import hashlib
import html
import os
import re
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
SHOKUKNOW = "/home/vgpnk/Projects/shokuknow"
BASE = "ab2bfaab661c846d1de9d58c01651cd156a13949"
DATA = "07f2641696b5ac73de1404ea737a9f27e9819aa1"
SEAT_DIR = os.path.join(LANE, ".ufo/waves/round-41/w2/RevAssimGate")
ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}


def git_show(rev, path):
    return subprocess.check_output(
        ["git", "-C", LANE, "show", f"{rev}:{path}"], env=ENV
    )


def looks_html(blob):
    return re.search(rb"<(!doctype|html|body|div|p)\b", blob[:4096], re.I) is not None


def norm_receipt(blob):
    text = blob.decode("utf-8", "replace")
    if looks_html(blob):
        text = re.sub(r"<script.*?</script>|<style.*?</style>", " ", text, flags=re.S | re.I)
        text = re.sub(r"<[^>]+>", " ", text)
        return re.sub(r"\s+", " ", html.unescape(text)).strip()
    return re.sub(r"\s+", " ", text).strip()


def main():
    failures = 0

    # 1. Verify id-guard numbers at BASE and DATA
    row_re = re.compile(r"^ {0,3}\|[ \t]*S[0-9]{3,}", re.M)
    id_re = re.compile(r"S[0-9]+")

    src_base_bytes = git_show(BASE, "corpus/SOURCES.md")
    src_data_bytes = git_show(DATA, "corpus/SOURCES.md")
    with open(os.path.join(SHOKUKNOW, "merge/mado/SOURCES.append.md"), "rb") as f:
        staged_bytes = f.read()

    assert hashlib.sha256(src_base_bytes).hexdigest() == "51a65515231b0a180f88c4fa1bc71482afa5f3eaeede4bdfbe6c4869493812ce"
    assert hashlib.sha256(staged_bytes).hexdigest() == "684efe8c23b8b64d789187dab61bfbf7c0dcef4f0428e447c94d7be4e73a27c0"

    reg_base = sorted(id_re.search(m).group(0) for m in row_re.findall(src_base_bytes.decode()))
    reg_data = sorted(id_re.search(m).group(0) for m in row_re.findall(src_data_bytes.decode()))
    staged = sorted(id_re.search(m).group(0) for m in row_re.findall(staged_bytes.decode()))

    coll_base = sorted(set(reg_base) & set(staged))
    coll_data = sorted(set(reg_data) & set(staged))

    assert (len(reg_base), len(staged), len(coll_base)) == (219, 147, 27), (
        len(reg_base), len(staged), len(coll_base)
    )
    assert (len(reg_data), len(staged), len(coll_data)) == (226, 147, 34), (
        len(reg_data), len(staged), len(coll_data)
    )
    print(f"ID-GUARD BASE: reg={len(reg_base)} staged={len(staged)} collisions={len(coll_base)} -> OK")
    print(f"ID-GUARD DATA: reg={len(reg_data)} staged={len(staged)} collisions={len(coll_data)} -> OK (new: {sorted(set(coll_data) - set(coll_base))})")

    # 2. Verify quotes in spotcheck.md and RevAssimGate.md
    receipt_blobs = {
        "focus-grab-v1.xml": git_show(DATA, ".ufo/waves/round-41/fetch/focus-grab-v1.xml"),
        "Hyprland-FocusGrab.cpp": git_show(DATA, ".ufo/waves/round-41/fetch/Hyprland-FocusGrab.cpp"),
        "quickshell-grab.cpp": git_show(DATA, ".ufo/waves/round-41/fetch/quickshell-grab.cpp"),
        "xdph-PortalManager.cpp": git_show(DATA, ".ufo/waves/round-41/fetch/xdph-PortalManager.cpp"),
        "issue-565.html": git_show(DATA, ".ufo/waves/round-41/fetch/issue-565.html"),
        "protocols-README.md": git_show(DATA, ".ufo/waves/round-41/fetch/protocols-README.md"),
        "xdph-journal.txt": git_show(DATA, ".ufo/waves/round-41/fetch/xdph-journal.txt"),
        "xdph-installed-version.txt": git_show(DATA, ".ufo/waves/round-41/fetch/xdph-installed-version.txt"),
        "input-capture-v1.xml": git_show(DATA, ".ufo/waves/round-41/fetch/input-capture-v1.xml"),
        "entry": git_show(DATA, "corpus/knowledge/hyprland-focus-grab-r41.md"),
        "lesson": git_show(DATA, "corpus/lessons/round-41.md"),
        "SOURCES.md": src_data_bytes,
        "PROVINCE.md": git_show(DATA, "PROVINCE.md"),
        "id-guard.md": open(os.path.join(LANE, ".ufo/waves/round-41/assimilation/id-guard.md"), "rb").read(),
        "staged-r14": open(os.path.join(SHOKUKNOW, "merge/mado/knowledge/corpus/knowledge/focus-grab-protocol-live-on-host-r14.md"), "rb").read(),
        "staged-r29": open(os.path.join(SHOKUKNOW, "merge/mado/knowledge/corpus/knowledge/privileged-client-surface-r29.md"), "rb").read(),
        "staged-r28": open(os.path.join(SHOKUKNOW, "merge/mado/knowledge/corpus/knowledge/focus-control-surfaces-r28.md"), "rb").read(),
        "staged-append": staged_bytes,
        "round14-adv": open(os.path.join(SHOKUKNOW, "lanes/mado/round14/fetch/host-focus-grab-portal-advertisement.txt"), "rb").read(),
    }
    normed = {k: norm_receipt(v) for k, v in receipt_blobs.items()}
    raw_text = {k: re.sub(r"\s+", " ", v.decode("utf-8", "replace")).strip() for k, v in receipt_blobs.items()}

    checks = [
        # (target_key, quote)
        ("lesson", "ADMIT merge/mado/knowledge/corpus/knowledge/focus-grab-protocol-live-on-host-r14.md as corpus/knowledge/hyprland-focus-grab-r41.md"),
        ("lesson", "REFUSE merge/mado/knowledge/corpus/knowledge/privileged-client-surface-r29.md reason=generic Wayland analysis, one truncated quote, no measurement and no host state"),
        ("lesson", "REFUSE merge/mado/knowledge/corpus/knowledge/focus-control-surfaces-r28.md reason=section 3 rests on a localized (Japanese) documentation channel, outside PROVINCE.md"),
        ("lesson", "re-grounded this round as C2 with lane ids S283–S290"),
        ("lesson", "theown-work") if False else ("lesson", "the own-work journal S289, `input-capture-v1.xml` S290."),
        ("lesson", "S290 (`input-capture-v1.xml`) is **not** cited by the entry and has no row."),
        ("focus-grab-v1.xml", "This interface restricts input focus to a specified whitelist of surfaces"),
        ("Hyprland-FocusGrab.cpp", "m_grab->m_keyboard = true;"),
        ("quickshell-grab.cpp", "the protocol will always send cleared() when the grab is deactivated,"),
        ("xdph-PortalManager.cpp", "Got interface: {} (ver {})"),
        ("issue-565.html", "Tried to set workspace silent rule to a nofocus window!"),
        ("protocols-README.md", "for grabbing input focus, primarily for complex context menus"),
        ("xdph-journal.txt", "Got interface: hyprland_focus_grab_manager_v1 (ver 1)"),
        ("xdph-installed-version.txt", "%NAME% xdg-desktop-portal-hyprland %VERSION% 1.4.1-2"),
        ("entry", "and what follows is a fixed set of ten named branches"),
        ("SOURCES.md", "and the portal binds nine named interfaces none of which is the focus-grab manager"),
        ("SOURCES.md", "The two interfaces, four requests and one event that define a focus grab"),
        ("entry", "What can a client ask for? | S283: two interfaces, five requests, one event (§1)"),
        ("entry", "logs \"called with no committed surfaces. This should never happen.\" - the compositor treats"),
        ("staged-r14", "advertisement lines naming the focus-grab manager: 2"),
        ("round14-adv", "advertisement lines naming the focus-grab manager: 2"),
        ("staged-r29", "But there is also `WAYLAND_SOCKET`, which"),
        ("staged-r29", "A focus-grab client is therefore a privileged client"),
        ("staged-r28", "windowrule = match:class ^(.*jetbrains.*)$ title:^(win.*)$, no_focus on"),
        ("staged-r28", "The round-2 paper (wave-2 row S199) measured focus hijacking on X11"),
        ("PROVINCE.md", "documentation written in a localized channel — is outside the province"),
        ("id-guard.md", "Result: **reg=219 staged=147 coll=27**"),
    ]

    for key, q in checks:
        nq = re.sub(r"\s+", " ", q).strip()
        words = len(nq.split())
        in_norm = nq in normed[key] or nq in raw_text[key]
        status = "OK" if (words <= 25 and in_norm) else "FAIL"
        if status == "FAIL":
            failures += 1
        print(f"QUOTE [{status}] key={key} words={words}: {nq[:60]}...")

    # Also scan spotcheck.md and RevAssimGate.md for any QUOTE-CHECK lines if present
    for md_path in [
        os.path.join(SEAT_DIR, "spotcheck.md"),
        os.path.join(LANE, ".ufo/waves/round-41/w2/RevAssimGate.md"),
    ]:
        if os.path.exists(md_path):
            with open(md_path) as f:
                text = f.read()
            for m in re.finditer(r'QUOTE_VERIFIED\[(\S+)\]: "([^"]+)"', text):
                k, q = m.group(1), m.group(2)
                nq = re.sub(r"\s+", " ", q).strip()
                w = len(nq.split())
                ok = w <= 25 and (nq in normed.get(k, "") or nq in raw_text.get(k, ""))
                if not ok:
                    failures += 1
                    print(f"DOC QUOTE FAIL in {os.path.basename(md_path)} [{k}] words={w}: {nq}")

    print(f"SUMMARY: checked={len(checks)} failures={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
