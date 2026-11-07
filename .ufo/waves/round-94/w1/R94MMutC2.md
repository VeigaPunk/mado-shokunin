# R94MMutC2 — mutation probe of the C2 kill-sets and the C2 counter (round 94, w1)

Seat R94MMutC2 (mutation-tester, leaf — no dispatch). Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`,
base rev `a3de997289014e7dbf1d73ae206be1d6f8cdadd0`. Scratch `S=/fast/scratch/hyaku/mado-r94/R94MMutC2`
(deleted on exit; every cited artefact was copied to `.ufo/waves/round-94/w1/` first).

**Every run recorded here is a DRAFT run.** Nothing in this report is a measurement of PRED-C2-r94-v1, no
`TARGET_*` word is claimed for the lane, nothing was written under `.ufo/waves/round-94/receipts/`, and no lane
file was modified except this report and the evidence JSONs listed in §7. No installs, no pacman, no network, no
git/jj mutation outside throwaway fixture repos under `$S` (each verified with `git rev-parse --show-toplevel`).

## 0. Objects and pins (re-read after every measurement)

| object | sha256 |
|---|---|
| `quality/check-selftest-strength.py` (round-93 frozen gate) | `2d6f1219fae19a85cc92f7d4103db396e1306fea74c2226bb068b335598da61b` |
| `tools/mado-xdgmime.py` | `4e7fff9efbd32d101d1383099566008fc49ba626be5bcc53a20766d71bc7fd88` |
| `tools/mado-mime.py` | `2532ccb57cf9d67f6590e4aac2e8d0a9f9eb011b25eb42e45118a6ff51871a5e` |
| candidate kill-set `build/mado-xdgmime-kills.c2.json` | `126b508aa1841ba99fa17ecaef46a5a79cdee99956ac2a605479b96122f09ea9` (12 kills) |
| candidate kill-set `build/mado-mime-kills.c2.json` | `d930689e6ff82e51722195e0c8d209fe46fb4697fd10f01f33cec30e98e81601` (15 kills) |
| kill-set revision **B** `build/mado-xdgmime-kills.c2b.json` | `d8a450bfb3bd67a6…` (19 kills) |
| kill-set revision **B** `build/mado-mime-kills.c2b.json` | `1a0c4fe8cec8ac4d…` (27 kills) |
| counter v1 `quality/counters/c2-r94-selftest-kills.py` (measured in §3.2) | `9c65bf86a3c9d356a4f62286228f113ed482cdddee5c25e1d5749f6b698d35a1` |
| counter v2 (clause (vii), measured in §3.3) | `0eb3aadad4b72eeacb6a5d382071efd78105fa0e8ccdd751445f5c3ccb1d9a02` |
| panel `controls/selftest-panel-r94.json` | `2727794c0f8a0bc27d8c7d16f517be6bc17fe6647e6265f2dedb3f1cf6288f3f` (12 hand, 6 neutral) |

Revision A of the kill-sets appeared at 03:26 (xdgmime) and 03:29 (mime), revision B at 03:54; counter v1 at
03:30 and v2 at 03:55. Each measurement names the revision it used, and every pinned object was re-read after the
last run (all unchanged except the two artefacts that were deliberately revised). Both revisions pin
`selftest_checks` (12 / 17) and `tool_sha256`; all `must_fail` values are lists, so the gate compares the exact
FAIL-label set.

## 1. Method

For each tool I built a hand catalogue of weakenings — edits that keep the selftest **green**
(`checks=N failed=0`, same result line) yet weaken an assertion — and measured each one with

```
python3 -I quality/check-selftest-strength.py --tool <weakened copy> --kills <candidate kill-set> \
    --scratch-root $S/g --timeout 120 --allow-sha-drift
```

A weakening **escapes** when that gate prints `SELFTEST_STRENGTH: OK … survived=0 wrong_check=0` rc 0. The
formal reason: the gate applies each kill to the *weakened* tool and requires the mutant's FAIL set to equal
`must_fail`; a weakening that silences a label set S is invisible iff no kill's `must_fail` meets S, and a
weakening that keeps the label failing but weakens a *different* component of the same assertion is invisible
whenever every kill that dies there flips the component that is still asserted.

The weakened objects are `tools/mado-xdgmime.py:773-789` (the eleven tuple checks and the RFC-refusal arm) and
`tools/mado-mime.py:869-898` (the seventeen `chk(...)` calls). A reproduction is: copy the tool, apply the row's
`find → replace` once, confirm `python3 -I <copy> --selftest` still prints `checks=N failed=0`, then run the gate
command above with the candidate kill-set.

Each escape was then **proved genuine** by a *closing kill*: a production defect that the pristine selftest kills
and the weakened selftest does not kill at full strength, so that the same gate with that kill added prints
`WEAK` rc 1. Every closing kill was verified in both directions — `WEAK` on the weakened tool and `OK` on the
pristine tool with the identical kill-set (`gate_with_extra_kill`/`pristine_line` columns in the evidence JSON).

## 2. Part 1 — escapes from the two candidate kill-sets (DRAFT)

Baseline (unmodified tool, candidate kill-set):

* xdgmime — `SELFTEST_STRENGTH: OK tool=tools/mado-xdgmime.py kills=12 held=12 survived=0 wrong_check=0`
* mime — `SELFTEST_STRENGTH: OK tool=tools/mado-mime.py kills=15 held=15 survived=0 wrong_check=0`

Catalogue size and outcome:

| tool | kills | weakenings tried | green | flagged | **escaped** | escaped + closer verified |
|---|---|---|---|---|---|---|
| xdgmime | 12 | 53 | 53 | 28 | **23** | 23/23 |
| mime | 15 | 59 | 59 | 34 | **23** | 23/23 |

**46 of 112 hand weakenings keep the selftest green and are not flagged by the gate with
the candidate kill-sets** — while the C2 counter on the same inputs prints
`DRAFT_TARGET_MET … neutralised_flagged=29/29 hand_flagged=12/12` (§3). The escapes are not exotic: they are the
ordinary "the check observes only one component" weakenings of the r93 E-family.

Label codes used in the `must_fail` cells:

| code | xdgmime label | code | mime label |
|---|---|---|---|
| L1 | `m03 list: second id installed` | L1 | `cache addition is default` |
| L2 | `m05 desktop-specific file first` | L2 | `hidden and unloadable dropped from lists` |
| L3 | `m09 only a file's first matching line counts; the next file is read` | L3 | `subdir id` |
| L4 | `m16 CR kept in the id` | L4 | `alias unaliased` |
| L5 | `d09 Exec=true is a builtin: not installed` | L5 | `parent in registered not recommended` |
| L6 | `f06 unanchored grep in mimeinfo.cache` | L6 | `unloadable only -> none` |
| L7 | `f09 a cache value -n is an echo option` | L7 | `hidden default accepted` |
| L8 | `b02 InitialPreference picks` | L8 | `desktop list wins` |
| L9 | `s01 LXQt: rc 3` | L9 | `desktop list additions ignored` |
| L10 | `s05 no slash: rc 1` | L10 | `other desktop ignores it` |
| L11 | `s08 --version` | L11 | `removal blocks lower addition` |
| L12 | `type outside RFC 6838 refused` | L12 | `added group is read before removed whatever the file order` |
|  |  | L13 | `unloadable list skipped` |
|  |  | L14 | `masked lower addition skipped, hidden one taken` |
|  |  | L15 | `default from masked id still loads in a lower dir` |
|  |  | L16 | `desktops` |
|  |  | L17 | `fgets chop` |

