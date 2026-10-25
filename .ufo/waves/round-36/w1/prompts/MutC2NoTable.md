# MutC2NoTable — mutation-tester seat, mado round 36 wave 1

Lane: /home/vgpnk/Projects/shokunin/mado-shokunin
Role: mutation-tester

Write a /tmp variant of C2 that keeps the computed tip rule and the tip-line test but drops the document-table parse (rows re-derived from the spec, as round 35 did). Run it against `c2-blob-corrupt` and `c2-blob-row-deleted`. Report the two verdicts; this isolates the cost of parsing the document's own table.
