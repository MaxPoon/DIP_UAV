import cv2
import glob

face_cascade = cv2.CascadeClassifier('resources/haarcascade_frontalface_default.xml')
images = glob.glob("images/*.jpg")
for imageName in images:
	img = cv2.imread(imageName)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray, 1.3, 5)
	if len(faces):
		print('faces:'+str(faces))
		for (x, y, w, h) in faces:
			img = cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0),2)
		cv2.imshow(imageName,img)
cv2.waitKey()
cv2.destroyAllWindows()