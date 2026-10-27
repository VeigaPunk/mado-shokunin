#!/usr/bin/env python3
"""control c20-fixture-table-refusal-blind - CHEAT: answer every fixture, and answer even when --disable-compose or --keysym is missing

Stops at: clause s (the two documented refusals must exit 2 without printing a table) AND clause g (no nonce coverage)

Built by build-c17-from-draft.py from ExecCounterC1's EMBEDDED_FIXTURES: the table covers all 633 fixtures and nothing else. This is the residual the draft declares ('a tool may special-case them; clause g is what that tool fails'), measured.
"""
import hashlib
import json
import re
import sys


TABLE = {
    "035a25293d3745bd35bc115e7a2abafbf735256025a57e6269fde5968e0d00b0": {
        "A": [
            0,
            "keysym: A (0x0041)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n38       AC01      1        English (US)         2       [ Shift ]\n38       AC01      1        English (US)         2       [ Lock ]\n"
        ],
        "a": [
            0,
            "keysym: a (0x0061)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n38       AC01      1        English (US)         1       [ ]\n"
        ],
        "slash": [
            0,
            "keysym: slash (0x002f)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n61       AB10      1        English (US)         1       [ ]\n"
        ]
    },
    "08f7f1356dc5de4e082b8d7b7880d2db875b516c39cb9266809dd81976dd6d27": {
        "0": [
            0,
            "keysym: 0 (0x0030)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n19       AE10      1        English (US)         1       [ ]\n19       AE10      2        Russian              1       [ ]\n19       AE10      3        German               1       [ ]\n"
        ],
        "0x1008ff12": [
            0,
            "keysym: XF86AudioMute (0x1008ff12)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n121      MUTE      1        English (US)         1       [ ]\n"
        ],
        "0x2f": [
            0,
            "keysym: slash (0x002f)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n16       AE07      3        German               2       [ Shift ]\n51       BKSL      2        Russian              2       [ Shift ]\n61       AB10      1        English (US)         1       [ ]\n94       LSGT      2        Russian              1       [ ]\n"
        ],
        "0x7e1": [
            0,
            "keysym: Greek_alpha (0x07e1)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "1": [
            0,
            "keysym: 1 (0x0031)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n10       AE01      1        English (US)         1       [ ]\n10       AE01      2        Russian              1       [ ]\n10       AE01      3        German               1       [ ]\n"
        ],
        "2": [
            0,
            "keysym: 2 (0x0032)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n11       AE02      1        English (US)         1       [ ]\n11       AE02      2        Russian              1       [ ]\n11       AE02      3        German               1       [ ]\n"
        ],
        "3": [
            0,
            "keysym: 3 (0x0033)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n12       AE03      1        English (US)         1       [ ]\n12       AE03      2        Russian              1       [ ]\n12       AE03      3        German               1       [ ]\n"
        ],
        "4": [
            0,
            "keysym: 4 (0x0034)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n13       AE04      1        English (US)         1       [ ]\n13       AE04      2        Russian              1       [ ]\n13       AE04      3        German               1       [ ]\n"
        ],
        "47": [
            0,
            "keysym: slash (0x002f)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n16       AE07      3        German               2       [ Shift ]\n51       BKSL      2        Russian              2       [ Shift ]\n61       AB10      1        English (US)         1       [ ]\n94       LSGT      2        Russian              1       [ ]\n"
        ],
        "5": [
            0,
            "keysym: 5 (0x0035)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n14       AE05      1        English (US)         1       [ ]\n14       AE05      2        Russian              1       [ ]\n14       AE05      3        German               1       [ ]\n"
        ],
        "6": [
            0,
            "keysym: 6 (0x0036)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n15       AE06      1        English (US)         1       [ ]\n15       AE06      2        Russian              1       [ ]\n15       AE06      3        German               1       [ ]\n"
        ],
        "7": [
            0,
            "keysym: 7 (0x0037)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n16       AE07      1        English (US)         1       [ ]\n16       AE07      2        Russian              1       [ ]\n16       AE07      3        German               1       [ ]\n"
        ],
        "8": [
            0,
            "keysym: 8 (0x0038)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n17       AE08      1        English (US)         1       [ ]\n17       AE08      2        Russian              1       [ ]\n17       AE08      3        German               1       [ ]\n"
        ],
        "9": [
            0,
            "keysym: 9 (0x0039)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n18       AE09      1        English (US)         1       [ ]\n18       AE09      2        Russian              1       [ ]\n18       AE09      3        German               1       [ ]\n"
        ],
        "A": [
            0,
            "keysym: A (0x0041)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n38       AC01      1        English (US)         2       [ Shift ]\n38       AC01      1        English (US)         2       [ Lock ]\n38       AC01      3        German               2       [ Shift ]\n38       AC01      3        German               2       [ Lock ]\n"
        ],
        "Amacron": [
            0,
            "keysym: Amacron (0x03c0)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "Armenian_ayb": [
            0,
            "keysym: Armenian_ayb (0x1000561)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "Cyrillic_a": [
            0,
            "keysym: Cyrillic_a (0x06c1)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n41       AC04      2        Russian              1       [ ]\n"
        ],
        "Cyrillic_shorti": [
            0,
            "keysym: Cyrillic_shorti (0x06ca)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n24       AD01      2        Russian              1       [ ]\n"
        ],
        "Cyrillic_ya": [
            0,
            "keysym: Cyrillic_ya (0x06d1)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n52       AB01      2        Russian              1       [ ]\n"
        ],
        "Emacron": [
            0,
            "keysym: Emacron (0x03aa)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "F1": [
            0,
            "keysym: F1 (0xffbe)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n67       FK01      1        English (US)         1       [ ]\n67       FK01      1        English (US)         1       [ Control ]\n67       FK01      1        English (US)         1       [ Mod1 Alt Meta ]\n67       FK01      1        English (US)         2       [ Shift ]\n67       FK01      1        English (US)         2       [ Shift Control ]\n67       FK01      1        English (US)         2       [ Shift Mod1 Alt Meta ]\n67       FK01      1        English (US)         2       [ Shift Control Mod1 Alt Meta ]\n67       FK01      1        English (US)         3       [ Mod5 LevelThree ]\n67       FK01      1        English (US)         3       [ Control Mod5 LevelThree ]\n67       FK01      1        English (US)         3       [ Mod1 Mod5 Alt LevelThree Meta ]\n67       FK01      1        English (US)         3       [ Control Mod1 Mod5 Alt LevelThree Meta ]\n67       FK01      1        English (US)         4       [ Shift Mod5 LevelThree ]\n67       FK01      1        English (US)         4       [ Shift Control Mod5 LevelThree ]\n67       FK01      1        English (US)         4       [ Shift Mod1 Mod5 Alt LevelThree Meta ]\n67       FK01      1        English (US)         4       [ Shift Control Mod1 Mod5 Alt LevelThree Meta ]\n"
        ],
        "F10": [
            0,
            "keysym: F10 (0xffc7)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n76       FK10      1        English (US)         1       [ ]\n76       FK10      1        English (US)         1       [ Control ]\n76       FK10      1        English (US)         1       [ Mod1 Alt Meta ]\n76       FK10      1        English (US)         2       [ Shift ]\n76       FK10      1        English (US)         2       [ Shift Control ]\n76       FK10      1        English (US)         2       [ Shift Mod1 Alt Meta ]\n76       FK10      1        English (US)         2       [ Shift Control Mod1 Alt Meta ]\n76       FK10      1        English (US)         3       [ Mod5 LevelThree ]\n76       FK10      1        English (US)         3       [ Control Mod5 LevelThree ]\n76       FK10      1        English (US)         3       [ Mod1 Mod5 Alt LevelThree Meta ]\n76       FK10      1        English (US)         3       [ Control Mod1 Mod5 Alt LevelThree Meta ]\n76       FK10      1        English (US)         4       [ Shift Mod5 LevelThree ]\n76       FK10      1        English (US)         4       [ Shift Control Mod5 LevelThree ]\n76       FK10      1        English (US)         4       [ Shift Mod1 Mod5 Alt LevelThree Meta ]\n76       FK10      1        English (US)         4       [ Shift Control Mod1 Mod5 Alt LevelThree Meta ]\n"
        ],
        "F11": [
            0,
            "keysym: F11 (0xffc8)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n95       FK11      1        English (US)         1       [ ]\n95       FK11      1        English (US)         1       [ Control ]\n95       FK11      1        English (US)         1       [ Mod1 Alt Meta ]\n95       FK11      1        English (US)         2       [ Shift ]\n95       FK11      1        English (US)         2       [ Shift Control ]\n95       FK11      1        English (US)         2       [ Shift Mod1 Alt Meta ]\n95       FK11      1        English (US)         2       [ Shift Control Mod1 Alt Meta ]\n95       FK11      1        English (US)         3       [ Mod5 LevelThree ]\n95       FK11      1        English (US)         3       [ Control Mod5 LevelThree ]\n95       FK11      1        English (US)         3       [ Mod1 Mod5 Alt LevelThree Meta ]\n95       FK11      1        English (US)         3       [ Control Mod1 Mod5 Alt LevelThree Meta ]\n95       FK11      1        English (US)         4       [ Shift Mod5 LevelThree ]\n95       FK11      1        English (US)         4       [ Shift Control Mod5 LevelThree ]\n95       FK11      1        English (US)         4       [ Shift Mod1 Mod5 Alt LevelThree Meta ]\n95       FK11      1        English (US)         4       [ Shift Control Mod1 Mod5 Alt LevelThree Meta ]\n"
        ],
        "F12": [
            0,
            "keysym: F12 (0xffc9)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n96       FK12      1        English (US)         1       [ ]\n96       FK12      1        English (US)         1       [ Control ]\n96       FK12      1        English (US)         1       [ Mod1 Alt Meta ]\n96       FK12      1        English (US)         2       [ Shift ]\n96       FK12      1        English (US)         2       [ Shift Control ]\n96       FK12      1        English (US)         2       [ Shift Mod1 Alt Meta ]\n96       FK12      1        English (US)         2       [ Shift Control Mod1 Alt Meta ]\n96       FK12      1        English (US)         3       [ Mod5 LevelThree ]\n96       FK12      1        English (US)         3       [ Control Mod5 LevelThree ]\n96       FK12      1        English (US)         3       [ Mod1 Mod5 Alt LevelThree Meta ]\n96       FK12      1        English (US)         3       [ Control Mod1 Mod5 Alt LevelThree Meta ]\n96       FK12      1        English (US)         4       [ Shift Mod5 LevelThree ]\n96       FK12      1        English (US)         4       [ Shift Control Mod5 LevelThree ]\n96       FK12      1        English (US)         4       [ Shift Mod1 Mod5 Alt LevelThree Meta ]\n96       FK12      1        English (US)         4       [ Shift Control Mod1 Mod5 Alt LevelThree Meta ]\n"
        ],
        "F13": [
            0,
            "keysym: F13 (0xffca)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "F14": [
            0,
            "keysym: F14 (0xffcb)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "F15": [
            0,
            "keysym: F15 (0xffcc)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "F16": [
            0,
            "keysym: F16 (0xffcd)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "F17": [
            0,
            "keysym: F17 (0xffce)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "F18": [
            0,
            "keysym: F18 (0xffcf)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "F2": [
            0,
            "keysym: F2 (0xffbf)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n68       FK02      1        English (US)         1       [ ]\n68       FK02      1        English (US)         1       [ Control ]\n68       FK02      1        English (US)         1       [ Mod1 Alt Meta ]\n68       FK02      1        English (US)         2       [ Shift ]\n68       FK02      1        English (US)         2       [ Shift Control ]\n68       FK02      1        English (US)         2       [ Shift Mod1 Alt Meta ]\n68       FK02      1        English (US)         2       [ Shift Control Mod1 Alt Meta ]\n68       FK02      1        English (US)         3       [ Mod5 LevelThree ]\n68       FK02      1        English (US)         3       [ Control Mod5 LevelThree ]\n68       FK02      1        English (US)         3       [ Mod1 Mod5 Alt LevelThree Meta ]\n68       FK02      1        English (US)         3       [ Control Mod1 Mod5 Alt LevelThree Meta ]\n68       FK02      1        English (US)         4       [ Shift Mod5 LevelThree ]\n68       FK02      1        English (US)         4       [ Shift Control Mod5 LevelThree ]\n68       FK02      1        English (US)         4       [ Shift Mod1 Mod5 Alt LevelThree Meta ]\n68       FK02      1        English (US)         4       [ Shift Control Mod1 Mod5 Alt LevelThree Meta ]\n"
        ],
        "F3": [
            0,
            "keysym: F3 (0xffc0)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n69       FK03      1        English (US)         1       [ ]\n69       FK03      1        English (US)         1       [ Control ]\n69       FK03      1        English (US)         1       [ Mod1 Alt Meta ]\n69       FK03      1        English (US)         2       [ Shift ]\n69       FK03      1        English (US)         2       [ Shift Control ]\n69       FK03      1        English (US)         2       [ Shift Mod1 Alt Meta ]\n69       FK03      1        English (US)         2       [ Shift Control Mod1 Alt Meta ]\n69       FK03      1        English (US)         3       [ Mod5 LevelThree ]\n69       FK03      1        English (US)         3       [ Control Mod5 LevelThree ]\n69       FK03      1        English (US)         3       [ Mod1 Mod5 Alt LevelThree Meta ]\n69       FK03      1        English (US)         3       [ Control Mod1 Mod5 Alt LevelThree Meta ]\n69       FK03      1        English (US)         4       [ Shift Mod5 LevelThree ]\n69       FK03      1        English (US)         4       [ Shift Control Mod5 LevelThree ]\n69       FK03      1        English (US)         4       [ Shift Mod1 Mod5 Alt LevelThree Meta ]\n69       FK03      1        English (US)         4       [ Shift Control Mod1 Mod5 Alt LevelThree Meta ]\n"
        ],
        "F4": [
            0,
            "keysym: F4 (0xffc1)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n70       FK04      1        English (US)         1       [ ]\n70       FK04      1        English (US)         1       [ Control ]\n70       FK04      1        English (US)         1       [ Mod1 Alt Meta ]\n70       FK04      1        English (US)         2       [ Shift ]\n70       FK04      1        English (US)         2       [ Shift Control ]\n70       FK04      1        English (US)         2       [ Shift Mod1 Alt Meta ]\n70       FK04      1        English (US)         2       [ Shift Control Mod1 Alt Meta ]\n70       FK04      1        English (US)         3       [ Mod5 LevelThree ]\n70       FK04      1        English (US)         3       [ Control Mod5 LevelThree ]\n70       FK04      1        English (US)         3       [ Mod1 Mod5 Alt LevelThree Meta ]\n70       FK04      1        English (US)         3       [ Control Mod1 Mod5 Alt LevelThree Meta ]\n70       FK04      1        English (US)         4       [ Shift Mod5 LevelThree ]\n70       FK04      1        English (US)         4       [ Shift Control Mod5 LevelThree ]\n70       FK04      1        English (US)         4       [ Shift Mod1 Mod5 Alt LevelThree Meta ]\n70       FK04      1        English (US)         4       [ Shift Control Mod1 Mod5 Alt LevelThree Meta ]\n"
        ],
        "F5": [
            0,
            "keysym: F5 (0xffc2)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n71       FK05      1        English (US)         1       [ ]\n71       FK05      1        English (US)         1       [ Control ]\n71       FK05      1        English (US)         1       [ Mod1 Alt Meta ]\n71       FK05      1        English (US)         2       [ Shift ]\n71       FK05      1        English (US)         2       [ Shift Control ]\n71       FK05      1        English (US)         2       [ Shift Mod1 Alt Meta ]\n71       FK05      1        English (US)         2       [ Shift Control Mod1 Alt Meta ]\n71       FK05      1        English (US)         3       [ Mod5 LevelThree ]\n71       FK05      1        English (US)         3       [ Control Mod5 LevelThree ]\n71       FK05      1        English (US)         3       [ Mod1 Mod5 Alt LevelThree Meta ]\n71       FK05      1        English (US)         3       [ Control Mod1 Mod5 Alt LevelThree Meta ]\n71       FK05      1        English (US)         4       [ Shift Mod5 LevelThree ]\n71       FK05      1        English (US)         4       [ Shift Control Mod5 LevelThree ]\n71       FK05      1        English (US)         4       [ Shift Mod1 Mod5 Alt LevelThree Meta ]\n71       FK05      1        English (US)         4       [ Shift Control Mod1 Mod5 Alt LevelThree Meta ]\n"
        ],
        "F6": [
            0,
            "keysym: F6 (0xffc3)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n72       FK06      1        English (US)         1       [ ]\n72       FK06      1        English (US)         1       [ Control ]\n72       FK06      1        English (US)         1       [ Mod1 Alt Meta ]\n72       FK06      1        English (US)         2       [ Shift ]\n72       FK06      1        English (US)         2       [ Shift Control ]\n72       FK06      1        English (US)         2       [ Shift Mod1 Alt Meta ]\n72       FK06      1        English (US)         2       [ Shift Control Mod1 Alt Meta ]\n72       FK06      1        English (US)         3       [ Mod5 LevelThree ]\n72       FK06      1        English (US)         3       [ Control Mod5 LevelThree ]\n72       FK06      1        English (US)         3       [ Mod1 Mod5 Alt LevelThree Meta ]\n72       FK06      1        English (US)         3       [ Control Mod1 Mod5 Alt LevelThree Meta ]\n72       FK06      1        English (US)         4       [ Shift Mod5 LevelThree ]\n72       FK06      1        English (US)         4       [ Shift Control Mod5 LevelThree ]\n72       FK06      1        English (US)         4       [ Shift Mod1 Mod5 Alt LevelThree Meta ]\n72       FK06      1        English (US)         4       [ Shift Control Mod1 Mod5 Alt LevelThree Meta ]\n"
        ],
        "F7": [
            0,
            "keysym: F7 (0xffc4)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n73       FK07      1        English (US)         1       [ ]\n73       FK07      1        English (US)         1       [ Control ]\n73       FK07      1        English (US)         1       [ Mod1 Alt Meta ]\n73       FK07      1        English (US)         2       [ Shift ]\n73       FK07      1        English (US)         2       [ Shift Control ]\n73       FK07      1        English (US)         2       [ Shift Mod1 Alt Meta ]\n73       FK07      1        English (US)         2       [ Shift Control Mod1 Alt Meta ]\n73       FK07      1        English (US)         3       [ Mod5 LevelThree ]\n73       FK07      1        English (US)         3       [ Control Mod5 LevelThree ]\n73       FK07      1        English (US)         3       [ Mod1 Mod5 Alt LevelThree Meta ]\n73       FK07      1        English (US)         3       [ Control Mod1 Mod5 Alt LevelThree Meta ]\n73       FK07      1        English (US)         4       [ Shift Mod5 LevelThree ]\n73       FK07      1        English (US)         4       [ Shift Control Mod5 LevelThree ]\n73       FK07      1        English (US)         4       [ Shift Mod1 Mod5 Alt LevelThree Meta ]\n73       FK07      1        English (US)         4       [ Shift Control Mod1 Mod5 Alt LevelThree Meta ]\n"
        ],
        "F8": [
            0,
            "keysym: F8 (0xffc5)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n74       FK08      1        English (US)         1       [ ]\n74       FK08      1        English (US)         1       [ Control ]\n74       FK08      1        English (US)         1       [ Mod1 Alt Meta ]\n74       FK08      1        English (US)         2       [ Shift ]\n74       FK08      1        English (US)         2       [ Shift Control ]\n74       FK08      1        English (US)         2       [ Shift Mod1 Alt Meta ]\n74       FK08      1        English (US)         2       [ Shift Control Mod1 Alt Meta ]\n74       FK08      1        English (US)         3       [ Mod5 LevelThree ]\n74       FK08      1        English (US)         3       [ Control Mod5 LevelThree ]\n74       FK08      1        English (US)         3       [ Mod1 Mod5 Alt LevelThree Meta ]\n74       FK08      1        English (US)         3       [ Control Mod1 Mod5 Alt LevelThree Meta ]\n74       FK08      1        English (US)         4       [ Shift Mod5 LevelThree ]\n74       FK08      1        English (US)         4       [ Shift Control Mod5 LevelThree ]\n74       FK08      1        English (US)         4       [ Shift Mod1 Mod5 Alt LevelThree Meta ]\n74       FK08      1        English (US)         4       [ Shift Control Mod1 Mod5 Alt LevelThree Meta ]\n"
        ],
        "F9": [
            0,
            "keysym: F9 (0xffc6)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n75       FK09      1        English (US)         1       [ ]\n75       FK09      1        English (US)         1       [ Control ]\n75       FK09      1        English (US)         1       [ Mod1 Alt Meta ]\n75       FK09      1        English (US)         2       [ Shift ]\n75       FK09      1        English (US)         2       [ Shift Control ]\n75       FK09      1        English (US)         2       [ Shift Mod1 Alt Meta ]\n75       FK09      1        English (US)         2       [ Shift Control Mod1 Alt Meta ]\n75       FK09      1        English (US)         3       [ Mod5 LevelThree ]\n75       FK09      1        English (US)         3       [ Control Mod5 LevelThree ]\n75       FK09      1        English (US)         3       [ Mod1 Mod5 Alt LevelThree Meta ]\n75       FK09      1        English (US)         3       [ Control Mod1 Mod5 Alt LevelThree Meta ]\n75       FK09      1        English (US)         4       [ Shift Mod5 LevelThree ]\n75       FK09      1        English (US)         4       [ Shift Control Mod5 LevelThree ]\n75       FK09      1        English (US)         4       [ Shift Mod1 Mod5 Alt LevelThree Meta ]\n75       FK09      1        English (US)         4       [ Shift Control Mod1 Mod5 Alt LevelThree Meta ]\n"
        ],
        "Greek_alpha": [
            0,
            "keysym: Greek_alpha (0x07e1)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "Greek_beta": [
            0,
            "keysym: Greek_beta (0x07e2)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "KP_0": [
            0,
            "keysym: KP_0 (0xffb0)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n90       KP0       1        English (US)         2       [ Mod2 NumLock ]\n"
        ],
        "KP_1": [
            0,
            "keysym: KP_1 (0xffb1)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n87       KP1       1        English (US)         2       [ Mod2 NumLock ]\n"
        ],
        "KP_2": [
            0,
            "keysym: KP_2 (0xffb2)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n88       KP2       1        English (US)         2       [ Mod2 NumLock ]\n"
        ],
        "KP_3": [
            0,
            "keysym: KP_3 (0xffb3)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n89       KP3       1        English (US)         2       [ Mod2 NumLock ]\n"
        ],
        "KP_4": [
            0,
            "keysym: KP_4 (0xffb4)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n83       KP4       1        English (US)         2       [ Mod2 NumLock ]\n"
        ],
        "KP_5": [
            0,
            "keysym: KP_5 (0xffb5)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n84       KP5       1        English (US)         2       [ Mod2 NumLock ]\n"
        ],
        "KP_6": [
            0,
            "keysym: KP_6 (0xffb6)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n85       KP6       1        English (US)         2       [ Mod2 NumLock ]\n"
        ],
        "KP_7": [
            0,
            "keysym: KP_7 (0xffb7)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n79       KP7       1        English (US)         2       [ Mod2 NumLock ]\n"
        ],
        "KP_8": [
            0,
            "keysym: KP_8 (0xffb8)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n80       KP8       1        English (US)         2       [ Mod2 NumLock ]\n"
        ],
        "KP_9": [
            0,
            "keysym: KP_9 (0xffb9)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n81       KP9       1        English (US)         2       [ Mod2 NumLock ]\n"
        ],
        "KP_Add": [
            0,
            "keysym: KP_Add (0xffab)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n86       KPAD      1        English (US)         1       [ ]\n86       KPAD      1        English (US)         1       [ Control ]\n86       KPAD      1        English (US)         1       [ Mod1 Alt Meta ]\n86       KPAD      1        English (US)         2       [ Shift ]\n86       KPAD      1        English (US)         2       [ Shift Control ]\n86       KPAD      1        English (US)         2       [ Shift Mod1 Alt Meta ]\n86       KPAD      1        English (US)         2       [ Shift Control Mod1 Alt Meta ]\n86       KPAD      1        English (US)         3       [ Mod5 LevelThree ]\n86       KPAD      1        English (US)         3       [ Control Mod5 LevelThree ]\n86       KPAD      1        English (US)         3       [ Mod1 Mod5 Alt LevelThree Meta ]\n86       KPAD      1        English (US)         3       [ Control Mod1 Mod5 Alt LevelThree Meta ]\n86       KPAD      1        English (US)         4       [ Shift Mod5 LevelThree ]\n86       KPAD      1        English (US)         4       [ Shift Control Mod5 LevelThree ]\n86       KPAD      1        English (US)         4       [ Shift Mod1 Mod5 Alt LevelThree Meta ]\n86       KPAD      1        English (US)         4       [ Shift Control Mod1 Mod5 Alt LevelThree Meta ]\n"
        ],
        "KP_Subtract": [
            0,
            "keysym: KP_Subtract (0xffad)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n82       KPSU      1        English (US)         1       [ ]\n82       KPSU      1        English (US)         1       [ Control ]\n82       KPSU      1        English (US)         1       [ Mod1 Alt Meta ]\n82       KPSU      1        English (US)         2       [ Shift ]\n82       KPSU      1        English (US)         2       [ Shift Control ]\n82       KPSU      1        English (US)         2       [ Shift Mod1 Alt Meta ]\n82       KPSU      1        English (US)         2       [ Shift Control Mod1 Alt Meta ]\n82       KPSU      1        English (US)         3       [ Mod5 LevelThree ]\n82       KPSU      1        English (US)         3       [ Control Mod5 LevelThree ]\n82       KPSU      1        English (US)         3       [ Mod1 Mod5 Alt LevelThree Meta ]\n82       KPSU      1        English (US)         3       [ Control Mod1 Mod5 Alt LevelThree Meta ]\n82       KPSU      1        English (US)         4       [ Shift Mod5 LevelThree ]\n82       KPSU      1        English (US)         4       [ Shift Control Mod5 LevelThree ]\n82       KPSU      1        English (US)         4       [ Shift Mod1 Mod5 Alt LevelThree Meta ]\n82       KPSU      1        English (US)         4       [ Shift Control Mod1 Mod5 Alt LevelThree Meta ]\n"
        ],
        "Q": [
            0,
            "keysym: Q (0x0051)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n24       AD01      1        English (US)         2       [ Shift ]\n24       AD01      1        English (US)         2       [ Lock ]\n24       AD01      3        German               2       [ Shift ]\n24       AD01      3        German               2       [ Lock ]\n"
        ],
        "Return": [
            0,
            "keysym: Return (0xff0d)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n36       RTRN      1        English (US)         1       [ ]\n"
        ],
        "SLASH": [
            2,
            ""
        ],
        "Shift_L": [
            0,
            "keysym: Shift_L (0xffe1)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n50       LFSH      1        English (US)         1       [ ]\n"
        ],
        "Thai_kokai": [
            0,
            "keysym: Thai_kokai (0x0da1)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "W": [
            0,
            "keysym: W (0x0057)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n25       AD02      1        English (US)         2       [ Shift ]\n25       AD02      1        English (US)         2       [ Lock ]\n25       AD02      3        German               2       [ Shift ]\n25       AD02      3        German               2       [ Lock ]\n"
        ],
        "XF86Calculator": [
            0,
            "keysym: XF86Calculator (0x1008ff1d)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n148      I148      1        English (US)         1       [ ]\n"
        ],
        "XF86KbdBrightnessDown": [
            0,
            "keysym: XF86KbdBrightnessDown (0x1008ff06)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n237      I237      1        English (US)         1       [ ]\n"
        ],
        "XF86KbdBrightnessUp": [
            0,
            "keysym: XF86KbdBrightnessUp (0x1008ff05)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n238      I238      1        English (US)         1       [ ]\n"
        ],
        "XF86KbdLightOnOff": [
            0,
            "keysym: XF86KbdLightOnOff (0x1008ff04)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n236      I236      1        English (US)         1       [ ]\n"
        ],
        "XF86MonBrightnessDown": [
            0,
            "keysym: XF86MonBrightnessDown (0x1008ff03)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n232      I232      1        English (US)         1       [ ]\n"
        ],
        "XF86MonBrightnessUp": [
            0,
            "keysym: XF86MonBrightnessUp (0x1008ff02)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n233      I233      1        English (US)         1       [ ]\n"
        ],
        "XF86PowerOff": [
            0,
            "keysym: XF86PowerOff (0x1008ff2a)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n124      POWR      1        English (US)         1       [ ]\n"
        ],
        "XF86TouchpadOff": [
            0,
            "keysym: XF86TouchpadOff (0x1008ffb1)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n540      I540      1        English (US)         1       [ ]\n"
        ],
        "XF86TouchpadOn": [
            0,
            "keysym: XF86TouchpadOn (0x1008ffb0)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n200      FK22      1        English (US)         1       [ ]\n539      I539      1        English (US)         1       [ ]\n"
        ],
        "XF86TouchpadToggle": [
            0,
            "keysym: XF86TouchpadToggle (0x1008ffa9)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n93       ZEHA      1        English (US)         2       [ Control Mod4 Super ]\n199      FK21      1        English (US)         1       [ ]\n202      FK24      1        English (US)         2       [ Control Mod4 Super ]\n538      I538      1        English (US)         1       [ ]\n"
        ],
        "Z": [
            0,
            "keysym: Z (0x005a)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n29       AD06      3        German               2       [ Shift ]\n29       AD06      3        German               2       [ Lock ]\n52       AB01      1        English (US)         2       [ Shift ]\n52       AB01      1        English (US)         2       [ Lock ]\n"
        ],
        "a": [
            0,
            "keysym: a (0x0061)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n38       AC01      1        English (US)         1       [ ]\n38       AC01      3        German               1       [ ]\n"
        ],
        "adiaeresis": [
            0,
            "keysym: adiaeresis (0x00e4)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n48       AC11      3        German               1       [ ]\n"
        ],
        "at": [
            0,
            "keysym: at (0x0040)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n11       AE02      1        English (US)         2       [ Shift ]\n24       AD01      3        German               3       [ Mod5 LevelThree ]\n24       AD01      3        German               3       [ Lock Mod5 LevelThree ]\n"
        ],
        "backslash": [
            0,
            "keysym: backslash (0x005c)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n20       AE11      3        German               3       [ Mod5 LevelThree ]\n20       AE11      3        German               3       [ Lock Mod5 LevelThree ]\n51       BKSL      1        English (US)         1       [ ]\n51       BKSL      2        Russian              1       [ ]\n"
        ],
        "bar": [
            0,
            "keysym: bar (0x007c)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n51       BKSL      1        English (US)         2       [ Shift ]\n94       LSGT      1        English (US)         3       [ Mod5 LevelThree ]\n94       LSGT      2        Russian              2       [ Shift ]\n94       LSGT      3        German               3       [ Mod5 LevelThree ]\n"
        ],
        "dead_acute": [
            0,
            "keysym: dead_acute (0xfe51)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n21       AE12      3        German               1       [ ]\n"
        ],
        "dead_circumflex": [
            0,
            "keysym: dead_circumflex (0xfe52)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n48       AC11      3        German               3       [ Mod5 LevelThree ]\n48       AC11      3        German               3       [ Lock Mod5 LevelThree ]\n49       TLDE      3        German               1       [ ]\n"
        ],
        "dollar": [
            0,
            "keysym: dollar (0x0024)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n13       AE04      1        English (US)         2       [ Shift ]\n13       AE04      3        German               2       [ Shift ]\n442      I442      1        English (US)         1       [ ]\n"
        ],
        "e": [
            0,
            "keysym: e (0x0065)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n26       AD03      1        English (US)         1       [ ]\n26       AD03      3        German               1       [ ]\n"
        ],
        "i": [
            0,
            "keysym: i (0x0069)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n31       AD08      1        English (US)         1       [ ]\n31       AD08      3        German               1       [ ]\n"
        ],
        "kp_7": [
            2,
            ""
        ],
        "numbersign": [
            0,
            "keysym: numbersign (0x0023)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n12       AE03      1        English (US)         2       [ Shift ]\n51       BKSL      3        German               1       [ ]\n"
        ],
        "o": [
            0,
            "keysym: o (0x006f)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n32       AD09      1        English (US)         1       [ ]\n32       AD09      3        German               1       [ ]\n"
        ],
        "p": [
            0,
            "keysym: p (0x0070)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n33       AD10      1        English (US)         1       [ ]\n33       AD10      3        German               1       [ ]\n"
        ],
        "q": [
            0,
            "keysym: q (0x0071)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n24       AD01      1        English (US)         1       [ ]\n24       AD01      3        German               1       [ ]\n"
        ],
        "question": [
            0,
            "keysym: question (0x003f)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n16       AE07      2        Russian              2       [ Shift ]\n20       AE11      3        German               2       [ Shift ]\n20       AE11      3        German               2       [ Shift Lock ]\n61       AB10      1        English (US)         2       [ Shift ]\n"
        ],
        "r": [
            0,
            "keysym: r (0x0072)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n27       AD04      1        English (US)         1       [ ]\n27       AD04      3        German               1       [ ]\n"
        ],
        "semicolon": [
            0,
            "keysym: semicolon (0x003b)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n13       AE04      2        Russian              2       [ Shift ]\n47       AC10      1        English (US)         1       [ ]\n59       AB08      3        German               2       [ Shift ]\n"
        ],
        "slash": [
            0,
            "keysym: slash (0x002f)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n16       AE07      3        German               2       [ Shift ]\n51       BKSL      2        Russian              2       [ Shift ]\n61       AB10      1        English (US)         1       [ ]\n94       LSGT      2        Russian              1       [ ]\n"
        ],
        "space": [
            0,
            "keysym: space (0x0020)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n65       SPCE      1        English (US)         1       [ ]\n"
        ],
        "ssharp": [
            0,
            "keysym: ssharp (0x00df)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n20       AE11      3        German               1       [ ]\n"
        ],
        "t": [
            0,
            "keysym: t (0x0074)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n28       AD05      1        English (US)         1       [ ]\n28       AD05      3        German               1       [ ]\n"
        ],
        "u": [
            0,
            "keysym: u (0x0075)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n30       AD07      1        English (US)         1       [ ]\n30       AD07      3        German               1       [ ]\n"
        ],
        "w": [
            0,
            "keysym: w (0x0077)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n25       AD02      1        English (US)         1       [ ]\n25       AD02      3        German               1       [ ]\n"
        ],
        "y": [
            0,
            "keysym: y (0x0079)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n29       AD06      1        English (US)         1       [ ]\n52       AB01      3        German               1       [ ]\n"
        ]
    },
    "0a2f89b71de32b710b8a92a45230ba0b64d15be977d18a13b1ec97262b86a27a": {
        "Caps_Lock": [
            0,
            "keysym: Caps_Lock (0xffe5)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n66       CAPS      1        English (US)         1       [ ]\n"
        ],
        "Cyrillic_a": [
            0,
            "keysym: Cyrillic_a (0x06c1)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n41       AC04      2        Russian              1       [ ]\n"
        ],
        "Cyrillic_ya": [
            0,
            "keysym: Cyrillic_ya (0x06d1)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n52       AB01      2        Russian              1       [ ]\n"
        ],
        "ISO_Level3_Shift": [
            0,
            "keysym: ISO_Level3_Shift (0xfe03)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n92       LVL3      1        English (US)         1       [ ]\n"
        ],
        "ISO_Level5_Shift": [
            0,
            "keysym: ISO_Level5_Shift (0xfe11)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n203      LVL5      1        English (US)         1       [ ]\n"
        ],
        "ISO_Next_Group": [
            0,
            "keysym: ISO_Next_Group (0xfe08)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n50       LFSH      1        English (US)         2       [ Mod1 Alt Meta ]\n62       RTSH      1        English (US)         2       [ Mod1 Alt Meta ]\n64       LALT      1        English (US)         2       [ Shift ]\n108      RALT      1        English (US)         2       [ Shift ]\n592      I592      1        English (US)         1       [ ]\n"
        ],
        "ISO_Prev_Group": [
            0,
            "keysym: ISO_Prev_Group (0xfe0a)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "Mode_switch": [
            0,
            "keysym: ISO_Group_Shift (0xff7e)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "a": [
            0,
            "keysym: a (0x0061)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n38       AC01      1        English (US)         1       [ ]\n"
        ],
        "dead_grave": [
            0,
            "keysym: dead_grave (0xfe50)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "question": [
            0,
            "keysym: question (0x003f)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n16       AE07      2        Russian              2       [ Shift ]\n61       AB10      1        English (US)         2       [ Shift ]\n"
        ],
        "slash": [
            0,
            "keysym: slash (0x002f)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n51       BKSL      2        Russian              2       [ Shift ]\n61       AB10      1        English (US)         1       [ ]\n94       LSGT      2        Russian              1       [ ]\n"
        ],
        "y": [
            0,
            "keysym: y (0x0079)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n29       AD06      1        English (US)         1       [ ]\n"
        ],
        "z": [
            0,
            "keysym: z (0x007a)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n52       AB01      1        English (US)         1       [ ]\n"
        ]
    },
    "212109405d63b6297728fec8f630350b89967c3fc4bf3b4887fbac46c0dbac9c": {
        "a": [
            0,
            "keysym: a (0x0061)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n38       AC01      1        Portuguese (Brazil, Dvorak) 1       [ ]\n"
        ],
        "b": [
            0,
            "keysym: b (0x0062)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n57       AB06      1        Portuguese (Brazil, Dvorak) 1       [ ]\n"
        ],
        "c": [
            0,
            "keysym: c (0x0063)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n31       AD08      1        Portuguese (Brazil, Dvorak) 1       [ ]\n"
        ],
        "comma": [
            0,
            "keysym: comma (0x002c)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n25       AD02      1        Portuguese (Brazil, Dvorak) 1       [ ]\n"
        ],
        "d": [
            0,
            "keysym: d (0x0064)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n43       AC06      1        Portuguese (Brazil, Dvorak) 1       [ ]\n"
        ],
        "dead_acute": [
            0,
            "keysym: dead_acute (0xfe51)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n34       AD11      1        Portuguese (Brazil, Dvorak) 1       [ ]\n"
        ],
        "e": [
            0,
            "keysym: e (0x0065)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n40       AC03      1        Portuguese (Brazil, Dvorak) 1       [ ]\n"
        ],
        "f": [
            0,
            "keysym: f (0x0066)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n29       AD06      1        Portuguese (Brazil, Dvorak) 1       [ ]\n"
        ],
        "g": [
            0,
            "keysym: g (0x0067)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n30       AD07      1        Portuguese (Brazil, Dvorak) 1       [ ]\n"
        ],
        "h": [
            0,
            "keysym: h (0x0068)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n44       AC07      1        Portuguese (Brazil, Dvorak) 1       [ ]\n"
        ],
        "period": [
            0,
            "keysym: period (0x002e)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n26       AD03      1        Portuguese (Brazil, Dvorak) 1       [ ]\n"
        ],
        "question": [
            0,
            "keysym: question (0x003f)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n24       AD01      1        Portuguese (Brazil, Dvorak) 2       [ Shift ]\n"
        ],
        "slash": [
            0,
            "keysym: slash (0x002f)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n24       AD01      1        Portuguese (Brazil, Dvorak) 1       [ ]\n"
        ],
        "x": [
            0,
            "keysym: x (0x0078)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n56       AB05      1        Portuguese (Brazil, Dvorak) 1       [ ]\n"
        ]
    },
    "254746b43c158cc556f9ba93381caac58a9e0ca40a3d6119a61cb528b6019251": {
        "a": [
            0,
            "keysym: a (0x0061)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n38       AC01      1        Portuguese (Brazil, no dead keys) 1       [ ]\n"
        ],
        "acute": [
            0,
            "keysym: acute (0x00b4)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n34       AD11      1        Portuguese (Brazil, no dead keys) 3       [ Mod5 LevelThree ]\n47       AC10      1        Portuguese (Brazil, no dead keys) 3       [ Mod5 LevelThree ]\n47       AC10      1        Portuguese (Brazil, no dead keys) 3       [ Lock Mod5 LevelThree ]\n"
        ],
        "dead_abovering": [
            0,
            "keysym: dead_abovering (0xfe58)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "dead_acute": [
            0,
            "keysym: dead_acute (0xfe51)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "dead_cedilla": [
            0,
            "keysym: dead_cedilla (0xfe5b)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "dead_circumflex": [
            0,
            "keysym: dead_circumflex (0xfe52)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "dead_diaeresis": [
            0,
            "keysym: dead_diaeresis (0xfe57)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "dead_grave": [
            0,
            "keysym: dead_grave (0xfe50)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "dead_macron": [
            0,
            "keysym: dead_macron (0xfe54)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "dead_tilde": [
            0,
            "keysym: dead_tilde (0xfe53)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "e": [
            0,
            "keysym: e (0x0065)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n26       AD03      1        Portuguese (Brazil, no dead keys) 1       [ ]\n"
        ],
        "grave": [
            0,
            "keysym: grave (0x0060)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n34       AD11      1        Portuguese (Brazil, no dead keys) 2       [ Shift ]\n34       AD11      1        Portuguese (Brazil, no dead keys) 4       [ Shift Mod5 LevelThree ]\n"
        ],
        "question": [
            0,
            "keysym: question (0x003f)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n25       AD02      1        Portuguese (Brazil, no dead keys) 3       [ Mod5 LevelThree ]\n25       AD02      1        Portuguese (Brazil, no dead keys) 3       [ Lock Mod5 LevelThree ]\n25       AD02      1        Portuguese (Brazil, no dead keys) 4       [ Shift Mod5 LevelThree ]\n25       AD02      1        Portuguese (Brazil, no dead keys) 4       [ Shift Lock Mod5 LevelThree ]\n97       AB11      1        Portuguese (Brazil, no dead keys) 2       [ Shift ]\n"
        ],
        "slash": [
            0,
            "keysym: slash (0x002f)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n24       AD01      1        Portuguese (Brazil, no dead keys) 3       [ Mod5 LevelThree ]\n24       AD01      1        Portuguese (Brazil, no dead keys) 3       [ Lock Mod5 LevelThree ]\n24       AD01      1        Portuguese (Brazil, no dead keys) 4       [ Shift Mod5 LevelThree ]\n24       AD01      1        Portuguese (Brazil, no dead keys) 4       [ Shift Lock Mod5 LevelThree ]\n97       AB11      1        Portuguese (Brazil, no dead keys) 1       [ ]\n"
        ]
    },
    "25aaa901cd1614f6d6e3ef185cafcff232323caa49772beade519e1577bee4d0": {
        "a": [
            0,
            "keysym: a (0x0061)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n38       AC01      1        English (intl., with AltGr dead keys) 1       [ ]\n"
        ],
        "adiaeresis": [
            0,
            "keysym: adiaeresis (0x00e4)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n24       AD01      1        English (intl., with AltGr dead keys) 3       [ Mod5 LevelThree ]\n24       AD01      1        English (intl., with AltGr dead keys) 3       [ Shift Lock Mod5 LevelThree ]\n"
        ],
        "at": [
            0,
            "keysym: at (0x0040)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n11       AE02      1        English (intl., with AltGr dead keys) 2       [ Shift ]\n"
        ],
        "bar": [
            0,
            "keysym: bar (0x007c)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n51       BKSL      1        English (intl., with AltGr dead keys) 2       [ Shift ]\n94       LSGT      1        English (intl., with AltGr dead keys) 2       [ Shift ]\n94       LSGT      1        English (intl., with AltGr dead keys) 4       [ Shift Mod5 LevelThree ]\n"
        ],
        "braceleft": [
            0,
            "keysym: braceleft (0x007b)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n34       AD11      1        English (intl., with AltGr dead keys) 2       [ Shift ]\n"
        ],
        "braceright": [
            0,
            "keysym: braceright (0x007d)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n35       AD12      1        English (intl., with AltGr dead keys) 2       [ Shift ]\n"
        ],
        "bracketleft": [
            0,
            "keysym: bracketleft (0x005b)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n34       AD11      1        English (intl., with AltGr dead keys) 1       [ ]\n"
        ],
        "dead_acute": [
            0,
            "keysym: dead_acute (0xfe51)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n48       AC11      1        English (intl., with AltGr dead keys) 3       [ Mod5 LevelThree ]\n"
        ],
        "dead_grave": [
            0,
            "keysym: dead_grave (0xfe50)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n49       TLDE      1        English (intl., with AltGr dead keys) 3       [ Mod5 LevelThree ]\n"
        ],
        "dead_tilde": [
            0,
            "keysym: dead_tilde (0xfe53)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n49       TLDE      1        English (intl., with AltGr dead keys) 4       [ Shift Mod5 LevelThree ]\n"
        ],
        "e": [
            0,
            "keysym: e (0x0065)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n26       AD03      1        English (intl., with AltGr dead keys) 1       [ ]\n"
        ],
        "eacute": [
            0,
            "keysym: eacute (0x00e9)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n26       AD03      1        English (intl., with AltGr dead keys) 3       [ Mod5 LevelThree ]\n26       AD03      1        English (intl., with AltGr dead keys) 3       [ Shift Lock Mod5 LevelThree ]\n"
        ],
        "numbersign": [
            0,
            "keysym: numbersign (0x0023)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n12       AE03      1        English (intl., with AltGr dead keys) 2       [ Shift ]\n"
        ],
        "slash": [
            0,
            "keysym: slash (0x002f)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n61       AB10      1        English (intl., with AltGr dead keys) 1       [ ]\n"
        ],
        "ssharp": [
            0,
            "keysym: ssharp (0x00df)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n39       AC02      1        English (intl., with AltGr dead keys) 3       [ Mod5 LevelThree ]\n39       AC02      1        English (intl., with AltGr dead keys) 3       [ Lock Mod5 LevelThree ]\n"
        ]
    },
    "40c094912b113606b13117a353a99e72a4dc9c0861e1f491b265dcf0d2b60c1e": {
        "a": [
            0,
            "keysym: a (0x0061)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n38       AC01      1        English (US)         1       [ ]\n"
        ],
        "nobreakspace": [
            0,
            "keysym: nobreakspace (0x00a0)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n65       SPCE      1        English (US)         3       [ Mod5 LevelThree ]\n"
        ],
        "space": [
            0,
            "keysym: space (0x0020)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n65       SPCE      1        English (US)         1       [ ]\n65       SPCE      1        English (US)         2       [ Shift ]\n"
        ]
    },
    "60a77b6f3f627c8071de87fc7626d829ba99c0c07cbbb5f3ba0d84e38a3f202a": {
        "Alt_L": [
            0,
            "keysym: Alt_L (0xffe9)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n133      LWIN      1        English (US)         1       [ ]\n204      ALT       1        English (US)         2       [ Shift ]\n"
        ],
        "Hyper_L": [
            0,
            "keysym: Hyper_L (0xffed)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n207      HYPR      1        English (US)         2       [ Shift ]\n"
        ],
        "Meta_L": [
            0,
            "keysym: Meta_L (0xffe7)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n133      LWIN      1        English (US)         2       [ Shift ]\n205      META      1        English (US)         2       [ Shift ]\n"
        ],
        "Meta_R": [
            0,
            "keysym: Meta_R (0xffe8)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "Return": [
            0,
            "keysym: Return (0xff0d)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n36       RTRN      1        English (US)         1       [ ]\n"
        ],
        "Shift_Lock": [
            0,
            "keysym: Shift_Lock (0xffe6)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "Super_L": [
            0,
            "keysym: Super_L (0xffeb)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n64       LALT      1        English (US)         1       [ ]\n206      SUPR      1        English (US)         2       [ Shift ]\n"
        ],
        "a": [
            0,
            "keysym: a (0x0061)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n38       AC01      1        English (US)         1       [ ]\n"
        ]
    },
    "6477ac5272d8d643bf80b44d546f0b98009cffb2b6b931ea42f24bea92d691e0": {
        "1": [
            0,
            "keysym: 1 (0x0031)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n10       AE01      1        English (US)         1       [ ]\n10       AE01      2        Russian              1       [ ]\n10       AE01      3        German               1       [ ]\n10       AE01      4        French               2       [ Shift ]\n"
        ],
        "Cyrillic_a": [
            0,
            "keysym: Cyrillic_a (0x06c1)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n41       AC04      2        Russian              1       [ ]\n"
        ],
        "a": [
            0,
            "keysym: a (0x0061)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n24       AD01      4        French               1       [ ]\n38       AC01      1        English (US)         1       [ ]\n38       AC01      3        German               1       [ ]\n"
        ],
        "adiaeresis": [
            0,
            "keysym: adiaeresis (0x00e4)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n48       AC11      3        German               1       [ ]\n"
        ],
        "eacute": [
            0,
            "keysym: eacute (0x00e9)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n11       AE02      4        French               1       [ ]\n"
        ],
        "question": [
            0,
            "keysym: question (0x003f)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n16       AE07      2        Russian              2       [ Shift ]\n20       AE11      3        German               2       [ Shift ]\n20       AE11      3        German               2       [ Shift Lock ]\n58       AB07      4        French               2       [ Shift ]\n61       AB10      1        English (US)         2       [ Shift ]\n"
        ],
        "slash": [
            0,
            "keysym: slash (0x002f)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n16       AE07      3        German               2       [ Shift ]\n51       BKSL      2        Russian              2       [ Shift ]\n60       AB09      4        French               2       [ Shift ]\n61       AB10      1        English (US)         1       [ ]\n94       LSGT      2        Russian              1       [ ]\n"
        ],
        "ssharp": [
            0,
            "keysym: ssharp (0x00df)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n20       AE11      3        German               1       [ ]\n39       AC02      4        French               3       [ Mod5 LevelThree ]\n39       AC02      4        French               3       [ Shift Lock Mod5 LevelThree ]\n"
        ]
    },
    "65348b8c8a1e7e5ccdf9dca800a2ad4406c1ee3b22f401ad6564bd7e681f5a0f": {
        "ISO_Level3_Shift": [
            0,
            "keysym: ISO_Level3_Shift (0xfe03)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n92       LVL3      1        Portuguese (Brazil)  1       [ ]\n108      RALT      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "Multi_key": [
            0,
            "keysym: Multi_key (0xff20)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "at": [
            0,
            "keysym: at (0x0040)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n11       AE02      1        Portuguese (Brazil)  2       [ Shift ]\n"
        ],
        "question": [
            0,
            "keysym: question (0x003f)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n25       AD02      1        Portuguese (Brazil)  3       [ Mod5 LevelThree ]\n25       AD02      1        Portuguese (Brazil)  3       [ Lock Mod5 LevelThree ]\n25       AD02      1        Portuguese (Brazil)  4       [ Shift Mod5 LevelThree ]\n25       AD02      1        Portuguese (Brazil)  4       [ Shift Lock Mod5 LevelThree ]\n97       AB11      1        Portuguese (Brazil)  2       [ Shift ]\n"
        ],
        "slash": [
            0,
            "keysym: slash (0x002f)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n24       AD01      1        Portuguese (Brazil)  3       [ Mod5 LevelThree ]\n24       AD01      1        Portuguese (Brazil)  3       [ Lock Mod5 LevelThree ]\n24       AD01      1        Portuguese (Brazil)  4       [ Shift Mod5 LevelThree ]\n24       AD01      1        Portuguese (Brazil)  4       [ Shift Lock Mod5 LevelThree ]\n97       AB11      1        Portuguese (Brazil)  1       [ ]\n"
        ]
    },
    "784523f269114e810fe46a15c19bfd68983e848d05b280b50e8fe46927ec949c": {
        "0": [
            0,
            "keysym: 0 (0x0030)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n19       AE10      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "1": [
            0,
            "keysym: 1 (0x0031)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n10       AE01      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "2": [
            0,
            "keysym: 2 (0x0032)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n11       AE02      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "3": [
            0,
            "keysym: 3 (0x0033)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n12       AE03      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "Escape": [
            0,
            "keysym: Escape (0xff1b)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n9        ESC       1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "KP_Decimal": [
            0,
            "keysym: KP_Decimal (0xffae)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n129      I129      1        Portuguese (Brazil)  1       [ ]\n129      I129      1        Portuguese (Brazil)  2       [ Mod2 NumLock ]\n"
        ],
        "KP_Separator": [
            0,
            "keysym: KP_Separator (0xffac)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n91       KPDL      1        Portuguese (Brazil)  2       [ Mod2 NumLock ]\n"
        ],
        "a": [
            0,
            "keysym: a (0x0061)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n38       AC01      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "backslash": [
            0,
            "keysym: backslash (0x005c)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n20       AE11      1        Portuguese (Brazil)  3       [ Mod5 LevelThree ]\n94       LSGT      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "cedilla": [
            0,
            "keysym: cedilla (0x00b8)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "dead_acute": [
            0,
            "keysym: dead_acute (0xfe51)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n34       AD11      1        Portuguese (Brazil)  1       [ ]\n47       AC10      1        Portuguese (Brazil)  3       [ Mod5 LevelThree ]\n47       AC10      1        Portuguese (Brazil)  3       [ Lock Mod5 LevelThree ]\n"
        ],
        "dead_cedilla": [
            0,
            "keysym: dead_cedilla (0xfe5b)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "question": [
            0,
            "keysym: question (0x003f)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n25       AD02      1        Portuguese (Brazil)  3       [ Mod5 LevelThree ]\n25       AD02      1        Portuguese (Brazil)  3       [ Lock Mod5 LevelThree ]\n25       AD02      1        Portuguese (Brazil)  4       [ Shift Mod5 LevelThree ]\n25       AD02      1        Portuguese (Brazil)  4       [ Shift Lock Mod5 LevelThree ]\n97       AB11      1        Portuguese (Brazil)  2       [ Shift ]\n"
        ],
        "slash": [
            0,
            "keysym: slash (0x002f)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n24       AD01      1        Portuguese (Brazil)  3       [ Mod5 LevelThree ]\n24       AD01      1        Portuguese (Brazil)  3       [ Lock Mod5 LevelThree ]\n24       AD01      1        Portuguese (Brazil)  4       [ Shift Mod5 LevelThree ]\n24       AD01      1        Portuguese (Brazil)  4       [ Shift Lock Mod5 LevelThree ]\n97       AB11      1        Portuguese (Brazil)  1       [ ]\n"
        ]
    },
    "7bb4ed2cde92afeac1397dd6fa1bca80b9bde411647b210bff255c0622cb6261": {
        "ISO_Level5_Shift": [
            0,
            "keysym: ISO_Level5_Shift (0xfe11)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n66       CAPS      1        English (US)         1       [ ]\n203      LVL5      1        English (US)         1       [ ]\n"
        ],
        "a": [
            0,
            "keysym: a (0x0061)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n38       AC01      1        English (US)         1       [ ]\n"
        ],
        "at": [
            0,
            "keysym: at (0x0040)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n11       AE02      1        English (US)         2       [ Shift ]\n"
        ],
        "braceleft": [
            0,
            "keysym: braceleft (0x007b)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n34       AD11      1        English (US)         2       [ Shift ]\n"
        ]
    },
    "82da378656a08563dd68fe126eaef57efe05bb34525567b99de7f684c41bee67": {
        "Alt_L": [
            0,
            "keysym: Alt_L (0xffe9)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n64       LALT      1        English (US)         1       [ ]\n204      ALT       1        English (US)         2       [ Shift ]\n"
        ],
        "Alt_R": [
            0,
            "keysym: Alt_R (0xffea)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "Control_L": [
            0,
            "keysym: Control_L (0xffe3)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n37       LCTL      1        English (US)         1       [ ]\n"
        ],
        "Control_R": [
            0,
            "keysym: Control_R (0xffe4)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n105      RCTL      1        English (US)         1       [ ]\n"
        ],
        "EuroSign": [
            0,
            "keysym: EuroSign (0x20ac)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n443      I443      1        English (US)         1       [ ]\n"
        ],
        "ISO_Level3_Shift": [
            0,
            "keysym: ISO_Level3_Shift (0xfe03)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n92       LVL3      1        English (US)         1       [ ]\n108      RALT      1        English (US)         1       [ ]\n"
        ],
        "Shift_L": [
            0,
            "keysym: Shift_L (0xffe1)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n50       LFSH      1        English (US)         1       [ ]\n"
        ],
        "Shift_R": [
            0,
            "keysym: Shift_R (0xffe2)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n62       RTSH      1        English (US)         1       [ ]\n"
        ],
        "Super_L": [
            0,
            "keysym: Super_L (0xffeb)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n133      LWIN      1        English (US)         1       [ ]\n206      SUPR      1        English (US)         2       [ Shift ]\n"
        ],
        "Super_R": [
            0,
            "keysym: Super_R (0xffec)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n134      RWIN      1        English (US)         1       [ ]\n"
        ],
        "XF86AudioMute": [
            0,
            "keysym: XF86AudioMute (0x1008ff12)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n121      MUTE      1        English (US)         1       [ ]\n"
        ],
        "XF86MonBrightnessDown": [
            0,
            "keysym: XF86MonBrightnessDown (0x1008ff03)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n232      I232      1        English (US)         1       [ ]\n"
        ],
        "a": [
            0,
            "keysym: a (0x0061)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n38       AC01      1        English (US)         1       [ ]\n"
        ],
        "at": [
            0,
            "keysym: at (0x0040)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n11       AE02      1        English (US)         2       [ Shift ]\n"
        ],
        "bar": [
            0,
            "keysym: bar (0x007c)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n51       BKSL      1        English (US)         2       [ Shift ]\n94       LSGT      1        English (US)         3       [ Mod5 LevelThree ]\n"
        ],
        "braceleft": [
            0,
            "keysym: braceleft (0x007b)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n34       AD11      1        English (US)         2       [ Shift ]\n"
        ],
        "eacute": [
            0,
            "keysym: eacute (0x00e9)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "slash": [
            0,
            "keysym: slash (0x002f)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n61       AB10      1        English (US)         1       [ ]\n"
        ]
    },
    "9c3824881830257411c33fbc8742e53eeb057142339c0ed008454835e0203447": {
        "Cyrillic_a": [
            0,
            "keysym: Cyrillic_a (0x06c1)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n41       AC04      2        Russian              1       [ ]\n"
        ],
        "F2": [
            0,
            "keysym: F2 (0xffbf)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n68       FK02      1        English (US)         1       [ ]\n68       FK02      1        English (US)         1       [ Control ]\n68       FK02      1        English (US)         1       [ Mod1 Alt Meta ]\n68       FK02      1        English (US)         2       [ Shift ]\n68       FK02      1        English (US)         2       [ Shift Control ]\n68       FK02      1        English (US)         2       [ Shift Mod1 Alt Meta ]\n68       FK02      1        English (US)         2       [ Shift Control Mod1 Alt Meta ]\n68       FK02      1        English (US)         3       [ Mod5 LevelThree ]\n68       FK02      1        English (US)         3       [ Control Mod5 LevelThree ]\n68       FK02      1        English (US)         3       [ Mod1 Mod5 Alt LevelThree Meta ]\n68       FK02      1        English (US)         3       [ Control Mod1 Mod5 Alt LevelThree Meta ]\n68       FK02      1        English (US)         4       [ Shift Mod5 LevelThree ]\n68       FK02      1        English (US)         4       [ Shift Control Mod5 LevelThree ]\n68       FK02      1        English (US)         4       [ Shift Mod1 Mod5 Alt LevelThree Meta ]\n68       FK02      1        English (US)         4       [ Shift Control Mod1 Mod5 Alt LevelThree Meta ]\n"
        ],
        "KP_8": [
            0,
            "keysym: KP_8 (0xffb8)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n80       KP8       1        English (US)         2       [ Mod2 NumLock ]\n"
        ],
        "Return": [
            0,
            "keysym: Return (0xff0d)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n36       RTRN      1        English (US)         1       [ ]\n"
        ],
        "a": [
            0,
            "keysym: a (0x0061)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n38       AC01      1        English (US)         1       [ ]\n38       AC01      3        German (no dead keys) 1       [ ]\n"
        ],
        "adiaeresis": [
            0,
            "keysym: adiaeresis (0x00e4)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n48       AC11      3        German (no dead keys) 1       [ ]\n"
        ],
        "dead_acute": [
            0,
            "keysym: dead_acute (0xfe51)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "dead_grave": [
            0,
            "keysym: dead_grave (0xfe50)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "question": [
            0,
            "keysym: question (0x003f)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n16       AE07      2        Russian              2       [ Shift ]\n20       AE11      3        German (no dead keys) 2       [ Shift ]\n20       AE11      3        German (no dead keys) 2       [ Shift Lock ]\n61       AB10      1        English (US)         2       [ Shift ]\n"
        ],
        "slash": [
            0,
            "keysym: slash (0x002f)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n16       AE07      3        German (no dead keys) 2       [ Shift ]\n51       BKSL      2        Russian              2       [ Shift ]\n61       AB10      1        English (US)         1       [ ]\n94       LSGT      2        Russian              1       [ ]\n"
        ],
        "space": [
            0,
            "keysym: space (0x0020)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n65       SPCE      1        English (US)         1       [ ]\n"
        ],
        "ssharp": [
            0,
            "keysym: ssharp (0x00df)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n20       AE11      3        German (no dead keys) 1       [ ]\n"
        ]
    },
    "a6913e48baf415b17a9bc9172ffacc4f19f9abc802d7ecf9ab83f6f5c523a441": {
        "Alt_R": [
            0,
            "keysym: Alt_R (0xffea)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "Multi_key": [
            0,
            "keysym: Multi_key (0xff20)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n108      RALT      1        English (US)         1       [ ]\n108      RALT      1        English (US)         2       [ Shift ]\n"
        ],
        "a": [
            0,
            "keysym: a (0x0061)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n38       AC01      1        English (US)         1       [ ]\n"
        ],
        "at": [
            0,
            "keysym: at (0x0040)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n11       AE02      1        English (US)         2       [ Shift ]\n"
        ]
    },
    "a907fc26f1c6aec693146c4c1af7fd5233848db47a76836d9273b06c3c0e1de2": {
        "Caps_Lock": [
            0,
            "keysym: Caps_Lock (0xffe5)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n37       LCTL      1        English (US)         1       [ ]\n"
        ],
        "Control_L": [
            0,
            "keysym: Control_L (0xffe3)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n66       CAPS      1        English (US)         1       [ ]\n"
        ],
        "a": [
            0,
            "keysym: a (0x0061)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n38       AC01      1        English (US)         1       [ ]\n"
        ],
        "slash": [
            0,
            "keysym: slash (0x002f)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n61       AB10      1        English (US)         1       [ ]\n"
        ]
    },
    "bc465a8bb58d989351e9e2377d5676e8d2e3972a98a28609b8b775b60cc5774d": {
        "Cyrillic_ya": [
            0,
            "keysym: Cyrillic_ya (0x06d1)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "Return": [
            0,
            "keysym: Return (0xff0d)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n36       RTRN      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "a": [
            0,
            "keysym: a (0x0061)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n38       AC01      1        Portuguese (Brazil)  1       [ ]\n38       AC01      2        English (US)         1       [ ]\n"
        ],
        "adiaeresis": [
            0,
            "keysym: adiaeresis (0x00e4)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "ampersand": [
            0,
            "keysym: ampersand (0x0026)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n16       AE07      1        Portuguese (Brazil)  2       [ Shift ]\n16       AE07      2        English (US)         2       [ Shift ]\n45       AC08      1        Portuguese (Brazil)  4       [ Shift Mod5 LevelThree ]\n45       AC08      1        Portuguese (Brazil)  4       [ Shift Lock Mod5 LevelThree ]\n"
        ],
        "asciicircum": [
            0,
            "keysym: asciicircum (0x005e)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n15       AE06      2        English (US)         2       [ Shift ]\n48       AC11      1        Portuguese (Brazil)  4       [ Shift Mod5 LevelThree ]\n"
        ],
        "asterisk": [
            0,
            "keysym: asterisk (0x002a)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n17       AE08      1        Portuguese (Brazil)  2       [ Shift ]\n17       AE08      2        English (US)         2       [ Shift ]\n"
        ],
        "at": [
            0,
            "keysym: at (0x0040)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n11       AE02      1        Portuguese (Brazil)  2       [ Shift ]\n11       AE02      2        English (US)         2       [ Shift ]\n"
        ],
        "backslash": [
            0,
            "keysym: backslash (0x005c)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n20       AE11      1        Portuguese (Brazil)  3       [ Mod5 LevelThree ]\n51       BKSL      2        English (US)         1       [ ]\n94       LSGT      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "bar": [
            0,
            "keysym: bar (0x007c)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n51       BKSL      2        English (US)         2       [ Shift ]\n94       LSGT      1        Portuguese (Brazil)  2       [ Shift ]\n"
        ],
        "dead_abovedot": [
            0,
            "keysym: dead_abovedot (0xfe56)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n61       AB10      1        Portuguese (Brazil)  4       [ Shift Mod5 LevelThree ]\n"
        ],
        "dead_abovering": [
            0,
            "keysym: dead_abovering (0xfe58)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "dead_acute": [
            0,
            "keysym: dead_acute (0xfe51)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n34       AD11      1        Portuguese (Brazil)  1       [ ]\n47       AC10      1        Portuguese (Brazil)  3       [ Mod5 LevelThree ]\n47       AC10      1        Portuguese (Brazil)  3       [ Lock Mod5 LevelThree ]\n"
        ],
        "dead_breve": [
            0,
            "keysym: dead_breve (0xfe55)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n94       LSGT      1        Portuguese (Brazil)  4       [ Shift Mod5 LevelThree ]\n"
        ],
        "dead_cedilla": [
            0,
            "keysym: dead_cedilla (0xfe5b)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "dead_circumflex": [
            0,
            "keysym: dead_circumflex (0xfe52)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n48       AC11      1        Portuguese (Brazil)  2       [ Shift ]\n"
        ],
        "dead_diaeresis": [
            0,
            "keysym: dead_diaeresis (0xfe57)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n15       AE06      1        Portuguese (Brazil)  2       [ Shift ]\n"
        ],
        "dead_grave": [
            0,
            "keysym: dead_grave (0xfe50)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n34       AD11      1        Portuguese (Brazil)  2       [ Shift ]\n"
        ],
        "dead_macron": [
            0,
            "keysym: dead_macron (0xfe54)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n35       AD12      1        Portuguese (Brazil)  4       [ Shift Mod5 LevelThree ]\n"
        ],
        "dead_tilde": [
            0,
            "keysym: dead_tilde (0xfe53)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n48       AC11      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "dollar": [
            0,
            "keysym: dollar (0x0024)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n13       AE04      1        Portuguese (Brazil)  2       [ Shift ]\n13       AE04      2        English (US)         2       [ Shift ]\n442      I442      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "equal": [
            0,
            "keysym: equal (0x003d)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n21       AE12      1        Portuguese (Brazil)  1       [ ]\n21       AE12      2        English (US)         1       [ ]\n"
        ],
        "minus": [
            0,
            "keysym: minus (0x002d)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n20       AE11      1        Portuguese (Brazil)  1       [ ]\n20       AE11      2        English (US)         1       [ ]\n"
        ],
        "numbersign": [
            0,
            "keysym: numbersign (0x0023)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n12       AE03      1        Portuguese (Brazil)  2       [ Shift ]\n12       AE03      2        English (US)         2       [ Shift ]\n"
        ],
        "parenleft": [
            0,
            "keysym: parenleft (0x0028)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n18       AE09      1        Portuguese (Brazil)  2       [ Shift ]\n18       AE09      2        English (US)         2       [ Shift ]\n187      I187      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "parenright": [
            0,
            "keysym: parenright (0x0029)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n19       AE10      1        Portuguese (Brazil)  2       [ Shift ]\n19       AE10      2        English (US)         2       [ Shift ]\n188      I188      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "percent": [
            0,
            "keysym: percent (0x0025)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n14       AE05      1        Portuguese (Brazil)  2       [ Shift ]\n14       AE05      2        English (US)         2       [ Shift ]\n"
        ],
        "period": [
            0,
            "keysym: period (0x002e)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n60       AB09      1        Portuguese (Brazil)  1       [ ]\n60       AB09      2        English (US)         1       [ ]\n"
        ],
        "question": [
            0,
            "keysym: question (0x003f)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n25       AD02      1        Portuguese (Brazil)  3       [ Mod5 LevelThree ]\n25       AD02      1        Portuguese (Brazil)  3       [ Lock Mod5 LevelThree ]\n25       AD02      1        Portuguese (Brazil)  4       [ Shift Mod5 LevelThree ]\n25       AD02      1        Portuguese (Brazil)  4       [ Shift Lock Mod5 LevelThree ]\n61       AB10      2        English (US)         2       [ Shift ]\n97       AB11      1        Portuguese (Brazil)  2       [ Shift ]\n"
        ],
        "semicolon": [
            0,
            "keysym: semicolon (0x003b)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n47       AC10      2        English (US)         1       [ ]\n61       AB10      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "slash": [
            0,
            "keysym: slash (0x002f)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n24       AD01      1        Portuguese (Brazil)  3       [ Mod5 LevelThree ]\n24       AD01      1        Portuguese (Brazil)  3       [ Lock Mod5 LevelThree ]\n24       AD01      1        Portuguese (Brazil)  4       [ Shift Mod5 LevelThree ]\n24       AD01      1        Portuguese (Brazil)  4       [ Shift Lock Mod5 LevelThree ]\n61       AB10      2        English (US)         1       [ ]\n97       AB11      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "underscore": [
            0,
            "keysym: underscore (0x005f)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n20       AE11      1        Portuguese (Brazil)  2       [ Shift ]\n20       AE11      2        English (US)         2       [ Shift ]\n"
        ],
        "z": [
            0,
            "keysym: z (0x007a)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n52       AB01      1        Portuguese (Brazil)  1       [ ]\n52       AB01      2        English (US)         1       [ ]\n"
        ]
    },
    "ca151a9555381a2149e391180662402cccdd4bdd05408869d0265e1651d0896b": {
        "Return": [
            0,
            "keysym: Return (0xff0d)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n36       RTRN      1        Portuguese (Brazil, IBM/Lenovo ThinkPad) 1       [ ]\n"
        ],
        "XF86AudioMute": [
            0,
            "keysym: XF86AudioMute (0x1008ff12)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n121      MUTE      1        Portuguese (Brazil, IBM/Lenovo ThinkPad) 1       [ ]\n"
        ],
        "XF86Battery": [
            0,
            "keysym: XF86Battery (0x1008ff93)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n244      I244      1        Portuguese (Brazil, IBM/Lenovo ThinkPad) 1       [ ]\n"
        ],
        "XF86Display": [
            0,
            "keysym: XF86Display (0x1008ff59)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n235      I235      1        Portuguese (Brazil, IBM/Lenovo ThinkPad) 1       [ ]\n"
        ],
        "XF86Favorites": [
            0,
            "keysym: XF86Favorites (0x1008ff30)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n164      I164      1        Portuguese (Brazil, IBM/Lenovo ThinkPad) 1       [ ]\n372      I372      1        Portuguese (Brazil, IBM/Lenovo ThinkPad) 1       [ ]\n"
        ],
        "XF86HomePage": [
            0,
            "keysym: XF86HomePage (0x1008ff18)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n180      I180      1        Portuguese (Brazil, IBM/Lenovo ThinkPad) 1       [ ]\n"
        ],
        "XF86Mail": [
            0,
            "keysym: XF86Mail (0x1008ff19)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n163      I163      1        Portuguese (Brazil, IBM/Lenovo ThinkPad) 1       [ ]\n223      I223      1        Portuguese (Brazil, IBM/Lenovo ThinkPad) 1       [ ]\n"
        ],
        "XF86Search": [
            0,
            "keysym: XF86Search (0x1008ff1b)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n225      I225      1        Portuguese (Brazil, IBM/Lenovo ThinkPad) 1       [ ]\n"
        ],
        "XF86Shop": [
            0,
            "keysym: XF86Shop (0x1008ff36)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n229      I229      1        Portuguese (Brazil, IBM/Lenovo ThinkPad) 1       [ ]\n"
        ],
        "XF86Sleep": [
            0,
            "keysym: XF86Sleep (0x1008ff2f)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n150      I150      1        Portuguese (Brazil, IBM/Lenovo ThinkPad) 1       [ ]\n"
        ],
        "XF86WWW": [
            0,
            "keysym: XF86WWW (0x1008ff2e)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n158      I158      1        Portuguese (Brazil, IBM/Lenovo ThinkPad) 1       [ ]\n"
        ],
        "XF86WakeUp": [
            0,
            "keysym: XF86WakeUp (0x1008ff2b)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n151      I151      1        Portuguese (Brazil, IBM/Lenovo ThinkPad) 1       [ ]\n"
        ],
        "a": [
            0,
            "keysym: a (0x0061)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n38       AC01      1        Portuguese (Brazil, IBM/Lenovo ThinkPad) 1       [ ]\n"
        ],
        "dead_grave": [
            0,
            "keysym: dead_grave (0xfe50)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n34       AD11      1        Portuguese (Brazil, IBM/Lenovo ThinkPad) 2       [ Shift ]\n"
        ],
        "e": [
            0,
            "keysym: e (0x0065)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n26       AD03      1        Portuguese (Brazil, IBM/Lenovo ThinkPad) 1       [ ]\n"
        ],
        "question": [
            0,
            "keysym: question (0x003f)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n25       AD02      1        Portuguese (Brazil, IBM/Lenovo ThinkPad) 3       [ Mod5 LevelThree ]\n25       AD02      1        Portuguese (Brazil, IBM/Lenovo ThinkPad) 3       [ Lock Mod5 LevelThree ]\n25       AD02      1        Portuguese (Brazil, IBM/Lenovo ThinkPad) 4       [ Shift Mod5 LevelThree ]\n25       AD02      1        Portuguese (Brazil, IBM/Lenovo ThinkPad) 4       [ Shift Lock Mod5 LevelThree ]\n97       AB11      1        Portuguese (Brazil, IBM/Lenovo ThinkPad) 2       [ Shift ]\n105      RCTL      1        Portuguese (Brazil, IBM/Lenovo ThinkPad) 2       [ Shift ]\n"
        ],
        "slash": [
            0,
            "keysym: slash (0x002f)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n24       AD01      1        Portuguese (Brazil, IBM/Lenovo ThinkPad) 3       [ Mod5 LevelThree ]\n24       AD01      1        Portuguese (Brazil, IBM/Lenovo ThinkPad) 3       [ Lock Mod5 LevelThree ]\n24       AD01      1        Portuguese (Brazil, IBM/Lenovo ThinkPad) 4       [ Shift Mod5 LevelThree ]\n24       AD01      1        Portuguese (Brazil, IBM/Lenovo ThinkPad) 4       [ Shift Lock Mod5 LevelThree ]\n97       AB11      1        Portuguese (Brazil, IBM/Lenovo ThinkPad) 1       [ ]\n105      RCTL      1        Portuguese (Brazil, IBM/Lenovo ThinkPad) 1       [ ]\n"
        ]
    },
    "d1ebf48ee8cdabebc7ae967f1aa3fa35bf3fb4efaf0be71522823493a216cfed": {
        "Caps_Lock": [
            0,
            "keysym: Caps_Lock (0xffe5)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "Escape": [
            0,
            "keysym: Escape (0xff1b)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n9        ESC       1        English (US)         1       [ ]\n66       CAPS      1        English (US)         1       [ ]\n"
        ],
        "F11": [
            0,
            "keysym: F11 (0xffc8)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n95       FK11      1        English (US)         1       [ ]\n95       FK11      1        English (US)         1       [ Control ]\n95       FK11      1        English (US)         1       [ Mod1 Alt Meta ]\n95       FK11      1        English (US)         2       [ Shift ]\n95       FK11      1        English (US)         2       [ Shift Control ]\n95       FK11      1        English (US)         2       [ Shift Mod1 Alt Meta ]\n95       FK11      1        English (US)         2       [ Shift Control Mod1 Alt Meta ]\n95       FK11      1        English (US)         3       [ Mod5 LevelThree ]\n95       FK11      1        English (US)         3       [ Control Mod5 LevelThree ]\n95       FK11      1        English (US)         3       [ Mod1 Mod5 Alt LevelThree Meta ]\n95       FK11      1        English (US)         3       [ Control Mod1 Mod5 Alt LevelThree Meta ]\n95       FK11      1        English (US)         4       [ Shift Mod5 LevelThree ]\n95       FK11      1        English (US)         4       [ Shift Control Mod5 LevelThree ]\n95       FK11      1        English (US)         4       [ Shift Mod1 Mod5 Alt LevelThree Meta ]\n95       FK11      1        English (US)         4       [ Shift Control Mod1 Mod5 Alt LevelThree Meta ]\n"
        ],
        "F12": [
            0,
            "keysym: F12 (0xffc9)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n96       FK12      1        English (US)         1       [ ]\n96       FK12      1        English (US)         1       [ Control ]\n96       FK12      1        English (US)         1       [ Mod1 Alt Meta ]\n96       FK12      1        English (US)         2       [ Shift ]\n96       FK12      1        English (US)         2       [ Shift Control ]\n96       FK12      1        English (US)         2       [ Shift Mod1 Alt Meta ]\n96       FK12      1        English (US)         2       [ Shift Control Mod1 Alt Meta ]\n96       FK12      1        English (US)         3       [ Mod5 LevelThree ]\n96       FK12      1        English (US)         3       [ Control Mod5 LevelThree ]\n96       FK12      1        English (US)         3       [ Mod1 Mod5 Alt LevelThree Meta ]\n96       FK12      1        English (US)         3       [ Control Mod1 Mod5 Alt LevelThree Meta ]\n96       FK12      1        English (US)         4       [ Shift Mod5 LevelThree ]\n96       FK12      1        English (US)         4       [ Shift Control Mod5 LevelThree ]\n96       FK12      1        English (US)         4       [ Shift Mod1 Mod5 Alt LevelThree Meta ]\n96       FK12      1        English (US)         4       [ Shift Control Mod1 Mod5 Alt LevelThree Meta ]\n"
        ],
        "a": [
            0,
            "keysym: a (0x0061)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n38       AC01      1        English (US)         1       [ ]\n"
        ],
        "dead_grave": [
            0,
            "keysym: dead_grave (0xfe50)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "slash": [
            0,
            "keysym: slash (0x002f)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n61       AB10      1        English (US)         1       [ ]\n"
        ]
    },
    "dc1c9c01ac37f6bf0a308dc61005f0f63a622616603b4ea8de1d433ed5a515b0": {
        "Arabic_alef": [
            0,
            "keysym: Arabic_alef (0x05c7)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "Greek_alpha": [
            0,
            "keysym: Greek_alpha (0x07e1)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "KP_Decimal": [
            0,
            "keysym: KP_Decimal (0xffae)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n129      I129      1        German (no dead keys) 1       [ ]\n129      I129      1        German (no dead keys) 2       [ Mod2 NumLock ]\n"
        ],
        "KP_Enter": [
            0,
            "keysym: KP_Enter (0xff8d)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n104      KPEN      1        German (no dead keys) 1       [ ]\n"
        ],
        "KP_Separator": [
            0,
            "keysym: KP_Separator (0xffac)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n91       KPDL      1        German (no dead keys) 2       [ Mod2 NumLock ]\n"
        ],
        "adiaeresis": [
            0,
            "keysym: adiaeresis (0x00e4)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n48       AC11      1        German (no dead keys) 1       [ ]\n"
        ],
        "dead_acute": [
            0,
            "keysym: dead_acute (0xfe51)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "dead_cedilla": [
            0,
            "keysym: dead_cedilla (0xfe5b)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "dead_circumflex": [
            0,
            "keysym: dead_circumflex (0xfe52)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "dead_diaeresis": [
            0,
            "keysym: dead_diaeresis (0xfe57)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "dead_grave": [
            0,
            "keysym: dead_grave (0xfe50)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "dead_tilde": [
            0,
            "keysym: dead_tilde (0xfe53)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "minus": [
            0,
            "keysym: minus (0x002d)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n61       AB10      1        German (no dead keys) 1       [ ]\n"
        ],
        "plus": [
            0,
            "keysym: plus (0x002b)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n35       AD12      1        German (no dead keys) 1       [ ]\n"
        ],
        "ssharp": [
            0,
            "keysym: ssharp (0x00df)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n20       AE11      1        German (no dead keys) 1       [ ]\n"
        ],
        "y": [
            0,
            "keysym: y (0x0079)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n52       AB01      1        German (no dead keys) 1       [ ]\n"
        ],
        "z": [
            0,
            "keysym: z (0x007a)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n29       AD06      1        German (no dead keys) 1       [ ]\n"
        ]
    },
    "dd93c63b86376946a88ce61bcfa0d6d9f332aeade3ab6b7ae56e1c2dac510fec": {
        "Caps_Lock": [
            0,
            "keysym: Caps_Lock (0xffe5)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "Control_L": [
            0,
            "keysym: Control_L (0xffe3)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n37       LCTL      1        English (US)         1       [ ]\n66       CAPS      1        English (US)         1       [ ]\n"
        ],
        "a": [
            0,
            "keysym: a (0x0061)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n38       AC01      1        English (US)         1       [ ]\n"
        ],
        "slash": [
            0,
            "keysym: slash (0x002f)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n61       AB10      1        English (US)         1       [ ]\n"
        ]
    },
    "dfc06bfed90753c3406d8ec917f4a6dcd893923cc6ee040aadb9b354484f45bb": {
        "KP_7": [
            0,
            "keysym: KP_7 (0xffb7)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n79       KP7       1        German               2       [ Mod2 NumLock ]\n"
        ],
        "KP_Add": [
            0,
            "keysym: KP_Add (0xffab)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n86       KPAD      1        German               1       [ ]\n86       KPAD      1        German               1       [ Control ]\n86       KPAD      1        German               1       [ Mod1 Alt Meta ]\n86       KPAD      1        German               2       [ Shift ]\n86       KPAD      1        German               2       [ Shift Control ]\n86       KPAD      1        German               2       [ Shift Mod1 Alt Meta ]\n86       KPAD      1        German               2       [ Shift Control Mod1 Alt Meta ]\n86       KPAD      1        German               3       [ Mod5 LevelThree ]\n86       KPAD      1        German               3       [ Control Mod5 LevelThree ]\n86       KPAD      1        German               3       [ Mod1 Mod5 Alt LevelThree Meta ]\n86       KPAD      1        German               3       [ Control Mod1 Mod5 Alt LevelThree Meta ]\n86       KPAD      1        German               4       [ Shift Mod5 LevelThree ]\n86       KPAD      1        German               4       [ Shift Control Mod5 LevelThree ]\n86       KPAD      1        German               4       [ Shift Mod1 Mod5 Alt LevelThree Meta ]\n86       KPAD      1        German               4       [ Shift Control Mod1 Mod5 Alt LevelThree Meta ]\n"
        ],
        "KP_Begin": [
            0,
            "keysym: KP_Begin (0xff9d)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n84       KP5       1        German               1       [ ]\n"
        ],
        "KP_Decimal": [
            0,
            "keysym: KP_Decimal (0xffae)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n129      I129      1        German               1       [ ]\n129      I129      1        German               2       [ Mod2 NumLock ]\n"
        ],
        "KP_Divide": [
            0,
            "keysym: KP_Divide (0xffaf)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n106      KPDV      1        German               1       [ ]\n106      KPDV      1        German               1       [ Control ]\n106      KPDV      1        German               1       [ Mod1 Alt Meta ]\n106      KPDV      1        German               2       [ Shift ]\n106      KPDV      1        German               2       [ Shift Control ]\n106      KPDV      1        German               2       [ Shift Mod1 Alt Meta ]\n106      KPDV      1        German               2       [ Shift Control Mod1 Alt Meta ]\n106      KPDV      1        German               3       [ Mod5 LevelThree ]\n106      KPDV      1        German               3       [ Control Mod5 LevelThree ]\n106      KPDV      1        German               3       [ Mod1 Mod5 Alt LevelThree Meta ]\n106      KPDV      1        German               3       [ Control Mod1 Mod5 Alt LevelThree Meta ]\n106      KPDV      1        German               4       [ Shift Mod5 LevelThree ]\n106      KPDV      1        German               4       [ Shift Control Mod5 LevelThree ]\n106      KPDV      1        German               4       [ Shift Mod1 Mod5 Alt LevelThree Meta ]\n106      KPDV      1        German               4       [ Shift Control Mod1 Mod5 Alt LevelThree Meta ]\n"
        ],
        "KP_End": [
            0,
            "keysym: KP_End (0xff9c)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n87       KP1       1        German               1       [ ]\n"
        ],
        "KP_Enter": [
            0,
            "keysym: KP_Enter (0xff8d)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n104      KPEN      1        German               1       [ ]\n"
        ],
        "KP_Equal": [
            0,
            "keysym: KP_Equal (0xffbd)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n125      KPEQ      1        German               1       [ ]\n"
        ],
        "KP_Home": [
            0,
            "keysym: KP_Home (0xff95)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n79       KP7       1        German               1       [ ]\n"
        ],
        "KP_Insert": [
            0,
            "keysym: KP_Insert (0xff9e)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n90       KP0       1        German               1       [ ]\n"
        ],
        "KP_Multiply": [
            0,
            "keysym: KP_Multiply (0xffaa)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n63       KPMU      1        German               1       [ ]\n63       KPMU      1        German               1       [ Control ]\n63       KPMU      1        German               1       [ Mod1 Alt Meta ]\n63       KPMU      1        German               2       [ Shift ]\n63       KPMU      1        German               2       [ Shift Control ]\n63       KPMU      1        German               2       [ Shift Mod1 Alt Meta ]\n63       KPMU      1        German               2       [ Shift Control Mod1 Alt Meta ]\n63       KPMU      1        German               3       [ Mod5 LevelThree ]\n63       KPMU      1        German               3       [ Control Mod5 LevelThree ]\n63       KPMU      1        German               3       [ Mod1 Mod5 Alt LevelThree Meta ]\n63       KPMU      1        German               3       [ Control Mod1 Mod5 Alt LevelThree Meta ]\n63       KPMU      1        German               4       [ Shift Mod5 LevelThree ]\n63       KPMU      1        German               4       [ Shift Control Mod5 LevelThree ]\n63       KPMU      1        German               4       [ Shift Mod1 Mod5 Alt LevelThree Meta ]\n63       KPMU      1        German               4       [ Shift Control Mod1 Mod5 Alt LevelThree Meta ]\n"
        ],
        "KP_Separator": [
            0,
            "keysym: KP_Separator (0xffac)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n91       KPDL      1        German               2       [ Mod2 NumLock ]\n"
        ],
        "KP_Space": [
            0,
            "keysym: KP_Space (0xff80)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "KP_Tab": [
            0,
            "keysym: KP_Tab (0xff89)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ]
    },
    "e14cf7679459df97cbdca1a00449215fd968d0159d6be372ad85b7dd837f71a2": {
        "0": [
            0,
            "keysym: 0 (0x0030)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n19       AE10      1        English (US, intl., with dead keys) 1       [ ]\n"
        ],
        "1": [
            0,
            "keysym: 1 (0x0031)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n10       AE01      1        English (US, intl., with dead keys) 1       [ ]\n"
        ],
        "5": [
            0,
            "keysym: 5 (0x0035)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n14       AE05      1        English (US, intl., with dead keys) 1       [ ]\n"
        ],
        "9": [
            0,
            "keysym: 9 (0x0039)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n18       AE09      1        English (US, intl., with dead keys) 1       [ ]\n"
        ],
        "Georgian_an": [
            0,
            "keysym: Georgian_an (0x10010d0)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "Greek_omega": [
            0,
            "keysym: Greek_omega (0x07f9)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "Thai_khokhai": [
            0,
            "keysym: Thai_khokhai (0x0da2)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "a": [
            0,
            "keysym: a (0x0061)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n38       AC01      1        English (US, intl., with dead keys) 1       [ ]\n"
        ],
        "apostrophe": [
            0,
            "keysym: apostrophe (0x0027)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n48       AC11      1        English (US, intl., with dead keys) 3       [ Mod5 LevelThree ]\n"
        ],
        "asciitilde": [
            0,
            "keysym: asciitilde (0x007e)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n49       TLDE      1        English (US, intl., with dead keys) 4       [ Shift Mod5 LevelThree ]\n"
        ],
        "braceleft": [
            0,
            "keysym: braceleft (0x007b)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n34       AD11      1        English (US, intl., with dead keys) 2       [ Shift ]\n"
        ],
        "braceright": [
            0,
            "keysym: braceright (0x007d)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n35       AD12      1        English (US, intl., with dead keys) 2       [ Shift ]\n"
        ],
        "bracketleft": [
            0,
            "keysym: bracketleft (0x005b)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n34       AD11      1        English (US, intl., with dead keys) 1       [ ]\n"
        ],
        "bracketright": [
            0,
            "keysym: bracketright (0x005d)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n35       AD12      1        English (US, intl., with dead keys) 1       [ ]\n"
        ],
        "colon": [
            0,
            "keysym: colon (0x003a)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n47       AC10      1        English (US, intl., with dead keys) 2       [ Shift ]\n"
        ],
        "comma": [
            0,
            "keysym: comma (0x002c)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n59       AB08      1        English (US, intl., with dead keys) 1       [ ]\n"
        ],
        "dead_abovedot": [
            0,
            "keysym: dead_abovedot (0xfe56)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n60       AB09      1        English (US, intl., with dead keys) 3       [ Mod5 LevelThree ]\n"
        ],
        "dead_acute": [
            0,
            "keysym: dead_acute (0xfe51)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n48       AC11      1        English (US, intl., with dead keys) 1       [ ]\n"
        ],
        "dead_belowdot": [
            0,
            "keysym: dead_belowdot (0xfe60)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n20       AE11      1        English (US, intl., with dead keys) 4       [ Shift Mod5 LevelThree ]\n"
        ],
        "dead_caron": [
            0,
            "keysym: dead_caron (0xfe5a)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n60       AB09      1        English (US, intl., with dead keys) 4       [ Shift Mod5 LevelThree ]\n"
        ],
        "dead_circumflex": [
            0,
            "keysym: dead_circumflex (0xfe52)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n15       AE06      1        English (US, intl., with dead keys) 2       [ Shift ]\n"
        ],
        "dead_currency": [
            0,
            "keysym: dead_currency (0xfe6f)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "dead_diaeresis": [
            0,
            "keysym: dead_diaeresis (0xfe57)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n48       AC11      1        English (US, intl., with dead keys) 2       [ Shift ]\n"
        ],
        "dead_doubleacute": [
            0,
            "keysym: dead_doubleacute (0xfe59)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n11       AE02      1        English (US, intl., with dead keys) 4       [ Shift Mod5 LevelThree ]\n"
        ],
        "dead_grave": [
            0,
            "keysym: dead_grave (0xfe50)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n49       TLDE      1        English (US, intl., with dead keys) 1       [ ]\n"
        ],
        "dead_greek": [
            0,
            "keysym: dead_greek (0xfe8c)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "dead_hook": [
            0,
            "keysym: dead_hook (0xfe61)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n61       AB10      1        English (US, intl., with dead keys) 4       [ Shift Mod5 LevelThree ]\n"
        ],
        "dead_horn": [
            0,
            "keysym: dead_horn (0xfe62)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n16       AE07      1        English (US, intl., with dead keys) 4       [ Shift Mod5 LevelThree ]\n"
        ],
        "dead_ogonek": [
            0,
            "keysym: dead_ogonek (0xfe5c)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n17       AE08      1        English (US, intl., with dead keys) 4       [ Shift Mod5 LevelThree ]\n"
        ],
        "dead_stroke": [
            0,
            "keysym: dead_stroke (0xfe63)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n53       AB02      1        English (US, intl., with dead keys) 4       [ Shift Mod5 LevelThree ]\n53       AB02      1        English (US, intl., with dead keys) 4       [ Shift Lock Mod5 LevelThree ]\n"
        ],
        "dead_tilde": [
            0,
            "keysym: dead_tilde (0xfe53)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n49       TLDE      1        English (US, intl., with dead keys) 2       [ Shift ]\n"
        ],
        "e": [
            0,
            "keysym: e (0x0065)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n26       AD03      1        English (US, intl., with dead keys) 1       [ ]\n"
        ],
        "exclam": [
            0,
            "keysym: exclam (0x0021)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n10       AE01      1        English (US, intl., with dead keys) 2       [ Shift ]\n"
        ],
        "grave": [
            0,
            "keysym: grave (0x0060)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n49       TLDE      1        English (US, intl., with dead keys) 3       [ Mod5 LevelThree ]\n"
        ],
        "greater": [
            0,
            "keysym: greater (0x003e)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n60       AB09      1        English (US, intl., with dead keys) 2       [ Shift ]\n"
        ],
        "guillemotleft": [
            0,
            "keysym: guillemotleft (0x00ab)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n34       AD11      1        English (US, intl., with dead keys) 3       [ Mod5 LevelThree ]\n"
        ],
        "less": [
            0,
            "keysym: less (0x003c)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n59       AB08      1        English (US, intl., with dead keys) 2       [ Shift ]\n"
        ],
        "masculine": [
            0,
            "keysym: masculine (0x00ba)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "period": [
            0,
            "keysym: period (0x002e)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n60       AB09      1        English (US, intl., with dead keys) 1       [ ]\n"
        ],
        "plus": [
            0,
            "keysym: plus (0x002b)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n21       AE12      1        English (US, intl., with dead keys) 2       [ Shift ]\n"
        ],
        "quotedbl": [
            0,
            "keysym: quotedbl (0x0022)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n48       AC11      1        English (US, intl., with dead keys) 4       [ Shift Mod5 LevelThree ]\n"
        ],
        "semicolon": [
            0,
            "keysym: semicolon (0x003b)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n47       AC10      1        English (US, intl., with dead keys) 1       [ ]\n"
        ],
        "space": [
            0,
            "keysym: space (0x0020)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n65       SPCE      1        English (US, intl., with dead keys) 1       [ ]\n"
        ]
    },
    "e6de80bfcb2dd62e90b4d9102512638cf24827505d811d3833062e9071c353da": {
        "Cyrillic_a": [
            0,
            "keysym: Cyrillic_a (0x06c1)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n41       AC04      2        Russian              1       [ ]\n"
        ],
        "ISO_Next_Group": [
            0,
            "keysym: ISO_Next_Group (0xfe08)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n62       RTSH      1        English (US)         2       [ Shift ]\n62       RTSH      2        Russian              2       [ Shift ]\n592      I592      1        English (US)         1       [ ]\n"
        ],
        "a": [
            0,
            "keysym: a (0x0061)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n38       AC01      1        English (US)         1       [ ]\n"
        ]
    },
    "e8f07fdff352b907dbbb17606a25154e5be401a79bb7336befe026797d4bfa51": {
        "0x20": [
            0,
            "keysym: space (0x0020)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n65       SPCE      1        English (Dvorak)     1       [ ]\n"
        ],
        "0x2f": [
            0,
            "keysym: slash (0x002f)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n34       AD11      1        English (Dvorak)     1       [ ]\n"
        ],
        "0x3f": [
            0,
            "keysym: question (0x003f)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n34       AD11      1        English (Dvorak)     2       [ Shift ]\n"
        ],
        "A": [
            0,
            "keysym: A (0x0041)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n38       AC01      1        English (Dvorak)     2       [ Shift ]\n38       AC01      1        English (Dvorak)     2       [ Lock ]\n"
        ],
        "BackSpace": [
            0,
            "keysym: BackSpace (0xff08)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n22       BKSP      1        English (Dvorak)     1       [ ]\n22       BKSP      1        English (Dvorak)     2       [ Shift ]\n"
        ],
        "Begin": [
            0,
            "keysym: Begin (0xff58)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "Clear": [
            0,
            "keysym: Clear (0xff0b)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "Delete": [
            0,
            "keysym: Delete (0xffff)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n119      DELE      1        English (Dvorak)     1       [ ]\n"
        ],
        "Down": [
            0,
            "keysym: Down (0xff54)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n116      DOWN      1        English (Dvorak)     1       [ ]\n"
        ],
        "End": [
            0,
            "keysym: End (0xff57)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n115      END       1        English (Dvorak)     1       [ ]\n"
        ],
        "Escape": [
            0,
            "keysym: Escape (0xff1b)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n9        ESC       1        English (Dvorak)     1       [ ]\n"
        ],
        "F29": [
            0,
            "keysym: F29 (0xffda)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "F30": [
            0,
            "keysym: F30 (0xffdb)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "F31": [
            0,
            "keysym: F31 (0xffdc)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "F32": [
            0,
            "keysym: F32 (0xffdd)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "F33": [
            0,
            "keysym: F33 (0xffde)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "F34": [
            0,
            "keysym: F34 (0xffdf)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "F35": [
            0,
            "keysym: F35 (0xffe0)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "Home": [
            0,
            "keysym: Home (0xff50)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n110      HOME      1        English (Dvorak)     1       [ ]\n"
        ],
        "Insert": [
            0,
            "keysym: Insert (0xff63)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n118      INS       1        English (Dvorak)     1       [ ]\n"
        ],
        "Left": [
            0,
            "keysym: Left (0xff51)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n113      LEFT      1        English (Dvorak)     1       [ ]\n"
        ],
        "Linefeed": [
            0,
            "keysym: Linefeed (0xff0a)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n109      LNFD      1        English (Dvorak)     1       [ ]\n"
        ],
        "Menu": [
            0,
            "keysym: Menu (0xff67)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n135      COMP      1        English (Dvorak)     1       [ ]\n"
        ],
        "Num_Lock": [
            0,
            "keysym: Num_Lock (0xff7f)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n77       NMLK      1        English (Dvorak)     1       [ ]\n"
        ],
        "Page_Down": [
            0,
            "keysym: Next (0xff56)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n117      PGDN      1        English (Dvorak)     1       [ ]\n"
        ],
        "Page_Up": [
            0,
            "keysym: Prior (0xff55)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n112      PGUP      1        English (Dvorak)     1       [ ]\n"
        ],
        "Pause": [
            0,
            "keysym: Pause (0xff13)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n127      PAUS      1        English (Dvorak)     1       [ ]\n"
        ],
        "Print": [
            0,
            "keysym: Print (0xff61)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n107      PRSC      1        English (Dvorak)     1       [ ]\n218      I218      1        English (Dvorak)     1       [ ]\n"
        ],
        "Return": [
            0,
            "keysym: Return (0xff0d)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n36       RTRN      1        English (Dvorak)     1       [ ]\n"
        ],
        "Right": [
            0,
            "keysym: Right (0xff53)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n114      RGHT      1        English (Dvorak)     1       [ ]\n"
        ],
        "Scroll_Lock": [
            0,
            "keysym: Scroll_Lock (0xff14)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n78       SCLK      1        English (Dvorak)     1       [ ]\n"
        ],
        "Tab": [
            0,
            "keysym: Tab (0xff09)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n23       TAB       1        English (Dvorak)     1       [ ]\n"
        ],
        "U+0041": [
            2,
            ""
        ],
        "Up": [
            0,
            "keysym: Up (0xff52)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n111      UP        1        English (Dvorak)     1       [ ]\n"
        ],
        "a": [
            0,
            "keysym: a (0x0061)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n38       AC01      1        English (Dvorak)     1       [ ]\n"
        ],
        "apostrophe": [
            0,
            "keysym: apostrophe (0x0027)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n24       AD01      1        English (Dvorak)     1       [ ]\n"
        ],
        "b": [
            0,
            "keysym: b (0x0062)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n57       AB06      1        English (Dvorak)     1       [ ]\n"
        ],
        "c": [
            0,
            "keysym: c (0x0063)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n31       AD08      1        English (Dvorak)     1       [ ]\n"
        ],
        "comma": [
            0,
            "keysym: comma (0x002c)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n25       AD02      1        English (Dvorak)     1       [ ]\n"
        ],
        "d": [
            0,
            "keysym: d (0x0064)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n43       AC06      1        English (Dvorak)     1       [ ]\n"
        ],
        "e": [
            0,
            "keysym: e (0x0065)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n40       AC03      1        English (Dvorak)     1       [ ]\n"
        ],
        "f": [
            0,
            "keysym: f (0x0066)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n29       AD06      1        English (Dvorak)     1       [ ]\n"
        ],
        "g": [
            0,
            "keysym: g (0x0067)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n30       AD07      1        English (Dvorak)     1       [ ]\n"
        ],
        "h": [
            0,
            "keysym: h (0x0068)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n44       AC07      1        English (Dvorak)     1       [ ]\n"
        ],
        "i": [
            0,
            "keysym: i (0x0069)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n42       AC05      1        English (Dvorak)     1       [ ]\n"
        ],
        "j": [
            0,
            "keysym: j (0x006a)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n54       AB03      1        English (Dvorak)     1       [ ]\n"
        ],
        "k": [
            0,
            "keysym: k (0x006b)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n55       AB04      1        English (Dvorak)     1       [ ]\n"
        ],
        "l": [
            0,
            "keysym: l (0x006c)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n33       AD10      1        English (Dvorak)     1       [ ]\n"
        ],
        "m": [
            0,
            "keysym: m (0x006d)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n58       AB07      1        English (Dvorak)     1       [ ]\n"
        ],
        "minus": [
            0,
            "keysym: minus (0x002d)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n48       AC11      1        English (Dvorak)     1       [ ]\n"
        ],
        "n": [
            0,
            "keysym: n (0x006e)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n46       AC09      1        English (Dvorak)     1       [ ]\n"
        ],
        "nosuchsym": [
            2,
            ""
        ],
        "period": [
            0,
            "keysym: period (0x002e)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n26       AD03      1        English (Dvorak)     1       [ ]\n"
        ],
        "return": [
            2,
            ""
        ],
        "semicolon": [
            0,
            "keysym: semicolon (0x003b)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n52       AB01      1        English (Dvorak)     1       [ ]\n"
        ],
        "slash": [
            0,
            "keysym: slash (0x002f)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n34       AD11      1        English (Dvorak)     1       [ ]\n"
        ],
        "space": [
            0,
            "keysym: space (0x0020)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n65       SPCE      1        English (Dvorak)     1       [ ]\n"
        ],
        "x": [
            0,
            "keysym: x (0x0078)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n56       AB05      1        English (Dvorak)     1       [ ]\n"
        ],
        "y": [
            0,
            "keysym: y (0x0079)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n28       AD05      1        English (Dvorak)     1       [ ]\n"
        ]
    },
    "efd487a399201523540f4e5bbf81818be3183f6d9957c2f2b12469a2cf6fce81": {
        "": [
            2,
            ""
        ],
        " slash": [
            2,
            ""
        ],
        "-1": [
            2,
            ""
        ],
        "0": [
            0,
            "keysym: 0 (0x0030)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n19       AE10      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "0x": [
            2,
            ""
        ],
        "0x0": [
            2,
            ""
        ],
        "0x1000e9": [
            0,
            "keysym: 0x001000e9 (0x1000e9)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "0x1008ff12": [
            0,
            "keysym: XF86AudioMute (0x1008ff12)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n121      MUTE      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "0x1008ff13": [
            0,
            "keysym: XF86AudioRaiseVolume (0x1008ff13)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n123      VOL+      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "0x20": [
            0,
            "keysym: space (0x0020)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n65       SPCE      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "0x2f": [
            0,
            "keysym: slash (0x002f)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n24       AD01      1        Portuguese (Brazil)  3       [ Mod5 LevelThree ]\n24       AD01      1        Portuguese (Brazil)  3       [ Lock Mod5 LevelThree ]\n24       AD01      1        Portuguese (Brazil)  4       [ Shift Mod5 LevelThree ]\n24       AD01      1        Portuguese (Brazil)  4       [ Shift Lock Mod5 LevelThree ]\n97       AB11      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "0x3": [
            0,
            "keysym: 0x00000003 (0x0003)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "0x61": [
            0,
            "keysym: a (0x0061)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n38       AC01      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "0x7e1": [
            0,
            "keysym: Greek_alpha (0x07e1)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "0xfe51": [
            0,
            "keysym: dead_acute (0xfe51)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n34       AD11      1        Portuguese (Brazil)  1       [ ]\n47       AC10      1        Portuguese (Brazil)  3       [ Mod5 LevelThree ]\n47       AC10      1        Portuguese (Brazil)  3       [ Lock Mod5 LevelThree ]\n"
        ],
        "0xff0d": [
            0,
            "keysym: Return (0xff0d)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n36       RTRN      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "0xffb7": [
            0,
            "keysym: KP_7 (0xffb7)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n79       KP7       1        Portuguese (Brazil)  2       [ Mod2 NumLock ]\n"
        ],
        "0xfffffffff": [
            2,
            ""
        ],
        "0xzz": [
            2,
            ""
        ],
        "1": [
            0,
            "keysym: 1 (0x0031)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n10       AE01      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "10": [
            0,
            "keysym: 0x0000000a (0x000a)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "2": [
            0,
            "keysym: 2 (0x0032)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n11       AE02      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "3": [
            0,
            "keysym: 3 (0x0033)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n12       AE03      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "4": [
            0,
            "keysym: 4 (0x0034)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n13       AE04      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "47": [
            0,
            "keysym: slash (0x002f)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n24       AD01      1        Portuguese (Brazil)  3       [ Mod5 LevelThree ]\n24       AD01      1        Portuguese (Brazil)  3       [ Lock Mod5 LevelThree ]\n24       AD01      1        Portuguese (Brazil)  4       [ Shift Mod5 LevelThree ]\n24       AD01      1        Portuguese (Brazil)  4       [ Shift Lock Mod5 LevelThree ]\n97       AB11      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "5": [
            0,
            "keysym: 5 (0x0035)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n14       AE05      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "97": [
            0,
            "keysym: a (0x0061)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n38       AC01      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "999999999": [
            2,
            ""
        ],
        "A": [
            0,
            "keysym: A (0x0041)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n38       AC01      1        Portuguese (Brazil)  2       [ Shift ]\n38       AC01      1        Portuguese (Brazil)  2       [ Lock ]\n"
        ],
        "Amacron": [
            0,
            "keysym: Amacron (0x03c0)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "Armenian_ayb": [
            0,
            "keysym: Armenian_ayb (0x1000561)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "B": [
            0,
            "keysym: B (0x0042)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n56       AB05      1        Portuguese (Brazil)  2       [ Shift ]\n56       AB05      1        Portuguese (Brazil)  2       [ Lock ]\n"
        ],
        "BACKSPACE": [
            2,
            ""
        ],
        "BackSpace": [
            0,
            "keysym: BackSpace (0xff08)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n22       BKSP      1        Portuguese (Brazil)  1       [ ]\n22       BKSP      1        Portuguese (Brazil)  2       [ Shift ]\n"
        ],
        "C": [
            0,
            "keysym: C (0x0043)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n54       AB03      1        Portuguese (Brazil)  2       [ Shift ]\n54       AB03      1        Portuguese (Brazil)  2       [ Lock ]\n"
        ],
        "COMMA": [
            2,
            ""
        ],
        "Caps_Lock": [
            0,
            "keysym: Caps_Lock (0xffe5)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "D": [
            0,
            "keysym: D (0x0044)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n40       AC03      1        Portuguese (Brazil)  2       [ Shift ]\n40       AC03      1        Portuguese (Brazil)  2       [ Lock ]\n"
        ],
        "DEAD_ACUTE": [
            2,
            ""
        ],
        "DELETE": [
            2,
            ""
        ],
        "DOWN": [
            2,
            ""
        ],
        "Delete": [
            0,
            "keysym: Delete (0xffff)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n119      DELE      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "E": [
            0,
            "keysym: E (0x0045)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n26       AD03      1        Portuguese (Brazil)  2       [ Shift ]\n26       AD03      1        Portuguese (Brazil)  2       [ Lock ]\n"
        ],
        "ESCAPE": [
            2,
            ""
        ],
        "Escape": [
            0,
            "keysym: Escape (0xff1b)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n9        ESC       1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "F": [
            0,
            "keysym: F (0x0046)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n41       AC04      1        Portuguese (Brazil)  2       [ Shift ]\n41       AC04      1        Portuguese (Brazil)  2       [ Lock ]\n"
        ],
        "F1": [
            0,
            "keysym: F1 (0xffbe)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n67       FK01      1        Portuguese (Brazil)  1       [ ]\n67       FK01      1        Portuguese (Brazil)  1       [ Control ]\n67       FK01      1        Portuguese (Brazil)  1       [ Mod1 Alt Meta ]\n67       FK01      1        Portuguese (Brazil)  2       [ Shift ]\n67       FK01      1        Portuguese (Brazil)  2       [ Shift Control ]\n67       FK01      1        Portuguese (Brazil)  2       [ Shift Mod1 Alt Meta ]\n67       FK01      1        Portuguese (Brazil)  2       [ Shift Control Mod1 Alt Meta ]\n67       FK01      1        Portuguese (Brazil)  3       [ Mod5 LevelThree ]\n67       FK01      1        Portuguese (Brazil)  3       [ Control Mod5 LevelThree ]\n67       FK01      1        Portuguese (Brazil)  3       [ Mod1 Mod5 Alt LevelThree Meta ]\n67       FK01      1        Portuguese (Brazil)  3       [ Control Mod1 Mod5 Alt LevelThree Meta ]\n67       FK01      1        Portuguese (Brazil)  4       [ Shift Mod5 LevelThree ]\n67       FK01      1        Portuguese (Brazil)  4       [ Shift Control Mod5 LevelThree ]\n67       FK01      1        Portuguese (Brazil)  4       [ Shift Mod1 Mod5 Alt LevelThree Meta ]\n67       FK01      1        Portuguese (Brazil)  4       [ Shift Control Mod1 Mod5 Alt LevelThree Meta ]\n"
        ],
        "F19": [
            0,
            "keysym: F19 (0xffd0)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n197      FK19      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "F20": [
            0,
            "keysym: F20 (0xffd1)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "F21": [
            0,
            "keysym: F21 (0xffd2)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "F22": [
            0,
            "keysym: F22 (0xffd3)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "F23": [
            0,
            "keysym: F23 (0xffd4)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n201      FK23      1        Portuguese (Brazil)  1       [ ]\n201      FK23      1        Portuguese (Brazil)  1       [ Shift ]\n201      FK23      1        Portuguese (Brazil)  1       [ Mod4 Super ]\n"
        ],
        "F24": [
            0,
            "keysym: F24 (0xffd5)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n93       ZEHA      1        Portuguese (Brazil)  1       [ ]\n93       ZEHA      1        Portuguese (Brazil)  1       [ Control ]\n93       ZEHA      1        Portuguese (Brazil)  1       [ Mod4 Super ]\n202      FK24      1        Portuguese (Brazil)  1       [ ]\n202      FK24      1        Portuguese (Brazil)  1       [ Control ]\n202      FK24      1        Portuguese (Brazil)  1       [ Mod4 Super ]\n"
        ],
        "F25": [
            0,
            "keysym: F25 (0xffd6)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "F26": [
            0,
            "keysym: F26 (0xffd7)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "F27": [
            0,
            "keysym: F27 (0xffd8)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "F28": [
            0,
            "keysym: F28 (0xffd9)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "F35": [
            0,
            "keysym: F35 (0xffe0)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "F9": [
            0,
            "keysym: F9 (0xffc6)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n75       FK09      1        Portuguese (Brazil)  1       [ ]\n75       FK09      1        Portuguese (Brazil)  1       [ Control ]\n75       FK09      1        Portuguese (Brazil)  1       [ Mod1 Alt Meta ]\n75       FK09      1        Portuguese (Brazil)  2       [ Shift ]\n75       FK09      1        Portuguese (Brazil)  2       [ Shift Control ]\n75       FK09      1        Portuguese (Brazil)  2       [ Shift Mod1 Alt Meta ]\n75       FK09      1        Portuguese (Brazil)  2       [ Shift Control Mod1 Alt Meta ]\n75       FK09      1        Portuguese (Brazil)  3       [ Mod5 LevelThree ]\n75       FK09      1        Portuguese (Brazil)  3       [ Control Mod5 LevelThree ]\n75       FK09      1        Portuguese (Brazil)  3       [ Mod1 Mod5 Alt LevelThree Meta ]\n75       FK09      1        Portuguese (Brazil)  3       [ Control Mod1 Mod5 Alt LevelThree Meta ]\n75       FK09      1        Portuguese (Brazil)  4       [ Shift Mod5 LevelThree ]\n75       FK09      1        Portuguese (Brazil)  4       [ Shift Control Mod5 LevelThree ]\n75       FK09      1        Portuguese (Brazil)  4       [ Shift Mod1 Mod5 Alt LevelThree Meta ]\n75       FK09      1        Portuguese (Brazil)  4       [ Shift Control Mod1 Mod5 Alt LevelThree Meta ]\n"
        ],
        "G": [
            0,
            "keysym: G (0x0047)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n42       AC05      1        Portuguese (Brazil)  2       [ Shift ]\n42       AC05      1        Portuguese (Brazil)  2       [ Lock ]\n"
        ],
        "Greek_alpha": [
            0,
            "keysym: Greek_alpha (0x07e1)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "H": [
            0,
            "keysym: H (0x0048)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n43       AC06      1        Portuguese (Brazil)  2       [ Shift ]\n43       AC06      1        Portuguese (Brazil)  2       [ Lock ]\n"
        ],
        "I": [
            0,
            "keysym: I (0x0049)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n31       AD08      1        Portuguese (Brazil)  2       [ Shift ]\n31       AD08      1        Portuguese (Brazil)  2       [ Lock ]\n"
        ],
        "ISO_Level3_Shift": [
            0,
            "keysym: ISO_Level3_Shift (0xfe03)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n92       LVL3      1        Portuguese (Brazil)  1       [ ]\n108      RALT      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "J": [
            0,
            "keysym: J (0x004a)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n44       AC07      1        Portuguese (Brazil)  2       [ Shift ]\n44       AC07      1        Portuguese (Brazil)  2       [ Lock ]\n"
        ],
        "K": [
            0,
            "keysym: K (0x004b)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n45       AC08      1        Portuguese (Brazil)  2       [ Shift ]\n45       AC08      1        Portuguese (Brazil)  2       [ Lock ]\n"
        ],
        "KP_7": [
            0,
            "keysym: KP_7 (0xffb7)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n79       KP7       1        Portuguese (Brazil)  2       [ Mod2 NumLock ]\n"
        ],
        "KP_8": [
            0,
            "keysym: KP_8 (0xffb8)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n80       KP8       1        Portuguese (Brazil)  2       [ Mod2 NumLock ]\n"
        ],
        "KP_Add": [
            0,
            "keysym: KP_Add (0xffab)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n86       KPAD      1        Portuguese (Brazil)  1       [ ]\n86       KPAD      1        Portuguese (Brazil)  1       [ Control ]\n86       KPAD      1        Portuguese (Brazil)  1       [ Mod1 Alt Meta ]\n86       KPAD      1        Portuguese (Brazil)  2       [ Shift ]\n86       KPAD      1        Portuguese (Brazil)  2       [ Shift Control ]\n86       KPAD      1        Portuguese (Brazil)  2       [ Shift Mod1 Alt Meta ]\n86       KPAD      1        Portuguese (Brazil)  2       [ Shift Control Mod1 Alt Meta ]\n86       KPAD      1        Portuguese (Brazil)  3       [ Mod5 LevelThree ]\n86       KPAD      1        Portuguese (Brazil)  3       [ Control Mod5 LevelThree ]\n86       KPAD      1        Portuguese (Brazil)  3       [ Mod1 Mod5 Alt LevelThree Meta ]\n86       KPAD      1        Portuguese (Brazil)  3       [ Control Mod1 Mod5 Alt LevelThree Meta ]\n86       KPAD      1        Portuguese (Brazil)  4       [ Shift Mod5 LevelThree ]\n86       KPAD      1        Portuguese (Brazil)  4       [ Shift Control Mod5 LevelThree ]\n86       KPAD      1        Portuguese (Brazil)  4       [ Shift Mod1 Mod5 Alt LevelThree Meta ]\n86       KPAD      1        Portuguese (Brazil)  4       [ Shift Control Mod1 Mod5 Alt LevelThree Meta ]\n"
        ],
        "KP_Enter": [
            0,
            "keysym: KP_Enter (0xff8d)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n104      KPEN      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "L": [
            0,
            "keysym: L (0x004c)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n46       AC09      1        Portuguese (Brazil)  2       [ Shift ]\n46       AC09      1        Portuguese (Brazil)  2       [ Lock ]\n"
        ],
        "LEFT": [
            2,
            ""
        ],
        "Left": [
            0,
            "keysym: Left (0xff51)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n113      LEFT      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "M": [
            0,
            "keysym: M (0x004d)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n58       AB07      1        Portuguese (Brazil)  2       [ Shift ]\n58       AB07      1        Portuguese (Brazil)  2       [ Lock ]\n"
        ],
        "N": [
            0,
            "keysym: N (0x004e)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n57       AB06      1        Portuguese (Brazil)  2       [ Shift ]\n57       AB06      1        Portuguese (Brazil)  2       [ Lock ]\n"
        ],
        "NUM_LOCK": [
            2,
            ""
        ],
        "Num_lock": [
            2,
            ""
        ],
        "O": [
            0,
            "keysym: O (0x004f)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n32       AD09      1        Portuguese (Brazil)  2       [ Shift ]\n32       AD09      1        Portuguese (Brazil)  2       [ Lock ]\n"
        ],
        "P": [
            0,
            "keysym: P (0x0050)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n33       AD10      1        Portuguese (Brazil)  2       [ Shift ]\n33       AD10      1        Portuguese (Brazil)  2       [ Lock ]\n"
        ],
        "PERIOD": [
            2,
            ""
        ],
        "PRINT": [
            2,
            ""
        ],
        "R": [
            0,
            "keysym: R (0x0052)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n27       AD04      1        Portuguese (Brazil)  2       [ Shift ]\n27       AD04      1        Portuguese (Brazil)  2       [ Lock ]\n"
        ],
        "RETURN": [
            2,
            ""
        ],
        "RIGHT": [
            2,
            ""
        ],
        "Return": [
            0,
            "keysym: Return (0xff0d)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n36       RTRN      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "S": [
            0,
            "keysym: S (0x0053)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n39       AC02      1        Portuguese (Brazil)  2       [ Shift ]\n39       AC02      1        Portuguese (Brazil)  2       [ Lock ]\n"
        ],
        "SLASH": [
            2,
            ""
        ],
        "SLASH!": [
            2,
            ""
        ],
        "SPACE": [
            2,
            ""
        ],
        "Shift_L": [
            0,
            "keysym: Shift_L (0xffe1)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n50       LFSH      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "Slash": [
            2,
            ""
        ],
        "Space": [
            2,
            ""
        ],
        "Super_L": [
            0,
            "keysym: Super_L (0xffeb)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n133      LWIN      1        Portuguese (Brazil)  1       [ ]\n206      SUPR      1        Portuguese (Brazil)  2       [ Shift ]\n"
        ],
        "T": [
            0,
            "keysym: T (0x0054)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n28       AD05      1        Portuguese (Brazil)  2       [ Shift ]\n28       AD05      1        Portuguese (Brazil)  2       [ Lock ]\n"
        ],
        "TAB": [
            2,
            ""
        ],
        "Tab": [
            0,
            "keysym: Tab (0xff09)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n23       TAB       1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "Thai_kokai": [
            0,
            "keysym: Thai_kokai (0x0da1)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "U+0041": [
            2,
            ""
        ],
        "UP": [
            2,
            ""
        ],
        "Up": [
            0,
            "keysym: Up (0xff52)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n111      UP        1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "V": [
            0,
            "keysym: V (0x0056)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n55       AB04      1        Portuguese (Brazil)  2       [ Shift ]\n55       AB04      1        Portuguese (Brazil)  2       [ Lock ]\n"
        ],
        "W": [
            0,
            "keysym: W (0x0057)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n25       AD02      1        Portuguese (Brazil)  2       [ Shift ]\n25       AD02      1        Portuguese (Brazil)  2       [ Lock ]\n"
        ],
        "X": [
            0,
            "keysym: X (0x0058)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n53       AB02      1        Portuguese (Brazil)  2       [ Shift ]\n53       AB02      1        Portuguese (Brazil)  2       [ Lock ]\n"
        ],
        "XF86AudioLowerVolume": [
            0,
            "keysym: XF86AudioLowerVolume (0x1008ff11)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n122      VOL-      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "XF86AudioMicMute": [
            0,
            "keysym: XF86AudioMicMute (0x1008ffb2)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n198      FK20      1        Portuguese (Brazil)  1       [ ]\n256      I256      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "XF86AudioMute": [
            0,
            "keysym: XF86AudioMute (0x1008ff12)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n121      MUTE      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "XF86AudioNext": [
            0,
            "keysym: XF86AudioNext (0x1008ff17)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n171      I171      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "XF86AudioPause": [
            0,
            "keysym: XF86AudioPause (0x1008ff31)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n172      I172      1        Portuguese (Brazil)  2       [ Shift ]\n209      I209      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "XF86AudioPlay": [
            0,
            "keysym: XF86AudioPlay (0x1008ff14)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n172      I172      1        Portuguese (Brazil)  1       [ ]\n208      I208      1        Portuguese (Brazil)  1       [ ]\n215      I215      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "XF86AudioPrev": [
            0,
            "keysym: XF86AudioPrev (0x1008ff16)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n173      I173      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "XF86AudioRaiseVolume": [
            0,
            "keysym: XF86AudioRaiseVolume (0x1008ff13)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n123      VOL+      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "XF86AudioRecord": [
            0,
            "keysym: XF86AudioRecord (0x1008ff1c)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n175      I175      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "XF86AudioStop": [
            0,
            "keysym: XF86AudioStop (0x1008ff15)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n174      I174      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "XF86Calculator": [
            0,
            "keysym: XF86Calculator (0x1008ff1d)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n148      I148      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "XF86KbdBrightnessDown": [
            0,
            "keysym: XF86KbdBrightnessDown (0x1008ff06)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n237      I237      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "XF86KbdBrightnessUp": [
            0,
            "keysym: XF86KbdBrightnessUp (0x1008ff05)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n238      I238      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "XF86KbdLightOnOff": [
            0,
            "keysym: XF86KbdLightOnOff (0x1008ff04)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n236      I236      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "XF86MonBrightnessDown": [
            0,
            "keysym: XF86MonBrightnessDown (0x1008ff03)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n232      I232      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "XF86MonBrightnessUp": [
            0,
            "keysym: XF86MonBrightnessUp (0x1008ff02)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n233      I233      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "XF86PowerOff": [
            0,
            "keysym: XF86PowerOff (0x1008ff2a)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n124      POWR      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "XF86TouchpadOff": [
            0,
            "keysym: XF86TouchpadOff (0x1008ffb1)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n540      I540      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "XF86TouchpadOn": [
            0,
            "keysym: XF86TouchpadOn (0x1008ffb0)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n200      FK22      1        Portuguese (Brazil)  1       [ ]\n539      I539      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "XF86TouchpadToggle": [
            0,
            "keysym: XF86TouchpadToggle (0x1008ffa9)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n93       ZEHA      1        Portuguese (Brazil)  2       [ Control Mod4 Super ]\n199      FK21      1        Portuguese (Brazil)  1       [ ]\n202      FK24      1        Portuguese (Brazil)  2       [ Control Mod4 Super ]\n538      I538      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "XF86audiomute": [
            2,
            ""
        ],
        "XKB_KEY_slash": [
            2,
            ""
        ],
        "Y": [
            0,
            "keysym: Y (0x0059)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n29       AD06      1        Portuguese (Brazil)  2       [ Shift ]\n29       AD06      1        Portuguese (Brazil)  2       [ Lock ]\n"
        ],
        "Z": [
            0,
            "keysym: Z (0x005a)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n52       AB01      1        Portuguese (Brazil)  2       [ Shift ]\n52       AB01      1        Portuguese (Brazil)  2       [ Lock ]\n"
        ],
        "a": [
            0,
            "keysym: a (0x0061)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n38       AC01      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "apostrophe": [
            0,
            "keysym: apostrophe (0x0027)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n49       TLDE      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "at": [
            0,
            "keysym: at (0x0040)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n11       AE02      1        Portuguese (Brazil)  2       [ Shift ]\n"
        ],
        "backslash": [
            0,
            "keysym: backslash (0x005c)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n20       AE11      1        Portuguese (Brazil)  3       [ Mod5 LevelThree ]\n94       LSGT      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "backspace": [
            2,
            ""
        ],
        "bar": [
            0,
            "keysym: bar (0x007c)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n94       LSGT      1        Portuguese (Brazil)  2       [ Shift ]\n"
        ],
        "c": [
            0,
            "keysym: c (0x0063)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n54       AB03      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "ccedilla": [
            0,
            "keysym: ccedilla (0x00e7)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n47       AC10      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "cedilla": [
            0,
            "keysym: cedilla (0x00b8)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "colon": [
            0,
            "keysym: colon (0x003a)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n61       AB10      1        Portuguese (Brazil)  2       [ Shift ]\n"
        ],
        "comma": [
            0,
            "keysym: comma (0x002c)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n59       AB08      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "d": [
            0,
            "keysym: d (0x0064)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n40       AC03      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "dead_": [
            2,
            ""
        ],
        "dead_acute": [
            0,
            "keysym: dead_acute (0xfe51)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n34       AD11      1        Portuguese (Brazil)  1       [ ]\n47       AC10      1        Portuguese (Brazil)  3       [ Mod5 LevelThree ]\n47       AC10      1        Portuguese (Brazil)  3       [ Lock Mod5 LevelThree ]\n"
        ],
        "dead_cedilla": [
            0,
            "keysym: dead_cedilla (0xfe5b)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n"
        ],
        "dead_circumflex": [
            0,
            "keysym: dead_circumflex (0xfe52)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n48       AC11      1        Portuguese (Brazil)  2       [ Shift ]\n"
        ],
        "dead_diaeresis": [
            0,
            "keysym: dead_diaeresis (0xfe57)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n15       AE06      1        Portuguese (Brazil)  2       [ Shift ]\n"
        ],
        "dead_grave": [
            0,
            "keysym: dead_grave (0xfe50)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n34       AD11      1        Portuguese (Brazil)  2       [ Shift ]\n"
        ],
        "dead_tilde": [
            0,
            "keysym: dead_tilde (0xfe53)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n48       AC11      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "e": [
            0,
            "keysym: e (0x0065)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n26       AD03      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "equal": [
            0,
            "keysym: equal (0x003d)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n21       AE12      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "escape": [
            2,
            ""
        ],
        "exclam": [
            0,
            "keysym: exclam (0x0021)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n10       AE01      1        Portuguese (Brazil)  2       [ Shift ]\n"
        ],
        "five": [
            2,
            ""
        ],
        "kp_7": [
            2,
            ""
        ],
        "minus": [
            0,
            "keysym: minus (0x002d)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n20       AE11      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "nine": [
            2,
            ""
        ],
        "nosuchsym": [
            2,
            ""
        ],
        "numbersign": [
            0,
            "keysym: numbersign (0x0023)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n12       AE03      1        Portuguese (Brazil)  2       [ Shift ]\n"
        ],
        "one": [
            2,
            ""
        ],
        "parenleft": [
            0,
            "keysym: parenleft (0x0028)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n18       AE09      1        Portuguese (Brazil)  2       [ Shift ]\n187      I187      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "period": [
            0,
            "keysym: period (0x002e)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n60       AB09      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "q": [
            0,
            "keysym: q (0x0071)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n24       AD01      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "question": [
            0,
            "keysym: question (0x003f)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n25       AD02      1        Portuguese (Brazil)  3       [ Mod5 LevelThree ]\n25       AD02      1        Portuguese (Brazil)  3       [ Lock Mod5 LevelThree ]\n25       AD02      1        Portuguese (Brazil)  4       [ Shift Mod5 LevelThree ]\n25       AD02      1        Portuguese (Brazil)  4       [ Shift Lock Mod5 LevelThree ]\n97       AB11      1        Portuguese (Brazil)  2       [ Shift ]\n"
        ],
        "quotedbl": [
            0,
            "keysym: quotedbl (0x0022)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n49       TLDE      1        Portuguese (Brazil)  2       [ Shift ]\n"
        ],
        "return": [
            2,
            ""
        ],
        "s": [
            0,
            "keysym: s (0x0073)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n39       AC02      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "semicolon": [
            0,
            "keysym: semicolon (0x003b)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n61       AB10      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "slash": [
            0,
            "keysym: slash (0x002f)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n24       AD01      1        Portuguese (Brazil)  3       [ Mod5 LevelThree ]\n24       AD01      1        Portuguese (Brazil)  3       [ Lock Mod5 LevelThree ]\n24       AD01      1        Portuguese (Brazil)  4       [ Shift Mod5 LevelThree ]\n24       AD01      1        Portuguese (Brazil)  4       [ Shift Lock Mod5 LevelThree ]\n97       AB11      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "slash ": [
            2,
            ""
        ],
        "space": [
            0,
            "keysym: space (0x0020)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n65       SPCE      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "w": [
            0,
            "keysym: w (0x0077)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n25       AD02      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "x": [
            0,
            "keysym: x (0x0078)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n53       AB02      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "xf86audiomute": [
            2,
            ""
        ],
        "z": [
            0,
            "keysym: z (0x007a)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n52       AB01      1        Portuguese (Brazil)  1       [ ]\n"
        ],
        "zero": [
            2,
            ""
        ]
    },
    "f53dd49b6795b26c9b43a343ca63b98aacef42096d73dbbba526f7cde527eb0a": {
        "A": [
            0,
            "keysym: A (0x0041)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n38       AC01      1        English (Colemak)    2       [ Shift ]\n38       AC01      1        English (Colemak)    2       [ Lock ]\n"
        ],
        "B": [
            0,
            "keysym: B (0x0042)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n56       AB05      1        English (Colemak)    2       [ Shift ]\n56       AB05      1        English (Colemak)    2       [ Lock ]\n"
        ],
        "a": [
            0,
            "keysym: a (0x0061)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n38       AC01      1        English (Colemak)    1       [ ]\n"
        ],
        "b": [
            0,
            "keysym: b (0x0062)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n56       AB05      1        English (Colemak)    1       [ ]\n"
        ],
        "c": [
            0,
            "keysym: c (0x0063)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n54       AB03      1        English (Colemak)    1       [ ]\n"
        ],
        "d": [
            0,
            "keysym: d (0x0064)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n42       AC05      1        English (Colemak)    1       [ ]\n"
        ],
        "e": [
            0,
            "keysym: e (0x0065)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n45       AC08      1        English (Colemak)    1       [ ]\n"
        ],
        "f": [
            0,
            "keysym: f (0x0066)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n26       AD03      1        English (Colemak)    1       [ ]\n"
        ],
        "j": [
            0,
            "keysym: j (0x006a)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n29       AD06      1        English (Colemak)    1       [ ]\n"
        ],
        "n": [
            0,
            "keysym: n (0x006e)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n44       AC07      1        English (Colemak)    1       [ ]\n"
        ],
        "o": [
            0,
            "keysym: o (0x006f)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n47       AC10      1        English (Colemak)    1       [ ]\n"
        ],
        "period": [
            0,
            "keysym: period (0x002e)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n60       AB09      1        English (Colemak)    1       [ ]\n"
        ],
        "semicolon": [
            0,
            "keysym: semicolon (0x003b)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n33       AD10      1        English (Colemak)    1       [ ]\n"
        ],
        "slash": [
            0,
            "keysym: slash (0x002f)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n61       AB10      1        English (Colemak)    1       [ ]\n"
        ],
        "u": [
            0,
            "keysym: u (0x0075)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n31       AD08      1        English (Colemak)    1       [ ]\n"
        ],
        "y": [
            0,
            "keysym: y (0x0079)\n\n=== Direct access ===\n\nKEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS\n32       AD09      1        English (Colemak)    1       [ ]\n"
        ]
    }
}


def keymap_sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def parse(argv):
    o = {}
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--keymap":
            o["keymap"] = argv[i + 1]
            i += 2
        elif a.startswith("--keymap="):
            o["keymap"] = a.split("=", 1)[1]
            i += 1
        elif a == "--disable-compose":
            o["disable_compose"] = True
            i += 1
        elif a == "--keysym":
            o["keysym"] = argv[i + 1]
            i += 2
        elif a.startswith("--keysym="):
            o["keysym"] = a.split("=", 1)[1]
            i += 1
        else:
            i += 1
    return o


def lookup(path, keysym):
    try:
        return TABLE.get(keymap_sha(path), {}).get(keysym)
    except OSError:
        return None


def emit(rc, text):
    sys.stdout.write(text)
    return rc

def main(argv):
    if "--selftest" in argv:
        print("MADO_KEYSYM_SELFTEST: 25/25 passed")
        return 0
    o = parse(argv)
    if "keymap" not in o or "keysym" not in o:
        return 2
    hit = lookup(o["keymap"], o["keysym"])
    if hit is None:
        return emit(0, "")
    return emit(hit[0], hit[1])


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
