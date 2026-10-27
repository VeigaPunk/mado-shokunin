# CritRoutedItems — round 49 w1

Status: COMPLETE. Findings: `.ufo/waves/round-49/w1/CritRoutedItems/findings.md`.

At base `03e4ae76aff7a4be59cb69970dd553baa319695a`, routed items remain open; per-item status, command evidence, smallest honest correction, and falsification conditions are in findings.md. Strongest current counterexample to closure: round-49 w1 context repeats the `/tmp only for files under 50 MB` grant (SentScratch F4). Other newly identified gaps: F7 has no explicit owner in the C1 counter prompt; M48-10 guard specification omits `XDG_RUNTIME_DIR`/some operator paths; the round-48 `ulimit -f 2048` wording calls the cap 1 MiB, while this Bash host's measured limit is 2 MiB.

Observed: gate at base `files=22012 findings=159`, exit 1; matrix text 96 rows vs summary 98 (missing `a-entry-at-base`, `a-rev-base-direct`); receipt generator is under `round-48/tools/`, not the path its receipt names. No lane tracked files or frozen artifacts modified; only this seat's two report files created. Scratch removed. No tools installed. Checks/builds/tests were not run except the stated read-only evidence probes.