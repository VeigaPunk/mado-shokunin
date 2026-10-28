import subprocess, sys
print("note: extra stdout line")
sys.exit(subprocess.run([sys.executable, "-I", "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-55/w1/R55ExecC1Harness/tests/counter_ref.py", *sys.argv[1:]]).returncode)
