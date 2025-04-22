depth = 3
iterative_depth = 3
iterative_deepening = True
qDepth = depth // 2 + 2
qDepth_restricted = False
qDepth_removed = False

def set_global_depth(new_depth):
    global depth
    depth = new_depth

def get_global_depth():
    global depth
    return depth

def set_iterative_depth(new_depth):
    global iterative_depth
    iterative_depth = new_depth

def get_iterative_depth():
    global iterative_depth
    return iterative_depth

def set_iterative_deepening(enabled):
    global iterative_deepening
    iterative_deepening = enabled

def get_iterative_deepening():
    global iterative_deepening
    return iterative_deepening

def get_qDepth():
    global qDepth
    if qDepth_removed:
        return 0
    return qDepth if qDepth_restricted else 100

def set_qDepth_restricted(bool):
    global qDepth_restricted
    qDepth_restricted = bool

def set_qDepth_removed(bool):
    global qDepth_removed
    qDepth_removed = bool
