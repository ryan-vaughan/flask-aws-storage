FROM python:3.6.9

RUN groupadd flaskgroup && useradd -m -g flaskgroup -s /bin/bash flask

RUN mkdir -p /home/flask/app/
WORKDIR /home/flask/app/
RUN git clone https://github.com/ryan-vaughan/flask-aws-storage.git
RUN mv flask-aws-storage web && mkdir -p /home/flask/app/web/uploads
WORKDIR /home/flask/app/web
RUN pip install --no-cache-dir -r requirements.txt
RUN chown -R flask:flaskgroup /home/flask

EXPOSE 5000
USER flask
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]

