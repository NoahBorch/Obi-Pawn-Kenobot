import chess
import chess.pgn
import random
import argparse
from utils.log import logger, configure_logging, debug_config, log_result
from utils.counters import get_total_counters, reset_total_counters
from engine.search import find_best_move

debug_main = debug_config["main"]

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

    parser.add_argument(
    "--selfplay-loop",
    action="store_true",
    help="Enable infinite bot vs bot self-play loop mode"
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


    
def main():
    global total_positions_evaluated, total_lines_pruned
    args, players_color = parse_args()
    # Configure logging based on user selection
    configure_logging(get_log_level(args))

    board = chess.Board()
    depth = 3
    logger.playing("Welcome to Obi-Pawn Kenobot! Let's play.")
    logger.playing("You are playing as " + ("White" if players_color == chess.WHITE else "Black"))

    #PGN
    game = chess.pgn.Game()
    game.headers["Event"] = "Obi-Pawn Kenobot Game"
    game.headers["White"] = "Human" if players_color == chess.WHITE else "Obi-Pawn"
    game.headers["Black"] = "Obi-Pawn" if players_color == chess.WHITE else "Human"
    game.headers["Depth"] = str(depth)
    node = game

 
    if players_color == "only_bot" and args.selfplay_loop:
        logger.playing("Obi-Pawn Kenobot is playing against itself (loop mode).")
        while True:
            board = chess.Board()

            game = chess.pgn.Game()
            game.headers["Event"] = "Obi-Pawn Kenobot Self-Play"
            game.headers["White"] = "Obi-Pawn"
            game.headers["Black"] = "Obi-Pawn"
            game.headers["Depth"] = str(depth)
            node = game

            while not board.is_game_over():
                logger.playing("\n" + str(board))
                move, eval = find_best_move(board, depth)
                logger.playing(f"Obi-Pawn plays: {board.san(move)}")
                logger.info(f"Bot chose {move} from {len(list(board.legal_moves))} legal options. Score: {eval}")
                board.push(move)
                node = node.add_variation(move)

            log_result(board)

            counters = get_total_counters()
            game.headers["PositionsEvaluated"] = str(counters[0])
            game.headers["LinesPruned"] = str(counters[1])
            game.headers["Result"] = board.result()

            with open("bot_vs_bot_games.pgn", "a") as pgn_file:
                print(game, file=pgn_file, end="\n\n")

            logger.info("Game finished and appended to PGN. Starting new game...\n")
            reset_total_counters()
            

    elif players_color == "only_bot":
        logger.playing("Obi-Pawn Kenobot is playing against itself.")
        while not board.is_game_over():
            logger.playing("\n" + str(board))
            move, eval = find_best_move(board, depth)
            logger.playing(f"Obi-Pawn plays: {board.san(move)}")
            logger.info(f"Bot chose {move} from {len(list(board.legal_moves))} legal options. It gave the move a score of {eval}")
            board.push(move)
            node = node.add_variation(move)
    else:
        while not board.is_game_over():
            logger.playing("\n" + str(board))

            if board.turn == players_color:
                move_input = input("Your move: ")
                try:
                    uci_move = chess.Move.from_uci(move_input)
                    if uci_move not in board.legal_moves: 
                        raise ValueError
                    board.push(uci_move)
                    node = node.add_variation(uci_move)
                except ValueError:
                    logger.warning("Invalid move format or illegal move. Try again.")
                    continue
            else:
                move, eval = find_best_move(board, depth)
                board.push(move)
                node = node.add_variation(move)
                logger.playing(f"Obi-Pawn plays: {move}")
                logger.info(f"Bot chose {move} from {len(list(board.legal_moves))} legal options. It gave the move a score of {eval}")
    
    log_result(board)

    counters = get_total_counters()
    game.headers["PositionsEvaluated"] = str(counters[0])
    game.headers["LinesPruned"] = str(counters[1])
    game.headers["Result"] = board.result()

    if players_color == "only_bot":
        pgn_filename = "bot_vs_bot_games.pgn"
    else:
        pgn_filename = "bot_vs_human_games.pgn"

    with open(pgn_filename, "a") as pgn_file:
        print(game, file=pgn_file, end="\n\n")  # ensure proper spacing between games

    logger.info(f"Game PGN appended to {pgn_filename}")


    


if __name__ == "__main__":
    main()
