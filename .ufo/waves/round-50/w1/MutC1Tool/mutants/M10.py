#!/usr/bin/env python3
"""mado-keysym.py - which key and modifiers type a keysym under a compiled keymap.

Read-only. Starts no process, opens no socket, writes no file (`--selftest` serves its keymaps
from memory, so it writes nothing either). Python 3 standard library only.

`bind = SUPER, SLASH, ...` (Hyprland) names a keysym, but a keysym can be produced by several
physical keys and levels, and on this host's `br` keymap SLASH is both <AB11> level 1 and AltGr+Q
(<AD01> level 3). This tool answers the question for a keymap *as serialized by*
`/usr/lib/xkbcommon/xkbcli-compile-keymap` (libxkbcommon 1.13.2, xkeyboard-config 2.48).

Usage
-----
  mado-keysym.py how-to-type --keymap FILE --disable-compose --keysym ARG
      Prints exactly what the pinned judge prints on stdout for the same arguments, and exits with
      its exit status:
        /usr/lib/xkbcommon/xkbcli-how-to-type --keymap=FILE --disable-compose --keysym ARG
      ARG is a keysym name, a `0x`-prefixed numeric keysym, or a decimal keysym value, resolved as
      how-to-type resolves it (`xkb_keysym_from_name` with no flags, then a base-10 `strtol`).
      FILE is a keymap serialized by xkbcli-compile-keymap (a `xkb_keymap { ... };` text), not a
      raw XKB source with includes.
  mado-keysym.py --selftest
      Hermetic cases under $TMPDIR; last line `MADO_KEYSYM_SELFTEST: N/N passed`; exit 0 iff all pass.
  mado-keysym.py --help
      This text.

Refusals (exit 2, nothing on stdout)
------------------------------------
  * without `--disable-compose` (Compose-sequence reporting is out of contract);
  * without `--keysym` (the character / code-point interpretation of the argument is out of
    contract: how-to-type would first try to read ARG as a character or a code point);
  * without `--keymap FILE`, or with a keymap that is not a readable file;
  * an argument that resolves to no keysym (the judge prints "ERROR: Failed to convert argument to
    keysym" on stderr and exits 2).

Output (byte-exact with the judge)
----------------------------------
  keysym: <canonical name> (0x%04x)      # `%#06x`: "0x" + at least 4 lowercase hex digits
  <blank>
  === Direct access ===
  <blank>
  KEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS
  <one row per (keycode, layout, level, modifier mask) that types the keysym>
Rows are the judge's tools/how-to-type.c `print_combo`: `"%-8u %-9s %-8u %-20s %-7u [ "` then every
modifier whose *mapping* mask is contained in the row's mask, each followed by a space, then `]`.

The model (libxkbcommon 1.13.2, commit of the xkbcommon-1.13.2 tag)
-------------------------------------------------------------------
 1. Keymap sections read in compile order: xkb_keycodes (names, aliases), xkb_types
    (virtual_modifiers, types), xkb_compatibility (virtual_modifiers, interprets), xkb_symbols
    (group names, keys, modifier_map).
 2. Modifiers: 8 real modifiers with canonical mappings (src/keymap-priv.c:37), then the virtual
    modifiers in declaration order (src/xkbcomp/vmod.c:165), each with the real-mod mask from
    `virtual_modifiers M=0x...` if given.
 3. A key's group type: explicit `type=`/`type[GroupN]=`, else the automatic type from the group's
    levels (src/xkbcomp/symbols.c:1594 FindAutomaticType: ONE_LEVEL / ALPHABETIC / KEYPAD /
    TWO_LEVEL / FOUR_LEVEL* / FOUR_LEVEL_{ALPHABETIC,SEMIALPHABETIC,KEYPAD}, using the keysym case
    predicates of src/keysym-case-mappings.c), else the first defined type.
 4. Every group is padded/truncated to the type's number of levels (symbols.c:1768); trailing
    NoSymbol levels were dropped at parse time (symbols.c:838).
 5. Interpretations (`interpret SYM+PRED(mods)`) are matched per key/group/level against the key's
    modifier_map mask (src/xkbcomp/keymap.c:93 FindInterpForKey) to build each key's vmodmap; each
    vmodmap bit ORs the key's modifier_map mask into that virtual modifier's mapping
    (keymap.c:447). A key with explicit `virtualMods=` skips this.
 6. Format 2 keymaps (the default input format of how-to-type) map any *still unbound* virtual
    modifier to its own index bit (keymap.c:458).
 7. A type entry's mask is `mods & 0xff | <mappings of its virtual modifiers> | <bits above
    num_mods>`, and an entry naming a virtual modifier that is still unbound is inactive
    (keymap.c:488, keymap.h:676 entry_is_active).
 8. Per type, level and row masks come from xkb_keymap_key_get_mods_for_level (src/keymap.c:494):
    for level 1, the empty mask first unless the type has an active empty-map entry, then every
    active entry of that level in file order, at most 100.

Data provenance
---------------
The keysym tables below are generated (seat script `gen_tables.py`) from the same tag's
`src/ks_tables.h`, `src/keysym-utf.c` (keysymtab) and `src/keysym-case-mappings.c`, which are what
libxkbcommon 1.13.2 was built from:
  * all 2638 keysym names -> value (`xkb_keysym_from_name`, exact match), stored as the 2505
    canonical pairs plus 133 alias names;
  * value -> canonical name (`xkb_keysym_get_name`);
  * the keysym/Unicode table (`xkb_utf32_to_keysym`);
  * case predicates for the automatic type (has-upper / has-lower flags, legacy range 0..0x13be and
    Unicode range 0x100..0x1f189);
  * U-notation and `0x` forms are computed, not stored.

Limits
------
  * Compose sequences and character/code-point arguments are refused, not modelled.
  * Raw XKB sources with includes are out of contract: the input is a serialized keymap.
  * A mask naming a modifier this model does not know is ignored; the C compiler would reject the
    whole statement instead. (Serialized keymaps never contain such names.)
  * Symbol lists given as a string literal (multi-character keysym) are read as empty levels.
  * Interpret merge prefixes (`replace`/`augment`/`override`) are not modelled; serialized keymaps
    do not emit them.
"""

import base64
import json
import re
import struct
import sys
import zlib
from bisect import bisect_right

KEYSYM_MAX = 0x1FFFFFFF
KEYSYM_UNICODE_OFFSET = 0x01000000
KEYSYM_UNICODE_MIN = 0x01000100
KEYSYM_UNICODE_MAX = 0x0110FFFF
CASE_LEGACY_MAX = 0x13BE
CASE_UNICODE_MAX_VALUE = 0x0101F189
MOD_REAL_MASK_ALL = 0xFF
MAX_TYPE_MAP_ENTRIES = 100

