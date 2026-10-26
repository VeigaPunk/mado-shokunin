#!/usr/bin/env python3
"""verify-quotes.py — verify quotes cited by seat ConnSiblingClosure.

Rules:
- Quotes <= 25 words
- Located with file and line range
- Normalized whitespace substring match against source file
"""

import os
import sys

QUOTES = [
    {
        "file": "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-41/fetch/focus-grab-v1.xml",
        "lines": "34-36",
        "text": "This protocol allows clients to limit input focus to a specific set of surfaces and receive a notification when the limiter is removed as",
    },
    {
        "file": "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-41/fetch/focus-grab-v1.xml",
        "lines": "62-64",
        "text": "This interface restricts input focus to a specified whitelist of surfaces as long as the focus grab object exists and has at least one comitted",
    },
    {
        "file": "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-41/fetch/xdph-PortalManager.cpp",
        "lines": "88",
        "text": 'Debug::log(LOG, " | Got interface: {} (ver {})", INTERFACE, version);',
    },
    {
        "file": "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-41/fetch/xdph-journal.txt",
        "lines": "117",
        "text": "2026-10-25T13:36:24-03:00 plazir27 xdg-desktop-portal-hyprland[1952]: [LOG]  | Got interface: hyprland_focus_grab_manager_v1 (ver 1)",
    },
    {
        "file": "/home/vgpnk/Projects/shokunin/kasegi-shokunin/PROVINCE.md",
        "lines": "3",
        "text": "**Domain:** bounty & security research — scopes ~/Projects/bounties, program rules, claim packages",
    },
    {
        "file": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/PROVINCE.md",
        "lines": "3-4",
        "text": "**Domain:** host operability & system repair (繕, mending) — the OS substrate itself: package state, systemd, drivers/firmware, boot health.",
    },
    {
        "file": "/home/vgpnk/Projects/shokunin/mori-shokunin/PROVINCE.md",
        "lines": "3-4",
        "text": "**Domain:** fleet & host observability (森) — whether the fleet, its waves and its host are alive and progressing.",
    },
    {
        "file": "/home/vgpnk/Projects/shokunin/mado-shokunin/PROVINCE.md",
        "lines": "3-4",
        "text": "**Domain:** desktop & compositor craft — the Hyprland/waybar/walker configuration plane and display behavior on this host.",
    },
    {
        "file": "/home/vgpnk/Projects/shokunin/mado-shokunin/PROVINCE.md",
        "lines": "34",
        "text": "**Out of province → report, never absorb.**",
    },
]

def main():
    failures = 0
    print("VERIFYING QUOTES FOR ConnSiblingClosure:")
    for idx, item in enumerate(QUOTES, 1):
        path = item["file"]
        lines = item["lines"]
        text = item["text"]
        words = text.split()
        count = len(words)
        
        if count > 25:
            print(f"[{idx}] FAIL: exceeds 25 words ({count}): {text}")
            failures += 1
            continue
            
        if not os.path.isfile(path):
            print(f"[{idx}] FAIL: file missing: {path}")
            failures += 1
            continue
            
        with open(path, "r", errors="ignore") as f:
            src = f.read()
            
        norm_src = " ".join(src.split())
        norm_text = " ".join(text.split())
        
        if norm_text not in norm_src:
            print(f"[{idx}] FAIL: text not found in {path}:{lines}")
            failures += 1
        else:
            print(f"[{idx}] PASS ({count} words): {os.path.basename(path)}:{lines} -> '{text[:45]}...'")

    print(f"\nTOTAL: {len(QUOTES)} checked, {failures} failures.")
    sys.exit(1 if failures else 0)

if __name__ == "__main__":
    main()
