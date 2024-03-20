FROM python:3.10

WORKDIR /pythonTgBot

COPY requirements.txt ./requirements.txt

RUN pip install --no-cache-dir --upgrade -r /pythonTgBot/requirements.txt

COPY . /pythonTgBot

CMD ["python", "main.py"]

