import json

from pydantic import BaseModel
from fastapi.responses import FileResponse
from fastapi import FastAPI, UploadFile, HTTPException, File, Depends

from overlay import overlay_images
from cerificate import create_certificate
from s3 import get_signed_url, upload_file_to_s3
from util import get_tmp_path, get_char_uuid, save_upload_file, temporary_files


app = FastAPI()


def load_config():
    with open('config.json') as file:
        return json.load(file)


@app.post("/overlay/")
async def overlay(
    user_image: UploadFile = File(...),
    config=Depends(load_config)
):
    try:
        TMP_PATH = get_tmp_path()
        bg_path = f"{TMP_PATH}/{user_image.filename}"
        ov_path = "artifacts/overlay_image.png"
        output_image_name = f"OVERLAY_{get_char_uuid(10)}.jpg"
        output_path = f"{TMP_PATH}/{output_image_name}"

        save_upload_file(user_image, bg_path)

        with temporary_files(bg_path, output_path):
            overlay_images(bg_path, ov_path, output_path)

            s3_key = upload_file_to_s3(output_path, output_image_name, config)
            url = get_signed_url(s3_key, config)

            return {"url": url}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class CertificateRequest(BaseModel):
    name: str
    in_hindi: bool = False


@app.post("/certificate/")
async def certificate(
    request: CertificateRequest,
    config=Depends(load_config)
):
    try:
        name = request.name
        in_hindi = request.in_hindi

        TMP_PATH = get_tmp_path()

        output_image_name = f"CERTIFICATE_{name}_{get_char_uuid(10)}.jpg"
        output_path = f"{TMP_PATH}/{output_image_name}"

        with temporary_files(output_path):
            create_certificate(name, in_hindi, output_path)

            s3_key = upload_file_to_s3(output_path, output_image_name, config)
            url = get_signed_url(s3_key, config)

            return {"url": url}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
