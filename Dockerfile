FROM python:3.8
WORKDIR /usr/src/server
ADD requirements.txt .
RUN pip install --trusted-host pypi.python.org -r requirements.txt
ADD ./main .
ENV HOST_NAME=https://akb49.herokuapp.com/
RUN adduser customer
RUN chown customer sql_app.db
RUN chown customer /usr/src/server
USER customer
CMD uvicorn main:app --host 0.0.0.0 --port $PORT
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "$PORT"]