
from utils.log import logger

total_positions_evaluated = 0
total_lines_pruned = 0
curent_ply_positions_evaluated = 0
curent_ply_lines_pruned = 0

def update_total_counters(positions_evaluated, lines_pruned, reset_ply=False):
    global total_positions_evaluated, total_lines_pruned, curent_ply_positions_evaluated, curent_ply_lines_pruned
    
    total_positions_evaluated += positions_evaluated
    total_lines_pruned += lines_pruned

    curent_ply_positions_evaluated += positions_evaluated
    curent_ply_lines_pruned += lines_pruned


    if reset_ply:
        logger.debug(f"Total positions evaluated: {total_positions_evaluated}, Total lines pruned: {total_lines_pruned}")
        logger.debug(f"Current ply positions evaluated: {curent_ply_positions_evaluated}, Current ply lines pruned: {curent_ply_lines_pruned}")
        logger.info(f"Positions evaluated to find this move: {curent_ply_positions_evaluated}, Lines pruned: {curent_ply_lines_pruned}")
        curent_ply_positions_evaluated = 0
        curent_ply_lines_pruned = 0
        
