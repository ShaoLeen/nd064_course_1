FROM python:3.12
LABEL maintainer="Alexander Olschok"

WORKDIR /project/techtrends
COPY . .
RUN pip install -r requirements.txt&&python init_db.py

EXPOSE 3111

# command to run on container start
CMD [ "python", "app.py" ]
