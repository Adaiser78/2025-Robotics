import cv2
import game
import FindBalloons
import time
import numpy as np
from model import Model

Y_POS_INVULNERABILITY = 250

prev_result = False

""""
cv2 is the computer vision module being used for all sorts of vision tasks. 
Time is the standard in-built python library used for time functions. 
numpy is the numerical processing module being used for all sorts of mathematical tasks.
game is the CUSTOM BUILT module for interacting with the game screen and objects. 
FindBalloons is the CUSTOM BUILT module for image processing. 
model is the CUSTOM BUILT module for interacting with the machine learning model. 
"""

# FIXME: SPEED CAN BE A CERTAIN AMOUNT OF Y_CHANGE PERCENTAGE AND MENU OPTIONS CAN BE TEXT OR MORE COMPLICATED. INPUT.
# FIXME: High score system is extremely easy, just keep track of it in the main loop.


def close():
    game.pygame.quit()
    videoCapture.release()
    cv2.destroyAllWindows()
    quit()


Game = game.Game()

cv2.waitKey(500)

videoCapture = cv2.VideoCapture(0)


"""Calibration STUFF"""

# List to store points
points = []

ret, frame = videoCapture.read()


def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))
        # Display the point on the image
        cv2.circle(img, (x, y), 5, (0, 255, 0), -1)
        cv2.imshow('image', img)


def calibrate_frame(frame):
    frame_calibrated = cv2.warpPerspective(frame, h_matrix, (640, 480))
    return frame_calibrated

cv2.imshow('image', frame)
frame, img = videoCapture.read()

print("Setup: Press 'r' to refresh frame or press 's' to continue to calibration")

while True:
    if cv2.waitKey(0) & 0xFF == ord('r'):
        ret, img = videoCapture.read()
        cv2.imshow('image', img)
    if cv2.waitKey(0) & 0xFF == ord('s'):
        break

print("\nReady to calibrate!")
print("Select points in this order:\n1) Top Left\n2) Top Right\n3) Bottom Right\n4) Bottom Left")
cv2.setMouseCallback('image', click_event)

# Wait until a key is pressed
time.sleep(0.25)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Save the points to a file
with open('coordinates.txt', 'w') as file:
    for point in points:
        file.write(f'{point[0]}, {point[1]}\n')

# Perform calibration based on the selected points
if len(points) >= 4:
    # Assuming we want to map the selected points to a rectangle
    pts_src = np.array(points[:4], dtype=float)
    pts_dst = np.array([[0, 0], [640, 0], [640, 480], [0, 480]], dtype=float)

    # Calculate the homography matrix
    h_matrix, status = cv2.findHomography(pts_src, pts_dst)


"""Calibration STUFF"""

"""MODEL INITIALIZATION"""


model = Model()

Game.game_begin()

while not Game.quit_game:

    for event in game.pygame.event.get():  # Checks if the game window has been closed, if so exit the loop.
        if event.type == game.pygame.QUIT:
            Game.quit_game = True

    Game.step()  # Advances the game one frame.
    #  print(f"These are the x: {Game.x_pos} and y: {Game.y_pos}")  # X and Y positions of the balloon.

    ret, frame = videoCapture.read()  # Captures a frame.
    img = calibrate_frame(frame)
    print("image taken")
    #cv2.imshow("Raw Camera Feed", img)

    contours = FindBalloons.find_contours(img)       # Finds the contours.

    img = FindBalloons.draw_bounding_boxes(img, contours)  # Draws boxes around the contours.
    #cv2.imshow("Edge Detection", img)  # Displays the frame.

    # Get the cropped image of the balloon
    # "is_balloon" simply confirms that "cropped_image" is not an empty variable...This is required!
    cropped_image, is_balloon = FindBalloons.crop_objects(img, contours)  # Crops the objects detected.
    cv2.waitKey(500)
    #  filename = f'training_images/frame_{int(time.time())}.jpg'
    #  cv2.imwrite(filename, cropped_image)
    #print("main.py is running")
    #  If FindBalloons found and cropped a balloon image, show the image
    if is_balloon:
        print("image verified")
        #  filename = f'training_images/frame_{int(time.time())}.jpg'
        #  cv2.imwrite(filename, cropped_image)

        result = model.assess(cropped_image)
        print("passed to model")
        if result and (result != prev_result):
            cv2.waitKey(1500) 
            #cv2.imshow("Cropped Image", cropped_image)
            Game.pop()
            print("POPPED")
            filename = f'training_images/frame_{int(time.time())}.jpg'
            cv2.imwrite(filename, cropped_image)
        prev_result = result 

  # I WILL CHANGE NAMING LATER ON.

    if Game.restart_game:
        model = Model()
        Game = game.Game()
        Game.game_begin()

close()