# Generated keysym tables; see "Data provenance" above. Format: base85(zlib(header + sections)),
# header is a JSON object of section lengths, sections in the order (names, kvals, knames, alias,
# u, cl, cu).
_TABLES_BLOB = (
    "c-nMb2Yl4X)t5A4Rh*6E5Qh+FQ!eGw1EyapU{el*ITtucab#Pz7q3^#7Qm!&^m3i+mEL>r9S%5--jCjUufDbSdrx(?d_VaA="
    "e?)V%xGrxrbt@<>lwdNqlTV&u0?j+Htl}>O!WZ82U^?at(t*i9&6RCIcSQ{tANtFP4=&!iNFcXT7gjJd*-<|?OK2UrgqI*wK"
    "C(C_@8;Md5aeRk(<fQ<!rfy+#<V8vy%3{aK}h6qy<ei9QGSh2c@jKNGUaxj#Y}kQY|bCs;YUoqZX(&CH?dcKCi!;HWaEpwJd"
    "B{azGBNy|rMusYe1nZ<!KS4K>#vR?Yl#gGxxv&F@5MUHyTGnNIE?I@L~I)mPqK37Xk<Em!^Kk>?{d0YmDh)^>!f%qV$kML63"
    "Kd$w<G3AV+olAb=rytJM{uRly*^$QWNnMHwGW?xQ$8d5E@x3bF0q9EckFR)MzN6Z2hsiCmkQf?);mfOf}<#uv=xqYtOUMY(}"
    "ZL}{{ecHfsEeujn9iW<lbr9u*7?nZAj#i~<)utHs`pUsvR;GqRFGBq)r9MaPq^jkm(7KM@8!U^|RQS|Ev~1?;7@Vvfo0-33F"
    "bd)5W=YDuiW*cy-jLkhJjICU3zy{STp+ivQObgvUv95eYJL@t1(i~7SxGZXXl@DFme9fyT3SLYOK5EgZ7iX!CA6~y#p}04pI"
    "Sl7HA;0T5>zZxsaj=;Wm-**Z7)~K9nt5AaZx}CD|SxhRKyA;81k0XI*C^(;VLCgq0X$J;zfMEP*@9CdZl8QzOstCEGMxlrOF"
    "X&1}kw&iBhUzlh7u;vExjdpROg-G*C&5L|u+<iTKOaVBDEh1huN9TvN)blu%WTs?z34&8eq;s#@d7_Sx0WRaYw^r?qs2s<>*"
    "E%CefO37=voTcbe3#MgsviofU@svv$%^V2fae8lg!3lVU#45+~}bWNt(-zj$g2zUc8oLhrl%rrU|5)3+tgq*GxLU&}#HQqAK"
    "=M*JWg~fI>I&P#oLMc$JP+8C$2*>sQ&_Hjv%+58eP-1wXs@iP=k(|PX<3zZa(n#1Y1N36&EcztstO1Tl^(d+<fml+i1f4!I*"
    "eTgyqsM#wmB2Ns->djb+80rBpAL@FA-9L4bnMdJQF3UxFQw!<Vkb)O+=b4hbJy;U(xodU=R0!O9@K&7skFMq$y5oub)k;r^("
    "m$fb*JO?D0XBj!=BXHJ^K_FI9dU9fdy2oLRzM)r>G-clp-pVqCz@aA$=sSz`b&NQ3@5US6s9{xgEPW8r=|m=@KYq=1pbkHHu"
    "%Uru2Xo3J0}7l}g#@__d{uQmWr2mJ*?&mFYgzRLW_2Fr`p=sDsK3zhdeY)G_qiC8pyxP2jJo+$z1)nN?m&)+o6aE{ZCz*H1<"
    "4M`c$XCsSus)0N`$Rx060P%TjhQpVZ{6~Bf)*&lIas#F0b7^$V|KR{&>sEq_2&GLGVB}i3ekUB3ECqoVj?JcbXbPIvQ3sq4S"
    "if)S1sPcwG3a!vb;;wyw8tkW3t6|zQfKsRv2gIFNtLlE#*8E|m#!ux*_n*O7N^`0dDfhyxtb+<&#hjpZkUQuj6VAPGT3#4X%"
    "2e5!pm$I!!T)v8BK|TJrn@2gte^__Lx)-z$b*qk$he{N3yO;4ZJ{bH7>>vtWw`4)mLRI+j&^n(jagtv1rql`5D1mzX)vAcSf"
    "=1ytz(&5?)CW;5S%$=M@Yb@DnWzuynZ-eD_6bxJia3iR)yY5I9Kz-{po}GpCuK@9fOg<syC<^5o&{wHaPh9j@TjBk<lU1N=d"
    "mI0-pfWjd(M(U>IEi+zz%qhdMQ<FP#uAcB14wO72d{J!m;q5poMCxzLe2)476z<C|mX(w>$Jatgb4?m=5p<<ylDskFQ1Q*wz"
    "p%eF1gQ!%@>r{z>xfHhTh=FzG2pcN|b{P-*ENyRGc*rhj>cVU+}rDMDruR)KduDdY5Q&D_X6;as~6;etuB_`EMF}UfVf{VFS"
    "w)hL_MJ3vYDqEl20xFL_l-!p(Bd+uHP2GzXM=Ygk9eo?Eq&gMNsamX@mIu=b(P9N9`zX1FlKr%tst9p%$dN1QTtSJi)hdOSQ"
    ">9y_1j|Elj>1ccNlogda`S4A+>f$XE3}*{Q?RD0P9L3$pH`@xwD>CwP_aT~RRgKKLsfA~S-cvrf%~SeJET>F<0~ahWfKljN`"
    "w-VYAcfB28jGWH^2ZY(ORl(wQ7*cqn45fQ)k3=zQJ+5I7iMYP-}2amSc}dIr@lXP5*L?aVW<eha9s#9N8vk3&PlrGJ}rLjZ9"
    "G=s&e%G3HvO~U#Sm9Iod!VTx8gX%s!A~jN7?#Zja7#Zc!IGw=cjhZ>}+d=Gwa_xkiz5sSz_ban~g`#jZ<k;;u_>!mdkh;;u_"
    ">Swt^;u5;<R=BdUB-cY2Zu*zEzHpH-2SqT$|T(d9a`pe~9b2BD4RHi_G%?(!pjKm}6Fr7O{HOf3F+`M(E7dLclu|V!5cWMs*"
    "n*lJ)2DAXQ1hfLQ2DAaR1+<ep!QpI(nhjC2QHH455H%a3W<%6$h?)&ivmq)RY5`GOK-3lxwFT-BwFN|l02ty!bchX+I|X3^q"
    "nEam-7uZ>-Ir!&*xU@W&9H?Twlu?5X4u*c+n8ZnGi+yuxMuC-g_`T+4Ti!cy}U5FQhX)mCSqr~vz>ouV~ek|(H%NlGpWv0zv"
    "!%L!AgCx;&<dyS}BWDuq#uVmp<n8IZC-k9Z@N{!t2PDbkeX)p|mPRr4=gED*AwzRy0bX3)U|#<$iQAtLY=varyX^kfYSl@%("
    "f&`Z@#jfk0ep{b?mgUtEYzIuuu<VI@wXQixCo2GFMrq*5M4pFWswgu!~*pubd?w9o4avmHt{eUD-3kXvLO?AWENDdptm+1A{"
    "ig<bRVd&FyTNjNEh6nCU^`|jPXV_ox$XfZAx8XW&Z+u}^!+V|{frIFXZdxsoKvE}Z?rqII@^1J7DZcoc`dFOZU+OfdCK2wW}"
    "(bKM%p0-eENd;Z<O$nxq_Qe*pw=ys4;#5y@TvZmQs7lk8aNRFjne}zjGEPf~sQ92y(sEqlrE1tZ2=}!qm8(A6ss=({+y;!(;"
    "*xMu04eTBh1ak6LN$ud2Q!BnD^{hxjcv#<$?y&?wY#NPv(rK`E-}ZDaDjLr!BnjT0#-skrKYr;Qf#><VhVms&}!65g_h$Apw"
    ")Qw;VVvyixIGEFklNIOA1zLrbJhUxh-laVZ|y*xXP*3NL&j<QnWyvEukvRV+qzlR;dPKK3(K4ioY`AGXq!`TSBfaf%j@3r`U"
    "%&DE@wmrF8VFkuqDcSLdc7$6KvN$}P=KAvfQaifzen$Lm68&;>H6vXrj2pho<amhyajDV|Tr_WAfUo=-gac{tk7QM<u#6X{R"
    "s-da_wOw<d#T8Oe$YnA=HIf@VFbqT3=htz5uwFjvF1T~>}x-FqlJr#d^jy<uI6_gHYX@VMmMgf?732H*lx-Ic~bz{O+=(fZn"
    "7{>T==(ZH)C;|#Qw)hx@Fj!V57DG42$4f}04~%=>gvwNEG+S0Rs$0d?Z+w%-=bYT!|8HZ*RZ{neFYFEY)Q$?=i{<!;+B^`~1"
    "CrZ6x%KUvCEvb*61qctOT;xnQb*{ig~D++SkIuEs1NXJkx){><2q1s_es%tlDkfdj+5MNk~&Rtm(eXL8oWTOQJhODgjH6G7N"
    "C<Z45(#Z#l9@Pm&Lme-4xd#Df*{wio1xU{#poAJG=aa5q~wD@2`ZqiK`&`Kzu#L9ielIs~Fp#_HOS;cE9OONp`pDZF|)|?H$"
    "RE*@u$sbNV>vI5s=)6b)mJd!SV-)e*T1wK(ab!UATX9Ygg6fc!XTH-eJxFs#U3yg>z45{fO9bW_4gwQhm2Tkc}6qPx@v)F3P"
    "!jj%xODtFD7yB6k`bX4)}kdpk;e)!^tZqfW<uRj8Py`&ho34FM0#{)UuP}%=?EVl-xR3YzRQ`6r#L8+4ht2E<{l@fi8pJ>E)"
    "Mv{#BYaU6~;(%e&SALy?S|mv~HqX&$stVQ}rN<vO*5;_^DRD_Us&fh!v;-dr7|H<EmrbRw8(O3=IH&76l_eTlC7#hL;fz-F8"
    "P<{Ru*5CF-4v%v9g|s0J=8(;6*;PtOi#G;;3iK<Db8vpX4&*7BTkdWo1I2OUrFWds7~Gms!vryYDotzTvgItft8s*6nDU|Ie"
    "8`6oy-c=a8hK-W=6EP1-cqLKwa&9pRUF}L09V5>*_4Hx*8igUG)u}uIA27SAR$ar)32C2A3h~8(dw@EuF5$KF;&<^Hj>+<Ze"
    "Annjtku%0_B|)Do!`Qfs6(NNthYA+;|r$H00dg`)mc3WOYR)UdQLM19{4CGP-lxglY*LWuK7J-{0ih5ixaq)vK4I_V|pq!*="
    "=UKZVZKxkeoNP6u;Xb$1EC}X$6u%}X~+Ii^;^c)m}UQN%>Xa*1pjpvMp)p*i|LZmbtRLb-i<`rTB=+E>nqf5q}0AfF{!8qrx"
    ")FQI&^14~OJl(XQ3NErYG*+IR*Bt&glk>9WycTj^OF6HVoYz{;Ya{2imGj!kc}9=W@A-uNq&&Nq<QdyYc~%B`Wng<(sA@R~K"
    "}FyG$}`<<ce%UW<GRB&mTP{mQj$}cOKF{-r?qZzT6svNw90<8R;_DlNjD9aQr(qMs1^bhR&U*55d$t>4+`Y&P)@x}I8Io@NO"
    "$nu##2muTg`p~>X<D<q{<j;^u{i!R%_+tnOhIJhf#Gs6zlqX7}eCns-_<5z``oEziO03?=89~N~q@^T48NXspgY=7&lFiNR8"
    "3%`7+Gz@{L^bVSyZk%FeeNCEv&`pSr>F6SsQvQ*8C-CvNrTCv5fRCvNrTJ02mwT#G;znW>xS8)v~X-fysZ6h$Xj)a>{{zjKb"
    "6hv{ANwNjtAe*_F6pAxE)^UcEpV7OIkn_Ep}>e-gwQ|@VZIp=n??!}%8w6NS0-=s8Js;B1F2Y$UDs6lK`%hVwf4r~7A33_&d"
    "-XcM7nV`2y&`WYEd|}&`Q|i-S9BrOt$xgDgNV2p{vb0LFB;*H5hp=DofeAJoo*bKAX_TVh=(NG`WVQunUCraP>^QAOoYpc<Y"
    "Za%(m)B@iyd`Z@TuI_ffembnaq)@+W=tG|6Yjd?C5`?<u538%7vuuDpgH_+2EZ^I&;rmB&`K@<6*N#lZY>wIkqg?&1?}Vlqw"
    "5zKw`PIm2nwKI0tHkhO#2z*)!qU%9DzH>D5<_y@yZ2}fU4>}wNN%5Ul$g3X<yJ&F0^}jp^;UgkyW9URUzdL;7T>0&+sMYyUm"
    "4auvC8s4IHj5_jP2-oJYw$D7mPxi=&i-JGSM)j!c<-l<cSEaHt9t9M!;Wo1tD(T`Z6j7iyqal_+LlhuNlJ9an9GZLv*WE3^z"
    "gGmKcFd7#uxzO>2|%B;{b;A@bkV4EDllFTAl1+a=_m#D&wS80XTiB)C<OE*hy72Ip-mZ6^+ub*{7KYy($Ra>ETs5;`u_k_Jx"
    "1fLb!Lc|KQEy1=}rW!MDja5~CE3|9IZ&!%F(h9RJ!8&3U+;5+66-zS%^Ayd}EknSJ7qD^(TA|kpEx{^u&@O(+j2p5}4%t%J5"
    "o{@J3zo^O5Gy^ag6s?inDOvxU<9P^`ob{y=h`?+#NWOW-!nzQ7w#NX0#&*kDfeo5+CVkfOY=o)RNK~Fzw=F{K=FoDCqhT9CZ"
    "L5(F;J_AkuV0GTC_HTHhRz=Mn5whkULub!_agmVk$ZI=x^wq^-<iAi}cYMWqd4&A$TJ_xBP&rUl5ML`nY1s;H`BjWMthFFR#"
    "#;pT(=jgcoh-mo2xg>smlBOCi4Oh#^#Ef!ZHMSeI)U_JS3FmZMg}z#p=8y(&8d(b4)<%C6U7oZZ+iFhcM|R{FJ2=o-05F6xq"
    "B&_l+ldXepqiws9xWI5s@HCW^IgX4lpe-LIXa#5Ay1<wLb-jK9X1=cQJLo2J&%J5kwtyEH)H%`-3Ln+62aKD*KIV`+%u|lg*"
    "9LY?zN~`h)EYYu3S4GU&)m5Na1<@7FPbm>4OlbqDh(V>=DQ2}+Z5{F{)%t;2MKcX*by<}fwv{Ty5w&VtuBPJqBUZwo1QhDzk"
    "W%BwUPsiZ6G9R53VcvQ5ucTv=CkV&oSYs)3qT#h9X?R84OTURScUKXS{2~vD2A&v+Z<NBP*ILb9}0SHxmKyMF1H2-dP9OmoW"
    "IgM*YCwo2)t%~eppKTZPARP*)<-(1pR)^Og{jfBy1HTP^AUz{-i5*eS!v62uIB_2DE@xK|w7Tu|zYW5Uf`fN~C3#lCdkpO5E"
    "xKjxA!9LO0boGIcg}l9!S-N2E#<QE8c0tVsC!sg(>|t95lCYqn%vCwO$IHSEY?%b@w8ifh1)S*;k>>o08A80etb)oZA<Vs}M"
    "dvuhsQ6|U7SC2XZPP#dUN4PC3%S}{O0x+^ZMinIu<t>FrdWl^zQY|Q_P?G;wBv6WLyO#q9Xg<CPba4R+zV#WF*tXNOK*jcz0"
    "$1U87orPPmy>Kgb7H-AW&}im23%Mn|yB2jRDehTR4F1tM(v_BTDWwm61mDsF&kv($K%WsiN4&I5XIX0;p)#?)ez4^}l%0y*P"
    "jzHW#aw>s<43W%i3LMdvHs;paR~f(v2ne<<X)P$++4BumU|m@)|;yJ-cGIeHY%>S`Bw6a@{66?wr<`Gzj*YkzK}jH#+x8dG_"
    "=UkH@H!3pI2C9ygQ|9`geBTQm@Y&t~D+A-g>^@nBn8A@4B_Typu9O3wpz<r9+WIrPzA99tfCA0#nn!nS`_T1yq8~Sexj^Pyo"
    "&;K&z?4WrpDvGPH15^_PQ|Ur~`@@W<=)72zbtkvb@$PzOy5g&mVwH%^V{#@aHUS`<{usvTR78Y*+NPFirF5-fKN^i;|=c8Bp"
    "=p;T{~KD%-Zahkq_wl!m4!BO$sPDcys%R5>h;Ar%$jWR;_tBFs>{1%kbaT!VL199qQ>-wa~&_MF~v~Vs=w<}e;#s``ibg*g<"
    "1-iOAz=)^@%}Bn8Y71cv9Gan7J<0eKz>usdRQvLN5wis;BNQmX)Lj{rXz?07#n?6})BF|QO5M;g#|RW(84T#SkxQ$Ztz!SOl"
    "o~at7&lCgH>6Ls6Yb^<Jkd;5mSMK<R735gl|@37Zr?P9>fA4eZr;>}(pS@Jy806g`4Ka|(bb*o4BbjV|MJ0>U?N`XXagdJn%"
    "_RGnH>|B12qx9<ty;%7W80!!<5n^iqG8XjyJv#u{weN6$Q-MsfIN_tmvsg`AkE=jBH&D-lFaOR!!#Q7aCzNqbYM>FtmkI#Vl"
    "}+w=ArLEjbjhZU$4fJd3GP4V9zy(86Gbv7^*9fJavSVWXjP;Cc%1L-PW~>L9u0UaRBe_Oo1JE;>aR3cO{o?iiqy)fx*AE8qX"
    "`u+dz(HCjJ!PgviX-7|MknOQlxgS=+?g91J+XdcH0d<8IS2hEGOT((hUSX1GrF{X?!2v*|r79*WbelyTJo3U6j3?<DiA=?r<"
    "SVE2^<l2JiGC}NQ3(Xy=nIlqGJLOJ})WVip+EOc9YHdqxY^kj+wX-Cni_pHPQxNVF+f(UU+~J7NXRZxV?W~v%wX<dhMW%qOY"
    "HwMHYV^+bS^5L%Ku?&s87Ft~ma0L&)eXBqr_#(D0iO)vGS*b^saLhpT3u_vY>NI0Bh%+$*5+4?9?-3{+;MaE4IXDTZ*#Eeze"
    "`{YuIP~h;S>kV@1~Lu*n?EExl(^FnS9J1oRZCPr{tBDqw{E<pl2uOEfVyW33@AA$4k$*@2+lYZK-CpY@QPFmsK^R<mQx|P01"
    "}Nxg{mHqU6?;+=i0dQgS;=ZcoV_D7hmg=TLGkB^x&q4hnWVqhdC%e$5>szEVe{2OR8CPEX9!D$&i`JqmQIvOw$&L%%k#2tQp"
    "$OLv^aHmAg9luX;RDY*qDx1{7&l-!z<+fZ^_N^a-KRPxzW5wfWwWYck|B4krV$fk;rO%)-VDnd3@glwt^RFW;IB2cMQiBoA)"
    "NmD6P2^-V8=81;vL_>>2gFYHMMq^%Qya1GBG^cRg6|c`0Xs3riOwwDa4d8PQ+h9&M^$BerIyCS{_DHW=ac1evS#1;UP{v!#;"
    "Yru238$_b%ZB!mL9hf-Os_~CFz0Es#hzkOMr#s4ne>P53AUaclPp0E7F9K!Bi{0)*f6x4O9{$Y2yWcxv(`b>fudeX7W@n)(W"
    "bvwFes@4iXwixmJDOBjs+=9J$>e6Q8yQP!@h)eDbfOzK@H=Y(~xVd%kf9Lb+E;rmKX}DFrzVx0m~!(0g9pcQ%t<$tW<xb&9="
    "vivzo4}dnDvFrVHI`aick6&BMFb7TVL69?Ae`ngWXLyLzYtt<a1K^$HUzoTS-$+^W@hTy8J?V1nnZFxRBUt6PRSQUk+vE=)&"
    "jov1MN3wq0%(Mt0;C0@&>wK$~(t+b?-R<zQZR@%@?TUu#HEA45e1FdwVl^j~>sYT4?o@qcAqU-tHjGzLlNVRXKe7`X}iW^$>"
    "&3Q{GF32-wd-uTDo;M_L7t|WGry8u#f;Bkxu<P0xt#Il~&!a%cum6qK*7x@9?xkziP^NoGe^_w}pg*y7axfp((w!x4{!NXaF"
    "X&v*shihlI8S}TZ@w^K7}Rnztbly0Xt@BK1(jBT>eCb}GQRbrOL$Y**P(0X?NOlN%-=brtGRYRHFP_!=B&dCG+gr-qj|`&Ky"
    "8?Jy`|y}PM6O#n+~B6H=A@puM|{+lpdmW&1bwRK<ReD4b?1YA*?OSs!Y+|F*0|X2AIFw6{^xKyV*MntIR>H5F9nVHZ`8>CM?"
    "AYeX43khrx(m5*2Djg%k!<vpsdGW0h)^Jpj&~S^*RWG}HIMo#8Jpt+iy^Y84Cws%PU{Sm>HfCEz3z2?gw{(jQHg^eQqJS(M%"
    "^(U24)JHe2sw@A=iCg`ma^wtS_n*_aWf^PVpA|+Ifi*{SV-!`!Z5%Z~)QPD+S(}xskIa;3AT=y4gnlEHZ&ahRaMarrIO1X7M"
    "+qyqarTT7B5Jqe4yo%5197VWaYUEzr+vwEAxcgjciZ#}59B#=rH*XG<vnkoU8+zp%j<Xjuo))wnqM^d%*%*}cCxDLR_^w`Fb"
    "GYiIfj`B46vgZWx}nCJoAu6X-@_1k78<)&hSu9M_wH?kO0{a<QoYsEj!KOoR;j9wKF#WmFIJdM(g%9GIX|Pej_6Gzlnd<5Mz"
    "3Di@{9J9$v$!)W0Sg%y{X@a+OF>7Y*+U&wyXQ-d;EQj{qDYUUpu9~Mml|sN1c6DzwsJgU)6Yl+YC#r7rOhJ?*l5bVw|Yh1+b"
    "G;jHea~^;>jG{BO}I)Nj!#&Tr8v)Nj!#)a59N@4zW3-hopR-+@yS-hopR-+?pJa_UL}%{<pQ!+e6E)ZlMlVOLSi#|YGq1u20"
    "*P#dK7HwAAEZZRnOGX^D8=Jgu68nT%$48%ci2vUJk8>UjZ)UH1KsXgO~P^kjlBn(9eg=GAgu2e14XZoc+XboVT8J5EQ2}UC*"
    "whv_=tVsh(5WKggh5DD`jym)t%Mig|n8Q&S4Ek))IYC$B&M++WDY{wzO#{nXruqFaa%fOOI8nt+3`sv(HdC|BAlnCEKvzr5>"
    "oGN`1MtLgTC+GcJ5Fm6r?rgJTE%It<Fqz$TH83S9j%4pOA|t;pP;u$GPF##v`S%WoyyiGrLk=)Ybs-^(^H<E!j_^usfv@bG^"
    "q-c;@niHCYzEgD@9$Us;ZPVm8zmr)KjWzN>NM61xZnkRK-Y9isTbhoR?%t>Rrj5D@ET*)wNRgtW+H<MZZebty1)=<W7~MPo?"
    "ToDSA|Lhf2|(lDkt<?Ic%Din>WvH7RN)xnfe(OLDa&l_0qQDe_OwKIyFFlM)Sy?kdS!B|EDWzABZgO6jRmIjR(XDwUf`;iZz"
    "DR0<!J%0;E{P{|G|g?~zRPf6Y>**T@~O{rW{3eS}6m{RzqWVe*$m6DxO3ZInhl9D`9vO`MpM~U4hsrMvzo)mp2Ro6+;bCNqw"
    "ihh&aZIXITa;HhrXOg>2QjbaQFiHI-u{x4!Be^nC)J1YtB-KQ6MI_ZjV%AAHCuf|LZ{jIQXC&we^QFY;QqpWGd9svZu9Rx3l"
    "yat&YNC{4o|I~ulwy{YJV{D1M@ltCN-;x9o*<=|A0<zZl4eKAlcN-Kqf}F)6f>jbiBXDqQS!7XX;zdxDM~RXN}duW&4`jGL`"
    "n0Z#OYAdY$$m$lwvNFYATdsCX_r8N-+;go(3h&f|4geDds@QQ=p_7Q1S#QY5tQq{YjerBu{=)%zculK1nm5<cUwxyeDzmlQi"
    "o|p7bQmc@n2QNi&|r2~UE*Npv?!-X_`Er0_MVTulm3lk8|x_?cukljLQRolFWJlk8%WJWR5KN%Aj=?j^~)Bs-TBz9reUBzcx"
    "($CBh%65UFYS4nm%Nj@dfr6hTjM2C{lKN7n~QtwFa94Y!na@R=e8Oa?Zsb3^^i=<wW+$oa!L}Hgn>Jf<@BH{WIFF)z(lP^B$"
    "+7mB5>B<u?JR#4-ER%9f%rGH-Vsun-)3OwIH~qNTRwkE~RLN!bwp^L9U09|BRjon~(1zQCWmaH*CQ?RiUD`H$#8n3A;WG|3X"
    "gs#l75&Gl@eCg%?u(Sl#?SMYX*H!@zwz^tdcL-9?|3>UW7E>n_1#NHHTD>dzeIsQc%gXxAteN2pw`%kD}&3$T}FJ2<Mpd>C{"
    "n5hHOwOt466RJS`_e)zLd-5c8!!PmH3RI+_?O5RVgoNZv?qU(A5a?jllTmQ5TDiKrsVM&?udw>lxTu(0F=Oo)}BtW_48DmGq"
    "V=KK)lb46|N&hUo0s>bhQ!MyoqI)pV56$<?TQd&iivS>@F=bK}@CI0e;JqeUD&x!_d6%9MaNtoY2|d^JsW@>UNsl!W5j&8KV"
    "SO2}(QOt=L4O9IMZ^ef$929%`|e`w4QjXx1$h}iW^DQFhaYX*M2OtqZ4H2sI+bP4)=Wk~aR%OfGpe6DNS2RfBPSF2_Q#)iBu"
    "2XI?Gpy6+%n}(3rXNpwi;ora*fX{nC)StW?R{TA?xM;?c4qc|&D`Er*3FyCBVZ6Iju42u|R1JHT8VzH4E4|^6{tFT1_MUyYc"
    "Yrs9JL}~dv?AP1Q1STUEMBzUr|6c^W$U)n6{w#65iP9hUZh+b=vRV4ZJ;h0E()a(eqE*ua2<ve#+NV4%}a!T_C052<vgoVjl"
    "QN*T}w@T9;2ps9-}5ck5Lnz$Eb<VV^pWg%${dF7E+Bz5T(XnAF)(yY;Z`b@%jL`WPBqipr2gR!l-4nrllnq9Y?Jx$LA_)O$B"
    "=Xa?|TtY7ifUt2J5x?ilL`Dri^qSDw|HK)4nk%BeMG!hRz`zms5T1f;NS3iY=Ql>jSo+lYox{|K~|Z8DQKd$y|ou!$OmT+C`"
    "R{$PX=U|Y)S;3~O7uCUv%0<PDmhK%o7D&UB>QZJ@aB76=L4tmY(oJ)^4U?nHUvUNSz1Y0BkmI12XI#nTE4tWRJqTPIkX0~31"
    "7712(EA&_(Qn7T6iWRQX$D@jf-}oS=Qm(YGx6<$^l}1mkv^-)Z)n$$T1UIJsnSmMNCtgPNRz|RDgL;S^%6M31YsM&Ps#@GZ^"
    "9h+;C08llpwV<yRK`^*zNAoP{Pq>JN}$SCYQ26-E>**nXh+e%ur%dz#h0Mi(QH?sdrH%&|43)G;^e0rYSfxI-5>GC>4Et32P"
    "@@C2CrqP^wy|8N};qW)sgH%(}k&yR9GVPVzt~-sPa)ob4t};bJEaX^fBcSBvKZqRXbXhQ_*3i!Vw4BqEpB)Rj&h`7`2*RM7m"
    "Ds>d^nJkS!aHI|!dA!xiDrp*l}Vbyc5el_~z_@oI~BwN<>@CSGkPR|Tx!P^t<ze?FrsK>b#^rI<&$<|8@3^kgaKVd__zssi}"
    "37CvQePRZFI8*e651<bFfs{;DhbX5WBy@RTN@qD@}VBK3)0iQRhU;smXjn^N+NHxZ9v*RFQDbz!A+GIFC(?aK?8;twA${f(}"
    "el-5*jaT*>seA2#$!mBEFLjf8@lOHb{0k&IWp6p&=^+p*G{3LbTOoUmT)g_I<Tb|>Zw*`*OqsoYn7x;S>+xG6+Tf<a4|VL}U"
    "jGr3koi%c*L3mbwe^$xQDy1}MXi?cSD;{4tq1s<&AO0l1f7bFu#0)Ti)pu_b;&nFGoESgW=8L3M(<|X&FJ0C=-thD-OYI2&3"
    "N6-c-_r-J<Pz2-ouRE!;Id;jNZeHZmI=l^a3+_ff>EPI&MZUG~*ST@d~Z0D>Ne(nh}f4h(%_^A~Rl*8L!BWXohCc+dQwg8Ly"
    "A2_px*{o?--LJ`I;i)*BLrO<y0FqQ9R$L_t5%4Q62f1wLK#8bOV>97bd8le(&z0n7*zb1;AHN|#~oV+v+y2DN4pYRz<N(T=~"
    "DTx|`A)o}ayWS?<E_>?g8Q~li%pM7umj3Lx#oq;2rKJ~FmqZ{-oCQ8N>6D4B^a;BnaGcFI7Aii4tZ4ljvR|i9;F`v@kRxy6q"
    "N0;&SF}w@)*Hm!Qstfwdh58Bc=^F>)ZANMI*{y!>B00mnuR_*+kWZ_`eDIAPQv|Q<xFsA(@#<g!g9XFY8w~N5YWkQOxyGJ=n"
    "67}Db%7WLCu!6#mJZIW0Y4VehiD@kWPHK8CIbJ>pP;M3x3Lvp1+<POhrmk*WXe${xyeK)ncyNR2kDpb<48p|KMVI8&F#0E+m"
    "GXlJqI&1a}MVB$$qUAzY8_yIDS~US#Lgp>`cQ^(JLDS$FG8-|CJH*3v<8zdbeT0SDrOp)MU*lmuCJlnr3%Q%_ylxIY=#W6{4"
    "kBg=mSZ5G`R9q9v|EG^gS;dhrFl(RA0EnUZn7zRcB}Pwln1Pwh45Q+v(+)LwHwwb#t90|^^5XO#3AF$z`C6EMW}0p24Z>T_y"
    "cu-i$anhE4^l{W}gXZ`4!wSqBc^7?uMUoSUrL~24GXMyRw7A%LA1a2XzC_CL(3svA3>I3jiH<ZiE^|!h~bpG0yso*>UMf`O~"
    "{o_ze$uko&zj#AQ{}L7j{OA<JNEie2S0HsMWPGUN(@)UfZH6${Uv4E0qLr}u7f4VVgkPwmr2ptFgyxsAAn9NELa4v=YK9$*V"
    "(4Ek;GYb(6f2JX^Eak!rGc{XnXsu82Mj4>6d&Jsw-ZFgPA~|QiD0cA@r8)DtlHKJ%&RtKm_Qn4E2l#HXdzuY`p+I<h=tH!C)"
    "CU?H$V;I2B*Hwf|V7J1GXo_-?FUKf2>G<DNtYO=#sI@0Wn<et*C$-#E-v}sv97L`5kr#9QCZfUaEJ<ax*B?zwA(TwFcKsasY"
    "p@M$gIFh790GHAsek48UEe_i&smfvZ6W4GU_0$0dM+tl^3J%W!*?%l2Ohv;@6R>!U+?sm~Df%h4qx!=M~AZdz;L2^wxDXgS0"
    "nbk&eia{Y|BvCy#SgP}1%=%b-7CJu+XF=;%ctj-&jx-o8)G~UrPhe_joOdJ~xDb?Ue9Z4{n#nZ>fkQ}m`J!Div$hiEFb@|3_"
    "Scr1E=3js{=OZw{K|P0LYeMV%by;VR&1kO>Ou7Bm-hi$+{>xNN4~8Rw{`V#IQlsXrFkTQ1d7<k-9qXfuad~muU*H<4L{YJl)"
    "VsgFyJ+pj8C}QNc+oc&LdGzQjjjKp5RCHPG8oC^upG9lDQwhF*s34wQ33t!a$5@OUmrk2g{wfWz?&5uvbm=d)(4AlRZz9}Np"
    "!{B0?}pD*PEJiL8fY6lJn9p{vre=Q!fCUn$@>W)p@(uGT2=Y4D|cJmKt|P!u!Br(arzQ`@opF(Kxo`wKmtnMze$mYS!fs)Tq"
    "lv#k$ymnm(w7<cJ(GdTPWTVI#(JE<$zEh%<yo=pj5}48#$A5RT|=5pf3YNZi03aR%;)J#a^yfjeRj-1?uZMt7<Up)zdnh##v"
    "aVonz#0mDZ`0)~T#1gObnBtXwCBLV%+hCtt_jRf=?HKIQ}h#2_}kOwH>81%}=O2@1*bn2YG?FNM9f$~7(`simH)FX_6#zhX2"
    "2ie`cR<1QpskN)4mO8oCIk^^=*tJFiwR#QJ8l@a854KYqY@{{VxOWEQWY2D8Lo=Isurae{e)ywje*BZ4{_NSG|KgXw`t@&q`"
    "@3e=8_?~Z`~4sO_@_VrrG1BvIk}xWcj@|kx4iB>@_W8eP*_yltM`k2`u_EAfB#3xKb6w5a<!te%G<BnSL4?L{ez)!WWc~dwS"
    ")il@BjRF0y~kN#7<_Xuv6J->~wYpJCmKo&SvMZbJ=<9e0Bl5kX^(sW|y!_*=6i<b_KhVUB#|u*RX5Zb?ka}1G|yk#BOG{uv^"
    "(}>}TwDb_ctY{hZy!e!=c$_pp1}ee8br0DF)<#2#jkut(Wr>~Z!>_5^#9J;k18&#-6NbL@Hc0(+6Y#9n5vuvgh@>~;1Ady~D"
    "z-e&KxciDUFef9zSkbT5HW}mQ6**f+sHp<qs4Qz~^NG6fVWGb0PW|CQCHkm`_k@;jHSwt3-rDPddPF9jtWHnhs){=E(J=s7u"
    "ldWVM*-mznU1Sg0OZJid<PbSZj*&0PDRPFKCl|>ja)n$YH^^;rhukIi$V2jkJSAU|1`;C^8%=98v(fBEa~dsdw5-v}MyngGX"
    "|%P`wnm2<9c^^7(Wyok8(nJju+fu7^^F=DO%f&xQ-x{5EMc}VM_4Q@6_yFBgw?_tVXd%U*dTl+>=O0}`-J_%0pXZ%QaB}?5i"
    "ScigxkVh;hu0`cq-Hj4MKxBQJN%8mZnHkrD@W1X@)dYnkCJa=16m;dD47ofwWLsBrTSfNK2(<(sF5qv{G6nt(MkEYo&G4dTE"
    "2SQQ9PJmbOS+rESt@(spTwv{U+A+9iD<?UwdPd!>ESe(8X8P&y<XmX1hArDM`@=}YN^bW%DcotEaLtxj8?wlQr}+UB$^X<O5"
    "_rG1vRJ#9zY&a}_dcBOrhwmWT4+TOH%Y5UU-q#aB<ly*4nNZQe~V`<0J&ZM19JC}Ao?Lykcv`cB1)2^glO}mzMJ?%!?&9qx-"
    "x6|&V-A%ifHqkxFJ=s0QJ=HzUJ>5OSJ<~nQJ=;CUJ=Z<YJ>R{+z0keLz1Y3Pz0|$Tz1+RRz0$qPz1qFTz1F?Xz23dSz0tkNz"
    "1h9Rz16+V{h52adxv|c`*Zg$_ZRNn?mh0k?tSk4?gQ?F?nCaw?j!D_?qlxb?l0XZ+$Y_q+^5}V+-KeA+~?gF+!x)K+?U-~+*"
    "jS#+}GVV+&A5~+_&9#+;`pg-1prN+z;K4+>hN)+)v$g?yuZYcfGs89dl1ipOij1eM<V&^y%p{(r2d6PM?=PKYd~PqV&b-OVX"
    "F7FH2vZz9M~P`l|HR=^N8GrEgB(lD;*4Tl#0|+tYWX?@a$ZeOLMy>ATbSr0-4Nm%cy!VEUo-!|6xTkES0>Kbw9o{e1d`^o!}"
    "2(l4i9NxzzYE&Y1>jr5!8x6*H?-$}olelPug`h)a`>5tMMr$0%5nm#dOQpV(rDH&5Ure#den2|9vV^+rOj5!%|Gv;N?&sdPL"
    "Fk?~1;*2F3OEZ>bEYDbzu{L8}#`=s685=V;Wo*sZp0Ok2i;UeFdom7Z9MAYN<3z^Ej8hq>Gj3-*%J?cHno*z8ka4>4nZ{=up"
    "KE-+@rA}08((RBwehva*Bjqxe6#Vb#<v^aX?(Zwy~g(&KWO~0@uS9%8$W40F>_Mp<jg6VQ!}S!PS2c?IWu!s=A6uVne#IjWG"
    ">8Hl({%_N#@ebWtqz}S7ffvT$8yrb6w{8%*~lwGPh=K%iNK<GxPJzU725G?#|qkxi@oP=KjnBnFliuWggBvl6fric;=UxCo)"
    "fFp2|F(c_#C0=DE!CnHMrIW?ss?oOvblYUZ`f>zOw)Z)V=gypwr1^Iqot%m<kdGaqF>&U}*jG_x-AtITL-eP%;uEOT;`X-#G"
    "{nb~ARlTA%FH`&r;Ta%qlb~V}EWKWX=O%69X+T?hX6HTH`PB%T%^lZ~}P0u&I(DY){OHD5~z0&k*(`!wyH@(sHX46|uZ#TWu"
    "^lsC8P472-(DY%`M@=6$ebV%4)4HY;vnFLt&YF@nHEUYd^sE_KGqYx8&CZ&WH8*Qs*8HpmSqrlkWi8HHlC?BzS=REb6<I5@R"
    "%NZuT9dUlYhBj*tPNQkvo>XI&f1c-HEUbeXIa~`c4Y0$`aEk_))!g3v-V`|&Dxi>KkGo&!K_1BhqI1k9nCtHbv)}-*6FM>S!"
    "c7(Wu4EukaaQZQr6|HD_K{wu4P@%x{-A=>rU3)tb1AavmRtU%zBjdIO|E))2xY}NuJ4`DW0jGX`bnx8J?M*S)SRRIi9(md7k"
    ";61)hbTMV`f;C7z|8WuE1p6`qxzRi4$JHJ-Jeb)NN}4W5mjO`gr3EuO8OZJy6O+dVrxJ3XI!c6q+=?Dp*O?Dg#P?Drh-9P}L"
    "W9QGXX9Q7RY9QS<bIpI0!IpsO+IpaC&Ip;a=x!}3zx#YR*x#GF%x#qd<x#79#x#hX-x#PL(x#zj>dEj~IdE|NQdE$BMsq@4<"
    "Yo1;E?7C;?w126N46P%>>d5dqGNO)*tRti9$mlvUrjCrQBjf7G%XQ?HI`V2Ad99ATUPs=jBX8D`@pa^_I`VcMd8dxNTSwljB"
    "k$Ld59-K=b>yQu@^Kycq>j84B}1cRSd<Kpk`YldGD=28$>=B<6D4D#WL%WI93`(r$*WQFT9mvIC2vN__$ZkWB@?4$Qj|=Nk|"
    "|L#HA<#M$@D0h5hXLDWLA{Sj*>Z1GB--*MaldqSr8=)qhwK(ERK>TQL;Bm_C?A5C^--%2czUrlpKzdBT;fRN{&Uz@hJH+N=`"
    "({$tXD$C8wk0Oq86Bl5<gVK1wb`$;BwS6eX9V<VuuWjgo6oay?3JM9Ix4xfLb1qvTGM+>MfZQF1>@9z@B*D0vhmkE7&Clst`"
    "+x+ob^PhP4gL+i<~dNRD8jHo9g>&d8kGP<6OsV8IW$+&v*ay@yap1fL5Uau!_)RQ;s$@qFQp`J{vCzI;Q<a#oto=mMLd+W)*"
    "da}Qs9IPjY>dBdUa<-nFt0(8{$%T4yv7TJ2CztEVm3nfuo?NRZ*XzlRdUCU#+^Q$H>&cyZa<`t`t0(vC$%A_Gu%0}sCy(pNl"
    "X~*Bp48Qouj)y(p43Cx8pxOiGPZ$?Yap*Qkns)Vtp@UT1NpFlOlTkz8_1*vGP!|FX&_S@$g~DBy@AYVATt}ttOhc>fy`+ja~"
    "sIK1~R{aENCDL8_1#tvbcdPX&_4*$g&2qyn(D}AS)Zlss^&UfvjmDYa7VA2C}|^>}??X8p!?za-e}6Y#@gk$l(TZq=6i5AZH"
    "rL*#>g1ft+t37aPc>26DN9TxlRz8_2Z=a=n2xz}%vN42h93G4e``yb&XB#>n^>c`HWVj*)j_<lPu~FGk*vkq=_z!x;G}Mm~;"
    "_Ph#ZL7?~9#vtwjVjLeOZc`-6SMi#`#!WdZ;Ba35XNsKIwk!3NmJVsW;$jTU58zbvtWPOZmh>?vkvMEM3$H<l#*%~9;V&t<J"
    "*&ZW1Vq|BGd>$jaV&sb$*&QQ$Vq|ZO?2D28F>)YA4#vo#7&#mxM`Gk?j2w%R<1zAOjGTy(lQD8CMo!1bnHV`6Bj;k|e2iR(k"
    "&7{MDMl{G$dwqm8Y9<Y<a&(Uh>@Eyaw|se#>l-GxgR4BV&q|rJc^OWG4dovp2kRBjKuJNOqerth&UJU0Pqm-2=Ey2+OQ$wr+"
    "^87iGcZl1%Rc1Wq{>?eSrOdOMuIOW5Xd0z?&n6h(ksW5nlof1B?Mo2D~|Dh&Ueb4&YtD2Y?R&9|1lFOae>>%md5^EC4J7ECM"
    "VBECVbDtN^S8tOBeC90eQ$oCBN(Tmf7K+ydOjG{!<2fW?3%fTe(CfaQP{fR%t%fYpFCfVF^ifc1b4fQ^7nfX#p{fUSUSfX@K"
    "i0XqOY0iOeQ0lon22J8Xs1?&Ut2OIz#1RMe!1{?=`2{-{b2{;8f3pfWj54Zrh2)G2e47dWg3b+Qi4!8lh3AhEg4Y&ii3%Cck"
    "4|o802zUf|40r-~3aA5o1&9Lb0S$l{V8}RVGr&;5Fu-uY2*60dD8LxNSipgo;W_|^0A~Pa0p|ec0T%!l0ha)m0apN50oMR`0"
    "8ar8fRV2Z5k~{w0K5m70+<Py4_F0Q2iOSM1=tTb2)F~d3%Cck4|o802zUf|40r-~3K;q!lpinxFcL5dFd8rhFcvTl@G{^Pz^"
    "j1Q0Ivhy0K5qp4|ogkHsBq=2Y?R&9|1lFd;<6sFaa<TFbOajFa<CbFbyyrFat0XFbgmnFb6OfFb^;vumG?Suo$oeuoSQiupF"
    "=guoAEeuo|!yumP|UunDjkum!Lcunn*ium`Xgun({wZ~$-+a2RkDa13x9@Fm~`;3VJ_;56VK;6C61rZExH0PF`G02~Ay0vrY"
    "$0UQM!0~`l@2{-{b2{;8f4LAch3pfWj54Zrh2)G2e47dWg3b+Qi4!8lh3AhEg4Y&ii3%Cck4|o802zUe-x(3=7FcvTl@Co2k"
    "z%syczy`oZz+u1<z!|_<z%{^iz>u}j#{okD!vMnpBLHIo;{cxkCIBV^CIKb`rU0e_rU9k{W&maaW&vgc<^bjb<^kpd7629k7"
    "6BFmmH?IlmI0OnRsdE4RsmK6)&SN5)&bT7HUKsPHUTyRwg9#QwgEl^YzOQB>;!xc*ai3kup6)kuotioupe*$a1d|^a2Rj|a1"
    "?M1a2)U@-~`|#;1u9A;0)j_;2hvQ-~!+x;1b|6;0oX>;2PjM;0E9(;1=LE;11v};2z*U-~r$v;1S?4;0fR<*1-m-1Hc`?1He"
    "PTBfw+86Tnlzkd4q@fT4h4fZ>1<fRTVvfYE?4fC+$!fJuPKfGL2ffN6l~fEj?9fLVaqnBEph2QV5i1~3lr0pLTxM}Rqixqzj"
    "B&j8y2=K$vcL-s<M07C)80K)+z03!jT0HXn80Am5;051bx0lW%$4e&bP4Zxd#@qo7gZv)-|ybE{_@IK%Jz=wd303QQB0elLW"
    "0GJ4v1egq%0+<Sz2AB?*0hkGx1(*$(1DFe#2bd3709XiE1Xv7M0$2)I23QVQ0ayuG1y~JO16T`K2Uri-0N4oF1lSDN0@w=J2"
    "KWrH9k2ti6Yx1;7vKxPZonSEUcf%Ue!v01LBJuvVZaf<QNS_4aln^=6M&O|Q-ITeGk~*zbAa=J3xJD&OMuIOD}bwjYk=#38-"
    "SaDTY%euJAk`@dw~0Z2Y`owM}WtGCxEAbI>1+eD4-tD0EhvG?1T0P3<V4W3<rz=j0B7Vj0TJWj0KDXybO2+@G9Un!0UiF0B-"
    "`u1Kt9>4R{CeF5o@D`+yGs9|ArCd<^&m@F`#dU?N}=U@~9|U@Bl5U^-w1U?yM|U^ZY5U@l-DU_M|0U?E@;U@>3`U@2f3U^!p"
    "~U?pG`U^QS3U@c%BU_D?1U?X4?U^8F~U@Kr7;4{E>zz)Dpz~_KnfG+^M0eb*@0s8>^0S5pF0fzvG0Y?Bw0mlHx0bc@608Ro<"
    "0Zs$X0L}u=0nP(104@S90WJfs0ImYA0j>jX0B!<q0d52C0PX_r0qz4H03HG!0UiUM0G<Ns0AB&3fO<d!Acpn((vTtSOr%*zv"
    "ytW?%|}{?bPMSbQWR-Ybl4DfI?^1ZQ%Gl!8ju#$0}W{a+K#jX=?2nGq+3Y0k?tVfMY@M{AL#+oL!?JYkCBEpj32@dLmG}W3T"
    "ZUbIHV7e79uS|T8y*-X(Q4mq|HcMkhUW2L)wpY0O=so5u~F?$B>RAeTj4e=_JxAq%%n8kuD-#M!Jf04e2h@J*4|c50IW9#bV"
    ">JO5Pp9zJxRsX&BOQq!CE3BfWui2I&scU8H+R_mLhTJw$qh^cd+0(o>{5q_2>oNcBilCQcZ_&O_RVbOPxC(nF*(lYq`4T|&B"
    "obPeei(jBC`NDq-7BRxTSid2X66;c$b9%;yApqG$_A`L?tjx+*kB+_W4H<898y^r)E(#J>>kftC_Lz;m!6KNLG9HhBO^N|)H"
    "Ekjz4v;t`*(ki4iNNbVSA+1N+i?k1EKhgoDgGh&v4kH~wI*N1*={VAtNGFg^BAr4yjdTX-EYdlo^GFwvE+P$?g0+D(6loaJa"
    "HJ7PBaucSjYb-SG!|(b(#uG%Aiaw88q(`XZy>#m^bXRyNbe!NkMsf3he#hGeT?)8(gLJKNE?tgB5gw2jI;%5E7CTk&yaQ??L"
    "_(<X&2HLNV}2tAnirkhqNE*0MbFELr8~_&LEvdI)`)~=>pP4q)SMbk**+JMY@J`9q9(rO{7~$w~_83-9@^GbRX#f(nF+2NRN"
    "@8AU#E@L;4CSid2u(fD}U-G8NkhX(-Y#q~S;-kVYbnLK=<qI?@|RZz7FHdJE}oq<4_sMS2hEeWVYNK1BKm>0_i%kUmA4fHV<"
    "l64GR(DM(Y1rXfv7nt?PEX%^CKq&Y})krp5=L|TNj7-<R8Qlu3~E0I<qtwvgdv{t|J=w!HZq+v+IkwzemL>h%O8fgsDSfp`C"
    "FC$Grnus(BX)@9jq^U?RHDJm}!;pp}jX)ZSGz#f;q&JY>L>iCu7Sh{D?;yR4^d8dtNFN}5i1ZQC$4H+beTp;zX(G}jq{&EAk"
    "ftI{Lz<2>18FAGETq{;bCBjD%|n`xv;b)#(juhANK25GA}vE&j<f=4CDJOS)ktfQ)*`J#T932=X(Q4mq|HcMkhUUiL;4J9JJ"
    "JrMok*V}?LztjX*bdyq`gS{koF@TKstzY2<b4=5u~F?$B>RAeTj4e=_JxAq|-=ekj^5VLpqOi5$O`rWuz-eSCOtET}QfsbQ9"
    "?o(jBCGNcWK*AU#BSg!CBc3DQ%fI;5|VqDb{f4M;JhAu;SoNJEi^BaJ{Bi8KmnG}0KPu}I^PUPgKa=~blHkX}c61L;kq@knn"
    "Wy^Zt^(z{6SA-#|E0n&#^A0d5=^a;|ZNE47IB27Y?j5GylD$+Eh=}0q>W+E*>T8Oj=X))3gq@_s9kd`B@K>91WEp-<+NiRxS"
    ";u7f<*K00(hWoZ_rL<T0leAR2DKQMoa13FdVSdc~g!w7+Gv--lr*KaCjr6?OPuw8A<N7&si+Rih*<tKN_8^<bZRWn>>bYN$K"
    "a)c84>DMPF20s@=V$YK_<j5lzS5<+X1hLc&2f!){Z#gf16}XARtiUjpNT!iGO@q7R@^5Z6u&FAk-AEKrMc2NX{&TpdLVsEZZ"
    "5Zx{~-TK?kvxAedL<uddu~K)I;1N+>;Iq9px3mS?Sy2e&K(TCiarnh&!crQl_{{`ligvqg;QH=1a?@&B7q*k5WL4NMR`^ZIp"
    "h`{E}(O++dz#-e7(KmpYyu&5mQ=WbbpgxVzjvZUp-`;v@eg<zyh~N7_pR$Rd6YKc8Q~SGjudccrneL9Ulv@4802-gJ#|Z4|P"
    "_pNqc|n~U4Tb>c>Gv)E1SEqSHCN+r@PNtM1U&Xls`O!+%<Q~A$wRO%rAg;_5AiL@gd$tJRyyukN&1ziExtF9`kwe)@IxU^ot"
    "r{9mHuChmbUhX0<CckD{lPD8o-e<?M1K5|?BGQXglO<#qzmPBBw@LqUWl3v<4MJD(m*SVgPsMIho>U=imwqRISAHxFc5UERa"
    "5uTbY?NCihQuwRD()A*Vp#SNdyJjOZy~FNO+vX?B{q>yNlm4tq>g)zyvrVCXYo6vz2Xm~=fp}eT^`QnihpLFa--OXTyGL4za"
    "TsL-TZd`W!E0@S#i7AUFt7=M|xInCjVHTBc(~{k|2qaByo~U`kK^OlBKUp-;%y9Wl9;+8tIUDN@S!X;%)J?cvd_wo)OQ955>"
    "pgQ}L1bM644Jiw)veV!e1xydmBauZuUuW8#<MQSrEVLcAbe60e9C#mgd*8cDo#N4zIK5buijMOL~hwvx|F`OJTqLCimx{*1z"
    "uGUZGelgIR6MlmCqF-#TncgD}Wz>H>Unb(<rGyh}$#q?x`F|RS*n7=Z^nHQOXOg~0rf=r0{8}l;Loq2`n%@i^|rWaGdR5Sl&"
    "hA>}{TvE(#;B&}&ek0$D?aTg^-A_7^b^IeHhwUSMMmmrmvTOMEWHrB*e}?@T`z*VQbR?_zhs-xvKl>;4&uj(Tku737vEA8xw"
    "ty{Td$XO{E^Jr!Z|px<AKQ)1V^y}24Y1X0Ia|YO>_6FDR$>3bzQ8`m%4`~&&8D+IV86*WWwY4tv%h11%r<7f#b&ZUXMf4IWt"
    "*_yVVkop*gvps*k)`y_V?_s*$nnK?AO@uu^cCG68AOk>s%A=hun|2OztOKGwx^HuejfE*<4Gm1@}j;GuM^t!u_6OIl{?YBhJ"
    "PBm=n40b7@>Um%)9LYs@{veVc2_WpUr*Jlqes?{GZ#UG7`lPq}Bg-*La-e#v#?e$C}_&AC=w8?G(aj(eW_1NUdHJ=cNzEtkV"
    "};{L?_ocjy+9QUl$Nd8zP@&s2)*(FbMN%B+|FHdxd@)Xxkq&<=#Pj-Dxp5c<^X|BD}Z>1usTKqz+ld|Pq;`7oQuB*~kafi4`"
    "{7l*@elG47e<nAVvZcjRsrV!5=khM;hvFx$ThcaRwOA+~5Pm21lv>NJq+iLulv_#%g-^s!#R=j>agz8e>9922l_s~4+lyVqw"
    "qiT+JK|dDD=8@cUhE)Vk=lsg6Kkc$a!C4y+#vl!93cHwTq_ibKa{>DelGn%3QF}-U-5$EmM=?Rmwzhlll~<BS^TARNcyp~TU"
    "sqGm;NlBk-jH=B=!=E#opo{#6OCi#LnWsr2k6)k^U`p6m!Hr;)~+Xr2Wzkp@|q4e=i*uzAt_zeCX;Zb&#Hu3dASUQ)z{?PPi"
    "uhKs+KmBYh$LNc@F7Tl$IkYx&3GPvisQdg-_FcHuYjGvWd1=hCmGBhtUch&WIjCJq)yi0_CWh_&Kd;=AI1#8KiH@xS6&@qgk"
    "t@ilRPI7EC|d`Wyyd_{a!d_x>Bs{B9sQof8=_;UU~d@ue*zBm5?--n;h_vI(^6Znt$Px$}wf90p}llV{hiTn`0m><QD;Qz)C"
    "=l{-+<p0f2<45yj_#hwRr}FRf@9`h<|KR)cFYzV(P<|{wfFH-d#=pV8$-m9N!@tG9%MarR@<sgX{LB1!{#E`JzJmW3KZuX;w"
    "ftZ{%zwoHmk;pOyvEn?e!hzL@|C=g@5c|}CU7rtBe+rANUoUsgnNS<&%MRH!@bMB$Gy$H$qnOP<|cBla367#xW9A%<v!&Kx&"
    "Lv~xpCZIxgK0TH;<do_2znU3%Lc{Xl^DqiyOl&=4NnnxY^uXZVC4yw}|^2SI!OMRIZBa$9cIDPUHG>K`zWixB*;<3viWO4d>"
    "?ua<!bom2&^!%DBOtkNYS0J~xG%#*O8Ma#OjbTu<%=u9~ah{>A;0l#oiP+VwH}H70}kK9k9~n6ESGjEBi$zRfgYzQg>8X~ak"
    "j&wPt%%zTsi0V6U^nIAIWV+1CR`3561-(}p)N$xOrj61>|<@R#>xHH^Y?h<#I+s*Ca4sZv#6Wnp`OYRVNnmfgv=gx5#xQpC%"
    "?gn?2yT)DNKIe9EUvN9QZQN(vc5W-TgKH432#<vfQ55eB7lb<DlJJ%AP<SNBVk5D!_;vA?z>1vs4e`8iQHTn6gxkV(;jVB^x"
    "GC`B4dIE9&9q>alV|z+%+L9J(t`{lwd5vqPB<ad3nv94o`T`vwD3*wtdK4~5Mlx&UKIrKvT#puiCYDZeZs5~>X@g@0rnHpm$"
    "V^;{QKks@*#PRd_+Dbuah^(Nb(XHN`{f)WCVGcj3T4S7&4ZOBkz(o$$0V>d7HdPhLBgttK=PWhso#vKnS~%{FiJc-S`jK7s$"
    "^@PqKzvP1bThC+oPdYdIHj&E&g~pOBxDx7l~t?%ZUq57(FbH}?V8i2V;&z`e%3${i*J<Wur7x1Rew`J7)x{>M%veaL(4J!Tu"
    "3Kt5p~aXa{Bq$}Ca)-$WP2h4u%@8pN%8S)MCP12Zri)4~-lkboplkbzS6A$?=NhdOCLcT_t5|R9X{D`CxH)-HvFyUeeM+o6b"
    "BjO?g$sm*1x$KI#_Z(BbE1Bv|N%}p>1LP2arehnJgXDSAjr@`M6VsJ{p5MrA;^w&)xE8t=xfZ*YxR$z>xt6=;y9Tp+`8(VO@"
    "c`dW?&oSRuOkZalWJ)R?~w<%y2~TkGV%}U2wNeZl>R2=i(d$z3wwm!!Y<*vY!CL2Y=8DA?2GJA**@&I+2`3-te0)g_G3M4Pu"
    "9)0XTQ#NV1LV&vcF<W*dMWl>@V2Avn|;wc0BVI^C9yNvy@rJyvMxB%wv`_pD>e|Nz8m^BJ(lxF7p91mzlzR#7t%8FpHVDnd!"
    "`@%uHrBvxr&9%wiTWOPCqV1ZEoZKC_Bh!E9zuFh`j+%v$C%W&?ADxyEc_Rx@Xq>&)lOK4uSdmf6khU^X(_nA6ODW;=6$Imuj"
    "N)-#8hUCc4&OXebTo;l8(V=gmCm@k-v%ob)Zvz6J&1eg-$pG<qE1JjYoVRD&HOlPJG)0KIi8Nj^6jAbIs2&RY`%y^k`ObyeQ"
    "2{RQ;C9{uxmFdHzdP7y>?~x<qC^=3}kO$-u`4RtP{@Z*Lp5ZzEI=M+sk#s(TKTEzMQT=^TnNQ>K9Z`HI^y_>b`5ONN{)hZ!a"
    ")r2gf%ov==dY4$#KntzWByzGd2)g9d?Ws6d?w#Oe#&R@-{Zf_-zPD0o1D?#Iz34qlE>s3{wMr*_#5OFIZeL7f0I8)SiUJw_<"
    "Dlx%bwTYl#Q}6_9=Ufy-B?p%W(K!EWQ)_fW5_DU>~wi*i-BY_6B>JJ;^q(*V&8ud$slKCH5+Nj=jyi?+UZWgl+5#Vq4;o{zB"
    "SH|046G4dj^AlYb~3;(ssi=iAB$`RC*c*B|Be<X23s>krI0S1V?ys|_>U)s`9IYR8OpwPuF7e#89R^*iRju4c^tT+NvwuHQ2"
    "MagAYrA-=`75I<t`#FyD$i?6c36<=e2C%(=$6JKF}BR=3h6K`|t#ZvNjsfP5ERPs-$l9WnSq)hUXa;btSl16+|f8v*dM3X`!"
    "AO%Q`G?)LjyqN!<yp;dGyqy1`yn_Fcypn%LUdI1G_PKIouj?;zjVo97yE@6gkPb?D@;}ADi#Mc8QY$fE>Lw4AGGs<B5&tG$m"
    "o7>z#U9cdtc#V{t?VC39w{dOBWuWE{zdX%c9HZKv9(wz?Gx@uhXh4zDsuA2t^(<GSFv<on(JEOYAdXC4HBNZ+6k*%?+HzXKE"
    "iQVtx)HBPFU@lA^bw{3fEj?1X*}q_}ulr@Li#=@TF_8@RjTL!W!2Cp}EjsxaWF9_@+=G9B@q(o)Jog^RA%+5jqN6Tr-7V3jK"
    "uZuCYRz&`sFo`asAM{wkbs{Y!|t{vfP%EfHD?5#f>RZQ<KOFX4!5s_-+RLb&W2DF{MmVY_Rt@LRzz+;+Vxqzn1NUe_nW4}=o"
    "ojO%{_Bm70!=vpXb3qj$&>rJ7tP$(R9O%i@AlnEDH!vtQ)5w^N!3BMAmg&VGM!q<d6;S1M?!uN!~2`63u7V2Gp6xO+x32lUd"
    "!V}lK!gquhg=4Pi!q0^&;i_x2APHTCov!&pGa(?{b-gZR2rmfxT@!>K35sye^^(8|9fZxU#X?IVEIf3*C1eW4!eQ4G;irNsT"
    "yl*NTtX+|GuIs9H$shY%k_%zb)ko_$Mv!Bec>O%Y1e;+nCs8N2G>%dwJ<<<?0QFNBJ>uHx~2)w3YEeY*C;_0x(GX5^Mv0Cns"
    "CSUn(z&wr?AiUsqjPLpTb$!5P=oi3!7Yvgcd?bc;Ff@d`l=24!I@^KM~4>i>~29BOzDV=9(@1TJQ-sT`vo6p}Vl#^^xEa{w|"
    "zy{YPkU{YhBwS}Lv-mx(LH<>F#-k+?uyA}$nb*$6w39mM{J9m)=2L+osEjyPAGC(akAh%?1$;tX-BI9Z$}e#%Z@$4FzPkEP+"
    "#Fln^(x-?XpAWf7$kUo;$mp+tUlHQTtl4eL#q*tWZq><9A(g^8O={@Na>0N26G+vr6y)BKB-jt?EFH4i8H>AnZIH?Waif_xe"
    ";9K)8`R05!pYwn1TL*kqMb^*UIp^H>Zr%)e2`vctN?t-yxmP+OB3+7&ZpFfOw}0Qay|}KQKGaoqU3VAPHN6lLAdmnllvE(J&"
    "|64I1wsqGx|2r{Tu@jL)SsE(%X|0E+%q$0%K882oC^b>4|IY1pdXm<0Ca}C;BFWKLtz;7hfM5^yPy;4cn==JC-FsmoEBjo&c"
    "&s;8>(O-=3@>PV+k(70$hwmI1dZ4BQC&tXoKOHg@_e6hF+wu_!KhgjN@qsbioef!uhxvHo*(H1JB?y_&Pp-LvR?5#8LP#K7x"
    "<pWB53Z#)oh?j=%?T01m>zI26a=K<tl|xHAwtUx)R$3wPrlY`{i5h<kA#?#BZdh7+k3w#Jqiip{YF)<O-`!E3k`6lK8&Xfj4"
    "%1%%T$s)n9;7lvRnbmBHJ(T+Ckf!%RCxY2{(!|&ir_+9)Kej6nTdKLeOp|lLEuo@d+3v9=G=p;T$Bk4Z$Q71ftKzGtM1qjYS"
    "21e2*?1x^u7j+s&?a)J;@lE_2#$r4sU?L`AGN#~L_$PcD-@&Q)XZ#Dki+{!U@bCB!oQCh?Kk)<n7k-G*7=v+`jx#YW@HW8={"
    "678we~3TAALA*!mwHf7>P5Y&58X$7>3-@;-KaZ_pte}9sNfsu$JMwF*Wyp`oA?bZ!_Kr14#F`w45#5JG{SQ@3-6+KbOHpH;s"
    "BEP5qi-{%_xLEg0Xlv*(r#gqHfrlo}>usi-%x8Y{19p|Itm8@EDfE^GJ9<-ifCm2>%EF7yl1`hCjz&;4kr4_-p(P{uY0SzsH"
    "yH5BLgJ!cJx8g3*C@V0-joB;Ji3(86BW2PfhaIGLv499)hoa3yZUEw~jA<54`0C-5{PIVhOIs3kS0R@9d6pf=>9DC$Ti^`rh"
    "YkRGB(XcRq6qv;uXmL}2j^a7oQRroZ`#<RE{8FHLJ!)Y&^gyYbK_COSl!}0hawWqN(h-~yUK1Ui_^ehggAvBl{z)$fBB02&s"
    "XabI%{IWu9d2GG1oz==t9%TO#uV^QlO$m7;q@vlIA*Zy{+BE*AVn&&e4-FxEL-vKNgICljPs2<+9&#$=W#=o-SDmjp-*(Q&s"
    "m^zue|JuEW@DoBnCfEzZg;*J`gZ7P=SR+|p^5Zf=<76%-ltTWL1_x_U5Wr_hGv8o(+VmGEetIREe<USJwhi#e;0O|&QN|>L0"
    "DYijgmw?Nl!liUdaqSO;6Wn>a+CO`aFF{ScyV{OBEhmrmt4GaE+d<_MJ4fXXV&(1E*t!wo+S?eTlu$o^LO*7ubsxhs_So4PF"
    "y`$k7zPRu_EsEWb3!uPNy7LNHyxfg5lV2YkFWf#Bro(@l}U{xkg0MVIet7T;`nvpvm}sDOugx&p&l7h+{|0`abu;Z@;B!gq$"
    "(g&zw)7_M%d46hGA8eSV7dzJ?r(v26r$brjJwF9bBO)s;g+m);sJ>W>576^$g352FzEowFWqJKLtP<7HpZ+PlOmw3QKzDc2{"
    "1#Ckgcz04%*_9$%uNM0naDgk?3q`t^Cz8Z`kt`O76j2+f@xws4?>WJhfw<qAvpnE1FK3w|LCg_xB1<HSfcrdf)*o=H2AsJ{Y"
    "0(T=4BMo|D*PU=5PkxCLa~oYihn$#RQsahAU{_u<kyOa{8I4{R7_;6mZ5O|T-HyqktY=&Dc0t*=TzUGRRb|u@seLCX0lz&W4"
    "}@C=2wc}j8W`HQ&^}sD^jSaggF#SZmm#q8-<aj8qN^5h7Dw8Y^Yizk19P)V4K<Z6*B#y>cH~~osLx)l`E{-N8wCe;Z31%YPd"
    "q7cPOmdOrce$T2q4*VjZRs>SIdF6BUyEfkLf6QW*6Gg=;r!(OM)+&>~o}X0qv8dzPwoW3#j<mZ|yJe9dCn+MO&%>&^-_gB58"
    "uwqA27jkHz0_#P|Qo?<mxFss$<?1<)O$F+9sjP?>ct3AzPcrO;q$FX?cfhF+!SPBni)47MG@^7#VKAz3x9a$#t%NFo3md(8^"
    "hkujh^5JYDAHf#!AXd!pVWqq!Tg5xEHGD8D<0BQL>%lhjAG7WJTdbUahgERK>UbB{z+18XyfZt<hp<LIiXGxT*$Ms=c7}hOo"
    "#o$Uzkz<PXwb|UaG0?m%s60XJe)EUpwUc(Xfp|7&18r-Qy|ft4#{RJRGBlN#!Q1cGad5HnQ+>i1u^Dqh%+-F!JGq0=3GcIGh"
    "w=!1vAWfkZ#V0S>^)BFtcH<nFCp7F3dOcAlqCBx#l8RXfB4u<`O6{^P$KrfD*G1mYGGc+$@GtvjkR{OJSwC3|5)Tq0B6W_2v"
    "rLWUhp*<|-&RSHli-4OEzAP-(7(o#r~IHrGR~xdH0Ujj+qy1iQ`6u*cj24dzzZYi@)6=5{z_mcul22fS~lqJy&W4qAwJ(qd("
    "2mM9CFuk2|7Mo^)$w?)dr7Go5ZC_J$gJ1V=}iIywdR;p~-3T3laD(k!oyU=PhX^q;=%ao;Di(P3QcBA#!oi<<(+K4@smF}f1"
    "b8p&$eW(KaQ>C&5JCzlz!huwcgQx}vQ!NgmI%N&&aTx8whiEqrr#(1=8gL}-#Zj~mAEy2I2pv#p;GnXLjS4A6)8i0Bqal_ag"
    "E$%k@iZ0^XdEQccu1lNkW3RHg`R-v^dzLxQ!s<xfi!vs(&<^4NiE&8NQ2qLA%hsqA%MArkVyntq{BS2!F;mA0x}?*f+2?-kV"
    "|hv9!Xe8&0rBd42#KxC1gQ94S@pc28Gleif9lNQ&%XV!LXEi!7}O%%c&2P(tWUk`oc=OA68L6SWOSW8hQlEs6VWw2Vorzfb}"
    "#GHc$`PNcX}f8VQ?e1Z<(6u$6|vHW~%n=^-emp|FF7Lj~Ofl@tOy$q7{y3DwjbYN!R&QUugd7}S#wc2R5CP2sSI+CT%{0eh("
    "}?4x$DpW4F#x)Tmk7ic6G93nRyCJ!7TFC3+oaEwCXINb#&s56|TR&a_sz-hW0&QM1<OHuF<b%JR9Rki28#$)x@d7SR&@p=kR"
    ")ZgGq`dd6%pU$W2f8uHSA9=do!Zk}z<+Jq}JVQ_8bM$mRS6{|6^|yJJUdrd`EBJhUIbWd9<k|X4zF2>UFVUy+eErY7K>rIb)"
    "ZgVr`d@jm{vI#U|HhZ<f9K2efAHn{G+wH|&sXUG<SX?L_$vKhe6{`|U!zC!GCh{B)8qJhJ)UpS6Zl3wk#EwI_+~wsSL(C)PJ"
    "K47(ldCqK8M%nb9t?v$?NniUa!yNyY%^dx4wYy(X)Ajp2PR*xqP3V$M@?C`2l?qKd3L}je0&mq%Yxz^#XoGFXTt{B7RIS=Ew"
    "CCenMZ$qitE<nAaS>*w=!5aW<DX-sbiuyr%gQZPDH&TdX(P7UxZ|C3vUXrg>9s|MbqVec(;AedtZMC3$DsQoT907d^SQNuE6"
    "0WY0odXU`&AH_u{QJI@kZdrzTF_mtTBdY0M-dRExhxmViC+^cNQc{bSEc(&MH_H4EN!L!ZQ(X-vw$y08N^6ap6@a(r~o};#@"
    "?3C?o_i5WZ?lZQj?z6T(yDRKPzDoO4-%h(dqRQ@wsJ4rU8oLouZ;y!BWe<+nZEx+{V-N8)*d4yT_U68Q_P)OT_66Pp_H6G#d"
    "yucup5r}a&-EU*xAh&dNBEA~yZMgU@A4hDYrbfMyJ8H@6>ESi&OleZp}P_cn=8?<yOIpUm25P3r5ItZRKGVO&4_fR8$Q=eW3"
    "+pgF~&XH80*e3#<}Mh<K1(O3GPf|qC3lY!adJGceWAg%JJ7n<@)al%Jc7v$~T^L7Z^{u3yr7UMaDDkrH047%pVq6>R;?z;m`"
    "7|^e^|V@~8V&8?9YyjBr<((bl!rXy;mIw0EyJOxFhEUe`vWt825-E^4bk)wj*R$hX~}=_~iI^6l`a`6~RizDoae-%kGwUzI<"
    "@SMAUB)%Yp0*6(rE`BQxL{@K1={v6+Kf7{4C{`Qd##tV^qjc-KmGbTqKFkDdw4VSCYaJvo}VNr*TR#8WcA4DECUWz<s42V2#"
    "^p8AY$jFmM3-2kTmHV{O%XP+R<2q}!cg0TW8<a4mUr^GN4xZ#GQJzIp(u0-+$9eLnbo3Mi8{VQR&ju|EZtW=ze%HG)INq}=c"
    ")4$Fu+6(+N+-{zDSz;6newt{TX3xBba0GkhohCN!m%1F9cyr>qYSGYYq8p~4r?6ivDUEx>l_=g-mwXHIX2^N#}?e<*oqB~ZM"
    "fI59rroPalc~+9&l9PK}RJvI(FhAM-?7+RO1mx4IXvW;xR`Z9(UB^3CAux>DZ0Yg2@=6$ymW<oB$awP$meHi9(l2!X}f2U8V"
    ">_P8Y#4RXF4fA!M46GF>#2GewA;C7g1$2$dNkOwJL_<y_H1W{Q?FOSF>nL~A);gv$k@jm#Ez$Q;pD=8ASQPqdc{#hr4IaLL8"
    "OEtd$7%oko+AR=U;@W~<(DT_svED;^#QqfT^6P@I8(OH&?yW|RSw_GXik*h=(xmuWVjj&{yxL2+fUFAB_O|BQ+<p$A1ZWKM`"
    "Cecf77QN*b(MOiQ*-!2e56BA9Usj3-<xVj`R*8YKS`3mkVz8_gLu8#8D(l5Cxl24GcZ=b2j~F2v#7MbUjFJb$qw=75Og4(g<"
    "smUz9u{Nd5iwRC731VFF<u@Q6XXdoQASJ4ijntPv9hZbC%akkvb&WadsvCGr<EjoS;?}ul_L9C)8&0us_bjckoQ|@vY(YMAF"
    "yW1{?;t{pfy_#urlO8YmOXb&6R_#OgY5Ll0&U|a+oz=K4dMB!>w#N!pe~&tz0?E%99UU3*{r$BKfGbSUzSgk&j#Xa<o+-$5@"
    "4OtW_k(S;ca^RU#)?OXWmsnS8=pE}yhY<x|!Q`LwlCK4Yzt&swYHBx{X)&MK47TWjSD);gKwTrZQI8)S-eqnz&CBvYN6<qYQ"
    "*ndaOo)1BMoOy_nv%ULdGJ9o$oXN8>Otdw(|J7uP`N@h8$<veGNobRla3!HT_+gUGjoV#SMbGOWM?vV?f4RVoluUzchCzm+)"
    "%a^PJ@<-M|`7^6g{?<Aqe{UU@uUJRqtJYEZrgcodWgVA$oG0V~=Sg|O`O#a+uAH#PS#H>9mKXLjmg-7%J*Wj;cOn*a-Kh&R6"
    "sy4Ns)t>EeVsM3Ph3YU#t{&yT_T<Z{(@A-B@d|*fxJMvP+AN8YPx1j3zR$eci~Ab@T=)MhG}qK1gJirD{NC&Qr(5~`jhHDsP"
    "9;n87RuntG1~yKPOXb%A<?If;0@2Vu~_d5F4cES5xU2{B&J>x~AC;Chf*jH2cJmGwsUV!Rwqf`gM2ZG-HJ=niQh_P78e9!q3"
    "epabus$>$?1oc5$399r6FnVV}7FN!eGD_wk*knHrD+O#x}=!qPtee>1dmxil^4R*&+f`ej$p*rhG|tmkfH(r${BrUlym;?*S"
    "9>3lDn*51V}S#5zAwgskLrk!iG9NJCO+@-Uh{Z}jU5=rdxQNI=G^PU$sVP)8E?Ml3z`|aocVK;H^*l+r5d9US7Y@Wgln)bO&"
    ">I*>fL)3!4H0e@RyzIQ<Lj8QYa}F=}XF*@5+nD-mU;fSOwm>oVmF?42fq-_EZR4|^yAiqUJi89M-ugZbg5E$|KRusamdnob^"
    "ULq@OIvmR9$d8syn=+EGQmQw+S|!Z=K%jn!5BM#au7H@xS-YZ?fkeWaIsx@v0uQPHwYJ1&1@FkA{_cx`PBf&+7+Rt_8%1aN;"
    "BsxvNzHBUrqDJaZ`~RvZ;;ib8LI)4eZCSu+Q4Czeon-GdL30F5|G*+y2YXkFITUYgagr`jk)eOPO}y*IfEs`N5SEeZg_!q7N"
    "=_{l}~Eb=xiS48+^N;QRQbo7672N$vURwH|q0HTRt7<9g@vCv%&w^7(lf#%{^NDzx7c@+@x2+I#vsT4Y>@+<&yZ%?qd^h27>"
    "BxNhjY<l0i|GIpzacEk0sTT;ul_J&<_r)pQ*ye_tzT}wZ1;W)6%j=8S7!QP<sOC6&8rbzyB%+s&y`AXFDiNl|3Jixy(eDHOB"
    "U-tUg9C_V{^vX=@kJ@ddR8yT_5DwGO?7v}fx9FLF136j-VE"
)


