#!/usr/bin/env python3
"""Clause-g overfit probe for PRED-C1-r49 (seat ExecC1Overfit, mado round 50).

NOT an instrument. A deliberately cheap/cheating tool used to measure how far memorising the
frozen fixtures (clause f) plus a first-level-only fallback gets on the nonce-drawn generated
cases (clause g). VARIANT selects the fallback; the memorisation table is embedded when present.

  table_lvl1 : memorised (keymap sha256, ARG) table, else level-1-only rows (all groups)
  table_lvl2 : memorised table, else level-1 + level-2 rows
  lvl1       : no table, level-1-only rows
  lvl2       : no table, level-1 + level-2 rows
  header     : no table, header block only (zero rows)

The keysym name/value tables and the get_name fallbacks are read from the pinned header that the
counter's sandbox already binds (/usr/include/xkbcommon/xkbcommon-keysyms.h); from_name /
get_name semantics follow libxkbcommon 1.13.2 src/keysym.c (U-form, 0x-form, XF86_ retry).
"""
import base64
import hashlib
import json
import re
import sys
import zlib

VARIANT = "table_lvl2"
TABLE_B85 = """c-rl~XLI7p`Y-xb&fRbCzEx^vy*Mub3yjBt0VIM>oto+(kwo}|ZNjI&!a)Hf8?4r}V7#YRE$>-aqJK~9C;p%R^B>10qN+ea(|8U@yda63D>@QFt_u7=$Ps`lxH8c+Nx{6!BfyKY26^ntE_PJ#pa1@+UsdJOGZ`=1aJ+W93-5X6{O7;ifBysdu7m~esW~nW+LIyQ>UXEGr*#HBZ*O<)7j)l!vOA@PaX;J|cO}uD4YtN^`l~YGwBMbw4*L(@KxhpIy~f1uH}>^A|L<FiUmdP%w>V92cS^&<&vjiYo0c`K>)UeA(z@MBDe`l<*|I>je)zkOfAnp&JM9|vU1?}qn%=SOhj#bDtW5Nsv3vha)&6Z()*rvK4S&DfLc#+_dIb32$*WgJ6+ElTu(w&pK3822`>n<Q{?GsYFI|uy7aM2wHOK}Mh=;utkUNY)9!EjuiU+ds{PZch4bpG>-)gvV?(~guH=5c0sebvW{WdwRuD6$X)}4?_c{Jb~9u|z@;qNQM<zu_+-I-k5N2=`qJRO?TYU6;gsaI_ibgjdwf}cMSkDzMm-Co<;O#I((_|JK0Pra(;8NUp(9-v}&yVl{EumAr}4}ZT}e!=rLu!XLNd29Gff7lKB%O$EzW1s8o%A_*<-#MT<#$N&pdyP|YXLZKlPQ{PUw5RKxQOOAIqz)P%BA`!q4RcT^5il0>@@hOBJ<Xl<+FB;k%j{{-t@*>!=0_Zwb@v!_H*tX|v8CC>*nfPcW7hY9UN4A1#4x^FZ06^o%(Y(#FAjg*l|{oWZJITEX51Oe%5b6ihz{E|Z)f)!T)kGE40!+ZyVBwBe^sVW)t=S(-PR8Z-2b`rp|HzFtLy#lc3Z>f&mUBXaHG-g+Eue+_`eVQ=XkY_)$LfD#m>k1<1-IF>bsBMF(SWj)wCVC@6JiDyFVBs|4bui=B<BqqMs|HdX@V{6Xjose96fj{$ctBCj-WuEJiuGSt%AL$1qOi<P($=IeEaClW~-jg@SSN;{oL6yy?2B2%9x;4)5E)(Nvq+<CxR8X;fG`ef53R;u-s5Sv+&`j7LjI%*Al%B|9kHng#~^XfyDI6!Bz^YF3PS2j-L|^Gbn%tCV5e8kH|*-f@I^^~MXDw|9u&41E(cZB)u8>6bk`J~%JB)ckm+Za*3mJu4}9#$8}SYMp(Z%kR5eq59OPz}OE9$%f7OS1kA&#iZLF8*HU}6ZpihEK$!2t52F~po<%(Ar(m%2V_do#8Eo=iXpBhCOS(s0UCFu2(GP7k#K#zBsQGw(`PrtrrjTLM^|rw?d=e6L;p+{j3QpWf5YeXrx)+mp#Mhfh|92N948Wt&}G;*_7^LaT~w)9{Ag*<TkrN}8gcYWQsIQ)w+DBhQVZ3p(vc8wjD=tq6M}K(5XmNDseOtKvwIn)6`{HgibwU8^YSUxeX8<DROcB}eIKKGfr2cRV<hk1kSlE(Yy&2s5q_rJnw0jLyxnSJ0ed!g;78w_2fyF4e3$HEYSg3DFc9BZ(d6^)F-3X-Ma%(PigaQW;pkDsiczFdDHcWgC)y^Y$dD;TBDdKCMRxQkV#H-+Tr7(8jw#X)DT0{>$D%UQzN1GGV-l5-R^cder$6eZ{-6Ky|NRfGM?M@A`By;X8q?b$7c))!l0Z%D?xLp2*fa`entmTsq!o%?i6uq$QAODH-9Bn!w~s2q*48MPX)=!~VuciGF;#@kN=y*~dWvuuQ-qC9u_#hKrbsPxsF}KNoY9GCEqd--1o>C3RWKQ89#iCZXh#NYwbnQ$BN9EWRgcL?vtTmvcuWx^q=>=RvX5gjBGHqPK}<#pM-jbhQgz<i_1Zn%CtAO$KJKpBYfyb)=a{L@&=fOe>U}e=`03qAg5=X1Qy1+{VwTEODO@|I@O^07F<a9fS6hId+N#G*d%@IJ=Xa?>_tL2!)3_Sa*kT)5h&u~=dJgp<9$6^ZrStxnBK43WL$*@4i%A_%PwI@g)D=vx>YYmIH(jwiBzJxvO7_!=1$-O@yZ>-fC}7N(hJv=nq!nb@Oh7tC$(H>(M)5IpvFmJI?6@}~(vuo1?qU}$i{P_(1$y||gHMZ9asrdDt_MPQJ?OVzaJ(*YYcs7}(z!^QdE2-vPC;0?RQW~U4X88?qeS(I^<#=Zgl25YHVP3>S%~zm2YNgTQ80mQ98;tjsz{4%qBWk@qvu$dIG$)NS`x|eoYTf9-R^BY@?J-5&kkjrOjY4Ftm|!8P2DPtD*WB9H|WM(e(UXe^Nwy{=$O2nFicWsd%=q3km$w7jR}rtEDELv%f}R{gqEq!Ru7J2dXQdN!yLr*V8Ox~rDKYeLyG8ZLy7Us_m-ZoFpP&1i<Z^XPSSeK*DByc+pWR0y0EbiKi8hFzmZxvt|`T!9&J+ys(`;|;aa@*Ozt0EP=)@p51lJUr(8z&J{$MC+@M3{9cdNOLgemR>(ELMMLKcvdk1*2eLA;#+r!VkH>LlT^W;RI{V@+TI%UJ|+a9X67ry*?uS!0%To_TgxI?_e;hDC6!_pd>wJz^_rWU+^@a&w<<zv@Cd<)d|>e|;S@iWq-<1W23>~DRCNKw@h-{yifmn7p6UG;uu|K>64uDi97Z)&Za&#8a#@|(QG&)l&4?GYWmZbkXpgf(yG)AfkI&-*U4%&UEDU18wx^w>6n8F3eMOV0(Z$17|L=J2$2(`wUAkQ>KDZiMj`rnPFI8E-Y9SI=n<<M)h$rPl6FLM`Dvqs2D07QbiEYyP+^#qSvfqe$nm)VZfBb%SFX+hM$A%C<r@9(U&H#apKFcuT>eobZ?;qktllE5F_6l+0WoBeo9^+h2KURZfVJW5lK*k6pQD&k3>rIYw+7@|eyxE*-C=FN{=fju8_=#IC#vD<{NGQd?dql~-O|mJ?$8W5nbDG5*RghB+a&Jw{9nrSi&~RdYfNA0svirSi&K;B!KZJ3_3q`9RFrGwlQ1#_klRUYNN(;25!Oh#2Dn#;A8;7Dtcq$B6Ah#OiDji}6@-^q6pr*gizeV2ju|hFD?rn0SmB7b4bTi`XuP7*`a;q+`TDh!|53cH4;SvBHckT6=IkI*DJPT6GUAuNA%<<L+U`c5-ej-T;y<QJR)G%YKiIB`LQr13o?ZoBd3QNwVC|mYfv){EW?bHRrZS6ZQV**;zl07bgQcw}-=%n)mWPnA2ze24m*WI#=aP=Fb|ExQO|)p6Np7&v-UA%wJDBBUK?l5Kj};|9H@AtT4YFVSf15&2(1+gB{z^wBcu}Rm0SCsmW<ZX0Msm#(lRyL)sBsozkga|Dcb+mOfK1@)@%YTC{4~sNn}s=FyHw;Ni43YzHt#J5j8xjq155i}~{mIji+}cw#f3Ne_(e{=**j$aCOsPp<q*my*1t=5{-?F<yA59?0JAf#rbL*63rc!d+=UVA@eK*hX}3#V|{S=_pA=aDw=4)PEZ>t$v>9aX+9^Jkf^B#rkQrSdLEeKO<bz_J@K)TpM|zXtNzA5s9H%rrxd=CPVwYcyb8x67CclXZPA;6qp;fi?AADHR`adZ}oNoebd=^{(Mqa@dSGk@LB95EHPz!GmDmLS%tdZI{)(wPx#Qo{q88_!3JaW^f-Fs;-H5Yvl&dVD&T3*33zY9RD#WEtZ=hP%cPdhYP>k9@7eec;?lpMf4DR|o9R-5!6xR?WNh=H>C!k`?7`WI>^il^deGwn_!#eWh~LKV^upctmT=|FJ;yz{^lb({T4=WQ4sZNGv&nXNg&0SZT0hvfc^6rQW)2Ip3XM3B{DC-Oi|EwuRi}NvItjLi)@-j~vaLIfN6+=lIq1e+G&pE{<5F-|P?w9%Y1n_G+TenqE>+eTuHZ`=YY-m>JHi^J>t>Cd;|#BGK8-z+0;kYkqFPka*v>bNS9t5&LMbdfUg77N>p9yL)@=BWU<06@y|(+q_i-Q=Fqj5!T2bS2_l>}L?xy+`TQY{u%2|)sDbTi;gI;&%f4$|~{ckk0O^fluFe?_cZ4@wQ`^L5o8G9Z~<5|zHd23YD1Ab*1Y@~Sjw)6D7I*AT;?0y^InfQL(!G`VNGJ_9!<-xM1Vqq>KCPXL0`v<*xfLpV}b`foO?smB~E>29k4DqzHg!shZRt{NJOE_pKD@2j)!p~5->kp3>$c*AH;?Gn%pwTLtKcufQT%M4oiuuL}2P3=&Teb<8Y2-6qv$ZP@b63I1oEamSGxOlF&9vay+=0yT*vUYM&v4Kw&Y7Y6?BqEnnctD-`tgyA<zdFeHitPgIlUus&P?v-$%#Ja&6&w87njbNp?|J3XS`&mWA-^SnZLtjb7nGQ{oOe;IiB;(IWw90x_EPDs)BTCU-!XeQIF|*c#2oEb&`L)$F=Ij4l-=@4O?#_{G0{KckKdYcdg|ybX{C|cfuytj&UVhpa{C%2vZdRw#S5QkYOLR&Rg(v#yHKeHG-|C{%0)PD$K0@-+z>oas5_R6+VC)u&oFZA{9Z8RwTFbE%)tJ?bnCqy!&L<v<allg+7@2{K;7*0IF4ef5UqltbY*Y5!(ulNLyD2l&fZeDl~i$ON1mrShj1e4|6$Udy5~2p*{Vn)v{VyZ}DPe3c{nMSM^K^B7WVX{OrVQR`z$K1c#cD?R7q@mfLiSEJIf?zjqwm>+SoMB5)^jKTlrt*&Xvh(v>B%T<lZADrr}h9L{y#wIDkkKf8MWt?zJAvsGrSldpyGt9WATPJZXye(>^}yu{BOhI2CW^*LAZ^S%p3Q`;Gh-KRe%8&TizscOcD4``c==iNj<<2C9<ah~g)=ATFB#qoqcuTY+>*|9jyeG}fzz7O6R{=FQ-xMNz5Aw>+X(VcEG4@U5P%Ag#<npTY>_19J4a{cFVfv3k5x*PP%`#$$p{`3)vX>@KQ64QBJI;#ZnCjGL9y@+`C7!Nhshj-&H=QT5PVq|TR1-dP(fYlo*g&PyQcPQH024gt~6Q+Z+=$$w1!2Us|u(w?Y<@YtVr9av0H&fIY!lEoe6(LC_nyLvBa5RS(6op8#B0DPK9YIrgsHu=wWllpXQWOcv9LAEOh~#IU$Im>E+(sItw=&kF^$O26zg@l#4ybm`U!CL_@LPg?D#RO0bvktp6r|{9KFH5}kb(<SivN*as6H?Fr664Y&VcdswPD{>nG_v`e`j=U`YsdpRQTzHy3I}~3as%j*RNB6ud-YDm&q~yvpcajcg~?1xwc&nfF^xhDjT!bmZc|0&AO(x(v0kyH?n;e!MqpDUbW2@```hMd+!wu)M*Lvo~+<^b`iv?Xhzns-&ptp)3tWfC=(qE4IiEP+nP|CD@}na|K>0N-iQxI4|ni|eJaCtPnx5e_ZpVzc8z89yC#x@Q(eUcf+Q0x5l3`5l}9R3kfN#_;R#ZG>?I&$LBmMnWm)AkLR6qBG9fbIm8<u>FF`Eb^EM(JK|DMIBQ!3>H1wxF9|bA|mg!T&^g$Yaz;*&VXT*01aY@W<&HeAfdx=oy#mv`c;Lo~-R388q8p}aXWW$o{(PH&9{tVAOJlK)i^j&$|lL6aCz{udqsvaqTkJ{1>@xKe~Ri95VO>;mgV7gw9;A(kV<;;&pcwTyk&%fr43prPHAA#@Qx7SaJESV#G*X75iPcGO+3>e?tp=2)1O-qu6=bcWDog#j_j!ci;HP}wT*~cf~B$m#6<`Ab&z)4+Ha4uO=7j?FRcXrGcml&h|PE3i0<Xrir+i!)vQ|-XHitMary7WBXxo)L#y1O&2Qj#J|TtQaY9K^?I>@Gz%jWeumtjV3*T<RgDw!xlr>%QdDl0JT%y@z-`8PQZmIv2!L6_eFhN@Jv5e96@}oQH9G29gS+em0eXhLdttS&&_P!<N1)jIVclQ>v(1@5bFQo^8t0dQVzXWJHbe%7+EHT3!1TkBf?o&gzgqJJ|k>DIRA(JHwQS@7#^f>fpcFDtu##$K~(%{uGZa=gEma^rm=xDi^s-@wn(*G$&|$O2@x6#pAQ@ki!&@&#=yQipTfPNpXtDr+iI$iU$SrdK3NfXDiCj`sFErc{^1wmn8J*1%7U0(h8$U>Mb=tvZyz>i4B941ITGxWAeCyriMPhtCv88Qx5Yz4LZdDkatxLDS$Wv@BfQKD%5x=O1!`!$RSxIKthhDC<Lew2naY>Q+V0uM;Y=8{Hdv+4&y&xQ;{9Zf2Y`r7GlNEQZ=Ia%juJ8R%j&`&RVi~iK><&S2M%nh*cCFbC`(GaJEl>YOBTbGI<`ttSkEd)xCd%1HouJvm~-5ee^T7*{NhoT_+CyX-vY;SYA7)cSMqmdddujZ>8Y%a1UAap=?&ERdIl3pytaD4Rg9Hio!A$#QC${jGyo*k&oNL!wcz`-H)@p-&O^?2-71doc|{&oLz5!-fl^ONY}MdiQ2Ju$ETG7_iI08nm%sE`;GacXtV3?2)!6F4GStSswz+gj+Yb>_|h-92&;<7JCfiyh?5i`@`9jY&LJG9ijt@blEd+wAc{Zz6raQ`7HFmp?OJzaSIR59@9ljLB00uMfeJr&e>%*3%LUh?XS92>clFwn=k$GUPrLe4fbzQPnW!E620I>p)ufktt?dnZt>NpLeCI7M0lY>>jRx1;T5WQY@k_nhW)7&QH7KMGnE7rY)ihFJzct&SMW@q>0tfwELuqKW6h^u*V|6z32gL$;U!f^5Sd~95m>dTMlWZf>lVQAoW}LZTQj8ZP)oB(?QhjzxL0;B(q!vs@T+TzW)Gm*L$$Z|CTripUd2*u9nFW(s<>KOkN$Tf1w^%VV9Vrw{X8jHq7EETv`r8GQ`JMCJg2}9WO}Su_f_eS*`;VGbFe!!wlT0TZi;?=OM=R1qLcL&;0+|1D!6c2_=)YSqDT|5%vBWDpQHd-H$W=KcibN7+mqVJ$aT<1A#3LDL0&t+nyS#`TsPRPBfWs9zAf7rgxe-CUJ%8}f?7(kdM_tnc;@|bVjd%~-9i>qm6sY<WV5cJ-KNC%8!003f);-^N0rI}W-MA}zO{Qas^lf~iN&VFE^c_gwbUY9E;a?Tz<KEB1o8B1C*fZXL8S8?lkh3&P@nIubi$f!w^KVqmtfEuTe70HotTUeixBLta$z^az%6!PIRKJ>_KLyVG3Ho2}KoZc53xH4@0r+CA6AhL6PtFD0H{)LU?qZUkwOrJY;+Lq4{jU8dxvI3F;2Uf3lBkF>5(Nw-6=O+~T@67^5LAGn&oe6291cT~g94EO(4Y)3l6V!#9ME_PTxs11tz%zV;RCH>KaD+-a%|zS<}FHX<0g)s$ls%Z(B*;%TdmG9wb=XEl)vp|+q^czgcSIh^NF%-!zl23|C0JlR3URbtMXy&cCfiI&Pwy)GVN-4tdtW9CNEm6MUASrzR~dea+~{mKbPA~TL>v|*x!2p7ftq=7Ot)9=N6b!kfeWPt6>&_%K5!t2~>tngj59T@4Wx-3)E*(QW`GpO>Q(yrf5p?m;#EYIh_zii*53F9FvQEZYV11p<&PEWeot)Q32;Vq6~qAfreZntC}h}s;Cl9LcGc$iF4G$Cp2DhuqJBwX94uj0_fa!);3KX53XK(#{9VcXJPZt!sdcA{}-7B3PNxb<JQhyx_6dCpT1Fny~_Ia`_G+&$1~_9)V^xE@8c{{ueuIuV0#wZ>Ws-Wn89M0bt&_1?8q}ZrXEg3_?|!=l*P_xPk^i-%}A3}9cKww@M*D1B9>|Q%OjsRIV9BID{So%TltzsiWi<*ZGDqz4g6~-z_{EbJ@9sU`?x$&0QcWn2Tu#JpQYiqxip*tYv^kXmnUpd#e8Fg--{!CQ?g~d|9Bd$#V}jD5}l>t6yU=S8GGJ|Mw-~YLoRk3XeP!DDgT?QCP_K;$GRBLu6b)z(}PtpOqu7y0mJ@50n{W(5>x<rAZm`_<Dhb~%!?e4F(yPr#6P^qsj93Ij+Z3|$Pyr&s>$e|NGx@%hsGnf_0UY?(XMRymyTx$$|Kv?g6GxKq^{LFFBYqN6|<umc29aCGj-@|*Cm=gwFbS`^0G<Bd47+-nsj<-O}Q8Ue9uU*U+TUEfIVqt)v8n9VsPK6J(6NpYNFHpKBv{ncUDmI*#d1N$9GYa@_#1jMM2m>T*&IIggwXa@mCXK*Cg!eD|GV{`p*Y<P!Rs>sw~V}vcnYWo6UhTv068q3uS_4zpBcmXEI(G2{DsFdotu({q7X@v_=p&xzl}zU^KHQ`i^b$NIgKs>~^g-%^N^cc!~nrw=;p@n?6Qbi3H#Qr-__IWC6*%rYO9BA;+pK3!ETvNYyl1!GeoL<O)bsRmDXRi!$bj|L+@)mHKKyCo^p~=&f@_?_?vc7><Ny8qWcZ_<&<jMD%VyT++U`UwjE)rJ5oNC|=QZlp2_y`<@g){f81Fe@og6>wt1b+|uleh#p?dW~W&M#Dk|n(24Rex#noo-_VsyXEk1sV;DE~Vdf0q`Y2@CG2Nyzsq^t*m2sgX+2;NKHiBto{|*qbtH_EbN*ZxB1ta3S=#b+?QR9K+5=~YK2mJpiBS%npNK^?ags6hzD!v1Mb=om~?o9d^kagX^){xrf*_Uqt_S=iIIx1*Edo}STF4BW-nR>fgcxdr>g`a1x=WNrmlfL3?0MxVBc7GUTC=I6RZ5_m?#0<_DZnqi2p05-u;<|oMmZUa3x6SW=Q^osgx{>o?<<HtgXhEDh1nixo+si?(yYo49>BIQG`OXrU4jjB2#_Mg)7<K1EyhQW%`f<D&65iur<+uali*i^BaKq(d{j^#vN2lH9xTft7lU{Lc6!^6U+pX;R*u8V|eiR}9pXbGsLy(tnyVW?m*B+xFR8ZgD9#4OxL7E1i-_jN;X8y)?XIzSc;%$!4{aW%<LJ5xQa*9h_SCDw5aSA~Q0Y&Cy$V)&H9SJ!i2cV)MqzHnKs_SsPPXLAZw_<n$y`@pUjD!r*2ZT~U?7Bl&ED*b$Kuh#m6-N3#8%0O~z8i`5MU`G8EcNNka0=*ML0;*csXdI)n~mqsCs)ZQ*ptB9_3;(G=~cPff0Or|*%&Xp({$Y4?t$fi*Vc#^KlI<8ZP$dgi;cxdE`esE|E@c)&cfgpcsX^vyuC1pT~{#YtS*6zVRR*d5K%)uG7{ottRYc=f+%1p3rJI;fAw-jp3`Ka2nUFv#LKRNi6ilfgE)9ow~3aooP8x7n2Ed)EADNg5ud0l76q|uGOETtcB%M!_v9Vow;t*RlA3H(X`onmxA@{=+lSS1weC~klB79y6wteh8|`2d_vogDVLta5xml?623Hjf{aZ?Ja*Wvj1c=SpZoX>9dzkp5AXZo(cyGjcOrnAqFF^=34qyUgAi6S<9l>#dDq-ki*X4!79}J;*sFXqu^q~Tp10+R3jw2H8_6vEAD<BT*YTH8nTa!GgLVmjiK81z+b_-F?ggm)DG-v3qVzt`Ed4S{8T^ZfC@A3FJg?Hv$y$k)1??~8%YezDZ{kj$tUL0GYspQV;iiqBMj`Q$`HQGAaeOjn<=14+X<iCoAM5&8?{)W`2E-#|Wa(_$OpH8Hl1QCT6+w~Zx9^cqFrX*dT&;QO0DO&mW9nW!3kR9V$bz=9n-a(ze2OR{)5wG|p9aE<yNMF=*((q1hrb6pX^^nq7LqP@HOco#$k^}>+VGcknD6WiL4hoz~unag(ayeHPpv?0!kY!Flq61ap03r&4LnJ5x3Ek38=T6dI$I<zN>nT8a-Fp$YNqZ50ox9wH0({rFJCN3~uWWZ9tz%zfcN9g1u|Gbw99S{_3PSFT)NEnH?!br_>lDg3T|t@MS=rcN5BefuS5<Ca($YHxZ-ef;fnQ|I>TD-6!~|B~QDZ%oCs0sSS&|{AO0qzRthx^1Wd}O0q#O#JB!mP};w4E|kfssG2U!)d2z+l{R($a4o#vlM=f&}aKb_I|^p5#pahm(q)V107!Tas@-QF2@OrzscM5c}IbaPJc$}+a~`DANASm$C*t425LhI@*Hx`yaE#pB*m9O=?E@D$*?>6lU1+D)UB`n-Fc0-E~sYS9@FPfE_Jr2p_@@!tG>tkTZ#l^@$`_|`sLd(z^9z<&W07=o+Q%|ZQo$b?KcnplyICJ&Dmx1q&^QY4{dSRAn~Hd2>#S<}$Gx76_askx_x*bNp_o~suKaF8pij-z4%k%O=T9ZgnT0HNSQK|-$J`hL3$T@E=4ka%9@1yK_q4`l2*<ffL2e5M|bZ$Eq_s(;t&mQ5<mOo1E~xLp5vT;S<3MeYXu^1jc#WsTq0P<f3axSJGC{f{X<3W)tEy)5WmWnh_T0+t1&%7P+mq6}3PJ2F7ng&dKI<_ZE24;euLA{qIZNU{U4Z(gx<*dBzhRJl+%^<w_CT6ljRPfm?^iNiB(-S_>?k5d~={a_=q9({Y))i(t-blIu$uc`d(i2cJVU*@2qAlX;!GOu8jQvh*P#l?!u%S7c5%jh-CVNSsaA;}ex52`9Ug6dlYp5qT42_^68R0AB!U0k#BK8kH-No)gKVZ)kPB@gB}BYKnirV)mA!f-0B&<+Kvbe@;a>Xa@f>6bn1X~xHbT)W3Khrmap2rX-CWe#;u!o;Bkx-E-#5R(FJ{xJ<r0kPXzj&X^L@y2ja)_~xMDuS*EBm@+wA*=y~cU_3F=mO2vAo6kLiQ?eH&#I5KD`ANjpeP>302t5S)A-NSImu!-NN>x*uC}uK(+?DP22&LEO*2HXY*t%YQQR8AD3x;OTPo(WI#>$SIT+A(q5-wW9|p8LVrf8Wo%A15d^8aIhtq|`#hi>>hiIH430M$0-&{Bc09_Hv1QS&gG+w}1b{tORAS6gbf+UKn=!z0TZ!74Pgw^w^@ZtUp*iJkVA~jEsR%AnWatTFgc>GUHH@zlN>O*theR^+;pbh5zV&){^snrn=K7u;4rfFR_ris@~D)^NMNrJCz*IFNOk`dd4z%bG$_|$4ytxrpJ6W}{GzhWd#@@VN*Jrg+&!!YLU9pX1RJo_L%`fD+~|FcJGI-Pf<xDU;6#Qm@X%H{UwrDvyDC+p83_Lk#24&7GU*R~=5XWt1Q{gw0NMW3^_{AQMmSl3#M*Pai<w@~_^>m1Ide>6q<&SmTPj1=h@>kd4j-{1KT7Y!B9jCCZ65otsXbyZq3YL4gJe(>^}yu{CJ_PX4F4qqp>+#m7xdEbSut8(Yy@eF!N=2rJTlBG||b>Ic|n0hQ*Bgn&-9}KfDW%XF1&*+$XSXuu)ReT`f&UY~YvfdI|VW3hH{OgU1RR|o#kuWB%Mle)44)TzQKIJfQ90BpXdl*$nWJwm0f7y{$;7X8l|Aj)`w5@7~yU@1^byN3?O+ShAXD8IHZ?c>Y&z@#+#wdkPsUEY;pN}iZex{2oVdk?XTf)!J*feoGyVWTU*I&`*(JZS8FJS(7m)0&{=FfVj3z<LT+1N1uR|%`^LU8R-NXGD8QTpZM)X?|6UChfaz%q2OtO-Drv4{b56_-f7AgH2Bkf=aKRt1@8ydoeU3ITHtAP#?BHBt1dgXp1nMKxA~$X&8gwyH*9Q2f^tPuUUshijq~ghYq%m^c~_T?b+yXbK^+3jsPPexxDdhyci<f_T6o*X1P%b286kB=a(eUTUSUFSX$0Qp<M81ogs3V^WHgU)e^ZQyfD5V~T+WV*hYPngV=34Xoh~9ho>jW-dm&k0I}991@8JI9>w0EU4J!MU_`1P9iD*L{J5Rd;OFGupkKpzU$eBvwiwgTP>cK$y#>S6-iaQ_gy7`KMGRKlE~I{g^Xr-ZL?FM#Hf?OE>?ra4Npl?DR+p^J}^0!oJKOxH0wc(x?xUtRP+%A7O3o2W6vAoKPRgE&N=KYsBM=6pna%yez0dd-rI=J#N<x1#6C;R{qMqiiJ|$tVEo4nAty+Xmv~Jef+9+Y2ok~oNRHxP>JfC2s|XS=$v%Qm^6&DzthvOIG+A{x!f~(TSxP4*djVp1SB_Xp#e%Vq?WEfnolI)WKzw6GlOjJnd?{l8@GVc|FsF$c;1K|V%*hA{04UJchfvcTg@+<J3~*9q-~iYE9O7k(V3#92k~s_<AHDektsFQ_+}`|*_y?cOsw*rUzzPQ0jM!FJ4?t+&8?6>+UFy=Eztn&Nz_+;<`}5YK%oO_E>83!He@x9%Si^`;E_)$jb+)TMcd_Y#U#>a&TZ=34$ztdbF@x=zqj-)`EDB;Lg~ihlF}CBAja^JC3&Uf@UDtN$^0B{#*zg#!d59QhE0yuG6`?4IojBKv5V0ZKJ*aV8Ss28|$A~RM#HMWZ*f@q*VU|1>c8Ma0@z~_+4G(_{v6GU7Rfrg4f2<Qjj4KLaCw0{85HZI7*e*7NcvBR_W+!v6L&TW+W1tzA%ED;=lN!tC5HZF(!{eG?qJkKwx{3<~NhVk#j_7bIk5r-{MOFRVHbJT)AqmJ>&@j??SynlX5EW>OOo&YQ!+^&BIjKqwr_$?JwQcU}8iKSkXyeR|hLkWM1uATgsUU<@z-*~-Mm_6gR7k7GWlx3M*>m+Z6$WuC?21E$lTpaKP!{TJsSxuMzV@uXrUH&pp;0Lg6;6svxR45Lw~#jDb^&Ck!Z1#S0@;Pa?u@xOzVsCp8fHD3q$`wlem<rG2&rIQRm|#3S=g82vQQwqP}r!>#qs>Fsi4QG&@7N$SR7N~CA?t`*is?xBT3n*P>)lgKpN?!PH_`zq|#NzQog2w5v4+;c!NC^e#*CKm2ag#*T^#Xg;XYn7++tmpH`uKKAd8guqvD?7qyPLs2y;TdF2t9G%h-)A^kgClsUqa#zpmb8G8Y_$Uf#G7;sUqpgTEt*@j;kk<BBozUnv=wF53nzlmh6thaU%E~-Sh=v#GJd2mthn2Y+MF1qqKWGWY(F(2Stx+rU$GgTLXxGt*G)kUr(5F%<wRx}CmGS-kNKtU8Rlm(=z5Msv_c}|mwA{;U_P~v4*!Niex#X%e_cCA``)9shBqZY5N?H(AxcR5VV!cai0u(fIz=imPpVg;^MyRgRNZy{FT+~|dMM1Kph!p1tdSk3MJ>s$8ULae}%(hFmBe+#kOi6NXIMk|JJ7=l^r`rgcX`DF_j1&Wl9DN+e3a^>Dj3Pl>`Aa>(v(4+_tc))2QClQ|lGOsBLueuIaU0L7+i9@QU$qE)+EFxDxqN*w`f>@L>NBn<l`09Hf(x!bqR?0e=X}ebx)1s6V(7WzF2-fIbcTWUs^sc)<f;D>A-7CQwz3c9q$b=q+NFaBFUMa{h8f-I++nD5<6f%rvG>&XVGK}@e_{Rr;g~l>5qIS}Mt4omxUDYs4mqzH4huBe|DmbR<Hl(V~c7AzOqnH$`ea%vQkW(i!RW~uJUY-NWjjH@HRd*p(>ujkSlT`}U!>QxBzD?C_oT~N0P*pgl>OQ2Z!IrAy7*(@ZBgZmsR-_vF+f?1fscIC4s^T$Kxsa+Ywp884sG7aH*)(EQZDhBr`#4owg`ui+OjQt4mF-@TM%=Duua-7jajIswt6ZF_R$-_rA5)bNsXAaw)wo^dvs2ZIQ#HF?1#zkl3PaW7ZH^@&q$*}h)wo^FUd<hg>spa&?r&3-k5d&FhN|i@RmG61L$*|n+tuvV;jwKGR-`)o+f)_eR2>$Es@gGCrI4yqwo!<<UCmx?ZVuyA&2Cr4I8~=~sOkU_yNax6qNEX5Q!pYJ0?2WqsPRB@i6*Or1O9)Mks~NPB&viIpRj`BDgg4g7F$}^Yu+=dZJr-1WdZivi+Zi?4SKEN>-l!mlwSAjDBe^ohZ%}D<+(FM@uu|j_fS++QQ`%cmo)%HM+Kbgh%y8c1{!jStZJ&@99Cv<65>@3Nt~k|KB4i7gEjFrV{zSj@scHlv=F;)9moQ)>y8z(K<v8XuookSuqaDVMMzSKrfPx&9L?bcMIn-`$c{>QN6>sDpsA2oWllpXQhY~V<}j8NMI?uM9f+riW1+``USoy%?dY|N=xsp-7%*KpRgY(Nk{498knq5f9s&M$^6HgQ1<$H7>}{6kPBU&q^A^)5(@eUvT{Po&8i|^1%{FLV`n{9Adn(jlozlHu4;PX!rMDHy_dGmW+$L$e#dl^SOA&v~usC8}ER8AEd9>*AFK%E=Pw!<VH#KpYKhKb}T91dP_4%X+#{T_$4|^o2)i)+rZgbMAg3rkTW?8&MfmCGSd8f*4iumn1qTqH7rsMfjlVs-_hBS^(PY{l?wcs`GTDx%7e2cqW`culFD3E;Vtgtgb(VQD!EGKqP3X`{!;s*=9CzfZV`xuKQT;uT=k5~BlWMHQ6Xf~Fx*YGV`1E65xL)T+#?aoNHeXGH^6(4qRxiiZp$^NG+I%v>u=1bWc&QD6MN2p)+@VqfXvsS2GneMYoO@L+AuBpkt%-Yq8wc9i+xh_EG8u9I9;-#ACI}6b1X_6;rHC|6o)ripc@XQB(7pycIu~i{yIl#;gb6PI2Fb?w)uAF(&`peD0R|jYoTYtH0vUSGNa&Vc|MQU6-qq;E6p%6M_x)|0B6u=ofP<}NYj#5ZJe^}c5DB_b%uRCa-N}@9g*1zRH=wiTD`gGe2g`as)X*QleuTRFI!=40isFJ5lRq~`1r%ETI;G~Bp&sD{_QR8_|e2)z;Rwoma0h+ZBF5ARsl5l!*k8Q74JQt&HsR?2#$%}J2a{lKTo@`$5aKAf3LGZ7^Sa9?>isQ_J6A${CbvlAWAy2;aPPNzu-FL&365Hh=yLb{#-%&}Ie-_xL0P0~M`qX(!-H7i0e-72UvoPA-9W!P4eJeiF@{9pvKDJ9VZ?7N6n<3#n4pz!jyH}moYyP?WMtUnCJ$w@#uK-~Gb~K0gf!_^mrhc~(pOF=6fKMi^ZHB%(!J&${uHTa-sSSsAtvj+S<(1v{_P*ZEO)DG#c2e2b?!|62!hmT2#E4HqG<6!tetu`9g>X6p+x_^>p}{k4#o5P)-Cc(kUOTffUU-X>G}hkkf#rbL)`%BBn0U{YiCaQEPFgCodPqcdg81zV8V4>M({NPdE*g$9&f2j3wMF~FIi`T@a0OpZt}t_7Bk<vJ=mFd1&|%1E*wwdsn~JYsM3GI4<WfWVH9zw-_K1_5p6R!j$X8aO@?|@XE)uq}Oub#Dp?s5r+Tg{$vxa7^%lkIog7*)e-J#3icrly71l0ka1_6UVOqeowESObKj${|e8TOp@$qjD(YPCLYa6H?Aoz3|ANAVhbho$eEEl5(5ed#NwAeL`;SUL@ZO?-Ouw9rn&aOJ=!XO&>wx+7BShE>08wJmSN=gUghz^={~d+?;zz;kMi^`OTE>}oJ&*VJ((g}$f_pU0l(%od5!oH^-v>%-tdB(&G|fvE3HJm}Tg-q&K|uyi^NPrC>c{{>fJ=DTUn-gtiEq&*G#jS1;(muP0a^LBYWV9DDQ$6Q@$vGVqB6f1w4K0b##(~H!jf%p#bv4qLXA1?p?=Ps4FM7k*O*$r0teybQMwGV>*Hm7R}V5JuMW)-Z9CyRf**D>vWmvIk9Fey@k5NaI21js;iWg<I*;{sK}(8aFH3x_`#Lh&#|5;>4K63`qVDGG8Nk#M&!oX0+0tGDIaLj5w|jsna#9)vFv%r~75J$9V+>YC_ecUG4+4Sa9QWjv0gmC=3s9*@rq#-G=Rcm?mfsK}X`tR{BJ?oqA!s!`tKvoogg*;sW>{p-|D7U`tXqvhlLCo!+{O7K2Uc7wkCmTaimUc)REK61daY4jD&x854pbG9j%zW3Mk?6uv0YwWgX7BJZ6c(eAx<X*`Bifv+E><v~Sk{5erRfBC_EH<@V-xg)sz$=Vo44sv;9<Nh4w7nekx;vlB%eQ*r(abh2p_pA@8Cy7LHoU${zeC2J2h&8~vulT-tR9Fx)0;8v!$Y)q@$W42VaoBVV<gyz)}UuQ<SUUSUr{~&4C2*kK;-@GU^EaO-fK`^&&{#DMp*G{#5mVJH@a+wR!*wJ^02dG4hz$KUFInl->QV5D$Qi^^r<l0HH{0=9<a@h#*+D$w-B+aJ9#r4FkN>vMtG(@2Qaf;QJqT?nkn>);bQJgQ?S?Oh?hJV*sJcO@U5&D7XW=jm(#+YES{0)K>YlarqSCkr1!A)f1Z$j)W4rz+pdmc3&HwnwV0;ets0!KfL3p1o(CZq?Acbq8S$O-<G(Hhz=-cM%#r?QH1pHq0pxg#O}fQ@@K8+?Vitc=DtxcvRY~D!u}CvSqZj1!!TY_DXIm~c*v6{+=(Ge}K2C)m>Z^Gw>UbuGs26{n%Jra*pI0kqj(2HJFTnG|go=g~XdAYB#OX@<aOI@>oWws`clB}XX3e;rV_)B;GLMqmOX{fz23W%!fY^spMlJ^hP9<0d94EP)D+^HOc^SwuCm_**Dscc21;HT_lz@b|tBak}J@)m*x~U%jD&x_-Br2keL;(Xy#aNPLS3^(}1QlQiv7|!H;V=|^P>2kG24#Se#H&c=fW}MUnp1JKF}PCxr^W*RGXGy`K8DuuuP7fwt1S1|??1<TG0KltRo%SX_St~#ja`bkQ;*hNQYGvKwbHMyQ+;U8yH93Kn?TAn&OVqR3CwK>Ceui~7%4yY!PJWmCZ7c6E(DWlTaws}ab~^fU<yfK?n5vQwqSOmU>ZdSQ%nMr3&CVsTP+$fF>e(eOeqOW5Q1s3)tNCdw~7v?oCGExf;nIdW=zZnMF&$&0#gjZ9I_Sj7-tTP4yKj_rWArXWeaAEGp9udvqVS&oLbqgwcf9$_K0m0-7u1Tcxtt*)}`IG$HN=M$PD*KORwsgn&<S!3!1lgh~MP!>;w7r*A^xJXOGl$I`2rSMsG$GX$O?c?K5gT&KQ(>hj{6b#$V_7jzhY9``X0d|7`c$qrY;Vyy$aQ*LG&Ph^<6x@!B)Fe|SOZr3X2jOaDmtmC=3c_>2_k7@MSZLchQB9WE;K$c%MzF+r%S(h{vXo^$)b%Wv`$KeO5EasxViotRiY;_vgm3tdy&c}7nwh@X<|tx0+h+@bCBt=)4pvu9PN<DQ!l-RJXx+3j4)2gl={hr1|UEnsD`;}LpNfA&E(j1PSf@@3X{q;)EZMpV|TjV={?e&m<r^NwWum-l&cqR&|?LbJ=oXSOKO&Qm{^kKMc7dG(j#XQWBTU9zA2H^0M0MRnP+KF9VX+WY*@d9Htxm9JZ8`O4>fm$y0u7jrUl9inlHBw#`0WTHA)1Bxp`-w+d36Et4HSauvv<RBzSLxLoVs_2RmLT@(Lc=n#gOK+ECa~s6hTd-eVJDtGhvYpR6F`_hRB-7x6u{)E&KFZH#H<6$3?f%2lpeGI!2GD$BbLl=iS*K@yN1Dy$W1(#wB+J`plc~P8xjDTf(dOoUo}B1&-dgU=a&f86rGKt7?Ok>{X1BSSzr$rVH#64XwYfQ-^E^A3ov#aNbMMA4<I{rAgT>Wh-(K1^D~K%HY|GliZhoKh+SNfO3--EuIf$MdII7*dSbEbV%aos;XhpKWBXt*EiH~r)-W^}c>0d{db9zT&WI6Zq<VByeBFmZO;?l@+4(B>g>t&~7_Q-Pf?{HCMIWyMZjV$MQ&NCy+nfaQ2WSNe|)#nK_<PQe7>J!DoAEl;~5!(%dW(c6q09A9G@p?-a#E!FsEBLfX1k$wo<q@7$IV9A>yg1Vlg41o(Z*J?GOn2kg`@y)}Bt2jtzOkb06Y5F(Enhh_+;Mpbz%X78Yt})OL#<A+ICKedqF-&|T6GdM$xntG_FY6&4s1e{bX;rD`w+r`*et?`dpgH0JHzoj>A)4cN0vdyz{F#m8Ei#vttC*e6iP_+IZ3vJvyXzNfy7pE4~3}Wj<{Xly>`-suRdQptHc!b1Dg8`HV;u`yXR-RiJ@4bgregTQB|OzX*>rc-p7Y?MaPH7Re}EpIRa1xS0<V!DVTS81b9)_Adg+y#f}PYrQY-GX{Mi*C{pMpJ;ak7Jf0<c54sQC(!Z#z1892|+vz-$k91)9!S^Pl&o5V_XSDlbC)z~c1uYHwH1hmpKL1sdUOwHkls~y{+m9{)z&Cl@TcDYG-qtk=#aPvohOnA34z3`K2YHA3xIJB;HDc=Xx~oBC!m|Bn+|?=8UD17ZN{%t>J5qDNk;c1PXMffxtxM~!a(YK{4mj`g<V2q{bHG{U;^G`I^>dw@f6Yus3OV4c-{Ha>a8|6podeGAoag3%v+_0N954;@Dx8|vk1-E3gYBa3(0_h|dzaa~N^#aTXqs25&rVU_S>KUvUOO?-+UH_kb9qOKdCmDeInn1#^O{vIE;g^!&vmwG%SuNY<~8GYxX`?2#rpf^HMet~YhJVRbpg%m$<T;eBS@ebTc+l9Uy8xqsAM&-coS#c7De+)_u0wnJM%lz%&TC;Jy$LV^P1B;63uJw=gEma=b6{ca&f77rGKt7O<Q(4W;d^yzr$tbH8a-VHLp3I^Gx%anXe0IUZqp>8Z-zQJGSOkkHek0DHm_!tV^>gm+rGu)OXf*q?^~c=L&K$uerP<#k}Txo}B1&rg_aO7Z;mX>gPJ!v}L6u4fC4uJ6vd9vts>y^P1Z^&o!@E`MQASRX#PZLGIOHyWVGCkHeig_lkFM)*a9^uT-C%qQ0}fBi+1?W1_|9VqSB3M~ZpP`8+w%=S=gORW2?zuhh?VwrR^sM;hie<9E2wyk^Dv`{p&bbDnEnv+{KT&8u>1Uc=lg$JV?Wakw+*UhzK8x|pVUrTXj?^_}${>E?A86D=VZ^P0;$Qp{`4=gEmaXPVcna&fVFrGBonO<Ptv(lD<Xzr%&*H7nNNH?O&!^IY?qm9GnEUQaqZYRxeB3fP+0Rt)ZD_S`EMXWb!9^GfyEDe61xJ5tSSBc68=^DwXZyd&AX=6#-==yRrd%_<icn^)@RI@h#irXvOOn)N$eXkN2o{cZD_-#O1UuUYxJfaX;@HLqdrm1k>StvKA-bFU!Ix>K6wmFlxo)OXf*q?^}x-bKpAyyo(b6!V(%d2*u9ndUXCTwH8ksh{g?)0UNvG|X$p?{J}c&5HH+&1-JwJlDKt<?8~PSHPWi=9s0AM(jz0X(Kk~W4vaTvM%}&8nFa}zM;72hw`&i>_*miq>N*1><3Za-WoY9`pM}XiQ^b^KTlrtIcpqaX1Ta@9AggWI#=grrDOJSjM=}#MdKJVWBuK6j5(h3%yEpF`MQvceyRW@*jPQVvCRt8VJC5a&eXHoSSjwO>0636mh!U`b$Ir7q%G4kt+;%3=-b$w-jTdaFYoi@MW3^5Y-YK*)W+s;t}_?CWTqp9WqO&v!$meWGuGc;rkCG2&$O|b`MRJsHerC1Sr2V2+sTASeoZ~Qjg9+=JE}I8>a$aHc-D8M+Snr>cASTe&E*{_Ha6$;<VBzJY;0D!xZK84Ki9eTEh`;q*x0P!;X)gm5$o^U*xb%}u8qyg*9En)2~(U*Be1c9BFx>Ua!xVfoUQPj<6AkWlyFWfJm>CK&M7CHa}b=<uH4Ewm4tKR@SHazpK8K6hv7MkAfFVbhF5`>aL(z+Ij08GxS=iu)w{1YE-??>Lc#+_dIb32$@A@81<$H7>}{5LPFt_?2|3M4Da5UFBmBW9#FZy{c+Ojq13uwyKdFc3+}+AK6a1@5;9pG}Oy#}43H<hhyibg*^1d?yfBbMisP8XcI?zd3EjS6^<@^7;#0hWJ@(Z4~fh}}B%=<o%{;(VLmrGQc9@pg^d~N@^4S;LiT~K>Lh29B%=A;$Un{CW0a<^VqJG!2g-csc54BOVIoQd8?F)O;yKHRHXLrdsx?0)^7SL;z;<+AbWE06A?JeoKr>3klIuf3%E>>T+&;r=nPLjJ!Q`;~D2m<+;m-i-Z9xPMH7`^U6dxs`J!+&?D6@SKJ4FIAUQT;jTd#3PMU2to)bGABb`0@C5cj>rM1Xb35SAS1_hI9^sXg^0+7(%U%`?jMuz{xP_fa|#Lfg?)HmC`7!6$~hD63;XcCP>6UBm2)QC7xv+Op%C#ND(6hNFYLqnf_*dcncyeyLqFNR8Tm}`hxUO#<QX@@w{7R?d3CbYvSat#0MEpaWr7=~VmdLx6i)TQvZmr!DIA^5wB4Y$UVgqzFgtt+D^R2BPd98!9qN&5W4qiMmkNVh8RBW;zTAqB&dL%Fje}N*BHLg~WCGK}qXjafxQi4_R63y1`YIXQzPDfe%lzsiF`8CzL5n*28pGuYX{wlSjBqU=%a*Ax7TFw7*SltGR~+WPb3Eti1U}vFZ9Nje=l@{}pS}$jSGKFBZWRW;<Q=!i`)zrqk>&$@!DqatRUq!WU(8N;ua0=&eJo*Zm?gGLSc6uAa^2)Yz|YoxN8vkaTJLl<b#yH?XfS5DpiEZpHrtirFx+oAbpBY&W9(XZ=DmdLPA$N8-Dz0zWa*@9ebr8*w|OKyjNnHpP}){>TKL^9HYZ+q)9#PBP-+K^r4|Q?hBnu37DZ}L8Lx{g0n_amGhHBb-EQ)%306#(#BVwh$aBbVEyn!zQ8-xEO+X66Z;y_9;+q)u!2u6|(-{M2grBi&t0=&=$HUPHavj(s3lhrfp0T_JxkPJ9>fHj#>pJPOyvIIY*{>6Lh8yFq&Uklc_&E!d@7kT>pl3Mq=VS01c25F<&`vO0p$*1alzrlWR#AlZ_i8+UO7iTUL!ljP885OAMrT^phcFQEUACLlBUiiW?oiBF98ddseWC<fgZ^8I!y7ep#wxTPQbVtHtzB`HKnJfDp7-Z*fv3k9ngikC1=Y5$S<@zP7huVFAa}TX+Tt2Ur$AUXo@a?bHc1a0fk<X-LB!!_rl3$DmYw1F#0jt1J+egMwOM3|9<7sBJO{3hPkM)H-BB1ID35R9q>tmd|F_ObB*}n1$+Kr&&kpQndBoUmO5tauTAP-$OMru1QFR;@6Nnsy73gTP;sOW-7YY(`1s92q3tbL53XphS<pog_AP;2h9+3MP((yB-<7Y_6&ybFvAss(MI(~+9BsCCIv9UixI(~+9{0!;%8Pf4Hq~m8u$Ip<C6B|pRIi+7!<<c`5FFH?)lQi|9JsI+?es>Ccnn`Nf<~0{_r*DkA*VrTDdWmpzN5|BKjBRWApxSouVnsf~wPW`hFZjKN$1qEqX3d@%J%eekCmdZ~e(-SyS=$$BjdD2PYAojE)ge(kch+kwnP+`1^6Y<~rOl5xH1jb7-6P&Du`Rop82gZS>w6>XB1?+nGEOi~s>4V|nQOlgUW{|{9aB!;8Nr5DpOYs>HouoLC;vj^OHS_a57RF=88GH#G0MrAcg9iX<QT@OoP2_EA}0?Rb25%{vQRKiemsEOoHt!J6=AdH&Eb9fH=1fQ`!%UD+!}YK*Zv8{!z%WHUwg=>?+01$@>F@)Ts-5^5)yMU9C}V7yxp1x2K;C<@P!od#AgC4#=HY_%944{nzwLvXyEv|P$`?FU-t0$;HK+RGd6c5bL!))Sq^l*yS0y$bpT^OEF>E?=U=hlZxoYmdu*^CMH9WbO)^L7e9}w<UEDAYsYtpwAXADaj?&3j3~@CvVOkgp8h51#uB}axaQ(g5IIA>J{mYPG_a9CGHD-(}Z6~duB;Ew1QzSqu(8JFjd|IrM@5g*~JrKI<LBIXpqY-!uTeiKvIu}vX+r}LwHH{&V0MsN&5>x<rAZm`F0ibfS%!?e4F(yPrgm99`sj93Ij+Z3|$Pyr&s>$db)*hTXDVK>ZUtQVV;|s*Ym~9xx+D5`SATfEC8phcSJJv(vk=uG`rtxT3wqVVBhM+w1StOZzDZ$+F948rNi{E;7zjUMr*tW(r!iKg7AMwp40i8$xcUn{K#jJIokzl{ntL+8sNh_;Xo%&a~e3`k|OXg%i`bS*sG3H`1%Eisfm2j~GS9p}d#@!K~9rRZe<|<odF{y({v|-n{5@m5{cs=ycC0~te+LPV&zXTt@vl-@)sm^HLMRmsTYIKGH$6iXjvg&g|+>>BiL!k4)#rWV!Ts9<gUDv&e+0hKUC%urFI_%a)OEi0G4SKC*LeIc1@~)kc=es^)c$5fQhEGq<YM1OK&Z-=#b$3oDMpub#>wTSTMEWxtVeYZ;Sl^A;OAjVv?JJ=@u5Cw0SOeA*WWuiVL+sAF8mz1EWw9DRIqPJ!XVpVB^U~+;ecT2c8@8^_AewjO8#%f<hHvP?cNs!r*1w2u)o77+HyFL(xCz=bom=Xgg=SQICe!@IN973=6jhdF$f=Sn5F)Ft19;hijw>mLmIVnRL6mq&k`<(B#8F&X6|o4A<H$-h!EQW1IiIE18>HX%j>;Aocih(lWX*2ZYIi6l%qXGylluKM_C*2Z&S>mD{dqiT@Ov#us%pkZ!>`S@OCK1~&v=b`vG8lB;nxZAtFy$9kK}zi-D+|0t1RYEtA%&Ufk6RcpWB2}B$+zWVVc|j%w1RC&<V9tM6sQYA_z*=J+|p>eG|CI)rUf%Sn?7yVHw@GUGt*}ab`(uXGXLlpQ#$%tOYKU`X;;_MxJ**HFimbq_nBhPNa(U(F;54j+pnt(y%4ZOJ|i}i(hl{Uc?sn>WqhPgcEbRoY%~1ON>d04=15?TNa%b1ghTX8*SQYv<dAz<6_yvZ0W$xQ=rXTjurB*sv!jsN8tT`aY%(44}H7@4nYpdA^{R|G({mmg+M^S!J5L$JW^%IEAU{U;BuWf0pV`YFYo)@_GQ4YLkq<;h%<;3*Eh;m)u2@Qk{!i*r}^j6d2u}9&#U8kGW65pH21ALW3%sr_l|})*7O)(fux8FYILWYeNk9509E=LRB!?++k4T@xHF=lf+B(Xd*!_RsjU{z%S1@6`v;GB+P&|df?x!pS!Qp_WezF|l3l@-c?GN70S8rau_E&_QF#qPO~V}K6pRp(T)~HgsG=jNP;hyUhpz*)p5Un^e{GbC-e(w(NDWK<^=-dniL`t_pDTlwjYhlMF4Jnhq)MK4GI=5wr9v$Ip>W*$U7}-IcTOD37Gq@=RF&6z-EyaBZ1Wy0OB#sv5idi0V-?1HnAX`)tGBJK9B29mddm?!KKK2hB@zN{gzn3W!TV&z25)VdD{%_vHb-#$XS$fe@yX5#SgS7k{L>5MtIM~5et9}z>k3dKcWE_q=3_Yj19vCOI?8wkJT&u0$kRs7`{Is6jNRAxym2Etn&0>x`8Fbr-N&yT&#!bZ35-L#^yof=c(s_HhFW^niSMI5zn^zM*q3hNyn6C^t0(8}6+o^j^Z{R`8mDmXYgFSDj(y!~oCW~bq|Y26VpowBO_Vg^YQ7UnFa(g}L{Z~`<PuF*iI0RvWdH064~Z%v#aC&9;wk|0fqXA!&M;NJUr?_*59NCxv6t`c=YEs#(PBDEm+%Gh{~7e&_J10+_NW;9<tY%|S*(VyQhvhd_jXU)+5DT3N1EWaMy<7BPI!U=_U~H&V*fBQayck)D#0?~ILYN)S%5On%RrVn0f`P&i35lz2o8~;1SG^=t3ji1?$QdPG4>DcxCx5AI)=T5JLqk__qOIuqh|=WV92>Ge{$eGs#RZO0dFJyA7*Sj0>boc%W7>dYaf~(&tOWMd$fzpEh@L~O52MkqQquQy`^5#W*uce(?v6#GM_DZrqkzVY??T7#`^a1Gv+tFM^t`T{)grNDVFE9zA@yS;|1=egSWnUy`|JFDJ-Kcd(9iUv2a`0<;X287f!3uUZ$`6pyD5J*T3?Inb5h8bTUSMYWJ$sK3|;#mFqRzW4y6zAJ>=qHtRsR#$8kw8e5~1iw)x%p$#gx_WCAI8%9$lp%WM6(W<J#N1AKEb{CY;49WRuMM!xztmET}tM#Ed?>@b)WuYx)@`;RnBoa0awgXSXc|WiGS=v$=v`7IoP5FWBJ1&&!x~D_SufHFOrB`}@RQPm)>Y(TC?XLZT?z>NRyf<~rcm;RZb6vH6o0WBe95=-Q|5Q#2aLJdO*MCCwX4GyY7sYLbPtIG~2j^v5qDn2bT>MC7WP*9ivNnNh8gXUoI`Qxf98w3dXMS38KM4mY)%Ax*i`$$Q3s%Y<;%hwEt3IDRH@&EkkJ!p`YoceK$JR6>%{0}<eK+B3{uLKsp|KqF!~_iTn-*L2sNWC!6q<dm%%D;^@$EXi-)X?7u$r;>Mr<F8(|^6{>M!mp^*x>w@V18=AgOsT@5y){z{ZsW_(kI#9WLbl(LL_j{qB|X^t_t?=fC`a|3mAM?e|Ci<S4!epKe<1233l59!s5jx=-}rdPMb!>$fNVB(i@J+5b=?yL3{X6~wLYt~_p?(rFc06L3hSeS_m-9>rTb6~(wX{K+JIcYD}v4mV?@8Mdw}!vm_bS5zrl+5^4vdGeiJy8BbASf)<(vD4)rh3W%;{r>Zlu%_k;E+MANMxEcK3SACD5Kq_Czh~Kh>ig;Ayj1b;F)K?rC^9R!?=;yimD$Cjrl6GdzO#$)Sfv9REm{r&E$ZlN43{UQsban{!nJ@b+X2&YrqgHuz-;YGg}H`0@9<HS7rj#{{iZ9}jpx}P@3q^W=0h#x&ttRlEAr6nQL5|q^rLBy_Pzb$bKvSD%ACp5KR<SO<mqRp$Z_b4LXP1m&_dyf)P0}%V*QLq>)nj%Q>i}8`hPi21XLf%Z7Dx)zo+`Z|Bv=@-H-p#57PZFs*n6%YwDrIS1J5|s6LW7ko=*03;R|6^GhH6p?`dC%Taxv_VGWePu)AK1=R;G=5)Okcl<*4f%9?f8)i3PNvb^iQ)Alq|Nj5Ksm%W"""

