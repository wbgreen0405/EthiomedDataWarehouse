# ml_pipeline/scripts/prepare_data.py

import os
import random
import shutil
import sys
from roboflow import Roboflow # Import Roboflow

# Ensure project root is in path for config and logger
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config
from scripts.logger import Logger

logger = Logger(log_file=config.LOG_FILE)

def setup_directories():
    """Creates necessary directories for training and validation images and labels."""
    try:
        os.makedirs(config.TRAIN_DIR, exist_ok=True)
        os.makedirs(config.VAL_DIR, exist_ok=True)
        # Create corresponding labels directories
        os.makedirs(os.path.join(os.path.dirname(config.TRAIN_DIR), 'labels'), exist_ok=True)
        os.makedirs(os.path.join(os.path.dirname(config.VAL_DIR), 'labels'), exist_ok=True)
        # Ensure PHOTOS_DIR exists for downloads/source
        os.makedirs(config.PHOTOS_DIR, exist_ok=True)
        logger.info(f"Created/ensured directories: {config.TRAIN_DIR}, {config.VAL_DIR}, their labels subdirs, and {config.PHOTOS_DIR}.")
        return True
    except Exception as e:
        logger.error(f"Error setting up directories: {e}")
        return False

def download_dataset_from_roboflow():
    """Downloads the dataset from Roboflow to a temporary location and moves contents to config.PHOTOS_DIR."""
    logger.info("Attempting to download dataset from Roboflow...")
    if not config.ROBOFLOW_API_KEY:
        logger.error("ROBOFLOW_API_KEY not set in .env. Cannot download from Roboflow.")
        return False

    temp_download_dir_name = f"{config.ROBOFLOW_PROJECT}-{config.ROBOFLOW_VERSION}-{config.ROBOFLOW_FORMAT}"
    temp_download_path = os.path.join(config.DATA_DIR, temp_download_dir_name)

    try:
        # Clean up previous temporary download if it exists
        if os.path.exists(temp_download_path):
            logger.info(f"Cleaning up old temporary download directory: {temp_download_path}")
            shutil.rmtree(temp_download_path)

        rf = Roboflow(api_key=config.ROBOFLOW_API_KEY)
        project = rf.workspace(config.ROBOFLOW_WORKSPACE).project(config.ROBOFLOW_PROJECT)
        version = project.version(config.ROBOFLOW_VERSION)
        
        logger.info(f"Downloading Roboflow dataset version {config.ROBOFLOW_VERSION} to {temp_download_path}...")
        dataset_obj = version.download(config.ROBOFLOW_FORMAT, location=temp_download_path)
        
        # Roboflow's download method usually creates a subdirectory (e.g., 'medical-products-1-yolov5')
        # within the specified location. The 'dataset_obj.location' points to this.
        actual_download_dir = dataset_obj.location
        
        if not os.path.isdir(actual_download_dir):
            logger.error(f"Roboflow download did not create expected directory: {actual_download_dir}")
            return False

        logger.info(f"Roboflow dataset downloaded to: {actual_download_dir}")

        # Copy ALL image and label files from Roboflow's train/valid/test into config.PHOTOS_DIR
        # This centralizes all raw data for our prepare_data's split_dataset function.
        
        # Clear PHOTOS_DIR before copying from download
        if os.path.exists(config.PHOTOS_DIR):
            logger.info(f"Clearing existing files in {config.PHOTOS_DIR} before copying downloaded data.")
            for item in os.listdir(config.PHOTOS_DIR):
                item_path = os.path.join(config.PHOTOS_DIR, item)
                if os.path.isfile(item_path) or os.path.islink(item_path):
                    os.unlink(item_path)
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
        os.makedirs(config.PHOTOS_DIR, exist_ok=True) # Re-create if deleted

        subdirs_to_copy = ['train', 'valid', 'test'] # Roboflow YOLOv5 export structure
        total_copied_files = 0
        
        for subdir in subdirs_to_copy:
            # Paths to images and labels within the downloaded dataset
            subdir_images_path = os.path.join(actual_download_dir, subdir, 'images')
            subdir_labels_path = os.path.join(actual_download_dir, subdir, 'labels')
            
            if os.path.exists(subdir_images_path):
                for f in os.listdir(subdir_images_path):
                    shutil.copy(os.path.join(subdir_images_path, f), config.PHOTOS_DIR)
                    total_copied_files += 1
            
            if os.path.exists(subdir_labels_path):
                for f in os.listdir(subdir_labels_path):
                    shutil.copy(os.path.join(subdir_labels_path, f), config.PHOTOS_DIR)
                    total_copied_files += 1
                    
        logger.info(f"Copied {total_copied_files} files (images and labels) from Roboflow download to {config.PHOTOS_DIR}.")
        
        # Clean up the temporary download directory
        shutil.rmtree(temp_download_path)
        logger.info(f"Cleaned up temporary download directory: {temp_download_path}")

        return True

    except Exception as e:
        logger.error(f"Error during Roboflow dataset download: {e}")
        return False

