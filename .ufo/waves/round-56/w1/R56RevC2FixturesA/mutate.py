import json, os, subprocess
EXP = '/fast/scratch/hyaku/mado-r56/R56RevC2FixturesA/export/.ufo/waves/round-56/fixtures/c2'
BASE = open('/fast/scratch/hyaku/mado-r56/R56RevC2FixturesA/interp.py').read()
MUT = {
 'M1_case_insensitive_sort': ("matches = sorted(glob.glob(value))", "matches = sorted(glob.glob(value), key=str.lower)"),
 'M2_no_double_hash_check': ("        if '##' in rhs:\n            st['unsupported'] += 1\n            continue\n", ""),
 'M3_dotdot_from_curdir': ("parent = curdir[:curdir.rfind('/')] if '/' in curdir else curdir", "parent = curdir"),
 'M4_no_canonical_watch': ("            if os.path.islink(p):", "            if False:"),
 'M5_skip_counts_error': ("            st['events'].append(f'MADO_WATCH: SKIP via={via} path={display(v)} reason=directory')",
                          "            st['events'].append(f'MADO_WATCH: SKIP via={via} path={display(v)} reason=directory'); st['errors'] += 1"),
 'M6_dotfiles_included': ("matches = sorted(glob.glob(value))", "matches = sorted(glob.glob(value, include_hidden=True)) if False else sorted(set(glob.glob(value)) | set(p for p in glob.glob(os.path.dirname(value)+'/.*') if glob.fnmatch.fnmatch(os.path.basename(p), os.path.basename(value))))"),
 'M7_first_value_wins': ("        st['last'] = v", "        st['last'] = v if st['last'] is None else st['last']"),
 'M8_dir_watch_mask_file': ("                watches.append(('primary', p, 'dir', MASK_DIR, via))", "                watches.append(('primary', p, 'dir', MASK_FILE, via))"),
 'M9_no_unsupported_for_dollar_lhs': ("        if lhs.startswith('$'):\n            continue", "        if lhs.startswith('$'):\n            st['unsupported'] += 1\n            continue"),
 'M10_source_in_category_processed': ("        if lhs == 'source':\n            if stack:\n                st['unsupported'] += 1\n                continue", "        if lhs == 'source':\n            if stack:\n                pass\n            "),
}
for name, (a, b) in MUT.items():
    assert BASE.count(a) == 1, (name, BASE.count(a))
    code = BASE.replace(a, b)
    path = f'/fast/scratch/hyaku/mado-r56/R56RevC2FixturesA/work/{name}.py'
    open(path, 'w').write(code)
    failing = []
    for n in range(1, 10):
        fx = f'{EXP}/F{n:02d}'
        args = [x.replace('{FX}', fx) for x in json.load(open(f'{fx}/args.json'))]
        p = subprocess.run(['python3', '-I', path] + args, cwd='/fast/scratch/hyaku/mado-r56/R56RevC2FixturesA/work', env={'PATH': '/usr/bin:/bin', 'LC_ALL': 'C'}, capture_output=True)
        if p.stdout != open(f'{fx}/expected.out', 'rb').read():
            failing.append(f'F{n:02d}')
    print(name, 'killed_by=', failing if failing else 'NONE (fixtures blind to this mutant)')
