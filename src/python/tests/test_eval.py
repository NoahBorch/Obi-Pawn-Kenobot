import unittest
import chess
from pathlib import Path
import sys

# Filepath shenanigans
project_root = Path(__file__).resolve().parents[1]  # this is src/python
sys.path.insert(0, str(project_root))

from utils.debug_config import set_debug_config_for_module
set_debug_config_for_module("play", False)
set_debug_config_for_module("evaluation", False)
set_debug_config_for_module("search", True)
from utils.config import set_global_depth
from engine.evaluation.evaluation import evaluate_position
from lichess_integration.play import play_board
from utils.log import logger, configure_logging
from ui.terminal_prints import print_board_clean

class TestEval(unittest.TestCase):
    def test_from_FEN(self, fen: str, iterations: int = 1, depth: int = 4):
        """
        Test the evaluation of a position from a FEN string.
        """
        if not isinstance(fen, str):
            raise ValueError("FEN must be a string")
        if not isinstance(iterations, int):
            raise ValueError("Iterations must be an integer")
        if fen is None or iterations < 1:
            raise ValueError("FEN cannot be None and iterations must be at least 1")
        # Initialize the board from the FEN string
        board = chess.Board(fen)
        set_global_depth(depth)
        

        logger.info(f"Debugging current position:\n{print_board_clean(board)}")

        
        # Evaluate the position
        evaluation = evaluate_position(board)
        logger.info(f"Position eval: {evaluation}")
        

        #testing play_board 
        total_time_left = 3 * 60* 1000  
        increment = 20000000
        logger.info(f"Testing play_board with total_time = {total_time_left}s and increment set to {increment}s")
        move_uci = play_board(board, total_time_left=total_time_left, increment=increment)
        move = chess.Move.from_uci(move_uci)
        logger.info(f"Best move according to play_board: {board.san(move)}")
        # Apply the move to the board
        for i in range(iterations):
            logger.info(f"Iteration {i+1}:")
            if board.is_checkmate():
                logger.info("Checkmate detected! Final board state: \n" + print_board_clean(board))
                break
            board.push(move)
            logger.info(f"Board after move: \n{print_board_clean(board)}")
            move_uci = play_board(board, total_time_left=total_time_left, increment=increment)
            move = chess.Move.from_uci(move_uci)
            logger.info(f"Best response according to play_board: {board.san(move)}")
    
    def test_FEN_1(self):
        fen = "1rr3k1/5pp1/p2p3p/1pP1p3/4R3/5q2/P1PP1PPP/3R2K1 w - - 0 26"
        iterations = 4
        self.test_from_FEN(fen, iterations)


if __name__ == "__main__":
    # Configure logging
    path = configure_logging("debug", save_to_file=True, logdir=".logs/tests", category="test_eval")
    print(f"saving logs to {path}")
    
    # Run the tests
    unittest.main()
            
        
