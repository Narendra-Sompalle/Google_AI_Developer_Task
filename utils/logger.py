"""
Logging utility module for the application.
Provides simple logging functionality.
"""

import logging
from datetime import datetime


def setup_logger(name: str = 'AI_Assistant') -> logging.Logger:
    """
    Setup and return a logger instance.
    
    Args:
        name (str): Logger name.
    
    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Create console handler
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    
    # Add handler to logger
    if not logger.handlers:
        logger.addHandler(handler)
    
    return logger


# Create a default logger instance
logger = setup_logger()
