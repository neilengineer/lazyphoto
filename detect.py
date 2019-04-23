import cv2 as cv

#detect and return x,y,w,h of face
def detect_it(image_gray,debug):
    if debug == 1:
        filterPath = "lbpcascade_frontalface.xml"
    else:
        filterPath = "../../lbpcascade_frontalface.xml"
    faceCascade = cv.CascadeClassifier(filterPath)

    # Detect faces in the image
    loop = 0
    scale = 2
    while loop < 5:
        print("detect time: "+str(loop))
        faces = faceCascade.detectMultiScale(
            image_gray,
            scaleFactor = scale,
            minSize = (200,200),
            minNeighbors = 1
        )
        if len(faces) != 1:
            loop += 1
            scale -= 0.2
        else:
            break;

    if debug == 1:
        ret = None
        for face in faces:
            x,y,w,h = face
            ret = cv.rectangle(image, (x,y), (x+w,y+h), (255,255,255))
        cv.imwrite("test0.jpg", ret)
    print("Found {0} faces!".format(len(faces)))
    if len(faces) == 1:
        #only has 1 person in photo
        x,y,w,h = faces[0]
        return (x,y,w,h)
    else:
        return None


#for function unit test
if __name__ == '__main__':
    import sys
    image = cv.imread(sys.argv[1])
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    print(detect_it(gray,1))
