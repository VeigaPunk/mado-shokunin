# PRED-C2-r47 controls - measured output

Every row below is one receipt in this directory, produced by running the counter;
the rev is the commit in the scratch clone the run read. The quoted line is grepped
from the receipt (locators computed, not typed).

| control | receipt | rev | exit | decisive line | sha256(receipt) |
|---|---|---|---|---|---|
| POSITIVE | `ctl-pos.txt` | `f0c21752fcab` | 0 | `PRED-C2-r47: admitted=1/1 verdict=TARGET_MET rev=f0c21752fcabcfe153d34a73a7ace63df47aa796` | `325c2a5c6de739d6` |
| base (entry absent) | `ctl-neg-base.txt` | `60edb66e2f1c` | 1 | `PRED-C2-r47 xdg-terminal-selection-r47.md clause=a entry_absent` | `494fe00b5149cfa0` |
| quote not in pin | `ctl-neg-quote.txt` | `4da00111193e` | 1 | `PRED-C2-r47 xdg-terminal-selection-r47.md clause=d quote_not_in_pin line=15 pin=xdgte-xdg-terminal-exec q='Populate list of config files to read, in u` | `d4b23f5420901837` |
| branch URL in a cited row | `ctl-neg-branch.txt` | `249ea41822c7` | 1 | `PRED-C2-r47 xdg-terminal-selection-r47.md clause=c id=S327 url_branch_ref:https://raw.githubusercontent.com/Vladimir-csp/xdg-terminal-exec/main/README` | `c2f80f5edef354f9` |
| held row S056 moved | `ctl-neg-held.txt` | `f417f9041da0` | 1 | `PRED-C2-r47 xdg-terminal-selection-r47.md clause=h held_row_moved=S056` | `2168254826dc9343` |
| receipt absent at REV | `ctl-neg-receipt.txt` | `eda4fc5bbf3b` | 1 | `PRED-C2-r47 xdg-terminal-selection-r47.md clause=f receipt_missing=.ufo/waves/round-47/receipts/live-host.txt` | `4af39fa397fa20a9` |
| citation index, no steps | `ctl-neg-nosteps.txt` | `154e2044f684` | 1 | `PRED-C2-r47 xdg-terminal-selection-r47.md clause=e steps=0 <6` | `a7de4e04fd8532ef` |
| receipt contradicts its capture | `ctl-neg-observed.txt` | `0e1b0b42dfe1` | 1 | `PRED-C2-r47 xdg-terminal-selection-r47.md clause=f observed_mismatch=.ufo/waves/round-47/receipts/live-observed.txt` | `81ed43a87fcccecf` |
| true quote, false stated range | `ctl-neg-range.txt` | `90965701cdef` | 1 | `PRED-C2-r47 xdg-terminal-selection-r47.md clause=d quote_out_of_range line=15 pin=xdgte-xdg-terminal-exec q='Populate list of config files to read, in` | `5aba10a9a1ac4dd2` |
| pin bytes changed under the row sha | `ctl-neg-pin.txt` | `42d5fb5dc131` | 1 | `PRED-C2-r47 xdg-terminal-selection-r47.md clause=c id=S328 pin_sha_mismatch=xdgte-xdg-terminals.list` | `26531e49633e6d09` |
| setup: entry already at base | `ctl-setup-base-has-entry.txt` | `?` | 2 | `PRED-C2-r47 SETUP precondition_failed entry_present_at_base corpus/knowledge/xdg-terminal-selection-r47.md` | `89e4abc7a9194d3d` |
| head source on whole-file row S333 | `x1-head-s333.txt` | `a096debf558e` | 0 | `PRED-C2-r47: admitted=1/1 verdict=TARGET_MET rev=a096debf558ebff11ef7df47fd99b97bbc8774b9` | `35fabb21c22e2ec4` |
| head source on host-bytes row S337 | `x2-head-s337.txt` | `854f56274f4a` | 1 | `PRED-C2-r47 xdg-terminal-selection-r47.md clause=c id=S337 no_url` | `81100ef0948a97bb` |
| prose mention of registry row S338 | `x3-prose-s338.txt` | `c937530c8f4e` | 0 | `PRED-C2-r47: admitted=1/1 verdict=TARGET_MET rev=c937530c8f4e03c513adead3713f8eb9072acc54` | `4afa37e938d4975f` |
| real w1 drafts (preview wiring) | `preview-real-drafts.txt` | `a9ee5c504477` | 0 | `PRED-C2-r47: admitted=1/1 verdict=TARGET_MET rev=a9ee5c504477426337950f0606f738804a61fb41` | `8b283e2b9d9d184c` |
