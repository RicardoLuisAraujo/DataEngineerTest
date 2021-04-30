FROM python:3

ADD DataEngineerTest /

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY DataEngineerTest/ .
RUN mkdir data_cache

CMD [ "python", "main.py" ]