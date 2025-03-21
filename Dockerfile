FROM python:3.12
LABEL maintainer="Alexander Olschok"

WORKDIR /project/techtrends
COPY . .
RUN pip install --upgrade pip && pip install -r requirements.txt && python3 /project/techtrends/init_db.py

EXPOSE 3111

# command to run on container start
CMD [ "python", "app.py" ]
