#!/usr/bin/env python3
"""Keysym name table + argument parsing for the mado-keysym tool (C1, round 49).

Reproduces, byte for byte, what libxkbcommon 1.13.2's how-to-type does with its
``--keysym ARG`` argument and with the ``keysym: NAME (0x....)`` header line:

* ``from_name``  -- xkb_keysym_from_name(arg, XKB_KEYSYM_NO_FLAGS)  (src/keysym.c)
* ``parse_arg``  -- the ``--keysym`` branch of tools/how-to-type.c parse_options()
* ``get_name``   -- xkb_keysym_get_name()                          (src/keysym.c)
* ``header_line``-- the ``printf("keysym: %s (%#06x)\\n\\n", ...)`` line

Data source: ``/usr/include/xkbcommon/xkbcommon-keysyms.h`` (sha256
13023369f65a17411606084e3e09557b4886aeb15f89affba4aaa86490a463f3) is sufficient.
Distinct value -> canonical name is the FIRST ``#define XKB_KEY_<name>`` line for
that value in file order; that rule reproduces all 2505 entries of the committed
``src/ks_tables.h`` ``keysym_to_name[]`` table with zero mismatches, and the 2638
``#define`` names equal ``name_to_keysym[]`` name for name and value for value.
The derived table is therefore embedded (below) so the tool needs no header file
at run time; ``--emit-table`` / ``--verify`` regenerate and re-check it.

Python 3 standard library only. Starts no process, opens no socket, writes nothing.
"""

import re
import sys

XKB_KEYSYM_MAX = 0x1fffffff          # include/xkbcommon/xkbcommon.h:280
XKB_KEYSYM_UNICODE_OFFSET = 0x01000000
XKB_KEYSYM_UNICODE_MIN = 0x01000100
XKB_KEYSYM_UNICODE_MAX = 0x0110ffff
XKB_KEYSYM_NAME_MAX_SIZE = 31        # -> "Failed to get name of keysym" if exceeded

