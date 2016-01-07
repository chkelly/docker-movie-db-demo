FROM python:2.7
ADD . /code
WORKDIR /code
RUN apt-get update
RUN pip install -r requirements.txt
CMD python app.py 5000