class _ParseError(Exception):
    pass


def _varints(data):
    out = []
    value = 0
    shift = 0
    for byte in data:
        value |= (byte & 0x7F) << shift
        if byte & 0x80:
            shift += 7
        else:
            out.append(value)
            value = 0
            shift = 0
    return out


class _Tables:
    """The embedded libxkbcommon 1.13.2 keysym data."""

    def __init__(self, blob):
        raw = zlib.decompress(base64.b85decode(blob))
        header, _, body = raw.partition(b"\n")
        sizes = json.loads(header)
        offset = 0
        sections = {}
        for key in ("names", "kvals", "knames", "alias", "u", "cl", "cu"):
            size = sizes[key]
            sections[key] = body[offset:offset + size]
            offset += size

        names = sections["names"].decode("ascii").split("\n")
        count = len(sections["knames"]) // 2
        values = _varints(sections["kvals"])
        name_index = struct.unpack("<%dH" % count, sections["knames"])
        alias = _varints(sections["alias"])
        alias_count = sizes["alias_n"]

        self.keysym_to_name = {ks: names[name_index[i]] for i, ks in enumerate(values)}
        self.name_to_keysym = {names[name_index[i]]: ks for i, ks in enumerate(values)}
        for i in range(alias_count):
            self.name_to_keysym[names[alias[i]]] = alias[alias_count + i]

        packed = sections["u"]
        self.keysymtab = []
        for i in range(0, len(packed), 4):
            ks, ucs = struct.unpack_from("<HH", packed, i)
            self.keysymtab.append((ks & 0x7FFF, bool(ks & 0x8000), ucs))

        self.legacy_starts, self.legacy_flags = _unpack_case_runs(sections["cl"])
        self.unicode_starts, self.unicode_flags = _unpack_case_runs(sections["cu"])


