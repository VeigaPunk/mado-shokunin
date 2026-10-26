# ExecSkillVerify — round 41 w2 report

Target: w1 `ScrSkillProvince` drafts (`skill-rows.md`, `province-row.md`) run as written against the
delivered tool at `07f2641696b5ac73de1404ea737a9f27e9819aa1` (own clone; every command executed).

## Findings

1. **Wrong — row A sample cell omits `ignored=0`.** The delivered tool (and the v2 reference,
   byte-identical: main `sha256sum 392a621d…`, `--diff` byte-identical, `--selftest` 63/63 on
   both) prints the final line with an extra field:
   `… classes=capture:2,clipboard:3,focus-grab:1,idle:2,input-capture:3,input-synthesis:3,other:38,output-control:4,sandbox:1,session-lock:2,toplevel-control:4 expected_missing=- ignored=0 verdict=OK`.
   `diff` vs committed `ref-run-journal.txt`/`ref-run-diff.txt` shows exactly this one line
   differs (line 66/67). The w1 quotes (`expected_missing=- verdict=OK`) are the v1 reference's
   format, not the landed tool's. Corrected insertion text in
   `.ufo/waves/round-41/w2/ExecSkillVerify/verify.md` §2 (full row A + sample line + both
   `--expect` excerpts).
2. **ok — everything else in both drafts.** Exit map fully exercised: 0 OK (rc 0, stderr empty,
   66 lines, 2 sessions + 63 `MADO_GLOBAL:` sorted + final), 1 MISSING_EXPECTED (zwlr_screencopy_manager_v2,
   rc 1), 2 SETUP usage/unreadable/too_large/bad_expect (all legs, incl. abbreviated flag), 3
   NO_SESSIONS (non-empty no-advert journal), 5 journalctl_unusable/journalctl_failed (via
   `--journalctl` overrides; no host mutation). `--diff` rc 0, 67 lines, diff line 1902 B, added
   63 (first ext_background_effect_manager_v1, last zxdg_output_manager_v1), removed 8, ver_changed=-.
   `--live` end-to-end rc 0 under the allowed journal verb. Cap boundary 8388608 B accepted,
   8388609 → too_large. Implementation facts (8 MiB cap line 36; env limited PATH/XDG_RUNTIME_DIR/
   DBUS_SESSION_BUS_ADDRESS/LC_ALL lines 191-192; `TemporaryDirectory` selftest; eleven-class table
   + fallback other) confirmed by source read.
3. **Anchors exact at 07f264.** SKILL.md 142/144/145/156/157/158 and 202/204/205/221/222/223 all
   match the claimed line numbers; PROVINCE.md 22/23/24-30 (last mado-anims.py)/31/32/84/95 match,
   and 95 = `half).` is the file's last line (true end-of-file append).
4. **Province-row finding verified.** `git ls-tree --name-only cd950ec tools/` = 10; eventq/
   options/wsrules tracked-unlisted. At 07f264 tools/ = 11 (globals added): staleness persists and
   the insert-as-row-8 decision should disclose the other three omissions (draft's own proposal).
5. **Notes (no row change).** Selftest count of the landed tool is 63/63 (draft's 47/47 was
   explicitly reference-labeled); 0-byte journal → SETUP unreadable (rc 2) while non-empty
   no-advert → NO_SESSIONS (rc 3); draft cites `PRED-C2-r41-v1` while registered predicate is v2
   (clause i unchanged, verified in `c2-r41-focus-entry-v2.py:121`).

All quotes ≤ 25 words, located and verified by grep/awk on the fetch receipts. No tools installed
(existing python3/git used). No lane files edited — L1 integrates.
