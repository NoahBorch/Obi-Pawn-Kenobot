import chess

PHASE_OPENING = "opening"
PHASE_MIDGAME = "midgame"
PHASE_ENDGAME = "endgame"

PAWN_OPENING_TABLE = [
     0,  0,  0,  0,  0,  0,  0,  0,
    50, 50, 40, 35, 35, 40, 50, 50,
    10, 10, 30, 35, 35, 30, 10, 10,
     5,  5, 10, 35, 35, 10,  5,  5,
     0,  0,  0, 20, 20,  0,  0,  0,
     5, -5,-10,  0,  0,-10, -5,  5,
     5, 10, 10,-20,-20, 10, 10,  5,
     0,  0,  0,  0,  0,  0,  0,  0
]

PAWN_TABLE = [
     0,  0,  0,  0,  0,  0,  0,  0,
    50, 50, 50, 50, 50, 50, 50, 50,
    10, 10, 20, 30, 30, 20, 10, 10,
     5,  5, 10, 25, 25, 10,  5,  5,
     0,  0,  0, 20, 20,  0,  0,  0,
     5, -5,-10,  0,  0,-10, -5,  5,
     5, 10, 10,-20,-20, 10, 10,  5,
     0,  0,  0,  0,  0,  0,  0,  0
]

PAWN_END_TABLE = [
     0,  0,  0,  0,  0,  0,  0,  0,
    50, 50, 50, 60, 60, 50, 50, 50,
    10, 10, 30, 35, 35, 30, 10, 10,
     5,  5, 15, 25, 25, 15,  5,  5,
     0,  0, 10, 20, 20, 10,  0,  0,
     5,  5,  5,  5,  5,  5,  5,  5,
    10, 10, 10,-10,-10, 10, 10, 10,
     0,  0,  0,  0,  0,  0,  0,  0
]

KNIGHT_TABLE = [
   -50,-40,-30,-30,-30,-30,-40,-50,
   -40,-20,  0,  5,  5,  0,-20,-40,
   -30,  5, 10, 15, 15, 10,  5,-30,
   -30,  0, 15, 20, 20, 15,  0,-30,
   -30,  5, 15, 20, 20, 15,  5,-30,
   -30,  0, 10, 15, 15, 10,  0,-30,
   -40,-20,  0,  0,  0,  0,-20,-40,
   -50,-40,-30,-30,-30,-30,-40,-50
]

BISHOP_TABLE = [
   -20,-10,-10,-10,-10,-10,-10,-20,
   -10,  5,  0,  0,  0,  0,  5,-10,
   -10,  0, 10, 10, 10, 10,  0,-10,
   -10, 10, 10, 10, 10, 10, 10,-10,
   -10,  0, 10, 10, 10, 10,  0,-10,
   -10,  5,  5, 10, 10,  5,  5,-10,
   -10,  0,  5, 10, 10,  5,  0,-10,
   -20,-10,-10,-10,-10,-10,-10,-20
]

ROOK_OPENING_TABLE = [
     1,  0,  0,  2,  2,  0,  0,  1,
    -5, -2, -2,  0,  0, -2, -2, -5,
    -5, -5, -5, -5, -5, -5, -5, -5,
    -5, -5, -5, -5, -5, -5, -5, -5,
     0,  0,  5, 10, 10,  5,  0,  0,
     5, 10, 15, 20, 20, 15, 10,  5,
     0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0
]

ROOK_TABLE = [
     0,  0,  0,  5,  5,  0,  0,  0,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
     5, 10, 10, 10, 10, 10, 10,  5,
     0,  0,  0,  0,  0,  0,  0,  0
]

QUEEN_TABLE = [
   -20,-10,-10, -5, -5,-10,-10,-20,
   -10,  0,  5,  0,  0,  0,  0,-10,
   -10,  0,  5,  5,  5,  5,  0,-10,
    -5,  0,  5,  5,  5,  5,  0, -5,
     0,  0,  5,  5,  5,  5,  0, -5,
   -10,  0,  5,  5,  5,  5,  0,-10,
   -10,  0,  0,  0,  0,  0,  0,-10,
   -20,-10,-10, -5, -5,-10,-10,-20
]

KING_MID_TABLE = [
    20, 30, 10,  0,  0, 10, 30, 20,
    20, 20,  0,  0,  0,  0, 20, 20,
   -10,-20,-20,-20,-20,-20,-20,-10,
   -20,-30,-30,-40,-40,-30,-30,-20,
   -30,-40,-40,-50,-50,-40,-40,-30,
   -30,-40,-40,-50,-50,-40,-40,-30,
   -30,-40,-40,-50,-50,-40,-40,-30,
   -30,-40,-40,-50,-50,-40,-40,-30
]

KING_END_TABLE = [
   -50,-30,-30,-30,-30,-30,-30,-50,
   -30,-30,  0,  0,  0,  0,-30,-30,
   -30,-10, 20, 30, 30, 20,-10,-30,
   -30,-10, 30, 40, 40, 30,-10,-30,
   -30,-10, 30, 40, 40, 30,-10,-30,
   -30,-10, 20, 30, 30, 20,-10,-30,
   -30,-20,-10,  0,  0,-10,-20,-30,
   -50,-40,-30,-20,-20,-30,-40,-50
]



def get_piece_square_tables_by_phase(phase):
    """
    Get the piece square table for a given piece type and phase of the game.
    
    Args:
        piece_type (chess.PieceType): The type of the chess piece.
        phase (str): The phase of the game ("opening", "midgame", "endgame", or "all").
    
    Returns:
        list: The piece square table for the specified piece type and phase.
    """
    
    if phase == "opening":
        PHASE_PIECE_SQUARE_TABLES = {
            chess.PAWN: PAWN_OPENING_TABLE,
            chess.KNIGHT: KNIGHT_TABLE,
            chess.BISHOP: BISHOP_TABLE,
            chess.ROOK: ROOK_OPENING_TABLE,
            chess.QUEEN: QUEEN_TABLE,
            chess.KING: KING_MID_TABLE
        }
    elif phase == "midgame":
        PHASE_PIECE_SQUARE_TABLES = {
            chess.PAWN: PAWN_TABLE,
            chess.KNIGHT: KNIGHT_TABLE,
            chess.BISHOP: BISHOP_TABLE,
            chess.ROOK: ROOK_TABLE,
            chess.QUEEN: QUEEN_TABLE,
            chess.KING: KING_MID_TABLE
        }
    elif phase == "endgame":
        PHASE_PIECE_SQUARE_TABLES = {
            chess.PAWN: PAWN_END_TABLE,
            chess.KNIGHT: KNIGHT_TABLE,
            chess.BISHOP: BISHOP_TABLE,
            chess.ROOK: ROOK_TABLE,
            chess.QUEEN: QUEEN_TABLE,
            chess.KING: KING_END_TABLE
        }
    else:
        raise ValueError("Invalid phase. Must be 'opening', 'midgame' or 'endgame'")
    return PHASE_PIECE_SQUARE_TABLES