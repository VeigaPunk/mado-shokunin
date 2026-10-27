# ConnMistakes w2 evidence — reproduced outputs (lane clone at freeze 3e6c848a)

All commands run in a scratch clone of the lane at the freeze commit
`3e6c848a0e1bbc9c7058226b86d0faefc5351c9d` (clone under /fast/scratch/hyaku/mado-r48/ConnMistakes, removed
after use). `ulimit -f 2048` was in force for every writer command except the one-time `git clone`/`git checkout`
of the lane (git-internal pack files exceed 1 MiB by nature; total clone 390 MB, under the 2 GB seat budget).

## M48-1 reproductions

```
$ git show d7527d60:.ufo/waves/round-47/l1-draft/mado-terminal.py | sha256sum
762d042c96e7e5f2c3187133b0ffe670c1d076b698b958199602cfa019aa6c08  -
$ sha256sum tools/mado-terminal.py        # at freeze 3e6c848a
b84d5c4f723049c0fd14189ffc7b6db1f71eb70fb97e0c476d20ddeca6de2222
$ grep -n S_ISFIFO tools/mado-terminal.py -> 526 (check), 529 (raise)
$ grep -c S_ISFIFO <frozen blob> -> 0 ; frozen blob has 'raise OutOfContract("HOME unset")' at :407,
  landed at :410 (identical)
$ sed -n '52,56p' .ufo/waves/round-47/registration.md   # contract sentence names neither HOME unset, FIFO, nor symlink loops
$ python3 -I w1/ScrMistakes/check96.py --repo . --frozen-rev d7527d60 --frozen <frozen> --landed tools/mado-terminal.py
ADDED-UNREGISTERED x3 / CHECK96: frozen=6 landed=9 added=3 unregistered=3 removed=0 verdict=NARROWED / rc=1   (reproduced)
$ python3 -I w1/ScrMistakes/check96.py --repo . --frozen-rev d7527d60 --frozen <frozen> --landed <frozen>
CHECK96: frozen=6 landed=6 added=0 unregistered=0 removed=0 verdict=OK / rc=0   (reproduced)
```

Round-48 landing (fix status):
```
$ grep -n 'HOME-unset' .ufo/waves/round-48/registration.md
11: ... HOME-unset follows the resolver's `set -u` exit 1/empty stdout when a default expansion needs HOME
$ sed -n '102,108p' .ufo/waves/round-48/l1-draft/mado-terminal.py
102: cache=absent|hit|stale|invalid|disabled`; HOME unset is modelled as the script (`set -u`, x:23): when any HOME-based
103: default is needed ... it exits 1 with empty stdout, and with all three set it runs normally.
105: Out of contract: -h/--help; a FIFO named like a desktop file in a later application dir when it is the candidate the
106: resolver reads (the script blocks); an empty-string argument ...
$ grep -n -i symlink .ufo/waves/round-48/l1-draft/mado-terminal.py -> only :728 comment "dangling symlink: find -L still visits it"
$ grep -c -i symlink .ufo/waves/round-48/registration.md -> 0
# the r48 out-of-contract list does NOT carry "symlink loops" (r47 landed list at tools/mado-terminal.py:86 did)
$ sed -n '715,719p' .ufo/waves/round-48/l1-draft/mado-terminal.py   # walk still prunes silently on repeated key
    key = (st.st_dev, st.st_ino)
    if key in ancestors:
        return
```

check96 instrument holes (reproduced):
```
$ python3 -I w1/ScrMistakes/check96.py --repo . --frozen-rev 579f694b --frozen tools/mado-terminal.py \
    --landed .ufo/waves/round-48/l1-draft/mado-terminal.py
