#! /usr/bin/python3.6
import os
import boto3
import urllib3
import json

http = urllib3.PoolManager()
s3 = boto3.client('s3')

def lambda_handler(event, context):
    url = os.environ['TEAMS_WEBHOOK_URL']
    s3_event = json.loads(event['Records'][0]['Sns']['Message'])
    s3_region = s3_event['Records'][0]['awsRegion']
    s3_event_name = s3_event['Records'][0]['eventName']
    s3_event_record = s3_event['Records'][0]['s3']
    s3_bucket_name = s3_event_record['bucket']['name']
    s3_object_name = s3_event_record['object']['key']
    s3_url = f'https://{s3_bucket_name}.s3.{s3_region}.amazonaws.com/{s3_object_name}'

    msg = {
            '@type': 'MessageCard',
            '@context':'http://schema.org/extensions',
            'themeColor': 'theme_color_normal',
            'summary': 'S3Bucket is Updated.',
            'sections': [
                {
                    'activityTitle': '<strong style="color:blue;"> S3Bucket Update Detection </strong>' 
                },
                {
                    'markdown': 'true',
                    'facts': [
                        {
                            'name': 'Event Name',
                            'value': s3_event_name
                        },
                        {
                            'name': 'URL of the Object updated',
                            'value': s3_url
                        }
                    ]
                }
            ]
    }
    encoded_msg = json.dumps(msg).encode('utf-8')
    resp = http.request('POST', url, body=encoded_msg)
