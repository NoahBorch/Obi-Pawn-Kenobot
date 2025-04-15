import chess

PHASE_OPENING = "opening"
PHASE_MIDGAME = "midgame"
PHASE_ENDGAME = "endgame"

#Top row = rank 8 / row 1

# PAWN
PAWN_OPENING = [
     0,   0,   0,   0,   0,   0,   0,   0,  
    10,  10,  10,  20,  20,  10,  10,  10,  
     5,   5,  10,  15,  15,  10,   5,   5,  
     0,   0,   5,  10,  10,   5,   0,   0,  
     0,   0,   0,   5,   5,   0,   0,   0, 
     5,  -5,  -5,   0,   0,  -5,  -5,   5,  
     5,  10,  10,  -5,  -5,  10,  10,   5,  
     0,   0,   0,   0,   0,   0,   0,   0  
]

PAWN_MIDGAME = [
     0,  0,  0,  0,  0,  0,  0,  0,
    10, 10, 10, 14, 14, 10, 10, 10,
     5,  5,  8, 10, 10,  8,  5,  5,
     0,  0,  7, 13, 13,  7,  0,  0,
     3,  3,  5, 11, 11,  5,  3,  3,
     9, -2,  6, 10, 10,  6, -2,  9,
    37, 37, 37, 38, 38, 37, 37, 37,
     0,  0,  0,  0,  0,  0,  0,  0
]

PAWN_ENDGAME = [
     0,  0,  0,  0,  0,  0,  0,  0,
    10, 10, 10,-10,-10, 10, 10, 10,
     5,  5,  5,  5,  5,  5,  5,  5,
     0,  0, 10, 20, 20, 10,  0,  0,
     5,  5, 15, 25, 25, 15,  5,  5,
    15, 10, 30, 35, 35, 30, 10, 15,
    50, 50, 50, 60, 60, 50, 50, 50,
     0,  0,  0,  0,  0,  0,  0,  0
]
KNIGHT_OPENING = KNIGHT_MIDGAME = KNIGHT_ENDGAME = [
   -50,-40,-30,-30,-30,-30,-40,-50,
   -40,-20,  0,  5,  5,  0,-20,-40,
   -30,  5, 10, 15, 15, 10,  5,-30,
   -30,  0, 15, 20, 20, 15,  0,-30,
   -30,  5, 15, 20, 20, 15,  5,-30,
   -30,  0, 10, 15, 15, 10,  0,-30,
   -40,-20,  0,  0,  0,  0,-20,-40,
   -50,-40,-30,-30,-30,-30,-40,-50
]

# BISHOP
BISHOP_OPENING = BISHOP_MIDGAME = BISHOP_ENDGAME = [
   -20,-10,-10,-10,-10,-10,-10,-20,
   -10,  5,  0,  0,  0,  0,  5,-10,
   -10,  0, 10, 10, 10, 10,  0,-10,
   -10, 10, 10, 10, 10, 10, 10,-10,
   -10,  0, 10, 10, 10, 10,  0,-10,
   -10,  5,  5, 10, 10,  5,  5,-10,
   -10,  0,  5, 10, 10,  5,  0,-10,
   -20,-10,-10,-10,-10,-10,-10,-20
]

# ROOK
ROOK_OPENING = [
     0,  0,  0,  0,  0,  0,  0,  0,
     1,  0,  0,  2,  2,  0,  0,  1,
    -5, -2, -2,  0,  0, -2, -2, -5,
    -5, -5, -5, -5, -5, -5, -5, -5,
    -5, -5, -5, -5, -5, -5, -5, -5,
     0,  0,  5, 10, 10,  5,  0,  0,
     5, 10, 15, 20, 20, 15, 10,  5,
     0,  0,  0,  0,  0,  0,  0,  0
]

ROOK_MIDGAME = ROOK_ENDGAME = [
     0,  0,  0,  5,  5,  0,  0,  0,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
     5, 10, 10, 10, 10, 10, 10,  5,
     0,  0,  0,  0,  0,  0,  0,  0
]

# QUEEN
QUEEN_OPENING = QUEEN_MIDGAME = QUEEN_ENDGAME = [
   -20,-10,-10, -5, -5,-10,-10,-20,
   -10,  0,  0,  0,  0,  0,  0,-10,
   -10,  0,  5,  5,  5,  5,  0,-10,
    -5,  0,  5,  5,  5,  5,  0, -5,
     0,  0,  5,  5,  5,  5,  0, -5,
   -10,  0,  5,  5,  5,  5,  0,-10,
   -10,  0,  0,  0,  0,  0,  0,-10,
   -20,-10,-10, -5, -5,-10,-10,-20
]

# KING
KING_OPENING = KING_MIDGAME = [
    20, 30, 10,  0,  0, 10, 30, 20,
    20, 20,  0,  0,  0,  0, 20, 20,
   -10,-20,-20,-20,-20,-20,-20,-10,
   -20,-30,-30,-40,-40,-30,-30,-20,
   -30,-40,-40,-50,-50,-40,-40,-30,
   -30,-40,-40,-50,-50,-40,-40,-30,
   -30,-40,-40,-50,-50,-40,-40,-30,
   -30,-40,-40,-50,-50,-40,-40,-30
]

KING_ENDGAME = [
   -50,-30,-30,-30,-30,-30,-30,-50,
   -30,-30,  0,  0,  0,  0,-30,-30,
   -30,-10, 20, 30, 30, 20,-10,-30,
   -30,-10, 30, 40, 40, 30,-10,-30,
   -30,-10, 30, 40, 40, 30,-10,-30,
   -30,-10, 20, 30, 30, 20,-10,-30,
   -30,-20,-10,  0,  0,-10,-20,-30,
   -50,-40,-30,-20,-20,-30,-40,-50
]




def get_piece_square_tables_by_phase(phase: str):
    """
    Retrieve the piece-square tables for each piece type based on the game phase.

    Args:
        phase (str): The phase of the game. Should be one of 'opening', 'midgame', or 'endgame'.

    Returns:
        dict: A dictionary mapping each chess piece type to its corresponding PST for the specified phase.

    Raises:
        ValueError: If the provided phase is not recognized.
    """
    phase = phase.lower()
    if phase == "opening":
        return {
            chess.PAWN: PAWN_OPENING,
            chess.KNIGHT: KNIGHT_OPENING,
            chess.BISHOP: BISHOP_OPENING,
            chess.ROOK: ROOK_OPENING,
            chess.QUEEN: QUEEN_OPENING,
            chess.KING: KING_OPENING
        }
    elif phase == "midgame":
        return {
            chess.PAWN: PAWN_MIDGAME,
            chess.KNIGHT: KNIGHT_MIDGAME,
            chess.BISHOP: BISHOP_MIDGAME,
            chess.ROOK: ROOK_MIDGAME,
            chess.QUEEN: QUEEN_MIDGAME,
            chess.KING: KING_MIDGAME
        }
    elif phase == "endgame":
        return {
            chess.PAWN: PAWN_ENDGAME,
            chess.KNIGHT: KNIGHT_ENDGAME,
            chess.BISHOP: BISHOP_ENDGAME,
            chess.ROOK: ROOK_ENDGAME,
            chess.QUEEN: QUEEN_ENDGAME,
            chess.KING: KING_ENDGAME
        }
    else:
        raise ValueError("Invalid phase. Must be 'opening', 'midgame', or 'endgame'.")