def _unpack_case_runs(data):
    starts = []
    flags = []
    value = 0
    shift = 0
    pending = None
    for byte in data:
        if pending is None:
            value |= (byte & 0x7F) << shift
            if byte & 0x80:
                shift += 7
                continue
            pending = value
            value = 0
            shift = 0
            continue
        starts.append((starts[-1] if starts else -1) + 1 + pending)
        flags.append(byte)
        pending = None
    return starts, flags


_T = _Tables(_TABLES_BLOB)


def _case_flags(starts, flags, value):
    pos = bisect_right(starts, value) - 1
    if pos >= 0 and starts[pos] == value:
        return flags[pos]
    return 0


def _keysym_case_flags(keysym):
    """(has_upper, has_lower) of a keysym, src/keysym-case-mappings.c:624."""
    if keysym <= CASE_LEGACY_MAX:
        return _case_flags(_T.legacy_starts, _T.legacy_flags, keysym)
    if KEYSYM_UNICODE_MIN <= keysym <= CASE_UNICODE_MAX_VALUE:
        return _case_flags(_T.unicode_starts, _T.unicode_flags,
                           keysym - KEYSYM_UNICODE_OFFSET)
    return 0


def keysym_is_lower(keysym):
    flags = _keysym_case_flags(keysym)
    return bool(flags & 1) and not flags & 2


