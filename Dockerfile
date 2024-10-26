FROM python:3.12
ENV PYTHONUNBUFFERED 1
ENV APP_HOME=/swa
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/static
WORKDIR $APP_HOME
COPY requirements.txt $APP_HOME
RUN pip install --upgrade pip
RUN apt-get update
RUN pip install -r requirements.txt
COPY . $APP_HOME
