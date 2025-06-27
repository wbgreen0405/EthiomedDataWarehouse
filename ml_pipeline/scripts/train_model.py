# scripts/train_model.py

import os
import subprocess
import sys

# Add project root to path for config and logger
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config
from scripts.logger import Logger

logger = Logger(log_file=config.LOG_FILE)

def setup_yolov5_environment():
    """Clones YOLOv5 repo and installs its requirements."""
    if not os.path.exists(config.YOLOV5_DIR):
        logger.info(f"Cloning YOLOv5 repository into {config.YOLOV5_DIR}...")
        try:
            subprocess.run(['git', 'clone', config.YOLOV5_REPO_URL, config.YOLOV5_DIR], check=True)
            logger.info("YOLOv5 cloned successfully.")
        except subprocess.CalledProcessError as e:
            logger.error(f"Error cloning YOLOv5: {e}")
            return False
    else:
        logger.info(f"YOLOv5 directory already exists at {config.YOLOV5_DIR}. Skipping clone.")

    logger.info("Installing YOLOv5 requirements...")
    try:
        # Use sys.executable to ensure pip from the active venv is used
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', config.YOLOV5_REQUIREMENTS], check=True)
        logger.info("YOLOv5 requirements installed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Error installing YOLOv5 requirements: {e}")
        return False
    except FileNotFoundError:
        logger.error(f"pip or requirements.txt not found. Ensure Python and pip are in PATH and '{config.YOLOV5_REQUIREMENTS}' exists.")
        return False

def create_yolo_data_yaml():
    """Creates the data.yaml file required by YOLOv5 training."""
    data_yaml_content = f"""
path: {os.path.dirname(config.YOLO_DATA_YAML_PATH)} # Parent directory of train/val relative to yolov5/
train: {os.path.relpath(config.TRAIN_DIR, os.path.dirname(config.YOLO_DATA_YAML_PATH))} # Relative path to training images
val: {os.path.relpath(config.VAL_DIR, os.path.dirname(config.YOLO_DATA_YAML_PATH))} # Relative path to validation images

nc: {config.NUM_CLASSES}
names: {config.CLASS_NAMES}
"""
    try:
        with open(config.YOLO_DATA_YAML_PATH, 'w') as f:
            f.write(data_yaml_content)
        logger.info(f"YOLOv5 data YAML created at {config.YOLO_DATA_YAML_PATH}")
        return True
    except Exception as e:
        logger.error(f"Error creating YOLOv5 data YAML: {e}")
        return False

def train_yolov5_model():
    """Runs the YOLOv5 training command."""
    logger.info("Starting YOLOv5 model training...")
    try:
        # Construct the command to run train.py from inside the yolov5 directory
        train_script_path = os.path.join(config.YOLOV5_DIR, 'train.py')
        
        # Ensure data.yaml path is relative to the directory from where train.py is run (i.e., yolov5 dir)
        data_yaml_relative_path = os.path.relpath(config.YOLO_DATA_YAML_PATH, config.YOLOV5_DIR)

        command = [
            sys.executable, # Use the current Python executable
            train_script_path,
            '--img', str(config.IMG_SIZE),
            '--batch', str(config.BATCH_SIZE),
            '--epochs', str(config.EPOCHS),
            '--data', data_yaml_relative_path, # Path relative to YOLOv5_DIR
            '--weights', config.WEIGHTS,
            '--name', config.RUN_NAME
        ]
        
        logger.info(f"Executing training command: {' '.join(command)}")
        
        # Run from the yolov5 directory
        subprocess.run(command, cwd=config.YOLOV5_DIR, check=True)
        logger.info("YOLOv5 model training completed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Error during YOLOv5 training: {e}")
        logger.error(f"Stdout: {e.stdout.decode() if e.stdout else 'N/A'}")
        logger.error(f"Stderr: {e.stderr.decode() if e.stderr else 'N/A'}")
        return False
    except Exception as e:
        logger.error(f"An unexpected error occurred during training: {e}")
        return False

if __name__ == "__main__":
    logger.info("Starting model training process...")
    if setup_yolov5_environment():
        if create_yolo_data_yaml():
            if train_yolov5_model():
                logger.info("Model training successfully completed.")
            else:
                logger.error("Model training failed.")
        else:
            logger.error("YOLOv5 data YAML creation failed.")
    else:
        logger.error("YOLOv5 environment setup failed.")