# --------------------------------------------------------------------------- data
# "value name" lines, sorted by value; the first line of each value is the
# canonical name (what xkb_keysym_get_name prints).  zlib+base85 of that text.
_BLOB = """\
c-nn^+g{te^7eVILYI(u??Vc-uu6eH(027b;V0X2;*!L9?W8Te`fo;>k;it{cLJK{(Qan6x2-JIe
f#{rE86WMSgQV@OS1@8%KRy}dbbDy_3x=YnyLUgRQuDeFkRoQ_lqD>RlD8lZV|-lV7k)mkBcBtdI
v(U_thdul|Honv1<<-gObguYt|cxn5l#A%zkTX5OOCFrIqe6UjMcT3U%0?`bAKxvfb_UBB<1^*&|
}G(58iAYSnLbzgdJ!wOoWNwOWLM3Kn6g!bKRVXc5LLUWAEC7GbK=MVP5<5#}migc`Elw);g`sNU=
v5=yl-eZL4RW&S<s?IJX4-5CvaT7)%dVfteO@uH>D$3?VK7mFxR9~M!lE*DXxt`<?Ot`||FJ}#nE
eOg4Bx>-cIx?MzC{bvys>hmHh)!ibh)R#qM)cqo=)x#oQs>emVQvbJz1NF3sL-o9fBlWU~WA$|rC
+gcGPSy8CoT>jV;#~b$#9IBchznJ8x_mQ7Yt6V+1xU^&amAc7ZfwA~Wz&>RSDto@xK^iq1^z1A&M
cB8=&66%fc2HlFIg$QNCH(Xl2Db41pK~8Vg<1hRWFiMtrtnAHj5-z%_7n2=OQW8+adugE)sCpA~9
;eNNUwC(xo~q(v|vmkp`+;q@n5;X{3&eG*+iYny6okG*!PBX{P=x(p<eSQmy_jQm3G+PKxS5TBjH
_r<Bw>HrvW9^iu8H0zCHSnzQEST(!UV3mquiRyC9kF5Nc!^+HFgJay0n%lCzj)w_Xc2^7%2nLU=K
Q)nNh^}5bf)o9b1zUdb_hX!<bca_juwOv(1JK8sUD78@QQ?uQgUF#e(0OToMLOqYRH|a`k-l3a7$
f(Y&8?2hC7P?kDU3O4zu~e0TW@r}0%61CZ4~jq?f4BX~c7|?IgzC6~NCOZlU7n7RDptGGqDZi-X>
jvlvnW#PLue0MT#<ooDyXAg6uD~mA|DME>C4j=RV%EfLKdnzTNFZ9LQ2dJ`csGfsHjld=xx0yjH@
zHpwiICti#Hsx^V5XgudpqDFb!k+Hk!!e->q^E}ZYnNL>v6DPwifp@YjrU0g59R9&)uWu~qv*IZp
wu3BBoTnlwA@+#FWC8*RbB{1q%CaBfzkf2(s>z5n*@3>i1D|PRxSOx0AWmJXg!DUoM>Oo{w#p;0~
C+b0DnSv9y$L6qoUsRcTaGe}OZLw{@YKtmYUnz5~zEb9e`YJOo)mM>arG8K}qh4+vp6+d6({}qs1
w(7U(cNKTV61c58W;{-d=o&^8nQJZ42QPP2HM<EfQgm1J}@vj0GX<iePA+WDA!yW%2g{Pb1jq+d6
lZ61eIzifl-Z2P^)H0P%o7M<JT*-cXg`+)w&$&P_-_HI#R93p^jBckrUO5yi(}-znUILfjU#IGd_
mc_;s#Ml(|+X%Dhk~nR%&BBFjp>Q#9-aX!E*O??Z$Yj9nM)8v4o`gkccw4CKCovFi>e);A2t>aNr
{M66)UdUn~ZU}Sn`R6~#~zJfvMh4E7T!?BI}htV3)qWxv6_PAKVSfjc40!>H3P;I$<7+AKH7Dktz
a)hyk!Cdtm)DYyFzz}g{yi|WVT?NaEQ?WHH8}*lC)ey_q3`T_~ii5qM3<Dkhj?qM2axjB_?=rzI&
RRf^zGk>qR}_T)dd0e7r=>ig*WPms=$)fVLI-?e4*H*M?JMkc<5<wGy!OzcI>NEzQ1zj&Y#B|!fE
0vLnX<>;!PSS(U>L4dML}rs6;~gdJ>>!Ie$O$WeUB;zO}JwYTCl4=w%c(mXraFP&`P~40%)T*RAc
~6@J2NE0NUZLh*_vlPSpTf-+yF8XlWbH1lrMN#KF>{!dVnnWdTktln1n%pE4eJ|8gh{8-QfNZJ!1
feD-O?R_ZHd3yyl06nLc^5~5=y3+7x8EZA~AVk>o`Y{7uNphD=*Z=H7k_2Gb_5ZV!$ID~$E>xQ8a
jCwcV(1K}A5TZQ?qEs)m5{CZSc^o<@EsR1i>~_GREpbL@)PX3~ku$2)_5COKUn>KxBE-3v)4*(cO
Kma4uH=mn;ylQ)unYN|aq9C#s6Gz_bQ{hKJwf#aPkiP0I0gA|sv3@t-C!shhkuTR&EJ=R1HUIi^)
?XD<T)?&78MQNI#K)xmY0x!XV*FrwDvc>*RS<y3u9n=03>iodoZx_ThoFY@X+Dqw(UoFM7Z73MBr
!=_did2SY`e)1GsCdYHL-CpcPo?`vZhi7slk73pNnUUGM}!?Shz9LDhp`>4NW=uA(r;HWbD<wF@8
nlMo;bE6_uSJEXO#`WE&L0Ff<V2UL&|V3Sjj-d`a|s={`tAdR5*1!?jb(~%~hF(Ik)8B>xjpD`&Z
^BL2UHqV%r)Oo(a#H7zNCMJEJF)^v|42hxn+VBe`E~)O9n3#nZ43j1=n3ESUOnSXQt|ck<g1M4r_
n0fGc8?j6YWJ9yRJ+Htq}n~ECDm>)EvaTJM5=xKI)ra9Oj_PxKBVOh=0jS3fqW{`@(biskz!vUZA
H3#fwUFr@&(dXq{|OXOS=5P_@v7Zj6=FSVI0!s3G*jio-jV?@`U-5E>D=2>i-?nQvG4e3!VE{+my
aB;c62$PZEov!CrK_XiDlVF}R<AVZ$DSiwWe7!|P6WZ?F|!F|pCRzmOdF4G!4ps?zOV!%hs~a1_t
O(FFdje*+qiP`iPq_{k*xyMZk@Gy_5@R>pE+>72!**+8|6(-AAG1qz~9`?#^Px64msU>^_7!k3J+
Ve!q$-awV!E@EgPJ~u0SGr@cmSKdZ{bpzI|!olPQWp9;!;{b1vUW3o7WGD<pul^CMQe{K#D0=N(S
zhh+#sX%jsy_ZU25M`3ZEG}z@zwoTgLRFs?VA;SW$`#GHomGmYd7QTx^J;1nRKw@NU|mQs@ry8a_
QHde(O(YKI2ue-Z$QJwFYY+HI`Bi7J^pouxhAx-w|d;X#uE52^Vp_9HjzaH8=-bI3V6W{pszrUnD
SrJ)5p*^!~N_X+RFt7Y$vm-8cGmZIMu2zIQM^LZYSxIZ|I?snYB*O=CP@Wt$)tSyVkDiA>^UFQ$T
iAAmv5hAP++GGA#c<^#PYfO#kDA;O*jj^O0N%SUL(0F*+9HyfoAm0WMk>+j~cc|9GDrw+|%)Q5Mo
ZM#$7V}u^IZ!k?JFlG9ZtG_nqdNBB3kYOU-pLV8e?a@zC4F0(K&o#)>AD=8D{BipLvh>I8wFj(h6
G(qtJtHFhaqDF-N`L$qfI$}iuq6!su%htC9RbWcS@`3g0FL0~!5=TrHwZ|7e6~@fKR(@Dzka`cxq
1Ei`11AX9@vRLo^KwWVAf6w;g73-Y|eu}uKocTRs}u=tcDVpHN31r3<j|P_m#pMM{MgbO$;7KITq
aq<z$dy0!Z)}isdynkWv_TgCz=ULSHC_?QAPUtQfF2Oj3$6wjftR-hpg{42`Z7R)HQ~2@@QkMwKu
DEEbbW*uZok3mcdoWMP6MrWYmvi&nw{wo6pP1bE<F2@CXX?G8ngO4#AubeNGa1$L#Xkfy<kN;`m9
Nxrl(ge6K_ms(oCt6bSeSOgYBi4hjL08tp^1GFI{4Dx~<&IpTKp)4$dUDgPbTz>>vSmYD7QX@=qg
Cz=MK!-HK61J%$Cam!plL%v6-+?Twas35kVTx<$LPl5uhM8KJ;1Oz63lqRvF{y<OuAe{_Hn@HUS(
xAj(+d-TMQdRJ+b?Tjf^R4b3p_u3e0je81eL6X9e!LtVMf9f*q`e{ng%N>?EqpW`AZu^SmM&wrIy
xzy0T@bFm-<FjCp&#xO=?0(4~ElkirD&(Cf$N+q;K*kB5xE3~?jEZXW~~3$SYF>~9KdkEet`e7U`
R66Ixtf1T7LALF8g!sm4TX{e4N)Bz%TO#}==&0qT%reKTc?O~%ihk`9)4t)blbdR$|%yEdz7HL`m
#sVBF0JGLKt{~YgEo=-rQ7D_`G^tEJ#zjv0TnfP#z9h5ubuLGZ17tSB2k<|Ltox^nFJDk*y|1qCE
FX_s5g@GXKQ4oGXigxpRxdYB&P8JZkyZG7@%V@`SNZPZ%hg2wV1beV*eRwkdpO}91#S-iy#=8jx4
lIQQ-?zyfv(sFPp~OXE4Bdi9#pwvm0vC(-zpwAOF&rR#~aLx^}Vzb>kE-V%4Ne{q-N9%LFSSRXlW
p_?bmkMoEol3Www@&$L$pmuF7ARK{_;Ckhm_e8MAUOnk9&Adv~mt8n!h)f}F^O1=#kx69{bkJqm3
5KMe@=xPdRynr(jox@H@6n-(Ot08D47a?K{F8`$0UJH6d9!^SvjD6x*mZ66Re#bJY`uq8?>u_Yif
NV)76iwuTKe9+lJ4=!P!nZZDLY!727RCX{a+x^~@$F>6~!dT7zh|h*FO00_ZDC9)_GTl+8NIBpBU
p{5aU^Fb;lUE7m7}GwHl&Hq2Gqm7b?b``GASGw%k;>=iA>%XiP;Kqt&hpArw|%$It``~X1Z>1J%*
v~D!Yv{`bjn~@Wt9XNVobD%2Zd>1bcH1UlZ^*+h#Zr_90E;cT_xe(mw*lG-n}o8!9soC9$D~jPsk
Xx8XOAiZ|F#!sqrO*42IEPx@#zN7(|;rG}-3(4nnN<y4XU?g3%B9R@eS%pca@YSADZ<wqS5q0E}Q
w-R`&VO$~xk&F-*mV5ORs_<Rt?YuEf>#PLlL)|Sn_+@2~^HBd4vElGq_u&l)TcKjAV1`Es6-i3_X
wrk7+UwX-4HAx~G7`iMpf@7n%mFb#a+8*v^(4%U5(u?U~wSpeiUDy5wsZ^%}hbw1s7LCH^;ZDk-9
I(XxZIQ!DwQslJl}7Ji76V|VU||c5xGP#%&jJvr%@O{Es;=Q*q{<Hd#cGREruJL-m#beGMMLd>+f
vK6+Z&8mK#j%-))DLMfeKTN5CdhjJsx}Gsd*1b?K-*@OTAw$au~fvPzca!48;HiV<-hE978!kk+m
YI00Wq<Ee35v#(*6lFp$}?!@kpjuZ8UB4G|cbpr=we1UzIR0wH1{R#mfZjw~kXfNo?F3fVM1mrQM
R)3KC8HWfZn(J<JUJq1gJn~kP+p42dO7+7&0?5ia(XyEg=LiYys#76)c#*21upcL?`#v$T&YXyjo
PiOb0Zt5dsjAO#@)(S{P?hOks$Et2mofi}PrbqL~rc6~0ZPZH0W%wA^v^4|^VAihUw#!4C1@9UjF
Eu{8H6?V&?V)Y(1smx3uKkXq;VUg2G|q*FB@vWtFb-r|QZ=0ng+q78x(srndh^Td2LMKM=)T4t_G
(!2pf&aJ)G<;FJoM$JE4Sc_(p4Ux*1#ZVD+eI;wFwFi*&*c9)&z7g5Ktso0NEiK+q$vuO}WxxE#$
_~84=h7?&+$;LziGqMCt%b&$4R{?j5AczH+z27i>UC>^pHs=w-UHFDk((fZ<$iVZhnjjtHVw8}kR
>;@E+J&V<wz>QS5^1fGFG&VjZkb&ba>j%@ptAkaLHVgpsRhcN4fhSACF*@T=BMkojN_|}i{FtlN^
t%pKIE^)}|09Z7}+-qGhp4l9a*tcQ%X7)qPd~T_SVWMX+BlX6G<WrQ2(bjpkiDMgv;nB_Y9w-&e8
U+L@#Y3`&@o-~cB3Nh`^q_};vkdtKhP+Cz*O(NBI_G;2gl;5v%>c%@0+wy<kyGL;T|G`U?j;=!;~
fDtcpl^w%QC%ty;H;BSDO(4{l{$0VbkLKYOsy=61br4DqDp@A=27c#>C5RFj3*ifT2pcCJu9eXtZ
{^LS-g!jj!7E_LZ{Gn$l%cz-a1b84@!)+p(0xltW=yF5uHx9K(w;u(6IXwtx^qq<+&H2u2p~kIfd
P#J%R|l4$j_#cWCijjw`$fn<~eRL(WzqOzH}^w7g>ZZ>P!h`4U;B-b2Ba3hP$3k>A?3rZ#Qiw%r{
=J%^NihZ11LjNE_qwN7$F#vm)iHLN-^19iX?F4X0=*!Yuo5vWyTp~s`ScjM;e6UeM=ONKP02;~f7
DyR@)_Ih&6EhZ%GZD+qS$=OT5H*W-XY!`45ef!LE?I^>lfhKgDAmsF05gm^u^vU)pP=Tox3&|#ae
K(N+)R--M7({S@^v`M_5k*)y)~^Ak0Sil)mg9sP#D%mk}~q%uK%`Zg+YEh)gXGq!sLLoH*CMLHT9
M~qFbd{FDh96yub?O^{su=4Tu4WoAzyEflvS^7)~l!3k}F`8z&YBOiUGYVg@=5`Rvz#r4HM#+x_|
ka^~c6)0PkefLs8LO`=Cp5Gfqew|xszDfkxOb*vol-oCpGjFT%&4_oXCR#O&$30@!d+oFP{lmj;H
(bl3^d0-Dk!nh3~fCCR7HYbRR7@1}dBPFJcxUkA#&M_Btw2>20&<QJ7q_SvNcqX9MM#_B|V6%b@Q
nZDJ6&9GjAcGuWmk9b5WRZidrp<s%QnxkoM)0=8dZ0lpm!5})f3RwnWRYFFgB;4hn;7j^k`21HJ0
VLp=%BJC8DQJmm#eFiEU-n6bpPG{)@Zvj^M2K+N13zS!Au6S_Pi~IwBEFv<^W>JC6$|#O-@R;w$Y
S^WACvIW35T+gKpmSe&0d~6=~k<PD2hAE3F%_lYYa7Uj-rx#tDVI134OG%rO=s%E=((E4o!GWdt$
-fS3yrWzD{UCB_B;Gp!>AZF8+i!9v3%T^XSpzTmqO^+s9f1!;{`3tQRlgiXUlQy4r2Y8iI3ezQIO
-R6<_s=dS72TX2Kj~sRLhV?g@hp@w#e29TM7(K`x7F2i{dNWL@zrhEl<Q}8JC^*)jzU2OWgYP{wf
YfAxt$FKD_(t=}%X`~R>R^aqJ6;_Q06Mph1{o?-$6nk(HR@y#QQJE8vYi{NI`hCmTOjwq8(7TX+m
m3u)Asdq^KRNTAOR!KJ^c4@IF9(-v^}5^qxX#g4GoOR68I1N`3Yz;LT}*D2GEqztLDv|DnPPP*&f
areu9)+0Q3m(bu32k7x=RSv>c(2@TUN@8lj|)8G$eG=Ll#$&R_$7>xF?aT*9PO;SEZ~7v7#!auJS
{WHcH@bM+~_HAzlJNeT33yfxUUOyR9a<}dP5GDf`-F99e4@aFrBD*g+IHyxRx@K*Cy@FrsecxzoO
OzCZOaSf8U%@5>)K|<1-<@y06Zw{oq8GcwU8AOo0`bc@zzhepcAYn|e@B>O-+aH+FYx)%gujO}Jo
*6`tynf$r7pC$G{(yv)SMVC8K|ze^^+Um{_aEQ!s(8RgU9U=}k)7kKbik?mRoMh0Usw4ACudc9z`
3_o#eh+NtI7%Ft5!`2YV?(v;MB^idV)Jm%yI%#b2F=HHq`1&Fd;}E6An04#RyYVElfOts20M`grp
Of5G<@rea;92lg*8=E%h)XOv`=D2-~vS!m3_lVNq6gJTCn(ZP&14Yj4r#)BX*dwO@lZ$RzdZ97)E
hhw)19oxb%j_P@33pUsutLP?}~9i7dLs$CCVcT_!Z>I+yKKv%8P5di(H7DgUwBFucQF2dyF@@n<D
?Tp^Pe#Z|D@FjB?16KHkIV|AezfnJiXWYRO=8Wr8*FNLR7<IK=sW3>FuUDtTwkh$*AF#k-9~-l+z
Tn{kV4=gFaOWK$5INuu_T^TNo%{iI<uAHGByq@fr+ah#@DZU@K)3q?v<Lt*%G&hC%DI#O@6=dPJM
r;ig;K$iEwp4QM5%Jpi|K7b<HU>O(P~;d@zNfWe1H`+>a|)@r0vlWh>=Y`oA*mFij77l`Oj&0K#{
C*iw`_dCSyFEwrIc=+2XQ2yrW2lc-(3$k`bQmc^JrEe>@sOfDCYni$C*RcK9+Vz+{Lkvo%Nao#K)
`uKzp(T-wT%Qqch>>pVi!IS!eUk*@6-TWz2{+&(|N-nFQ<ftFw;^UG|5*E@ZLojjo7fQGNno2EV@
8cEd0jYlYDn^^Eu*PaeT%v6FDF|*jc`EzsxV)+E~k+mfrJM(LZTud+@xwOQ`rt3x4)fDv6jZ;I**
!2YC$g9<$bL{Q23M9%}ufh@PG6<Fg*2h=dmrUTY{L=n1uXoMfyne+R1i=Ko!jn|MU8axj0hvq?%?
VBukEmySykcvBTylo9BLR}mZ_t`wVXRm;d!H(s5<ZD@;S)4X7zd`w^f}TeEk^7I*ws^%9$E4#y2L
eqpKCQ^e3oWLIb+o`oNN_3|6I2FW3xZCr~dUTo`TwQM_`?=uA0959}%3}uJJUWZ~j`ydF;}DFZ}v
Y{Iq@6gw9{wIb-}(Sy!+0DWr*4PUbHi<G{)Cvq%$%4x}$Hy^P-<_lI_8_6?$uL+Q&L0AdHYZ>&I0
s4V^>2%ywK;<HN=XCj*Y;0>^x;)$=`0M%4kO$8Pt)AvJwln$YfhybV@VBZD-(Kyk4*zoGUYyh}+@
bJxprxG$?fycy7iG*ypX<IBJ30TBWMomJ-q7Uc*h=hLb(}@AZ7dz0HNi2;3_Un3BXL4jBEAYLQ6K
NfGZIX(bk{y#wVBS$lF3^$Z6D=5ae^LmLotu=>F2bD&TYQgCcVYd^35+b1H6z3OFaB$jF4aX@n!f
)pG-6%g>}b-J$3DV(5bsnFWT2kR!RRAQzP*4$^$aCVz({=n$ChRS$LjeA)AsuWPSh9ZiPOlbK(Sg
|!DZ?JzfRNdD*@&V1_IRT;#4&td@x&)Lq_clt&>qhyTCBDG8>1Q*foZ!Az>rRsGZzmnA%8-VQLu<
7^W6+!Z5XiuNWrJ+qaQk`*QPJOO$2qar)34^>&6oU*3GTwJmwrF}53K)F|AiKOj?M5SNnFCMVVTc
?=*c(JQby;qx@+0@0qPT*x`?*Y<skQ{Ord0I8SC&ZByzF75w7UEbjTP?fJ1h}5ME#1KFV_O)(?|J
HQJ6V7L}7{WcST`A0oK-u-ioQRa2|K~)kUhqNk9+uQF1$Mve01lhMNB20B=Ox$%GQ#r_YycUu^AK
$OSf=?0_I*PP&L|d`&ng)u<*4Zh^^r3Ve>feF?f&(u-dZA`5Gw@r1Pl-?CSZtQIRPUCs|gq*XoiX
vTf6r5b*N_))}mg{V5~>In!#9;I+(#&mpYumSetsV@>QqTT$4H;!L}C32(mRuN02Q&8$q_@!Ln}5
z+njS!MJuzGM(L-nR>7<*5<=;kIfQ^a!O!BMxq)O3VPMBsK!m2UB#i8E4#+5Vf~B?Li7zvg}Q{vy
2D@vW3v4=r><eW`lw;N#9*YLxwkODxMgb%+n#3_MW4*SC=}|thmi$i!g}@#-mdZbX5O6$`{~Pe2j
hjMSL(Cg|7<WAK+KKVziBKC*0DD>3`^X~NC3l;dTMvtC4;Sa1M2C$Mk#^(j{1$H)N`*A&eT7c)!P
XLyZ2^6GxI9ILcO%GZFT~FLDTo|Eru(syk;A~V$zDV>aSrDdEN9UFT>K&%Exw%@3;WK2NoC}&Zm#
~P6Hsr$ssOa>d>D^z`viUM>rh#=p9xl^yd%OJT^|MF2R6}+i;_3?G1bN{klClgwIQ5yy2L_v{afu
r1-$)`*R6salTUiFz6Ac1do>L*}l(ksrOY=*(QykKL?(1m1{SL84M13{oHO^C-JHDxwys-=?%>B6
ZnfZJ_{psn8)>JQO^fc!UhO1Sc%`j(iuZ5<%ZQ7R^K>Y*Ra5*A+?58wHvZ)SWZ9M`+i(duicIe1?
USXJ26qNM`Osw;`9l}V<1(oNx+KxgMs}I1Yvp0+x<GhxeVVHvq4OYlAoYzSm<8=F>Wnh!!q}F-y7
THV0{XkmDYtI9SaEz0vrPPVy#`7uz)gqY(%g;{n*$lK?q{7kSnkz3}P+}#4~=}4+69tv$df@eZX6
#Aeb6)3c#HPKpX&G``?Y-H6!3&+8ROj`)3L8=a~YcSGNUnLr?Z4<lHSG)OdURWUqGupjP*%9rt-y
<$Zp9<?$5OVIa976;?_RrtMn|3m}j_t}qzbV1U8U215)+HW*<r#vrw^JVAk)S)QU`TT7l{kQ-ZW3
#R6gYZSQ2k>p!lUZ6}Z%?Yxx<)y1Ox-YjXa0|-~O1`b+wJp*fNP(zrF<<y1B>-&J7ZqltZKlr#ug
N;vT4|g0^Qky?+O}D3Tz2+dN0eRm&9BCe{)M&k5<}LKXvo4E675)6JE9p2YeuwUVXcUhUSUm`V94
4p#gH{$h9PUZ97E1y_FZR?jI!=3YGr*@!qO2-C|AmQsSMOd%)JcNN6fp7)JM#@jMYcXw@lPW%(YA
*AFOx@ePp$Afjj#@2Ow~PJNsV)5W2vf{a*kOxxk(MUjh)jz@7bH0g$-Bo&As1PF>*6{)hUnG8eeR
|F{NT<t}h%|AR)s(gp5pRbkEhF<804ll>1$27wDa+5ezz5W2vV{SRsfkqbQ8|Db;myTFtE4~7U57
kIM&!5~5E0#Eio7$nGC;K}|6g9Nz?JlX$XkZ|b&Pp+z9k#OY#Pu9E@m?R8b;K|yz0-J=P3p`l^S7
4Mda)BpnVT10CUEs-@7?$UD5PH2sAt2!ig;3%753GM27kSaLcwx?==Me(d;gk)@IA|WVOPRT_O_n
PdWgM(+(4qwlKL^}1piq)v8JPRtJ!42f23EjDr|~_@*Q!0*u2Kgh2#o?OUkRaA@Lfm&p;=(XD<QN
Cz5p&D^dzi!C4|0&6|aQQo3P@Q5c(4qyQ8Y2N9$VoQN>E%+NPr0G*`>za)l>-bhncgE7b@wjnsE>
6ymU0{hnco`Z2>&^*+V2TDi@zm0;9+D0GMS`dJzFpbz%E$Vn^J3aM6K2MI>7laONd58o(d<wX4*$
uPzLbK}C$Eg$GADJur56(W9ACB;;&2Qi58qA=XrTM6vYirNP-6`8*q8xEICybiR$dluJp%INTw!0
Fm5i-!VtCrl2{1#VB)EF8$_{tOPOC=W(o>AvC{rH%+k-*gLN{FUo#W%|<KDJ#+G=*#FCt>qWJGj{
Y5_>3(_Y3(;agWICK8YQ06T7KMnKh0a-5CLo4DJ#CF{fdW@+Rpus6Cc)|CS0*Rmu|3Su{xJl@PYh
jcUmiXi^67Rts)tH0X(DA(O2U$Ivb~+T2tPSfXQe4=xgqq3qnU<w{Kj}h~&5OLwAql$MQozisXmt
w|s8y7<tRbm=PsB4Ca+zptk}Zd3%)4$k&32L%gO0&-7u_eDUK0fx!TNxV|Sa9KcVvUkHo_@alrFc
))&KU)~U!4Cp@`GaayNf-+H`7sB!ZdwC#Ci|lSVaWR0m_qPO=19<o2D{E5?=x3kah=QKElC_A*#)
y^!ctcf+gek9B#YmX)(+z7B30uBga`BNc<`-X*u;vY^6bW12e<e)V^7)2K7uNj7)fCpe^bv(QAGt
chn*U);81sqK3R6CFJYmUi*WU;fmVEJ^h=nPiD0#e+j-ZOi!j#{J<ieDXKfXQ@8cC-SCM?NW3PXP
6Xu=fYgxYb!B=oiU4DUCl-!LxBMHhL`aJ|DfM+q0E?A^}C-=Q^&P@K3FVQhaX_KbntPVbaWBJ8W*
3j&3G3qv_1!o2H-s-Fn!R+=zj-FJM0-=V_5e>tXTsbtqgv{Ox5C8C`kTf&5I{<2dNVSHFB5GX9Xe
Lt}_!hCN&y)e?T=SqsU`o_jcMN{2Sl~Q5Kid9U7Dc2j;C>6FmmRx))jJfkA32SahrBv8*e<CcE4U
bC~*8IiQ6xJ+#L}AVYS4UX$Cu72x9j6^NRl<ZNf0<td3QHcnCo*Bmj*@39=?JQLCQSKjNG?oyct3
T7M$&172}^R8!jLsb6NcP2Yy0iutNBf&Fdp7E`D(A5oKdir_^I*JO2-J}(v{*f{2fLRz1usJCUH2
r6VE;PB5HgA-iR9Cg6G!Bj!OKcWJ?14rDQ7t{GDV00lp3)0lwsj0AF5AfWNveA;90(mJ;CaYs(1m
H@4*j_`BNp7Yr<%E{7}A@Yf978J@kp&+)^ReRw;c!_1HsL7A^1b~^@rr7FCO&tmy-|6a%O@@%-_k
09-B^2<ZMCU3?Uq5Um!YfUvSw7lmI28Yw0-Cr1S$sKHMHT2VdvoqvpafKq#>z3<`$2+>~8+*$gBm
TC!5iwjS2oSCtIq%^nL4TR5#p@;IP3@;%kxb2}4oIffQ->r|<EbN(sqNG;$<%b}gk)+tbxJZdoH`
?!+D)C4?3zslgTr&P-@M{I$yN@Xya`B-ovcYrNMt!B*^r#E%s}pdhD1#w%Y~CqB$gzyTsgVp=!Rt
mY6om7LB3>}ft3TOIytG!)yqj;P5I@KlUou=`<7)^pK~X5-pCv|sq?mBfD~G@ObV@i1jF_xgXc8^
6ho6rCCj7{&q4UPn+1NdOgjDa5lE^1I|HQF&jBID_C6DG?D5Dz#(>Y3Tw7HPXa;-~vIqB2{MyX{L
n5-skgZ|BBV-bvZLws)BV-gVrwF+mAA^i=V3}-i@Da!a1<PcC!bczr>{urKcRmH_&qggs`;KK&bx
U$dYW!lEl;C9uey8Su0U^D5mPsqmlU7?_25D8ZOm(EO55FR#4o&T^T5=C&VCB0sBUG)1<&Zly15~
RM%L#XD2FR412gsJb2+jSJfr2|K1JsgQmMiY63>faK4EV8vfI8q>cqH`02P34)+X<WOwsF2)E%B-
-({^jS-rf_o8nD8H!2qs37!F|7G8he@VJsf7Uk!uF0RHtc(*ZpCa<T#Rsq+DQ^AYs`Zgo#!F@QTC
vmC&^J2wHa8bGg(8L)$oSc|G}7&XF}otsJk6xQsybQ4G|Ik~Xri6aVQ9)^O1Io}3U*mJ${MG1rc>
!S*T+AotGDok1qsIY12a}_rI*=z|EHZ46^$xM9(gjN6eOodf{dIf4>)eT#<7FOLbCXBji7!*eR%~
&LJq#D)2ruYG~1BFRzJGZXz)%Fj=k6u_LRK*0*>S}@%sv09J1521OQmcB5go(P7$K8OWYCA@vrTQ
{X6|K~6jM#Sq#z?9TV+7v;m>?_FPY{i-{EU!79mfc4=)U_W04scZ@wXHM_1!-QSm8U2zoi(d@8YL
cEEKEXQ%I}-PRcCQpD}_9lINR?r$;Bk>f>T;Hdue?2?C2^e&n#i_W-q!BKhk^qQ<ZW(dUUorVti@
C5b*yWHN;)JC_Lru4R1x5M_m*eCqQ=DN{_euVkVLXXxi#q<%I1MvB0SCB+k3;qTSVuz=zX$`t&QD
*}orme2r}J9>sC6mMK<Sor93aHg&&NUo-Fw7M4cD3q*Ksjg+=l^WH>$lt4yrm5wRC<y{qPuFLg11
zJ=c_NT0hMK{m%ACa`8DCTuR$1mek;oKd+mxwHG~qIJE6UAPBP6YEC$S6FOpsDNOpr>o6U5*%Q=e
;%&rDf@)y%_LBg2xWJx>HOg)lNKZQAq1=y$<H*|AI@@I=NJMuwG6d!EQ-im~>v>S_Ncr`^+Jsb1k
8DNCqyv7}0sizOlBVhKHJ7imBYJ-rrHH}nWwLV=4lt}9+5bq0;p*9j7<(*#NIxwx-GiqFNpl(}c-
LS0zXoTiX=v4pyKquvxMT`ZA%<su2hxHwYX+C>r&EMUIQb%hno=?ogEAEFYldU=;(q<&1|$Lf88B
<jad!#Y*(Ldw(+S+QKbdofssxwth=k8enG5wyHM?Ocp>ss7?E`urP(4vg&Ob`#LuBsT#Q)i-}8Sn
95ro1mF8?l#O3nk)RF$1#|3oeFnqNa)J_nBo|upKct3{s$b#Fl#kNS*<ZjdW}J^*ckSjjbT=8gle
2TPWFpjC$H2c{s4<W0(IG){+fn9+;w26K7Q=<z7$ZT?wU>uAXZ<R?N$JZy4T|<sd~guZzYteC$PQ
|NUpw*Dx}rD`Te{x{~DQjp{`o|l$?M7R@rz>XVug-EdBQQ`5+N6Y3&Zj_ud_^0{{lYU$xvH+nSKv
UUoVG3x!|R>1N-%jbRY1v~suIb!|(TtsoW*I07iGo1q1GC@59suS#`DrH*4Hj8y?s-pM@>34$oaD
!B_%&A){4jj0SI0Y)0`LUkbiC~DV~M~am#m;S9McS)r~N3U)5?pzk&U<?NYhm+WhM`JuBIG#jjJe
lOqcsk9ViEK<n1m~0ZjO$7Mj2F}VnJ6dqXS|v!z=WA<z(hS$ftb~D%)|sw9l-e11B}mHz{J!CjL)
3F#LNp!%-z7u)DMi$9KpoQ6HLrq!OYATOw66Z%-kEyoN)(H!Nea4!Bc-QKJ^FVGk-8K^#|iKe=sr
g2NQFDFf;WB<1>FSG4lr#bAK>1^9K`ie=sxm2Qz2<K~y;HAB@jB2otj&!o<9bFf;2TOw2n8GxJ`;
%$aV&)U2N{G4CkM%zFwmXSxbg^S;8&na;x0ncl+Gx$Z(-H1SVL@YFqwPrbwV%sEU<eZ%<7HB8Jr!
^GS%%uM~l_{=R#%)G+H+$qe=e8R-sCCtn{!ps?m5EW1R3*)o?!o;k<Ffs2h%*^@=6Z8JU%)GxabE
dyAHR~@-%=-&7^Zvrjnf}7myuUDWroS+CroS+CuD=kMOy?KIXA=w)vl)ho`4q#<Y>r`KKFKgMpJk
XiGtDqHn`fAqPc+QTXBuYCOf^i+=Ne|tOg2oNnQfRlH{B4I&gL5?<`WJx^BISkGgA&z^Ero^Gm{Q
eXJ#Fy&P_Ya&F39v&P+T^otb%<Iydz&cV_Nk>fGeR+_~9@xwF#`k=evw8NpL;F+TMb<1<e&G4&JU
GcPeQ^AQts4>2?K592fMFfsED6LZfnGxG}*bFVNn_X#s+JVI1H?LUmqx(^ex-owPa^Dr~(J50>G4
m0zf!_1kE!_=(bFfs2o%*=ZYGiN#tQ}aH<%$Y93)R`W`)VU5roSx1<jL+sDCT8;w6Z83pnc4iq#C
-l?W<LKgb7uZwYBv8cF`s{!na@AWoSA=^n$JJXoSA=^Iy3(;b#DG4u9(d~Ow8vWX6Ew`GiT->rsn
exGiT->rq0YiOr4v5n48Z(%$%8jm^w56Fm-PJVeZWQ!_>L?hq-g}4|8YdA0o@?{)h3|28fB-4v2~
Q7KoYI9*BwgCWx8&E{K^k+aRW9`yeLf8zE-qJ0WJyY=xMb?}eB-vl(LQ%x;LObK4=}s@Z;siTQ?z
nfZ>0nKN4=rsjJhX3lJim^!m7V(Q$sh`IT`h?z4RBc{&mjF>vNHDd0}-iWDln<M7V?T(l`yFDV(%
=Sl2%r{8P%y&r4oY^8VHQysKb7qso)R|opQ|Gox%+2>n%$(UMF?D9A#MHU15_4zvN=%*GEHQU(x5
V7p?Glmoe80rZnGF+DXLd|Xo!c@ocV^GT)VWO)bLVzV%$?mfF?nX+#MHTs6LaTwPRyO%Ix%@}@5J
2M%@dPncTY^7-#)ol-<SA|ZFAV2jz)Y?ZP7WFbIjqBY>Un@?epx*rg5(r4BY=>3Qje8L(4Je@p4q
o@a4Cq{s&P*nr%a`A6r>SunyQ9)+dbL4bT|CpP@PYnAXLjw-1Bl!}zN&2fQ^7f5odGz!`+v6kEKS
!2^S6uUWksmuhc4y|O-%-woOeNU!Ju%P|ofAp9F2V=h^$E9=EE3|sT7!GJZsmUY#+5AcUr^%Br0v
*XW)>N>)9h1cbv1}g@00R{vnsJFXy*#jf70{;2EKbqZujAgX_*Pc9NWhtS@?ImJ(uh;-ip>&BJw0
Fvk(K)t)nC@bTF*?TrpXVjL9O}?H7WzEL=p2h6Cf{%Ep$QN}9K0}Riq5e_UH>_*lA^&2KL|?)%zp
VAfrA6p_O-oAnt;#(?rTw$Ba|O??*<G+Qba^?k-hbeFn3WAp@q%MUi9XWl||_4HV1_(gf6Pe-oi$
ht<_`K>~!}o%MNYr{_oV3ZxW7{u99nGuQ4KU#o*TiLjgnfE+PU$2A}v&14OOf7v&Lu{?nHeBZxOr
eef#9wir=vYzy&a#x{GIb!@X1HHfW6ulE%<vB+M$g%-t|ktCW^%q#6aRzXbrm=Z0V3C%Biffj)!f
_O8N1S^hduViP`a8!vV*3fhf7(rG)y0nQPYbJZO7Xc~TjRC6%-P}cxRm0xd<$!cGly$M?XsNaC6$
~U3+?knh2Cb!`(VIPMkY*I`*mi7Hm`iP*_DUFlVmt8RC1V$_pLha9a7EyypWtHKg&g|A!)a{0kpn
Mys*P=5a^RI5?~#Z(W4fN$!7En@_W&4WSH63|6}ubRPJ6x;(P8P*UB}iQIP=t{>RLCd$JU1SibU7
xV{1GB9uDpUi`W{@UI^Fwx~H~^G%mz;fWa8;Z__=yo6HDL?QLeKs%h_#{MK$yJD*AB$uEOh(%hp@
y6Me0iAM5UQ<?V4to5n)Y89Ta1%0ruo$bvKq4W`Kw(|(pL<M&v9FW-x-*x)$$1M2*4$*kE{v*Gqg
PgJ4^`C}g!?qI<tHTG~_aEA}_grbY=R?~uRJ+WF8eN>+N9zOkrQM&WV@qE({Q+wAP}dG$L0drl;W
NvDl|QvFEhC9VZuhlEGK+kJ-qCh<?b_pd(B1VvXixYHq@PYrWjK<VMzZ(GIWk=i<Q?932cs)@f23
Cf{n8w_BQ73HiN8^>H(Q<=kWC%iAE3Y|yzqdDY*yz>rt&HE@{OsPrkD0|Wnzmd`|a|Hx$+G6xOK}
u<f|$F4D-l#+Z;LfY&okI&5B5_rsR{Zys}v^OM2S7l@YSxxakf=G)rd3ygx^dK#l9$)ff;d1eZ*?
i_@QG+rX5~F|xsx1m&*g<XAUJA{<JXr$!|5u`bW_xjIq>bt2;~#6ZXy{r<EoOn1FMcJHF;XlHLbA
UxXNP9@w~<)60Q`SmHnPQB}@Iks#-?G&;XH8y2G=3Gr-9_{fveZE!$8P~{ga>k#9X4EyHZ+M6NPP
;Fm5OylSdI&P=3wkXViCT927k9&}qlzVsFwnj(@rP#_cPil3abn6xA|0&iE<|U-DY#maCwlLpBA+
nANrhAJb_czj+kfHIyKj$8jX(VY=5W71z`WD*5ms`igLFsX#ua-@=9q8>fYs2Oge#}~N3IMF#UJ;
tu*_sEVC>_Hq0mDCLy?C<hGGvz3?&|l8A?5rFqC;HWhnPh#*p?<&QLK_b;(#cV7~s<fO!QBV?I{R
2*)vOu2=5IW-u5dgSi;-)_P{d8|wojY%9Cg6?18@TynQGT~jU@T}gDsXduym(NLlxqme`-Mq`P_j
3yFI7)>RbGMY&=V>Fj&&Zw5?GkvIuL?MYs`x_C&l#;n%w36rtMvX)-8LcHsjto}L%$FKa{jn{1E(
%u8(%&DS-EHU$$09xsf481VCd|W$eYr{n#iK*8$^<%$48bZFIPZ}V*8=x@BP5*FE{?cl*Zbpx&#9
acyz&WF)tHe(W3VzbXyDuOBPMj#y108D!>;{3nHqnc7giW%L`N=_vt!xr>t@Z2GxCe>-|&v6HIH;
b<Z}E^d+PRj%V6k-=C0j7>b>!dYt$Eq!?4Xl*g4DHu-xlkL-xrqk6hw!W%za$@mdKs8b`hNIXRzP
@7kXY4!=WAG*30<Q6Ig+h47U7WexfP3gXKd4^xzkP|YHYE$Tevn5KXQ#POXen(|thMIh7TsVj(ym
y-qbmxdckyqZ$_4^z$)*JxJQ4neQ%V0T}>JEQuh7Ki`eXujda<f#%Tw}-uRm!I~7IF_^TNpFWeGP
22p{lAmpg;PL_`OigVf5yyt(B8RE{OSyU@7HkwE&k`}*Y?+?C{p-8G8sjR&O}0A9ei2wnHa;)9%D
FFZ8!HLMv@Mo7%*r{f<wg+HTRf|>00Yk+lrM<kccJwOM8&aXw>C-G)P9nE>EQa?QZPS^~&%<B1l|
|46lZDWk7o!dsL!-wVhw#2ei$>8_DVC*9dp+v0KV9;au|Vfrs?eng8p4cN%h~c@{S3Pwv-$m~eK+
CGvzw{Q{H`XJ%-$woQLF??tPJYVcB4H2YDXrEL?n_+RuZa{Z>|MnO9#w8^#m#D<BISIPD!{0T`TI
qY^1&9*&W@7FMnj!ULpr|#aq>-Pix_yjY~HP0>2dbGc~*T3+Tm7~$d>SKdf8mvc*^NRbSfG7NMJl
Jyi>6|uISI|@Eob!@}=;wQwalU%#VDpAUgWf*3`ym~T0eC?A>oj6gs!L@iM8--D`}iQIoh07W$?Z
B{4H!3S+I(4z*HE<cvKX(R@@T+#{glT8#;d1188BWu<>`R&$|=tVjMq)Pv9opNC1I`w=rt(>=v65
N=yj<C=#?=7^xD({WOcMOBkQAu9apT77KU80Mp{@hV2!jeWxyI~VatFu(!!VlYovuW1J+0ja|W!D
7WNFhM#7$f*GSki@EQqw23{j!&yY1Lgq7Uj<$g|t*wvhEc_1%@+3Y^~c==xXu3dyvmhDwUQ-+OJ#
8ZYXM>|=VmhQ?5rvaZ?J|TQwdP4ZDiV4AvpgrzDurqjbYr4Aab~qRM`NIAPrtRDI$no{t3vJfy?_
rLKfQfKIgiJ&eB4Q$*5HS<Ugh-f3Cq&9bHX$-5@(GbMp{EKinJK1>*S(xFtbDMfDRAAn$4#02!Ad
`HeiCrtXPwt?!s0>bC!I0w%y-wWzc>4;{ry5$+-3F$D~ZDV{a9<C0l4GY%G}XI+{``$m>t^E`o%s
An2~-VW1k9eD?;|cuQ2U%0iw=jo6Jd>Z8|S?=x+Amf?J%xhM{<8P@H2=j_;8T2A0q7GyAJe9-bWF
XZDAjJp0Hqqy0H25Bnhk;6%jc1uwwq0Q+?=z^-lL!81O;W0Z$NI#dHhv#y;_N=*@3kb8E4SSb`4)
@4BO9%fsfwwllU0OvFC9XF4an^<1jtM;zxxv+qD=3CsNa%yVD_5p-&9JOM*HH0<ZMfLMEWE9e(7q
@M`B~UwdsLUxA__aTLv%g_w_ek0|;DC;>+U~dZY6qELzcP}`-7$lD&|_%3fiv)T{bq)WIs;$-<bA
FEg{xs-`|S6%_P4HV`tRQvpatI67|xIO@VxBq85XU0cy41KD-Z1#cL<DA2Ytt14Lc2H3M27+#6R7
zzl!A#6+WD{1;aG9ZoIidXVseqpEh#K4{7avF#E4hcMRry>^s^+*k8bMO&s4;c=H+-(+5bhm4tL&
*z9rYVUXHzyW5@iyvMe`P9@s>?`F@=4{P5>#;t;mK<@NuUv8ERt^~MZFc4tCU?{+l!AO7+gRuZ(1
``1$45k818O#KjF_;T5XHX09g26(79~dkJc*$TTz$*rg0IwOW1^AIbI?K2?xZg;JU4lO-vu_tn$l
<iizG`57#7_zA+XmLlS7TW|;PO;78q|EN=W`2wZ6mY459XlO_obN50qG%fX5Uz_$jR3(mrpDhq(i
2MX9fy7<S9?M733Bk(@^n;&k^j43JyAK+is|?GxR6zyJuX}qfe6QG^KfIPkyMU6BL-=hY>3Y{NB>
A4hh@O92<9UY-ZnYaNz#*nOjDZc<j+*GzGsui@}LbIPTqb(V2Z0f&d@I*$8UZltzp@bhyFK=`;II
l|%fwlYNcKoi6l#5TVnI;jxK*PXM9+W08+N@u#&2qPfOwTg`nx<(URg2;HKIE1kvz1(oqepi>FPy
}{^E;+bBr$n4tzG!?Ylt)DaKFv6i?a^o`yi`$>oWP)dQKa{2A@O+FRns%UD@z2#0;Y{^>I{4@H_7
~asY!{De38e!D`XyG*nGP6U+IGvPp_7Fde3isUqm!N9bly~ST7cNf+ldYd5DW$|9iC+}<gE97W6V
|@^V^?{v&68R$(-r_Tl-Fw75*9Mtxs2a?7{cxjE-o2`wpG)8mRBhem&&qO!nOrm+p5A0Q2V*&2~J
c&|$@6Q{qkPY&JfwIQ31*P)L)~@o4;nO2-u+wkLCJ+aq^zI<feEcX7`MnescEF&E3qNsTf&E&3;<
_IL2aVi!8VPAqEa`~rV;4&Q2Ev=DDJ;0hcXf^V&KkYVwQ{d!15&-XeQ*Tg!FPBSb#sWG+D#t#>Co
*^D10Jfrr<A)zQ%aDhq0CL~w-02+SljtdQitz(FRqHcLyek-?Zhq<yLx-djjGLw~-Cp})iq0_XID
OESIQX+a&nLMDu0^pL<9;+R<YKQW#eRhj8b*hn_ILf<deb)-I$U`A__^`pMls%>^nRkCN9sJx;of
jue|jK%+HPsQ`F~0tla2
"""