### 2.1 xdgmime — 23 escapes

| # | weakening (wid) | find → replace | gate on the weakened tool | closing kill | gate with that kill |
|---|---|---|---|---|---|
| 1 | `x-id-s01` | `OP="LXQt") == (None, 3)` → `OP="LXQt")[1] == 3` | `OK tool=tools/mado-xdgmime.py kills=12 held=12 survived=0 wrong_check=0` | `xc-lxqt-app-with-rc3`: `   return None` → `   return b"a.desktop"`, must_fail=[L9] | `WEAK tool=tools/mado-xdgmime.py kills=13 held=12 survived=1 wrong_check=0` |
| 2 | `x-id-s05` | `q("plain") == (None, 1)` → `q("plain")[1] == 1` | `OK tool=tools/mado-xdgmime.py kills=12 held=12 survived=0 wrong_check=0` | `xc-noslash-app-with-rc1`: `   return None` → `   return b"a.desktop"`, must_fail=[L10] | `WEAK tool=tools/mado-xdgmime.py kills=13 held=12 survived=1 wrong_check=0` |
| 3 | `x-rc-m03` | `xt/plain") == ("a.desktop", 0)` → `xt/plain")[0] == "a.desktop"` | `OK tool=tools/mado-xdgmime.py kills=12 held=12 survived=0 wrong_check=0` | `xc-found-app-rc1`: `lse out), 0` → `lse out), 1`, must_fail=[L1, L2, L3, L6, L8] | `WEAK tool=tools/mado-xdgmime.py kills=13 held=12 survived=0 wrong_check=1` |
| 4 | `x-rc-f06` | `text/csv") == ("un.desktop", 0)` → `text/csv")[0] == "un.desktop"` | `OK tool=tools/mado-xdgmime.py kills=12 held=12 survived=0 wrong_check=0` | `xc-found-app-rc1`: `lse out), 0` → `lse out), 1`, must_fail=[L1, L2, L3, L6, L8] | `WEAK tool=tools/mado-xdgmime.py kills=13 held=12 survived=0 wrong_check=1` |
| 5 | `x-rc-b02` | `text/x-p") == ("p2.desktop", 0)` → `text/x-p")[0] == "p2.desktop"` | `OK tool=tools/mado-xdgmime.py kills=12 held=12 survived=0 wrong_check=0` | `xc-found-app-rc1`: `lse out), 0` → `lse out), 1`, must_fail=[L1, L2, L3, L6, L8] | `WEAK tool=tools/mado-xdgmime.py kills=13 held=12 survived=0 wrong_check=1` |
| 6 | `x-loose-m03` | `xt/plain") == ("a.desktop", 0)` → `xt/plain")[0] is not None` | `OK tool=tools/mado-xdgmime.py kills=12 held=12 survived=0 wrong_check=0` | `x01-list-first-app`: `       if self.desktop_file_to_binary(app)` → `       if True`, must_fail=[L1, L3, L4, L5] | `WEAK tool=tools/mado-xdgmime.py kills=13 held=12 survived=0 wrong_check=1` |
| 7 | `x-rc-m05` | `mage/png") == ("h.desktop", 0)` → `mage/png")[0] == "h.desktop"` | `OK tool=tools/mado-xdgmime.py kills=12 held=12 survived=0 wrong_check=0` | `xc-found-app-rc1`: `lse out), 0` → `lse out), 1`, must_fail=[L1, L2, L3, L6, L8] | `WEAK tool=tools/mado-xdgmime.py kills=13 held=12 survived=0 wrong_check=1` |
| 8 | `x-rc-m09` | `ideo/mp4") == ("a.desktop", 0)` → `ideo/mp4")[0] == "a.desktop"` | `OK tool=tools/mado-xdgmime.py kills=12 held=12 survived=0 wrong_check=0` | `xc-found-app-rc1`: `lse out), 0` → `lse out), 1`, must_fail=[L1, L2, L3, L6, L8] | `WEAK tool=tools/mado-xdgmime.py kills=13 held=12 survived=0 wrong_check=1` |
| 9 | `x-rc-m16` | `ext/html") == (None, 0)` → `ext/html")[0] is None` | `OK tool=tools/mado-xdgmime.py kills=12 held=12 survived=0 wrong_check=0` | `xc-empty-rc1`: `urn None, 0` → `urn None, 1`, must_fail=[L4, L5, L7] | `WEAK tool=tools/mado-xdgmime.py kills=13 held=12 survived=0 wrong_check=1` |
| 10 | `x-rc-d09` | `andler/x") == (None, 0)` → `andler/x")[0] is None` | `OK tool=tools/mado-xdgmime.py kills=12 held=12 survived=0 wrong_check=0` | `xc-empty-rc1`: `urn None, 0` → `urn None, 1`, must_fail=[L4, L5, L7] | `WEAK tool=tools/mado-xdgmime.py kills=13 held=12 survived=0 wrong_check=1` |
| 11 | `x-rc-f09` | `cation/q") == (None, 0)` → `cation/q")[0] is None` | `OK tool=tools/mado-xdgmime.py kills=12 held=12 survived=0 wrong_check=0` | `xc-empty-rc1`: `urn None, 0` → `urn None, 1`, must_fail=[L4, L5, L7] | `WEAK tool=tools/mado-xdgmime.py kills=13 held=12 survived=0 wrong_check=1` |
| 12 | `x-rc-s01` | `OP="LXQt") == (None, 3)` → `OP="LXQt")[0] is None` | `OK tool=tools/mado-xdgmime.py kills=12 held=12 survived=0 wrong_check=0` | `x09-lxqt-rc-0`: `urn None, 3` → `urn None, 0`, must_fail=[L9] | `WEAK tool=tools/mado-xdgmime.py kills=13 held=12 survived=1 wrong_check=0` |
| 13 | `x-rc-s08` | `-version") == ("xdg-mime 1.2.1", 0)` → `-version")[0] == "xdg-mime 1.2.1"` | `OK tool=tools/mado-xdgmime.py kills=12 held=12 survived=0 wrong_check=0` | `xc-version-rc1`: `e 1.2.1", 0` → `e 1.2.1", 1`, must_fail=[L11] | `WEAK tool=tools/mado-xdgmime.py kills=13 held=12 survived=1 wrong_check=0` |
| 14 | `x-not-m03` | `t/plain") == ("a.desktop"` → `t/plain") != (None` | `OK tool=tools/mado-xdgmime.py kills=12 held=12 survived=0 wrong_check=0` | `x01-list-first-app`: `       if self.desktop_file_to_binary(app)` → `       if True`, must_fail=[L1, L3, L4, L5] | `WEAK tool=tools/mado-xdgmime.py kills=13 held=12 survived=0 wrong_check=1` |
| 15 | `x-not-m05` | `age/png") == ("h` → `age/png") != ("a` | `OK tool=tools/mado-xdgmime.py kills=12 held=12 survived=0 wrong_check=0` | `xc-found-app-rc1`: `lse out), 0` → `lse out), 1`, must_fail=[L1, L2, L3, L6, L8] | `WEAK tool=tools/mado-xdgmime.py kills=13 held=12 survived=0 wrong_check=1` |
| 16 | `x-not-m09` | `deo/mp4") == ("a` → `deo/mp4") != ("h` | `OK tool=tools/mado-xdgmime.py kills=12 held=12 survived=0 wrong_check=0` | `x01-list-first-app`: `       if self.desktop_file_to_binary(app)` → `       if True`, must_fail=[L1, L3, L4, L5] | `WEAK tool=tools/mado-xdgmime.py kills=13 held=12 survived=0 wrong_check=1` |
| 17 | `x-not-m16` | `xt/html") == (None` → `xt/html") != ("a.desktop"` | `OK tool=tools/mado-xdgmime.py kills=12 held=12 survived=0 wrong_check=0` | `x01-list-first-app`: `       if self.desktop_file_to_binary(app)` → `       if True`, must_fail=[L1, L3, L4, L5] | `WEAK tool=tools/mado-xdgmime.py kills=13 held=12 survived=0 wrong_check=1` |
| 18 | `x-not-d09` | `ndler/x") == (None` → `ndler/x") != ("t.desktop"` | `OK tool=tools/mado-xdgmime.py kills=12 held=12 survived=0 wrong_check=0` | `xc-empty-rc1`: `urn None, 0` → `urn None, 1`, must_fail=[L4, L5, L7] | `WEAK tool=tools/mado-xdgmime.py kills=13 held=12 survived=0 wrong_check=1` |
| 19 | `x-not-f06` | `ext/csv") == ("un.desktop"` → `ext/csv") != (None` | `OK tool=tools/mado-xdgmime.py kills=12 held=12 survived=0 wrong_check=0` | `xc-found-app-rc1`: `lse out), 0` → `lse out), 1`, must_fail=[L1, L2, L3, L6, L8] | `WEAK tool=tools/mado-xdgmime.py kills=13 held=12 survived=0 wrong_check=1` |
| 20 | `x-not-f09` | `ation/q") == (None` → `ation/q") != ("-n"` | `OK tool=tools/mado-xdgmime.py kills=12 held=12 survived=0 wrong_check=0` | `xc-empty-rc1`: `urn None, 0` → `urn None, 1`, must_fail=[L4, L5, L7] | `WEAK tool=tools/mado-xdgmime.py kills=13 held=12 survived=0 wrong_check=1` |
| 21 | `x-not-s01` | `P="LXQt") == (None, 3` → `P="LXQt") != ("a.desktop", 0` | `OK tool=tools/mado-xdgmime.py kills=12 held=12 survived=0 wrong_check=0` | `x09-lxqt-rc-0`: `urn None, 3` → `urn None, 0`, must_fail=[L9] | `WEAK tool=tools/mado-xdgmime.py kills=13 held=12 survived=1 wrong_check=0` |
| 22 | `x-not-s05` | `("plain") == (None, 1` → `("plain") != (None, 0` | `OK tool=tools/mado-xdgmime.py kills=12 held=12 survived=0 wrong_check=0` | `xc-noslash-app-with-rc1`: `   return None` → `   return b"a.desktop"`, must_fail=[L10] | `WEAK tool=tools/mado-xdgmime.py kills=13 held=12 survived=1 wrong_check=0` |
| 23 | `x-not-s08` | `version") == ("xdg-mime 1.2.1` → `version") != ("xdg-mime 1.2.0` | `OK tool=tools/mado-xdgmime.py kills=12 held=12 survived=0 wrong_check=0` | `xc-version-rc1`: `e 1.2.1", 0` → `e 1.2.1", 1`, must_fail=[L11] | `WEAK tool=tools/mado-xdgmime.py kills=13 held=12 survived=1 wrong_check=0` |

