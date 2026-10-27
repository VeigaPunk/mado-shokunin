# Attack09 — W2 attack #09: C2 quote location and max 25 words (round 52)

seat=`Attack09` (mutation-tester, W2 leaf) lane=`mado-shokunin` base=`85d57a818c3707397e21c840b6498b105ba798aa`
attacked clause — `claims-frozen.md` C2: "each material factual proposition maps to a pinned source quote <=25 words"
and `registration.md` C2: "a pin path/revision and **exact located quote <=25 words**, with a written support rationale".
Specified control: the committed counter `quality/counters/c2-r52-proposition-entry.py` (frozen predicate:
"a new committed counter checks proposition count, row/pin/quote bindings and complete mapping").
Scope: quote **location** and the **≤25-word** cap only. Entailment/row-freshness/index clauses belong to other seats;
one observed cross-clause line is recorded as context, not judged.

## Verdict summary

| # | finding | verdict |
|---|---|---|
| V1 | Landed P16 quote is **not located** at its cited pin/anchor: it splices `ConfigActions.cpp:1554` directly onto `:1558`, eliding 1555–1557; the quote's fused text occurs **nowhere** in the pinned file (`grep -c` = 0); the anchor's second span `1576` (`sendKeyboardMods(0, 0, 0, 0);`) is never quoted. | **reproduced** against pinned bytes |
| V2 | The committed counter contains **no quote-location check at all** — `pin` and `anchor` columns are captured and never used; it never opens a pin file. Three single-change location mutants (fabricated quote / wrong span / wrong pin file) each `TARGET_MET` exit 0. | **falsified** — 3/3 mutants survived |
| V3 | ≤25-word cap: satisfied on the landing's content (T1 max = 19 words, 18/18 rows); the committed stub enforces `len(quote.split())>25` (26- and 28-word mutants flagged, 25-word passes) — but only on a table shape it can parse. On the **landed** table shape its regex matches **0 rows** (`props=0` → `TARGET_MISSED`), so even the cap is vacuous on the artifact as landed. | cap holds on content; enforcement **vacuous on landed shape** |
| V4 | The committed counter is **not** the W1-validated bytes: committed sha256 `5c7fb820…`, 47 lines, vs W1 `C2CounterDraft` sha256 `55452a3d…` (the hash that report declares), 965 lines. | artifact substitution observed |
| V5 | The W1-validated 965-line detector, run by me against the staged landing, flags exactly the V1 defect: `miss=P16:quote_not_at_pin(Hyprland-ConfigActions.cpp:1554)`, `quotes_bound=17/18`. So P16 fails the round's own frozen comparison policy and the committed control is the broken link. | observed (that counter is uncommitted) |

**Bottom line for L1:** the "exact located quote" half of C2 is falsified as landed (P16) and the committed control cannot
see any location defect; the "≤25 words" half is true of the content and machine-checkable only after a manual column
reorder the landing does not use.

## Attacked artifact

- Landed entry: `corpus/knowledge/hyprland-synthetic-dispatch-r52.md` (sha256 `bee0d14379eb560595c5d2237ffc9fd0f6d61c3b6b728fbb0dab851687ecb078`; 18 proposition rows P01–P18 over rows S370–S373, pins under `.ufo/waves/round-52/fetch/`, revision `efb50993780079460b0cbed1363e2166a2de1d9f`).
- Committed counter: `quality/counters/c2-r52-proposition-entry.py`.
- Pin bytes: `.ufo/waves/round-52/fetch/` — sha256 of all four files re-computed by me and **4/4 equal** to `fetch/SHA256SUMS` and to the `r52 fetch SHA256` declared in SOURCES rows S370–S373 (S370 `7248cbb8…`, S371 `a83abeb5…`, S372 `746c6f51…`, S373 `8d8f35fc…`).

## T1 — direct location + word-count truth check (independent of any counter)

Method (script embedded in Appendix A, run with `python3 -I`): parse the landed table (order
`ID | Proposition | Source row | Pin:anchor | Quote | Support class | Why it supports`, `\|`-escape aware), strip
backticks, collapse whitespace, split each `pin:anchor` on the last `:` into pin basename and comma-separated
1-indexed inclusive spans, build the whitespace-collapsed text of the union of cited spans from the pinned fetch
file, and test containment; word count = whitespace tokens of the normalized quote.

