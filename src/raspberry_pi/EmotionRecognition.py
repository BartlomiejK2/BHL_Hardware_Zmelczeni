import cv2
import numpy as np
import tflite_runtime.interpreter as tflite

class EmotionRecognition:
    def __init__(self):

        # Paths to resources
        self.video_output = "output_emotions.avi"  # Output video file
        self.frame_width = 320
        self.frame_height = 240
        self.fps = 15
        self.cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"  # Haar cascade path
        self.tflite_model_path = "model.tflite"  # Replace with your .tflite model path

        # Load face detection cascade
        self.face_cascade = cv2.CascadeClassifier(self.cascade_path)
        if self.face_cascade.empty():
            raise IOError("Failed to load Haar cascade. Check your OpenCV installation.")

        # Load TensorFlow Lite model
        self.interpreter = tflite.Interpreter(model_path=self.tflite_model_path)
        self.interpreter.allocate_tensors()

        # Get input/output tensor details
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

        # Video capture and writer
        self.cap = cv2.VideoCapture(2)  # Use 0 for the default webcam (change to 2 for an external camera)
        self.cap.set(cv2.CAP_PROP_self.frame_width, self.frame_width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.frame_height)
        self.cap.set(cv2.CAP_PROP_FPS, self.fps)

        if not self.cap.isOpened():
            print("Error: Unable to access the webcam")
            exit()

        # Emotion labels (adjust based on your model's training)
        self.emotion_labels = ["Angry", "Disgust", "Fear", "Happy", "Sad", "Surprise", "Neutral"]

        print(f"Recording video to {self.video_output}... Press Ctrl+C to stop.")

    def get_emotion(self):
        
        # Capture frame from webcam
        ret, frame = self.cap.read()
        if not ret:
            print("Failed to grab a frame. Exiting...")
            return None
        
        # Convert frame to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

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
            self.interpreter.set_tensor(self.input_details[0]['index'], face_reshaped)
            self.interpreter.invoke()
            predictions = self.interpreter.get_tensor(self.output_details[0]['index'])[0]

        
            # Find the emotion with the highest score
            emotion_idx = np.argmax(predictions)
            emotion_label = self.emotion_labels[emotion_idx]

            return emotion_label
        
    def free_resources(self):
        self.cap.release()
        self.out.release()