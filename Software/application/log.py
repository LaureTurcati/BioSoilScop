import json
import os
from datetime import datetime
from dataclasses import dataclass

#LOG_FILE_PATH = "/home/pi/camtrap/test/logs.jsonl"
#DEBUG_LEVEL = 2
# 0: ERROR
# 1: INFO
# 2: DEBUG

@dataclass
class Logger:
    log_file: str
    max_level: int

    def _log(self, level, log_data):
        logs = []
        if level <= self.max_level:
            if os.path.exists(self.log_file):
                try:
                    with open(self.log_file, "r") as f:
                        logs = json.load(f)
                except json.JSONDecodeError:
                    logs = []
            log_data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logs.append(log_data)

            with open(self.log_file, "w") as f:
                json.dump(logs, f, indent=4)

    def error(self, log_data):
        # log_data["level"] = "ERROR"
        self._log(0, log_data)

    def info(self, log_data):
        self._log(1, log_data)    

    def debug(self, log_data):
        self._log(2, log_data)
    
    def change_log_file(self, new_log_file):
        self.log_file = new_log_file

    def change_log_level(self, new_log_level):
        self.max_level = new_log_level 

# variable globale
LOG = Logger("/tmp/camtrap.logs", 0)
