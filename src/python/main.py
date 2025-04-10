import chess
import random
import argparse
from utils.log import logger, configure_logging
from utils.counters import total_positions_evaluated, total_lines_pruned
from engine.evaluation import evaluate_position
from engine.search import find_best_move

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

    parser.add_argument(
        "--player",
        choices=["white", "black", "random", "none", "choose_later"],
        default="choose_later",
    )

    args = parser.parse_args()
    # if no argument is passed, set default to "choose_later"
    if args.player == "choose_later":
        user_input = input("Choose your color (white, black, random, none): ").strip().lower()
        while user_input not in ["white", "black", "random", "none"]:
            print("Invalid choice. Please choose from: white, black, random, none.")
            user_input = input("Choose your color (white, black, random, none): ").strip().lower()
        args.player = user_input
    
    if args.player == "white":
        players_color = chess.WHITE
    elif args.player == "black":
        players_color = chess.BLACK
    elif args.player == "random":
        players_color = random.choice([chess.WHITE, chess.BLACK])
    elif args.player == "none":
        players_color = "only_bot"

    return parser.parse_args(), players_color

def get_log_level(args):
    return "playing" if args.play else args.log

def log_result(board):
    global total_positions_evaluated, total_lines_pruned
    logger.playing(f"Game Over: {board.result()}")
    logger.playing("Final Position:\n" + str(board))
    if board.result() == "1-0":
        logger.playing("White won!")
    elif board.result() == "0-1":
        logger.playing("Black won!")
    else:
        logger.playing("It's a draw!")
    logger.info(f"Positions evaluated: {total_positions_evaluated} | Lines pruned: {total_lines_pruned}")
    
def main():
    global total_positions_evaluated, total_lines_pruned
    args, players_color = parse_args()
    # Configure logging based on user selection
    configure_logging(get_log_level(args))


    board = chess.Board()
    depth = 3
    logger.playing("Welcome to Obi-Pawn Kenobot! Let's play.")
    logger.playing("You are playing as " + ("White" if players_color == chess.WHITE else "Black"))

    if players_color == "only_bot":
        logger.playing("Obi-Pawn Kenobot is playing against itself.")
        while not board.is_game_over():
            logger.playing("\n" + str(board))
            move, eval = find_best_move(board, depth)
            logger.playing(f"Obi-Pawn plays: {board.san(move)}")
            logger.info(f"Bot chose {move} from {len(list(board.legal_moves))} legal options. It gave the move a score of {eval}")
            board.push(move)
        log_result(board)
        logger.info(f"Positions evaluated: {total_positions_evaluated} | Lines pruned: {total_lines_pruned}")
        return

    while not board.is_game_over():
        logger.playing("\n" + str(board))

        if board.turn == players_color:
            move = input("Your move: ")
            try:
                board.push_uci(move)
            except ValueError:
                logger.warning("Invalid move format or illegal move. Try again.")
                continue
        else:
            move, eval = find_best_move(board, depth)
            board.push(move)
            logger.playing(f"Obi-Pawn plays: {move}")
            logger.info(f"Bot chose {move} from {len(list(board.legal_moves))} legal options. It gave the move a score of {eval}")

    log_result(board)
    logger.info(f"Positions evaluated: {total_positions_evaluated} | Lines pruned: {total_lines_pruned}")



if __name__ == "__main__":
    main()
