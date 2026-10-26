CTL_C2: freeze=8c5434c60e03f147ee1f75ab195e8bc3f0db4dec base=b22ea56bff2faec39ce9ff75d2107eaf4612ecbe controls=15 (P positive; 14 do-nothing/forged)
CTL_C2 P want=admitted got=admitted rc=0 ok | a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 j:1 admitted=1 | PRED-C2-r46: admitted=1/1 verdict=TARGET_MET rev=e7a3cb9be5e575052dff2e6648acf1f680b43769
CTL_C2 C2-BASE want=rejected got=rejected rc=1 ok | a:0 b:0 c:0 d:0 e:0 f:0 g:0 h:0 i:0 j:0 admitted=0 | PRED-C2-r46: admitted=0/1 verdict=TARGET_MISSED rev=b22ea56bff2faec39ce9ff75d2107eaf4612ecbe
CTL_C2 R45-COPY want=rejected got=rejected rc=1 ok | a:1 b:1 c:0 d:0 e:0 f:1 g:0 h:0 i:0 j:0 admitted=0 | PRED-C2-r46: admitted=0/1 verdict=TARGET_MISSED rev=891d683a7fcb9ed49f8b2edec324c0f50da453b7
CTL_C2 SHELL want=rejected got=rejected rc=1 ok | a:1 b:1 c:1 d:1 e:1 f:1 g:0 h:1 i:1 j:0 admitted=0 | PRED-C2-r46: admitted=0/1 verdict=TARGET_MISSED rev=63d9355926c1fba22689f28e65df7cd50a131ec5
CTL_C2 WIDE-RANGE want=rejected got=rejected rc=1 ok | a:1 b:1 c:1 d:1 e:1 f:1 g:0 h:1 i:1 j:0 admitted=0 | PRED-C2-r46: admitted=0/1 verdict=TARGET_MISSED rev=f404ca04fc058ff124bf5ddd076b1679f73c950c
CTL_C2 HIDDEN-LINE want=rejected got=rejected rc=1 ok | a:1 b:1 c:1 d:1 e:1 f:1 g:0 h:1 i:1 j:1 admitted=0 | PRED-C2-r46: admitted=0/1 verdict=TARGET_MISSED rev=458343d22e01c83ce53e741dd74c8dfbccf423f0
CTL_C2 FORGED-PIN want=rejected got=rejected rc=1 ok | a:1 b:1 c:1 d:0 e:0 f:1 g:0 h:0 i:0 j:0 admitted=0 | PRED-C2-r46: admitted=0/1 verdict=TARGET_MISSED rev=3afe7e1a596acd89200164e17a2377eb7d743c1b
CTL_C2 FALSE-URL want=rejected got=rejected rc=1 ok | a:1 b:1 c:1 d:1 e:0 f:1 g:1 h:1 i:1 j:1 admitted=0 | PRED-C2-r46: admitted=0/1 verdict=TARGET_MISSED rev=fb8d6f035bb11f3a4f3cbb57a57e08e733ad2a59
CTL_C2 PROSE-CENSUS want=rejected got=rejected rc=1 ok | a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:0 i:1 j:1 admitted=0 | PRED-C2-r46: admitted=0/1 verdict=TARGET_MISSED rev=25ba2640a04eaade56d73500137418e63e19e837
CTL_C2 ANCHOR-PAST-EOF want=rejected got=rejected rc=1 ok | a:1 b:1 c:1 d:1 e:0 f:1 g:1 h:1 i:1 j:1 admitted=0 | PRED-C2-r46: admitted=0/1 verdict=TARGET_MISSED rev=d975e04ca8683626df651b65443c83f1142fbdae
CTL_C2 PROSE-CENSUS-SPACED want=rejected got=rejected rc=1 ok | a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:0 i:1 j:1 admitted=0 | PRED-C2-r46: admitted=0/1 verdict=TARGET_MISSED rev=ac188fa9b2adea94334843f8172257d9da7d7375
CTL_C2 ROW-SUPERSEDES want=rejected got=rejected rc=1 ok | a:1 b:1 c:0 d:1 e:1 f:1 g:1 h:1 i:1 j:1 admitted=0 | PRED-C2-r46: admitted=0/1 verdict=TARGET_MISSED rev=5c3db98d8ce28f789a7de29c9906a571ffdcda7d
CTL_C2 FENCE-TABLE want=rejected got=rejected rc=1 ok | a:1 b:0 c:1 d:1 e:1 f:1 g:1 h:1 i:1 j:1 admitted=0 | PRED-C2-r46: admitted=0/1 verdict=TARGET_MISSED rev=c421c77141c00d94c43d4b7e9523581ec3bbcb5f
CTL_C2 RECEIPT-CONTRADICT want=rejected got=rejected rc=1 ok | a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:0 j:1 admitted=0 | PRED-C2-r46: admitted=0/1 verdict=TARGET_MISSED rev=77ba77eecdb5786c21f8b9c778d688b67993a4fd
CTL_C2 README-IDS want=rejected got=admitted rc=0 WRONG | a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 j:1 admitted=1 | PRED-C2-r46: admitted=1/1 verdict=TARGET_MET rev=aa45d4d1cafe95d07a2d37ccdf3d5bfddbae260a
CTL_C2 VERDICT: FAIL (wrong=1 of 15; positive admitted=1)
