# ReboundArg — C1 recall/binding oracle

Authored `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w1/oracles/ReboundArg.json` as an independent static expectation.

- The Python helper is visible, defined before use, and directly passes its bound `argv` to `subprocess.run`.
- The two calls bind distinct literal argv lists, so both commands are exact and must be retained: `pacman -Q hyprland` and `pacman -Q waybar`.
- Both are `package_query` findings with `observed` evidence: execution reaches the known process-spawning call through a visible helper with bindable arguments. No callback or recursion makes either path uncertain, so `lead` is not appropriate.
- The transcript is inert data and was not executed. I did not open the production tool or run the scanner; no build, tests, or other verification was performed.

Sources: `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md` S108/S111; `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/knowledge/tripwire-precision-r20.md:27`; prior category semantics at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/precision/expected.json:1028-1035`.

Residual risk / verification gap: this is the semantic oracle, not a measurement; scanner agreement remains unverified by design for this wave. No tools were installed or updated.
