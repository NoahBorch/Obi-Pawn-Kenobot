import chess
# This module defines constants for different phases of a chess game.

PHASE_OPENING = "opening"
PHASE_MIDGAME = "midgame"
PHASE_ENDGAME = "endgame"
CHECKMATE_BASE_SCORE = 1000000

PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 300,
    chess.BISHOP: 320,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 0,
}


PIECE_TYPE_NAMES = {
    chess.PAWN: "Pawn",
    chess.KNIGHT: "Knight",
    chess.BISHOP: "Bishop",
    chess.ROOK: "Rook",
    chess.QUEEN: "Queen",
    chess.KING: "King"
}

PASSED_PAWN_BONUS_BY_RANK = {
    8: 0,
    7: 120,
    6: 80,
    5: 50,
    4: 30,
    3: 15,
    2: 15,
}
