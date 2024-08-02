import os
import pickle

import cv2
import cvzone
import face_recognition
import numpy as np

from config.config import (
    logger,
    STUDENTS_ENCODING_FILE
)

from firebase.database import download_student_data, mark_student_present


cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)


imageBackground = cv2.imread("assets/background.png")
modes_folder = "assets/modes"
modes_path = os.listdir(modes_folder)
modes_images = []
for path in modes_path:
    modes_images.append(cv2.imread(os.path.join(modes_folder,path)))


with open(STUDENTS_ENCODING_FILE, "rb") as file:
    encodings_list_with_ids = pickle.load(file)
encodings_list, student_ids = encodings_list_with_ids


recognized_students = set()

while True:
    success, camera = cap.read()
    if not success:
        break

    camera_small = cv2.resize(camera, (0,0), None, 0.25, 0.25) # 1/4 size
    camera_small = cv2.cvtColor(camera_small, cv2.COLOR_BGR2RGB)

    faces_current_frame = face_recognition.face_locations(camera_small)
    encode_current_frame = face_recognition.face_encodings(camera_small, faces_current_frame)

    imageBackground[162 : 162+480, 55 : 55+640] = camera
    imageBackground[44 : 44+633, 808 : 808+414] = modes_images[0]


    for encode_face, face_location in zip(encode_current_frame, faces_current_frame):
        matches = face_recognition.compare_faces(encodings_list, encode_face)
        face_distance = face_recognition.face_distance(encodings_list, encode_face)

        match_index = np.argmin(face_distance)
        student_id = student_ids[match_index]

        if matches[match_index] and student_id not in recognized_students:
            student_data = download_student_data(student_id)
            mark_student_present(student_id)
            recognized_students.add(student_id)

        if matches[match_index]:
            y1, x2, y2, x1 = face_location 
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            bbox = 55+x1, 162+y1, x2-x1, y2-y1

            imageBackground = cvzone.cornerRect(imageBackground, bbox, rt=0)

    cv2.imshow("Face Attendant System", imageBackground)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break