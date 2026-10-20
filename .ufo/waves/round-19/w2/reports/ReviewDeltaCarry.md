# ReviewDeltaCarry — partial

Scope: are the w1 DeltaWalkerConfig 2.17.0→2.17.2 deltas (blur_corner_radius `:22`, `[niri]` `:24-27`, desktopapplications `edit`/ctrl-e `:174`, clipboard remove `after = "SimpleDelete"` `:250`; config 298→305 L / 13,220→13,743 B) reflected wherever walker-deep, walker-deep-r9, walker-live-surface and waybar-walker-semantics state the affected claims? Answer: **yes inside the marked scopes, no at six claim sites**, listed below with measured evidence. All paths relative to `/home/vgpnk/Projects/shokunin/mado-shokunin`. Worktree == `01b8094` (verified `git rev-parse HEAD`); read-only git only.

## Independent re-measurement (all file bytes; walker never executed)

Commands: `wc -l/-c`, `sha256sum`, `stat`, `grep -n`, `tar --zstd -xOf /var/cache/pacman/pkg/walker-2.17.0-1-x86_64.pkg.tar.zst …` (cache read, extraction to /tmp only), and one `python3` byte-read of `/usr/bin/walker` + the extracted 2.17.0 binary. No pacman transaction, no host-service op.

- `/etc/xdg/walker/config.toml`: 305 L / 13,743 B / sha256 `3c5c6867d0216d0c…` / mtime 2026-10-08 11:14:32 -0300. Contains `blur_corner_radius = 20` `:22`, `[niri]` `:24-27`, `{ action = "edit", bind = "ctrl e" }` `:174`, `{ action = "remove", bind = "ctrl d", after = "SimpleDelete" }` `:250`.
- Distinct `after` values now **7**: Nothing 23, AsyncClearReload 28, AsyncReload 17, Nothing/SimpleDelete/KeepOpen/ClearReload/Close (SimpleDelete ×1). Old file (cache, sha `5b4e47b7…`, 298 L): exactly the 6 walker-deep lists, zero `SimpleDelete`/`blur_corner_radius`/`[niri]`.
- Anchor drift confirmed: `[providers]` :52→:58, prefixes block :69-107→:75-113, MERGED comment :112→:118, reload-bearing rows :117-296→:123-303, quick_activate :47→:53, placeholders :35→:41, `"symbols" = 3` :32→:38, max_results :61→:67, `[shell]` :23→:29, `[providers.argument_delimiter]` :63→:69 (map: +6 for n≤167, +7 for n≥168 — w1 §5 map is accurate).
- Binary `/usr/bin/walker` (sha `25240650…` per S096): embedded default at **806,960**, `b[i:i+13743]==file` **True**; `struct Walker with 29 elements` **0**, `…31 elements` **1**; `SimpleDelete` ×2; literal `2.17.2` at 856,302, `2.17.0` absent; `WALKER_` 820,714; `config.toml` 820,703; `config not initialized` 820,721; `Failed to set loaded config` 806,884 (lowercase form absent); `reload` 814,881; `Reload` count **51**, first 753,642; `hide search input` 832,867; `XDG_DATA_HOME` 837,965; socket run `XDG_RUNTIME_DIRwalkerwalker.sock` 832,681. Old binary (cache): `WALKER_` 797,295, `config.toml` 797,284, socket run 818,871, `hide search input` 819,042 — matching the notes' dated pins.

## What IS already reflected (checked, not assumed)

- `corpus/knowledge/walker-deep.md:620-631` — freshness pointer names all four deltas and says "§2.1-2.4 key enumerations are incomplete for 2.17.2"; the wave-2 block re-pins embedded offset 806,960 (S091), struct arity 31, and the +6/+7 anchor shift. §2.1 (:68-69), §2.3 (:109), §2.4 (:124-147), §4.2 anchors (:250, :245-247), §5/§6.1/§6.3, §7.4, §13 pin table (:587), §14 expectations (:604/:607) are all covered by pointer+wave-2 in substance.
- `corpus/knowledge/walker-deep-r9.md:403-414` — wave-2: "Every §3.3/§5.5 rodata offset is version-bound … The note's values describe the 2.17.0 binary" — covers :109, :175, :179-184 and §5.5's `Reload`=52 (:320); pointer covers §1 config layers/:64, :69, §5.9/:334.
- `corpus/knowledge/walker-live-surface.md:305-314` — pointer marks §1 binary/package rows, §2 help, §3 L0 equality at 784,064; wave-2 records the packaged-config move 13,220 `5b4e47b7…` → 13,743 `3c5c6867…` (covers :114 and :277 in substance) and the S096 re-read.
- `corpus/knowledge/waybar-walker-semantics.md:465-476` — pointer marks §6.1's "298 lines" (:234) and the §6.2 table with its anchors; wave-2 records 305 L / 13,743 B / `3c5c6867…`.

## Findings — claims now false (or stale) and not marked

**F1 — walker-deep.md:162-164 (§3): the `after`-value enumeration is incomplete; not covered by any marked scope.** §3 states "(the `after` values in use: `Nothing`, `Close`, `KeepOpen`, `AsyncReload`, `AsyncClearReload`, `ClearReload`)". The host set is now 7 values (`SimpleDelete` at `/etc/xdg/walker/config.toml:250`, measured). The pointer (:623) names the SimpleDelete delta but scopes the incompleteness to "§2.1-24 key enumerations", and its anchor clause lists §2.1-2.4/§4.2/§7.4 only; the wave-2 block (:628-631) covers anchors, not value sets. §3 is in no marked scope. Severity: medium — this is exactly the class of claim the pointer says it is correcting, one section over.

