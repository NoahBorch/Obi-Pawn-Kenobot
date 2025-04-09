

import chess



def count_material(board):
    material_score = 0
    piece_value = {
        chess.PAWN: 100,
        chess.KNIGHT: 300,
        chess.BISHOP: 320,
        chess.ROOK: 500,
        chess.QUEEN: 900,
        chess.KING: 0,
    }
    for square, piece in board.piece_map().items():
        if piece.color:
            material_score += piece_value[piece.piece_type]
        else:
            material_score -= piece_value[piece.piece_type]
    return material_score


def evaluate_position(board):
    """
    Evaluate the position of the board for the given color.
    :param board: The chess board, currently uses the python chess board object
    :param color: The color whos turn it is to move
    :return: A score representing the evaluation of the position.
    """
    return count_material(board)