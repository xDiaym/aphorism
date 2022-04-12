import hashlib
import os

from flask import current_app
from werkzeug.datastructures import FileStorage

ALLOWED_EXTENSIONS = [".mp3", ".opus"]


def calc_md5(file: FileStorage) -> str:
    hash_md5 = hashlib.md5()
    for chunk in iter(lambda: file.read(4096), b""):
        hash_md5.update(chunk)
    return hash_md5.hexdigest()


def is_allowed_ext(file: FileStorage) -> bool:
    _, file_ext = os.path.splitext(file.filename)
    return file_ext in ALLOWED_EXTENSIONS


def save_voice_file(file: FileStorage) -> str:
    _, file_ext = os.path.splitext(file.filename)
    fname = calc_md5(file) + file_ext
    file.save(os.path.join(current_app.config["UPLOAD_FOLDER"], fname))
    return fname
