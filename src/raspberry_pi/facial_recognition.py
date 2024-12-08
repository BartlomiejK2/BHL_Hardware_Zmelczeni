import cv2
import numpy as np
import tflite_runtime.interpreter as tflite

# Paths to resources
video_output = "output_emotions.avi"  # Output video file
frame_width = 320
frame_height = 240
fps = 15
cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"  # Haar cascade path
tflite_model_path = "model.tflite"  # Replace with your .tflite model path

# Load face detection cascade
face_cascade = cv2.CascadeClassifier(cascade_path)
if face_cascade.empty():
    raise IOError("Failed to load Haar cascade. Check your OpenCV installation.")

# Load TensorFlow Lite model
interpreter = tflite.Interpreter(model_path=tflite_model_path)
interpreter.allocate_tensors()

# Get input/output tensor details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Video capture and writer
cap = cv2.VideoCapture(2)  # Use 0 for the default webcam (change to 2 for an external camera)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
cap.set(cv2.CAP_PROP_FPS, fps)

fourcc = cv2.VideoWriter_fourcc(*"MJPG")
out = cv2.VideoWriter(video_output, fourcc, fps, (frame_width, frame_height))

if not cap.isOpened():
    print("Error: Unable to access the webcam")
    exit()

# Emotion labels (adjust based on your model's training)
emotion_labels = ["Angry", "Disgust", "Fear", "Happy", "Sad", "Surprise", "Neutral"]

print(f"Recording video to {video_output}... Press Ctrl+C to stop.")

try:
    while True:
        # Capture frame from webcam
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab a frame. Exiting...")
            break

        # Convert frame to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            # Extract the face ROI
            face_roi = gray[y:y+h, x:x+w]

            # Preprocess the face ROI for the TFLite model
            face_resized = cv2.resize(face_roi, (64, 64))  # Resize to model input size
            face_normalized = face_resized.astype("float32") / 255.0  # Normalize pixel values
            
            # Convert grayscale to 3-channel image (duplicate the grayscale values across 3 channels)
            face_3channel = np.repeat(face_normalized[..., np.newaxis], 3, axis=-1)

            # Add batch dimension (1 sample in the batch)
            face_reshaped = np.expand_dims(face_3channel, axis=0)

            # Run inference with TensorFlow Lite
            interpreter.set_tensor(input_details[0]['index'], face_reshaped)
            interpreter.invoke()
            predictions = interpreter.get_tensor(output_details[0]['index'])[0]

           

            # Find the emotion with the highest score
            emotion_idx = np.argmax(predictions)
            emotion_label = emotion_labels[emotion_idx]

            # Draw rectangle and emotion label
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, emotion_label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)

        # Write the frame to output video
        out.write(frame)

        # Display the frame (optional)
        # cv2.imshow("Emotion Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

except KeyboardInterrupt:
    print("\nRecording stopped.")

# Release resources
cap.release()
out.release()
cv2.destroyAllWindows()
print("Video saved. Resources released.")
