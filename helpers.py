import os
import requests
import time


import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
from flask import session

from app import app

load_dotenv()

def transcribe(filename):
    transcribe = boto3.client(
        'transcribe',
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name='us-west-1')
    job_name = "job14"
    job_uri = f"https://innerstiss-audio-uploads.s3-us-west-1.amazonaws.com/{filename}"
    transcribe.start_transcription_job(TranscriptionJobName=job_name,
                                       Media={'MediaFileUri': job_uri},
                                       MediaFormat='mp3',
                                       LanguageCode='en-US')
    while True:
        status = transcribe.get_transcription_job(
            TranscriptionJobName=job_name)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in [
                'COMPLETED', 'FAILED'
        ]:
            break
        print("Not ready yet...")
        time.sleep(5)
    print(status)
    return status

def upload_to_s3(filepath, filename):
    s3 = boto3.client("s3", aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"), aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"), region_name='us-west-1')
    with open(filepath, "rb") as file:
        try:
            res = s3.upload_fileobj(file, os.getenv("AWS_BUCKET_NAME"), filename)
            return res
        except ClientError as e:
            raise e


def transcript_exists(transcript_id):
    return transcript_id in session

def transcript_by_id(transcript_id):
    if transcript_exists(transcript_id):
        return {
            "transcript_title": session[transcript_id]["jobName"],
            "transcript_content": session[transcript_id]["results"]["transcripts"][0]["transcript"]
        }
    raise FileNotFoundError(f"The transcription {transcription_id} doesn't exist")

def file_is_valid(filename):
    return True

def load_json_from_uri(uri):
    return requests.get(uri).json()


#
# if __name__ == "__main__":
#     #transcribe()
#     upload_to_s3("tmp/transcribe-sample.mp3")
