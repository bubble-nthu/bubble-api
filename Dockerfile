FROM python:3.9

ENV FLASK_APP bubble.py
ENV FLASK_CONFIG docker

RUN useradd -m bubble
USER bubble

WORKDIR /home/bubble

COPY requirements requirements
RUN python -m venv venv
RUN venv/bin/pip install -r requirements/docker.txt

COPY app app
COPY migrations migrations
COPY bubble.py config.py boot.sh ./

# run-time configuration
EXPOSE 5000
#CMD ["source", "venv/bin/activate"]
#CMD ["flask", "deploy"]
#CMD ["exec", "gunicorn", "-b", ":5000", "--access-logfile", "-", "--error-logfile", "-", "bubble:app"]
ENTRYPOINT ["./boot.sh"]