```
prop  words  pin_file                                anchor            at_pin
P01      7  Hyprland-legacy-DispatcherTranslator.cpp  591-594          True
P02     12  Hyprland-legacy-DispatcherTranslator.cpp  597-598          True
P03     19  Hyprland-legacy-DispatcherTranslator.cpp  600-604          True
P04     13  Hyprland-legacy-DispatcherTranslator.cpp  619-622          True
P05     12  Hyprland-legacy-DispatcherTranslator.cpp  607              True
P06      7  Hyprland-legacy-DispatcherTranslator.cpp  531-535          True
P07      5  Hyprland-KeybindManager.cpp              221-225          True
P08     17  Hyprland-legacy-DispatcherTranslator.cpp  540-543          True
P09     14  Hyprland-legacy-DispatcherTranslator.cpp  544-547          True
P10     15  Hyprland-legacy-DispatcherTranslator.cpp  565-566          True
P11      7  Hyprland-legacy-DispatcherTranslator.cpp  557              True
P12      8  Hyprland-legacy-DispatcherTranslator.cpp  582-586          True
P13      5  Hyprland-ConfigActions.cpp               1558             True
P14     10  Hyprland-ConfigActions.hpp               117              True
P15      5  Hyprland-legacy-DispatcherTranslator.cpp  612              True
P16      9  Hyprland-ConfigActions.cpp               1554-1558,1576   False  (elsewhere=absent)
P17      9  Hyprland-legacy-DispatcherTranslator.cpp  619-622          True
P18     10  Hyprland-legacy-DispatcherTranslator.cpp  574              True
T1 rows=18 at_pin_failures=1 ['P16'] max_quote_words=19 cap_le_25=PASS
```

17/18 quotes locate; max 19 words ≤ 25; min 5 words. **P16 fails even under the permissive union-of-spans reading**
(and under whole-file search), i.e. it is not a compound-anchor parsing artifact.

### Byte-level reproduction of V1 (no tooling beyond coreutils)

```
$ awk 'NR>=1554 && NR<=1558' .ufo/waves/round-52/fetch/Hyprland-ConfigActions.cpp | tr -s '[:space:]' ' '
 g_pSeatManager->sendKeyboardMods(modMask, 0, 0, 0); if (S.m_passPressed == 1) { if (!isMouse) g_pSeatManager->sendKeyboardKey(S.m_timeLastMs, key - 8, WL_KEYBOARD_KEY_STATE_PRESSED);
$ grep -c 'sendKeyboardMods(modMask, 0, 0, 0); g_pSeatManager' .ufo/waves/round-52/fetch/Hyprland-ConfigActions.cpp
0
$ awk 'NR==1576' .ufo/waves/round-52/fetch/Hyprland-ConfigActions.cpp
    g_pSeatManager->sendKeyboardMods(0, 0, 0, 0);
```

Line map: 1554 = `…sendKeyboardMods(modMask, 0, 0, 0);` (quote fragment 1), 1555 = blank, 1556 = `if (S.m_passPressed == 1) {`,
1557 = `if (!isMouse)` (both elided by the quote), 1558 = `…sendKeyboardKey(S.m_timeLastMs, key - 8, WL_KEYBOARD_KEY_STATE_PRESSED);`
(quote fragment 2), 1576 = the clear call asserted by the proposition but present only in the locator, never in the quote.
The quote's fused adjacency exists at **no** line of the pinned file.

## T2 — the committed counter on the landing (pristine)

Staged the landing into a scratch git repo (`/fast/scratch/hyaku/mado-r52/Attack09/stage`, toplevel asserted before
any git mutation; base commit `4c6d3458bb36c690ec4813debf2addedb55dda02`), then:

```
$ python3 -I quality/counters/c2-r52-proposition-entry.py --repo <stage> --rev 4c6d3458… --work <scratch>/work \
    --entry corpus/knowledge/hyprland-synthetic-dispatch-r52.md
C2_R52: props=0 rows=0 indexed=1 failures=1 verdict=TARGET_MISSED rev=4c6d3458…
miss=props
exit=1
```

