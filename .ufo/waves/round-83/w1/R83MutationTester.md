STATUS: defect

# R83MutationTester — bounded independent mutation probes

Axes: C1 surface-band coverage; C2 matcher strictness. No admission vote.

Read frozen declaration. Lane HEAD observed dbc09269fe547ab13541e722dd7d2ba33015f348; source hashes below identify actual tested bytes. No instrument, controls, shared source, git/jj state, or host configuration changed. No installs/updates. Only owned report and isolated scratch were written.

## Findings

Three plausible independent defects survive BOTH frozen-case replay and existing selftests. Additional adversarial witnesses distinguish pristine/mutated/restored behavior; they are not new frozen acceptance criteria.

| Mutant | Exact scratch delta | Frozen replay / existing selftest | Witness before → mutated → restored | Verdict |
|---|---|---|---|---|
| C1 extra-positive-allocation-overrides | After composition resolver's `spec[axis] = band_of(spec, allocation)`, append `elif spec is not bar_spec and spec["namespace"] in allocation:` then `spec[axis] = allocation[spec["namespace"]]` | 58/58 and 136/136 in all phases | panel explicit height 40, allocation 60: CLEAN rc0 / height40 zone40 → DIFFER rc1 / height60 zone60 → CLEAN rc0 / height40 zone40 | SURVIVED |
| C2 boolean-padding-normalized | `re.fullmatch(r"b (true|false)", text)` → `re.fullmatch(r"b (true|false)", text.strip())` | 31/31 and 96/96 in all phases | `matches("bool_property", {}, 0, " b true\n")`: false → true → false | SURVIVED |
| C2 array-first-projection | `all(fields_ok(item, value) for item in data)` → `all(fields_ok(item, value) for item in data[:1])` | 31/31 and 96/96 in all phases | array `[valid_monitor, {}]` with frozen monitors-dump schema: false → true → false | SURVIVED |
| C2 upper-bound-omitted | `return lo <= number <= hi` → `return lo <= number` | frozen cases 31/31, but selftest 94/96 rc1 (`int range upper`, `case churn refused`) | `[0,10000]`, `10001\n`: false → true → false | KILLED by selftest; frozen cases alone miss it |

Existing C1 `alloc-explicit-overridden` alters band_of globally, not the composition-only non-bar reader tested here. Existing C2 bool mutants remove literal validation or refuse false; neither tests whitespace normalization. Existing array/object selftest does not test invalid later array entries.

Exploratory count probe also tested `return lo <= number <= (hi + 1 if hi == 10000 else hi)`: 31/31, 96/96, witness false→true→false, SHA 26f6989201177e76414daf33d46f12d5f20c842138cc1c55c2c114da306a7270. This domain-targeted mutation is weaker evidence than the generic upper-bound omission, so it is not counted among the three plausible surviving defects above.

## Detector scope and reproduction

Only bounded local replay; NO live bus/session/desktop commands, full counter target verdict, or named-mutant sweep claimed. The C1 frozen detector was the unchanged counter's run_cases (58 supplied fixtures) plus tool selftest. C2 detector was unchanged case_correct for every frozen case (using frozen output when provided, otherwise first positive sample; case_correct also checks all declared samples and negatives), plus counter selftest. New witnesses expose rule violations separately. Same detector ran pristine, mutated, and exact-restored sources. Initial witness harness lacked anchor_names; repaired fixture by using parse_surfaces before the successful pristine baseline. That harness failure was not a mutant kill.

To reproduce, copy the two source files into an isolated directory as c1.py and c2count.py/c2bool.py/c2array.py. Run the driver below with argument pristine, apply the exact deltas above only to those copies, run with mutated, restore source bytes, run with restored. The driver uses absolute seat scratch paths; replace that root consistently for a new isolated replay. All successful driver commands exited 0; per-probe selftest_rc and witness verdict/rc are captured separately.

## Hash and restoration evidence

C1 pristine and restored SHA256: 8b17706014e6708a11413f0bd6c3398ca4e1b95b40b9c2d51f80f5064c677207.
C1 mutated: 0504f81b72d781ed0caca63399a978e9fff59951a9077275bcda9e54e400bd35.
All C2 pristine/restored copies: 7e256b0fbbef517802a3bc939cef4a1784abf2606f7f5826e0808b6975bad3a0.
C2 boolean mutated: dcb4826dfb2b1c21d6f13ad5abc17157b7286cef794df36c26d006cbd61163ec.
C2 array mutated: 8fdf470c4a420e3dd53e424baa15bcd832877b395c3deec6ac6d9bde74dcc4fa.
C2 generic count mutated: c1c24c0584116fd15c2ff92a6457af9be0d66e06f91c4da40062b90659203afd.

