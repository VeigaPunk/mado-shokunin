import importlib.util, json, pathlib, sys
sys.dont_write_bytecode=True
root=pathlib.Path('/home/vgpnk/Projects/shokunin/mado-shokunin')
seat=root/'.ufo/waves/round-67/w1/R67RevRegister'
spec=importlib.util.spec_from_file_location('candidate',sys.argv[1])
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
for c in json.loads((seat/'forgeries.json').read_text()):
    if len(sys.argv)>2 and c['name']!=sys.argv[2]:continue
    reasons,summary,*_=m.assess(c['province'],c['objects'].get)
    print(c['name'], 'reject' if reasons else 'accept',summary,reasons)
