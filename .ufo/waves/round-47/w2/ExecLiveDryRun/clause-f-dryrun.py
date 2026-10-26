#!/usr/bin/env python3
"""ExecLiveDryRun — clause-f dry-run against the FROZEN C2 counter (imported, not re-implemented).

Builds a throwaway git fixture under --work, plants an entry (real w1 entry.md with the
<LIVE:*> placeholders substituted), a receipt and the live capture, then calls the frozen
counter's own clause_f() for each shape variant. Nothing in the lane is written.
"""
import importlib.util
import os
import shutil
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
COUNTER = LANE + "/quality/counters/c2-r47-terminal-entry.py"
ENTRY_SRC = LANE + "/.ufo/waves/round-47/w1/ScrEntry/entry.md"
CAPTURE = LANE + "/.ufo/waves/round-47/w2/ExecLiveDryRun/capture-r47.txt"
RECEIPT = ".ufo/waves/round-47/receipts/live-receipt-r47.txt"
OBSERVED = ".ufo/waves/round-47/receipts/live-capture-r47.txt"
SHA = "89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac"
CAP_SHA = "9eb0a761e78db8b69a386536e2332cb4cb86275ca83c2eeb43a8721edae45cbc"


def load_counter():
    spec = importlib.util.spec_from_file_location("c2frozen", COUNTER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def git(repo, *args):
    p = subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True)
    if p.returncode != 0:
        raise SystemExit("git %s failed: %s" % (args, p.stderr.strip()))
    return p.stdout.strip()


def subst(entry_text):
    cap = open(CAPTURE, encoding="utf-8").read().split("\n")
    live = {
        "<LIVE:print-id>": cap[0],
        "<LIVE:print-path>": cap[1],
        "<LIVE:print-cmd>": cap[2],
        "<LIVE:print-path-class>": "user override (~/.local/share/applications)",
        "<LIVE:verdict>": "AGREE",
        "<LIVE:selected-list-locator>": "~/.config/xdg-terminals.list:3",
        "<LIVE:cache-file>": "xdg-terminal-exec (188 B, in the scratch cache dir)",
        "<LIVE:live-receipt>": "live-receipt-r47.txt",
    }
    out = entry_text
    for k, v in live.items():
        out = out.replace(k, v)
    return out


def make_entry(variant, base_text):
    """Return entry text for a variant."""
    if variant == "V1-mechanical":
        return base_text
    if variant == "V2-states-id-and-path":
        # the ground line cites terminal-route-r17.md:144-145; make it state id + tilde path
        marker = "answered by the live receipt `.ufo/waves/round-47/receipts/live-receipt-r47.txt`)"
        if marker not in base_text:
            raise SystemExit("marker not found in ground line")
        return base_text.replace(
            marker,
            marker[:-1] + "; the resolver picks `Alacritty.desktop` at "
            "`~/.local/share/applications/Alacritty.desktop` there)",
        )
    if variant == "V4-absolute-path":
        return make_entry("V2-states-id-and-path", base_text).replace(
            "`~/.local/share/applications/Alacritty.desktop`",
            "`/home/vgpnk/.local/share/applications/Alacritty.desktop`")
    if variant == "V5-subdir":
        return make_entry("V2-states-id-and-path", base_text).replace(
            "receipts/live-receipt-r47.txt", "receipts/c2/live-receipt-r47.txt")
    if variant == "V3-wrong-id":
        # same shape as V2 but the stated id/path contradict the capture (hostile entry)
        marker = "answered by the live receipt `.ufo/waves/round-47/receipts/live-receipt-r47.txt`)"
        return base_text.replace(
            marker,
            marker[:-1] + "; the resolver picks `kitty.desktop` at "
            "`~/.local/share/applications/kitty.desktop` there)",
        )
    raise SystemExit("unknown entry variant %s" % variant)


def receipt_text(kind):
    good = (
        "LIVE RECEIPT - round 47 C2 clause f - terminal selection on this host\n"
        "captured 2026-10-26, read-only: print modes only, never a launch\n"
        "resolver: /usr/bin/xdg-terminal-exec\n"
        "resolver_sha256=%s\n"
        "command: xdg-terminal-exec --print-id --print-path --print-cmd\n"
        "observed=%s\n"
        "capture_sha256=%s (stdout incl. trailing newline)\n"
        "XDG_CURRENT_DESKTOP=Hyprland\n"
        "XDG_CONFIG_HOME=/home/vgpnk/.config\n"
        "XDG_CONFIG_DIRS=/etc/xdg\n"
        "XDG_DATA_HOME=/home/vgpnk/.local/share\n"
        "XDG_DATA_DIRS=/usr/local/share:/usr/share\n"
        "XDG_CACHE_HOME=<scratch>/cache-cold (fresh, so the capture is a cold-cache run)\n"
        "explain: MADO_TERM: selected=Alacritty.desktop "
        "path=/home/vgpnk/.local/share/applications/Alacritty.desktop cmd=alacritty "
        "cache=present verdict=AGREE (rc=0)\n" % (SHA, OBSERVED, CAP_SHA)
    )
    if kind == "good":
        return good
    if kind == "colon":
        return good.replace("observed=" + OBSERVED, "observed: " + OBSERVED)
    if kind == "short":
        return "LIVE RECEIPT r47\nresolver_sha256=%s\nobserved=%s\nXDG_A=1\nXDG_B=2\nXDG_C=3\n" % (
            SHA, OBSERVED)
    if kind == "env2":
        return good.replace("XDG_CONFIG_DIRS=/etc/xdg\n", "").replace(
            "XDG_DATA_DIRS=/usr/local/share:/usr/share\n", "").replace(
            "XDG_DATA_HOME=/home/vgpnk/.local/share\n", "").replace(
            "XDG_CONFIG_HOME=/home/vgpnk/.config\n", "")
    if kind == "relative":
        return good.replace("observed=" + OBSERVED, "observed=receipts/live-capture-r47.txt")
    if kind == "badsha":
        return good.replace("resolver_sha256=" + SHA, "resolver_sha256=" + SHA[:16])
    if kind == "gnome":
        return good.replace("XDG_CURRENT_DESKTOP=Hyprland", "XDG_CURRENT_DESKTOP=GNOME")
    raise SystemExit("unknown receipt kind %s" % kind)


