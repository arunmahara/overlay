# overlay (FastAPI)

- Run web service

```commandline
docker build -t overlay .
docker run -dp 443:443 overlay
```

- API endpoint
```curl
curl --location 'http://127.0.0.1:443/overlay/' \
--form 'user_image=@"/home/arun/Downloads/image.png"'
```

```
curl --location 'http://127.0.0.1:8000/certificate/' \
--header 'Content-Type: application/json' \
--data '{
    "name": "Arun Mahara",
    "in_hindi": false
    
    // "name": "अरुण महरा",
    // "in_hindi": true
}'
```