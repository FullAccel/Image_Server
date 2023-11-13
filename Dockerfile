# 도커 허브에서 이미지를 가져와서 이미지를 작업한다
# FROM (이미지 이름:버전)
FROM python:3.9.18

# Set working directory
WORKDIR /fastAPI_study

# Install python lib
COPY requirements.txt ./requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# Copy files
COPY ./main.py /fastAPI_study/

CMD ["python", "main.py", "--host", "0.0.0.0", "--port", "8088"]