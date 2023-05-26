FROM python:3.9

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 8000

CMD python create_db.py && yoyo apply --batch && python main.py && ./run_migrations.sh
