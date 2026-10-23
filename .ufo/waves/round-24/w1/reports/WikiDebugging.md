# Wiki debugging source report — round 24, wave 1

## Behavior and findings

**Observed in the pinned wiki bytes:**

- `content/contributing-and-debugging/_index.md` describes a live-log command that watches `hyprland.log`, filters lines containing `arranged`, and tails the last 40 lines; it says to replace `hyprland` with `hyprlandd` for debug builds.
- `content/crashes-and-bugs/_index.md` says to set `debug.disable_logs` to `false` for file logging, and `debug.gl_debugging` to `true` for OpenGL messages. It also documents dynamic toggling through `hyprctl eval`, plus `HYPRLAND_TRACE=1 AQ_TRACE=1` for very verbose trace logs.
- The `Debug` category in `content/configuring/core/config-options.md` is marked for development/testing. Its table says `disable_logs` defaults to `true`, `enable_stdout_logs` to `false`, and `disable_time` to `true`; it also lists `gl_debugging` and other debug controls.
- `content/configuring/core/environment-variables.md` describes `HYPRLAND_TRACE` as enabling more verbose logging and `AQ_TRACE` as enabling very verbose trace logging.
- The rules overview says rule props in `match` determine whether a window gets a rule, all props must match for application, and rules are evaluated top-to-bottom with named rules first. It also explains two `hyprctl clients` fullscreen fields. These are rules semantics, not a documented rule-attribution log format.

**Scoped negative sweep:** `functions.grep` searched the fetched contribution-debugging page, crashes-and-bugs page, debug section of config-options, and relevant environment-variable lines using the case-insensitive pattern `\b(windowrule|layerrule|getprop|rules?|prop|tag|match)\b`. Output: `No matches found`. This is limited to those fetched debugging/debug-variable passages; it is not a claim about every wiki page or Hyprland source file.

**Inference:** The wiki documents generic file/stdout/trace logging routes, but these inspected debugging passages do not promise that logs identify which window/layer rule matched or which rule produced an effect. A generic log capture alone is therefore not documentary proof of rule attribution. Host behavior remains **[UNK]**; no host logs or runtime behavior were inspected.

## Proposed claim rows

A1–A3 use the provisional `S?` for the `Rules` source row below. Quotes are verbatim, whitespace-collapsed substrings of `WikiDebugging-4.bin`; Python validation passed for all three (A1: 13 quote words; A2: 10; A3: 17; each quote-topic, quote-substring, claim length, and four-word anchor check passed).

```text
| A1 | The wiki says rules can enforce specific options for matched windows/workspaces/layers. | S? | "Rules can be used to enforce specific options for matched windows/workspaces/layers." |
| A2 | The wiki states: _All_ props must match for a rule to be applied. | S? | "_All_ props must match for a rule to be applied." |
| A3 | Rules are evaluated top to bottom, but all named rules are evaluated first, then all anonymous ones. | S? | "Rules are evaluated top to bottom, but all named rules are evaluated first, then all anonymous ones." |
```

## Draft SOURCES rows

IDs remain the provisional `S?` required for integration; source rows are distinguished here by title and fetch artifact. The `S?` in A1–A3 maps to the `Rules` row.

```text
| S? | Contributing and Debugging — https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c66e8de21f5ecdc4bc5e278e7d94800ea10957af/content/contributing-and-debugging/_index.md | docs | A | Live log viewing | content/contributing-and-debugging/_index.md:84-97 @ c66e8de21f5ecdc4bc5e278e7d94800ea10957af, sha256:f0369f91a39c5cca7e3c8376e59fb27023a92a2393697e7b9b69bc6ac06217ba, 3698 B | Gives a live log tail command and names the debug-build log directory | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |
| S? | Crashes and Bugs — https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c66e8de21f5ecdc4bc5e278e7d94800ea10957af/content/crashes-and-bugs/_index.md | docs | A | File and trace logs | content/crashes-and-bugs/_index.md:6-15,17-26,65-71 @ c66e8de21f5ecdc4bc5e278e7d94800ea10957af, sha256:a38b772750c12be106ac41e15ad2cb5bb4a848902945b19b438e8cf04d5b8d98, 5833 B | Gives file-log/OpenGL toggles, dynamic toggle instructions, and trace-log instructions | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |
| S? | Configuring Core Config Options — https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c66e8de21f5ecdc4bc5e278e7d94800ea10957af/content/configuring/core/config-options.md | docs | A | Debug config settings | content/configuring/core/config-options.md:793-824 @ c66e8de21f5ecdc4bc5e278e7d94800ea10957af, sha256:8c183e0223bda890498df4d19c69a5b0e5423e023a4f6aee3eebc0f96df86ce0, 58796 B | Lists debug settings and their descriptions/defaults, including file/stdout logging controls | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |
| S? | Rules — https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c66e8de21f5ecdc4bc5e278e7d94800ea10957af/content/configuring/core/rules/_index.md | docs | A | Rule match and evaluation semantics | content/configuring/core/rules/_index.md:6-20 @ c66e8de21f5ecdc4bc5e278e7d94800ea10957af, sha256:46fee4dba2801e2bb5554df13cbabf1e6476dec948de180e88c687c1a307b789, 953 B | Defines props, effects, all-props matching, rule order, and two clients-output field meanings | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |
| S? | Configuring Core Environment Variables — https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c66e8de21f5ecdc4bc5e278e7d94800ea10957af/content/configuring/core/environment-variables.md | docs | A | Debug environment variables | content/configuring/core/environment-variables.md:20-39 @ c66e8de21f5ecdc4bc5e278e7d94800ea10957af, sha256:a94878cbc0dd4b851da04d351570297a721380ee4a02066e36658ba283c04b42, 3863 B | Describes HYPRLAND_TRACE and AQ_TRACE as logging controls | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |
```

