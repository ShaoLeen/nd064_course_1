FROM python:3.8
LABEL maintainer="Alexander Olschok"

COPY . /project
WORKDIR /project
RUN pip install -r requirements.txt

EXPOSE 3111

# command to run on container start
CMD [ "python", "app.py" ]
