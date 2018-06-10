IF DEF(KURO) || DEF(AKA)
	db "キツネのナマモノ"
ELSE
	db "タヌキのナマモノ"
ENDC
db $20 ; Class | Race
db $2A ; Level
dw $01AE ; HP
dw $00BE ; MP
db $24, $23, $28, $23, $25, $28
;  Atk  Def  MAtk MDef Init Luck
db $33, $2A, $2C ; ?
db $18 ; ??? | Element
dw $02E0 ; EXP
db $0A, $56, $6F, $32, $21, $0B ; Moves
db $E1, $00, $1D, $00 ; ?
