# Guard-proof fixture — NOT a real registry
# Purpose: prove the 0-3-space extractor catches an indented id row that a
# column-zero-only extractor would miss. S002 is indented on purpose.

| id | source | kind |
|---|---|---|
| S001 | fixture source one | docs |
  | S002 | fixture source two (INDENTED collision carrier) | docs |
| S003 | fixture source three | docs |
