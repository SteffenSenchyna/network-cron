FROM python:3.9.2-alpine3.13
# To build container run 
RUN apk update && apk add bash
RUN apk add gcc musl-dev && \
    pip install --upgrade setuptools
WORKDIR /app
COPY . /app
COPY ./mibs/ /usr/local/lib/python3.9/site-packages/pysnmp/smi/mibs
RUN chmod a+x *.sh
RUN pip install -r requirements.txt 
ENTRYPOINT ["/bin/sh"]
