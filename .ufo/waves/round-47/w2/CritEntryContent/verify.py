#!/usr/bin/env python3
"""CritEntryContent verification receipt generator (round 47 w2).
Greps the pinned resolver/README pins, asserts locators, and replays the scratch experiments.
Output: verification-receipt.txt in the seat dir.
"""
import subprocess, hashlib, os, sys, tempfile, shutil

SEAT = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-47/w2/CritEntryContent"
PIN  = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-47/fetch/xdg-terminal-exec"
RM   = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-47/w1/ScrEntry/README-v0.14.3.md"
OUT = os.path.join(SEAT, "verification-receipt.txt")

lines = []
def log(s): lines.append(str(s))

def grep1(path, needle):
    p = subprocess.run(["grep", "-n", "-F", "--", needle, path], capture_output=True, text=True)
    if p.returncode != 0: return None
    return int(p.stdout.split(":", 1)[0])

LOCS = [
 (145,"IFS=':'",PIN),(1144,"XTE__LOWERCASE_XDG_CURRENT_DESKTOP=$(printf",PIN),
 (148,"for xte__dir in ${XDG_CONFIG_HOME:-",PIN),(151,"${xte__dir%/}/${xte__desktop}-xdg-terminals.list",PIN),
 (153,"${xte__dir%/}/xdg-terminals.list",PIN),(157,"for xte__dir in ${XDG_DATA_DIRS:-",PIN),
 (160,"xdg-terminal-exec/${xte__desktop}-xdg-terminals.list",PIN),(162,"xdg-terminal-exec/xdg-terminals.list",PIN),
 (166,"for xte__dir in ${XDG_DATA_HOME:-",PIN),(168,"XTE__APPLICATIONS_DIRS=${xte__dir%/}/applications/",PIN),
 (172,"XDG_CACHE_HOME=${XDG_CACHE_HOME:-",PIN),(173,"XTE__CACHE_FILE=${XDG_CACHE_HOME}/xdg-terminal-exec",PIN),
 (353,"All config files are read immediatelly",PIN),(357,"LC_ALL=C read_config_paths \"$@\"",PIN),
 (365,"[ -f \"$xte__config_path\" ] || continue",PIN),(374,"/enable_cache)",PIN),(380,"/disable_cache)",PIN),
 (388,"/execarg_compat)",PIN),(394,"/execarg_strict)",PIN),(402,"/execarg_default:*:*)",PIN),
 (378,"XTE__CACHE_CONFIGURED=1",PIN),(392,"XTE__EXECARG_COMPAT_CONFIGURED=1",PIN),
 (425,"[a-zA-Z0-9_]* | [+-][a-zA-Z0-9_]*)",PIN),
 (436,"IFS=':' read -r xte__entry_id xte__action_id",PIN),
 (439,"if validate_entry_id \"${xte__entry_id}\" && validate_action_id",PIN),
 (442,"XTE__ENTRY_IDS=${XTE__ENTRY_IDS:+",PIN),(462,"XTE__EXCLUDED_ENTRY_IDS=${XTE__EXCLUDED_ENTRY_IDS:+",PIN),
 (467,"Discarded possibly misspelled entry",PIN),(754,"find_entry_paths() {",PIN),
 (762,"set -- \"$@\" \"$xte__directory\".",PIN),(766,"set -- \"$@\" -type f",PIN),
 (773,"-path \"$xte__directory\"'./[a-zA-Z0-9_]*.desktop'",PIN),
 (779,"while IFS= read -r xte__entry_path && IFS= read -r xte__entry_id; do",PIN),
 (780,"Entries are checked in ascending order of preference",PIN),
 (782,"alias \"$xte__entry_id\"=\"xte__entry_path='",PIN),
 (785,"list_contains \"$XTE__EXCLUDED_ENTRY_IDS\"",PIN),(790,"XTE__FALLBACK_ENTRY_IDS=${xte__entry_id}",PIN),
 (795,"LC_ALL=C find -L \"$@\"",PIN),(797,"awk '{ print; sub(\".*/[.]/\", \"\"); gsub(\"/\", \"-\"); print }'",PIN),
 (802,"check_entry_key() {",PIN),(814,"Order of checks is important",PIN),(816,"'Categories'*=*)",PIN),
 (829,"'Actions'*=*)",PIN),(846,"'OnlyShowIn'*=*)",PIN),(865,"'NotShowIn'*=*)",PIN),
 (885,"'X-TerminalArgExec'*=* | 'TerminalArgExec'*=*)",PIN),(893,"'X-ExecArg'*=* | 'ExecArg'*=*)",PIN),
 (905,"'X-TerminalArgAppId'*=* | 'TerminalArgAppId'*=*)",PIN),(912,"'X-TerminalArgTitle'*=* | 'TerminalArgTitle'*=*)",PIN),
 (919,"'X-TerminalArgDir'*=* | 'TerminalArgDir'*=*)",PIN),(926,"'X-TerminalArgHold'*=* | 'TerminalArgHold'*=*)",PIN),
 (933,"'TryExec'*=*)",PIN),(938,"'Hidden'*=*)",PIN),(947,"'Exec'*=*)",PIN),
 (955,"# Escape sequences of DE string value (sets $XTE__EXPANDED_STR)",PIN),
 (958,"de_tokenize_exec \"$XTE__EXPANDED_STR\"",PIN),(959,"# Expand % fields",PIN),
 (962,"XTE__EXEC0=${XTE__EXEC_USEP%%",PIN),
 (964,"command -v \"$XTE__EXEC0\" > /dev/null || return 1",PIN),(970,"read_entry_path() {",PIN),
 (985,"while IFS=$XTE__OIFS read -r xte__line; do",PIN),
 (989,"'[Desktop Entry]'*) [ -z \"$xte__entry_action\" ] && xte__read_exec=true",PIN),
 (991,"[a-zA-Z0-9-]*)",PIN),(993,"xte__value=${xte__line#*=}",PIN),
 (995,"xte__value=${xte__value#\"${xte__value%%[! ]*}\"}",PIN),
 (997,"check_entry_key \"$xte__line\" \"$xte__value\"",PIN),(998,"# Reset values that might have been set",PIN),
 (1001,"debug \"entry discarded\"",PIN),
 (1005,"\"[Desktop Action ${xte__entry_action}]\"*",PIN),
 (1014,"'['*) [ \"$xte__read_exec\" = \"true\" ] && break",PIN),
 (1060,"for xte__entry_id in ${XTE__ENTRY_IDS}",PIN),
 (1065,"xte__entry_action=${xte__entry_id#*:}",PIN),
 (1066,"xte__entry_id=${xte__entry_id%:*}",PIN),
 (1071,"'//fallback_start//')",PIN),(1072,"xte__de_checks=true",PIN),
 (1081,"alias \"$xte__entry_id\" > /dev/null 2>&1 || continue",PIN),(1083,"eval \"$xte__entry_id\"",PIN),
 (1085,"unalias \"$xte__entry_id\"",PIN),
 (1086,"read_entry_path \"$xte__entry_path\" \"$xte__entry_action\" \"$xte__de_checks\" || continue",PIN),
 (1088,"[ -z \"${XTE__EXEC_USEP}\" ] && continue",PIN),
 (1090,"[ -z \"${XTE__IS_TERMINAL}\" ] && continue",PIN),
 (1092,"if [ \"$XTE__EXECARG_DEFINED\" != \"true\" ]; then",PIN),
 (1095,"get_default_execarg \"$xte__entry_id\"",PIN),
 (1103,"XTE__ENTRY_PATH=$xte__entry_path",PIN),(1104,"XTE__ENTRY_ID=$xte__entry_id",PIN),
 (1105,"XTE__ENTRY_ACTION=$xte__entry_action",PIN),
 (1109,"IFS=':' error \"No valid terminal entry was found in:\"",PIN),
 (1113,"get_default_execarg() {",PIN),(1128,"XTE__DEFAULT_EXECARG='-e'",PIN),
 (1147,"XTE__EXECARG_COMPAT=${XTE_EXECARG_COMPAT-true}",PIN),
 (1172,"XTE__CACHE_ENABLED=${XTE_CACHE_ENABLED-true}",PIN),
 (1179,"if check_bool \"${XTE__CACHE_ENABLED}\" && read_cache; then",PIN),
 (1222,"XTE__PRINT_DELIMITER='\\n'",PIN),(1223,"XTE__PRINT_CMD_DELIMITER='\\n'",PIN),
 (1227,"debug \"found explicit end of options $1\"",PIN),(1231,"-e | \"$XTE__EXECARG\")",PIN),
 (1236,"--app-id=*)",PIN),(1244,"--title=*)",PIN),(1252,"--dir=*)",PIN),(1260,"--hold)",PIN),(1266,"--test)",PIN),
 (1272,"--print-path)",PIN),(1278,"--print-id)",PIN),(1284,"--print-content)",PIN),(1290,"--print-cmd)",PIN),
 (1296,"--print-cmd=*)",PIN),(1305,"--print-delimiter=*)",PIN),(1313,"[!-]*)",PIN),(1317,"-*)",PIN),
 (1327,"case \" $XTE__PRINT_DATA \" in",PIN),
 (1331,"printf '%s' \"${XTE__ENTRY_ID}${XTE__ENTRY_ACTION:+:}${XTE__ENTRY_ACTION}\"",PIN),
 (1342,"XTE__ENTRY_PATH=${XTE__ENTRY_PATH%%/./*}/${XTE__ENTRY_PATH##*/./}",PIN),
 (1349,"printf '%s' \"${XTE__ENTRY_PATH}${XTE__ENTRY_ACTION:+:}${XTE__ENTRY_ACTION}\"",PIN),
 (1362,"shcat < \"${XTE__ENTRY_PATH}\"",PIN),(1375,"# content already has newline at the end, just exit",PIN),
 (1380,"case \"$XTE__PRINT_DELIMITER\" in",PIN),(1381,"'\\n') printf '%b' '\\n'",PIN),
 (1388,"if [ \"$#\" -gt 0 ] && [ -n \"$XTE__EXECARG\" ]; then",PIN),
 (1389,"set -- \"$XTE__EXECARG\" \"$@\"",PIN),
 (1396,"elif [ -z \"$XTE__HOLDARG\" ] && check_bool \"$XTE__HOLD\"; then",PIN),
 (1403,"set -- \"${XTE__DIRARG}${XTE__DIRVAL}\" \"$@\"",PIN),
 (1407,"set -- \"${XTE__DIRARG}\" \"${XTE__DIRVAL}\" \"$@\"",PIN),
 (1422,"set -- \"${XTE__TITLEARG}\" \"${XTE__TITLEVAL}\" \"$@\"",PIN),
 (1426,"elif [ -z \"$XTE__TITLEARG\" ]",PIN),
 (1437,"set -- \"${XTE__APPIDARG}\" \"${XTE__APPIDVAL}\" \"$@\"",PIN),
 (1441,"elif [ -z \"$XTE__APPIDARG\" ]",PIN),
 (1450,"set -- $XTE__EXEC_USEP \"$@\"",PIN),(1457,"save_cache \"$1\" &",PIN),
 (1480,"printf '%b' \"${XTE__PRINT_CMD_DELIMITER:-\\n}\"",PIN),
 (1486,"if [ \"${XTE__PRINT_CMD_DELIMITER}\" = '\\n' ]",PIN),
 (1496,"cd \"$XTE__DIRVAL\"",PIN),(1499,"exec \"$@\"",PIN),
 (194,"echo 4",PIN),(195,"echo \"${XDG_CURRENT_DESKTOP-}\"",PIN),(200,"LANG=C ls -LRl ${xte__hash_paths}",PIN),
 (227,"xte__line_num=$((xte__line_num + 1))",PIN),
 (274,"if [ \"$XTE__HASH\" = \"$xte__cached_hash\" ] && command -v \"$xte__cached_cmd\" > /dev/null; then",PIN),
 (303,"[ ! -d \"${XDG_CACHE_HOME}\" ] && mkdir -p \"${XDG_CACHE_HOME}\"",PIN),
 (312,"case \"${XTE__HASH}${1}${XTE__EXECARG}",PIN),(314,"error \"One or more of terminal's arguments contains a newline, removing",PIN),
 (320,"umask 0077",PIN),(321,"printf '%s\\n' \\",PIN),
 (7,"while this spec is in proposed state",RM),(8,"compatibility is maintained as best effort",RM),
 (179,"the order in which found entries under the same base directory are checked",RM),
 (180,"in is undefined",RM),(218,"The resulting command is executed without forking.",RM),
 (300,"Valid cache bypasses",RM),(301,"reading of any other file.",RM),
]

