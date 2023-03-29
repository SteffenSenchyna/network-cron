FROM python:3.9.2-alpine3.13
# To build container run 
RUN apk update && apk add bash
WORKDIR /app
COPY . /app
RUN chmod a+x run.sh
RUN pip install -r requirements.txt 

CMD [ "./run.sh" ]