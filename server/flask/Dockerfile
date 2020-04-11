FROM python:3.7.2-stretch

#set working dir in container, make if it doesn't exist
WORKDIR /app

#install requirements
#COPY REQUIREMENTS /app
#RUN pip install -r REQUIREMENTS

ADD REQUIREMENTS .

#COPY app.ini /app
#COPY /app /app
#COPY run.py /app

#uwsgi is listening on container port 8080
#EXPOSE 8080

RUN pip install -r REQUIREMENTS

ADD . .

CMD ["uwsgi","app.ini"]