### 2.2 mime — 23 escapes

| # | weakening (wid) | find → replace | gate on the weakened tool | closing kill | gate with that kill |
|---|---|---|---|---|---|
| 1 | `m-loose-cache-default` | `t/plain") == "a.desktop"` → `t/plain") is not None` | `OK tool=tools/mado-mime.py kills=15 held=15 survived=0 wrong_check=0` | `m13-unloadable-becomes-default`: `          return\n` → `          groups = {DEFAULTS: {"text/plain": "b.desktop"}}\n        else:\n    `, must_fail=[L1, L12, L13] | `WEAK tool=tools/mado-mime.py kills=16 held=15 survived=0 wrong_check=1` |
| 2 | `m-parent-recommended-dropped` | `      and r.ids_for_type("text/x-src", False) == ["sub-d.desktop"]` → `      and True` | `OK tool=tools/mado-mime.py kills=15 held=15 survived=0 wrong_check=0` | `mc-recommended-parents`: `ime_type, fallback` → `ime_type, True`, must_fail=[L5] | `WEAK tool=tools/mado-mime.py kills=16 held=15 survived=1 wrong_check=0` |
| 3 | `m-loose-added-before-removed` | `t/plain") == "a.desktop"` → `t/plain") is not None` | `OK tool=tools/mado-mime.py kills=15 held=15 survived=0 wrong_check=0` | `m12-removed-file-loses-additions`: `k, ids in lists(added_group` → `k, ids in ([] if groups.get(REMOVED) else lists(added_group)`, must_fail=[L12] | `WEAK tool=tools/mado-mime.py kills=16 held=15 survived=1 wrong_check=0` |
| 4 | `m-loose-unloadable` | `t/plain") == "a.desktop"` → `t/plain") is not None` | `OK tool=tools/mado-mime.py kills=15 held=15 survived=0 wrong_check=0` | `m13-unloadable-becomes-default`: `          return\n` → `          groups = {DEFAULTS: {"text/plain": "b.desktop"}}\n        else:\n    `, must_fail=[L1, L12, L13] | `WEAK tool=tools/mado-mime.py kills=16 held=15 survived=0 wrong_check=1` |
| 5 | `m-loose-lower-dir` | `          == "a.desktop"` → `          is not None` | `OK tool=tools/mado-mime.py kills=15 held=15 survived=0 wrong_check=0` | `mc-default-wrong-id`: `or app in results` → `or app in (["b.desktop"] + results)`, must_fail=[L1, L3, L4, L6, L8, L9, L12, L13, L15] | `WEAK tool=tools/mado-mime.py kills=16 held=15 survived=0 wrong_check=1` |
| 6 | `m-len-registered` | `m lists", r.resolve("text/plain")["registered"] == ["a.desktop"]` → `m lists", len(r.resolve("text/plain")["registered"]) <= 1` | `OK tool=tools/mado-mime.py kills=15 held=15 survived=0 wrong_check=0` | `m01-cache-additions-dropped`: `), CACHE, Tru` → `), CACHE, Fals`, must_fail=[L1, L2, L3, L4, L5, L13, L14] | `WEAK tool=tools/mado-mime.py kills=16 held=15 survived=0 wrong_check=1` |
| 7 | `m-desktops-length` | `esktops", current_desktops("KDE::bad/x:GNOME-Classic") == ["kde", "gnome-classic"]` → `esktops", len(current_desktops("KDE::bad/x:GNOME-Classic")) == 2` | `OK tool=tools/mado-mime.py kills=15 held=15 survived=0 wrong_check=0` | `m10-desktop-name-constant`: `ut.append(t.lower()` → `ut.append("hyprland"`, must_fail=[L10, L16] | `WEAK tool=tools/mado-mime.py kills=16 held=15 survived=0 wrong_check=1` |
| 8 | `m-alt-cache-default` | `t/plain") == "a.desktop"` → `t/plain") in ("a.desktop", "a.desktop ")` | `OK tool=tools/mado-mime.py kills=15 held=15 survived=0 wrong_check=0` | `mc-default-trailing`: `return app` → `return app + " "`, must_fail=[L1, L3, L4, L7, L8, L10, L12, L13, L14, L15] | `WEAK tool=tools/mado-mime.py kills=16 held=15 survived=0 wrong_check=1` |
| 9 | `m-alt-registered` | `istered"] == ["a.desktop"]` → `istered"] in (["a.desktop"], ["a.desktop "])` | `OK tool=tools/mado-mime.py kills=15 held=15 survived=0 wrong_check=0` | `mc-registered-padded-only`: `return [a ` → `return [a + " " if fallback else a `, must_fail=[L2, L5] | `WEAK tool=tools/mado-mime.py kills=16 held=15 survived=0 wrong_check=1` |
| 10 | `m-alt-subdir` | `t/x-src") == "sub-d.desktop"` → `t/x-src") in ("sub-d.desktop", "sub-d.desktop ")` | `OK tool=tools/mado-mime.py kills=15 held=15 survived=0 wrong_check=0` | `mc-default-trailing`: `return app` → `return app + " "`, must_fail=[L1, L3, L4, L7, L8, L10, L12, L13, L14, L15] | `WEAK tool=tools/mado-mime.py kills=16 held=15 survived=0 wrong_check=1` |
| 11 | `m-alt-alias` | `x-alias") == "sub-d.desktop"` → `x-alias") in ("sub-d.desktop", "sub-d.desktop ")` | `OK tool=tools/mado-mime.py kills=15 held=15 survived=0 wrong_check=0` | `mc-default-trailing`: `return app` → `return app + " "`, must_fail=[L1, L3, L4, L7, L8, L10, L12, L13, L14, L15] | `WEAK tool=tools/mado-mime.py kills=16 held=15 survived=0 wrong_check=1` |
| 12 | `m-alt-parent-registered` | `c", True) == ["sub-d.desktop", "a.desktop"]` → `c", True) in (["sub-d.desktop", "a.desktop"], ["sub-d.desktop ", "a.desktop "])` | `OK tool=tools/mado-mime.py kills=15 held=15 survived=0 wrong_check=0` | `mc-registered-padded-only`: `return [a ` → `return [a + " " if fallback else a `, must_fail=[L2, L5] | `WEAK tool=tools/mado-mime.py kills=16 held=15 survived=0 wrong_check=1` |
| 13 | `m-alt-parent-recommended` | `", False) == ["sub-d.desktop"]` → `", False) in (["sub-d.desktop"], ["sub-d.desktop "])` | `OK tool=tools/mado-mime.py kills=15 held=15 survived=0 wrong_check=0` | `mc-recommended-padded-only`: `return [a ` → `return [a if fallback else a + " " `, must_fail=[L5] | `WEAK tool=tools/mado-mime.py kills=16 held=15 survived=1 wrong_check=0` |
| 14 | `m-alt-unloadable-none` | `ge/png") is None` → `ge/png") in (None, "c.desktop ")` | `OK tool=tools/mado-mime.py kills=15 held=15 survived=0 wrong_check=0` | `mc-default-first-padded`: `       if self._get_app(k, app)[0]:\n                        return app` → `       if results:\n                        return results[0] + " "`, must_fail=[L1, L3, L4, L6, L7, L8, L9, L10, L12, L13, L14, L15] | `WEAK tool=tools/mado-mime.py kills=16 held=15 survived=0 wrong_check=1` |
| 15 | `m-alt-hidden-default` | `t/plain") == "b.desktop"` → `t/plain") in ("b.desktop", "b.desktop ")` | `OK tool=tools/mado-mime.py kills=15 held=15 survived=0 wrong_check=0` | `mc-default-trailing`: `return app` → `return app + " "`, must_fail=[L1, L3, L4, L7, L8, L10, L12, L13, L14, L15] | `WEAK tool=tools/mado-mime.py kills=16 held=15 survived=0 wrong_check=1` |
| 16 | `m-alt-desktop-wins` | `t/plain") == "sub-d.desktop"` → `t/plain") in ("sub-d.desktop", "sub-d.desktop ")` | `OK tool=tools/mado-mime.py kills=15 held=15 survived=0 wrong_check=0` | `mc-default-trailing`: `return app` → `return app + " "`, must_fail=[L1, L3, L4, L7, L8, L10, L12, L13, L14, L15] | `WEAK tool=tools/mado-mime.py kills=16 held=15 survived=0 wrong_check=1` |
| 17 | `m-alt-additions-none` | `ge/png") is None` → `ge/png") in (None, "c.desktop ")` | `OK tool=tools/mado-mime.py kills=15 held=15 survived=0 wrong_check=0` | `mc-default-first-padded`: `       if self._get_app(k, app)[0]:\n                        return app` → `       if results:\n                        return results[0] + " "`, must_fail=[L1, L3, L4, L6, L7, L8, L9, L10, L12, L13, L14, L15] | `WEAK tool=tools/mado-mime.py kills=16 held=15 survived=0 wrong_check=1` |
| 18 | `m-alt-other-desktop` | `t/plain") == "b.desktop"` → `t/plain") in ("b.desktop", "b.desktop ")` | `OK tool=tools/mado-mime.py kills=15 held=15 survived=0 wrong_check=0` | `mc-default-trailing`: `return app` → `return app + " "`, must_fail=[L1, L3, L4, L7, L8, L10, L12, L13, L14, L15] | `WEAK tool=tools/mado-mime.py kills=16 held=15 survived=0 wrong_check=1` |
| 19 | `m-alt-added-before-removed` | `t/plain") == "a.desktop"` → `t/plain") in ("a.desktop", "a.desktop ")` | `OK tool=tools/mado-mime.py kills=15 held=15 survived=0 wrong_check=0` | `mc-default-trailing`: `return app` → `return app + " "`, must_fail=[L1, L3, L4, L7, L8, L10, L12, L13, L14, L15] | `WEAK tool=tools/mado-mime.py kills=16 held=15 survived=0 wrong_check=1` |
| 20 | `m-alt-unloadable` | `t/plain") == "a.desktop"` → `t/plain") in ("a.desktop", "a.desktop ")` | `OK tool=tools/mado-mime.py kills=15 held=15 survived=0 wrong_check=0` | `mc-default-trailing`: `return app` → `return app + " "`, must_fail=[L1, L3, L4, L7, L8, L10, L12, L13, L14, L15] | `WEAK tool=tools/mado-mime.py kills=16 held=15 survived=0 wrong_check=1` |
| 21 | `m-alt-masked` | `t/plain") == "b.desktop"` → `t/plain") in ("b.desktop", "b.desktop ")` | `OK tool=tools/mado-mime.py kills=15 held=15 survived=0 wrong_check=0` | `mc-default-trailing`: `return app` → `return app + " "`, must_fail=[L1, L3, L4, L7, L8, L10, L12, L13, L14, L15] | `WEAK tool=tools/mado-mime.py kills=16 held=15 survived=0 wrong_check=1` |
| 22 | `m-alt-desktops` | `Classic") == ["kde", "gnome-classic"]` → `Classic") in (["kde", "gnome-classic"], ["KDE", "GNOME-Classic"])` | `OK tool=tools/mado-mime.py kills=15 held=15 survived=0 wrong_check=0` | `mc-desktop-case-kept`: `t.append(t.lower()` → `t.append(t`, must_fail=[L8, L16] | `WEAK tool=tools/mado-mime.py kills=16 held=15 survived=0 wrong_check=1` |
| 23 | `m-alt-fgets` | `v/null")] == []` → `v/null")] in ([], [("", "")])` | `OK tool=tools/mado-mime.py kills=15 held=15 survived=0 wrong_check=0` | `m17-empty-pair`: ` pairs = [` → ` pairs = [("", "")`, must_fail=[L17] | `WEAK tool=tools/mado-mime.py kills=16 held=15 survived=1 wrong_check=0` |

