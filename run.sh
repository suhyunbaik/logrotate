#!/bin/bash
source /home/service/.venv/bin/activate
python /home/service/logrotate/run.py $1