def main():
    work = sys.argv[1]
    mode = sys.argv[2] if len(sys.argv) > 2 else "matrix"
    if mode == "emit":
        sys.stdout.write(receipt_text("good"))
        return
    c2 = load_counter()
    repo = os.path.join(work, "f")
    shutil.rmtree(repo, ignore_errors=True)
    os.makedirs(repo)
    git(repo, "init", "-q")
    top = git(repo, "rev-parse", "--show-toplevel")
    assert os.path.realpath(top) == os.path.realpath(repo), "fixture toplevel escaped: %s" % top
    git(repo, "-c", "user.name=seat", "-c", "user.email=seat@scratch.invalid",
        "commit", "-q", "--allow-empty", "-m", "base")
    base = git(repo, "rev-parse", "HEAD")

    base_text = subst(open(ENTRY_SRC, encoding="utf-8").read())
    cap = open(CAPTURE, "rb").read()

    def put(rel, data):
        p = os.path.join(repo, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "wb") as fh:
            fh.write(data if isinstance(data, bytes) else data.encode())

    def commit(msg):
        git(repo, "add", "-A")
        git(repo, "-c", "user.name=seat", "-c", "user.email=seat@scratch.invalid",
            "commit", "-q", "-m", msg)
        return git(repo, "rev-parse", "HEAD")

    RECEIPT_SUB = ".ufo/waves/round-47/receipts/c2/live-receipt-r47.txt"
    cases = [
        {"ev": "V1-mechanical", "rk": "good", "ck": "CAP-ok"},
        {"ev": "V2-states-id-and-path", "rk": "good", "ck": "CAP-ok"},
        {"ev": "V2-states-id-and-path", "rk": "colon", "ck": "CAP-ok"},
        {"ev": "V2-states-id-and-path", "rk": "short", "ck": "CAP-ok"},
        {"ev": "V2-states-id-and-path", "rk": "env2", "ck": "CAP-ok"},
        {"ev": "V2-states-id-and-path", "rk": "relative", "ck": "CAP-ok"},
        {"ev": "V3-wrong-id", "rk": "good", "ck": "CAP-ok"},
    ]
    if mode == "extra":
        cases += [
            {"ev": "V2-states-id-and-path", "rk": "badsha", "ck": "CAP-ok"},
            {"ev": "V2-states-id-and-path", "rk": "good", "ck": "CAP-action-id"},
        ]
    if mode == "gaps":
        cases += [
            {"ev": "V2-states-id-and-path", "rk": "good", "ck": "CAP-ok"},
            {"ev": "V2-states-id-and-path", "rk": "gnome", "ck": "CAP-ok"},
            {"ev": "V2-states-id-and-path", "rk": "good", "ck": "CAP-dir4"},
            {"ev": "V4-absolute-path", "rk": "good", "ck": "CAP-ok"},
            {"ev": "V5-subdir", "rk": "good", "ck": "CAP-ok", "rpath": RECEIPT_SUB},
        ]
    for i, case in enumerate(cases):
        ev, rk, ck = case["ev"], case["rk"], case["ck"]
        rpath = case.get("rpath", RECEIPT)
        for rel in (RECEIPT, RECEIPT_SUB, OBSERVED,
                    "corpus/knowledge/xdg-terminal-selection-r47.md"):
            p = os.path.join(repo, rel)
            if os.path.exists(p):
                os.remove(p)
        put("corpus/knowledge/xdg-terminal-selection-r47.md", make_entry(ev, base_text))
        put(rpath, receipt_text(rk))
        if ck == "CAP-ok":
            put(OBSERVED, cap)
        elif ck == "CAP-dir4":
            put(OBSERVED, cap + b"--working-directory=/tmp\n")
        else:  # an id printed with an action never ends in .desktop
            put(OBSERVED, cap.replace(b"Alacritty.desktop\n", b"Alacritty.desktop:New\n", 1))
        rev = commit("case %d" % i)
        lines = c2.unfenced(open(os.path.join(
            repo, "corpus/knowledge/xdg-terminal-selection-r47.md"), encoding="utf-8").read())
        print("=" * 78)
        print("CASE %d entry=%s receipt=%s capture=%s rpath=%s" % (i, ev, rk, ck, rpath))
        ok = c2.clause_f(repo, rev, base, lines, "dryrun")
        print("clause_f=%s" % ("PASS" if ok else "FAIL"))


if __name__ == "__main__":
    main()
