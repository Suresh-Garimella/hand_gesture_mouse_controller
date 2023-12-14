import cv2
import mediapipe
import pyautogui

camera = cv2.VideoCapture(0)
capture_hands = mediapipe.solutions.hands.Hands()
draw_options = mediapipe.solutions.drawing_utils
screen_width,screen_height = pyautogui.size()
print("screen width",screen_height,screen_height)
x1 = y1 = x2 = y2 = 0
while True:
    _,frame = camera.read()
    frame_height, frame_width , _ = frame.shape
    frame = cv2.flip(frame,1)
    rgb_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    output_hands = capture_hands.process(rgb_frame)
    all_hands = output_hands.multi_hand_landmarks
    if all_hands:
        for hand in all_hands:
            draw_options.draw_landmarks(frame,hand)
            one_hand_landmarks = hand.landmark
            for id,lm in enumerate(one_hand_landmarks):
                x = int(lm.x * frame_width)
                y = int(lm.y * frame_height)

                # print(x,y)
                # id = 12 for middle-finger
                if id == 12:
                    mouse_x = int(screen_width/frame_width*x)
                    mouse_y = int(screen_height/frame_height*(y/2))
                    cv2.circle(frame,(x,y),10,(255,255,0))
                    pyautogui.moveTo(mouse_x, mouse_y)

                # id = 8 for fore-finger
                if id == 8:
                    cv2.circle(frame,(x,y),10,(0,255,255))
                    x1 = x
                    y1 = y
                # id = 4 for thumb-finger
                if id == 4:
                    cv2.circle(frame,(x,y),10,(0,255,255))
                    x2 = x
                    y2 = y
            dist = y2 - y1
            # print(dist)
            if dist < 20:
                print("clicked")
                pyautogui.click()
    cv2.imshow("Video Capture Hand Movement", frame)

    key = cv2.waitKey(100)
    if key == 27:
        break
camera.release()
cv2.destroyAllWindows()