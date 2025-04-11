
import chess

# ANSI escape codes
RESET = "\033[0m"
WHITE_PIECE = "\033[97m"  # Bright white
BLACK_PIECE = "\033[30m"  # Bright black
LIGHT_SQUARE = "\033[48;5;180m"  # light tan
DARK_SQUARE = "\033[48;5;94m"    # medium brown


UNICODE_PIECES = {
    (chess.PAWN, False):   '♙',
    (chess.KNIGHT, False): '♘',
    (chess.BISHOP, False): '♗',
    (chess.ROOK, False):   '♖',
    (chess.QUEEN, False):  '♕',
    (chess.KING, False):   '♔',
    (chess.PAWN, True):    '♟',
    (chess.KNIGHT, True):  '♞',
    (chess.BISHOP, True):  '♝',
    (chess.ROOK, True):    '♜',
    (chess.QUEEN, True):   '♛',
    (chess.KING, True):    '♚',
}

def colored_square(square, piece):
    is_light = (chess.square_rank(square) + chess.square_file(square)) % 2 == 0
    bg_color = LIGHT_SQUARE if is_light else DARK_SQUARE
    if piece:
        symbol = UNICODE_PIECES[(piece.piece_type, True)]
        fg_color = WHITE_PIECE if piece.color == chess.WHITE else BLACK_PIECE
        return f"{bg_color} {fg_color}{symbol} {RESET}"
    else:
        return f"{bg_color}   {RESET}"

def print_board_colored(board: chess.Board) -> str:
    piece_map = board.piece_map()
    rows = []
    for rank in range(8, 0, -1):
        row = f"{rank} "
        for file in range(8):
            square = chess.square(file, rank - 1)
            piece = piece_map.get(square)
            row += colored_square(square, piece) + " "
        rows.append(row + RESET)
    footer = "   " + "   ".join("abcdefgh")
    return "\n".join(rows) + "\n" + footer

def print_board_clean(board: chess.Board) -> str:
    piece_map = board.piece_map()
    rows = []
    for rank in range(8, 0, -1):
        row = []
        for file in range(8):
            square = chess.square(file, rank - 1)
            piece = piece_map.get(square)
            if piece:
                row.append(UNICODE_PIECES[(piece.piece_type, piece.color)])
            else:
                row.append('.')
        rows.append(f"{rank}{' '.join(row)}")
    board_str = "\n".join(rows)
    board_str += "\n a b c d e f g h"
    return board_str