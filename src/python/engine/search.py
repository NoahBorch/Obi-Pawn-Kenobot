
import chess

from engine.evaluation import evaluate_position


def select_single_move(board, color=chess.BLACK, best_move=None, best_eval=None):
    """
    Select a single move from the list of legal moves.
    :param board: The chess board, currently uses the python chess board object
    :return: A single move from the list of legal moves.
    """
    legal_moves = list(board.legal_moves)

    if color == chess.WHITE:
        if best_move is None:
            best_move = legal_moves[0]
            board.push(best_move)
            best_eval = evaluate_position(board)
            board.pop()
        for move in legal_moves:
            board.push(move)
            eval = evaluate_position(board)
            if eval > best_eval:
                best_eval = eval
                best_move = move
            board.pop()
    else:
        if best_move is None:
            best_move = legal_moves[0]
            board.push(best_move)
            best_eval = evaluate_position(board)
            board.pop()
        for move in legal_moves:
            board.push(move)
            eval = evaluate_position(board)
            if eval < best_eval:
                best_eval = eval
                best_move = move
            board.pop()
        
    return best_move

        