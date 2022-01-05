#!/bin/bash
export PORT=80
echo "starting searx on localhost:80"
sudo docker run --rm -d -v /home/ferit/searx:/etc/searx -p $PORT:8080 -e BASE_URL=http://localhost:$PORT/ searx/searx
