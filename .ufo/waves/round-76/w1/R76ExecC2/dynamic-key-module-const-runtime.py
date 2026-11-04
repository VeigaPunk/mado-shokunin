import subprocess, sys
KEY = 'GIT_NO_REPLACE_OBJECTS'
def trace(frame, event, arg):
    if frame.f_code.co_filename == '<fixture>' and event == 'line' and frame.f_code.co_name == 'run':
        if frame.f_lineno == LAUNCH_LINE:
            print('AT_LAUNCH key_present=' + str(KEY in frame.f_locals['env']), flush=True)
    if frame.f_code is subprocess.run.__code__ and event == 'return' and arg is not None:
        print('GIT_CHILD_RC=' + str(arg.returncode), flush=True)
    return trace
LAUNCH_LINE = 5
SOURCE = 'KEYNAME = "GIT_NO_REPLACE_OBJECTS"\ndef run(repo):\n    env = {"PATH": "/usr/bin", "GIT_NO_REPLACE_OBJECTS": "1"}\n    del env[KEYNAME]\n    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=env)\n'
exec(compile(SOURCE, '<fixture>', 'exec'))
sys.settrace(trace)
run('/fast/scratch/hyaku/mado-r76/R76ExecC2/dynamic-key-module-const.CNqo3T')
sys.settrace(None)
