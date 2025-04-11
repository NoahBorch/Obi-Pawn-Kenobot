import unittest
import chess
import time
from pathlib import Path


from engine.search import find_best_move
from main import set_global_depth
from ui.terminal_prints import print_board_clean
from utils.log import logger, configure_logging
from utils.debug_config import get_debug_config, set_debug_config_for_module





class TestSearch(unittest.TestCase):
  

    def test_mate_in_one(self):
        # White to move, Qa8#
        board = chess.Board("6k1/5ppp/8/8/8/8/5PPP/3Q2KR w - - 0 1")
        
        
        logger.debug(f"Testing mate in one on this board: \n{print_board_clean(board)}")

        best_move, eval_score = find_best_move(board, depth=2)
        self.assertEqual(best_move.uci(), "d1d8")
        self.assertGreaterEqual(eval_score, 1000000)  # Adjust if you use a different MATE_SCORE
    
    
    def test_all_EPD_positions(self):
        configure_logging("debug", save_to_file=True, logdir="logs/epd_tests")
        set_debug_config_for_module("search", True)


        # Prompt user for depth
        #depth = input("Enter the depth for EPD tests (default is 3): ")
        depth = "5"
        if not depth.isdigit():
            depth = 3
        else:
            depth = int(depth)
        set_global_depth(depth)

        logger.debug(f"Using depth: {depth}")
        epd_path = Path(__file__).parent / "EPD_tests.txt"

        with open(epd_path, "r") as file:
            epd_positions = file.readlines()

        total = 0
        correct = 0
        failed = 0
        errors = 0
        start_time = time.perf_counter()

        for epd_line in epd_positions:
            epd_line = epd_line.strip()
            if not epd_line or epd_line.startswith("#"):
                continue

            total += 1
          

            try:
                board = chess.Board()
                operations = board.set_epd(epd_line)
                expected_moves = operations.get("bm", [])

                if not expected_moves:
                    logger.warning(f"⚠️ No best move found in: {epd_line}")
                    continue

                expected_move = expected_moves[0]  # just use the first one

                logger.debug("=" * 50)
                logger.debug(f"📌 Position {total}")
                logger.debug(f"\n{print_board_clean(board)}")
                logger.debug(f"🔍 Expected move: {board.san(expected_move)}")

                best_move, eval_score = find_best_move(board, depth=depth)
                #move_san = board.san(best_move)

                if not board.is_legal(expected_move):
                    logger.error("🚫🚫🚫🚫🚫🚫🚫🚫🚫 SOMETHING IS WRONG 🚫🚫🚫🚫🚫🚫🚫🚫🚫🚫🚫🚫")
                    logger.error(f"Expected move {board.san(expected_move)} is not legal in this position!")
                    logger.debug(f"Legal moves were: {[board.san(move) for move in board.legal_moves]}")
                    logger.debug(f"Best move was: {board.san(best_move)}")
                    logger.debug(f"Expected move was: {board.san(expected_move)}")
                    logger.debug(f"EPD line was: {epd_line}")
                    logger.debug(f"FEN was: {board.fen()}")
                elif best_move.uci() not in [move.uci() for move in board.legal_moves]:
                    logger.error(f"🚫 ILLEGAL move from engine: {best_move.san()} is not legal in this position!")
                    logger.debug(f"Legal moves were: {[move.san() for move in board.legal_moves]}")
                    errors += 1
                    continue

                try:
                    move_san = board.san(best_move)
                except ValueError:
                    move_san = f"[INVALID MOVE: {best_move.uci()}]"

                if best_move == expected_move:
                    correct += 1
                    logger.debug(f"✅ Chosen move: {move_san} (Eval: {eval_score}) — CORRECT")
                else:
                    failed += 1
                    logger.warning(f"❌ Chosen move: {move_san} (Eval: {eval_score}) — WRONG")

            except Exception as e:
                errors += 1
                logger.error(f"💥 ERROR: Could not process EPD: {epd_line}\n{e}")

        # Final summary
        duration = round(time.perf_counter() - start_time, 2)
        logger.info("\n" + "=" * 50)
        logger.info("📊 EPD TEST SUMMARY")
        logger.info(f"🧩 Total positions: {total}")
        logger.info(f"✅ Correct: {correct}")
        logger.info(f"❌ Wrong: {failed}")
        logger.info(f"💥 Errors: {errors}")
        logger.info(f"⏱ Duration: {duration} seconds")
        logger.info("=" * 50 + "\n")

if __name__ == "__main__":  
    suite = unittest.TestSuite()
    suite.addTest(TestSearch("test_all_EPD_positions"))
    runner = unittest.TextTestRunner()
    runner.run(suite)