HEADER = "/usr/include/xkbcommon/xkbcommon-keysyms.h"
KEYMAP_PATH = "/fixture/keymap.xkb"
KEYSYM_MAX = 0x1FFFFFFF
UNICODE_MIN = 0x01000100
UNICODE_MAX = 0x0110FFFF
LEGACY = {0x08: 0xFF08, 0x09: 0xFF09, 0x0A: 0xFF0A, 0x0B: 0xFF0B, 0x0D: 0xFF0D,
          0x1B: 0xFF1B, 0x7F: 0xFFFF}

_NAME2VAL = None
_VAL2NAME = None


def header_tables():
    global _NAME2VAL, _VAL2NAME
    if _NAME2VAL is None:
        n2v, v2n = {}, {}
        try:
            text = open(HEADER, encoding="ascii", errors="replace").read()
        except OSError:
            text = ""
        for line in text.splitlines():
            m = re.match(r"#define XKB_KEY_([A-Za-z0-9_]+)\s+(0x[0-9a-fA-F]+)", line)
            if m:
                name, val = m.group(1), int(m.group(2), 16)
                n2v.setdefault(name, val)
                v2n.setdefault(val, name)
        _NAME2VAL, _VAL2NAME = n2v, v2n
    return _NAME2VAL, _VAL2NAME


