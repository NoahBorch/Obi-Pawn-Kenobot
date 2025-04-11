import unittest
import chess

from engine.search import find_best_move
from main import print_board_clean
from utils.log import logger, configure_logging, debug_config




configure_logging("debug")

class TestSearch(unittest.TestCase):
  

    def test_mate_in_one(self):
        # White to move, Qa8#
        board = chess.Board("6k1/5ppp/8/8/8/8/5PPP/6KQ w - - 0 1")
        
        
        logger.debug(f"Testing mate in one on this board: \n{print_board_clean(board)}")

        best_move, eval_score = find_best_move(board, depth=2)
        self.assertEqual(best_move.uci(), "h1a8")
        self.assertGreaterEqual(eval_score, 1000000)  # Adjust if you use a different MATE_SCORE

if __name__ == "__main__":
    unittest.main()