def split_dataset(source_dir, train_images_dir, val_images_dir, split_ratio):
    """
    Splits images and their corresponding label files from source_dir
    into training and validation sets.
    Assumes image files are .jpg/.jpeg/.png and labels are .txt with same base name.
    """
    if not os.path.exists(source_dir):
        logger.error(f"Source directory not found for splitting: {source_dir}")
        return False

    all_files_in_source = os.listdir(source_dir)
    images = [f for f in all_files_in_source if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    if not images:
        logger.error(f"No images found in source directory for splitting: {source_dir}. Cannot split dataset.")
        return False
    logger.info(f"Found {len(images)} images for splitting in {source_dir}.")

    # Get corresponding labels directories
    train_labels_dir = os.path.join(os.path.dirname(train_images_dir), 'labels')
    val_labels_dir = os.path.join(os.path.dirname(val_images_dir), 'labels')

    # Clear existing images and labels in train/val directories to ensure fresh split
    logger.info("Clearing existing train/valid image and label directories.")
    shutil.rmtree(train_images_dir, ignore_errors=True)
    shutil.rmtree(val_images_dir, ignore_errors=True)
    shutil.rmtree(train_labels_dir, ignore_errors=True)
    shutil.rmtree(val_labels_dir, ignore_errors=True)

    os.makedirs(train_images_dir, exist_ok=True)
    os.makedirs(val_images_dir, exist_ok=True)
    os.makedirs(train_labels_dir, exist_ok=True)
    os.makedirs(val_labels_dir, exist_ok=True)


    random.shuffle(images)
    split_index = int(len(images) * split_ratio)
    train_images = images[:split_index]
    val_images = images[split_index:]

    def copy_files_with_labels(file_list, dest_images_dir, dest_labels_dir):
        copied_images_count = 0
        copied_labels_count = 0
        for img_file in file_list:
            src_img_path = os.path.join(source_dir, img_file)
            dest_img_path = os.path.join(dest_images_dir, img_file)
            shutil.copy(src_img_path, dest_img_path)
            copied_images_count += 1
            
            # Assume label file has same name but .txt extension
            base_name = os.path.splitext(img_file)[0]
            label_file = base_name + '.txt'
            src_label_path = os.path.join(source_dir, label_file) # Labels might be in PHOTOS_DIR too
            dest_label_path = os.path.join(dest_labels_dir, label_file)
            
            if os.path.exists(src_label_path):
                shutil.copy(src_label_path, dest_label_path)
                copied_labels_count += 1
            else:
                logger.warning(f"Label file not found for image: {img_file} at {src_label_path}. Skipping label copy.")
        return copied_images_count, copied_labels_count

    copied_train_images, copied_train_labels = copy_files_with_labels(train_images, train_images_dir, train_labels_dir)
    logger.info(f"Copied {copied_train_images} images and {copied_train_labels} labels to training set.")

    copied_val_images, copied_val_labels = copy_files_with_labels(val_images, val_images_dir, val_labels_dir)
    logger.info(f"Copied {copied_val_images} images and {copied_val_labels} labels to validation set.")

    logger.info(f"Dataset split completed. Train images: {len(train_images)}, Validation images: {len(val_images)}")
    return True

if __name__ == "__main__":
    logger.info("Starting data preparation...")
    if setup_directories():
        initial_photos_count = len(os.listdir(config.PHOTOS_DIR))
        if initial_photos_count == 0:
            logger.info(f"No files found in {config.PHOTOS_DIR}. Attempting Roboflow download.")
            if not download_dataset_from_roboflow():
                logger.error("Pipeline aborted: Roboflow download failed in prepare_data.py.")
                sys.exit(1)
            # Re-check after download
            if not os.listdir(config.PHOTOS_DIR):
                logger.error(f"Source directory {config.PHOTOS_DIR} is still empty after Roboflow download. Check download process or network.")
                sys.exit(1)
        else:
            logger.info(f"Files already present in {config.PHOTOS_DIR} ({initial_photos_count} items). Skipping Roboflow download.")

        # Now proceed with splitting the data that is either pre-existing or just downloaded
        logger.info(f"Starting dataset splitting from {config.PHOTOS_DIR}...")
        if split_dataset(config.PHOTOS_DIR, config.TRAIN_DIR, config.VAL_DIR, config.SPLIT_RATIO):
            logger.info("Data preparation successfully completed.")
        else:
            logger.error("Data splitting failed in prepare_data.py.")
            sys.exit(1) # Exit if splitting fails
    else:
        logger.error("Directory setup failed in prepare_data.py.")
        sys.exit(1) # Exit if directory setup fails