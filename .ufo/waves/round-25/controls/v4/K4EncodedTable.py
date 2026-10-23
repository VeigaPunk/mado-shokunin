#!/usr/bin/env python3
"""K4EncodedTable: encoded live-table cache plus file-level easy-grammar delta.

This control deliberately skips parsing matching snapshot files. Only changed,
new, or newly reachable files go through its easy parser. It is not a complete
Hyprland resolver: modifier aliases/separators, keycode binds, submaps, key
chords, and the complete rejection grammar are not implemented. Cached rows are
live observations, not values reconstructed from their config lines.
"""
import argparse
import base64
import glob
import hashlib
import json
import os
import re
import sys
import zlib

DATA = 'eNrtfet2G8fV5av04orz2RND6rp2ldaaH7Z8ib/YkZakxM4Xe7zqSsIE0Ai6IYq5zDPM28xa83NeaF5hdgEk1UWCsroBymLHVuwIJPr06V2nztm7bv2Po9n0ZTh69Nd/HM1qdxr80aN2tQ4fH83rdYOfRzNr8GkVZsFkn5fBtJffndWL46er0DRXv1/Uix9dvWjW8+ni+OqnZt3WO358YpoffWjcarpsp/XitQd+bprTo0flx0fN2s7N8ujR0dHl339cL+D4qjEz/HRjCL86Def49N0XSn6y9tP6mZk24c/1bD2/+KWrfdjYc6Z1Jz+a2ezKicyBo+1FxXqJ6/Ct+uzH6WK5bn90ZtmuV69x8NNmmUyFFS4Kr4JL31/h0Y7quVm5k/NJc2bO68ZP3GwaFm0xmdTrFpYmL7d3WCUXj/718Rjh/7o+C6t94Pf12eKuG2CWnBxpA3yzbvsif3HJnUI+xz0mbX18PBtr5H8zdQOxL+ZTt6qXJ/Vi/2YwyZXJ5upJwnx8YH9TLz5dTY9P2gXc+tOyJ96vLz1EordX1ibpyzNzXvxOfDByzD/bZuiBqB8kv+/AXXwweb9xJ79krM/Nq+l8Pb8L4ElZfjBy5PeLePh6Z9iPMNf8wfo9Yv4P4dzWZuULe1eJ/vTyDjA7bvAHhP0u+A+d8a8aYGN4aBNcfHw/2+Dr9LBPFk9iHIy/caezZKVw524W7gT/reXxNcCLeu1Olsa/2MqVfi2wvahoL2zsDfxWM02u7I0X7id9k83nC2PvEOqiXowZ7d655bNpc8d4w6X3uqKqX3BQsliugps2dz5Q8zsy0jY4yMjku2qFyQhb4YADNwdrhl0DOO+7qFK//ADOXeJP9hjIeX/L7iYF/TG8ansCny4p2hXY/OFTToI7rFw7KxbJsZGC/tSsm74Z//KaOwM8/W2y3NxlrLDjCfuivr3kV9CHg74KL/uCjkumePa7TzLLizu95+BL/g6nXp+fTfGFYjNrV2wp4IGmAC/4ZLO5QQb5haF7jfnjnjj/6dJS4eplryTThIVvTupV67ZNs4H68YtnX39cfLVowqr9uDCuhfWz6QLUaHRI/3kw0kvT9FtXsBPq57//6osX/yZYfzc8qvvljTcE9Xf3DGN1x/H8eDZdboe752ZhjgHfvvl5ZtYLdzI5M7PTsCom88Jd3mJ0Af1tb7DrJhQXkdcD59PpbLaN2iu033csCe2J5Weff/35i88HAYrfX4Da7B29J+fL1cws/GRrEEQPd5gkD8YWvP85bOZni0vRLGfTXjkZPBmcbd4cX0G+HR/fGhobuE/7ypQmrH09IDUsNxfem7TQG8gXe0VpnNWmhX8P2+ksudkD2G10XhoYL8Bf9AT4izWyLX4QQq9VDxGXvb5qA2U5OvLVF8sX01nwRdwX0aY17WtmUBb0fQe2ou8iSM+mvj3ZM0bJ6Pr7k76VqV5eZlPU7+LDTUYsflssp4uPDs62lvVydIB/PbCC1atTwOdCsWVOB8T60vJka3nXvoVRAP/5F33Zwxe1WzdFvShQ+dsBbGxevwwx2bhCf3y64dlXX/5+MK6b+dCDALsaHbB/ejoUVWMBz0FQXY8O1c+efPvHobjaACAPguv4xr66mJK3nwpq605lI31AvbpsxOQsA5UMA5XuByodN6h0GKhsP1DZuEFlw0Dl+4HKxw0qHwaq2A9UMW5QxTBQ5X6gynGDKoeBWu0HajVuUKthoKr9QFXjBlUNA1XvB6oeN6h6IPkv92T/7//8gbhjTfXNa9m/h7BKarWt76O8Encsr27Flx4CXzpufOke+LJD4MvGjS/bA19+CHz5uPHle+ArDoGvGDe+Yg985SHwlePGV+6Bb3UIfKtx41vtga86BL5q3PiqPfDVh8BXjxtfvY++KA8iMN57BVexd6jgmuksLNrZ+eGk3Nbi/RF0+8FNDgE3PRzcdNxw00PAzQ4HNxs33OwQcPPDwc3HDTc/BNzicHCLccMtDgG3PBzcctxwy0PAXR0O7mrccFeHgFsdDm41brjVIeDWh4NbjxtufRCZUx5Q55Sjm3B9PmwTAX6UvtjzNMPLjZnBTc3spmzvGB3bPqO+MF8bIBkG95uD+aIZHt0f1Pvv8fzk0yHHhmWROXwdQfjd+Ca6+yN6dU7SoVCdkNFt7+yP6hf1ah5Wh8J05wlTY6ATA3ZqbTPvFX1A8t1s2ZrXi2lbr/qmX7derZB0r+y1dcfQ/djH1Rv0Ifu4bqK+3dB1Z7CvRgd7711eNzFfL+8O8PXoAB+wAewm5JtTYe8MdD86AjIgoz8/M8sOl25Pwial9zr3CyZe79a7J/tvxTvI2zuw3STuPcFdjQ7c3tm5i2y/F/HswHM9OjwHJN8uon3frbMD0/c+t74LFXKxn3mxkc29tzNvXoSz2B7ufT9OQdLvDtPllXA+AK7J2K/x+iy8DGZ2cU7n1eEzC1SuXgnWrvBYWyNtfXHtr9H7K8JDTqfcN+kOkA6bAySuK4X3f6ySsF8g9x4K3sm4j5Sgb/PWsVdLs/CXOaGvAsODT/8erp1VOyFlWZTjRvZtDus4Qbo8PSiy9wNYccchmwPbT4XthLUsUsiOG1fSNxX01WK3IHsfgO2bCTbO/+j7v3fquVvVs9c87GrEMdars3Rg+ugnNochvV4eCOf0GtkDAP1G2rB95PuI8yNa0eELIvoNk1+8kGqDZxo0/9nXM9xrWFlvvZZy6d7AblPySN8u8uVeJ4Ufr+r1ctAR4Zsr743y7b0k6sshGeDawMK6LepYXAHVZ/IM19Zx5BAPXv5wNaGzAejy3Nq+EE8XCOQM4dnoIB6+2OEmxr1nznaDvBodyAOXNtxEuOcw5G5816PDd/BKhpsI27pt6/n+II9vCfDQxahbjKeL/mXOnZjF8ZZGXFPLcXSLcfZZmHoXCNvRLVIdSiY26ISr0Z7N8HhvOvHvBPRgSrET6d6k4j5nDfquxtf+nVMzfTdDa//m+bk3zMPPzd+StwuYyWHwJePGlwzGlx4GXzpufOlgfNlh8GXjxpcNxpcfBl8+bnz5YHzFYfAd93H78i3y7+O0CPJyAU/RONP3RZ1vftnZheHJheHJZs3lqIN6MOhXs6HNHcNfTCYgjXiS8b1z7vnTTx73fYn115sXphdmuWwO+/L10Unuvsh+Pq9/mhbLqTu9i/faN+dzW8+a0aH8uO9L2LdQFvOwWO+NcjJSXF42NmSfDJuiPhyw9+RNn31x/X1PXH+PIodCd0hkTy5Mju9IlAEV7ckWmcPBO/IlruRXSPenXp8/f/zJ076R+vy8acP8gHmg2RjMwL18sPcH27IntN99oeTT+iysnsTY+/XhuOxu8R1D8P6hb9ye1GcFLijsdOHhWXMQdCeweGXwPYd4SAw/NjO3npntjp9+FLdz4TCcjxf1PEzca0NjK2lDiMIFwW3rZWHN/hJtS28h0c6TtbGx3EEAn4T5dpl7Gn1c+ANm4tdG33uk9TtD+oBSLdkbXZ379JPHf9gjUVyuZFuZBUBchYU7P9xY5db4pGt8ck8Es/hFmuHYLJuDw5+MTkY6TrEn7A2cS+Xt4hzdv63TEIZJB4S2B2+Gi3ttbzLZ3uS+NEvfpPT4yTfffNKzST6bNvNp0xQz07TFom6ncYpL0u+GtsTcnNaunRV+a3l0OWcflPGNDOTmUCgXk0m6++iG8AdgfZVkZqh8aTrwMIBf4+Zdo5Ore41u1HRIA3y1eFmfhjvIKNON4dGtJR+C8bPQQHvfBcirreXRpZKvhqWRBEFKIvWimPpZOFT62NgaG8R/HAbxIi0Zn/VdN/7G5Pza4tgw/gzutmFgLAPPepkow3Jmzg+/OGa6aMNqYWb3ZHq2kr8Y9sV8ulrVqztZIXbZCpPtPXY1xnswk3MVDwOHwZvNcsZH9eLR11NfbBc39myZ/aE/m4RXl2Bv0W+K3/62+PkOUsc41gaJ8ZdskdsRX4xtIujps6/++KL/+TEhLJqTev9Se3HFpHltcmQHfg4HeBVcvfKHyO7bueKO0dENWg1B+XE9Q2Hbcz3k8nQ6mxUpY2wNFf/8Z/fTxIyOOw6B+vNX7cq4tmjTDsQPnzx+9lERV/W8aA6fSdItUkFN95u+//m6/7xn77URaR3eYTLIiRmhpH/6+bOvnnzWl4+nabHNt/cWm1eWRrclvG+khrZYBfjkD7A+fROwl9YmTWhHpyOfDVkkdYnI/iPYl5aQFe7B8Wn6jsF9jKdb3QW6LhkeXey+GBK77XQ+PN1uRrfPkQgWvpisC5govj/6f//r/xT45zcfetOG4nffH33wSfHB7x998E1R/N//XRQf+OKDT4sP/rL99G0Ip8UHf/7+6KPvj0bXIJ8OaRBrWuji8xT2ZrrYR6jsbJ3ffHjZGy5uNGla066bMeL/7RD8z/BEJ3vUyp9B/cL8/UG9N0PpO1/2ydpP6wKOtau01e1Ae+hMsjq+1T09sf10tg5tXbcnB8fXXloeHcZ9s8a30zg9OLxnMDq+l9v2zQzpIINpe34oUNv1tLDp4MexAfvdsIkvP3XtfisTXtav2vNlKLYDoPdkcrHvaP4Xui+PaM2qfY1u8eFy3SD66klrZqcfHQrsJt2lB9aXp5mPDOrNzO1dIz3CnPFfPZH+r7qeF9PhqSKN36dFTLjnWQLVrVdNvXr0d5j9MRqXDgn5zYeXXzoGt9jceNfXJj8V/yx++lvxHw/irDZt8buC/MdHoxMv/9V/2Vloi4TTXTYRGd9hpn2PUsGzX24R3ZeXbM1MEpyjmzx89vmLPz3rvewsrOAVrA1Fdn3WzCdmuSwmk+KVP560FwYn6Vv4oZ+u/ntXjru5f/0dd+bvwzAIfSctMV+/+iVbobCmOSkmrvj+qIUrhWlb407SRPDm4yKcFZOm+LZend6DIRTxLlrs01V91hzuECJ7YW5s2H7R902Q03Q8jlmY4z2w7XaIBZ50OlunfSGI4sn9eFVO75Xz+8BcfJhywN2BXdzzCtB/L+avqeQuYnwgrFCpq+lL04aPDgwwgvzC8ugi+Ju+p+Cvm6k7FLz1arI9Qb9ZbiZ3RhfIg9AtXvzpq0MjvBmidbOpmS9HF8J9+dznfrrPYTDXEA5ba2MDte8Ss8/qQx7UmaJ1Zv5+7rdWxwZu3/fyPZ8e76Pdb8u6/6PZ2P0NaFuX2m1/OoELp229HCFr63uU5xPbTP3ULA7fAPWF5etNcPnzEYLfdxb4xfmyXpmDaJZ2Ywp/Cwtjt2dNbTbOTOfj43XPv/7ked+jVZ+apknj081B0CbLC3Ojw7bvQpzHJ6b98umLgy1hCDZB/P3RSdsum0cPHzrYP162D1w9vwejrOyO0f5yVZ/eGdTHMH4/cO5/xkv/cxXDwpvVnWGNTw9OwnmC+6G7uNnDsxBOm4cjhL//+fhmOnsX2I8Q67/0xPov9frF2oY7Q/u8Xrewv4n0EWbwvnLnW9Sz5pPl8uCDIBfAX9rvtAB+8+As/TgF/v1oht67RPo2w5d1nRazfYMnMMehuavW+P76jb4/6jTM/OKHD443X9q0DS58CLw2j7k54GqEKerpsMZ6elK39d031fY2WUMtNz/qNtMIW6XvetDv7qxkvBprsegNcfG0bto7xhn/LusmPMR/2oT5Dx8fxekMOfHRP47whUWcHj9Mi7wemulknfLV5ofpt82JoUKmt0mSUEkTtXKh0iQaRbXV2nNiBCkJD06T0mhvZUmDMFqV0hvKGBOl8ZyyBFC9xA3/+sO/Pr52T7TMZs3qzZsK4wKpSiJjoForY2SojKeUEkeU0paz0hhuNY8mihBJ1GXlJSuJ9yI6Lt/2pg+sOX1A8FyaU1HqzAdleUVZhcdXtorKaimkFczCJarLmG4qLQDQpbWlZMEGEhgjkrOqFBXC+sKHxXo2u+7F5YH3N588iIobEnypBBOBER+CwR0NhV3qpJLUWuAelOPCCyMti1pXvvJOkVIocvXkfz0Ki3Z1fvQxkdUPH3c+qeyT7n6qyuwTyT7R7BPLPvHsk8g+yexT5kuV+VJlvqjMF5X5ojJfVOaLynxRmS8q80VlvqjMF5X5ojNfNPnhRliFxcsdjVlyhKfzsaTKRo7ArYxwCJSqchUtPWeCaioCETpWjkblKq440zISG7Tj+k0hdHwawvLmLVlFZcCtXGmjZrgxbFlDEDKVgx+eontK75gsOZNUEWEdj6xiyqqg9etb3uw56T/pKLwdMVt5ZpX3WuGBWOA+RButcdGjG1QsOiF4WaFDi0pKAMEFR66oSsXQawMnb3rMy1OCbt4V+YgrFpkwVlDrqAp43NLIaEvjCLc04HEDukRlbFC0ClFxQU2J1oyKSdHpKU29XrmUqf7nwweoSWb2cHMIw8OLJPsQD2TWs3Zn2kqR0ev6y74PiuinZl8jbjZd2tqs/L6G2unmZYkv6b6G0vqaaTsNzUBDr7tS70tndX26iCHMBl6/KcIDr92uJLrF84uIvrzQrVcrZJOHm/P2r4X4LZdu7nF5cNnPf/MNT3J7HXrTN38G2jfU9VuQbE37GsntPqFme/1/e4tbZHTlTd/spMkffnhjcrnkApTKilUyyzU8CqoENwyJhXkXhUoMRFYaFV9LgmuYp1aUpSJEGEapL6VF9pGsCoZL+rMZDkT4ZoZDTkWhxe2iEIqqihnOlRQ0oFxUFL/hvDK8KrX3vAzcRU2liiVyncb/u5/Nq8160YQd7IuVyM/caMpKpFSmIw8+VhYkiUVO0idRkbISAkWlIqx0qFjMUtQSYAd29Kb7dgIzL1tSO02NRYUoI1pBOCt9aVC9nBNGSMINmKCl2gRUGQBjldBMWjx6hZJye9m6Frjdm1YV4ItgTlYSbzkn2qE5KepytFZwjVKtJCq3CsYo7rWNtFIe5bU0ypFgbr9p3lG790yP6ZXW0uPGXlYcToigFUdDaieYEbS0noLTauYZS1UT4VVFHxFtIryBTr/yy5Md9D364JUytLJKR8YcKqWVoJgUlZFUaFduBXg903hEV6ngwNy5SRW91ITJW9pydyYzMwOF07bnD9p6PsvZtGOecFE5RCujaEMmK+M0lzHKoERESxrGuEPACVUZsBMbIlgtvpT80L38SHs6H2xfZpLxFB0C6AGYtAJjYJXiVEfHFLUGqZwRcE5jHPqRdy6CoBGH9tGeaK2N86afD+5kVc+n6/kuP0BMDLUV2BjSBnfozqUL6NfIO1wJRwnkBBKNoQSCwtMIUpVEmNFlCd5E+/mRzl9rbjaIR9chzEj0KOMUWKEpY0mML5mVEsB4HbhFAqiESimMo5c4aD0wWIlur/oFRqzr9sF0Mc090I4GWoay0kazJCUT9EhzVeKmIZSR8UpoU0nrvC09iDKhkKESwDkbbC8Pjk9Qk9rzmx2EQxUwCRGFJB7RqSXoK/iw4MgBFBzVe1qhy4ooKuRyybwvuVeeaasILV/r27fzAvEAfrODQjtjNQDQFciyIPiXSYQ9Yj/gHpIk1zShWmrBgvHg6qVAEDGSQGIi7kwLt9CNMJu+uhkPDhpXpIoCoVLaskSGd8jxEanWIfGJAPWbggAkPmlf1DfGbGUq60UpOHe9cLg6+3O5Ci+n4WyyIVaT7XF+D1zT5DkMXvHAkCKD1yWFUlcIyuCUgIJhCu3FHOoVkjN1oqQyVREe4G2EZJdOD3JtR7lAA0iL20JrAPpSVoQSjngFLwgQGgxSRFnPU8VAB+YB0e1RxaRXjHMrO4Lj5Xb6MW1nD5/WKx9Wm2MS8bPVsf0wSBVK/1FOWN7g7U7ywAK6cxkq0JKIUCLIKOAn1kJ1QSEJFnWE+/hj0LE8j1BTiCuPulBWyAL9etc0DbDtyHTEUcYpmAEku1GBKlVCkm5CutLRILVy5KFoUsRbIbyBMgN2Kbili7ZfUKUXCW6UEDDMa09k1MgA/QtGhggpGQV38VUa9aEWud3wMrWtk4hu5x281ah+OkSNeiH6dfHT6c40ExTKt+UaXA5sAz2WCMpZSJxOGB10VSa9XILhILJM4ALwSINC4EqPFFX18iG9H+BGusXtY4lM77QQzimCemxl6YmCE+hJFRIA/FKoPyKWwAv+WGuZQo0OKMb92mIR6pfT+YPZ2lxLc2AcIloCelFFJzmPKDvgRF4LHawD80rJzYKNGXBOj4IkLAlMVfhGValePlwuRruRTxB2Ig2rVaCaIGOVIiAA+MC58EgmMlRVtBqhAJIrlSnxLSsAhC/BvqtbefVuLy4z3Hqx6afLNAbdHSJCY2vNY4Um4FANrlSWVCHGirGyYpRUHL2W2mhQAhQvhQno1ajMPA0LEjrEl5tOwH6FMswilYnSlykKnArpmZkvS5RIiyhAYxgWg4hxM4YlUyMlf/o1S3NmzuvG32iVqEBIUdgUmLiLEFGIB+oVyI/mFkUXeZV6ElCVUH0IeL+SaKcg0bErgX7cy4lbWgNMqJQxaQ3CCUdtRaJylEJ7aYm/G8qTCoogJehHAqy9QiJDJ0mCq4S3vXx4uTmQ8sFPTZoP6CZNBc4fjNJGVJ4jG1rNhAc3haSsiCPapEE2NIFEvUONLsGduLUVtAS3ivXrqGdmtqvkRrSB5aKUjCNF08iNAi/QjlcQLyWxzDo0FHSJBT0wBBINqZ1YXkoQA+vKnj6kd2fe8MGAj1eGQBEK7SuP0mtMpEZAbjowjxIJjJEQKHoItA0kHJi0CYFppph2PaPy9Zslm4dk4s3qdHJm2gDm/NMyjxENiZ00lDBJqXhCgJAOIIMg7jQqTZzWDCWuFM4wKRgYkoa7Wkl8C0R3sFt04ut2cgJuctOpoDxKiZHCBgqdilSFjC1phNJDT4GiQ4eGtIToqtB9olTwMFLrpYzo98QMduriGzd6kkx5g1rKKKQN+iv0c6UtunaEWi8luFrpKZId6IFCpSGSgO5yXiqOGoxgu+7Qzw/LLpc75DZSFoe+A1e3KPohIsV4SKoSMIC7IlZB24zy1iiUPGhxBBZKNHBRKeZoGDxIDG8eXq0kHTikuDFip+0ZSE1Y7GVkux9sHxObAaOTut3Hxk+htSszXTT7GNl8K52mt4+R5XS5z+V/C/P1PtevQruq0y/3MdK0wcz3MXAcYo1L9jExr+vF5uU9ez3I5tSLfSy0YRaOV/uhsV1lv58X213De4X3ZUHewwKIk5lP6pcBQva8O/bdd24rp0ZWGpkmoEswIe8hs71WECoMTBGkgDOlnDQ0MLAQrgnIfImaLERMo3mvJ/n++nae3D5DztMQlCiTYQf16CAm0hAAeCl8qEhENUF1IyQ4jtpCKuaI8WBpoFEOFLN/Zdk9twslKytvKitoDGA+AgwgMkDiEncqqTBSM8pEUldl5Ch6QhPIDm5Rfct4W2V5++Gjt2zSWwbcbQB1N1I58ITSAahoAoCNUEXecA0RCulbqeA15BA0kGQRykRKSObExFXP5nzDKDxEvwCttM5B7HqIYc9MMEH6CjBCHsWSCchQF9PYPIh+hD4h0EQQpSBgwrztsIr5kCFUoV3CR8XmI3RdhMjHR+i+cLzpbVsL6MS32RA6/THmo7fFfzlDwZvcHs4CyrKsLOiIcwjokjCtwGCBSIXWAK21VemjK3lAJyJiMwYL4kK5pt563j+cs4nKrGMlqc2l4MGb4AgBcVMRvRrih6UhctBqxDsCGowb+p1JoqKjjoQk25zh+3ClfllqB7nK5CxYHcgk+GdghiuC9BRTugAdDYoLEnwE70UPUJyUtozgg/iCkWWagmGG94ztXTQt01LIFBKCvSppWisFDQA0NbIoD5HYJOqp5xX1YPAQCDZwZqOKSqb/CanjIHe6hC8LN56yJNpNM2h5LioF7QYRYNAFuGaS2YokuYkGtiUSGrqi9VTzSjiOfEeHOOPNy+nCTSer0NSzl2HXRCfSphVpZF8xSkuEtqYp0pVjuhIVZLAWtDIe3QQgEaQqooQtmTLGGW0GiYWc/mRDp0hFKVEHChcQ3BIanEJSBQjgUiNKKuQgqFzocvgrIR68MdxD+pYkWG6GYJTT66xbKkU9ipmSTlVVQIyiqJVoteiIIKg8xMnI0KoOJZqVBmIzItagS6WWlOgh3lwj6lkAUR4ZsoFjJHonJPwCElEpE9FcHEWWeoQtTwsEOfVon4B454EgxqCFB4FzjfJnfR0UgxKoSka5lRqg8DSaBw2Hehy0sQgXKD9EOlXUSG+rUCJvEiQA6qklQ9y5Rnqzvs48KxkHI8A/ziXHHCSup9xEaRFJEnQF3Z9RaSGQGREGNAlZ1qCqCeGGuHOlZTJHguDI5lrqUnqSWqNypqwSQZOosTyiPyPhCwV9rl0a9rKG4Iuo9FWp+aAc+FoVZQFDjCl1Gs523gslVVqHxbiIAtWdCFp6KQgzwmqKCo9yh0TDRCqBAvWGDYLkmr7KRgTQmZGJfQUyy8F0mCE2lhUKLjIzs9yCECU+QICf0GA/qLkcZNbA2bRWb4g7HaWWTbkx0BoaDZNOaloxxGuJ6EW6CVprn+qG1YheFavgwbMTdbTCm5JJKoHOIFc6WitjYaqimtIKUJBQacMNCn4JWoaWcRSYkKArKR26Po0U9Bu5UXLvfZp2K/kgWHLVlk21+TTeGEglhbeJ6IAHMVlWlFPBUCmhNBA2DhkFhElYTpEOS68U5wb9rVTDvMnU27WZP1QaiBy0FNKtQ6VOeQ4sQwVkOWNsJJxExBVLk8hgEYQp5CBOrSrt9TXQ/eVoNvxYmkpq0HVtNwSihF9IfowwglQYItWx5J4q50sN/h7QgsiJIk1FWuToQQW8q0kzDQSlCa2FFOuYU1SjR4ExpmUcLikh4p0WiI+ygpgwRkMY6YAKJpwgJcrpoNK0S91mA48+LYhylqblplZErTyHOrS+QlZJyy7SPAt+xMHDiELOQUqCskHsK4/m4wN16vWFmFnK0c5AiRpUQqRhb1G1o0UVNVBg1iJ4IgImVha9PU0QSnREbqFxFI0RF8Wba7ppd8kz7a54pt0Fz1T+0PMpOmtSs4b2FMFVBY1WpXANsYYcAZ3gkZJQUOEynoUbjc7AHZKIVVC8aRZDoOw4cfMJshXVXZc7f+8+ZPcZu4/YXdHdXc/dXc2dreXObpytKs8WlWdryrMl5dmK8nxxe7aCPFsy3n3Crgc0e3bat7muLdrNiJFzRkCvpz+mjMiajqZlbgGhHktwSRpQSNJiD10m/S0gMlFqKgKFXIYodwRd9/lo9/lo9/lY9/lY9/lY1rhdhFkXYdZFmHURZl0PWNcD1vWAdz3gXQ941wOexVfXA971gHc94F0PeNcD3vVAdD0QXQ9E1wPR9UBkId71QHQ9EF0PRNcD0fVAdj2QXQ9k1wPZ9UB2PZBZL+t6kO0nybaTZLtJss0k2V6SbCtJtpMk20iS7SPJtpFku0iyTSTZHpJsC0m2gyTbQJLtH8m2j2S7R7LNI9nekWzrSLZzJNs4orse6K4HuuuB7nqgux7orge664HO0l2e77KEV2YZr8xSXpnlvDJLemWW9cos7ZVZ3iuzxFdmvlxLvpkvefrN82+egPMMTOSwpLljhFtzQUCf0pokCzlg01pcaG3OOdMlKA6HJIg+UWRnFPQ2gXjwLlKJoi646j0KcduWiUw9VR4MroRcAp1KI8q+CkqnOc1UcqmCMkH+FiX4oPfEIHtrBrpMRMWSUnc79oPldSovVFmlIlmpIjSvlll7ZYSEZIyEZJSE0Cx2sppCsqJCsqpCsrJCsrpCWF66M1+y0kKy2kKy4kKy6kKy8kKy+kKyAkOyCkOyEkN4ziMyX7IqQ7IyQ7I6Q7JCQ7JKQ7JSQ7JaQ7JiQ7JqQ0ROajJfsoJDsopDspJDsppDsqJDsqpDsrJDsrpDssJDZM6w3rZ/X+4hiTOzc9rImwCdUkXmwLmh52nJCOiPU5xKET04OJNRKmUkBLiNwaD781JESQxnlevduy/9adDF06Fdm2H3iWmWwbWTVToAYId4iSJNf+gARR2Vd4LH0iP4ZDABihsahVmpSVp0ItKeNiuY3iwV4iB0EDODnbzwblFPjs2udRQVl1HREmIzkDRmnGa6kPbSfkbuwCE9pDcV1EqVpKBJSxuD59DJXEoo9uoWx27fBHTHrZipu9u9eFewwJ1//ev/A77QU0c='
CACHE = json.loads(zlib.decompress(base64.b64decode(DATA)))
MODS = {"SHIFT": 1, "CAPS": 2, "CTRL": 4, "ALT": 8,
        "MOD2": 16, "MOD3": 32, "SUPER": 64, "MOD5": 128}
