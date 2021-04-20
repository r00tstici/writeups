FROM python:3.8.1
LABEL version="0.0.1"

COPY App/requirements.txt /service-ringring/
RUN pip3 install -r /service-ringring/requirements.txt

COPY App /service-ringring
WORKDIR /service-ringring

EXPOSE 7353

ENTRYPOINT [ "gunicorn", "-c", "gunicorn.conf.py", "app:app" ]