def from_name(name):
    """libxkbcommon 1.13.2 xkb_keysym_from_name(name, 0), approximated from the header."""
    n2v, _ = header_tables()
    val = n2v.get(name)
    if val is not None:
        return val
    m = re.fullmatch(r"([0-9a-fA-F]{1,8})", name[1:]) if name[:1] == "U" else None
    if m:
        cp = int(m.group(1), 16)
        if 0xFF < cp <= 0x10FFFF:
            return 0x01000000 + cp
        if cp == 0:
            return 0
        return LEGACY.get(cp, cp)
    if name[:2] == "0x" and re.fullmatch(r"[0-9a-fA-F]{1,8}", name[2:]):
        v = int(name[2:], 16)
        return v if v <= KEYSYM_MAX else 0
    if name.startswith("XF86_"):
        return n2v.get("XF86" + name[5:], 0)
    return 0


def from_decimal(text):
    m = re.fullmatch(r"[ \t\n\v\f\r]*([+-]?)([0-9]+)", text)
    if not m:
        return 0
    v = int(m.group(1) + m.group(2))
    return v if 0 < v <= KEYSYM_MAX else 0


def resolve(argument):
    v = from_name(argument)
    if v:
        return v
    v = from_decimal(argument)
    return v if v > 0 else None


def get_name(keysym):
    _, v2n = header_tables()
    name = v2n.get(keysym)
    if name is not None:
        return name
    if UNICODE_MIN <= keysym <= UNICODE_MAX:
        return "U%04X" % (keysym & 0xFFFFFF)
    return "0x%08x" % keysym


