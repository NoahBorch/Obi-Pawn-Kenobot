

debug_config = {
    "evaluation": True,
    "search": True,
    "move_ordering" : False,
    "counters": False,
    "logging": False,
    "main": False,
    "PST": True,
}





def set_no_debug():
    """
    Disable all debug configurations.
    """
    global debug_config
    for key in debug_config.keys():
        debug_config[key] = False



def set_debug_config_for_module(module, enabled = True):
    """
    Set the debug configuration for the application.
    
    Parameters:
    - config (dict): A dictionary containing the debug configuration.
    
    Returns:
    - None
    """
    global debug_config
    debug_config[module] = enabled

def get_debug_config():
    """
    Get the current debug configuration.
    
    Returns:
    - dict: The current debug configuration.
    """
    return debug_config

def get_debug_config(module):
    """
    Check if debugging is enabled for a specific module.
    
    Parameters:
    - module (str): The name of the module to check.
    
    Returns:
    - bool: True if debugging is enabled for the module, False otherwise.
    """
    return debug_config[module]