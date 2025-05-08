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
try:
    while True:
        success, img = cap.read()
        if not success:
            print("Error: Failed to capture image.")
            break

        imgScaled = cv2.resize(img, (overlay_width, overlay_height))

        hands, img_with_hands = detector.findHands(imgScaled, draw=True)

        if startGame:
            if not stateResult:
                timer = time.time() - initialTime
                cv2.putText(imgBG, str(int(timer)), (400, 305), cv2.FONT_HERSHEY_PLAIN, 6, (255, 0, 255), 4)

                if timer > 3:
                    stateResult = True
                    timer = 0

                    if hands:
                        hand = hands[0]
                        fingers = detector.fingersUp(hand)
                        playerMove = None

                        if fingers == [0, 0, 0, 0, 0]:
                            playerMove = 1  # Rock
                        elif fingers == [0, 1, 1, 0, 0]:
                            playerMove = 2  # Scissors
                        elif fingers == [1, 1, 1, 1, 1]:
                            playerMove = 3  # Paper

                        aiMove = random.randint(1, 3)

                        print(f"Loading AI move image: Resources/{aiMove}.png")
                        imgAI = cv2.imread(f"Resources/{aiMove}.png", cv2.IMREAD_UNCHANGED)
                        if imgAI is None:
                            print(f"Error: Failed to load AI move image for aiMove={aiMove}.")
                        else:
                            if imgAI.shape[2] == 3:
                                imgAI = cv2.cvtColor(imgAI, cv2.COLOR_RGB2RGBA)
                            imgBG = cvzone.overlayPNG(imgBG, imgAI, (530, 100))

                        if playerMove == aiMove:
                            result = "Tie!"
                        elif (playerMove == 1 and aiMove == 2) or (playerMove == 2 and aiMove == 3) or (playerMove == 3 and aiMove == 1):
                            result = "You Win!"
                            scores[0] += 1
                        else:
                            result = "You Lose!"
                            scores[1] += 1

                        cv2.putText(imgBG, result, (400, 450), cv2.FONT_HERSHEY_PLAIN, 4, (0, 255, 0), 4)
                        cv2.putText(imgBG, f"Player: {scores[0]}  AI: {scores[1]}", (400, 550), cv2.FONT_HERSHEY_PLAIN, 4, (255, 0, 0), 4)

                        print(f"Player Move: {playerMove}")
                        print(f"AI Move: {aiMove}")
                        print(f"Result: {result}"
