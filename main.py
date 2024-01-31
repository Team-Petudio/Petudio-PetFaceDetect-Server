from typing import List

import cv2
import uuid
import numpy as np
import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from starlette.status import HTTP_413_REQUEST_ENTITY_TOO_LARGE, HTTP_400_BAD_REQUEST

app = FastAPI()

# 인식할 애완동물 종류
pet_types = ["CAT", "DOG"]
# 최대 파일 사이즈 (1MB)
MAX_FILE_SIZE = 1 * 1024 * 1024

# Yolo 로드
# weights, cfg파일을 불러와서 yolo의 네트워크와 연결한다.
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")

# class 배열 만들기
classes = []

# coco 파일을 읽어온다.
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]  # 읽어온 coco 파일을 whitespace(공백라인)를 제거하여 classes 배열 안에 넣는다.

# 네트워크의 모든 레이어 이름을 가져와서 layer_names에 넣는다.
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in
                 net.getUnconnectedOutLayers()]  # 레이어 중 출력 레이어의 인덱스를 가져와서 output_layers에 넣는다.


@app.post("/detect")
async def detect_dog_face_endpoint(petType: str, files: List[UploadFile] = File(...)):
    await validate_pet_type(petType)

    global temp_image_name

    # petType은 애플리케이션 서버에 있는 PetType Enum 상수와 일치시켜 관리하기 위해 대문자로 관리하고 실제 처리는 소문자로 수행
    petType = petType.lower()
    results = [False for _ in range(len(files))]

    for idx in range(len(files)):
        file = files[idx]
        await validate_file_size(file)
        await file.seek(0)

        try:
            # 임시 디렉터리에 파일 저장
            temp_image_name = str(uuid.uuid1()) + ".jpeg"
            with open(temp_image_name, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            # OpenCV로 이미지 읽기
            img = cv2.imread(temp_image_name)

            # 이미지 처리 등의 작업 수행
            img = cv2.resize(img, None, fx=0.4, fy=0.4)  # 이미지 크기를 재설정한다.
            height, width, channels = img.shape  # 이미지의 속성들을 넣는다.

            blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)  # 이미지를 blob 객체로 처리한다.
            net.setInput(blob)  # blob 객체에 setInput 함수를 적용한다.
            outs = net.forward(output_layers)  # output_layers를 네트워크 순방향으로 실행(추론)한다.

            class_ids = []  # 인식한 사물 클래스 아이디를 넣는 배열
            confidences = []  # 0에서 1까지 사물 인식에 대한 신뢰도를 넣는 배열
            boxes = []  # 사물을 인식해서 그릴 상에 대한 배열

            for out in outs:
                for detection in out:
                    scores = detection[5:]
                    class_id = np.argmax(scores)  # scores 중에서 최대값을 색인하여 class_id에 넣는다.
                    confidence = scores[class_id]  # scores 중에서 class_id에 해당하는 값을 confidence에 넣는다.
                    if confidence > 0.75:  # 만약 정확도가 0.75가 넘는다면 사물이 인식되었다고 판단
                        # 좌표 인식
                        center_x = int(detection[0] * width)
                        center_y = int(detection[1] * height)
                        w = int(detection[2] * width)
                        h = int(detection[3] * height)
                        x = int(center_x - w / 2)
                        y = int(center_y - h / 2)
                        boxes.append([x, y, w, h])

                        # 객체 탐지(Object detected)
                        confidences.append(float(confidence))
                        class_ids.append(class_id)

            # 같은 좌표의 사물을 여러 개 인식한 노이즈를 제거
            indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
            # 인식된 사물이 고양이인지 판단
            for i in range(len(boxes)):
                if i in indexes:
                    detected = str(classes[class_ids[i]])
                    if (detected == petType):
                        results[idx] = True
                        continue
        finally:
            # 임시 파일 삭제
            os.remove(temp_image_name)

    return {"results": results}


async def validate_file_size(file):
    file_size = 0
    for chunk in file.file:
        file_size = file_size + len(chunk)
        if file_size > MAX_FILE_SIZE:
            raise HTTPException(status_code=HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="Image size is too large!")


async def validate_pet_type(pet_type):
    if pet_type not in pet_types:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="requested pet type is not supported!")
