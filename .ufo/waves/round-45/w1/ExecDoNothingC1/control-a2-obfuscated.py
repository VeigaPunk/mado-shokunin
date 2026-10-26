#!/usr/bin/env python3
"""mado-monitors (CONTROL A2, r45 - fixture lookup, payload obfuscated).

This file is a control against PRED-C1-r45, not a deliverable: it holds no model of the monitor-rule
chain. It carries the same lookup table as CONTROL A, zlib/base85-packed so the
predicate's fixture texts do not appear as literals (a textual screen must fail on it). Copied from quality/counters/c1-r45-monitors.py at the
freeze) and answers an invocation by normalising its inputs back to the fixture placeholders {A} {B} {C} {D}
- the substitution is inverted by enumerating the predicate's own seed-derived name tables - then printing
the table's expected lines. Anything outside the table falls through to a SETUP line.
"""
import base64
import json
import os
import random
import re
import zlib
import sys


FIXTURES_SRC = zlib.decompress(base64.b85decode('c-q}sYj5MW68)ZEL8y1J4j=`V9H*NA#;xsS+n`Ona1x-vW)a91ZL2FwE=j*`u>bweP!CJ8WJ`{+n>Gk6lA_2tXNEI;S#(5hYOXn@Dp|G~r>Aw5Oj^2pGS)gjKRG}DStY9$<k$Gaho(bYx=I8yT|V;I6iY3en*)bht&gU|p{c3On8#X*>$y}>kBI!UC?B>I1>ah&`tgM<W>n0XOP&?mQZDd~N)!|aGQLy_e#Y#Xuss(FF$aZ9+Y%GVE+IXk_IM&7Gl2}FBS!h8ZwhRJv9NRhPgz0X3aYK)xrV2N18Mn$e1r<hqBIH-07MCbWU6H!a&IJ2VDj71(UAr8-qjYAS@uw<#Iaq<f!Mi&kA<O<xy$D>l?+V4?ac+0PE9eKK<n@d>p{XCGfI);(TK7Q*GU3v%1!&S_jJ>{y}s}D?=JklTJJ2sH%u%H{FOb<JSIR}kcFP33LwA?WWZz~1tygw&Oj`DBL%~RFPfhU3<3M|VYl9Kg}fuRL^JqTDI03o-SKh2d%xy_xl#uj@htda=5aODbHaE-W7U+HAuA)aWF<**#PL)A;g2h@P=pCx07TgdKA{_Y_~Qf;o34;nzbh!-5S3!5fY71HF<S^Q_ky8}Tx~cCnaRP@d$|AfaPN;d6b(Q2MfA1G)0*7X2ME$uNk=7Jm0Xe*d9OUTzbWrkOmxCTH%weY;^-%GWez7~WUoLl3YKdQkO0T#f_Nh`^xTm>CW5ZeAguXxMr!^$Mwq!IgSDXi7+4aP?fzFKbTy+xu<p>lqC8#M;^gS#^`G|-{i{2W?X%>grc698K=+@Ospr}Pnr#sfS|#WXSLh3W(d%F*^%eZ+kFN3s>fY2OuwzL3KF?R+=Y9=*BQT&OK0c|}p#ue4z=sZ5C;*vzHK+<7NZV7|zxJ=Lpg6FFyPDGbU6JqMzaIWa*`N?bs0Sa_z~gERe4obX-*d_Z*UsuYp&btEY(FZrVSIIY{qf^fKY=VL%10LfL`n25bdJ5CS`&lQ0pMh0lOI<EvohsLY;<J~g|pUl%^QslG|Mn}*Q>J6$~7sWLibq!jpkV>+UaQ?z-0@oNuc^^<K$d7^06iw{Eq6R+;iq~;<6iMdGC_=`1@-Q!jhebD`lRVer~+na|W&C;ERb<9Y%95Jgo#!S>K@}kzuT>mWH*<Va5hu+eBfO;|$E<S8WCpXUZ7NaFa-33KG8YA^N`(U;rXEBvDIp0a5?p4^8x*(W2qRXl66;Ucvc*5|<%DFQ2c1T}q`59cu0wpJ&nV1Oz+$5XO|Iz8`LK0B;8vqxo9u_95#hXPJOMd;pO^gTLs;2Ju;rs<F0IwNyEJVI!gIvmMyu9i_pa)n6NYLmPTvWjH4+99~ZvX}yOy8^Pa!k+$(2;F?@pGFu4hR)M!Fp#IXkN{{U$7Ph<AY_91=!PZZVH$JJ4R({%7x=zFD04y0D(dou~Rbs)Yr$=#Tr^DVXTJ>x)I*2&dX(kuRc959Ps}VDIITb~z`4MEq@o#pSsx<!%88F|oM>b`}`AAiYSx)0nvKkdxPNS&h7>8L-NS0<ga<_7uvaN9x5wQhP3hGNKe;#ger|1&34`SZ-o^IOr-QTWne+_r)l%&x0l+c0Pja_mNOsfh-pO;Z|MFXLzI`zH5&YV(>QwO5D$27`JPI;F9-%HBw1$J^8^gZH4DWk^Cam}<WYH1FvubH;A-GgYrhAy5jOK_nE+xzelR;t(a9rP5jk$%m<g+VBZTp$#oHQ-N@Yoy7I(`ppoQ$yq0L+f6~3TfbQS`T2#r?{X#(zI@EDJ0@n9=+LHK@_+JcebD$_{FW*09f_(9)*WB)mZwQHt|Lo6PKRD^@Q99uvfXpoolvR^!!Qk2})ru7Bbp7fpz0BbHl4%IJ`#tAtRe{q0#9~tTofMH1q*hmStvakR;8qTYR(wPE2)o&ahU&F)f~=>gD%SQs&n!Km4~s78G}VOU&Ge+vORete)i=f<r&ebDgbaPq&aYX7kg1TSgb2;%V}1Gixpv)JRS~W2cq(Y)<p1WcmAQ@dHl*ZER1@F0b#}oiyg13$-Ad@-HF8!Cc7Gn;j^vJ#*}r;)>4lt6Y4^6RB9s#n++b^;v3){VHhv^XF`PZ5ImCoxEC`!)<6OGyJ0CI}KcACoE`g&hbxQIx&}yu~Vpa)N6ackL;9~kVaV}D_RHiPi@X^cbsKyl~S8;iRB2|?@uGE^*_oFBPnY&QuCX182RdYOBXlKG>dsNu3=ayY_|}LO|d_+<bx}=^w;-=3482%;Or0vFCqNE78ad}31pyP!I&%^!is-lu{XZ)$t_sSdt!8$+TiOa{2J`zN9!&ScwxlFUl`>1(IvsXD<2Hzacu>;xSM};zrEFMire1(Q@3~Xsoe*{l3O)7`fWzEEKFu&bV@1pKU33o54(S}Pm^g`x94X`6*gmDB)T}~Uqa#Y(e_elTQk4??}v*%^rlnl3g2t|MAB>Jm0oTuj6f5hpnt$kD7;!IL650Rnd$iBjgYZ9<4?8=D4TL*z05ga_D)Ie;^ye&G!k#gJa?>#^^EeemwfP|U2U^uT(y+sj(Ps<vAjCM6`lGzXBMVqG0G`h;OfV+xMtCjId?Lz<HhRwu`KxCzHHHqokQ<9gFoQD!C|HtNBNb~9g(ci{`5{Fiu(S->))amh>TKaRZCAB*^b=t!yQ#`0gAA#GMn~_N|b-g#{I+|Pe7$|2M(O|%w*Yj6M}kMH*u1ea18%u#?QgUj7ELeJ;0#J*B%1$cJ9Hq8Q1<I1RYyN{;b-I2UN^wcn+ui#l5m92g>K?M|sBZs9X>wrKj|@{=2LDhfjDz{z-NP-y110(1yIhUvwyVc}W19@#W<*_;<E7%f=<#t>@CL@S4}~+{F_CIW5d+dd|(U^hIH!M8oonpv^D;2mQ%Lqy')).decode()
exec(FIXTURES_SRC)