def _load(blob):
    import base64
    import zlib
    text = zlib.decompress(base64.b85decode("".join(blob.split()))).decode("ascii")
    canon = {}
    names = {}
    for line in text.splitlines():
        v, n = line.split(" ", 1)
        v = int(v, 16)
        names[n] = v
        canon.setdefault(v, n)
    return canon, names


_CANON, _NAMES = _load(_BLOB)


# ------------------------------------------------------------------ keysym.c API
def utf32_to_keysym(ucs):
    """src/keysym-utf.c:912 xkb_utf32_to_keysym(); keysymtab entries all have
    ucs >= 0x100, so the table search below only ever matters for ucs >= 0x100
    and this port reproduces the ucs <= 0xff outcome exactly."""
    if 0x0020 <= ucs <= 0x007E or 0x00A0 <= ucs <= 0x00FF:
        return ucs
    if 0x08 <= ucs <= 0x0B:                 # XKB_KEY_BackSpace..Clear, & 0x7f
        return ucs | 0xFF00
    if ucs == 0x0D:                         # XKB_KEY_Return & 0x7f
        return 0xFF0D
    if ucs == 0x1B:                         # XKB_KEY_Escape & 0x7f
        return 0xFF1B
    if ucs == 0x7F:                         # XKB_KEY_Delete & 0x7f
        return 0xFFFF
    if ucs == 0 or 0xD800 <= ucs <= 0xDFFF or ucs > 0x10FFFF:
        return 0                            # XKB_KEY_NoSymbol
    if ucs >= 0x100:                        # keysymtab lookup: no low entries
        # (unreached from the U-notation branch, kept for API completeness)
        return ucs | XKB_KEYSYM_UNICODE_OFFSET
    return ucs | XKB_KEYSYM_UNICODE_OFFSET