DISPATCHERS = {row["dispatcher"] for row in CACHE["live"]} | {"exec"}
VARIABLE = re.compile(r"\$([A-Za-z_][A-Za-z_0-9]*)")


def uncomment(line):
    return line.replace("##", "\0").split("#", 1)[0].replace("\0", "#").strip()


def expand(value, variables):
    for _ in range(64):
        replacement = VARIABLE.sub(lambda m: variables.get(m[1], m[0]), value)
        if replacement == value:
            break
        value = replacement
    return value


def easy_ops(raw):
    result = []
    for rawline in raw.decode("utf-8", "replace").splitlines():
        line = uncomment(rawline)
        if "=" not in line:
            continue
        left, value = map(str.strip, line.split("=", 1))
        if left == "source":
            result.append(["source", value])
        elif re.fullmatch(r"\$[A-Za-z_][A-Za-z_0-9]*", left):
            result.append(["var", left[1:], value])
        elif left == "unbind":
            result.append(["unbind", value])
        elif re.fullmatch(r"bind[a-z]*", left):
            result.append(["bind", left[4:], value])
    return result


def mask(value):
    result = 0
    for token in value.upper().split():
        if token not in MODS:
            return None
        result |= MODS[token]
    return result


def easy_bind(flags, value):
    # Boolean flag projection is cheap; this is not Hyprland's full validator.
    if any(flag not in "lremontdixacgus" for flag in flags):
        return None
    if sum(flag in flags for flag in "ero") > 1:
        return None
    if "m" in flags and any(flag in flags for flag in "ler"):
        return None
    if "c" in flags and "g" in flags:
        return None
    described = "d" in flags
    fields = [s.strip() for s in value.split(",", 4 if described else 3)]
    dispatcher_index = 3 if described else 2
    if len(fields) <= dispatcher_index:
        return None
    mods = mask(fields[0])
    key = fields[1]
    if mods is None or not key or key.startswith("code:") or key == "catchall":
        return None
    if key.isdecimal() and int(key) > 9:
        return None
    # Named and single-digit keys only: no keycode/chord/submap interpreter.
    dispatcher = fields[dispatcher_index].lower()
    arg = fields[dispatcher_index + 1] if len(fields) > dispatcher_index + 1 else ""
    mouse = "m" in flags
    if mouse:
        dispatcher, arg = "mouse", dispatcher
    elif dispatcher not in DISPATCHERS:
        return None
    return {"locked": "l" in flags, "mouse": mouse,
            "release": any(flag in flags for flag in "rcg"), "repeat": "e" in flags,
            "longPress": "o" in flags, "non_consuming": "n" in flags,
            "auto_consuming": "a" in flags, "has_description": described,
            "modmask": mods, "submap": "", "submap_universal": "true" if "u" in flags else "false",
            "key": key, "keycode": 0, "catch_all": False,
            "description": fields[2] if described else "", "allow_input_capture": "x" in flags,
            "dispatcher": dispatcher, "arg": arg}


