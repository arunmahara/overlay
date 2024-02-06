FROM python:3.10
WORKDIR /app
COPY . /app
RUN apt-get update && apt-get install -y libgl1-mesa-glx
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir /logs
EXPOSE 9000
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000"]
CMD uvicorn main:app --host 0.0.0.0 --port 9000 >> logs/server.log

# sudo docker build -t overlay .
# sudo docker run -dp 9000:9000 -v /home/ubuntu/overlay-logs:/app/logs overlay