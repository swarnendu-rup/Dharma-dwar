🚪✨ Dharma Dwar
🧠 Vision–Voice Based Smart Door Access System (Offline AI)

Dharma Dwar is an offline smart door access system that uses hand-gesture recognition ✋ and speech recognition 🎙️ as a two-factor authentication mechanism.
The door opens only when:

A closed fist is detected ✊

The user speaks “open the door” 🗣️

After opening, the door automatically closes after 5 seconds ⏱️.

🔒 No internet
🔑 No API keys
☁️ No cloud services
🧩 Works on low-resource devices like Raspberry Pi Zero 2 W

🧩 System Architecture (High Level)

📷 Camera → Hand Gesture Detection
🎤 Microphone → Speech-to-Text
🧠 Decision Logic → Two-Factor Authentication
🚪 Door Control → Open → Auto-Close

✋ Hand Gesture Recognition Module

Built using MediaPipe Hands 🖐️ and OpenCV 👁️

Detects 21 hand landmarks per frame

Compares:

Finger tips vs PIP joints

Gesture classification:

🟢 OPEN HAND (4+ fingers extended)

🔴 CLOSED FIST (fingers folded)

📦 Real-time bounding box + label displayed on video feed

Gesture status is continuously tracked and shared with the voice module.

🎙️ Speech-to-Text Module (Offline)

Powered by Vosk (Offline STT Engine)

Uses SoundDevice for real-time audio capture

Audio format:

16-bit PCM

16 kHz sample rate

Recognizes speech locally (no internet required)

📝 Last recognized command shown on screen

This ensures privacy, reliability, and low latency.

🔐 Authentication & Decision Logic

Access is granted only when BOTH conditions are true:

✔️ Gesture = CLOSED FIST
✔️ Voice command = “open the door”

❌ Voice without gesture → Access denied
❌ Gesture without voice → Ignored

Thread-safe logic prevents repeated or accidental triggers.

⏱️ Door Control & Timing Logic

Prints 🚪 OPENING DOOR

Starts a 5-second timer

Automatically prints 🔒 CLOSING DOOR

🧪 Currently simulated using print()
⚙️ Easily extendable to:

Servo motors

Solenoid locks

Relay modules via GPIO

🧵 Concurrency & Performance

Multi-threaded design

Main thread → Camera + gesture detection

Background thread → Speech recognition

Prevents audio blocking video

Runs smoothly on constrained hardware

📦 Required Hardware
Component	Purpose
📷 USB Camera	Hand detection
🎤 USB Microphone	Voice input
💻 Raspberry Pi / PC	Processing
🔌 Power Supply	Stable operation

(Servo/lock optional for future upgrades)

📚 Required Software & Libraries
🐍 Python Version

Python 3.9 – 3.11 recommended

📦 Python Libraries

Install all dependencies using:

pip install opencv-python mediapipe numpy sounddevice vosk

📌 Library Purpose
Library	Use
opencv-python -------------	Camera & image processing
mediapipe	------------- Hand landmark detection
numpy	------------- Math & array operations
sounddevice	------------- Microphone audio stream
vosk -------------	Offline speech recognition
json -------------	STT result parsing
threading -------------	Multi-threading
queue -------------	Audio buffering

📥 Download Vosk Model

Download a small English model:

🔗 https://alphacephei.com/vosk/models

Recommended:

vosk-model-small-en-us-0.15


Place it inside:

models/
└── vosk-model-small-en-us-0.15/

▶️ How to Run (Beginner Steps)
git clone https://github.com/yourusername/dharma-dwar.git
cd dharma-dwar
python main.py


🖐️ Show a closed fist
🗣️ Say “open the door”
🚪 Watch the system respond

Press ESC to exit.

🌟 Key Features

✅ Fully offline AI
✅ Gesture + voice security
✅ Real-time visual feedback
✅ Low RAM & CPU usage
✅ Modular & extendable
✅ Beginner-friendly code

🚀 Applications & Future Scope

🏠 Smart Homes
🔐 Secure Rooms
🤖 Robotics
♿ Assistive Tech
🧪 AI Research

🔮 Future Enhancements:

👤 Face recognition

🔊 Voice feedback

📱 Mobile dashboard

🔐 Encrypted user profiles

⚙️ Servo / lock integration

🧠 Final Note

This is not a toy project.
It is a proper embedded AI access-control system following real-world human–machine interaction principles — scaled intelligently for learning and experimentation.
