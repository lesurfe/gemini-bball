// This file will assess the shots and performance from a video and its not intended to give live feedback from a stream
// Live feedback from a stream is part of the bigger project and is left for a later stage

// Code needs to differentiate between serve, normal game and volleys
// Code needs to differentiate between play time and non play time (this will reduce analysis requirements)

import cv2
import mediapipe as mp
import numpy as np
import json
from datetime import datetime
import textwrap
import time

# Load shot data from JSON
with open('text.json', 'r') as f:
    shot_data = json.load(f)

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

// Only one file to be saved on the location, filename will be taken directly from the source

# Open the video files
process_video_path = '/Users/thorfinn/Developer/tidbit-script/final_ball.mov' // video to be assessed, in other words without any processing
display_video_path = 'final_ball.mp4' // processed video

# Open processing video (lower res)
process_cap = cv2.VideoCapture(process_video_path)
process_fps = int(process_cap.get(cv2.CAP_PROP_FPS))
process_width = int(process_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
process_height = int(process_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Open display video (higher res)
display_cap = cv2.VideoCapture(display_video_path)
display_fps = int(display_cap.get(cv2.CAP_PROP_FPS))
display_width = int(display_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
display_height = int(display_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# List to store all processed frames
processed_frames = [] // some filter can be applied to only store frames during play time

# Animation variables
last_shot_time = None
animation_duration = 1.25  # seconds (changed from 0.5 to 1.0)
current_color = (255, 255, 255)  # Start with white

def parse_timestamp(timestamp):
    # Convert timestamp (e.g., "0:07.5") to seconds
    minutes, seconds = timestamp.split(':')
    return float(minutes) * 60 + float(seconds)

def timestamp_to_frame(timestamp, fps):
    # Convert timestamp to frame number
    seconds = parse_timestamp(timestamp)
    return int(seconds * fps)

def wrap_text(text, font, scale, thickness, max_width):
    # Calculate the maximum number of characters that can fit in max_width
    words = text.split()
    lines = []
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        text_size = cv2.getTextSize(test_line, font, scale, thickness)[0]
        
        if text_size[0] <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
    
    if current_line:
        lines.append(' '.join(current_line))
    
    return lines

def get_animation_color(elapsed_time, is_made):
    if elapsed_time >= animation_duration:
        return (255, 255, 255)  # Return to white
    
    # Calculate progress through animation (0 to 1)
    progress = elapsed_time / animation_duration
    
    if progress < 0.5:
        # Fade to color
        if is_made:
            # Fade to green (BGR format)
            return (
                int(255 * (1 - progress * 2)),  # B
                255,                            # G
                int(255 * (1 - progress * 2))   # R
            )
        else:
            # Fade to red (BGR format) - keeping some green and blue for brighter red
            return (
                int(255 * (1 - progress * 2)),  # B
                int(255 * (1 - progress * 2)),  # G
                255                             # R
            )
    else:
        # Fade back to white
        if is_made:
            # Fade from green to white
            return (
                int(255 * ((progress - 0.5) * 2)),  # B
                255,                                # G
                int(255 * ((progress - 0.5) * 2))   # R
            )
        else:
            # Fade from red to white
            return (
                int(255 * ((progress - 0.5) * 2)),  # B
                int(255 * ((progress - 0.5) * 2)),  # G
                255                                 # R
            )

# Convert timestamps to frame numbers and add feedback display duration
for shot in shot_data['shots']:
    shot['frame_number'] = timestamp_to_frame(shot['timestamp_of_outcome'], process_fps)
    shot['feedback_end_frame'] = shot['frame_number'] + (4 * process_fps)  # Show feedback for 4 seconds

last_head = None
frame_count = 0
process_every_n_frames = int(process_fps / 20)  # Process at 3 fps
last_shot_result = None

print("Processing video...")

while process_cap.isOpened() and display_cap.isOpened():
    # Read frames from both videos
    process_ret, process_frame = process_cap.read()
    display_ret, display_frame = display_cap.read()
    
    if not process_ret or not display_ret:
        break

    frame_count += 1
    
    # Only process every nth frame
    if frame_count % process_every_n_frames == 0:
        # Convert the BGR image to RGB
        rgb_frame = cv2.cvtColor(process_frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb_frame)

    timestamp_of_outcome, serve, forehand, backhand, forehand_volley, backhand_volley, forehand_normal, backhand_normal, points_won, points_lost, shots_in, shots_out, winners, forced_errors, unforced_errors, feedback
    
    # Calculate current shot statistics
    serve = 0
    forehand = 0
    backhand = 0
    forehand_volley = 0
    backhand_volley = 0
    forehand_normal = 0
    backhand_normal = 0
    points_won = 0
    points_lost = 0
    serve_in = 0
    serve_out = 0
    shot_in = 0
    shout_out = 0
    winner = 0
    forced_error = 0
    unforced_error = 0
    
    current_serves = 0
    current_forehands = 0
    current_backhands = 0
    current_forehand_volleys = 0
    current_backhand_volleys = 0
    current_forehands_normal = 0
    current_backhands_normal = 0
    current_points_won = 0
    current_points_lost = 0
    current_serves_in = 0
    current_serves_out = 0
    current_shots_in = 0
    current_shouts_out = 0
    current_winners = 0
    current_forced_errors = 0
    current_unforced_errors = 0
    
    current_shots_missed = 0
    current_feedback = None
    
    for shot in shot_data['shots']:
        if shot['frame_number'] <= frame_count:
            if shot['frame_number'] == frame_count:
                # New shot detected
                last_shot_time = time.time()
                last_shot_result = shot['result']
            if shot['result'] == 'made':
                current_shots_made = shot['total_shots_made_so_far']
            else:
                current_shots_missed = shot['total_shots_missed_so_far']
            # Check if we should show feedback for this shot
            if shot['frame_number'] <= frame_count <= shot['feedback_end_frame']:
                current_feedback = shot['feedback']

    # Display shot statistics in top left
    stats_font = cv2.FONT_HERSHEY_SIMPLEX
    stats_border = (0, 0, 0)  # Black border
    stats_scale = 2.1  # Changed from 0.7 to 2.1 (3x larger)
    stats_thickness = 6  # Increased from 2 to 6
    stats_border_thickness = 12  # Increased from 4 to 12
    stats_spacing = 90  # Increased spacing for larger text
    white_color = (255, 255, 255)

    # Position for stats (top left with padding)
    stats_x = 30
    stats_y = 150  # Increased y position to account for larger text

    # Calculate animation color if needed
    if last_shot_time is not None:
        elapsed_time = time.time() - last_shot_time
        if elapsed_time < animation_duration:
            current_color = get_animation_color(elapsed_time, last_shot_result == 'made')
        else:
            current_color = white_color
            last_shot_time = None

    # Draw made shots
    made_text = f"Shots Made: {current_shots_made}"
    
    # Draw made shots with border
    cv2.putText(display_frame, made_text, 
                (stats_x, stats_y), stats_font, stats_scale, 
                stats_border, stats_border_thickness, cv2.LINE_AA)
    # Draw made shots with color
    cv2.putText(display_frame, made_text, 
                (stats_x, stats_y), stats_font, stats_scale, 
                current_color if last_shot_result == 'made' else white_color, stats_thickness, cv2.LINE_AA)
    
    # Draw missed shots
    missed_text = f"Shots Missed: {current_shots_missed}"
    
    # Draw missed shots with border
    cv2.putText(display_frame, missed_text, 
                (stats_x, stats_y + stats_spacing), stats_font, stats_scale, 
                stats_border, stats_border_thickness, cv2.LINE_AA)
    # Draw missed shots with color
    cv2.putText(display_frame, missed_text, 
                (stats_x, stats_y + stats_spacing), stats_font, stats_scale, 
                current_color if last_shot_result == 'missed' else white_color, stats_thickness, cv2.LINE_AA)

    # Display feedback if available
    if current_feedback:
        feedback_font = cv2.FONT_HERSHEY_SIMPLEX
        feedback_scale = 1.8  # Changed from 0.6 to 1.8 (3x larger)
        feedback_color = (255, 255, 255)  # White text
        feedback_border = (0, 0, 0)  # Black border
        feedback_thickness = 4  # Increased from 1 to 4
        feedback_border_thickness = 8  # Increased from 3 to 8
        feedback_spacing = 60  # Increased spacing for larger text

        # Wrap text to fit within 80% of screen width
        max_width = int(display_width * 0.8)
        wrapped_lines = wrap_text(current_feedback, feedback_font, feedback_scale, feedback_thickness, max_width)

        # Calculate total height of wrapped text
        total_height = len(wrapped_lines) * feedback_spacing
        start_y = display_height - 90 - total_height  # Increased bottom padding for larger text

        # Draw each line centered
        for i, line in enumerate(wrapped_lines):
            text_size = cv2.getTextSize(line, feedback_font, feedback_scale, feedback_thickness)[0]
            feedback_x = (display_width - text_size[0]) // 2
            feedback_y = start_y + (i * feedback_spacing)

            # Draw text with border
            cv2.putText(display_frame, line, 
                        (feedback_x, feedback_y), feedback_font, feedback_scale, 
                        feedback_border, feedback_border_thickness, cv2.LINE_AA)
            cv2.putText(display_frame, line, 
                        (feedback_x, feedback_y), feedback_font, feedback_scale, 
                        feedback_color, feedback_thickness, cv2.LINE_AA)

    # Store the processed frame
    processed_frames.append(display_frame.copy())

    # Display the frame (optional)
    cv2.imshow('Tenis Player Detection', display_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
process_cap.release()
display_cap.release()
cv2.destroyAllWindows()

print("Creating final video...")

# Create the final video at normal speed
final_output_path = 'final.mp4'
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
final_out = cv2.VideoWriter(final_output_path, fourcc, display_fps, (display_width, display_height))

# Write all frames to the final video
for frame in processed_frames:
    final_out.write(frame)

final_out.release()

print(f"Processing complete. Final video saved to {final_output_path}")

