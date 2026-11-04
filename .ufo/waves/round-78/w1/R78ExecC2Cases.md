# R78ExecC2Cases — C2 runbook re-derivation (17 cases, live execution + anchor audit)

Seat: R78ExecC2Cases (executor) · round 78 wave w1 · 2026-11-04 · read-only on the repo, live read verbs only.
Inputs: frozen declaration `.ufo/waves/round-78/claims-declaration-r78.md`; control set `.ufo/waves/round-78/controls/c2-runbook-cases-r78.json` (sha256 `f1c75a7d…`, verified); frozen instrument `quality/counters/c2-r78-runbook.py` sha256 `b9c774b8…` verified byte-identical in commit `44a36b64` (`git cat-file blob`) and in my scratch copy. SKILL.md pinned at `44a36b64` (2859 lines; working tree was identical at pin time). No repo file was edited; only read verbs were executed (`hyprctl version|configerrors|monitors|getoption|binds -j|layers|activeworkspace|clients|workspaces|instances`, `pgrep`, `makoctl mode`, `omarchy theme current|version`, file reads, read-only git).

## 0. Instrument-state observation (data, not judged)

During this seat's run the lane landed post-amendment commits (`00ed4ac0` → `fa6f3fda` → `93a10a13` → `90fc8d84` → `e117a113` → `d27c5ff4`; HEAD `d27c5ff4df9ee7c…`). The counter on disk is now sha256 `9171bb36…` (HEAD) versus the frozen `b9c774b8…` at `44a36b64`. The deltas are exactly two, both verifiable in the diff:

- `observed()` privacy repair (90fc8d84): JSON-kind probe lines now print `rc=<n> json-bytes=<n>` instead of quoting dump text — "a monitors reply carries the output's serial/description" (HEAD `quality/counters/c2-r78-runbook.py:239-246`). The original receipt quoted `out='{\n"DP-1"…'` for layers-dump/monitors-dump; the receipt now on disk does not.
- anchor-check tightening (d27c5ff4): file-wide substring containment (`if case["skill_anchor"] not in skill`, frozen bytes line 365) replaced by `row_bound()` — the anchor must appear in a Markdown table row's **first (command) cell** (HEAD `quality/counters/c2-r78-runbook.py:249-259`, check at `:398-400`), +3 selftest rows.

Reproductions (receipt copies in `.ufo/waves/round-78/w1/R78ExecC2Cases/`):

| run | verdict |
|---|---|
| frozen bytes `b9c774b8…` at rev `44a36b64` | `cases=17 executed=17 matched=17 shapes=12/12 anchors=17/17 control=5/17 mutants=5 killed=5 verdict=TARGET_MET` — probe lines identical in format and content to the original frozen receipt (`receipt-frozen-counter-at-44a36b64.txt`, sha `ef50a4e6…`) |
| HEAD bytes at rev `44a36b64` | same contract line, `TARGET_MET` (`receipt-head-counter-at-44a36b64.txt`, sha `a6a9a2c7…`) — the row-bound check passes at the pinned rev too |
| HEAD bytes at rev HEAD `d27c5ff4…` | `TARGET_MET`, stdout byte-identical to committed `.ufo/waves/round-78/receipts/measurement-c2-r78.txt` (sha `74339011…`) |

Provenance note: the declaration pins the receipt to `44a36b64` ("both counters TARGET_MET at 44a36b64"); the receipt file at that path is now the post-repair one (e117a113 re-measured at `90fc8d84`; its text no longer carries dump output). Facts only; the predicate/case/label/kill-rule/target text of the contract line is unchanged across all three runs.

## 1. Per-case re-derivation — `case | live | declared | anchor row verdict | class`

All 17 live runs executed today under the counter's completed env; every live output equals its declared value; the full counter reproduces 17/17 at both revs. "Anchor row verdict" cites SKILL.md at `44a36b64` (the probe table sits at lines 207-229; none of these rows changed by HEAD — the post-amendment SKILL.md diff touches only the gate-registry rows at ~743-746).

