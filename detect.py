import cv2 as cv

#detect and return x,y,w,h of face
def detect_it(image_gray):
	filterPath = "../../lbpcascade_frontalface.xml"
	faceCascade = cv.CascadeClassifier(filterPath)

	# Detect faces in the image
	faces = faceCascade.detectMultiScale(
		image_gray,
		scaleFactor=1.1,
		minNeighbors=1
	)

	print("Found {0} faces!".format(len(faces)))
	if len(faces) == 1:
		#only has 1 person in photo
		x,y,w,h = faces[0]
		return (x,y,w,h)
	else:
		return None


#for function unit test
'''
import sys
image = cv.imread(sys.argv[1])
gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
print(detect_it(gray))
'''