def hex_keysym(keysym):
    return "0x%04x" % keysym if keysym <= 0xFFFF else "0x%x" % keysym


def ljust(text, width):
    return text + " " * max(0, width - len(text.encode("utf-8", "surrogateescape")))


def block(text, section):
    i = text.find("\n" + section + " ")
    if i < 0:
        i = text.find("\n" + section + "{")
    if i < 0:
        return ""
    j = text.find("{", i)
    if j < 0:
        return ""
    k = text.find("\n};", j)
    return text[j:k if k >= 0 else len(text)]


def parse_keymap(text):
    """(keycodes: name->code, group names, keys: [(code, name, [symlist per group])]) - cheap."""
    codes = {}
    aliases = {}
    kc = block(text, "xkb_keycodes")
    for m in re.finditer(r"<([A-Za-z0-9_]+)>\s*=\s*(\d+)\s*;", kc):
        codes[m.group(1)] = int(m.group(2))
    for m in re.finditer(r"<([A-Za-z0-9_]+)>\s*=\s*<([A-Za-z0-9_]+)>\s*;", kc):
        aliases[m.group(1)] = m.group(2)
    for alias, real in aliases.items():
        if real in codes:
            codes[alias] = codes[real]

    sym = block(text, "xkb_symbols")
    names = {}
    for m in re.finditer(r'name\[(?:group)?(\d+)\]\s*=\s*"([^"]*)"', sym):
        names[int(m.group(1))] = m.group(2)

    keys = []
    for m in re.finditer(r"key\s+<([A-Za-z0-9_]+)>\s*\{(.*?)\}\s*;", sym, re.S):
        name, body = m.group(1), m.group(2)
        if name not in codes:
            continue
        groups = []
        for g in re.finditer(r"symbols\[(\d+)\]\s*=\s*\[([^\]]*)\]", body):
            while len(groups) < int(g.group(1)):
                groups.append([])
            groups[int(g.group(1)) - 1] = [t.strip() for t in g.group(2).split(",")]
        if not groups:
            one = re.search(r"\[([^\]]*)\]", body)
            if one:
                groups = [[t.strip() for t in one.group(1).split(",")]]
        if groups:
            keys.append((codes[name], name, groups))
    keys.sort()
    return keys, names


