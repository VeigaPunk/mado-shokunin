# MutGateInstalled — round-50 w2 FALSIFY

Target: installed gate v3 `quality/check-session-material.py`; pristine SHA-256 `ffdc9d62c387050e016cf9d0eaacbf87f37d6647021cbd2c492eb6328dddbb61`. Attack revision `b4a79843cc2545bbe800db9322e58f6e00436629`; frozen counter SHA-256 `1d52a62cd969aba59c2cd1f944212b6f9619212b5fb313c470c4c14ebd62b298`. All counters scored committed gate bytes in the scratch `--shared` clone. No lane tracked files changed.

| Probe | Mutant rev / gate SHA | Direct selftest | Frozen PRED-C2-r50 | Verdict |
|---|---|---:|---|---|
| Pristine control | `b4a79843cc2545bbe800db9322e58f6e00436629` / `ffdc9d62…` | 94/94 | nonce 50501: red 41/41, green 44/44, scope seen, TARGET_MET (rc 0) | baseline valid |
| (a) Remove R8 emission | `c4e4e6c9fd6866200588fcf3b9cd81be8f9de37f` / `818031de…` | 90/94 | nonce 50511: red 34/41, R8 0/7, TARGET_MISSED (rc 1) | KILLED |
| (b) retain only waived findings (invert waiver delta) | `ccea812138e35f83669f92af372a0056538e4737` / `8fb80263…` | 65/94 | nonce 50512: red 0/42, scope blind, TARGET_MISSED (rc 1) | KILLED |
| (c) bypass target SHA comparison | `9413dbc187b4cd6b775cc00773db8ddebf07c739` / `e4de62b9…` | 92/94 | nonce 50513: red 43/43, green 41/41, scope seen, but selftest 92/94; TARGET_MISSED (rc 1) | KILLED |
| (d) registry validation accepts all RULES incl. R5/R6 (w1 MutGateV3 survivor form) | `753df0106ec009adad53c3ca92d03eb0a1df12bf` / `c2fb05d3…` | 94/94 | nonce 50514: red 44/44, green 41/41, scope seen, TARGET_MET (rc 0) | SURVIVED — counter coverage gap |
| (e) R5 detail uses raw matched token instead of `_shape_mask` | `4bc9e25a7d9f2d0c450e86ef3c88806f6d34753c` / `a4dc6e2d…` | 92/94 | nonce 50515: selftest 92/94; TARGET_MISSED (rc 1) | KILLED |

The (d) mutant is specifically the w1 survivor recorded in `.ufo/waves/round-50/w1/MutGateV3.md` as “registry allows all RULES instead of WAIVABLE_RULES.” It accepts R5/R6 in `load_registry`; the existing serial-rule rejection remains. The frozen C2 counter exercises no waiver registry/marker path, and its selftest does not distinguish the registry predicate, so it still reports TARGET_MET. This is a coverage finding, not a contract change.

Synthetic leak proof for (e): scratch-only fixture content `Synthetic serial 481QZRTM9027 only.`; mutant output was `FINDING file=receipts/synthetic.txt rule=R5_SERIAL_PROSE count=1 detail=tokens=1 shapes=481QZRTM9027`, followed by `SYNTHETIC_RAW_VALUE_LEAK_CONFIRMED`. No real serial/session data used. Receipt: `receipts/leak-output.txt`.

Receipts: `receipts/receipts-control-50501.txt`, `receipts/receipts-mutA-50511.txt`, `receipts/receipts-mutB-50512.txt`, `receipts/receipts-mutC-50513.txt`, `receipts/receipts-mutD-50514.txt`, `receipts/receipts-mutE-50515.txt`, `receipts/leak-output.txt`.

Restoration: after all probes, `lane/quality/check-session-material.py` in the scratch clone was restored from `b4a79843`; its SHA-256 and `git show b4a79843:quality/check-session-material.py` SHA-256 both equal `ffdc9d62c387050e016cf9d0eaacbf87f37d6647021cbd2c492eb6328dddbb61`. Pristine baseline selftest was 94/94. No tools installed.
