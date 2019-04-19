import sys
import os
import cv2 as cv
import random
import string
from detect import *
from makephoto import *

app, inputfile = sys.argv

ppi=300
target_w = int(1.5*ppi)
target_h = int(2*ppi)

def random_string_generator(str_size, allowed_chars):
    return ''.join(random.choice(allowed_chars) for x in range(str_size))

#create temp working folder
WORK_DIR="./workspace"
chars = string.ascii_letters + string.digits
size = 12
out_folder = random_string_generator(size, chars)
os.makedirs(WORK_DIR+"/"+out_folder)
os.chdir(WORK_DIR+"/"+out_folder)

image = cv.imread(sys.argv[1])
gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

#1 find face
x,y,w,h = detect_it(gray)
#print(x,y,w,h)
#cv.rectangle(image, (x,y), (x+w,y+h), (255,255,255))
#cv.imwrite("test1.jpg", image)

#2 crop photo, make sure whole upper body included
center_x = int(x+w/2)
center_y = int(y+h/2)
#increase w,h by ratio
h_w_ratio = target_h/target_w
zoom=2
w = w*zoom
h = int(w*h_w_ratio)
#adjust x,y with new w,h
x = int(center_x-w/2)
y = int(center_y-h/2)

if x < 0: x = 0
if y < 0: y = 0
height, width, channels = image.shape
if x+w > width: w = width-x
if y+h > height: h = height-y

sub_face = image[y:y+h, x:x+w]
#cv.circle(image, (center_x, center_y), 2, (0, 0, 255))
#cv.rectangle(image, (x,y), (x+w,y+h), (255,255,255))
#cv.imwrite("test2.jpg", sub_face)

#3 resize to target size
#print(x,y,target_w, target_h)
resized = cv.resize(sub_face, (target_w, target_h))
cv.imwrite("test3.jpg", resized)

#4 beautify
img = Image.open("test3.jpg")
beautified = beautify_img(img)

#5 make photo
crop_size_inch_w = target_w/ppi
crop_size_inch_h = target_h/ppi
if crop_size_inch_w <= 4:
    photo_paper_size = (4,6)
elif crop_size_inch_w > 4 and crop_size_inch_w < 8:
    photo_paper_size = (8,10)
else:
    photo_paper_size = (4,6)

out_file = random_string_generator(size, chars)
make_photo(beautified, photo_paper_size, out_file,"jpeg")

print(os.getcwd())
print("found photo: "+out_file+".jpeg")
print("Please print on photo paper size: "+str(photo_paper_size[0])+"x"+str(photo_paper_size[1]))


