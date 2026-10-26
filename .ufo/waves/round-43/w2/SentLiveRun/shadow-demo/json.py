# shadow module used only inside the seat scratch: proves which invocation is import-isolated
import sys
open("/fast/scratch/hyaku/mado-r43/SentLiveRun/shadow/MARKER-written", "w").write("shadow json executed\n")
sys.stderr.write("SHADOW_JSON_EXECUTED\n")