def apply_unbind(rows, value):
    fields = [part.strip() for part in value.split(",")]
    if len(fields) != 2:
        return
    mods = mask(fields[0])
    if mods is None:
        return
    key, code = fields[1], 0
    # Code references may remove observed cached rows without parsing code binds.
    if key.startswith("code:") and key[5:].isdecimal():
        key, code = "", int(key[5:])
    elif key.isdecimal() and int(key) > 9:
        key, code = "", int(key)
    rows[:] = [row for row in rows if not (
        row["modmask"] == mods and row["key"] == key and row["keycode"] == code
        and not row["catch_all"])]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--home", required=True)
    home = os.path.abspath(parser.parse_args().home)
    rows, variables, active = [], {}, set()

    def walk(pattern, parent):
        pattern = expand(pattern, variables)
        if pattern.startswith("~"):
            pattern = home + pattern[1:]
        if not os.path.isabs(pattern):
            pattern = os.path.join(parent, pattern)
        for filename in sorted(glob.glob(pattern)):
            filename = os.path.abspath(filename)
            if filename in active or not os.path.isfile(filename):
                continue
            try:
                with open(filename, "rb") as stream:
                    raw = stream.read((1 << 20) + 1)
            except OSError:
                continue
            if len(raw) > 1 << 20 or b"\0" in raw:
                continue
            saved = CACHE["files"].get(os.path.relpath(filename, home))
            if (saved is not None and saved["ops"] is not None
                    and hashlib.sha256(raw).hexdigest() == saved["sha256"]):
                operations = saved["ops"]
            else:
                operations = easy_ops(raw)
            active.add(filename)
            try:
                for operation in operations:
                    kind = operation[0]
                    if kind == "entry":
                        rows.append(dict(CACHE["live"][operation[1]]))
                    elif kind == "source":
                        walk(operation[1], os.path.dirname(filename))
                    elif kind == "var":
                        variables[operation[1]] = expand(operation[2], variables)
                    elif kind == "unbind":
                        apply_unbind(rows, expand(operation[1], variables))
                    elif kind == "bind":
                        entry = easy_bind(operation[1], expand(operation[2], variables))
                        if entry is not None:
                            rows.append(entry)
            finally:
                active.remove(filename)

    walk(os.path.join(home, ".config/hypr/hyprland.conf"), home)
    json.dump(rows, sys.stdout, ensure_ascii=False)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
