import json
import unittest
import chess
import time
from pathlib import Path
import sys

# Filepath shenanigans
project_root = Path(__file__).resolve().parents[1]  # this is src/python
sys.path.insert(0, str(project_root))

from utils.debug_config import get_debug_config, set_debug_config_for_module, set_no_debug
set_debug_config_for_module("search", False)
set_debug_config_for_module("play", False)
from engine.search import find_best_move
from main import set_global_depth
from ui.terminal_prints import print_board_clean
from utils.log import logger, configure_logging
from utils.constants import CHECKMATE_BASE_SCORE





class TestSearch(unittest.TestCase):
  

    def test_mate_in_one(self):
        # White to move, Qa8#
        configure_logging("debug", save_to_file=False)
        
        board = chess.Board("6k1/5ppp/8/8/8/8/5PPP/3Q2KR w - - 0 1")
        logger.debug(f"Testing mate in one on this board: \n{print_board_clean(board)}")
        best_move, eval_score = find_best_move(board, depth=2, time_budget=10)
        logger.debug(f"Best move: {best_move} (Eval: {eval_score})")
        self.assertEqual(best_move.uci(), "d1d8")
        self.assertGreaterEqual(eval_score, CHECKMATE_BASE_SCORE) 

    def test_epd_10_positions_depth6_time10(self):
        self.run_epd_test_suite(file_name="EPD_tests.txt", depth=10, max_lines=10, time_budget=10)

    def test_bratko_10_positions_depth6_time10(self):
        self.run_epd_test_suite(file_name="Bratko-Kopec_test_suite.txt", depth=10, max_lines=10, time_budget=10)

    
    def run_epd_test_suite(self, file_name="EPD_tests.txt", depth=4, max_lines=None, time_budget=None):
        set_global_depth(depth)

        log_path = configure_logging(
            "debug",
            save_to_file=True,
            logdir=f".logs/search_test/depth{depth}",
            category=file_name.replace('.txt','')
        )

        print(f"Log path: {log_path}")
        print(f"Log saved to absolute path: {log_path.resolve()}")

        set_debug_config_for_module("search", False)
        set_debug_config_for_module("play", True)

        epd_path = Path(__file__).parent / file_name
        with open(epd_path, "r") as file:
            epd_positions = [line.strip() for line in file if line.strip() and not line.startswith("#")]

        if max_lines is not None:
            epd_positions = epd_positions[:max_lines]

        results_log = []
        total = correct = failed = errors = 0
        output_file = log_path / f"{file_name.replace('.txt','')}_results.json"
        output_results = log_path / f"{file_name.replace('.txt','')}_results.log"
        start_time = time.perf_counter()

        try:
            for idx, epd_line in enumerate(epd_positions, 1):
                best_move = expected_move = eval_score = None
                try:
                    board = chess.Board()
                    operations = board.set_epd(epd_line)
                    expected_moves = operations.get("bm", [])

                    if not expected_moves:
                        logger.warning(f"⚠️ No best move in line {idx}: {epd_line}")
                        result_status = "skipped"
                        continue

                    expected_move = expected_moves[0]

                    logger.debug("=" * 50)
                    logger.info(f"📌 Position {idx}")
                    logger.info(f"\n{print_board_clean(board)}")
                    logger.info(f"🔍 Expected move: {board.san(expected_move)}")

                    best_move, eval_score = find_best_move(board, depth=depth, time_budget=time_budget)

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
                    logger.error(f"💥 ERROR on line {idx} — {epd_line}\n{e}")
                    errors += 1
                    result_status = "error"

                total += 1
                results_log.append({
                    "line": idx,
                    "epd": epd_line,
                    "fen": board.fen() if 'board' in locals() else None,
                    "expected_move": expected_move.uci() if 'expected_move' in locals() and expected_move else None,
                    "best_move": best_move.uci() if 'best_move' in locals() and best_move else None,
                    "eval": eval_score,
                    "result": result_status
                })

        except KeyboardInterrupt:
            logger.warning("⚠️ Interrupted — saving progress.")

        finally:
            duration = round(time.perf_counter() - start_time, 2)

            logger.info("\n" + "=" * 50)
            logger.info(f"📊 TEST SUMMARY ({file_name})")
            logger.info(f"🧩 Total: {total} | ✅ Correct: {correct} | ❌ Wrong: {failed} | 💥 Errors: {errors}")
            logger.info(f"⏱ Duration: {duration} seconds")
            logger.info("=" * 50 + "\n")

            try:
                with open(output_file, "w") as f:
                    json.dump(results_log, f, indent=2)
                logger.info(f"📄 JSON saved: {output_file}")
            except Exception as e:
                logger.error(f"💥 Failed to save JSON: {e}")

            try:
                with open(output_results, "w") as f:
                    f.write("\n" + "=" * 50)
                    f.write(f"\n📊 TEST SUMMARY ({file_name})")
                    f.write(f"\n🧩 Total: {total}")
                    f.write(f"\n✅ Correct: {correct}")
                    f.write(f"\n❌ Wrong: {failed}")
                    f.write(f"\n💥 Errors: {errors}")
                    f.write(f"\n⏱ Duration: {duration} seconds")
                    f.write("\n" + "=" * 50 + "\n")
                logger.info(f"📄 Log saved: {output_results}")
            except Exception as e:
                logger.error(f"💥 Failed to save log: {e}")


if __name__ == "__main__":  
    suite = unittest.TestSuite()
    suite.addTest(TestSearch("test_epd_10_positions_depth6_time10"))
    suite.addTest(TestSearch("test_bratko_10_positions_depth6_time10"))
    suite.addTest(TestSearch("test_mate_in_one"))
    runner = unittest.TextTestRunner()
    runner.run(suite)

#To run: python3 -m unittest tests.test_search.TestSearch.run_epd_test_suite