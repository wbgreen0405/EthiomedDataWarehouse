# scripts/predict_images.py

import os
import subprocess
import sys

# Add project root to path for config and logger
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config
from scripts.logger import Logger

logger = Logger(log_file=config.LOG_FILE)

def predict_with_yolov5():
    """Runs YOLOv5 detection on the specified source directory."""
    logger.info("Starting YOLOv5 image prediction...")

    # Ensure the weights path exists. If training just finished, it might be in RUN_NAME + N
    # You might need a more robust way to get the exact run directory if RUN_NAME is not unique
    # For now, let's assume config.RUN_NAME is the exact folder name created
    actual_weights_path = os.path.join(config.YOLOV5_DIR, 'runs', 'train', config.RUN_NAME, 'weights', 'best.pt')
    if not os.path.exists(actual_weights_path):
        logger.error(f"Trained weights not found at {actual_weights_path}. Please check training output.")
        # Fallback to default if best.pt is not found in expected run_name
        # Or, you might want to explicitly pass the exact path after training
        logger.warning("Using default yolov5s.pt weights for prediction as trained weights were not found.")
        actual_weights_path = os.path.join(config.YOLOV5_DIR, config.WEIGHTS) # Use the base weights

    detect_script_path = os.path.join(config.YOLOV5_DIR, 'detect.py')

    command = [
        sys.executable,
        detect_script_path,
        '--weights', actual_weights_path,
        '--img', str(config.IMG_SIZE),
        '--conf', str(config.PREDICT_CONF_THRESHOLD),
        '--source', config.PREDICT_SOURCE_DIR,
        '--name', config.PREDICT_OUTPUT_NAME,
        '--save-conf', # To save confidence scores in the .txt files
        '--save-txt'   # To save labels in the .txt files
    ]

    logger.info(f"Executing prediction command: {' '.join(command)}")

    try:
        # Run from the yolov5 directory to handle relative paths correctly internally
        subprocess.run(command, cwd=config.YOLOV5_DIR, check=True)
        logger.info("YOLOv5 image prediction completed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Error during YOLOv5 prediction: {e}")
        logger.error(f"Stdout: {e.stdout.decode() if e.stdout else 'N/A'}")
        logger.error(f"Stderr: {e.stderr.decode() if e.stderr else 'N/A'}")
        return False
    except Exception as e:
        logger.error(f"An unexpected error occurred during prediction: {e}")
        return False

if __name__ == "__main__":
    logger.info("Starting image prediction process...")
    if predict_with_yolov5():
        logger.info("Image prediction successfully completed.")
    else:
        logger.error("Image prediction failed.")