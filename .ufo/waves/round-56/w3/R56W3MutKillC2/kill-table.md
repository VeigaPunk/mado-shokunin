# R56W3MutKillC2 — survivor -> fixture -> kill

Tool: `tools/mado-watchplan.py` at lane tip `0f3a54361a9824484d0801679ceb1fd8ac7c32e1`, blob sha256 `3ccf070841b3c0134a05f612a35e553364f318a9d36843455f4207df118f22b7`.

Mutants are rebuilt from the two wave-2 reports (`.ufo/waves/round-56/w2/R56W2MutC2ToolA/mutants.md`, `.../R56W2MutC2ToolB/mutants.md`) as one-line edits of a COPY of the tip tool (the lane is never touched). `claim oracle` = the frozen C2 harness' own `score()` over the 18 committed and the 8 hold-out fixtures: a mutant listed here still scores 18/18 and 8/8, i.e. the frozen predicate `MADO_R56_C2 ... verdict=TARGET_MET` accepts it. `selftest` = the tool's own `--selftest` at the tip. A **kill** is a byte or exit-status difference between the mutant's staged run and the fixture's `expected.out` / `expected.rc` in the harness' staged layout (bwrap, empty cwd, tree only).

| mutant | src | claim oracle (committed/holdout) | selftest | killer fixture(s) | killed |
|---|---|---|---|---|---|
| `AM04` | A | 18/8 | FAIL(1) | `a-k04` | yes |
| `AM06` | A | 18/8 | FAIL(1) | `a-k06` | yes |
| `AM07` | A | 18/8 | FAIL(1) | `a-k07` | yes |
| `AM100` | A | 18/8 | pass | `a-k100` | yes |
| `AM101` | A | 18/8 | pass | `a-k101` | yes |
| `AM104` | A | 18/8 | pass | — | NO |
| `AM11` | A | 18/8 | FAIL(1) | `a-k06` | yes |
| `AM12` | A | 18/8 | FAIL(1) | `a-k07` | yes |
| `AM16` | A | 18/8 | pass | `a-k16`, `a-k71`, `b-k13` | yes |
| `AM17` | A | 18/8 | pass | `a-k16`, `b-k13` | yes |
| `AM18` | A | 18/8 | FAIL(1) | `a-k18` | yes |
| `AM26` | A | 18/8 | FAIL(1) | `a-k26`, `b-k15` | yes |
| `AM27` | A | 18/8 | pass | `a-k27` | yes |
| `AM28` | A | 18/8 | pass | `a-k28` | yes |
| `AM29` | A | 18/8 | pass | `a-k29`, `b-k11` | yes |
| `AM33` | A | 18/8 | FAIL(1) | `a-k33`, `a-k76` | yes |
| `AM44` | A | 18/8 | pass | `a-k44`, `b-k04` | yes |
| `AM50` | A | 18/8 | pass | `a-k50` | yes |
| `AM54` | A | 18/8 | FAIL(1) | `a-k54`, `b-k06` | yes |
| `AM55` | A | 18/8 | FAIL(1) | `a-k55` | yes |
| `AM56` | A | 18/8 | pass | `a-k56`, `b-k08` | yes |
| `AM57` | A | 18/8 | FAIL(1) | `a-k55`, `a-k57`, `b-k09` | yes |
| `AM60` | A | 18/8 | FAIL(1) | `a-k60` | yes |
| `AM62` | A | 18/8 | FAIL(1) | `a-k60`, `a-k62`, `a-k98`, `b-k16` | yes |
| `AM63` | A | 18/8 | pass | `a-k63` | yes |
| `AM71` | A | 18/8 | pass | `a-k71` | yes |
| `AM73` | A | 18/8 | pass | — | NO |
| `AM76` | A | 18/8 | pass | `a-k76` | yes |
| `AM77` | A | 18/8 | pass | — | NO |
| `AM78` | A | 18/8 | pass | — | NO |
| `AM79` | A | 18/8 | pass | — | NO |
| `AM80` | A | 18/8 | pass | `a-k27` | yes |
| `AM81` | A | 18/8 | pass | — | NO |
| `AM83` | A | 18/8 | pass | — | NO |
| `AM85` | A | 18/8 | pass | — | NO |
| `AM89` | A | 18/8 | pass | `a-k50` | yes |
| `AM90` | A | 18/8 | pass | `a-k50` | yes |
| `AM93` | A | 18/8 | FAIL(1) | `a-k54`, `b-k06` | yes |
| `AM94` | A | 18/8 | pass | `a-k57`, `a-k94`, `b-k07` | yes |
| `AM96` | A | 18/8 | FAIL(1) | `a-k55`, `a-k57`, `b-k09` | yes |
| `AM97` | A | 18/8 | pass | `a-k63` | yes |
| `AM98` | A | 18/8 | pass | `a-k98` | yes |
| `AM99` | A | 18/8 | pass | — | NO |
| `Bm01` | B | 18/8 | pass | `b-k01` | yes |
| `Bm06` | B | 18/8 | pass | — | NO |
| `Bm07` | B | 18/8 | pass | `b-k02` | yes |
| `Bm08` | B | 18/8 | pass | `b-k03` | yes |
| `Bm09` | B | 18/8 | pass | `b-k20` | yes |
| `Bm101` | B | 18/8 | pass | `b-k16` | yes |
| `Bm102` | B | 18/8 | pass | — | NO |
| `Bm104` | B | 18/8 | pass | — | NO |
| `Bm105` | B | 18/8 | pass | `b-k15` | yes |
| `Bm108` | B | 18/8 | pass | — | NO |
| `Bm109` | B | 18/8 | pass | `b-k18` | yes |
| `Bm114` | B | 18/8 | pass | `b-k17` | yes |
| `Bm116` | B | 18/8 | pass | — | NO |
| `Bm14` | B | 18/8 | pass | `a-k44`, `b-k04` | yes |
| `Bm15` | B | 18/8 | pass | — | NO |
| `Bm18` | B | 18/8 | pass | `a-k50` | yes |
| `Bm19` | B | 18/8 | pass | — | NO |
| `Bm21` | B | 18/8 | pass | `a-k50` | yes |
| `Bm25` | B | 18/8 | pass | `b-k06` | yes |
| `Bm30` | B | 18/8 | pass | `a-k56`, `b-k08` | yes |
| `Bm31` | B | 18/8 | pass | `a-k56`, `a-k57`, `a-k94`, `b-k07`, `b-k08` | yes |
| `Bm36` | B | 18/8 | pass | `a-k57`, `a-k94`, `b-k07` | yes |
| `Bm49` | B | 18/8 | pass | `a-k29`, `b-k11` | yes |
| `Bm51` | B | 18/8 | pass | `b-k12` | yes |
| `Bm55` | B | 18/8 | pass | `a-k16`, `b-k13` | yes |
| `Bm56` | B | 18/8 | pass | `b-k14` | yes |
| `Bm64` | B | 18/8 | pass | `b-k18` | yes |
| `Bm65` | B | 18/8 | pass | `b-k19` | yes |
| `Bm75` | B | 18/8 | pass | — | NO |
| `Bm76` | B | 18/8 | pass | — | NO |
| `Bm77` | B | 18/8 | pass | — | NO |
| `Bm82` | B | 18/8 | pass | — | NO |
| `Bm94` | B | 18/8 | pass | `b-k10` | yes |
| `Bm95` | B | 18/8 | pass | `a-k56`, `a-k57`, `a-k94`, `b-k07`, `b-k08` | yes |
| `Bm97` | B | 18/8 | pass | — | NO |

