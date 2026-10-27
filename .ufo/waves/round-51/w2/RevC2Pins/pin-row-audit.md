# S364–S369 pin-row audit

Checked `corpus/SOURCES.md` rows, entry source block + pin manifest, fetched files, and `fetch/SHA256SUMS`. Status is against pin provenance/quote integrity, not whether the entry's broader interpretations are true.

| Row | Registry anchor / locator | Entry quote → fetched line | Revision / digest / manifest | Result |
|---|---|---|---|---|
| S364 | SOURCES.md:313; `Hyprland-KeybindManager.cpp:41-113,602,782,785,798-823` | `m_dispatchers.find(k->mouse ? "mouse" : k->handler);` at fetched line 785; quote appears verbatim in entry line 14. | URL and anchor use commit `efb50993780079460b0cbed1363e2166a2de1d9f`; pin listed manifest line 32; SHA256SUMS line 6 and recomputed SHA-256 agree: `8d8f35fc84c4a2f8de63ac2bf6f6531c651c6fa6d37b1aac7c8fc5d9342d4e40`. | PASS |
| S365 | SOURCES.md:314; `Hyprland-legacy-DispatcherTranslator.cpp:30-35,797-867` | `Bad dispatcher` at fetched line 32; entry line 15 quotes it. | URL/anchor commit `efb50993780079460b0cbed1363e2166a2de1d9f`; manifest line 34; SHA256SUMS line 11/recomputed agree: `7248cbb89f898c783c50c89d068df9821a6b38aeb6abeb6064e92c1610fbe771`. | PASS |
| S366 | SOURCES.md:315; `Hyprland-HyprCtl.cpp:1126-1158,2036` | `m_dispatchers.find(DISPATCHSTR)` at fetched line 1149; entry line 16 quotes it. | URL/anchor commit `efb50993780079460b0cbed1363e2166a2de1d9f`; manifest line 36; SHA256SUMS line 5/recomputed agree: `798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa`. | PASS |
| S367 | SOURCES.md:316; `Hyprland-ConfigActions.cpp:1664-1682` | `Cannot set submap` at fetched line 1681; entry line 17 quotes it. | URL/anchor commit `efb50993780079460b0cbed1363e2166a2de1d9f`; manifest line 37; SHA256SUMS line 1/recomputed agree: `a83abeb57175e65908d8d67ddc9802310134e5a4752fa3764f980401b48a7637`. | PASS |
| S368 | SOURCES.md:317; `Hyprland-legacy-ConfigManager.cpp:1580-1601` | `m_dispatchers.find(HANDLER)` at fetched line 1594; entry line 18 quotes it. | URL/anchor commit `efb50993780079460b0cbed1363e2166a2de1d9f`; manifest line 39; SHA256SUMS line 10/recomputed agree: `9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b`. | PASS |
| S369 | SOURCES.md:318; `Hyprland-SharedDefs.hpp:53` | `passEvent = false` at fetched line 53; entry line 19 quotes it. | URL/anchor commit `efb50993780079460b0cbed1363e2166a2de1d9f`; manifest line 40; SHA256SUMS line 8/recomputed agree: `0b40cc83f827587f3a94260ca89d4464150dc2b45de2b9331e3d1876cafe0087`. | PASS |

All six row URLs point to raw GitHub files at the same immutable commit. The entry's manifest binds each quoted pin to its matching row; the checksum manifest binds those pin bytes. Registry rows state `mined`, opened `2026-10-27`, and used-by the C2 entry (SOURCES.md:313-318). No pin-row integrity failure observed.
