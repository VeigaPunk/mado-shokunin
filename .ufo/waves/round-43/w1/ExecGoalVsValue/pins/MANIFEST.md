# pins — ExecGoalVsValue, mado round 43 w1

Every quote used in `../finding.md` lives in one of these files and is checked verbatim at the claimed
line by `../verify-quotes.py` (ledger: `quotes.tsv`; receipt: `../verify-quotes.txt`,
`quotes=69 fails=0`, every file in `pins/` covered by `SHA256SUMS` (22 entries)). Line numbers in `quotes.tsv` are physical
lines of the pin; the three own-work host excerpts carry the original host line number as a prefix.

Hyprland files are raw bytes of `https://raw.githubusercontent.com/hyprwm/Hyprland/<commit>/<path>`
at tag `v0.56.2` = commit `efb50993780079460b0cbed1363e2166a2de1d9f` (verified via
`api.github.com/repos/hyprwm/Hyprland/git/ref/tags/v0.56.2`). Hyprutils file is
`https://raw.githubusercontent.com/hyprwm/hyprutils/v0.14.2/include/hyprutils/animation/AnimatedVariable.hpp`,
tag `v0.14.2` = commit `a21e87b878e72ee5dfd375899e8b2ad0d0c4c0e1` (ref API); the host reports
`Hyprutils: built against 0.14.2, system has 0.14.2` (`host-getoption.txt`), and Hyprland's
`CMakeLists.txt:150` requires `>= 0.14.0` (not pinned here; the version comes from the host receipt).

| pin | origin | bytes | sha256 | ledger id |
|---|---|---|---|---|
| `hyprctl.cpp` | Hyprland `src/debug/HyprCtl.cpp` | 97582 | `798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa` | **S296** (reuse; byte-identical to `fetch/Hyprland-HyprCtl.cpp`) |
| `geometric-movable-animated.cpp` | `src/desktop/view/types/GeometricMovableAnimated.cpp` | 1576 | `649f1a8d01d28e20e23380db65c5aeb35846d7ef48c8aada9b84ff0e4a1a207d` | **S295** (reuse) |
| `floating-algorithm.cpp` | `src/layout/algorithm/floating/default/DefaultFloatingAlgorithm.cpp` | 10359 | `f05f256150c8dcf5041ba71eaa9b8ba0ec16b94d231bff7a213d18fc23632e91` | **S292** (reuse) |
| `target.cpp` | `src/layout/target/Target.cpp` | 3064 | `49323833c6bc327656e6d02245ebbccf7643fc94f4fbee3cebbae035bbd4ca06` | **S293** (reuse) |
| `window-target.cpp` | `src/layout/target/WindowTarget.cpp` | 16614 | `8bcaf37000cf55e1d2084bf732f0589b4ab49d36c778d8d4efa98949dd14734d` | **S294** (reuse) |
| `window.cpp` | `src/desktop/view/Window.cpp` | 124226 | `d735d454cc4b7983f19626514d310669047da46780c509ffae68ccf072211ded` | new — proposal **S301** |
| `window.hpp` | `src/desktop/view/Window.hpp` | 23988 | `1f60b8ff0bc6b5a48af5c03cb2cac1108db677efc70b4424b56ef6f1f2d1cc81` | new — proposal **S311** |
| `geometric-movable-animated.hpp` | `src/desktop/view/types/GeometricMovableAnimated.hpp` | 1097 | `8dcf6e86a78eb0e4bd2c71a289329d8ffef7ca400cf6971dd4e744ba38499394` | new — proposal **S303** |
| `window-animation-controller.cpp` | `src/desktop/view/animationControllers/WindowAnimationController.cpp` | 6589 | `9a8c3c2961a1a55fca7b8783e1c3b808b424291e832bf4cdf88ed7a73e5bab08` | new — proposal **S302** |
| `animation-manager.cpp` | `src/animation/AnimationManager.cpp` | 16288 | `8c37cd0d1e972e8789468fdf063456a6a40ed17d482b898b0639a6d2a1fa7985` | new — proposal **S306** |
| `animation-manager.hpp` | `src/animation/AnimationManager.hpp` | 2638 | `e7834aef3b0f3259a109e5407c27bd31d5ad8ed05b698e4726e5972bacd479fa` | new — proposal **S306** |
| `animation-tree.cpp` | `src/config/shared/animation/AnimationTree.cpp` | 3483 | `313ed20167618dfe163fceee8753e9a49d8ef356bc3f580963e07039839e7bae` | new — proposal **S307** |
| `helpers-animated-variable.hpp` | `src/helpers/AnimatedVariable.hpp` | 2028 | `6c8db9a2a55eac3f1463918b39a2a36bd641c8ea1c33e74414d64fe891aaea3a` | new — proposal **S308** |
| `algorithm.cpp` | `src/layout/algorithm/Algorithm.cpp` | 8422 | `fe4a129a6402ba86a65d2f9750f96b509c420bd0295124b636f4ee5facdd3428` | new — proposal **S305** |
| `renderer.cpp` | `src/render/Renderer.cpp` | 143211 | `9af8a74e7dc42ba3c5532303b9bb4ee7c350d4cef2f2c8984e41f2a01b3bdd22` | new — proposal **S304** |
| `hyprutils-animated-variable-0.14.2.hpp` | hyprutils `include/hyprutils/animation/AnimatedVariable.hpp` @ v0.14.2 | 10677 | `960660cf41fb4ecf56bfa269d316c06b499e0d915fd6c8faeb7782ca324e5bcb` | new — proposal **S300** |
| `host-clients-r43.json` | own-work, `hyprctl clients -j` reduced, 2026-10-26 | 711 | `21db902e1f1234b9f52411cf7885097a18d67b00b9dd0110f9bbd2b36fb442ad` | **S298** (reuse; identical to `fetch/`) |
| `host-getoption.txt` | own-work, `hyprctl version` + three `getoption -j`, 2026-10-26 | 900 | `c206e8539637e766c5cc9827a5a4afec283b398afe759fad985ef564c5b61eee` | new — proposal **S309** |
| `omarchy-looknfeel-80-96.txt` | own-work, read-only copy of `~/.local/share/omarchy/default/hypr/looknfeel.conf:80-96` | 840 | `a5d2c473282ab01a92bef5773b56b1910107bb0b8e2ab4eabd0fa393a4ed860d` | new — proposal **S310** |
| `host-config-chain.txt` | own-work, `~/.config/hypr/hyprland.conf:1-32`, `~/.config/hypr/looknfeel.conf:24-28`, and a no-output theme/toggle grep, 2026-10-26 | 4936 | `0243d71787db7aa68dd9956b6ef7273168091e51d55fafcf847754a93f85a365` | new — proposal **S310** |

Sizes for the two pinned Hyprland files equal the byte counts in the round-43 fetch receipt
(`receipts/fetch-sha256.txt`), and their sha256 match it exactly, so `S292`–`S296` are the same bytes
the wave already trusts. Ids above S300 are *proposals*: the wave's other seats also propose from
`S300+`, so the integrator assigns final ids (collision is expected; the anchors and hashes are what
must survive).

Not pinned / not quoted: `src/config/ConfigManager.cpp` (a 2597-byte dispatcher, no animation values),
`src/helpers/MiscFunctions.hpp`, `src/SharedDefs.hpp`, `src/defines.hpp`, `src/macros.hpp`
(opened while looking for the definition of the `sc<int>` helper; not found there). The `sc`
definition is therefore **unverified** — see the risk section of `../finding.md`.