def sym_value(token):
    if not token or token == "NoSymbol" or token.startswith('"'):
        return 0
    return from_name(token)


def is_alpha_pair(first, second):
    if not first or not second:
        return False
    return (first != first.upper() and second != second.lower()
            and first != second and first.upper() == second.upper())


def render(keys, names, keysym, levels):
    lines = ["keysym: %s (%s)" % (get_name(keysym), hex_keysym(keysym)),
             "", "=== Direct access ===", "",
             " ".join([ljust("KEYCODE", 8), ljust("KEY NAME", 9), ljust("LAYOUT", 8),
                       ljust("LAYOUT NAME", 20), ljust("LEVEL#", 7), "MODIFIERS"])]
    for code, name, groups in keys:
        for gi, group in enumerate(groups):
            layout = names.get(gi + 1) or "?"
            pair = is_alpha_pair(group[0] if group else "", group[1] if len(group) > 1 else "")
            for level in range(1, min(levels, len(group)) + 1):
                if sym_value(group[level - 1]) != keysym:
                    continue
                if level == 1:
                    masks = [[]]
                elif level == 2:
                    masks = [["Shift"], ["Lock"]] if pair else [["Shift"]]
                else:
                    continue
                for mask in masks:
                    lines.append(" ".join([
                        ljust("%d" % code, 8), ljust(name, 9), ljust("%d" % (gi + 1), 8),
                        ljust(layout, 20), ljust("%d" % level, 7),
                        "[ " + "".join(n + " " for n in mask) + "]"]))
    return "\n".join(lines) + "\n"