| case | live (2026-11-04) | declared | anchor row verdict | class |
|---|---|---|---|---|
| version | rc0 `Hyprland 0.56.2 built from branch v0.56.2 at commit efb5099… clean ([gha] Nix: update inputs).` | same | :208 row states probe + sample; regex `^Hyprland [0-9]+\.[0-9]+\.[0-9]+ ` absorbs version churn — consistent | regex shape; env-supplied (HIS, PATH); `head -n 1` masks hyprctl's rc |
| configerrors | rc0 `` (empty) | same | :209 "empty = clean" — consistent | empty shape; env-supplied (HIS); rc gate real here (bare shell: rc1) |
| monitors-size | rc0 `DP-1 3440x1440@99.99700` | same | anchor hits TWO rows: :210 (fixed sample `DP-1 3440x1440@99.997`) and :229 (shape row). Covered, but the anchor string alone does not name the claim row — **shared-anchor flag** (also matched prose :75 and the tools row :2126 under the frozen substring check) | regex shape; needs `jq`; keys `.[0]` (first array element, positional) |
| monitors-reserved | rc0 `[0,26,0,0]` | same | :210 + :229; the actual claim ("four non-negative integers", :229) is not the first-anchored row — **shared-anchor flag** | int4 shape; needs `jq`; `.[0]` positional |
| gaps-out | rc0 `custom type: 0 0 0 0` | same | :211 template row names the key and the exact value — consistent | **exact, value-bound but volatile** (gaps toggle `window-no-gaps.conf` flips it; the `custom type: ` prefix is Hyprland-release text); `head -n 1` masks rc |
| kb-layout | rc0 `str: br` | same | :211 names key + value — consistent | **exact, value-bound**; volatile only on deliberate `input.conf` edit or prefix-text change |
| binds-count | rc0 `192` | `192` | :212 "192 (matches file arithmetic)" — consistent | int_range [1,100000] shape; needs `jq` |
| layers-namespaces | rc0 `wallpaper,waybar` | same | anchor hits :213 (dated fixed capture, pid 1707) AND :229 (shape row) — claim split across two rows, **shared-anchor flag** | sorted_unique shape with `must_include: waybar` (fails if waybar is down — correct bar-presence semantics); needs `jq` |
| waybar-process | rc0 `1720` | `1720` | :218 row sample says waybar 1707 (dated 2026-10-14; historical-labeled); live pid today 1720, absorbed by int_range — consistent | int_range [1,4194304]; **the only case needing no counter-supplied environment** |
| mako-mode | rc0 `default` | `default` | :220 "DND state → default" — consistent | **exact, value-bound but volatile**: enabling DND produces exactly the committed negative `do-not-disturb` |
| omarchy-theme | rc0 `Matte Black` | same | :215 — consistent | **exact, value-bound but volatile**: `omarchy theme set` breaks it; SKILL :1068-1069 itself declares the theme operator-owned mutable state |
| omarchy-version | rc0 `3.8.3` | `3.8.3` | :215 — the SAME combined row as omarchy-theme (`omarchy theme current` / `omarchy version` … `Matte Black` / `3.8.3`). This is the r77 `omarchy-version` defect class: two probes bound to one row. Mitigated: the row explicitly states both values, so each case's claim is stated; the dual-pin paragraph :23-24 also matches the substring under the frozen check | regex shape; env-supplied (PATH + OMARCHY_PATH) |
| active-workspace | rc0 `{"id":1,"name":"1"}` | same | :227 round-78 shape row ("id an integer, name non-empty; ids change") — consistent | json_object_fields shape; needs `jq` |
| layers-dump | rc0 JSON dict keyed DP-1 with levels 0-3 | (no frozen value; shape-only) | :229 — consistent | levels_dump shape; env-supplied |
| monitors-dump | rc0 JSON array, DP-1 name/width/height/reserved/scale | (shape-only) | :229 — consistent | array_fields shape (min 1; name str, w/h positive ints, reserved int4, scale number); env-supplied |
| clients-count | rc0 `2` | `2` | :228 round-78 row ("positive / non-negative integers; counts change") — [0,100000] is the non-negative leg, consistent | int_range; needs `jq` |
| workspaces-count | rc0 `2` | `2` | :228 — [1,1000] is the positive leg, consistent | int_range; needs `jq` |

## 2. Flags asked for by the seat spec

**(a) Rows whose anchor is shared (r77 `omarchy-version` defect class).**
- Same anchor string across cases: `hyprctl monitors` → monitors-size, monitors-reserved, monitors-dump (3 cases; claim split between fixed-sample row :210 and shape row :229); `hyprctl layers -j` → layers-namespaces, layers-dump (2 cases; :213 vs :229); `hyprctl getoption <key>` → gaps-out, kb-layout (2 cases; coherent — one template row :211 states both claims by design).
- Same anchor row across cases: `omarchy theme current` and `omarchy version` both bind to the single combined row :215 — the direct survivor of the r77 class; mitigated because the row states both values, but a future edit of one value cell now regresses two probes at once.
- Mechanism note: at the frozen rev the anchor check is substring containment (frozen bytes `:365`), which survives deletion of the very row it names (e.g. `hyprctl monitors` also matches prose :75 and the unrelated registry row :2126; `makoctl mode` matches 8 lines; `pgrep -a` matches a gate-failure report line :1900). The landed d27c5ff4 `row_bound()` fixes the mechanism (first table cell); all 17 anchors still bind at `44a36b64` and at HEAD (both reruns green).

