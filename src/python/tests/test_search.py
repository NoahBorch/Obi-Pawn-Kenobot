import json
import unittest
import chess
import time
from pathlib import Path


from utils.debug_config import get_debug_config, set_debug_config_for_module, set_no_debug
from engine.search import find_best_move
from main import set_global_depth
from ui.terminal_prints import print_board_clean
from utils.log import logger, configure_logging





class TestSearch(unittest.TestCase):
  

    def test_mate_in_one(self):
        # White to move, Qa8#
        board = chess.Board("6k1/5ppp/8/8/8/8/5PPP/3Q2KR w - - 0 1")
        
        
        logger.debug(f"Testing mate in one on this board: \n{print_board_clean(board)}")

        best_move, eval_score = find_best_move(board, depth=2)
        self.assertEqual(best_move.uci(), "d1d8")
        self.assertGreaterEqual(eval_score, 1000000)  # Adjust if you use a different MATE_SCORE
    
    
    def test_all_EPD_positions(self):

        # Set depth manually or via prompt
        depth = "3"
        if not depth.isdigit():
            depth = 3
        else:
            depth = int(depth)
        set_global_depth(depth)

        # Use new logger config that returns the log folder path
        log_path = configure_logging("debug", save_to_file=True, logdir=f"../../.logs/search_test/depth{depth}/epd_tests_split")
        set_debug_config_for_module("search", True)

        logger.debug(f"Using depth: {depth}")
        epd_path = Path(__file__).parent / "EPD_tests.txt"

        with open(epd_path, "r") as file:
            epd_positions = file.readlines()

        total = 0
        correct = 0
        failed = 0
        errors = 0
        results_log = []
        output_file = log_path / "epd_test_results.json"
        output_results = log_path / "epd_test_results.log"
        start_time = time.perf_counter()

        try:
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

                    expected_move = expected_moves[0]

                    logger.debug("=" * 50)
                    logger.info(f"📌 Position {total}")
                    logger.info(f"\n{print_board_clean(board)}")
                    logger.info(f"🔍 Expected move: {board.san(expected_move)}")

                    best_move, eval_score = find_best_move(board, depth=depth)

                    if not board.is_legal(expected_move):
                        logger.error("🚫 SOMETHING IS WRONG")
                        logger.error(f"Expected move {board.san(expected_move)} is not legal!")
                        logger.debug(f"Legal moves: {[board.san(m) for m in board.legal_moves]}")
                        errors += 1
                        result_status = "error"
                        continue

                    try:
                        move_san = board.san(best_move)
                    except ValueError:
                        move_san = f"[INVALID MOVE: {best_move.uci()}]"

                    if best_move == expected_move:
                        correct += 1
                        logger.info(f"✅ Chosen move: {move_san} (Eval: {eval_score}) — CORRECT")
                        result_status = "correct"
                    else:
                        failed += 1
                        logger.warning(f"❌ Chosen move: {move_san} (Eval: {eval_score}) — WRONG")
                        result_status = "wrong"

                except Exception as e:
                    logger.error(f"💥 ERROR processing EPD: {epd_line}\n{e}")
                    errors += 1
                    best_move = None
                    expected_move = None
                    eval_score = None
                    result_status = "error"

                results_log.append({
                    "position": epd_line,
                    "fen": board.fen() if 'board' in locals() else None,
                    "expected_move": expected_move.uci() if expected_moves else None,
                    "best_move": best_move.uci() if best_move else None,
                    "eval": eval_score,
                    "result": result_status
                })

        except KeyboardInterrupt:
            logger.warning("⚠️ KeyboardInterrupt — Exiting early and saving results.")

        finally:
            duration = round(time.perf_counter() - start_time, 2)

            logger.info("\n" + "=" * 50)
            logger.info("📊 EPD TEST SUMMARY")
            logger.info(f"🧩 Total positions: {total}")
            logger.info(f"✅ Correct: {correct}")
            logger.info(f"❌ Wrong: {failed}")
            logger.info(f"💥 Errors: {errors}")
            logger.info(f"⏱ Duration: {duration} seconds")
            logger.info("=" * 50 + "\n")
            logger.info(f"Depth used: {depth}")

            try:
                with open(output_file, "w") as f:
                    json.dump(results_log, f, indent=2)
                logger.info(f"📄 Results saved to {output_file}")
            except Exception as e:
                logger.error(f"💥 Failed to save results JSON: {e}")
            try:
                with open(output_results, "w") as f:
                    f.write("\n" + "=" * 50)
                    f.write(f"📊 EPD TEST SUMMARY")
                    f.write(f"\n🧩 Total positions: {total}")
                    f.write(f"\n✅ Correct: {correct}")
                    f.write(f"\n❌ Wrong: {failed}")
                    f.write(f"\n💥 Errors: {errors}")
                    f.write(f"\n⏱ Duration: {duration} seconds")
                    f.write(f"Depth used: {depth}")
                    f.write("\n" + "=" * 50 + "\n")

                logger.info(f"📄 Results saved to {output_results}")
            except Exception as e:
                logger.error(f"💥 Failed to save results log: {e}")

if __name__ == "__main__":  
    suite = unittest.TestSuite()
    suite.addTest(TestSearch("test_all_EPD_positions"))
    runner = unittest.TextTestRunner()
    runner.run(suite)

    #To run: python -m unittest tests.test_search.TestSearch.test_all_EPD_positions