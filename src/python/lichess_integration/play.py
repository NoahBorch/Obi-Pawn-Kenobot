from pathlib import Path
import sys
import chess
import time

from ui.terminal_prints import print_board_clean

#Filepath shenanigans 
project_root = Path(__file__).parent.resolve()
sys.path.insert(0, str(project_root))


from engine.search import find_best_move  
from utils.log import logger
from utils.debug_config import get_debug_config
from utils.config import get_global_depth
from utils.game_phase import calculate_game_phase, get_last_logged_phase, PHASE_ENDGAME, PHASE_MIDGAME, PHASE_OPENING

debug_play = get_debug_config("play")



def play_board(board: chess.Board, total_time_left: float = None, increment: float = None, using_movetime: bool = False) -> str:
    """
    Play a move on the given board with an optional time limit.
    
    Parameters:
        board (chess.Board): The chess board to play on.
        time_limit (float, optional): The time limit for the move in seconds. Defaults to None.
        
    Returns:
        str: The UCI representation of the chosen move.
    """
    start_time = time.perf_counter()
    phase = calculate_game_phase(board)

    if total_time_left and not using_movetime:
        if debug_play:
            logger.debug("using_movetime=False =>  Calculating move time based on game phase")
        if phase == PHASE_OPENING:
            expected_moves_left = 40
        elif phase == PHASE_MIDGAME:
            expected_moves_left = 30
        else:
            expected_moves_left = 20
        move_time = (total_time_left / expected_moves_left) 
        if increment:
            move_time += 0.95 * increment
            if debug_play:
                logger.debug(f"Adding increment: {increment} to move time: {move_time}")
        if debug_play:
            logger.debug(f"Using expected moves left: {expected_moves_left}")
            logger.debug(f"Current move_time set to {move_time}")
        move_time = min(move_time, total_time_left * 0.6)
        if debug_play:
            logger.debug(f"Current move_time set to {move_time} after checking against total time left")
        move_time = max(0.5, move_time)
        if debug_play:
            logger.debug(f"Final move_time set to {move_time} after making sure it's at least 0.5s")
    elif total_time_left and using_movetime:
        if debug_play:
            logger.debug("using_movetime=True =>  Using total time left as the move time")
        move_time = total_time_left
    else:
        move_time = 5.0  # Fallback default
        if debug_play:
            logger.debug("No time limit provided, using default move time of 5.0 seconds")
    if debug_play:
        logger.debug(f"Using move time: {move_time:.2f}s")

    depth = get_global_depth()
    move, eval = find_best_move(board, depth=depth, time_budget=move_time)

    think_time = time.perf_counter() - start_time

    logger.info(f"Chosen move: {move}, Time spent: {think_time:.2f}s / {move_time:.2f}s, My eval estimate: {eval:.2f}")
    return move.uci()


def play(fen: str, history: list[str], time_limit: float = None) -> str:

    board = chess.Board()
    for move_uci in history:
        board.push_uci(move_uci)
    assert board.fen() == fen  # Should match the input if everything is consistent

    start_time = time.perf_counter()

    if time_limit:
        phase = calculate_game_phase(board)
        if phase == PHASE_OPENING:
            expected_moves_left = 40
        elif phase == PHASE_MIDGAME:
            expected_moves_left = 30
        else:
            expected_moves_left = 20
        move_time = time_limit / expected_moves_left
        move_time = min(move_time * 2, time_limit * 0.6)
        move_time = max(0.05, move_time)
    else:
        move_time = 5.0  # Fallback default

    move, eval = find_best_move(board, depth=10, move_time=move_time)

    think_time = time.perf_counter() - start_time

    logger.info(f"Chosen move: {move}, Time spent: {think_time:.2f}s / {move_time:.2f}s,  My eval estimate: {eval:.2f}")
    return move.uci()



