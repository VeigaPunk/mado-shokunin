# WikiUsingHyprctl — pinned source opening

## Behavior and scope

Opened the `hyprland-wiki` page `Using hyprctl` at commit `c66e8de21f5ecdc4bc5e278e7d94800ea10957af`. The page documents a runtime `hyprctl binds` query, an `instances` inventory, the `i` instance selector, and JSON output with `-j`. It does not describe static config-tree parsing, `source =` resolution, or how the compositor constructs a bind table from config bytes. Its documentation is not a measurement of the installed compositor.

The fetched page lists only the short `i` flag, described as selecting an instance by id or index in `hyprctl instances`; this file contains no `--instance` spelling. It shows `hyprctl -j monitors` and identifies `j` as JSON output.

## Gates and commands

This is a source-opener item only. No C1 counter was scored, no C2 demonstration was rerun, and no resolver/tool was built. No host compositor command or mutation was run.

Exact fetch and metadata command:

```sh
mkdir -p /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/fetch/a3w1 && timeout 60 prlimit --as=4000000000 curl -fsSL https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c66e8de21f5ecdc4bc5e278e7d94800ea10957af/content/configuring/core/advanced-configuration/using-hyprctl.md -o /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/fetch/a3w1/WikiUsingHyprctl.bin && sha256sum /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/fetch/a3w1/WikiUsingHyprctl.bin && wc -c -l /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/fetch/a3w1/WikiUsingHyprctl.bin
```

The command chain completed successfully. Output:

```text
95d8b8422a1fd25229bfe350e05624d8a318c746803efb7f3893015bf7c417f0  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/fetch/a3w1/WikiUsingHyprctl.bin
 295 8239 /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/fetch/a3w1/WikiUsingHyprctl.bin
```

The four quotations below were checked with Python by decoding the fetched bytes as UTF-8 and testing whether `' '.join(quote.split())` is a substring of `' '.join(text.split())`; all four checks matched. Each quotation is fewer than 25 words.

## Located quotations

1. `content/configuring/core/advanced-configuration/using-hyprctl.md:249`

   ```text
   binds                - lists all registered binds
   ```

   This describes `binds` as a runtime query for registered binds, not the config parser that produced them.

2. `content/configuring/core/advanced-configuration/using-hyprctl.md:256`

   ```text
   instances            - lists all running instances of Hyprland with their info
   ```

   This identifies the running-instance inventory that the selector refers to; it does not document starting or configuring an instance.

3. `content/configuring/core/advanced-configuration/using-hyprctl.md:289`

   ```text
   hyprctl -j monitors
   ```

   This is the page's concrete example of the short JSON option, and documents an output mode rather than bind-table construction.

4. `content/configuring/core/advanced-configuration/using-hyprctl.md:293-294`

   ```text
   - `j` - output in JSON
   - `i` - select instance (id or index in hyprctl instances)
   ```

   These flag descriptions establish that JSON output and instance targeting are query options; they do not establish an offline oracle or static bind resolver.

## Duplicate review and SOURCES draft

The pinned raw URL is **not an exact URL duplicate of S016**: S016 cites the live wiki URL `https://wiki.hypr.land/Configuring/Advanced-and-Cool/Using-hyprctl/`, whereas this fetch uses a commit-pinned `raw.githubusercontent.com` URL. However, the pinned raw URL **exactly duplicates S167's source URL** in `corpus/SOURCES.md`; S167 already records the identical 8,239-byte blob and SHA-256. The proposed scope below highlights binds/instances, but adding it would repeat that exact pinned URL across scopes and be flagged by the duplicate-URL census. Draft only; do not append a second registry row without resolving the existing S167 entry.

```text
| S? | Using hyprctl — https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c66e8de21f5ecdc4bc5e278e7d94800ea10957af/content/configuring/core/advanced-configuration/using-hyprctl.md | docs | A | Hyprctl bind-list, running-instance inventory, instance selection and JSON-output flags at the pinned wiki revision | content/configuring/core/advanced-configuration/using-hyprctl.md:249,256,289,293-295 @ c66e8de21f5ecdc4bc5e278e7d94800ea10957af, sha256:95d8b8422a1fd25229bfe350e05624d8a318c746803efb7f3893015bf7c417f0, 8239 B | Documents the runtime binds query, instance inventory and selector, and JSON output; does not establish static config parsing or compositor behavior | mined | 2026-10-23 | on-release | corpus/knowledge/bind-table-r25.md |
```

## Touched surfaces, out of scope, and artifacts

- Wrote the required fetched blob and this report only; did not write to `corpus/`.
- No source package/tool installation was needed.
- Out of scope: implementing or scoring `tools/mado-binds.py`, running `count.py`, and making any claim about live host behavior.
- Artifact paths (relative to the lane): `.ufo/waves/round-25/fetch/a3w1/WikiUsingHyprctl.bin`; `.ufo/waves/round-25/a3w1/reports/WikiUsingHyprctl.md`.
