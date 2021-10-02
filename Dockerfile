FROM nginx:latest
USER root

RUN apt-get update && apt-get install -y python python-pip

RUN mkdir /Application
ADD requirements.txt entrypoint.sh /
RUN chmod +x /entrypoint.sh
ADD app.py /Application

RUN pip install -r /requirements.txt

EXPOSE 8000

CMD ["./entrypoint.sh"]