### 2.3 Families (what the kill-sets do not pin)

1. **Component dropping in a two-component answer** (xdgmime, 12 rows): eleven of the twelve xdgmime checks
   compare `(id, rc)`. Ten escapes keep the id and drop the exit code (`q(...)[0] == …`); two (`s01`, `s05`) keep
   the rc and drop the id (`q(...)[1] == rc`). Both are invisible because the candidate kill that dies under that
   label flips the component that is still asserted (the id for most labels, the rc for `x10-s05-no-slash-rc0`).
2. **Negative assertions** (xdgmime, 10 rows): `q(...) != (<the defect's answer>)` is green today, still fails on
   the matching kill, and accepts *every other answer*. No kill can see it because no kill produces another one.
3. **Alternative spelling** (mime, 16 rows): `x in (expected, expected + " ")` / a differently-cased list is green
   and fails on every existing kill; a defect that leaves one trailing byte on an id or keeps a desktop token's
   case would then pass unseen. This is the exact r93 `E5-substring-case` family with a different literal.
4. **Length/membership instead of identity** (mime, 1 row): `len(current_desktops(...)) == 2`; the list-valued
   loosenings (`len(registered) <= 1`, `"a.desktop" in registered`) escape too but as *alt/loose* rows above
   (`m-len-registered`).
