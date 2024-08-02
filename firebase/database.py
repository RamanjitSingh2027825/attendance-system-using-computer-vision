import json
from datetime import datetime

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db, storage

from config.config import (
    DATABASE_URL,
    STORAGE_BUCKET,
    FIREBASE_CREDENTIALS
)

cred = credentials.Certificate(FIREBASE_CREDENTIALS)
firebase_admin.initialize_app(cred, {
    'databaseURL': DATABASE_URL,
    'storageBucket': STORAGE_BUCKET
})

# ----------------------------- UPLOADING DATA TO FIREBASE -----------------------------

def upload_student_data(file_path):
    ref = db.reference('Students')
    with open(file_path) as f:
        data = json.load(f)
        for key, value in data.items():
            ref.child(key).set(value)

def upload_images_to_storage(file_name):
    bucket = storage.bucket()
    blob = bucket.blob(file_name)
    blob.upload_from_filename(file_name)


# ----------------------------- DOWNLOADING DATA FROM FIREBASE -----------------------------

def download_student_data(student_id):
    data = db.reference(f'Students/{student_id}').get()
    return data


# ----------------------------- UPDATING DATA FROM FIREBASE -----------------------------

def mark_student_present(student_id):
    total_attendance = int(db.reference(f'Students/{student_id}/total_attendance').get()) + 1
    last_login = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ref = db.reference(f'Students/{student_id}')
    ref.update({
        'total_attendance': total_attendance,
        'last_login': last_login
    })