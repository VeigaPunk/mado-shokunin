# Criterion 107 mutant receipts

## widen-past-eof
rc=1
ANCHOR_COVER: row=K03 sid=S383 line=33 name=ConfigWatcher.cpp locators=33-34,46,54-56,60,67,69,105-200 eof=checked verdict=MISS reason=past-eof
ANCHOR_COVER: row=K04 sid=S383 line=34 name=ConfigWatcher.cpp locators=33-34,46,54-56,60,67,69,105-200 eof=checked verdict=MISS reason=past-eof
ANCHOR_COVER: row=K05 sid=S383 line=46 name=ConfigWatcher.cpp locators=33-34,46,54-56,60,67,69,105-200 eof=checked verdict=MISS reason=past-eof
ANCHOR_COVER: row=K06 sid=S383 line=54 name=ConfigWatcher.cpp locators=33-34,46,54-56,60,67,69,105-200 eof=checked verdict=MISS reason=past-eof
ANCHOR_COVER: row=K07 sid=S383 line=55 name=ConfigWatcher.cpp locators=33-34,46,54-56,60,67,69,105-200 eof=checked verdict=MISS reason=past-eof
ANCHOR_COVER: row=K08 sid=S383 line=56 name=ConfigWatcher.cpp locators=33-34,46,54-56,60,67,69,105-200 eof=checked verdict=MISS reason=past-eof
ANCHOR_COVER: row=K09 sid=S383 line=60 name=ConfigWatcher.cpp locators=33-34,46,54-56,60,67,69,105-200 eof=checked verdict=MISS reason=past-eof
ANCHOR_COVER: row=K10 sid=S383 line=67 name=ConfigWatcher.cpp locators=33-34,46,54-56,60,67,69,105-200 eof=checked verdict=MISS reason=past-eof
ANCHOR_COVER: row=K11 sid=S383 line=69 name=ConfigWatcher.cpp locators=33-34,46,54-56,60,67,69,105-200 eof=checked verdict=MISS reason=past-eof
ANCHOR_COVER: row=K12 sid=S383 line=105 name=ConfigWatcher.cpp locators=33-34,46,54-56,60,67,69,105-200 eof=checked verdict=MISS reason=past-eof
ANCHOR_COVER: row=E02 sid=S383 line=60 name=ConfigWatcher.cpp locators=33-34,46,54-56,60,67,69,105-200 eof=checked verdict=MISS reason=past-eof
CHECK107: rows=39 covered=28 miss=11 verdict=FAIL

## narrow-below-K-row
rc=1
ANCHOR_COVER: row=K12 sid=S383 line=105 name=ConfigWatcher.cpp locators=33-34,46,54-56,60,67,69,104 eof=checked verdict=MISS reason=no-cover
CHECK107: rows=39 covered=38 miss=1 verdict=FAIL

## drop-name
rc=1
ANCHOR_COVER: row=K03 sid=S383 line=33 name=ConfigWatcher.cpp locators=none eof=checked verdict=MISS reason=no-cover
ANCHOR_COVER: row=K04 sid=S383 line=34 name=ConfigWatcher.cpp locators=none eof=checked verdict=MISS reason=no-cover
ANCHOR_COVER: row=K05 sid=S383 line=46 name=ConfigWatcher.cpp locators=none eof=checked verdict=MISS reason=no-cover
ANCHOR_COVER: row=K06 sid=S383 line=54 name=ConfigWatcher.cpp locators=none eof=checked verdict=MISS reason=no-cover
ANCHOR_COVER: row=K07 sid=S383 line=55 name=ConfigWatcher.cpp locators=none eof=checked verdict=MISS reason=no-cover
ANCHOR_COVER: row=K08 sid=S383 line=56 name=ConfigWatcher.cpp locators=none eof=checked verdict=MISS reason=no-cover
ANCHOR_COVER: row=K09 sid=S383 line=60 name=ConfigWatcher.cpp locators=none eof=checked verdict=MISS reason=no-cover
ANCHOR_COVER: row=K10 sid=S383 line=67 name=ConfigWatcher.cpp locators=none eof=checked verdict=MISS reason=no-cover
ANCHOR_COVER: row=K11 sid=S383 line=69 name=ConfigWatcher.cpp locators=none eof=checked verdict=MISS reason=no-cover
ANCHOR_COVER: row=K12 sid=S383 line=105 name=ConfigWatcher.cpp locators=none eof=checked verdict=MISS reason=no-cover
ANCHOR_COVER: row=E02 sid=S383 line=60 name=ConfigWatcher.cpp locators=none eof=checked verdict=MISS reason=no-cover
CHECK107: rows=39 covered=28 miss=11 verdict=FAIL

