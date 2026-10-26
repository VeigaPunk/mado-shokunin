# synthetic matrix against check-locators.py, fetch dir = fx/fetch (rec.cpp, 6 lines)

S1 FALSE-OK comment-only support: `size` at `rec.cpp:3`.  [expect OK]
S2 FALSE-OK short tokens: `a->b` at `rec.cpp:2`.  [expect NOFRAG]
S3 FALSE-OK attribution shift: `size` `x` at `rec.cpp:3`.  [expect OK]
S4 FALSE-OK wrapped + wrong: the sum is `alpha_size
` at `rec.cpp:900`.  [expect NOFRAG on this line]
S5 FALSE-OK unwrapped fragment absent: the sum is at rec.cpp:900.  [expect NOFRAG]
S6 FALSE-OK reordered quote: the sum is `beta + alpha_size` at `rec.cpp:6`.  [expect OK]
S7 negative control: the sum is `alpha_size` at `rec.cpp:900`.  [expect MISS]
S8 FALSE-OK number: the width is `int size = 999` at `rec.cpp:5`.  [expect OK]
S9 FALSE-OK wrapped correct: the sum is `alpha_size + beta`
(`rec.cpp:900`).  [expect NOFRAG on line 9]
