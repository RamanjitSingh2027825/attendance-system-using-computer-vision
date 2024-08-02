import os
import pickle

import cv2
import face_recognition

from firebase.database import upload_images_to_storage

from config.config import (
    logger
)


def find_encodings(images_list):
    encodings_list = []
    for image in images_list:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(image)[0]
        encodings_list.append(encode)
    return encodings_list


def generate_encodings_pickle(student_images_dir, students_encoding_file):
    images_path = os.listdir(student_images_dir)
    loaded_images, student_ids = [], []

    for path in images_path:
        file_name = f"{student_images_dir}/{path}"
        loaded_images.append(cv2.imread(file_name))  
        
        student_ids.append(path.split(".")[0])
        
        upload_images_to_storage(file_name)
        logger.info(f"Image {path} uploaded to storage")

    encodings_list = find_encodings(loaded_images)
    encodings_list_with_ids = [encodings_list, student_ids]

    with open(students_encoding_file, "wb") as file:
        pickle.dump(encodings_list_with_ids, file)