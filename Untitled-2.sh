#!/bin/bash

sleep 2

# Server URL
# SERVER_URL="http://localhost:5173"
SERVER_URL="https://buckethatrobot.onrender.com/"

# Update Message
echo "Sending POST request to /update-message..."
curl -X POST "$SERVER_URL/update-message" \
     -H "Content-Type: application/json" \
     -d '{"message": "New update received at 12:50PM!"}' \
     -v

# Update Instructions
echo "Sending POST request to /update-instructions..."
curl -X POST "$SERVER_URL/update-instructions" \
     -H "Content-Type: application/json" \
     -d '{"instructions": "Follow the steps: 1. Check inventory 2. Reorder items 3. Update database"}' \
     -v

# Update Image URI
echo "Sending POST request to /update-img-uri..."
curl -X POST "$SERVER_URL/update-img-uri" \
     -H "Content-Type: application/json" \
     -d '{"img_uri": "https://d6af-129-97-124-163.ngrok-free.app/static/img/generic.jpg"}' \
     -v

# Update Grocery List
echo "Sending POST request to /update-grocery-list..."
curl -X POST "$SERVER_URL/update-grocery-list" \
     -H "Content-Type: application/json" \
     -d '{"grocery_list": "Apples, Bananas, Carrots"}' \
     -v

echo "All POST requests sent."