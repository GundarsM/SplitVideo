import cv2
import os
import argparse


def progress_bar(current, total, bar_length=20):
    fraction = current / total

    arrow = int(fraction * bar_length - 1) * '-' + '>'
    padding = int(bar_length - len(arrow)) * ' '

    ending = '\n' if current == total else '\r'

    print(f'Progress: [{arrow}{padding}] {int(fraction*100)}%', end=ending)


parser = argparse.ArgumentParser(description="add video location and frames to process")
parser.add_argument('-f', '--file', default='natrix.mp4', required=False, help="path to input video")
parser.add_argument('-o', '--output', default='output', required=False, help="output folder name")
parser.add_argument('-sf', '--start', default=0, required=False, help="Enter starting frame")
parser.add_argument('-ef', '--end', default=max, required=False, help="Enter ending frame")
args = parser.parse_args()


# define inout file
input_video = cv2.VideoCapture(args.file)
output_location = args.output

length = int(input_video.get(cv2.CAP_PROP_FRAME_COUNT))

# set end
if args.end == max:
    args.end = length

# tracking frames
if args.start > args.end:
    print("Wrong order. I'll change them places")
    tmp = args.start
    args.start = args.end
    args.end = tmp

# set start and max length
frameNr = int(args.start)
print("Total frames in the video " + str(length))
input_video.set(cv2.CAP_PROP_POS_FRAMES, int(args.start))
total_frames_for_processing = int(args.end)-int(args.start)

# check or create directory for file processing
if os.path.isdir(output_location):
    print("Location exists")
else:
    print("Locations does not exist. It will be created")
    os.mkdir(output_location)

while True:
    # process frames
    # returns tuple - if read / actual frame
    success, frame = input_video.read()
    if success:
        progress_bar(frameNr-int(args.start), total_frames_for_processing, 25)
        cv2.imwrite(f'{output_location}/frame_{frameNr}.jpg', frame)
    else:
        print("Not read")
        break
    frameNr += 1
    if frameNr > int(args.end):
        break
input_video.release()

print("Done")

