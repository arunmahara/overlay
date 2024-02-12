import json

from pydantic import BaseModel
from fastapi.responses import FileResponse
from fastapi import FastAPI, UploadFile, HTTPException, File, Depends

from overlay import overlay_images
from cerificate import create_certificate
from s3 import get_signed_url, upload_file_to_s3
from util import get_tmp_path, get_char_uuid, save_upload_file, temporary_files
import logging


logging.basicConfig(filename='logs/app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger(__name__)


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
        logging.info("/overlay/")
        logging.info(f"Overlay request received")

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
            logging.info(f"Overlay request completed URL: {s3_key}")

            return {"url": url}

    except Exception as e:
        logging.error(f"Error in overlay function: {e}")
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
        logging.info("/certificate/")
        logging.info(f"Certificate request received {request}")

        name = request.name
        in_hindi = request.in_hindi

        TMP_PATH = get_tmp_path()

        output_image_name = f"CERTIFICATE_{name}_{get_char_uuid(10)}.jpg"
        output_path = f"{TMP_PATH}/{output_image_name}"

        with temporary_files(output_path):
            create_certificate(name, in_hindi, output_path, "v1")

            s3_key = upload_file_to_s3(output_path, output_image_name, config)
            url = get_signed_url(s3_key, config)
            logging.info(f"Certificate request completed URL: {s3_key}")

            return {"url": url}

    except Exception as e:
        logging.error(f"Error in certificate function: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/v2/certificate/")
async def certificate(
    request: CertificateRequest,
    config=Depends(load_config)
):
    try:
        logging.info("/v2/certificate/")
        logging.info(f"V2 Certificate request received {request}")

        name = request.name
        in_hindi = request.in_hindi

        TMP_PATH = get_tmp_path()

        output_image_name = f"CERTIFICATE_V2_{name}_{get_char_uuid(10)}.jpg"
        output_path = f"{TMP_PATH}/{output_image_name}"

        with temporary_files(output_path):
            create_certificate(name, in_hindi, output_path, "v2")

            s3_key = upload_file_to_s3(output_path, output_image_name, config)
            url = get_signed_url(s3_key, config)
            logging.info(f"V2 Certificate request completed URL: {s3_key}")

            return {"url": url}

    except Exception as e:
        logging.error(f"Error in v2 certificate function: {e}")
        raise HTTPException(status_code=500, detail=str(e))
