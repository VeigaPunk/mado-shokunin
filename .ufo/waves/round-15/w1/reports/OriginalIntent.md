# Original U6 intent — bounded input-debugging layer route

## Reconstructed contract

U6 was pre-registered as the **kernel-input → Wayland debugging ladder**, complementary to the existing desktop/compositor configuration evidence—not a claim that this host's input works. The R12 ART dossier calls the gap an *inference* and describes the learning goal as identifying what each probe observes while keeping upstream documentation separate from host facts (`.ufo/waves/kaika-w1/mado-art.md:3,12,24`). Its candidate matrix says `wayland-info` enumerates globals; libinput inventory/default tools describe lower-layer state; `debug-events` observes input events; and `libinput list-devices` reports libinput defaults, not desktop-applied settings (`mado-art.md:99-105`).

The defensible conceptual ladder is: **kernel/device visibility → libinput device/default layer → compositor-visible devices/keymaps → Wayland compositor dispatch to a client**. The layer labels explain where a symptom could be localized; they do not prove an event traversed the chain. `wayland-info` is an advertised-global probe (U4), not proof of input delivery. The R12 scout specifically records `hyprctl devices` as available and limited to compositor-visible devices/keymaps; it does not establish kernel inventory, libinput defaults, or event-level diagnosis (`.ufo/evidence/round-12/l2-scout.md:3,12,17`). The R12 lesson likewise rejects inferring compositor-applied settings from `libinput list-devices` (`corpus/lessons/round-12.md:37`).

## R14 plan and scope boundary

R14 explicitly left kernel input unclaimed (`.ufo/waves/round-14/w1/ScribeClaims.md:24-27`) and kept the input debugging ladder open (`ScribeFrontier.md:106-115`). Its committed next-round intent was a bounded U6 layer route from primary sources, **without raw input capture, injection, or kernel diagnosis** (`SCORECARD.md:588-593`). Therefore the R12 ART suggestions to use kernel-device listing or `debug-events` are documentation candidates, not authorization to run them. The lane's captured U6 limit is explicit: no input injection; event observation requires suitable device access/consent (`l2-scout.md:12`).

Round 15's intended admission is a sourced explanation of the layer distinctions, with the required `## Layer ladder`, `## Safe boundary`, and `## Unexercised delivery` sections; delivery remains `[UNK]` (`SCORECARD.md:598-620`). Keep actual client delivery, IME/text-input behavior, kernel/device facts, and event-level results unexercised. Do not turn protocol documentation, device/keymap visibility, or libinput defaults into successful-delivery evidence or a hardware diagnosis.

## Divergence and confidence

**Divergence to avoid:** the broad ART candidate matrix can be misread as an operational probe plan; R14's selected move and R15's fence narrow it to a documentation-backed layer map, not raw input observation. This is consistent with R12's own warnings about probe-layer limits.

**Confidence:** high on the intended bounds and non-claims (explicit in R14/R15); medium on the exact tier ordering, which is a synthesis of the ART sources rather than an exercised end-to-end path. Inspection was read-only; no live probe or verification run.