import re
L=open('/usr/bin/xdg-terminal-exec').read().split('\n')
A=[(23,'set -euf'),(32,'XTE__SELF_NAME'),(61,'XTE_DEBUG'),(148,'XDG_CONFIG_HOME'),(150,'LOWERCASE'),(157,'XDG_DATA_DIRS'),(166,'XDG_DATA_HOME'),(168,'XTE__APPLICATIONS_DIRS'),(172,'XDG_CACHE_HOME'),
(185,'LC_ALL=C gen_hash'),(195,'XDG_CURRENT_DESKTOP'),(200,'ls -LRl'),(201,'md5sum'),(221,'-f "${XTE__CACHE_FILE}"'),(296,'return 1'),(303,'mkdir'),(357,'LC_ALL=C read_config_paths'),
(361,'XTE__CONFIGS'),(365,'-f "$xte__config_path"'),(367,'while read -r'),(374,'/enable_cache'),(388,'/execarg_compat'),(402,'/execarg_default'),(425,'a-zA-Z0-9_'),(436,"IFS=':' read"),(442,'XTE__ENTRY_IDS='),
(446,'list_contains'),(467,'Discarded'),(552,'unsupported'),(782,'alias'),(785,'list_contains'),(790,'XTE__FALLBACK_ENTRY_IDS='),(795,'find -L'),(797,'awk'),(773,'-path'),(816,'Categories'),(829,'Actions'),
(846,'OnlyShowIn'),(865,'NotShowIn'),(885,'TerminalArgExec'),(893,'ExecArg'),(895,'XTE__EXECARG_COMPAT'),(933,'TryExec'),(938,'Hidden'),(947,"'Exec'"),(958,'de_tokenize_exec'),(960,'de_strip_fields'),
(972,'LC_ALL'),(989,'Desktop Entry'),(997,'check_entry_key'),(999,'reset_keys'),(1005,'Desktop Action'),(1014,"'['*"),(1060,'fallback_start'),(1081,'alias'),(1083,'eval'),(1085,'unalias'),(1086,'read_entry_path'),
(1088,'EXEC_USEP'),(1090,'IS_TERMINAL'),(1094,'check_bool'),(1099,'continue'),(1103,'XTE__ENTRY_PATH'),(1109,'No valid'),(1138,'exit 0'),(1144,'tr '),(1147,'XTE_EXECARG_COMPAT'),(1164,'reset_keys'),(1172,'XTE_CACHE_ENABLED'),
(1179,'read_cache'),(1186,'duplicates removed'),(1198,'read_config_paths'),(1200,'find_entry_paths'),(1208,'exit 1'),(1226,'--)'),(1231,'-e |'),(1236,'--app-id'),(1296,'--print-cmd=*'),(1305,'--print-delimiter'),(1313,'[!-]*'),(1317,'-*)'),
(1331,'printf'),(1342,'/./'),(1362,'shcat'),(1376,'exit 0'),(1380,'XTE__PRINT_DELIMITER'),(1383,'exit 0'),(1388,'XTE__EXECARG'),(1393,'XTE__HOLDARG'),(1400,'XTE__DIRARG'),(1415,'XTE__TITLEARG'),(1430,'XTE__APPIDARG'),
(1450,'set --'),(1455,'XTE__CACHE_USED'),(1457,'save_cache'),(1460,'TEST_MODE'),(1464,'exit 0'),(1480,'XTE__PRINT_CMD_DELIMITER'),(1486,'XTE__PRINT_CMD_DELIMITER'),(1490,'exit 0'),(1496,'cd '),(1499,'exec'),(738,'XTE__EXEC_USEP=')]
bad=0
for n,s in A:
    ok = s in L[n-1]
    if not ok: bad+=1
    print(('OK  ' if ok else 'FAIL'),n,s,'|',L[n-1].strip()[:70])
print('SUMMARY',len(A)-bad,'/',len(A))
