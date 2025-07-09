"""
Logging utility for Pine Ridge test automation
"""

import logging
import sys
from datetime import datetime
from pathlib import Path


class Logger:
    """Centralized logging configuration"""
    
    _loggers = {}
    
    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:
        """Get or create a logger with the specified name"""
        
        if name not in cls._loggers:
            logger = logging.getLogger(name)
            logger.setLevel(logging.DEBUG)
            
            # Create console handler
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.INFO)
            
            # Create file handler
            log_dir = Path("logs")
            log_dir.mkdir(exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file = log_dir / f"pine_ridge_test_{timestamp}.log"
            
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.DEBUG)
            
            # Create formatters
            console_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
            )
            
            console_handler.setFormatter(console_formatter)
            file_handler.setFormatter(file_formatter)
            
            logger.addHandler(console_handler)
            logger.addHandler(file_handler)
            
            cls._loggers[name] = logger
        
        return cls._loggers[name]