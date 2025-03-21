FROM python:3.12
LABEL maintainer="Alexander Olschok"

COPY . .
WORKDIR /project/techtrends
RUN pip install -r requirements.txt

EXPOSE 3111

# command to run on container start
CMD [ "python", "app.py" ]
