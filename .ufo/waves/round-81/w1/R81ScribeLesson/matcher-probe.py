import importlib.util, json
p="/home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c2-r81-runbook.py"
spec=importlib.util.spec_from_file_location("c2","/home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c2-r81-runbook.py")
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
AC={"min_lines":2,"prefix":" \u2192 "}
print("action bare-& :", m.special_matches("action_column",AC,0," \u2192 Pop window out (float & pin)\n \u2192 Action 1\n"))
print("action &amp;   :", m.special_matches("action_column",AC,0," \u2192 Terminal &amp;&amp; log\n \u2192 Action 1\n"))
print("pid '1720\\n'  :", m.special_matches("pid_state",{},0,"1720\n"))
print("pid ' 1720\\n' :", m.special_matches("pid_state",{},0," 1720\n"))
print("pid '1720\\n1721\\n':", m.special_matches("pid_state",{},0,"1720\n1721\n"))
print("pid '' rc1   :", m.special_matches("pid_state",{},1,""))
# what a .strip() variant would do with the frozen negative
def strip_variant(rc, stdout):
    t=stdout.strip()
    if rc==0:
        import re
        return bool(t) and all(re.fullmatch(r"[0-9]+",l) for l in t.splitlines()) and all(0<int(l)<=4194304 for l in t.splitlines())
    return rc==1 and t==""
print("STRIP variant on negative ' 1720\\n':", strip_variant(0," 1720\n"))
print("frozen negative would then MATCH -> case incorrect:", strip_variant(0," 1720\n") is True)
