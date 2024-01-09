# overlay (FastAPI)

- Run web service

```commandline
docker build -t overlay .
docker run -dp 443:443 overlay
```

- API endpoint
```curl
curl --location 'http://127.0.0.1:443/overlay/' \
--header 'accept: application/json' \
--header 'Cookie: csrftoken=xQsfHdMsWckc4rrLRu48YlXVUHuZV0c9' \
--form 'background_image=@"/home/arun/Downloads/image.png"' \
--form 'overlay_image=@"/home/arun/Downloads/img/logo.png"'
```