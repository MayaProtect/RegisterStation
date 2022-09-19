FROM python:3.10-bullseye

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

ENV MONGO_HOST=mongo
ENV MONGO_PORT=27017
ENV MONGO_DB=mayaprotect

EXPOSE 8080

CMD python run.py