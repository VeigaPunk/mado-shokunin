# C2 extra controls - observed verdicts

Primary scorer per control: patched for paperwork mutants, pinfree for defects inside a pinned receipt, real for the real-seeded forgeries. `a/p/f` = admitted flag under real/patched/pinfree.

| control | primary | expected | observed | a/p/f | clause vector (primary) | clause that should kill |
|---|---|---|---|---|---|---|
| CL01-verified-at-line-21 | patched | kill | rejected | 0/0/0 | a:1 b:0 c:1 d:1 e:1 f:1 g:1 h:1 i:1 | b |
| CL02-source-S299-line-21 | patched | kill | rejected | 0/0/0 | a:1 b:0 c:1 d:1 e:1 f:1 g:1 h:0 i:1 | b |
| CL03-two-recheck-lines | patched | kill | rejected | 0/0/0 | a:1 b:0 c:1 d:1 e:1 f:1 g:1 h:1 i:1 | b |
| CL04-source-line-fenced | patched | kill | rejected | 0/0/0 | a:1 b:0 c:1 d:1 e:1 f:1 g:1 h:1 i:1 | b |
| CL05-recheck-invalid-month | patched | kill | rejected | 0/0/0 | a:1 b:0 c:1 d:1 e:1 f:1 g:1 h:1 i:1 | b |
| CL06-two-verified-at | patched | kill | rejected | 0/0/0 | a:1 b:0 c:1 d:1 e:1 f:1 g:1 h:1 i:1 | b |
| CL07-four-digit-id-no-row | patched | kill | rejected | 0/0/0 | a:1 b:1 c:0 d:0 e:1 f:1 g:0 h:1 i:1 | c |
| CL08-row-12-cells | patched | kill | rejected | 0/0/0 | a:1 b:1 c:0 d:1 e:1 f:1 g:1 h:1 i:1 | c |
| CL09-row-10-cells | patched | kill | rejected | 0/0/0 | a:1 b:1 c:0 d:1 e:1 f:1 g:1 h:1 i:1 | c |
| CL10-status-case | patched | kill | rejected | 0/0/0 | a:1 b:1 c:0 d:1 e:1 f:1 g:1 h:1 i:1 | c |
| CL11-usedby-case | patched | kill | rejected | 0/0/0 | a:1 b:1 c:0 d:1 e:1 f:1 g:1 h:1 i:1 | c |
| CL12-held-status-cell | patched | kill | rejected | 0/0/0 | a:1 b:1 c:0 d:1 e:1 f:1 g:1 h:1 i:1 | c |
| CL13-new-opened-empty | patched | kill | rejected | 0/0/0 | a:1 b:1 c:0 d:1 e:1 f:1 g:1 h:1 i:1 | c |
| CL14-new-recheck-unit | patched | kill | rejected | 0/0/0 | a:1 b:1 c:0 d:1 e:1 f:1 g:1 h:1 i:1 | c |
| CL15-row-indented-4 | patched | kill | rejected | 0/0/0 | a:1 b:1 c:0 d:1 e:1 f:1 g:1 h:1 i:1 | c |
| CL16-row-duplicate | patched | kill | rejected | 0/0/0 | a:1 b:1 c:0 d:1 e:1 f:1 g:1 h:1 i:1 | c |
| CL17-gate-single-quoted | patched | kill | rejected | 0/0/0 | a:1 b:1 c:1 d:0 e:0 f:1 g:0 h:1 i:1 | d |
| CL18-gate-sha-uppercase | patched | kill | rejected | 0/0/0 | a:1 b:1 c:1 d:0 e:0 f:1 g:0 h:1 i:1 | d |
| CL19-gate-trailing-text | patched | kill | rejected | 0/0/0 | a:1 b:1 c:1 d:0 e:0 f:1 g:0 h:1 i:1 | d |
| CL20-gate-absolute-path | patched | kill | rejected | 0/0/0 | a:1 b:1 c:1 d:0 e:1 f:1 g:0 h:1 i:1 | d |
| CL21-gate-path-traversal | patched | kill | rejected | 0/0/0 | a:1 b:1 c:1 d:0 e:1 f:1 g:0 h:1 i:1 | d |
| CL22-gate-quote-2-words | patched | kill | rejected | 0/0/0 | a:1 b:1 c:1 d:0 e:1 f:1 g:0 h:1 i:1 | d |
| CL23-gate-outside-section | patched | kill | ADMITTED | 1/1/1 | a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 | d |
| CL24-gate-tab-indented | patched | kill | rejected | 0/0/0 | a:1 b:1 c:1 d:0 e:0 f:1 g:0 h:1 i:1 | d |
| CL25-receipt-255-bytes | patched | kill | rejected | 0/0/0 | a:1 b:1 c:1 d:0 e:1 f:1 g:0 h:1 i:1 | d |
| CL26-gate-two-lines-same-id | patched | kill | rejected | 0/0/0 | a:1 b:1 c:1 d:0 e:0 f:1 g:0 h:1 i:1 | d |
| CL27-gate-wrong-round-path | patched | kill | rejected | 0/0/0 | a:1 b:1 c:1 d:0 e:1 f:1 g:0 h:1 i:1 | d |
| CL28-gate-no-quote-key | patched | kill | rejected | 0/0/0 | a:1 b:1 c:1 d:0 e:0 f:1 g:0 h:1 i:1 | d |
| CL29-gate-h3-section | patched | kill | rejected | 0/0/0 | a:1 b:1 c:1 d:0 e:0 f:1 g:0 h:0 i:0 | d |
| CL30-census-tilde-fence | patched | kill | rejected | 0/0/0 | a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:0 i:1 | h |
| CL31-obs-line-fenced | patched | kill | rejected | 0/0/0 | a:1 b:1 c:1 d:1 e:1 f:1 g:0 h:1 i:1 | g |
| CL32-readme-row-indented | patched | kill | rejected | 0/0/0 | a:1 b:1 c:1 d:1 e:1 f:0 g:1 h:1 i:1 | f |
| CL33-gate-section-uppercase | patched | kill | rejected | 0/0/0 | a:1 b:1 c:1 d:0 e:0 f:1 g:0 h:0 i:0 | d |
| CL34-readme-duplicate-row | patched | kill | rejected | 0/0/0 | a:1 b:1 c:1 d:1 e:1 f:0 g:1 h:1 i:1 | f |
| CL35-admit-no-as | patched | kill | rejected | 0/0/0 | a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:0 | i |
| CL36-admit-path-not-md | patched | kill | rejected | 0/0/0 | a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:0 | i |
| CL37-refuse-reason-short | patched | kill | rejected | 0/0/0 | a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:0 | i |
| CL38-refuse-3-distinct | patched | kill | rejected | 0/0/0 | a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:0 | i |
| CL39-refuse-foreign-path | patched | admit | ADMITTED | 1/1/1 | a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 | i |
| CL40-admit-foreign-path | patched | admit | ADMITTED | 1/1/1 | a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 | i |
| CL41-refuse-tab-separated | patched | kill | rejected | 0/0/0 | a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:0 | i |
| CL42-gate-section-missing | patched | kill | rejected | 0/0/0 | a:1 b:1 c:1 d:0 e:0 f:1 g:0 h:0 i:0 | d |
| CL43-census-extra-mapped-client | pinfree | kill | rejected | 0/0/0 | a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:0 i:1 | h |
| CL44-census-json-object-not-list | pinfree | kill | rejected | 0/0/0 | a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:0 i:1 | h |
| CL45-census-hidden-gkeep-client | pinfree | kill | rejected | 0/0/0 | a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:0 i:1 | h |
| CL46-census-two-float-rules | pinfree | kill | rejected | 0/0/0 | a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:0 i:1 | h |
| CL47-census-float-off | pinfree | kill | rejected | 0/0/0 | a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:0 i:1 | h |
| CL48-census-fourth-own-work | patched | kill | rejected | 0/0/0 | a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:0 i:1 | h |
| CL49-census-second-app-id | pinfree | kill | rejected | 0/0/0 | a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:0 i:1 | h |
| CL50-census-second-default-size | pinfree | kill | rejected | 0/0/0 | a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:0 i:1 | h |
| CL51-census-json-nondict | pinfree | kill | rejected | 0/0/0 | a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:0 i:1 | h |
| CL52-census-two-center-rules | pinfree | kill | rejected | 0/0/0 | a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:0 i:1 | h |
| CL63-gate-outside-section-differing | patched | kill | rejected | 0/0/0 | a:1 b:1 c:1 d:0 e:1 f:1 g:1 h:1 i:1 | d |
| CL64-entry-absent-at-rev | patched | kill | rejected | 0/0/0 | a:0 b:0 c:0 d:0 e:0 f:1 g:0 h:0 i:1 | a |
| CL53-loc-component-unrelated | patched | kill | rejected | 0/0/0 | a:1 b:1 c:1 d:1 e:0 f:1 g:1 h:1 i:1 | e |
| CL54-two-rows-one-location | patched | kill | rejected | 0/0/0 | a:1 b:1 c:1 d:1 e:0 f:1 g:1 h:1 i:1 | e |
| CL55-quote-truncated-at-punctuation | patched | admit | ADMITTED | 1/1/1 | a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 | d |
| CL56-locator-second-occurrence | pinfree | kill | rejected | 0/0/0 | a:1 b:1 c:1 d:1 e:1 f:1 g:0 h:1 i:1 | g |
| CL57-quote-preceded-by-digit | pinfree | kill | rejected | 0/0/0 | a:1 b:1 c:1 d:0 e:1 f:1 g:0 h:1 i:1 | d |
| CL58-quote-preceded-by-underscore | pinfree | kill | rejected | 0/0/0 | a:1 b:1 c:1 d:0 e:1 f:1 g:0 h:1 i:1 | d |
| CL59-quote-followed-by-digit | pinfree | kill | rejected | 0/0/0 | a:1 b:1 c:1 d:0 e:1 f:1 g:0 h:1 i:1 | d |
| CL60-quote-prefix-of-longer | pinfree | kill | rejected | 0/0/0 | a:1 b:1 c:1 d:0 e:1 f:1 g:0 h:1 i:1 | d |
| CL61-quote-plus-period | patched | kill | rejected | 0/0/0 | a:1 b:1 c:1 d:0 e:1 f:1 g:0 h:1 i:1 | d |
| CL62-two-digit-id-invisible | patched | admit | ADMITTED | 1/1/1 | a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 | b |
| R01-real-quote-unsupported-size-claim | real | admit | ADMITTED | 1/1/1 | a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 | g |
| R02-real-quote-reused-two-ids | real | kill | rejected | 0/0/0 | a:1 b:1 c:1 d:0 e:1 f:1 g:0 h:1 i:1 | d |
| R03-real-quote-wrong-locator | real | kill | rejected | 0/0/0 | a:1 b:1 c:1 d:1 e:1 f:1 g:0 h:1 i:1 | g |
| R04-real-quote-other-file-locator | real | kill | rejected | 0/0/0 | a:1 b:1 c:1 d:1 e:1 f:1 g:0 h:1 i:1 | g |
| R05-real-quote-exclusivity-claim | real | admit | ADMITTED | 1/1/1 | a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 | g |
| R06-real-quote-current-value-claim | real | admit | ADMITTED | 1/1/1 | a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 | g |
| R07-real-quote-staged-row-location | real | kill | rejected | 0/0/0 | a:1 b:1 c:1 d:1 e:0 f:1 g:1 h:1 i:1 | e |
| R08-held-id-invented-receipt | real | admit | ADMITTED | 1/1/1 | a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 | d |

## surprises (prediction != observation)

- **CL23-gate-outside-section** predicted kill, observed ADMITTED: HOLE (low): the outside-section scan drops any line whose TEXT equals an in-section line (`line not in in_gate`), so a byte-identical GATE line under another heading is invisible to d. Only a differing outside line is counted.
