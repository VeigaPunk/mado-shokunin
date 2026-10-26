#!/bin/sh
# Verifies every "file:line<TAB>quote" row of quotes.txt: the row is in the receipt, and the source line named by the
# locator contains the quote verbatim (locators are grep -n results, never typed by hand).
set -u
L=/home/vgpnk/Projects/shokunin/mado-shokunin
cd "$(dirname "$0")" || exit 2
rc=0
tab=$(printf '\t')
while IFS="$tab" read -r loc q; do
    [ -z "${loc:-}" ] && continue
    f=${loc%:*}; n=${loc##*:}
    if ! grep -qF -- "$loc" quotes.txt; then
        echo "MISSING-RECEIPT $loc"; rc=1; continue
    fi
    if sed -n "${n}p" "$L/$f" | grep -qF -- "$q"; then
        echo "OK $loc :: $q"
    else
        echo "MISMATCH $loc :: $q"; rc=1
    fi
done < quotes.txt
exit $rc
