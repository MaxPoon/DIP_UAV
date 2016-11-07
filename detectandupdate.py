import web, requests
import numpy as np
import cv2
import picamera

def foundFace():
	#raspistill -o image.jpg
	camera = picamera.Picamera()
	camera.capture("image.jpg")_

	# load the image
	image = cv2.imread("image.jpg")
	face_cascade = cv2.CascadeClassifier('../resources/haarcascade_frontalface_default.xml')
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	faces = face_cascade.detectMultiScale(gray, 1.3, 5)
	for (x, y, w, h) in faces:
		image = cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)
	if len(faces) >0:
		return True
	else:
		return False

def foundColor():
#raspistill -o image.jpg
	camera = picamera.Picamera()
	camera.capture("image.jpg")_

	# load the image
	image = cv2.imread("image.jpg")

	# define the list of boundaries
	boundaries = [
		([20, 20, 100], [110, 110, 255]),
		
	]

	# loop over the boundaries
	for (lower, upper) in boundaries:
		# create NumPy arrays from the boundaries
		lower = np.array(lower, dtype = "uint8")
		upper = np.array(upper, dtype = "uint8")

		# find the colors within the specified boundaries and apply
		# the mask
		mask = cv2.inRange(image, lower, upper)
		output = cv2.bitwise_and(image, image, mask = mask)

		# show the images
		cv2.imshow("images", np.hstack([image, output]))
		cv2.waitKey(0)
		# getting pixels from output
		px = output[10,10]
		RED_MIN = np.array([20, 20, 100], np.uint8)
		RED_MAX = np.array([110, 110, 255], np.uint8)

		dst = cv2.inRange(output, RED_MIN, RED_MAX)
		no_red = cv2.countNonZero(dst)
		print('The number of red pixels is: ' + str(no_red))
		if(no_red> 10000):
			return true
		

urls = (
	'/', 'index'
)

class index:
	def GET(self):
		global string
		return string
if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()
string="start"

while True:
	if foundColor():
		r = requests.post('https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyAev2Ky8pGEMl5v04YuIOEQos4m3Hl8Ge8')
		string = 'find target at longitude: '+r.json()['location']['lng']+'latitude: '+r.json()['location']['lat']