_XDIGITS = "0123456789abcdefABCDEF"


def _hexval(c):
    if "0" <= c <= "9":
        return ord(c) - 48
    return (ord(c) | 0x20) - 87


def _parse_hex(s, maxlen=8):
    """src/utils-numbers.h:88 parse_hex_to_uint32_t(s, 8).

    Returns the number of characters consumed, or -1 when a 9th hex digit
    follows.  The prefix is not accepted here: callers strip it.
    """
    val = 0
    i = 0
    n = len(s)
    while i < n and i < maxlen:
        if s[i] not in _XDIGITS:
            break
        val = val * 16 + _hexval(s[i])
        i += 1
    if i >= maxlen and i < n and s[i] in _XDIGITS:
        return -1, val
    return i, val


def _parse_keysym_hex(s):
    """src/keysym.c:215 parse_keysym_hex(): full string, 1..8 hex digits."""
    count, val = _parse_hex(s, 8)
    return (count > 0 and count == len(s)), val


def from_name(name):
    """src/keysym.c:232 xkb_keysym_from_name(name, XKB_KEYSYM_NO_FLAGS).

    Returns the keysym, or 0 (XKB_KEY_NoSymbol) when nothing matched.
    """
    hit = _NAMES.get(name)
    if hit is not None:                     # strcmp on the perfect-hash candidate
        return hit                           # (names never map to 0: NoSymbol
                                             # is not in the table)
    if name[:1] == "U":
        ok, val = _parse_keysym_hex(name[1:])
        if not ok:
            return 0
        return (XKB_KEYSYM_UNICODE_OFFSET + val) if 0xFF < val <= 0x10FFFF \
            else utf32_to_keysym(val)
    if name[:2] == "0x":
        ok, val = _parse_keysym_hex(name[2:])
        if not ok or val > XKB_KEYSYM_MAX:
            return 0
        return val
    if name.startswith("XF86_"):
        # XKeysymDB spelled some names XF86_<rest>; retry without the underscore
        return from_name("XF86" + name[5:])
    return 0


