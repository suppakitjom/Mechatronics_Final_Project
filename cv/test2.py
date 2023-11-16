import cv2
from ultralytics import YOLO
import torch
import requests
# device = "cuda" if torch.cuda.is_available() else "cpu"
# Load the YOLOv8 model
model = YOLO('best-n.pt')
response = requests.get(url='http://0.0.0.0:6969/clearitems')
# Open the video file
video_path = "luggage.mp4"
cap = cv2.VideoCapture(1)

# Define a line for detection
line_x_coord = 800

# Set to keep track of unique object IDs that crossed the line
crossed_ids = set()

# Dictionary to store count of each class crossing the line
class_counts = {}

# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Run YOLOv8 tracking on the frame, persisting tracks between frames
        results = model.track(frame, persist=True,conf = 0.7)
        # Check if there are detections and the id attribute is not None
        if results[0].boxes and results[0].boxes.id is not None:
            # Get the boxes, track IDs, and class names
            boxes = results[0].boxes.xywh.cpu()
            track_ids = results[0].boxes.id.int().cpu().tolist()
            class_names = [results[0].names[i] for i in results[0].boxes.cls.int().cpu().tolist()]

            # Iterate over detected objects
            for box, track_id, class_name in zip(boxes, track_ids, class_names):
                x_center = box[0] + (box[2] / 2)  # Calculate center x-coordinate from box (x, y, w, h)

                # Check if this object has crossed the line and is not already counted
                if x_center > line_x_coord and track_id not in crossed_ids:
                    crossed_ids.add(track_id)
                    class_counts[class_name] = class_counts.get(class_name, 0) + 1
                    try:
                        r = requests.post(url='http://0.0.0.0:6969/add',json={"name": f"{class_name}"})
                    except:
                        print("Error")
                    print(f"Object ID {track_id} ({class_name}) has crossed the line.")

        # Visualize the results on the frame
        annotated_frame = results[0].plot()

        # Optionally, draw the detection line on the frame
        cv2.line(annotated_frame, (line_x_coord, 0), (line_x_coord, frame.shape[0]), (0, 255, 0), 2)

        # Display the annotated frame
        cv2.imshow("YOLOv8 Tracking", annotated_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()

# Print the final class counts
print("Final class counts of objects that crossed the line:", class_counts)
