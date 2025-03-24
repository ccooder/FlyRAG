#! /usr/bin/python
# encoding=utf-8
# Created by Fenglu Niu on 2025/3/13 22:14
import datetime
import uuid
from pathlib import Path
from typing import List

from fastapi import APIRouter, UploadFile, File
from starlette.responses import JSONResponse

import common
from flyrag.api import R
from common.minio_client import MinioClient

router = APIRouter(prefix='/file', tags=["file"])

@router.post("/upload")
async def upload(files: List[UploadFile] = File(...)):
    result = []
    for f in files:
        file_path = Path(f.filename)
        date = datetime.datetime.now().strftime("%Y%m%d")
        obj_name = date + '/' +str(uuid.uuid1()) + file_path.suffix
        if not MinioClient().upload_file(common.DEFAULT_BUCKET_NAME, obj_name, f.file, f.size, f.content_type):
            return JSONResponse(content=R.fail('上传失败'))
        obj = {'name': f.filename, 'obj_name': obj_name, 'size': f.size}
        result.append(obj)
    return R.ok(msg='上传成功', data=result)