The stub's row regex `^\|\s*(P\d+)\s*\|\s*(S\d+)\s*\|…` hardcodes the S-row as the **second** cell; the landed table
puts the proposition text there and the S-row third. It parses **zero** proposition rows of the landing, so no
proposition-count, row, quote or cap check ever executes on the artifact as landed (MISSED, not a false pass — but a
dead control).

```
$ python3 -I quality/counters/c2-r52-proposition-entry.py --repo <stage> --rev 4c6d3458… --work <scratch>/work
C2_R52: entry=absent verdict=TARGET_MISSED rev=4c6d3458…
exit=1
```

Its `--entry` default is still the W1 draft slug `corpus/knowledge/hyprland-synthetic-key-dispatch-r52.md`; the landed
slug is `…synthetic-dispatch-r52.md`. Out of the box the committed counter cannot even name the landed entry.

Source inspection of the stub (committed bytes, 47 lines): `pin` and `anchor` are captured by the regex and **never
referenced again**; the only quote check is `len(quote.split())>25` plus a non-empty-rationale test. There is no file
read of any pin, no span arithmetic, no string comparison against pinned bytes.

## T3 — single-change mutants at the landed path (mutation probe)

Each variant is the landed table re-expressed in the column order the stub parses
(`ID | Source row | Proposition | Pin | Anchor | Quote | Why it supports`; support-class column folded out — a
metadata cell, not a predicate field), committed **alone at the landed entry path** so `indexed=1` and `rowmeta` stay
green and the single mutation is the only delta. Baseline `v-correct` (reorder only, zero content change) is green.

| mutant | single change | counter output | verdict |
|---|---|---|---|
| `v-correct` rev `46085a4d…` | none (column reorder) | `props=18 rows=4 indexed=1 failures=0 verdict=TARGET_MET` exit 0 | baseline green — **stub METs an entry containing P16's spliced quote** |
| `v-fabquote` rev `44270735…` | P13 quote → fabricated call `g_pSeatManager->sendKeyboardKey(999999, key, WL_KEYBOARD_KEY_STATE_RELEASED);` (programmatically verified absent from `ConfigActions.cpp`) | `failures=0 verdict=TARGET_MET` exit 0 | **survived** — fabricated quote accepted |
| `v-wronganchor` rev `c66370d5…` | P15 anchor `612` → `600-604` (span not containing the quote) | `failures=0 verdict=TARGET_MET` exit 0 | **survived** — anchor span never validated |
| `v-wrongpin` rev `51b53c81…` | P15 pin → `Hyprland-KeybindManager.cpp:221-225` (quote in no line of that file) | `failures=0 verdict=TARGET_MET` exit 0 | **survived** — pin file never opened |
| `v-quote25` rev `f4fd5746…` | P14 quote → exactly 25 real words (first 25 tokens of `ConfigActions.hpp:110-117`) | `failures=0 verdict=TARGET_MET` exit 0 | cap boundary inclusive at 25 — control holds |
| `v-quote26` rev `a3a2081e…` | same, 26 words | `miss=quote/rationale:P14 verdict=TARGET_MISSED` exit 1 | **killed** |
| `v-quote28` rev `98104ca1…` | same, 28 words | `miss=quote/rationale:P14 verdict=TARGET_MISSED` exit 1 | **killed** |

(An earlier run at a *variant* path — rev `06857d38…` — drowned the location mutants in unrelated `index`/`rowmeta`
failures; the landed-path series above is the clean one-change series. Both outputs were captured; only the landed-path
series is evidentiary.)

Reading: for the **location** half of the attacked clause the committed control has zero discriminating power —
3/3 location mutants survive, and `v-correct` shows it green-lighting the real P16 splice. For the **word-cap** half
the control does discriminate (26>25 flagged, 25 passes) whenever it can parse the table at all — which, on the
landing's actual shape, it cannot (T2).

## T4 — the W1-validated detector run against the same staged landing

To separate "P16 is a defect" from "the committed tool is broken", I ran the untouched W1 bytes
(`.ufo/waves/round-52/w1/C2CounterDraft/c2-r52-proposition-entry.py`, sha256 `55452a3d…`, 965 lines) against the
landing staged with the four fetch pins (rev `5c8b648a…`; base object fetched read-only from the lane so its
base-registry comparison works):

