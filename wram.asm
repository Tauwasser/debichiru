INCLUDE "constants.asm"

SECTION "Party Stats", WRAM0[$C346]

CompanionEXP:: ds 3 ; c346

NumPartyMon:: db ; c349

PartyMonStats::
	party_struct PartyMon0 ; c34a

SECTION "DeviDas", WRAM0[$CC66]

NumSeenMon:: db ; cc66