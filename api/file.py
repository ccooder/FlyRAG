#! /usr/bin/python
# encoding=utf-8
# Created by Fenglu Niu on 2025/3/13 22:14
import uuid
from pathlib import Path
from typing import List

from fastapi import APIRouter, UploadFile, File
from starlette.responses import JSONResponse

import common
from api import R
from common.minio_client import MinioClient

router = APIRouter(prefix='/file', tags=["file"])

@router.post("/upload")
async def upload(files: List[UploadFile] = File(...)):
    for f in files:
        file_path = Path(f.filename)
        obj_name = str(uuid.uuid1()) + file_path.suffix
        if MinioClient().upload_file(common.DEFAULT_BUCKET_NAME, obj_name, f.file, f.size, f.content_type):
            return JSONResponse(content=R.ok())
        else:
            return JSONResponse(content=R.fail('上传失败'))