## Exact fetch commands and outcomes

All fetches used ordinary `curl` against the pinned raw GitHub URLs. `sha256sum` and `wc -c` followed each successful fetch in the same `&&` chain.

```sh
mkdir -p /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1 && timeout 30s curl -fsSL 'https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c66e8de21f5ecdc4bc5e278e7d94800ea10957af/content/contributing-and-debugging/_index.md' -o /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/WikiDebugging-1.bin && sha256sum /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/WikiDebugging-1.bin && wc -c /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/WikiDebugging-1.bin
mkdir -p /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1 && timeout 30s curl -fsSL 'https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c66e8de21f5ecdc4bc5e278e7d94800ea10957af/content/crashes-and-bugs/_index.md' -o /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/WikiDebugging-2.bin && sha256sum /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/WikiDebugging-2.bin && wc -c /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/WikiDebugging-2.bin
mkdir -p /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1 && timeout 30s curl -fsSL 'https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c66e8de21f5ecdc4bc5e278e7d94800ea10957af/content/configuring/core/config-options.md' -o /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/WikiDebugging-3.bin && sha256sum /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/WikiDebugging-3.bin && wc -c /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/WikiDebugging-3.bin
timeout 30s curl -fsSL 'https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c66e8de21f5ecdc4bc5e278e7d94800ea10957af/content/configuring/core/rules/_index.md' -o /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/WikiDebugging-4.bin && sha256sum /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/WikiDebugging-4.bin && wc -c /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/WikiDebugging-4.bin
timeout 30s curl -fsSL 'https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c66e8de21f5ecdc4bc5e278e7d94800ea10957af/content/configuring/core/environment-variables.md' -o /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/WikiDebugging-5.bin && sha256sum /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/WikiDebugging-5.bin && wc -c /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/WikiDebugging-5.bin
```

Outcome receipts:

| Fetch artifact | `sha256:` | Bytes |
|---|---|---:|
| `WikiDebugging-1.bin` | `f0369f91a39c5cca7e3c8376e59fb27023a92a2393697e7b9b69bc6ac06217ba` | 3698 |
| `WikiDebugging-2.bin` | `a38b772750c12be106ac41e15ad2cb5bb4a848902945b19b438e8cf04d5b8d98` | 5833 |
| `WikiDebugging-3.bin` | `8c183e0223bda890498df4d19c69a5b0e5423e023a4f6aee3eebc0f96df86ce0` | 58796 |
| `WikiDebugging-4.bin` | `46fee4dba2801e2bb5554df13cbabf1e6476dec948de180e88c687c1a307b789` | 953 |
| `WikiDebugging-5.bin` | `a94878cbc0dd4b851da04d351570297a721380ee4a02066e36658ba283c04b42` | 3863 |

Python validation used `Path.read_bytes()`, UTF-8 decode, whitespace collapse with `re.sub` over whitespace, and assertions for each proposed row: quote substring, <=25 quote words, >=8 claim words, rule-topic term, and four-word quote anchor. All three assertions passed; output reported `quote_substring=True topical=True anchor4=True` for A1–A3.

## Gates, touched surfaces, and limits

- **Gate exercised:** the three proposed quote/claim pairs passed the requested Python anchor checks. The scoped search for rule-topic terms in the debugging/debug-variable passages returned no matches.
- **Not exercised:** no frozen C1/C2 counters, build, tests, or runtime check. These are source findings, not a counted C1 result; no C1 target claim is made here.
- **Touched surfaces:** this report and fetch receipts `WikiDebugging-1.bin` through `WikiDebugging-5.bin` under `.ufo/waves/round-24/fetch/w1/` only. No product code, corpus note, `SOURCES.md`, or README was edited. No tools were installed.
- **Out of scope:** no host `hyprctl` calls, live log inspection, compositor/service/config/package changes, or source edits.
- **Verdict:** the pinned wiki documents generic debug logging and rule-match semantics, but these opened debugging passages do not document a rule-to-effect attribution trace; host behavior remains **[UNK]**.
