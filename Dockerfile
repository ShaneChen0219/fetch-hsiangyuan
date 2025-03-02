FROM python:3.9-slim

WORKDIR /app

COPY receiptprocessor.py requirements.txt ./

RUN pip install -r requirements.txt

EXPOSE 8080

CMD [ "python3" , "receiptprocessor.py" ]