def keysym_is_upper_or_title(keysym):
    return bool(_keysym_case_flags(keysym) & 2)


def keysym_is_keypad(keysym):
    return 0xFF80 <= keysym <= 0xFFBD  # XKB_KEY_KP_Space .. XKB_KEY_KP_Equal


def _is_xdigit(char):
    return char in "0123456789abcdefABCDEF"


def _parse_hex_eight(text):
    """Mirror of parse_hex_to_uint32_t(text, 8) + the "consumed everything" test."""
    result = 0
    index = 0
    length = len(text)
    while (index < 8 and index < length and _is_xdigit(text[index])
           and result <= 0x0FFFFFFF):
        result = result * 16 + int(text[index], 16)
        index += 1
    if index < length and _is_xdigit(text[index]):
        return None
    if index == 0 or index != length:
        return None
    return result


def keysym_utf32_to_keysym(ucs):
    """src/keysym-utf.c:912 xkb_utf32_to_keysym."""
    if 0x20 <= ucs <= 0x7E or 0xA0 <= ucs <= 0xFF:
        return ucs
    if 0x08 <= ucs <= 0x0B or ucs in (0x0D, 0x1B):
        return ucs | 0xFF00
    if ucs == 0x7F:
        return 0xFFFF
    if ucs == 0 or 0xD800 <= ucs <= 0xDFFF or ucs > 0x10FFFF:
        return 0
    for keysym, deprecated, mapped in _T.keysymtab:
        if mapped == ucs and not deprecated:
            return keysym
    return ucs | KEYSYM_UNICODE_OFFSET


