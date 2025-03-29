import cv2
import threading
import time
import pygame
from cvzone.HandTrackingModule import HandDetector

# 🎵 Initialize Pygame mixer
pygame.mixer.init()

# Load chord sounds
chord_sounds = {
    "d_major": pygame.mixer.Sound("sounds/d_major.wav"),
    "e_minor": pygame.mixer.Sound("sounds/e_minor.wav"),
    "f_sharp_minor": pygame.mixer.Sound("sounds/f_sharp_minor.wav"),
    "g_major": pygame.mixer.Sound("sounds/g_major.wav"),
    "a_major": pygame.mixer.Sound("sounds/a_major.wav"),
}

# Map chords to each finger
chords = {
    "left": {
        "thumb": "d_major",
        "index": "e_minor",
        "middle": "f_sharp_minor",
        "ring": "g_major",
        "pinky": "a_major"
    },
    "right": {
        "thumb": "d_major",
        "index": "e_minor",
        "middle": "f_sharp_minor",
        "ring": "g_major",
        "pinky": "a_major"
    }
}

# Sustain Time (in seconds)
SUSTAIN_TIME = 2.0

# Keep track of previous finger states
prev_states = {hand: {finger: 0 for finger in chords[hand]} for hand in chords}

# Play a chord sound
def play_chord(name):
    chord_sounds[name].play()

# Stop a chord after delay (optional: fade out)
def stop_chord_after_delay(name):
    time.sleep(SUSTAIN_TIME)
    chord_sounds[name].fadeout(500)

# 🎐 Initialize camera and hand detector
cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8)

while True:
    success, img = cap.read()
    if not success:
        print("❌ Camera not capturing frames")
        continue

    hands, img = detector.findHands(img, draw=True)

    if hands:
        for hand in hands:
            hand_type = "left" if hand["type"] == "Left" else "right"
            fingers = detector.fingersUp(hand)
            finger_names = ["thumb", "index", "middle", "ring", "pinky"]

            for i, finger in enumerate(finger_names):
                if finger in chords[hand_type]:
                    chord_name = chords[hand_type][finger]
                    if fingers[i] == 1 and prev_states[hand_type][finger] == 0:
                        play_chord(chord_name)
                    elif fingers[i] == 0 and prev_states[hand_type][finger] == 1:
                        threading.Thread(target=stop_chord_after_delay, args=(chord_name,), daemon=True).start()
                    prev_states[hand_type][finger] = fingers[i]
    else:
        # No hands: stop all chords
        for hand in chords:
            for finger in chords[hand]:
                threading.Thread(target=stop_chord_after_delay, args=(chords[hand][finger],), daemon=True).start()
        prev_states = {hand: {finger: 0 for finger in chords[hand]} for hand in chords}

    cv2.imshow("Hand Tracking Piano", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()