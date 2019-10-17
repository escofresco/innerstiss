import time
import boto3

def transcribe(filename="transcribe-sample.mp3"):
    transcribe = boto3.client('transcribe',
                              aws_access_key_id="AKIAZCPCW36LVTOWBLZ7",
                              aws_secret_access_key="nPKczU6Gfbz/IFvCxm3TT1HNKROuMmeanigSjR6Q",
                              region_name='us-west-1')
    job_name = "test2"
    job_uri = f"https://innerstiss-audio-uploads.s3-us-west-1.amazonaws.com/{filename}"
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': job_uri},
        MediaFormat='mp3',
        LanguageCode='en-US'
    )
    while True:
        status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break
        print("Not ready yet...")
        time.sleep(5)
    print(status)


if __name__ == "__main__":
    transcribe()
