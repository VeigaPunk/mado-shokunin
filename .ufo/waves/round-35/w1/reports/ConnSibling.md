# ConnSibling — sibling-overlap scan, mado round 35 wave 1

**Scope (frozen theme):** the idle-lock control surface (hypridle/hyprlock where
present, per `PROVINCE.md:9`), the bar's custom indicators (`~/.config/waybar/`),
and the desktop toggle menu (`~/.config/walker/` / launcher plane).

**Method:** read all 20 sibling `*-shokunin/PROVINCE.md` files under
`/home/vgpnk/Projects/shokunin/` end to end, then a cross-check grep over every
sibling province for `idle|hypridle|hyprlock|waybar|walker|swayosd|menu|
indicator|toggle|lock|bar|wofi|rofi|fuzzel|desktop|hypr|compositor|mado`. Every
grep hit is classified below; none is a competing claim. Read-only: no sibling
file was written.

## Verdict per sibling

| Sibling | Claims a theme surface? | Evidence |
|---|---|---|
| kumitate | **No** | Orchestration/tooling: ufo-fsd scripts + runtime, OMP task/hub, MCP revisions, agent isolation. No desktop surface. (`PROVINCE.md:3-27`) |
| kake | **No** | Web properties & publishing (Pages, sitemaps, robots.txt, OG, security.txt). Contested Chrome profile lease is a kagi/tabi/kake browser matter, not desktop. (`PROVINCE.md:3-8,32-43`) |
| kama | **No** | Local model serving & endpoint health only; refuses dispatch and remote surfaces. (`PROVINCE.md:3-14,40-49`) |
| kotoba | **No** | Prompt/skill craft. Its own census classifies mado `none` — "desktop and compositor craft … no split on its scope surfaces" (`kotoba/PROVINCE.md:61`). One nuance: a mado wave report had assigned the omarchy skill-file *frontmatter* facet to kotoba with no province clause — that is SKILL.md craft, not the idle-lock/bar/menu surfaces. |
| tsukuroi | **No — confirms mado owns it** | ADJ-03 routes "Desktop rendering, bindings, menu or idle behavior needs configuration-level diagnosis" → mado (`tsukuroi/PROVINCE.md:48`); OUT-004 anchor quotes mado's owns-clause: "Mado owns the Hyprland, waybar, walker and terminal configuration plane, themes/wallpapers and screen/idle behavior" (`tsukuroi/PROVINCE.md:124,140`). Tsukuroi retains only the OS-side reading (user-manager/unit state, package, driver). |
| kaidoku | **No** | Shipped-artifact RE (REA/Ghidra). No desktop surface; grep hits are `unlock`/adb/Frida rows only. |
| mori | **No** | Fleet & host observability; refuses desktop-adjacent grounds to their owners. No idle/bar/menu rows. |
| tameshi | **No** | Verification-fixture method. Names mado's `tools/mado-verify.sh` only as a read-only primary surface for the mutation method (`tameshi/PROVINCE.md:32-35`); explicitly adjacent on "visual/UI snapshot diffing … the adjacent UI lanes" (`:46-47`). Never claims the config plane itself. |
| kagi | **No** | Secrets & vault ops. `lock` hits are the-janitor `client.lock` flock — unrelated. |
| kengaku | **No** | LLM eval; "Not owned: the model-serving plane … escalate to the integrator" — no desktop ground anywhere. |
| souji | **No** | Fleet repo hygiene; `lock` hits are worktree locks it never removes. Refuses `~/.config/**` outright as operator config (`souji/PROVINCE.md:38-39`). |
| audio | **No** | Game audio production only. |
| game-dev-2d | **No** | 2D headless fixtures; no display-config scope. |
| lore | **No** | Fictional-world records. |
| kasegi | **No** | Bounty/security research corpus. |
| game-dev-3d | **No — confirms mado owns it** | Adjacent table: "Desktop/compositor display behavior belongs to mado-shokunin" (`game-dev-3d/PROVINCE.md:75`). |
| kotodama | **No** | Linguistic-cultural worldbuilding. |
| revenger | **No** | Shipped-artifact RE. |
| chousa | **No** | Deep-research method. |
| tabi | **No** | Browser/web-interaction craft; CDP is browser surfaces, not the compositor/bar/menu. |

## Cross-domain bleed verdict

**Not a bleed.** All three surfaces sit inside mado's own declared Core:
`~/.config/hypr/`, `~/.config/waybar/`, `~/.config/walker/`, and "screen/idle
behavior (hypridle/hyprlock where present)" (`mado/PROVINCE.md:3-9`). Two
siblings (tsukuroi ADJ-03/OUT-004; game-dev-3d `:75`) explicitly delegate this
exact ground to mado; kotoba's fleet census records `none` for mado on scope
surfaces; tameshi touches only mado's gate as read-only method surface. Zero
sibling claims, zero contested rows.

## Boundary caveat to carry

If the idle-lock chain runs through a systemd **user unit** (e.g. a hypridle
service), the *unit state* (`systemctl --user`, unit files, failed states) is
tsukuroi's read surface, while the *desktop behavior and config bytes* stay
mado's — tsukuroi's own ADJ-03 splits it exactly this way ("an active unit does
not prove the UI works"). Read of unit health is adjacency, not contest; any
remediation is operator-owned in both lanes. All mado-side work remains
read-only probe/measure/recommend per `mado/PROVINCE.md:11-16`.