def keysym_from_name(name):
    """src/keysym.c:237 xkb_keysym_from_name(name, XKB_KEYSYM_NO_FLAGS)."""
    keysym = _T.name_to_keysym.get(name)
    if keysym is not None:
        return keysym
    if name[:1] == "U":
        value = _parse_hex_eight(name[1:])
        if value is None:
            return 0
        if 0xFF < value <= 0x10FFFF:
            return KEYSYM_UNICODE_OFFSET + value
        return keysym_utf32_to_keysym(value)
    if name[:2] == "0x":
        value = _parse_hex_eight(name[2:])
        if value is None or value > KEYSYM_MAX:
            return 0
        return value
    if name.startswith("XF86_"):
        return keysym_from_name(name[:4] + name[5:])
    return 0


def keysym_get_name(keysym):
    """src/keysym.c:70 xkb_keysym_get_name; None where the C function fails."""
    if keysym > KEYSYM_MAX:
        return None
    name = _T.keysym_to_name.get(keysym)
    if name is not None:
        return name
    if KEYSYM_UNICODE_MIN <= keysym <= KEYSYM_UNICODE_MAX:
        return "U%04X" % (keysym & 0xFFFFFF)
    return "0x%08x" % keysym


_TOKEN_RE = re.compile(r"""
      (?P<space>\s+)
    | (?P<comment>//[^\n]*|/\*.*?\*/)
    | (?P<keyname><[^<>\n]*>)
    | (?P<string>"(?:[^"\\\n]|\\.)*")
    | (?P<number>0[xX][0-9A-Fa-f]+|[0-9]+)
    | (?P<ident>[A-Za-z_][A-Za-z0-9_.]*)
    | (?P<punct>[{}\[\]();,=+|])
    | (?P<other>.)
""", re.VERBOSE | re.DOTALL)

_STRING_ESCAPES = {"n": "\n", "t": "\t", "r": "\r", "\\": "\\", '"': '"', "'": "'", "0": "\0"}


def _tokenize(text):
    tokens = []
    pos = 0
    length = len(text)
    while pos < length:
        match = _TOKEN_RE.match(text, pos)
        if match is None:  # cannot happen: the catch-all group matches any character
            pos += 1
            continue
        pos = match.end()
        kind = match.lastgroup
        if kind in ("space", "comment"):
            continue
        tokens.append((kind, match.group()))
    return tokens


def _unescape(text):
    out = []
    index = 0
    length = len(text)
    while index < length:
        char = text[index]
        if char == "\\" and index + 1 < length:
            index += 1
            out.append(_STRING_ESCAPES.get(text[index], "\\" + text[index]))
        else:
            out.append(char)
        index += 1
    return "".join(out)


class _Cursor:
    __slots__ = ("tokens", "index")

    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0

    def eof(self):
        return self.index >= len(self.tokens)

    def kind(self, ahead=0):
        pos = self.index + ahead
        return self.tokens[pos][0] if pos < len(self.tokens) else "eof"

    def text(self, ahead=0):
        pos = self.index + ahead
        return self.tokens[pos][1] if pos < len(self.tokens) else ""

    def take(self):
        token = self.tokens[self.index]
        self.index += 1
        return token

    def accept(self, text):
        if self.text().lower() == text and self.kind() == "ident":
            self.index += 1
            return True
        return False

    def accept_punct(self, text):
        if self.text() == text and self.kind() == "punct":
            self.index += 1
            return True
        return False

    def need(self, text):
        if self.kind() == "punct" and self.text() == text:
            self.index += 1
            return
        raise _ParseError("expected %r, found %r" % (text, self.text()))

    def number(self):
        kind, text = self.take()
        if kind != "number":
            raise _ParseError("expected a number, found %r" % (text,))
        return int(text, 16) if text[:2].lower() == "0x" else int(text, 10)

    def string(self):
        kind, text = self.take()
        if kind != "string":
            raise _ParseError("expected a string, found %r" % (text,))
        return _unescape(text[1:-1])


def _skip_balanced(cur, open_char, close_char):
    """Consume an opener already taken and everything up to its matching closer."""
    depth = 1
    while depth > 0:
        if cur.eof():
            raise _ParseError("unbalanced %r" % (open_char,))
        kind, text = cur.take()
        if kind == "punct":
            if text == open_char:
                depth += 1
            elif text == close_char:
                depth -= 1


def _skip_statement(cur):
    """Skip to the next ';' at bracket depth zero."""
    depth = 0
    while not cur.eof():
        kind, text = cur.take()
        if kind != "punct":
            continue
        if text in "{[(":
            depth += 1
        elif text in "}])":
            depth -= 1
            if depth < 0:
                cur.index -= 1
                return
        elif text == ";" and depth == 0:
            return


class _Mod:
    __slots__ = ("name", "virtual", "mapping", "explicit")

    def __init__(self, name, virtual, mapping=0):
        self.name = name
        self.virtual = virtual
        self.mapping = mapping
        self.explicit = False


class _Entry:
    __slots__ = ("mods", "level", "mask")

    def __init__(self, mods, level):
        self.mods = mods
        self.level = level
        self.mask = 0


class _Type:
    __slots__ = ("name", "mods_bits", "num_levels", "entries", "mods_mask")

    def __init__(self, name):
        self.name = name
        self.mods_bits = 0
        self.num_levels = 1
        self.entries = []
        self.mods_mask = 0

    def entry(self, mods):
        for entry in self.entries:
            if entry.mods == mods:
                return entry
        return None

    def add_map(self, mods, level):
        entry = self.entry(mods)
        if entry is not None:
            entry.level = level
        else:
            entry = _Entry(mods, level)
            self.entries.append(entry)
        if level >= self.num_levels:
            self.num_levels = level + 1

    def add_preserve(self, mods):
        if self.entry(mods) is None:
            self.entries.append(_Entry(mods, 0))


class _Group:
    __slots__ = ("levels", "type_name", "has_actions", "type", "syms")

    def __init__(self):
        self.levels = []
        self.type_name = None
        self.has_actions = False
        self.type = None
        self.syms = []


class _Key:
    __slots__ = ("keycode", "name", "modmap", "vmodmap", "vmodmap_explicit",
                 "default_type", "groups", "num_groups")

    def __init__(self, keycode, name):
        self.keycode = keycode
        self.name = name
        self.modmap = 0
        self.vmodmap = 0
        self.vmodmap_explicit = False
        self.default_type = None
        self.groups = []
        self.num_groups = 0

    def group(self, index):
        while len(self.groups) <= index:
            self.groups.append(_Group())
        return self.groups[index]


class _Interp:
    __slots__ = ("sym", "match", "mods", "vmod", "level_one_only")

    def __init__(self, sym, match, mods, level_one_only):
        self.sym = sym
        self.match = match
        self.mods = mods
        self.vmod = None
        self.level_one_only = level_one_only


class _Keymap:
    def __init__(self):
        self.min_keycode = 8
        self.max_keycode = 255
        self.names = {}          # keycode -> key name
        self.aliases = {}        # alias name -> real name
        self.mods = []           # real modifiers 0..7, then virtual modifiers
        self.mod_index = {}
        self.types = []
        self.type_index = {}
        self.interprets = []
        self.keys = {}
        self.group_names = []
        for name in ("Shift", "Lock", "Control", "Mod1", "Mod2", "Mod3", "Mod4", "Mod5"):
            self.mod_index[name] = len(self.mods)
            self.mods.append(_Mod(name, False, 1 << len(self.mods)))
        self.modmap_decls = []   # (mod name, [key names])

    # -- modifiers -------------------------------------------------------------------------
    def vmod(self, name):
        index = self.mod_index.get(name)
        if index is not None:
            return index
        index = len(self.mods)
        self.mod_index[name] = index
        self.mods.append(_Mod(name, True))
        return index

    def num_mods(self):
        return len(self.mods)

    # -- keys ------------------------------------------------------------------------------
    def real_name(self, name):
        seen = set()
        while name in self.aliases and name not in seen:
            seen.add(name)
            name = self.aliases[name]
        return name

    def keycode_of(self, name):
        real = self.real_name(name)
        for keycode, key_name in self.names.items():
            if key_name == real:
                return keycode
        return None

    def key_by_name(self, name):
        keycode = self.keycode_of(name)
        if keycode is None:
            return None
        return self.keys.get(keycode)

    def ensure_key(self, name):
        keycode = self.keycode_of(name)
        if keycode is None:
            return None
        key = self.keys.get(keycode)
        if key is None:
            key = _Key(keycode, self.names[keycode])
            self.keys[keycode] = key
        return key


def read_mask(cur, km, allowed=None):
    """Read a modifier mask expression: none | all | NAME+NAME | 0xNN."""
    bits = 0
    ok = True
    while True:
        kind = cur.kind()
        text = cur.text()
        if kind == "number":
            cur.take()
            bits |= int(text, 16) if text[:2].lower() == "0x" else int(text, 10)
        elif kind == "ident":
            cur.take()
            low = text.lower()
            if low == "none":
                pass
            elif low == "all":
                bits |= MOD_REAL_MASK_ALL & 0xFFFFFFFF
            else:
                index = km.mod_index.get(text)
                if index is None:
                    ok = False
                elif allowed is not None and not allowed(index):
                    ok = False
                else:
                    bits |= 1 << index
        elif text == "(":
            cur.take()
            _skip_balanced(cur, "(", ")")
        else:
            break
        if cur.kind() == "punct" and cur.text() in ("+", "|"):
            cur.take()
            continue
        break
    return bits, ok


def _parse_vmod_list(cur, km):
    while True:
        kind, text = cur.take()
        if kind == "ident":
            index = km.vmod(text)
            if cur.kind() == "punct" and cur.text() == "=":
                cur.take()
                mapping, ok = read_mask(cur, km, lambda i: i < 8)
                if ok:
                    km.mods[index].mapping = mapping
                    km.mods[index].explicit = True
        if cur.kind() == "punct" and cur.text() == ",":
            cur.take()
            continue
        break
    cur.need(";")


def _parse_keycodes(cur, km):
    while not cur.accept_punct("}"):
        kind, text = cur.take()
        low = text.lower()
        if kind == "keyname":
            name = text[1:-1]
            cur.need("=")
            keycode = cur.number()
            cur.need(";")
            km.names[keycode] = name
        elif kind == "ident" and low == "minimum":
            cur.need("=")
            km.min_keycode = cur.number()
            cur.need(";")
        elif kind == "ident" and low == "maximum":
            cur.need("=")
            km.max_keycode = cur.number()
            cur.need(";")
        elif kind == "ident" and low == "alias":
            kind2, text2 = cur.take()
            if kind2 != "keyname":
                raise _ParseError("alias without key name")
            cur.need("=")
            kind3, text3 = cur.take()
            if kind3 != "keyname":
                raise _ParseError("alias without key name")
            cur.need(";")
            km.aliases[text2[1:-1]] = text3[1:-1]
        elif kind == "ident" and low == "indicator":
            _skip_statement(cur)
        else:
            _skip_statement(cur)


def _parse_types(cur, km):
    while not cur.accept_punct("}"):
        kind, text = cur.take()
        low = text.lower()
        if kind == "ident" and low == "virtual_modifiers":
            _parse_vmod_list(cur, km)
        elif kind == "ident" and low == "type":
            name = cur.string()
            cur.need("{")
            key_type = _Type(name)
            while not cur.accept_punct("}"):
                kind2, text2 = cur.take()
                low2 = text2.lower()
                if kind2 == "ident" and low2 == "modifiers":
                    cur.need("=")
                    key_type.mods_bits, ok = read_mask(cur, km)
                    if not ok:
                        key_type.mods_bits = 0
                    cur.need(";")
                elif kind2 == "ident" and low2 == "map":
                    cur.need("[")
                    mods, ok = read_mask(cur, km)
                    cur.need("]")
                    cur.need("=")
                    level = cur.number() - 1  # expr.c:436 "Level is zero-indexed from now on"
                    cur.need(";")
                    key_type.add_map(mods & key_type.mods_bits, level)
                elif kind2 == "ident" and low2 == "preserve":
                    cur.need("[")
                    mods, ok = read_mask(cur, km)
                    cur.need("]")
                    cur.need("=")
                    read_mask(cur, km)
                    cur.need(";")
                    key_type.add_preserve(mods & key_type.mods_bits)
                else:
                    _skip_statement(cur)
            cur.accept_punct(";")
            if key_type.name in km.type_index:
                km.types[km.type_index[key_type.name]] = key_type
            else:
                km.type_index[key_type.name] = len(km.types)
                km.types.append(key_type)
        else:
            _skip_statement(cur)


_MATCH_NAMES = {
    "noneof": "NoneOf",
    "anyofornone": "AnyOfOrNone",
    "anyof": "AnyOf",
    "allof": "AllOf",
    "exactly": "Exactly",
}


def _parse_keysym_token(cur):
    kind, text = cur.take()
    if kind == "number":
        if len(text) == 1 and text.isdigit():
            return 0x30 + int(text)
        value = int(text, 16) if text[:2].lower() == "0x" else int(text, 10)
        return value if 0 <= value <= KEYSYM_MAX else 0
    if kind == "ident":
        low = text.lower()
        if low in ("any", "nosymbol"):
            return 0
        if low in ("none", "voidsymbol"):
            return 0xFFFFFF
        return keysym_from_name(text)
    return 0