Final restored run: C1 58/58 + selftest136/136, all C2 31/31 + selftest96/96, all witnesses back to pristine values; hashes exactly match pristine. Scratch removed after report capture, before terminal yield.

## Executed driver

```python
import contextlib, hashlib, importlib.util, io, json, pathlib, sys
ROOT=pathlib.Path('/fast/scratch/hyaku/mado-r83/R83MutationTester')
LANE=pathlib.Path('/home/vgpnk/Projects/shokunin/mado-shokunin')
def load(path, name):
    spec=importlib.util.spec_from_file_location(name, path)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod
phase=sys.argv[1]
results=[]
for name in ('c2count','c2bool','c2array','c1'):
    path=ROOT/(name+'.py')
    mod=load(path,name)
    captured=io.StringIO()
    with contextlib.redirect_stdout(captured):
        selfrc=mod.selftest()
    row={'phase':phase,'probe':name,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'selftest_rc':selfrc,'selftest_output':captured.getvalue().strip()}
    if name=='c1':
        detector=load(LANE/'quality/counters/c1-r83-surface-band.py','detector')
        cases=json.loads((LANE/'.ufo/waves/round-83/controls/c1-cases-r83.json').read_text())['cases']
        correct, details=detector.run_cases(str(path),cases,str(ROOT),phase)
        row.update(correct=correct,total=len(cases),failures=[x for x in details if not x[-1]])
        tool=mod
        spec=tool.parse_surfaces(json.dumps([{'namespace':'panel','position':'top','height':40,'width':0,'exclusive':'auto','level':3}]).encode())[0]
        cfg={'position':'top','layer':'top','height':26}
        layers={'M1':{'levels':{'0':[],'1':[],'2':[{'namespace':'waybar','x':0,'y':0,'w':1000,'h':26}],'3':[{'namespace':'panel','x':0,'y':26,'w':1000,'h':40}]}}}
        mon={'M1':{'name':'M1','width':1000,'height':800,'reserved':[0,66,0,0],'scale':1.0,'transform':0}}
        v,rc,lines=tool.evaluate(cfg,layers,mon,'M1',None,'none',[spec],{'panel':60})
        row['witness']={'verdict':v,'rc':rc,'decl':[text for kind,text in lines if kind=='DECL']}
    else:
        cases=json.loads((LANE/'.ufo/waves/round-83/controls/c2-runbook-cases-r83.json').read_text())['cases']
        good=[]
        for case in cases:
            sample={'rc':0,'out':case['frozen']} if 'frozen' in case else case['samples'][0]
            good.append(mod.case_correct(case,sample['rc'],sample['out']))
        row.update(correct=sum(good),total=len(cases),failures=[c['name'] for c,g in zip(cases,good) if not g])
        if name=='c2count':
            row['witness']=mod.matches('int_range',[0,10000],0,'10001\n')
        elif name=='c2bool':
            row['witness']=mod.matches('bool_property',{},0,' b true\n')
        else:
            schema=next(c['value'] for c in cases if c['kind']=='array_fields')
            valid=json.loads(next(c['samples'][0]['out'] for c in cases if c['kind']=='array_fields'))[0]
            row['witness']=mod.matches('array_fields',schema,0,json.dumps([valid,{}]))
    results.append(row)
print(json.dumps(results,indent=2))
(ROOT/(phase+'.json')).write_text(json.dumps(results,indent=2)+'\n')

```

## Actual JSON receipts

### pristine

```json
[
  {
    "phase": "pristine",
    "probe": "c2count",
    "sha256": "7e256b0fbbef517802a3bc939cef4a1784abf2606f7f5826e0808b6975bad3a0",
    "selftest_rc": 0,
    "selftest_output": "MADO_R83_RUNBOOK_SELFTEST: 96/96",
    "correct": 31,
    "total": 31,
    "failures": [],
    "witness": false
  },
  {
    "phase": "pristine",
    "probe": "c2bool",
    "sha256": "7e256b0fbbef517802a3bc939cef4a1784abf2606f7f5826e0808b6975bad3a0",
    "selftest_rc": 0,
    "selftest_output": "MADO_R83_RUNBOOK_SELFTEST: 96/96",
    "correct": 31,
    "total": 31,
    "failures": [],
    "witness": false
  },
  {
    "phase": "pristine",
    "probe": "c2array",
    "sha256": "7e256b0fbbef517802a3bc939cef4a1784abf2606f7f5826e0808b6975bad3a0",
    "selftest_rc": 0,
    "selftest_output": "MADO_R83_RUNBOOK_SELFTEST: 96/96",
    "correct": 31,
    "total": 31,
    "failures": [],
    "witness": false
  },
  {
    "phase": "pristine",
    "probe": "c1",
    "sha256": "8b17706014e6708a11413f0bd6c3398ca4e1b95b40b9c2d51f80f5064c677207",
    "selftest_rc": 0,
    "selftest_output": "MADO_BARFOOT_SELFTEST: 136/136",
    "correct": 58,
    "total": 58,
    "failures": [],
    "witness": {
      "verdict": "CLEAN",
      "rc": 0,
      "decl": [
        "monitor=M1 level=2 ns=waybar box=0,0,1000,26 anchor=top+left+right zone=26",
        "monitor=M1 level=3 ns=panel box=0,26,1000,40 anchor=top+left+right zone=40"
      ]
    }
  }
]

```

