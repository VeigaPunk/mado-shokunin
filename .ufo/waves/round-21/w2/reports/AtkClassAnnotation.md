# ClassAnnotation review (C1, supplemental)

**Axes:** frozen semantic correctness; generality of the scanner rule; nearby variant.

## Frozen expectation — correct

The pinned input at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/oracle/inputs/ClassAnnotation.jsonl` has `annotation: f`, where `f` is an ordinary function whose body contains `subprocess.run(["pacman", "-Q", "r21"])`. The empty expected findings are semantically warranted. In Python 3.14.8, simple class-scope variable annotations are lazily evaluated in an annotation scope; class creation does not evaluate `f`. If the annotation is later forced, evaluating the name `f` yields the function object but still does not call its body. The oracle proposal at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w1/oracles/ClassAnnotation.json` therefore has a correct rationale and `want: []`. Under earlier eager annotation semantics, evaluating the name `f` likewise produces a function object without invoking it.

Primary references: [Python 3.14.8 annotated assignment semantics](https://docs.python.org/3.14/reference/simple_stmts.html#annotated-assignment-statements), [lazy evaluation](https://docs.python.org/3.14/reference/executionmodel.html#lazy-evaluation), and [annotationlib formats](https://docs.python.org/3.14/library/annotationlib.html#annotation-semantics). The pinned input SHA-256 is `ab124d7b62819dd72ed98b258125584ac6479d40088518b651d67dc2b4e9577a`; the proposal SHA-256 is `ad8cb5ef4c35404a3d25bd30b699a47d10f7559b533318e9dcfc2979fd55ffd7`; the expected snapshot SHA-256 is `fd2bfbc86897e1ee7a79302f6ccf6c3403709b132180864a0674f8212925576f`.

## Rule generality and source-derived risk

The candidate rule is syntactic, not keyed to fixture text: `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:1879-1891` treats all `ast.AnnAssign` nodes alike and omits annotation expressions. `prepare_eval_calls` at lines 1979-1980 consumes that walk; `classify_eval` at lines 2036-2039 sends only the resulting calls/references to `spawn_scan`. This is correct for the frozen unforced `annotation: f` case, but leaves explicit lazy-annotation forcing unmodeled.

Nearby forced variant, considered as inert source only:

```python
import subprocess

def f():
    subprocess.run(["pacman", "-Q", "r21"])

class C:
    annotation: f()

C.__annotations__
```

Python 3.14.8 documents `C.__annotations__` as a way to evaluate simple class-scope annotations. On that path the annotation expression calls `f`, reaching the literal subprocess call; the expected static finding is `package_query`, command `pacman -Q r21`, evidence `observed`. The scanner source has no corresponding path: it drops the `AnnAssign.annotation` AST, while `C.__annotations__` is an attribute expression rather than an `ast.Call`. `eager_calls` records only the receiver reference as a `__getattr__` protocol at lines 1843-1844; `spawn_scan`'s protocol branch at lines 2373-2385 does not force class annotations and continues without resolving this class attribute. This is a source-derived likely miss, not an observed scanner output; no classifier rerun or payload execution was performed per the parent instruction.

### Correction to the initial probe interpretation

The retained inert probe at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w2/fixtures/AtkClassAnnotation-2/class-annotation-call.jsonl` changes only `annotation: f` to `annotation: f()`. Its SHA-256 is `d989cd6b6787b2aa8362f518fa18ff810e65e64bf7dc808a9a53709e37a0b443`. The earlier bounded scanner run returned `exit=0`, zero findings, and no stderr. Under Python 3.14.8 that output is not evidence of a false negative: without subsequent annotation access, `f()` remains lazily unevaluated. The earlier report's expected-finding interpretation and unconditional false-negative verdict are withdrawn. The forced variant above is the relevant challenge; its scanner output was not rerun or observed.

## Verdict and limits

**Verdict: no defect established for the frozen case or the unforced `f()` probe; medium source-derived risk for an explicitly forced annotation.** The scanner rule is general rather than fixture-specific, but its failure to model access-triggered evaluation appears to miss the forced variant above. This finding is tied to tested scanner bytes and the cited Python 3.14.8 semantics; it is not presented as measured output.

The scanner bytes reviewed were `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py`, SHA-256 `2e152f6dcd9a0d13ffc1d64e88bcc600548e66bd04c34f92dbc5a0808338372d`. This seat observed `git rev-parse HEAD` as `a8da015624c92f4cb4a7de92adbf6643a3f8b38a`; the parent update named candidate commit `f499a8db7171b7476fe9f204ab9edbac5a956fa9`, so this finding is explicitly bound to the tested file hash, not inferred to apply to that different revision. The committed receipt `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/evidence/oracle-candidate.json` records an older measured commit/tool hash (`843d301d1b17af78427918f7845af336b2218de0` / `56ff93751ac09a75065534b5a8d7af5f94986369cee6963b49d27912fce73e11`); its ClassAnnotation pass does not certify the reviewed bytes.

No LSP route was mounted: the `xd://lsp` device lookup reported no such tool and listed mounted devices without LSP. Accordingly, this review used the literal-text fallback and cites source lines; grep results were not treated as semantic proof. No full suite/corpus was run, no tools were installed, and no payload was executed. The forced-annotation finding is source-derived only.

Report: `.ufo/waves/round-21/w2/reports/AtkClassAnnotation.md`