log("=" * 78)
log("CRITENTRYCONTENT VERIFICATION RECEIPT — round 47 w2")
log("=" * 78)
log("pin: %s" % PIN)
log("sha256(pin) = %s" % hashlib.sha256(open(PIN,"rb").read()).hexdigest())
host = "/usr/bin/xdg-terminal-exec"
if os.path.exists(host):
    log("sha256(host) = %s" % hashlib.sha256(open(host,"rb").read()).hexdigest())
    log("cmp pin host = %s" % ("identical" if open(PIN,"rb").read() == open(host,"rb").read() else "DIFFERENT"))
else:
    log("host /usr/bin/xdg-terminal-exec ABSENT")
log("wc -l pin = %s" % subprocess.run(["wc","-l"], stdin=open(PIN), capture_output=True, text=True).stdout.split()[0])
log("prototype defs col0 = %s" % subprocess.run(["grep","-c","^[a-zA-Z_][a-zA-Z0-9_]*()",PIN], capture_output=True, text=True).stdout.strip())
log("prototype defs any-indent = %s" % subprocess.run(["grep","-cE","^\\s*[a-zA-Z_][a-zA-Z0-9_]*()",PIN], capture_output=True, text=True).stdout.strip())
log("directive arms = %s" % subprocess.run(["grep","-c","/enable_cache)",PIN], capture_output=True, text=True).stdout.strip())

log("")
log("LOCATOR ASSERTIONS (grep -n -F --, expected line vs found)")
bad = 0
for want, needle, path in LOCS:
    got = grep1(path, needle)
    ok = got == want
    if not ok: bad += 1
    log("%s %-6s line=%s needle=%r" % ("PASS" if ok else "FAIL", os.path.basename(path), got, needle[:70]))
log("locator FAILs = %d" % bad)

# append experiment outputs
for ex in ("experiments.sh", "experiments2.sh"):
    log("")
    log("-- %s --" % ex)
    p = subprocess.run(["/bin/sh", os.path.join(SEAT, ex)], capture_output=True, text=True)
    log(p.stdout)
    if p.stderr.strip(): log("STDERR: " + p.stderr[:2000])

with open(OUT, "w") as fh:
    fh.write("\n".join(lines) + "\n")
print("receipt written: %s (%d lines)" % (OUT, len(lines)))