### mutated

```json
[
  {
    "phase": "mutated",
    "probe": "c2count",
    "sha256": "26f6989201177e76414daf33d46f12d5f20c842138cc1c55c2c114da306a7270",
    "selftest_rc": 0,
    "selftest_output": "MADO_R83_RUNBOOK_SELFTEST: 96/96",
    "correct": 31,
    "total": 31,
    "failures": [],
    "witness": true
  },
  {
    "phase": "mutated",
    "probe": "c2bool",
    "sha256": "dcb4826dfb2b1c21d6f13ad5abc17157b7286cef794df36c26d006cbd61163ec",
    "selftest_rc": 0,
    "selftest_output": "MADO_R83_RUNBOOK_SELFTEST: 96/96",
    "correct": 31,
    "total": 31,
    "failures": [],
    "witness": true
  },
  {
    "phase": "mutated",
    "probe": "c2array",
    "sha256": "8fdf470c4a420e3dd53e424baa15bcd832877b395c3deec6ac6d9bde74dcc4fa",
    "selftest_rc": 0,
    "selftest_output": "MADO_R83_RUNBOOK_SELFTEST: 96/96",
    "correct": 31,
    "total": 31,
    "failures": [],
    "witness": true
  },
  {
    "phase": "mutated",
    "probe": "c1",
    "sha256": "0504f81b72d781ed0caca63399a978e9fff59951a9077275bcda9e54e400bd35",
    "selftest_rc": 0,
    "selftest_output": "MADO_BARFOOT_SELFTEST: 136/136",
    "correct": 58,
    "total": 58,
    "failures": [],
    "witness": {
      "verdict": "DIFFER",
      "rc": 1,
      "decl": [
        "monitor=M1 level=2 ns=waybar box=0,0,1000,26 anchor=top+left+right zone=26",
        "monitor=M1 level=3 ns=panel box=0,26,1000,60 anchor=top+left+right zone=60"
      ]
    }
  }
]

```

### restored

```json
[
  {
    "phase": "restored",
    "probe": "c2count",
    "sha256": "7e256b0fbbef517802a3bc939cef4a1784abf2606f7f5826e0808b6975bad3a0",
    "selftest_rc": 0,
    "selftest_output": "MADO_R83_RUNBOOK_SELFTEST: 96/96",
    "correct": 31,
    "total": 31,
    "failures": [],
    "witness": false
  },
  {
    "phase": "restored",
    "probe": "c2bool",
    "sha256": "7e256b0fbbef517802a3bc939cef4a1784abf2606f7f5826e0808b6975bad3a0",
    "selftest_rc": 0,
    "selftest_output": "MADO_R83_RUNBOOK_SELFTEST: 96/96",
    "correct": 31,
    "total": 31,
    "failures": [],
    "witness": false
  },
  {
    "phase": "restored",
    "probe": "c2array",
    "sha256": "7e256b0fbbef517802a3bc939cef4a1784abf2606f7f5826e0808b6975bad3a0",
    "selftest_rc": 0,
    "selftest_output": "MADO_R83_RUNBOOK_SELFTEST: 96/96",
    "correct": 31,
    "total": 31,
    "failures": [],
    "witness": false
  },
  {
    "phase": "restored",
    "probe": "c1",
    "sha256": "8b17706014e6708a11413f0bd6c3398ca4e1b95b40b9c2d51f80f5064c677207",
    "selftest_rc": 0,
    "selftest_output": "MADO_BARFOOT_SELFTEST: 136/136",
    "correct": 58,
    "total": 58,
    "failures": [],
    "witness": {
      "verdict": "CLEAN",
      "rc": 0,
      "decl": [
        "monitor=M1 level=2 ns=waybar box=0,0,1000,26 anchor=top+left+right zone=26",
        "monitor=M1 level=3 ns=panel box=0,26,1000,40 anchor=top+left+right zone=40"
      ]
    }
  }
]

```

