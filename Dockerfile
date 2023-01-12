FROM python:3.9.16
USER root

RUN apt-get update
RUN apt-get -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

RUN apt-get install -y vim less
RUN apt-get install apt-transport-https
RUN apt install -y tesseract-ocr libtesseract-dev

RUN curl https://cli-assets.heroku.com/install.sh | sh

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

WORKDIR /Python/Flask

COPY requirements.txt /Python
RUN pip install -r /Python/requirements.txt
RUN pip install gunicorn
#RUN pip install --upgrade flask-cors
#RUN pip install --upgrade opencv-python
#RUN pip install --upgrade opencv-contrib-python
#RUN pip install --upgrade pytesseract

COPY Flask /Python/Flask

CMD ["python", "app.py", "--bind", "0.0.0.0:$PORT", "wsgi"]