5. **Conjunct dropping** (mime, 1 row): the `parent in registered not recommended` check has two conjuncts; the
   candidate kill `a05` only exercises the parent fallback, so dropping the *recommended* conjunct survives.
6. **Loosening an `is None` / exact-default assertion** (mime, 5 rows): `default(T) is not None`, `!= "gone.desktop"`,
   `in (None, "c.desktop ")` — each green, each still failing on every candidate kill.

### 2.4 Every escape is closable by one added kill

All 46 escapes have a verified closing kill (column "gate with that kill" shows `WEAK` rc 1; the
evidence JSON also records the same kill-set on the pristine tool, `OK` rc 0, so the proposal never breaks clause
(i)). The proposals are ordinary production defects of the class each weakening hides — a resolved default that
exits 1, an LXQt miss that returns an id, a default id that keeps a trailing space, a list that keeps a trailing
space on every id — and each was checked to be killed by the unweakened selftest (`must_fail` is its measured FAIL
set, so the kill-set stays exact-set valid).


### 2.5 Second kill-set revision (c2b, 19 / 27 kills): the same catalogue is fully flagged (DRAFT)

While this seat was measuring, R94MExecKillsC2 published a second revision of both kill-sets
(`…-kills.c2b.json`, 19 xdgmime kills / 27 mime kills, adding isolation and component kills). The identical 112
weakenings were run against it:

