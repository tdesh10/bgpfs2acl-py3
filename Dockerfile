FROM python:3.9-slim

WORKDIR /app/

COPY . .
RUN pip install -Ur requirements.txt

CMD ["./start_app.sh"]