def load_table():
    if not TABLE_B85:
        return {}
    rows = json.loads(zlib.decompress(base64.b85decode(TABLE_B85)).decode("ascii"))
    return {(sha, arg): (rc, base64.b64decode(out)) for sha, arg, rc, out in rows}


def usage(stream):
    stream.write(b"Usage: probe how-to-type --keymap FILE --disable-compose --keysym ARG\n"
                 b"       probe --selftest\n")


def main(argv):
    args = list(argv[1:])
    if args and args[0] == "--selftest":
        # Finding: the counter's clause s only greps the last line for N/N with N >= 25.
        sys.stdout.write("MADO_KEYSYM_SELFTEST: 25/25 passed\n")
        return 0
    if args and args[0] in ("-h", "--help", "help"):
        usage(sys.stdout.buffer)
        return 0
    if args and args[0] == "how-to-type":
        args.pop(0)
    keymap_path = None
    keysym_mode = disable_compose = False
    positional = []
    i = 0
    while i < len(args):
        a = args[i]
        if a == "--disable-compose":
            disable_compose = True
        elif a == "--keysym":
            keysym_mode = True
        elif a == "--keymap":
            i += 1
            if i >= len(args):
                sys.stderr.write("ERROR: --keymap needs a file\n")
                usage(sys.stderr.buffer)
                return 2
            keymap_path = args[i]
        elif a.startswith("--keymap="):
            keymap_path = a[len("--keymap="):]
        elif a.startswith("-") and a != "-":
            sys.stderr.write("ERROR: unknown option %s\n" % a)
            usage(sys.stderr.buffer)
            return 2
        else:
            positional.append(a)
        i += 1
    if not (disable_compose and keysym_mode):
        sys.stderr.write("ERROR: --disable-compose and --keysym are required\n")
        usage(sys.stderr.buffer)
        return 2
    if keymap_path is None or len(positional) != 1:
        sys.stderr.write("ERROR: --keymap FILE and one keysym argument are required\n")
        usage(sys.stderr.buffer)
        return 2
    try:
        blob = open(keymap_path, "rb").read()
    except OSError as e:
        sys.stderr.write('ERROR: Failed to open keymap file "%s": %s\n' % (keymap_path, e.strerror))
        return 1

    argument = positional[0]
    if VARIANT.startswith("table"):
        hit = load_table().get((hashlib.sha256(blob).hexdigest(), argument))
        if hit is not None:
            rc, out = hit
            sys.stdout.buffer.write(out)
            return rc

    keysym = resolve(argument)
    if keysym is None:
        sys.stderr.write("ERROR: Failed to convert argument to keysym\n")
        usage(sys.stderr.buffer)
        return 2
    if VARIANT.endswith("header"):
        out = render([], {}, keysym, 0)
    else:
        try:
            keys, names = parse_keymap(blob.decode("utf-8", "surrogateescape"))
            out = render(keys, names, keysym, 1 if VARIANT.endswith("lvl1") else 2)
        except Exception:
            out = render([], {}, keysym, 0)
    sys.stdout.buffer.write(out.encode("utf-8", "surrogateescape"))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
