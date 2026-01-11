import cv2
import mediapipe as mp
import numpy as np
import threading
import time
import queue
import json
import sounddevice as sd
from vosk import Model, KaldiRecognizer

# =========================
# CONFIGURATION
# =========================
VOSK_MODEL_PATH = "models/vosk-model-small-en-us-0.15"
SAMPLE_RATE = 16000
CAMERA_INDEX = 0
AUTO_CLOSE_DELAY = 5  # seconds

# =========================
# GLOBAL STATES
# =========================
hand_status = "UNKNOWN"
last_spoken_text = ""
door_state = "CLOSED"
door_lock = threading.Lock()

audio_queue = queue.Queue()

# =========================
# MEDIAPIPE SETUP
# =========================
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)

FINGER_TIPS = [8, 12, 16, 20]
FINGER_PIPS = [6, 10, 14, 18]

# =========================
# AUDIO CALLBACK
# =========================
def audio_callback(indata, frames, time_info, status):
    if status:
        print("Audio status:", status)
    audio_queue.put(bytes(indata))

# =========================
# DOOR CONTROL LOGIC
# =========================
def open_door_sequence():
    global door_state

    with door_lock:
        if door_state == "OPEN":
            return
        door_state = "OPEN"

    print("\n🚪 OPENING DOOR")
    print("⏱️ Door will close in 5 seconds...")

    time.sleep(AUTO_CLOSE_DELAY)

    with door_lock:
        door_state = "CLOSED"

    print("🔒 CLOSING DOOR\n")

# =========================
# SPEECH THREAD
# =========================
def speech_recognition_thread():
    global last_spoken_text

    print("Loading Vosk model...")
    model = Model(VOSK_MODEL_PATH)
    recognizer = KaldiRecognizer(model, SAMPLE_RATE)
    recognizer.SetWords(True)
    print("Vosk model loaded")

    with sd.RawInputStream(
        samplerate=SAMPLE_RATE,
        blocksize=8000,
        dtype="int16",
        channels=1,
        callback=audio_callback
    ):
        print("🎤 Listening for voice commands...")

        while True:
            data = audio_queue.get()
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get("text", "").strip()

                if text:
                    last_spoken_text = text
                    print("📝 Heard:", text)

                    if "open the door" in text.lower():
                        if hand_status == "CLOSED FIST":
                            threading.Thread(
                                target=open_door_sequence,
                                daemon=True
                            ).start()
                        else:
                            print("❌ Hand not closed — access denied")

# =========================
# CAMERA / HAND LOOP
# =========================
cap = cv2.VideoCapture(CAMERA_INDEX)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Start STT thread
threading.Thread(
    target=speech_recognition_thread,
    daemon=True
).start()

print("🖐️ Hand detection started")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:

            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            lm = []
            for point in hand_landmarks.landmark:
                lm.append((int(point.x * w), int(point.y * h)))

            xs = [p[0] for p in lm]
            ys = [p[1] for p in lm]
            x_min, x_max = min(xs), max(xs)
            y_min, y_max = min(ys), max(ys)

            cv2.rectangle(
                frame,
                (x_min - 10, y_min - 10),
                (x_max + 10, y_max + 10),
                (0, 255, 0),
                2
            )

            open_fingers = 0
            for tip, pip in zip(FINGER_TIPS, FINGER_PIPS):
                if lm[tip][1] < lm[pip][1]:
                    open_fingers += 1

            if open_fingers >= 4:
                hand_status = "OPEN HAND"
                color = (0, 255, 0)
            else:
                hand_status = "CLOSED FIST"
                color = (0, 0, 255)

            cv2.putText(
                frame,
                hand_status,
                (x_min, y_min - 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                color,
                2
            )

    # =========================
    # OVERLAY TEXT
    # =========================
    cv2.putText(
        frame,
        f"Last Command: {last_spoken_text}",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        f"Door State: {door_state}",
        (10, 60),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 255),
        2
    )

    cv2.imshow("Dharma Dwar | Vision + Voice Access", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
