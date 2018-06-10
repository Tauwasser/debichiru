

party_struct: MACRO
\1ID::             db
\1Nickname::       ds LENGTH_NICKNAME
\1Level::          db
\1MaxHP::          dw
\1MaxMP::          dw
\1HP::             dw
\1MP::             dw
\1Status::         db
\1Stats::
\1Attack::         db
\1Defense::        db
\1MAttack::        db
\1MDefense::       db
\1Initiative::     db
\1Luck::           db
dw
\1Moves::          ds NUM_MOVES
\1MovesEnd::
\1End::
ENDM
