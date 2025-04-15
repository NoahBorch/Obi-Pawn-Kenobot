
#search.py
import time
import chess

from engine.evaluation.evaluation import evaluate_position, MVV_LVA, add_check_bonus, CHECKMATE_BASE_SCORE
from ui.terminal_prints import print_board_clean
from utils.counters import update_total_counters
from utils.log import logger
from utils.debug_config import debug_config, get_debug_config
from utils.config import get_global_depth, set_global_depth, get_iterative_deepening, get_iterative_depth, set_iterative_depth, get_qDepth


GLOBAL_DEPTH = get_global_depth()
qDepth = get_qDepth()
try:
    global_depth = get_global_depth()
except ValueError:
    logger.error("Global depth not set. Using default value of 3.")
    global_depth = 3

debug_search = get_debug_config("search")
debug_move_ordering = get_debug_config("move_ordering")



def order_moves(board, quiescence=False):
    all_moves = list(board.legal_moves)
    check_bonus = 100
    # Sort moves by their type
    checkmates = []
    promotions = []
    captures = []
    checks = []
    non_captures = []
    for move in all_moves:
        # board.push(move)
        # if board.is_checkmate():
        #     checkmates.append(move)
        # board.pop()
        if move.promotion:
            promotions.append(move)
        elif board.gives_check(move):
            board.push(move)
            if board.is_checkmate():
                checkmates.append(move)
                board.pop()
                return checkmates
            else: checks.append(move)
            board.pop()
        elif board.is_capture(move):
            captures.append(move)
        else:
            non_captures.append(move)
        
    if debug_move_ordering and checkmates: 
        logger.debug(f"Found {len(checkmates)} checkmate move(s): {checkmates}")

    if debug_move_ordering:
        logger.debug(f"Ordering moves: {len(promotions)} promotions, {len(captures)} captures, {len(checks)} checks, {len(non_captures)} non-captures")
        logger.debug(f"Promotions: {len(promotions)}, Captures: {len(captures)}, Checks: {len(checks)}, Non-captures: {len(non_captures)}")
        logger.debug(f"All captures: {captures}")

    #Sort captures by MVV - LVA
    captures.sort(key=lambda x: MVV_LVA(board, x) + add_check_bonus(board,x,check_bonus), reverse=True)
    
    if quiescence:
        return checkmates + promotions + captures + checks 
    return checkmates + promotions + captures + checks + non_captures

        
def is_quiet(board):
    #NO LONGER USED
    for move in board.legal_moves:
        if board.is_capture(move) or board.gives_check(move) or move.promotion:
            return False
    return True


def quiescence_search(board, qDepth, alpha, beta):
    
    """
    Perform a quiescence search on the given board.

    A quiescence search is a search of the most relevant moves, which are moves that are captures, checks, or promotions.
    This search is used to extend the search tree beyond the horizon of the main search, by searching all possible captures until there are no more captures left.
    This helps to reduce the horizon effect, which is the problem of not seeing the consequences of a move far enough into the future.

    :param board: The board to search
    :param alpha: The alpha value for alpha-beta pruning
    :param beta: The beta value for alpha-beta pruning
    :return: The best evaluation score of all possible moves
    """
    max_eval = evaluate_position(board)

    if board.outcome() or qDepth == 0:
        if max_eval == CHECKMATE_BASE_SCORE:
            return CHECKMATE_BASE_SCORE + qDepth
        elif max_eval == -CHECKMATE_BASE_SCORE:
            return -CHECKMATE_BASE_SCORE - qDepth
        return max_eval
    elif (board.can_claim_threefold_repetition() or board.can_claim_fifty_moves()):
        return -1
    if max_eval >= beta:
        return beta
    if max_eval > alpha:
        alpha = max_eval

    local_positions_evaluated = 0
    local_lines_pruned = 0
    for move in order_moves(board, quiescence=True):
        local_positions_evaluated += 1
        board.push(move)
        eval = -quiescence_search(board, qDepth - 1 , -beta, -alpha)
        board.pop()
        if eval == CHECKMATE_BASE_SCORE:
            update_total_counters(local_positions_evaluated, local_lines_pruned, reset_ply=False)
            return CHECKMATE_BASE_SCORE + qDepth
        elif eval == -CHECKMATE_BASE_SCORE:
            update_total_counters(local_positions_evaluated, local_lines_pruned, reset_ply=False)
            return -CHECKMATE_BASE_SCORE - qDepth

        if eval > max_eval:
            max_eval = eval
        alpha = max(alpha, eval)
        if alpha >= beta:
            local_lines_pruned += 1
            break 

    update_total_counters(local_positions_evaluated, local_lines_pruned, reset_ply=False)
    return max_eval
        




