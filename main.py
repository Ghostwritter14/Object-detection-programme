import cv2
import time
import glob
import os
from emailing import send_email
from threading import Thread

# Starting the camera
video = cv2.VideoCapture(0)
# Adding a pause time
time.sleep(1)

first_frame = None
status_list = []
count = 1


def clean_folder():
    print("clean started")
    images = glob.glob("images/*.png")
    for image in images:
        os.remove(image)
    print("clean function ended")


while True:
    status = 0
    check, frame = video.read()

    # Convert from BGR to grayscale
    grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # using gaussian blur with 21 blur value and 0 stand-dev
    grayscale_gau = cv2.GaussianBlur(grayscale, (21, 21), 0)

    if first_frame is None:
        first_frame = grayscale_gau

    delta_frame = cv2.absdiff(first_frame, grayscale_gau)

    thresh_frame = cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1]
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)
    cv2.imshow("My video", dil_frame)

    # Defining the contour for detection
    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # drawing the boundary for detection
    for contour in contours:
        if cv2.contourArea(contour) < 10000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        rectangle_detector = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
        # Send notification if an object is detected
        if rectangle_detector.any():
            status = 1
            # Counting the frames to capture the image of when the object entered
            cv2.imwrite(f"images/{count}.png", frame)
            count = count + 1
            all_images = glob.glob("images/*.png")
            # selecting the best image that captured the object
            index = int(len(all_images) / 2)
            detected_object_image = all_images[index]

    status_list.append(status)
    status_list = status_list[-2:]

    # check if the image has exited the vision radius and then send email
    if status_list[0] == 1 and status_list[1] == 0:
        # Introduced threading to reduce memory usage
        # thread1 represents sending the email and thread2 cleaning the folder after email has been sent)
        thread1 = Thread(target=send_email, args=(detected_object_image,))
        thread1.daemon = True
        thread2 = Thread(target=clean_folder)
        thread2.daemon = True

        thread1.start()

    # visualising the video
    cv2.imshow("Video", frame)

    #
    key = cv2.waitKey(1)

    # quit key for the programme
    if key == ord("q"):
        break
thread2.start()
video.release()

