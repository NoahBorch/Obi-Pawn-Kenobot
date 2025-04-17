from pathlib import Path
import sys
import chess
import time

#Filepath shenanigans 
project_root = Path(__file__).parent.resolve()
sys.path.insert(0, str(project_root))


from engine.search import find_best_move  
from utils.log import logger
from utils.debug_config import get_debug_config
from utils.game_phase import calculate_game_phase, get_last_logged_phase, PHASE_ENDGAME, PHASE_MIDGAME, PHASE_OPENING



def play(fen: str, history: list[str], time_limit: float = None) -> str:

    board = chess.Board(fen)
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



