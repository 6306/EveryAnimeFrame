import cv2
import tweepy
import requests
import os

# Set up your Twitter API credentials
consumer_key = "YOUR_CONSUMER_KEY"
consumer_secret = "YOUR_CONSUMER_SECRET"
access_token = "YOUR_ACCESS_TOKEN"
access_token_secret = "YOUR_ACCESS_TOKEN_SECRET"

# Authenticate with Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Create the Tweepy API object
api = tweepy.API(auth)

# Define the path to your video file
video_file = "PATH_TO_VIDEO_FILE"

# Create a directory to store the extracted frames
frames_folder = "PATH_TO_FRAMES_FOLDER"
if not os.path.exists(frames_folder):
    os.makedirs(frames_folder)

# Open the video file and get its properties
cap = cv2.VideoCapture(video_file)
fps = cap.get(cv2.CAP_PROP_FPS)
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
duration = frame_count / fps

# Set the frame interval (1 frame per second)
frame_interval = 5 * int(fps)

# Set the starting frame number to 0
frame_num = 0

# Loop through the video frames and extract every nth frame
while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        break

    if frame_num % frame_interval == 0:
        # Save the extracted frame to the frames folder
        frame_filename = f"frame_{frame_num}.jpg"
        cv2.imwrite(os.path.join(frames_folder, frame_filename), frame)

        # Upload the frame to Twitter
        media = api.media_upload(os.path.join(frames_folder, frame_filename))

        # Post the frame to Twitter with a caption
        caption = "Enter whatever you want to say with your frames."
        api.update_status(status=caption, media_ids=[media.media_id])

    frame_num += 1

    # Stop the loop if we have processed all the frames
    if frame_num == frame_count:
        break

# Release the video file and print some statistics
cap.release()
print(f"Extracted {frame_num} frames from the video ({duration:.2f} seconds, {fps:.2f} FPS).")