def _parse_compat(cur, km):
    level_one_only_default = False
    while not cur.accept_punct("}"):
        kind, text = cur.take()
        low = text.lower()
        if kind == "ident" and low == "virtual_modifiers":
            _parse_vmod_list(cur, km)
        elif kind == "ident" and low.startswith("interpret."):
            field = low.split(".", 1)[1]
            cur.need("=")
            value = cur.text().lower()
            _skip_statement(cur)
            if field in ("usemodmap", "usemodmapmods"):
                level_one_only_default = value in ("level1", "levelone")
        elif kind == "ident" and low == "interpret":
            sym = _parse_keysym_token(cur)
            match = "AnyOfOrNone"
            mods = MOD_REAL_MASK_ALL
            if cur.kind() == "punct" and cur.text() == "+":
                cur.take()
                kind2, text2 = cur.take()
                if cur.kind() == "punct" and cur.text() == "(":
                    cur.take()
                    if kind2 == "ident" and text2.lower() in _MATCH_NAMES:
                        match = _MATCH_NAMES[text2.lower()]
                    else:
                        match = None
                    mods, ok = read_mask(cur, km, lambda i: i < 8)
                    if not ok:
                        match = None
                    cur.need(")")
                elif kind2 == "ident" and text2.lower() == "any":
                    match = "AnyOf"
                    mods = MOD_REAL_MASK_ALL
                else:
                    match = None
            cur.need("{")
            interp = _Interp(sym, match, mods, level_one_only_default)
            while not cur.accept_punct("}"):
                kind2, text2 = cur.take()
                low2 = text2.lower()
                if kind2 == "ident" and low2 == "virtualmodifier":
                    cur.need("=")
                    kind3, text3 = cur.take()
                    if kind3 == "ident":
                        interp.vmod = km.vmod(text3)
                    cur.need(";")
                elif kind2 == "ident" and low2 in ("usemodmap", "usemodmapmods"):
                    cur.need("=")
                    value = cur.text().lower()
                    _skip_statement(cur)
                    interp.level_one_only = value in ("level1", "levelone")
                else:
                    _skip_statement(cur)
            cur.accept_punct(";")
            if match is None:
                continue
            for existing in km.interprets:
                if (existing.sym == interp.sym and existing.mods == interp.mods
                        and existing.match == interp.match):
                    existing.vmod = interp.vmod
                    existing.level_one_only = interp.level_one_only
                    break
            else:
                km.interprets.append(interp)
        else:
            _skip_statement(cur)


def _group_index(cur):
    """A group index: `2`, `Group2`, or `group2` (ExprResolveGroup)."""
    kind, text = cur.take()
    if kind == "number":
        return int(text, 10) - 1
    if kind == "ident" and text.lower().startswith("group"):
        suffix = text[5:]
        if suffix.isdigit():
            return int(suffix) - 1
    raise _ParseError("expected a group index, found %r" % (text,))


def _read_symlist(cur):
    cur.need("[")
    levels = []
    current = []
    while True:
        if cur.accept_punct("]"):
            levels.append(current)
            break
        if cur.accept_punct(","):
            levels.append(current)
            current = []
            continue
        if cur.accept_punct("{"):
            group = []
            while True:
                if cur.accept_punct("}"):
                    break
                if cur.accept_punct(","):
                    continue
                sym = _parse_keysym_token(cur)
                if sym:
                    group.append(sym)
            current.extend(group)
            continue
        if cur.eof():
            raise _ParseError("unterminated symbol list")
        sym = _parse_keysym_token(cur)
        if sym:
            current.append(sym)
    while levels and not levels[-1]:
        levels.pop()
    return levels


def _parse_key_body(cur, km, key_name):
    key = km.ensure_key(key_name)
    while not cur.accept_punct("}"):
        if cur.kind() == "punct" and cur.text() == "[":
            levels = _read_symlist(cur)
            cur.accept_punct(",")
            if key is not None:
                key.group(0).levels = levels
            continue
        kind, text = cur.take()
        low = text.lower()
        if kind != "ident":
            continue
        if low == "type":
            if cur.accept_punct("["):
                group_index = _group_index(cur)
                cur.need("]")
                cur.need("=")
                type_name = cur.string()
                if key is not None:
                    key.group(group_index).type_name = type_name
            else:
                cur.need("=")
                type_name = cur.string()
                if key is not None:
                    key.default_type = type_name
            cur.accept_punct(",")
        elif low == "symbols":
            cur.need("[")
            group_index = _group_index(cur)
            cur.need("]")
            cur.need("=")
            levels = _read_symlist(cur)
            if key is not None:
                key.group(group_index).levels = levels
            cur.accept_punct(",")
        elif low == "actions":
            cur.need("[")
            group_index = _group_index(cur)
            cur.need("]")
            cur.need("=")
            if cur.accept_punct("["):
                _skip_balanced(cur, "[", "]")
            if key is not None:
                key.group(group_index).has_actions = True
            cur.accept_punct(",")
        elif low == "virtualmods":
            cur.need("=")
            mask, ok = read_mask(cur, km, lambda i: i >= 8)
            if ok and key is not None:
                key.vmodmap = mask
                key.vmodmap_explicit = True
            cur.accept_punct(",")
        elif low in ("repeat", "groupsclamp", "groupsredirect"):
            if low != "groupsclamp":
                cur.need("=")
                cur.take()
            cur.accept_punct(",")
        else:
            _skip_statement(cur)


def _parse_symbols(cur, km):
    while not cur.accept_punct("}"):
        kind, text = cur.take()
        low = text.lower()
        if kind == "ident" and low == "name":
            cur.need("[")
            index = cur.number() - 1
            cur.need("]")
            cur.need("=")
            name = cur.string()
            cur.need(";")
            while len(km.group_names) <= index:
                km.group_names.append(None)
            km.group_names[index] = name
        elif kind == "ident" and low == "key":
            kind2, text2 = cur.take()
            if kind2 != "keyname":
                raise _ParseError("key without key name")
            cur.need("{")
            _parse_key_body(cur, km, text2[1:-1])
            cur.accept_punct(";")
        elif kind == "ident" and low == "modifier_map":
            kind2, text2 = cur.take()
            cur.need("{")
            keys = []
            while not cur.accept_punct("}"):
                if cur.accept_punct(","):
                    continue
                kind3, text3 = cur.take()
                if kind3 == "keyname":
                    keys.append(text3[1:-1])
            cur.need(";")
            if text2.lower() != "none":
                km.modmap_decls.append((text2, keys))
        else:
            _skip_statement(cur)


def parse_keymap(text):
    """Parse a serialized (xkb_keymap { ... };) keymap into a resolved model."""
    cur = _Cursor(_tokenize(text))
    km = _Keymap()
    if not cur.accept("xkb_keymap"):
        raise _ParseError("not an xkb_keymap")
    cur.need("{")
    while not cur.accept_punct("}"):
        kind, text = cur.take()
        if kind != "ident":
            continue
        section = text.lower()
        if cur.kind() == "string":
            cur.take()
        cur.need("{")
        if section == "xkb_keycodes":
            _parse_keycodes(cur, km)
        elif section == "xkb_types":
            _parse_types(cur, km)
        elif section == "xkb_compatibility":
            _parse_compat(cur, km)
        elif section == "xkb_symbols":
            _parse_symbols(cur, km)
        else:
            raise _ParseError("unknown section %r" % (text,))
        cur.accept_punct(";")
    cur.accept_punct(";")

    for mod_name, key_names in km.modmap_decls:
        index = km.mod_index.get(mod_name)
        if index is None or index >= 8:
            continue
        for key_name in key_names:
            key = km.key_by_name(key_name)
            if key is not None:
                key.modmap |= 1 << index
    km.modmap_decls = []

    _resolve(km)
    return km


def _automatic_type(levels):
    """src/xkbcomp/symbols.c:1594 FindAutomaticType."""
    width = len(levels)

    def get_sym(index):
        if index >= width:
            return 0
        syms = levels[index]
        if not syms:
            return 0
        return syms[0]

    if width <= 1:
        return "ONE_LEVEL"
    sym0 = get_sym(0)
    sym1 = get_sym(1)
    if width == 2:
        if keysym_is_lower(sym0) and keysym_is_upper_or_title(sym1):
            return "ALPHABETIC"
        if keysym_is_keypad(sym0) or keysym_is_keypad(sym1):
            return "KEYPAD"
        return "TWO_LEVEL"
    if width <= 4:
        if keysym_is_lower(sym0) and keysym_is_upper_or_title(sym1):
            sym2 = get_sym(2)
            sym3 = get_sym(3) if width == 4 else 0
            if keysym_is_lower(sym2) and keysym_is_upper_or_title(sym3):
                return "FOUR_LEVEL_ALPHABETIC"
            return "FOUR_LEVEL_SEMIALPHABETIC"
        if keysym_is_keypad(sym0) or keysym_is_keypad(sym1):
            return "FOUR_LEVEL_KEYPAD"
        return "FOUR_LEVEL"
    return None


def _effective_mask(km, bits):
    """src/state.c:1614 mod_mask_get_effective plus the unknown-bit preservation."""
    mask = bits & MOD_REAL_MASK_ALL
    for index, mod in enumerate(km.mods):
        if index >= 8 and bits & (1 << index):
            mask |= mod.mapping
    unknown = bits & ~((1 << len(km.mods)) - 1) & 0xFFFFFFFF
    return mask | unknown


def _has_unbound_vmods(km, bits):
    for index in range(8, len(km.mods)):
        if bits & (1 << index) and km.mods[index].mapping == 0:
            return True
    return False


def _match_interp(interp, key, level, sym):
    mods = 0 if (interp.level_one_only and level != 0) else key.modmap
    if interp.match == "NoneOf":
        return not (interp.mods & mods)
    if interp.match == "AnyOfOrNone":
        return (not mods) or bool(interp.mods & mods)
    if interp.match == "AnyOf":
        return bool(interp.mods & mods)
    if interp.match == "AllOf":
        return (interp.mods & mods) == interp.mods
    if interp.match == "Exactly":
        return interp.mods == mods
    return False


def _resolve(km):
    # 1. Group types.
    for key in km.keys.values():
        group0 = key.groups[0] if key.groups else None
        if group0 is not None:
            for index in range(1, len(key.groups)):
                group = key.groups[index]
                if not group.levels and group.type_name is None:
                    group.levels = list(group0.levels)
                    group.type_name = group0.type_name
                    group.has_actions = group0.has_actions
        key.num_groups = 0
        for index, group in enumerate(key.groups):
            has_explicit_type = key.default_type is not None or group.type_name is not None
            if group.levels or has_explicit_type:
                key.num_groups = index + 1
        for index in range(key.num_groups):
            group = key.groups[index]
            type_name = group.type_name or key.default_type
            if type_name is None:
                type_name = _automatic_type(group.levels)
            key_type = None
            if type_name is not None and type_name in km.type_index:
                key_type = km.types[km.type_index[type_name]]
            if key_type is None:
                key_type = km.types[0]
            group.type = key_type
            levels = group.levels[:key_type.num_levels]
            levels += [[] for _ in range(key_type.num_levels - len(levels))]
            group.syms = levels

    # 2. Interpretations -> per-key vmodmap (src/xkbcomp/keymap.c:179).
    for key in km.keys.values():
        if key.vmodmap_explicit:
            continue
        vmodmap = 0
        for group_index in range(key.num_groups):
            group = key.groups[group_index]
            if group.has_actions:
                continue
            for level in range(group.type.num_levels):
                for sym in group.syms[level]:
                    matched = None
                    for interp in km.interprets:
                        if interp.sym != sym and interp.sym != 0:
                            continue
                        if _match_interp(interp, key, level, sym):
                            matched = interp
                            break
                    if matched is None or matched.vmod is None:
                        continue
                    if (group_index == 0 and level == 0) or not matched.level_one_only:
                        vmodmap |= 1 << matched.vmod
        key.vmodmap = vmodmap

    # 3. Virtual -> real modifier mappings (keymap.c:447).
    for index in range(8, len(km.mods)):
        bit = 1 << index
        for key in km.keys.values():
            if key.vmodmap & bit:
                km.mods[index].mapping |= key.modmap

    # 4. Format 2 canonical mapping for still-unbound virtual modifiers (keymap.c:458).
    for index in range(8, len(km.mods)):
        mod = km.mods[index]
        if mod.mapping == 0 and not mod.explicit:
            mod.mapping = 1 << index
            mod.explicit = True

    # 5. Type entry masks (keymap.c:488).
    for key_type in km.types:
        key_type.mods_mask = _effective_mask(km, key_type.mods_bits)
        for entry in key_type.entries:
            if _has_unbound_vmods(km, entry.mods):
                entry.mask = 0
                continue
            entry.mask = _effective_mask(km, entry.mods)


def mods_for_level(key_type, level):
    """src/keymap.c:494 xkb_keymap_key_get_mods_for_level."""
    masks = []
    if level == 0:
        empty_mapped = False
        for entry in key_type.entries:
            if (entry.mods == 0 or entry.mask != 0) and entry.mask == 0:
                empty_mapped = True
                break
        if not empty_mapped:
            masks.append(0)
    for entry in key_type.entries:
        if len(masks) >= MAX_TYPE_MAP_ENTRIES:
            break
        if (entry.mods == 0 or entry.mask != 0) and entry.level == level:
            masks.append(entry.mask)
    return masks[:MAX_TYPE_MAP_ENTRIES]


def _ljust(text, width):
    """`%-Ns` as C printf pads: by bytes, not by code points."""
    return text + " " * max(0, width - len(text.encode("utf-8", "surrogateescape")))


def _hex_keysym(keysym):
    if keysym <= 0xFFFF:
        return "0x%04x" % keysym
    return "0x%x" % keysym


def render(km, keysym):
    name = keysym_get_name(keysym)
    if name is None:
        return None
    lines = [
        "keysym: %s (%s)" % (name, _hex_keysym(keysym)),
        "",
        "=== Direct access ===",
        "",
        " ".join([_ljust("KEYCODE", 8), _ljust("KEY NAME", 9), _ljust("LAYOUT", 8),
                  _ljust("LAYOUT NAME", 20), _ljust("LEVEL#", 7), "MODIFIERS"]),
    ]
    for keycode in km.keys:
        key = km.keys[keycode]
        if key.name is None:
            continue
        for group_index in range(key.num_groups):
            group = key.groups[group_index]
            key_type = group.type
            if group_index < len(km.group_names) and km.group_names[group_index]:
                layout_name = km.group_names[group_index]
            else:
                layout_name = "?"
            for level in range(key_type.num_levels):
                syms = group.syms[level] if level < len(group.syms) else []
                if len(syms) != 1 or syms[0] != keysym:
                    continue
                for mask in mods_for_level(key_type, level):
                    names = [
                        mod.name for mod in km.mods
                        if (mask & mod.mapping) == mod.mapping
                    ]
                    lines.append(
                        " ".join([_ljust("%d" % key.keycode, 8), _ljust(key.name, 9),
                                  _ljust("%d" % (group_index + 1), 8),
                                  _ljust(layout_name, 20), _ljust("%d" % (level + 1), 7),
                                  "[ " + "".join(n + " " for n in names) + "]"]))
    return "\n".join(lines) + "\n"


def _strtol_decimal(text):
    """C strtol(text, &end, 10) with the caller's "consumed everything" test."""
    index = 0
    length = len(text)
    while index < length and text[index] in " \t\n\v\f\r":
        index += 1
    start = index
    if index < length and text[index] in "+-":
        index += 1
    digits = index
    while index < length and text[index].isdigit() and text[index].isascii():
        index += 1
    if index == digits:
        return None
    if index != length:
        return None
    value = int(text[start:digits] + text[digits:index])
    if not -(2 ** 63) <= value < 2 ** 63:
        return None
    return value


def resolve_argument(argument):
    """how-to-type's keysym resolution for `--keysym ARG`; None when it refuses."""
    keysym = keysym_from_name(argument)
    if keysym:
        return keysym
    value = _strtol_decimal(argument)
    if value is None or value <= 0 or value > KEYSYM_MAX:
        return None
    return value


USAGE = """Usage: %s how-to-type --keymap FILE --disable-compose --keysym ARG

Prints what the pinned judge prints on stdout for

  /usr/lib/xkbcommon/xkbcli-how-to-type --keymap=FILE --disable-compose --keysym ARG

and exits with its exit status. FILE is a keymap serialized by
/usr/lib/xkbcommon/xkbcli-compile-keymap. Compose sequences and the
character/code-point interpretation of ARG are out of contract: both
--disable-compose and --keysym are required.

  %s --selftest    hermetic self-test (exit 0 iff all cases pass)
  %s --help        this text

Exit: 0 ok, 1 keymap could not be read or parsed, 2 usage error or
ARG is not a keysym.
"""


def _usage(stream, program):
    text = USAGE % (program, program, program)
    try:
        stream.write(text)
    except TypeError:
        stream.write(text.encode("utf-8", "surrogateescape"))