```
C2_R52: a ok=1 … b ok=1 propositions=18 ids=18 forms=table
C2_R52: c ok=0 rows_bound=0/18 … miss=P01:anchor_no_fetch_root,…
C2_R52: d ok=0 quotes_bound=17/18 quotes_raw=6/17 pins=4 policy=whitespace-collapsed pins_prior_equal=4/17
        miss=P16:quote_not_at_pin(Hyprland-ConfigActions.cpp:1554)
C2_R52: e ok=0 … miss=P01:id_not_referenced,…
C2_R52: clauses=abcde clauses_met=2 admitted=0/1 verdict=TARGET_MISSED
```

Clause (d) — my clause — independently confirms V1 under the round's frozen comparison policy
(`quote_policy=whitespace-collapsed`): **17/18 bind, P16 does not, at `ConfigActions.cpp:1554`**. The clause (c)/(e)
misses are other seats' clauses (registry anchor cells lack the fetch path; proposition ids not drawn on outside the
map in the landed entry) — recorded as context for L1, not judged here. Note this detector is **uncommitted**; it is
evidence of the defect, not the frozen control.

## Restoration and hygiene evidence

- Stage repo: entry blob `b4496f75b8426f3e46f352a4a74b084fd5f1aab8` before first run and after `git reset --hard` back
  to base commit `4c6d3458…`; `git status --porcelain` = 0 lines at restoration. Mutant commits were scratch-only.
- Lane repo untouched by me: `git status --porcelain` before and after identical
  (` M corpus/README.md`, ` M corpus/SOURCES.md`, ` M quality/tool-ledger.md`, `?? .ufo/waves/round-52/`,
  `?? corpus/knowledge/hyprland-synthetic-dispatch-r52.md`, `?? corpus/lessons/round-52.md`,
  `?? quality/counters/c1-r52-ledger.py`, `?? quality/counters/c2-r52-proposition-entry.py`).
  The lane tip remains `85d57a81` — the entire C2 landing is uncommitted working-tree state (context for L1; the
  predicate says "new committed counter").
- Scratch `/fast/scratch/hyaku/mado-r52/Attack09` removed after this report was written. No install, no package
  query, no network fetch, no live read, no probe, no git/jj mutation outside the scratch fixture.

## Limitations

- **Offline truth.** No live reads were permitted: quote-location truth is established against the local fetch bytes,
  whose sha256 values equal the fetch manifest and the rows' declared r52 fetch SHA (4/4). That those bytes equal
  upstream `efb50993780079460b0cbed1363e2166a2de1d9f` rests on the round's own fetch receipts, not on my re-download.
- **Policy dependence.** My T1 uses the same comparison policy as the round's counters (backticks stripped,
  whitespace-collapsed, span union for compound anchors). A laxer policy that permits interior elision would pass
  P16; the round's frozen policy (verbatim whitespace-collapsed within the cited span, as implemented by the W1
  detector's `quote_not_at_pin`) does not.
- **Word count** = whitespace tokens of the normalized quote cell (the stub's own `quote.split()`), backticks stripped;
  a different tokenization (e.g. counting punctuation-separated code tokens) would change counts but not the 19 ≤ 25
  verdict direction.
- **Not judged here:** whether P16's *proposition* is true (the quote also conceals that the key send is conditional on
  `S.m_passPressed == 1 && !isMouse`) — that is entailment, reserved to the independent non-author review; the clause
  (c)/(e) failures seen in T4; and C1 entirely.
- The 47-line stub shares none of the 965-line detector's code paths; my "would have caught" statements are limited to
  T4, which I actually ran.

## Reproduction commands (all paths lane-root-relative)

