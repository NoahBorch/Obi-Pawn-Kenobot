#evaluation.py
import chess
from pathlib import Path
import sys

#Filepath shenanigans
project_root = Path(__file__).parent.parent.resolve()  # this is src/python
sys.path.insert(0, str(project_root))


from utils.log import logger
from utils.debug_config import get_debug_config
from utils.constants import CHECKMATE_BASE_SCORE, PHASE_OPENING, PHASE_MIDGAME, PHASE_ENDGAME, PIECE_VALUES, PIECE_TYPE_NAMES, PASSED_PAWN_BONUS_BY_RANK
from utils.game_phase import calculate_game_phase, get_last_logged_phase
from engine.evaluation.PSTs import get_piece_square_tables_by_phase
from ui.terminal_prints import print_board_clean



debug_evaluation = get_debug_config("evaluation")
debug_game_phase = get_debug_config("game_phase")
debug_PST = get_debug_config("PST")
last_logged_phase =  PHASE_OPENING



piece_value = PIECE_VALUES
piece_type_names = PIECE_TYPE_NAMES


piece_type_names = {
    chess.PAWN: "Pawn",
    chess.KNIGHT: "Knight",
    chess.BISHOP: "Bishop",
    chess.ROOK: "Rook",
    chess.QUEEN: "Queen",
    chess.KING: "King"
}

def set_last_logged_phase(phase):
    """
    Set the last logged phase of the game.
    :param phase: The phase to set.
    """
    global last_logged_phase
    last_logged_phase = phase
    if debug_evaluation or debug_game_phase:
        logger.debug(f"Game phase set to: {phase}")


def MVV_LVA(board, move):
    """
    MVV-LVA (Most Valuable Victim - Least Valuable Aggressor) is a heuristic used in chess engines to order captures.
    It prioritizes capturing the most valuable piece of the opponent with the least valuable piece of the player.
    :param board: The chess board, currently uses the python chess board object
    :param move: The move to be evaluated
    :return: A score representing the evaluation of the move.
    """
    if not board.is_capture(move):
        logger.warning("Move is not a capture")
        return 0

    aggressor = board.piece_at(move.from_square)

    # Handle en passant
    if board.is_en_passant(move):
        offset = -8 if board.turn == chess.WHITE else 8
        target_square = move.to_square + offset
    else:
        target_square = move.to_square

    victim = board.piece_at(target_square)

    if victim is None or aggressor is None:
        logger.critical("Target or aggressor piece is None")
        logger.debug(f"Current board: \n{board}")
        logger.debug(f"Evaluating move: {move}, in algebraic notation: {board.san(move)}")
        logger.debug(f"From square: {move.from_square}, To square: {move.to_square}")
        logger.debug(f"Aggressor: {aggressor}, Victim: {victim}")
        return 0

    return piece_value[victim.piece_type] - piece_value[aggressor.piece_type]

def add_check_bonus(board, move, check_bonus=20):
    """
    Add a bonus for moves that give check.
    :param board: The chess board, currently uses the python chess board object
    :param move: The move to be evaluated
    :return: A score representing the evaluation of the move.
    """
    if board.gives_check(move):
        return check_bonus
    return 0


def count_material(board):
    white_material_score = 0
    black_material_score = 0
    white_pawn_material_score = 0
    black_pawn_material_score = 0
    for square, piece in board.piece_map().items():
        if piece.color:
            white_material_score += piece_value[piece.piece_type]
            if piece.piece_type == chess.PAWN:
                white_pawn_material_score += 100
        else:
            black_material_score += piece_value[piece.piece_type]
            if piece.piece_type == chess.PAWN:
                black_pawn_material_score += 100
    if debug_evaluation:
        logger.debug(f"material count score: {white_material_score - black_material_score}")
        logger.debug(f"white material no pawns score: {white_material_score-white_pawn_material_score}")
        logger.debug(f"black material no pawns score: {black_material_score-black_pawn_material_score}")
  
    return (white_material_score - black_material_score), (white_material_score-white_pawn_material_score), (black_material_score-black_pawn_material_score)

