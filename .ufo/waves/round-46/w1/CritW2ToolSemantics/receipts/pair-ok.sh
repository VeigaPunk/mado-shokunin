echo "### ATTACK (false OK): bracket v2 mode + legacy preferred/auto/auto; live = v2 mode"
python3 -I tool.py --monitors one.json --config ok.conf; echo "rc=$?"
