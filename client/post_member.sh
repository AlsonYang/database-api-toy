#!/bin/sh
# -H is the header which specifies the content-type of the data to be json. Without it, it will raise the following error:
    # error: `Did not attempt to load JSON data because the request Content-Type was not &#x27;application/json&#x27`
curl -d '{
    "name":"Alson",
    "description":"the author"
}' \
    -H "Content-Type: application/json" \
    -X POST http://localhost:8080/members