**F2 — walker-deep-r9.md:176 (§3.3): "(`/etc/xdg/walker/config.toml:117-296` carries the same rows)" is false twice over; the r9 erratum never names the config-content deltas.** Rows now sit at `:123-303` (measured) and are not the same rows: clipboard remove is `after = "SimpleDelete"` (`:250`) and desktopapplications gained `{ action = "edit", bind = "ctrl e" }` (`:174`). r9's pointer marks packaged size/sha (§1/§5.9) and, via wave-2, the §3.3/§5.5 rodata offsets and values — but no r9 block mentions `blur_corner_radius`, `[niri]`, the ctrl-e row, `SimpleDelete`, or the anchor drift. Same row's `Reload | 52` (now 51, first 753,642, measured) is covered only by wave-2's generic tail "The note's values describe the 2.17.0 binary" [INFERENCE that a count is meant to be included under "values"]. Severity: medium.

**F3 — walker-deep-r9.md:406 (:290-291 and :345): §4 and §6 are declared "Not version-bound" while containing version-bound claims.** Pointer line :406 lists "(§1, §4, §6)" under host-file/units state, but §4:291 asserts "The embedded-config offset (784,064, round-5 pin) also reproduces with byte-equality `True`" (now **806,960 True**, measured) and §6:345 pins packaged sha `5b4e47b7…` (now `3c5c6867…`, measured; the new sha is recorded nowhere in r9). Both are version-bound, both false on 2.17.2, both outside the pointer's version-bound bullets (§1/§5.9, §3.3/§5.5). Severity: medium.

**F4 — walker-live-surface.md: binary-offset claims outside the pointer's named scope.** The pointer (:306) marks §1 identity, §2 help, and §3 **L0 equality only**; the wave-2 block (:310-314) re-read only the binary sha and the version literal. Unmarked and now false: §3 env census offsets `config.toml` 797,284 / `WALKER_` 797,295 (:130-132; now 820,703/820,714); §4 "Path-construction token in the binary (offset 818,871)" (:172; the run is at 832,681, `XDG_DATA_HOME` at 837,965 — measured; §4 is marked only as "PIDs, sockets, D-Bus owner and layer invariant", :307); §5 ledger row 5 "exactly one bare `WALKER_` literal (offset 797,295)" (:229; §5 named nowhere); §6 expectations `797295` (:251), `784064 True` (:258) and "offset ≈818,871 region" (:249; now 820,714 / 806,960 True / 832,867). Severity: medium-low (same census family, five sites).

**F5 — waybar-walker-semantics.md:385-386 (§8 item 3): packaged anchor `/etc/xdg/walker/config.toml:53-58` drifts to `:59-64` (measured); §8 is outside the pointer (:468 lists §6.1, §6.2, §6.2/§6.3/§6.4 strings claims, §6.8, §9 item 7) and outside wave-2.** Minor sibling: §6.3's packaged anchors `:31-32` / `:53-58` (:261-262) — the pointer's §6.3 entry names only the GridView/list_max_columns strings claims, so the two anchors drift unmarked. Severity: low (pointer drift, not value claims).

**F6 — walker-deep.md:623 internal contradiction (consistency).** "…and **every** `/etc/xdg/walker/config.toml` line anchor (§2.1-2.4, §4.2, §7.4)": "every" is contradicted by the three-section scope. §3 (`:69-107` at :156, `:63-67` at :168 → now `:75-113`/`:69-73`), §4.3 (:266) and §9 (:514) anchors are saved only by the wave-2 block's generic "shifted +6/+7, map in w1 DeltaWalkerConfig" sentence (map verified accurate). A strict reading leaves them unmarked. Severity: low — fix is a one-word scope repair.

## Verdict on the assignment question

The four deltas and the 298→305 move **are** reflected in every place the round-19 erratum/wave-2 blocks name (walker-deep §2.1-2.4 + pins + arity; r9 §1/§3.3/§5.5/§5.9; live-surface §1-§3-L0 + L1 values; semantics §6.1-§6.2), and every measured value those blocks record reproduced exactly under independent re-measurement. They are **not** reflected at F1-F5; F6 is the scope wording that lets F1's neighborhood stay ambiguous. No finding touches C1/C2/C3; these are completeness gaps in the delta carry, not calibration or tripwire issues.

## Limits

- `walker` never executed (host pause): all binary facts are file-byte reads of `/usr/bin/walker` and the cached 2.17.0 binary; no `--version`/`--help` behaviour checked (r9 §5.1/§5.2, live-surface §2 stay [UNK] as their errata already say).
- Whether wave-2's "The note's values describe the 2.17.0 binary" was meant to cover the `Reload`=52 *count* (not just offsets) is [INFERENCE]; F2 is limited to the config-rows parenthetical, which no reading covers.
- `waybar-walker-plane.md` is outside the four-note scope: its packaged anchors at `:440`/`:443` (`:53-58`, `:31-32`) and its erratum (:479-484, which marks only the version print and help list) suggest the same F5-class gap there [INFERENCE from grep; not audited].
- `walker-route-r18.md` records the drift correctly (:239-244, :182, :206) and was used only as cross-reference, per w1.
- Old-package reads came from `/var/cache/pacman/pkg` (cache hit, no network); no fetch receipts this seat — no URLs fetched.

## Installs

none.
