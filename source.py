import tweepy
import cv2
import os
import time

# Twitter API credentials
consumer_key = "your_consumer_key"
consumer_secret = "your_consumer_secret"
access_token = "your_access_token"
access_token_secret = "your_access_token_secret"

# Authenticate with Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Open the video file
video = cv2.VideoCapture("video.mp4")

# Get the framerate of the video
fps = video.get(cv2.CAP_PROP_FPS)

# If the framerate is zero, try specifying it manually
if fps == 0:
    fps = 25  # Replace 25 with the actual framerate of the video

# Calculate the duration of the video
frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
duration = frame_count / fps

# Create a folder to store the frames
frames_folder = "frames"
if not os.path.exists(frames_folder):
    os.makedirs(frames_folder)

# Loop through the frames
for i in range(frame_count):
    # Set the current frame position
    video.set(cv2.CAP_PROP_POS_FRAMES, i)

    # Read the next frame from the video
    ret, frame = video.read()

    # If the frame was successfully read
    if ret:
        # Save the frame to a file
        filename = os.path.join(frames_folder, f"frame{i:06d}.jpg")
        cv2.imwrite(filename, frame)

        # If this is the 5th frame, post it to Twitter
        if (i + 1) % 5 == 0:
            # Wait for 30 minutes before posting the frames
            time.sleep(1800)

            # Create a tweet with the frames
            tweet = "Check out these frames from my video!"
            media = [api.media_upload(os.path.join(frames_folder, f"frame{j:06d}.jpg")) for j in range(i - 4, i + 1)]
            api.update_status(tweet, media_ids=[media_item.media_id for media_item in media])

# Release the video capture object
video.release()

# Remove the frames folder and all its contents
for file in os.listdir(frames_folder):
    os.remove(os.path.join(frames_folder, file))
os.rmdir(frames_folder)
