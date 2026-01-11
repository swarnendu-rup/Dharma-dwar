# Dharma-dwar
Dharma Dwar is an offline smart door access system that combines hand-gesture recognition and speech recognition for secure authentication. Using a camera and microphone, the door opens only when a closed fist is detected and the command “open the door” is spoken, then closes automatically after 5 seconds.

System Description: Vision–Voice Based Smart Door Access System (Dharma Dwar)

The Dharma Dwar system is an offline, multi-factor intelligent door access mechanism that combines computer vision and speech recognition to authorize entry in a secure and deterministic manner. The system is designed to operate on low-resource hardware such as the Raspberry Pi Zero 2 W, without relying on cloud services or paid APIs.

The system uses a USB camera for real-time hand-gesture recognition and a USB microphone for speech-to-text processing. Access is granted only when two independent conditions are simultaneously satisfied:

The user presents a closed fist gesture, and

The user verbally issues the command “open the door.”

This dual-condition logic significantly reduces false positives and accidental activation, making the system more robust than single-input authentication methods.

Hand Gesture Recognition Module

The vision subsystem is implemented using MediaPipe Hands and OpenCV. A live video stream is captured from the camera, and 21 anatomical hand landmarks are extracted per frame. The system evaluates finger joint positions by comparing finger tip landmarks with their corresponding proximal interphalangeal (PIP) joints.

If four or more fingers are extended, the hand is classified as OPEN HAND. If the fingers are folded, the system classifies the gesture as a CLOSED FIST. A bounding box and gesture label are rendered in real time on the video feed to provide visual feedback to the user.

The gesture state is continuously tracked and shared with the voice-processing logic through a global state variable.

Speech-to-Text Processing Module

The speech recognition subsystem is powered by Vosk, an offline speech-to-text engine optimized for embedded devices. Audio is captured in real time using the SoundDevice library at a sample rate of 16 kHz, which is ideal for speech recognition accuracy while minimizing CPU and memory usage.

The recognized text is processed incrementally. When a complete phrase is detected, it is parsed to check for the presence of the command “open the door.” The final recognized sentence is displayed on the video feed for transparency and debugging purposes.

Because the speech model runs entirely offline, the system remains functional even without internet connectivity and avoids privacy risks associated with cloud-based voice processing.

Authentication and Decision Logic

The core authentication logic acts as a two-factor gate:

Factor 1: Gesture must be CLOSED FIST

Factor 2: Voice command must match “open the door”

Only when both conditions are true does the system initiate the door-opening sequence. If the voice command is detected without the correct hand gesture, access is explicitly denied.

This logic is implemented using thread-safe state management to prevent multiple triggers or race conditions.

Door Control and Timing Mechanism

Upon successful authentication, the system simulates door actuation by printing “OPENING DOOR” and starting a countdown timer. After a fixed delay of 5 seconds, the system automatically transitions the door state back to CLOSED, printing “CLOSING DOOR.”

In the current implementation, this behavior is represented using print statements. However, the design is hardware-agnostic and can be directly extended to control a servo motor or electronic lock using GPIO pins.

Concurrency and Performance Design

The system uses multi-threading to ensure smooth performance:

The camera and gesture detection run in the main thread.

The speech recognition engine runs in a background daemon thread.

This architecture prevents audio processing from blocking video rendering, ensuring real-time responsiveness even on constrained hardware.

Key Features

Fully offline operation

Dual-factor authentication (gesture + voice)

Real-time visual feedback

Low memory and CPU footprint

Modular and hardware-extensible design

No cloud dependency or API keys required

Applications and Future Scope

The Dharma Dwar system can be deployed in:

Smart homes

Secure rooms or lockers

Robotics projects

Assistive technology interfaces

AI-based access control research

Future enhancements may include face recognition, speaker feedback, gesture confidence thresholds, mobile dashboards, and encrypted user profiles.

Final Note

This system is not a gimmick—it is a correctly engineered embedded AI access control pipeline. The architecture follows real-world design principles used in industrial human–machine interaction systems, scaled intelligently for student-level hardware.
