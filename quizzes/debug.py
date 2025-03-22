"""
Debug logging module for quiz application.
Centralizes debug logging functionality.
"""

# Debug mode flag - default to False
DEBUG_MODE = False

def set_debug_mode(enabled=True):
    """
    Enable or disable debug mode globally.
    
    Args:
        enabled: True to enable debug logging, False to disable
    """
    global DEBUG_MODE
    DEBUG_MODE = enabled
    if enabled:
        print("[Debug] Debug mode enabled")
    
def is_debug_mode():
    """
    Check if debug mode is enabled.
    
    Returns:
        Boolean indicating if debug mode is enabled
    """
    return DEBUG_MODE
    
def log(module, message):
    """
    Print a debug log message if debug mode is enabled.
    
    Args:
        module: Name of the module logging the message
        message: Message to log
    """
    if DEBUG_MODE:
        print(f"[{module}] {message}") 