### count-upper-removed

```json
[
  {
    "phase": "count-upper-removed",
    "probe": "c2count",
    "sha256": "c1c24c0584116fd15c2ff92a6457af9be0d66e06f91c4da40062b90659203afd",
    "selftest_rc": 1,
    "selftest_output": "MADO_R83_RUNBOOK_SELFTEST_FAIL: int range upper\nMADO_R83_RUNBOOK_SELFTEST_FAIL: case churn refused\nMADO_R83_RUNBOOK_SELFTEST: 94/96",
    "correct": 31,
    "total": 31,
    "failures": [],
    "witness": true
  },
  {
    "phase": "count-upper-removed",
    "probe": "c2bool",
    "sha256": "7e256b0fbbef517802a3bc939cef4a1784abf2606f7f5826e0808b6975bad3a0",
    "selftest_rc": 0,
    "selftest_output": "MADO_R83_RUNBOOK_SELFTEST: 96/96",
    "correct": 31,
    "total": 31,
    "failures": [],
    "witness": false
  },
  {
    "phase": "count-upper-removed",
    "probe": "c2array",
    "sha256": "7e256b0fbbef517802a3bc939cef4a1784abf2606f7f5826e0808b6975bad3a0",
    "selftest_rc": 0,
    "selftest_output": "MADO_R83_RUNBOOK_SELFTEST: 96/96",
    "correct": 31,
    "total": 31,
    "failures": [],
    "witness": false
  },
  {
    "phase": "count-upper-removed",
    "probe": "c1",
    "sha256": "8b17706014e6708a11413f0bd6c3398ca4e1b95b40b9c2d51f80f5064c677207",
    "selftest_rc": 0,
    "selftest_output": "MADO_BARFOOT_SELFTEST: 136/136",
    "correct": 58,
    "total": 58,
    "failures": [],
    "witness": {
      "verdict": "CLEAN",
      "rc": 0,
      "decl": [
        "monitor=M1 level=2 ns=waybar box=0,0,1000,26 anchor=top+left+right zone=26",
        "monitor=M1 level=3 ns=panel box=0,26,1000,40 anchor=top+left+right zone=40"
      ]
    }
  }
]

```

### final-restored

```json
[
  {
    "phase": "final-restored",
    "probe": "c2count",
    "sha256": "7e256b0fbbef517802a3bc939cef4a1784abf2606f7f5826e0808b6975bad3a0",
    "selftest_rc": 0,
    "selftest_output": "MADO_R83_RUNBOOK_SELFTEST: 96/96",
    "correct": 31,
    "total": 31,
    "failures": [],
    "witness": false
  },
  {
    "phase": "final-restored",
    "probe": "c2bool",
    "sha256": "7e256b0fbbef517802a3bc939cef4a1784abf2606f7f5826e0808b6975bad3a0",
    "selftest_rc": 0,
    "selftest_output": "MADO_R83_RUNBOOK_SELFTEST: 96/96",
    "correct": 31,
    "total": 31,
    "failures": [],
    "witness": false
  },
  {
    "phase": "final-restored",
    "probe": "c2array",
    "sha256": "7e256b0fbbef517802a3bc939cef4a1784abf2606f7f5826e0808b6975bad3a0",
    "selftest_rc": 0,
    "selftest_output": "MADO_R83_RUNBOOK_SELFTEST: 96/96",
    "correct": 31,
    "total": 31,
    "failures": [],
    "witness": false
  },
  {
    "phase": "final-restored",
    "probe": "c1",
    "sha256": "8b17706014e6708a11413f0bd6c3398ca4e1b95b40b9c2d51f80f5064c677207",
    "selftest_rc": 0,
    "selftest_output": "MADO_BARFOOT_SELFTEST: 136/136",
    "correct": 58,
    "total": 58,
    "failures": [],
    "witness": {
      "verdict": "CLEAN",
      "rc": 0,
      "decl": [
        "monitor=M1 level=2 ns=waybar box=0,0,1000,26 anchor=top+left+right zone=26",
        "monitor=M1 level=3 ns=panel box=0,26,1000,40 anchor=top+left+right zone=40"
      ]
    }
  }
]

```

## Self-evaluation
Accuracy 5: actual hashes and outputs retained. Completeness 4: bounded synthetic replay, not live/full-counter acceptance; deliberately no wider claim. Clarity 5: exact deltas and witness separation. Actionability 5: driver and fixture retained. Conciseness 4: receipts verbose to preserve restoration evidence. Overall 4.6/5. Improvement: add the three witness classes to a future pre-freeze control set; no instruments changed here.

Report: .ufo/waves/round-83/w1/R83MutationTester.md
