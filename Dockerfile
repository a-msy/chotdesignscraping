FROM python:3
USER root

WORKDIR /app

RUN apt-get update
RUN apt-get -y install locales && localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

RUN apt-get install -y vim less
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add && \
wget http://dl.google.com/linux/deb/pool/main/g/google-chrome-unstable/google-chrome-unstable_93.0.4577.18-1_amd64.deb && \
apt-get install -y -f ./google-chrome-unstable_93.0.4577.18-1_amd64.deb

ADD https://chromedriver.storage.googleapis.com/93.0.4577.15/chromedriver_linux64.zip /opt/chrome/
RUN cd /opt/chrome/ && unzip chromedriver_linux64.zip

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install selenium && pip install bs4 && pip install oauth2client && chromedriver_binary

ENV PATH /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/opt/chrome