_C_SPACE = " \t\n\v\f\r"


def _strtol_base10(s):
    """glibc strtol(s, &endp, 10) -> (val, consumed_all, overflow)."""
    i = 0
    n = len(s)
    while i < n and s[i] in _C_SPACE:
        i += 1
    start = i
    neg = False
    if i < n and s[i] in "+-":
        neg = s[i] == "-"
        i += 1
    digits_at = i
    while i < n and "0" <= s[i] <= "9":
        i += 1
    if i == digits_at:                      # no digits: endp == nptr
        return 0, n == 0, False
    val = int(s[digits_at:i])
    if neg:
        val = -val
    if val > 0x7FFFFFFFFFFFFFFF:
        return 0x7FFFFFFFFFFFFFFF, True, True
    if val < -0x8000000000000000:
        return -0x8000000000000000, True, True
    return val, i == n, False


def parse_arg(arg):
    """tools/how-to-type.c:269-299, the --keysym branch of parse_options().

    Returns the keysym, or None when the judge prints
    "ERROR: Failed to convert argument to keysym" + usage and exits 2.
    """
    ks = from_name(arg)
    if ks != 0:
        return ks
    val, consumed_all, overflow = _strtol_base10(arg)
    if overflow or not consumed_all or val <= 0 or val > XKB_KEYSYM_MAX:
        return None
    return val