## fixtures delivered

| fixture | aliases | proposed target(s) | kills | frozen-harness score (pristine) |
|---|---|---|---|---|
| `a-k04` | — | `M04` | `AM04` | 1/1 |
| `a-k06` | `a-k11` | `M06`, `M11` | `AM06`, `AM11` | 1/1 |
| `a-k07` | `a-k12` | `M07`, `M12` | `AM07`, `AM12` | 1/1 |
| `a-k100` | — | `M100` | `AM100` | 1/1 |
| `a-k101` | — | `M101` | `AM101` | 1/1 |
| `a-k104` | — | `M104` | — | 1/1 |
| `a-k16` | `a-k17` | `M16`, `M17` | `AM16`, `AM17`, `Bm55` | 1/1 |
| `a-k18` | `a-k73` | `M18`, `M73` | `AM18` | 1/1 |
| `a-k26` | — | `M26` | `AM26` | 1/1 |
| `a-k27` | — | `M27` | `AM27`, `AM80` | 1/1 |
| `a-k28` | — | `M28` | `AM28` | 1/1 |
| `a-k29` | — | `M29` | `AM29`, `Bm49` | 1/1 |
| `a-k33` | — | `M33` | `AM33` | 1/1 |
| `a-k44` | — | `M44` | `AM44`, `Bm14` | 1/1 |
| `a-k50` | `a-k89`, `a-k90`, `b-k05` | `M50`, `M89`, `M90`, `m18`, `m21` | `AM50`, `AM89`, `AM90`, `Bm18`, `Bm21` | 1/1 |
| `a-k54` | `a-k93` | `M54`, `M93` | `AM54`, `AM93` | 1/1 |
| `a-k55` | — | `M55` | `AM55`, `AM57`, `AM96` | 1/1 |
| `a-k56` | — | `M56` | `AM56`, `Bm30`, `Bm31`, `Bm95` | 1/1 |
| `a-k57` | — | `M57` | `AM57`, `AM94`, `AM96`, `Bm31`, `Bm36`, `Bm95` | 1/1 |
| `a-k60` | — | `M60` | `AM60`, `AM62` | 1/1 |
| `a-k62` | `a-k99` | `M62`, `M99` | `AM62` | 1/1 |
| `a-k63` | `a-k97` | `M63`, `M97` | `AM63`, `AM97` | 1/1 |
| `a-k71` | — | `M71` | `AM16`, `AM71` | 1/1 |
| `a-k76` | — | `M76` | `AM33`, `AM76` | 1/1 |
| `a-k77` | — | `M77` | — | 1/1 |
| `a-k78` | — | `M78` | — | 1/1 |
| `a-k79` | — | `M79` | — | 1/1 |
| `a-k80` | — | `M80` | — | 1/1 |
| `a-k81` | — | `M81` | — | 1/1 |
| `a-k83` | — | `M83` | — | 1/1 |
| `a-k85` | — | `M85` | — | 1/1 |
| `a-k94` | `a-k96` | `M94`, `M96` | `AM94`, `Bm31`, `Bm36`, `Bm95` | 1/1 |
| `a-k98` | — | `M98` | `AM62`, `AM98` | 1/1 |
| `b-k01` | — | `m01` | `Bm01` | 1/1 |
| `b-k02` | — | `m07` | `Bm07` | 1/1 |
| `b-k03` | — | `m08` | `Bm08` | 1/1 |
| `b-k04` | — | `m14` | `AM44`, `Bm14` | 1/1 |
| `b-k06` | — | `m25` | `AM54`, `AM93`, `Bm25` | 1/1 |
| `b-k07` | — | `m31`, `m36`, `m95` | `AM94`, `Bm31`, `Bm36`, `Bm95` | 1/1 |
| `b-k08` | — | `m30` | `AM56`, `Bm30`, `Bm31`, `Bm95` | 1/1 |
| `b-k09` | — | `m96` | `AM57`, `AM96` | 1/1 |
| `b-k10` | — | `m94` | `Bm94` | 1/1 |
| `b-k11` | — | `m49` | `AM29`, `Bm49` | 1/1 |
| `b-k12` | — | `m51` | `Bm51` | 1/1 |
| `b-k13` | — | `m55` | `AM16`, `AM17`, `Bm55` | 1/1 |
| `b-k14` | — | `m56` | `Bm56` | 1/1 |
| `b-k15` | — | `m105` | `AM26`, `Bm105` | 1/1 |
| `b-k16` | — | `m101` | `AM62`, `Bm101` | 1/1 |
| `b-k17` | — | `m114` | `Bm114` | 1/1 |
| `b-k18` | — | `m109`, `m64` | `Bm109`, `Bm64` | 1/1 |
| `b-k19` | — | `m65` | `Bm65` | 1/1 |
| `b-k20` | — | `m09` | `Bm09` | 1/1 |

