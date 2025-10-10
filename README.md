# gemini-tenis

Inspiration comes from [this](https://x.com/FarzaTV/status/1928484483076087922) viral demo.

<img width="543" alt="Screenshot 2025-07-02 at 1 31 28 PM" src="https://github.com/user-attachments/assets/8d317156-f187-470c-8e26-5b7f7f60d6f2" />

First stage of the project will be based on video analysis but not in real time. Thus, starting point will be a file in .mp4 format.
Outcome of the video will be the another mp4 file with text overlayed giving feedback of each hit and an excel file with a short analysis.

'text.json' will be the file that overlays text on top of the video
'tenis.py' is mostly just an OpenCV visualizer.
'analysis.xlsx' will be the excel file with the short analysis

To make this a real time product I'll need to:

1) Smartly send frames to Gemini (Gemini Video can only handle 1 FPS)
2) Use Gemini API to return content.
3) Render it.

While developing this project I'll break it into smaller ones:

a. Starting from a mp4 file generate a new file only with its sound (wav or mp3 formats)

b. Analyze the sound files with a spectogram and identify the moments where the players hit the ball. Generate a database with moment when the ball is being hit
and the type of sound that it had (good, bad, strong, weak, etc.). ML model to analyze the sound

c. Extract short videos/frames of the before and after of each hit based on the audio analysis. Audios are simpler to analyse, by identifying the moments when the ball
was hit it reduces overal computational power demand for video analysis

d. ML model to analyze each short video/frame to classify the type of hit (serve, volley, forehand, backhand).

e. ML model to analyze each short video/frame to assess how the ball was hit and provide feedback. Feedback to be saved on 'text.json'


Additional features that can be added to the program:

i. YOLO model to track the player

ii. Hit counter for a later analysis

iii. Exercises proposed after main findings


Real time analysis will be left for a second stage where a video buffer will have to be in place as players start their hitting moves before impacting the ball
and given that those moves highly affect the outcome of the hit.
