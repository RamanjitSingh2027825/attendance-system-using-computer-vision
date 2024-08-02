from config.config import (
    logger,
    STUDENTS_DATA,
    STUDENTS_IMAGE_DIR,
    STUDENTS_ENCODING_FILE
)

from firebase.database import upload_student_data
from utils.encodings import generate_encodings_pickle

try:
    upload_student_data(
        file_path=STUDENTS_DATA
    )
    logger.info("Student data uploaded to firebase")
    
    generate_encodings_pickle(
        student_images_dir=STUDENTS_IMAGE_DIR,
        students_encoding_file=STUDENTS_ENCODING_FILE
    )
    logger.info("Student encodings generated and uploaded to firebase") 

except Exception as e:
    logger.error(f"Error: {e}")