# scripts/logger.py

import logging
import os

class Logger:
    def __init__(self, log_file='../yolo_training.log', name='yolo_pipeline'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

        # Create handlers
        file_handler = logging.FileHandler(log_file)
        console_handler = logging.StreamHandler()

        # Create formatters and add them to handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add handlers to the logger
        if not self.logger.handlers: # Prevent adding handlers multiple times
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def debug(self, message):
        self.logger.debug(message)