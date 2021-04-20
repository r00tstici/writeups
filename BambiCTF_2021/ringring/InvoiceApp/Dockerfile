FROM python:3.8.1

COPY InvoiceApp/requirements.txt /InvoiceApp/requirements.txt
RUN pip3 install -r /InvoiceApp/requirements.txt

COPY InvoiceApp/ /InvoiceApp

RUN apt-get update && \
    apt-get -y install netcat


RUN useradd -m hotelguest && \
    echo "hotelguest:$(openssl rand -hex 20)" | chpasswd

RUN chmod -R 0766 /InvoiceApp/accounting
RUN chown -R hotelguest:hotelguest InvoiceApp/accounting

RUN echo "root:$(openssl rand -hex 20)" | chpasswd

USER hotelguest

WORKDIR /InvoiceApp
EXPOSE 7354
ENTRYPOINT ["gunicorn", "-c", "gunicorn.conf.py", "app:app" ]