## claim survivors with no delivered killer fixture

- `AM104` (A, claim oracle 18/8, selftest pass)
- `AM73` (A, claim oracle 18/8, selftest pass)
- `AM77` (A, claim oracle 18/8, selftest pass)
- `AM78` (A, claim oracle 18/8, selftest pass)
- `AM79` (A, claim oracle 18/8, selftest pass)
- `AM81` (A, claim oracle 18/8, selftest pass)
- `AM83` (A, claim oracle 18/8, selftest pass)
- `AM85` (A, claim oracle 18/8, selftest pass)
- `AM99` (A, claim oracle 18/8, selftest pass)
- `Bm06` (B, claim oracle 18/8, selftest pass)
- `Bm102` (B, claim oracle 18/8, selftest pass)
- `Bm104` (B, claim oracle 18/8, selftest pass)
- `Bm108` (B, claim oracle 18/8, selftest pass)
- `Bm116` (B, claim oracle 18/8, selftest pass)
- `Bm15` (B, claim oracle 18/8, selftest pass)
- `Bm19` (B, claim oracle 18/8, selftest pass)
- `Bm75` (B, claim oracle 18/8, selftest pass)
- `Bm76` (B, claim oracle 18/8, selftest pass)
- `Bm77` (B, claim oracle 18/8, selftest pass)
- `Bm82` (B, claim oracle 18/8, selftest pass)
- `Bm97` (B, claim oracle 18/8, selftest pass)

