FROM python:3.8

RUN mkdir /src && mkdir /build

COPY requirements.txt /build

RUN pip install -r /build/requirements.txt

WORKDIR /src

COPY . /src

EXPOSE 1200

EXPOSE 6006

CMD python app.py