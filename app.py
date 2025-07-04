import cv2
import mediapipe as mp
import time
import pyttsx3

# Voice engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)

def speak(message):
    engine.say(message)
    engine.runAndWait()

# Mediapipe setup
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

def eye_aspect_ratio(eye_landmarks, landmarks, width, height):
    v1 = landmarks[eye_landmarks[1]]
    v2 = landmarks[eye_landmarks[5]]
    v_dist = ((v1.x - v2.x)**2 + (v1.y - v2.y)**2) ** 0.5

    h1 = landmarks[eye_landmarks[0]]
    h2 = landmarks[eye_landmarks[3]]
    h_dist = ((h1.x - h2.x)**2 + (h1.y - h2.y)**2) ** 0.5

    return v_dist / h_dist

# Parameters
EAR_THRESHOLD = 0.22
CLOSED_EYE_FRAMES = 40
counter = 0
status = "Awake"

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    h, w, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = face_mesh.process(rgb_frame)

    if result.multi_face_landmarks:
        mesh_points = result.multi_face_landmarks[0].landmark

        left_ear = eye_aspect_ratio(LEFT_EYE, mesh_points, w, h)
        right_ear = eye_aspect_ratio(RIGHT_EYE, mesh_points, w, h)
        avg_ear = (left_ear + right_ear) / 2

        # Draw landmarks for visualization
        mp_drawing.draw_landmarks(
            frame,
            result.multi_face_landmarks[0],
            mp_face_mesh.FACEMESH_CONTOURS,
            mp_drawing.DrawingSpec(color=(0,255,0), thickness=1, circle_radius=1),
            mp_drawing.DrawingSpec(color=(0,0,255), thickness=1)
        )

        # Status logic
        if avg_ear < EAR_THRESHOLD:
            counter += 1
            if counter > CLOSED_EYE_FRAMES:
                if status != "Drowsy":
                    speak("Wake up! You are feeling sleepy!")
                status = "Drowsy"
        else:
            counter = 0
            status = "Awake"

        # Visual status box
        cv2.putText(frame, f"EAR: {avg_ear:.2f}", (30, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, f"Status: {status}", (30, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                    (0, 255, 0) if status == "Awake" else (0, 0, 255), 2)

    cv2.imshow("Drowsiness Detection", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
