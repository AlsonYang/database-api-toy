#!/bin/sh
curl -d '{
    "name": "Alson2"
}' \
    -H 'Content-Type: application/json' \
    -X PUT http://localhost:8080/members/1