| tool | kills | weakenings | WEAK | SETUP_ERROR | escapes |
|---|---|---|---|---|---|
| xdgmime | 19 | 53 | 51 | 2 | 0 |
| mime | 27 | 59 | 57 | 2 | 0 |

The two `SETUP_ERROR` rows are the same two as before and are *caught*, not escaped: a deleted check
(`x-drop-s05`, `m-drop-fgets`) trips the `selftest_checks` pin and an inflated result line
(`x-count-inflated`, `m-count-inflated`) trips the same pin — the gate prints `SETUP_ERROR` rc 2, never `OK`.
So revision B closes every escape of §2.1/§2.2 on this catalogue, and the escape surface of §2 is exactly the
delta between the two revisions: **12 of revision B's added kills carry the ids and the byte-identical
`find`/`replace` pairs of the closing kills proposed in §2.1/§2.2** (`xc-lxqt-app-with-rc3`,
`xc-noslash-app-with-rc1`, `xc-found-app-rc1`, `xc-empty-rc1`, `xc-version-rc1`, `mc-default-trailing`,
`mc-default-first-padded`, `mc-default-wrong-id`, `mc-registered-padded-only`, `mc-recommended-padded-only`,
`mc-recommended-parents`, `mc-desktop-case-kept` — checked by string equality, 12/12 identical).

## 3. Part 2 — mutation of the C2 counter (DRAFT)

The counter was run in draft mode
(`--repo <repo> --rev <rev> --panel <frozen panel> --draft-kills <xdgmime>,<mime> --expect-* … --workers 8`)
against an eight-probe panel, because the counter's own printout is only as discriminating as the material it is
shown:

| probe | rc | verdict line (truncated) |
|---|---|---|
| P6-gate-pin-drift | 3 | `DRAFT_TARGET_MISSED pred=PRED-C2-r94-v1 rev=draft gate_pin=FAIL kills_pin=ok,ok tools=2 checks=29 positive=OK:0,OK:0 n` |
| P7-tool-pin-drift | 3 | `DRAFT_TARGET_MISSED pred=PRED-C2-r94-v1 rev=draft gate_pin=ok kills_pin=ok,ok tools=2 checks=29 positive=OK:0,SETUP_ER` |
| P0-strong | 3 | `DRAFT_TARGET_MET pred=PRED-C2-r94-v1 rev=draft gate_pin=ok kills_pin=ok,ok tools=2 checks=29 positive=OK:0,OK:0 neutra` |
| P1-empty-kills | 3 | `DRAFT_TARGET_MISSED pred=PRED-C2-r94-v1 rev=draft gate_pin=ok kills_pin=ok,ok tools=2 checks=29 positive=OK:0,OK:0 neu` |
| P2-pin-drift | 3 | `DRAFT_TARGET_MISSED pred=PRED-C2-r94-v1 rev=draft gate_pin=ok kills_pin=FAIL,FAIL tools=2 checks=29 positive=OK:0,OK:0` |
| P3-gate-selftest-red | 3 | `DRAFT_TARGET_MISSED pred=PRED-C2-r94-v1 rev=draft gate_pin=ok kills_pin=ok,ok tools=2 checks=29 positive=OK:0,OK:0 neu` |
| P4-dup-label | 2 | `SETUP_ERROR pred=PRED-C2-r94-v1 tools/mado-mime.py: labels enumerated 16 (unique 16) != checks=17` |
| P5-red-variant | 2 | `SETUP_ERROR pred=PRED-C2-r94-v1 variant T2 W:rig-red does not keep the selftest green: rc=1 'MADO_MIME_SELFTEST: check` |

The `P8` probe (`panel-escape.json`) exists only for the counter-v2 run of §3.1; `P0` is the frozen candidates;
`P1` empty `kills` arrays; `P2` the candidate bytes with drifted
`--expect-kills-sha256`; `P3` a fixture repo whose gate answers `--selftest` with rc 1; `P4` a fixture repo whose
`mado-mime.py` has a duplicated label (17 checks, 16 unique); `P5` a rigged panel with one hand weakening that
makes the mime selftest red; `P6` a drifted `--expect-gate-sha256`; `P7` a kill-set copy whose `tool_sha256` does
not match the tool. Only `P0` reads `MET`; the other seven each break one clause or one setup guard, so a mutant
is killed when any probe's `(rc, line)` differs from the baseline's.
Fixture repositories: `git init` under `$S/c2probes/repos/…`, every `git -C` call naming the repo, toplevel
verified before the commit; nothing in the lane repo was touched.

