# encoding: utf8
import os
import sys
import boto3
import time
import requests
import subprocess


logrotate_path = '{}.{}'.format(sys.argv[1], time.strftime('%Y%m%d'))
compress_path = '{}.gz'.format(logrotate_path)

cmd = "cd /home/service/service && git remote -v | grep origin | grep fetch | awk '{print $2}' | awk -F'/' '{print $2}'"
repository = subprocess.check_output(cmd, shell=True).decode('utf-8').strip().replace('.git', '')

try:
    os.system('gzip {}'.format(logrotate_path))
    s3 = boto3.resource(
        's3',
        region_name='ap-northeast-2',
        aws_access_key_id='',
        aws_secret_access_key=''
    )
    s3.Bucket('server-logs').upload_file(
        compress_path,
        '{}/{}.{}.gz'.format(
            time.strftime('%Y/%m/%d'),
            repository,
            os.path.basename(sys.argv[1]).split('.')[0]
        )
    )
    os.remove(compress_path)
except Exception as e:
    requests.post(
        '',
        json=dict(
            pretext='{} 업로드 실패'.format(sys.argv[1]),
            text=str(e),
            color='warning'
        )
    )

