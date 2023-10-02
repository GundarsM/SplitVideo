import cv2
import os
import argparse
from datetime import datetime


def progress_bar(current, total, bar_length=20):
    fraction = current / total

    arrow = int(fraction * bar_length - 1) * '-' + '>'
    padding = int(bar_length - len(arrow)) * ' '

    ending = '\n' if current == total else '\r'

    print(f'Progress: [{arrow}{padding}] {int(fraction*100)}%', end=ending)


parser = argparse.ArgumentParser(description="add video location and frames to process")
parser.add_argument('-f', '--file', default='Natrix/nat3.mp4', required=False, help="path to input video")
parser.add_argument('-o', '--output', default='output2', required=False, help="output folder name")
parser.add_argument('-sf', '--start', default=0, required=False, help="Enter starting frame")
parser.add_argument('-ef', '--end', default=  2525, required=False, help="Enter ending frame")
parser.add_argument('-st', '--startTime', default='00:00:00', required=False, help="Enter ending frame")
parser.add_argument('-et', '--endTime', default='00:00:00', required=False, help="Enter ending frame")
args = parser.parse_args()


# define inout file
input_video = cv2.VideoCapture(args.file)
output_location = args.output

length = int(input_video.get(cv2.CAP_PROP_FRAME_COUNT))
curr_time = input_video.get(cv2.CAP_PROP_POS_MSEC)
frame_rate = input_video.get(cv2.CAP_PROP_FPS)

min_hours = int(args.startTime[0:2])
min_minutes = int(args.startTime[3:5])
min_seconds = int(args.startTime[6:8])

min_milliseconds = ((min_hours * 3600) + (min_minutes * 60) + min_seconds) * 1000

if args.endTime == max:
    max_milliseconds = length * frame_rate
else:
    max_hours = int(args.endTime[0:2])
    max_minutes = int(args.endTime[3:5])
    max_seconds = int(args.endTime[6:8])
    max_milliseconds = ((max_hours * 3600) + (max_minutes * 60) + max_seconds) * 1000

print(frame_rate*length)

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
start_frame = int(args.start)
print("Total frames in the video " + str(length))

if start_frame > 0:
    print("start from frame", end=" ")
    print(int(args.start))
    start_frame = int(args.start)
    input_video.set(cv2.CAP_PROP_POS_FRAMES, int(args.start))
elif min_milliseconds > 0:
    print("start from time", end=" ")
    print(int((min_milliseconds * frame_rate)/1000))
    start_frame = int((min_milliseconds * frame_rate)/1000)
    input_video.set(cv2.CAP_PROP_POS_FRAMES, (min_milliseconds * frame_rate)/1000)
else:
    print("start from default", end=" ")
    print(0)
    start_frame = 0
    input_video.set(cv2.CAP_PROP_POS_FRAMES, 0)

if max_milliseconds > 0:
    print("end from time", end=" ")
    print(int((max_milliseconds*frame_rate)/1000) - start_frame)
    total_frames_for_processing = int((max_milliseconds*frame_rate)/1000) - start_frame
elif int(args.end) > 0:
    print("end from frame", end=" ")
    print(int(args.end)-int(args.start))
    total_frames_for_processing = int(args.end)-int(args.start)
else:
    print("end from default", end=" ")
    print(length)
    total_frames_for_processing = length

# check or create directory for file processing
if os.path.isdir(output_location):
    print("Location exists")
else:
    print("Locations does not exist. It will be created")
    os.mkdir(output_location)

print("Start Frames ", end="")
print(start_frame)
print("Frames to be processed ", end="")
print(total_frames_for_processing)

end_frame = start_frame + total_frames_for_processing
current_frame = 0
while True:
    # process frames
    # returns tuple - if read / actual frame
    success, frame = input_video.read()
    if success:
        progress_bar(current_frame, total_frames_for_processing, 25)
        # print("for frame : " + str(frameNr) + "   timestamp is: ", str(input_video.get(cv2.CAP_PROP_POS_MSEC)))
        cv2.imwrite(f'{output_location}/frame_{start_frame}.jpg', frame)
    else:
        break
    start_frame += 1
    current_frame += 1
    if start_frame > end_frame - 1:
        break
input_video.release()

print("Done")

