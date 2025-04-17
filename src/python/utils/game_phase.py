
import chess

from utils.log import logger
from utils.debug_config import get_debug_config
#from engine.evaluation.evaluation import count_opponents_material_no_pawns this would be a circular import so I define it here instead
from utils.constants import PHASE_OPENING, PHASE_MIDGAME, PHASE_ENDGAME, PIECE_VALUES 


debug_game_phase = get_debug_config("game_phase")
piece_value = PIECE_VALUES



# The last logged phase of the game.
last_logged_phase = PHASE_OPENING

def count_material_no_pawns(board):
    """
    Count the material on the board excluding pawns.
    :param board: The chess board, currently uses the python chess board object
    :return: A tuple containing the material count for white and black without pawns.
    """
    white_material_score = 0
    black_material_score = 0
    for square, piece in board.piece_map().items():
        if piece.piece_type == chess.PAWN:
            continue
        elif piece.color:
            white_material_score += piece_value[piece.piece_type]
        else:
            black_material_score += piece_value[piece.piece_type]
    return (white_material_score - black_material_score), (white_material_score), (black_material_score)


def set_last_logged_phase(phase: str) -> None:
    """
    Set the last logged phase of the game.
    
    Parameters:
        phase: str - The phase to set.
    """
    global last_logged_phase
    last_logged_phase = phase

    if debug_game_phase:
        logger.debug(f"Game phase set to: {phase}")

def get_last_logged_phase() -> str:
    """
    Get the last logged phase of the game.
    
    Returns:
        str: The last logged phase.
    """
    global last_logged_phase
    return last_logged_phase


def calculate_game_phase(board: chess.Board, opponent_material_without_pawns = None) -> str:
    """
    Calculate the game phase based on the current board state.
    
    Parameters:
        board: chess.Board - current board state.

    Returns:
        str: One of 'opening', 'midgame', or 'endgame'
    """

    if opponent_material_without_pawns is None:
        opponent_material_without_pawns = count_opponents_material_no_pawns(board)


    if opponent_material_without_pawns <= 1300:
        phase = PHASE_ENDGAME
    elif board.fullmove_number <= 10:
        phase = PHASE_OPENING
    else:
        phase = PHASE_MIDGAME

    global last_logged_phase
    if phase != last_logged_phase:
        logger.info(f"Game phase changed to: {phase}")
        last_logged_phase = phase

    return phase


