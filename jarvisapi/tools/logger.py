from termcolor import colored
from colorama import init
from utils import current_path

import os

# Initialize colorama for windows
init()

levels = {
    "debug": {
        "color": "magenta"
    },
    "info": {
        "color": "cyan"
    },
    "warning": {
        "color": "yellow"
    },
    "error": {
        "color": "red"
    },
    "critical": {
        "color": "white",
        "on": "red"
    }
}

class Logger:
    def __init__(self, logging_file=current_path("main.log"), log_level=1, default_level=1, debug=False):
        self.logging_file = logging_file
        self.log_level = log_level
        self.debug = debug
        self.default_level = default_level

        if self.debug:
            self.log_level = 0
    
    def log(self, text, level=None, return_type="terminal"):
        if level is None:
            level = self.default_level
        
        if isinstance(level, str):
            level = list(levels.keys()).index(level)
        
        if level >= self.log_level:
            level_data = list(levels.values())[level]
            args = [str(text), level_data['color']]

            if "on" in list(level_data.keys()):
                args.append(f"on_{level_data['on']}")
            
            color = colored(*args)
            print(color)

            logging_file_text = f"{list(levels.keys())[level].upper()}: {text}"
            with open(self.logging_file, "a") as f:
                f.write(logging_file_text + "\n")

            if return_type == "file":
                return logging_file_text
            elif return_type == "terminal":
                return color
