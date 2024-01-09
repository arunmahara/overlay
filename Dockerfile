FROM python:3.10
WORKDIR /app
COPY . /app
RUN apt-get update && apt-get install -y libgl1-mesa-glx
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 443
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "443"]


# docker build -t overlay .
# docker run -dp 443:443 overlay