def negamax_alpha_beta(board, depth, alpha= -float('inf'), beta = float('inf'), return_move_evals=False):
    """
    New Negamax alpha beta search function, using the python chess board object. This function is the old negamax function, 
    but changed to work with my new chess bot. It uses the python chess board object and the evaluate_position function.
    :param board: The chess board, currently uses the python chess board object
    :param depth: The depth to search
    :param alpha: The alpha value for alpha beta pruning
    :param beta: The beta value for alpha beta pruning
    :return: The evaluation score of the best move
    """

    
    if board.outcome():
        return evaluate_position(board)
    elif (board.can_claim_threefold_repetition() or board.can_claim_fifty_moves()):
        return -1
    
    elif depth == 0:
        return quiescence_search(board, qDepth, alpha, beta)
    
    ordered_moves = order_moves(board)
    max_eval = -float('inf')
    local_positions_evaluated = 0
    local_lines_pruned = 0
    if return_move_evals:
        move_evals = {}

    if debug_search:
        global_depth = get_global_depth()
        if depth == global_depth -1 :
            logger.debug(f"Evaluating position: \n{print_board_clean(board)}")
            logger.debug(f"Depth: {depth}, Alpha: {alpha}, Beta: {beta}")
            logger.debug(f"Legal moves: {[board.san(move) for move in ordered_moves]}")

    for move in ordered_moves:
        local_positions_evaluated += 1
        board.push(move)
        eval = -negamax_alpha_beta(board, depth - 1, -beta, -alpha)
        board.pop()

        if return_move_evals:
            move_evals[move] = eval

        if debug_search and depth == GLOBAL_DEPTH - 1:
            logger.debug(f"Evaluated move {board.san(move)} to score {eval}")
        
        if eval == CHECKMATE_BASE_SCORE:
            update_total_counters(local_positions_evaluated, local_lines_pruned, reset_ply=False)
            eval = CHECKMATE_BASE_SCORE + qDepth + depth
            if return_move_evals: return {move: eval}, -eval
            else: return eval
        if eval == -CHECKMATE_BASE_SCORE:
            eval = -CHECKMATE_BASE_SCORE - qDepth - depth
            if return_move_evals: return {move: eval}, -eval
            else: return eval
        
        if eval > max_eval:
            max_eval = eval
        alpha = max(alpha, eval)
        if alpha >= beta:
            local_lines_pruned += 1
            break 

    update_total_counters(local_positions_evaluated, local_lines_pruned, reset_ply=False)
    if return_move_evals: return move_evals, -max_eval
    return max_eval
  

def find_best_move(board, depth):
    global debug_search
    debug_search = get_debug_config("search")
    if not board.legal_moves:
        logger.info("No legal moves available.")
        return None, 0

    best_move = None
    local_positions_evaluated = 0
    local_lines_pruned = 0
    ordered_moves = order_moves(board)
    previous_move_evals = None
    for local_depth in range(2, depth + 1):
        set_iterative_depth(local_depth)
        max_eval = -float('inf')
        alpha = -float('inf')
        beta = float('inf')
        current_move_evals = {}

        if previous_move_evals:
            ordered_moves = dict(sorted(previous_move_evals.items(), key=lambda item: item[1], reverse=True)).keys()
        if debug_search:
            logger.debug(f"Searching depth {local_depth}")
            logger.debug(f"Current board: \n{print_board_clean(board)}")
            logger.debug(f"Alpha: {alpha}, Beta: {beta}")
            logger.debug(f" searching moves in order {[board.san(move) for move in ordered_moves]}")      
        
        for move in ordered_moves:
            if debug_search:
                move_search_time = time.perf_counter()
                logger.debug(f"Evaluating move: {board.san(move)}")
            local_positions_evaluated += 1
            board.push(move)
            if board.is_checkmate():
                board.pop()
                return move, CHECKMATE_BASE_SCORE + qDepth + GLOBAL_DEPTH
            eval = negamax_alpha_beta(board, local_depth - 1, -beta, -alpha, return_move_evals=False)
            board.pop()
            current_move_evals[move] = eval
            if debug_search:
                move_search_time = time.perf_counter() - move_search_time
                logger.debug(f"Move {board.san(move)} evaluated in {move_search_time:.4f} seconds")
                logger.debug(f"Evaluated move {board.san(move)} to score {eval}")

            if eval > max_eval:
                max_eval = eval
                best_move = move
                
            alpha = max(alpha, eval)
        previous_move_evals = current_move_evals
        if debug_search:
            logger.debug(f"Best move at depth {local_depth}: {board.san(best_move)} with evaluation {max_eval}")
            
    logger.info(f"Best move: {best_move}, Evaluation: {max_eval}")
    update_total_counters(local_positions_evaluated, local_lines_pruned, reset_ply=True)
    
    return best_move, max_eval