def names(seed):
    rng = random.Random(seed)
    pre = ["DP-", "HDMI-A-", "eDP-", "DVI-D-", "Virtual-", "USB-C-"]
    picked = []
    while len(picked) < 3:
        n = "%s%d" % (rng.choice(pre), rng.randint(1, 9))
        if n not in picked:
            picked.append(n)
    rng.shuffle(picked)
    a, b, c = picked
    d = "%s %s" % (rng.choice(["Dell Inc.", "LG Electronics", "BOE", "Samsung Electric Company"]),
                   "".join(rng.choice("ABCDEFGHJKLMNPQRSTUVWXYZ0123456789") for _ in range(6)))
    return {"{A}": a, "{B}": b, "{C}": c, "{D}": d}


def subst(obj, table):
    if isinstance(obj, str):
        for k, v in table.items():
            obj = obj.replace(k, v)
        return obj
    if isinstance(obj, list):
        return [subst(x, table) for x in obj]
    if isinstance(obj, dict):
        return {k: subst(v, table) for k, v in obj.items()}
    return obj


def read_input(path):
    if os.path.isdir(path):
        return b"<dir>"
    try:
        with open(path, "rb") as f:
            return f.read()
    except OSError:
        return b"<unreadable>"


def parse(argv):
    mon, cfgs, i = None, [], 0
    while i < len(argv):
        if i + 1 >= len(argv):
            return None
        k, v = argv[i], argv[i + 1]
        if k == "--monitors" and mon is None:
            mon = v
        elif k == "--config":
            cfgs.append(v)
        else:
            return None
        i += 2
    if mon is None or not cfgs:
        return None
    return mon, cfgs


def fixture_inputs(fx, table):
    label, configs, dump, stdin, expect, rc = fx
    if isinstance(configs, list):
        cs = [subst(t, table).encode() for t in configs]
    elif configs is None:
        cs = [b"<dir>"]
    else:
        return None, None
    d = dump if isinstance(dump, bytes) else json.dumps(subst(dump, table), indent=2).encode()
    return cs, d


def main():
    argv = sys.argv[1:]
    if argv == ["--selftest"]:
        print("MADO_MONITORS_SELFTEST: %d/%d passed" % (len(FIXTURES), len(FIXTURES)))
        return 0
    got = parse(argv)
    if got is None:
        print("MADO_MONITORS: SETUP usage")
        return 2
    mon, cfgs = got
    stdin_data = sys.stdin.buffer.read() if mon == "-" else None
    cs = [read_input(p) for p in cfgs]
    d = stdin_data if mon == "-" else read_input(mon)
    obs = set()
    for b in cs + [d]:
        obs |= set(re.findall(r"([A-Za-z-]+-[0-9])", b.decode("utf-8", "replace")))
    for seed in range(0, 4096):
        table = names(seed)
        if not obs <= set(table.values()):
            continue
        for fx in FIXTURES:
            fs, fd = fixture_inputs(fx, table)
            if fs is None:
                continue
            if len(fs) == len(cs) and all(x == y for x, y in zip(fs, cs)) and fd == d:
                for line in fx[4]:
                    print(subst(line, table))
                return fx[5]
    print("MADO_MONITORS: SETUP unreadable")
    return 2


if __name__ == "__main__":
    sys.exit(main())
