import sys
import os
import cv2 as cv
import random
import string
from detect import *
from makephoto import *

def lazyphoto_process_main(inputfile,width,height):
    base = os.path.basename(inputfile)
    out_file = 'lazyphoto-bottomdata-com-'+os.path.splitext(base)[0]
    out_file_final = out_file+'.jpg'
    out_file_final_single = out_file+'-single.jpg'

    ppi=300
    target_w = int(width*ppi)
    target_h = int(height*ppi)

    image = cv.imread(inputfile)
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    #1 find face
    x,y,w,h = detect_it(gray,0)
    #print(x,y,w,h)
    #cv.rectangle(image, (x,y), (x+w,y+h), (255,255,255))
    #cv.imwrite("test1.jpg", image)

    #2 crop photo, make sure whole upper body included
    center_x = int(x+w/2)
    center_y = int(y+h/2)
    #increase w,h by ratio
    h_w_ratio = target_h/target_w
    zoom=1.5
    w = int(w*zoom)
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
    cv.imwrite(out_file_final_single, resized)

    #4 beautify
    img = Image.open(out_file_final_single)
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

    make_photo(beautified, photo_paper_size, out_file_final)
    dis_string = 'Print on photo paper with size: '+str(photo_paper_size[0])+"x"+str(photo_paper_size[1]) + ' inches'
    output = (out_file_final,out_file_final_single,dis_string)
    return output

#    return os.path.join(os.getcwd(), out_file)
#    print(os.getcwd())
#    print("found photo: "+out_file+".jpg")


#unit test
if __name__ == '__main__':
    print(lazyphoto_process_main(sys.argv[1],1.5,2))


