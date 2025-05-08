import cv2
import cvzone
import time
from cvzone.HandTrackingModule import HandDetector

# Initialize video capture
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

detector = HandDetector(maxHands=1)

timer = 0
stateResult = False
startGame = False
scores = [0, 0]  # [Player, AI]

# Load background image
print("Loading background image...")
imgBG = cv2.imread("Resources/bg.png")
if imgBG is None:
    print("Error: Failed to load background image.")
    exit()

# Define overlay size and position
overlay_width, overlay_height = 320, 240
overlay_x, overlay_y = 50, 50