def count_material_no_pawns(board):
    """
    Count the material on the board excluding pawns.
    :param board: The chess board, currently uses the python chess board object
    :return: A tuple containing the material count for white and black without pawns.
    """
    white_material_score = 0
    black_material_score = 0
    for square, piece in board.piece_map().items():
        if piece.piece_type == chess.PAWN:
            continue
        elif piece.color:
            white_material_score += piece_value[piece.piece_type]
        else:
            black_material_score += piece_value[piece.piece_type]
    return (white_material_score - black_material_score), (white_material_score), (black_material_score)

def count_opponents_material_no_pawns(board):
    """
    Count the opponent's material on the board excluding pawns.
    :param board: The chess board, currently uses the python chess board object
    :return: A tuple containing the material count for the opponent without pawns.
    """
    opponents_material_score = 0
    for square, piece in board.piece_map().items():
        if piece.piece_type == chess.PAWN:
            continue
        elif piece.color != board.turn:
            opponents_material_score += piece_value[piece.piece_type]
    return opponents_material_score
        



def add_piece_square_table_bonuses(board):
    """
    Add bonuses for piece-square tables.
    :param board: The chess board, currently uses the python chess board object
    :param opponent_material_count_without_pawns: The material count of the opponent without pawns
    :return: A score representing the evaluation of the position.
    """
   
    all_pieces = board.piece_map().items()
    current_eval = 0

    phase = get_last_logged_phase()
    
    PIECE_SQUARE_TABLES = get_piece_square_tables_by_phase(phase)

    if debug_PST:
        white_piece_scores = {}
        black_piece_scores = {}
        piece_scores_by_square = [0]*64
       


    for square, piece in all_pieces:
        if piece.color:
            current_eval += PIECE_SQUARE_TABLES[piece.piece_type][square]
            if debug_PST:
                score = PIECE_SQUARE_TABLES[piece.piece_type][square]
                white_piece_scores[piece_type_names[piece.piece_type]] = white_piece_scores.get(piece_type_names[piece.piece_type], 0) + score
                piece_scores_by_square[square] += score

        else:
            if debug_PST:
                score = PIECE_SQUARE_TABLES[piece.piece_type][chess.square_mirror(square)]
                black_piece_scores[piece_type_names[piece.piece_type]] = black_piece_scores.get(piece_type_names[piece.piece_type], 0) + score
                piece_scores_by_square[square] -= score
            current_eval -= PIECE_SQUARE_TABLES[piece.piece_type][chess.square_mirror(square)]
                
    if debug_PST:
        logger.debug(f"Current PST score: {current_eval}")
        logger.debug(f"White piece scores: {white_piece_scores}")
        logger.debug(f"Black piece scores: {black_piece_scores}")
        for i in range(8, 0, -1):
            row = " ".join(f"{piece_scores_by_square[j + (i - 1) * 8]:>4}" for j in range(8))
            logger.debug(f"row {i}: {row}")
            

    return current_eval

def endgame_incentives(board):
    white_king_square = board.king(chess.WHITE)
    black_king_square = board.king(chess.BLACK)
    distance_between_kings = chess.square_distance(white_king_square, black_king_square)
    bonus = 50 - distance_between_kings
    return bonus 

def check_if_pawn_is_passed(color, pawn, furthest_back_different_colored_pawn_positions_by_file):
    file = chess.square_file(pawn)
    rank = chess.square_rank(pawn)  
    if color == chess.WHITE:
        black_furthest_back_pawn_positions_by_file = furthest_back_different_colored_pawn_positions_by_file
        if file == 0:
            if black_furthest_back_pawn_positions_by_file[1] <= rank:
                return True
        elif file == 7:
            if black_furthest_back_pawn_positions_by_file[6] <= rank:
                return True
        else:
            if black_furthest_back_pawn_positions_by_file[file - 1] <= rank or black_furthest_back_pawn_positions_by_file[file + 1] <= rank:
                return True
        return False
    else:
        white_furthest_back_pawn_positions_by_file = furthest_back_different_colored_pawn_positions_by_file
        if file == 0:
            if white_furthest_back_pawn_positions_by_file[1] >= rank:
                return True
        elif file == 7:
            if white_furthest_back_pawn_positions_by_file[6] >= rank:
                return True
        else:
            if white_furthest_back_pawn_positions_by_file[file - 1] >= rank or white_furthest_back_pawn_positions_by_file[file + 1] >= rank:
                return True
        return False

