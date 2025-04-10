import logging


# Custom level: Between DEBUG (10) and INFO (20)
PLAYING_VERBOSE_LEVEL = 25
logging.addLevelName(PLAYING_VERBOSE_LEVEL, "PLAYING")
debug_config = {
    "evaluation": False,
    "search": False,
    "counters": False,
    "logging": False,
    "main": False,
}


def playing(self, message, *args, **kwargs):
    if self.isEnabledFor(PLAYING_VERBOSE_LEVEL):
        self._log(PLAYING_VERBOSE_LEVEL, message, args, **kwargs)

logging.Logger.playing = playing
logger = logging.getLogger("Kenobot")

class PlayingFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == PLAYING_VERBOSE_LEVEL

def configure_logging(level_str: str = "info"):
    level_str = level_str.lower()

    level_map = {
        "debug": logging.DEBUG,
        "playing": PLAYING_VERBOSE_LEVEL,
        "info": logging.INFO
    }

    selected_level = level_map.get(level_str, logging.INFO)
    logger.setLevel(selected_level)

    if not logger.hasHandlers():
        # Handler for standard levels (INFO, DEBUG)
        std_handler = logging.StreamHandler()
        std_formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)s - %(message)s', '%H:%M:%S'
        )
        std_handler.setFormatter(std_formatter)
        std_handler.addFilter(lambda record: record.levelno != PLAYING_VERBOSE_LEVEL)
        logger.addHandler(std_handler)

        # Handler for PLAYING level — clean output
        playing_handler = logging.StreamHandler()
        playing_formatter = logging.Formatter('%(message)s')  # No timestamp, no level
        playing_handler.setFormatter(playing_formatter)
        playing_handler.addFilter(PlayingFilter())
        logger.addHandler(playing_handler)

def log_result(board):
    from utils.counters import get_total_counters
    
    logger.playing(f"Game Over: {board.result()}")
    logger.playing("Final Position:\n" + str(board))
    if board.result() == "1-0":
        logger.playing("White won!")
    elif board.result() == "0-1":
        logger.playing("Black won!")
    else:
        logger.playing("It's a draw!")
    total_positions_evaluated, total_lines_pruned = get_total_counters()
    logger.info(f"Positions evaluated: {total_positions_evaluated} | Lines pruned: {total_lines_pruned}")
    logger.info("Thank you for playing!")