**(b) Expectations really volatile but bound by value** (the 5 exact rows minus the genuinely static one): `mako-mode` (DND toggle → committed negative becomes live), `omarchy-theme` (operator theme switch), `gaps-out` (gaps toggle; plus the `custom type: ` prefix is Hyprland-version text baked into the exact value), `kb-layout` (deliberate layout change; `str: ` prefix likewise). `configerrors` (empty) is shape-like and fine. The declaration's "live values remain a point sample" sentence covers these, but they are the rows that age.

**(c) Commands needing an environment the counter silently supplies** (`session_env`, frozen bytes `:78-99`):
- All 10 `hyprctl` cases: the caller shell here has NO `HYPRLAND_INSTANCE_SIGNATURE` (observed: both bare and session shells print `HYPRLAND_INSTANCE_SIGNATURE not set!` on stdout; `hyprctl version | head` still exits 0 through `head`). The counter invents it by scanning `$XDG_RUNTIME_DIR/hypr/*/​.socket.sock` and taking the **sorted-first** match (`:79-87`). Host today: exactly 1 instance (`hyprctl instances -j | jq length` → 1), so the pick is unambiguous — but on a multi-instance host the probes bind to an arbitrary instance, the exact trap SKILL.md:472 warns about ("resolve via the session's own signature; never guess").
- `makoctl mode`: needs `XDG_RUNTIME_DIR` (observed: with XDG only → rc0 `default`; with `DBUS_SESSION_BUS_ADDRESS` but no XDG → rc1). The counter supplies XDG (`:78`).
- `omarchy theme current` / `omarchy version`: need PATH extended with `~/.local/share/omarchy/bin` (bare → rc127) and, for `version`, `OMARCHY_PATH` — without it the session shell reproduces `omarchy version` rc1, stderr `cat: /version: No such file or directory` (the script concatenates `$OMARCHY_PATH/version`). The counter synthesizes both (`:88-99`).
- `jq`/`head` availability and `LC_ALL=C`/`LANG=C` come from the same silent env. Only `waybar-process` (pgrep) runs with no counter help at all.

Related, observed: the three `| head -n 1` pipelines (version, gaps-out, kb-layout) report the *pipeline* rc — `head`'s 0 — even when hyprctl fails (observed rc0 with the error text as stdout under a HIS-less shell). The content match catches every such case, so no case passes wrongly, but `executed=17` counts these as executed on a masked rc.

## 3. Rows that would break on a plausible host change

- **Theme switch** (`omarchy theme set …`) → `omarchy-theme` FAILS (exact).
- **DND on** → `mako-mode` FAILS (exact; the negative sample becomes the live value).
- **Gaps toggle / looknfeel edit** → `gaps-out` FAILS (exact).
- **Deliberate `input.conf` layout change** → `kb-layout` FAILS (exact).
- **Hyprland release that renames the `getoption` prefix text** → `gaps-out` + `kb-layout` FAIL (prefix is inside the exact value).
- **Waybar down** (crash, no restart) → `waybar-process` FAILS (rc1) and `layers-namespaces` FAILS (`must_include: waybar`); `layers-dump` still passes (shape) — arguably correct: the namespace probe is the bar-presence probe.
- **Waybar restart** → nothing fails (pid range, namespace returns, dump shapes hold).
- **Another workspace / more clients / window churn** → nothing fails (shapes absorb; live samples verified with id=1 today).
- **Monitor added/changed** → nothing fails shape-wise; note monitors-size/reserved read `.[0]`, so they follow whatever monitor sorts first — shapes hold, only the held r77 frozen values detach.
- **A second Hyprland instance** → all 10 hyprctl probes may bind to the wrong instance (sorted-first HIS pick); unambiguous today (1 instance).
- Survives cleanly: Hyprland upgrade (`version` regex), omarchy upgrade 3.9/3.10 (`omarchy-version` regex, covered by committed samples), bind-count drift, extra layer namespaces (sorted_unique absorbs any extra; needs `waybar` present).

## 4. Evidence

Copied into my write dir `.ufo/waves/round-78/w1/R78ExecC2Cases/`: `receipt-frozen-counter-at-44a36b64.txt` (sha `ef50a4e6…`), `receipt-head-counter-at-44a36b64.txt` (sha `a6a9a2c7…`), `receipt-head-counter-at-head.txt` (sha `74339011…` = committed receipt). Repo-side citations: `.ufo/waves/round-78/controls/c2-runbook-cases-r78.json` (all argv/frozen/samples quoted above), `quality/counters/c2-r78-runbook.py` at `44a36b64` (`:78-99` env synthesis, `:365` substring anchor check) and at HEAD (`:239-246`, `:249-259`, `:398-400`), SKILL.md at `44a36b64` lines 207-229 (probe table), 23-24 (dual pin), 58-61, 1068-1069 (theme operator-owned), 472 (instance trap), 2126. No repo file modified; scratch deleted.

Report: .ufo/waves/round-78/w1/R78ExecC2Cases.md
