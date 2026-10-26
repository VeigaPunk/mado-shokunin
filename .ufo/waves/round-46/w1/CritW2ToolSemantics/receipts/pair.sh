echo "### CONTROL: same rule, keyed monitorv2 spelling"
python3 -I ../mado-monitors.py --monitors one.json --config ctl-keyed.conf; echo "rc=$?"; echo
echo "### ATTACK: same rule, bracket monitorv2 spelling"
python3 -I ../mado-monitors.py --monitors one.json --config brk.conf; echo "rc=$?"
