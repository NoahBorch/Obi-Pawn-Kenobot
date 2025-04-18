
import sys
import chess
import time
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]  # this is src/python
sys.path.insert(0, str(project_root))

from lichess_integration.play import play_board
from utils.log import logger, configure_logging
from ui.terminal_prints import print_board_clean

board = chess.Board()
configure_logging("debug", save_to_file=True, logdir="../../.logs/games", category="uci")
using_movetime = False

def uci_loop():
    logger.playing("Starting UCI loop...")
    # logger.debug(f"printing: \nid name Obi-Pawn-Kenobot\nid author noahborch\nuciok")
    # print("id name Obi-Pawn-Kenobot")
    # print("id author noahborch")
    # print("uciok")

    while True:
        try:
            line = input().strip()
            logger.debug(f"Received command: {line}")
        except EOFError:
            break

        if line == "uci":
            print("id name Obi-Pawn-Kenobot")
            print("id author noahborch")
            print("uciok")

        elif line == "isready":
            print("readyok")

        elif line.startswith("position"):
            parts = line.split(" ", 2)
            if parts[1] == "startpos":
                board.reset()
                if len(parts) > 2 and parts[2].startswith("moves"):
                    for move in parts[2][6:].split():
                        board.push_uci(move)
            elif parts[1] == "fen":
                fen = parts[2].split(" moves")[0]
                board.set_fen(fen)
                if "moves" in parts[2]:
                    moves = parts[2].split("moves")[1].strip().split()
                    for move in moves:
                        board.push_uci(move)
            # logger.info(f"Position set to:\n\n{print_board_clean(board)}")

        elif line.startswith("go"):
            tokens = line.split()
            movetime = None
            wtime = btime = winc = binc = 0
            for i in range(len(tokens)):
                if tokens[i] == "movetime":
                    movetime = int(tokens[i + 1]) / 1000 
                elif tokens[i] == "wtime":
                    wtime = int(tokens[i + 1]) / 1000
                elif tokens[i] == "btime":
                    btime = int(tokens[i + 1]) / 1000
                elif tokens[i] == "winc":
                    winc = int(tokens[i + 1]) / 1000
                elif tokens[i] == "binc":
                    binc = int(tokens[i + 1]) / 1000

            if movetime:
                if board.fullmove_number > 2:
                    total_time_left = movetime
                    using_movetime = True
                    increment = 0
                else:
                    total_time_left = movetime//40
                    increment = 0
                    using_movetime = True
            else:
                using_movetime = False
                if board.turn:
                    total_time_left = wtime  
                    increment = winc
                else:
                    total_time_left = btime
                    increment = binc
           
            logger.info(f"Calculating move with time left: {total_time_left}, increment: {increment}")
            logger.info(f"Current board position:\n{print_board_clean(board)}")
            

            try:
                move = play_board(board, total_time_left, increment, using_movetime)
                logger.info(f"Best move: {move}")
                print(f"bestmove {move}")
                logger.debug(f"Best move sent: {move}")
                board.push_uci(move)
                logger.info(f"New board position:\n{print_board_clean(board)}")
                sys.stdout.flush()
            except Exception as e:
                import traceback
                logger.error("Exception during move calculation:")
                logger.error(traceback.format_exc())
                print("bestmove 0000")  
                sys.stdout.flush()

            
            

        elif line == "quit":
            break

if __name__ == "__main__":
    uci_loop()
