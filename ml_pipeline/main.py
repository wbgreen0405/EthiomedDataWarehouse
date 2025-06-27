# main.py

import os
import sys
import subprocess

# Add scripts directory to Python path for module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'scripts')))

# Import config and logger (Logger is used indirectly via scripts)
import config
from scripts.logger import Logger

logger = Logger(log_file=config.LOG_FILE, name='YOLO_Pipeline_Main')

def run_script(script_path, script_name):
    """Helper function to run a Python script."""
    logger.info(f"--- Running {script_name} ---")
    try:
        # Use sys.executable to ensure the correct Python environment
        result = subprocess.run([sys.executable, script_path], check=True, capture_output=True, text=True)
        logger.info(f"{script_name} completed successfully.")
        if result.stdout:
            logger.info(f"stdout for {script_name}:\n{result.stdout}")
        if result.stderr:
            logger.warning(f"stderr for {script_name}:\n{result.stderr}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"{script_name} failed with exit code {e.returncode}.")
        logger.error(f"stdout for {script_name}:\n{e.stdout}")
        logger.error(f"stderr for {script_name}:\n{e.stderr}")
        return False
    except Exception as e:
        logger.error(f"An unexpected error occurred while running {script_name}: {e}")
        return False

if __name__ == "__main__":
    logger.info("Starting the complete YOLOv5 Medical Product Detection Pipeline.")

    # Step 1: Prepare Data (Setup directories and split dataset)
    if not run_script(os.path.join(config.PROJECT_ROOT, 'scripts', 'prepare_data.py'), 'prepare_data.py'):
        logger.error("Pipeline aborted: Data preparation failed.")
        sys.exit(1)

    # Step 2: Train Model (Setup YOLOv5, create YAML, train)
    if not run_script(os.path.join(config.PROJECT_ROOT, 'scripts', 'train_model.py'), 'train_model.py'):
        logger.error("Pipeline aborted: Model training failed.")
        sys.exit(1)

    # Step 3: Predict Images (Run inference on the whole dataset)
    # Important: The PREDICT_WEIGHTS_PATH in config.py might need dynamic update
    # or ensure RUN_NAME creates a consistent folder like 'fine_tuned_model'
    # and not 'fine_tuned_model1', 'fine_tuned_model2', etc.
    # YOLOv5 train.py creates runs/train/RUN_NAME if RUN_NAME exists it appends a number
    # You might need to parse the actual run directory created by train_model.py
    # For simplicity here, assuming RUN_NAME is fixed.
    if not run_script(os.path.join(config.PROJECT_ROOT, 'scripts', 'predict_images.py'), 'predict_images.py'):
        logger.error("Pipeline aborted: Image prediction failed.")
        sys.exit(1)

    # Step 4: Store Detection Results (Your existing script)
    # Ensure 'store_detection_results.py' is updated to read from YOLOv5 prediction output
    if not run_script(config.STORE_RESULTS_SCRIPT, 'store_detection_results.py'):
        logger.error("Pipeline aborted: Storing detection results failed.")
        sys.exit(1)

    logger.info("YOLOv5 Medical Product Detection Pipeline completed successfully.")