| mutant | what | verdict on the 8-probe panel | probes that differ |
|---|---|---|---|
| `C01-nflag-rc-dropped` | the neutralisation count ignores the gate's exit code | **SURVIVED** | — |
| `C02-nflag-ok-as-flagged` | an OK verdict counts as flagged | **KILLED** | P1-empty-kills |
| `C03-neutral-accepts-weak` | a neutral edit that is flagged still counts as preserved | **SURVIVED** | — |
| `C04-label-count-skipped` | the label-count/enumeration check is skipped | **KILLED** | P4-dup-label |
| `C05-gate-pin-skipped` | the gate sha256 pin is not enforced | **KILLED** | P6-gate-pin-drift |
| `C06-kills-pin-skipped` | the kill-set sha256 pins are not enforced | **KILLED** | P2-pin-drift |
| `C07-tool-pin-skipped` | the kill-sets' tool_sha256 pins are not enforced | **KILLED** | P7-tool-pin-drift |
| `C08-neutral-one-tool-only` | only the xdgmime neutralisations must be flagged | **KILLED** | P0-strong |
| `C09-positive-skipped` | the positive control is not checked | **SURVIVED** | — |
| `C10-donothing-control-dropped` | the do-nothing control is not checked | **SURVIVED** | — |
| `C11-alwaysweak-control-dropped` | the always-WEAK gate control is not checked | **SURVIVED** | — |
| `C12-shadiff-control-dropped` | the sha-diff neutral control is not checked | **SURVIVED** | — |
| `C13-gate-selftest-skipped` | the gate's own selftest is not run/required | **KILLED** | P3-gate-selftest-red |
| `C14-variant-green-skipped` | variants are not checked to keep the selftest green | **KILLED** | P5-red-variant |
| `C15-met-forced` | the verdict is always TARGET_MET | **KILLED** | P6-gate-pin-drift, P7-tool-pin-drift, P1-empty-kills, P2-pin-drift, P3-gate-selftest-red |
| `C16-hand-count-dropped` | hand weakenings need only be weakly flagged (never OK) | **SURVIVED** | — |

**9 of 16 counter mutants are killed by the eight-probe DRAFT panel; 7 survive.**

Survivors and why:

* `C01-nflag-rc-dropped` — the gate's WEAK arm exits 1 on every WEAK verdict it can print here, so `WEAK:1` is the only WEAK string observable
* `C03-neutral-accepts-weak` — every frozen neutral edit is OK:0 on this gate by construction (a flagged neutral edit would itself be a gate defect, which the sha-diff control covers), so accepting WEAK changes no count
* `C09-positive-skipped` — the positive verdict is a function of (gate, tool, kill-set); no probe can make it non-OK without also collapsing (ii) or the pins, so the conjunct is masked on every probe of this panel
* `C10-donothing-control-dropped` — dn is 0 on every variant (all frozen variants are green with the unmodified result line), so the conjunct is satisfied by construction
* `C11-alwaysweak-control-dropped` — aw comes from the constant ALWAYS_WEAK script, which prints WEAK:1 unconditionally
* `C12-shadiff-control-dropped` — SHA_DIFF cannot match any variant's sha, so sd_zok is 0 by construction
* `C16-hand-count-dropped` — `!= OK:0` and `== WEAK:1` agree on every frozen variant because a non-green variant is rejected earlier as SETUP_ERROR

### 3.1 Counter v2 — clause (vii) is the escape count of §2, and the pins are testable

The second counter revision (`0eb3aada…`, 17 732 bytes) adds, verbatim from this seat's §2, clause (vii):

> the round's first-draft kill-sets (`--control-kills`, sha256-pinned; 12 + 15 kills, the ones the wave's mutation
> tester escaped 46 times) flag strictly fewer hand weakenings than the frozen kill-sets
> (`control_hand_flagged < hand`)

Against the nine-probe panel with `--control-kills` = the first-draft pair (revision A, 12 + 15 kills) and
`--draft-kills` = the c2b pair (revision B, 19 + 27 kills), the unmutated v2 counter **still prints
`DRAFT_TARGET_MISSED`** on the frozen panel:

`MADO_SELFTEST_KILLS: DRAFT_TARGET_MISSED pred=PRED-C2-r94-v1 rev=draft gate_pin=ok kills_pin=ok,ok tools=2 checks=29 positive=OK:0,OK:0 neutralised_flagged=29/29 hand_flagged=12/12 neutral_ok=6/6 do_nothing_flagged=0 always_ok_flagged=0 always_weak_positive=WEAK:1,WEAK:1 shadiff_neutral_ok=0/6 gate_selftest=ok control_hand_flagged=12/12 singleton_labels=22/29 tool_pin=ok,ok kill_paths=quality/selftest-kills/mado-xdgmime.json,quality/selftest-kills/mado-mime.json gate_sha256=2d6f1219fae19a85cc92f7d4103db396e1306fea7`

`hand_flagged=12/12` **and** `control_hand_flagged=12/12`: clause (vii) needs a strict inequality, and the frozen
panel cannot produce one, because every one of its twelve hand weakenings is a tautology (§3.2) that any kill-set
with union coverage flags. **As frozen, clause (vii) is unsatisfiable.** The repair is the panel of §2: with twelve
rows taken from this seat's escape catalogue (6 per tool; `P8-escape-panel` in the probe table) the same frozen
v2 counter prints

`MADO_SELFTEST_KILLS: DRAFT_TARGET_MET pred=PRED-C2-r94-v1 rev=draft gate_pin=ok kills_pin=ok,ok tools=2 checks=29 positive=OK:0,OK:0 neutralised_flagged=29/29 hand_flagged=12/12 neutral_ok=6/6 do_nothing_flagged=0 always_ok_flagged=0 always_weak_positive=WEAK:1,WEAK:1 shadiff_neutral_ok=0/6 gate_selftest=ok control_hand_flagged=0/12 singleton_labels=22/29 tool_pin=ok,ok kill_paths=quality/selftest-kills/mado-xdgmime.json,quality/selftest-kills/mado-mime.json gate_sha256=2d6f1219fae19a85cc92f7d4103db396e1306fea74c22`

so `control_hand_flagged < hand` holds and the panel discriminates the two kill-set revisions. `singleton_labels`
is reported as `22/29` on revision B (7 labels still have no `must_fail == [X]` kill: the isolation requirement
R94MReviewC2 proposed is only partly met).

The v2 mutant panel was **not completed**: the run was killed at its 2400 s deadline
(`Error: [Command timed out after 2400 seconds]`) after the counter's added control-kill leg roughly doubled each
run's cost; no v2 mutant verdict is claimed here. The v1 panel below (16 mutants, 9 killed / 7
survived) is the measured part-2 result, and the v2 evidence in this section is the two baseline lines above
(`P0` on the frozen panel = `DRAFT_TARGET_MISSED`, `P8` on the escape-derived panel = `DRAFT_TARGET_MET`).

### 3.2 The frozen panel's 12 hand weakenings are tautologies