LANDED-NO-LIST .ufo/waves/round-48/l1-draft/mado-terminal.py carries no 'Also out of contract' list / rc=2
# (r48 docstring says "Out of contract:", not "Also out of contract:" — the check cannot score the real r48 delta)
# verdict logic: NARROWED only if unregistered>0; REMOVED items are printed but do not fail the check
# (narrowing-by-deletion exits 0)
```

## M48-2 reproductions

```
$ sed -n '104p' /home/vgpnk/Projects/shokunin/.ufo/reports/round-47/mado.md
  - Note: the session-material gate reads `findings=128` at the tip (115 at base). ...
$ git grep -n 'findings=128' d40189c924e01dc1cbe290474eb4256d343590d4 -> rc=1 (absent)
$ git ls-tree -r --name-only d40189c9 -- .ufo/waves/round-47 | wc -l -> 1598
$ git grep -l 'findings=136' d40189c9 -- .ufo/waves/round-47 | wc -l -> 13
$ python3 -I w1/ScrMistakes/check97.py --repo . --rev d40189c9 --report <r47 report> --receipts .ufo/waves/round-47 --text --quiet-ok
MISSING findings=128 ... / CHECK97: tokens=11 missing=1 receipts=1598 verdict=UNREceiptED / rc=1   (reproduced)
$ grep SESSION_MATERIAL w1/ExecD2Receipt/receipts/session-material-d40189c9.txt
SESSION_MATERIAL: files=19969 findings=128 rev=d40189c924e01dc1cbe290474eb4256d343590d4   (the tip value 128 reproduces; receipt now committed in r48 w1)
```

## M48-3 reproductions

```
$ check98 red reproduced verbatim: seats=44 finding_seats=7 unrouted=4 (ExecC1Determinism, MutC1Counter,
  MutC2Counter, RevengerCache) and w1 seats=41 finding_seats=4 unrouted=1 (ExecAxisBase);
  green (report-98-routed.md) unrouted=0 rc=0
$ sed -n '10p' .ufo/waves/round-47/w2/ExecC1Determinism.md | grep 'blind to' ; MutC1Counter.md:17 'survived';
  MutC2Counter.md:40 'Coverage holes' ; RevengerCache.md:122 'coverage gap' ; ExecAxisBase.md:71 'blind to'  (all verified)
$ grep -c ExecC1Determinism <r47 report> corpus/lessons/round-47.md -> 0 0
$ grep -n 'MutC1Counter\|MutC2Counter\|RevengerCache\|ExecAxisBase' .ufo/waves/round-48/w1/ScrLesson/round-48.md
-> no matches (only ExecC1Determinism appears, at the M48-3 slot line 210)   [fix gap]
```

## M48-4 reproductions

```
$ sed -n '95p' corpus/knowledge/xdg-terminal-selection-r47.md ; awk 148-151 terminal-route-r17.md  (verified: bullet at 149)
$ python3 -I w1/ScrMistakes/check99.py --repo . --rev d40189c9 --citing <entry> --fetch .ufo/waves/round-47/fetch
-> 3 AMBIGUOUS + 1 UNK-HEAD-CUT (bullet_at=149) + CHECK99: locators=7 checked=4 violations=4 verdict=CUT rc=1  (reproduced)
$ python3 -I quality/check-locators.py --fetch .ufo/waves/round-43/fetch <entry>
CHECK_LOCATORS: locators=0 miss=0 rc=0     (this is the fetch dir the w1 d4 receipt used)
$ python3 -I quality/check-locators.py --fetch .ufo/waves/round-47/fetch <entry>
LOC :38 README.md:218 MISS ; :43 README.md:300-301 OK ; :47 xdg-terminal-exec-proposal.md NOFRAG ;
    :51 desktop-entry-spec.xml:636-645 MISS ; :53 OK ; :66 README.md:179-180 OK ; :93 README.md:179-180 MISS
