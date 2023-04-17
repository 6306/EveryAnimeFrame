import tweepy
import cv2
import os
import time

# Twitter API credentials
consumer_key = "your_consumer_key_here"
consumer_secret = "your_consumer_secret_here"
access_key = "your_access_token_here"
access_secret = "your_access_secret_here"

# Authenticate to Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)

# Create API object
api = tweepy.API(auth)

# Video file name
video_file = "video.mp4"

# Folder to store frames
frames_folder = "frames_folder"

# Frame interval (in seconds)
frame_interval = 1

# Number of frames per tweet
frames_per_tweet = 4

# Get video duration and FPS
cap = cv2.VideoCapture(video_file)
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = cap.get(cv2.CAP_PROP_FPS)
duration = frame_count / fps
cap.release()

# Convert frame interval to number of frames
frame_skip = int(frame_interval * fps)

# Create frames folder
if not os.path.exists(frames_folder):
    os.makedirs(frames_folder)

# Tweet every 30 minutes
while True:
    try:
        # Remove frames from previous tweet
        files = os.listdir(frames_folder)
        for file in files:
            os.remove(os.path.join(frames_folder, file))
        
        # Capture video frames
        cap = cv2.VideoCapture(video_file)
        count = 0
        frame_index = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            count += 1
            if count % frame_skip == 0:
                frame_file = os.path.join(frames_folder, f"frame_{frame_index}.jpg")
                cv2.imwrite(frame_file, frame)
                frame_index += 1
            if frame_index == frames_per_tweet:
                break
        cap.release()

        # Upload frames and post tweet
        media_ids = []
        for i in range(frames_per_tweet):
            frame_file = os.path.join(frames_folder, f"frame_{i}.jpg")
            media = api.media_upload(frame_file)
            media_ids.append(media.media_id_string)

        tweet = "Every Frame of Azumanga Daioh!"
        tweet_with_media = api.update_status(status=tweet, media_ids=media_ids)

        print("Tweeted:", tweet)
        
        # Wait for 30 minutes before posting the next tweet
        next_tweet_time = time.time() + 30 * 60
        while time.time() < next_tweet_time:
            remaining_time = next_tweet_time - time.time()
            print(f"Next tweet in {int(remaining_time // 60)} minutes {int(remaining_time % 60)} seconds", end="\r")
            time.sleep(1)
    except tweepy.TweepError as error:
        print('Tweepy error:', error)
