# OpenCV를 활용한 강아지,고양이 얼굴 탐지 API 서버 🐶🐱
Dog and cat face detector api server with OpenCV

### Main Tech
- Python 3.9
- FastAPI
- OpenCV
- Numpy
- Uvicorn


### Docs
FastAPI 서버 실행 후, `http://127.0.0.1/docs` 접속

Access line `http://127.0.0.1/docs` after running FastAPI server

<br>

---

## 사용 방법 (How to use)

### pip 설치
```shell
sudo apt-get install python3-pip
```

### pip를 최신버전으로 업데이트 (Update pip to latest version)
```shell
python -m pip install --upgrade pip
```

<br>

### FastAPI 설치 (Install FastAPI)
```shell
pip install fastapi
```

<br>

### Numpy 설치 (Install Numpy)
```shell
pip install numpy
```

<br>

### OpenCV 설치 (Install OpenCV)
```shell
pip install opencv-python
```

<br>

### Uvicorn 설치 (Install Uvicorn)
```shell
pip install "uvicorn[standard]"
```

FastAPI로 작성한 프로그램을 작동시키기 위해서는 작동시킬 서버가 필요하다.
`유비콘(Uvicorn)`은 비동기 호출을 지원하는 파이썬용 웹 서버이며, 이를 사용해서 FastAPI를 실행시킬 수 있다.

To run a program written with FastAPI, you need a server to run it.
`Uvicorn` is a web server for Python that supports asynchronous calls, which can be used to run FastAPI.

<br>

### python-multipart 설치
```shell
pip install python-multipart
```
멀티파트 파일을 다루기 위한 `python-multipart` 설치

<br>

### 서버 실행 (Run server)
```shell
uvicorn main:app --reload
```

---

## 서버 실행 후, 에러 발생 시 (When an error occurs)

![스크린샷 2024-01-31 오후 11 36 06](https://github.com/Team-Petudio/Petudio-PetFaceDetect-Server/assets/84304802/8cb2fb36-5398-4bea-8ed6-753f710782e5)

### libgl1-mesa-glx 설치
```shell
sudo apt-get install -y libgl1-mesa-glx
```

<br>

---


![스크린샷 2024-01-31 오후 11 45 25](https://github.com/Team-Petudio/Petudio-PetFaceDetect-Server/assets/84304802/5aff4bff-22e5-4d6a-af0c-ddb86eda9bce)

### libglib2.0-0 설치
```shell
sudo apt-get install -y libglib2.0-0
```