CHECK_LOCATORS: locators=7 miss=3 rc=1     (with the entry's own pins, criterion 77's instrument DOES bite)
$ sed -n '111,123p' quality/check-locators.py   # resolve_name: only names in --fetch are checked (scope claim verified)
```

## M48-5 reproductions

```
$ sed -n '189,191p' corpus/lessons/round-47.md   (M47-7 row, captured-by none)
$ grep -n 'lessons/round-47.md#mistakes' corpus/QUALITY.md -> 468/478/488/496/504 cite M47-1..M47-6 only
$ grep -c 'M47-7' corpus/QUALITY.md -> 0
$ grep -c ulimit .ufo/waves/round-47/w1-spec.json .ufo/waves/round-48/w1-spec.json .ufo/waves/round-48/w2-spec.json
-> 0 / 0 / 49
$ python3 -I w1/ScrMistakes/check100.py --spec .ufo/waves/round-47/w1-spec.json
-> PROSE x4 / CHECK100: sources=1 enforced=0 prose=4 verdict=PROSE-ONLY rc=1   (reproduced)
$ python3 -I w1/ScrMistakes/check100.py --spec .ufo/waves/round-48/w1-spec.json -> PROSE-ONLY rc=1 (reproduced)
$ python3 -I w1/ScrMistakes/check100.py --spec .ufo/waves/round-48/w2-spec.json
-> ENFORCED x49 (ulimit -f 2048) / CHECK100: sources=1 enforced=49 prose=102 verdict=OK rc=0   (fix landed in w2 dispatch)
```

## Proposal 6 (ScrConsider)

```
$ git show 579f694b:corpus/QUALITY.md | grep -cE '^[0-9]+\. ' -> 95
$ python3 -I w1/ScrConsider/check96.py --selftest -> SELFTEST: ok cases=5
$ python3 -I w1/ScrConsider/check96.py --repo . --rev 579f694b --rounds 44-47
-> round=44/45/46/47 verdict=FAIL process_tokens=9/10/14/11 ; SUMMARY rounds=4 pass=0 fail=4 skip=0  (reproduced)
$ grep -n 'provisional' w1/ScrConsider/draft.md -> "provisional number 96; the L1 freezes the final number"
$ grep -rn 'criterion 96' w1/ScrMistakes/mistakes.md w1/ScrConsider/draft.md   (both claim 96 — collision)
```

## Misroot incident (fleet root, read-only)

```
$ cat /home/vgpnk/Projects/shokunin/.tower/quarantine/fleet-root-strays-20261026T2055/SHA256SUMS
fdb0b7a49736a50b956ef899b64a4381547a0b37a4663a3eae46f731257e16d3  tree.json
$ head -c 320 tree.json -> { "sha": "efb50993780079460b0cbed1363e2166a2de1d9f",
  "url": "https://api.github.com/repos/hyprwm/Hyprland/git/trees/efb50993..."   (Hyprland v0.56.2 trees dump)
$ git -C /home/vgpnk/Projects/shokunin status --porcelain -> empty (fleet root clean now)
$ grep -c tree.json /home/vgpnk/Projects/shokunin/LOG.md ; grep -ci 'tree.json|quarantine' .ufo/watchdog.log -> no records
seat denials on record: w1/ExecXkbLive.md:251-256, w1/ExecXkbSource.md:112, w1/ScoutXkbSpecs.md:93,
w1/CritPremiseC2.md:23-24 (reply sent to MadoR48). No admission found anywhere in w1.
```

## Sweep accounting

```
round-45/46/47 'captured-by: none' rows = M45-2(:51), M45-4(:56), M45-6(:61), M46-6(:195), M46-11(:248),
  M46-13(:280), M46-16(:309), M47-6(:178)  -> 8 rows, matching mistakes.md's "eight rows"
M46-13 (pyc write) is NOT named in mistakes.md's duplicate-check accounting sentence; its class is de-facto
  criterion 95's failing input, but 95 cites M47-6 (grep 'lesson:' at QUALITY.md:504).
grep -c M46-6|M46-11 corpus/QUALITY.md -> rc 1 (matches "still uncited")
```
