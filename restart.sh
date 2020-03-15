#!/usr/bin/bash

echo '开始杀死进程'

`ps aux | grep python | grep "flask_server" | awk {'print $2'} | xargs kill -9`

nohup python3 -u ./server/flask_server.py > nohub.out 2>nohub.log &