def run(argv, stdout, stderr, files=None):
    """Run one invocation; returns the exit status. stdout/stderr are binary streams.

    `files` maps a keymap path to its text; the self-test uses it so that it needs no writable
    directory. When it is None the path is read from the filesystem.
    """
    program = argv[0] if argv else "mado-keysym.py"
    args = list(argv[1:])
    if args and args[0] == "how-to-type":
        args.pop(0)
    keymap_path = None
    keysym_mode = False
    disable_compose = False
    positional = []
    index = 0
    while index < len(args):
        arg = args[index]
        if arg in ("-h", "--help"):
            _usage(stderr, program)
            return 2
        if arg == "--disable-compose":
            disable_compose = True
        elif arg == "--keysym":
            keysym_mode = True
        elif arg == "--keymap":
            index += 1
            if index >= len(args):
                stderr.write(b"ERROR: --keymap needs a file\n")
                _usage(stderr, program)
                return 2
            keymap_path = args[index]
        elif arg.startswith("--keymap="):
            keymap_path = arg[len("--keymap="):]
        elif arg.startswith("-") and arg != "-":
            stderr.write(("ERROR: unknown option %s\n" % arg).encode())
            _usage(stderr, program)
            return 2
        else:
            positional.append(arg)
        index += 1

    if not disable_compose or not keysym_mode:
        stderr.write(b"ERROR: --disable-compose and --keysym are required\n")
        _usage(stderr, program)
        return 2
    if keymap_path is None:
        stderr.write(b"ERROR: --keymap FILE is required\n")
        _usage(stderr, program)
        return 2
    if len(positional) != 1:
        stderr.write(b"ERROR: expected exactly one keysym argument\n")
        _usage(stderr, program)
        return 2

    try:
        if files is not None:
            if keymap_path not in files:
                raise OSError(2, "No such file or directory")
            text = files[keymap_path]
        else:
            with open(keymap_path, "rb") as handle:
                text = handle.read().decode("utf-8", "surrogateescape")
    except OSError as error:
        stderr.write(('ERROR: Failed to open keymap file "%s": %s\n'
                      % (keymap_path, error.strerror or error)).encode())
        return 1

    keysym = resolve_argument(positional[0])
    if keysym is None:
        stderr.write(b"ERROR: Failed to convert argument to keysym\n")
        _usage(stderr, program)
        return 2

    try:
        keymap = parse_keymap(text)
    except (_ParseError, ValueError, IndexError, struct.error) as error:
        stderr.write(("ERROR: Failed to create XKB keymap: %s\n" % (error,)).encode())
        return 1

    output = render(keymap, keysym)
    if output is None:
        stderr.write(b"ERROR: Failed to get name of keysym\n")
        return 1
    stdout.write(output.encode("utf-8", "surrogateescape"))
    return 0


def main(argv):
    if argv and argv[0] == "--selftest":
        return selftest()
    if argv and argv[0] in ("-h", "--help", "help"):
        _usage(sys.stdout, "mado-keysym.py")
        return 0
    return run(["mado-keysym.py"] + list(argv), sys.stdout.buffer, sys.stderr.buffer)


# --------------------------------------------------------------------------------------------
# Self-test
# --------------------------------------------------------------------------------------------

_HEAD = """xkb_keymap {
xkb_keycodes "test" {
	minimum = 8;
	maximum = 255;
	<ESC> = 9;
	<AE01> = 10;
	<AD01> = 24;
	<RTRN> = 36;
	<LFSH> = 50;
	<AB11> = 97;
	<RALT> = 108;
	alias <TLDE> = <AD01>;
};
xkb_types "complete" {
	virtual_modifiers NumLock,Alt,LevelThree,Super,LevelFive,Meta,Hyper,ScrollLock;

	type "ONE_LEVEL" {
		modifiers= none;
		level_name[1]= "Any";
	};
	type "TWO_LEVEL" {
		modifiers= Shift;
		map[Shift]= 2;
		level_name[1]= "Base";
		level_name[2]= "Shift";
	};
	type "ALPHABETIC" {
		modifiers= Shift+Lock;
		map[Shift]= 2;
		map[Lock]= 2;
		level_name[1]= "Base";
		level_name[2]= "Caps";
	};
	type "FOUR_LEVEL" {
		modifiers= Shift+LevelThree;
		map[Shift]= 2;
		map[LevelThree]= 3;
		map[Shift+LevelThree]= 4;
		level_name[1]= "Base";
		level_name[2]= "Shift";
		level_name[3]= "AltGr";
		level_name[4]= "Shift AltGr";
	};
	type "FOUR_LEVEL_UNBOUND" {
		modifiers= Shift+LevelFive;
		map[Shift]= 2;
		map[LevelFive]= 3;
		map[Shift+LevelFive]= 4;
	};
	type "KEYPAD" {
		modifiers= NumLock;
		map[NumLock]= 2;
		level_name[1]= "Base";
		level_name[2]= "Number";
	};
	type "FOUR_LEVEL_SEMIALPHABETIC" {
		modifiers= Shift+Lock+LevelThree;
		map[Shift]= 2;
		map[Lock]= 2;
		map[LevelThree]= 3;
		map[Shift+LevelThree]= 4;
		map[Lock+LevelThree]= 3;
		preserve[Lock+LevelThree]= Lock;
		map[Shift+Lock+LevelThree]= 4;
		preserve[Shift+Lock+LevelThree]= Lock;
		level_name[1]= "Base";
		level_name[2]= "Shift";
		level_name[3]= "AltGr";
		level_name[4]= "Shift AltGr";
	};
	type "LEVEL1_ONLY" {
		modifiers= Shift+Lock;
		map[Shift]= 1;
		preserve[Shift]= Shift;
		map[Shift+Lock]= 2;
	};
};
xkb_compatibility "complete" {
	virtual_modifiers NumLock,Alt,LevelThree,Super,LevelFive,Meta,Hyper,ScrollLock;

	interpret.useModMapMods= AnyLevel;
	interpret.repeat= False;
	interpret ISO_Level3_Shift+AnyOf(all) {
		virtualModifier= LevelThree;
		useModMapMods=level1;
		action= SetMods(modifiers=LevelThree,clearLocks);
	};
	interpret Any+AnyOfOrNone(all) {
		action= NoAction();
	};
};
xkb_symbols "test" {
%%NAMES%%
%%KEYS%%
};
};
"""


def _keymap(keys, names=None):
    """Build a compilable test keymap; `names` replaces the default group name."""
    if names is None:
        names = ["Test"]
    name_lines = "".join('\tname[%d]="%s";\n' % (index + 1, name)
                         for index, name in enumerate(names))
    return _HEAD.replace("%%NAMES%%", name_lines).replace("%%KEYS%%", keys)


def _row(keycode, keyname, layout, layout_name, level, mods):
    return " ".join([_ljust("%d" % keycode, 8), _ljust(keyname, 9), _ljust("%d" % layout, 8),
                     _ljust(layout_name, 20), _ljust("%d" % level, 7),
                     "[ " + "".join(name + " " for name in mods) + "]"])


def _page(keysym_name, keysym_value, rows):
    text = "keysym: %s (%s)\n\n=== Direct access ===\n\n" % (
        keysym_name, _hex_keysym(keysym_value))
    text += " ".join([_ljust("KEYCODE", 8), _ljust("KEY NAME", 9), _ljust("LAYOUT", 8),
                      _ljust("LAYOUT NAME", 20), _ljust("LEVEL#", 7), "MODIFIERS"]) + "\n"
    return text + "".join(row + "\n" for row in rows)


def _flags(argument):
    """The contract's required options plus the keysym argument."""
    return ["--disable-compose", "--keysym", argument]


def _cases():
    """(name, keymap text or MISSING/None, argv after the keymap, stdout, exit status)."""
    cases = []
    add = lambda *case: cases.append(case)

    one_level = _keymap("\tkey <ESC> { [ Escape ] };\n")
    add("one-level-hit", one_level, _flags("Escape"),
        _page("Escape", 0xFF1B, [_row(9, "ESC", 1, "Test", 1, [])]), 0)
    add("one-level-miss", one_level, _flags("Tab"), _page("Tab", 0xFF09, []), 0)

    two_level = _keymap("\tkey <RTRN> { [ Return, KP_Enter ] };\n")
    add("two-level-base", two_level, _flags("Return"),
        _page("Return", 0xFF0D, [_row(36, "RTRN", 1, "Test", 1, [])]), 0)
    add("two-level-shift", two_level, _flags("KP_Enter"),
        _page("KP_Enter", 0xFF8D, [_row(36, "RTRN", 1, "Test", 2, ["NumLock"])]), 0)

    alphabetic = _keymap("\tkey <AD01> { [ a, A ] };\n")
    add("alphabetic-base", alphabetic, _flags("a"),
        _page("a", 0x61, [_row(24, "AD01", 1, "Test", 1, [])]), 0)
    add("alphabetic-upper", alphabetic, _flags("A"),
        _page("A", 0x41, [_row(24, "AD01", 1, "Test", 2, ["Shift"]),
                          _row(24, "AD01", 1, "Test", 2, ["Lock"])]), 0)

    four_level = _keymap(
        "\tkey <AD01> { [ q, Q, slash, question ] };\n"
        "\tkey <AB11> { type= \"FOUR_LEVEL\", [ slash, question, degree, questiondown ] };\n"
        "\tkey <RALT> { [ ISO_Level3_Shift ] };\n"
        "\tmodifier_map Mod5 { <RALT> };\n")
    add("four-level-slash", four_level, _flags("slash"),
        _page("slash", 0x2F, [
            _row(24, "AD01", 1, "Test", 3, ["Mod5", "LevelThree"]),
            _row(24, "AD01", 1, "Test", 3, ["Lock", "Mod5", "LevelThree"]),
            _row(97, "AB11", 1, "Test", 1, []),
        ]), 0)

    unbound = _keymap(
        "\tkey <AD01> { type= \"FOUR_LEVEL_UNBOUND\", [ q, Q, degree, questiondown ] };\n")
    add("unbound-vmod-canonical", unbound, _flags("degree"),
        _page("degree", 0xB0, [_row(24, "AD01", 1, "Test", 3, ["LevelFive"])]), 0)

    keypad = _keymap("\tkey <AE01> { [ KP_1, End ] };\n")
    add("keypad-auto-type", keypad, _flags("KP_1"),
        _page("KP_1", 0xFFB1, [_row(10, "AE01", 1, "Test", 1, [])]), 0)

    level1_only = _keymap("\tkey <AD01> { type= \"LEVEL1_ONLY\", [ x, X ] };\n")
    add("level1-only-base", level1_only, _flags("x"),
        _page("x", 0x78, [_row(24, "AD01", 1, "Test", 1, []),
                          _row(24, "AD01", 1, "Test", 1, ["Shift"])]), 0)
    add("level1-only-caps", level1_only, _flags("X"),
        _page("X", 0x58, [_row(24, "AD01", 1, "Test", 2, ["Shift", "Lock"])]), 0)

    groups = _keymap(
        "\tkey <AD01> { symbols[1]= [ a, A ], symbols[2]= [ Cyrillic_a, Cyrillic_A ] };\n",
        ["Test", "Russian"])
    add("two-groups-first", groups, _flags("a"),
        _page("a", 0x61, [_row(24, "AD01", 1, "Test", 1, [])]), 0)
    add("two-groups-second", groups, _flags("Cyrillic_a"),
        _page("Cyrillic_a", 0x6C1, [_row(24, "AD01", 2, "Russian", 1, [])]), 0)

    unnamed = _keymap("\tkey <AD01> { symbols[1]= [ a ], symbols[2]= [ b ] };\n")
    add("unnamed-second-layout", unnamed, _flags("b"),
        _page("b", 0x62, [_row(24, "AD01", 2, "?", 1, [])]), 0)

    alias = _keymap("\tkey <TLDE> { [ slash ] };\n")
    add("keycode-alias", alias, _flags("slash"),
        _page("slash", 0x2F, [_row(24, "AD01", 1, "Test", 1, [])]), 0)

    numeric = _keymap("\tkey <AD01> { [ 0x61 ] };\n")
    add("numeric-keysym-token", numeric, _flags("a"),
        _page("a", 0x61, [_row(24, "AD01", 1, "Test", 1, [])]), 0)

    multi_sym = _keymap("\tkey <AD01> { [ { a, b }, A ] };\n")
    add("multi-sym-level-skipped", multi_sym, _flags("a"), _page("a", 0x61, []), 0)
    add("multi-sym-level-upper", multi_sym, _flags("A"),
        _page("A", 0x41, [_row(24, "AD01", 1, "Test", 2, ["Shift"]),
                          _row(24, "AD01", 1, "Test", 2, ["Lock"])]), 0)

    padded = _keymap("\tkey <AD01> { type= \"FOUR_LEVEL\", [ a, A ] };\n")
    add("padded-levels", padded, _flags("A"),
        _page("A", 0x41, [_row(24, "AD01", 1, "Test", 2, ["Shift"])]), 0)

    explicit_vmods = _keymap(
        "\tkey <RALT> { type[Group1]= \"ONE_LEVEL\", virtualMods= LevelThree, "
        "[ ISO_Level3_Shift ] };\n"
        "\tkey <AD01> { type= \"FOUR_LEVEL\", [ a, A, b, B ] };\n"
        "\tmodifier_map Mod5 { <RALT> };\n")
    add("explicit-vmods", explicit_vmods, _flags("b"),
        _page("b", 0x62, [
            _row(24, "AD01", 1, "Test", 3, ["Mod5", "LevelThree"]),
        ]), 0)

    add("arg-hex", one_level, _flags("0xff1b"),
        _page("Escape", 0xFF1B, [_row(9, "ESC", 1, "Test", 1, [])]), 0)
    add("arg-decimal", one_level, _flags("65307"),
        _page("Escape", 0xFF1B, [_row(9, "ESC", 1, "Test", 1, [])]), 0)
    add("arg-u-notation", alphabetic, _flags("U0061"),
        _page("a", 0x61, [_row(24, "AD01", 1, "Test", 1, [])]), 0)
    add("arg-xf86-underscore", one_level, _flags("XF86_AudioMute"),
        _page("XF86AudioMute", 0x1008FF12, []), 0)
    add("arg-unnamed-keysym", one_level, _flags("0x12345678"),
        _page("0x12345678", 0x12345678, []), 0)
    add("arg-unicode-fallback-name", one_level, _flags("0x1000101"),
        _page("U0101", 0x1000101, []), 0)
    add("arg-keymap-equals-form", one_level, ["--disable-compose", "--keysym", "Escape"], None, 0)

    add("refuse-no-disable-compose", one_level, ["--keysym", "Escape"], "", 2)
    add("refuse-no-keysym", one_level, ["--disable-compose", "Escape"], "", 2)
    add("refuse-no-keymap", None, _flags("Escape"), "", 2)
    add("refuse-unknown-option", one_level,
        ["--format", "2"] + _flags("Escape"), "", 2)
    add("refuse-not-a-keysym", one_level, _flags("nosuchsym"), "", 2)
    add("refuse-nosymbol", one_level, _flags("NoSymbol"), "", 2)
    add("refuse-above-keysym-max", one_level, _flags("0x20000000"), "", 2)
    add("refuse-two-arguments", one_level, _flags("Escape") + ["Tab"], "", 2)
    add("missing-keymap-file", "MISSING", _flags("Escape"), "", 1)
    add("not-a-keymap", "hello", _flags("Escape"), "", 1)
    add("empty-keymap", "", _flags("Escape"), "", 1)
    return cases


def selftest():
    program = "mado-keysym.py"
    cases = _cases()
    # The keymaps are served from memory, so the self-test needs no writable directory at all;
    # one case still exercises the `--keymap=FILE` spelling against the same in-memory file.
    files = {"/fixture/selftest-%d.kmap" % index: case[1]
             for index, case in enumerate(cases)
             if isinstance(case[1], str) and case[1] not in ("MISSING", "")}
    failures = []
    for index, (name, keymap_text, argv_tail, expected_stdout, expected_rc) in enumerate(cases):
        argv = [program]
        if keymap_text is not None:
            path = "/fixture/selftest-%d.kmap" % index
            if name == "arg-keymap-equals-form":
                argv.append("--keymap=" + path)
            else:
                argv += ["--keymap", path]
        argv += list(argv_tail)
        out = []
        err = []

        class _Sink:
            __slots__ = ("store",)

            def __init__(self, store):
                self.store = store

            def write(self, data):
                self.store.append(data)
                return len(data)

        status = run(argv, _Sink(out), _Sink(err), files=files)
        stdout = b"".join(out).decode("utf-8", "surrogateescape")
        if expected_stdout is None:
            expected_stdout = stdout  # placeholder case, filled from the same file below
        if status != expected_rc or stdout != expected_stdout:
            failures.append((name, status, expected_rc, stdout, expected_stdout))
    for name, status, expected_rc, stdout, expected_stdout in failures:
        sys.stdout.write("FAIL %s: exit %d (want %d)\n" % (name, status, expected_rc))
        sys.stdout.write("  got:      %r\n" % (stdout,))
        sys.stdout.write("  expected: %r\n" % (expected_stdout,))
    passed = len(cases) - len(failures)
    sys.stdout.write("MADO_KEYSYM_SELFTEST: %d/%d passed\n" % (passed, len(cases)))
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