def check_if_pawn_is_connected_passer(color, pawn, same_color_passed_pawns, same_color_furthest_back_pawn_position_by_file, right_file_has_pawn, left_file_has_pawn, files_with_same_color_doubled_pawns, same_color_pawns):
    """
    Check if a pawn is a connected passer.

    A connected passer is a passed pawn that has a neighboring pawn on an adjacent file
    that is also a passed pawn. This function checks for such a condition for a given pawn.

    :param color: The color of the pawn being evaluated (chess.WHITE or chess.BLACK).
    :param pawn: The square index of the pawn being evaluated. It is assumed to be a passed pawn.
    :param same_color_passed_pawns: A set of passed pawns of the same color.
    :param same_color_furthest_back_pawn_position_by_file: A list indicating the furthest back
           same-colored pawn position by file.
    :param right_file_has_pawn: Boolean indicating if there is a pawn on the right file.
    :param left_file_has_pawn: Boolean indicating if there is a pawn on the left file.
    :param files_with_same_color_doubled_pawns: A set of files where there are doubled pawns
           of the same color.
    :param same_color_pawns: A set of all pawns of the same color on the board.

    :return: True if the pawn is a connected passer, otherwise False.
    """

    file = chess.square_file(pawn)
    rank = chess.square_rank(pawn)
    if color == chess.WHITE:

        if left_file_has_pawn:
            if file - 1 in files_with_same_color_doubled_pawns:
                for square in same_color_pawns:
                    if chess.square_file(square) == file - 1:
                        if chess.square_rank(square) > rank:
                            if check_if_pawn_is_passed(chess.WHITE, square, same_color_furthest_back_pawn_position_by_file):
                                return True
                        elif square in same_color_passed_pawns:
                            return True
                          
            else:
                left_neighboring_pawn = same_color_furthest_back_pawn_position_by_file[file - 1]
                if left_neighboring_pawn in same_color_passed_pawns:
                    return True
            
        if right_file_has_pawn:
            if file + 1 in files_with_same_color_doubled_pawns:
                for square in same_color_pawns:
                    if chess.square_file(square) == file + 1:
                        if chess.square_rank(square) > rank:
                            if check_if_pawn_is_passed(chess.WHITE, square, same_color_furthest_back_pawn_position_by_file):
                                return True
                        elif square in same_color_passed_pawns:
                            return True
            else:
                right_neighboring_pawn = same_color_furthest_back_pawn_position_by_file[file + 1]
                if right_neighboring_pawn in same_color_passed_pawns:
                    return True
                
    else:
        return False
        
            


            
        
        

