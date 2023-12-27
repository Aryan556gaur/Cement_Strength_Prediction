from datetime import datetime
import os
import logging

Log_file = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
logs = os.path.join(os.getcwd(),"logs",Log_file)
os.makedirs(logs,exist_ok=True)

Log_file_path = os.path.join(logs,Log_file)

logging.basicConfig(
    filename=Log_file_path,
    format= "[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level= logging.INFO
)