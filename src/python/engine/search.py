
import chess

from engine.evaluation import evaluate_position, MVV_LVA, add_check_bonus
from utils.counters import total_positions_evaluated, total_lines_pruned, curent_ply_positions_evaluated, curent_ply_lines_pruned, update_total_counters
from utils.log import logger


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

def order_moves(board):
    all_moves = list(board.legal_moves)
    check_bonus = 100
    # Sort moves by their type
    promotions = []
    captures = []
    checks = []
    non_captures = []
    for move in all_moves:
        if move.promotion:
            promotions.append(move)
        elif board.gives_check(move):
            checks.append(move)
        elif board.is_capture(move):
            captures.append(move)
        else:
            non_captures.append(move)

    #logger.debug(f"Promotions: {len(promotions)}, Captures: {len(captures)}, Checks: {len(checks)}, Non-captures: {len(non_captures)}")
    #logger.debug(f"All captures: {captures}")
    #Sort captures by MVV - LVA
    captures.sort(key=lambda x: MVV_LVA(board, x) + add_check_bonus(board,x,check_bonus), reverse=True)
    return promotions + captures + checks + non_captures

        

def negamax_alpha_beta(board, depth, alpha= -float('inf'), beta = float('inf')):
    """
    New Negamax alpha beta search function, using the python chess board object. This function is the old negamax function, 
    but changed to work with my new chess bot. It uses the python chess board object and the evaluate_position function.
    :param board: The chess board, currently uses the python chess board object
    :param depth: The depth to search
    :param alpha: The alpha value for alpha beta pruning
    :param beta: The beta value for alpha beta pruning
    :return: The evaluation score of the best move
    """

    
    if depth == 0 or board.outcome():
        return evaluate_position(board)
    
    ordered_moves = order_moves(board)
    max_eval = -float('inf')

    local_positions_evaluated = 0
    local_lines_pruned = 0
    for move in ordered_moves:
        local_positions_evaluated += 1
        board.push(move)
        eval = -negamax_alpha_beta(board, depth - 1, -beta, -alpha)
        board.pop()
        
        if eval > max_eval:
            max_eval = eval
        alpha = max(alpha, eval)
        if alpha >= beta:
            local_lines_pruned += 1
            break 

    update_total_counters(local_positions_evaluated, local_lines_pruned, reset_ply=False)
    return max_eval

def find_best_move(board, depth):
    if not board.legal_moves:
        logger.info("No legal moves available.")
        return None, 0

    best_move = None
    max_eval = -float('inf')
    alpha = -float('inf')
    beta = float('inf')
    local_positions_evaluated = 0
    local_lines_pruned = 0

    for move in order_moves(board):
        local_positions_evaluated += 1
        board.push(move)
        eval = -negamax_alpha_beta(board, depth - 1, -beta, -alpha)
        board.pop()

        if eval > max_eval:
            max_eval = eval
            best_move = move

        alpha = max(alpha, eval)
        if alpha >= beta:
            local_lines_pruned += 1
            break  
    logger.info(f"Best move: {best_move}, Evaluation: {max_eval}")
    update_total_counters(local_positions_evaluated, local_lines_pruned, reset_ply=True)
    
    return best_move, max_eval




