#!/bin/bash

# 1. Post image as octet/stream to server
# 2. Get response as json ({"label": "audi", "confidence": 0.95})

URL='https://fabio-kost--flask-server-flask-app.modal.run/classify'
IMAGE_PATH='data/tycan.jpg'
IMAGE_TYPE='image/jpeg'

curl -X POST -F "file=@$IMAGE_PATH;type=$IMAGE_TYPE" "$URL" -o response.json
cat response.json
