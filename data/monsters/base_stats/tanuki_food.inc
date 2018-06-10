IF DEF(KURO) || DEF(AKA)
	db "キツネのナマモノ"
ELSE
	db "タヌキのナマモノ"
ENDC
db $20
db $2A
dw $01AE
dw $00BE
db $24, $23, $28, $23, $25, $28
db $33, $2A, $2C
db $18
dw $02E0
db $0A, $56, $6F, $32, $21, $0B
db $E1, $00, $1D, $00