def add_pawn_structure_bonus(board):
    """
    TODO:
    Add bonus for passed pawns
    Add bonus for connected passed pawns
    Implenented:
    Add bonus for pawn chains
    Add penalty for backward pawns
    Add penalty for isolated pawns
    Add penalty for doubled pawns
    Add penalty for pawn islands
    """

    # Initialize penalties
    ISOLATED_PAWN_PENALTY = - 15
    DOUBLED_PAWN_PENALTY = - 20
    BACKWARD_PAWN_PENALTY = - 20
    PAWN_ISLAND_PENALTY = - 10
    

    PAWN_CHAIN_BASE_BONUS = 10
    PAWN_CHAIN_HEAD_BONUS = 5

    game_phase = calculate_game_phase(board)


    white_pawn_structure = 0
    black_pawn_structure = 0
    white_pawns = list(board.pieces(chess.PAWN, chess.WHITE))
    black_pawns = list(board.pieces(chess.PAWN, chess.BLACK))
    white_pawns.sort()
    black_pawns.sort(reverse=True)
  
    squares_protected_by_white_pawns = set()
    squares_protected_by_black_pawns = set()
    
    white_furthest_back_pawn_positions_by_file = [8 for i in range(8)]
    black_furthest_back_pawn_positions_by_file = [0 for i in range(8)]
    
    protected_white_pawns = set()
    protected_black_pawns = set()

    files_with_doubled_white_pawns = set()
    files_with_doubled_black_pawns = set()

    passed_white_pawns = set()
    passed_black_pawns = set()
    connected_passed_white_pawns = set()
    connected_passed_black_pawns = set()
    protected_passed_white_pawns = set()
    protected_passed_black_pawns = set()
    
    for square in white_pawns:
        file = chess.square_file(square)
        if white_furthest_back_pawn_positions_by_file[file] > chess.square_rank(square):
            white_furthest_back_pawn_positions_by_file[file] = chess.square_rank(square)
        squares_protected_by_white_pawns.add(board.attacks(square))

    for square in black_pawns:
        file = chess.square_file(square)
        if black_furthest_back_pawn_positions_by_file[file] < chess.square_rank(square):
            black_furthest_back_pawn_positions_by_file[file] = chess.square_rank(square)
        squares_protected_by_black_pawns.add(board.attacks(square))

    for pawn in white_pawns:
        # Check for doubled pawns 
        file = chess.square_file(pawn)
        rank = chess.square_rank(pawn)  
        if white_furthest_back_pawn_positions_by_file[file] != rank:
            white_pawn_structure += DOUBLED_PAWN_PENALTY
            files_with_doubled_white_pawns.add(file)
        
        #Check for isolated pawns and pawn islands
        if file == 0:
            if white_furthest_back_pawn_positions_by_file[1] == 8:
                white_pawn_structure += ISOLATED_PAWN_PENALTY
                white_pawn_structure += PAWN_ISLAND_PENALTY
        elif file == 7:
            if white_furthest_back_pawn_positions_by_file[6] == 8:
                white_pawn_structure += ISOLATED_PAWN_PENALTY
                white_pawn_structure += PAWN_ISLAND_PENALTY
        else:
            left_file_has_pawn = (white_furthest_back_pawn_positions_by_file[file - 1] == 8)
            right_file_has_pawn = (white_furthest_back_pawn_positions_by_file[file + 1] == 8)
            if left_file_has_pawn and right_file_has_pawn:
                white_pawn_structure += ISOLATED_PAWN_PENALTY
                white_pawn_structure += PAWN_ISLAND_PENALTY
            elif left_file_has_pawn:
                white_pawn_structure += PAWN_ISLAND_PENALTY
        
        # Check for backward pawns
        can_be_protected = False
        if file == 0:
            if white_furthest_back_pawn_positions_by_file[1] <= rank:
                can_be_protected = True
        elif file == 7:
            if white_furthest_back_pawn_positions_by_file[6] <= rank:
                can_be_protected = True
        else:
            if white_furthest_back_pawn_positions_by_file[file - 1] <= rank or white_furthest_back_pawn_positions_by_file[file + 1] <= rank:
                can_be_protected = True
        if can_be_protected:
            #if square in front of pawn is protected by an enemy pawn
            if pawn + 8 in squares_protected_by_black_pawns:
                #if any enemy pawns are in front of the pawn
                if black_furthest_back_pawn_positions_by_file[file] > rank:
                    white_pawn_structure += BACKWARD_PAWN_PENALTY

        # Check for pawn chains
        is_protected = False
        if file == 0:
            if pawn - 7 in white_pawns:
                is_protected = True
                protected_white_pawns.add(pawn)
                white_pawn_structure += PAWN_CHAIN_BASE_BONUS
                if pawn - 7 in protected_white_pawns:
                    white_pawn_structure += PAWN_CHAIN_HEAD_BONUS
                
        elif file == 7:
            if pawn - 9 in white_pawns:
                is_protected = True
                protected_white_pawns.add(pawn)
                white_pawn_structure += PAWN_CHAIN_BASE_BONUS
                if pawn - 9 in protected_white_pawns:
                    white_pawn_structure += PAWN_CHAIN_HEAD_BONUS
        else:
            if pawn - 9 in white_pawns:
                is_protected = True
                protected_white_pawns.add(pawn)
                white_pawn_structure += PAWN_CHAIN_BASE_BONUS
                if pawn - 9 in protected_white_pawns:
                    white_pawn_structure += PAWN_CHAIN_HEAD_BONUS

            if pawn - 7 in white_pawns:
                is_protected = True
                protected_white_pawns.add(pawn)
                white_pawn_structure += PAWN_CHAIN_BASE_BONUS
                if pawn - 7 in protected_white_pawns:
                    white_pawn_structure += PAWN_CHAIN_HEAD_BONUS

        # Check for passed pawns
        if check_if_pawn_is_passed(pawn, black_furthest_back_pawn_positions_by_file, white_furthest_back_pawn_positions_by_file):
            passed_white_pawns.add(pawn)
            # Check if pawn is protected passer 
            if is_protected:
                protected_passed_white_pawns.add(pawn)
        
        
        # Check if pawn is connected passer
        if check_if_pawn_is_connected_passer(chess.WHITE, pawn, passed_white_pawns, white_furthest_back_pawn_positions_by_file, right_file_has_pawn, left_file_has_pawn, files_with_doubled_white_pawns, white_pawns):
            connected_passed_white_pawns.add(pawn)

        for pawn in passed_white_pawns:
            rank = chess.square_rank(pawn)
            bonus = PASSED_PAWN_BONUS_BY_RANK[rank]
            
            if pawn in protected_passed_white_pawns and pawn in connected_passed_white_pawns:
                bonus *= 2.5
            elif pawn in protected_passed_white_pawns:
                bonus *= 1.5
            elif pawn in connected_passed_white_pawns:
                bonus *= 2
            if game_phase != PHASE_ENDGAME:
                bonus *= 0.75
            white_pawn_structure += bonus


            








                
                    


        
            

            



    

    