def get_name(ks):
    """src/keysym.c:74 xkb_keysym_get_name(); None == error return -1."""
    if ks > XKB_KEYSYM_MAX:
        return None
    hit = _CANON.get(ks)
    if hit is not None:
        return hit
    if XKB_KEYSYM_UNICODE_MIN <= ks <= XKB_KEYSYM_UNICODE_MAX:
        return "U%04X" % (ks & 0xFFFFFF)
    return "0x%08x" % ks


def header_line(ks):
    """The judge's first stdout line; None when get_name fails (rc 1)."""
    name = get_name(ks)
    if name is None:
        return None
    if len(name) >= XKB_KEYSYM_NAME_MAX_SIZE:      # snprintf would truncate
        return None
    # C "%#06" PRIx32: 0x-prefixed, zero padded to 6 columns; the value 0 would
    # print "000000" (no 0x for a zero result), but parse_arg never yields 0.
    return "keysym: %s (0x%04x)" % (name, ks)


# --------------------------------------------------------------- table plumbing
_DEFINE = re.compile(r"^#define\s+XKB_KEY_(\w+)\s+(0x[0-9a-fA-F]+)\b")


def derive(header_path):
    """Rebuild (canon, names) from an xkbcommon-keysyms.h, first define wins."""
    canon = {}
    names = {}
    with open(header_path, "rt", encoding="utf-8", errors="replace") as fd:
        for line in fd:
            m = _DEFINE.match(line)
            if not m:
                continue
            val = int(m.group(2), 16)
            name = m.group(1)
            names[name] = val
            canon.setdefault(val, name)
    return canon, names


