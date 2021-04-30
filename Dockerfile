FROM python:3

ADD . /DataEngineerTest

RUN make /DataEngineerTest

CMD python /DataEngineerTest/notebooks/showcase_notebook.ipynb


COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY DataEngineerTest/ .
RUN mkdir data_cache

CMD [ "python", "main.py" ]