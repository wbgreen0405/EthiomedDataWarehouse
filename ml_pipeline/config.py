# ml_pipeline/config.py

import os
from dotenv import load_dotenv # Import load_dotenv

# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env'))

# --- General Project Paths ---
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
PHOTOS_DIR = os.path.join(DATA_DIR, 'photos')
TRAIN_DIR = os.path.join(DATA_DIR, 'train', 'images')
VAL_DIR = os.path.join(DATA_DIR, 'valid', 'images')
LOG_FILE = os.path.join(DATA_DIR, 'yolo_training.log')

# --- YOLOv5 Paths ---
YOLOV5_REPO_URL = "https://github.com/ultralytics/yolov5.git"
YOLOV5_DIR = os.path.join(PROJECT_ROOT, 'yolov5')
YOLOV5_REQUIREMENTS = os.path.join(YOLOV5_DIR, 'requirements.txt')

# --- Dataset Splitting Parameters ---
SPLIT_RATIO = 0.8

# --- YOLOv5 Training Parameters ---
YOLO_DATA_YAML_PATH = os.path.join(DATA_DIR, 'ethio_medical_dataset.yml')
YOLO_DATA_YAML_RELATIVE_PATH = os.path.relpath(YOLO_DATA_YAML_PATH, YOLOV5_DIR)

IMG_SIZE = 320
BATCH_SIZE = 8
EPOCHS = 50
WEIGHTS = 'yolov5n.pt'
RUN_NAME = 'fine_tuned_model'

# --- Roboflow Parameters (Read from environment variable) ---
ROBOFLOW_API_KEY = os.getenv("ROBOFLOW_API_KEY") 
ROBOFLOW_WORKSPACE = "robo-irnwv"   # <-- UPDATED
ROBOFLOW_PROJECT = "datawarehouse_medical" # <-- UPDATED
ROBOFLOW_VERSION = 1
ROBOFLOW_FORMAT = "yolov5"

# --- Prediction Parameters ---
PREDICT_WEIGHTS_PATH = os.path.join(YOLOV5_DIR, 'runs', 'train', RUN_NAME, 'weights', 'best.pt')
PREDICT_CONF_THRESHOLD = 0.25
PREDICT_SOURCE_DIR = PHOTOS_DIR
PREDICT_OUTPUT_NAME = 'predictions'

# --- Database Storage Script Path ---
STORE_RESULTS_SCRIPT = os.path.join(PROJECT_ROOT, 'scripts', 'store_detection_results.py')

# --- Classes for YOLOv5 Data YAML ---
NUM_CLASSES = 1
CLASS_NAMES = ['product']

# Basic check to ensure API key is loaded
if ROBOFLOW_API_KEY is None:
    print("Warning: ROBOFLOW_API_KEY not found in .env file or environment variables.")