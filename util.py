import os
import uuid

from contextlib import contextmanager

from fastapi import UploadFile


def get_tmp_path():
    return "/tmp"


def remove_file(file_path):
    try:
        os.remove(file_path)
    except OSError:
        return


def get_char_uuid(length=0):
    uid = uuid.uuid4().hex
    if length:
        return uid[:length]

    return uid


@contextmanager
def temporary_files(*paths):
    try:
        yield
    finally:
        for path in paths:
            remove_file(path)


def save_upload_file(upload_file: UploadFile, path: str):
    with open(path, "wb") as file:
        file.write(upload_file.file.read())
