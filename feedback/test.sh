#!/bin/bash

set -euo pipefail

# POST new feedback
echo "POST feedback"
feedback=$(curl -s -X POST http://localhost:5000/feedback/feedback \
  -H "Content-Type: application/json" \
  -d '{
    "image": "'$(base64 -i ./mock/audi.jpg)'",
    "label": "bmw",
    "correct": false,
    "correct_label": "audi",
    "trained": false
}')

feedbackId=$(echo $feedback | jq -r '.id')
echo $feedback | jq

# PATCH feedback
echo "PATCH feedback"
curl -s -X PATCH http://localhost:5000/feedback/feedback/$feedbackId \
  -H "Content-Type: application/json" \
  -d '{"trained": true}' | jq

# GET labels
echo "GET labels"
curl -s -X GET http://localhost:5000/feedback/labels | jq
