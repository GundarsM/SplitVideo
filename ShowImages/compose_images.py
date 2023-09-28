import cv2
import os
import numpy as np

# files
file_1_location = '/home/gundars/Documents/yolo/tiny_yolo/Natrix/out7/'
file_2_location = '/home/gundars/Documents/yolo/tiny_yolo/Natrix/out8/'
output_folder = 'output2'

# read image file
image_name = 'frame_'

# create output location
if not os.path.isdir(output_folder):
    os.mkdir(output_folder)

first_frame_number = 1136       # input("Enter start frame :")
last_frame_number =  1304       # input("Enter start frame :")
current_frame = int(first_frame_number)

# Setting up a view window
cv2.namedWindow('composition', cv2.WINDOW_NORMAL)
cv2.resizeWindow('composition', 1200, 1000)

# process images
while current_frame <= int(last_frame_number):
    file_1_to_open = file_1_location + image_name + str(current_frame) + '.jpg'
    file_2_to_open = file_2_location + image_name + str(current_frame) + '.jpg'

    my_img_1 = cv2.imread(file_1_to_open)
    my_img_2 = cv2.imread(file_2_to_open)

    # place both images together
    comp_img = np.concatenate((my_img_1, my_img_2), axis=1)

    # get image size
    h, w, _ = comp_img.shape

    cv2.putText(comp_img, "YOLO v3", (10, 50), cv2.FONT_HERSHEY_PLAIN, 4, (0, 255, 0), 3)
    cv2.putText(comp_img, "TINY YOLO v3", (int((w / 2) + 10), 50), cv2.FONT_HERSHEY_PLAIN, 4, (0, 255, 0), 3)
    cv2.line(comp_img, (int(w/2), 0), (int(w/2), h), (255, 255, 255), 4)

    cv2.imshow('composition', comp_img,)

    # save the image
    cv2.imwrite(f'{output_folder}/out_{current_frame}.jpg', comp_img)
    current_frame += 1

    # process keyboard input
    k = cv2.waitKey(1)

    if k % 256 == 27:
        # ESC pressed
        print("ESC pressed")
        break

# clean-up
cv2.destroyAllWindows()
