import logging
import os

def setup_logger():
    logs_dir = './logs'
    os.makedirs(logs_dir, exist_ok=True)
    logging.basicConfig(
        filename=os.path.join(logs_dir, 'scan.log'),
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

# Initialize the logger and expose a simple log() function
logger = setup_logger()

def log(message):
    print(f"[LOG] {message}")    # Optional: console output
    logger.info(message)
