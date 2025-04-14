#main.py
import chess
import chess.pgn
import random
import argparse
import time

from utils.debug_config import debug_config
from utils.log import logger, configure_logging, log_result
from utils.config import get_global_depth, set_global_depth
from utils.debug_config import get_debug_config, set_debug_config_for_module
from utils.counters import get_total_counters, reset_total_counters
from engine.search import find_best_move
from ui.terminal_prints import print_board_clean, print_board_colored


debug_main = get_debug_config("main")
depth = get_global_depth()


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
        default="none",
    )

    parser.add_argument(
    "--selfplay-loop",
    action="store_true",
    help="Enable infinite bot vs bot self-play loop mode"
    )

    parser.add_argument(
        "--depth",
        choices=["choose_later"] + [str(i) for i in range(1, 10)],
        default="choose_later",
        help="Set the search depth for the engine (default: 5)"
    )

    parser.add_argument(
        "--color",
        action="store_true",
        help="Enable colored board output"
    )

    parser.add_argument(
        "--load_from_pgn",
        type=str,
        default=None,
        help="Load a game from a PGN file"
    )

    parser.add_argument(
        "--load_from_FEN",
        type=str,
        default=None,
        help="Load a game from a FEN string"
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

def create_pgn_game_and_node(players_color, depth):
    game = chess.pgn.Game()
    game.headers["Event"] = "Obi-Pawn Kenobot Game"
    game.headers["White"] = "Human" if players_color == chess.WHITE else "Obi-Pawn"
    game.headers["Black"] = "Obi-Pawn" if players_color == chess.WHITE else "Human"
    game.headers["Depth"] = str(depth)
    node = game
    return game, node

def add_game_result_to_pgn_and_write_pgn(game, board, players_color, start_time):
    counters = get_total_counters()
    game.headers["PositionsEvaluated"] = str(counters[0])
    game.headers["LinesPruned"] = str(counters[1])
    game.headers["Result"] = board.result()
    game.headers["Time"] = str(time.perf_counter() - start_time)

    if players_color == "only_bot":
        pgn_filename = "bot_vs_bot_games.pgn"
    else:
        pgn_filename = "bot_vs_human_games.pgn"

    with open(pgn_filename, "a") as pgn_file:
        print(game, file=pgn_file, end="\n\n")

    logger.info(f"Game result added to {pgn_filename}.")
    logger.info(f"Time taken: {game.headers['Time']} seconds")


def main():
    global total_positions_evaluated, total_lines_pruned, depth
    args, players_color = parse_args()
    # Configure logging based on user selection
    configure_logging(get_log_level(args))

    if args.depth == "choose_later" or int(args.depth) < 1:
        if args.depth == "choose_later":
            user_input = input("Choose search depth: ").strip()
        elif args.depth < 1:
            logger.playing("Invalid choice. Please choose a number between 1 and 10.")
            user_input = input("Choose search depth (1-10): ").strip()
        while not user_input.isdigit() or int(user_input) < 1 or int(user_input) > 10:
            logger.playing("Invalid choice. Please choose a number between 1 and 10.")
            user_input = input("Choose search depth (1-10): ").strip()
        depth = int(user_input)
       
    else:
        depth = int(args.depth)
    set_global_depth(depth)

    start_time = time.perf_counter()

    if args.load_from_pgn:
        logger.playing("Loading game from PGN:")
        PGN = args.load_from_pgn
        board = chess.pgn.read_game(PGN)
    elif args.load_from_FEN:
        logger.playing("Loading game from FEN:")
        FEN = args.load_from_FEN
        board = chess.Board(FEN)
    else:
        board = chess.Board()
  

    if players_color != "only_bot":
        logger.playing("Welcome to Obi-Pawn Kenobot! Let's play.")
        logger.playing("You are playing as " + ("White" if players_color == chess.WHITE else "Black"))
    elif players_color == "only_bot":
        logger.playing("Welcome to Obi-Pawn Kenobot! I am playing against myself.")
        

    #PGN
    game, node = create_pgn_game_and_node(players_color, depth)

    if players_color == "only_bot" and args.selfplay_loop:
        logger.playing("Obi-Pawn Kenobot is playing against itself (loop mode).")
        while True:
            board = chess.Board()

            game, node = create_pgn_game_and_node(chess.WHITE, depth)

            while not board.is_game_over():
                logger.playing(f"\n{print_board_colored(board) if args.color else print_board_clean(board)}")

                move, eval = find_best_move(board, depth)
                logger.playing(f"{"White" if board.turn else "Black"} plays: {board.san(move)}")
                logger.info(f"Bot chose {board.san(move)} / {move} from {len(list(board.legal_moves))} legal options. Score: {eval}")
                board.push(move)
                node = node.add_variation(move)

            log_result(board)
            add_game_result_to_pgn_and_write_pgn(game, board, players_color, start_time)

            logger.info("Game finished and appended to PGN. Starting new game...\n")
            reset_total_counters()
            

    elif players_color == "only_bot":
        logger.playing("Obi-Pawn Kenobot is playing against itself.")
        while not board.is_game_over():
            logger.playing(f"\n{print_board_colored(board) if args.color else print_board_clean(board)}")

            move, eval = find_best_move(board, depth)
            logger.playing(f"{"White" if board.turn else "Black"}  plays: {board.san(move)}")
            logger.info(f"Bot chose {board.san(move)} / {move} from {len(list(board.legal_moves))} legal options. It gave the move a score of {eval}")
            board.push(move)
            node = node.add_variation(move)

            if board.is_game_over():
                log_result(board)
                add_game_result_to_pgn_and_write_pgn(game, board, players_color, start_time)
                break
        
    else:
        while not board.is_game_over():
            logger.playing(f"\n{print_board_colored(board) if args.color else print_board_clean(board)}")

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
                logger.playing(f"Obi-Pawn plays: {move}")
                logger.info(f"Bot chose {board.san(move)} / {move} from {len(list(board.legal_moves))} legal options. It gave the move a score of {eval}")
                board.push(move)
                node = node.add_variation(move)
    
    log_result(board)

    add_game_result_to_pgn_and_write_pgn(game, board, players_color, start_time)

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    logger.info(f"Total elapsed time: {elapsed_time:.2f} seconds")


    


if __name__ == "__main__":
    main()
