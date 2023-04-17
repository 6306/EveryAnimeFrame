import tweepy
import cv2
import os
import time

# Set up Twitter API credentials
consumer_key = 'your_consumer_key_here'
consumer_secret = 'your_consumer_secret_here'
access_token = 'your_access_token_here'
access_secret = 'your_access_secret_here'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

# Set up video capture object
video_file = 'videoed.mp4'
cap = cv2.VideoCapture(video_file)
fps = cap.get(cv2.CAP_PROP_FPS)
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# Set up tweet parameters
tweet = "Every Frame of Azumanga Daioh!"
media_id = image

# Create frame folder if it doesn't exist
frames_folder = 'frames'
if not os.path.exists(frames_folder):
    os.makedirs(frames_folder)

# Set time delay between tweets (30 minutes)
time_delay = 1800

# Main loop
while True:
    # Capture 5 frames from the video
    for i in range(5):
        frame_number = i + 1
        frame_interval = int(fps * time_delay / 5)
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number * frame_interval)
        ret, frame = cap.read()
        if ret:
            filename = f"{frames_folder}/frame{frame_number}.jpg"
            cv2.imwrite(filename, frame)
        else:
            break

    # Construct tweet with 5 frames attached
    media_ids = []
    for i in range(1, 6):
        filename = f"{frames_folder}/frame{i}.jpg"
        res = api.media_upload(filename)
        media_ids.append(res.media_id)

    tweet_with_media = api.update_status(status=tweet, media_ids=media_ids)

    # Wait before posting again
    print("Next tweet in:")
    for i in range(time_delay, 0, -1):
        print(i)
        time.sleep(1)
    
    # Remove the frames from the previous tweet
    for i in range(1, 6):
        filename = f"{frames_folder}/frame{i}.jpg"
        os.remove(filename)
