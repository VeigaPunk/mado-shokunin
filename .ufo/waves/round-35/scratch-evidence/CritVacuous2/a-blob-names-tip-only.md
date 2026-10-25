# Blob ledger — names the tip only

The round-34 tip is dff394109f3cc3d851309ad7c67dd3b35b46adf2.

That is the entire evidential content the counter consumes: the hash as a substring.
Below is a deliberately FALSE table — the counter never parses it. Its rows re-verify
against `frozen_blobs` in the frozen spec, not against anything written here.

| Path | blob @ r34 tip (FABRICATED — every row is the same dead hex) |
|---|---|
| `.ufo/waves/round-33/c1/count.py` | `deadbeefdeadbeefdeadbeefdeadbeefdeadbeef` |
| `.ufo/waves/round-33/c1/frozen.json` | `deadbeefdeadbeefdeadbeefdeadbeefdeadbeef` |
| `.ufo/waves/round-33/c2/count.py` | `deadbeefdeadbeefdeadbeefdeadbeefdeadbeef` |
| `.ufo/waves/round-34/c1/count.py` | `deadbeefdeadbeefdeadbeefdeadbeefdeadbeef` |
| `.ufo/waves/round-34/c1/frozen.json` | `deadbeefdeadbeefdeadbeefdeadbeefdeadbeef` |
| `.ufo/waves/round-34/c2/count.py` | `deadbeefdeadbeefdeadbeefdeadbeefdeadbeef` |
| `.ufo/waves/round-34/c2/frozen.json` | `deadbeefdeadbeefdeadbeefdeadbeefdeadbeef` |

PROVEN, apparently.