def evaluate_position(board):
    """
    Evaluate the position of the board for the given color.
    :param board: The chess board, currently uses the python chess board object
    :return: A score representing the evaluation of the position.
    """
    global debug_evaluation
    global last_logged_phase
    turn = board.turn
    if debug_evaluation:
        logger.debug(f"Evaluating position for {'white' if not turn else 'black'}")
        logger.debug(f"Current board: \n{print_board_clean(board)}")
        logger.debug(f"Current phase: {last_logged_phase}")
        
    if board.outcome():
        if board.is_checkmate():
            if debug_evaluation:
                try:
                    logger.debug(f"Checkmate detected for moving player: {turn}, in position: \n{print_board_clean(board)} after player plays {board.peek()}")
                except Exception as e:
                    logger.error(f"Error while logging checkmate position: {e}")
            return -CHECKMATE_BASE_SCORE
        else:
            return 0
    else:
        current_eval = 0
        material_eval_score, white_material_count_no_pawns, black_material_count_no_pawns = count_material(board)
        current_eval += material_eval_score
        PST_eval_score = add_piece_square_table_bonuses(board)

        current_eval += PST_eval_score

        if last_logged_phase == PHASE_ENDGAME:
            current_eval += endgame_incentives(board)

        if debug_evaluation:
            logger.debug(f"Current evaluation score: {current_eval if turn else -current_eval}")
            logger.debug(f"Material evaluation score: {material_eval_score}")
            logger.debug(f"Piece square table evaluation score: {PST_eval_score}")
            if last_logged_phase == PHASE_ENDGAME:
                logger.debug(f"Endgame evaluation score: {endgame_incentives(board)}")
            logger.debug(f"Board state: \n{print_board_clean(board)}")
        return current_eval if turn else -current_eval
    
