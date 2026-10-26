# ScoutCoverage report - done
Full findings: `.ufo/waves/round-44/w1/ScoutCoverage/coverage.md`.
Base 6a1a905: zero hits for sendWindowSize/realToReportSize/scheduleConfigure/pendingSizeAcks/onAck/setSize/xdg-shell/xdg_toplevel/set_size_request/maximized/work-area/setTargetSizeAndPosition/eFullscreenMode in corpus/knowledge, PROVINCE.md, SKILL.md, tools (only `SCORECARD.md:1`, raw `.ufo` pins). Held: r43 §4 default_size(420,500)+application_id, keybind `fullscreen` dispatcher vocabulary.
C2: new coverage-map row after README.md:71 + new `### Round-44` sub-route continuing README.md:294-301 (moves only "the client's acknowledgement path"). New ground (xdg-shell, GTK toplevel, ack path), deepening of r43 §4; S164 scope does not cover onAck 1514 / realToReportSize 1685 / sendWindowSize 1732.
C1: no coverage credit (operability); stale sentences README.md:298, SKILL.md:158,225,246-290(274-277),PROVINCE.md:32.
Tool: git grep only; no install.
