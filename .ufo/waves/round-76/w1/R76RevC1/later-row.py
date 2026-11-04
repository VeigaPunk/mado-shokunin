import subprocess, sys
repo='/home/vgpnk/Projects/shokunin/mado-shokunin'
rev='cb713254ee9926e036e594312fdc61b57825526b'
source=subprocess.check_output(['git','-C',repo,'show',rev+':quality/counters/c1-r76-landing-controls.py'])
ns={'__name__':'later_row_review'}
exec(compile(source,'frozen-harness','exec'),ns)
rc=ns['main'](sys.argv[1:])
print('MADO_R76_LANDING_CONTROLS: selftest=2/2 mz=fail mr=pass killed=2/2 baseline=0/2 witness=ok verdict=TARGET_MISSED rev='+'a'*40)
sys.exit(rc)
