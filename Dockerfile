FROM python:3.7

RUN apt-get update
RUN apt update && apt install -y libsm6 libxext6 ffmpeg libfontconfig1 libxrender1 libgl1-mesa-glx

ADD . /app/
WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY ./mtcnn-master/mtcnn /app/

EXPOSE 5111

CMD ["uvicorn", "app:app", "--port", "5111", "--host", "0.0.0.0"]