Read from the frozen panel (DRAFT, text only): eleven of the twelve hand weakenings replace the expected value by
an expression that *tracks the actual value* — `q(...) == q(...)`, `r.default(T) == r.default(T)`,
`[p for p in …] == [p for p in …]` — and the twelfth (`mime-w04`) is `in (expected, actual)`. The six xdgmime
entries that keep a tuple (`… == (q(...)[0], 0)`) drop the **id** and hardcode the exit code to 0 — i.e. they
weaken exactly the component the candidate kills flip. Every one of them therefore makes the corresponding kill
*pass*, so the gate sees `SURVIVED` and prints `WEAK`; `hand_flagged=12/12` certifies only that the gate notices a
tautology. The complement — keep the id, drop the exit code — is what 10 of the 23 xdgmime escapes do, and no
panel row tests it.

### 3.3 What this means for PRED-C2-r94-v1

* The predicate's (iii) is a **finite 12-row panel**. The 46 escapes of §2 are outside it, so
  `hand_flagged=12/12` is compatible with a weakened selftest that the gate cannot see. The counter is not wrong;
  it is *not sensitive to anything the panel does not enumerate*.
* Clauses (i)+(ii) only force **union coverage of labels** by `must_fail` sets. R94MReviewC2 showed a 1-kill and a
  5-kill forgery that satisfies them; §2 shows the concrete weakenings such a kill-set misses. A cheap repair that
  kills most of §2's families: require, for every label X, at least one kill whose `must_fail == [X]`, and add to
  the panel one weakening per *component* of each assertion (id-only, rc-only, negative form, alternative
  spelling). Every escape in §2 was found mechanically from that matrix, not by taste.
* A **deleted check** is caught only as `SETUP_ERROR` (the `selftest_checks` pin), never as `WEAK` rc 1 — measured:
  `x-drop-s05` (checks=11) and `m-drop-fgets` (checks=16) both give `SELFTEST_STRENGTH: SETUP_ERROR … unmutated
  selftest result … is not checks=N` rc 2. Clause (iii) demands `WEAK` rc 1, so a check-deletion cannot be frozen
  into the panel as a hand weakening even though the pin does catch it.
* The always-OK / always-WEAK / sha-diff / do-nothing control conjuncts are satisfied by construction (the stubs
  are constants in the counter, and every frozen variant is green), so mutants that drop them are unobservable on
  any realistic probe — they are panel gaps, not counter defects, and are listed as equivalents above.

## 4. Commands run (all DRAFT; exit status shown)

| command | rc |
|---|---|
| `python3 -I tools/mado-xdgmime.py --selftest` (TMPDIR=$S/runs) | 0 (`checks=12 failed=0`) |
| `python3 -I tools/mado-mime.py --selftest` | 0 (`checks=17 failed=0`) |
| gate on each unmodified tool + candidate kill-set | 0 (`OK`, held=12 / held=15) |
| gate on each weakening of §2 (112 runs) + one closing-kill run per escape | 0 (driver rc) |
| `python3 -I quality/counters/c2-r94-selftest-kills.py … --draft-kills …` (P0) | 3 (`DRAFT_TARGET_MET`) |
| the same on probes P6, P7, P1–P5 | 3/3/3/3/3/2/2 |
| counter mutant panel (v1): 16 × 8 probes | 0 (driver rc) |
| counter v2 on the frozen panel + revision-B kill-sets (`P0`) | 3 (`DRAFT_TARGET_MISSED`) |
| counter v2 on the escape-derived panel (`P8`) | 3 (`DRAFT_TARGET_MET`) |
| counter mutant panel (v2): 0 × 9 probes | 0 (driver rc) |

## 5. Dead steps and errors

1. `defects.py` first `d09` entry used `cmd in BUILTINS` (bytes vs a `str` set) — inert; the measured FAIL list was
   empty (`MADO_XDGMIME_SELFTEST: checks=12 failed=0` on the mutant) and it was replaced with
   `fs(cmd) in BUILTINS`.
2. First `m12`/`m13` mime defects were equivalent mutants: `_expand` ignores the block list when `cur is None`, and
   `self.tweaks.clear()` on a fresh dir is a no-op; both passed the pristine selftest (`failed=0`) and were replaced.
3. `driver.py` kill-set builder raised `TypeError: replace() takes at least 2 positional arguments (1 given)`
   (`src.replace(find, replace=repl, count=1)`); fixed to `src.replace(find, repl, 1)`.
4. The closing-kill block raised `NameError: name 'row' is not defined` after the refactor to on-demand FAIL sets;
   fixed to use the measured `fails`.
5. The blast-kill-set run was launched with an empty output path and died with
   `FileNotFoundError: [Errno 2] No such file or directory: ''`; the reviewer's forgery is reported from their
   evidence instead of being re-measured here.
6. One evidence file was clobbered by a later run (`KeyError: 'xdgmime'` when reading it); the affected measurement
   was re-run and reproduced 23 escapes / 23 closed exactly.
7. A bulk edit moving the alternative-spelling weakenings to trailing-space alternates rewrote the first element of
   the `parent in registered` tuple, so three escapes reported "no closer". Fixed and re-measured: 23/23 closed.

## 6. Restoration and cleanliness

The candidate kill-sets, the counter, the panel, the gate and both tools were only ever read and copied into `$S`;
all lane files keep the pinned hashes of §0 (re-read after the last run). All mutants, weakenings and fixtures lived
under `$S`; `$S` is deleted on exit after the evidence copies of §7.

## 7. Files written by this seat

* `.ufo/waves/round-94/w1/R94MMutC2.md` (this report)
* `.ufo/waves/round-94/w1/R94MMutC2-escapes-xdgmime.json` (53 weakenings, per-row gate lines, closers)
* `.ufo/waves/round-94/w1/R94MMutC2-escapes-mime.json` (59 weakenings, per-row gate lines, closers)
* `.ufo/waves/round-94/w1/R94MMutC2-counter-baseline.json` (8-probe baseline)
* `.ufo/waves/round-94/w1/R94MMutC2-counter-mutants.json` (16 counter mutants, per-probe verdict lines)
* `.ufo/waves/round-94/w1/R94MMutC2-counter-baseline-v2.json` (9-probe baseline, counter v2)
* `.ufo/waves/round-94/w1/R94MMutC2-escapes-c2b.json` (the same 112 weakenings against kill-set revision B)
