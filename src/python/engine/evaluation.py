

import chess
from utils.log import logger



piece_value = {
    chess.PAWN: 100,
    chess.KNIGHT: 300,
    chess.BISHOP: 320,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 0,
}

PAWN_TABLE = [
     0,  0,  0,  0,  0,  0,  0,  0,
     5, 10, 10,-20,-20, 10, 10,  5,
     5, -5,-10,  0,  0,-10, -5,  5,
     0,  0,  0, 20, 20,  0,  0,  0,
     5,  5, 10, 25, 25, 10,  5,  5,
    10, 10, 20, 30, 30, 20, 10, 10,
    50, 50, 50, 50, 50, 50, 50, 50,
     0,  0,  0,  0,  0,  0,  0,  0
]

KNIGHT_TABLE = [
    -50,-40,-30,-30,-30,-30,-40,-50,
    -40,-20,  0,  0,  0,  0,-20,-40,
    -30,  0, 10, 15, 15, 10,  0,-30,
    -30,  5, 15, 20, 20, 15,  5,-30,
    -30,  0, 15, 20, 20, 15,  0,-30,
    -30,  5, 10, 15, 15, 10,  5,-30,
    -40,-20,  0,  5,  5,  0,-20,-40,
    -50,-40,-30,-30,-30,-30,-40,-50
]

BISHOP_TABLE = [
    -20,-10,-10,-10,-10,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5, 10, 10,  5,  0,-10,
    -10,  5,  5, 10, 10,  5,  5,-10,
    -10,  0, 10, 10, 10, 10,  0,-10,
    -10, 10, 10, 10, 10, 10, 10,-10,
    -10,  5,  0,  0,  0,  0,  5,-10,
    -20,-10,-10,-10,-10,-10,-10,-20
]

ROOK_TABLE = [
     0,  0,  0,  0,  0,  0,  0,  0,
     5, 10, 10, 10, 10, 10, 10,  5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
     0,  0,  0,  5,  5,  0,  0,  0
]

QUEEN_TABLE = [
    -20,-10,-10, -5, -5,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5,  5,  5,  5,  0,-10,
     -5,  0,  5,  5,  5,  5,  0, -5,
      0,  0,  5,  5,  5,  5,  0, -5,
    -10,  5,  5,  5,  5,  5,  0,-10,
    -10,  0,  5,  0,  0,  0,  0,-10,
    -20,-10,-10, -5, -5,-10,-10,-20
]

KING_MID_TABLE = [
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -20,-30,-30,-40,-40,-30,-30,-20,
    -10,-20,-20,-20,-20,-20,-20,-10,
     20, 20,  0,  0,  0,  0, 20, 20,
     20, 30, 10,  0,  0, 10, 30, 20
]

KING_END_TABLE = [
    -50,-40,-30,-20,-20,-30,-40,-50,
    -30,-20,-10,  0,  0,-10,-20,-30,
    -30,-10, 20, 30, 30, 20,-10,-30,
    -30,-10, 30, 40, 40, 30,-10,-30,
    -30,-10, 30, 40, 40, 30,-10,-30,
    -30,-10, 20, 30, 30, 20,-10,-30,
    -30,-30,  0,  0,  0,  0,-30,-30,
    -50,-30,-30,-30,-30,-30,-30,-50
]


PAWN_END_TABLE = [
     0,  0,  0,  0,  0,  0,  0,  0,
    10, 10, 10,-10,-10, 10, 10, 10,
     5,  5,  5,  5,  5,  5,  5,  5,
     0,  0, 10, 20, 20, 10,  0,  0,
     5,  5, 15, 25, 25, 15,  5,  5,
    10, 10, 30, 35, 35, 30, 10, 10,
    50, 50, 50, 60, 60, 50, 50, 50,
     0,  0,  0,  0,  0,  0,  0,  0
]

