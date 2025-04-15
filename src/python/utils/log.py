from datetime import datetime
import logging
from pathlib import Path

from ui.terminal_prints import print_board_clean



# Custom level: Between DEBUG (10) and INFO (20)
PLAYING_VERBOSE_LEVEL = 25
logging.addLevelName(PLAYING_VERBOSE_LEVEL, "PLAYING")
# debug_config = {
#     "evaluation": False,
#     "search": False,
#     "counters": False,
#     "logging": False,
#     "main": False,
# }


def playing(self, message, *args, **kwargs):
    if self.isEnabledFor(PLAYING_VERBOSE_LEVEL):
        self._log(PLAYING_VERBOSE_LEVEL, message, args, **kwargs)

logging.Logger.playing = playing
logger = logging.getLogger("Kenobot")

class PlayingFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == PLAYING_VERBOSE_LEVEL

def configure_logging(level_str: str = "info", save_to_file: bool = False, logdir: str = "logs"):


    level_str = level_str.lower()

    level_map = {
        "debug": logging.DEBUG,
        "playing": PLAYING_VERBOSE_LEVEL,
        "info": logging.INFO
    }

    selected_level = level_map.get(level_str, logging.INFO)
    logger.setLevel(logging.DEBUG)  # Always capture all; filter per handler

    if not logger.hasHandlers():
        # Console output for DEBUG and INFO (excluding PLAYING)
        std_handler = logging.StreamHandler()
        std_formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)s - %(message)s', '%H:%M:%S'
        )
        std_handler.setFormatter(std_formatter)
        std_handler.addFilter(lambda record: record.levelno != PLAYING_VERBOSE_LEVEL)
        logger.addHandler(std_handler)

        # Console output for PLAYING level
        playing_handler = logging.StreamHandler()
        playing_formatter = logging.Formatter('%(message)s')
        playing_handler.setFormatter(playing_formatter)
        playing_handler.addFilter(PlayingFilter())
        logger.addHandler(playing_handler)

        if save_to_file:
            logs_dir = Path(logdir)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_subdir = logs_dir / f"epd_test_{timestamp}"
            log_subdir.mkdir(parents=True, exist_ok=True)

            # Full debug log file
            full_log_path = log_subdir / "full_debug.log"
            full_file_handler = logging.FileHandler(full_log_path, mode="w", encoding="utf-8")
            full_file_handler.setLevel(logging.DEBUG)
            full_file_handler.setFormatter(std_formatter)
            logger.addHandler(full_file_handler)

            # Summary log file (INFO+ only)
            summary_log_path = log_subdir / "summary.log"
            summary_file_handler = logging.FileHandler(summary_log_path, mode="w", encoding="utf-8")
            summary_file_handler.setLevel(logging.INFO)
            summary_file_handler.setFormatter(std_formatter)
            logger.addHandler(summary_file_handler)

            logger.debug(f"📄 Logging to: {full_log_path} (full) and {summary_log_path} (summary)")
            return log_subdir
    
def log_result(board):
    from utils.counters import get_total_counters
    
    logger.playing(f"Game Over: {board.result()}")
    logger.playing("Final Position:\n" + print_board_clean(board))
    if board.result() == "1-0":
        logger.playing("White won!")
    elif board.result() == "0-1":
        logger.playing("Black won!")
    else:
        logger.playing("It's a draw!")
    total_positions_evaluated, total_lines_pruned = get_total_counters()
    logger.info(f"Positions evaluated: {total_positions_evaluated} | Lines pruned: {total_lines_pruned}")
    logger.info("Thank you for playing!")

