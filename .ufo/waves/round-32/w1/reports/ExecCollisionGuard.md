# ExecCollisionGuard — round-32 w1 · id-collision guard (scratch)

Scope: operator item-10 guard for the pending append of
`/home/vgpnk/Projects/shokuknow/merge/mado/SOURCES.append.md` into
`corpus/SOURCES.md`. Ran BEFORE any append. Working dir for all artifacts:
`.ufo/waves/round-32/assimilation/`. Nothing written into the lane registry or
into `/home/vgpnk/Projects/shokuknow/merge/mado/`.

## Verdict

**COLLISIONS: 0 — append is green to proceed.** No renumber map required.

- Registry ids (`reg-ids.txt`): 185 ids, S001–S185, contiguous, no gaps, no duplicates.
- Staged ids (`staged-ids.txt`): 132 ids, S186–S317, contiguous, no gaps, no duplicates.
- Intersection (`collisions.txt`): empty. Staged range starts exactly where the
  registry range ends +1 (S186 vs registry max S185).

## (1) Real check — commands run

Extractor (spacing-tolerant, census-compatible — accepts 0–3 leading spaces):

```
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' <file> | grep -oE 'S[0-9]+' | sort
```

```
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort > assimilation/reg-ids.txt
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' /home/vgpnk/Projects/shokuknow/merge/mado/SOURCES.append.md | grep -oE 'S[0-9]+' | sort > assimilation/staged-ids.txt
comm -12 assimilation/reg-ids.txt assimilation/staged-ids.txt > assimilation/collisions.txt
```

Observed:

```
185 reg-ids.txt
132 staged-ids.txt
  0 collisions.txt
```

Collision count: **0**.

Contiguity/dup sanity (run after extraction, same files): registry sort -u
= 185 ids, first 1 last 185, no gaps; staged sort -u = 132 ids, first 186 last
317, no gaps; `uniq -d` empty on both.

## (2) Guard proof — scratch fixture, proven able to fail

Fixture `guard-proof-registry-fixture.md` carries an **indented** row
(`  | S002 | ...` — two leading spaces) whose id the staged fixture
(`guard-proof-staged-fixture.md`) also contains at column zero.

Same pipeline, two extractor variants:

| extractor | pattern | reg ids seen | collisions file |
|---|---|---|---|
| tolerant (0–3 spaces) | `^ {0,3}\|[[:space:]]*S[0-9]{3,}` | S001 S002 S003 | `guard-proof-collisions-tolerant.txt` = `S002` (NON-EMPTY) |
| column-zero only | `^\|[[:space:]]*S[0-9]{3,}` | S001 S003 (S002 missed) | `guard-proof-collisions-col0.txt` = 0 bytes (EMPTY) |

Result: the naive column-zero pattern produces a FALSE-GREEN on a real
indented collision; the 0–3-space pattern catches it. Guard proven able to
fail. Fixture and both outputs committed alongside this report in
`.ufo/waves/round-32/assimilation/`:

- `guard-proof-registry-fixture.md`
- `guard-proof-staged-fixture.md`
- `guard-proof-reg-ids-tolerant.txt`
- `guard-proof-staged-ids-tolerant.txt`
- `guard-proof-collisions-tolerant.txt` (contains `S002`)
- `guard-proof-reg-ids-col0.txt` (S001, S003 — indented S002 absent)
- `guard-proof-collisions-col0.txt` (empty)

## (3) Renumber map

Not applicable — `collisions.txt` is empty. No staged id claims an existing
registry id; no renumber proposed.

## Boundary note

Registry max is S185; staged opens at S186. The staged set was evidently
numbered against this registry head. If the registry gains any row before the
append lands, this check MUST be re-run — the green is only valid for the
registry state at extraction time (S001–S185).

## Full file contents

### reg-ids.txt (185 lines)
```
S001
S002
S003
S004
S005
S006
S007
S008
S009
S010
S011
S012
S013
S014
S015
S016
S017
S018
S019
S020
S021
S022
S023
S024
S025
S026
S027
S028
S029
S030
S031
S032
S033
S034
S035
S036
S037
S038
S039
S040
S041
S042
S043
S044
S045
S046
S047
S048
S049
S050
S051
S052
S053
S054
S055
S056
S057
S058
S059
S060
S061
S062
S063
S064
S065
S066
S067
S068
S069
S070
S071
S072
S073
S074
S075
S076
S077
S078
S079
S080
S081
S082
S083
S084
S085
S086
S087
S088
S089
S090
S091
S092
S093
S094
S095
S096
S097
S098
S099
S100
S101
S102
S103
S104
S105
S106
S107
S108
S109
S110
S111
S112
S113
S114
S115
S116
S117
S118
S119
S120
S121
S122
S123
S124
S125
S126
S127
S128
S129
S130
S131
S132
S133
S134
S135
S136
S137
S138
S139
S140
S141
S142
S143
S144
S145
S146
S147
S148
S149
S150
S151
S152
S153
S154
S155
S156
S157
S158
S159
S160
S161
S162
S163
S164
S165
S166
S167
S168
S169
S170
S171
S172
S173
S174
S175
S176
S177
S178
S179
S180
S181
S182
S183
S184
S185
```
### staged-ids.txt (132 lines)
```
S186
S187
S188
S189
S190
S191
S192
S193
S194
S195
S196
S197
S198
S199
S200
S201
S202
S203
S204
S205
S206
S207
S208
S209
S210
S211
S212
S213
S214
S215
S216
S217
S218
S219
S220
S221
S222
S223
S224
S225
S226
S227
S228
S229
S230
S231
S232
S233
S234
S235
S236
S237
S238
S239
S240
S241
S242
S243
S244
S245
S246
S247
S248
S249
S250
S251
S252
S253
S254
S255
S256
S257
S258
S259
S260
S261
S262
S263
S264
S265
S266
S267
S268
S269
S270
S271
S272
S273
S274
S275
S276
S277
S278
S279
S280
S281
S282
S283
S284
S285
S286
S287
S288
S289
S290
S291
S292
S293
S294
S295
S296
S297
S298
S299
S300
S301
S302
S303
S304
S305
S306
S307
S308
S309
S310
S311
S312
S313
S314
S315
S316
S317
```
### collisions.txt (0 lines — empty)
```
```
Collision count: 0
