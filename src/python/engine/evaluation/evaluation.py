#evaluation.py

import chess
from utils.log import logger, debug_config
from engine.evaluation.PSTs import get_piece_square_tables_by_phase, PHASE_OPENING, PHASE_MIDGAME, PHASE_ENDGAME



debug_evaluation = debug_config["evaluation"]
last_logged_phase = PHASE_OPENING



piece_value = {
    chess.PAWN: 100,
    chess.KNIGHT: 300,
    chess.BISHOP: 320,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 0,
}
# Define all correctly-oriented PSTs as Python lists from rank 1 to rank 8



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
            black_material_score += piece_value[piece.piece_type]
            if piece.piece_type == chess.PAWN:
                black_pawn_material_score += 100
    if debug_evaluation:
        logger.debug(f"material count score: {white_material_score - black_material_score}")
        logger.debug(f"white material no pawns score: {white_material_score-black_material_score-white_pawn_material_score+black_pawn_material_score}")
        logger.debug(f"black material no pawns score: {black_material_score-white_material_score+white_pawn_material_score-black_pawn_material_score}")
  
    return (white_material_score - black_material_score), (white_material_score-white_pawn_material_score), (black_material_score-black_pawn_material_score)


def add_piece_square_table_bonuses(board, opponent_material_count_without_pawns):
    """
    Add bonuses for piece-square tables.
    :param board: The chess board, currently uses the python chess board object
    :param opponent_material_count_without_pawns: The material count of the opponent without pawns
    :return: A score representing the evaluation of the position.
    """
    global last_logged_phase
    all_pieces = board.piece_map().items()
    current_eval = 0

    if last_logged_phase != PHASE_ENDGAME:
        if opponent_material_count_without_pawns <= 1300:
            phase = PHASE_ENDGAME
        elif board.fullmove_number <= 10:
            phase = PHASE_OPENING
        else:
            phase = PHASE_MIDGAME
        if phase != last_logged_phase:
            if debug_evaluation:
                logger.debug(f"Phase changed from {last_logged_phase} to {phase}")
            last_logged_phase = phase
    else:   
        phase = PHASE_ENDGAME
    
    PIECE_SQUARE_TABLES = get_piece_square_tables_by_phase(phase)

    for square, piece in all_pieces:
        if piece.color:
            current_eval += PIECE_SQUARE_TABLES[piece.piece_type][square]
        else:
            current_eval -= PIECE_SQUARE_TABLES[piece.piece_type][square]
    if debug_evaluation:
        logger.debug(f"Current PST score: {current_eval}")
    return current_eval

def endgame_incentives(board):
    white_king_square = board.king(chess.WHITE)
    black_king_square = board.king(chess.BLACK)
    distance_between_kings = chess.square_distance(white_king_square, black_king_square)
    bonus = 50 - distance_between_kings
    return bonus 


def evaluate_position(board):
    """
    Evaluate the position of the board for the given color.
    :param board: The chess board, currently uses the python chess board object
    :return: A score representing the evaluation of the position.
    """
    global debug_evaluation
    turn = board.turn
    if debug_evaluation:
        logger.debug(f"Evaluating position for {'white' if turn else 'black'}")
        logger.debug(f"Current board: \n{board}")
        logger.debug(f"Turn: {turn}")
        logger.debug(f"Current phase: {last_logged_phase}")
        if board.is_checkmate():
            logger.debug("Checkmate detected")
    if board.outcome():
        if board.is_checkmate():
            if debug_evaluation:
                from main import print_board_clean
                logger.debug(f"Checkmate detected for moving player: {turn}, in position: \n{print_board_clean(board)} after player plays {board.san(board.peek())}")
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

        if last_logged_phase == PHASE_ENDGAME:
            current_eval += endgame_incentives(board)

        if debug_evaluation:
            logger.debug(f"Current evaluation score: {current_eval if turn else -current_eval}")
        return current_eval if turn else -current_eval