```
# V1 splice
awk 'NR>=1554 && NR<=1558' .ufo/waves/round-52/fetch/Hyprland-ConfigActions.cpp | tr -s '[:space:]' ' '
grep -c 'sendKeyboardMods(modMask, 0, 0, 0); g_pSeatManager' .ufo/waves/round-52/fetch/Hyprland-ConfigActions.cpp   # 0
# T2 dead control (needs a scratch git repo holding the landing; see Appendix A for staging)
python3 -I quality/counters/c2-r52-proposition-entry.py --repo <stage> --rev <stage-rev> --work <scratch>/work \
  --entry corpus/knowledge/hyprland-synthetic-dispatch-r52.md    # props=0 -> TARGET_MISSED
# T3/T4: stage each Appendix-A variant at the landed path and rerun the same command per commit;
# T4 uses .ufo/waves/round-52/w1/C2CounterDraft/c2-r52-proposition-entry.py with fetch pins staged.
```

Appendix A (exact probe source, preserved here since scratch is removed):

```python
#!/usr/bin/env python3
# t1_variants.py — Attack09 r52 W2; read-only on the lane, writes only under the Attack09 scratch.
import os, re, sys
LANE='/home/vgpnk/Projects/shokunin/mado-shokunin'
FETCH=os.path.join(LANE,'.ufo/waves/round-52/fetch')
ENTRY=os.path.join(LANE,'corpus/knowledge/hyprland-synthetic-dispatch-r52.md')
STAGE='/fast/scratch/hyaku/mado-r52/Attack09/stage/corpus/knowledge'
def collapse(s):
    s=s.replace('`','')
    return re.sub(r'\s+',' ',s).strip()
def split_cells(line):
    out,cur,esc=[],[],False
    for ch in line.strip().strip('|'):
        if esc: cur.append(ch); esc=False
        elif ch=='\\': esc=True
        elif ch=='|': out.append(''.join(cur)); cur=[]
        else: cur.append(ch)
    out.append(''.join(cur)); return [c.strip() for c in out]
body=open(ENTRY,encoding='utf-8').read(); rows=[]
for line in body.splitlines():
    if re.match(r'^\|\s*P\d+\s*\|',line):
        c=split_cells(line)
        rows.append(dict(pid=c[0],prop=c[1],sid=c[2],pac=c[3],quote=c[4],sup=c[5],why=c[6]))
fcache={}
def file_lines(n):
    if n not in fcache: fcache[n]=open(os.path.join(FETCH,n),encoding='utf-8').read().splitlines()
    return fcache[n]
maxw=0; bad=[]
for r in rows:
    pinname,_,sp=r['pac'].rpartition(':'); q=collapse(r['quote']); w=len(q.split()); maxw=max(maxw,w)
    spans=[]
    for part in sp.split(','):
        a,sep,b=part.partition('-'); spans.append((int(a),int(b) if sep else int(a)))
    lines=file_lines(pinname)
    span_text=collapse(' '.join(' '.join(lines[a-1:b]) for a,b in spans))
    at=q in span_text
    if not at: bad.append(r['pid'])
    print(r['pid'],w,pinname,sp,at)
print(f'T1 rows={len(rows)} at_pin_failures={len(bad)} {bad} max_quote_words={maxw}')
# variants: column reorder the stub parses: ID | S | prop | pin | anchor | quote | why
def vrows(mut):
    out=[]
    for r in rows:
        pinname,_,sp=r['pac'].rpartition(':')
        pid,sid,prop,pin,anchor,quote,why=mut(r['pid'],r['sid'],r['prop'],pinname,sp,r['quote'],r['why'])
        out.append(f'| {pid} | {sid} | {prop} | {pin} | {anchor} | {quote} | {why} |')
    return out
HDR=('## Proposition map\n\n| ID | Source row | Proposition | Pin | Anchor | Quote (<=25 words) | Why it supports |\n|---|---|---|---|---|---|---|\n')
FTR='\nAll pins under `.ufo/waves/round-52/fetch/`, revision efb50993780079460b0cbed1363e2166a2de1d9f, opened 2026-10-27.\n'
def write(name,mut):
    open(os.path.join(STAGE,name),'w',encoding='utf-8').write(
        body.split('\n',1)[0]+'\n\n'+HDR+'\n'.join(vrows(mut))+'\n'+FTR)
def ident(pid,sid,prop,pin,anchor,quote,why): return pid,sid,prop,pin,anchor,quote,why
write('v-correct.md',ident)
def fab(pid,sid,prop,pin,anchor,quote,why):
    return (pid,sid,prop,pin,anchor,'`g_pSeatManager->sendKeyboardKey(999999, key, WL_KEYBOARD_KEY_STATE_RELEASED);`',why) if pid=='P13' else (pid,sid,prop,pin,anchor,quote,why)