## reversed-range
rc=1
ANCHOR_COVER: row=K12 sid=S383 line=105 name=ConfigWatcher.cpp locators=33-34,46,54-56,60,67,69,105-104 eof=checked verdict=MISS reason=no-cover
CHECK107: rows=39 covered=38 miss=1 verdict=FAIL

## identifier-prefixed-name
rc=1
ANCHOR_COVER: row=K03 sid=S383 line=33 name=ConfigWatcher.cpp locators=none eof=checked verdict=MISS reason=no-cover
ANCHOR_COVER: row=K04 sid=S383 line=34 name=ConfigWatcher.cpp locators=none eof=checked verdict=MISS reason=no-cover
ANCHOR_COVER: row=K05 sid=S383 line=46 name=ConfigWatcher.cpp locators=none eof=checked verdict=MISS reason=no-cover
ANCHOR_COVER: row=K06 sid=S383 line=54 name=ConfigWatcher.cpp locators=none eof=checked verdict=MISS reason=no-cover
ANCHOR_COVER: row=K07 sid=S383 line=55 name=ConfigWatcher.cpp locators=none eof=checked verdict=MISS reason=no-cover
ANCHOR_COVER: row=K08 sid=S383 line=56 name=ConfigWatcher.cpp locators=none eof=checked verdict=MISS reason=no-cover
ANCHOR_COVER: row=K09 sid=S383 line=60 name=ConfigWatcher.cpp locators=none eof=checked verdict=MISS reason=no-cover
ANCHOR_COVER: row=K10 sid=S383 line=67 name=ConfigWatcher.cpp locators=none eof=checked verdict=MISS reason=no-cover
ANCHOR_COVER: row=K11 sid=S383 line=69 name=ConfigWatcher.cpp locators=none eof=checked verdict=MISS reason=no-cover
ANCHOR_COVER: row=K12 sid=S383 line=105 name=ConfigWatcher.cpp locators=none eof=checked verdict=MISS reason=no-cover
ANCHOR_COVER: row=E02 sid=S383 line=60 name=ConfigWatcher.cpp locators=none eof=checked verdict=MISS reason=no-cover
CHECK107: rows=39 covered=28 miss=11 verdict=FAIL

## malformed-pin
rc=1
ANCHOR_COVER: row=K01 sid=S384 line=492 name=- locators=none eof=unchecked verdict=MISS reason=malformed-pin
CHECK107: rows=39 covered=38 miss=1 verdict=FAIL

## duplicate-id
rc=1
ANCHOR_COVER: row=K03 sid=S383 line=33 name=- locators=none eof=unchecked verdict=MISS reason=dup-id
ANCHOR_COVER: row=K04 sid=S383 line=34 name=- locators=none eof=unchecked verdict=MISS reason=dup-id
ANCHOR_COVER: row=K05 sid=S383 line=46 name=- locators=none eof=unchecked verdict=MISS reason=dup-id
ANCHOR_COVER: row=K06 sid=S383 line=54 name=- locators=none eof=unchecked verdict=MISS reason=dup-id
ANCHOR_COVER: row=K07 sid=S383 line=55 name=- locators=none eof=unchecked verdict=MISS reason=dup-id
ANCHOR_COVER: row=K08 sid=S383 line=56 name=- locators=none eof=unchecked verdict=MISS reason=dup-id
ANCHOR_COVER: row=K09 sid=S383 line=60 name=- locators=none eof=unchecked verdict=MISS reason=dup-id
ANCHOR_COVER: row=K10 sid=S383 line=67 name=- locators=none eof=unchecked verdict=MISS reason=dup-id
ANCHOR_COVER: row=K11 sid=S383 line=69 name=- locators=none eof=unchecked verdict=MISS reason=dup-id
ANCHOR_COVER: row=K12 sid=S383 line=105 name=- locators=none eof=unchecked verdict=MISS reason=dup-id
ANCHOR_COVER: row=E02 sid=S383 line=60 name=- locators=none eof=unchecked verdict=MISS reason=dup-id
CHECK107: rows=39 covered=28 miss=11 verdict=FAIL