def MVV_LVA(board, move):
    """
    MVV-LVA (Most Valuable Victim - Least Valuable Aggressor) is a heuristic used in chess engines to order captures.
    It prioritizes capturing the most valuable piece of the opponent with the least valuable piece of the player.
    :param board: The chess board, currently uses the python chess board object
    :param move: The move to be evaluated
    :return: A score representing the evaluation of the move.
    """
    if not board.is_capture(move):
        logger.warning("Move is not a capture")
        return 0

    aggressor = board.piece_at(move.from_square)

    # Handle en passant
    if board.is_en_passant(move):
        offset = -8 if board.turn == chess.WHITE else 8
        target_square = move.to_square + offset
    else:
        target_square = move.to_square

    victim = board.piece_at(target_square)

    if victim is None or aggressor is None:
        logger.critical("Target or aggressor piece is None")
        logger.debug(f"Current board: \n{board}")
        logger.debug(f"Evaluating move: {move}, in algebraic notation: {board.san(move)}")
        logger.debug(f"From square: {move.from_square}, To square: {move.to_square}")
        logger.debug(f"Aggressor: {aggressor}, Victim: {victim}")
        return 0

    return piece_value[victim.piece_type] - piece_value[aggressor.piece_type]

def add_check_bonus(board, move, check_bonus=20):
    """
    Add a bonus for moves that give check.
    :param board: The chess board, currently uses the python chess board object
    :param move: The move to be evaluated
    :return: A score representing the evaluation of the move.
    """
    if board.gives_check(move):
        return check_bonus
    return 0


def count_material(board):
    white_material_score = 0
    black_material_score = 0
    white_pawn_material_score = 0
    black_pawn_material_score = 0
    for square, piece in board.piece_map().items():
        if piece.color:
            white_material_score += piece_value[piece.piece_type]
            if piece.piece_type == chess.PAWN:
                white_pawn_material_score += 100
        else:
            black_material_score -= piece_value[piece.piece_type]
            if piece.piece_type == chess.PAWN:
                black_pawn_material_score -= 100
    return (white_material_score - black_material_score), (white_material_score-white_pawn_material_score), (black_material_score-black_pawn_material_score)


def add_piece_square_table_bonuses(board, opponent_material_count_without_pawns):
    """
    Add bonuses for piece-square tables.
    :param board: The chess board, currently uses the python chess board object
    :param opponent_material_count_without_pawns: The material count of the opponent without pawns
    :return: A score representing the evaluation of the position.
    """
    all_pieces = board.piece_map().items()
    current_eval = 0
    if opponent_material_count_without_pawns <= 1300:
        #if endgame
        for square, piece in all_pieces:
            if not piece.color:
                square = chess.square_mirror(square)
            if piece.piece_type == chess.PAWN:
                current_eval += PAWN_END_TABLE[square]
            elif piece.piece_type == chess.KNIGHT:
                current_eval += KNIGHT_TABLE[square]
            elif piece.piece_type == chess.BISHOP:
                current_eval += BISHOP_TABLE[square]
            elif piece.piece_type == chess.ROOK:
                current_eval += ROOK_TABLE[square]
            elif piece.piece_type == chess.QUEEN:
                current_eval += QUEEN_TABLE[square]
            elif piece.piece_type == chess.KING:
                current_eval += KING_END_TABLE[square]
    else:
        for square, piece in all_pieces:
            if not piece.color:
                square = chess.square_mirror(square)
            if piece.piece_type == chess.PAWN:
                current_eval += PAWN_TABLE[square]
            elif piece.piece_type == chess.KNIGHT:
                current_eval += KNIGHT_TABLE[square]
            elif piece.piece_type == chess.BISHOP:
                current_eval += BISHOP_TABLE[square]
            elif piece.piece_type == chess.ROOK:
                current_eval += ROOK_TABLE[square]
            elif piece.piece_type == chess.QUEEN:
                current_eval += QUEEN_TABLE[square]
            elif piece.piece_type == chess.KING:
                current_eval += KING_MID_TABLE[square]
    return current_eval






def evaluate_position(board):
    """
    Evaluate the position of the board for the given color.
    :param board: The chess board, currently uses the python chess board object
    :return: A score representing the evaluation of the position.
    """
    turn = board.turn
    if board.outcome():
        if board.is_checkmate():
            return 1000000 if turn else -1000000
        else:
            return -1
    else:
        current_eval = 0
        material_eval_score, white_material_count_no_pawns, black_material_count_no_pawns = count_material(board)
        current_eval += material_eval_score
        if turn:
            PST_eval_score = add_piece_square_table_bonuses(board, black_material_count_no_pawns)
        else:
            PST_eval_score = add_piece_square_table_bonuses(board, white_material_count_no_pawns)
            
        current_eval += PST_eval_score
        return current_eval if turn else -current_eval