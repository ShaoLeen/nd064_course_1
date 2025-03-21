FROM python:3.12
LABEL maintainer="Alexander Olschok"

WORKDIR /project/techtrends
COPY /project/techtrends

RUN pip install --upgrade pip && pip install -r requirements.txt

RUN python3 init_db.py

EXPOSE 3111

# command to run on container start
CMD [ "python", "app.py" ]
