import chess
import random
import argparse
from utils.log import logger, configure_logging

def parse_args():
    parser = argparse.ArgumentParser(description="Play a game against Obi-Pawn Kenobot")

    parser.add_argument(
        "--log",
        choices=["info", "playing", "debug"],
        default="info",
        help="Set logging verbosity level"
    )

    parser.add_argument(
        "--play",
        action="store_true",
        help="Enable play mode (same as --log playing)"
    )

    return parser.parse_args()
def get_log_level(args):
    return "playing" if args.play else args.log

def log_result(board):
    logger.playing(f"Game Over: {board.result()}")
    logger.playing("Final Position:\n" + str(board))
    if board.result() == "1-0":
        logger.playing("White won!")
    elif board.result() == "0-1":
        logger.playing("Black won!")
    else:
        logger.playing("It's a draw!")
    
def main():
    args = parse_args()
    # Configure logging based on user selection
    configure_logging(get_log_level(args))

    board = chess.Board()
    logger.playing("Welcome to Obi-Pawn Kenobot! Let's play.")

    while not board.is_game_over():
        logger.playing("\n" + str(board))

        if board.turn == chess.WHITE:
            move = input("Your move: ")
            try:
                board.push_uci(move)
            except ValueError:
                logger.warning("Invalid move format or illegal move. Try again.")
                continue
        else:
            move = random.choice(list(board.legal_moves))
            board.push(move)
            logger.playing(f"Obi-Pawn plays: {move}")
            logger.info(f"Bot chose {move} from {len(list(board.legal_moves))} legal options.")

    log_result(board)


if __name__ == "__main__":
    main()
