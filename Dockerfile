# 도커 허브에서 이미지를 가져와서 이미지를 작업한다
# FROM (이미지 이름:버전)
FROM python:3.9.18

# Set working directory
WORKDIR /ChaeDa_server

# Install python lib
COPY requirements.txt ./requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

RUN apt-get update
RUN apt-get -y install libgl1-mesa-glx

# Copy files
COPY ./main.py /ChaeDa_server/
COPY ./models.py /ChaeDa_server/
COPY ./.env /ChaeDa_server/
COPY ./domain /ChaeDa_server/domain
COPY ./domain /ChaeDa_server/images


CMD ["python", "main.py", "--host", "0.0.0.0", "--port", "8088"]