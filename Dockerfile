FROM ubuntu:latest
RUN apt update
RUN apt -qy install python3
RUN apt -qy install python3-pip
RUN apt -qy install mysql-server
WORKDIR /app
COPY . /app
RUN /bin/sh -c 'service mysql start;mysql <"init.sql"'
RUN pip3 install -r requirements.txt
EXPOSE 8080
ENTRYPOINT ["python3"]
CMD ["app.py"]
