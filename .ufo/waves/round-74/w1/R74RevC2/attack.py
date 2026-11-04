import argparse
import ast
import hashlib
import json
from pathlib import Path
import runpy
import shutil
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--scratch-root', required=True)
args = parser.parse_args()
scratch = Path(args.scratch_root).resolve()
assert str(scratch) == '/fast/scratch/hyaku/mado-r74/R74RevC2'
assert scratch.is_dir()
owned = Path(__file__).resolve().parent
repo = owned.parents[4]
candidate = repo / 'quality/counters/c2-r74-shapes.py'
module = runpy.run_path(str(candidate))
held_source = subprocess.run(
    ['git', 'show', 'bd5a971532f37df85a78f6f566dd1e649b79de11:quality/counters/c2-r73-shapes.py'],
    cwd=repo, capture_output=True, check=True).stdout
held = {'__name__': 'held_review'}
exec(compile(held_source, '<held-round73>', 'exec'), held)
rows = []
for fixture in sorted(owned.glob('[0-9][0-9]_*.py')):
    source = fixture.read_text()
    tree = ast.parse(source)
    dead = module['false_guarded_lines'](tree)
    consts = module['const_key_names'](tree)
    rows.append({
        'fixture': fixture.name,
        'classify': module['classify'](source),
        'held_classify': held['classify'](source),
        'twohop_guard': module['twohop_guard'](tree, dead, consts),
        'environ_alias_guard': module['environ_alias_guard'](tree, dead, consts),
        'object_alias_map': module['object_alias_map'](tree, dead),
        'environ_alias_names': module['environ_alias_names'](tree, dead),
    })
receipt = {'candidate_sha256': hashlib.sha256(candidate.read_bytes()).hexdigest(),
           'held_sha256': hashlib.sha256(held_source).hexdigest(), 'fixtures': rows}
output = json.dumps(receipt, indent=2) + '\n'
(scratch / 'classification.json').write_text(output)
shutil.copyfile(scratch / 'classification.json', owned / 'classification.json')
print(output, end='')