write('v-fabquote.md',fab)
def wang(pid,sid,prop,pin,anchor,quote,why):
    return (pid,sid,prop,pin,'600-604',quote,why) if pid=='P15' else (pid,sid,prop,pin,anchor,quote,why)
write('v-wronganchor.md',wang)
def wpin(pid,sid,prop,pin,anchor,quote,why):
    return (pid,sid,prop,'Hyprland-KeybindManager.cpp','221-225',quote,why) if pid=='P15' else (pid,sid,prop,pin,anchor,quote,why)
write('v-wrongpin.md',wpin)
hp=re.sub(r'\s+',' ',' '.join(file_lines('Hyprland-ConfigActions.hpp')[109:117])).strip(); toks=hp.split(' ')
for n in (25,26,28):
    write(f'v-quote{n}.md',(lambda n: lambda pid,sid,prop,pin,anchor,quote,why:
        (pid,sid,prop,pin,anchor,'`'+' '.join(toks[:n])+'`',why) if pid=='P14' else (pid,sid,prop,pin,anchor,quote,why))(n))
```

Counter-run harness (scratch staging, per variant):

```
SCRATCH=/fast/scratch/hyaku/mado-r52/Attack09; LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
mkdir -p $SCRATCH/stage/corpus/knowledge $SCRATCH/work
cp $LANE/corpus/README.md $LANE/corpus/SOURCES.md $SCRATCH/stage/corpus/
cp $LANE/corpus/knowledge/hyprland-synthetic-dispatch-r52.md $SCRATCH/stage/corpus/knowledge/
git -C $SCRATCH/stage init -q
test "$(git -C $SCRATCH/stage rev-parse --show-toplevel)" = "$SCRATCH/stage"   # host guard
git -C $SCRATCH/stage add -A && git -C $SCRATCH/stage -c user.email=a@scratch -c user.name=Attack09 commit -qm stage
# then per variant: cp variant over the landed path, commit, run the T2 command at that rev; reset --hard to base after.
```

## Report trailer

```
seat=Attack09 wave=w2 round=52 lane=mado-shokunin base=85d57a818c3707397e21c840b6498b105ba798aa
claim=C2 coverage proposition-bound dispatcher source entry
attacked_clause="pin path/revision and exact located quote <=25 words" target="quote location and max 25 words"
entry=corpus/knowledge/hyprland-synthetic-dispatch-r52.md sha256=bee0d14379eb560595c5d2237ffc9fd0f6d61c3b6b728fbb0dab851687ecb078
committed_counter=quality/counters/c2-r52-proposition-entry.py sha256=5c7fb820e43c7f6782b6ebfc90d018c25d74976d9e8ab2a90df5e4c82fb50c0a lines=47
w1_counter=.ufo/waves/round-52/w1/C2CounterDraft/c2-r52-proposition-entry.py sha256=55452a3d6eab7cca2b20095f8678fbe936c8c65f241a561611a675defd8379fb lines=965
t1_direct=17/18 at_pin, failures=[P16 splice 1554+1558 eliding 1555-1557, span 1576 unquoted], max_quote_words=19 cap_le_25=PASS
t2_committed_on_landing=props=0 TARGET_MISSED (regex shape mismatch; default --entry slug = W1 draft slug, absent)
t3_mutants=fabricated_quote SURVIVED, wrong_anchor SURVIVED, wrong_pin SURVIVED, quote25 MET, quote26 KILLED, quote28 KILLED
t4_w1_detector_on_landing=clause_d quotes_bound=17/18 miss=P16:quote_not_at_pin(Hyprland-ConfigActions.cpp:1554)
verdict=quote-location falsifier REPRODUCED on landing; committed control performs NO location check (3/3 survived); <=25 cap true on content, enforced only on parseable shape
scratch=/fast/scratch/hyaku/mado-r52/Attack09 REMOVED
lane_untouched=true (status identical pre/post; no tracked edits; no git/jj mutation outside scratch)
```
