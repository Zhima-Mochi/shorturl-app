FROM python:3.8
WORKDIR /usr/src/server
ADD requirements.txt .
RUN pip install --trusted-host pypi.python.org -r requirements.txt
ADD ./main .
ENV HOST_NAME=http://localhost:8005
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8005"]