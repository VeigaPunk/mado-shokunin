## Erratum (2026-10-26, round 47)

**E1 - the live host run reads two config files, and the citation names the wrong receipt.** Corrects the parenthetical and the citation at line 57; nothing else in this entry changes.

*What line 57 says:* "one `input` block in `~/.config/hypr/input.conf`, no `device` block" (hyprland-input-devices-r46.md:57), citing `.ufo/waves/round-46/receipts/live-devices-host-l1.txt`.

*What is true:* "one `input` block" holds only for that one file read alone. The effective chain has two input files, in this order:

| order | file | sha256 | input block | kb_layout |
|---|---|---|---|---|
| 1 | `~/.local/share/omarchy/default/hypr/input.conf`, sourced at `~/.config/hypr/hyprland.conf:11` | `bee5aa68cbec0c428fae7a5faf7da49a30e6f78ed96e78a063f08b66942448b8` | `input {` at :2 | `us` at :3 |
| 2 | `~/.config/hypr/input.conf`, sourced at `~/.config/hypr/hyprland.conf:17` | `3769c92ab7660f1795cb6d0af1bcc5a5614a299b29ae8358d1b85936bdd47bf4` | `input {` at :3 | `br` at :10 |

So two `input` blocks reach the compositor and the first one names `us`; the join reports `br` because it parses the given files in order into one state (`tools/mado-devices.py:418-419`, `for t in config_texts: parse_config(t, st)`) and a global is a plain dict assignment (`tools/mado-devices.py:334`, `st.globals[key[len("input:"):]] = rhs`), so each later file overwrites the earlier value. The "no `device` block" half stands in both files: each has zero `device` blocks.

*Corrected citation:* `.ufo/waves/round-46/receipts/live-devices-host-r46.txt` (sha256 `0c749e1d255538a6767992f116d44c48022b7dd8140df50f773fc355dabd956f`) - the read-only run of the landed tool `tools/mado-devices.py` (sha256 `3a80368997120503d5715596a17e762bbcb67a41db23d9241425bf19349d594f`), which passes both files and records both hashes plus the chain: "# chain: ~/.config/hypr/hyprland.conf sources the omarchy default input.conf before the user's input.conf" (live-devices-host-r46.txt:5). The receipt line 57 cites is the draft's run: its header names `.ufo/waves/round-46/l1-draft/mado-devices.py` sha256 `b229efd08d2d329dd60ced114598943d0419dac2f3cf05b1f6c1eb506c49a33b` (live-devices-host-l1.txt:1), 135 changed lines away from the landed tool (30 removed, 105 added, 9 hunks).

*What stands unchanged:* the observation itself. Both receipts print the same fourteen device lines - 10 keyboards, 9 AGREE on `br` with `compose:caps`, fcitx5 as VIRTUAL, 4 mice AGREE at -1.00, `verdict=OK` - so the single-file and two-file runs agree on this host and the entry's numbers are not affected. The r46 receipt adds `MADO_DEVICES_SELFTEST: 59/59 passed`, which the L1 receipt lacks.

*Limit of this erratum:* the two-config run was not repeated in round 47; the r46 receipt is the witness, and only the config hashes, the source lines and the block counts were re-read on the host today (2026-10-26).