def emit_table(canon, names):
    """The embedded blob text: canonical name first for every value."""
    rows = {}
    for name, val in names.items():
        rows.setdefault(val, []).append(name)
    out = []
    for val in sorted(rows):
        group = rows[val]
        head = canon[val]
        out.append("%x %s" % (val, head))
        for name in group:
            if name != head:
                out.append("%x %s" % (val, name))
    return "\n".join(out) + "\n"


def main(argv):
    if len(argv) >= 3 and argv[1] == "--emit-table":
        import base64
        import zlib
        canon, names = derive(argv[2])
        text = emit_table(canon, names)
        blob = base64.b85encode(zlib.compress(text.encode("ascii"), 9)).decode()
        sys.stdout.write(''.join(blob[i:i + 76] + "\n" for i in range(0, len(blob), 76)))
        return 0
    if len(argv) >= 3 and argv[1] == "--verify":
        canon, names = derive(argv[2])
        bad = []
        if canon != _CANON:
            bad.append("canon table differs (%d vs %d entries)"
                       % (len(canon), len(_CANON)))
        if names != _NAMES:
            bad.append("name table differs (%d vs %d entries)"
                       % (len(names), len(_NAMES)))
        sys.stdout.write("embedded: %d values, %d names\n" % (len(_CANON), len(_NAMES)))
        sys.stdout.write("derived:  %d values, %d names\n" % (len(canon), len(names)))
        for line in bad:
            sys.stdout.write("FAIL: %s\n" % line)
        return 2 if bad else 0
    if len(argv) == 3 and argv[1] == "header":
        ks = parse_arg(argv[2])
        if ks is None:
            sys.stderr.write("ERROR: Failed to convert argument to keysym\n")
            return 2
        print(header_line(ks))
        return 0
    sys.stderr.write("usage: keysyms.py header ARG | --verify HEADER | --emit-table HEADER\n")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
